---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "表格", "position": "左上", "complexity": "低"}, {"type": "图片", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "低"}], "tables": {"count": 1, "max_rows_estimate": 6, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 154.94
page_num: 3
task_id: dff5f0a8-3713-48b3-94a6-b4f5d937cb5e
re_extracted: True
re_extract_focus: "双栏排版顺序错误：右上和右下段落被错误归入左栏输出，需严格按‘左栏全部→右栏全部’重新组织；同时修正Table 1结构标识及流程图YAML边定义不规范问题。"
review_needed: False
review_reason: ""
---

Table 1. Elements of a regional STEMI network  
A preplanned default initial reperfusion strategy (PPCI or fibrinolysis) for each hospital within the network on the basis of geographic and transport considerations.  
The ability to deliver appropriate adjunctive PCI after fibrinolysis.  
The capability of EMS and emergency department teams to rapidly diagnose and treat STEMI.  
For PPCI, the ability for EMS and emergency departments to activate the STEMI team for reperfusion therapy through a “single call” mechanism immediately from the point of first medical contact with the patient.  
The implementation of a “no-refusal” policy at PCI centres for STEMI patients who are deemed appropriate for PPCI.  
The ability for EMS teams that diagnose STEMI patients in the field to bypass non-PCI centres and transport patients directly to a PCI centre.  
The ability for appropriately selected patients to bypass the emergency department of a PCI centre and proceed directly to the cardiac catheterization laboratory.  

EMS, emergency medical service; PCI, percutaneous coronary intervention; PPCI, primary PCI; STEMI, ST-elevation myocardial infarction.

Regionalization of STEMI Care  

Development of regional STEMI centres (hub and spoke) and regional reperfusion strategies  

Reperfusion therapy within 12 hours of symptom onset reduces mortality in STEMI patients. Although PPCI is the preferred reperfusion strategy when it can be rapidly performed, there are patient, hospital, and geographic factors that can affect the ability for it to be delivered within recommended timelines. Fibrinolysis remains a suitable alternative for appropriately selected patients who cannot undergo timely PPCI. These considerations should be accounted for when selecting a reperfusion strategy for a STEMI patient.  

Although logistical considerations vary across Canada, each regional care system can work to streamline the diagnosis and management of patients with STEMI. Evidence suggests that STEMI care is best performed within the setting of an organized STEMI network with a PPCI centre (the “hub”) receiving referrals from surrounding hospitals (the “spokes”) and a defined catchment area from the field via emergency medical services (EMS). Table 1 shows a list of important fundamental elements of such a program.  

Reperfusion decision-making within a regional STEMI network  

STEMI patients can potentially be identified either in the prehospital setting by EMS or in a hospital (with or without PCI capability) within a given regional network of STEMI care. Geographical proximity to centres that perform 24/7 PPCI, along with the presence of appropriate EMS transport systems, can help determine the optimal default reperfusion strategy for these STEMI patients (Fig. 1).

#### 图 1 ST-elevation myocardial infarction (STEMI) reperfusion strategies. EMS, emergency medical services; FL, fibrinolysis; FMC, first medical contact; PCI, percutaneous coronary intervention; PPCI, primary percutaneous coronary intervention.

**自然语言概述**：  
该流程图描述了STEMI患者在区域化医疗网络中的再灌注决策路径，依据首次医疗接触（FMC）地点分为三类场景：非PCI中心（“Spoke”医院）、院前诊断（EMS）、PCI中心（“Hub”医院）。核心决策点为“FMC至PCI时间是否＜120分钟”。若否，则选择溶栓治疗（FL），随后根据溶栓是否成功决定是否行补救性PCI；若是，则直接转运至PCI中心行直接PCI（PPCI），要求转运时间≤60分钟且FMC至PPCI＜120分钟；若患者已在PCI中心，则直接行Primary PCI，要求FMC至PPCI＜90分钟。所有路径最终均导向PCI治疗，其中溶栓后成功者可采用“药理侵入性策略”（Pharmacoinvasive Strategy）。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "ST-elevation myocardial infarction (STEMI) reperfusion strategies"
  levels:
    - level_name: "Initial diagnosis setting"
      nodes:
        - id: "node_1"
          type: process
          content: "DIAGNOSIS AT NON PCI CENTRE (\"Spoke\" hospital)"
          items:
            - "*FMC to STEMI diagnosis < 10 min"
          color_hint: "blue"
        - id: "node_2"
          type: process
          content: "PREHOSPITAL DIAGNOSIS (EMS)"
          items:
            - "*FMC to STEMI diagnosis < 10 min"
          color_hint: "teal"
        - id: "node_3"
          type: process
          content: "DIAGNOSIS AT PCI CENTRE (\"Hub\" hospital)"
          items:
            - "*FMC to STEMI diagnosis < 10 min"
          color_hint: "darkblue"
    - level_name: "Reperfusion decision"
      nodes:
        - id: "node_4"
          type: decision
          content: "Time from FMC to PCI < 120 min?"
          color_hint: "lightblue"
    - level_name: "NO branch"
      nodes:
        - id: "node_5"
          type: process
          content: "Fibrinolysis (FL)"
          items:
            - "FMC to needle time < 30 min*"
          color_hint: "purple"
        - id: "node_6"
          type: process
          content: "Routine Rapid Transfer"
          items:
            - "Immediate PCI for Failed FL"
            - "Routine PCI within 24hrs of successful FL"
          recommendation: '"Pharmacoinvasive Strategy"'
          color_hint: "maroon"
    - level_name: "YES branch"
      nodes:
        - id: "node_7"
          type: process
          content: "Transfer for PPCI"
          items:
            - "Transfer time ≤ 60 min"
            - "FMC to PPCI < 120 min*"
          color_hint: "orange"
        - id: "node_8"
          type: process
          content: "Perform Primary PCI"
          items:
            - "FMC to PPCI < 90 min*"
          color_hint: "gray"
    - level_name: "Additional considerations"
      nodes:
        - id: "node_9"
          type: note
          content: "† Also consider clinical factors such as symptom duration and presence of contraindications to fibrinolysis"
          color_hint: "lightgray"
        - id: "node_10"
          type: note
          content: "Guideline based recommendations:"
          items:
            - "• Strong"
            - "# Weak"
          color_hint: "lightgray"
  edges:
    - from: "node_1"
      to: "node_4"
    - from: "node_2"
      to: "node_4"
    - from: "node_3"
      to: "node_8"
    - from: "node_4"
      to: "node_5"
      condition: "NO"
    - from: "node_4"
      to: "node_7"
      condition: "YES"
    - from: "node_5"
      to: "node_6"
    - from: "node_6"
      to: "node_8"
      condition: "dashed arrow → Pharmacoinvasive Strategy"
    - from: "node_7"
      to: "node_8"
    - from: "node_8"
      to: "node_10"
    - from: "node_5"
      to: "node_9"
```

**图注说明**：  
EMS, emergency medical services; FL, fibrinolysis; FMC, first medical contact; PCI, percutaneous coronary intervention; PPCI, primary percutaneous coronary intervention.