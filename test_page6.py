#!/usr/bin/env python3
import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")
from _shared import extract_final_content
from pathlib import Path

filepath = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/医脉通】血小板糖蛋白Ⅱb／Ⅲa+受体拮抗剂在冠状动脉粥样硬化性心脏病治疗的中国专家共识(2016)/医脉通】血小板糖蛋白Ⅱb／Ⅲa+受体拮抗剂在冠状动脉粥样硬化性心脏病治疗的中国专家共识(2016)_6.md")
result = extract_final_content(filepath)

# 检查残留
residuals = [
    "[自我校验启动]",
    "✅ 整页结构预扫描完成",
    "- 主体为双栏排版",
    "- 左栏内容块（从上至下）",
    "- 右栏内容块（从上至下）",
    "- 页面底部",
    "—删除页眉",
    "—删除左下角",
    "—删除正文中的上标引用标记",
    "✅ 内容块边界确认",
    "✅ 排版顺序",
    "✅ 内容过滤执行",
    "✅ 数值与术语保真核查",
    "✅ 无表格、无公式、无流程图",
    "✅ 自我校验全部勾选通过",
    "—— 开始输出干净数字化副本",
    "- 所有剂量",
    "- 缩写",
    "- 推荐等级未出现",
]

print("Result first 500 chars:", result[:500])
print("\n--- Residual check ---")
for r in residuals:
    if r in result:
        print(f"RESIDUAL: {r!r}")
        # find context
        idx = result.index(r)
        start = max(0, idx - 50)
        end = min(len(result), idx + len(r) + 50)
        print(f"  Context: ...{result[start:end]}...")
