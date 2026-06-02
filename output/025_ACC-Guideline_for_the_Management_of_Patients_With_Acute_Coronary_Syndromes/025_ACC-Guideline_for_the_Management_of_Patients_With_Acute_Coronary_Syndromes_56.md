---
extraction_strategy: 标准提取
scout_result: {"page_layout": "混排", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}, {"type": "表格", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "左下（嵌套于段落下方）", "complexity": "中"}], "tables": {"count": 2, "max_rows_estimate": 6, "has_merged_cells": true, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 66.89
page_num: 56
task_id: af244532-a35e-42ee-9329-8702515f118c
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

#### 图 10 Core Components of Cardiac Rehabilitation.

**自然语言概述**：  
该流程图以环形拼图形式呈现心脏康复的核心组成模块，共9个相互衔接的组成部分，围绕中心标题“Core Components of Cardiac Rehabilitation”呈放射状排列。各模块按顺时针方向依次为：患者评估（Patient Assessment）、营养咨询（Nutrition Counseling）、体重管理（Weight Management）、血压管理（Blood Pressure Management）、血脂管理（Lipid Management）、糖尿病管理（Diabetes Management）、戒烟（Tobacco Cessation）、心理社会管理（Psychosocial Management）、体力活动咨询（Physical Activity Counseling）和运动训练（Exercise Training）。每个模块配以对应图标，体现其临床内涵。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Core Components of Cardiac Rehabilitation"
  levels:
    - level_name: "Core Components"
      nodes:
        - id: "node_1"
          type: process
          content: "Patient Assessment"
          items: []
          recommendation: ""
          color_hint: "yellow"
        - id: "node_2"
          type: process
          content: "Nutrition Counseling"
          items: []
          recommendation: ""
          color_hint: "red"
        - id: "node_3"
          type: process
          content: "Weight Management"
          items: []
          recommendation: ""
          color_hint: "green"
        - id: "node_4"
          type: process
          content: "Blood Pressure Management"
          items: []
          recommendation: ""
          color_hint: "blue"
        - id: "node_5"
          type: process
          content: "Lipid Management"
          items: []
          recommendation: ""
          color_hint: "pink"
        - id: "node_6"
          type: process
          content: "Diabetes Management"
          items: []
          recommendation: ""
          color_hint: "orange"
        - id: "node_7"
          type: process
          content: "Tobacco Cessation"
          items: []
          recommendation: ""
          color_hint: "dark_blue"
        - id: "node_8"
          type: process
          content: "Psychosocial Management"
          items: []
          recommendation: ""
          color_hint: "teal"
        - id: "node_9"
          type: process
          content: "Physical Activity Counseling"
          items: []
          recommendation: ""
          color_hint: "purple"
        - id: "node_10"
          type: process
          content: "Exercise Training"
          items: []
          recommendation: ""
          color_hint: "light_blue"
  edges:
    - from: "node_1"
      to: "node_2"
      condition: ""
    - from: "node_2"
      to: "node_3"
      condition: ""
    - from: "node_3"
      to: "node_4"
      condition: ""
    - from: "node_4"
      to: "node_5"
      condition: ""
    - from: "node_5"
      to: "node_6"
      condition: ""
    - from: "node_6"
      to: "node_7"
      condition: ""
    - from: "node_7"
      to: "node_8"
      condition: ""
    - from: "node_8"
      to: "node_9"
      condition: ""
    - from: "node_9"
      to: "node_10"
      condition: ""
    - from: "node_10"
      to: "node_1"
      condition: ""
```

**图注说明**：  
Figure 10. Core Components of Cardiac Rehabilitation.  
Adapted with permission from Sandesara et al.<sup>30</sup> Copyright 2015 American College of Cardiology Foundation.

---

### 11. DISCHARGE: LONG-TERM MANAGEMENT AND SECONDARY PREVENTION

#### 11.1. DAPT Strategies in the First 12 Months Postdischarge

**Recommendations for DAPT Strategies in the First 12 Months Postdischarge**  
Referenced studies that support recommendations are summarized in the Evidence Table.

| COR | LOE | Recommendations |
|-----|-----|----------------|
| 1   | A   | 1. In patients with ACS who are not at high bleeding risk, DAPT with aspirin and an oral P2Y12 inhibitor should be administered for at least 1 year to reduce MACE.<sup>1–6</sup> |

**Default Duration of DAPT**

| COR | LOE | Recommendations |
|-----|-----|----------------|
| 1   | A   | 2. In patients with ACS who have tolerated DAPT with ticagrelor, transition to ticagrelor monotherapy ≥1 month post PCI is useful to reduce bleeding risk.<sup>7–11</sup> |
| 1   | A   | 3. In patients at high risk of gastrointestinal bleeding, a proton pump inhibitor (PPI) is recommended in combination with DAPT, oral anticoagulants, or both to reduce risk of bleeding.<sup>12–15</sup> |
| 2b  | B-R | 4. In patients with ACS undergoing PCI, de-escalation of DAPT (switching from ticagrelor or prasugrel to clopidogrel) after 1 month may be reasonable to reduce bleeding risk.<sup>16–20</sup> |
| 2b  | B-R | 5. In patients with ACS undergoing PCI who are at high bleeding risk, transition to single antiplatelet therapy (aspirin or P2Y12 inhibitor) after 1 month may be reasonable to reduce bleeding risk.<sup>21</sup> |

*注：表格上方“Bleeding Reduction Strategies”为该子表标题，已整合至表格结构中；所有上标引用标记（如<sup>1–6</sup>）已按规则删除。*