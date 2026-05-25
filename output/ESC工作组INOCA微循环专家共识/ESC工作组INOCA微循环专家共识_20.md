---
extraction_strategy: 轻量提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "轻量提取"}
total_time_seconds: 19.64
page_num: 20
task_id: 06499017-80c4-4cf1-b364-a5524a9c7095
---

根据您提供的图像内容及《医学指南文本提取提示词（轻量版）》规则，本页为**参考文献列表页**，应**全部删除**。

理由如下：

- 页面顶部标题为 **“Ischaemia with non-obstructive coronary arteries”**，属文章标题，非本页正文内容；
- 正文内容已结束（前页应为正文末段或图注等）；
- 本页从编号 **84.** 开始，至 **119.** 结束，全部为标准参考文献条目格式：
  - 以数字编号（含标点如 `84.`、`103.`）开头；
  - 包含作者全名、期刊名、年份、卷期、页码（如 *J Am Coll Cardiol 2018;72:2841–2855*）；
  - 符合规则 **5.1.2 文末参考文献列表** 的起始信号与条目特征；
- 右侧栏同样为连续文献条目（103–119），双栏均为文献，符合“双栏排版中左右栏同时出现文献条目时，整页跳过”；
- 页面右上角页码 `352c` 及右侧水印文字（“Downloaded from...”）属于需删除的页眉/水印信息；
- 无任何正文段落、表格、图片或图注混入（即无第三层保护兜底情形）。

✅ **处理结论**：  
**整页内容应全部跳过，不输出任何文本**。

（注：若此页上方紧接前一页末尾有未完成的正文段落或图注，请提供前一页图像以确保跨页延续内容被正确提取。）