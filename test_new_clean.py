#!/usr/bin/env python3
"""测试新变体的清洗效果"""
import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")
from _shared import strip_all_process_content

test_input = """\
[整页结构预扫描完成]

页面为双栏排版（左栏、右栏），无表格、无流程图/决策树、无公式。

- **左栏内容**：
  1. 第一段（起始为“0.001) 比伐卢定组均低于肝素组…”）→ 含统计值（RR=2.89等）及2013 ACC/AHA STEMI指南引述；
  2. “治疗建议: 接受直接 PCI 的 STEMI 患者…” → 四条编号建议（①–④）；
  3. “(2) 不稳定型心绞痛和非 ST 段抬高型心肌梗死” → 二级标题；
- **右栏内容**：
  1. 第一段（起始为“已经预先行双联抗血小板药物治疗的上述患者…”）→ 含2015 ESC指南、Valgimigli等研究；
  - 无其他角落文字。

开始按规则逐块提取（严格左栏→右栏顺序，删除水印/页眉/页脚/上标引用）：

---

0.001) 比伐卢定组均低于肝素组，但30 d内支架内血栓发生率比伐卢定组高于肝素组

治疗建议：接受直接 PCI 的 STEMI 患者无论是否置入支架
"""

result = strip_all_process_content(test_input)
print("=" * 60)
print("CLEANED OUTPUT:")
print("=" * 60)
print(result)
print("=" * 60)

# 检查是否有残留
residual_keywords = [
    "[整页结构预扫描完成]",
    "页面为双栏排版",
    "- **左栏内容**",
    "- **右栏内容**",
    "→ 含",
    "开始按规则逐块提取",
    "无其他角落文字",
]
has_residual = False
for kw in residual_keywords:
    if kw in result:
        print(f"RESIDUAL FOUND: {kw!r}")
        has_residual = True
if not has_residual:
    print("✅ No residuals found!")

# Also test on the actual merged output file
from pathlib import Path
merged_path = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/医脉通】血小板糖蛋白Ⅱb／Ⅲa+受体拮抗剂在冠状动脉粥样硬化性心脏病治疗的中国专家共识(2016)/医脉通】血小板糖蛋白Ⅱb／Ⅲa+受体拮抗剂在冠状动脉粥样硬化性心脏病治疗的中国专家共识(2016)_merged_output.md")
if merged_path.exists():
    text = merged_path.read_text(encoding="utf-8")
    cleaned = strip_all_process_content(text)
    print("\n" + "=" * 60)
    print("ACTUAL MERGED OUTPUT TEST:")
    print("=" * 60)
    found = []
    for kw in residual_keywords:
        if kw in cleaned:
            found.append(kw)
    if found:
        print(f"❌ Residuals found: {found}")
    else:
        print("✅ No residuals found in actual merged output!")
    # Show context around page 5
    lines = cleaned.splitlines()
    for i, line in enumerate(lines):
        if "第 5 页" in line or (i > 0 and "第 5 页" in lines[i-1]):
            print(f"\nContext around page 5 (lines {i}-{i+10}):")
            for j in range(i, min(i+15, len(lines))):
                print(f"  {j}: {lines[j]}")
            break
