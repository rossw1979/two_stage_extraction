---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "表格", "position": "左上", "complexity": "高"}, {"type": "表格", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "低"}, {"type": "图片", "position": "右下", "complexity": "中"}], "tables": {"count": 2, "max_rows_estimate": 25, "has_merged_cells": true, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 195.47
page_num: 4
task_id: 93c2e037-b09e-41fe-b1ac-2baa755cb03f
re_extracted: True
re_extract_focus: "左下段落起始处存在截断句被错误处理为独立短语'tion.'，需严格按原文截断状态保留（不补全），并确保图注、表格脚注与主体内容位置绑定正确"
review_needed: True
review_reason: "修正跨页延续段落截断问题（左下段落以'tion.'开头需还原为完整延续句），并确保图注、脚注与原文标点/上标严格对应，避免混淆参考文献标号与脚注符号"
---

Table 2 Final risk models predicting death and death or myocardial infarction from hospital admission to six month follow-up (hazard ratios and 95% confidence intervals)

| Predictors | χ² | Death model | χ² | Death/MI model |
|---|---|---|---|---|
| Age (per 10 year increase) | 505.7 | 1.8 (1.68 to 1.84) | 176.3 | 1.25 (1.21 to 1.29) |
| Medical history: | | | | |
| &nbsp;&nbsp;Congestive heart failure | 34.2 | 1.5 (1.32 to 1.73) | 22.1 | 1.3 (1.17 to 1.45) |
| &nbsp;&nbsp;Hypertension | 8.8 | 1.2 (1.05 to 1.33) | — | — |
| &nbsp;&nbsp;Peripheral vascular disease | 21.8 | 1.4 (1.21 to 1.62) | 10.5 | 1.2 (1.08 to 1.36) |
| &nbsp;&nbsp;PCI | 8.3 | 0.8 (0.64 to 0.93) | — | — |
| Presentation characteristics: | | | | |
| &nbsp;&nbsp;Pulse (per 30 beats/min increase) | 44.3 | 1.2 (1.16 to 1.31) | — | — |
| &nbsp;&nbsp;Systolic blood pressure (per 20 mm Hg decrease) | 152.0 | 1.2 (1.22 to 1.30) | 52.9 | 1.1 (1.07 to 1.13) |
| &nbsp;&nbsp;Killip class<sup>20</sup> (per level increase) | 142.8 | 1.5 (1.41 to 1.62) | 126.2 | 1.4 (1.30 to 1.46) |
| &nbsp;&nbsp;Initial serum creatinine (per 88 μmol/l* increase) | 135.3 | 1.2 (1.19 to 1.29) | 41.1 | 1.1 (1.08 to 1.16) |
| &nbsp;&nbsp;Initial cardiac markers or enzymes | 63.0 | 1.6 (1.42 to 1.78) | 184.3 | 1.7 (1.60 to 1.87) |
| &nbsp;&nbsp;Cardiac arrest | 58.5 | 2.6 (2.00 to 3.32) | 55.4 | 2.2 (1.76 to 2.63) |
| Findings on electrocardiography: | | | | |
| &nbsp;&nbsp;ST segment deviation | 46.8 | 1.6 (1.41 to 1.88) | — | — |
| &nbsp;&nbsp;Left bundle block branch | 10.0 | 1.3 (1.10 to 1.60) | — | — |
| &nbsp;&nbsp;No of leads with ST segment elevation or depression | 20.1 | 1.2 (1.10 to 1.33) | 158.4 | 1.4 (1.34 to 1.49) |
| &nbsp;&nbsp;ST depression, anterior | — | — | 36.2 | 1.3 (1.22 to 1.47) |
| &nbsp;&nbsp;ST depression, inferior | — | — | 10.8 | 1.2 (1.09 to 1.40) |
| &nbsp;&nbsp;Other changes | — | — | 7.2 | 1.1 (1.04 to 1.27) |
| Hosmer and Lemeshow goodness of fit test | | 0.30 | | 0.42 |
| C-statistic | | 0.82 | | 0.70 |

PCI=percutaneous coronary intervention.  
*Equivalent to 1 mg/dl.

Table 3 C-statistics for validation of the full model and the simplified model (as used for the nomogram) for all GRACE patients and for acute coronary syndrome subgroups

| | All patients | STEMI | Unstable angina/ NSTEMI |
|---|---|---|---|
| **All GRACE patients** | | | |
| Death: | | | |
| &nbsp;&nbsp;Full model | 0.82 | 0.82 | 0.81 |
| &nbsp;&nbsp;Simplified model | 0.81 | 0.82 | 0.79 |
| Death or myocardial infarction: | | | |
| &nbsp;&nbsp;Full model | 0.70 | 0.66 | 0.71 |
| &nbsp;&nbsp;Simplified model | 0.70 | 0.66 | 0.70 |
| **Transferred patients** | | | |
| Death: | | | |
| &nbsp;&nbsp;Full model | 0.83 | — | — |
| &nbsp;&nbsp;Simplified model | 0.83 | — | — |
| Death or myocardial infarction: | | | |
| &nbsp;&nbsp;Full model | 0.71 | — | — |
| &nbsp;&nbsp;Simplified model | 0.70 | — | — |
| **Model validation\*** | | | |
| Death: | | | |
| &nbsp;&nbsp;Full model | 0.82 | 0.83 | 0.81 |
| &nbsp;&nbsp;Simplified model | 0.81 | 0.82 | 0.81 |
| Death or myocardial infarction: | | | |
| &nbsp;&nbsp;Full model | 0.73 | 0.73 | 0.73 |
| &nbsp;&nbsp;Simplified model | 0.73 | 0.73 | 0.73 |

STEMI=ST segment elevation myocardial infarction; NSTEMI=non-ST segment elevation myocardial infarction.  
\*On subsequent patients with acute coronary syndrome (22 122 enrolled between 1 October 2003 and 30 September 2005).

tion. This nomogram retained excellent discriminant characteristics based on eight variables and was used for the calculation of risk (fig 3).

## Discussion

The GRACE risk prediction tool (simplified nomogram) includes variables that are readily available to clinicians even in smaller community hospitals. It provides a novel and widely applicable method of assessing the cumulative six month risk of death and death or myocardial infarction across the spectrum of patients admitted to hospital with acute coronary syndrome. Accurate longer term assessment of risk is important because most cardiac ischaemic events occur within the first few weeks after initial presentation with acute coronary syndrome.<sup>15 16</sup> Our findings, based on 48 389 patients, support the validity of the GRACE models for mortality in hospital and after discharge,<sup>14</sup> which were derived from data from about 11 000 and 15 000 patients, respectively.

## The need for risk prediction in patients with acute coronary syndrome

In clinical practice, initial stratification of patients aims to identify those suitable for reperfusion therapy (on the basis of a clinical syndrome and ST segment elevation or other electrocardiographic markers of acute infarction). Binary approaches are commonly applied among others with acute coronary syndrome, but separating patients based on one or two characteristics may substantially overestimate or underestimate the risk of death or myocardial infarction. There is therefore a need for one predictive instrument that performs well in all patients with acute coronary syndrome.

Robust evidence and practice guidelines (including NICE) suggest that interventional and pharmacological therapies predominantly benefit patients at higher risk.<sup>2 3 21</sup> Despite the availability of such guidelines, identification of patients at high risk of cardiac ischaemic events remains challenging.<sup>22 23</sup> In addition, the triage of patients into high intensity care units (cardiac care units) is based predominantly on the criteria for reperfusion therapy rather than risk in the patient. For example, a 55 year old woman (blood pressure 142/80 mm Hg; heart rate 88 per minute) who presents with ST elevation and raised troponin concentration but without complications of a myocardial infarc-

#### 图 3 GRACE risk calculator for death or myocardial infarction from admission to hospital to six months after discharge with the simplified model  
(www.outcomes.org/grace)

```yaml
flowchart:
  title: "GRACE ACS Risk Model Calculator"
  levels:
    - level_name: "Input Parameters (At Admission)"
      nodes:
        - id: "age"
          type: process
          content: "Age"
          items:
            - "Years"
        - id: "hr"
          type: process
          content: "HR"
          items:
            - "bpm"
        - id: "sbp"
          type: process
          content: "SBP"
          items:
            - "mmHg"
        - id: "creat"
          type: process
          content: "Creat."
          items:
            - "μmol/l"
        - id: "chf"
          type: process
          content: "CHF"
          items:
            - "Killip Class"
        - id: "arrest"
          type: process
          content: "Cardiac arrest at admission"
          recommendation: "checkbox"
        - id: "st_dev"
          type: process
          content: "ST-segment deviation"
          recommendation: "checkbox"
        - id: "markers"
          type: process
          content: "Elevated cardiac enzymes/markers"
          recommendation: "checkbox"
    - level_name: "Output Probabilities"
      nodes:
        - id: "prob_inhospital"
          type: process
          content: "Probability of Death / Death or MI"
          items:
            - "In-hospital"
            - "To 6 months"
  edges: []
```