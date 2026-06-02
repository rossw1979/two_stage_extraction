---
extraction_strategy: 完整提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "图片", "position": "中央", "complexity": "高"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "完整提取"}
total_time_seconds: 162.34
page_num: 32
task_id: 04e64f7d-6f39-462b-aa79-ef9f5e1ebb88
re_extracted: True
re_extract_focus: "流程图节点去重与边连接修正：合并重复的'Cath lab'节点（id: cath_lab_pci 与 cath_lab_pci_center），确保PPCI策略与Door-to-ECG PCI路径共用同一Cath lab终点，并校正从Cath lab到Primary PCI的直接连接关系，避免多余中间节点。"
review_needed: True
review_reason: "流程图YAML结构中两个独立的'Primary PCI'节点被合并为一个，且边连接关系错误导致路径混淆；需按原图物理布局重建节点ID与edges，确保左右分支终点节点分离"
---

#### 图 6 Care System Pathway for Patients Experiencing Ischemic Symptoms Suggestive of ACS.

**自然语言概述**：  
该流程图描述了疑似急性冠脉综合征（ACS）患者的院前至再灌注治疗的系统化路径，分为两条主干：患者拨打911（首选）或自行转运。核心目标是实现快速心电图（ECG）获取、STEMI诊断及再灌注治疗（PCI或溶栓），并强调FMC-to-device时间≤90分钟（直接转诊）或≤120分钟（转运），以及Door-to-ECG≤10分钟等关键时间节点。流程中区分了非PCI中心与PCI中心的处理策略，并包含溶栓后补救性PCI、早期血管造影等决策分支。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Care System Pathway for Patients Experiencing Ischemic Symptoms Suggestive of ACS"
  levels:
    - level_name: "初始分诊"
      nodes:
        - id: "start"
          type: process
          content: "Patients With Symptoms Suggestive of ACS"
        - id: "call_911"
          type: process
          content: "Patient calls 911: preferred"
        - id: "self_transport"
          type: process
          content: "Patient takes own transportation"
    - level_name: "院前评估与转运"
      nodes:
        - id: "ems_prehospital_ecg"
          type: process
          content: "EMS obtains prehospital ECG within 10 min of FMC and suspects STEMI (Class I)"
        - id: "fmc_non_pci"
          type: process
          content: "FMC: arrive at non-PCI center"
        - id: "fmc_pci"
          type: process
          content: "FMC: arrive at PCI center"
        - id: "door_to_ecg_non_pci"
          type: decision
          content: "Door-to-ECG ≤10 min (Class I)<br>Diagnose STEMI"
        - id: "door_to_ecg_pci"
          type: decision
          content: "Door-to-ECG ≤10 min (Class I)<br>Diagnose STEMI<br>Activate cath lab"
    - level_name: "非PCI中心路径"
      nodes:
        - id: "notify_non_pci"
          type: process
          content: "Notify non-PCI center of STEMI patient en route"
        - id: "arrive_non_pci"
          type: process
          content: "Arrive at non-PCI center"
        - id: "non_pci_reperfusion_commit"
          type: process
          content: "Non-PCI center commits to reperfusion strategy"
        - id: "fibrinolysis_strategy"
          type: process
          content: "Fibrinolysis strategy<br>- If PPCI not feasible within 120 min of FMC, or<br>  lysis contraindicated (Class I)<br>- Goal door-to-lysis ≤30 min"
        - id: "assess_post_lysis"
          type: process
          content: "Assess patient for reperfusion after lysis"
        - id: "arrange_transfer_pci"
          type: process
          content: "Arrange for immediate transfer to PCI center:<br>- If lysis failed or patient unstable, arrange for urgent angiography for rescue PCI (Class I)<br>- If lysis successful and patient stable, arrange for early angiography (Class I)"
        - id: "ppci_strategy"
          type: process
          content: "PPCI strategy<br>- If PPCI feasible within 120 min of FMC, or lysis contraindicated (Class I)<br>- Activate cath lab for PPCI<br>- Urgent transfer to PCI center (bypass ED, direct to cath lab, if feasible)"
    - level_name: "PCI中心路径"
      nodes:
        - id: "transport_to_pci"
          type: process
          content: "Transport to PCI center:<br>- Prehospital cath lab activation (Class I)<br>- Direct transport to PCI center for PPCI (Class I)"
        - id: "arrive_pci"
          type: process
          content: "Arrive at PCI center"
        - id: "bypass_ed"
          type: decision
          content: "Bypass ED (if feasible)"
        - id: "ed"
          type: process
          content: "ED"
        - id: "cath_lab"
          type: process
          content: "Cath lab"
        - id: "goal_fmc_to_device"
          type: process
          content: "Goal EMS FMC-to-device ≤90 min (Class I)"
        - id: "goal_fmc_to_device_pci"
          type: process
          content: "Goal FMC-to-device ≤90 min (direct presenters) or ≤120 min (transfers) (Class I)"
        - id: "primary_pci"
          type: process
          content: "Primary PCI"
  edges:
    - from: "start"
      to: "call_911"
    - from: "start"
      to: "self_transport"
    - from: "call_911"
      to: "ems_prehospital_ecg"
    - from: "self_transport"
      to: "fmc_non_pci"
    - from: "self_transport"
      to: "fmc_pci"
    - from: "ems_prehospital_ecg"
      to: "transport_to_pci"
    - from: "fmc_non_pci"
      to: "door_to_ecg_non_pci"
    - from: "fmc_pci"
      to: "door_to_ecg_pci"
    - from: "door_to_ecg_non_pci"
      to: "notify_non_pci"
    - from: "notify_non_pci"
      to: "arrive_non_pci"
    - from: "arrive_non_pci"
      to: "non_pci_reperfusion_commit"
    - from: "non_pci_reperfusion_commit"
      to: "fibrinolysis_strategy"
    - from: "non_pci_reperfusion_commit"
      to: "ppci_strategy"
    - from: "fibrinolysis_strategy"
      to: "assess_post_lysis"
    - from: "assess_post_lysis"
      to: "arrange_transfer_pci"
    - from: "ppci_strategy"
      to: "cath_lab"
    - from: "transport_to_pci"
      to: "arrive_pci"
    - from: "arrive_pci"
      to: "bypass_ed"
    - from: "arrive_pci"
      to: "ed"
    - from: "bypass_ed"
      to: "cath_lab"
    - from: "ed"
      to: "cath_lab"
    - from: "cath_lab"
      to: "goal_fmc_to_device"
    - from: "goal_fmc_to_device"
      to: "primary_pci"
    - from: "door_to_ecg_pci"
      to: "cath_lab"
    - from: "cath_lab"
      to: "goal_fmc_to_device_pci"
    - from: "goal_fmc_to_device_pci"
      to: "primary_pci"
```

**图注说明**：  
Systems of STEMI care, and the most common routes by which patients present for diagnosis and definitive reperfusion therapy for STEMI. Best clinical practice consists of patients calling 9-1-1 (or other emergency services) to activate EMS; EMS obtaining a prehospital ECG, activating the cardiac catheterization laboratory from the field for suspected STEMIs, and transporting the patient to the nearest PCI center when possible; and achieving a system goal of FMC-to-device time within 90 minutes. Colors correspond to Class of Recommendation in Table 2. *Patients with chest tightness or other symptoms indicative of a heart attack. ACS indicates acute coronary syndromes; ED, emergency department; EMS, emergency medical services; FMC, first medical contact; PCI, percutaneous coronary intervention; PPCI, primary percutaneous coronary intervention; and STEMI, ST-segment elevation myocardial infarction.

reperfusion and increased survival in STEMI in several pre- versus postimplementation comparison studies throughout the world.¹⁻⁶ Over the past 15 years, considerable gains have been made in reducing FMC to reperfusion times in patients with STEMI and these improvements in reperfusion times have been associated with improved outcomes.⁵,⁷ Unfortunately, recent declines have been reported in the rates of achieving established STEMI performance measures,⁸ in part due to the COVID-19