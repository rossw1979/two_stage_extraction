---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "图片", "position": "中央", "complexity": "高"}, {"type": "表格", "position": "左下", "complexity": "低"}], "tables": {"count": 1, "max_rows_estimate": 14, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "标准提取"}
total_time_seconds: 119.83
page_num: 2
task_id: ed6e2d3c-996c-40f7-af70-775acc100e91
re_extracted: True
re_extract_focus: "修正YAML流程图边关系逻辑（endotypes应并列引出、management三项为并列非串联），将缩写表转为Markdown表格格式，并删除右侧下载水印"
review_needed: False
review_reason: ""
---

This consensus document, a summary of the views of an expert panel organized by the European Association of Percutaneous Cardiovascular Interventions (EAPCI), appraises the importance of ischaemia with non-obstructive coronary arteries (INOCA). Angina pectoris affects approximately 112 million people globally. Up to 70% of patients undergoing invasive angiography do not have obstructive coronary artery disease, more common in women than in men, and a large proportion have INOCA as a cause of their symptoms. INOCA patients present with a wide spectrum of symptoms and signs that are often misdiagnosed as non-cardiac leading to under-diagnosis/investigation and under-treatment. INOCA can result from heterogeneous mechanism including coronary vasospasm and microvascular dysfunction and is not a benign condition. Compared to asymptomatic individuals, INOCA is associated with increased incidence of cardiovascular events, repeated hospital admissions, as well as impaired quality of life and associated increased health care costs. This consensus document provides a definition of INOCA and guidance to the community on the diagnostic approach and management of INOCA based on existing evidence from research and best available clinical practice; noting gaps in knowledge and potential areas for further investigation.

### Graphical Abstract

#### 图 1 Ischaemia with non obstructive coronary arteries (INOCA)

**自然语言概述**：  
该流程图系统呈现了INOCA的诊断路径与表型分类及管理策略。诊断分为非侵入性评估与侵入性评估两大路径；非侵入性评估包括患者评估及功能影像（±冠状动脉CT血管成像）；侵入性评估包括侵入性冠状动脉造影、FCA血流储备分数/腺苷试验及FCA血管反应性（ACH试验）。根据评估结果，可识别三种INOCA表型：心外膜型血管痉挛性心绞痛、微血管性心绞痛、微血管性合并心外膜型血管痉挛性心绞痛。三者为并列关系，共同导向三大并列管理措施：1. 生活方式干预；2. 危险因素管理；3. 抗心绞痛药物治疗。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Ischaemia with non obstructive coronary arteries (INOCA)"
  levels:
    - level_name: "Definition & Context"
      nodes:
        - id: "def_1"
          type: process
          content: "Coronary Microvascular dysfunction (CMD)/Vasospastic angina (VSA)"
    - level_name: "Non-invasive evaluation"
      nodes:
        - id: "ni_1"
          type: process
          content: "Step 1: Patient evaluation"
        - id: "ni_2"
          type: process
          content: "Step 2: Non-invasive evaluation"
          items:
            - "Functional Imaging"
            - "± Coronary CT Angiography"
    - level_name: "Invasive evaluation"
      nodes:
        - id: "i_1"
          type: process
          content: "Step 1: Invasive Coronary angiography"
        - id: "i_2"
          type: process
          content: "Step 2: FCA guidewire and Adenosine test"
        - id: "i_3"
          type: process
          content: "Step 3: FCA Vasoreactivity (ACH test)"
    - level_name: "INOCA Endotypes"
      nodes:
        - id: "end_1"
          type: process
          content: "Epicardial Vasospastic Angina"
        - id: "end_2"
          type: process
          content: "Microvascular Angina"
        - id: "end_3"
          type: process
          content: "Microvascular And Epicardial Vasospastic Angina"
    - level_name: "Management of INOCA"
      nodes:
        - id: "mgt_1"
          type: process
          content: "1. Lifestyle factors"
        - id: "mgt_2"
          type: process
          content: "2. Risk factor management"
        - id: "mgt_3"
          type: process
          content: "3. Antianginal medications"
  edges:
    - from: "def_1"
      to: "ni_1"
    - from: "ni_1"
      to: "ni_2"
    - from: "ni_2"
      to: "i_1"
    - from: "i_1"
      to: "i_2"
    - from: "i_2"
      to: "i_3"
    - from: "i_3"
      to: "end_1"
    - from: "i_3"
      to: "end_2"
    - from: "i_3"
      to: "end_3"
    - from: "end_1"
      to: "mgt_1"
    - from: "end_1"
      to: "mgt_2"
    - from: "end_1"
      to: "mgt_3"
    - from: "end_2"
      to: "mgt_1"
    - from: "end_2"
      to: "mgt_2"
    - from: "end_2"
      to: "mgt_3"
    - from: "end_3"
      to: "mgt_1"
    - from: "end_3"
      to: "mgt_2"
    - from: "end_3"
      to: "mgt_3"
```

### Abbreviations

| 缩写 | 全称 |
|------|------|
| ACEis | Angiotensin-converting enzyme inhibitors |
| ACH | Acetylcholine |
| ARB | Angiotensin receptor blockade |
| ATP | Adenosine-5′-triphosphate |
| BP | blood pressure |
| CABG | Coronary artery bypass surgery |
| CAD | Coronary artery disease |
| CCS | Chronic coronary syndrome |
| CCTA | Coronary computed tomographic angiography |
| CFR | Coronary flow reserve |
| CFVR | Coronary flow velocity reserve |
| CMD | Coronary microvascular dysfunction |
| CVD | cardiovascular disease |
| COVADIS | Coronary Vasomotor Disorders International Study |
| EAPCI | European Association of Percutaneous Cardiovascular Interventions |
| EECP | Enhanced external counterpulsation |
| ESC | European Society of Cardiology |
| FCA | Invasive functional coronary angiography |
| FFR | Fractional flow reserve |