#!/usr/bin/env python3
import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")
from _shared import extract_final_content
from pathlib import Path

filepath = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/医脉通】非ST段抬高型急性冠状动脉综合征基层诊疗指南（2019年）/医脉通】非ST段抬高型急性冠状动脉综合征基层诊疗指南（2019年）_1.md")
result = extract_final_content(filepath)

# 检测 VLM 残留（而非正文中的合法内容）
vlm_residuals = [
    "**内容块定位",
    "页眉左上角：",
    "页眉中部：",
    "主标题上方：",
    "编写单位与专家组：",
    "通信作者信息（三行",
    "7. 【关键词】行",
    "8. 英文标题及英文作者",
    "底部左侧：",
    "底部右侧：",
    "二维码（图像元素",
    "保留 DOI、收稿日期",
    "校验通过，开始输出",
    "排版判断",
    "本页为单页封面页",
    "四角检查：",
]

print("Result first 500 chars:", result[:500])
print("\n--- VLM Residual check ---")
found_any = False
for r in vlm_residuals:
    if r in result:
        print(f"RESIDUAL: {r!r}")
        found_any = True
if not found_any:
    print("✅ No VLM residuals found!")
