#!/usr/bin/env python3
"""
VLM 文本提取服务 —— FastAPI HTTP 服务

独立负责：接收图片 → Scout侦察 → Extract提取 → Verify校验 → 输出单页Markdown

启动:
    uvicorn extraction_service:app --host 0.0.0.0 --port 8001

API:
    POST /extract        提交图片列表，启动批量提取任务
    GET  /task/{task_id} 查询单个任务状态与结果
    GET  /tasks          查询所有任务状态
    GET  /health         健康检查
"""

import asyncio
import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from _shared import (
    TaskStatus,
    ExtractionTaskInfo,
    scout_phase,
    extract_phase,
    verify_phase,
    call_vlm,
    DEFAULT_CONCURRENCY,
)

load_dotenv()

_app_logger = logging.getLogger("extraction_service")
_app_logger.setLevel(logging.DEBUG)
_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
_app_logger.addHandler(_console)

app = FastAPI(
    title="VLM 文本提取服务",
    description="两阶段/三阶段 VLM 文档文本提取服务，独立于合并清洗服务",
    version="1.0.0",
)


# ──────────────────── 内存任务存储 ────────────────────

# task_id -> ExtractionTaskInfo
_tasks: dict[str, ExtractionTaskInfo] = {}


# ──────────────────── 请求 / 响应模型 ────────────────────

class ExtractRequest(BaseModel):
    images: list[str] = Field(..., description="图片文件路径列表（服务器本地绝对路径或相对路径）")
    pdf_name: str = Field(..., description="原始PDF文件名（含扩展名），输出目录自动取无后缀名")
    output_dir: str = Field(default="./output", description="输出根目录")
    prompt_dir: str = Field(default=".", description="提示词文件所在目录")
    model: str = Field(default="qwen3-vl-plus", description="VLM模型名称")
    api_key: Optional[str] = Field(default=None, description="API Key（不传则读环境变量 QWEN_API_KEY）")
    base_url: Optional[str] = Field(default=None, description="API Base URL（不传则读环境变量 QWEN_BASE_URL）")
    verify: bool = Field(default=False, description="是否启用阶段3定向校验")
    force_strategy: Optional[str] = Field(
        default=None,
        description="强制使用指定策略，跳过Scout阶段。可选值: 轻量提取, 标准提取, 完整提取",
    )


class ExtractResponse(BaseModel):
    success: bool
    message: str
    pdf_name: str
    total_tasks: int
    task_ids: list[str]


class TaskListResponse(BaseModel):
    total: int
    tasks: list[ExtractionTaskInfo]


# ──────────────────── 日志 ────────────────────

def setup_task_logger(output_dir: Path) -> Path:
    log_file = output_dir / "extraction.log"
    _file = logging.FileHandler(log_file, encoding="utf-8")
    _file.setLevel(logging.DEBUG)
    _file.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    ))
    _app_logger.addHandler(_file)
    return log_file


def cleanup_task_logger():
    for h in _app_logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            h.close()
            _app_logger.removeHandler(h)


# ──────────────────── 单页提取核心逻辑 ────────────────────

async def run_single_extraction(
    task_id: str,
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
) -> None:
    """执行单个图片的完整提取流程，更新内存中的任务状态。"""
    task = _tasks[task_id]
    image_filename = Path(image_path).name

    page_output_dir = output_dir / pdf_name
    page_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = page_output_dir / f"{pdf_name}_{page_num}.md"

    # 更新状态为处理中
    task.status = TaskStatus.PROCESSING
    task.output_file = str(output_file)

    _app_logger.info(f"\n{'='*50}")
    _app_logger.info(f"[{task_id}] 开始处理第 {page_num} 页: {image_filename}")

    try:
        img = Path(image_path)
        if not img.exists():
            raise FileNotFoundError(f"图片不存在: {image_path}")

        total_start = time.time()

        # 阶段1: Scout
        if force_strategy:
            scout_result = {"recommendation": force_strategy, "tables": {"count": 1}}
            _app_logger.info(f"[{task_id}] Scout 已跳过，强制策略: {force_strategy}")
        else:
            scout_result = await scout_phase(str(img), model, api_key, base_url, prompt_dir)

        strategy = scout_result.get("recommendation", "标准提取")
        if strategy == "轻量提取":
            has_tables = scout_result.get("tables", {}).get("count", 0) > 0
            has_images = any(
                b.get("type") == "图片"
                for b in scout_result.get("content_blocks", [])
            )
            if has_tables or has_images:
                strategy = "标准提取"
                reason = "含表格" if has_tables else "含图片"
                _app_logger.info(f"[{task_id}] 保守修正: 页面{reason}，策略提升为 标准提取")

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
task_id: {task_id}
---

"""
        output_file.write_text(frontmatter + extract_result, encoding="utf-8")

        # 更新任务完成状态
        task.status = TaskStatus.COMPLETED
        task.success = True
        task.elapsed_time = round(total_elapsed, 2)
        task.strategy = strategy
        task.output_file = str(output_file)

        _app_logger.info(
            f"[{task_id}] 完成! 耗时 {total_elapsed:.2f}s, 策略={strategy}, 结果={output_file}"
        )

    except Exception as e:
        _app_logger.error(f"[{task_id}] 处理失败: {type(e).__name__}: {e}", exc_info=True)
        task.status = TaskStatus.FAILED
        task.success = False
        task.error = f"{type(e).__name__}: {e}"
        task.elapsed_time = round(time.time() - total_start, 2) if 'total_start' in dir() else None

        error_file = page_output_dir / f"{pdf_name}_{page_num}_error.txt"
        error_file.write_text(f"处理失败: {type(e).__name__}: {e}\n", encoding="utf-8")


# ──────────────────── API 端点 ────────────────────

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "vlm-extraction"}


@app.post("/extract", response_model=ExtractResponse)
async def extract(req: ExtractRequest):
    """
    提交图片列表进行 VLM 文本提取。

    立即返回每个图片对应的任务ID和初始状态，
    实际提取在后台异步执行。
    """
    api_key = req.api_key or os.getenv("QWEN_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="未提供 API Key")

    base_url = req.base_url or os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

    if not req.images or len(req.images) == 0:
        raise HTTPException(status_code=400, detail="images 不能为空")

    valid_strategies = ["轻量提取", "标准提取", "完整提取"]
    if req.force_strategy and req.force_strategy not in valid_strategies:
        raise HTTPException(status_code=400, detail=f"force_strategy 无效，可选值: {valid_strategies}")

    prompt_dir = Path(req.prompt_dir)
    output_dir = Path(req.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_stem = Path(req.pdf_name).stem
    task_output_dir = output_dir / pdf_stem
    task_output_dir.mkdir(parents=True, exist_ok=True)

    log_file = setup_task_logger(task_output_dir)

    _app_logger.info(f"{'='*60}")
    _app_logger.info(f"VLM 文本提取服务 — 新任务")
    _app_logger.info(f"  PDF 文件名: {req.pdf_name}")
    _app_logger.info(f"  输出目录前缀: {pdf_stem}")
    _app_logger.info(f"  图片数量: {len(req.images)}")
    _app_logger.info(f"  模型: {req.model}")
    _app_logger.info(f"  校验模式: {'开启' if req.verify else '关闭'}")
    _app_logger.info(f"{'='*60}")

    # 为每个图片创建任务记录
    task_infos: list[ExtractionTaskInfo] = []
    task_ids: list[str] = []

    for idx, image_path in enumerate(req.images, start=1):
        task_id = str(uuid.uuid4())
        image_filename = Path(image_path).name

        task_info = ExtractionTaskInfo(
            task_id=task_id,
            image_filename=image_filename,
            image_path=image_path,
            output_file=None,
            status=TaskStatus.PENDING,
            success=None,
            error=None,
            elapsed_time=None,
            strategy=None,
            pdf_name=pdf_stem,
            page_num=idx,
        )
        _tasks[task_id] = task_info
        task_infos.append(task_info)
        task_ids.append(task_id)

        _app_logger.info(f"  任务创建: {task_id} → {image_filename} (第{idx}页)")

    # 后台并发执行提取
    semaphore = asyncio.Semaphore(DEFAULT_CONCURRENCY)

    async def _process_with_semaphore(task_info: ExtractionTaskInfo):
        async with semaphore:
            await run_single_extraction(
                task_id=task_info.task_id,
                image_path=task_info.image_path,
                page_num=task_info.page_num,
                pdf_name=task_info.pdf_name,
                output_dir=output_dir,
                model=req.model,
                api_key=api_key,
                base_url=base_url,
                prompt_dir=prompt_dir,
                enable_verify=req.verify,
                force_strategy=req.force_strategy,
            )

    async def _run_all_extractions():
        await asyncio.gather(*[_process_with_semaphore(t) for t in task_infos])
        cleanup_task_logger()

    asyncio.create_task(_run_all_extractions())

    return ExtractResponse(
        success=True,
        message=f"已提交 {len(req.images)} 个提取任务，正在后台执行",
        pdf_name=req.pdf_name,
        total_tasks=len(req.images),
        task_ids=task_ids,
    )


@app.get("/task/{task_id}", response_model=ExtractionTaskInfo)
async def get_task(task_id: str):
    """查询单个提取任务的详细状态和结果。"""
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"任务不存在: {task_id}")
    return task


@app.get("/tasks", response_model=TaskListResponse)
async def get_tasks(pdf_name: Optional[str] = None):
    """
    查询所有任务状态。

    可选参数 pdf_name: 过滤指定PDF的任务。
    """
    all_tasks = list(_tasks.values())
    if pdf_name:
        all_tasks = [t for t in all_tasks if t.pdf_name == pdf_name]
    return TaskListResponse(total=len(all_tasks), tasks=all_tasks)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="extraction_service:app", host="0.0.0.0", port=8001, reload=True)
