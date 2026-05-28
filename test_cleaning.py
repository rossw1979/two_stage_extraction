#!/usr/bin/env python3
"""测试增强后的清洗逻辑效果"""

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

print("=" * 60)
print("清洗逻辑增强后测试")
print("=" * 60)

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

    # 检查残留问题
    issues = []
    if "内容块分布如下" in result:
        issues.append("残留: 内容块分布描述")
    if "左栏内容块" in result or "右栏内容块" in result:
        issues.append("残留: 左/右栏内容块枚举")
    if "自我校验启动" in result:
        issues.append("残留: 自我校验启动")
    if "自我校验完成" in result:
        issues.append("残留: 自我校验完成")
    if "修正版（删除所有上标引用标记）" in result:
        issues.append("残留: 修正版标记")
    if "内容完整性核验补充说明" in result:
        issues.append("残留: 内容完整性核验补充说明")
    if "页脚与水印处理说明" in result:
        issues.append("残留: 页脚与水印处理说明")
    if "页眉/页脚处理说明" in result:
        issues.append("残留: 页眉/页脚处理说明")
    if "校验通过，开始输出" in result:
        issues.append("残留: 校验通过标记")
    if "输出完毕" in result:
        issues.append("残留: 输出完毕标记")
    if "[✓] 整页结构已扫描" in result:
        issues.append("残留: ✓ 校验清单")
    if "- [x] 整页结构已扫描" in result:
        issues.append("残留: - [x] 校验清单")
    if "#### 参考文献" in result:
        issues.append("残留: 参考文献标题")

    if issues:
        print(f"  字符数: {len(result)}")
        print(f"  问题 ({len(issues)}项):")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print(f"  字符数: {len(result)}")
        print("  状态: 无过程内容残留")

    # 输出前300字符作为预览
    preview = result[:300].replace('\n', ' ')
    print(f"  预览: {preview}...")

print(f"\n{'='*60}")
print("测试完成")
print("=" * 60)
