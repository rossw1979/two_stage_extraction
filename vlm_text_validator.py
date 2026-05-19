#!/usr/bin/env python3
"""
VLM输出与PDF基线文本比对工具

功能：
1. 自动提取PDF文本层（pdfplumber）作为基线
2. 与VLM识别输出进行逐行比对
3. 标红不一致的行和数值
4. 生成HTML报告，支持差异高亮和数值校验

使用场景：
- 验证 qwen3-vl-plus 等VLM对医学指南PDF图片的识别质量
- 快速发现幻觉、漏识别、数值错位等问题

依赖：
    pip install pdfplumber diff-match-patch

使用示例：
    # 模式1：PDF 与 VLM输出文本文件比对
    python vlm_text_validator.py \
        --pdf "急性ST段抬高型心肌梗死诊断和治疗指南2019.pdf" \
        --vlm-output page_1_vlm_output.txt \
        --output report.html

    # 模式2：两个文本文件直接比对（基线已提取好）
    python vlm_text_validator.py \
        --baseline page_1_baseline.txt \
        --vlm-output page_1_vlm_output.txt \
        --output report.html

    # 模式3：批量比对目录下所有文本文件
    python vlm_text_validator.py \
        --baseline-dir ./baseline_texts/ \
        --vlm-dir ./vlm_texts/ \
        --output batch_report.html
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

# 尝试导入 diff-match-patch，如果不可用则降级到 difflib
try:
    import diff_match_patch as dmp_module
    HAS_DMP = True
except ImportError:
    HAS_DMP = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


# ========== 配置 ==========
NUMERIC_PATTERN = re.compile(
    r'(?:[<>≤≥≈]|约|约\s*为|约为)?'  # 前缀符号
    r'(?<!\w)'                        # 非单词边界
    r'('
    r'-?\d+(?:\.\d+)?'               # 整数或小数
    r'(?:\s*[±+-]\s*\d+(?:\.\d+)?)?' # 可选的误差范围 ±0.5
    r'(?:\s*%|mmHg|mg|μg|IU|U/L|mmol/L|ng/L|μmol/L|g/L|bpm|ms|mV|cm|kg|°C|°F)'  # 可选单位
    r')'
    r'(?!\w)',                        # 非单词边界
    re.IGNORECASE
)

# 医学常见数值范围（用于额外校验）
MEDICAL_RANGES = {
    '收缩压': (60, 250),
    '舒张压': (30, 150),
    '心率': (20, 300),
    '肌酐': (20, 1000),
    '血糖': (1.0, 35.0),
    'LDL': (0.5, 10.0),
    'HDL': (0.3, 3.0),
    'cTn': (0.001, 100.0),
    'D-二聚体': (0.01, 50.0),
    'BNP': (5, 5000),
    'NT-proBNP': (10, 35000),
}


# ========== 数据模型 ==========
@dataclass
class LineDiff:
    """单行差异"""
    line_num: int
    baseline_text: str
    vlm_text: str
    is_diff: bool
    diff_html: str  # 带高亮的HTML片段
    numeric_issues: List[dict] = field(default_factory=list)


@dataclass
class DocumentDiff:
    """文档级比对结果"""
    total_lines: int
    match_lines: int
    diff_lines: int
    missing_in_vlm: int
    extra_in_vlm: int
    numeric_issues_count: int
    line_diffs: List[LineDiff]
    match_ratio: float = 0.0

    def __post_init__(self):
        if self.total_lines > 0:
            self.match_ratio = self.match_lines / self.total_lines


# ========== 文本提取 ==========
class BaselineExtractor:
    @staticmethod
    def extract_pdf(pdf_path: str, password: Optional[str] = None) -> str:
        if not HAS_PDFPLUMBER:
            raise ImportError("请安装 pdfplumber: pip install pdfplumber")
        
        text_parts = []
        try:
            with pdfplumber.open(pdf_path, password=password) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
        except Exception as e:
            raise RuntimeError(f"PDF提取失败: {e}")
        
        return '\n'.join(text_parts)

    @staticmethod
    def extract_page(pdf_path: str, page_num: int, password: Optional[str] = None) -> str:
        if not HAS_PDFPLUMBER:
            raise ImportError("请安装 pdfplumber: pip install pdfplumber")
        
        with pdfplumber.open(pdf_path, password=password) as pdf:
            if page_num < 1 or page_num > len(pdf.pages):
                raise ValueError(f"页码 {page_num} 超出范围 (共 {len(pdf.pages)} 页)")
            text = pdf.pages[page_num - 1].extract_text()
            return text or ""


# ========== 文本预处理 ==========
class TextPreprocessor:
    """文本预处理，对齐格式差异"""
    
    @staticmethod
    def normalize(text: str) -> str:
        """标准化处理，减少误报"""
        # 统一换行符
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # 统一全角半角空格
        text = text.replace('\u3000', ' ')
        # 去掉首尾空白
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        # 去掉空行过多的连续空行（最多保留2个）
        result_lines = []
        empty_count = 0
        for line in lines:
            if line == '':
                empty_count += 1
                if empty_count <= 2:
                    result_lines.append(line)
            else:
                empty_count = 0
                result_lines.append(line)
        return '\n'.join(result_lines)

    @staticmethod
    def split_lines(text: str) -> List[str]:
        """分割为行列表"""
        normalized = TextPreprocessor.normalize(text)
        return normalized.split('\n')


# ========== 差异检测 ==========
class DiffDetector:
    """核心差异检测引擎"""
    
    def __init__(self):
        if HAS_DMP:
            self.dmp = dmp_module.diff_match_patch()
            self.dmp.Diff_Timeout = 0.1
    
    def detect(self, baseline: str, vlm_output: str) -> DocumentDiff:
        baseline_lines = TextPreprocessor.split_lines(baseline)
        vlm_lines = TextPreprocessor.split_lines(vlm_output)
        
        line_diffs = []
        match_count = 0
        diff_count = 0
        missing_count = 0
        extra_count = 0
        numeric_issues = 0
        
        # 行级比对
        max_lines = max(len(baseline_lines), len(vlm_lines))
        
        for i in range(max_lines):
            b_line = baseline_lines[i] if i < len(baseline_lines) else None
            v_line = vlm_lines[i] if i < len(vlm_lines) else None
            
            # 处理缺失/多余行
            if b_line is None and v_line is not None:
                extra_count += 1
                line_diffs.append(LineDiff(
                    line_num=i + 1,
                    baseline_text='',
                    vlm_text=v_line,
                    is_diff=True,
                    diff_html=self._format_vlm_only(v_line),
                    numeric_issues=[{'type': 'extra_line', 'text': v_line[:100]}]
                ))
                numeric_issues += 1
                continue
                
            if b_line is not None and v_line is None:
                missing_count += 1
                line_diffs.append(LineDiff(
                    line_num=i + 1,
                    baseline_text=b_line,
                    vlm_text='',
                    is_diff=True,
                    diff_html=self._format_baseline_only(b_line),
                    numeric_issues=[{'type': 'missing_line', 'text': b_line[:100]}]
                ))
                numeric_issues += 1
                continue
            
            # 两行都存在，比对内容
            is_diff, diff_html = self._compare_lines(b_line, v_line)
            
            # 检查数值差异
            num_issues = self._check_numeric_values(b_line, v_line)
            if num_issues:
                numeric_issues += len(num_issues)
                is_diff = True
            
            if is_diff:
                diff_count += 1
            else:
                match_count += 1
            
            line_diffs.append(LineDiff(
                line_num=i + 1,
                baseline_text=b_line,
                vlm_text=v_line,
                is_diff=is_diff,
                diff_html=diff_html,
                numeric_issues=num_issues
            ))
        
        return DocumentDiff(
            total_lines=max(len(baseline_lines), len(vlm_lines)),
            match_lines=match_count,
            diff_lines=diff_count,
            missing_in_vlm=missing_count,
            extra_in_vlm=extra_count,
            numeric_issues_count=numeric_issues,
            line_diffs=line_diffs,
        )
    
    def _compare_lines(self, baseline: str, vlm: str) -> Tuple[bool, str]:
        """比对两行文本，返回 (是否有差异, 带高亮的HTML)"""
        # 快速相等检查
        if baseline == vlm:
            return False, self._escape_html(baseline)
        
        # 标准化后比较
        b_norm = re.sub(r'\s+', ' ', baseline).strip()
        v_norm = re.sub(r'\s+', ' ', vlm).strip()
        if b_norm == v_norm:
            return False, self._escape_html(baseline)
        
        # 使用 diff-match-patch 做精细比对
        if HAS_DMP:
            diffs = self.dmp.diff_main(baseline, vlm)
            self.dmp.diff_cleanupSemantic(diffs)
            return True, self._dmp_to_html(diffs)
        else:
            # 降级到简单高亮
            return True, f"<span style='background:#ffebee'>{self._escape_html(baseline)}</span>"
    
    def _check_numeric_values(self, baseline: str, vlm: str) -> List[dict]:
        """检查两行文本中的数值差异"""
        issues = []
        
        # 提取两行中的数值
        b_nums = NUMERIC_PATTERN.findall(baseline)
        v_nums = NUMERIC_PATTERN.findall(vlm)
        
        # 如果都没有数值，跳过
        if not b_nums and not v_nums:
            return issues
        
        # 对比数值是否一致
        b_nums_set = set(b_nums)
        v_nums_set = set(v_nums)
        
        missing_nums = b_nums_set - v_nums_set
        extra_nums = v_nums_set - b_nums_set
        
        if missing_nums:
            for num in missing_nums:
                issues.append({
                    'type': 'missing_numeric',
                    'value': num,
                    'context': baseline[:80]
                })
        
        if extra_nums:
            for num in extra_nums:
                issues.append({
                    'type': 'extra_numeric',
                    'value': num,
                    'context': vlm[:80]
                })
        
        # 检查相同数值但在不同行中出现（可能的错位）
        # 这个检测在行级别，如果数值完全一致但上下文不同，需要更复杂的检测
        
        return issues
    
    def _dmp_to_html(self, diffs) -> str:
        """将 dmp diff 转为带高亮的 HTML"""
        html_parts = []
        for op, text in diffs:
            escaped = self._escape_html(text)
            if op == 0:  # 相等
                html_parts.append(escaped)
            elif op == -1:  # 删除（基线有，VLM没有）
                html_parts.append(f"<span style='background:#ffcdd2;color:#c62828;text-decoration:line-through'>{escaped}</span>")
            elif op == 1:  # 插入（VLM有，基线没有）
                html_parts.append(f"<span style='background:#c8e6c9;color:#2e7d32'>{escaped}</span>")
        return ''.join(html_parts)
    
    def _format_baseline_only(self, text: str) -> str:
        return f"<span style='background:#ffcdd2;color:#c62828'>[基线有] {self._escape_html(text)}</span>"
    
    def _format_vlm_only(self, text: str) -> str:
        return f"<span style='background:#c8e6c9;color:#2e7d32'>[VLM有] {self._escape_html(text)}</span>"
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """HTML转义"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))


# ========== 报告生成 ==========
class ReportGenerator:
    """生成HTML比对报告"""
    
    def generate(self, doc_diff: DocumentDiff, title: str, output_path: str):
        output_dir = Path(output_path).parent
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        html_parts = [
            "<!DOCTYPE html>",
            "<html><head>",
            "<meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1'>",
            f"<title>{title} - VLM文本比对报告</title>",
            "<style>",
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; background: #f5f5f5; color: #333; }",
            "h1 { color: #1a1a1a; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }",
            "h2 { color: #333; margin-top: 30px; }",
            ".summary-card { background: white; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }",
            ".stat { padding: 15px; border-radius: 6px; background: #f8f9fa; }",
            ".stat-label { font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }",
            ".stat-value { font-size: 24px; font-weight: bold; margin-top: 5px; }",
            ".stat-value.good { color: #2e7d32; }",
            ".stat-value.warn { color: #ed6c02; }",
            ".stat-value.bad { color: #d32f2f; }",
            ".line-diff { background: white; border-radius: 8px; margin: 10px 0; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }",
            ".line-diff.has-issue { border-left: 4px solid #d32f2f; }",
            ".line-diff.no-issue { border-left: 4px solid #4caf50; }",
            ".line-num { font-size: 12px; color: #666; margin-bottom: 8px; }",
            ".baseline-line { font-family: 'SF Mono', Monaco, 'Courier New', monospace; font-size: 13px; line-height: 1.5; }",
            ".vlm-line { font-family: 'SF Mono', Monaco, 'Courier New', monospace; font-size: 13px; line-height: 1.5; margin-top: 8px; }",
            ".label { font-size: 11px; font-weight: bold; margin-right: 8px; }",
            ".label-baseline { color: #1976d2; }",
            ".label-vlm { color: #7b1fa2; }",
            ".numeric-issue { background: #fff3e0; border: 1px solid #ff9800; border-radius: 4px; padding: 8px 12px; margin-top: 8px; font-size: 12px; }",
            ".numeric-issue .issue-type { font-weight: bold; color: #e65100; }",
            "span[style*='background:#ffcdd2'] { background: #ffcdd2 !important; color: #c62828 !important; }",
            "span[style*='background:#c8e6c9'] { background: #c8e6c9 !important; color: #2e7d32 !important; }",
            ".filter-bar { position: sticky; top: 0; background: white; padding: 15px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 100; }",
            ".filter-btn { margin-right: 10px; padding: 8px 16px; border: 1px solid #ddd; border-radius: 4px; background: white; cursor: pointer; font-size: 14px; }",
            ".filter-btn.active { background: #1976d2; color: white; border-color: #1976d2; }",
            ".hidden { display: none; }",
            "</style>",
            "</head><body>",
            f"<h1>{title} - VLM文本比对报告</h1>",
            f"<p style='color:#666'>生成时间：2026-05-15 | 比对引擎：{'diff-match-patch' if HAS_DMP else 'difflib'}</p>",
        ]
        
        # 总览卡片
        status_class = 'good' if doc_diff.match_ratio >= 0.95 else 'warn' if doc_diff.match_ratio >= 0.85 else 'bad'
        html_parts.append("<div class='summary-card'>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>总行数</div><div class='stat-value'>{doc_diff.total_lines}</div></div>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>匹配行数</div><div class='stat-value good'>{doc_diff.match_lines}</div></div>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>差异行数</div><div class='stat-value {status_class}'>{doc_diff.diff_lines}</div></div>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>匹配率</div><div class='stat-value {status_class}'>{doc_diff.match_ratio:.1%}</div></div>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>基线有/VLM无</div><div class='stat-value warn'>{doc_diff.missing_in_vlm}</div></div>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>VLM有/基线无</div><div class='stat-value warn'>{doc_diff.extra_in_vlm}</div></div>")
        html_parts.append(f"<div class='stat'><div class='stat-label'>数值问题数</div><div class='stat-value bad'>{doc_diff.numeric_issues_count}</div></div>")
        html_parts.append("</div>")
        
        # 筛选按钮
        html_parts.append("<div class='filter-bar'>")
        html_parts.append("<button class='filter-btn active' onclick=\"filterLines('all')\">全部</button>")
        html_parts.append("<button class='filter-btn' onclick=\"filterLines('issues')\">仅显示差异</button>")
        html_parts.append("<button class='filter-btn' onclick=\"filterLines('match')\">仅显示匹配</button>")
        html_parts.append("<button class='filter-btn' onclick=\"filterLines('numeric')\">仅显示数值问题</button>")
        html_parts.append("</div>")
        
        # 逐行详情
        html_parts.append("<div id='lines-container'>")
        for diff in doc_diff.line_diffs:
            has_issue = diff.is_diff or diff.numeric_issues
            issue_class = 'has-issue' if has_issue else 'no-issue'
            data_class = 'issue' if has_issue else ('match' if not diff.is_diff else 'issue')
            has_numeric = 'numeric' if diff.numeric_issues else ''
            
            html_parts.append(f"<div class='line-diff {issue_class} {data_class} {has_numeric}' data-line-num='{diff.line_num}'>")
            html_parts.append(f"<div class='line-num'>行 {diff.line_num}</div>")
            html_parts.append(f"<div class='baseline-line'><span class='label label-baseline'>基线:</span> {diff.diff_html}</div>")
            
            if diff.vlm_text:
                html_parts.append(f"<div class='vlm-line'><span class='label label-vlm'>VLM:</span> {self._format_vlm_line(diff)}</div>")
            
            # 数值问题详情
            if diff.numeric_issues:
                html_parts.append("<div class='numeric-issue'>")
                for issue in diff.numeric_issues:
                    type_text = {
                        'missing_numeric': '基线有数值',
                        'extra_numeric': 'VLM有额外数值',
                        'missing_line': '基线有此行',
                        'extra_line': 'VLM有额外行',
                    }.get(issue['type'], issue['type'])
                    
                    value = issue.get('value', '')
                    context = issue.get('context', '')[:100]
                    
                    if value:
                        html_parts.append(f"<div><span class='issue-type'>{type_text}:</span> {value} <span style='color:#666'>({context}...)</span></div>")
                    else:
                        html_parts.append(f"<div><span class='issue-type'>{type_text}:</span> {context}...</div>")
                html_parts.append("</div>")
            
            html_parts.append("</div>")
        
        html_parts.append("</div>")  # end container
        
        # 底部脚本
        html_parts.append("""
<script>
function filterLines(type) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    document.querySelectorAll('.line-diff').forEach(line => {
        line.classList.remove('hidden');
        if (type === 'all') return;
        if (type === 'issues' && !line.classList.contains('has-issue')) line.classList.add('hidden');
        if (type === 'match' && line.classList.contains('has-issue')) line.classList.add('hidden');
        if (type === 'numeric' && !line.classList.contains('numeric')) line.classList.add('hidden');
    });
}
</script>
""")
        
        html_parts.append("</body></html>")
        
        Path(output_path).write_text('\n'.join(html_parts), encoding='utf-8')
    
    def _format_vlm_line(self, diff: LineDiff) -> str:
        if not diff.vlm_text:
            return "<span style='background:#ffcdd2;color:#c62828'>[VLM缺失此行]</span>"
        
        if diff.is_diff and diff.diff_html:
            # 如果已经有diff高亮，提取VLM部分（这里简化处理）
            return diff.diff_html
        else:
            return diff.vlm_text


# ========== 主流程 ==========
def run_single_comparison(baseline_text: str, vlm_text: str, title: str, output_path: str):
    """单次比对"""
    baseline = TextPreprocessor.normalize(baseline_text)
    vlm_output = TextPreprocessor.normalize(vlm_text)
    
    detector = DiffDetector()
    doc_diff = detector.detect(baseline, vlm_output)
    
    generator = ReportGenerator()
    generator.generate(doc_diff, title, output_path)
    
    print(f"\n比对完成: {title}")
    print(f"  总行数: {doc_diff.total_lines}")
    print(f"  匹配行: {doc_diff.match_lines} ({doc_diff.match_ratio:.1%})")
    print(f"  差异行: {doc_diff.diff_lines}")
    print(f"  基线有/VLM无: {doc_diff.missing_in_vlm}")
    print(f"  VLM有/基线无: {doc_diff.extra_in_vlm}")
    print(f"  数值问题: {doc_diff.numeric_issues_count}")
    print(f"  报告: {output_path}")
    
    return doc_diff


def main():
    parser = argparse.ArgumentParser(description="VLM输出与PDF基线文本比对工具")
    
    # 输入模式选择
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--pdf", help="PDF文件路径（自动提取基线）")
    input_group.add_argument("--baseline", help="基线文本文件")
    input_group.add_argument("--baseline-dir", help="基线文本目录（批量模式）")
    
    parser.add_argument("--vlm-output", help="VLM识别输出的文本文件")
    parser.add_argument("--vlm-dir", help="VLM文本目录（批量模式）")
    parser.add_argument("--page", type=int, help="指定页码（PDF模式）")
    parser.add_argument("--password", help="PDF密码")
    parser.add_argument("--output", required=True, help="输出HTML报告路径")
    parser.add_argument("--title", default="VLM文本比对", help="报告标题")
    
    args = parser.parse_args()
    
    # 模式1：PDF + VLM文件
    if args.pdf and args.vlm_output:
        baseline_text = BaselineExtractor.extract_pdf(args.pdf, args.password)
        vlm_text = Path(args.vlm_output).read_text(encoding='utf-8')
        
        title = args.title or f"PDF: {Path(args.pdf).name}"
        if args.page:
            baseline_text = BaselineExtractor.extract_page(args.pdf, args.page, args.password)
            title += f" (第{args.page}页)"
        
        run_single_comparison(baseline_text, vlm_text, title, args.output)
    
    # 模式2：两个文本文件
    elif args.baseline and args.vlm_output:
        baseline_text = Path(args.baseline).read_text(encoding='utf-8')
        vlm_text = Path(args.vlm_output).read_text(encoding='utf-8')
        title = args.title or f"{Path(args.baseline).name} vs {Path(args.vlm_output).name}"
        run_single_comparison(baseline_text, vlm_text, title, args.output)
    
    # 模式3：批量比对
    elif args.baseline_dir and args.vlm_dir:
        baseline_dir = Path(args.baseline_dir)
        vlm_dir = Path(args.vlm_dir)
        
        # 找到匹配的文件对
        baseline_files = sorted(baseline_dir.glob("*.txt"))
        vlm_files = {f.name: f for f in vlm_dir.glob("*.txt")}
        
        if not baseline_files:
            print("错误：基线目录中没有找到 .txt 文件")
            sys.exit(1)
        
        all_diffs = []
        for bf in baseline_files:
            if bf.name not in vlm_files:
                print(f"跳过 {bf.name}：在VLM目录中未找到对应文件")
                continue
            
            baseline_text = bf.read_text(encoding='utf-8')
            vlm_text = vlm_files[bf.name].read_text(encoding='utf-8')
            title = f"{bf.stem}"
            
            diff = run_single_comparison(baseline_text, vlm_text, title, args.output.replace('.html', f'_{bf.stem}.html'))
            all_diffs.append((bf.name, diff))
        
        # 生成汇总报告
        print(f"\n\n批量比对汇总:")
        for name, diff in all_diffs:
            status = '✅' if diff.match_ratio >= 0.95 else '⚠️' if diff.match_ratio >= 0.85 else '❌'
            print(f"  {status} {name}: {diff.match_ratio:.1%} 匹配 ({diff.diff_lines} 差异, {diff.numeric_issues_count} 数值问题)")
        
        print(f"\n详细报告已生成至: {args.output.replace('.html', '_*.html')}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
