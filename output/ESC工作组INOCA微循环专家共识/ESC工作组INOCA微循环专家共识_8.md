---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 110.30
page_num: 8
task_id: f326b413-2943-42f1-9551-b509e146d949
re_extracted: True
re_extract_focus: "需修正图注与正文段落的边界划分，将'In the diagnostic pathway...'及后续小标题段落作为独立内容块提取；同时规范YAML中决策框的items结构与双向边表示方式。"
review_needed: True
review_reason: "遗漏了对跨页内容的正确截断：右下角标题及后续段落属于下一页正文，不应提取；同时左下与右下两个段落应严格按原图位置分离，避免合并为单一图注块。"
---

#### 图 3 Non-invasive evaluation of INOCA. GP, general practitioner.

**自然语言概述**：  
该流程图描述了INOCA（缺血性心肌病伴非阻塞性冠状动脉疾病）的非侵入性评估路径，分为两个主要步骤：Step 1为患者评估，Step 2为非侵入性评估。Step 1从患者症状出发，经全科医生（GP）初步评估后转诊至心内科；若ECG无诊断价值或正常，则需心内科转诊。Step 2根据临床可能性分层：高临床可能性者优先考虑功能性影像检查（含6种技术），低临床可能性者在满足特定条件时可考虑冠状动脉CT血管成像（CCTA）；功能性影像与CCTA之间为双向选择关系，取决于本地可行性。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Non-invasive evaluation of INOCA"
  levels:
    - level_name: "Step 1: Patient evaluation"
      nodes:
        - id: "patient"
          type: process
          content: "Patient"
          items: []
        - id: "symptoms"
          type: process
          content: "Ischaemic symptoms"
          items: []
        - id: "history_exam"
          type: process
          content: "History taking including risk factors\nPhysical examination"
          items: []
        - id: "convincing_history"
          type: process
          content: "Convincing ongoing history of cardiac ischaemia"
          items: []
        - id: "ecg"
          type: process
          content: "ECG – non-diagnostic/normal"
          items: []
        - id: "referral"
          type: process
          content: "Cardiology referral"
          items: []
        - id: "gp"
          type: process
          content: "GP"
          items: []
        - id: "cardiologist"
          type: process
          content: "Cardiologist"
          items: []
      edges:
        - from: "patient"
          to: "gp"
          condition: ""
        - from: "gp"
          to: "cardiologist"
          condition: ""
        - from: "patient"
          to: "symptoms"
          condition: ""
        - from: "symptoms"
          to: "history_exam"
          condition: ""
        - from: "history_exam"
          to: "convincing_history"
          condition: ""
        - from: "convincing_history"
          to: "ecg"
          condition: ""
        - from: "ecg"
          to: "referral"
          condition: ""

    - level_name: "Step 2: Non-invasive evaluation"
      nodes:
        - id: "high_likelihood_box"
          type: decision
          content: "Preferentially considered if:"
          items:
            - "High clinical likelihood"
            - "Revascularisation likely"
            - "Local expertise and availability"
            - "Viability assessment also required"
        - id: "functional_imaging"
          type: process
          content: "Functional imaging"
          items:
            - "Exercise Tolerance Test"
            - "Transthoracic Doppler Echocardiography"
            - "Myocardial Contrast Echocardiography"
            - "Myocardial Perfusion Imaging"
            - "Positron Emission Tomography"
            - "Cardiac Magnetic Resonance Imaging"
        - id: "low_likelihood_box"
          type: decision
          content: "Preferentially considered if:"
          items:
            - "Low clinical likelihood"
            - "Patient characteristics suggest high image quality"
            - "Local expertise and availability"
            - "Information on atherosclerosis desired"
            - "No history of CAD"
        - id: "ccta"
          type: process
          content: "± Coronary Computed Tomographic angiography"
          items: []
        - id: "denotes_note"
          type: note
          content: "Denotes can be performed in any sequence based on local availability"
          items: []
      edges:
        - from: "referral"
          to: "high_likelihood_box"
          condition: ""
        - from: "high_likelihood_box"
          to: "functional_imaging"
          condition: ""
        - from: "referral"
          to: "low_likelihood_box"
          condition: ""
        - from: "low_likelihood_box"
          to: "ccta"
          condition: ""
        - from: "functional_imaging"
          to: "ccta"
          condition: ""
        - from: "ccta"
          to: "functional_imaging"
          condition: ""
```

**图注说明**：  
Figure 3 Non-invasive evaluation of INOCA. GP, general practitioner.

In the diagnostic pathway for patients assessed for angina recommended in the ESC CCS 2019 guideline, first line of testing is non-invasive. In patients with no obstructive CAD on their coronary computed tomographic angiography and/or no regional reversible ischaemia on functional testing, CMD or VSA may be the cause of their symptoms and in patients with a significant burden of disease, further testing through non-invasive and invasive techniques should be considered. While non-endothelial dependent dysfunction may be assessed non-invasively, acetylcholine can only be administered during invasive testing. Thus, a full diagnostic assessment for INOCA currently requires invasive angiography. Several non-invasive techniques allow assessment of CFR (Figure 3, Supplementary material online, Table S3).

Invasive diagnosis in the catheterization laboratory  
The 2019 ESC CCS guidelines have given a IIa recommendation (“should be considered”) for guidewire-based measurement of CFR