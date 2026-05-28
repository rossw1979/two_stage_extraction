#!/usr/bin/env python3
import sys
sys.path.insert(0, "/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction")
from _shared import (
    _skip_frontmatter, _strip_frontmatter_checklist,
    _find_body_content_marker, _find_content_start_after_separator,
    _remove_duplicate_revisions, _truncate_at_references,
    strip_all_process_content,
    _is_block_header, _is_block_inner_line, _is_body_signal, _looks_like_body_text,
    _GLOBAL_SWEEP_PATTERNS
)
from pathlib import Path
import re

filepath = Path("/Users/rossw/Downloads/projects/clinical-laboratory/two_stage_extraction/output/医脉通】血小板糖蛋白Ⅱb／Ⅲa+受体拮抗剂在冠状动脉粥样硬化性心脏病治疗的中国专家共识(2016)/医脉通】血小板糖蛋白Ⅱb／Ⅲa+受体拮抗剂在冠状动脉粥样硬化性心脏病治疗的中国专家共识(2016)_6.md")

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

body_start = _skip_frontmatter(lines)
body = lines[body_start:]
body = _strip_frontmatter_checklist(body)
full_text = "".join(body).strip()

marker_idx = _find_body_content_marker(body)
sep_idx = _find_content_start_after_separator(body)

if marker_idx >= 0:
    text_to_clean = "".join(body[marker_idx:]).strip()
elif sep_idx >= 0:
    text_to_clean = "".join(body[sep_idx:]).strip()
else:
    text_to_clean = full_text

text_to_clean = _remove_duplicate_revisions(text_to_clean)
text_to_clean = _truncate_at_references(text_to_clean)

# Now run strip_all_process_content step by step
print("=== Pass 0 ===")
lines_tc = text_to_clean.splitlines(True)
swept = []
for i, line in enumerate(lines_tc):
    stripped = line.strip()
    if not stripped:
        swept.append(line)
        continue
    matched = any(re.match(p, stripped) for p in _GLOBAL_SWEEP_PATTERNS)
    if matched:
        print(f"  Skip [{i}]: {stripped[:60]!r}")
        continue
    swept.append(line)
text = "".join(swept)

print("\n=== Pass 1 ===")
lines_p1 = text.splitlines(True)
for i, line in enumerate(lines_p1):
    s = line.strip()
    if not s:
        continue
    bh = _is_block_header(s)
    bi = _is_block_inner_line(s)
    bs = _is_body_signal(s)
    bt = _looks_like_body_text(s)
    if bh or bi or bs or bt or s == '---':
        flags = []
        if bh: flags.append("HEADER")
        if bi: flags.append("INNER")
        if bs: flags.append("BODY_SIG")
        if bt: flags.append("BODY_TXT")
        if s == '---': flags.append("SEP")
        print(f"  [{i}] {', '.join(flags)}: {s[:80]!r}")
