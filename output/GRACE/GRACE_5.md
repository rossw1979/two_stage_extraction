---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "表格", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "右中", "complexity": "低"}, {"type": "段落", "position": "右下", "complexity": "低"}, {"type": "图片", "position": "右下（蓝色框内信息图）", "complexity": "低"}], "tables": {"count": 1, "max_rows_estimate": 10, "has_merged_cells": true, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 142.68
page_num: 5
task_id: 4228b575-c23c-4b56-83ba-1026246dd8eb
re_extracted: True
re_extract_focus: "遗漏了跨页延续段落的前置处理（应作为首个内容块），且左下角水印'BMJ Online First bmj.com'未删除，右下蓝色信息图格式未体现其为独立图形模块"
review_needed: True
review_reason: "严格按双栏顺序输出：先完整左栏（表格+左下段落），再完整右栏（右上→右中→右下段落+蓝色信息图+致谢），确保右栏顶部延续段落不被插入左栏后续章节中，并明确标识表格脚注与信息图模块结构。"
---

tion (normal creatinine concentration, no heart failure) has a probability of death of only 3% in the next six months. However, a 55 year old woman with non-ST segment elevation myocardial infarction (blood pressure 118/68; heart rate 92 per min) with mild heart failure and raised creatinine concentration has a six month risk of death of 16%. Without formal risk stratification, the second patient would probably be managed in a low intensity ward area and the management on discharge may not reflect the risk in the patient.

#### Table 4 Resolving intermediate risk (examples). Which patient has higher risk of death or death or myocardial infarction? Is most of risk in hospital or later?

| Variable | Example 1 | Example 2 | Example 3 |
|---|---|---|---|
| Sex | Female | Male | Female |
| Age (years) | 49 | 60 | 62 |
| Heart rate (bpm) | 109 | 94 | 90 |
| Systolic BP (mm Hg) | 100 | 110 | 114 |
| Creatinine (μmol/l) | 104 | 71 | 106 |
| Killip class | II | I | II |
| Electrocardiographic results | T wave inversion | Non-specific T wave changes | T wave t inversion |
| Troponin T (μg/l) | <0.1 | 1.5 | 2.0 |
| Death in hospital (death at six months) | 1% (2%) | 2% (7%) | 5% (12%) |
| Death or MI at six months | 12% | 22% | 31% |

BP=blood pressure; bpm=beats per minute; MI=myocardial infarction.

### Resolving intermediate risk

Despite similarities in key pathophysiological mechanisms, the characteristics on presentation of patients with acute coronary syndrome depend on the extent of the ischaemic territory (influenced by acute thrombotic risk) and previous risk features (such as older age, heart failure, and renal insufficiency). Whereas patients with high risk features, including cardiogenic shock and heart failure, are relatively straightforward to identify, most patients lie in the intermediate range and risk is less obvious (table 4). This intermediate range encompasses up to 10-fold differences in the risk of death. Binary approaches, including those that require separation of patients into high or low risk, are not accurate enough for most patients in the middle range.<sup>2,3</sup> We propose that an appropriate instrument for risk prediction needs to be applicable across the spectrum of acute coronary syndrome, should be derived from a representative and broadly based population, and needs to use variables that are readily available to most clinicians shortly after the patient arrives at hospital.

### How does the present model differ from previous methods of risk stratification?

Several other multivariable prognostic models have been developed,<sup>5–10 24–28</sup> most of which were derived from clinical trial databases or specific subgroups of patients with acute coronary syndrome. Patients with complications and comorbidity tend to be excluded from such trials, thus limiting applicability in clinical practice. Models developed from large claims databases are potentially subject to bias.<sup>8 11</sup> In contrast, the GRACE registry spans the spectrum of acute coronary syndrome and is based on an unselected contemporary population.

A C-statistic of less than 0.70 has been suggested to be of limited clinical value.<sup>12</sup> The TIMI (thrombolysis in myocardial infarction) model performs well in patients who are eligible for reperfusion therapy but is less effective in more general patients, including those who are ineligible for reperfusion (C-statistic=0.65).<sup>24</sup> An independent study suggests that the unselected GRACE mortality model is superior to either the TIMI or the PURSUIT (platelet glycoprotein IIb/IIIa in unstable angina: receptor suppression with eptifibatide) models.<sup>29</sup> We have shown that the cumulative (0 to six month) GRACE risk model performs well across the spectrum of acute coronary syndrome and has prospective and external validity. External validation with the GUSTO III dataset confirms the discriminant characteristics of the model when applied to patients with ST segment elevation myocardial infarction and those with non-ST segment elevation myocardial infarction. Although we excluded transferred patients from the derivation of this model (because such patients may lack data for several baseline characteristics), testing the model in the transfer dataset confirmed its applicability to such patients (C-statistic=0.83 for predicting death and 0.70 for predicting myocardial infarction, simplified model).

### Simplified risk calculation for clinical application

The simplified model includes most the predictive information: >92% of the total model χ² for death and >90% for death or myocardial infarction (fig 3). The GRACE risk calculator (fig 3) (available at www.outcomes.org/grace) can be used to derive a prognostic score and to estimate the risk of clinically important end points—death or the combined risk of death or myocardial infarction—in individual patients. For ease of use, this nomogram can be installed into a handheld device or personal computer (data entry takes about 30 seconds) and is also available as a score card.<sup>14</sup>

### Limitations

GRACE is designed to enrol an unselected and generalisable population of patients, though some participating centres are required to obtain informed consent from patients before enrolment. Therefore some patients who died early or who experienced major clinical complications immediately on arrival in hospital may be under-represented. The model may not be appropriate for stratifying low risk patients with non-specific chest pain without acute coronary syndrome, but such patients do not require the same therapeutic and management decisions as those with acute coronary syndrome.

We thank the physicians and nurses who participated in GRACE. The risk calculator is available together with further information about the project

#### What is already known on this topic

- Specific treatments are indicated in higher or lower risk patients with acute coronary syndrome  
- Conventional clinical assessment and binary methods for predicting risk based on results of electrocardiography and markers of injury are not sufficiently accurate  
- Previous risk models were based on subgroups of patients with acute coronary syndrome and were derived from large clinical trials or healthcare claims databases  

#### What this study adds

- The GRACE risk tool can be used to predict the cumulative risk of death and death or myocardial infarction in the period from admission to hospital to six months after discharge  
- The tool is simple to apply, robust, externally validated, and applicable to patients across the complete spectrum of acute coronary syndrome