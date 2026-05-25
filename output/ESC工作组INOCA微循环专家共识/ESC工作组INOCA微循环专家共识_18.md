---
extraction_strategy: 轻量提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "轻量提取"}
total_time_seconds: 20.67
page_num: 18
task_id: d99decf9-8da5-4fea-9b63-e66ef894cd41
---

根据您提供的图像内容及《医学指南文本提取提示词（轻量版）》规则，该页为**参考文献列表页**，应**整页删除**。

### 判断依据：
- 页面顶部标题为 **“Ischaemia with non-obstructive coronary arteries”**（属正文标题，但本页无正文内容）；
- 全页内容为编号文献条目（12–49），格式统一为：  
  `[序号]. 作者. 文章标题. 期刊名 年份;卷:起止页码.`  
  符合 **5.1.2 文末参考文献列表特征**；
- 所有条目均以数字编号开头（如 `12.`、`31.`），含作者、期刊、年份、页码等典型文献要素；
- 无任何正文段落、表格、图片或图注；
- 右侧有下载水印（“Downloaded from...”），属需删除的无关元信息；
- 页码“352a”位于右上角，属页脚信息，应删除。

### 处理结论：
✅ **整页跳过，不输出任何内容**。  
（依据规则：5.1.2 起始信号虽未显式出现“参考文献”标题，但满足第二层高置信度特征——80%以上行为编号文献条目，且含年份+期刊；无混入正文内容，故判定为纯参考文献页）

---  
如后续页面出现正文内容（如章节标题、段落、图注等），请继续提供图像，我将严格按规则提取。