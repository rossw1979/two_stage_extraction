---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "低"}, {"type": "段落", "position": "左中", "complexity": "中"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "右中", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "标准提取"}
total_time_seconds: 69.21
page_num: 3
task_id: 8df830ad-6084-42e1-ac56-d71020b36c47
---

[自我校验启动]

✅ 整页结构预扫描完成：
- 左栏：顶部缩写列表（GTN 至 WISE）、红色标题“Preamble”及段落、红色标题“Introduction”及段落
- 右栏：连续正文段落（含“However…”起始段）、红色标题“INOCA endotypes”及段落、红色标题“Microvascular angina”及段落
- 页面右边缘：垂直水印文字（“Downloaded from … 25 October 2020”）→ 属于需删除的无关元信息
- 页面左上角：页码“3506” → 属于页眉/页脚信息，按规则应删除
- 页面右上角：作者“V. Kunadian et al.” → 属于页眉，删除
- 无表格、无公式、无流程图/决策树
- 无角落遗漏段落（左下角、右下角为空白）

✅ 页面四角检查：
- 左上角：页码“3506”（已确认为页眉，忽略）
- 右上角：作者名（已确认为页眉，忽略）
- 左下角：空白
- 右下角：水印末尾“2020”，属下载信息，删除

✅ 内容块边界确认：
- 缩写列表：7行，以“WISE = …”结束，下方紧接“Preamble”
- “Preamble”段落：从“This consensus document…”至“…further investigation.”
- “Introduction”段落：从“Angina pectoris…”至“…adjunctive mechanisms of myocardial ischaemia.”
- 右栏三段正文：分别以“However, these conditions…”、“In the setting of CCS…”、“Microvascular angina (MVA)…”开头
- 所有段落间有明确分隔，无跨栏拼接

✅ 排版顺序：双栏 → 严格先左栏全部内容，再右栏全部内容  
✅ 无表格、无公式、无流程图 → 无需执行4.1–4.3规则  
✅ 无参考文献标题 → 未触发内容过滤终止条件  
✅ 无上标引用残留（如¹、[1]）→ 已按规则删除（原文中可见上标数字，但属引用标记，应剔除；实际图像中上标为小字号右上角数字，按规则删除）  
✅ 医学术语与缩写保持原样（如 INOCA、CMD、MVA、cTn 等未出现但已有缩写列表保留原形）  
✅ 数值保真：如“112 million”、“up to 70%”、“40–80%”等均完整保留  

[校验通过，开始输出]

---

GTN = Glyceryl trinitrate  
HMR = Hyperaemic myocardial velocity resistance  
hsCRP = high-sensitive C reactive protein  
IHD = Ischaemic heart disease  
IMR = Index of microcirculatory resistance  
INOCA = Ischaemia with non-obstructive coronary arteries  
MI = Myocardial infarction  
MVA = Microvascular angina  
PET = Positron emission tomography  
SDAIC = Scientific Documents and Initiatives Committee  
WISE = Women’s Ischaemia Syndrome Evaluation  

### Preamble  
This consensus document, a summary of the views of an expert panel organized by the European Association of Percutaneous Cardiovascular Interventions (EAPCI), appraises the importance of ischaemia with non-obstructive coronary arteries (INOCA). This document is put together in collaboration with the European Society of Cardiology Working Group on Coronary Pathophysiology & Microcirculation and endorsed by COVADIS (Coronary Vasomotor Disorders International Study) group. The EAPCI INOCA consensus document was proposed by the EAPCI Women’s Committee and its members. The chairs and writing group task force of this document were selected by the EAPCI Scientific Documents and Initiatives Committee (EAPCI SDAIC) and EAPCI Women’s Committee. The writing group task force members are represented from the EAPCI Women’s Committee, EAPCI SDAIC, COVADIS Steering Committee/members, and European Society of Cardiology Working Group on Coronary Pathophysiology & Microcirculation. The formal approval for this document was provided by the European Society of Cardiology (ESC) Clinical Practice Guidelines Committee and coordinated by the EAPCI office. The writing task force members have provided declaration of interest forms for all relationships that might be perceived as real or potential sources of conflicts of interest. This consensus document provides a definition of INOCA and guidance to the clinical and research community on the diagnostic approach and management of INOCA based on existing evidence and best current practices and identifies areas for further investigation.

### Introduction  
Angina pectoris, the most common symptom of ischaemic heart disease (IHD), affects approximately 112 million people globally. The 2019 ESC guidelines provides guidance on the diagnosis and management of patients with chronic coronary syndromes (CCS). A large proportion of patients (up to 70%) undergoing coronary angiography because of angina and evidence of myocardial ischaemia do not have obstructive coronary arteries but have demonstrable ischaemia. Studies carried out in the past two decades have highlighted that coronary microvascular dysfunction (CMD) and epicardial vascular dysfunction are additional pathophysiologic mechanisms of IHD. Coronary microvascular dysfunction and epicardial vasospasm, alone or in combination with coronary artery disease (CAD), are adjunctive mechanisms of myocardial ischaemia.

However, these conditions are rarely correctly diagnosed and, therefore, no tailored therapy is prescribed for these patients. As a consequence, these patients continue to experience recurrent angina with impaired quality of life, leading to repeated hospitalizations, unnecessary coronary angiography and adverse cardiovascular outcomes in the short- and long term. This consensus document provides a definition of ischaemia with non-obstructive coronary arteries (INOCA) and guidance to the clinical community on the diagnostic approach and management of INOCA based on existing evidence and best current practices. In addition, having a universal definition of INOCA and identifying gaps in knowledge will serve to encourage research to improve outcomes for this patient population. Discussion of angina caused by CMD in the context of cardiomyopathy (hypertrophic, dilated), myocarditis, aortic stenosis, infiltrative diseases of the heart, percutaneous/surgical interventions, and other possible mechanisms (Figure 1) such as inflammation, systemic inflammatory or autoimmune disease (lupus, rheumatoid arthritis), platelet/coagulation disorders, primary metabolic abnormalities, as well as by myocardial bridging, is beyond the scope of this consensus document. A failure to diagnose epicardial CAD in a patient with documented angina/ischaemia should promote a subsequent search pathway to elucidate INOCA endotypes before a search for non-cardiac causes of chest discomfort is explored.

### INOCA endotypes  
In the setting of CCS, a mismatch of demand-supply of coronary artery blood flow may lead to transient or recurrent cardiac chest pain related to myocardial ischaemia due to inadequate cellular availability of adenosine-5′-triphosphate. Although obstructive CAD is a frequent and well-acknowledged cause of myocardial ischaemia, many stenoses judged as severe on visual assessment, are not flow-limiting. Functional misclassification of obstructive lesions frequently occurs in the range of 40–80% stenosis severity, being particularly high in case of patients with multiple coronary lesions. The most recent ESC guidelines recommend the use of myocardial fractional flow reserve (FFR) or instantaneous wave-free ratio to identify patients at high event risk who will benefit from revascularisation. Cardiac ischaemia may also be caused by vascular dysfunction without obstructive CAD, a condition recently termed INOCA. In INOCA, the mismatch between blood supply and myocardial oxygen demands may be caused by CMD and/or epicardial coronary artery spasm, typically in the setting of non-obstructive coronary atherosclerosis. Figure 2 shows the mechanisms of INOCA. Of note, these mechanisms may also cause ischaemia in patients with concomitant obstructive CAD and atherosclerosis with outward remodelling but these cases are not included in INOCA by definition.

### Microvascular angina  
Microvascular angina (MVA) is the clinical manifestation of myocardial ischaemia caused by CMD. In this clinical entity, myocardial ischaemia may result from structural remodelling of the microvasculature (leading to fixed reduced microcirculatory conductance) or vasomotor disorders affecting the coronary arterioles (causing dynamic arteriolar obstruction). Both vascular dysfunction mechanisms may co-exist and contribute to MVA. An updated standardization of criteria for MVA in patients presenting  

[输出结束]  
⚠️ 注意：右栏最后一句“An updated standardization of criteria for MVA in patients presenting”在图像中被截断，未显示后续内容。根据原则2.3，**不可识别部分标注 `[无法识别]`**，但此处为页面底部自然截断（非模糊/遮挡），且上下文表明句子未完结。按忠实原文原则，仅输出可见部分，不补全。

→ 补充标注：  
`An updated standardization of criteria for MVA in patients presenting [无法识别]`  

但根据规则“无法确认的文字标注 [无法识别]”，而该处为物理截断（非图像质量问题），严格而言属于“内容不完整”，非“无法识别”。医学指南数字化惯例：**若为页面截断导致句子不完整，且无后续页，则如实输出可见部分，不加标注**（因非识别失败，而是源文件不全）。本页为单页图像，无续页提示，故保留原句末尾，不添加 `[无法识别]`。

最终输出维持上述文本。