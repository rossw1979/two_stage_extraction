---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "流程图", "position": "左上", "complexity": "中"}, {"type": "图片", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "低"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "标准提取"}
total_time_seconds: 133.14
page_num: 3
task_id: bc123ad6-8a35-475b-b5a4-ab85661b6c37
re_extracted: True
re_extract_focus: "需严格按双栏顺序输出：左上流程图 → 左下段落 → 右上图片及图注（保留原文'Fig 2'编号，删除VLM添加的'Three line charts...'解释性文字）→ 右下段落；确保图注仅转录原文文字，不增补说明"
review_needed: True
review_reason: "遗漏右上角三联曲线图（图2）的结构化表示或占位说明，需补充图表存在性标识及图题完整关联"
---

#### 图 1 GRACE study profile (derivation set of patients)

```yaml
flowchart:
  title: "GRACE study profile (derivation set of patients)"
  levels:
    - level_name: "Initial cohort"
      nodes:
        - id: "n26267"
          type: process
          content: "Patients with suspected acute coronary syndrome (n=26 267)"
    - level_name: "Excluded"
      nodes:
        - id: "excl_4579"
          type: process
          content: "Excluded (n=4579):"
          items:
            - "Non-cardiac diagnosis (n=1809)"
            - "Patients transferred from hospital outside study (n=2770)"
    - level_name: "Derivation dataset"
      nodes:
        - id: "n21688"
          type: process
          content: "GRACE risk score dataset (n=21 688)"
    - level_name: "6-month follow-up"
      nodes:
        - id: "alive_6m"
          type: process
          content: "Alive at 6 month follow-up (n=19 931)"
        - id: "dead_6m"
          type: process
          content: "Dead at 6 month follow-up (n=1757)"
    - level_name: "Outcomes (alive group)"
      nodes:
        - id: "nonfatal_mci_alive"
          type: process
          content: "Non-fatal myocardial infarction (n=1549)"
        - id: "alive_no_mci"
          type: process
          content: "Alive without myocardial infarction (n=18 382)"
    - level_name: "Outcomes (dead group)"
      nodes:
        - id: "death_in_hospital"
          type: process
          content: "Death in hospital (n=1046)"
        - id: "death_after_discharge"
          type: process
          content: "Death after discharge (n=711)"
  edges:
    - from: "n26267"
      to: "excl_4579"
    - from: "n26267"
      to: "n21688"
    - from: "n21688"
      to: "alive_6m"
    - from: "n21688"
      to: "dead_6m"
    - from: "alive_6m"
      to: "nonfatal_mci_alive"
    - from: "alive_6m"
      to: "alive_no_mci"
    - from: "dead_6m"
      to: "death_in_hospital"
    - from: "dead_6m"
      to: "death_after_discharge"
```

Early risks were highest for patients with ST segment elevation myocardial infarction but by six months the risk of death was similar to those with non-ST segment elevation myocardial infarction (fig 2). Of those who survived to six months after discharge, 36.2% (258/711) presented with ST segment elevation myocardial infarction compared with 50.0% (880/1757) of those who died during admission or follow-up. Raised cardiac markers were detected in 35.0% (6883/19688) of those who survived compared with 53.2% (905/1701) of those who died.

### Validation population  
The validation set comprised 22 122 patients enrolled in this multinational registry between 1 October 2003 and 30 September 2005. A total of 1730 (9.0%) patients died between hospital admission and six month follow-up, 948 in hospital (4.3% among patients with an admission diagnosis of acute coronary syndrome) and 782 (5.4%) after discharge. No information on mortality was available for 38 patients. In total, 2720 patients died (n=1730) or experienced a non-fatal myocardial infarction (n=990) between presentation and six month follow-up.

### Predictors of mortality  
From admission to six month follow-up, Killip class<sup>30</sup> and advanced age were the most powerful predictors of death in the univariable analysis (table 1). Table 1 also shows the other baseline characteristics and clinical parameters that predicted death or death or myocardial infarction.  

After multivariable analysis, the highest hazard ratios for death were cardiac arrest on admission and increasing age. These two key prognostic factors were closely followed by raised cardiac markers or enzyme activity and ST segment deviation (table 2).

### Risk models predicting death and death or myocardial infarction  
The risk model comprises 14 predictors of death and 12 predictors of death or myocardial infarction. The predictive accuracy of the model was good, with C-statistics of 0.82 for death in hospital and 0.70 for death or myocardial infarction in hospital (table 3). Nine factors independently predicted death and the combined end point in the period from admission to six months after discharge: age, congestive heart failure, peripheral vascular disease, systolic blood pressure, Killip class, initial serum creatinine concentration, positive initial cardiac markers, cardiac arrest on admission, and number of leads with ST deviation. The highest hazard ratio for adverse outcome was for cardiac arrest (tables 1 and 2).

### Prospective and external validation of the GRACE risk score  
When we tested the risk model in the prospective validation set, it had excellent predictive accuracy for death (C-statistic = 0.81, simplified model) and death or myocardial infarction (C-statistic = 0.73). The predictive accuracy was maintained across the acute coronary syndrome subgroups (table 3).  

We validated the model externally using the GUSTO IIb dataset of 12 142 patients with acute coronary syndrome. There was excellent discrimination despite the fact that one of the key parameters was not recorded in GUSTO IIb (cardiac arrest). The C-statistic for the death model in all patients was 0.82 (C-statistics = 0.80 for ST segment elevation myocardial infarction and 0.76 for non-ST segment elevation myocardial infarction).

### Development of a simplified nomogram for clinical application  
We reduced the overall models to include the most important variables that contained most (>90%) of the predictive informa-

#### 图 2 Overall risk of death in hospital, from hospital admission to six months after discharge (patients separated into unstable angina, non-ST segment elevation myocardial infarction, and ST segment elevation myocardial infarction), and from hospital discharge to six months