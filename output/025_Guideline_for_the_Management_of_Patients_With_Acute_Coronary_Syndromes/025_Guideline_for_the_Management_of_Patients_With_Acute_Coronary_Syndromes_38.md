---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "右中", "complexity": "中"}, {"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "图片", "position": "中央", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 66.53
page_num: 38
task_id: 6c4107bb-63b2-4531-8c73-e413f2a0fa63
re_extracted: False
re_extract_focus: ""
review_needed: False
review_reason: ""
---

perform coronary revascularization by PCI or CABG (as appropriate) in patients with NSTE-ACS. This approach provides important prognostic information, including delineating the extent and severity of CAD. Several RCTs have demonstrated that a routine invasive approach in patients with NSTE-ACS reduces the risk of MACE when compared with a selective invasive approach.¹⁻³ Notably, these strategy trials were conducted in an era prior to the availability of hs-cTn assays, routine use of radial approach for coronary angiography, newer generation drug-eluting stents, and contemporary evidence-based antiplatelet therapies. Patients who are at prohibitively high risk from angiography or who have known coronary anatomy or preferences that preclude revascularization (PCI or CABG) may be managed non-invasively.¹³ In addition, some low-risk patients, particularly those who have normal cardiac biomarkers and in whom a diagnosis of an ACS is questioned, should be considered for a “selective invasive” approach that includes further noninvasive risk stratification prior to consideration of coronary angiography, because they derive less benefit from a routine invasive approach.⁴,⁷,¹³ These low-risk patients should still undergo noninvasive stress testing or coronary CT angiography prior to hospital discharge. Patients with higher risk findings on noninvasive testing or who have recurrent ischemic symptoms should be referred for invasive coronary angiography prior to hospital discharge in the absence of contraindication (Figure 7).

#### Figure 7 Selection of a Routine Invasive Versus Selected Invasive Strategy in Patients With NSTE-ACS

**Natural language overview**:  
The flowchart outlines the decision pathway for selecting between routine invasive and selective invasive strategies in patients with NSTE-ACS. It begins with initial risk stratification into "High- or intermediate-risk NSTE-ACS" versus "Lower-risk NSTE-ACS". High- or intermediate-risk patients proceed directly to a routine invasive strategy (Class I), which leads to either PCI or CABG. Lower-risk patients are directed toward a selective invasive strategy (Class I), which first requires noninvasive risk stratification (e.g., stress testing or CCTA) or assessment of recurrent ischemic symptoms; based on results (+ or −), patients may then proceed to medical therapy alone (with consideration of additional diagnostic workup for MINOCA cases) or to the routine invasive strategy.

**YAML structure**:
```yaml
flowchart:
  title: "Routine Invasive Versus Selective Invasive Strategy in Patients With NSTE-ACS"
  levels:
    - level_name: "Initial Risk Stratification"
      nodes:
        - id: "node_1"
          type: process
          content: "High- or intermediate-risk NSTE-ACS"
        - id: "node_2"
          type: process
          content: "Lower-risk NSTE-ACS"
    - level_name: "Strategy Assignment"
      nodes:
        - id: "node_3"
          type: process
          content: "Routine invasive strategy (Class I)"
          recommendation: "I"
          color_hint: "green"
        - id: "node_4"
          type: process
          content: "Selective invasive strategy (Class I)"
          recommendation: "I"
          color_hint: "green"
    - level_name: "Noninvasive Risk Stratification (for lower-risk group)"
      nodes:
        - id: "node_5"
          type: process
          content: "Noninvasive risk stratification (eg, stress testing or CCTA) or recurrent ischemic symptoms"
    - level_name: "Decision Point"
      nodes:
        - id: "node_6"
          type: decision
          content: "+"
        - id: "node_7"
          type: decision
          content: "−"
    - level_name: "Final Management"
      nodes:
        - id: "node_8"
          type: process
          content: "PCI"
        - id: "node_9"
          type: process
          content: "CABG"
        - id: "node_10"
          type: process
          content: "Medical therapy alone (consider additional diagnostic work up for cases of MINOCA*)"
  edges:
    - from: "node_1"
      to: "node_3"
    - from: "node_2"
      to: "node_4"
    - from: "node_3"
      to: "node_8"
    - from: "node_3"
      to: "node_9"
    - from: "node_4"
      to: "node_5"
    - from: "node_5"
      to: "node_6"
    - from: "node_5"
      to: "node_7"
    - from: "node_6"
      to: "node_3"
    - from: "node_7"
      to: "node_10"
```

**Figure caption**:  
Figure 7. Selection of a Routine Invasive Versus Selected Invasive Strategy in Patients With NSTE-ACS.  
Colors correspond to Class of Recommendation in Table 2. *AHA Scientific Statement on MINOCA.¹⁷ CABG indicates coronary artery bypass grafting; CCTA, cardiac CT angiography; MINOCA, myocardial infarction with nonobstructive coronary artery disease; NSTE-ACS, non–ST-segment elevation acute coronary syndromes; and PCI, percutaneous coronary intervention.

Recommendation-Specific Supportive Text  
1. In patients with NSTE-ACS, a routine invasive approach improves clinical outcomes, including lower rates of recurrent MI and recurrent ischemia, compared with a selective invasive approach that involves further noninvasive risk stratification prior to consideration of angiography.¹⁻³ In a collaborative meta-analysis of RCTs, a routine invasive approach reduced death or MI by 18% (OR, 0.82 [95% CI, 0.72–0.93]), including a 25% reduction in MI (OR, 0.75 [95% CI, 0.65–0.88]) when compared with a selective invasive approach.⁵ The benefit was more apparent in higher risk patients with elevated biomarkers.⁴ The studies that established the benefit of a routine invasive approach were conducted in the late 1990s and early 2000s, and it is unknown whether contemporary