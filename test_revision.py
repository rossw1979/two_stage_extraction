#!/usr/bin/env python3
import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")
from _shared import extract_final_content
from pathlib import Path

filepath = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/医脉通】非ST段抬高型急性冠状动脉综合征基层诊疗指南（2019年）/医脉通】非ST段抬高型急性冠状动脉综合征基层诊疗指南（2019年）_1.md")
result = extract_final_content(filepath)

vlm_residuals = [
    "[自我校验复核]",
    "页眉页脚已删",
    "双栏顺序正确",
    "所有段落（含定义、流行病学、DOI、引用）均已提取",
    "无表格/流程图/公式",
    "上标引用",
    "规则五明确",
    "修正后",
    "重新输出修正版",
    "⚠️",
]

print("Result:")
print(result)
print("\n--- VLM Residual check ---")
found_any = False
for r in vlm_residuals:
    if r in result:
        print(f"RESIDUAL: {r!r}")
        found_any = True
if not found_any:
    print("✅ No VLM residuals found!")
