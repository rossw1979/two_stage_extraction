#!/usr/bin/env python3
"""测试增强后的清洗逻辑效果 - 扩展检测范围"""

import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")

from _shared import extract_final_content
from pathlib import Path

# 测试文件列表
test_files = [
    "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/急性ST段抬高型心肌梗死诊断和治疗指南2019/急性ST段抬高型心肌梗死诊断和治疗指南2019_2.md",
    "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/急性ST段抬高型心肌梗死诊断和治疗指南2019/急性ST段抬高型心肌梗死诊断和治疗指南2019_10.md",
    "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/经皮冠状动脉介入治疗指南（2025）/经皮冠状动脉介入治疗指南（2025）_10.md",
    "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/老年人心脑血管病和糖尿病共病管理中国专家共识2023/老年人心脑血管病和糖尿病共病管理中国专家共识2023_3.md",
]

# 扩展的残留检测规则
def check_residuals(text: str) -> list[str]:
    issues = []
    lines = text.splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        # 内容块相关
        if "内容块分布如下" in s:
            issues.append("残留: 内容块分布描述")
        if re.search(r'^\s*-\s*\*\*(?:左|右)栏内容块', s):
            issues.append("残留: 左/右栏内容块枚举")
        if re.search(r'^\s*-\s*\*\*主标题\*\*', s):
            issues.append("残留: 主标题描述")
        if re.search(r'^\s*-\s*(?:主体内容|页面底部|页面顶部|无表格|无流程图|无公式|无图片|无水印)', s):
            issues.append("残留: 页面结构描述")
        if re.search(r'^\s*\d+\.\s*(?:段落|标题|子标题|首段|表|图)', s) and ('（' in s or '含' in s or '接' in s):
            issues.append("残留: 内容块枚举编号项")
        # 自我校验相关
        if "自我校验启动" in s:
            issues.append("残留: 自我校验启动")
        if "自我校验完成" in s:
            issues.append("残留: 自我校验完成")
        if "校验通过，开始输出" in s:
            issues.append("残留: 校验通过标记")
        if "[输出结束]" in s:
            issues.append("残留: 输出结束标记")
        # 修正版相关
        if "修正版（删除所有上标引用标记）" in s:
            issues.append("残留: 修正版标记")
        # 处理说明相关
        if "内容完整性核验补充说明" in s:
            issues.append("残留: 内容完整性核验补充说明")
        if "页脚与水印处理说明" in s:
            issues.append("残留: 页脚与水印处理说明")
        if "页眉/页脚处理说明" in s:
            issues.append("残留: 页眉/页脚处理说明")
        # 页面描述相关
        if re.search(r'右上角页码|左上角|右下角|左下角.*→.*删除', s):
            issues.append("残留: 页面角落删除描述")
        if re.search(r'页面为\*\*[^*]+\*\*排版', s):
            issues.append("残留: 页面排版描述")
        # 参考文献
        if re.search(r'^#{1,4}\s*参\s*考\s*文\s*献', s):
            issues.append("残留: 参考文献标题")
        # 整页结构预扫描
        if re.search(r'^✅\s*整页结构预扫描', s):
            issues.append("残留: 整页结构预扫描")
        if re.search(r'^✅\s*所有内容块已识别', s):
            issues.append("残留: 内容块已识别标记")
        if re.search(r'^-?\s*→\s*确认无遗漏', s):
            issues.append("残留: 确认无遗漏标记")
    return issues

import re

print("=" * 60)
print("清洗逻辑增强后测试 v2")
print("=" * 60)

all_clean = True
for filepath in test_files:
    fp = Path(filepath)
    if not fp.exists():
        print(f"\n[跳过] 文件不存在: {filepath}")
        continue

    result = extract_final_content(fp)
    print(f"\n{'='*60}")
    print(f"文件: {fp.name}")
    print(f"{'='*60}")

    if result is None:
        print("  → 被识别为参考文献页，跳过")
        continue

    issues = check_residuals(result)
    print(f"  字符数: {len(result)}")

    if issues:
        all_clean = False
        unique_issues = list(dict.fromkeys(issues))  # 去重保持顺序
        print(f"  问题 ({len(unique_issues)}项):")
        for issue in unique_issues:
            print(f"    - {issue}")
    else:
        print("  状态: 无过程内容残留")

    # 输出前200字符作为预览
    preview = result[:200].replace('\n', ' ')
    print(f"  预览: {preview}...")

print(f"\n{'='*60}")
if all_clean:
    print("全部测试通过，无过程内容残留")
else:
    print("存在残留问题，需进一步修复")
print("=" * 60)
