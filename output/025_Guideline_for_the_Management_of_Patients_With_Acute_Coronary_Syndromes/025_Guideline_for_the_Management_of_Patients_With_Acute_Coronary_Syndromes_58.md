---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 186.66
page_num: 58
task_id: 84c736f6-11ff-4d7e-ae8a-d01f49d2757c
re_extracted: True
re_extract_focus: "需严格按双栏顺序输出：先完整提取左栏全部段落（含编号4段落全文），再提取右栏段落（含编号5段落，保持截断状态）；修正YAML流程图中默认策略各时间点节点缺失与内容错位问题，并删除所有参考文献上标。"
review_needed: True
review_reason: "需严格按双栏顺序分离左下与右下段落，并完整保留两段正文内容（含编号4.和5.起始部分），确保页面末尾截断处不补全、仅忠实呈现原文不完整状态"
---

#### 图 11 DAPT Strategies in the First 12 Months Postdischarge.

自然语言概述：  
该流程图展示了急性冠脉综合征（ACS）患者在经皮冠状动脉介入治疗（PCI）后前12个月的双联抗血小板治疗（DAPT）策略选择路径，依据出血风险分层与时间轴动态调整。整体结构分为三大主干策略：默认策略（Default strategy）、PCI术后出血风险降低策略（Bleeding reduction strategies post PCI）、高出血风险患者PCI术后策略（High bleeding risk post PCI*）。各策略按时间点（1周、1月、3月、6月、9月、12月）纵向展开，推荐方案以颜色编码对应推荐等级（见图注），并标注了具体药物组合、停药时机及证据等级。

YAML 结构化数据：

```yaml
flowchart:
  title: "DAPT Strategies in the First 12 Months Postdischarge"
  levels:
    - level_name: "Initial Stratification (Index admission)"
      nodes:
        - id: "acs"
          type: process
          content: "ACS"
          recommendation: ""
          color_hint: ""
    - level_name: "Strategy Branches"
      nodes:
        - id: "default_strategy"
          type: process
          content: "Default strategy"
          recommendation: ""
          color_hint: "light blue"
        - id: "bleeding_reduction"
          type: process
          content: "Bleeding reduction strategies post PCI"
          recommendation: ""
          color_hint: "light blue"
        - id: "high_bleeding_risk"
          type: process
          content: "High bleeding risk post PCI*"
          recommendation: ""
          color_hint: "light blue"
    - level_name: "Time-based Recommendations (1 wk–12 mo)"
      nodes:
        - id: "default_1wk"
          type: process
          content: "DAPT ≥12 mo (ticagrelor/prasugrel preferred post PCI) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "1 wk"
        - id: "default_1mo"
          type: process
          content: "DAPT ≥12 mo (ticagrelor/prasugrel preferred post PCI) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "1 mo"
        - id: "default_3mo"
          type: process
          content: "DAPT ≥12 mo (ticagrelor/prasugrel preferred post PCI) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "3 mo"
        - id: "default_6mo"
          type: process
          content: "DAPT ≥12 mo (ticagrelor/prasugrel preferred post PCI) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "6 mo"
        - id: "default_9mo"
          type: process
          content: "DAPT ≥12 mo (ticagrelor/prasugrel preferred post PCI) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "9 mo"
        - id: "default_12mo"
          type: process
          content: "DAPT ≥12 mo (ticagrelor/prasugrel preferred post PCI) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "12 mo"
        - id: "bleed_red_dapt_1wk"
          type: process
          content: "DAPT (aspirin + ticagrelor)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "1 wk"
        - id: "bleed_red_dapt_1_3mo"
          type: process
          content: "Discontinue aspirin 1–3 mo post PCI"
          items: []
          recommendation: ""
          color_hint: "light green"
          timeline: "1–3 mo"
        - id: "bleed_red_triple_1_4wk"
          type: process
          content: "Triple therapy (DAPT + OAC)"
          items:
            - "Discontinue aspirin 1–4 wk post PCI"
          recommendation: ""
          color_hint: "green"
          timeline: "1–4 wk"
        - id: "bleed_red_sapt_oac_3mo"
          type: process
          content: "SAPT + OAC (clopidogrel monotherapy and OAC) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "3 mo"
        - id: "bleed_red_sapt_6mo"
          type: process
          content: "SAPT (ticagrelor monotherapy) (Class I)"
          items: []
          recommendation: ""
          color_hint: "green"
          timeline: "6 mo"
        - id: "high_risk_dapt_1wk"
          type: process
          content: "DAPT (aspirin + ticagrelor/prasugrel)"
          items: []
          recommendation: ""
          color_hint: "orange"
          timeline: "1 wk"
        - id: "high_risk_dapt_1mo"
          type: process
          content: "DAPT (aspirin + P2Y12 inhibitor)"
          items:
            - "Deescalate potency of P2Y12 inhibitor >1 mo post PCI"
          recommendation: ""
          color_hint: "orange"
          timeline: "1 mo"
        - id: "high_risk_stop_asp_1mo"
          type: process
          content: "Stop aspirin or P2Y12 inhibitor >1 mo post PCI"
          items: []
          recommendation: ""
          color_hint: "orange"
          timeline: "1 mo"
        - id: "high_risk_dapt_3mo"
          type: process
          content: "DAPT (aspirin + clopidogrel) (Class 2b)"
          items: []
          recommendation: ""
          color_hint: "orange"
          timeline: "3 mo"
        - id: "high_risk_sapt_6mo"
          type: process
          content: "SAPT (aspirin or P2Y12 inhibitor monotherapy) (Class 2b)"
          items: []
          recommendation: ""
          color_hint: "orange"
          timeline: "6 mo"
  edges:
    - from: "acs"
      to: "default_strategy"
      condition: ""
    - from: "acs"
      to: "bleeding_reduction"
      condition: ""
    - from: "acs"
      to: "high_bleeding_risk"
      condition: ""
    - from: "default_strategy"
      to: "default_1wk"
      condition: "Index admission → continue ≥12 mo"
    - from: "default_strategy"
      to: "default_1mo"
      condition: "1 mo"
    - from: "default_strategy"
      to: "default_3mo"
      condition: "3 mo"
    - from: "default_strategy"
      to: "default_6mo"
      condition: "6 mo"
    - from: "default_strategy"
      to: "default_9mo"
      condition: "9 mo"
    - from: "default_strategy"
      to: "default_12mo"
      condition: "12 mo"
    - from: "bleeding_reduction"
      to: "bleed_red_dapt_1wk"
      condition: "1 wk"
    - from: "bleeding_reduction"
      to: "bleed_red_dapt_1_3mo"
      condition: "1–3 mo"
    - from: "bleeding_reduction"
      to: "bleed_red_triple_1_4wk"
      condition: "1–4 wk (if OAC needed)"
    - from: "bleeding_reduction"
      to: "bleed_red_sapt_oac_3mo"
      condition: "3 mo"
    - from: "bleeding_reduction"
      to: "bleed_red_sapt_6mo"
      condition: "6 mo"
    - from: "high_bleeding_risk"
      to: "high_risk_dapt_1wk"
      condition: "1 wk"
    - from: "high_bleeding_risk"
      to: "high_risk_dapt_1mo"
      condition: "1 mo"
    - from: "high_bleeding_risk"
      to: "high_risk_stop_asp_1mo"
      condition: ">1 mo post PCI (de-escalation option)"
    - from: "high_bleeding_risk"
      to: "high_risk_dapt_3mo"
      condition: "3 mo"
    - from: "high_bleeding_risk"
      to: "high_risk_sapt_6mo"
      condition: "6 mo"
```

图注说明：  
Colors correspond to Class of Recommendation in Table 2. *High bleeding risk discussed in Section 11.1, “Recommendation-Specific Supportive Text” item 5, and outlined in Table 22. ACS indicates acute coronary syndromes; DAPT, dual antiplatelet therapy; OAC, oral anticoagulant; PCI, percutaneous coronary intervention; and SAPT, single antiplatelet therapy.

oral anticoagulant. Because the conversion of clopidogrel to its active metabolite and the metabolism of certain PPIs depend on some common hepatic enzymes (eg, CYP2C19), the potential for a drug-drug interaction exists when both agents are coadministered. The results of several ex vivo studies found that clopidogrel-induced platelet inhibition is attenuated with use of certain PPIs, a pharmacodynamic effect that is most pronounced with omeprazole. Nonetheless, results from a double-blind, placebo-controlled randomized trial showed no significant differences in ischemic events between omeprazole versus placebo among patients treated with clopidogrel, but PPI use markedly decreased the risk of gastrointestinal bleeding. Moreover, post hoc analyses from several randomized trials have shown that ischemic risk is not increased when a clinically indicated PPI is used with clopidogrel. Importantly, the antiplatelet effects and clinical efficacy of ticagrelor and prasugrel are not appreciably modified with concomitant PPI use. Therefore, it is recommended to administer a PPI in patients with ACS at elevated bleeding risk treated with DAPT or oral anticoagulant.

4. De-escalation implies modulating DAPT intensity by switching from ticagrelor or prasugrel to clopidogrel. De-escalation can be guided by the results of platelet function assays that quantify the degree of platelet inhibition among patients treated with clopidogrel. Patients with adequate response may continue to receive clopidogrel, whereas nonresponders are switched to a more potent P2Y12 inhibitor. Clopidogrel responsiveness may also be inferred with use of genotyping assays that identify polymorphisms in genes involved in clopidogrel metabolism. Clinical trials examining guided de-escalation after PCI have either shown a lack of benefit, noninferiority, or reductions in minor bleeding versus conventional DAPT. By contrast, unguided de-escalation is performed without antecedent knowledge of platelet responsiveness. Randomized trials have suggested that unguided de-escalation 1 month after PCI reduces bleeding without incurring ischemic risk as compared with longer term prasugrel- or ticagrelor-based DAPT. Pooled analyses have shown that de-escalation (guided or unguided) yields comparable efficacy to DAPT with respect to ischemic events while reducing bleeding. However, trials of ticagrelor and prasugrel have suggested that the benefit of more potent P2Y12 inhibitor therapy extends beyond the early phase post ACS, but with increased bleeding.

5. In the MASTER DAPT (Management of High Bleeding Risk Patients Post Bioresorbable Polymer Coated Stent Implantation With an Abbreviated Versus Standard DAPT Regimen) trial, patients at high risk of bleeding who had completed a 4-week course of DAPT after successful PCI with drug-eluting stents were randomly allocated to single antiplatelet therapy or more prolonged DAPT (≥2