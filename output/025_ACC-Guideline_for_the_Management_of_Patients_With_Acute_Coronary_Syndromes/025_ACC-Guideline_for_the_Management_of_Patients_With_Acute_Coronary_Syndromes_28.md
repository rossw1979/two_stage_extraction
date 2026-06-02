---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "左下", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 6, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 175.38
page_num: 28
task_id: 223d3f4c-1a46-4602-8d3d-97f1dc0f4d5a
re_extracted: True
re_extract_focus: "修正流程图YAML中Group 1路径的并列逻辑结构，并确保页面底部截断段落以原始不完整形式呈现（不隐式衔接表格），同时分离表格脚注与页底缩写释义段落。"
review_needed: False
review_reason: ""
---

#### 图 5 Management of Lipid-Lowering Therapy for Patients With ACS.

**自然语言概述**：  
该流程图针对住院急性冠脉综合征（ACS）患者的降脂治疗管理，根据患者基线他汀使用状态分为三类路径：  
1. **未使用他汀或使用低/中强度他汀者**：起始高强度他汀治疗（Ⅰ类推荐）；可考虑同步加用依折麦布（Ⅱb类）；4–8周后复查血脂并调整治疗以达目标。  
2. **已使用最大耐受剂量他汀者**：依据LDL-C水平分层处理——  
   - LDL-C <55 mg/dL：继续高强度他汀（Ⅰ类）；  
   - LDL-C 55–69 mg/dL：加用非他汀类降脂药合理（Ⅱa类）；  
   - LDL-C ≥70 mg/dL：加用非他汀类降脂药（Ⅰ类）；  
   所有分支均在4–8周后复查并调整。  
3. **他汀不耐受或拒绝者**：直接加用非他汀类降脂药（Ⅰ类），4–8周后复查调整治疗。  
所有“Reassess lipid profile 4–8 wk after discharge...”步骤均为Ⅰ类推荐。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Management of Lipid-Lowering Therapy for Patients With ACS"
  levels:
    - level_name: "Initial Assessment"
      nodes:
        - id: "start"
          type: process
          content: "Hospitalization with ACS"
        - id: "baseline_lipid"
          type: process
          content: "Baseline lipid profile"
    - level_name: "Patient Stratification"
      nodes:
        - id: "group1"
          type: decision
          content: "Patient not on statin or on low/moderate intensity regimen"
        - id: "group2"
          type: decision
          content: "Patient already on maximally tolerated statin regimen"
        - id: "group3"
          type: decision
          content: "Patient statin intolerant or refusal"
    - level_name: "Group 1 Pathway"
      nodes:
        - id: "g1_init"
          type: process
          content: "Initiation of high-intensity statin therapy"
          recommendation: "Class I"
        - id: "g1_ezetimibe"
          type: process
          content: "May consider concurrent addition of ezetimibe"
          recommendation: "Class IIb"
        - id: "g1_reassess"
          type: process
          content: "Reassess lipid profile 4–8 wk after discharge and adjust therapy as needed to achieve desired lipid targets"
          recommendation: "Class I"
    - level_name: "Group 2 Substratification"
      nodes:
        - id: "g2_ldl_low"
          type: decision
          content: "LDL-C <55 mg/dL"
        - id: "g2_ldl_mid"
          type: decision
          content: "LDL-C 55–69 mg/dL"
        - id: "g2_ldl_high"
          type: decision
          content: "LDL-C ≥70 mg/dL"
    - level_name: "Group 2 Interventions"
      nodes:
        - id: "g2_cont"
          type: process
          content: "Continue high-intensity statin"
          recommendation: "Class I"
        - id: "g2_add_nonstatin_reasonable"
          type: process
          content: "Addition of nonstatin* LDL-lowering therapy is reasonable"
          recommendation: "Class IIa"
        - id: "g2_add_nonstatin"
          type: process
          content: "Add a nonstatin* LDL-lowering therapy"
          recommendation: "Class I"
        - id: "g2_reassess"
          type: process
          content: "Reassess lipid profile 4–8 wk after discharge and adjust therapy as needed to achieve desired lipid targets"
          recommendation: "Class I"
    - level_name: "Group 3 Pathway"
      nodes:
        - id: "g3_add_nonstatin"
          type: process
          content: "Add a nonstatin* LDL-lowering therapy"
          recommendation: "Class I"
        - id: "g3_reassess"
          type: process
          content: "Reassess lipid profile 4–8 wk after discharge and adjust therapy as needed to achieve desired lipid targets"
          recommendation: "Class I"
  edges:
    - from: "start"
      to: "baseline_lipid"
    - from: "baseline_lipid"
      to: "group1"
    - from: "baseline_lipid"
      to: "group2"
    - from: "baseline_lipid"
      to: "group3"
    - from: "group1"
      to: "g1_init"
    - from: "g1_init"
      to: "g1_reassess"
    - from: "g1_init"
      to: "g1_ezetimibe"
    - from: "g1_ezetimibe"
      to: "g1_reassess"
    - from: "group2"
      to: "g2_ldl_low"
    - from: "group2"
      to: "g2_ldl_mid"
    - from: "group2"
      to: "g2_ldl_high"
    - from: "g2_ldl_low"
      to: "g2_cont"
    - from: "g2_ldl_mid"
      to: "g2_add_nonstatin_reasonable"
    - from: "g2_ldl_high"
      to: "g2_add_nonstatin"
    - from: "g2_cont"
      to: "g2_reassess"
    - from: "g2_add_nonstatin_reasonable"
      to: "g2_reassess"
    - from: "g2_add_nonstatin"
      to: "g2_reassess"
    - from: "group3"
      to: "g3_add_nonstatin"
    - from: "g3_add_nonstatin"
      to: "g3_reassess"
```

**图注说明**：  
Colors correspond to Class of Recommendation in Table 2.  
\*Nonstatin LDL-lowering therapy: ezetimibe, PCSK9 inhibitor (alirocumab, evolocumab and inclisiran), and/or bempedoic acid.  
ACS indicates acute coronary syndromes; LDL, low-density lipoprotein; LDL-C, low-density lipoprotein cholesterol; and PCSK9, proprotein convertase subtilisin/kexin type 9.

demonstrated in those patients enrolled closer to their ACS event.<sup>20,21</sup> Evolocumab effectively reduces LDL-C levels early after ACS and has demonstrated favorable changes on plaque components by intracoronary imaging in patients with NSTEMI.<sup>22–24</sup> Greater plaque regression has also been reported by intracoronary imaging for patients treated with alirocumab after AMI.<sup>25</sup> Inclisiran is a small interfering RNA targeting synthesis of the PCSK9 protein that is administered at 6-month intervals after an initial 3-month dose. Inclisiran lowers LDL-C levels by approximately 50% and is well tolerated,<sup>26</sup> but clinical outcome studies are not yet available. Bempedoic acid works upstream from statins in the liver and leads to approximately 20% reduction in LDL-C levels. It reduces MACE

### Table 11. Nonstatin Treatment Options for LDL-C Lowering in Patients With ACS Who Are Not at LDL-C Goal on Maximally Tolerated Statin Therapy

| Drug | Mechanism of Action | LDL-C Lowering (%) | Outcomes Study Performed in Patients With Recent ACS? | Potential Adverse Effects |
|------|---------------------|--------------------|--------------------------------------------------------|---------------------------|
| Ezetimibe\* | Blocks NPC1L1 cholesterol absorption | 15–25 | Yes (<10 d post ACS) | Liver function test abnormalities |
| Evolocumab | Monoclonal antibody to PCSK9 | ~60 | Established ASCVD (>1 mo post ACS) | Injection site reaction |
| Alirocumab | Monoclonal antibody to PCSK9 | ~60 | Yes (1–12 mo post ACS) | Injection site reaction |
| Inclisiran | Inhibitor of PCSK9 synthesis (small interfering RNA) | ~50 | Clinical outcomes trials in ASCVD are ongoing | Injection site reaction |
| Bempedoic acid† | ATP-citrate lyase inhibitor | ~20 | With or at high risk for CVD (>90 d post ACS) | Gout; gallstones; liver function test abnormalities |

All agents are approved by the FDA.  
\*The LDL-C lowering potency of ezetimibe is greater when used in combination with statin therapy (approximately 25% LDL-C reduction) than when used as monotherapy (15%–20%).  
†Coadministration of bempedoic acid with simvastatin at a dose >20 mg and pravastatin at a dose >40 mg is not recommended due to the increased risk of muscle-related adverse effects from statins.  

ACS indicates acute coronary syndromes; ASCVD, atherosclerotic cardiovascular disease; CVD, cardiovascular disease; FDA, US Food and Drug Administration; LDL-C, low-density lipoprotein cholesterol; NPC1L1, Niemann-Pick C1-Like 1 protein; and PCSK9, proprotein convertase subtilisin/kexin type 9.