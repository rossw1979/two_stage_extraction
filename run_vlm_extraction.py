#!/usr/bin/env python3
"""
VLM 提取脚本 —— 使用 prompt_v3_with_fewshot.md 对指定图片进行提取

依赖:
    pip install openai

使用:
    export QWEN_API_KEY="your-api-key"
    export QWEN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
    python run_vlm_extraction.py --image ./page_3_300dpi.png --output ./page_3_extracted.md

支持的模型:
    qwen-vl-plus、qwen-vl-max、qwen3-vl-plus 等
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path: str) -> str:
    """将图片转为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_messages(system_prompt: str, image_path: str) -> list:
    """构造 OpenAI 兼容的 messages"""
    base64_image = encode_image(image_path)
    # 支持常见图片格式
    ext = Path(image_path).suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")

    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime};base64,{base64_image}",
                        "detail": "high",  # 请求高清模式
                    },
                },
            ],
        },
    ]


def call_vlm(messages: list, model: str, api_key: str, base_url: str) -> str:
    """调用 VLM API"""
    try:
        from openai import OpenAI
    except ImportError:
        print("错误：缺少 openai 依赖。请运行: pip install openai")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    print(f"正在调用 {model} ...")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,
        temperature=0.0,  # 降低随机性，提高格式一致性
    )
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="使用 VLM 提取医学指南图像文本")
    parser.add_argument("--image", required=True, help="输入图片路径")
    parser.add_argument("--output", required=True, help="输出 markdown 文件路径")
    parser.add_argument(
        "--prompt",
        default="./prompt_v3_with_fewshot.md",
        help="系统提示词文件路径（默认: ./prompt_v3_with_fewshot.md）",
    )
    parser.add_argument(
        "--model",
        default="qwen3-vl-plus",
        help="模型名称（默认: qwen3-vl-plus）",
    )
    parser.add_argument(
        "--api-key",
        #default=os.environ.get("QWEN_API_KEY"),
        default=os.getenv("QWEN_API_KEY"),
        help="API Key（默认从环境变量 QWEN_API_KEY 读取）",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get(
            "QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
        ),
        help="API Base URL",
    )
    args = parser.parse_args()

    if not args.api_key:
        print("错误：未提供 API Key。请设置环境变量 QWEN_API_KEY 或使用 --api-key 参数。")
        sys.exit(1)

    # 读取提示词
    prompt_path = Path(args.prompt)
    if not prompt_path.exists():
        print(f"错误：提示词文件不存在: {prompt_path}")
        sys.exit(1)
    system_prompt = prompt_path.read_text(encoding="utf-8")

    # 读取图片
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"错误：图片不存在: {image_path}")
        sys.exit(1)

    # 构造请求
    messages = build_messages(system_prompt, str(image_path))

    # 调用 VLM
    result = call_vlm(
        messages=messages,
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url,
    )

    # 保存结果
    output_path = Path(args.output)
    output_path.write_text(result, encoding="utf-8")
    print(f"提取完成，结果已保存至: {output_path}")


if __name__ == "__main__":
    main()
