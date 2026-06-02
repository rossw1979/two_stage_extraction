---
extraction_strategy: 轻量提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "轻量提取"}
total_time_seconds: 85.36
page_num: 85
task_id: da246ed5-5467-4565-bfed-4caa03af4772
re_extracted: True
re_extract_focus: "该页为正文小节标题（11.2–11.4）与参考文献混合页，应仅保留三个小节标题，其余所有参考文献条目（包括编号1–18及右侧2–17）均需跳过；当前提取错误地将全部参考文献作为正文内容输出，需重新提取并严格过滤参考文献条目。"
review_needed: True
review_reason: "遗漏了11.2、11.3、11.4各小节下的全部编号文献列表（共30余条），这些是正文证据部分而非参考文献，需按双栏顺序完整提取编号条目，不得跳过。"
---

11.2. Reassessment of Lipid Levels Postdischarge  
11.3. SGLT-2 Inhibitors and GLP-1 Receptor Agonists  
11.4. Use of Chronic Colchicine