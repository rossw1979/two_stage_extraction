#!/usr/bin/env python3
"""
分阶段 VLM 提取流水线 —— 两阶段/三阶段动态策略

依赖:
    pip install openai

使用:
    export QWEN_API_KEY="your-api-key"
    export QWEN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

    # 两阶段（ Scout → Extract ）
    python run_two_stage_extraction.py --image ./page_3_300dpi.png --output ./result.md

    # 三阶段（ Scout → Extract → Verify ）
    python run_two_stage_extraction.py --image ./page_3_300dpi.png --output ./result.md --verify

    # 强制使用指定策略
    python run_two_stage_extraction.py --image ./page_3_300dpi.png --output ./result.md --force-strategy full
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


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


def call_vlm(messages: list, model: str, api_key: str, base_url: str, max_tokens: int = 4096) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        print("错误：缺少 openai 依赖。请运行: pip install openai")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
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
    """从 VLM 输出中解析 JSON，兼容代码块包裹的情况"""
    raw = raw.strip()
    if raw.startswith("```"):
        # 去掉 markdown 代码块标记
        lines = raw.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines)
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        print(f"[警告] Scout JSON 解析失败: {e}")
        print(f"原始输出:\n{raw[:500]}")
        # 兜底：返回一个保守的默认值，强制走标准提取
        return {"recommendation": "标准提取", "tables": {"count": 1}}


def scout_phase(image_path: str, model: str, api_key: str, base_url: str, prompt_dir: Path) -> dict:
    """阶段1：结构侦察"""
    print("\n[阶段1/3] Scout —— 结构侦察...")
    start = time.time()

    system_prompt = load_prompt(prompt_dir / "scout_prompt.md")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [build_image_message(image_path)]},
    ]
    raw = call_vlm(messages, model, api_key, base_url, max_tokens=512)
    elapsed = time.time() - start

    result = parse_scout_result(raw)
    print(f"  Scout 耗时: {elapsed:.2f}s")
    print(f"  判断结果: {result.get('recommendation', '未知')}")
    print(f"  页面布局: {result.get('page_layout', '未知')}")
    print(f"  表格数量: {result.get('tables', {}).get('count', 0)}")
    return result


def extract_phase(
    image_path: str,
    strategy: str,
    model: str,
    api_key: str,
    base_url: str,
    prompt_dir: Path,
) -> str:
    """阶段2：按需提取"""
    print(f"\n[阶段2/3] Extract —— 使用策略: {strategy}...")
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
    result = call_vlm(messages, model, api_key, base_url, max_tokens=16384)
    elapsed = time.time() - start
    print(f"  Extract 耗时: {elapsed:.2f}s")
    return result


def verify_phase(
    image_path: str,
    scout_result: dict,
    extract_result: str,
    model: str,
    api_key: str,
    base_url: str,
) -> str:
    """阶段3：定向校验（可选）"""
    print("\n[阶段3/3] Verify —— 定向校验...")
    start = time.time()

    # 构造校验 prompt
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
    raw = call_vlm(messages, model, api_key, base_url, max_tokens=1024)
    elapsed = time.time() - start
    print(f"  Verify 耗时: {elapsed:.2f}s")

    try:
        result = parse_scout_result(raw)
    except Exception:
        result = {"issues": [], "needs_re_extract": False}

    issues = result.get("issues", [])
    if issues:
        print(f"  发现问题 {len(issues)} 个:")
        for issue in issues:
            print(f"    [{issue.get('severity', '?')}] {issue.get('location', '?')}: {issue.get('problem', '')}")
    else:
        print("  未发现问题，提取结果可用。")

    return result


def main():
    parser = argparse.ArgumentParser(description="分阶段 VLM 提取流水线")
    parser.add_argument("--image", required=True, help="输入图片路径")
    parser.add_argument("--output", required=True, help="输出 markdown 文件路径")
    parser.add_argument("--prompt-dir", default=".", help="提示词文件所在目录（默认当前目录）")
    parser.add_argument("--model", default="qwen3-vl-plus", help="模型名称")
    #parser.add_argument("--api-key", default=os.environ.get("QWEN_API_KEY"), help="API Key")
    parser.add_argument("--api-key", default=os.getenv("QWEN_API_KEY"), help="API Key")
    parser.add_argument("--base-url", default=os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"), help="API Base URL")
    parser.add_argument("--verify", action="store_true", help="启用阶段3定向校验")
    parser.add_argument("--force-strategy", choices=["轻量提取", "标准提取", "完整提取"], help="强制使用指定策略，跳过 Scout 阶段")
    args = parser.parse_args()

    if not args.api_key:
        print("错误：未提供 API Key。请设置环境变量 QWEN_API_KEY 或使用 --api-key 参数。")
        sys.exit(1)

    prompt_dir = Path(args.prompt_dir)
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"错误：图片不存在: {image_path}")
        sys.exit(1)

    total_start = time.time()

    # ========== 阶段1: Scout ==========
    if args.force_strategy:
        scout_result = {"recommendation": args.force_strategy, "tables": {"count": 1}}
        print(f"\n[阶段1/3] Scout 已跳过，强制策略: {args.force_strategy}")
    else:
        scout_result = scout_phase(
            str(image_path), args.model, args.api_key, args.base_url, prompt_dir
        )

    strategy = scout_result.get("recommendation", "标准提取")
    # 保守兜底：如果推荐轻量但页面有表格，至少走标准
    if strategy == "轻量提取" and scout_result.get("tables", {}).get("count", 0) > 0:
        strategy = "标准提取"
        print(f"  保守修正: 页面含表格，策略提升为 标准提取")

    # ========== 阶段2: Extract ==========
    extract_result = extract_phase(
        str(image_path), strategy, args.model, args.api_key, args.base_url, prompt_dir
    )

    # ========== 阶段3: Verify (可选) ==========
    verify_result = None
    if args.verify:
        verify_result = verify_phase(
            str(image_path), scout_result, extract_result, args.model, args.api_key, args.base_url
        )

    total_elapsed = time.time() - total_start

    # ========== 保存结果 ==========
    output_path = Path(args.output)
    meta = f"""---
extraction_strategy: {strategy}
scout_result: {json.dumps(scout_result, ensure_ascii=False)}
total_time_seconds: {total_elapsed:.2f}
---

"""
    output_path.write_text(meta + extract_result, encoding="utf-8")

    print(f"\n{'='*40}")
    print(f"总耗时: {total_elapsed:.2f}s")
    print(f"使用策略: {strategy}")
    print(f"结果已保存: {output_path}")
    if verify_result and verify_result.get("issues"):
        print(f"校验警告: 发现 {len(verify_result['issues'])} 个问题")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()
