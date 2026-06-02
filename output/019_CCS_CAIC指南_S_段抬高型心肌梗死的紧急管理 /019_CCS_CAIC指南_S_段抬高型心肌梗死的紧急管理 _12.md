---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "右中", "complexity": "低"}], "tables": {"count": 1, "max_rows_estimate": 1, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 141.78
page_num: 12
task_id: 6e0ab946-8d18-4644-8260-6432a874db96
re_extracted: True
re_extract_focus: "遗漏了右中位置的表格；流程图下方两个独立注释框未准确分离提取; 页面末尾原文截断处被不当截断而未保留不完整词形式"
review_needed: True
review_reason: "需严格按双栏顺序重组正文（左栏：Management与Performance段落；右栏：RECOMMENDATION、Practical tip及Multivessel段落），并修正Scout误报的‘表格’为纯文本块，同时保留原文末尾截断状态不补全。"
---

#### 图 3 Procedural aspects of primary percutaneous coronary intervention (PPCI)

**自然语言概述**：  
该流程图描述了STEMI患者行急诊PCI（PPCI）的关键 procedural aspects，从首次医疗接触（FMC）开始，经PCI术中操作要点，至根据血流动力学状态或心源性休克情况决定后续策略。流程分为三个主要阶段：① FMC后目标时间窗（≤90分钟/≤120分钟）；② PCI术中应避免的操作与推荐措施；③ 基于多支血管病变评估后的分流决策——若血流动力学稳定，可考虑完全血运重建或分期手术；若存在心源性休克，则初始PCI期间不应处理非罪犯病变。图中包含两个独立注释框：左下角说明“Transferred patients”定义；右下角说明指南推荐等级标识（* Strong, † Weak）。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Procedural aspects of primary percutaneous coronary intervention (PPCI)"
  levels:
    - level_name: "Initial Contact & Time Target"
      nodes:
        - id: "node_1"
          type: process
          content: "Primary PCI should be performed as quickly as possible after diagnosis."
          items:
            - "Target a FMC-to-device time of ≤ 90 min for patients presenting to PCI centre*"
            - "≤ 120 minutes for transferred patients*"
          recommendation: ""
          color_hint: "orange"
    - level_name: "During PCI Procedure"
      nodes:
        - id: "node_2"
          type: process
          content: "Avoid Routine upfront thrombectomy*"
          items: []
          recommendation: ""
          color_hint: "black"
        - id: "node_3"
          type: process
          content: "Radial Access as Default Access Site*"
          items: []
          recommendation: ""
          color_hint: "black"
        - id: "node_4"
          type: process
          content: "Use Heparin*, Bivalirudin* or Enoxaparin*"
          items: []
          recommendation: ""
          color_hint: "black"
        - id: "node_5"
          type: process
          content: "Avoid Routine IV or IC GP IIb/IIIa inhibitors*"
          items: []
          recommendation: ""
          color_hint: "black"
        - id: "node_6"
          type: process
          content: "Avoid Routine IC Lytics* or IC Adenosine*"
          items: []
          recommendation: ""
          color_hint: "black"
    - level_name: "Multivessel Assessment"
      nodes:
        - id: "node_7"
          type: decision
          content: "Multivessel coronary disease?"
          items: []
          recommendation: ""
          color_hint: "blue"
    - level_name: "Post-Assessment Pathways"
      nodes:
        - id: "node_8"
          type: process
          content: "IF HEMODYNAMICALLY STABLE, complete revascularization at time of PCI or as staged procedure can be considered†"
          items: []
          recommendation: ""
          color_hint: "blue"
        - id: "node_9"
          type: process
          content: "IF CARDIOGENIC SHOCK, do not perform non-culprit lesion PCI during initial procedure*"
          items: []
          recommendation: ""
          color_hint: "red"
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
      condition: ""
    - from: "node_6"
      to: "node_7"
      condition: ""
    - from: "node_7"
      to: "node_8"
      condition: "Yes"
    - from: "node_7"
      to: "node_9"
      condition: "No (or shock present)"
  notes:
    - "Transferred patients refers to both patients who are diagnosed in the field and patients who are transferred from non-PCI capable centres"
    - "Guideline based recommendations: * Strong, † Weak"
```

Figure 3. Procedural aspects of primary percutaneous coronary intervention (PPCI). FMC, first medical contact; GP IIb/IIIa, glycoprotein IIb/IIIa; I.C., intracoronary; I.V., intravenous; PCI, percutaneous coronary intervention.

Management of the STEMI Patient at a PCI-Capable Centre  
The recommendations regarding the procedural aspects of PPCI are summarized in Figure 3.

Performance of primary PCI  
Many large, retrospective observational studies have shown improved, risk-adjusted outcomes among patients who present directly to a PCI-centre with the shortest reperfusion times, including door-to-balloon times of ≤ 90 minutes compared with patients with longer delays. Although some studies have shown a neutral mortality benefit of reduced reperfusion times at the population level, it has more recently been shown among patients who received PPCI that shorter patient-specific reperfusion is consistently associated with lower mortality rates.  
Contemporary cohort studies have shown that prospectively targeting an FMC-to-device time of ≤ 90 minutes is feasible and is associated with improved outcomes. Implementation of STEMI regionalization in the American Heart Association Accelerator 1 and 2 programs resulted in an increase in the proportion of patients with an FMC ≤ 90 minutes from 67% to 74%, with an associated 50% reduction in in-hospital mortality. Multiple regional STEMI programs in Canada have also been able to achieve this metric for most STEMI patients who present to PCI centres.

RECOMMENDATION  
21. For patients with STEMI identified at a primary PCI centre, we recommend that STEMI networks target a FMC-to-device time of ≤ 90 minutes (Strong Recommendation, Low-Quality Evidence).

Practical tip. Fibrinolytic therapy should be considered as a viable reperfusion strategy at a PPCI centre if it is anticipated that PCI will be significantly delayed because of extenuating circumstances (eg, multiple STEMI patients arriving concurrently).

Multivessel vs culprit-only PCI in STEMI patients with and without CS  
Approximately one-third to one-half of patients who present with STEMI have multivessel disease, defined as a significant stenosis in at least 1 nonculprit vessel (NCV). Whether patients should receive routine revascularization of angiographic or hemodynamically significant nonculprit lesions, or culprit lesion-only revascularization in addition to optimal medical therapy remains a common dilemma. Furthermore, the optimal timing of intervention remains uncertain if revascularization of the NCV(s) is considered.  
A total of 9 randomized trials have compared routine nonculprit lesion PCI with optimal medical therapy alone in