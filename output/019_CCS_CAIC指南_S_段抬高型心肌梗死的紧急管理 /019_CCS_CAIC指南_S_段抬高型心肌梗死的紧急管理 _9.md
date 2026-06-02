---
extraction_strategy: 标准提取
scout_result: {"page_layout": "混排", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "左下", "complexity": "低"}], "tables": {"count": 1, "max_rows_estimate": 2, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 172.36
page_num: 9
task_id: 89706984-3ab4-45e1-8091-5ac7219cd209
re_extracted: True
re_extract_focus: "遗漏了左下角带边框的RECOMMENDATION编号列表（应作为表格提取），且流程图YAML中node_3的结构错误（将并列要点错误嵌套为子项），需按原图重新解析流程图层级与表格结构。"
review_needed: True
review_reason: "流程图 YAML 结构错误：需修正 levels 划分与 edges 连接逻辑，确保补充性建议（如时间目标、条件选项）作为同 level 并列节点而非独立流程节点；同时校正推荐强度标注，仅对原图明确标有 * / # / † 的条目赋值。"
---

#### 图 2 Prehospital management of ST-elevation myocardial infarction (STEMI)

**自然语言概述**：  
该流程图描述了STEMI患者的院前管理路径，从急救人员现场获取心电图开始，依次进行转运策略决策、氧疗、镇痛及抗血小板治疗等关键干预步骤。每一步均明确操作目标、时间窗要求与推荐强度（强推荐、弱推荐、实用提示），各环节以水平箭头连接，体现并行与顺序关系。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Prehospital Management of STEMI"
  levels:
    - level_name: "Initial Assessment & ECG"
      nodes:
        - id: "node_1"
          type: process
          content: "EMS personnel acquire an ECG in the field to identify STEMI and alert STEMI care teams"
          recommendation: "Strong recommendation"
          color_hint: "blue"
    - level_name: "Transport Strategy"
      nodes:
        - id: "node_2"
          type: process
          content: "Bypass non-PCI capable centres and transport to the nearest PPCI centre with the goal of achieving a maximum FMC-to-device time of ≤ 120 minutes"
          recommendation: "Strong recommendation"
          color_hint: "blue"
        - id: "node_3a"
          type: process
          content: "Ideal FMC-to-device time ≤ 90 minutes in urban settings"
          recommendation: "Strong recommendation"
          color_hint: "gray"
        - id: "node_3b"
          type: process
          content: "Consider fibrinolysis if this timeline cannot be achieved"
          recommendation: "Strong recommendation"
          color_hint: "gray"
        - id: "node_3c"
          type: process
          content: "Consider bypassing the PCI centre emergency department when possible"
          recommendation: "Strong recommendation"
          color_hint: "gray"
    - level_name: "Oxygen Therapy"
      nodes:
        - id: "node_4"
          type: process
          content: "Avoid routine administration of supplemental oxygen with oxygen saturation ≥ 90%"
          recommendation: "Strong recommendation"
          color_hint: "blue"
        - id: "node_5"
          type: process
          content: "If SaO₂ monitoring is not available or not reliable, may provide oxygen to patients exhibiting respiratory distress"
          recommendation: "Practical Tip"
          color_hint: "gray"
    - level_name: "Analgesia"
      nodes:
        - id: "node_6"
          type: process
          content: "Avoidance of routine intravenous opioid analgesic for STEMI-related discomfort"
          recommendation: "Strong recommendation"
          color_hint: "blue"
        - id: "node_7"
          type: process
          content: "Selective use of opioid analgesics may be considered for severe pain"
          recommendation: "Weak recommendation"
          color_hint: "gray"
    - level_name: "Antiplatelet Therapy"
      nodes:
        - id: "node_8"
          type: process
          content: "P2Y12 receptor antagonist medications should not routinely be administered in ambulance"
          recommendation: "Strong recommendation"
          color_hint: "blue"
        - id: "node_9a"
          type: process
          content: "P2Y12 receptor antagonists should be administered in the emergency department or cardiac catheterization laboratory as early as possible"
          recommendation: "Strong recommendation"
          color_hint: "gray"
        - id: "node_9b"
          type: process
          content: "Prehospital administration of P2Y12 receptor antagonists may be considered for transport times > 60 minutes or for systems that administer prehospital fibrinolysis"
          recommendation: "Weak recommendation"
          color_hint: "gray"
  edges:
    - from: "node_1"
      to: "node_2"
      condition: ""
    - from: "node_2"
      to: "node_3a"
      condition: ""
    - from: "node_2"
      to: "node_4"
      condition: ""
    - from: "node_4"
      to: "node_5"
      condition: ""
    - from: "node_4"
      to: "node_6"
      condition: ""
    - from: "node_6"
      to: "node_7"
      condition: ""
    - from: "node_6"
      to: "node_8"
      condition: ""
    - from: "node_8"
      to: "node_9a"
      condition: ""
    - from: "node_9a"
      to: "node_9b"
      condition: ""
```

**图注说明**：  
Figure 2. Prehospital management of ST-elevation myocardial infarction (STEMI). EMS, emergency medical services; ECG, electrocardiogram; FMC, first medical contact; PCI, percutaneous coronary intervention; PPCI, primary PCI; SaO₂, oxygen saturation.  
* Strong recommendation  
# Weak recommendation  
† Practical Tip

| Recommendation | Content |
|----------------|---------|
| 14 | For patients with STEMI identified at a non–PCI-capable centre, if primary PCI is used as the default reperfusion strategy, we recommend that STEMI networks target a total FMC-to-device time (including interfacility transfer) of ≤ 120 minutes. Fibrinolytic therapy should be considered if this timeline cannot be achieved (Strong Recommendation, Low-Quality Evidence). |
| 15 | If primary PCI is used as a default reperfusion strategy, we recommend a target door-in-door-out time at the transferring hospital of ≤ 30 minutes (Strong Recommendation, Low-Quality Evidence). |

Fibrinolysis. Fibrinolytic agents that have been used as reperfusion therapy for STEMI include streptokinase, tenecteplase, reteplase, and alteplase. A recent network meta-analysis showed lower mortality rates with fibrin-specific agents (tenecteplase, reteplase, and accelerated infusion alteplase).<sup>100</sup> Fibrinolysis given within 12 hours of symptom onset significantly reduces mortality for STEMI. However, it has been estimated that 1.6 lives per 1000 patients treated are lost for every 1 hour of delay in administering fibrinolytic therapy.<sup>101</sup> On the basis of this time-dependent mortality benefit, previous guidelines have recommended a goal of FMC to needle time of ≤ 30 minutes.<sup>6</sup> This goal is achievable for most STEMI patients in Canadian centres.<sup>102,103</sup> Although European guidelines recommend fibrinolytic therapy within 10 minutes, this is on the basis of 10 minutes from STEMI diagnosis, not from FMC.<sup>43</sup> Strategies to minimize treatment delays in sites that use fibrinolysis as their default initial reperfusion strategy include prehospital diagnosis and advance notification, use of triage algorithms to expedite ECG acquisition and interpretation, and prehospital fibrinolysis if feasible.

Fibrinolytic therapy might be particularly suitable for STEMI patients who present early in the course of their infarct, with the greatest benefit seen within the first 2–3 hours after symptom onset.<sup>48,104,105</sup> Administration of fibrinolysis provides an opportunity to deliver reperfusion therapy early in the course of an evolving infarct.<sup>106</sup> Indeed, fibrinolysis administered within the first hour of symptom onset successfully aborted the MI in approximately 30% of STEMI patients.<sup>107</sup> The feasibility of paramedic-based administration of prehospital fibrinolysis was established within the Assessment of the Safety and Efficacy of a New Thrombolytic Agent (ASSENT) 3+ trial.<sup>108</sup> Prehospital fibrinolysis administered within 2 hours of chest pain in the Comparison of Angioplasty and Prehospital Thrombolysis in Acute Myocardial