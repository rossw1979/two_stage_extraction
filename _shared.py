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
    import asyncio

    try:
        from openai import AsyncOpenAI, APIConnectionError
    except ImportError:
        raise RuntimeError("缺少 openai 依赖。请运行: pip install openai")

    # 兼容不同版本的 openai SDK
    try:
        from openai import APIStatusError as _APIStatusError
        RETRYABLE = (APIConnectionError, _APIStatusError)
    except ImportError:
        RETRYABLE = (APIConnectionError,)
    MAX_RETRIES = 3
    BASE_DELAY = 2  # 秒

    client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=120.0)

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.0,
            )
            return response.choices[0].message.content
        except RETRYABLE as e:
            if attempt < MAX_RETRIES:
                delay = BASE_DELAY * (2 ** attempt)
                logger.warning(
                    f"[VLM] 第 {attempt + 1}/{MAX_RETRIES + 1} 次尝试失败: {e}. "
                    f"{delay}s 后重试..."
                )
                await asyncio.sleep(delay)
            else:
                raise


def load_prompt(prompt_path: Path) -> str:
    if not prompt_path.exists():
        raise FileNotFoundError(f"提示词文件不存在: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")

# ────────────────────  Scout ────────────────────
def _clean_json_control_chars(raw: str) -> str:
    """修复 LLM 生成 JSON 字符串值中未转义的控制字符（换行/回车/制表符）。"""
    result = []
    in_string = False
    escaped = False
    for ch in raw:
        if escaped:
            result.append(ch)
            escaped = False
        elif ch == '\\' and in_string:
            result.append(ch)
            escaped = True
        elif ch == '"':
            result.append(ch)
            in_string = not in_string
        elif in_string and ch == '\n':
            result.append('\\n')
        elif in_string and ch == '\r':
            result.append('\\r')
        elif in_string and ch == '\t':
            result.append('\\t')
        elif in_string and ord(ch) < 0x20:
            # 其他控制字符，直接移除
            pass
        else:
            result.append(ch)
    return ''.join(result)


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
    except json.JSONDecodeError:
        # 尝试修复 LLM 生成的 JSON 中未转义控制字符
        try:
            fixed = _clean_json_control_chars(raw)
            return json.loads(fixed)
        except json.JSONDecodeError as e:
            tail = raw[-200:] if len(raw) > 200 else raw
            truncated = not raw.rstrip().endswith(('}', ']'))
            logger.warning(
                f"Scout JSON 解析失败: {e}"
                f"{' [疑似输出被截断]' if truncated else ''}"
                f"\n原始输出末尾200字符:\n{tail}"
            )
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

    # 加载完整的校验提示词
    prompt_path = Path(__file__).parent / "verify_prompt.md"
    if prompt_path.exists():
        system_prompt = load_prompt(prompt_path)
    else:
        system_prompt = "你是一位严谨的医学文献校验专家。"

    user_prompt = f"""【页面结构信息】
{json.dumps(scout_result, ensure_ascii=False, indent=2)}

【提取结果】
{extract_result}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [build_image_message(image_path), {"type": "text", "text": user_prompt}]},
    ]
    raw = await call_vlm(messages, model, api_key, base_url, max_tokens=8192)
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
    "正式提取输出",
    "正式输出",
    "提取结果",
    "正文提取",
    "最终输出",
    "最终提取结果",
    "📄 最终提取结果",
    "📤 最终输出",
    "**最终输出",
    "**第四步",
    "**第三步：最终输出",
    "正文段落",
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
    # 检测到参考文献标题即视为参考文献页
    if re.search(r'^#{1,4}\s*参\s*考\s*文\s*献', text, re.MULTILINE):
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
            # 兼容带 markdown 标题前缀的情况，如 "### 正式输出..."
            if re.search(r'^#{1,4}\s+' + re.escape(marker), stripped):
                return i
    return -1


_BLOCK_HEADER_PATTERNS = [
    r'###\s*[*✅🔍📄📌📨💡🔎]*\s*整页(?:结构)?预扫描(?:结果|确认|（必须执行）|（内部完成[^）]*）|（确认无遗漏）)?',
    r'###\s*[*📨]*\s*最终输出\s*[（(]',
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
    r'###\s*二、主内容区',
    r'###\s*📤\s*最终输出',
    r'^###\s*提取结果\s*\(干净',
    r'###\s*正文段落\s*\(.*?\)',
    r'###\s*段落\s*\(.*?\)',
    r'#{1,3}\s*最终输出说明\s*$',
    r'##\s+二、图注[（(]',
    r'###\s+参考文献\s*$',
    r'页面为\*\*[^*]+\*\*',
    r'页面可见(?:内容块|内容)及位置如下[：:]*$',
    r'^\s*-\s*\*\*(?:左栏|右栏)内容块',
    r'^\s*-\s*\*\*页面角落检查\*\*',
    r'\[输出结束\]',
    r'^-\s*\*\*(?:左|右)栏内容[：:]*\*\*',
]

_BLOCK_INNER_PATTERNS = [
    r'^\d+\.\s+\*\*[^*]{2,50}\*\*[：:]\s*$',
    r'^-\s+\*\*[^*]{2,50}\*\*[：:]',
    r'^-\s*(?:左栏|右栏)\s+\d+\s*段(?:正文)?',
    r'^-\s+表\s*\d+',
    r'^-\s+(?:页眉页脚|删除页眉|删除页脚|保留章节标题)',
    r'^-\s+无流程图(?:，无需\s*YAML)?',
    r'^-\s+上标引用标记',
    r'^-\s+(?:无额外文字|无文字|无遗漏文字|水印|参考文献列表|缩写)',
    r'^\s*-?\s*\[[ xX☑]\]\s+',
             r'|表格行列核对|流程图\s*YAML|已删除|已覆盖|已完整'
             r'|数值阈值和单位完整|确认无遗漏内容块'
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
    r'^-\s+\*\*(?:已删除|已覆盖|页眉|页脚|无流程图|表格中数值|上标引用|无额外文字|无遗漏)\*\*\s*[：:]',
    r'^-\s+(?:页眉页脚|删除页眉|删除页脚|保留章节标题|无流程图(?:，无需\s*YAML)?'
           r'|(?:无额外文字|无文字|无遗漏文字|水印|参考文献列表|缩写))',
    r'^-?\s*→\s*\*\*(?:删除|已过滤|已按规则删除)\*\*',
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
    r'^\s*-\s*\*\*(?:左|右)栏内容块',
    r'^\s*-\s*\*\*页面角落检查\*\*',
    r'^\s*-\s*\*\*修正版\*\*',
    r'^\s*-\s*(?:段落|标题|表格|图)\d*.*[：:]',
    r'^\s*\d+\.\s+.*→.*',
]

_BODY_SIGNAL_PATTERNS = [
    r'^##\s+表\d', r'^###\s+表\d', r'^\*\*表\d', r'^####\s+表\d', r'^#####\s+表\d',
    r'^##\s+Table\s+\d', r'^###\s+Table\s+\d', r'^\*\*Table\s+\d',
    r'^###\s+左栏内容', r'^###\s+右栏内容',
    r'^###\s*▶\s*(?:左栏|右栏)', r'^####\s*▶\s*左栏内容',
    r'^#####\s*【流程图标题】',
    r'^##\s+图\d', r'^###\s+图\d',
    r'^##\s+Figure\s+\d', r'^###\s+Figure\s+\d',
    r'^##\s+(?:第[一二三四五六七八九十]+部分|前言|摘要|关键词|总[结论]|执笔|核心专家|专家组|利益冲突|参考文献)\b',
    r'^\*\*(?:第一|第二|第三|第四|第五|第六)部分',
    r'^###\s+(?:一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)',
    r'^##\s+(?:一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)',
    r'^####\s+(?:一、|二、|三、|四、|五、)',
    r'^#####?\s*【',
    r'^\*\*Footnotes:\*\*',
    r'^\*\*Notes:\*\*',
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
           r'|右侧正文段落|表\d*下方(?:注释)?'
           r'|主体上部|底部图注|流程图下方'
           r'|左侧路径|右侧路径|图\d+左侧|图\d+右侧'
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
    r'^>?\s*输出完毕[，。]*.*$',
    r'.*数字化副本.*$.*(?:未增删|未解释|未推断|未改写)',
    r'^\*\*输出结束[^\n]*$',
    r'^如需对后续页面继续提取.*$',
    r',\s*严格遵循\s*v?\d[\w.]*\s*规范[。]*$',
    r'^>?\s*（以下为最终合规输出.*$',
    r'^[（(]?注[）：:][^)]*[）]?\s*(?:右栏末句|原文中|此处为|前文延续|图像中被截断)',
    r'^以下为严格按原文排版顺序.*$',
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
    r'^\d+\.\s+\*\*(?:顶部页眉|表\d*[\s]*标题|表格主体|表格下方段落\d*'
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
    r'^\s*-\s*\*\*(?:左|右)栏内容块',
    r'^\s*-\s*\*\*页面角落检查\*\*',
    r'^\s*-\s*\*\*修正版\*\*',
    r'页面为\*\*[^*]+\*\*.*内容块分布',
    r'^页面为.*内容块分布如下[：:]*$',
    r'页面可见(?:内容块|内容)及位置如下[：:]*$',
    r'^\s*-\s*\*\*(?:顶部|左上|右上|左下|右下|中部|页眉|页脚|期刊信息).*?\*\*\s*[：:]',
    r'^\s*-\s*(?:段落|标题|表格|图)\d*.*[：:]',
    r'^\s*-\s*\[\s*[xX☑]\s*\]\s+.*(?:内容块|扫描|四角|表格|跨栏|双栏|流程图|数值|HTML|注释|YAML|阈值|单位)',
    r'^\s*-\s*\[\s*[xX☑]\s*\]\s+.*(?:校验|检查|核对|确认|覆盖|删除|过滤)',
    r'\[输出结束\]',
    r'^-\s+无(?:表格|公式|流程图|决策树|图片|水印|参考文献)',
    r'^-\s+无参考文献标题出现',
    r'^-\s+左下角.*?水印.*?已删除',
    r'^-\s+页码.*?已删除',
    r'^-\s+全文完整提取',
    r'^-\s+右下角.*?网址.*?删除',
    r'^页面内容块分布如下[：:]*$',
    r'^内容块分布如下[：:]*$',
    r'^-\s+(?:\*\*)?(?:主体内容|右侧边栏|左侧边栏|页脚|页面顶部|页面底部|左上角|右上角|左下角|右下角|顶部标题|页码|表格下方|上标参考文献编号).*?(?:删除|覆盖|已删除|需删除|按规则)',
    r'^-\s+(?:\*\*)?(?:主体内容|页面底部|页面顶部|左栏|右栏)[:：].*',
    r'^-\s+(?:左栏|右栏|顶部|底部)[:：].*?段落',
    r'^\d+\.\s+(?:顶部段落|段落|首段|续接前页|主体内容|子标题|标题|表\d*\s*(?:标题|注释|：)?|表格|图\d+|图注).*?（',
    r'^-\s+无页眉页脚需保留内容',
    r'^-\s+页面顶部有.*',
    r'^（页脚水印已过滤.*）$',
    r'^✅\s*全部通过.*$',
    r'^>\s*提取完成.*$',
    r'^>\s*本输出为.*数字化副本.*$',
    r'^>\s*提取完毕.*$',
    r'^页面为[^。]*(?:双栏|单栏|多栏)[^。]*(?:无表格|无公式|无流程图|无决策树|无图片)[^。]*。?$',
    r'^-\s*\*\*(?:左|右)栏内容[：:]*\*\*',
    r'^\s*\d+\.\s+.*→.*',
    r'^-\s+主体为[^。]*(?:双栏|单栏|多栏)[^。]*。?$',
    r'^[-\s]*\*\*(?:左|右)栏内容块[（(].*?[）)]\*\*\s*[：:]$',
    r'^-\s+(?:左|右)栏内容块[（(].*?[）)]\s*[：:]$',
    r'^-\s+页面底部[：:].*',
    r'^-\s+无页脚页码.*',
    r'^[—-]+\s*(?:删除页眉|删除左下角|删除右下角|删除正文中的上标引用标记).*',
    r'^——\s*开始输出干净数字化副本\s*——$',
    r'^-\s+(?:所有剂量|缩写|推荐等级未出现)[（(].*',
    r'^\s*\d+\.\s*(?:标题)?["\u201c"].*?["\u201d"]段落[（(].*?[）)]',
    r'^\s*\d+\.\s*末段[：：].*',
    r'^-\s+.*(?:删除页眉|删除页脚|删除左下角|删除右下角|删除正文中的上标引用标记|推荐等级未出现|已过滤|已删除|已忽略|逐字提取|未生成|未补全|被截断).*',
    r'^\*\*（删除页眉.*',
    r'^\d+\.\s+(?:页眉|主标题|副标题|编写单位|通信作者|【关键词】|英文标题|底部左侧|底部右侧|左栏正文|右栏正文|二维码|图像元素|期刊信息).*',
    r'^-\s+保留\s+DOI.*',
    r'^\*\*(?:页眉|页脚)信息[（(]已过滤[）)]\*\*',
    r'^-\s+左上角页码[：:].*',
    r'^-\s+顶部期刊信息.*',
    r'^-\s+右上角标题.*',
    r'^-\s+右下角二维码.*',
    r'^✅\s*以下为严格遵循.*',
    r'^\s*⚠.*',
    r'^\s*→\s*修正后.*',
    r'^重新输出修正版.*',
    r'^\s*"[^"]*"\s*$',
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
    # 英文脚注/注释标记
    if re.match(r'^\*\*[A-Z][a-zA-Z]+:\*\*', s):
        return True
    # Markdown 标题（中英文）
    if re.match(r'^#{1,4}\s+(?:Table|Figure|表|图)\s*\d', s):
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


# ── 基于特征分类的 VLM 过程内容清洗器 ──────────────────────────

_PROCESS_HEADING_KEYWORDS = {
    '预扫描', '自我校验', '内容过滤', '四角检查', '四角专项', '最终输出说明',
    '提取结果', '按规则逐块提取', '页眉与元信息', '页面顶部信息',
    '正文内容提取', '格式处理说明', '其他说明', '页面四角', '自我校验',
    '整页结构预扫描', '最终输出说明', '提取结果', '按规则逐块提取', '主内容区',
    '表格提取', '页脚与水印处理', '内容完整性核验', '修正版', '重新输出',
    '正文段落', '最终修正版', '最终输出', '提取内容', '按排版顺序逐块提取',
    '内容块定位', '页眉/页脚信息', '四角检查', '页面布局', '整页结构',
}

_PROCESS_PREFIXES = [
    r'以下为', r'我将严格按照', r'此为该页', r'此为原始文献', r'此输出为',
    r'本提取结果为', r'本页提取内容', r'页面为', r'该页包含',
    r'页面可见', r'内容块分布如下', r'经四角检查', r'现按', r'已执行',
    r'输出完毕', r'提取完成', r'提取完毕', r'数字化副本', r'最终输出说明',
    r'如需继续处理', r'如需对后续页面', r'删除了原文中可能存在',
    r'所有节点', r'推荐等级原文未标注', r'颜色提示依据原图色块',
    r'同一level内nodes', r'无跨层嵌套', r'绝对忠实图像', r'图像截断',
    r'未做任何补全', r'及支\[无法识别\]', r'页面内容块分布如下',
]

_PROCESS_LINE_PREFIXES_EXACT = [
    r'——\s*开始按规则逐块提取——',
    r'——\s*开始输出干净数字化副本\s*——',
    r'——\s*校验通过，开始输出\s*——',
    r'\[整页结构预扫描完成\]',
    r'\[自我校验启动\]',
    r'\[自我校验复核\]',
    r'\[校验通过，开始输出\]',
    r'\[输出结束\]',
    r'\[\s*自我校验完成\s*\]',
]


def _classify_line(line: str) -> str:
    """将单行分类为 EMPTY / PROCESS / BODY。"""
    s = line.strip()
    if not s:
        return 'EMPTY'

    for pat in _PROCESS_LINE_PREFIXES_EXACT:
        if re.match(pat, s):
            return 'PROCESS'

    # 引述块（>）在 VLM 输出中几乎都是过程描述
    if s.startswith('> '):
        if re.match(r'> \*\*(?:说明|注意|表格周边文字提取|页眉|页脚|页码|期刊信息|内容完整性核验|页脚与水印处理)', s):
            return 'PROCESS'
        if re.match(r'> [✅⚠️→🔍📄📌💡🔎]', s):
            return 'PROCESS'
        if re.search(r'(?:左上|右上|左下|右下|上部|下部|左侧|右侧|中部|表格上方|表格下方|流程图|页眉|页脚|四角|预扫描|内容块|定位|检查|核对|提取完毕|数字化副本|本结果为|本页提取|表格周边文字提取|页面左下角|页面右下角|页面左上角|页面右上角)', s):
            return 'PROCESS'
        return 'BODY'

    # 校验清单
    if re.match(r'^\s*-\s*\[\s*[xX☑ ]\s*\]', s):
        return 'PROCESS'

    # 过程性 Emoji / 箭头
    if re.match(r'^[✅⚠️→🔍📄📌💡🔎]', s):
        return 'PROCESS'

    # 方括号过程阶段
    if re.match(r'^\[(?:自我校验|整页结构预扫描|校验通过|输出结束|自我校验复核|自我校验完成)\]', s):
        return 'PROCESS'

    # Markdown 标题含过程关键词
    if re.match(r'^#{1,4}\s', s):
        heading_text = re.sub(r'^#{1,4}\s*', '', s)
        if any(kw in heading_text for kw in _PROCESS_HEADING_KEYWORDS):
            return 'PROCESS'

    # 显式过程前缀
    for prefix in _PROCESS_PREFIXES:
        if re.match(prefix, s):
            return 'PROCESS'

    # 删除指令
    if re.match(r'^-\s+.*(?:删除页眉|删除页脚|删除左下角|删除右下角|删除右上角|删除正文中的上标引用标记|已过滤|已删除|已忽略|逐字提取|未生成|未补全|被截断)', s):
        return 'PROCESS'

    # 编号的过程项（内容块清单）
    if re.match(r'^\s*\d+\.\s+(?:页眉|主标题|副标题|编写单位|通信作者|【关键词】|英文标题|底部左侧|底部右侧|左栏正文|右栏正文|二维码|图像元素|期刊信息|左上角|右上角|左下角|右下角|顶部页眉|顶部居中|页码)', s):
        return 'PROCESS'

    # 星号包裹的过程标签
    if re.match(r'^\s*-\s*\*\*(?:顶部|左上区域|右上区域|中部偏下|左下角|右下角|左栏主体|右栏主体|左栏正文|右栏正文|页码|期刊信息|页眉|页脚|四角检查|页面四角检查|段落\d*|表\d*标题|表格主体|表格下方段落|右侧正文段落|表\d*下方(?:注释)?|主体上部|底部图注|流程图下方|左侧路径|右侧路径|图\d+左侧|图\d+右侧)\d*[\)）]?\*\*\s*[：:]', s):
        return 'PROCESS'

    # 带位置/过程词的列表项
    if re.match(r'^-\s+.*?(?:左上角|右上角|左下角|右下角|顶部|页眉|页脚|页码|期刊信息|二维码|DOI|水印|参考文献|内容块|定位|正文|删除|保留|忽略|无文字|已删除|已过滤|按规则|无水印|无参考文献|无上标引用|无页眉页脚|正文起始内容)', s):
        return 'PROCESS'

    # 无 markdown 标题号的星号包裹过程标签
    if re.match(r'^\*\*(?:内容块定位|页眉/页脚信息|四角检查|页面布局|整页结构|预扫描结果|页脚与水印处理说明|内容完整性核验补充说明|页眉/页脚处理说明).*?\*\*', s):
        return 'PROCESS'
    if re.match(r'^\*\*(?:顶部|顶部居中|页码|页眉|期刊信息|左上角|右上角|左上区域|右上区域|中部偏上|中部偏下|左下角|右下角|左栏主体|右栏主体|左栏正文|右栏正文|流程图上方|流程图下方|表格上方|表格下方|表\d*标题|表格主体|表格下方段落\d*|右侧正文段落|表\d*下方注释|主体上部|底部图注|左侧路径|右侧路径)\*\*\s*[：:]', s):
        return 'PROCESS'

    # 页面布局纯文本描述
    if re.match(r'^页面为[^。]*(?:双栏|单栏|多栏)[^。]*(?:无表格|无公式|无流程图|无决策树|无图片)[^。]*。?$', s):
        return 'PROCESS'
    if re.match(r'^页面为\*\*[^*]+\*\*排版.*内容块分布如下[：:]*$', s):
        return 'PROCESS'
    if re.match(r'^该页包含以下内容块[：:]*$', s):
        return 'PROCESS'
    if re.match(r'^内容块分布如下[：:]*$', s):
        return 'PROCESS'
    if re.match(r'^页面可见(?:内容块|内容)及位置如下[：:]*$', s):
        return 'PROCESS'

    # 常见尾部残留：输出声明、四角检查列表项
    if re.match(r'^输出为.*数字化副本.*$', s):
        return 'PROCESS'
    if re.match(r'^-\s+.*四角检查[：:]', s):
        return 'PROCESS'
    if re.match(r'^-\s+页面四角检查[：:]', s):
        return 'PROCESS'
    if re.match(r'^\d+\.\s+\*\*四角检查\*\*[：:]', s):
        return 'PROCESS'

    return 'BODY'


def strip_all_process_content(text: str) -> str:
    """从 VLM 输出文本中剥离所有过程分析/元数据内容（基于特征分类器）。"""
    lines = text.splitlines(True)
    classes = [_classify_line(line) for line in lines]

    # Pass 1：状态机扫描 —— 跳过过程块
    kept = []
    in_block = False
    for i, line in enumerate(lines):
        s = line.strip()
        cls = classes[i]
        if not s:
            if in_block:
                continue
            kept.append(line)
            continue

        if cls == 'PROCESS':
            in_block = True
            continue

        if in_block and cls != 'BODY':
            continue

        if in_block and cls == 'BODY':
            in_block = False
            kept.append(line)
            continue

        kept.append(line)

    # Pass 2：反向尾部扫描
    trailing_cleaned = []
    in_trailing = False
    for line in reversed(kept):
        s = line.strip()
        if not s:
            if in_trailing:
                continue
            trailing_cleaned.append(line)
            continue
        cls = _classify_line(line)
        if cls == 'PROCESS':
            in_trailing = True
            continue
        in_trailing = False
        trailing_cleaned.append(line)

    result = ''.join(reversed(trailing_cleaned))

    # Pass 3：去除引用上标 HTML 标签
    result = re.sub(r'<sup>.*?</sup>', '', result)

    # Pass 4：空行归一化
    result = re.sub(r'\n{3,}', '\n\n', result)

    # Pass 5：去除首尾残留的 --- 分隔线与空行
    result = re.sub(r'^(?:\s*---\s*\n|\s*\n)+', '', result)
    result = re.sub(r'(?:\n\s*---\s*|\n\s*)+$', '', result)

    return result.strip()


def _strip_frontmatter_checklist(body: list[str]) -> list[str]:
    """硬删除frontmatter后的校验清单块（- [x] / - [ ] 开头的连续块）。"""
    result = []
    in_checklist = False
    for line in body:
        s = line.strip()
        if not s:
            if in_checklist:
                continue
            result.append(line)
            continue
        # 检测到校验清单项
        if re.match(r'^\s*-\s*\[\s*[xX☑ ]\s*\]\s+', s):
            in_checklist = True
            continue
        # 校验清单结束后的 ✅ 汇总行
        if in_checklist and re.match(r'^✅\s*所有校验项通过|^✅\s*以下为严格遵循', s):
            continue
        if in_checklist and re.match(r'^✅\s*.+', s):
            continue
        # 遇到正文信号则退出清单模式
        in_checklist = False
        result.append(line)
    return result


def _truncate_at_references(text: str) -> str:
    """在'#### 参考文献'或'## 参考文献'处截断文本。"""
    match = re.search(r'\n#{1,4}\s*参\s*考\s*文\s*献\s*\n', text)
    if match:
        return text[:match.start()]
    return text


# ──────────────────── 参考文献残余清理 ────────────────────

_REF_NUMBER_PATTERN = re.compile(r'^\[\d+(?:[-,]\d+)?\]')
_REF_YEAR_PATTERN = re.compile(r'\b(19|20)\d{2}\b')
_REF_JOURNAL_TYPE_ZH = re.compile(r'\[[JMCNDRSjmcndrs]\]\.?')
_REF_JOURNAL_NAME_EN = re.compile(
    r'[Jj]ournal|Medicine|Cardiol|Heart|Surgery|Lancet|NEJM|N Engl J Med|'
    r'Circulation|JACC|Eur Heart|Am J|Catheter|Interv|Radiol|Ther|Clin|Res'
)
_REF_DOI_PATTERN = re.compile(r'DOI[\s:]*10\.\d+', re.IGNORECASE)
_REF_PURE_REF_MARKER = re.compile(r'（本页为参考文献，已跳过）')


def _is_reference_entry(text: str) -> bool:
    """判断文本是否为参考文献条目（支持多行拼接后的完整文本）。"""
    stripped = text.strip()
    if not stripped or not _REF_NUMBER_PATTERN.match(stripped):
        return False
    has_journal_type = bool(_REF_JOURNAL_TYPE_ZH.search(stripped))
    has_journal_name = bool(_REF_JOURNAL_NAME_EN.search(stripped))
    has_doi = bool(_REF_DOI_PATTERN.search(stripped))
    has_year = bool(_REF_YEAR_PATTERN.search(stripped))
    if has_journal_type or has_journal_name or has_doi:
        return True
    has_author_mark = bool(re.search(r'et al\.|等\.', stripped))
    if has_year and has_author_mark:
        return True
    if has_author_mark:
        return True
    return False


def _is_orphaned_reference_continuation(line: str) -> bool:
    """判断是否为孤立的参考文献续行（不以 [数字] 开头，但有参考文献特征）。"""
    stripped = line.strip()
    if not stripped or _REF_NUMBER_PATTERN.match(stripped):
        return False
    has_journal_type = bool(_REF_JOURNAL_TYPE_ZH.search(stripped))
    has_year = bool(_REF_YEAR_PATTERN.search(stripped))
    has_doi = bool(_REF_DOI_PATTERN.search(stripped))
    has_journal_name = bool(_REF_JOURNAL_NAME_EN.search(stripped))
    starts_lowercase = bool(re.match(r'^[a-z]', stripped))
    if starts_lowercase and has_journal_type and has_year and (has_doi or has_journal_name):
        return True
    return False


def _collect_reference_entry(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    """收集从 start_idx 开始的完整参考文献条目（处理跨行情况）。"""
    entry_lines = [lines[start_idx]]
    j = start_idx + 1
    while j < len(lines):
        next_stripped = lines[j].strip()
        if not next_stripped or _REF_NUMBER_PATTERN.match(next_stripped):
            break
        entry_lines.append(lines[j])
        j += 1
    return entry_lines, j


def remove_references_from_text(text: str) -> tuple[str, int]:
    """
    从文本中删除参考文献条目（支持跨行条目、单条删除和孤立续行）。
    返回：(清理后的文本, 删除的参考文献行数)
    """
    lines = text.splitlines()
    new_lines = []
    removed_count = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            i += 1
            continue

        if _REF_NUMBER_PATTERN.match(stripped):
            entry_lines, next_idx = _collect_reference_entry(lines, i)
            entry_text = '\n'.join(entry_lines)
            if _is_reference_entry(entry_text):
                removed_count += len(entry_lines)
                i = next_idx
                continue
            else:
                new_lines.extend(entry_lines)
                i = next_idx
                continue

        new_lines.append(line)
        i += 1

    # 清理孤立的参考文献续行（跨页断行）
    cleaned_lines = []
    for line in new_lines:
        stripped = line.strip()
        if stripped and _is_orphaned_reference_continuation(stripped):
            removed_count += 1
            continue
        cleaned_lines.append(line)

    # 清理连续的空行（最多保留2个空行）
    final_lines = []
    empty_count = 0
    for line in cleaned_lines:
        if not line.strip():
            empty_count += 1
            if empty_count <= 2:
                final_lines.append(line)
        else:
            empty_count = 0
            final_lines.append(line)

    return '\n'.join(final_lines), removed_count


def _remove_duplicate_revisions(text: str) -> str:
    """检测并去除'修正版'或'重新输出修正版'导致的重复内容。

    对于'重新输出修正版'，采用保守策略：仅删除该声明及其之后的所有内容，
    保留之前的原始正文（避免像 BODY_CONTENT_MARKERS 那样误删前置内容）。
    """
    # 保守处理"重新输出修正版"：截断到声明处
    re_output_match = re.search(r'^重新输出修正版.*[：:]?\s*$', text, re.MULTILINE)
    if re_output_match:
        text = text[:re_output_match.start()].strip()

    # 传统的"修正版（删除所有上标引用标记）"通常出现在重复块的开头，
    # 其后为净化后的内容，因此保留之后的内容
    marker = re.search(r'#{1,4}\s*修正版.*删除所有上标引用标记[：:]?\s*\n', text)
    if marker:
        return text[marker.end():].strip()
    return text


def _find_content_start_after_separator(body: list[str]) -> int:
    """
    查找 frontmatter 后 '---' 分隔线之后正文开始的行号。
    VLM 输出常在过程描述和正文之间用 '---' 分隔。
    """
    for i, line in enumerate(body):
        if line.strip() == '---':
            # 跳过空行，检查后面是否有正文
            for j in range(i + 1, len(body)):
                s = body[j].strip()
                if not s:
                    continue
                # 如果下一条是全局清洗列表中的过程内容，跳过这个分隔线
                if any(re.match(p, s) for p in _GLOBAL_SWEEP_PATTERNS):
                    break
                # 如果是正文信号，从这个分隔线之后开始
                if _looks_like_body_text(s) or _is_body_signal(s):
                    return i + 1
                # 如果是正文标记（如 ### 正式输出），也从这里开始
                if _find_body_content_marker(body[j:j+1]) >= 0:
                    return i + 1
                # 其他情况，跳过这个分隔线继续找下一个
                break
    return -1


def extract_final_content(filepath: Path) -> Optional[str]:
    """从单个 result 文件中提取最终输出内容。"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    body_start = _skip_frontmatter(lines)
    body = lines[body_start:]

    # 硬删除frontmatter后的校验清单
    body = _strip_frontmatter_checklist(body)

    full_text = "".join(body).strip()

    if _is_reference_page(full_text):
        return None

    # 优先查找显式的正文标记（安全标记，不含 revision 相关）
    marker_idx = _find_body_content_marker(body)
    if marker_idx >= 0:
        text_to_clean = "".join(body[marker_idx:]).strip()
    else:
        # 不再使用 --- 分隔线截断，直接处理完整文本，避免误删正文
        text_to_clean = full_text

    # 去除修正版重复内容
    text_to_clean = _remove_duplicate_revisions(text_to_clean)

    # 在参考文献标题处截断
    text_to_clean = _truncate_at_references(text_to_clean)

    # 清理混入正文的参考文献条目（VLM 可能未能完全跳过的参考文献）
    text_to_clean, ref_removed = remove_references_from_text(text_to_clean)
    if ref_removed > 0:
        logger.info(f"[Clean] 删除 {ref_removed} 行混入正文的参考文献")

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
                  and not f.name.endswith("_error.txt")
                  and not f.name.endswith("_review.md")]

    if not page_files:
        logger.warning("[Merge] 未找到任何单页提取结果文件")
        return {"status": "no_results", "merged_file": str(merged_file)}

    for pf in page_files:
        try:
            stem = pf.stem
            # 文件名可能是 xxx_10.md 或 xxx_10_review.md，需要正确提取页码
            parts = stem.rsplit("_", 2)
            if len(parts) >= 2 and parts[-1] == "review":
                page_num_str = parts[-2]
            else:
                page_num_str = parts[-1]
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

    # 合并完成后，对合并文件执行一次参考文献残余清理
    #（处理跨页断行导致的孤立参考文献续行）
    try:
        merged_text = merged_file.read_text(encoding='utf-8')
        cleaned_merged_text, ref_removed = remove_references_from_text(merged_text)
        if ref_removed > 0:
            merged_file.write_text(cleaned_merged_text, encoding='utf-8')
            logger.info(f"[Merge] 合并后清理：删除 {ref_removed} 行参考文献残余")
    except Exception as e:
        logger.error(f"[Merge] 合并后参考文献清理出错: {e}")

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
