#!/usr/bin/env python3
"""
分阶段 VLM 提取流水线 —— FastAPI HTTP 服务（供 Dify 工作流调用）

依赖:
    pip install openai python-dotenv fastapi uvicorn

启动服务:
    uvicorn run_two_stage_extraction:app --host 0.0.0.0 --port 8000

Dify 调用示例:
    POST /extract
    {
        "images": ["/path/to/page_1.png", "/path/to/page_2.png"],
        "pdf_name": "consensus.pdf",
        "output_dir": "./output",
        "verify": false,
        "force_strategy": null
    }

输出结构（自动取 pdf_name 无后缀名作为子目录和文件前缀）:
    {output_dir}/consensus/
    ├── consensus_1.md                ← 第 N 页提取结果
    ├── consensus_merged_output.md    ← 汇总结果
    ├── consensus_report.json         ← 运行报告
    └── extraction.log                ← 详细日志
"""

import asyncio
import base64
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DEFAULT_CONCURRENCY = 8

load_dotenv()

logger = logging.getLogger("two_stage_extraction")
logger.setLevel(logging.DEBUG)

_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(_console)

app = FastAPI(
    title="VLM 分阶段提取流水线",
    description="两阶段/三阶段 VLM 文档提取服务，供 Dify 工作流调用",
    version="1.0.0",
)


# ──────────────────── 请求 / 响应模型 ────────────────────

class ExtractionRequest(BaseModel):
    images: list[str] = Field(..., description="图片文件路径列表（服务器本地绝对路径或相对路径）")
    pdf_name: str = Field(..., description="原始 PDF 文件名（含扩展名，如 consensus.pdf），输出目录自动取其无后缀名")
    output_dir: str = Field(default="./output", description="输出根目录")
    prompt_dir: str = Field(default=".", description="提示词文件所在目录")
    model: str = Field(default="qwen3-vl-plus", description="VLM 模型名称")
    api_key: Optional[str] = Field(default=None, description="API Key（不传则读环境变量 QWEN_API_KEY）")
    base_url: Optional[str] = Field(default=None, description="API Base URL（不传则读环境变量 QWEN_BASE_URL）")
    verify: bool = Field(default=False, description="是否启用阶段3定向校验")
    force_strategy: Optional[str] = Field(
        default=None,
        description="强制使用指定策略，跳过 Scout 阶段。可选值: 轻量提取, 标准提取, 完整提取",
    )


class PageResult(BaseModel):
    page_num: int
    image_path: str
    status: str  # "ok" | "error"
    output_file: Optional[str] = None
    strategy: Optional[str] = None
    total_time_seconds: Optional[float] = None
    verify_issues: Optional[int] = None
    error: Optional[str] = None


class MergeResult(BaseModel):
    status: str
    merged_file: Optional[str] = None
    total_pages: Optional[int] = None
    effective_pages: Optional[int] = None
    skipped_pages: Optional[list[int]] = None
    error_files: Optional[list[str]] = None
    total_chars: Optional[int] = None
    error: Optional[str] = None


class ExtractionResponse(BaseModel):
    success: bool
    message: str
    pdf_name: str
    total_pages: int
    success_count: int
    fail_count: int
    per_page_results: list[PageResult]
    merge_result: Optional[MergeResult] = None


# ──────────────────── 日志 ────────────────────

def setup_task_logger(output_dir: Path) -> Path:
    """为当前任务创建独立的文件日志 handler"""
    log_file = output_dir / "extraction.log"
    _file = logging.FileHandler(log_file, encoding="utf-8")
    _file.setLevel(logging.DEBUG)
    _file.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    ))
    logger.addHandler(_file)
    return log_file


def cleanup_task_logger():
    """移除任务级别的文件 handler，避免泄漏到后续请求"""
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            h.close()
            logger.removeHandler(h)


# ──────────────────── 工具函数 ────────────────────

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_image_message(image_path: str) -> dict:
    base64_image = encode_image(image_path)
    ext = Path(image_path).suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{mime};base64,{base64_image}", "detail": "high"},
    }


async def call_vlm(messages: list, model: str, api_key: str, base_url: str, max_tokens: int = 4096) -> str:
    try:
        from openai import AsyncOpenAI
    except ImportError:
        raise RuntimeError("缺少 openai 依赖。请运行: pip install openai")

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.0,
    )
    return response.choices[0].message.content


def load_prompt(prompt_path: Path) -> str:
    if not prompt_path.exists():
        raise FileNotFoundError(f"提示词文件不存在: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def parse_scout_result(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines)
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        logger.warning(f"Scout JSON 解析失败: {e}, 原始输出前500字符:\n{raw[:500]}")
        return {"recommendation": "标准提取", "tables": {"count": 1}}


# ──────────────────── 三阶段流水线 ────────────────────

async def scout_phase(image_path: str, model: str, api_key: str, base_url: str, prompt_dir: Path) -> dict:
    logger.info("[Scout] 开始结构侦察...")
    start = time.time()

    system_prompt = load_prompt(prompt_dir / "scout_prompt.md")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [build_image_message(image_path)]},
    ]
    raw = await call_vlm(messages, model, api_key, base_url, max_tokens=512)
    elapsed = time.time() - start

    result = parse_scout_result(raw)
    logger.info(f"[Scout] 耗时 {elapsed:.2f}s, 推荐: {result.get('recommendation', '未知')}, "
                f"布局: {result.get('page_layout', '未知')}, 表格数: {result.get('tables', {}).get('count', 0)}")
    return result


async def extract_phase(
    image_path: str,
    strategy: str,
    model: str,
    api_key: str,
    base_url: str,
    prompt_dir: Path,
) -> str:
    logger.info(f"[Extract] 使用策略: {strategy} ...")
    start = time.time()

    strategy_files = {
        "轻量提取": "extract_light.md",
        "标准提取": "extract_standard.md",
        "完整提取": "prompt_v3_with_fewshot.md",
    }
    prompt_file = strategy_files.get(strategy, "extract_standard.md")
    system_prompt = load_prompt(prompt_dir / prompt_file)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [build_image_message(image_path)]},
    ]
    result = await call_vlm(messages, model, api_key, base_url, max_tokens=16384)
    elapsed = time.time() - start
    logger.info(f"[Extract] 耗时 {elapsed:.2f}s")
    return result


async def verify_phase(
    image_path: str,
    scout_result: dict,
    extract_result: str,
    model: str,
    api_key: str,
    base_url: str,
) -> dict:
    logger.info("[Verify] 开始定向校验...")
    start = time.time()

    verify_prompt = f"""你是一位医学文献校验专家。请对照原图检查下方的提取结果是否存在问题。

【页面结构信息】
{json.dumps(scout_result, ensure_ascii=False, indent=2)}

【提取结果】
{extract_result}

请仅输出以下 JSON 格式（不要 markdown 代码块）：
{{
  "issues": [
    {{"location": "问题位置", "problem": "具体问题描述", "severity": "高|中|低"}}
  ],
  "needs_re_extract": false,
  "re_extract_focus": ""
}}

检查重点：
1. Scout 报告表格下方有注释，但提取结果中是否遗漏？
2. Scout 报告有 N 个表格，提取结果中表格数量是否一致？
3. 提取结果中是否出现了 <div>、<span> 等被禁止的 HTML 标签？
4. 表格行数/列数是否与 Scout 报告的估算值严重不符？
5. 页面左下角/右下角是否有明显遗漏的段落？

如果没有发现问题，issues 留空，needs_re_extract 设为 false。"""

    messages = [
        {"role": "system", "content": "你是一位严谨的医学文献校验专家。"},
        {"role": "user", "content": [build_image_message(image_path), {"type": "text", "text": verify_prompt}]},
    ]
    raw = await call_vlm(messages, model, api_key, base_url, max_tokens=1024)
    elapsed = time.time() - start
    logger.info(f"[Verify] 耗时 {elapsed:.2f}s")

    try:
        result = parse_scout_result(raw)
    except Exception:
        result = {"issues": [], "needs_re_extract": False}

    issues = result.get("issues", [])
    if issues:
        for issue in issues:
            logger.warning(f"[Verify] [{issue.get('severity', '?')}] {issue.get('location', '?')}: {issue.get('problem', '')}")
    else:
        logger.info("[Verify] 未发现问题，提取结果可用。")

    return result


# ──────────────────── 单页处理 ────────────────────

async def process_single_page(
    image_path: str,
    page_num: int,
    pdf_name: str,
    output_dir: Path,
    model: str,
    api_key: str,
    base_url: str,
    prompt_dir: Path,
    enable_verify: bool = False,
    force_strategy: Optional[str] = None,
) -> dict:
    page_output_dir = output_dir / pdf_name
    page_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = page_output_dir / f"{pdf_name}_{page_num}.md"

    meta = {
        "page_num": page_num,
        "image_path": image_path,
        "output_file": str(output_file),
        "status": "error",
    }

    logger.info(f"\n{'='*50}")
    logger.info(f"开始处理第 {page_num} 页: {Path(image_path).name}")

    try:
        img = Path(image_path)
        if not img.exists():
            raise FileNotFoundError(f"图片不存在: {image_path}")

        total_start = time.time()

        # 阶段1: Scout
        if force_strategy:
            scout_result = {"recommendation": force_strategy, "tables": {"count": 1}}
            logger.info(f"[第{page_num}页] Scout 已跳过，强制策略: {force_strategy}")
        else:
            scout_result = await scout_phase(str(img), model, api_key, base_url, prompt_dir)

        strategy = scout_result.get("recommendation", "标准提取")
        if strategy == "轻量提取":
            # 保守修正：含表格或图片的页面不应使用轻量提取
            has_tables = scout_result.get("tables", {}).get("count", 0) > 0
            has_images = any(
                b.get("type") == "图片"
                for b in scout_result.get("content_blocks", [])
            )
            if has_tables or has_images:
                strategy = "标准提取"
                reason = "含表格" if has_tables else "含图片"
                logger.info(f"[第{page_num}页] 保守修正: 页面{reason}，策略提升为 标准提取")

        # 阶段2: Extract
        extract_result = await extract_phase(
            str(img), strategy, model, api_key, base_url, prompt_dir
        )

        # 阶段3: Verify (可选)
        verify_result = None
        if enable_verify:
            verify_result = await verify_phase(
                str(img), scout_result, extract_result, model, api_key, base_url
            )

        total_elapsed = time.time() - total_start

        frontmatter = f"""---
extraction_strategy: {strategy}
scout_result: {json.dumps(scout_result, ensure_ascii=False)}
total_time_seconds: {total_elapsed:.2f}
page_num: {page_num}
---

"""
        output_file.write_text(frontmatter + extract_result, encoding="utf-8")

        meta.update({
            "status": "ok",
            "strategy": strategy,
            "total_time_seconds": round(total_elapsed, 2),
            "verify_issues": len(verify_result.get("issues", [])) if verify_result else 0,
        })
        logger.info(f"[第{page_num}页] 完成! 耗时 {total_elapsed:.2f}s, 策略={strategy}, 结果={output_file}")

    except Exception as e:
        logger.error(f"[第{page_num}页] 处理失败: {type(e).__name__}: {e}", exc_info=True)
        meta["error"] = f"{type(e).__name__}: {e}"
        error_file = page_output_dir / f"{pdf_name}_{page_num}_error.txt"
        error_file.write_text(f"处理失败: {type(e).__name__}: {e}\n", encoding="utf-8")

    return meta


# ══════════════════════════════════════════════════════════════
#  多策略内容提取 + 多轮过程清洗流水线
# ══════════════════════════════════════════════════════════════

# ── 正文内容起始标记（VLM 输出的正文章节标题）──
BODY_CONTENT_MARKERS = [
    "## 正式提取输出",
    "## 提取结果",
    "## 正文提取",
    "### **最终输出",
    "### **第四步",
    "### **第三步：最终输出",
    "### 📄 最终提取结果",
    "### 最终提取结果",
    "### 最终输出",                          # ### 最终输出（干净数字化副本）
    "### 📤 最终输出",                       # ### 📤 最终输出（干净数字化副本）
]


def _skip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return i + 1
    return 0


def _is_reference_page(text):
    """判断是否为参考文献页（支持精确标记和分析判定两种格式）"""
    # 格式1：精确标记
    if re.search(r'（本页为参考文献，已跳过）', text):
        return True
    # 格式2：VLM分析式判定——同时包含"参考文献列表页"声明 + 整页删除结论 + 空输出
    has_ref_declaration = bool(re.search(r'[该本]页为\*\*?参考文献[列表]*[页]?\*\*', text))
    has_delete_conclusion = bool(re.search(
        r'整页.*(?:全部)?(?:删除|跳过|不输出)|'
        r'(?:全部|整页)(?:应|内容).*?(?:删除|跳过|不输出)|'
        r'纯参考文献页',
        text
    ))
    has_empty_output = bool(re.search(
        r'(?:输出)?[结果：:]*(?:（空）|空)|'
        r'不保留任何内容|'
        r'无内容输出|'
        r'无任何需保留|'
        r'不输出任何文本',
        text
    ))
    # 三条件满足2个以上即判定为参考文献页
    if sum([has_ref_declaration, has_delete_conclusion, has_empty_output]) >= 2:
        return True
    return False


def _find_body_content_marker(body):
    """查找正文起始标记，返回行号；未找到返回 -1"""
    for i, line in enumerate(body):
        stripped = line.strip()
        for marker in BODY_CONTENT_MARKERS:
            if stripped.startswith(marker):
                return i
    return -1


# ══════════════════════════════════════════════════════════════
#  多轮过程内容清除器
# ══════════════════════════════════════════════════════════════

# ── 类别 A：过程性章节标题（以 # 开头的元数据标题）──
_BLOCK_HEADER_PATTERNS = [
    # ── 结构预扫描 / 内容块定位 ──
    r'###\s*[*✅🔍📄📌📨💡🔎]*\s*整页(?:结构)?预扫描(?:结果|确认|（必须执行）|（内部完成[^）]*）|（确认无遗漏）)?',
    r'###\s*[*✅🔍]*\s*整页内容块定位',
    r'###\s*\*\*整页内容块定位',
    r'###\s*\*\*逐块处理与边界确认',
    r'####\s*\*\*第[一二三四五六七八九十\d]+块',
    r'该页包含以下内容块',
    r'\[\s*自我校验启动\s*\]',
    r'页面布局为[：:]',
    # ── 自我校验清单（所有已知变体）──
    r'###?\s*[*✅🔍]+\s*自我校验(?:清单)?(?:（[^)]*）)?$',
    r'##\s*[*✅🔍]*\s*自我校验',
    r'###\s*[*✅🔍]+\s*自我校验完成(?:（[^)]*）)?$',
    r'###\s*\*\*自我校验完成\*\*',
    r'##\s*六、自我校验',
    r'#{1,4}\s*三、自我校验',                        # ### 三、自我校验清单（全部勾选）
    # ── 提取步骤标题（非正文章节）──
    r'###\s*[*📄]*\s*按排版顺序逐块提取',
    r'###\s*[*📨]*\s*最终输出\s*[（(]',
    r'###\s*[*📌]+\s*最终修正版',
    r'##\s*提取结果\s*[（(]',
    r'##\s*正文提取\s*[（(]',
    r'###\s*[*📄]*\s*提取结果\s*[（(]',
    r'##\s*二、提取内容\s*[（(]',
    r'####\s*【左栏】',
    r'####\s*【右栏】',
    # ── 元信息 / 页眉说明 ──
    r'##\s*一、页眉与元信息',
    r'##\s*一、页面顶部信息',
    r'###\s*一、页面顶部信息',
    r'\*\*页眉信息\s*[（(]',
    # ── 核查 / 说明 / 过滤执行情况 ──
    r'##\s*四、其他说明',
    r'##\s*四、页面四角专项核查结果',
    r'##\s*五、内容过滤执行情况',
    r'###\s*三、页面四角专项检查结果',
    r'###\s*二、主内容区',
    r'###\s*四、自我校验',
    r'##\s*三、自我校验',
    r'###\s*四、内容过滤与格式处理说明',
    r'###\s*一、页面结构预扫描',
    r'###\s*页面结构预扫描结果',                       # ### 页面结构预扫描结果（确认无遗漏）：
    r'###\s*📤\s*最终输出',                             # ### 📤 最终输出（干净数字化副本）
    # ── 汇总确认行 ──
    r'^✅\s*所有内容块已覆盖[：:]',
    r'^✅\s*自我校验终检',
    r'^###\s*提取结果\s*\(干净',
    # ── 正文段落标签（VLM 输出的过程性章节标题，非正文）──
    r'###\s*正文段落\s*\(.*?\)',
    r'###\s*段落\s*\(.*?\)',
    # ── 最终输出 / 图注 / 参考文献等残留过程标题 ──
    r'#{1,3}\s*最终输出说明\s*$',
    r'##\s+二、图注[（(]',
    r'###\s+参考文献\s*$',
    r'##\s+五、自我校验清单',
]

# ── 类别 B：过程块内部行（属于某个过程块的内部内容行）──
_BLOCK_INNER_PATTERNS = [
    # 编号/加粗标题行
    r'^\d+\.\s+\*\*[^*]{2,50}\*\*[：:]\s*$',
    r'^-\s+\*\*[^*]{2,50}\*\*[：:]',
    # 区域描述行
    r'^-\s*(?:左栏|右栏)\s+\d+\s*段(?:正文)?',
    r'^-\s+表\s*\d+',
    r'^-\s+(?:页眉页脚|删除页眉|删除页脚|保留章节标题)',
    r'^-\s+无流程图(?:，无需\s*YAML)?',
    r'^-\s+表格中数值、单位、缩写',
    r'^-\s+上标引用标记',
    r'^-\s+(?:无额外文字|无文字|无遗漏文字|水印|参考文献列表|缩写)',
    # [x] 勾选项
    r'^\s*-?\s*\[[ xX☑]\]\s+',
    # ✅ 确认行（各种前缀格式）
    r'^✅\s*(?:所有内容块已覆盖|确认无遗漏|整页结构已扫描|四角检查'
             r'|自我校验完成|所有校验项通过|输出完成|输出完毕|提取完成'
             r'|页面四角检查|表格上方无|双栏结构识别正确'
             r'|表格行列核对|流程图\s*YAML|已删除|已覆盖|已完整'
             r'|数值阈值和单位完整|确认无遗漏内容块'
             r'|所有内容块均已定位并处理'
             r'|四角检查通过|表格上方段落已提取|双栏处理顺序正确)',
    r'^>\s*✅\s*(?:表格行数核对|单元格内多行内容|无HTML标签'
             r'|表格下方注释已提取|流程图已输出'
             r'|保留所有缩写原样|保留星号注释符号'
             r'|已删除|已覆盖|已完整|P2Y|保留|数值|上标|缩写)',
    # 表格式位置描述
    r'^\|\s*位置\s*\|',
    r'^-?\s*边界[：:]',
    r'^-?\s*内容为',
    # 警告/注意行
    r'^>\s*⚠?\s*注意[：:]',
    r'^-?\s*\*\*页码\*\*[：:]',
    r'^-?\s*\*\*期刊信息\*\*[：:]',
    r'^-\s+\*\*四角检查\*\*[：:]',                        # - **四角检查**：
    r'^-\s+\*\*(?:已删除|已覆盖|页眉|页脚|无流程图|表格中数值|上标引用|无额外文字|无遗漏)\*\*\s*[：:]',
    r'^-\s+(?:页眉页脚|删除页眉|删除页脚|保留章节标题|无流程图(?:，无需\s*YAML)?'
           r'|表格中数值、单位、缩写|上标引用标记'
           r'|(?:无额外文字|无文字|无遗漏文字|水印|参考文献列表|缩写))',
    # → 修正/删除行
    r'^-?\s*→\s*\*\*(?:删除|已过滤|已按规则删除)\*\*',
    r'^经四角检查与块边界确认',
    r'^现按\*\*',
    r'^已执行\*\*',
    # 块位置标签（**区域名**：... 格式）—— 扩展覆盖所有已知结构标签
    r'^\*\*(?:顶部|顶部居中|页码|页眉|期刊信息'
             r'|左上角|右上角|左上区域|右上区域'
             r'|中部偏上|中部偏下|左下角|右下角'
             r'|左栏主体|右栏主体|左栏正文|右栏正文|右栏上部|右栏中部|右栏下部'
             r'|流程图上方|流程图下方|表格上方|表格下方'
             r'|表\d*标题|表格主体|表格下方段落\d*'
             r'|右侧正文段落|表\d*下方注释'
             r'|主体上部|底部图注'
             r'|左侧路径|右侧路径)\*\*\s*[：:]',
    # 区域描述列表项（- **区域**：描述）
    r'^-\s*\*\*(?:顶部|左上区域|右上区域|中部偏下|左下角|右下角'
             r'|左栏主体|右栏主体|左栏正文|右栏正文)\*\*\s*[：:]',
    # > 说明块起始行（注意：> **注**：是表格脚注，属实质内容，不在此处删除）
    r'^>\s*\*\*说明\*\*[：:]',
    # 全文结束摘要
    r'^[（(]全文结束[）)]',
]

_BODY_SIGNAL_PATTERNS = [
    r'^##\s+表\d', r'^###\s+表\d', r'^\*\*表\d', r'^####\s+表\d', r'^#####\s+表\d',
    r'^###\s+左栏内容', r'^###\s+右栏内容',
    r'^###\s*▶\s*(?:左栏|右栏)', r'^####\s*▶\s*左栏内容',
    r'^#####\s*【流程图标题】',
    r'^##\s+图\d', r'^###\s+图\d',
    r'^##\s+(?:第[一二三四五六七八九十]+部分|前言|摘要|关键词|总[结论]|执笔|核心专家|专家组|利益冲突|参考文献)\b',
    r'^\*\*(?:第一|第二|第三|第四|第五|第六)部分',
    r'^###\s+(?:一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)',
    r'^##\s+(?:一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)',
    r'^####\s+(?:一、|二、|三、|四、|五、)',
    r'^#####?\s*【',
]

# ── 类别 C：全局逐行删除模式（Pass 0 —— 在状态机之前，全文档范围暴力清除）──
# 这些模式的匹配行无论出现在文档任何位置都会被直接删除
_GLOBAL_SWEEP_PATTERNS = [
    # ── C1: [x] 勾选列表项（自我校验清单的核心特征）──
    r'^\s*-?\s*\[[ xX☑]\]\s+.+',

    # ── C2: ✅ 确认/核查行（各种格式变体）──
    r'^>?\s*✅\s*.+',                                    # 任何以 ✅ 开头的行
    r'^>\s*✔\s*.+',                                     # ✔ 变体

    # ── C3: ⚠️ 警告/注意行 ──
    r'^>?\s*⚠\s*.+',                                   # 任何以 ⚠ 开头的行
    r'^>\s*\*\*注意\*\*[：:].*',                         # > **注意**：

    # ── C4: > 说明/解释块（含子行的多行块）──
    r'^>\s*\*\*说明\*\*[：:]',                           # > **说明**：起始行

    # ── C5: 块位置标签（**区域**： 或 **区域** : ）—— 扩展覆盖
    r'^\*\*(?:顶部|顶部居中|页码|页眉|期刊信息'
           r'|左上角|右上角|左上区域|右上区域'
           r'|中部偏上|中部偏下|左下角|右下角'
           r'|左栏主体|右栏主体|左栏正文|右栏正文|右栏上部|右栏中部|右栏下部'
           r'|流程图上方|流程图下方|表格上方|表格下方'
           r'|表\d*标题|表格主体|表格下方段落\d*'
           r'|右侧正文段落|表\d*下方注释'
           r'|主体上部|底部图注'
           r'|左侧路径|右侧路径)\* *\s*[：:]',

    # ── C6: 区域描述列表项（- **区域**：描述内容）── 扩展覆盖
    r'^-\s*\*\*(?:顶部|顶部页眉|页眉|页码|期刊信息'
           r'|左上角|右上角|左上区域|右上区域|中部偏上|中部偏下'
           r'|左下角|右下角|左栏主体|右栏主体|左栏正文|右栏正文'
           r'|右栏上部|右栏中部|右栏下部'
           r'|段落\d*|四角检查|表\d*标题|表格主体|表格下方段落\d*'
           r'|右侧正文段落|表\d*下方(?:注释)?'
           r'|主体上部|底部图注|流程图下方'
           r'|左侧路径|右侧路径|图\d+左侧|图\d+右侧'
           r'|页面四角检查)\d*[\)）]?\*\*\s*[：:]',
    # C6b: - 段落N：... / - 图N... / - 左上角：... 等（无加粗标签的描述行）
    r'^-\s+(?:段落\d*[：:]|图\d+[^\n]*[：:]'
           r'|左上角[：:]|右上角[：:]|左下角[：:]|右下角[：:]'
           r'|顶部页眉[：:])',

    # ── C7: 页面四角检查表格（管道符表格，含"左上角|页码|顶部居中|页眉"等）──
    r'^\|\s*(?:左上角|右上角|左下角|右下角|顶部居中|页眉|左栏主体|右栏主体'
           r'|左栏底部|右栏顶部|右栏中部偏下|右栏中下部|右栏底部)\s*\|',

    # ── C8: 过程性章节标题（# 开头的元数据标题，补充 _BLOCK_HEADER 未覆盖的变体）──
    r'^#{1,4}\s*[*✅🔍📄📌📨💡🔎]+\s*.+',                # 带 emoji 的 # 标题
    r'^###\s+左栏内容[：:]*$',                            # ### 左栏内容：
    r'^###\s+右栏内容[：:]*$',                            # ### 右栏内容：
    r'^###\s+左栏$',                                      # ### 左栏
    r'^###\s+右栏$',                                      # ### 右栏
    r'^####\s+左栏$',                                     # #### 左栏
    r'^####\s+右栏$',                                     # #### 右栏
    r'^##\s+左栏正文',                                    # ## 左栏正文
    r'^##\s+一、左栏内容',                                # ## 一、左栏内容

    # ── C9: 完成消息 / 数字化副本声明（各种变体）──
    r'^>?\s*输出完毕[。。]*$',                             # > 输出完毕。
    r'^>?\s*输出完毕[。].*$',                              # > 输出完毕。此为...
    r'.*数字化副本.*$.*(?:未增删|未解释|未推断|未改写)',   # ...数字化副本，未增删...
    r'^\*\*输出结束[^\n]*$',                               # **输出结束。...
    r'^如需对后续页面继续提取.*$',                         # 如需对后续页面继续提取...
    r'^,\s*严格遵循\s*v?\d[\w.]*\s*规范[。]*$',            # , 严格遵循 v3.0 规范。
    r'^>?\s*（以下为最终合规输出.*$',                      # （以下为最终合规输出...

    # ── C10: 截断/延续注释 ──
    r'^[（(]?注[）：:][^)]*[）]?\s*(?:右栏末句|原文中|此处为|前文延续|图像中被截断)',

    # ── C11: 介绍语 / 预扫描摘要 ──
    r'^以下为严格按原文排版顺序.*$',                       # 介绍语
    r'^以下为[^\n]*(?:文本提取|整页结构预扫描|严格遵循|已执行)[^\n]*$',
    r'^我将严格按照[^\n]*整页结构预扫描[^\n]*$',          # 我将严格按照...整页结构预扫描...
    r'^本页提取内容为[^\n]*数字化副本[^\n]*$',            # 本页提取内容为**原始文献的干净数字化副本**...

    # ── C12: → 箭头行（修正/说明类）──
    r'^→\s*.+$',                                          # 任何 → 开头的行
    r'^-\s*→\s*.+$',                                      # - → 开头的行

    # ── C13: 孤立的 --- 分隔线（连续的 --- 行，非 YAML 边界）──
    # 注意：不删除 YAML frontmatter 的 --- 和正文中的 ---

    # ── C14: 页面元数据行（页码、期刊信息等）──
    r'^\*\*页码\*\*[：:].*$',
    r'^\*\*期刊信息\*\*[（(].*$',

    # ── C15: VLM 提示词回显 / 介绍语 ──
    r'^我将严格按照[^\n]*$',
    r'^本提取结果为该页图像的[^\n]*数字化副本[^\n]*$',
    r'^此为该页图像的纯净数字化副本[^\n]*$',
    r'^此为[^\n]*(?:纯净|干净)?数字化副本[^\n]*$',

    # ── C16: 内容块列表标题 ──
    r'^页面可见(?:内容块|内容)及位置如下[：:]*$',
    r'^该页包含以下内容块\s*[：:]?$',

    # ── C17: 编号式结构描述项（N. **标签**：描述）──
    # 匹配 "1. **顶部页眉**：..." 等结构定位描述行
    r'^\d+\.\s+\*\*(?:顶部页眉|表\d*[\s]*标题|表格主体|表格下方段落\d*'
       r'|右栏正文|右侧正文段落|页面四角检查'
       r'|表\d*下方注释|表\d+)\*\*[：:]',

    # ── C18: 截断/推断/校验注释行 ──
    r'.*\[无法识别\].*$',
    r'.*绝对忠实图像.*不得推断.*$',
    r'.*此为图像截断导致的不完整句.*$',
    r'.*未做任何补全.*$',

    # ── C19: 最终输出说明段（标题+正文+结尾语）──
    r'^#{1,3}\s*最终输出说明\s*$',
    r'^如需继续处理后续页面.*$',
    r'^如需对后续页面继续提取.*$',
    r'^,\s*严格遵循\s*v?\d[\w.]*\s*规范[。]*$',          # already in C9 but broaden

    # ── C20: > 🔍 / > 📝 开头的说明/核查块（含子行）──
    r'^>\s*🔍\s*.+',                                      # > 🔍 任何内容
    r'^>\s*📝\s*.+',                                      # > 📝 任何内容
    r'^>\s*–\s+.+',                                       # > – 子项（en-dash）
    r'^>\s*-\s+(?:左上角|右上角|左下角|右下角|表格上方|表格下方'
       r'|表格行列|所有上标|所有数值|无任何|推荐等级|颜色提示'
       r'|无跨层|同一level|节点\s)',                       # > - 特定子项

    # ── C21: 流程图 YAML 元数据说明行 ──
    r'^>\s*-?\s*(?:所有节点|推荐等级|颜色提示|无跨层嵌套'
       r'|同一层级|同一层内|无任何概括)\s*[：:\w]',
    r'.*`content`\s*与\s*`items`.*逐字提取.*$',
    r'.*`recommendation`\s*留空.*$',
    r'.*颜色提示依据原图色块.*$',
    r'.*同一level内nodes为并列数组.*$',

    # ── C22: 参考文献清理说明 + 过程性章节标题残留 ──
    r'^>\s*删除了原文中可能存在的上标引用标记.*$',
    r'^##\s+二、图注[（(]',                             # ## 二、图注（紧接流程图...）
    r'^###\s+参考文献\s*$',                              # ### 参考文献（VLM输出结构标记）
    r'^##\s+五、自我校验清单',                           # ## 五、自我校验清单（...）

    # ── C23: 过程性 #### 子标题（修正后 / 正文 / 标题 / ▶ / 栏标签等）──
    r'^#{3,4}\s+修正后[：:]',
    r'^#{3,4}\s+正文[（(]',
    r'^#{3,4}\s+标题[（(]',
    r'^#{3,4}\s+▶\s+(?!表\d)',                         # #### ▶ 自然语言概述 / YAML结构化数据（排除表N标题）
    r'^#{2,4}\s+【最终净化版】',
    r'^#{2,4}\s+\[\s*最终净化版\s*\]',
    r'^###\s+YAML\s*流程图',
    r'^###\s+自然语言概述[（(]',
    r'^###\s+YAML\s*结构化数据',
    r'^#{3,4}\s+左栏正文[：:]\s*$',                     # #### 左栏正文：
    r'^#{3,4}\s+左栏小标题[：:]\s*$',                   # #### 左栏小标题：
    r'^#{3,4}\s+右栏正文[：:]\s*$',                     # #### 右栏正文：
    r'^#{3,4}\s+右栏小标题[：:]\s*$',                   # #### 右栏小标题：
    r'^###\s+总\s*结\s*$',                              # ### 总 结（过程段）
    r'^###\s+作者单位[（(]',
    r'^###\s+栏内容\s*$',                               # 孤立的 ### 栏内容
    r'^#{3,4}\s+图注说明[（(]',                         # 图注说明（过程标签）
    r'^#{3,4}\s+缩写释义[（(]',
    # ── C24: 流程图提取段标题 + 内联过程注释 ──
    r'^#{2,4}\s+.*流程图提取.*$',                       # ### 二、图1：流程图提取（...
    r'^#{2,4}\s+.*文本提取与YAML',                      # ## 一、流程图（图3）文本提取与YAML...
    r'^#{2,4}\s+.*YAML结构化输出.*$',                   # ...YAML结构化输出
    r'^>\s*（注：[^\n]*YAML结构化数据',                  # > （注：...YAML结构化数据）
    r'^>\s*（注：[^\n]*自然语言概述',                    # > （注：...自然语言概述
    r'.*其后附YAML结构化数据.*$',                        # ...其后附YAML结构化数据

    # ── C25: 提取步骤章节标题（一、二、三等编号 + 过程关键词）──
    r'^#{2,4}\s+[一二三四五六七八九十]、\s*(?:表格提取|正式提取内容'
       r'|主内容区|页面四角|内容过滤|格式处理|其他说明'
       r'|页眉与元信息|页面顶部信息)\b',

    # ── C26: 带括号说明的栏位/区域过程标题 ──
    # 匹配 ## 一、左栏正文（从上至下）、## 右栏正文（第五部分） 等
    r'^#{2,4}\s+(?:[一二三四五六七八九十]+、\s*)?(?:左栏正文|右栏正文'
       r'|左栏|右栏|左栏小标题|右栏小标题)\s*[（(]',

    # ── C27: 所有带尾部括号说明的 ##/### 过程标题（宽泛匹配）──
    # 排除合法内容标题（表N、图N、参考文献、摘要等），其余带（）的均为过程标记
    r'^#{2,4}\s+(?:[一二三四五六七八九十]+、\s*)?'
       r'(?!表\d|图\d|参考文献|摘要|关键词|总[结论]|执笔|核心专家'
       r'|专家组|利益冲突|通信作者|基金项目|收稿日期|引用本文|DOI'
       r'|第[一二三四五六七八九十]+部分)'
       r'.+\s*[（(][^）)]+[）)]\s*$',
]


def _is_block_header(line: str) -> bool:
    return any(re.match(p, line.strip()) for p in _BLOCK_HEADER_PATTERNS)


def _is_block_inner_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return any(re.match(p, s) for p in _BLOCK_INNER_PATTERNS)


def _is_body_signal(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return any(re.match(p, s) for p in _BODY_SIGNAL_PATTERNS)


def _looks_like_body_text(line: str) -> bool:
    s = line.strip()
    if not s or s == '---':
        return False
    if s.startswith('|') and '|' in s[1:]:
        return True
    if s.startswith('```'):
        return True
    if re.match(r'^(?:>\s*)?\*{0,2}注[：:]', s):
        return True
    if len(s) > 15 and ord(s[0]) > 0x2E80:
        _prefixes = [
            '页面', '左上角', '右上角', '左下角', '右下角',
            '确认', '注意', '⚠', '✅', '\U0001f4cc', '\U0001f50d',
            '边界', '内容为', '该页包含', '以下为严格遵循',
            '以下为对所提供', '我将严格按照',
            '经四角检查', '现按', '输出完毕', '提取完成',
            '此为原始文献', '此为该页', '此输出为',
            '（注：页眉', '（本页为',
            # 新增：更多过程性前缀
            '**页码**', '**期刊信息**', '**顶部页眉**',
            '页面可见内容', '及支[无法识别]',
            '绝对忠实图像', '图像截断', '未做任何补全',
            '数字化副本', '最终输出说明',
            '如需继续处理', '如需对后续页面',
            '删除了原文中可能存在',
            '所有节点 ', '推荐等级原文未标注',
            '颜色提示依据原图色块', '同一level内nodes',
            '无跨层嵌套', '本提取结果为该页图像',
            '此为该页图像的纯净',
        ]
        if not any(s.startswith(p) for p in _prefixes):
            return True
    if re.match(r'^[A-Z][a-z]', s) and len(s) > 25:
        return True
    if re.match(r'^(?:通信作者|Corresponding|基金项目|收稿日期|引用本文|DOI[：:])', s):
        return True
    if re.match(r'^\[\d+\]\s+[A-Z]', s):
        return True
    return False


def _strip_all_process_content(text: str) -> str:
    """
    从 VLM 输出文本中剥离所有过程分析/元数据内容。

    策略：
      Pass 0 – 全局暴力清除：逐行匹配 _GLOBAL_SWEEP_PATTERNS，命中即删
      Pass 1 – 状态机逐行扫描：处理结构性过程块（多行嵌套块）
      Pass 2 – 多行块正则删除：自我校验块、预扫描块等已知多行模式
      Pass 3 – 反向尾部扫描：从 EOF 向前截断尾部过程段
      Pass 4 – 空行归一化
    """
    # ═══ Pass 0：全局暴力逐行清除 ═══
    # 对每一行检查是否匹配任何已知过程模式，匹配则整行删除（含换行符）
    lines = text.splitlines(True)
    swept = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            swept.append(line); continue
        if any(re.match(p, stripped) for p in _GLOBAL_SWEEP_PATTERNS):
            continue  # 命中 → 跳过该行
        swept.append(line)
    text = "".join(swept)

    # ═══ Pass 1：状态机逐行扫描（处理结构性嵌套过程块）═══
    lines = text.splitlines(True)
    kept = []
    i = 0
    in_block = False

    while i < len(lines):
        s = lines[i].strip()
        if not s:
            if in_block:
                i += 1; continue
            else:
                kept.append(lines[i]); i += 1; continue

        if _is_block_header(s) or (in_block and _is_block_inner_line(s)):
            in_block = True; i += 1; continue

        if in_block:
            if _is_body_signal(s) or _looks_like_body_text(s) or s == '---':
                in_block = False; kept.append(lines[i]); i += 1; continue
            i += 1; continue

        kept.append(lines[i]); i += 1

    result = "".join(kept)

    # ═══ Pass 2：多行块正则删除（状态机可能遗漏的多行连续过程块）═══
    multi_line_blocks = [
        # 自我校验块：从标题到下一个正文信号之间的所有内容
        (
            r'\n*#{1,4}\s*[*✅🔍]*\s*自我校验(?:清单|完成)?(?:（[^)]*）)?\s*\n*'
            r'(?:[^\n]*\n*)*?'                          # 中间任意内容（非贪婪）
            r'(?=\n#{1,4}\s+(?:表\d|图\d|第[一二三四五六七八九十]+部分|参考文献'
              r'|左栏内容|右栏内容|左栏正文|右栏正文'
              r'|一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)'
              r'|\n---\n|\n\Z)'
        ),
        # 整页结构预扫描块
        (
            r'\n*#{1,4}\s*[*✅🔍📄]*\s*整页(?:结构)?预扫描[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文)|\n---\n|\n\Z)'
        ),
        # 页面四角专项核查块
        (
            r'\n*#{1,4}\s*[*✅]*\s*(?:页面四角|四角检查|四角专项)[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文)|\n---\n|\n\Z)'
        ),
        # 内容过滤执行情况块
        (
            r'\n*#{1,4}\s*[*✅]*\s*(?:内容过滤|格式处理说明|其他说明)[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文)|\n---\n|\n\Z)'
        ),
        # 提取步骤标题块（最终输出、最终修正版等）
        (
            r'\n*#{1,4}\s*[*📄📌]+\s*(?:最终(?:输出|修正版)|提取结果|提取内容)[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文|一、|二、)|\n---\n|\n\Z)'
        ),
    ]
    for pattern in multi_line_blocks:
        result = re.sub(pattern, '', result)

    # ═══ Pass 3：反向尾部扫描（截断尾部过程段）═══
    lines = result.splitlines(True)
    last_body_line = len(lines)
    i = len(lines) - 1
    trailing_process = False
    while i >= 0:
        s = lines[i].strip()
        if not s:
            if trailing_process:
                i -= 1; continue
            else:
                break
        # 检查是否为过程行（使用全部三类模式 + 全局扫描模式）
        is_process = (
            _is_block_header(s)
            or _is_block_inner_line(s)
            or any(re.match(p, s) for p in _GLOBAL_SWEEP_PATTERNS)
        )
        if is_process:
            trailing_process = True
            i -= 1; continue
        # 遇到非过程行 → 正文结尾
        last_body_line = i + 1
        break
    if trailing_process and last_body_line < len(lines):
        result = "".join(lines[:last_body_line])

    # ═══ Pass 4：空行归一化 ═══
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()



def extract_final_content(filepath: Path) -> Optional[str]:
    """
    从单个 result 文件中提取最终输出内容。
    两级策略：
      A. 查找显式正文分界标记 → 从该处提取到文件末尾
      B. 无标记时取全部 body 内容
    两种策略均由 _strip_all_process_content 统一清洗过程段。
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    body_start = _skip_frontmatter(lines)
    body = lines[body_start:]
    full_text = "".join(body).strip()

    if _is_reference_page(full_text):
        return None

    # 策略A：查找正文起始标记
    marker_idx = _find_body_content_marker(body)
    if marker_idx >= 0:
        text_to_clean = "".join(body[marker_idx:]).strip()
    else:
        # 策略B：无显式标记，取全部 body 内容由清洗器处理
        text_to_clean = full_text

    return _strip_all_process_content(text_to_clean) or None


def merge_page_results(pdf_name: str, output_dir: Path) -> dict:
    page_dir = output_dir / pdf_name
    merged_file = page_dir / f"{pdf_name}_merged_output.md"

    logger.info(f"\n{'='*50}")
    logger.info("[Merge] 开始汇总各页提取结果...")

    results = []
    skipped = []
    errors = []

    page_files = sorted(page_dir.glob(f"{pdf_name}_*.md"))
    page_files = [f for f in page_files
                  if not f.name.endswith("_merged_output.md")
                  and not f.name.endswith("_error.txt")]

    if not page_files:
        logger.warning("[Merge] 未找到任何单页提取结果文件")
        return {"status": "no_results", "merged_file": str(merged_file)}

    for pf in page_files:
        try:
            stem = pf.stem
            page_num_str = stem.rsplit("_", 1)[-1]
            page_num = int(page_num_str)

            content = extract_final_content(pf)
            if content is None:
                skipped.append(page_num)
                logger.info(f"[Merge] 第 {page_num} 页 → 参考文献页，跳过")
            elif content:
                results.append((page_num, content))
                logger.info(f"[Merge] 第 {page_num} 页 → 提取 {len(content)} 字符")
            else:
                logger.warning(f"[Merge] 第 {page_num} 页 → 未提取到有效内容")
        except Exception as e:
            logger.error(f"[Merge] 处理文件 {pf.name} 时出错: {e}", exc_info=True)
            errors.append(pf.name)

    results.sort(key=lambda x: x[0])

    with open(merged_file, "w", encoding="utf-8") as f:
        f.write(f"# {pdf_name} —— 提取结果汇总\n\n")
        f.write(f"> 由 VLM 分阶段提取流水线自动生成，共处理 {len(page_files)} 页。\n\n")
        f.write("---\n\n")

        for page_num, content in results:
            f.write(f"<!-- ===== 第 {page_num} 页 ===== -->\n\n")
            f.write(content)
            f.write("\n\n")

        if skipped:
            f.write(f"\n<!-- 备注：第 {skipped} 页为参考文献，已跳过 -->\n")

    total_chars = sum(len(c) for _, c in results)
    merge_meta = {
        "status": "ok",
        "merged_file": str(merged_file),
        "total_pages": len(page_files),
        "effective_pages": len(results),
        "skipped_pages": skipped,
        "error_files": errors,
        "total_chars": total_chars,
    }

    logger.info(f"[Merge] 汇总完成!")
    logger.info(f"  合并文件: {merged_file}")
    logger.info(f"  有效页面: {len(results)} / {len(page_files)}")
    logger.info(f"  跳过页面（参考文献）: {skipped}")
    logger.info(f"  总字符数: {total_chars}")

    return merge_meta


# ──────────────────── API 端点 ────────────────────

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "service": "vlm-extraction"}


@app.post("/extract", response_model=ExtractionResponse)
async def extract(req: ExtractionRequest):
    """
    执行分阶段 VLM 提取。

    接收图片路径列表，逐页执行 Scout → Extract → Verify 流水线，
    最后汇总所有页面结果并返回报告。
    """
    # ── 参数解析与校验 ──
    api_key = req.api_key or os.getenv("QWEN_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="未提供 API Key。请在请求体中传入 api_key 或设置环境变量 QWEN_API_KEY")

    base_url = req.base_url or os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

    if not req.images or len(req.images) == 0:
        raise HTTPException(status_code=400, detail="images 不能为空，需提供至少一个图片路径")

    valid_strategies = ["轻量提取", "标准提取", "完整提取"]
    if req.force_strategy and req.force_strategy not in valid_strategies:
        raise HTTPException(
            status_code=400,
            detail=f"force_strategy 无效，可选值: {valid_strategies}",
        )

    prompt_dir = Path(req.prompt_dir)
    output_dir = Path(req.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 从含扩展名的 pdf_name 提取无后缀名，用作输出目录和文件前缀
    pdf_stem = Path(req.pdf_name).stem

    # 任务目录：{output_dir}/{pdf_stem}/
    task_output_dir = output_dir / pdf_stem
    task_output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化本次任务的日志
    log_file = setup_task_logger(task_output_dir)

    logger.info(f"{'='*60}")
    logger.info(f"VLM 分阶段提取流水线 — 新任务")
    logger.info(f"  PDF 文件名: {req.pdf_name}")
    logger.info(f"  输出目录前缀: {pdf_stem}")
    logger.info(f"  图片数量: {len(req.images)}")
    logger.info(f"  输出目录: {task_output_dir}")
    logger.info(f"  模型: {req.model}")
    logger.info(f"  校验模式: {'开启' if req.verify else '关闭'}")
    logger.info(f"{'='*60}")

    # ── 并发逐页处理（Semaphore 控制并发数）──
    semaphore = asyncio.Semaphore(DEFAULT_CONCURRENCY)

    async def _process_with_semaphore(idx: int, image_path: str) -> dict:
        async with semaphore:
            try:
                return await process_single_page(
                    image_path=image_path,
                    page_num=idx,
                    pdf_name=pdf_stem,
                    output_dir=output_dir,
                    model=req.model,
                    api_key=api_key,
                    base_url=base_url,
                    prompt_dir=prompt_dir,
                    enable_verify=req.verify,
                    force_strategy=req.force_strategy,
                )
            except Exception as e:
                logger.error(f"[第{idx}页] 未捕获异常: {type(e).__name__}: {e}", exc_info=True)
                return {
                    "page_num": idx,
                    "image_path": image_path,
                    "status": "error",
                    "error": f"{type(e).__name__}: {e}",
                }

    tasks = [_process_with_semaphore(idx, img) for idx, img in enumerate(req.images, start=1)]
    all_results = await asyncio.gather(*tasks)

    success_count = sum(1 for r in all_results if r["status"] == "ok")
    fail_count = sum(1 for r in all_results if r["status"] != "ok")

    # ── 汇总 ──
    merge_meta = None
    if success_count > 0:
        try:
            merge_meta = merge_page_results(pdf_stem, output_dir)
        except Exception as e:
            logger.error(f"[汇总] 合并过程出错: {type(e).__name__}: {e}", exc_info=True)
            merge_meta = {"status": "error", "error": f"{type(e).__name__}: {e}"}

    # ── 写入运行报告 ──
    final_report = {
        "pdf_name": req.pdf_name,
        "pdf_stem": pdf_stem,
        "total_pages": len(req.images),
        "success_count": success_count,
        "fail_count": fail_count,
        "per_page_results": all_results,
        "merge_result": merge_meta,
    }
    report_file = task_output_dir / f"{pdf_stem}_report.json"
    report_file.write_text(json.dumps(final_report, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"\n{'='*60}")
    logger.info(f"全部处理完成!")
    logger.info(f"  总页数: {len(req.images)}, 成功: {success_count}, 失败: {fail_count}")
    logger.info(f"  单页结果目录: {task_output_dir}")
    if merge_meta and merge_meta.get("status") == "ok":
        logger.info(f"  汇总文件: {merge_meta['merged_file']}")
    logger.info(f"  运行报告: {report_file}")
    logger.info(f"  日志文件: {log_file}")
    logger.info(f"{'='*60}")

    cleanup_task_logger()

    return ExtractionResponse(
        success=fail_count == 0,
        message=f"处理完成: {success_count}/{len(req.images)} 页成功" +
                (f"，{fail_count} 页失败" if fail_count else ""),
        pdf_name=req.pdf_name,
        total_pages=len(req.images),
        success_count=success_count,
        fail_count=fail_count,
        per_page_results=[PageResult(**r) for r in all_results],
        merge_result=MergeResult(**merge_meta) if merge_meta else None,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="run_two_stage_extraction:app", host="0.0.0.0", port=8000, reload=True)
