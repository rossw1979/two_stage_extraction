#!/usr/bin/env python3
"""
汇总 result-1.md ~ result-17.md，仅保留最终输出内容，去除过程分析。
"""

import re
import os

# 标记「最终输出」开始的标题行
FINAL_OUTPUT_MARKERS = [
    "### **最终输出",
    "### **第四步",
    "### **第三步：最终输出",
    "### 📄 最终提取结果",
    "### 提取结果",
    "### 最终提取结果",
    "## 提取结果",
]

# 标记「过程内容」开始（遇到这些行时停止提取）
TRAILING_PROCESS_PATTERNS = [
    r'^### .*(?:自我校验|校验清单|勾选)',
    r'^### ✅',
    r'^✅\s*(?:全部通过|输出完毕|提取完成|校验)',
    r'^输出完毕',
    r'^提取完成',
    r'^- \[[ x]\].*整页结构已扫描',  # 校验清单项
]


def extract_final_content(filepath):
    """从单个 result 文件中提取最终输出内容，返回文本或 None（表示跳过）"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 1. 跳过 YAML frontmatter
    body_start = _skip_frontmatter(lines)
    body = lines[body_start:]
    full_text = "".join(body).strip()

    # 2. 参考文献页：跳过
    if _is_reference_page(full_text):
        return None

    # 3. 策略A：查找显式的「最终输出」分界标记
    final_start = _find_final_output_marker(body)
    if final_start >= 0:
        # 从标记处开始，找到内容结束位置（遇到尾部过程内容时停止）
        final_end = _find_content_end(body, final_start)
        result = "".join(body[final_start:final_end]).strip()
        return _clean_text(result)

    # 4. 策略B：无显式标记，启发式查找正文起始
    content_start = _find_content_start_heuristic(body)
    if content_start >= 0:
        final_end = _find_content_end(body, content_start)
        result = "".join(body[content_start:final_end]).strip()
        return _clean_text(result)

    # 5. 兜底：返回全部 body
    return _clean_text(full_text)


def _skip_frontmatter(lines):
    """跳过 YAML frontmatter，返回 body 起始行号"""
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return i + 1
    return 0


def _is_reference_page(text):
    """判断是否为参考文献页"""
    return bool(re.search(r'（本页为参考文献，已跳过）|(本页为参考文献，已跳过)', text))


def _find_final_output_marker(body):
    """查找「最终输出」标记在 body 中的索引，未找到返回 -1"""
    for i, line in enumerate(body):
        stripped = line.strip()
        for marker in FINAL_OUTPUT_MARKERS:
            if stripped.startswith(marker):
                return i
    return -1


def _find_content_end(body, start_idx):
    """
    从 start_idx 开始向后搜索，找到内容结束的位置。
    遇到尾部过程标记（校验清单、完成提示等）时停止。
    返回结束位置的索引（不包含该行）。
    """
    for i in range(start_idx, len(body)):
        stripped = body[i].strip()
        if not stripped:
            continue
        for pattern in TRAILING_PROCESS_PATTERNS:
            if re.match(pattern, stripped):
                return i
    return len(body)


def _find_content_start_heuristic(body):
    """启发式查找正文的起始行（用于无显式标记的文件）"""
    PROCESS_PREFIXES = [
        "我将严格按照", "以下为严格按图像内容提取",
        "- [ ] 整页结构", "- [x] 整页结构",
        "[ ] 整页结构", "[x] 整页结构",
        "### **第一步", "### **第二步",
        "### **整页结构预扫描", "### ✅",
        "### 整页内容块定位", "### 整页结构预扫描确认",
    ]

    SKIP_TITLES = ["预扫描", "逐块", "校验", "核对", "检查", "边界", "确认"]

    i = 0
    while i < len(body):
        line = body[i].strip()
        if not line:
            i += 1
            continue

        # 跳过已知的过程标记行
        is_process = any(line.startswith(p) or p in line for p in PROCESS_PREFIXES)

        # 跳过校验清单项
        if re.match(r'^- \[[ x]\]', line):
            is_process = True

        # 跳过页眉/页码说明
        if line.startswith(("**页码", "**期刊", "**页眉")):
            is_process = True

        # 跳过分隔线后紧跟的分析章节标题
        if line == "---" and i + 1 < len(body):
            next_line = body[i + 1].strip()
            if next_line.startswith(("### ", "## ", "#### ")):
                if any(t in next_line for t in SKIP_TITLES):
                    i += 2
                    continue

        if is_process:
            i += 1
            continue

        # 检查是否像正文内容
        if _looks_like_content(line):
            return i

        i += 1

    return 0


def _looks_like_content(line):
    """判断一行是否像正文内容而非分析标注"""
    # Markdown 标题（表/图/章节）
    if re.match(r'^(#{1,4}\s|\*\*[表图]\d|\*\*第)', line):
        return True

    # Markdown 表格
    if line.startswith("|") and "|" in line[1:]:
        return True

    # YAML / 代码块
    if line.startswith("```"):
        return True

    # 注释行
    if re.match(r'^(注[:：]|\\*\\*注)', line):
        return True

    # 中文开头的长段落 → 正文
    if len(line) > 15 and line and ord(line[0]) > 0x2E80:
        skip = ["页面", "左上角", "右上角", "左下角", "右下角",
               "确认", "注意", "⚠️", "✅", "🔍", "📌"]
        if not any(line.startswith(p) for p in skip):
            return True

    # 英文开头的段落（作者、利益冲突等）
    if re.match(r'^[A-Z]', line) and len(line) > 15:
        return True

    return False


def _clean_text(text):
    """清理提取结果文本"""
    # 去掉开头的「最终输出」标题行本身（保留其下的内容）
    text = re.sub(
        r'^#{1,6}\s+\*{1,2}最终输出[^*\n]*\*{0,2}\s*\n*', '', text, count=1
    )

    # 清理多余空行（最多保留2个连续空行）
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 去掉首尾空白
    text = text.strip()

    return text


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "merged_output.md")

    results = []
    skipped = []

    for i in range(1, 18):
        filepath = os.path.join(base_dir, f"result-{i}.md")
        if not os.path.exists(filepath):
            print(f"[跳过] {filepath} 不存在")
            continue

        content = extract_final_content(filepath)
        if content is None:
            skipped.append(i)
            print(f"[跳过] result-{i}.md → 参考文献页")
        elif content:
            results.append((i, content))
            print(f"[OK] result-{i}.md → 提取 {len(content)} 字符")
        else:
            print(f"[警告] result-{i}.md → 未提取到内容")

    # 写入合并文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 冠心病双联抗血小板治疗中国专家共识 —— 提取结果汇总\n\n")
        f.write("> 由 VLM 分阶段提取流水线自动生成，共处理 17 页。\n\n")
        f.write("---\n\n")

        for page_num, content in results:
            f.write(f"<!-- ===== 第 {page_num} 页 ===== -->\n\n")
            f.write(content)
            f.write("\n\n")

        if skipped:
            f.write(f"\n<!-- 备注：第 {skipped} 页为参考文献，已跳过 -->\n")

    total_chars = sum(len(c) for _, c in results)
    print(f"\n{'=' * 50}")
    print(f"合并完成！")
    print(f"  输出文件：{output_path}")
    print(f"  有效页面：{len(results)} / 17")
    print(f"  跳过页面（参考文献）：{skipped}")
    print(f"  总字符数：{total_chars}")


if __name__ == "__main__":
    main()
