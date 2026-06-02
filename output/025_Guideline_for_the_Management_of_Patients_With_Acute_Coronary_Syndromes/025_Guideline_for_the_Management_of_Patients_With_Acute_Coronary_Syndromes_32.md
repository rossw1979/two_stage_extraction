---
extraction_strategy: 完整提取
scout_result: {"page_layout": "单栏", "content_blocks": [{"type": "流程图", "position": "中央", "complexity": "高"}, {"type": "段落", "position": "左下", "complexity": "中"}, {"type": "段落", "position": "右下", "complexity": "中"}, {"type": "图片", "position": "中央", "complexity": "高"}], "tables": {"count": 0, "max_rows_estimate": 0, "has_merged_cells": false, "has_multiline_cells": false, "has_footnote_below": true}, "recommendation": "完整提取"}
total_time_seconds: 163.00
page_num: 32
task_id: 6bd3ac5b-c598-47b0-ad8a-caafc3189b3a
re_extracted: True
re_extract_focus: "流程图节点定义缺失（如'arrive_pci_center'未声明）、Cath lab节点被错误拆分、PPCI策略与转诊安排内容归属错位，需严格对照原图重构YAML节点与边关系"
review_needed: True
review_reason: "修正YAML中流程图节点层级错误（特别是'door_to_ecg_pci'不应包含子项，而应与'Diagnose STEMI''Activate cath lab'并列），并明确区分'Bypass ED'的虚线条件路径与ED实线路径的逻辑关系；同时确保截断段落末尾不产生完整性误解。"
---

#### 图 6 Care System Pathway for Patients Experiencing Ischemic Symptoms Suggestive of ACS.

**自然语言概述**：  
该流程图描述了疑似急性冠脉综合征（ACS）患者从症状出现到接受再灌注治疗的完整院前与院内路径。路径分为两条主干：患者拨打911（首选）或自行转运；前者触发EMS系统响应，后者直接进入医院FMC（首次医疗接触）环节。核心目标是实现STEMI患者的快速再灌注，关键时间窗包括：Door-to-ECG ≤10 min、FMC-to-device ≤90 min（直接转诊者）或 ≤120 min（转运者）。流程中明确区分PCI中心与非PCI中心的处理策略，并包含溶栓（Fibrinolysis）与直接PCI（Primary PCI）的决策节点，以及溶栓后补救性PCI或早期血管造影的安排。

**YAML 结构化数据**：

```yaml
flowchart:
  title: "Care System Pathway for Patients Experiencing Ischemic Symptoms Suggestive of ACS"
  levels:
    - level_name: "初始接触"
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
    - level_name: "院前响应（EMS路径）"
      nodes:
        - id: "ems_prehospital_ecg"
          type: process
          content: "EMS obtains prehospital ECG within 10 min of FMC and suspects STEMI (Class I)"
        - id: "ems_destination"
          type: process
          content: "EMS determines destination hospital"
        - id: "transport_to_pci"
          type: process
          content: "Transport to PCI center:"
          items:
            - "Prehospital cath lab activation (Class I)"
            - "Direct transport to PCI center for PPCI (Class I)"
        - id: "notify_non_pci"
          type: process
          content: "Notify non-PCI center of STEMI patient en route"
        - id: "arrive_non_pci"
          type: process
          content: "Arrive at non-PCI center"
        - id: "non_pci_reperfusion"
          type: process
          content: "Non-PCI center commits to reperfusion strategy"
        - id: "fibrinolysis"
          type: process
          content: "Fibrinolysis strategy"
          items:
            - "If PPCI not feasible within 120 min of FMC (Class I)"
            - "Goal door-to-lysis ≤30 min"
        - id: "assess_post_lysis"
          type: process
          content: "Assess patient for reperfusion after lysis"
        - id: "arrange_immediate_transfer"
          type: process
          content: "Arrange for immediate transfer to PCI center:"
          items:
            - "If lysis failed or patient unstable, arrange for urgent angiography for rescue PCI (Class I)"
            - "If lysis successful and patient stable, arrange for early angiography (Class I)"
        - id: "arrive_pci_center"
          type: process
          content: "Arrive at PCI center"
        - id: "bypass_ed"
          type: process
          content: "Bypass ED (if feasible)"
        - id: "ed"
          type: process
          content: "ED"
        - id: "cath_lab"
          type: process
          content: "Cath lab"
        - id: "goal_fmc_device"
          type: process
          content: "Goal EMS FMC-to-device ≤90 min (Class I)"
        - id: "primary_pci"
          type: process
          content: "Primary PCI"
    - level_name: "院内路径（自行转运）"
      nodes:
        - id: "fmc_non_pci"
          type: process
          content: "FMC: arrive at non-PCI center"
        - id: "door_to_ecg_non_pci"
          type: process
          content: "Door-to-ECG ≤10 min (Class I)"
          items:
            - "Diagnose STEMI"
        - id: "fmc_pci"
          type: process
          content: "FMC: arrive at PCI center"
        - id: "door_to_ecg_pci"
          type: process
          content: "Door-to-ECG ≤10 min (Class I)"
          items:
            - "Diagnose STEMI"
            - "Activate cath lab"
        - id: "ppci_strategy"
          type: process
          content: "PPCI strategy"
          items:
            - "If PPCI feasible within 120 min of FMC, or lysis contraindicated (Class I)"
            - "Activate cath lab for PPCI"
            - "Urgent transfer to PCI center (bypass ED, direct to cath lab, if feasible)"
        - id: "goal_fmc_device_direct"
          type: process
          content: "Goal FMC-to-device ≤90 min (direct presenters) or ≤120 min (transfers) (Class I)"
        - id: "primary_pci_direct"
          type: process
          content: "Primary PCI"
  edges:
    - from: "start"
      to: "call_911"
    - from: "start"
      to: "self_transport"
    - from: "call_911"
      to: "ems_prehospital_ecg"
    - from: "ems_prehospital_ecg"
      to: "ems_destination"
    - from: "ems_destination"
      to: "transport_to_pci"
    - from: "ems_destination"
      to: "notify_non_pci"
    - from: "notify_non_pci"
      to: "arrive_non_pci"
    - from: "arrive_non_pci"
      to: "non_pci_reperfusion"
    - from: "non_pci_reperfusion"
      to: "fibrinolysis"
    - from: "fibrinolysis"
      to: "assess_post_lysis"
    - from: "assess_post_lysis"
      to: "arrange_immediate_transfer"
    - from: "transport_to_pci"
      to: "arrive_pci_center"
    - from: "arrive_pci_center"
      to: "bypass_ed"
    - from: "bypass_ed"
      to: "cath_lab"
    - from: "arrive_pci_center"
      to: "ed"
    - from: "ed"
      to: "cath_lab"
    - from: "cath_lab"
      to: "goal_fmc_device"
    - from: "goal_fmc_device"
      to: "primary_pci"
    - from: "self_transport"
      to: "fmc_non_pci"
    - from: "self_transport"
      to: "fmc_pci"
    - from: "fmc_non_pci"
      to: "door_to_ecg_non_pci"
    - from: "door_to_ecg_non_pci"
      to: "non_pci_reperfusion"
    - from: "fmc_pci"
      to: "door_to_ecg_pci"
    - from: "door_to_ecg_pci"
      to: "ppci_strategy"
    - from: "ppci_strategy"
      to: "cath_lab"
    - from: "cath_lab"
      to: "goal_fmc_device_direct"
    - from: "goal_fmc_device_direct"
      to: "primary_pci_direct"
```

**图注说明**：  
Systems of STEMI care, and the most common routes by which patients present for diagnosis and definitive reperfusion therapy for STEMI. Best clinical practice consists of patients calling 9-1-1 (or other emergency services) to activate EMS; EMS obtaining a prehospital ECG, activating the cardiac catheterization laboratory from the field for suspected STEMIs, and transporting the patient to the nearest PCI center when possible; and achieving a system goal of FMC-to-device time within 90 minutes. Colors correspond to Class of Recommendation in Table 2. *Patients with chest tightness or other symptoms indicative of a heart attack. ACS indicates acute coronary syndromes; ED, emergency department; EMS, emergency medical services; FMC, first medical contact; PCI, percutaneous coronary intervention; PPCI, primary percutaneous coronary intervention; and STEMI, ST-segment elevation myocardial infarction.

reperfusion and increased survival in STEMI in several pre- versus postimplementation comparison studies throughout the world.¹⁻⁶ Over the past 15 years, considerable gains have been made in reducing FMC to reperfusion times in patients with STEMI and these improvements in reperfusion times have been associated with improved outcomes.⁵,⁷ Unfortunately, recent declines have been reported in the rates of achieving established STEMI performance measures,⁸ in part due to the COVID-19 pandemic and