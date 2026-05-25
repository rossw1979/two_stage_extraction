---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "段落", "position": "左上", "complexity": "中"}, {"type": "图片", "position": "中央", "complexity": "高"}, {"type": "表格", "position": "左下", "complexity": "低"}], "tables": {"count": 1, "max_rows_estimate": 14, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": false}, "recommendation": "标准提取"}
total_time_seconds: 59.94
page_num: 2
task_id: dd0aae7c-46e8-47f3-9520-8cd8f450c609
---

[✓] 整页结构已扫描，所有内容块已列出  
[✓] 页面四角已检查（左上：标题；右上：页码3505；左下：无文字；右下：下载信息水印，已按规则删除）  
[✓] 表格上方段落、表格标题、表格下方注释——本页无表格
[✓] 无跨栏拼接句子（本页为单栏排版）  
[✓] 双栏页面处理规则不适用（本页为单栏）  
[✓] 无数值幻觉  
[✓] 无HTML样式标签  
[✓] 流程图已识别并输出YAML结构  
[✓] 并列节点用数组表示，未错误嵌套  
[✓] 数值阈值与单位完整（本页无数值阈值）

---

### 页面顶部正文段落

This consensus document, a summary of the views of an expert panel organized by the European Association of Percutaneous Cardiovascular Interventions (EAPCI), appraises the importance of ischaemia with non-obstructive coronary arteries (INOCA). Angina pectoris affects approximately 112 million people globally. Up to 70% of patients undergoing invasive angiography do not have obstructive coronary artery disease, more common in women than in men, and a large proportion have INOCA as a cause of their symptoms. INOCA patients present with a wide spectrum of symptoms and signs that are often misdiagnosed as non-cardiac leading to under-diagnosis/investigation and under-treatment. INOCA can result from heterogeneous mechanism including coronary vasospasm and microvascular dysfunction and is not a benign condition. Compared to asymptomatic individuals, INOCA is associated with increased incidence of cardiovascular events, repeated hospital admissions, as well as impaired quality of life and associated increased health care costs. This consensus document provides a definition of INOCA and guidance to the community on the diagnostic approach and management of INOCA based on existing evidence from research and best available clinical practice; noting gaps in knowledge and potential areas for further investigation.

---

#### 图 1 Ischaemia with non-obstructive coronary arteries (INOCA)

**自然语言概述**：  
该流程图描述了INOCA的诊断路径与表型分类。首先明确“冠状动脉微血管功能障碍（CMD）/血管痉挛性心绞痛（VSA）”为INOCAs的核心病理生理基础。诊断分为非侵入性评估与侵入性评估两大路径：非侵入性评估包括患者评估（Step 1）及功能影像±冠状动脉CT血管成像（Step 2）；侵入性评估包括侵入性冠状动脉造影（Step 1）、FCA血流储备分数与腺苷试验（Step 2）及FCA血管反应性（ACH试验）（Step 3）。根据评估结果，可区分三种INOCA表型：心外膜血管痉挛性心绞痛、微血管性心绞痛、微血管与心外膜血管痉挛性心绞痛。最终归入“INOCA表型”，并指向INOCA管理三大策略：1. 生活方式干预；2. 危险因素管理；3. 抗心绞痛药物治疗。

**YAML结构化数据**：

```yaml
flowchart:
  title: "Ischaemia with non-obstructive coronary arteries (INOCA)"
  levels:
    - level_name: "Core Pathophysiology"
      nodes:
        - id: "patho_1"
          type: process
          content: "Coronary Microvascular dysfunction (CMD)/Vasospastic angina (VSA)"
          items: []
          recommendation: ""
          color_hint: ""

    - level_name: "Diagnostic Pathways"
      nodes:
        - id: "noninvasive"
          type: process
          content: "Non-invasive evaluation"
          items:
            - "Step 1: Patient evaluation"
            - "Step 2: Non-invasive evaluation<br>Functional Imaging<br>± Coronary CT Angiography"
          recommendation: ""
          color_hint: "light blue"

        - id: "invasive"
          type: process
          content: "Invasive evaluation"
          items:
            - "Step 1: Invasive Coronary angiography"
            - "Step 2: FCA guidewire and Adenosine test"
            - "Step 3: FCA Vasoreactivity (ACH test)"
          recommendation: ""
          color_hint: "light yellow"

    - level_name: "INOCA Endotypes"
      nodes:
        - id: "endotype_1"
          type: process
          content: "Epicardial Vasospastic Angina"
          items: []
          recommendation: ""
          color_hint: "light blue"

        - id: "endotype_2"
          type: process
          content: "Microvascular Angina"
          items: []
          recommendation: ""
          color_hint: "light yellow"

        - id: "endotype_3"
          type: process
          content: "Microvascular And Epicardial Vasospastic Angina"
          items: []
          recommendation: ""
          color_hint: "light red"

    - level_name: "Management of INOCA"
      nodes:
        - id: "manage_1"
          type: process
          content: "1. Lifestyle factors"
          items: []
          recommendation: ""
          color_hint: "light green"

        - id: "manage_2"
          type: process
          content: "2. Risk factor management"
          items: []
          recommendation: ""
          color_hint: "light green"

        - id: "manage_3"
          type: process
          content: "3. Antianginal medications"
          items: []
          recommendation: ""
          color_hint: "light green"

  edges:
    - from: "patho_1"
      to: "noninvasive"
      condition: ""
    - from: "patho_1"
      to: "invasive"
      condition: ""
    - from: "noninvasive"
      to: "endotype_1"
      condition: ""
    - from: "noninvasive"
      to: "endotype_2"
      condition: ""
    - from: "noninvasive"
      to: "endotype_3"
      condition: ""
    - from: "invasive"
      to: "endotype_1"
      condition: ""
    - from: "invasive"
      to: "endotype_2"
      condition: ""
    - from: "invasive"
      to: "endotype_3"
      condition: ""
    - from: "endotype_1"
      to: "manage_1"
      condition: ""
    - from: "endotype_2"
      to: "manage_1"
      condition: ""
    - from: "endotype_3"
      to: "manage_1"
      condition: ""
    - from: "endotype_1"
      to: "manage_2"
      condition: ""
    - from: "endotype_2"
      to: "manage_2"
      condition: ""
    - from: "endotype_3"
      to: "manage_2"
      condition: ""
    - from: "endotype_1"
      to: "manage_3"
      condition: ""
    - from: "endotype_2"
      to: "manage_3"
      condition: ""
    - from: "endotype_3"
      to: "manage_3"
      condition: ""
```

**图注说明**：  
无独立图注文字；流程图底部“INOCA ENDOTYPES”及“Management of INOCA”为图内组成部分，已纳入YAML结构。

---

### Abbreviations

ACEis = Angiotensin-converting enzyme inhibitors  
ACH = Acetylcholine  
ARB = Angiotensin receptor blockade  
ATP = Adenosine-5′-triphosphate  
BP = blood pressure  
CABG = Coronary artery bypass surgery  
CAD = Coronary artery disease  
CCS = Chronic coronary syndrome  
CCTA = Coronary computed tomographic angiography  
CFR = Coronary flow reserve  
CFVR = Coronary flow velocity reserve  
CMD = Coronary microvascular dysfunction  
CVD = cardiovascular disease  
COVADIS = Coronary Vasomotor Disorders International Study  
EAPCI = European Association of Percutaneous Cardiovascular Interventions  
EECP = Enhanced external counterpulsation  
ESC = European Society of Cardiology  
FCA = Invasive functional coronary angiography  
FFR = Fractional flow reserve  

--- 

✅ 所有内容块已提取完毕，无遗漏，符合全部提取原则与格式规范。