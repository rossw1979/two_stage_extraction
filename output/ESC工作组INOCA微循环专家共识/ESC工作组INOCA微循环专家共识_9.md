---
extraction_strategy: 标准提取
scout_result: {"page_layout": "双栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "左中", "complexity": "低"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "中"}, {"type": "段落", "position": "右中", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "标准提取"}
total_time_seconds: 62.59
page_num: 9
task_id: b4a27f91-37cb-44bc-8152-8d45d0cd73f8
---

[自我校验启动]

✅ 整页结构预扫描完成：
- 左栏（从上至下）：
  1. 顶部段落（接续前页，以“and/or microcirculatory resistance measurements...”开头）
  2. “Coronary angiography”小标题及正文
  3. “Invasive functional coronary angiography”小标题及正文
  4. “Diagnostic guidewire”小标题及正文（含设备型号、剂量等细节）
- 右栏（从上至下）：
  1. 段落（以“Coronary flow reserve can be calculated...”开头，含CFR、IMR、HMR、FFR定义与阈值）
  2. “Pharmacological invasive functional coronary angiography”小标题及正文（含乙酰胆碱用法、指南推荐、Figure 4 引用等）
- 页面四角检查：
  - 左上角：页码“3512”
  - 右上角：作者“V. Kunadian et al.”
  - 右侧边栏：垂直水印文字“Downloaded from https://academic.oup.com/... by Southern Medical University user on 25 October 2020” → **需删除**
  - 左下角：无文字
  - 右下角：无文字
- 表格/图：文中提及 Table 2、Table S4、Figure 4，但本页**未出现实际表格或图**，仅文字引用 → 无需转换
- 无公式、无流程图/决策树
- 无页眉页脚需保留内容（页码、作者属元信息，按规则应删除；但页码“3512”位于左上角，属页面标识，按惯例可保留于输出起始）

⚠️ 注意：右栏末尾提到“Figure 4 shows the steps...”，但本页无图，仅文字描述；按规则，**无图则不生成YAML**，仅忠实转录文字。

✅ 无跨栏拼接：左右栏内容语义虽相关，但排版独立; 严格按“先左后右”处理。

✅ 数值与缩写保真核查：GTN、MVA、VSA、CMD、CFR、IMR、HMR、FFR、cTn、STEMI等缩写均保留原形；剂量如“50–70 U/kg”、“140 μg/kg/min”、“up to 200 μg”等单位与数值完整。

✅ 删除项确认：
- 水印（右侧下载信息）→ 已忽略
- 页眉页脚（作者、下载信息）→ 已忽略；仅保留页码“3512”作为页面标识（非内容，但常见于文献数字化副本起始）
- 上标参考文献编号（如¹⁵, ⁸², ⁸³等）→ 已删除
- 无“参考文献”标题，未触发跳过

[校验通过，开始输出]

3512

and/or microcirculatory resistance measurements in patients with persistent symptoms, but coronary arteries that are either angiographically normal or have moderate stenoses with non-flow-limiting disease. Intracoronary acetylcholine (ACH) testing is supported by a IIb recommendation ‘may be considered’ to assess coronary microvascular spasm and for patients in whom VSA is considered, a Ila recommendation to clarify both endothelium-dependent as well as endothelium-independent pathobiological mechanisms of CMD.

Diagnostic testing provides information on coronary vascular dysfunction, including a functional disorder, i.e. impaired vasodilatation, or vasospasm, and/or structural problem, i.e. an increase in minimal vascular resistance. Relevant endotypes include (i) MVA, (ii) VSA, (iii) both, (iv) none, i.e. non-cardiac chest pain, and (v) non-flow-limiting CAD, e.g. diffuse atherosclerosis, <50% stenosis severity by visual assessment. A clinical diagnosis may be according to expert consensus criteria. The diagnostic criteria are shown in Table 2. Catheter-based measurements of absolute coronary blood flow and microvascular resistance have also been previously described which requires further evaluation in INOCA patients.

### Coronary angiography  
Glyceryl trinitrate (GTN) has a short half-life and is preferred during coronary angiography. A corrected thrombolysis in myocardial infarction frame count >27 (images acquired at 30 frames/s) in the presence of GTN suggests MVA due to impaired resting flow (coronary slow-flow phenomenon). Slow-flow points to an increase in vascular resistance under resting conditions.

### Invasive functional coronary angiography  
Invasive functional coronary angiography (FCA) is a combinatory technique involving direct invasive measurements of coronary vaso-motor function initially with a diagnostic guidewire in combination with pharmacological reactivity testing (Figure 4). Different approaches may slightly vary according to local experience and preference.

### Diagnostic guidewire  
Coronary function testing using a diagnostic guidewire is performed as an adjunct to coronary angiography. The left anterior descending coronary artery is usually preferred as the pre-specified target vessel reflecting its subtended myocardial mass and coronary dominance. Additional studies in other coronary arteries may be appropriate if the initial tests are negative and clinical suspicion is high. Intravenous heparin (50–70 U/kg) should be administered to achieve therapeutic anticoagulation (activated clotting time ~250 s). Diagnostic options include coronary thermodilution using a pressure–temperature sensor guidewire (PressureWire X™, Abbott Vascular, Santa Clara, CA, USA) or a Doppler technique (ComboWire XT or Flowire, Philips Volcano Corporation, San Diego, CA, USA). The ComboWire XT connects to the ComboMap system (Philips, Eindhoven). The usual approach to inducing steady-state hyperaemia is by use of intravenous adenosine (140 μg/kg/min) to achieve endothelium-independent vasodilation. Intracoronary bolus injection of adenosine (up to 200 μg) is an alternative option to assess endothelium-independent vasodilatation.

Coronary flow reserve can be calculated using thermodilution (as resting mean transit time divided by hyperaemic mean transit time) or Doppler flow velocity (hyperaemic flow velocity divided by resting flow velocity). Overall, most studies demonstrating the prognostic value of thermodilution-based CFR have used a cut-off value of 2.0, while studies showing a prognostic impact of CFR based on Doppler have used a CFR cut-off of 2.5 or lower.

Microcirculatory resistance can be calculated by combining pressure and flow measurements (either thermodilution- or Doppler-based). The index of microvascular resistance (IMR) is calculated as the product of distal coronary pressure at maximal hyperaemia multiplied by the hyperaemic mean transit time. Increased IMR (≥25) is representative of microvascular dysfunction. The hyperaemic myocardial velocity resistance (HMR) index is a Doppler-based index, calculated by dividing intracoronary pressure by hyperaemic flow velocity. In a previous study of patients with angina and non-obstructed coronary arteries, HMR >1.9 [odds ratio: 15.6 (95% confidence interval 2.1–114.0), P=0.007] was an independent predictor of recurrent chest pain. Other studies have suggested that a cut-off of ≥2.5 mmHg/cm/s provides the optimal sensitivity and specificity for predicting CMD, as judged with PET. Further studies are required to determine the optimal HMR index that would predict CMD.

Flow-limiting obstructive CAD may be assessed using FFR which is the ratio of mean distal coronary pressure to mean aortic pressure at maximal hyperaemia—abnormal FFR is defined as ≤0.80 or a non-hyperaemic pressure ratio ≤0.89. The binary thresholds of continuous data should be viewed within the context of the patient. Coronary flow reserve, IMR, and FFR have prognostic significance across the diagnostic range of their values. Thus, in this invasive evaluation it is possible to determine endothelium-independent CMD (CFR, IMR); endothelium-dependent CMD (microvascular response to ACH) and vasospastic response (epicardial artery response to ACH) as well as an assessment of low-grade stenoses (FFR).

### Pharmacological invasive functional coronary angiography  
The most established approach for vasoreactivity testing is by intracoronary infusion of acetylcholine, which influences coronary vascular tone via muscarinic receptors on endothelial and vascular smooth muscle cells. The use of intracoronary acetylcholine for the diagnosis of MVA and VSA is recommended by the 2019 ESC CCS clinical practice guidelines on the grounds of its demonstrated safety and efficacy. A pragmatic approach for FCA according to whichever protocol works best in individual centres might be implemented. A standard approach involves sequential infusion of acetylcholine at concentrations approximating 10⁻⁶, 10⁻⁵, and 10⁻⁴ mol/L, respectively (Supplementary material online, Table S4). A clinical diagnosis to rule-in or rule-out MVA and/or VSA due to vasospasm is made according to established criteria. Figure 4 shows the steps in the invasive evaluation of INOCA. Based on current practice, Steps 1, 2, 3 as shown in Figure 4 are suggested though some institutions might prefer Steps 1, 3, 2 in the invasive evaluation of INOCA. Further studies are warranted to determine the best sequence of invasive evaluation in the diagnosis of INOCA. The complications and risks of invasive coronary procedures are previously well