---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 56.33
page_num: 14
task_id: 676ef9c3-8ccf-4d30-b4a1-ae01dce0d169
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

#### 图 3 Initial Assessment of Patients With Suspected ACS.

**自然语言概述**：  
该流程图描述了疑似急性冠脉综合征（ACS）患者的初始评估路径。从“病史与体格检查”开始，经“疑似ACS”判断后，立即进行10分钟内心电图（ECG）和肌钙蛋白（cTn）检测（均为Ⅰ类推荐）。根据是否为ST段抬高型心肌梗死（STEMI）分流：若为STEMI（YES），转入“再灌注治疗评估”（见第5节）；若非STEMI（NO），则进行系列ECG监测缺血及系列肌钙蛋白检测（hs-cTn于1–2 h或常规cTn于3–6 h，均为Ⅰ类推荐），随后进入临床决策路径（CDP）以定义风险。CDP将患者分为低危、中危，或符合非ST段抬高型心肌梗死（NSTEMI）/高危标准；后者需启动药物治疗（第4节）并评估是否行侵入性策略（第6.1节），同时持续进行死亡或复发缺血的动态风险评估（第3.1.3节）。

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
        - id: "node_3"
          type: process
          content: "ECG within 10 min (Class I)"
          recommendation: "Class I"
          color_hint: "green"
        - id: "node_4"
          type: process
          content: "Obtain cTn (Class I)"
          recommendation: "Class I"
          color_hint: "green"
        - id: "node_5"
          type: decision
          content: "STEMI"
          recommendation: ""
          color_hint: "white"
    - level_name: "Non-STEMI Pathway"
      nodes:
        - id: "node_6"
          type: process
          content: "Serial ECG to detect ischemia (Class I)"
          recommendation: "Class I"
          color_hint: "green"
        - id: "node_7"
          type: process
          content: "Serial cTn<br>hs-cTn at 1–2 h or<br>conventional cTn at 3–6 h (Class I)"
          recommendation: "Class I"
          color_hint: "green"
        - id: "node_8"
          type: process
          content: "CDP<br>Used to define risk*"
          recommendation: ""
          color_hint: "steelblue"
        - id: "node_9"
          type: outcome
          content: "Low risk"
          recommendation: ""
          color_hint: "lightgray"
        - id: "node_10"
          type: outcome
          content: "Intermediate risk"
          recommendation: ""
          color_hint: "lightgray"
        - id: "node_11"
          type: outcome
          content: "Criteria met for NSTEMI or high risk"
          recommendation: ""
          color_hint: "lightgray"
        - id: "node_12"
          type: process
          content: "1. Initiate medical therapy (Section 4)<br>2. Assess for invasive evaluation (Section 6.1)"
          recommendation: ""
          color_hint: "white"
        - id: "node_13"
          type: process
          content: "Ongoing risk assessment for death or recurrent ischemia (Section 3.1.3)"
          recommendation: ""
          color_hint: "white"
    - level_name: "STEMI Pathway"
      nodes:
        - id: "node_14"
          type: process
          content: "Evaluate for reperfusion therapy (Section 5)"
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
      to: "node_14"
      condition: "YES"
    - from: "node_5"
      to: "node_6"
      condition: "NO"
    - from: "node_6"
      to: "node_7"
      condition: ""
    - from: "node_7"
      to: "node_8"
      condition: ""
    - from: "node_8"
      to: "node_9"
      condition: ""
    - from: "node_8"
      to: "node_10"
      condition: ""
    - from: "node_8"
      to: "node_11"
      condition: ""
    - from: "node_11"
      to: "node_12"
      condition: ""
    - from: "node_12"
      to: "node_13"
      condition: ""
    - from: "node_6"
      to: "node_5"
      condition: "dashed line (re-evaluation loop)"
```

**图注说明**：  
Colors correspond to Class of Recommendation in Table 2. *Examples of evidence-based CDPs and definition of low, intermediate, and high risk as defined in the 2021 AHA/ACC/Multisociety Chest Pain Guideline. ACS indicates acute coronary syndromes; CDP, clinical decision pathway; cTn, cardiac troponin; hs-cTn, high-sensitivity cardiac troponin; NSTEMI, non–ST-segment elevation myocardial infarction; and STEMI, ST-segment elevation myocardial infarction. Adapted with permission from Gulati et al.¹³ Copyright 2021 American Heart Association, Inc., and American College of Cardiology Foundation.