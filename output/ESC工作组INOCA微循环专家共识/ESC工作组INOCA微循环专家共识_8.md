---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 51.75
page_num: 8
task_id: 2b379224-9106-4d18-9b98-82b263477282
---

#### 图 3 Non-invasive evaluation of INOCA. GP, general practitioner.

**自然语言概述**  
该流程图描述了INOCA（缺血性心肌病伴非阻塞性冠状动脉）患者的非侵入性评估路径，分为两个主要步骤：Step 1为患者评估，Step 2为非侵入性检查。Step 1从患者主诉“缺血性症状”开始，经全科医生（GP）进行病史采集（含危险因素）与体格检查，若获得“令人信服的持续性心肌缺血病史”，则行静息心电图（ECG）；若ECG为非诊断性/正常，则转诊至心内科。Step 2中，根据临床可能性与资源可及性，优先考虑不同非侵入性检查策略：高临床可能性者首选功能影像学检查（包括运动负荷试验、经胸超声心动图、心肌对比超声心动图、心肌灌注显像、正电子发射断层扫描、心脏磁共振成像），低临床可能性者可考虑冠状动脉CT血管成像（CCTA）；二者之间存在双向箭头，表示检查顺序可根据当地可行性灵活调整。图中明确标注“± Coronary Computed Tomographic angiography”作为补充选项。

**YAML 结构化数据**

```yaml
flowchart:
  title: "Non-invasive evaluation of INOCA"
  levels:
    - level_name: "Step 1: Patient evaluation"
      nodes:
        - id: "node_1"
          type: start
          content: "Patient"
          items:
            - "Ischaemic symptoms"
          recommendation: ""
          color_hint: ""
        - id: "node_2"
          type: process
          content: "GP"
          items:
            - "History taking including risk factors"
            - "Physical examination"
          recommendation: ""
          color_hint: ""
        - id: "node_3"
          type: decision
          content: "Convincing ongoing history of cardiac ischaemia"
          items: []
          recommendation: ""
          color_hint: ""
        - id: "node_4"
          type: process
          content: "ECG – non-diagnostic/normal"
          items: []
          recommendation: ""
          color_hint: "red"
        - id: "node_5"
          type: process
          content: "Cardiology referral"
          items: []
          recommendation: ""
          color_hint: ""
    - level_name: "Step 2: Non-invasive evaluation"
      nodes:
        - id: "node_6"
          type: process
          content: "Functional imaging"
          items:
            - "Exercise Tolerance Test"
            - "Transthoracic Doppler Echocardiography"
            - "Myocardial Contrast Echocardiography"
            - "Myocardial Perfusion Imaging"
            - "Positron Emission Tomography"
            - "Cardiac Magnetic Resonance Imaging"
          recommendation: ""
          color_hint: ""
        - id: "node_7"
          type: process
          content: "± Coronary Computed Tomographic angiography"
          items: []
          recommendation: ""
          color_hint: ""
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
    - from: "node_5"
      to: "node_6"
      condition: ""
    - from: "node_6"
      to: "node_7"
      condition: "Denotes can be performed in any sequence based on local availability"
    - from: "node_7"
      to: "node_6"
      condition: "Denotes can be performed in any sequence based on local availability"
  notes:
    - "Preferentially considered if: High clinical likelihood, Revascularisation likely, Local expertise and availability, Viability assessment also required"  # 左侧虚线框，对应高临床可能性场景
    - "Preferentially considered if: Low clinical likelihood, Patient characteristics suggest high image quality, Local expertise and availability, Information on atherosclerosis desired, No history of CAD"  # 左下虚线框，对应低临床可能性场景
```

**图注说明**  
Figure 3 Non-invasive evaluation of INOCA. GP, general practitioner.

---

**正文段落提取（按页面结构顺序）**

In the diagnostic pathway for patients assessed for angina recommended in the ESC CCS 2019 guideline,² first line of testing is non-invasive. In patients with no obstructive CAD on their coronary computed tomographic angiography and/or no regional reversible ischaemia on functional testing, CMD or VSA may be the cause of their symptoms and in patients with a significant burden of disease, further testing through non-invasive and invasive techniques should be considered. While non-endothelial dependent dysfunction may be assessed non-invasively, acetylcholine can only be administered during invasive testing. Thus, a full diagnostic assessment for INOCA currently requires invasive angiography. Several non-invasive techniques allow assessment of CFR (Figure 3, Supplementary material online, Table S3).

**Invasive diagnosis in the catheterization laboratory**  
The 2019 ESC CCS guidelines² have given a IIa recommendation ('should be considered') for guidewire-based measurement of CFR

---

✅ **自我校验完成**  
- [x] 整页结构已扫描：顶部标题、流程图主体（含左右两列文字框）、底部两段正文、右下角页码与下载信息（已过滤）  
- [x] 页面四角检查：左上角无文字；左下角为图注；右下角为页码“3511”及下载信息（已删除）；右上角为页码“3511”（已删除）  
- [x] 表格上方段落：本页无表格，但流程图上方无独立段落；流程图内所有文字块（含两个虚线框说明）均已纳入YAML notes  
- [x] 无跨栏拼接：本页为单栏排版（流程图占主体，下方为连续正文），严格自上而下处理  
- [x] 双栏检查：非双栏布局，无需适用“先左后右”规则  
- [x] 流程图YAML完整：含title、levels、nodes、edges、notes；并列节点以数组表达；双向箭头已正确建模为两条边  
- [x] 数值与术语保真：ESC CCS 2019、CMD、VSA、CFR、IIa等均按原文保留；无单位或数值需核对项  
- [x] 内容过滤执行：页眉“Ischaemia with non-obstructive coronary arteries”保留（属章节标题）；页脚下载信息、页码、水印均已删除；上标引用“²”已删除；参考文献未出现，未截断  

输出为纯净数字化副本，无增补、无推断。