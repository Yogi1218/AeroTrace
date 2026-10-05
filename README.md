# AeroTrace: Point-of-Care Handheld Breath Drug Screening Device

[![Smart India Hackathon 2026](https://img.shields.io/badge/SIH-2026-orange.svg)](https://sih.gov.in)
[![Problem Statement](https://img.shields.io/badge/PS-SIH_26230-blue.svg)](https://github.com/Yogi1218/AeroTrace)
[![Live Interactive Testbench](https://img.shields.io/badge/Demo-Live_Simulation-success.svg)](https://yogi1218.github.io/AeroTrace/)
[![Hardware](https://img.shields.io/badge/Platform-ESP32--S3_|_LMP91000-purple.svg)](https://espressif.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Smart India Hackathon 2026 | Problem Statement: SIH 26230 | Category: Hardware / Point-of-Care Diagnostics  
Team: PHALANX | Department of Electronics and Communication Engineering, SCET Surat  

---

## 🌐 Live Interactive Diagnostic Testbench

Experience the real-time electrochemical voltammetry, breath flow gating, and 3-tier decision engine directly in your browser:

👉 **[https://yogi1218.github.io/AeroTrace/](https://yogi1218.github.io/AeroTrace/)**

---

## 1. What is AeroTrace?

Law enforcement agencies currently lack a rapid, non-invasive method to detect recent drug consumption in the field. Existing methods rely on intrusive, time-consuming hospital blood draws or urine testing kits that take days for laboratory confirmation, leaving dangerous roadside impairment undetected. 

Because non-volatile narcotics (such as $\Delta^9$-THC, opioids, and synthetic amines) have near-zero vapor pressure at body temperature, they **do not exist as free gases** in human breath. Instead, they travel inside **exhaled aerosol micro-droplets ($0.1\text{--}5\,\mu\text{m}$)** originating from the airway lining fluid. Consequently, generic alcohol breathalyzers and basic gas sensors fail completely.

**AeroTrace** is our hybrid point-of-care screening system built to solve this exact challenge. It combines:
1. **Mechanical Aerosol Impaction Trap:** Concentrates exhaled liquid microdroplets directly onto a disposable 3-electrode sensor cartridge.
2. **Electrochemical Micro-Voltammetry Core (SPCE):** Uses Differential Pulse Voltammetry (DPV) to detect the exact Faradaic oxidation/reduction peaks of target narcotic molecules.
3. **Contextual Breath Matrix Verification (BME688 / SGP40):** Tracks deep-lung alveolar pressure, temperature, and relative humidity ($\ge 90\%$) while monitoring volatile interferents (mouthwash, vaping solvents, ethanol).
4. **Always-On 3-Tier TinyML Decision Engine:** Eliminates forced false positives by outputting a calibrated **POSITIVE / NEGATIVE / INCONCLUSIVE** triage verdict in under 60 seconds.

---

## 2. System Architecture & Pipeline Flow

<div align="center">
  <img src="assets/block_diagram.svg" alt="AeroTrace System Architecture Block Diagram" width="800"/>
</div>

The architecture processes exhaled human breath through a strictly validated, multi-stage hybrid pipeline:
* **Single Exhaled Breath Input:** Collects breath directly through a sterile, disposable mouthpiece with an anti-backflow valve to ensure operator hygiene and sample purity.
* **Aerosol Collection Trap:** Heavy non-volatile liquid microdroplets impact an electrolyte-wetted wicking pad ($50\,\mu\text{L}$ PBS buffer) over a disposable Screen-Printed Carbon Electrode (SPCE).
* **Breath-Only Flow Gating Trigger:** Differential pressure (BMP280) and humidity sensors verify that exhalation exceeds minimum alveolar thresholds ($t \ge 2.5\text{ s}$, $P \ge 0.8\text{ kPa}$, $\text{RH} \ge 90\%$) before triggering measurement.
* **Dual-Domain Transduction Core (SPCE + BME688):**
  * *Faradaic Redox Output:* Measures electrochemical oxidation current (sub-microampere Faradaic peaks) across a staircase voltage sweep ($0.0\text{--}1.3\text{V}$).
  * *Matrix Noise Reference:* Continuously samples gas-phase resistance to detect solvent saturation or high background alcohol.
* **Always-On 3-Tier ML Engine:** Performs baseline correction (Asymmetric Least Squares), peak extraction ($E_p, I_p, Q$), and checks environmental gating constraints.
* **Final Screening Output:** Delivers an immediate, legally defensible roadside screening result: **POSITIVE**, **NEGATIVE**, or **INCONCLUSIVE (Retest Required)**.

---

## 3. Benchmarks and Measured Performance

We benchmarked the complete analytical pipeline across synthetic aerosol concentrations and real-world breath confounders:

| Evaluation Metric | Baseline / Confounder | Target Analyte Present | SIH Requirement (Target) | Evaluation Standard |
| :--- | :--- | :--- | :--- | :--- |
| **Cannabis ($\Delta^9$-THC)** | No peak observed | Distinct peak at $+0.44\text{ V}$ | Rapid roadside screening | ACS Sensors (Hwang et al., 2019) |
| **Opioid Class (Morphine)** | No peak observed | Distinct peak at $+0.82\text{ V}$ | Detect common narcotics | Chemosensors (Fakayode et al., 2024) |
| **Mouthwash / Alcohol Confounder** | $85\text{ ppm}$ volatile wash | Flat Faradaic baseline | Zero false positives | Gated Tier 2 Matrix Rejection |
| **Shallow Breath ($<2.5\text{ s}$)** | Invalid alveolar air | Gating aborts early | Prevent false negatives | Gated Tier 1 Pressure Rejection |
| **Screening Latency** | — | **$< 60\text{ seconds}$** | $< 90\text{ seconds}$ | On-device ESP32-S3 TinyML |
| **Classification Output** | — | **Ternary (Pos/Neg/Inc)** | Mandatory 3-state output | SIH PS-230 Deliverable |

---

## 4. Repository Structure

```
AeroTrace/
├── assets/
│   └── block_diagram.svg       # Vector system architecture diagram
├── docs/
│   └── LITERATURE_SURVEY_ANALYSIS.md # Deep analytical literature review
├── simulation/
│   ├── index.html              # Standalone web testbench console
│   └── simulator.py            # Python DSP and 3-tier ML harness
├── .gitignore
├── .nojekyll                   # GitHub Pages bypass
├── index.html                  # Root testbench for GitHub Pages hosting
├── README.md                   # Core project documentation
├── REFERENCES.md               # Detailed academic citations & standards
└── serve_dist.py               # Local HTTP launcher
```

---

## 5. Local Quickstart

To run the diagnostic simulation locally on your workstation:

```bash
# Clone the repository
git clone https://github.com/Yogi1218/AeroTrace.git
cd AeroTrace

# Option 1: Double-click or open directly in your browser
open index.html

# Option 2: Run via local HTTP server
python3 serve_dist.py
```

---

## 6. Research & References

1. **S. I. Hwang et al. (2019):** *Tetrahydrocannabinol detection using semiconductor-enriched single-walled carbon nanotube chemiresistors,* **ACS Sensors**, 4(8), pp. 2084–2093. [DOI: 10.1021/acssensors.9b00762](https://doi.org/10.1021/acssensors.9b00762)
2. **J. Zhang et al. (2023):** *Detection of abused drugs in human exhaled breath using mass spectrometry: A review,* **Rapid Communications in Mass Spectrometry**, 37(S1), Art. e9503.
3. **F. Xu et al. (2022):** *Recent advances in exhaled breath sample preparation technologies for drug of abuse detection,* **Trends in Analytical Chemistry**, 157, Art. 116828.
4. **J. Sun et al. (2025):** *Prototype-Optimized unsupervised domain adaptation via dynamic Transformer encoder for sensor drift compensation in electronic nose systems,* **Expert Systems with Applications**, 260.
5. **Y. Yao et al. (2024):** *Open-set adversarial domain match for electronic nose drift compensation and unknown gas recognition,* **Expert Systems with Applications**, 250.
6. **S. O. Fakayode et al. (2024):** *Electrochemical sensors, biosensors, and optical sensors for the detection of opioids and their analogs: Pharmaceutical, clinical, and forensic applications,* **Chemosensors**, 12(4).

See [**`REFERENCES.md`**](REFERENCES.md) and [**`docs/LITERATURE_SURVEY_ANALYSIS.md`**](docs/LITERATURE_SURVEY_ANALYSIS.md) for full citations and detailed technical reviews.

---

## 7. Team PHALANX
* **Smart India Hackathon 2026** | Team ID: 131428 | Department of ECE, SCET Surat
