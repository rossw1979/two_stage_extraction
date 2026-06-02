---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "中央（嵌入图中）", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 3, "has_merged_cells": true, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 115.54
page_num: 11
task_id: f56c9bd2-cee2-41ce-9264-89efe20e6fc7
re_extracted: True
re_extract_focus: "需严格按双栏顺序分离左下段落与右下Recommendation段落，并确保图注后不直接拼接正文；YAML中生物标志物部分应修正为反映原图并列方框结构。"
review_needed: True
review_reason: "严格按双栏顺序输出：先左栏（图+图注+左下段落），再右栏（右下Recommendation段落）；修正YAML中生物标志物部分的节点结构以匹配原图2×2+1表格布局；确保右下栏段落不与左栏内容混排。"
---

#### 图 2 Types and Classification of Acute Coronary Syndromes.

**自然语言概述**：  
该图将急性冠脉综合征（Acute Coronary Syndromes）分为两大类：非ST段抬高型心肌梗死（NSTEMI）与ST段抬高型心肌梗死（STEMI），依据血管造影表现、心电图改变及心肌生物标志物变化进行分类。左侧NSTEMI对应部分闭塞性血栓，心电图可表现为ST段压低、T波倒置或无特异性改变；右侧STEMI对应完全闭塞性血栓，心电图特征为≥2个连续导联ST段抬高（标准12导联ECG或后壁导联ECG）。生物标志物（心肌肌钙蛋白）方面，NSTEMI组中不稳定型心绞痛为阴性（–）、NSTEMI为阳性（+）；STEMI组通常为阳性（+），但症状发作早期可能为阴性（–）。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Types and Classification of Acute Coronary Syndromes"
  levels:
    - level_name: "Primary Classification"
      nodes:
        - id: "acs"
          type: process
          content: "Acute Coronary Syndromes"
          recommendation: ""
          color_hint: ""
    - level_name: "Pathological Subtypes"
      nodes:
        - id: "nstemi"
          type: process
          content: "NSTEMI"
          items:
            - "Partially occlusive thrombus"
          recommendation: ""
          color_hint: "lightblue"
        - id: "stemi"
          type: process
          content: "STEMI"
          items:
            - "Completely occlusive thrombus"
          recommendation: ""
          color_hint: "lightyellow"
    - level_name: "Electrocardiographic Changes"
      nodes:
        - id: "nstemi_ecg"
          type: process
          content: "ST-segment depression"
          items:
            - "T-wave inversion"
            - "Nonspecific or no electrocardiographic changes may instead be seen"
          recommendation: ""
          color_hint: "lightblue"
        - id: "stemi_ecg"
          type: process
          content: "ST-segment elevation"
          items:
            - "ST-elevation in ≥2 contiguous leads on standard 12-lead ECG (or ST-elevation on posterior lead ECG)"
          recommendation: ""
          color_hint: "lightyellow"
    - level_name: "Biomarker Changes (cardiac troponin)"
      nodes:
        - id: "biomarker_nstemi"
          type: process
          content: "Unstable angina"
          items:
            - "–"
          recommendation: ""
          color_hint: "lightblue"
        - id: "biomarker_nstemi_plus"
          type: process
          content: "NSTEMI"
          items:
            - "+"
          recommendation: ""
          color_hint: "lightblue"
        - id: "biomarker_stemi"
          type: process
          content: "+"
          items:
            - "(Might be – if short time from symptom onset)"
          recommendation: ""
          color_hint: "lightyellow"
  edges:
    - from: "acs"
      to: "nstemi"
      condition: ""
    - from: "acs"
      to: "stemi"
      condition: ""
    - from: "nstemi"
      to: "nstemi_ecg"
      condition: ""
    - from: "stemi"
      to: "stemi_ecg"
      condition: ""
    - from: "nstemi_ecg"
      to: "biomarker_nstemi"
      condition: ""
    - from: "nstemi_ecg"
      to: "biomarker_nstemi_plus"
      condition: ""
    - from: "stemi_ecg"
      to: "biomarker_stemi"
      condition: ""
```

**图注说明**：  
NSTEMI indicates non–ST-segment elevation myocardial infarction; and STEMI, ST-segment elevation myocardial infarction.  
Illustration by Patrick Lane, ScEYEnce Studios. Copyright 2025 American College of Cardiology Foundation, and the American Heart Association, Inc.

patient triage. Specifically, patients should be managed based on the presence or absence of ST-segment elevation (or suspected equivalent) on the 12-lead ECG (Table 3 for STEMI electrocardiographic criteria). When possible, electrocardiographic tracings can be transmitted to the PPCI center while en route to help expedite coronary reperfusion upon arrival. Because patients with ACS and evidence of heart failure (HF), ventricular arrhythmias, or cardiogenic shock in the prehospital setting are at highest risk for death, identification of these complications is important with subsequent triage of these patients to a PCI-capable facility when possible (Section 8, “Cardiogenic Shock Management”).

### Recommendation-Specific Supportive Text

1. The early acquisition and recording of prehospital 12-lead ECGs by trained personnel is associated with shorter reperfusion times and lower mortality rates from STEMI if this diagnostic information is integrated in patients’ care. Appropriately trained EMS personnel (ie, paramedics) can interpret 12-lead ECGs for the identification of STEMI