---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "表格", "position": "中央", "complexity": "高"}], "tables": {"count": 1, "max_rows_estimate": 6, "has_merged_cells": true, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 152.28
page_num: 58
task_id: 6ec8f590-ec5e-4e27-9ee2-9dbc6350af5a
re_extracted: True
re_extract_focus: "需修正排版顺序（将编号段落5作为首个内容块）、补全图注并明确标注原文截断处、校正流程图节点的时间点标注与原文一致"
review_needed: True
review_reason: "遗漏左栏前4段正文及右栏全部段落；YAML流程图结构错误，需按原图二维布局重构为单level多nodes并列结构，并完整提取图注与所有文字段落"
---

5. In the MASTER DAPT (Management of High Bleeding Risk Patients Post Bioresorbable Polymer Coated Stent Implantation With an Abbreviated Versus Standard DAPT Regimen) trial, patients at high risk of bleeding who had completed a 4-week course of DAPT after successful PCI with drug-eluting stents were randomly allocated to single antiplatelet therapy or more prolonged DAPT (≥2

#### 图 11 DAPT Strategies in the First 12 Months Postdischarge.

**自然语言概述**：  
该流程图以急性冠脉综合征（ACS）为起点，根据患者出血风险及是否行经皮冠状动脉介入治疗（PCI），将双联抗血小板治疗（DAPT）策略分为三类路径：默认策略、PCI术后出血减少策略、高出血风险PCI术后策略。时间轴纵轴为出院后1周至12个月，横轴按策略分组。各策略下推荐的药物组合、停用阿司匹林时机、降阶治疗（de-escalation）或升阶治疗（escalation）节点均以颜色编码，并标注推荐等级（Class 1 或 Class 2b）。绿色代表标准DAPT或SAPT方案（低/中出血风险），橙色代表高出血风险策略；虚线框表示需在特定时间点停用阿司匹林。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "DAPT Strategies in the First 12 Months Postdischarge"
  timeline: ["1 wk", "1 mo", "3 mo", "6 mo", "9 mo", "12 mo"]
  levels:
    - level_name: "Initial Condition"
      nodes:
        - id: "acs"
          type: start
          content: "ACS"
          recommendation: ""
          color_hint: ""
    - level_name: "Strategy Branches"
      nodes:
        - id: "default"
          type: process
          content: "Default strategy"
          recommendation: ""
          color_hint: ""
        - id: "bleeding_reduction"
          type: process
          content: "Bleeding reduction strategies post PCI"
          recommendation: ""
          color_hint: ""
        - id: "high_bleeding_risk"
          type: process
          content: "High bleeding risk post PCI*"
          recommendation: ""
          color_hint: ""
  edges:
    - from: "acs"
      to: "default"
      condition: ""
    - from: "acs"
      to: "bleeding_reduction"
      condition: ""
    - from: "acs"
      to: "high_bleeding_risk"
      condition: ""

    # Default strategy path (green column)
    - level_name: "Default Strategy Timeline"
      nodes:
        - id: "default_12mo"
          type: process
          content: "DAPT ≥12 mo<br>(ticagrelor/prasugrel preferred post PCI)<br>(Class 1)"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
          timeline_point: "12 mo"
        - id: "default_sapt"
          type: process
          content: "SAPT<br>(ticagrelor monotherapy)<br>(Class 1)"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
          timeline_point: "6 mo"
      edges: []

    # Bleeding reduction strategies post PCI (middle columns)
    - level_name: "Bleeding Reduction Path"
      nodes:
        - id: "dapt_1_3mo"
          type: process
          content: "DAPT<br>(aspirin + ticagrelor)<br>Discontinue aspirin 1–3 mo post PCI"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline_point: "1–3 mo"
        - id: "triple_1_4wk"
          type: process
          content: "Triple therapy<br>(DAPT + OAC)<br>Discontinue aspirin 1–4 wk post PCI"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline_point: "1–4 wk"
        - id: "sapt_oac"
          type: process
          content: "SAPT + OAC<br>(clopidogrel monotherapy and OAC)<br>(Class 1)"
          items: []
          recommendation: "Class 1"
          color_hint: "green"
          timeline_point: "6 mo"
        - id: "dapt_asp_clopidogrel"
          type: process
          content: "DAPT<br>(aspirin + clopidogrel)<br>(Class 2b)"
          items: []
          recommendation: "Class 2b"
          color_hint: "orange"
          timeline_point: "6 mo"
        - id: "dapt_asp_tica_pras"
          type: process
          content: "DAPT<br>(aspirin + ticagrelor/prasugrel)<br>Deescalate potency of P2Y12 inhibitor >1 mo post PCI"
          items: []
          recommendation: ""
          color_hint: "orange"
          timeline_point: "3 mo"
      edges: []

    # High bleeding risk post PCI (rightmost orange column)
    - level_name: "High Bleeding Risk Path"
      nodes:
        - id: "highrisk_dapt"
          type: process
          content: "DAPT<br>(aspirin + P2Y12 inhibitor)<br>Stop aspirin or P2Y12 inhibitor >1 mo post PCI"
          items: []
          recommendation: ""
          color_hint: "orange"
          timeline_point: "1–3 mo"
        - id: "highrisk_sapt"
          type: process
          content: "SAPT<br>(aspirin or P2Y12 inhibitor monotherapy)<br>(Class 2b)"
          items: []
          recommendation: "Class 2b"
          color_hint: "orange"
          timeline_point: "6 mo"
      edges: []

  notes:
    - "Colors correspond to Class of Recommendation in Table 2."
    - "*High bleeding risk discussed in Section 11.1, 'Recommendation-Specific Supportive Text' item 5, and outlined in Table 22."
    - "ACS indicates acute coronary syndromes; DAPT, dual antiplatelet therapy; OAC, oral anticoagulant; PCI, percutaneous coronary intervention; and SAPT, single antiplatelet therapy."
```