---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "表格", "position": "左下", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 2, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 71.56
page_num: 40
task_id: 145a1ee5-772e-42ad-be58-71560d5daa14
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

#### 图 8 Selection and Timing of an Invasive Strategy in NSTE-ACS

**自然语言概述**：  
该流程图根据患者风险分层（不稳定/极高危、高危、中危、低危NSTE-ACS）推荐相应的侵入性策略选择与时机。风险分层依据GRACE评分、TIMI评分、临床症状（如心源性休克、新发心力衰竭、持续缺血症状）、心电图动态ST段改变及肌钙蛋白（Tn）变化等指标。各风险组对应不同侵入性策略（立即侵入、常规侵入、选择性侵入）及冠脉造影时间窗，并标注推荐等级（Class 1 或 Class 2a）。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Choice and Timing of Management Strategy in NSTE-ACS"
  levels:
    - level_name: "Unstable/very high-risk patient"
      nodes:
        - id: "UH_1"
          type: condition
          content: "Any of:"
          items:
            - "Cardiogenic shock"
            - "Signs or symptoms of HF, including new/worsening mitral regurgitation or acute pulmonary edema"
            - "Refractory angina"
            - "Hemodynamic or electrical instability (eg, sustained VT or VF)"
        - id: "UH_2"
          type: process
          content: "Immediate invasive strategy (<2 h, Class 1)"
          recommendation: "Class 1"
    - level_name: "High-risk NSTE-ACS"
      nodes:
        - id: "H_1"
          type: condition
          content: "Any of:"
          items:
            - "GRACE Risk Score >140"
            - "Steeply rising Tn values on serial testing despite optimized medical therapy"
            - "Ongoing dynamic ST-segment changes"
        - id: "H_2"
          type: process
          content: "Routine invasive (Class 1)"
          recommendation: "Class 1"
        - id: "H_3"
          type: process
          content: "Coronary angiography <24 h (Class 2a)"
          recommendation: "Class 2a"
    - level_name: "Intermediate-risk NSTE-ACS"
      nodes:
        - id: "I_1"
          type: condition
          content: "Any of:"
          items:
            - "GRACE Risk Score 109–140"
            - "Absence of ongoing ischemic symptoms"
            - "Stable or downtrending Tn values"
        - id: "I_2"
          type: process
          content: "Routine invasive (Class 1)"
          recommendation: "Class 1"
        - id: "I_3"
          type: process
          content: "Coronary angiography before hospital discharge (<72 h) (Class 2a)"
          recommendation: "Class 2a"
    - level_name: "Lower-risk NSTE-ACS"
      nodes:
        - id: "L_1"
          type: condition
          content: "Any of:"
          items:
            - "GRACE Risk Score <109"
            - "TIMI Risk Score <2"
            - "Absence of ongoing ischemic symptoms"
            - "Tn <99th percentile (ie, unstable angina)"
            - "No dynamic ST-segment changes"
        - id: "L_2"
          type: process
          content: "Routine invasive or selective invasive (Class 1)"
          recommendation: "Class 1"
        - id: "L_3"
          type: process
          content: "Coronary angiography before hospital discharge (Class 2a)"
          recommendation: "Class 2a"
        - id: "L_4"
          type: process
          content: "Non-invasive risk stratification during hospitalization or recurrent symptoms"
          recommendation: ""
  edges:
    - from: "UH_1"
      to: "UH_2"
      condition: ""
    - from: "H_1"
      to: "H_2"
      condition: ""
    - from: "H_2"
      to: "H_3"
      condition: ""
    - from: "I_1"
      to: "I_2"
      condition: ""
    - from: "I_2"
      to: "I_3"
      condition: ""
    - from: "L_1"
      to: "L_2"
      condition: ""
    - from: "L_2"
      to: "L_3"
      condition: ""
    - from: "L_2"
      to: "L_4"
      condition: "if non-invasive risk stratification indicated"
```

**图注说明**：  
Figure 8 summarizes the recommendations in the 2025 ACS Guideline for a routine or selective invasive approach in NSTE-ACS. It is not meant to encompass every patient scenario or situation, and clinicians are encouraged to use a Heart Team approach when care decisions are unclear and to see the accompanying supportive text for each recommendation. Colors correspond to Class of Recommendation in Table 2. GRACE indicates Global Registry of Acute Coronary Events; HF, heart failure; NSTE-ACS, non–ST-segment elevation acute coronary syndromes; Tn, troponin; TIMI, Thrombolysis in Myocardial Infarction; VF, ventricular fibrillation; and VT, ventricular tachycardia. Adapted with permission from Lawton et al.<sup>18</sup> Copyright 2022 American Heart Association, Inc., and American College of Cardiology Foundation.

---

### 7. CATHETERIZATION LABORATORY CONSIDERATIONS IN ACS

#### 7.1. Vascular Access Approach for PCI

**Recommendation for Vascular Access Approach for PCI**  
Referenced studies that support recommendation are summarized in the Evidence Table.

| COR | LOE | Recommendation |
|-----|-----|----------------|
| 1   | A   | 1. In patients with ACS undergoing PCI, a radial approach is preferred to a femoral approach to reduce bleeding, vascular complications, and death.<sup>*1–6</sup> |

*Modified from the “2021 ACC/AHA/SCAI Guideline for Coronary Artery Revascularization.”<sup>7</sup>

---

**Synopsis**  
The radial artery has become the preferred vascular access site for patients undergoing cardiac catheterization and PCI.<sup>8,9</sup> Transradial access is associated with lower mortality, bleeding, and vascular complications in patients treated for ACS.<sup>5</sup> In addition, patients prefer radial access because it allows earlier ambulation and causes less discomfort than femoral access.<sup>9</sup> A caveat is most trials comparing radial versus femoral access had very low crossover rates because they required operators with expertise in radial access.<sup>3</sup> The choice of radial access has to be weighed against the possibility that the radial artery could be used as a bypass conduit for CABG surgery.<sup>10</sup> In sites where surgeons routinely utilize the radial artery as a bypass conduit, consideration should be given on the choice of vascular access and future use of radial artery for the cardiovascular surgical team. Although the radial artery is the most widely studied wrist access site, the use of alternative sites in the upper extremity, including the ulnar and distal radial arteries have yielded similar outcomes.<sup>11,12</sup> Transfemoral access, preferably with the use of ultrasound guidance, should be considered in patients in whom temporary MCS is planned and is the default alternative access site among patients in whom the radial artery cannot be used due to clinical, anatomical, or technical reasons.<sup>13</sup>

---

**Recommendation-Specific Supportive Text**  
1. RCTs have consistently demonstrated the benefit of radial access in comparison with femoral access among patients treated for ACS. A meta-analysis using individual patient data from 7 high-quality RCTs (48.6% with NSTE-ACS; 46.2% with