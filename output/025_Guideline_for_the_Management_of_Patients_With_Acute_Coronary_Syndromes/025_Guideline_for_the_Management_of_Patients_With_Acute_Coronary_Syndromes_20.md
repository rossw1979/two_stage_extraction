---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "图片", "position": "中央", "complexity": "高"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 63.38
page_num: 20
task_id: fcf64ee5-fb48-456e-86f5-3c9611d17599
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
该流程图指导在无需口服抗凝治疗的急性冠脉综合征（ACS）患者中，根据初始侵入性策略选择P2Y12抑制剂。流程始于“ACS：初始P2Y12抑制剂选择”，分为四条路径，分别对应：(1) 行PCI（NSTE-ACS或STEMI）；(2) 行CABG；(3) 无计划侵入性评估；(4) STEMI接受溶栓治疗。每条路径下进一步明确推荐的双联抗血小板方案（阿司匹林+替格瑞洛/普拉格雷/氯吡格雷），并标注推荐等级（Class 1），同时说明特殊情况下的替代方案或禁忌情形。

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
          recommendation: "Initial selection of oral P2Y12 inhibitor"
    - level_name: "Four clinical pathways"
      nodes:
        - id: "pci"
          type: process
          content: "PCI (NSTE-ACS or STEMI)"
          items:
            - "aspirin + ticagrelor or prasugrel (Class 1)"
            - "Clopidogrel when ticagrelor or prasugrel are not available, cannot be tolerated or contraindicated"
        - id: "cabg"
          type: process
          content: "CABG"
          items:
            - "aspirin + ticagrelor or clopidogrel (Class 1)"
            - "Continue aspirin during CABG and start P2Y12 inhibitor when safe postoperatively"
        - id: "no_invasive"
          type: process
          content: "No planned invasive evaluation"
          items:
            - "aspirin + ticagrelor (Class 1)"
            - "Clopidogrel when ticagrelor is not available, cannot be tolerated or contraindicated"
        - id: "fibrinolytic"
          type: process
          content: "Fibrinolytic in STEMI"
          items:
            - "aspirin + clopidogrel (Class 1)"
            - "Alternate P2Y12 inhibitor can be considered at PCI (if applicable)"
  edges:
    - from: "start"
      to: "pci"
    - from: "start"
      to: "cabg"
    - from: "start"
      to: "no_invasive"
    - from: "start"
      to: "fibrinolytic"
```

**图注说明**：  
Colors correspond to Class of Recommendation in Table 2.  
ACS indicates acute coronary syndromes; ASA, aspirin; CABG, coronary artery bypass grafting; NSTE-ACS, non–ST-segment elevation ACS; PCI, percutaneous coronary intervention; and STEMI, ST-segment elevation myocardial infarction.