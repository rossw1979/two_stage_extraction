---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "表格", "position": "中央", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 5, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 37.41
page_num: 10
task_id: e3b591bf-6599-43a6-84e4-0648ed48525d
---

#### 整页结构预扫描（执行中）

- 顶部标题：`Ischaemia with non-obstructive coronary arteries`（左上角）
- 页码：`3513`（右上角）
- 主体内容：单一大型表格（Table 2），占据页面主体
- 表格下方：脚注说明（3条，含上标 a, b, c 的解释）
- 右侧边栏：垂直水印文字（“Downloaded from https://academic.oup.com/... by Southern Medical University user on 25 October 2020”）——属下载信息，按规则**删除**
- 左下角/右下角：无独立段落；脚注位于表格正下方，已覆盖

✅ 确认无遗漏内容块：仅1个表格 + 3条脚注。无表格上方段落、无右栏、无角落独立文字

---

### Table 2 INOCA endotypes diagnostic criteria

| # | INOCA endotypes | Pathophysiology | Diagnostic criteria |
|---|------------------|-----------------|---------------------|
| 1 | Microvascular angina<sup>a</sup> | CMD | Diagnostic guidewire and Adenosine test<br>• FFR > 0.8<br>• CFR < 2.0<br>• IMR ≥ 25<sup>b</sup><br>• HMR ≥ 1.9<sup>b</sup><br>Vasoreactivity (acetylcholine test)<br>• No or <90% diameter reduction<br>• + angina<br>• + ischaemic ECG changes |
| 2 | Vasospastic angina | Epicardial spasm | Diagnostic guidewire and Adenosine test<br>• FFR > 0.8<br>• CFR ≥ 2.0<br>• IMR < 25<br>• HMR < 1.9<br>Vasoreactivity (acetylcholine test)<br>• ≥ 90% diameter reduction<br>• + angina<br>• + ischaemic ECG changes |
| 3 | Both microvascular and vasospastic angina | Both CMD and epicardial spasm | Diagnostic guidewire and Adenosine test<br>• FFR > 0.8<br>• CFR < 2.0<br>• IMR ≥ 25<br>• HMR ≥ 1.9<br>Vasoreactivity (acetylcholine test)<br>• No or <90% or ≥90% diameter reduction<br>• + angina<br>• + ischaemic ECG changes |
| 4 | Non-cardiac chest pain | None | Diagnostic guidewire and Adenosine test<br>• FFR > 0.8<br>• CFR ≥ 2.0<br>• IMR < 25<br>• HMR < 1.9<br>Vasoreactivity (acetylcholine test)<br>• No or <90% diameter reduction<br>• No angina<br>• No ischaemic ECG changes |
| 5 | Non-flow-limiting CAD<sup>c</sup> | Diffuse coronary artery atherosclerosis | Diagnostic guidewire and adenosine test<br>• FFR > 0.8<br>• CFR ≥ 2.0<br>• IMR < 25<br>• HMR < 1.9<br>Vasoreactivity (acetylcholine test)<br>• No or <90% diameter reduction<br>• No angina<br>• No ischaemic ECG changes |

---

**Footnotes:**

CAD, coronary artery disease; CFR, coronary flow reserve; FFR, fractional flow reserve; HMR, hyperaemic myocardial velocity resistance; IMR, index of microcirculatory resistance.

<sup>a</sup>Non endothelial dependent microvascular angina may be diagnosed non-invasively by the methods described.

<sup>b</sup>IMR and HMR values shown in table as alternative measures of microcirculatory resistance (based on thermodilution or Doppler, respectively).

<sup>c</sup>≤50% stenosis severity by visual assessment.

---

#### 自我校验（输出前逐项核对）

- [x] 整页结构已扫描，所有内容块（表格 + 3条脚注）已列出  
- [x] 页面四角检查完成：左上角标题、右上角页码、左下/右下无独立文字  
- [x] 表格上方无段落；表格标题已提取；表格下方脚注完整提取  
- [x] 单栏排版，无跨栏问题  
- [x] 表格行列无错位；单元格内多行用 `<br>` 分隔，无 HTML 样式标签  
- [x] 所有数值（FFR > 0.8、CFR < 2.0、IMR ≥ 25 等）逐字保真，单位与符号正确  
- [x] 上标 a/b/c 保留原格式，脚注内容完整对应  
- [x] 水印与下载信息已删除  
- [x] 无参考文献、无页眉页脚元信息残留  

✅ 提取完成，符合“干净的数字化副本”标准。