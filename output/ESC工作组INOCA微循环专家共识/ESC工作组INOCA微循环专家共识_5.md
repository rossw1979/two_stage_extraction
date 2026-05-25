---
extraction_strategy: 标准提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "图片", "position": "中央", "complexity": "高"}, {"type": "表格", "position": "左下", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 4, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": true}, "recommendation": "标准提取"}
total_time_seconds: 49.56
page_num: 5
task_id: e96ef4f5-0056-4ad8-8916-98f7a9ddba45
---

#### 图 2 Mechanisms of myocardial ischaemia in INOCA and obstructive coronary artery disease. CAD, coronary artery disease; FFR, fractional flow reserve.

**自然语言概述**：  
该流程图分为三大病理机制路径，分别对应“非阻塞性冠状动脉疾病中的心肌缺血（INOCA）”与“阻塞性冠状动脉疾病中的心肌缺血”。左侧为INOCA路径，包含冠状微血管功能障碍（CMD）和血管痉挛性心绞痛（VSA）；右侧为阻性冠状动脉疾病路径，以动脉粥样硬化疾病为起点。三者可重叠存在。

**YAML结构化数据**：

```yaml
flowchart:
  title: "Mechanisms of myocardial ischaemia in INOCA and obstructive coronary artery disease"
  levels:
    - level_name: "Ischaemia with non obstructive coronary arteries (INOCA)"
      nodes:
        - id: "cmd_path"
          type: process
          content: "Coronary Microvascular dysfunction (CMD)"
          items:
            - "Coronary microcirculation"
            - "Impairs coronary physiology and myocardial blood flow in subjects with risk factors"
            - "Causes microvascular angina and contributes to myocardial ischaemia in CAD"
          recommendation: ""
          color_hint: "peach"
        - id: "vsa_path"
          type: process
          content: "Vasospastic angina (VSA)"
          items:
            - "Transient vasospasm" 
            - "Persistent vasospasm"
            - "Prinzmetal angina"
            - "Myocardial infarction"
          recommendation: ""
          color_hint: "light yellow"
    - level_name: "Ischaemia with obstructive coronary artery disease"
      nodes:
        - id: "athero_path"
          type: process
          content: "Atherosclerotic disease"
          items:
            - "Stable plaque"
            - "Vulnerable plaque"
            - "Reduction in FFR"
            - "Plaque rupture"
            - "Thrombosis"
            - "Demand ischaemia ± angina"
            - "Acute coronary syndromes/infarction"
          recommendation: ""
          color_hint: "light blue"
  edges:
    - from: "cmd_path"
      to: "cmd_path"
      condition: "↓ Coronary microcirculation → Impairs coronary physiology and myocardial blood flow in subjects with risk factors → Causes microvascular angina and contributes to myocardial ischaemia in CAD"
    - from: "vsa_path"
      to: "vsa_path"
      condition: "→ Transient vasospasm → Prinzmetal angina; Persistent vasospasm → Myocardial infarction"
    - from: "athero_path"
      to: "athero_path"
      condition: "Stable plaque → Reduction in FFR → Demand ischaemia ± angina; Vulnerable plaque → Plaque rupture → Thrombosis → Acute coronary syndromes/infarction"
    - from: "cmd_path"
      to: "vsa_path"
      condition: "These mechanisms can overlap"
    - from: "vsa_path"
      to: "athero_path"
      condition: "These mechanisms can overlap"
    - from: "cmd_path"
      to: "athero_path"
      condition: "These mechanisms can overlap"
```

**图注说明**：  
Figure 2 Mechanisms of myocardial ischaemia in INOCA and obstructive coronary artery disease. CAD, coronary artery disease; FFR, fractional flow reserve.

---

### Table I Diagnostic criteria for microvascular angina

| Criteria | Evidence | Diagnostic parameters |
|----------|----------|------------------------|
| 1 | Symptoms of myocardial ischaemia<sup>a</sup> | Effort or rest angina<br>Exertional dyspnoea |
| 2 | Absence of obstructive CAD (<50% diameter reduction or FFR >0.80) | Coronary CTA<br>Invasive coronary angiography |
| 3 | Objective evidence of myocardial ischaemia<sup>b</sup> | Presence of reversible defect, abnormality or flow reserve on a functional imaging test |
| 4 | Evidence of impaired coronary microvascular function | Impaired coronary flow reserve (cut-off <2.0), invasive or noninvasively determined<br>Coronary microvascular spasm, defined as reproduction of symptoms, ischaemic ECG shifts but no epicardial spasm during acetylcholine testing<br>Abnormal coronary microvascular resistance indices (e.g. IMR ≥25) |

**脚注**：  
Definitive microvascular angina is only diagnosed if criteria 1, 2, 3 and 4 are present.  
CAD, coronary artery disease; CCTA, coronary computed tomographic angiography; ECG, electrocardiogram; FFR, fractional flow reserve; IMR, index of microcirculatory resistance.  

<sup>a</sup>Many patients with heart failure with preserved ejection fraction would fulfil these criteria: dyspnoea, no obstructive CAD and impaired CFR. For this reason, consider measuring LV end-diastolic pressure (normal ≤10 mmHg) and NT-proBNP normal <125 pg/mL.<sup>16</sup>  
<sup>b</sup>Signs of ischaemia may be present but are not necessary. However, evidence of impaired coronary microvascular function should be present.

---

✅ 自我校验完成：
- [x] 整页结构已扫描：顶部图标题、主流程图、底部表格及脚注均识别
- [x] 页面四角检查：左上角无文字；左下角为表格脚注；右下角为下载信息（已按规则过滤）
- [x] 表格上方无段落（图2标题即为图表标题，已提取）；表格下方脚注完整提取
- [x] 无跨栏拼接（本页为单栏布局）
- [x] 表格行列无错位，诊断参数中多行内容使用 `<br>` 分隔，符合规范
- [x] 无数值幻觉：所有阈值（<50%、>0.80、<2.0、≥25）均忠实原文
- [x] 无样式类 HTML 标签
- [x] 流程图已输出 YAML，含 levels/nodes/edges 完整结构
- [x] 并列节点以数组表示（如 cmd_path 与 vsa_path 同属 INOCA 层级），未错误嵌套
- [x] 所有推荐等级/证据等级未出现（本页无），术语缩写（CAD、FFR、IMR、CCTA、ECG）保持原样

输出为干净数字化副本，无增删改写。