#!/usr/bin/env python3
"""批量重新合并所有已生成的指南提取结果，使用更新后的清洗逻辑。"""
import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")
from pathlib import Path
from _shared import merge_page_results

OUTPUT_DIR = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output")

# 所有已合并的指南目录
merged_files = sorted(OUTPUT_DIR.glob("*/*_merged_output.md"))
pdf_names = [f.stem.replace("_merged_output", "") for f in merged_files]

print(f"发现 {len(pdf_names)} 个已合并指南，开始重新合并...\n")

success = 0
failed = 0
for pdf_name in pdf_names:
    try:
        result = merge_page_results(pdf_name, OUTPUT_DIR)
        if result.get("status") == "ok":
            success += 1
            print(f"  ✅ {pdf_name}: {result['effective_pages']}/{result['total_pages']} 页有效")
        else:
            failed += 1
            print(f"  ⚠️ {pdf_name}: {result.get('status', 'unknown')}")
    except Exception as e:
        failed += 1
        print(f"  ❌ {pdf_name}: {e}")

print(f"\n完成: {success} 成功, {failed} 失败")
