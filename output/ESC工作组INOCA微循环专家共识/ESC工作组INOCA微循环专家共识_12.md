---
extraction_strategy: 标准提取
scout_result: {"page_layout": "混排", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 49.08
page_num: 12
task_id: cb2cbb32-2e40-4079-89f4-11f95939535e
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

#### Figure 5 Management of INOCA. ACEI, angiotensin-converting enzyme inhibitor; ARB, angiotensin receptor blocker.

```yaml
flowchart:
  title: "Management of INOCA"
  levels:
    - level_name: "1. Lifestyle factors"
      nodes:
        - id: "lifestyle_nutrition"
          type: process
          content: "Nutrition"
        - id: "lifestyle_exercise"
          type: process
          content: "Exercise"
        - id: "lifestyle_weight"
          type: process
          content: "Weight management"
        - id: "lifestyle_smoking"
          type: process
          content: "Smoking cessation"
        - id: "lifestyle_stress"
          type: process
          content: "Coping with stress"
    - level_name: "2. Risk factor management"
      nodes:
        - id: "risk_hypertension"
          type: process
          content: "Hypertension"
        - id: "risk_dyslipidaemia"
          type: process
          content: "Dyslipidaemia"
        - id: "risk_diabetes"
          type: process
          content: "Diabetes mellitus"
    - level_name: "3. Antianginal medication"
      nodes:
        - id: "microvascular_angina"
          type: decision
          content: "Microvascular angina"
        - id: "vasospastic_angina"
          type: decision
          content: "Vasospastic angina"
        - id: "consider_statins_acei_arb"
          type: process
          content: "Consider statins and ACEI/ARB"
        - id: "microvascular_treatment"
          type: process
          content: "1. Betablocker<br>2. Calcium channel blocker<br>3. Nicorandil<br>4. Ranolazine<br>5. Ivabradine<br>6. Trimetazidine"
        - id: "vasospastic_treatment"
          type: process
          content: "1. Calcium channel blocker<br>2. Long-acting nitrate<br>3. Nicorandil"
  edges:
    - from: "microvascular_angina"
      to: "microvascular_treatment"
      condition: ""
    - from: "microvascular_angina"
      to: "consider_statins_acei_arb"
      condition: ""
    - from: "vasospastic_angina"
      to: "vasospastic_treatment"
      condition: ""
    - from: "vasospastic_angina"
      to: "consider_statins_acei_arb"
      condition: ""
    - from: "consider_statins_acei_arb"
      to: "microvascular_angina"
      condition: ""
    - from: "consider_statins_acei_arb"
      to: "vasospastic_angina"
      condition: ""
```

Lifestyle factors  
In all patients with established INOCA due to the frequent presence of coronary atherosclerosis and endothelial dysfunction, tailored counselling on lifestyle factors is warranted to address risk factors, reduce symptoms and improve quality of life and prognosis. Behavioural interventions can be supported by nurse practitioners, experts in nutrition, psychologists, exercise physiotherapists, sports medicine, and so on. Adequate lifestyle support is comparable to other cardiovascular disease (CVD) prevention guidelines and preventive strategies in patients with stable CAD. The ability of specific diets, such as anti-inflammatory, vegan, or Mediterranean, to improve symptomatic coronary vascular dysfunction is unknown. However, obesity should be addressed. Coping with stress, the chronic and recurrent nature of symptoms may need extra attention, as they may have an important impact on working abilities in this often relatively young patient group.

Risk factor management  
The traditional CVD risk factors hypertension, dyslipidaemia, smoking, and diabetes may all contribute to the pathology of coronary microvascular and vasospastic dysfunction and structural remodelling of the circulation. The main therapeutic objective of strict control of BP is to prevent progression of microvascular changes and to reduce the frequency and intensity of anginal symptoms. Best choice of (combined) BP medications depends on the predominant mechanism of anginal symptoms, e.g. vasospastic and/or MVA. The use of angiotensin-converting enzyme inhibitors (ACEIs) improves CFR in CMD and ACEI/angiotensin receptor blockade (ARB) can be easily combined with both calcium antagonists and beta-blockers. Statins are beneficial in patients with non-obstructive CAD, and their anti-inflammatory properties may also be effective in those patients with reduced CFR and vascular spasm.

Anti-anginal medication  
Treatment of anginal symptoms in patients with INOCA is challenging as the patients represent a heterogeneous group and randomized