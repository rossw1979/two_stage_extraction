---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 123.37
page_num: 14
task_id: 2f698c89-1552-4757-a48a-33fc94287971
re_extracted: True
re_extract_focus: "修正YAML流程边关系：node_12应并行指向node_13、node_14和node_15，取消node_13→node_14及node_14→node_15的错误串行连接；同时规范node_8多行内容排版与推荐等级位置。"
review_needed: True
review_reason: "修正流程图边关系：Serial ECG与Serial cTn应为并列节点，均直接连至CDP，而非串行；同时删除图注中的版权元信息。"
---

#### 图 3 Initial Assessment of Patients With Suspected ACS.

**自然语言概述**：  
该流程图描述了疑似急性冠脉综合征（ACS）患者的初始评估路径。起始于“病史与体格检查”，随后判断是否为“疑似ACS”。若为疑似ACS，则需在10分钟内完成心电图（ECG）并检测肌钙蛋白（cTn），均为Ⅰ类推荐。根据ECG结果判断是否为ST段抬高型心肌梗死（STEMI）：  
- 若为STEMI（YES），进入“再灌注治疗评估”（见第5节）；  
- 若非STEMI（NO），则进行系列ECG以检出缺血（Ⅰ类）及系列肌钙蛋白检测（hs-cTn于1–2 h或常规cTn于3–6 h，Ⅰ类），之后进入临床决策路径（CDP）用于风险分层。  
CDP将患者分为低危、中危，或符合非ST段抬高型心肌梗死（NSTEMI）/高危标准者。后者需：① 启动药物治疗（第4节）；② 评估是否需侵入性策略（第6.1节）。所有患者均需持续进行死亡或复发缺血的风险评估（第3.1.3节）。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Initial Assessment of Patients With Suspected ACS"
  levels:
    - level_name: "Initial Evaluation"
      nodes:
        - id: "node_1"
          type: process
          content: "History and Physical Examination"
          recommendation: ""
          color_hint: "lightblue"
    - level_name: "Diagnosis"
      nodes:
        - id: "node_2"
          type: decision
          content: "Suspected ACS"
          recommendation: ""
          color_hint: "steelblue"
    - level_name: "Immediate Testing"
      nodes:
        - id: "node_3"
          type: process
          content: "ECG within 10 min (Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
        - id: "node_4"
          type: process
          content: "Obtain cTn (Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
    - level_name: "STEMI Assessment"
      nodes:
        - id: "node_5"
          type: decision
          content: "STEMI"
          recommendation: ""
          color_hint: "white"
        - id: "node_6"
          type: process
          content: "Evaluate for reperfusion therapy (Section 5)"
          recommendation: ""
          color_hint: "white"
        - id: "node_7"
          type: process
          content: "Serial ECG to detect ischemia (Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
        - id: "node_8"
          type: process
          content: "Serial cTn<br>hs-cTn at 1–2 h or<br>conventional cTn at 3–6 h (Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
    - level_name: "Risk Stratification"
      nodes:
        - id: "node_9"
          type: process
          content: "CDP<br>Used to define risk*"
          recommendation: ""
          color_hint: "steelblue"
        - id: "node_10"
          type: outcome
          content: "Low risk"
          recommendation: ""
          color_hint: "lightblue"
        - id: "node_11"
          type: outcome
          content: "Intermediate risk"
          recommendation: ""
          color_hint: "lightblue"
        - id: "node_12"
          type: decision
          content: "Criteria met for NSTEMI or high risk"
          recommendation: ""
          color_hint: "lightblue"
    - level_name: "Management"
      nodes:
        - id: "node_13"
          type: process
          content: "1. Initiate medical therapy (Section 4)"
          recommendation: ""
          color_hint: "white"
        - id: "node_14"
          type: process
          content: "2. Assess for invasive evaluation (Section 6.1)"
          recommendation: ""
          color_hint: "white"
        - id: "node_15"
          type: process
          content: "Ongoing risk assessment for death or recurrent ischemia (Section 3.1.3)"
          recommendation: ""
          color_hint: "white"
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
      condition: "YES"
    - from: "node_5"
      to: "node_7"
      condition: "NO"
    - from: "node_7"
      to: "node_8"
      condition: ""
    - from: "node_8"
      to: "node_9"
      condition: ""
    - from: "node_9"
      to: "node_10"
      condition: ""
    - from: "node_9"
      to: "node_11"
      condition: ""
    - from: "node_9"
      to: "node_12"
      condition: ""
    - from: "node_12"
      to: "node_13"
      condition: ""
    - from: "node_12"
      to: "node_14"
      condition: ""
    - from: "node_12"
      to: "node_15"
      condition: ""
```

**图注说明**：  
Colors correspond to Class of Recommendation in Table 2. *Examples of evidence-based CDPs and definition of low, intermediate, and high risk as defined in the 2021 AHA/ACC/Multisociety Chest Pain Guideline. ACS indicates acute coronary syndromes; CDP, clinical decision pathway; cTn, cardiac troponin; hs-cTn, high-sensitivity cardiac troponin; NSTEMI, non–ST-segment elevation myocardial infarction; and STEMI, ST-segment elevation myocardial infarction. Adapted with permission from Gulati et al.¹³ Copyright 2021 American Heart Association, Inc., and American College of Cardiology Foundation.