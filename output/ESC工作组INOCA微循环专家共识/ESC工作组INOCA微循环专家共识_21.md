---
extraction_strategy: 轻量提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "低"}, {"type": "段落", "position": "右上", "complexity": "低"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "轻量提取"}
total_time_seconds: 15.10
page_num: 21
task_id: 7b168ecb-191b-424c-ad56-dfa038718649
---

根据您提供的医学指南文本提取提示词（轻量版）及当前图像页内容，该页为**参考文献列表页**，符合“5.1.2 文末参考文献列表（必须删除）”的起始信号与特征：

- 页面顶部无章节标题，仅有页码“3520d”和作者“V. Kunadian et al.”（属页眉信息，应删除）；
- 主体内容为编号从120至137的文献条目，每条均以 `[数字]` 开头，包含作者、题名、期刊、年份、卷期、页码等典型参考文献要素；
- 右侧有垂直水印文字“Downloaded from...”，属需删除的下载来源信息；
- 无任何正文段落、表格、图片或图注；
- 符合“第二层（特征验证）”：100% 行以 `[数字]` 开头，且全部含年份+期刊信息。

依据规则 **五、内容过滤 → 5.1.2**，该页应**整页删除**，不输出任何内容。

✅ 输出结果：  
（空）