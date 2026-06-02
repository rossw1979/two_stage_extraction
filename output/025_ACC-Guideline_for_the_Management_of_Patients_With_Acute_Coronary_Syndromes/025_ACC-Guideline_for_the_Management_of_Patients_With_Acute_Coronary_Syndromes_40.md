---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "表格", "position": "左下", "complexity": "低"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 2, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 163.63
page_num: 40
task_id: c032d170-0631-4e43-b654-723b0c547f4a
re_extracted: True
re_extract_focus: "修正双栏顺序：确保左栏标题'7. CATHETERIZATION LABORATORY CONSIDERATIONS IN ACS'及其子内容（含表格、Synopsis）完整置于流程图之前；同时修复低危组流程图分支的YAML结构化逻辑缺失及虚线连接关系。"
review_needed: True
review_reason: "修复流程图YAML中高危与中危路径共用同一节点ID导致的结构错误，并确保页面末尾截断内容明确保留截断状态（不补全、不隐藏）"
---

#### 图 8 Selection and Timing of an Invasive Strategy in NSTE-ACS.

**自然语言概述**：  
该流程图根据患者风险分层（不稳定/极高危、高危、中危、低危 NSTE-ACS）推荐相应的侵入性策略选择与时机。风险分层基于 GRACE 风险评分、临床症状（如心源性休克、新发肺水肿、持续缺血症状）、心电图动态改变（ST段变化）及生物标志物（Tn）趋势。各风险组对应不同侵入性策略（立即侵入、常规侵入、选择性侵入）及冠脉造影时间窗，并标注推荐等级（Class 1 或 Class 2a）。低危组进一步分支为“常规侵入或选择性侵入”与“非侵入性风险分层”，后者适用于住院期间或复发症状时再评估；二者之间存在虚线连接，表示非侵入性路径为可选替代方案，非强制顺序流程。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Choice and Timing of Management Strategy in NSTE-ACS"
  levels:
    - level_name: "Risk Stratification"
      nodes:
        - id: "unstable_high_risk"
          type: process
          content: "Unstable/very high-risk patient"
          items:
            - "Cardiogenic shock"
            - "Signs or symptoms of HF, including new/worsening mitral regurgitation or acute pulmonary edema"
            - "Refractory angina"
            - "Hemodynamic or electrical instability (eg, sustained VT or VF)"
          recommendation: ""
          color_hint: "pink"
        - id: "high_risk"
          type: process
          content: "High-risk NSTE-ACS"
          items:
            - "GRACE Risk Score >140"
            - "Steeply rising Tn values on serial testing despite optimized medical therapy"
            - "Ongoing dynamic ST-segment changes"
          recommendation: ""
          color_hint: "beige"
        - id: "intermediate_risk"
          type: process
          content: "Intermediate-risk NSTE-ACS"
          items:
            - "GRACE Risk Score 109–140"
            - "Absence of ongoing ischemic symptoms"
            - "Stable or downtrending Tn values"
          recommendation: ""
          color_hint: "lightblue"
        - id: "low_risk"
          type: process
          content: "Lower-risk NSTE-ACS"
          items:
            - "GRACE Risk Score <109"
            - "TIMI Risk Score <2"
            - "Absence of ongoing ischemic symptoms"
            - "Tn <99th percentile (ie, unstable angina)"
            - "No dynamic ST-segment changes"
          recommendation: ""
          color_hint: "lightgreen"
    - level_name: "Invasive Strategy"
      nodes:
        - id: "immediate_invasive"
          type: process
          content: "Immediate invasive strategy (<2 h, Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
        - id: "routine_invasive_high"
          type: process
          content: "Routine invasive (Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
        - id: "coro_angio_24h"
          type: process
          content: "Coronary angiography <24 h (Class 2a)"
          recommendation: "Class 2a"
          color_hint: "yellow"
        - id: "coro_angio_72h"
          type: process
          content: "Coronary angiography before hospital discharge (<72 h) (Class 2a)"
          recommendation: "Class 2a"
          color_hint: "yellow"
        - id: "routine_or_selective"
          type: process
          content: "Routine invasive or selective invasive (Class 1)"
          recommendation: "Class 1"
          color_hint: "green"
        - id: "coro_angio_discharge"
          type: process
          content: "Coronary angiography before hospital discharge (Class 2a)"
          recommendation: "Class 2a"
          color_hint: "yellow"
        - id: "non_invasive_strat"
          type: process
          content: "Non-invasive risk stratification during hospitalization or recurrent symptoms"
          recommendation: ""
          color_hint: "gray"
  edges:
    - from: "unstable_high_risk"
      to: "immediate_invasive"
      condition: ""
    - from: "high_risk"
      to: "routine_invasive_high"
      condition: ""
    - from: "routine_invasive_high"
      to: "coro_angio_24h"
      condition: ""
    - from: "intermediate_risk"
      to: "routine_invasive_high"
      condition: ""
    - from: "routine_invasive_high"
      to: "coro_angio_72h"
      condition: ""
    - from: "low_risk"
      to: "routine_or_selective"
      condition: ""
    - from: "routine_or_selective"
      to: "coro_angio_discharge"
      condition: ""
    - from: "routine_or_selective"
      to: "non_invasive_strat"
      condition: ""
      style: "dashed"
```

**图注说明**：  
Figure 8 summarizes the recommendations in the 2025 ACS Guideline for a routine or selective invasive approach in NSTE-ACS. It is not meant to encompass every patient scenario or situation, and clinicians are encouraged to use a Heart Team approach when care decisions are unclear and to see the accompanying supportive text for each recommendation. Colors correspond to Class of Recommendation in Table 2. GRACE indicates Global Registry of Acute Coronary Events; HF, heart failure; NSTE-ACS, non–ST-segment elevation acute coronary syndromes; Tn, troponin; TIMI, Thrombolysis in Myocardial Infarction; VF, ventricular fibrillation; and VT, ventricular tachycardia. Adapted with permission from Lawton et al.¹⁸

### 7. CATHETERIZATION LABORATORY CONSIDERATIONS IN ACS

#### 7.1. Vascular Access Approach for PCI

**Recommendation for Vascular Access Approach for PCI**  
*Referenced studies that support recommendation are summarized in the Evidence Table.*

| COR | LOE | Recommendation |
|-----|-----|----------------|
| 1   | A   | 1. In patients with ACS undergoing PCI, a radial approach is preferred to a femoral approach to reduce bleeding, vascular complications, and death.¹⁻⁶ |

*Modified from the “2021 ACC/AHA/SCAI Guideline for Coronary Artery Revascularization.”*

**Synopsis**  
The radial artery has become the preferred vascular access site for patients undergoing cardiac catheterization and PCI.⁸,⁹ Transradial access is associated with lower mortality, bleeding, and vascular complications in patients treated for ACS.⁵ In addition, patients prefer radial access because it allows earlier ambulation and causes less discomfort than femoral access.⁹ A caveat is most trials comparing radial versus femoral access had very low crossover rates because they required operators with expertise in radial access.³ The choice of radial access has to be weighed against the possibility that the radial artery could be used as a bypass conduit for CABG surgery.¹⁰ In sites where surgeons routinely utilize the radial artery as a bypass conduit, consideration should be given on the choice of vascular access and future use of radial artery for the cardiovascular surgical team. Although the radial artery is the most widely studied wrist access site, the use of alternative sites in the upper extremity, including the ulnar and distal radial arteries have yielded similar outcomes.¹¹,¹² Transfemoral access, preferably with the use of ultrasound guidance, should be considered in patients in whom temporary MCS is planned and is the default alternative access site among patients in whom the radial artery cannot be used due to clinical, anatomical, or technical reasons.¹³

**Recommendation-Specific Supportive Text**  
1. RCTs have consistently demonstrated the benefit of radial access in comparison with femoral access among patients treated for ACS. A meta-analysis using individual patient data from 7 high-quality RCTs (48.6% with NSTE-ACS; 46.2% with