"""
VLM 分阶段提取流水线 —— 共享工具模块

提供两个服务共用的：
  - VLM 调用封装（OpenAI 兼容接口）
  - 图片编解码
  - Scout / Extract / Verify 三阶段流水线核心逻辑
  - 多轮过程内容清洗器（Pass 0~4）
  - 合并与最终内容提取
  - 通用数据模型
"""

import asyncio
import base64
import json
import logging
import re
import time
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger("two_stage_extraction")

DEFAULT_CONCURRENCY = 8


# ──────────────────── 通用数据模型 ────────────────────

class TaskStatus(str):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExtractionTaskInfo(BaseModel):
    task_id: str = Field(..., description="唯一任务ID")
    image_filename: str = Field(..., description="原始图片文件名")
    image_path: str = Field(..., description="图片文件完整路径")
    output_file: Optional[str] = Field(None, description="提取结果输出Markdown文件全路径")
    status: str = Field(default=TaskStatus.PENDING, description="当前状态: pending/processing/completed/failed")
    success: Optional[bool] = Field(None, description="完成后成功或失败状态")
    error: Optional[str] = Field(None, description="错误信息")
    elapsed_time: Optional[float] = Field(None, description="总体提取耗时(秒)")
    strategy: Optional[str] = Field(None, description="使用的提取策略")
    pdf_name: str = Field(..., description="所属PDF名称(无后缀)")
    page_num: int = Field(..., description="页码")


class PageMergeDetail(BaseModel):
    page_num: int = Field(..., description="页码")
    image_filename: str = Field(..., description="原始图片文件名")
    output_file: str = Field(..., description="单页提取结果Markdown路径")
    status: str = Field(..., description="提取状态")
    success: bool = Field(..., description="是否成功")
    chars_before_clean: Optional[int] = Field(None, description="清洗前字符数")
    chars_after_clean: Optional[int] = Field(None, description="清洗后字符数")


class MergeTaskInfo(BaseModel):
    merge_id: str = Field(..., description="合并任务唯一ID")
    task_ids: list[str] = Field(..., description="关联的提取任务ID列表")
    pdf_name: str = Field(..., description="PDF名称(无后缀)")
    output_dir: str = Field(..., description="输出目录")
    status: str = Field(default=TaskStatus.PENDING, description="当前状态: pending/polling/merging/completed/failed")

    # 轮询阶段
    total_tasks: Optional[int] = Field(None, description="总任务数")
    completed_tasks: Optional[int] = Field(None, description="已完成任务数")
    poll_elapsed_seconds: Optional[float] = Field(None, description="轮询耗时(秒)")

    # 合并清洗阶段
    merged_file: Optional[str] = Field(None, description="最终合并文件完整路径")
    effective_pages: Optional[int] = Field(None, description="有效内容页面数")
    skipped_pages: Optional[list[int]] = Field(None, description="跳过的页码列表(参考文献等)")
    total_chars: Optional[int] = Field(None, description="合并后总字符数")
    merge_elapsed_seconds: Optional[float] = Field(None, description="合并清洗耗时(秒)")

    # 逐页明细
    page_details: Optional[list[PageMergeDetail]] = Field(None, description="逐页处理明细")

    error: Optional[str] = Field(None, description="错误信息")


# ──────────────────── VLM 调用 ────────────────────
# 图片base64编码，方便大模型model 读取
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

# ────────────────────  Scout ────────────────────
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

# ──────────────────── 提取 ────────────────────
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


# ══════════════════════════════════════════════════════════════
#  多轮过程内容清除器（从原代码完整迁移）
# ══════════════════════════════════════════════════════════════

BODY_CONTENT_MARKERS = [
    "## 正式提取输出",
    "## 提取结果",
    "## 正文提取",
    "### **最终输出",
    "### **第四步",
    "### **第三步：最终输出",
    "### 📄 最终提取结果",
    "### 最终提取结果",
    "### 最终输出",
    "### 📤 最终输出",
]


def _skip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return i + 1
    return 0


def _is_reference_page(text):
    if re.search(r'（本页为参考文献，已跳过）', text):
        return True
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
    if sum([has_ref_declaration, has_delete_conclusion, has_empty_output]) >= 2:
        return True
    return False


def _find_body_content_marker(body):
    for i, line in enumerate(body):
        stripped = line.strip()
        for marker in BODY_CONTENT_MARKERS:
            if stripped.startswith(marker):
                return i
    return -1


_BLOCK_HEADER_PATTERNS = [
    r'###\s*[*✅🔍📄📌📨💡🔎]*\s*整页(?:结构)?预扫描(?:结果|确认|（必须执行）|（内部完成[^）]*）|（确认无遗漏）)?',
    r'###\s*[*✅🔍]*\s*整页内容块定位',
    r'###\s*\*\*整页内容块定位',
    r'###\s*\*\*逐块处理与边界确认',
    r'####\s*\*\*第[一二三四五六七八九十\d]+块',
    r'该页包含以下内容块',
    r'\[\s*自我校验启动\s*\]',
    r'页面布局为[：:]',
    r'###?\s*[*✅🔍]+\s*自我校验(?:清单)?(?:（[^)]*）)?$',
    r'##\s*[*✅🔍]*\s*自我校验',
    r'###\s*[*✅🔍]+\s*自我校验完成(?:（[^)]*）)?$',
    r'###\s*\*\*自我校验完成\*\*',
    r'##\s*六、自我校验',
    r'#{1,4}\s*三、自我校验',
    r'###\s*[*📄]*\s*按排版顺序逐块提取',
    r'###\s*[*📨]*\s*最终输出\s*[（(]',
    r'###\s*[*📌]+\s*最终修正版',
    r'##\s*提取结果\s*[（(]',
    r'##\s*正文提取\s*[（(]',
    r'###\s*[*📄]*\s*提取结果\s*[（(]',
    r'##\s*二、提取内容\s*[（(]',
    r'####\s*【左栏】',
    r'####\s*【右栏】',
    r'##\s*一、页眉与元信息',
    r'##\s*一、页面顶部信息',
    r'###\s*一、页面顶部信息',
    r'\*\*页眉信息\s*[（(]',
    r'##\s*四、其他说明',
    r'##\s*四、页面四角专项核查结果',
    r'##\s*五、内容过滤执行情况',
    r'###\s*三、页面四角专项检查结果',
    r'###\s*二、主内容区',
    r'###\s*四、自我校验',
    r'##\s*三、自我校验',
    r'###\s*四、内容过滤与格式处理说明',
    r'###\s*一、页面结构预扫描',
    r'###\s*页面结构预扫描结果',
    r'###\s*📤\s*最终输出',
    r'^✅\s*所有内容块已覆盖[：:]',
    r'^✅\s*自我校验终检',
    r'^###\s*提取结果\s*\(干净',
    r'###\s*正文段落\s*\(.*?\)',
    r'###\s*段落\s*\(.*?\)',
    r'#{1,3}\s*最终输出说明\s*$',
    r'##\s+二、图注[（(]',
    r'###\s+参考文献\s*$',
    r'##\s+五、自我校验清单',
]

_BLOCK_INNER_PATTERNS = [
    r'^\d+\.\s+\*\*[^*]{2,50}\*\*[：:]\s*$',
    r'^-\s+\*\*[^*]{2,50}\*\*[：:]',
    r'^-\s*(?:左栏|右栏)\s+\d+\s*段(?:正文)?',
    r'^-\s+表\s*\d+',
    r'^-\s+(?:页眉页脚|删除页眉|删除页脚|保留章节标题)',
    r'^-\s+无流程图(?:，无需\s*YAML)?',
    r'^-\s+表格中数值、单位、缩写',
    r'^-\s+上标引用标记',
    r'^-\s+(?:无额外文字|无文字|无遗漏文字|水印|参考文献列表|缩写)',
    r'^\s*-?\s*\[[ xX☑]\]\s+',
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
    r'^\|\s*位置\s*\|',
    r'^-?\s*边界[：:]',
    r'^-?\s*内容为',
    r'^>\s*⚠?\s*注意[：:]',
    r'^-?\s*\*\*页码\*\*[：:]',
    r'^-?\s*\*\*期刊信息\*\*[：:]',
    r'^-\s+\*\*四角检查\*\*[：:]',
    r'^-\s+\*\*(?:已删除|已覆盖|页眉|页脚|无流程图|表格中数值|上标引用|无额外文字|无遗漏)\*\*\s*[：:]',
    r'^-\s+(?:页眉页脚|删除页眉|删除页脚|保留章节标题|无流程图(?:，无需\s*YAML)?'
           r'|表格中数值、单位、缩写|上标引用标记'
           r'|(?:无额外文字|无文字|无遗漏文字|水印|参考文献列表|缩写))',
    r'^-?\s*→\s*\*\*(?:删除|已过滤|已按规则删除)\*\*',
    r'经四角检查与块边界确认',
    r'现按\*\*',
    r'已执行\*\*',
    r'^\*\*(?:顶部|顶部居中|页码|页眉|期刊信息'
             r'|左上角|右上角|左上区域|右上区域'
             r'|中部偏上|中部偏下|左下角|右下角'
             r'|左栏主体|右栏主体|左栏正文|右栏正文|右栏上部|右栏中部|右栏下部'
             r'|流程图上方|流程图下方|表格上方|表格下方'
             r'|表\d*标题|表格主体|表格下方段落\d*'
             r'|右侧正文段落|表\d*下方注释'
             r'|主体上部|底部图注'
             r'|左侧路径|右侧路径)\*\*\s*[：:]',
    r'^-\s*\*\*(?:顶部|左上区域|右上区域|中部偏下|左下角|右下角'
             r'|左栏主体|右栏主体|左栏正文|右栏正文)\*\*\s*[：:]',
    r'^>\s*\*\*说明\*\*[：:]',
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

_GLOBAL_SWEEP_PATTERNS = [
    r'^\s*-?\s*\[[ xX☑]\]\s+.+',
    r'^>?\s*✅\s*.+',
    r'^>\s*✔\s*.+',
    r'^>?\s*⚠\s*.+',
    r'^>\s*\*\*注意\*\*[：:].*',
    r'^>\s*\*\*说明\*\*[：:]',
    r'^\*\*(?:顶部|顶部居中|页码|页眉|期刊信息'
           r'|左上角|右上角|左上区域|右上区域'
           r'|中部偏上|中部偏下|左下角|右下角'
           r'|左栏主体|右栏主体|左栏正文|右栏正文|右栏上部|右栏中部|右栏下部'
           r'|流程图上方|流程图下方|表格上方|表格下方'
           r'|表\d*标题|表格主体|表格下方段落\d*'
           r'|右侧正文段落|表\d*下方注释'
           r'|主体上部|底部图注'
           r'|左侧路径|右侧路径)\* *\s*[：:]',
    r'^-\s*\*\*(?:顶部|顶部页眉|页眉|页码|期刊信息'
           r'|左上角|右上角|左上区域|右上区域|中部偏上|中部偏下'
           r'|左下角|右下角|左栏主体|右栏主体|左栏正文|右栏正文'
           r'|右栏上部|右栏中部|右栏下部'
           r'|段落\d*|四角检查|表\d*标题|表格主体|表格下方段落\d*'
           r'|右侧正文段落|表\d*下方(?:注释)?'
           r'|主体上部|底部图注|流程图下方'
           r'|左侧路径|右侧路径|图\d+左侧|图\d+右侧'
           r'|页面四角检查)\d*[\)）]?\*\*\s*[：:]',
    r'^-\s+(?:段落\d*[：:]|图\d+[^\n]*[：:]'
           r'|左上角[：:]|右上角[：:]|左下角[：:]|右下角[：:]'
           r'|顶部页眉[：:])',
    r'^\|\s*(?:左上角|右上角|左下角|右下角|顶部居中|页眉|左栏主体|右栏主体'
           r'|左栏底部|右栏顶部|右栏中部偏下|右栏中下部|右栏底部)\s*\|',
    r'^#{1,4}\s*[*✅🔍📄📌📨💡🔎]+\s*.+',
    r'^###\s+左栏内容[：:]*$',
    r'^###\s+右栏内容[：:]*$',
    r'^###\s+左栏$',
    r'^###\s+右栏$',
    r'^####\s+左栏$',
    r'^####\s+右栏$',
    r'^##\s+左栏正文',
    r'^##\s+一、左栏内容',
    r'^>?\s*输出完毕[。。]*$',
    r'^>?\s*输出完毕[。].*$',
    r'.*数字化副本.*$.*(?:未增删|未解释|未推断|未改写)',
    r'^\*\*输出结束[^\n]*$',
    r'^如需对后续页面继续提取.*$',
    r',\s*严格遵循\s*v?\d[\w.]*\s*规范[。]*$',
    r'^>?\s*（以下为最终合规输出.*$',
    r'^[（(]?注[）：:][^)]*[）]?\s*(?:右栏末句|原文中|此处为|前文延续|图像中被截断)',
    r'^以下为严格按原文排版顺序.*$',
    r'^以下为[^\n]*(?:文本提取|整页结构预扫描|严格遵循|已执行)[^\n]*$',
    r'^我将严格按照[^\n]*整页结构预扫描[^\n]*$',
    r'^本页提取内容为[^\n]*数字化副本[^\n]*$',
    r'^→\s*.+$',
    r'^-\s*→\s*.+$',
    r'^\*\*页码\*\*[：:].*$',
    r'^\*\*期刊信息\*\*[（(].*$',
    r'^我将严格按照[^\n]*$',
    r'^本提取结果为该页图像的[^\n]*数字化副本[^\n]*$',
    r'^此为该页图像的纯净数字化副本[^\n]*$',
    r'^此为[^\n]*(?:纯净|干净)?数字化副本[^\n]*$',
    r'^页面可见(?:内容块|内容)及位置如下[：:]*$',
    r'^该页包含以下内容块\s*[：:]?$',
    r'^\d+\.\s+\*\*(?:顶部页眉|表\d*[\s]*标题|表格主体|表格下方段落\d*'
       r'|右栏正文|右侧正文段落|页面四角检查'
       r'|表\d*下方注释|表\d+)\*\*[：:]',
    r'.*\[无法识别\].*$',
    r'.*绝对忠实图像.*不得推断.*$',
    r'.*此为图像截断导致的不完整句.*$',
    r'.*未做任何补全.*$',
    r'^#{1,3}\s*最终输出说明\s*$',
    r'^如需继续处理后续页面.*$',
    r'^>\s*🔍\s*.+',
    r'^>\s*📝\s*.+',
    r'^>\s*–\s+.+',
    r'^>\s*-\s+(?:左上角|右上角|左下角|右下角|表格上方|表格下方'
       r'|表格行列|所有上标|所有数值|无任何|推荐等级|颜色提示'
       r'|无跨层|同一level|节点\s)',
    r'^>\s*-?\s*(?:所有节点|推荐等级|颜色提示|无跨层嵌套'
       r'|同一层级|同一层内|无任何概括)\s*[：:\w]',
    r'.*`content`\s*与\s*`items`.*逐字提取.*$',
    r'.*`recommendation`\s*留空.*$',
    r'.*颜色提示依据原图色块.*$',
    r'.*同一level内nodes为并列数组.*$',
    r'^>\s*删除了原文中可能存在的上标引用标记.*$',
    r'^##\s+二、图注[（(]',
    r'^###\s+参考文献\s*$',
    r'^##\s+五、自我校验清单',
    r'^#{3,4}\s+修正后[：:]',
    r'^#{3,4}\s+正文[（(]',
    r'^#{3,4}\s+标题[（(]',
    r'^#{3,4}\s+▶\s+(?!表\d)',
    r'^#{2,4}\s+【最终净化版】',
    r'^#{2,4}\s+\[\s*最终净化版\s*\]',
    r'^###\s+YAML\s*流程图',
    # r'^###\s+自然语言概述[（(]',  # 保留：流程图的自然语言描述是有价值的内容
    r'^###\s+YAML\s*结构化数据',
    r'^#{3,4}\s+左栏正文[：:]\s*$',
    r'^#{3,4}\s+左栏小标题[：:]\s*$',
    r'^#{3,4}\s+右栏正文[：:]\s*$',
    r'^#{3,4}\s+右栏小标题[：:]\s*$',
    r'^###\s+总\s*结\s*$',
    r'^###\s+作者单位[（(]',
    r'^###\s+栏内容\s*$',
    r'^#{3,4}\s+图注说明[（(]',
    r'^#{3,4}\s+缩写释义[（(]',
    r'^#{2,4}\s+.*流程图提取.*$',
    r'^#{2,4}\s+.*文本提取与YAML',
    r'^#{2,4}\s+.*YAML结构化输出.*$',
    r'^>\s*（注：[^\n]*YAML结构化数据',
    r'^>\s*（注：[^\n]*自然语言概述',
    r'.*其后附YAML结构化数据.*$',
    r'^#{2,4}\s+[一二三四五六七八九十]、\s*(?:表格提取|正式提取内容'
       r'|主内容区|页面四角|内容过滤|格式处理|其他说明'
       r'|页眉与元信息|页面顶部信息)\b',
    r'^#{2,4}\s+(?:[一二三四五六七八九十]+、\s*)?(?:左栏正文|右栏正文'
       r'|左栏|右栏|左栏小标题|右栏小标题)\s*[（(]',
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


def strip_all_process_content(text: str) -> str:
    """从 VLM 输出文本中剥离所有过程分析/元数据内容。"""
    # Pass 0：全局暴力逐行清除
    lines = text.splitlines(True)
    swept = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            swept.append(line); continue
        if any(re.match(p, stripped) for p in _GLOBAL_SWEEP_PATTERNS):
            continue
        swept.append(line)
    text = "".join(swept)

    # Pass 1：状态机逐行扫描
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

    # Pass 2：多行块正则删除
    multi_line_blocks = [
        (
            r'\n*#{1,4}\s*[*✅🔍]*\s*自我校验(?:清单|完成)?(?:（[^)]*）)?\s*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|第[一二三四五六七八九十]+部分|参考文献'
              r'|左栏内容|右栏内容|左栏正文|右栏正文'
              r'|一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)'
              r'|\n---\n|\n\Z)'
        ),
        (
            r'\n*#{1,4}\s*[*✅🔍📄]*\s*整页(?:结构)?预扫描[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文)|\n---\n|\n\Z)'
        ),
        (
            r'\n*#{1,4}\s*[*✅]*\s*(?:页面四角|四角检查|四角专项)[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文)|\n---\n|\n\Z)'
        ),
        (
            r'\n*#{1,4}\s*[*✅]*\s*(?:内容过滤|格式处理说明|其他说明)[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文)|\n---\n|\n\Z)'
        ),
        (
            r'\n*#{1,4}\s*[*📄📌]+\s*(?:最终(?:输出|修正版)|提取结果|提取内容)[^\n]*\n*'
            r'(?:[^\n]*\n*)*?'
            r'(?=\n#{1,4}\s+(?:表\d|图\d|左栏|右栏|正文|一、|二、)|\n---\n|\n\Z)'
        ),
    ]
    for pattern in multi_line_blocks:
        result = re.sub(pattern, '', result)

    # Pass 3：反向尾部扫描
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
        is_process = (
            _is_block_header(s)
            or _is_block_inner_line(s)
            or any(re.match(p, s) for p in _GLOBAL_SWEEP_PATTERNS)
        )
        if is_process:
            trailing_process = True
            i -= 1; continue
        last_body_line = i + 1
        break
    if trailing_process and last_body_line < len(lines):
        result = "".join(lines[:last_body_line])

    # Pass 4：空行归一化
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


def extract_final_content(filepath: Path) -> Optional[str]:
    """从单个 result 文件中提取最终输出内容。"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    body_start = _skip_frontmatter(lines)
    body = lines[body_start:]
    full_text = "".join(body).strip()

    if _is_reference_page(full_text):
        return None

    marker_idx = _find_body_content_marker(body)
    if marker_idx >= 0:
        text_to_clean = "".join(body[marker_idx:]).strip()
    else:
        text_to_clean = full_text

    return strip_all_process_content(text_to_clean) or None


def merge_page_results(pdf_name: str, output_dir: Path) -> dict:
    """按图片文件名严格排序后合并所有单页提取结果。"""
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

    # 严格按页码(即原图片文件名序号)排序
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
