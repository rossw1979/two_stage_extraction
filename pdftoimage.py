#!/usr/bin/env python3
"""
PDF 逐页转 PNG —— FastAPI HTTP 服务

依赖:
    pip install fastapi uvicorn pymupdf

启动服务:
    uvicorn pdftoimage:app --host 0.0.0.0 --port 8001

调用示例:
    POST /convert
    {
        "pdf_files": ["/path/to/a.pdf", "/path/to/b.pdf"],
        "output_dir": "./images",
        "dpi": 300
    }
"""

import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger("pdftoimage")
logger.setLevel(logging.INFO)

_console = logging.StreamHandler()
_console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(_console)

app = FastAPI(title="PDF 转 PNG 服务", version="1.0.0")


class ConvertRequest(BaseModel):
    pdf_files: list[str] = Field(..., description="PDF 文件路径列表（服务器本地绝对或相对路径）")
    output_dir: str = Field(default="./images", description="输出根目录")
    dpi: int = Field(default=300, ge=72, le=600, description="图片 DPI 分辨率")


# 兼容 multipart/form-data 提交
class ConvertFormRequest(BaseModel):
    pdf_files: str = Field(..., description="PDF 文件路径，多个文件用逗号分隔")
    output_dir: str = Field(default="./images", description="输出根目录")
    dpi: int = Field(default=300, ge=72, le=600, description="图片 DPI 分辨率")


class PdfResult(BaseModel):
    file_name: str
    status: str  # "success" | "error"
    message: str = ""
    png_file_path: list[str] = []


def convert_pdf_to_png(pdf_path: Path, output_dir: Path, dpi: int) -> dict:
    """将单个 PDF 的每一页转为 PNG，返回结果字典。"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError("缺少 pymupdf 依赖。请运行: pip install pymupdf")

    if not pdf_path.exists():
        return {
            "file_name": pdf_path.name,
            "status": "error",
            "message": f"文件不存在: {pdf_path}",
            "png_file_path": [],
        }

    # 按文件名（无后缀）创建子目录
    stem = pdf_path.stem
    page_dir = output_dir / stem
    page_dir.mkdir(parents=True, exist_ok=True)

    zoom = dpi / 72  # fitz 默认 72 DPI，zoom = 目标DPI / 72
    mat = fitz.Matrix(zoom, zoom)

    doc = fitz.open(str(pdf_path))
    png_paths = []

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=mat)
            png_name = f"{stem}_{page_num + 1:02d}.png"
            png_path = page_dir / png_name
            pix.save(str(png_path))
            png_paths.append(str(png_path))
    finally:
        doc.close()

    return {
        "file_name": pdf_path.name,
        "status": "success",
        "message": f"共转换 {len(png_paths)} 页",
        "png_file_path": png_paths,
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "pdftoimage"}


@app.post("/convert")
async def convert(
    pdf_files: Optional[str] = Form(default=None),
    output_dir: str = Form(default="./images"),
    dpi: int = Form(default=300, ge=72, le=600),
):
    """
    将一个或多个 PDF 文件逐页转换为 PNG 图片。

    支持 JSON body 和 multipart/form-data 两种提交方式。
    form-data 时 pdf_files 用逗号分隔多个路径。

    每个输出目录结构：
      {output_dir}/{pdf_stem}/
      ├── {pdf_stem}_01.png
      ├── {pdf_stem}_02.png
      └── ...
    """
    if not pdf_files:
        raise HTTPException(status_code=400, detail="pdf_files 不能为空")

    # 支持逗号分隔的路径列表
    file_paths = [p.strip() for p in pdf_files.split(",") if p.strip()]
    if not file_paths:
        raise HTTPException(status_code=400, detail="pdf_files 不能为空")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    results = []
    for pdf_path_str in file_paths:
        pdf_path = Path(pdf_path_str)
        print(f"转换文件: {pdf_path}")
        result = convert_pdf_to_png(pdf_path, out, dpi)
        results.append(PdfResult(**result))

    success_count = sum(1 for r in results if r.status == "success")
    fail_count = sum(1 for r in results if r.status == "error")

    return {
        "total": len(results),
        "success_count": success_count,
        "fail_count": fail_count,
        "results": [r.model_dump() for r in results],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="pdftoimage:app", host="0.0.0.0", port=8001, reload=True)
