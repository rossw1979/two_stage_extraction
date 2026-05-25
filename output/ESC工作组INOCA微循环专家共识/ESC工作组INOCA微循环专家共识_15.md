---
extraction_strategy: 标准提取
scout_result: {"page_layout": "混排", "content_blocks": [{"type": "流程图", "position": "左上", "complexity": "中"}, {"type": "段落", "position": "右上", "complexity": "低"}, {"type": "表格", "position": "右上", "complexity": "低"}, {"type": "流程图", "position": "中央", "complexity": "中"}], "tables": {"count": 1, "max_rows_estimate": 4, "has_merged_cells": false, "has_multiline_cells": true, "has_footnote_below": false}, "recommendation": "标准提取"}
total_time_seconds: 162.20
page_num: 15
task_id: 2b926cf8-efa1-49b0-bec2-73957fd579fd
---

### 整页结构预扫描（强制执行）

页面共包含以下内容块（按空间位置）：

1. **左上角**：标题“Ischaemia with non obstructive coronary arteries (INOCA)”的流程图（含“Non-invasive evaluation”“Invasive evaluation”分支，下方“INOCA ENDOTYPES”，再下方“Management of INOCA”三类措施），底部标注“Take home figure”。
2. **右上角**：正文段落（含CorCTCA trial、Women’s Ischemia Trial等信息），含上标引用¹³⁷。
3. **中右部**：**Table 5 Recommendations**（带红色边框的编号列表，4条推荐）。
4. **下半页主体**：**Figure 6 Key messages**（大型纵向流程图，左侧竖排红字“INOCA: KEY MESSAGES”，右侧为多层橙/棕/灰背景框+箭头流程结构），底部标注“Figure 6 Key messages.”。
5. **页面四角检查**：
   - 左上角：已计入流程图；
   - 右上角：正文段落；
   - 左下角：Figure 6左边缘文字“INOCA: KEY MESSAGES”及底部图注；
   - 右下角：下载来源水印（“Downloaded from https://academic.oup.com/...”），属需删除的元信息；
   - 页眉：左上“3518”，右上“V. Kunadian et al.” → 属页眉，**删除**；
   - 页脚：无显式页脚，但右下有下载信息 → **删除**。

确认无遗漏内容块。现在按排版顺序逐块提取。

---

### 左栏（本页实际为单栏布局，但上半部分左右分置；根据视觉结构，应视为：顶部左图 + 右文 → 中部右表 → 下部大图。严格按从上到下、从左到右原则，先处理左上图，再右上文，再中右表，最后下部大图）

#### 1. 左上流程图（“Take home figure”）

> 注：该图为结构化图表，需按规则输出为 YAML 流程图（见4.3）。但注意：此图非标准决策树，而是分类-评估-管理路径图，含层级与并列关系，适用 `levels` 结构。

##### 图表标题（隐含，位于图上方黄底黑字）：
**Ischaemia with non obstructive coronary arteries (INOCA)**

##### 自然语言概述：
该图展示INOCA的诊断评估路径与管理策略。分为非侵入性评估与侵入性评估两大路径；最终归为三种内型（Endotypes）：心外膜血管痉挛性心绞痛、微血管性心绞痛、混合型；管理聚焦于生活方式因素、危险因素管理及抗心绞痛药物。

##### YAML 结构化数据：

```yaml
flowchart:
  title: "Ischaemia with non obstructive coronary arteries (INOCA)"
  levels:
    - level_name: "Non-invasive evaluation"
      nodes:
        - id: "noninv_step1"
          type: process
          content: "Step 1: Patient evaluation"
          items: []
          recommendation: ""
          color_hint: "light blue"
        - id: "noninv_step2"
          type: process
          content: "Step 2: Non-invasive evaluation"
          items:
            - "Functional Imaging"
            - "± Coronary CT Angiography"
          recommendation: ""
          color_hint: "light blue"
    - level_name: "Invasive evaluation"
      nodes:
        - id: "inv_step1"
          type: process
          content: "Step 1: Invasive Coronary angiography"
          items: []
          recommendation: ""
          color_hint: "light yellow"
        - id: "inv_step2"
          type: process
          content: "Step 2: FCA guidewire and Adenosine test"
          items: []
          recommendation: ""
          color_hint: "light yellow"
        - id: "inv_step3"
          type: process
          content: "Step 3: FCA Vasoreactivity (ACH test)"
          items: []
          recommendation: ""
          color_hint: "light yellow"
    - level_name: "INOCA ENDOTYPES"
      nodes:
        - id: "endotype1"
          type: process
          content: "Epicardial Vasospastic Angina"
          items: []
          recommendation: ""
          color_hint: "light blue"
        - id: "endotype2"
          type: process
          content: "Microvascular Angina"
          items: []
          recommendation: ""
          color_hint: "light yellow"
        - id: "endotype3"
          type: process
          content: "Microvascular And Epicardial Vasospastic Angina"
          items: []
          recommendation: ""
          color_hint: "light red"
    - level_name: "Management of INOCA"
      nodes:
        - id: "manage1"
          type: process
          content: "1. Lifestyle factors"
          items: []
          recommendation: ""
          color_hint: "light gray"
        - id: "manage2"
          type: process
          content: "2. Risk factor management"
          items: []
          recommendation: ""
          color_hint: "light gray"
        - id: "manage3"
          type: process
          content: "3. Antianginal medications"
          items: []
          recommendation: ""
          color_hint: "light gray"
  edges:
    - from: "noninv_step1"
      to: "noninv_step2"
      condition: ""
    - from: "noninv_step2"
      to: "endotype1"
      condition: ""
    - from: "inv_step1"
      to: "inv_step2"
      condition: ""
    - from: "inv_step2"
      to: "inv_step3"
      condition: ""
    - from: "inv_step3"
      to: "endotype1"
      condition: ""
    - from: "inv_step3"
      to: "endotype2"
      condition: ""
    - from: "inv_step3"
      to: "endotype3"
      condition: ""
    - from: "endotype1"
      to: "manage1"
      condition: ""
    - from: "endotype2"
      to: "manage1"
      condition: ""
    - from: "endotype3"
      to: "manage1"
      condition: ""
```

##### 图注说明：
Take home figure

> 注：图中“Coronary Microvascular dysfunction (CMD)/Vasospastic angina (VSA)”为虚线框内说明文字, 已在流程中通过 endotype 分类体现；未单独设节点，因其为定义性说明，非操作步骤。

---

#### 2. 右上正文段落（紧接流程图右侧）

address this problem as shown in Tables 5 and 6. The CorCTCA trial (NCT03477890) is ongoing and will help clarify the prevalence and clinical significance of INOCA when standard care is based on coronary computed tomography angiography.¹³⁷ To date, there are no disease-modifying therapies specific to INOCA. The Women’s Ischemia Trial to Reduce Events in Non-ObstRuctIve CORONARY

> 注：末尾“CORONARY”疑似截断（原文可能为“CORONARY ARTERY DISEASE”），但图像中仅显示至此，故保留原样；上标¹³⁷为引用标记，按规则**删除**。

修正后（删除上标）：
address this problem as shown in Tables 5 and 6. The CorCTCA trial (NCT03477890) is ongoing and will help clarify the prevalence and clinical significance of INOCA when standard care is based on coronary computed tomography angiography. To date, there are no disease-modifying therapies specific to INOCA. The Women’s Ischemia Trial to Reduce Events in Non-ObstRuctIve CORONARY

---

#### 3. Table 5 Recommendations（中右部，带红色边框）

##### 表格标题：
**Table 5 Recommendations**

##### Markdown 表格（实际为编号列表，非行列表格；按规范，此类编号推荐列表仍视为“表格类结构”，但因无行列，直接转为带编号的段落列表，保留原文格式）：

1. INOCA should be recognized as a clinically important entity in daily clinical practice.  
2. A systematic approach to diagnose and treat these patients should be implemented by clinicians and interventional cardiologists dealing with these patients.  
3. National and international scientific societies, as well as the pharmaceutical and biomedical industries to support future research to address the incomplete understanding of the pathophysiology, the lack of targeted pharmacological treatment, and the evidence-based management of patients with INOCA.  
4. Creating awareness of this condition through campaigns and media to ensure timely provision of care to these patients.

> 注：原文为纯文本编号列表，无表头/列，故不强转Markdown表格，而以编号列表呈现——符合“忠实原文”原则。若强行套用表格将失真。

##### 表格下方无注释（无“注：”或“a.”等）。

---

#### 4. Figure 6 Key messages（下半页主图）

##### 图表标题：
**Figure 6 Key messages.**

##### 自然语言概述：
该图以纵向流程形式总结INOCA核心信息：定义→机制→检测方法→侵入性策略→管理框架→研究需求。采用双列布局（左列主题句，右列具体条目），通过向下箭头连接各层级。

##### YAML 结构化数据：

```yaml
flowchart:
  title: "Figure 6 Key messages"
  levels:
    - level_name: "Definition"
      nodes:
        - id: "def1"
          type: process
          content: "A large proportion of patients undergoing coronary angiography because of angina and evidence of myocardial ischaemia do not have obstructive coronary arteries but have demonstrable ischaemia. This entity is defined as INOCA."
          items: []
          recommendation: ""
          color_hint: "dark red"
    - level_name: "Mechanisms"
      nodes:
        - id: "mech1"
          type: process
          content: "CMD alone or in combination with CAD, is a mechanism of myocardial ischaemia and symptoms in INOCA."
          items: []
          recommendation: ""
          color_hint: "orange"
        - id: "mech2"
          type: process
          content: "Epicardial vasospasm, alone or in combination with CAD, is another mechanisms of myocardial ischaemia"
          items: []
          recommendation: ""
          color_hint: "orange"
    - level_name: "Detection"
      nodes:
        - id: "detect1"
          type: process
          content: "Non-invasive functional techniques are options to detect ischaemia in INOCA."
          items: []
          recommendation: ""
          color_hint: "brown"
        - id: "detect2"
          type: process
          content: "ETT, TTDE, MCE, SPECT"
          items: []
          recommendation: ""
          color_hint: "light orange"
        - id: "detect3"
          type: process
          content: "MRI, PET"
          items: []
          recommendation: ""
          color_hint: "light orange"
    - level_name: "Invasive strategies"
      nodes:
        - id: "invstrat1"
          type: process
          content: "Invasive strategies using coronary angiography and interventional diagnostic procedure (IDP) should be implemented to differentiate between vasospastic angina, microvascular angina and non-cardiac pain."
          items: []
          recommendation: ""
          color_hint: "dark orange"
        - id: "invstrat2"
          type: process
          content: "Diagnostic guidewire, pressure and flow measurements"
          items: []
          recommendation: ""
          color_hint: "light beige"
        - id: "invstrat3"
          type: process
          content: "Pharmacological coronary reactivity testing"
          items: []
          recommendation: ""
          color_hint: "light beige"
    - level_name: "Management"
      nodes:
        - id: "manage1"
          type: process
          content: "A stratified approach to the management of INOCA to address the short and long-term well-being and prognosis is warranted."
          items: []
          recommendation: ""
          color_hint: "olive"
        - id: "manage2"
          type: process
          content: "Tailored counselling on life-style factors, risk factor management as per CVD prevention guidelines"
          items: []
          recommendation: ""
          color_hint: "beige"
        - id: "manage3"
          type: process
          content: "Use of pharmacotherapy to alleviate ischaemia and symptoms"
          items: []
          recommendation: ""
          color_hint: "beige"
    - level_name: "Research needs"
      nodes:
        - id: "research1"
          type: process
          content: "Given the lack of in-depth knowledge, further research is urgently needed."
          items: []
          recommendation: ""
          color_hint: "gray"
        - id: "research2"
          type: process
          content: "To increase our mechanistic understanding"
          items: []
          recommendation: ""
          color_hint: "light gray"
        - id: "research3"
          type: process
          content: "To develop innovative therapies to better manage this serious condition"
          items: []
          recommendation: ""
          color_hint: "light gray"
  edges:
    - from: "def1"
      to: "mech1"
      condition: ""
    - from: "mech1"
      to: "mech2"
      condition: ""
    - from: "mech2"
      to: "detect1"
      condition: ""
    - from: "detect1"
      to: "detect2"
      condition: ""
    - from: "detect1"
      to: "detect3"
      condition: ""
    - from: "detect2"
      to: "invstrat1"
      condition: ""
    - from: "detect3"
      to: "invstrat1"
      condition: ""
    - from: "invstrat1"
      to: "invstrat2"
      condition: ""
    - from: "invstrat1"
      to: "invstrat3"
      condition: ""
    - from: "invstrat2"
      to: "manage1"
      condition: ""
    - from: "invstrat3"
      to: "manage1"
      condition: ""
    - from: "manage1"
      to: "manage2"
      condition: ""
    - from: "manage1"
      to: "manage3"
      condition: ""
    - from: "manage2"
      to: "research1"
      condition: ""
    - from: "manage3"
      to: "research1"
      condition: ""
    - from: "research1"
      to: "research2"
      condition: ""
    - from: "research1"
      to: "research3"
      condition: ""
```

##### 图注说明：
Figure 6 Key messages.

---

### 页面四角复查（输出前最终校验）

- [x] 整页结构已扫描：左图、右文、中表5、下图6 — 全覆盖  
- [x] 四角检查：左上（图）、右上（文）、左下（图6左标签+图注）、右下（水印已删）  
- [x] 表格上方段落：Table 5 上方无独立段落；Figure 6 上方为定义段，已纳入 levels[0]  
- [x] 无跨栏拼接：本页实为单列主导，右上文与左图并置，已按“上→下”顺序处理  
- [x] 双栏？否，无需“先左后右”切换  
- [x] 表格无错位：Table 5 为列表，非表格；Figure 6 已结构化  
- [x] 无数值幻觉：全文无具体数值，仅术语与描述  
- [x] 无HTML样式标签：未使用 `<div>` 等  
- [x] 表格下方注释：Table 5 无注；Figure 6 图注已提取  
- [x] 流程图YAML完整：两图均输出 levels + edges  
- [x] 并列节点用数组：所有同层 nodes 均为数组项，无错误嵌套  
- [x] 数值阈值：无具体数值，不适用  

✅ 所有校验项通过

---

### 最终输出（干净数字化副本）

#### Ischaemia with non obstructive coronary arteries (INOCA)

```yaml
flowchart:
  title: "Ischaemia with non obstructive coronary arteries (INOCA)"
  levels:
    - level_name: "Non-invasive evaluation"
      nodes:
        - id: "noninv_step1"
          type: process
          content: "Step 1: Patient evaluation"
          items: []
          recommendation: ""
          color_hint: "light blue"
        - id: "noninv_step2"
          type: process
          content: "Step 2: Non-invasive evaluation"
          items:
            - "Functional Imaging"
            - "± Coronary CT Angiography"
          recommendation: ""
          color_hint: "light blue"
    - level_name: "Invasive evaluation"
      nodes:
        - id: "inv_step1"
          type: process
          content: "Step 1: Invasive Coronary angiography"
          items: []
          recommendation: ""
          color_hint: "light yellow"
        - id: "inv_step2"
          type: process
          content: "Step 2: FCA guidewire and Adenosine test"
          items: []
          recommendation: ""
          color_hint: "light yellow"
        - id: "inv_step3"
          type: process
          content: "Step 3: FCA Vasoreactivity (ACH test)"
          items: []
          recommendation: ""
          color_hint: "light yellow"
    - level_name: "INOCA ENDOTYPES"
      nodes:
        - id: "endotype1"
          type: process
          content: "Epicardial Vasospastic Angina"
          items: []
          recommendation: ""
          color_hint: "light blue"
        - id: "endotype2"
          type: process
          content: "Microvascular Angina"
          items: []
          recommendation: ""
          color_hint: "light yellow"
        - id: "endotype3"
          type: process
          content: "Microvascular And Epicardial Vasospastic Angina"
          items: []
          recommendation: ""
          color_hint: "light red"
    - level_name: "Management of INOCA"
      nodes:
        - id: "manage1"
          type: process
          content: "1. Lifestyle factors"
          items: []
          recommendation: ""
          color_hint: "light gray"
        - id: "manage2"
          type: process
          content: "2. Risk factor management"
          items: []
          recommendation: ""
          color_hint: "light gray"
        - id: "manage3"
          type: process
          content: "3. Antianginal medications"
          items: []
          recommendation: ""
          color_hint: "light gray"
  edges:
    - from: "noninv_step1"
      to: "noninv_step2"
      condition: ""
    - from: "noninv_step2"
      to: "endotype1"
      condition: ""
    - from: "inv_step1"
      to: "inv_step2"
      condition: ""
    - from: "inv_step2"
      to: "inv_step3"
      condition: ""
    - from: "inv_step3"
      to: "endotype1"
      condition: ""
    - from: "inv_step3"
      to: "endotype2"
      condition: ""
    - from: "inv_step3"
      to: "endotype3"
      condition: ""
    - from: "endotype1"
      to: "manage1"
      condition: ""
    - from: "endotype2"
      to: "manage1"
      condition: ""
    - from: "endotype3"
      to: "manage1"
      condition: ""
```
Take home figure

address this problem as shown in Tables 5 and 6. The CorCTCA trial (NCT03477890) is ongoing and will help clarify the prevalence and clinical significance of INOCA when standard care is based on coronary computed tomography angiography. To date, there are no disease-modifying therapies specific to INOCA. The Women’s Ischemia Trial to Reduce Events in Non-ObstRuctIve CORONARY

#### Table 5 Recommendations

1. INOCA should be recognized as a clinically important entity in daily clinical practice.  
2. A systematic approach to diagnose and treat these patients should be implemented by clinicians and interventional cardiologists dealing with these patients.  
3. National and international scientific societies, as well as the pharmaceutical and biomedical industries to support future research to address the incomplete understanding of the pathophysiology, the lack of targeted pharmacological treatment, and the evidence-based management of patients with INOCA.  
4. Creating awareness of this condition through campaigns and media to ensure timely provision of care to these patients.

#### Figure 6 Key messages

```yaml
flowchart:
  title: "Figure 6 Key messages"
  levels:
    - level_name: "Definition"
      nodes:
        - id: "def1"
          type: process
          content: "A large proportion of patients undergoing coronary angiography because of angina and evidence of myocardial ischaemia do not have obstructive coronary arteries but have demonstrable ischaemia. This entity is defined as INOCA."
          items: []
          recommendation: ""
          color_hint: "dark red"
    - level_name: "Mechanisms"
      nodes:
        - id: "mech1"
          type: process
          content: "CMD alone or in combination with CAD, is a mechanism of myocardial ischaemia and symptoms in INOCA."
          items: []
          recommendation: ""
          color_hint: "orange"
        - id: "mech2"
          type: process
          content: "Epicardial vasospasm, alone or in combination with CAD, is another mechanisms of myocardial ischaemia"
          items: []
          recommendation: ""
          color_hint: "orange"
    - level_name: "Detection"
      nodes:
        - id: "detect1"
          type: process
          content: "Non-invasive functional techniques are options to detect ischaemia in INOCA."
          items: []
          recommendation: ""
          color_hint: "brown"
        - id: "detect2"
          type: process
          content: "ETT, TTDE, MCE, SPECT"
          items: []
          recommendation: ""
          color_hint: "light orange"
        - id: "detect3"
          type: process
          content: "MRI, PET"
          items: []
          recommendation: ""
          color_hint: "light orange"
    - level_name: "Invasive strategies"
      nodes:
        - id: "invstrat1"
          type: process
          content: "Invasive strategies using coronary angiography and interventional diagnostic procedure (IDP) should be implemented to differentiate between vasospastic angina, microvascular angina and non-cardiac pain."
          items: []
          recommendation: ""
          color_hint: "dark orange"
        - id: "invstrat2"
          type: process
          content: "Diagnostic guidewire, pressure and flow measurements"
          items: []
          recommendation: ""
          color_hint: "light beige"
        - id: "invstrat3"
          type: process
          content: "Pharmacological coronary reactivity testing"
          items: []
          recommendation: ""
          color_hint: "light beige"
    - level_name: "Management"
      nodes:
        - id: "manage1"
          type: process
          content: "A stratified approach to the management of INOCA to address the short and long-term well-being and prognosis is warranted."
          items: []
          recommendation: ""
          color_hint: "olive"
        - id: "manage2"
          type: process
          content: "Tailored counselling on life-style factors, risk factor management as per CVD prevention guidelines"
          items: []
          recommendation: ""
          color_hint: "beige"
        - id: "manage3"
          type: process
          content: "Use of pharmacotherapy to alleviate ischaemia and symptoms"
          items: []
          recommendation: ""
          color_hint: "beige"
    - level_name: "Research needs"
      nodes:
        - id: "research1"
          type: process
          content: "Given the lack of in-depth knowledge, further research is urgently needed."
          items: []
          recommendation: ""
          color_hint: "gray"
        - id: "research2"
          type: process
          content: "To increase our mechanistic understanding"
          items: []
          recommendation: ""
          color_hint: "light gray"
        - id: "research3"
          type: process
          content: "To develop innovative therapies to better manage this serious condition"
          items: []
          recommendation: ""
          color_hint: "light gray"
  edges:
    - from: "def1"
      to: "mech1"
      condition: ""
    - from: "mech1"
      to: "mech2"
      condition: ""
    - from: "mech2"
      to: "detect1"
      condition: ""
    - from: "detect1"
      to: "detect2"
      condition: ""
    - from: "detect1"
      to: "detect3"
      condition: ""
    - from: "detect2"
      to: "invstrat1"
      condition: ""
    - from: "detect3"
      to: "invstrat1"
      condition: ""
    - from: "invstrat1"
      to: "invstrat2"
      condition: ""
    - from: "invstrat1"
      to: "invstrat3"
      condition: ""
    - from: "invstrat2"
      to: "manage1"
      condition: ""
    - from: "invstrat3"
      to: "manage1"
      condition: ""
    - from: "manage1"
      to: "manage2"
      condition: ""
    - from: "manage1"
      to: "manage3"
      condition: ""
    - from: "manage2"
      to: "research1"
      condition: ""
    - from: "manage3"
      to: "research1"
      condition: ""
    - from: "research1"
      to: "research2"
      condition: ""
    - from: "research1"
      to: "research3"
      condition: ""
```
Figure 6 Key messages.