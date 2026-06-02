---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "图片", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "低"}, {"type": "表格", "position": "中央", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 4, "has_merged_cells": true, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 139.78
page_num: 11
task_id: 4d88ca12-0160-4a9f-881f-df556f49d7f8
re_extracted: True
re_extract_focus: "重点修正Step 3中四个乙酰胆碱试验分支的条件逻辑：橙色框（Microvascular Angina）应为‘无显著缩窄+有心绞痛+无缺血ECG’，而非复制绿色框内容；同时删除正文中的参考文献上标<sup>110,111</sup>。"
review_needed: True
review_reason: "修正流程图 YAML 中 Step 2 决策分支的逻辑条件表达及 acetylcholine_4 的直径缩减描述，确保与原图结构严格一致，避免逻辑歧义导致临床误读。"
---

#### 图 4 Invasive evaluation of INOCA. CFR, coronary flow reserve; FCA, functional coronary angiography; FFR, fractional flow reserve; IMR, index of microvascular resistance; LVEDP, left ventricular end-diastolic pressure. ^a^And negative non-invasive or invasive testing for epicardial ischaemia. ^b^Combo wire is an alternative option to measure FFR, CFR and IMR.

**自然语言概述**：  
该流程图描述了INOCA（缺血性心绞痛伴非阻塞性冠状动脉疾病）的侵入性评估路径，分为三步：  
1. **Step 1**：通过冠状动脉造影与左心室舒张末压（LVEDP）评估冠脉解剖与功能状态，依据LVEDP分为正常（0%）、轻度（<50%）和中度（50–80%）；  
2. **Step 2**：进行诊断性导丝检查与腺苷试验，联合测量FFR、CFR和IMR，根据阈值（FFR > 0.8、CFR ≥ 2.0、IMR < 25）判断是否存在冠状微血管功能障碍；  
3. **Step 3**：行乙酰胆碱激发试验（血管反应性测试），依据直径缩窄程度、有无心绞痛及缺血性ECG改变，将患者分为四类临床表型，最终归为四种INOCA内型：非心源性胸痛、心外膜血管痉挛性心绞痛、微血管性心绞痛、微血管与心外膜血管痉挛性心绞痛。

```yaml
flowchart:
  title: "Invasive evaluation of INOCA"
  levels:
    - level_name: "Step 1: Coronary angiography & LVEDP"
      nodes:
        - id: "step1"
          type: process
          content: "Coronary angiography & LVEDP"
          items:
            - "Normal: 0%"
            - "Mild: <50%"
            - "Moderate*: 50–80%"
          recommendation: ""
          color_hint: "light yellow"
    - level_name: "Step 2: Diagnostic guidewire and Adenosine test"
      nodes:
        - id: "step2"
          type: process
          content: "FFR + CFR + IMR*"
          items: []
          recommendation: ""
          color_hint: "light blue"
        - id: "no_mvd"
          type: decision
          content: "No Coronary Microvascular Dysfunction Present"
          items:
            - "FFR > 0.8"
            - "CFR ≥ 2.0"
            - "IMR < 25"
          recommendation: ""
          color_hint: "white"
        - id: "mvd_present"
          type: decision
          content: "Coronary Microvascular Dysfunction Present"
          items:
            - "FFR > 0.8"
            - "CFR < 2.0"
            - "IMR ≥ 25"
          recommendation: ""
          color_hint: "white"
    - level_name: "Step 3: Vasoreactivity (Acetylcholine test)"
      nodes:
        - id: "acetylcholine_1"
          type: condition
          content: "1. No or <90% diameter reduction<br>2. No angina<br>3. No ischaemic ECG changes"
          items: []
          recommendation: "Non cardiac pain"
          color_hint: "green"
        - id: "acetylcholine_2"
          type: condition
          content: "1. ≥90% diameter reduction<br>2. + angina<br>3. + ischaemic ECG changes"
          items: []
          recommendation: "Epicardial Vasospastic Angina"
          color_hint: "blue"
        - id: "acetylcholine_3"
          type: condition
          content: "1. No or <90% diameter reduction<br>2. + angina<br>3. No ischaemic ECG changes"
          items: []
          recommendation: "Microvascular Angina"
          color_hint: "orange"
        - id: "acetylcholine_4"
          type: condition
          content: "1. No or <90% or ≥90% diameter reduction<br>2. + angina<br>3. + ischaemic ECG changes"
          items: []
          recommendation: "Microvascular And Epicardial Vasospastic Angina"
          color_hint: "red"
        - id: "final"
          type: terminal
          content: "INOCA ENDOTYPES"
          items: []
          recommendation: ""
          color_hint: "dark blue"
  edges:
    - from: "step1"
      to: "step2"
      condition: ""
    - from: "step2"
      to: "no_mvd"
      condition: "FFR > 0.8, CFR ≥ 2.0, IMR < 25"
    - from: "step2"
      to: "mvd_present"
      condition: "FFR > 0.8, CFR < 2.0, IMR ≥ 25"
    - from: "no_mvd"
      to: "acetylcholine_1"
      condition: ""
    - from: "mvd_present"
      to: "acetylcholine_2"
      condition: ""
    - from: "no_mvd"
      to: "acetylcholine_3"
      condition: ""
    - from: "mvd_present"
      to: "acetylcholine_4"
      condition: ""
    - from: "acetylcholine_1"
      to: "final"
      condition: ""
    - from: "acetylcholine_2"
      to: "final"
      condition: ""
    - from: "acetylcholine_3"
      to: "final"
      condition: ""
    - from: "acetylcholine_4"
      to: "final"
      condition: ""
```

described. The potential risk of the invasive assessment should be weighed against the benefit of the diagnosis for the patient, acknowledging that so far it has not been studied whether management based on information gathered by invasive diagnostics may influence prognosis while only one pilot trial (CorMicA) has found a benefit in terms of symptoms.

### Management of INOCA

Management should be patient-centred with a multidisciplinary care approach might be helpful to the patient. Unfortunately, studies on therapy to improve CMD are small and heterogeneous in design and methodology and currently there is no evidence-based treatment of