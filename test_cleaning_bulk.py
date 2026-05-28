#!/usr/bin/env python3
"""批量测试清洗逻辑效果"""

import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")

from _shared import extract_final_content
from pathlib import Path
import re

OUTPUT_DIR = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output")

# 收集所有单页 md 文件
all_page_files = sorted(OUTPUT_DIR.rglob("*_*.md"))
# 排除 merged_output 和 error 文件
all_page_files = [
    f for f in all_page_files
    if not f.name.endswith("_merged_output.md")
    and not f.name.endswith("_error.txt")
]

print(f"共发现 {len(all_page_files)} 个单页提取文件")
print("=" * 60)

# 统计
stats = {
    "total": len(all_page_files),
    "reference_skipped": 0,
    "empty": 0,
    "clean": 0,
    "has_residual": 0,
}

residual_patterns = [
    ("内容块分布", r'内容块分布如下'),
    ("左/右栏内容块", r'^\s*-\s*\*\*(?:左|右)栏内容块'),
    ("主标题描述", r'^\s*-\s*\*\*主标题\*\*'),
    ("页面结构描述", r'^\s*-\s*(?:主体内容|页面底部|页面顶部|无表格|无流程图|无公式|无图片|无水印)'),
    ("内容块枚举", r'^\s*\d+\.\s*(?:段落|标题|子标题|首段|表|图).*（'),
    ("自我校验启动", r'\[自我校验启动\]'),
    ("自我校验完成", r'\[自我校验完成\]'),
    ("校验通过", r'\[校验通过，开始输出\]'),
    ("输出结束", r'\[输出结束\]'),
    ("修正版标记", r'修正版.*删除所有上标引用标记'),
    ("内容完整性核验", r'内容完整性核验补充说明'),
    ("页脚与水印", r'页脚与水印处理说明'),
    ("页眉/页脚处理", r'页眉/页脚处理说明'),
    ("页面角落删除", r'(?:右上角|左上角|右下角|左下角).*→.*删除'),
    ("页面排版描述", r'页面为\*\*[^*]+\*\*排版'),
    ("参考文献标题", r'^#{1,4}\s*参\s*考\s*文\s*献'),
    ("整页结构预扫描", r'^✅\s*整页结构预扫描'),
    ("内容块已识别", r'^✅\s*所有内容块已识别'),
    ("确认无遗漏", r'^-?\s*→\s*确认无遗漏'),
]

residual_samples = {}

for fp in all_page_files:
    result = extract_final_content(fp)
    if result is None:
        stats["reference_skipped"] += 1
        continue
    if not result.strip():
        stats["empty"] += 1
        continue

    has_residual = False
    lines = result.splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        for name, pattern in residual_patterns:
            if re.search(pattern, s):
                has_residual = True
                if name not in residual_samples:
                    residual_samples[name] = (fp.name, s)
                break
        if has_residual:
            break

    if has_residual:
        stats["has_residual"] += 1
    else:
        stats["clean"] += 1

print(f"\n统计结果:")
print(f"  总文件数:     {stats['total']}")
print(f"  参考文献跳过: {stats['reference_skipped']}")
print(f"  空内容:       {stats['empty']}")
print(f"  清洗完全:     {stats['clean']}")
print(f"  仍有残留:     {stats['has_residual']}")
print(f"  清洗率:       {stats['clean'] / max(1, stats['total'] - stats['reference_skipped'] - stats['empty']) * 100:.1f}%")

if residual_samples:
    print(f"\n残留类型样本 ({len(residual_samples)} 种):")
    for name, (fname, sample) in residual_samples.items():
        print(f"  [{name}] {fname}: {sample[:80]}...")

print("\n" + "=" * 60)
