---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "流程图", "position": "中央", "complexity": "高"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 73.15
page_num: 20
task_id: 37ba9e17-acf3-459b-9f1b-25caec32f255
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

egy and their risk of bleeding (Figure 4).¹⁻⁵,⁹,¹⁰ Clinically available oral P2Y12 inhibitors include clopidogrel, prasugrel, and ticagrelor. Clopidogrel is the least potent oral P2Y12 inhibitor and requires more time to reach its maximal platelet inhibition after a loading dose, because it requires biotransformation in the liver to form its active metabolite. Pharmacodynamic variability in response in clopidogrel has been well described,¹⁴,¹⁵ and hyporesponders may be at increased risk of MACE and stent thrombosis when treated with clopidogrel after PCI.¹⁶,¹⁷ Ticagrelor and prasugrel are more potent than clopidogrel and achieve more rapid onset of inhibition of platelet activation but with increased risk of bleeding compared with clopidogrel. Of note, ticagrelor may cause subjective transient dyspnea in approximately 10% to 15% of patients after ACS.⁵ The topic of duration of dual antiplatelet therapy is addressed in Section 11.1, “DAPT Strategies in the First 12 Months Postdischarge.”

recurrent MI, and improves survival.²,³ Moreover, in randomized trials, the use of prasugrel and ticagrelor further reduced risk of MACE, as well as stent thrombosis, when compared with clopidogrel in patients with STEMI (not receiving concurrent fibrinolytic therapy) or NSTE-ACS.⁴,⁵ The benefits of oral P2Y12 inhibitors have also been demonstrated in patients after coronary artery bypass graft (CABG) surgery.¹⁸⁻²¹ Guidance on dosing interruption for patients referred for CABG is in Table 8. Duration of administration after CABG is described in Section 11.1, “DAPT Strategies in the First 12 Months Postdischarge.”

2. In a secondary analysis of the randomized, double-blind TRITON-TIMI 38 (Trial to Assess Improvement in Therapeutic Outcomes by Optimizing Platelet Inhibition with Prasugrel–Thrombolysis in Myocardial Infarction) of prasugrel versus clopidogrel in addition to aspirin among patients with ACS, subgroup analyses using an outcome of net clinical benefit (MACE events plus bleeding) demonstrated net harm with prasugrel versus clopidogrel among patients with previous transient ischemic attack or stroke.⁴ Dose reduction of prasugrel should be considered in patients ≥75 years of age and in those with a body weight <60 kg (Table 7).

3. The randomized, double-blind TRITON-TIMI 38 and PLATO trials demonstrated that prasugrel (TRITON-TIMI 38) or ticagrelor (PLATO) reduced the rate of the composite endpoint of

#### 图 4 Initial Choice of P2Y12 Inhibitor in Patients Not Requiring an Oral Anticoagulant.

**自然语言概述**：  
该流程图指导急性冠脉综合征（ACS）患者在无需口服抗凝治疗时，初始P2Y12抑制剂的选择路径。依据是否计划行侵入性评估（PCI或CABG）及是否接受溶栓治疗，分为四条主路径：① 行PCI（NSTE-ACS或STEMI）；② 行CABG；③ 无计划侵入性评估；④ STEMI接受溶栓治疗。每条路径下进一步根据药物可获得性、耐受性及禁忌证推荐具体方案，并标注推荐等级（Class 1）。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Initial selection of oral P2Y12 inhibitor"
  levels:
    - level_name: "Initial decision"
      nodes:
        - id: "start"
          type: process
          content: "ACS"
          recommendation: ""
          color_hint: ""
    - level_name: "Pathway branches"
      nodes:
        - id: "pci"
          type: process
          content: "PCI (NSTE-ACS or STEMI)"
          items: []
          recommendation: ""
          color_hint: "gray"
        - id: "cabg"
          type: process
          content: "CABG"
          items: []
          recommendation: ""
          color_hint: "lightblue"
        - id: "no_invasive"
          type: process
          content: "No planned invasive evaluation"
          items: []
          recommendation: ""
          color_hint: "lightgreen"
        - id: "fibrinolytic"
          type: process
          content: "Fibrinolytic in STEMI"
          items: []
          recommendation: ""
          color_hint: "teal"
    - level_name: "PCI pathway options"
      nodes:
        - id: "pci_option1"
          type: process
          content: "aspirin + ticagrelor or prasugrel"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
        - id: "pci_option2"
          type: process
          content: "Clopidogrel when ticagrelor or prasugrel are not available, cannot be tolerated or contraindicated"
          items: []
          recommendation: ""
          color_hint: "white"
    - level_name: "CABG pathway options"
      nodes:
        - id: "cabg_option1"
          type: process
          content: "aspirin + ticagrelor or clopidogrel"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
        - id: "cabg_option2"
          type: process
          content: "Continue aspirin during CABG and start P2Y12 inhibitor when safe postoperatively"
          items: []
          recommendation: ""
          color_hint: "white"
    - level_name: "No invasive pathway options"
      nodes:
        - id: "no_invasive_option1"
          type: process
          content: "aspirin + ticagrelor"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
        - id: "no_invasive_option2"
          type: process
          content: "Clopidogrel when ticagrelor is not available, cannot be tolerated or contraindicated"
          items: []
          recommendation: ""
          color_hint: "white"
    - level_name: "Fibrinolytic pathway options"
      nodes:
        - id: "fibrinolytic_option1"
          type: process
          content: "aspirin + clopidogrel"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
        - id: "fibrinolytic_option2"
          type: process
          content: "Alternate P2Y12 inhibitor can be considered at PCI (if applicable)"
          items: []
          recommendation: ""
          color_hint: "white"
  edges:
    - from: "start"
      to: "pci"
      condition: ""
    - from: "start"
      to: "cabg"
      condition: ""
    - from: "start"
      to: "no_invasive"
      condition: ""
    - from: "start"
      to: "fibrinolytic"
      condition: ""
    - from: "pci"
      to: "pci_option1"
      condition: ""
    - from: "pci"
      to: "pci_option2"
      condition: ""
    - from: "cabg"
      to: "cabg_option1"
      condition: ""
    - from: "cabg"
      to: "cabg_option2"
      condition: ""
    - from: "no_invasive"
      to: "no_invasive_option1"
      condition: ""
    - from: "no_invasive"
      to: "no_invasive_option2"
      condition: ""
    - from: "fibrinolytic"
      to: "fibrinolytic_option1"
      condition: ""
    - from: "fibrinolytic"
      to: "fibrinolytic_option2"
      condition: ""
```

**图注说明**：  
Colors correspond to Class of Recommendation in Table 2.  
ACS indicates acute coronary syndromes; ASA, aspirin; CABG, coronary artery bypass grafting; NSTE-ACS, non–ST-segment elevation ACS; PCI, percutaneous coronary intervention; and STEMI, ST-segment elevation myocardial infarction.