#!/usr/bin/env python3
"""
跨页延续异常检测脚本

检测合并结果中可能存在的跨页延续/列顺序错乱问题：
1. 前一页末尾为不完整句子（无结尾标点）
2. 当前页开头为新章节标题
3. 当前页为双栏布局
4. 当前页中存在疑似承接前一页语义的段落

输出：可疑页面列表，供人工定向复核。
"""

import json
import re
from pathlib import Path
from typing import Optional

OUTPUT_DIR = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output")

# 章节标题检测模式
SECTION_HEADING_PATTERNS = [
    r'^重要技术\s*$',
    r'^(?:第[一二三四五六七八九十\d]+章|第[一二三四五六七八九十\d]+节)\s*',
    r'^(?:一|二|三|四|五|六|七|八|九|十)[、．.]\s*',
    r'^(?:\d+[、．.])?\s*(?:前言|引言|摘要|方法|结果|讨论|结论|参考文献)',
    r'^\d+\.\d+\s+',  # 如 "1.1 标题"
    r'^【?[一二三四五六七八九十]+】?\s*',  # 如 "一、" "【一】"
]

# 句末连接词/不完整信号（暗示句子未结束）
INCOMPLETE_ENDING_SIGNALS = [
    '时间', '对于', '因此', '此外', '同时', '如果', '当', '由于',
    '包括', '以及', '和', '或', '与', '的', '了', '在', '为',
    'min', 'h', 'd', 's',  # 时间单位后常接具体数值
]

# 结尾标点
ENDING_PUNCTUATION = {'。', '？', '！', '；', '.', '?', '!', ';', '"', '"', ''', ''', '）', ')', '」', '】', '>'}


def is_section_heading(text: str) -> bool:
    """判断文本是否为章节标题"""
    text = text.strip()
    if not text:
        return False
    for pattern in SECTION_HEADING_PATTERNS:
        if re.match(pattern, text):
            return True
    # 短文本且不含常规句子结构
    if len(text) <= 20 and not any(p in text for p in ENDING_PUNCTUATION):
        return True
    return False


def is_incomplete_sentence(text: str) -> tuple[bool, str]:
    """
    判断文本末尾是否为不完整句子。
    返回: (是否不完整, 原因)
    """
    text = text.strip()
    if not text:
        return False, "空文本"

    # 如果以明确的结尾标点结束，认为是完整的
    if any(text.endswith(p) for p in ENDING_PUNCTUATION):
        return False, "有结尾标点"

    # 如果以数字或单位结尾，可能是不完整的
    last_char = text[-1]
    if last_char.isdigit() or last_char in '＜<>≤≥%=~+-' or last_char in '一二三四五六七八九十':
        return True, f"以数字/符号/序数词'{last_char}'结尾"

    # 如果以连接词结尾
    for signal in INCOMPLETE_ENDING_SIGNALS:
        if text.endswith(signal):
            return True, f"以连接词/信号词'{signal}'结尾"

    # 默认认为是不完整的（无标点且不是明确结束）
    return True, "无结尾标点"


def get_page_layout(page_file: Path) -> Optional[str]:
    """从单页文件的 frontmatter 读取 page_layout"""
    if not page_file.exists():
        return None
    try:
        content = page_file.read_text(encoding="utf-8")
        # 解析 frontmatter 中的 scout_result
        match = re.search(r'scout_result:\s*(\{.*?\})\n', content, re.DOTALL)
        if match:
            scout_json = match.group(1)
            # 处理可能的换行
            scout_json = scout_json.replace('\n', ' ')
            scout_data = json.loads(scout_json)
            return scout_data.get("page_layout", "未知")
    except Exception:
        pass
    return None


def detect_review_needed_for_guideline(guideline_dir: Path) -> list[dict]:
    """检测单个指南中重提后仍需人工复核的页面"""
    guideline_name = guideline_dir.name
    review_files = list(guideline_dir.glob(f"{guideline_name}_*_review.md"))
    issues = []

    for review_file in review_files:
        try:
            # 从文件名提取页码，如 "指南名_5_review.md" -> 5
            stem = review_file.stem  # 去掉 .md
            page_num_str = stem.rsplit("_", 1)[0].rsplit("_", 1)[-1]
            page_num = int(page_num_str)

            content = review_file.read_text(encoding="utf-8")
            # 提取问题描述（第一行**之间的内容）
            match = re.search(r'\*\*问题描述\*\*：(.+)', content)
            reason = match.group(1).strip() if match else "未明确"

            issues.append({
                "guideline": guideline_name,
                "page": page_num,
                "issue_type": "review_needed",
                "severity": "高",
                "layout": "未知",
                "reason": reason,
                "review_file": str(review_file.name),
            })
        except Exception:
            continue

    return issues


def detect_issues_for_guideline(guideline_dir: Path) -> list[dict]:
    """检测单个指南中的可疑页面"""
    guideline_name = guideline_dir.name
    merged_file = guideline_dir / f"{guideline_name}_merged_output.md"
    if not merged_file.exists():
        return []

    content = merged_file.read_text(encoding="utf-8")

    # 分割页面
    page_pattern = r'<!-- ===== 第 (\d+) 页 ===== -->\n\n(.*?)\n\n(?=<!-- ===== 第 \d+ 页 ===== -->|\Z)'
    pages = re.findall(page_pattern, content, re.DOTALL)
    if not pages:
        # 尝试另一种分割方式
        page_pattern2 = r'<!-- ===== 第 (\d+) 页 ===== -->\n\n(.*?)\n?(?=<!-- ===== 第 \d+ 页 ===== -->|$)'
        pages = re.findall(page_pattern2, content, re.DOTALL)

    issues = []
    prev_page_last_para = ""
    prev_page_num = 0

    for page_num_str, page_content in pages:
        page_num = int(page_num_str)
        paragraphs = [p.strip() for p in page_content.split('\n\n') if p.strip()]
        if not paragraphs:
            continue

        first_para = paragraphs[0]
        last_para = paragraphs[-1] if paragraphs else ""

        # 检查当前页是否为双栏
        page_file = guideline_dir / f"{guideline_name}_{page_num}.md"
        layout = get_page_layout(page_file)

        # 检查前一页末尾是否不完整 + 当前页开头是否为新章节
        if prev_page_last_para and is_section_heading(first_para):
            incomplete, reason = is_incomplete_sentence(prev_page_last_para)
            if incomplete:
                issue = {
                    "guideline": guideline_name,
                    "page": page_num,
                    "issue_type": "跨页延续断裂",
                    "severity": "高" if layout == "双栏" else "中",
                    "layout": layout or "未知",
                    "prev_page_last_50chars": prev_page_last_para[-50:],
                    "current_page_first_line": first_para[:80],
                    "reason": reason,
                }

                # 额外检查：当前页后续段落中是否有疑似延续前一页的内容
                # 简单启发式：找不以章节标题开头、且语义上可能相关的段落
                for para in paragraphs[1:]:
                    if para and not is_section_heading(para):
                        # 如果段落以连接词或具体数值开头，可能是延续
                        if re.match(r'^(间[＜<]|因此|此外|同时|对于|如果|当|由于|包括|以及)', para):
                            issue["possible_continuation_found"] = para[:100]
                            issue["severity"] = "高"
                            break

                issues.append(issue)

        prev_page_last_para = last_para
        prev_page_num = page_num

    return issues


def main():
    all_crosspage_issues = []
    all_review_needed = []
    guideline_dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir() and d.name != "test"]

    print(f"开始扫描 {len(guideline_dirs)} 本指南...\n")

    for guideline_dir in sorted(guideline_dirs):
        # 检测跨页延续问题
        issues = detect_issues_for_guideline(guideline_dir)
        all_crosspage_issues.extend(issues)
        if issues:
            print(f"[{guideline_dir.name}] 跨页延续问题:")
            for issue in issues:
                sev = "🔴" if issue["severity"] == "高" else "🟡"
                print(f"  {sev} 第{issue['page']}页 [{issue['issue_type']}] 严重程度:{issue['severity']}")
                print(f"     布局: {issue['layout']}")
                print(f"     前页末尾: ...{issue['prev_page_last_50chars']}")
                print(f"     当前页首句: {issue['current_page_first_line']}")
                if issue.get("possible_continuation_found"):
                    print(f"     ⚠️ 疑似延续段落: {issue['possible_continuation_found']}")
                print()

        # 检测重提后仍需复核的页面
        reviews = detect_review_needed_for_guideline(guideline_dir)
        all_review_needed.extend(reviews)
        if reviews:
            print(f"[{guideline_dir.name}] 需人工复核页面:")
            for review in reviews:
                print(f"  🔴 第{review['page']}页 [review_needed] 严重程度:高")
                print(f"     问题: {review['reason']}")
                print()

    # 输出汇总报告
    high_crosspage = [i for i in all_crosspage_issues if i["severity"] == "高"]
    medium_crosspage = [i for i in all_crosspage_issues if i["severity"] == "中"]

    print("=" * 60)
    print(f"扫描完成。")
    print(f"\n跨页延续问题: {len(all_crosspage_issues)} 个可疑页面")
    print(f"  🔴 高危（需优先复核）: {len(high_crosspage)} 页")
    print(f"  🟡 中危（建议抽查）: {len(medium_crosspage)} 页")

    if all_review_needed:
        print(f"\n重提后仍需复核: {len(all_review_needed)} 个页面")
        for review in all_review_needed:
            print(f"  - {review['guideline']} / 第{review['page']}页: {review['reason']}")
    print()

    if high_crosspage:
        print("高危跨页延续页面清单：")
        for issue in high_crosspage:
            print(f"  - {issue['guideline']} / 第{issue['page']}页")
        print()

    # 写入详细报告文件
    report = {
        "crosspage_issues": all_crosspage_issues,
        "review_needed_pages": all_review_needed,
    }
    report_file = OUTPUT_DIR / "_crosspage_continuation_report.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"详细报告已保存至: {report_file}")


if __name__ == "__main__":
    main()
