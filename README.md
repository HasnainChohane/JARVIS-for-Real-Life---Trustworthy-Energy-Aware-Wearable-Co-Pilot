# JARVIS for Real Life — Trustworthy Wearable Co-Pilot

![Status](https://shields.io)
![Python](https://shields.io)
![Focus](https://shields.io)

> *"Inspired by J.A.R.V.I.S. in Avengers — Tony Stark had unlimited energy (Arc Reactor) and an always-correct AI. In real life, wearable sensors are batteryless, data is intermittent, and AI makes mistakes."*

**Author:** Muhammad Hasnain — National University of Sciences and Technology (NUST), Pakistan  
**Research Inspiration / Target Mentor:** Prof. Kristof Van Laerhoven, University of Siegen  
**Project Status:** Day 1 — Simulation & Baseline Implementation  

---

## 1. Overview

This project develops an **energy-aware, uncertainty-calibrated wearable AI Co-Pilot**. Unlike standard Human Activity Recognition (HAR) systems that assume continuous sensor streams and output overconfident predictions, this system:

* **Handles Intermittent Power:** Operates under realistic batteryless energy-harvesting cycles where 20–40% of sensor data drops out.
* **Communicates Uncertainty:** Explicitly calculates and reports calibrated confidence when data is missing (e.g., *"I am only 54% sure you are walking"*), preventing hallucinated certainty.
* **Adapts to Cognitive Load:** Delivers short, actionable prompts when the user is active and detailed insights when stationary.

**Core Research Pillars:** `HAR` + `Energy Constraints` + `Missing-Data Robustness` + `Trust Calibration`

---

## 2. Motivation

The gap between fictional AI assistants like J.A.R.V.I.S. and real-world wearable systems comes down to three practical constraints:

| Fictional AI (J.A.R.V.I.S.) | Real-World Wearable Constraints |
| :--- | :--- |
| Unlimited power via Arc Reactor | **Batteryless sensors** must sleep periodically to harvest energy |
| Always accurate and reliable | **Standard AI hallucinates** with high confidence even when data is missing |
| Seamless situational awareness | **Context-blind responses** overwhelm users during high physical/cognitive load |

---

## 3. Problems That Arise & How This Project Handles Them

Real-world wearable AI fails when treated as a standard classification problem. Below are the **five core technical problems** that arise in this pipeline and the exact mechanisms used to solve them:

| # | Problem That Arises | Why It Happens / Impact | How This System Handles It |
| :--- | :--- | :--- | :--- |
| **1** | **Burst Data Loss (Intermittent Sensing)** | Batteryless sensors sleep to harvest energy, dropping **20–40%** of consecutive samples. Standard HAR models treat `0`s as "standing still" and misclassify activity. | **Intermittent Simulation & Masking:** Models realistic burst-dropouts during training and tracks the exact `missing_rate` per time window rather than treating missingness blindly. |
| **2** | **Severe Compute & Memory Limits** | Running heavy deep learning or on-device LLMs drains harvested energy immediately and exceeds microcontroller RAM/FLOP budgets. | **Neural Architecture Search (NAS):** Searches a constrained TinyML space to find a lightweight 1D-CNN/TCN that maximizes accuracy under strict FLOP limits, offloading LLM generation off-device. |
| **3** | **Overconfident AI Hallucinations** | Softmax outputs often report `90–99%` confidence even when 40% of the sensor window is empty, leading to silent, dangerous errors. | **Missingness-Aware Calibration:** Penalizes raw model confidence using the window's missing data rate (`Conf_cal = Conf_raw × (1 - Missing_Rate)`), aligning confidence with true reliability. |
| **4** | **Blind Automation Failure** | When sensor dropouts make activity recognition unreliable, forcing an automated action destroys user trust. | **Human-in-the-Loop Fallback:** If calibrated confidence falls below `0.60`, the system pauses automation and asks a lightweight confirmation question (*"Are you walking? [Yes/No]"*). |
| **5** | **Cognitive Overload & Distraction** | Sending long text or voice explanations while a user is walking/running (HR > 120 BPM) increases stress and physical hazard. | **Activity-Adaptive Co-Pilot:** Conditions the LLM prompt on detected activity—delivering micro-prompts when walking, detailed advice when sitting, and remaining silent when running. |

---

## 4. Research Question

> *How can we design a wearable Co-Pilot that remains energy-efficient under intermittent sensing, robust to burst missing data, and trustworthy by accurately communicating its uncertainty and adapting to user cognitive load?*

---

## 5. End-to-End System Architecture & Failure Handling

```text
[Batteryless Wearable Sensors]
  Accelerometer + Gyroscope + Heart Rate
        │
        ▼
[Layer 1: Intermittent Data Simulation & Tracking]
  ├── Problem: Sensor sleeps to harvest energy -> 20–40% burst data loss.
  └── Handling: Masks dropped packets as 0 AND passes `missing_rate` metadata forward.
        │
        ▼
[Layer 2: Lightweight Robust Model (NAS)]
  ├── Problem: Heavy models exceed energy budget; standard models fail on zero-masked gaps.
  └── Handling: NAS discovers a compact TinyML model trained specifically on intermittent windows.
        │
        ▼
[Layer 3: Trust & Calibration Layer]
  ├── Problem: Raw softmax is overconfident (e.g., 90% sure despite 40% missing data).
  ├── Handling: Calibrated Confidence = Model Confidence × (1 - Missing Data Rate)
  ├── If Confidence < 0.60 ──► Human-in-the-Loop fallback ("Are you walking? [Yes/No]")
  └── If Confidence ≥ 0.60 ──► Verified activity state passed to Co-Pilot
        │
        ▼
[Layer 4: Activity-Adaptive Co-Pilot (LLM)]
  ├── Problem: Long responses distract or stress users during physical exertion.
  ├── WALKING ──► Concise micro-prompt ("Turn left.")
  ├── SITTING ──► Detailed explanation ("Turn left; heavy traffic ahead...")
  └── RUNNING ──► Silent mode (queues non-urgent alerts until user slows down)
        │
        ▼
[Human User]
  Retains final decision-making authority; AI acts strictly as an uncertainty-aware advisor.
```

---

## 6. Design Rationale & Academic Alignment

| Architectural Layer | Technical Justification | Academic Alignment |
| :--- | :--- | :--- |
| **Batteryless Sensing** | Eliminates battery maintenance; enforces realistic energy budgets | Prof. Jasmin Grosinger |
| **NAS + Robust Model** | Standard models fail on missing windows; NAS optimizes accuracy vs. FLOPs | Prof. Jovita Lukasik |
| **Trust + Calibration** | Prevents overconfident errors and enables human-in-the-loop fallback | RC-Trust Framework |
| **Activity-Adaptive Co-Pilot** | Aligns output verbosity with the user's real-time physical and cognitive state | Prof. Kristof Van Laerhoven |

---

## 7. Step-by-Step Walkthrough Scenarios

### Scenario A: High Missing Data While Walking (Uncertainty Handling)
1. **Sensor State:** Energy reserves drop; `40%` of the sensor window is lost during sleep cycles.
2. **Model Output:** The TinyML HAR model predicts `WALKING` with `90%` raw softmax confidence.
3. **Failure Prevented:** Without calibration, the system would act as if it is `90%` certain.
4. **Trust Layer Handling:** Computes `0.90 × (1 - 0.40) = 54%` calibrated confidence (`< 60%` threshold).
5. **Co-Pilot Output:** *"I'm only 54% sure you are walking due to missing sensor data. Are you currently walking? [Yes / No]"*

### Scenario B: Reliable Data While Sitting (Cognitive Load Adaptation)
1. **Sensor State:** Ample harvested energy; only `5%` data missing.
2. **Model Output:** Predicts `SITTING` with `95%` raw confidence.
3. **Trust Layer Handling:** Computes `0.95 × (1 - 0.05) = 90%` calibrated confidence (`≥ 60%` threshold).
4. **Co-Pilot Output:** *"You have been sitting for 2 hours and your heart rate is elevated. I recommend taking a 5-minute walk in 10 minutes."*

---

## 8. Tech Stack & Evaluation Metrics

* **Language:** Python 3.9+
* **Datasets:** UCI HAR (initial baseline), PAMAP2 (multi-sensor expansion)
* **Modeling & NAS:** PyTorch, Scikit-learn, compact 1D-CNN / TinyML search space
* **Co-Pilot Generation:** LLM API conditioned on activity state and calibrated confidence
* **Evaluation Metrics:**
  * **Baseline Accuracy:** Standard classification performance on complete data (`0%` missing).
  * **Missing-Data Robustness:** Accuracy retention across `10%`, `20%`, `30%`, and `40%` burst dropout rates.
  * **Calibration Quality:** Expected Calibration Error (ECE) & Brier Score before vs. after calibration.
  * **Hardware Efficiency:** Parameter count, memory footprint, and `FLOPs` per inference.

---

## 9. Repository Structure (Planned)

```text
trustworthy-wearable-copilot/
├── data/                         # Raw and preprocessed UCI HAR / PAMAP2 datasets
├── src/
│   ├── simulate_intermittent.py  # Simulates batteryless sleep cycles & burst dropouts
│   ├── baseline_har.py           # Baseline HAR classification model
│   ├── nas_search.py             # Lightweight architecture search under FLOP constraints
│   ├── trust_calibration.py      # Confidence calibration & human-in-the-loop logic
│   └── copilot_llm.py            # Activity-adaptive LLM response generator
├── notebooks/                    # Robustness curves & calibration plots
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 10. Development Roadmap

* [x] **Week 1:** Intermittent sensing simulation (`simulate_intermittent.py`) & baseline HAR model (UCI HAR)
* [ ] **Week 2:** Robustness benchmarking across `10%–40%` missing data rates
* [ ] **Week 3:** Neural Architecture Search (NAS) for compact, missing-data-resilient models
* [ ] **Week 4:** Uncertainty calibration & human-in-the-loop fallback mechanism*
* [ ] **Week 5:** Activity-adaptive LLM Co-Pilot integration
* [ ] **Week 6:** End-to-end prototype demo & final evaluation
      
## 11. Academic Inspiration & Collaboration Goals

This work is directly inspired by research in **Ubiquitous Computing and Embedded Systems** at the **University of Siegen**, particularly **Prof. Kristof Van Laerhoven's** work on wearable sensing and human activity recognition, alongside **Prof. Jasmin Grosinger** (batteryless systems), **Prof. Jovita Lukasik** (robust NAS), and **RC-Trust** (trustworthy human-AI interaction).

### Collaboration Objectives
1. Seek architectural and methodological feedback on intermittent HAR and calibration.
2. Discuss benchmark datasets and evaluation protocols for batteryless sensing.
3. Explore collaboration opportunities during **EXCELS Onsite (14 Days in Siegen)**.
4. Express interest in a **HiWi position or Master's Thesis** in Wearable Computing.

---

**Contact:** Muhammad Hasnain Maqsood Pakistan  
**Repository:** `trustworthy-wearable-copilot`

