#!/usr/bin/env python3
"""
合并 + 清洗服务 —— FastAPI HTTP 服务

独立负责：轮询提取任务状态 → 全部完成后合并清洗 → 输出最终Markdown

启动:
    uvicorn merge_service:app --host 0.0.0.0 --port 8002

API:
    POST /merge          提交提取任务ID列表，启动后台合并流程
    GET  /merge/{merge_id} 查询合并任务状态与结果
    GET  /merges          查询所有合并任务
    GET  /health          健康检查

依赖:
    提取服务 (extraction_service) 需正在运行，默认地址 http://localhost:8001
"""

import ast
import asyncio
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Optional, Union
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from _shared import (
    TaskStatus,
    MergeTaskInfo,
    PageMergeDetail,
    ExtractionTaskInfo,
    merge_page_results,
    logger,
)

load_dotenv()

_app_logger = logging.getLogger("merge_service")
_app_logger.setLevel(logging.DEBUG)
_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
_app_logger.addHandler(_console)


def setup_merge_logger(output_dir: Path) -> None:
    log_file = output_dir / "merge.log"
    _file = logging.FileHandler(log_file, encoding="utf-8")
    _file.setLevel(logging.DEBUG)
    _file.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    ))
    _app_logger.addHandler(_file)


def cleanup_merge_logger():
    for h in _app_logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            h.close()
            _app_logger.removeHandler(h)

app = FastAPI(
    title="VLM 合并+清洗服务",
    description="轮询提取任务状态，全部完成后执行结果合并与过程内容清洗",
    version="1.0.0",
)


# ──────────────────── 配置 ────────────────────

# 提取服务地址（可通过环境变量覆盖）
EXTRACTION_SERVICE_BASE_URL = os.getenv(
    "EXTRACTION_SERVICE_BASE_URL", "http://localhost:8001"
)

# 轮询间隔（秒）
POLL_INTERVAL = float(os.getenv("MERGE_POLL_INTERVAL", "3"))

# 单次超时（秒）
HTTP_TIMEOUT = float(os.getenv("MERGE_HTTP_TIMEOUT", "10"))

# 最大等待时间（秒），超时则标记失败
MAX_WAIT_SECONDS = float(os.getenv("MERGE_MAX_WAIT_SECONDS", "3600"))


# ──────────────────── 内存存储 ────────────────────

_merges: dict[str, MergeTaskInfo] = {}


# ──────────────────── 请求 / 响应模型 ────────────────────

class MergeRequest(BaseModel):
    task_ids: Union[str, list[str]] = Field(..., description="提取服务返回的任务ID列表或列表字符串（兼容 Dify 数组/字符串两种形式）")
    pdf_name: str = Field(..., description="PDF名称(无后缀)，需与提取时一致")
    output_dir: str = Field(default="./output", description="输出根目录")
    extraction_service_url: Optional[str] = Field(
        default=None,
        description="提取服务地址（不传则用环境变量或默认值）",
    )


class MergeResponse(BaseModel):
    success: bool
    message: str
    merge_id: str
    task_ids: list[str]
    status: str


class MergeListResponse(BaseModel):
    total: int
    merges: list[MergeTaskInfo]


# ──────────────────── 提取服务客户端 ────────────────────

async def fetch_task_status(
    task_id: str,
    extraction_base_url: str = EXTRACTION_SERVICE_BASE_URL,
) -> Optional[ExtractionTaskInfo]:
    """调用提取服务 API 查询单个任务状态。"""
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        try:
            resp = await client.get(f"{extraction_base_url}/task/{task_id}")
            if resp.status_code == 200:
                return ExtractionTaskInfo(**resp.json())
            elif resp.status_code == 404:
                _app_logger.warning(f"[Poll] 任务不存在: {task_id}")
                return None
            else:
                _app_logger.error(f"[Poll] 查询任务 {task_id} 失败: HTTP {resp.status_code}")
                return None
        except httpx.ConnectError:
            _app_logger.error(f"[Poll] 无法连接提取服务: {extraction_base_url}")
            return None
        except Exception as e:
            _app_logger.error(f"[Poll] 查询任务 {task_id} 异常: {e}")
            return None


async def wait_for_all_tasks(
    task_ids: list[str],
    extraction_base_url: str,
) -> tuple[bool, list[ExtractionTaskInfo]]:
    """
    轮询所有提取任务直到全部完成或失败。

    返回: (是否全部成功, 所有任务的最新状态列表)
    """
    start_time = time.time()
    pending = set(task_ids)
    results: dict[str, ExtractionTaskInfo] = {}

    _app_logger.info(f"[Poll] 开始轮询 {len(task_ids)} 个提取任务...")
    _app_logger.info(f"[Poll] 提取服务地址: {extraction_base_url}")
    _app_logger.info(f"[Poll] 轮询间隔: {POLL_INTERVAL}s, 最大等待: {MAX_WAIT_SECONDS}s")

    while pending:
        elapsed = time.time() - start_time
        if elapsed > MAX_WAIT_SECONDS:
            _app_logger.error(f"[Poll] 超过最大等待时间 {MAX_WAIT_SECONDS}s，停止轮询")
            # 收集当前已有结果
            for tid in list(pending):
                status = await fetch_task_status(tid, extraction_base_url)
                if status:
                    results[tid] = status
            remaining = [results.get(tid) for tid in task_ids if tid in results]
            return False, remaining

        for tid in list(pending):
            status = await fetch_task_status(tid, extraction_base_url)
            if status is None:
                continue  # 连接失败，下次重试

            results[tid] = status

            if status.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                pending.discard(tid)
                state = "成功" if status.success else "失败"
                _app_logger.info(
                    f"[Poll] 任务 {tid} ({status.image_filename}) → {status.status} [{state}]"
                )

        if pending:
            count_done = len(task_ids) - len(pending)
            _app_logger.info(
                f"[Poll] 进度: {count_done}/{len(task_ids)} 完成, "
                f"剩余 {len(pending)} 个任务仍在处理中..."
            )
            await asyncio.sleep(POLL_INTERVAL)

    final_results = [results[tid] for tid in task_ids]
    all_ok = all(r.status == TaskStatus.COMPLETED and r.success for r in final_results)
    return all_ok, final_results


# ──────────────────── 合并核心逻辑 ────────────────────

async def run_merge(
    merge_id: str,
    task_ids: list[str],
    pdf_name: str,
    output_dir: str,
    extraction_base_url: str,
) -> None:
    """执行完整的轮询→合并流程。"""
    merge_task = _merges[merge_id]
    output_path = Path(output_dir)

    try:
        # ── 阶段1：轮询等待所有提取任务完成 ──
        merge_task.status = "polling"
        merge_task.total_tasks = len(task_ids)

        poll_start = time.time()
        all_success, task_results = await wait_for_all_tasks(task_ids, extraction_base_url)
        poll_elapsed = round(time.time() - poll_start, 2)

        merge_task.poll_elapsed_seconds = poll_elapsed
        merge_task.completed_tasks = len(task_results)

        if not all_success:
            failed = [
                (t.task_id, t.image_filename, t.error or t.status)
                for t in task_results
                if t.status != TaskStatus.COMPLETED or not t.success
            ]
            merge_task.status = TaskStatus.FAILED
            merge_task.error = (
                f"以下提取任务未成功完成:\n" +
                "\n".join(f"  - {tid} ({fname}): {reason}" for tid, fname, reason in failed)
            )
            _app_logger.error(f"[{merge_id}] 合并终止: 存在失败的提取任务")
            return

        # ── 阶段2：按图片文件名严格排序后合并清洗 ──
        merge_task.status = "merging"
        _app_logger.info(f"[{merge_id}] 所有提取任务已完成，开始合并清洗...")

        merge_start = time.time()

        # 按 page_num 排序（page_num 对应原始图片文件名序号 XXX_01, XXX_02, ...）
        task_results_sorted = sorted(task_results, key=lambda t: t.page_num)

        _app_logger.info(f"[{merge_id}] 合并顺序（按原图片文件名序号）:")
        for t in task_results_sorted:
            _app_logger.info(f"  第{t.page_num}页: {t.image_filename} → {t.output_file}")

        # 执行合并（内部会读取各页输出文件并按页码严格排序）
        merge_meta = merge_page_results(pdf_name, output_path)

        merge_elapsed = round(time.time() - merge_start, 2)

        if merge_meta.get("status") != "ok":
            merge_task.status = TaskStatus.FAILED
            merge_task.error = merge_meta.get("error", "合并过程出错")
            _app_logger.error(f"[{merge_id}] 合并失败: {merge_task.error}")
            return

        # 构建逐页明细
        page_details = []
        skipped_set = set(merge_meta.get("skipped_pages", []))
        for t in task_results_sorted:
            is_skipped = t.page_num in skipped_set
            page_details.append(PageMergeDetail(
                page_num=t.page_num,
                image_filename=t.image_filename,
                output_file=t.output_file or "",
                status=t.status,
                success=bool(t.success),
                chars_before_clean=None,
                chars_after_clean=0 if is_skipped else None,
            ))

        # 更新合并任务状态与完整结果
        merge_task.status = TaskStatus.COMPLETED
        merge_task.merged_file = merge_meta["merged_file"]
        merge_task.total_chars = merge_meta["total_chars"]
        merge_task.effective_pages = merge_meta["effective_pages"]
        merge_task.skipped_pages = merge_meta.get("skipped_pages")
        merge_task.merge_elapsed_seconds = merge_elapsed
        merge_task.page_details = page_details

        _app_logger.info(f"\n{'='*50}")
        _app_logger.info(f"[{merge_id}] 合并清洗完成!")
        _app_logger.info(f"  合并文件: {merge_task.merged_file}")
        _app_logger.info(f"  有效页面: {merge_task.effective_pages}/{merge_task.total_tasks}")
        _app_logger.info(f"  总字符数: {merge_task.total_chars}")
        _app_logger.info(f"  轮询耗时: {poll_elapsed}s, 合并耗时: {merge_elapsed}s")
        if merge_task.skipped_pages:
            _app_logger.info(f"  跳过页面（参考文献）: {merge_task.skipped_pages}")
        _app_logger.info(f"{'='*50}")

        cleanup_merge_logger()
        
        # ── 阶段3：回调接口，上传合并结果 ──
        # TODO: 配置dify工作流回调地址
        #url = "http://192.168.43.15/triggers/webhook/BcnOp11BcryiJ4Aa1sJpNiA6"
        #url = "http://localhost/triggers/webhook/BcnOp11BcryiJ4Aa1sJpNiA6"
        url = "http://localhost/triggers/webhook-debug/BcnOp11BcryiJ4Aa1sJpNiA6"
        
        data = {
            "merge_id": merge_task.merge_id,
            "status": merge_task.status,
            "error": merge_task.error or "",
            "merged_file": merge_task.merged_file or "",
            "total_chars": str(merge_task.total_chars or 0),
            "effective_pages": str(merge_task.effective_pages or 0),
            "skipped_pages": merge_task.skipped_pages or [],
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(url, json=data)
            if resp.status_code != 200:
                _app_logger.error(f"[{merge_id}] 回调接口返回错误: {resp.status_code} {resp.text}")
            else:
                _app_logger.info(f"[{merge_id}] 回调接口调用成功: {resp.status_code}")
                
    except Exception as e:
        _app_logger.error(f"[{merge_id}] 合并过程异常: {type(e).__name__}: {e}", exc_info=True)
        merge_task.status = TaskStatus.FAILED
        merge_task.error = f"{type(e).__name__}: {e}"
        cleanup_merge_logger()


# ──────────────────── API 端点 ────────────────────

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "vlm-merge-clean"}


@app.post("/merge", response_model=MergeResponse)
async def create_merge(req: MergeRequest):
    """
    提交提取任务ID列表，启动后台合并+清洗流程。

    流程：
      1. 定期轮询提取服务，检查每个task_id的状态
      2. 待所有任务均为 completed + success=true 后
      3. 按原图片文件名顺序（XXX_01.md, XXX_02.md, ...）严格排序
      4. 执行多轮过程内容清洗（Pass 0~4）
      5. 输出合并后的最终 Markdown 文件
    """
    # task_ids 字段兼容字符串和列表两种形式
    if isinstance(req.task_ids, str):
        try:
            task_ids = ast.literal_eval(req.task_ids)
        except (ValueError, SyntaxError) as e:
            raise HTTPException(status_code=400, detail=f"task_ids 解析失败，需为合法 Python 列表字符串: {e}")
        if not isinstance(task_ids, list):
            raise HTTPException(status_code=400, detail="task_ids 解析后应为列表")
    else:
        task_ids = req.task_ids

    if not task_ids or len(task_ids) == 0:
        raise HTTPException(status_code=400, detail="task_ids 不能为空")

    extraction_url = req.extraction_service_url or EXTRACTION_SERVICE_BASE_URL

    # 快速校验：确认提取服务可达且任务存在
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        try:
            test_resp = await client.get(f"{extraction_url}/health")
            if test_resp.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"提取服务不可用: {extraction_url}",
                )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=502,
                detail=f"无法连接提取服务: {extraction_url}，请确认提取服务已启动",
            )

    pdf_stem = Path(req.pdf_name).stem
    output_path = Path(req.output_dir)
    page_dir = output_path / pdf_stem
    page_dir.mkdir(parents=True, exist_ok=True)
    setup_merge_logger(page_dir)

    merge_id = str(uuid.uuid4())

    merge_task = MergeTaskInfo(
        merge_id=merge_id,
        task_ids=task_ids,
        pdf_name=pdf_stem,
        output_dir=req.output_dir,
        status=TaskStatus.PENDING,
    )
    _merges[merge_id] = merge_task

    _app_logger.info(f"{'='*60}")
    _app_logger.info(f"合并+清洗服务 — 新任务")
    _app_logger.info(f"  合并ID: {merge_id}")
    _app_logger.info(f"  PDF名称: {pdf_stem} (原始: {req.pdf_name})")
    _app_logger.info(f"  关联提取任务数: {len(task_ids)}")
    _app_logger.info(f"  输出目录: {req.output_dir}")
    _app_logger.info(f"  提取服务: {extraction_url}")
    _app_logger.info(f"{'='*60}")

    # 后台执行合并流程
    asyncio.create_task(
        run_merge(
            merge_id=merge_id,
            task_ids=task_ids,
            pdf_name=pdf_stem,
            output_dir=req.output_dir,
            extraction_base_url=extraction_url,
        )
    )

    return MergeResponse(
        success=True,
        message=f"已提交合并任务，正在后台轮询 {len(task_ids)} 个提取任务",
        merge_id=merge_id,
        task_ids=task_ids,
        status=TaskStatus.PENDING,
    )


@app.get("/merge/{merge_id}", response_model=MergeTaskInfo)
async def get_merge(merge_id: str):
    """查询单个合并任务的状态和结果。"""
    merge_task = _merges.get(merge_id)
    if not merge_task:
        raise HTTPException(status_code=404, detail=f"合并任务不存在: {merge_id}")
    return merge_task


@app.get("/merges", response_model=MergeListResponse)
async def get_merges(pdf_name: Optional[str] = None):
    """
    查询所有合并任务。

    可选参数 pdf_name: 过滤指定PDF的合并任务。
    """
    all_merges = list(_merges.values())
    if pdf_name:
        all_merges = [m for m in all_merges if m.pdf_name == pdf_name]
    return MergeListResponse(total=len(all_merges), merges=all_merges)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="merge_service:app", host="0.0.0.0", port=8002, reload=True)
