---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "低"}, {"type": "段落", "position": "左上", "complexity": "低"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 58.53
page_num: 11
task_id: aba8c8b7-064f-40f7-be08-bda9f5b86cf1
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

#### 图 2 Types and Classification of Acute Coronary Syndromes.

自然语言概述：  
该流程图对急性冠脉综合征（Acute Coronary Syndromes）进行分类，依据血管造影表现、心电图改变及心肌标志物（肌钙蛋白）变化分为两大类：非ST段抬高型心肌梗死（NSTE-ACS，含NSTEMI和不稳定型心绞痛）与ST段抬高型心肌梗死（STEMI）。左侧蓝色区域代表NSTEMI路径：血管造影显示部分闭塞性血栓；心电图表现为ST段压低或T波倒置，亦可无特异性或无心电图改变；心肌标志物升高（+），而不稳定型心绞痛则标志物阴性（−）。右侧黄色区域代表STEMI路径：血管造影显示完全闭塞性血栓；心电图特征为≥2个连续导联ST段抬高（标准12导联ECG）或后壁导联ST段抬高；心肌标志物阳性（+），并标注“可能在症状发作后短时间内即呈阳性”。

YAML 结构化数据：

```yaml
flowchart:
  title: "Types and Classification of Acute Coronary Syndromes"
  levels:
    - level_name: "Initial Classification"
      nodes:
        - id: "root"
          type: process
          content: "Acute Coronary Syndromes"
          recommendation: ""
          color_hint: ""
    - level_name: "Angiographic Findings"
      nodes:
        - id: "nstemi_angio"
          type: process
          content: "Partially occlusive thrombus"
          items: []
          recommendation: ""
          color_hint: "lightblue"
        - id: "stemi_angio"
          type: process
          content: "Completely occlusive thrombus"
          items: []
          recommendation: ""
          color_hint: "lightyellow"
    - level_name: "Electrocardiographic Changes"
      nodes:
        - id: "nstemi_ecg"
          type: process
          content: "ST-segment depression or T-wave inversion"
          items:
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
        - id: "unstable_angina"
          type: process
          content: "Unstable angina"
          items: []
          recommendation: "-"
          color_hint: "lightblue"
        - id: "nstemi_biomarker"
          type: process
          content: "NSTEMI"
          items: []
          recommendation: "+"
          color_hint: "lightblue"
        - id: "stemi_biomarker"
          type: process
          content: "STEMI"
          items:
            - "(Might be + if short time from symptom onset)"
          recommendation: "+"
          color_hint: "lightyellow"
  edges:
    - from: "root"
      to: "nstemi_angio"
      condition: ""
    - from: "root"
      to: "stemi_angio"
      condition: ""
    - from: "nstemi_angio"
      to: "nstemi_ecg"
      condition: ""
    - from: "stemi_angio"
      to: "stemi_ecg"
      condition: ""
    - from: "nstemi_ecg"
      to: "unstable_angina"
      condition: ""
    - from: "nstemi_ecg"
      to: "nstemi_biomarker"
      condition: ""
    - from: "stemi_ecg"
      to: "stemi_biomarker"
      condition: ""
```

注：NSTEMI indicates non–ST-segment elevation myocardial infarction; and STEMI, ST-segment elevation myocardial infarction.  
Illustration by Patrick Lane, ScEYEnce Studios. Copyright 2025 American College of Cardiology Foundation, and the American Heart Association, Inc.

patient triage. Specifically, patients should be managed based on the presence or absence of ST-segment elevation (or suspected equivalent) on the 12-lead ECG (Table 3 for STEMI electrocardiographic criteria). When possible, electrocardiographic tracings can be transmitted to the PPCI center while en route to help expedite coronary reperfusion upon arrival. Because patients with ACS and evidence of heart failure (HF), ventricular arrhythmias, or cardiogenic shock in the prehospital setting are at highest risk for death, identification of these complications is important with subsequent triage of these patients to a PCI-capable facility when possible (Section 8, “Cardiogenic Shock Management”)<sup>14,15</sup>

### Recommendation-Specific Supportive Text

1. The early acquisition and recording of prehospital 12-lead ECGs by trained personnel is associated with shorter reperfusion times and lower mortality rates from STEMI if this diagnostic information is integrated in patients’ care.<sup>1,2,16</sup> Appropriately trained EMS personnel (ie, paramedics) can interpret 12-lead ECGs for the identification of STEMI