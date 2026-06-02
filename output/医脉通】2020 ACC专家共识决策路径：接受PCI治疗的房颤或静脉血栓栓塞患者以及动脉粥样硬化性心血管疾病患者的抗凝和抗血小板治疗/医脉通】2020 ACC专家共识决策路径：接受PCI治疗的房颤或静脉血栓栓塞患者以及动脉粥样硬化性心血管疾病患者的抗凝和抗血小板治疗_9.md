---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "中央（嵌入图中）", "complexity": "高"}], "tables": {"count": 1, "max_rows_estimate": 8, "has_merged_cells": true, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 163.11
page_num: 9
task_id: 0d18e6b7-5c0f-4f9c-8ee9-1796a7333365
re_extracted: True
re_extract_focus: "需重构流程图部分，将原图中‘Post-PCI Regimen by Indication’的双栏时间-方案表格结构准确映射为结构化数据（如用嵌套列表或分栏字段表示左右栏对应关系），并补全图下方的缩写定义脚注段落。"
review_needed: True
review_reason: "需重构流程图 YAML 结构以准确反映时间轴分层逻辑，并补全右下角未提取的 'b)' 后续内容及图下方注释"
---

#### 图 2 Patient With AF on AC Who Now Needs PCI

**Medication Key**  
**Antiplatelet therapy**  
- APT = Antiplatelet therapy  
- ASA = Aspirin  
- P2Y₁₂i = P2Y₁₂ inhibitor  

**Anticoagulant therapy**  
- OAC = Oral anticoagulant  
- DOAC = Direct oral anticoagulant  
- VKA = Vitamin K antagonist  

**Acid Blockers**  
- H₂ Blocker = Histamine H2-receptor antagonist  
- PPI = Proton pump inhibitor  

* *See Table 2: Dosing Table for Atrial Fibrillation.*  
† See text for DOAC dosing.  
‡ For those on a VKA, aspirin (81 mg daily) should be continued until the INR is in the therapeutic range.  
§ Clopidogrel preferred over prasugrel/ticagrelor to the extent possible.  
‖ If BMS, duration of P2Y₁₂i is 1 month.  
¶ The time frames listed here represent treatment durations post-PCI.  
# Early discontinuation in those at high risk of bleeding is reasonable (after 3 months for SIHD and after 6 months for ACS).  
** If perceived thrombotic risk is high and bleeding risk is low, continuation of SAPT (ASA 81 mg daily or clopidogrel 75 mg daily) beyond 12 months is reasonable.  

AC = anticoagulant; ACS = acute coronary syndrome;  
AF = atrial fibrillation; BMS = bare metal stent; DES = drug-eluting stent; INR = international normalized ratio;  
PCI = percutaneous coronary intervention; SIHD = stable ischemic heart disease.

```yaml
flowchart:
  title: "Patient With AF on AC Who Now Needs PCI"
  levels:
    - level_name: "Initial Assessment"
      nodes:
        - id: "node_1"
          type: process
          content: "Patient With AF on Indefinite OAC"
          recommendation: ""
          color_hint: ""
    - level_name: "Decision Point"
      nodes:
        - id: "node_2"
          type: decision
          content: "Who Needs PCI?"
          recommendation: ""
          color_hint: ""
    - level_name: "Pre-PCI Anticoagulation"
      nodes:
        - id: "node_3"
          type: process
          content: "OAC Prior to PCI"
          items:
            - "VKA"
            - "DOAC"
          recommendation: ""
          color_hint: ""
    - level_name: "Periprocedural Management"
      nodes:
        - id: "node_4"
          type: process
          content: "Follow PCI Periprocedural Management (See Figure 3)"
          recommendation: ""
          color_hint: "green"
    - level_name: "Post-procedure Strategy"
      nodes:
        - id: "node_5"
          type: process
          content: "RESTART OAC"
          items:
            - "DOAC† preferred"
            - "P2Y₁₂i§"
          recommendation: ""
          color_hint: "yellow"
        - id: "node_6"
          type: process
          content: "RESTART pre-PCI"
          items:
            - "DOAC† & INITIATE P2Y₁₂i§"
          recommendation: ""
          color_hint: "yellow"
        - id: "node_7"
          type: process
          content: "INITIATE P2Y₁₂i§"
          recommendation: ""
          color_hint: "yellow"
    - level_name: "Triple Therapy Option"
      nodes:
        - id: "node_8"
          type: process
          content: "Start or continue PPI or H₂ Blocker"
          recommendation: "Can add ASA 81 mg daily for limited period of time (as part of triple therapy) if thrombotic risk is high and bleeding risk is low"
          color_hint: "lightblue"
    - level_name: "Post-PCI Regimen by Indication"
      nodes:
        - id: "node_9"
          type: process
          content: "PCI for SIHD (DES)‡"
          items:
            - "Discharge (0): Continue P2Y₁₂i§ for 0–6 months (clopidogrel preferred)"
            - "1–3 mo: Continue P2Y₁₂i§ OR switch to ASA for 6–12 months"
            - "6–12 mo: Continue OAC"
            - "12 mo: STOP** APT / Continue OAC indefinitely"
          recommendation: ""
          color_hint: "pink"
        - id: "node_10"
          type: process
          content: "PCI for ACS (BMS/DES)‡"
          items:
            - "Discharge (0): Continue P2Y₁₂i§ for 0–12 months (clopidogrel preferred)"
            - "1–12 mo: Continue OAC"
            - "12 mo: STOP** APT / Continue OAC indefinitely"
          recommendation: ""
          color_hint: "pink"
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
    - from: "node_4"
      to: "node_6"
      condition: ""
    - from: "node_4"
      to: "node_7"
      condition: ""
    - from: "node_5"
      to: "node_8"
      condition: ""
    - from: "node_6"
      to: "node_8"
      condition: ""
    - from: "node_7"
      to: "node_8"
      condition: ""
    - from: "node_8"
      to: "node_9"
      condition: ""
    - from: "node_8"
      to: "node_10"
      condition: ""
```

Figures 2 and 3 provide an overview of the patient with pre-existing AF receiving an OAC who presents for PCI. In general, if the patient was on a DOAC before PCI, the same DOAC would be continued afterwards, with the addition of a P2Y₁₂i (clopidogrel is generally preferred). If the patient was on a VKA previously, the VKA could be reinitiated post-PCI, although the preferred option in eligible patients would be to substitute a DOAC instead. Assessment of the type and dose of DOAC can be based on the clinical trial results. An unusual scenario would be a patient who was on a DOAC for AF prior to PCI who then develops a specific allergy or significant renal dysfunction that precludes further use of a DOAC and instead warrants the transition to a VKA, or switching to another DOAC.

Low-dose aspirin is recommended for the duration of the hospitalization, and in general, we recommend discontinuing it prior to/upon discharge in most patients (71). Although the default approach is DAPT, because the risk of stent-related thrombotic complications is greatest in the first month post-PCI, one may consider continuing aspirin (81 mg/day) for 30 days (at which point the patient should switch to an OAC and P2Y₁₂i) in those with high thrombotic risk and low bleeding risk. Alternatively, in patients at particularly high stent thrombosis risk (e.g., patients with ACS), ticagrelor may be used in lieu of clopidogrel as the P2Y₁₂i agent of choice, although data on ticagrelor are limited. At this time, we do not recommend prasugrel as a component of a triple-therapy regimen. In 1 small study, triple therapy using a VKA, aspirin, and prasugrel was associated with a 4-fold higher rate of bleeding (72). As discussed in the previous text, the duration of P2Y₁₂i monotherapy should be, in general, 6 months for SIHD and 12 months for ACS.

### 5.1.1. General Principles  
1. The proposed antithrombotic regimen should always account for the patient’s ischemic and bleeding risk as well as presentation (SIHD vs. ACS). An individualized approach is important.  
2. For OAC therapy post-PCI in patients with AF, a DOAC is preferred, owing to its: a) lower risk of major, fatal, and intracranial bleeding compared with a VKA; b)