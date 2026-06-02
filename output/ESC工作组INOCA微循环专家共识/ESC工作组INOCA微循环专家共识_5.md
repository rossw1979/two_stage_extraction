---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "高"}, {"type": "表格", "position": "左下", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 4, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 149.72
page_num: 5
task_id: 708ec40a-2dc6-4199-95b5-41498e170b0c
re_extracted: True
re_extract_focus: "修正流程图 YAML 结构：将 transient/persistent vasospasm 作为 VSA 节点的 items 子项而非独立节点，并确保同一 level 内 nodes 为严格并列关系；同时补全表格内脚注上标标记并与下方脚注内容明确关联。"
review_needed: True
review_reason: "图2流程图的节点划分与边连接关系需严格按原图三栏结构重建：左栏CMD路径、中栏VSA分支、右栏阻塞性CAD路径，确保黄色高亮框'Non-obstructive coronary atherosclerosis is frequently present.'作为独立强调节点，且所有图示关联箭头必须准确映射到edges；同时修正Table 1脚注a中NT-proBNP阈值表述错误。"
---

#### 图 2 Mechanisms of myocardial ischaemia in INOCA and obstructive coronary artery disease. CAD, coronary artery disease; FFR, fractional flow reserve.

**自然语言概述**：  
该流程图对比了两种心肌缺血机制：非阻塞性冠状动脉疾病（INOCA）与阻塞性冠状动脉疾病。左侧为INOCA路径，起始于冠状微血管功能障碍（CMD）或血管痉挛性心绞痛（VSA），最终导致微血管性心绞痛及心肌缺血；中间路径描述VSA进一步发展为短暂或持续性血管痉挛，可引发变异型心绞痛或心肌梗死；右侧为阻塞性冠状动脉疾病路径，由动脉粥样硬化疾病起始，经稳定斑块→血流储备分数（FFR）降低→劳力性/静息性心肌缺血，或脆弱斑块→斑块破裂→血栓形成→急性冠脉综合征/心肌梗死。三者机制可重叠，且INOCA中常合并非阻塞性冠状动脉粥样硬化。

```yaml
flowchart:
  title: "Mechanisms of myocardial ischaemia in INOCA and obstructive coronary artery disease"
  levels:
    - level_name: "Primary Pathways"
      nodes:
        - id: "INOCA_start"
          type: process
          content: "Ischaemia with non obstructive coronary arteries (INOCA)"
          items: []
        - id: "OCA_start"
          type: process
          content: "Ischaemia with obstructive coronary artery disease"
          items: []
    - level_name: "INOCA Subtypes"
      nodes:
        - id: "CMD"
          type: process
          content: "Coronary Microvascular dysfunction (CMD)"
          items:
            - "Coronary microcirculation"
            - "Impairs coronary physiology and myocardial blood flow in subjects with risk factors"
            - "Causes microvascular angina and contributes to myocardial ischaemia in CAD"
        - id: "VSA"
          type: process
          content: "Vasospastic angina (VSA)"
          items:
            - "Epicardial coronary artery"
            - "Transient vasospasm → Prinzmetal angina"
            - "Persistent vasospasm → Myocardial infarction"
    - level_name: "Obstructive CAD Pathway"
      nodes:
        - id: "Atherosclerosis"
          type: process
          content: "Atherosclerotic disease"
          items: []
        - id: "Stable_plaque"
          type: process
          content: "Stable plaque"
          items:
            - "Reduction in FFR"
            - "Demand ischaemia ± angina"
        - id: "Vulnerable_plaque"
          type: process
          content: "Vulnerable plaque"
          items:
            - "Plaque rupture"
            - "Thrombosis"
            - "Acute coronary syndromes/infarction"
    - level_name: "Overlap & Summary"
      nodes:
        - id: "Overlap"
          type: process
          content: "Non-obstructive coronary atherosclerosis is frequently present."
          items: []
        - id: "Summary"
          type: process
          content: "These mechanisms can overlap"
          items: []
  edges:
    - from: "INOCA_start"
      to: "CMD"
      condition: ""
    - from: "INOCA_start"
      to: "VSA"
      condition: ""
    - from: "CMD"
      to: "Causes microvascular angina and contributes to myocardial ischaemia in CAD"
      condition: ""
    - from: "VSA"
      to: "Transient vasospasm → Prinzmetal angina"
      condition: ""
    - from: "VSA"
      to: "Persistent vasospasm → Myocardial infarction"
      condition: ""
    - from: "OCA_start"
      to: "Atherosclerosis"
      condition: ""
    - from: "Atherosclerosis"
      to: "Stable_plaque"
      condition: ""
    - from: "Atherosclerosis"
      to: "Vulnerable_plaque"
      condition: ""
    - from: "Stable_plaque"
      to: "Reduction in FFR"
      condition: ""
    - from: "Reduction in FFR"
      to: "Demand ischaemia ± angina"
      condition: ""
    - from: "Vulnerable_plaque"
      to: "Plaque rupture"
      condition: ""
    - from: "Plaque rupture"
      to: "Thrombosis"
      condition: ""
    - from: "Thrombosis"
      to: "Acute coronary syndromes/infarction"
      condition: ""
    - from: "CMD"
      to: "Overlap"
      condition: ""
    - from: "VSA"
      to: "Overlap"
      condition: ""
    - from: "Atherosclerosis"
      to: "Overlap"
      condition: ""
```

**图注说明**：  
CAD, coronary artery disease; FFR, fractional flow reserve.

---

### Table 1 Diagnostic criteria for microvascular angina

| Criteria | Evidence | Diagnostic parameters |
|----------|----------|------------------------|
| 1 | Symptoms of myocardial ischaemia<sup>a</sup> | Effort or rest angina<br>Exertional dyspnoea |
| 2 | Absence of obstructive CAD (<50% diameter reduction or FFR >0.80) | Coronary CTA<br>Invasive coronary angiography |
| 3 | Objective evidence of myocardial ischaemia<sup>b</sup> | Presence of reversible defect, abnormality or flow reserve on a functional imaging test |
| 4 | Evidence of impaired coronary microvascular function | Impaired coronary flow reserve (cut-off <2.0), invasive or noninvasively determined<br>Coronary microvascular spasm, defined as reproduction of symptoms, ischaemic ECG shifts but no epicardial spasm during acetylcholine testing<br>Abnormal coronary microvascular resistance indices (e.g. IMR ≥25) |

Definitive microvascular angina is only diagnosed if criteria 1, 2, 3 and 4 are present.  
CAD, coronary artery disease; CCTA, coronary computed tomographic angiography; ECG, electrocardiogram; FFR, fractional flow reserve; IMR, index of microcirculatory resistance.  

<sup>a</sup>Many patients with heart failure with preserved ejection fraction would fulfil these criteria: dyspnoea, no obstructive CAD and impaired CFR. For this reason, consider measuring LV end-diastolic pressure (normal ≤10 mmHg) and NT-proBNP normal <125 pg/mL.<sup>16</sup>  
<sup>b</sup>Signs of ischaemia may be present but are not necessary. However, evidence of impaired coronary microvascular function should be present.