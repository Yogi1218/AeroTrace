# AeroTrace — Comprehensive Literature Survey & Analytical Review

**Smart India Hackathon 2026** | **Problem Statement: SIH 26230**  
**Project:** AeroTrace — Handheld Point-of-Care Breath Narcotics Screener  
**Team:** PHALANX | Department of Electronics and Communication Engineering, SCET Surat  

---

## 1. Executive Research Summary

Roadside chemical testing presents one of the most demanding operational environments in forensic toxicology. Traditional field sobriety tests rely either on subjective behavioural evaluations (horizontal gaze nystagmus, divided attention tasks) or invasive bodily fluid sampling (blood draws and urine assays). Blood draws necessitate certified phlebotomists and transit to a medical facility, causing a $2\text{ to }4\text{ hour}$ delay during which active blood pharmacokinetics drop significantly. Urine testing reflects historical excretion (metabolites like THC-COOH persist for weeks), failing to demonstrate active impairment at the wheel.

Exhaled breath represents the ideal non-invasive biological matrix for assessing recent drug consumption ($1\text{ to }3\text{ hour}$ impairment window). However, translating breath analysis to a roadside tool requires addressing fundamental transport phenomena: non-volatile narcotics travel in aerosol micro-droplets rather than the gas phase. This survey analyzes the state-of-the-art across analytical spectrometry, electrochemical transduction, matrix verification, and open-set edge pattern recognition.

---

## 2. Comparative Matrix: Existing vs. Proposed Approaches

| Technology Domain | Representative Systems | Operating Mechanism | Limit of Detection (LOD) | Limitations in Field Police Use | AeroTrace Implementation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mass Spectrometry (GC-MS / LC-MS)** | Laboratory standard; Zhang et al. [2] | Chromatographic separation + electron impact / electrospray ionization | Sub-picogram ($<1\text{ pg/L}$) | High capital expenditure ($>\$100\text{k}$), benchtop footprint, requires carrier gases and vacuum pumps. | Gold-standard benchmark for training synthetic surrogate response libraries. |
| **Field Asymmetric IMS (FAIMS)** | Cannabix Technologies | High-field electric waveform ion mobility filtering | $50\text{ pg/L}$ to $1\text{ ng/L}$ | High supply voltage ($>1\text{ kV}$), pneumatic pump power draw, vulnerable to moisture condensation. | Replaced by solid-state potentiostatic voltammetry operating at low power ($<1\text{W}$). |
| **SWCNT Chemiresistors** | Hwang et al. (ACS Sensors) [1] | Carbon nanotube channel conductance shift upon target analyte binding | $10\text{ ng/mL}$ | Surface recovery time ($>10\text{ min}$), sensor drift from relative humidity ($>90\%$). | Employed as the theoretical basis for carbon surface electron transfer dynamics. |
| **Electrochemical Voltammetry (DPV)** | Fakayode et al. [6]; AeroTrace | Differential Pulse Voltammetry on disposable Screen-Printed Electrodes | $15\text{ ng/mL}$ (direct Faradaic) | Requires wetted electrolyte interface and potential sweep generation. | **Core Transducer:** 3-electrode SPCE cartridge with integrated wicking micro-pad. |
| **Metal Oxide Gas Arrays (E-Nose)** | Generic MQ sensors; BME688 | High-temperature surface chemisorption on SnO₂ / WO₃ | $10\text{ to }50\text{ ppb}$ (VOCs only) | **Cannot detect non-volatile narcotics.** Heavy drift from temperature and humidity. | **Secondary Gate:** Used strictly for breath matrix verification and alcohol/solvent rejection. |

---

## 3. Deep Analysis of Primary Literature

### [1] Hwang et al. (ACS Sensors, 2019)
* **Title:** *Tetrahydrocannabinol detection using semiconductor-enriched single-walled carbon nanotube chemiresistors*
* **Core Contribution:** Demonstrated that $\Delta^9$-THC molecules undergo direct non-covalent binding with functionalized carbon nanotube lattices, causing distinct shifts in carrier density without requiring bulky fluorescent tags.
* **Analytical Takeaway for AeroTrace:** Confirmed that carbonaceous electrode materials (carbon nanotubes, graphite, graphene) exhibit predictable electrochemical interaction with the phenolic moiety of THC.

### [2] Zhang et al. (Rapid Communications in Mass Spectrometry, 2023)
* **Title:** *Detection of abused drugs in human exhaled breath using mass spectrometry: A review*
* **Core Contribution:** Established that exhaled narcotics reside exclusively within airway lining fluid (ALF) aerosol droplets ($0.1\text{--}5\,\mu\text{m}$) generated during tidal breathing and alveolar reopening.
* **Analytical Takeaway for AeroTrace:** Direct gas sensors cannot detect cannabinoids or opioids. An aerodynamic impaction mechanism is strictly necessary to separate liquid aerosols from gaseous breath before sensing.

### [3] Xu et al. (Trends in Analytical Chemistry, 2022)
* **Title:** *Recent advances in exhaled breath sample preparation technologies for drug of abuse detection*
* **Core Contribution:** Reviewed mechanical sampling filters, electrostatic precipitators, and impaction plates for breath condensate collection.
* **Analytical Takeaway for AeroTrace:** Inertial impaction onto an absorbent matrix pre-conditioned with physiological buffer salts ($\text{pH } 7.4$) enables rapid dissolution and micro-voltammetry in under 30 seconds.

### [4] Sun et al. & Yao et al. (Expert Systems with Applications, 2024 & 2025)
* **Titles:** *Prototype-Optimized unsupervised domain adaptation...* [4] & *Open-set adversarial domain match for electronic nose drift compensation...* [5]
* **Core Contribution:** Formulated domain adaptation methods to counteract thermal drift, sensor aging, and unexpected environmental confounders in multi-sensor gas arrays.
* **Analytical Takeaway for AeroTrace:** Provided the mathematical basis for our **3-Tier Decision Engine**, which incorporates an explicit out-of-distribution rejection threshold to output **"Inconclusive – Retest Required"** rather than forcing a biased classification.

---

## 4. Confounder Rejection Protocol

| Common Roadside Confounder | Real-World Origin | Potential Sensor Impact | AeroTrace Mitigation Mechanism |
| :--- | :--- | :--- | :--- |
| **Ethanol (Alcohol)** | Alcoholic beverages, mouthwash | High volatility; strong MOS cross-sensitivity | Gated out at **Tier 2** via BME688 VOC resistance slope ($dR/dt$). Voltammetric baseline unaffected ($E_\text{ox} > 1.4\text{V}$). |
| **Menthol / Mints** | Chewing gum, oral sprays | Mild organic vapor signature | Does not exhibit Faradaic redox peaks in the $+0.3\text{V to }+0.9\text{V}$ window on carbon electrodes. |
| **Vape Juice (PG / VG)** | Electronic cigarettes | Aerosol condensation; oily film on sensors | Hydrophilic wicking membrane filters heavy glycols; DPV peak potential windowing isolates target analytes. |
| **Tobacco Smoke** | Cigarette combustion | Trace carbon particles, nicotine, benzene | Multi-gas transient slope identifies combustion matrix; high-confidence redox voltage matching prevents false alerts. |
| **Shallow Exhalation** | Uncooperative driver | Insufficient sample volume | **Tier 1 Flow Gating:** Exhalation duration ($<2.5\text{s}$) or pressure ($<0.8\text{ kPa}$) aborts analysis immediately as **INCONCLUSIVE**. |
