# AeroTrace: Literature Survey, Benchmark Analysis, and Theoretical Foundations

Smart India Hackathon 2026 | Problem Statement: SIH 26230 | Team PHALANX  
Category: Hardware / Point-of-Care Diagnostics  
Department of Electronics and Communication Engineering, SCET Surat  

---

## 1. Why Existing Solutions Fall Short in Roadside Field Screening

When evaluating existing narcotics detection technologies for law enforcement at checkpoints, standard analytical methods encounter critical operational bottlenecks:

1. **The Gas-Phase Physical Impossibility:** Cannabinoids ($\Delta^9$-THC), opioids (morphine, fentanyl), and synthetic amines have near-zero vapor pressures ($<10^{-6}\text{ to }10^{-8}\text{ mmHg}$) at physiological temperatures. They **do not exist as free volatile organic gases (VOCs)** in breath. Instead, they travel inside **aerosol microdroplets ($0.1\text{--}5\,\mu\text{m}$)** from airway lining fluid. Consequently, generic alcohol breathalyzers and MOS gas sensors (MQ series) are fundamentally incapable of detecting them.
2. **Invasive & Delayed Lab draws:** Standard blood and urine tests require certified medical personnel, chain-of-custody transport, and multi-day laboratory backlogs at State Forensic Science Laboratories (FSLs). By the time blood is drawn (typically $2\text{ to }4\text{ hours}$ post-stop), active pharmacodynamic impairment has plummeted.
3. **Historical vs. Impairment Confusion in Urine:** Urine testing detects non-psychoactive hydrophilic metabolites (e.g., THC-COOH glucuronide) that clear slowly over days or weeks. This punishes historical users without providing proof of acute roadside impairment.
4. **Humidity & Thermal Saturation in Field Hardware:** Human exhaled breath contains $95\%\text{--}100\%$ relative humidity (RH) at $34^\circ\text{C}$ to $37^\circ\text{C}$. Unconditioned gas sensors saturate immediately, causing severe baseline drift and false positives.

AeroTrace solves these limitations by coupling an **aerodynamic inertial impaction chamber** with disposable **Screen-Printed Carbon Electrodes (SPCE)** and an **Always-On 3-Tier ML Decision Engine**.

---

## 2. Comparative Analysis of Published Literature (Chronological Order: Newest First)

We reviewed and benchmarked the published state-of-the-art across aerosol toxicology, electrochemical voltammetry, and open-set domain adaptation:

| Year | Citation & Authors | Core Technology / Methodology | Benchmark Results / LOD | Identified Gap in Roadside Field Use | How AeroTrace Solves It |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2025** | **J. Sun, Y. Yao et al.**<br>*Prototype-Optimized Unsupervised Domain Adaptation* (Expert Systems with Applications) | Dynamic Transformer encoder for electronic nose drift compensation across shifting environments | Substantial classification accuracy improvement under ambient drift | Focuses solely on gas-phase sensor drift; does not address aerosol collection or electrochemical cell interfaces. | We apply their mathematical framework to construct **Tier 3 uncertainty gating**, preventing false classifications when sensor drift is detected. |
| **2024** | **Y. Yao, J. Sun, K. Zhang et al.**<br>*Open-Set Adversarial Domain Match for E-Nose Drift* (Expert Systems with Applications) | Adversarial feature alignment for identifying unknown/out-of-distribution gas classes | Accurate rejection of unseen interfering volatile species | Evaluated purely in synthetic software; lacks embedded hardware implementation on low-power microcontrollers. | We embed a compact version of this open-set rejection logic directly into our ESP32-S3 firmware, outputting **"Inconclusive – Retest Required"**. |
| **2024** | **S. O. Fakayode, P. N. Brady et al.**<br>*Electrochemical, Biosensors & Optical Sensors for Opioids* (Chemosensors) | Comprehensive review of voltammetric and optical sensing mechanisms for morphine, codeine, fentanyl | Sub-nanomolar LOD in buffer; rapid Faradaic electron transfer kinetics | Focuses on laboratory liquid aliquots; does not address breath aerosol capture or field sample preparation. | We bridge this gap by wicking breath aerosols onto disposable SPCE cartridges pre-wetted with physiological PBS buffer ($50\,\mu\text{L}$). |
| **2023** | **J. Zhang, Y. Zhang, B. Hu et al.**<br>*Detection of Abused Drugs in Human Breath using MS* (Rapid Comm. Mass Spectrom.) | Mass spectrometry profiling of illicit drugs in exhaled breath condensate (EBC) | Direct picogram quantification ($<1\text{ pg/L}$) across THC, opioids, and synthetic stimulants | Requires high-vacuum turbomolecular pumps and expensive benchtop spectrometers ($\$150\text{k+}$). | Serves as the analytical reference baseline for our synthetic benchmark dataset and calibration windows. |
| **2022** | **F. Xu, J. Zhou, H. Yang, Y. Zhao et al.**<br>*Recent Advances in Exhaled Breath Sample Preparation* (Trends in Anal. Chem.) | Evaluated membrane filtration, cyclone separators, and impaction plates for breath drug collection | $85\%\text{--}92\%$ aerosol capture efficiency for droplets $>1\,\mu\text{m}$ | Devices were passive collectors requiring external extraction solvents and secondary lab bench instruments. | We design a self-contained 3D-printed aerodynamic impaction chamber where droplets impact directly onto the disposable SPCE electrode surface. |
| **2019** | **S. I. Hwang, A. Star et al.**<br>*Tetrahydrocannabinol Detection Using SWCNT Chemiresistors* (ACS Sensors) | Carbon nanotube chemiresistive field-effect transistors binding phenolic THC molecules | $10\text{ ng/mL}$ in breath simulator; clean electronic readout | Nanotube surface recovery requires prolonged thermal desorption; prone to fouling by ambient saliva droplets. | We use disposable, low-cost (₹300) screen-printed carbon strips that are discarded after each single roadside test, eliminating fouling. |

---

## 3. Mathematical & Analytical Foundations

### 3.1 Randles-Ševčík Faradaic Peak Current Formulation
In Differential Pulse Voltammetry (DPV) at the working electrode of our SPCE strip, the peak Faradaic oxidation current $I_p$ is governed by diffusion-controlled mass transport:
$$I_p = 0.4463 \cdot n F A C^* \sqrt{\frac{n F v D}{R T}}$$

Where:
* $n$: Number of electrons transferred during target oxidation ($n = 2$ for phenolic $\Delta^9$-THC oxidation to quinone).
* $F$: Faraday's constant ($96,485\text{ C/mol}$).
* $A$: Working electrode geometric surface area ($0.126\text{ cm}^2$ for standard $4\text{ mm}$ carbon disk).
* $D$: Diffusion coefficient of analyte in physiological buffer ($\approx 5.2 \times 10^{-6}\text{ cm}^2/\text{s}$).
* $v$: Voltammetric potential scan rate ($v = 50\text{ mV/s}$).
* $C^*$: Bulk concentration of drug molecules impacted onto the wicking membrane.

This direct proportionality ($I_p \propto C^*$) enables our embedded ML model to correlate peak current height with recent consumption levels.

### 3.2 Breath Inertial Droplet Impaction Physics
To separate non-volatile aerosol droplets from exhaled air, breath is directed through a narrowing nozzle towards the wicking collection pad. The impaction efficiency is determined by the dimensionless **Stokes number ($Stk$)**:
$$Stk = \frac{\rho_p d_p^2 U C_c}{9 \mu D_{\text{nozzle}}}$$

Where $\rho_p$ is droplet density ($1000\text{ kg/m}^3$), $d_p$ is aerosol aerodynamic diameter ($1\text{--}5\,\mu\text{m}$), $U$ is breath flow velocity ($>15\text{ m/s}$), and $\mu$ is air viscosity. For $Stk > 0.5$, droplets cross fluid streamlines and impact the wicking matrix, while lighter gas-phase air flows around to the BME688 sensor chamber.

### 3.3 3-Tier Calibrated Decision Engine Equations
The final screening outcome $Y \in \{\text{POSITIVE}, \text{NEGATIVE}, \text{INCONCLUSIVE}\}$ is evaluated via strict hierarchical gating:

$$\text{Tier 1 (Breath Quality Gate):} \quad G_1 = \mathbb{I}\left( t_{\text{breath}} \ge 2.5\text{ s} \;\land\; P_{\text{max}} \ge 0.8\text{ kPa} \;\land\; \text{RH} \ge 90\% \right)$$

$$\text{Tier 2 (Matrix & Solvent Gate):} \quad G_2 = \mathbb{I}\left( \text{VOC}_{\text{interferent}} < 45\text{ ppm} \;\land\; \left|\frac{dR_{\text{gas}}}{dt}\right| < \theta_{\text{thermal}} \right)$$

$$\text{Tier 3 (ML Impairment Classifier):} \quad P(\text{Drug} \mid \mathbf{X}) = \sigma\left(\mathbf{w}^T \mathbf{X} + b\right)$$

$$\text{Outcome} = \begin{cases} 
\text{INCONCLUSIVE}, & \text{if } G_1 = 0 \lor G_2 = 0 \lor H(P) > H_{\text{threshold}} \\
\text{POSITIVE}, & \text{if } G_1 = 1 \land G_2 = 1 \land P(\text{Drug}) \ge 0.85 \land E_p \in [E_{\text{target}} \pm 60\text{mV}] \\
\text{NEGATIVE}, & \text{if } G_1 = 1 \land G_2 = 1 \land P(\text{Drug}) \le 0.15
\end{cases}$$

Where $H(P) = -P\log_2(P) - (1-P)\log_2(1-P)$ is the Shannon prediction entropy representing classification uncertainty.

---

## 4. Hardware Datasheet Specifications

* **LMP91000 Potentiostat AFE IC:** Low power ($10\,\mu\text{A}$ standby), integrated internal transimpedance amplifier (TIA gain selectable $2.75\text{ k}\Omega\text{ to }350\text{ k}\Omega$), $I^2C$ programmable bias.
* **ADS1115 16-Bit Precision ADC:** 860 SPS sample rate, internal low-drift voltage reference ($V_{\text{ref}} = 2.048\text{V}$), 16-bit effective resolution ($7.8\,\mu\text{V}/\text{LSB}$ at PGA gain 4).
* **Bosch BME688 AI Multi-Gas Sensor:** Integrated relative humidity ($0\text{--}100\% \pm 3\%$), barometric pressure ($300\text{--}1100\text{ hPa}$), and customized scanning gas resistance.
* **ESP32-S3 Dual-Core SoC:** Xtensa 32-bit LX7 at $240\text{ MHz}$, 512 KB SRAM, 8 MB PSRAM, hardware-accelerated vector instructions for quantized TinyML inference, integrated BLE 5.0.
