"""
AeroScreen SIH PS-230: Pure Python Signal Processing & 3-Tier ML Classifier Simulator
(Zero external dependencies - runs on standard Python 3 standard library)

Simulates:
1. Synthetic Differential Pulse Voltammetry (DPV) curve generation (Butler-Volmer / Randles-Sevcik)
2. Breath flow and BME688 multi-gas resistance curves
3. Feature Extraction (Ep, Ip, Charge Q, dR/dt, Duration)
4. 3-Tier Calibrated Decision Engine (Positive / Negative / Inconclusive)
"""

import math
import random
import json

def generate_dpv_curve(analyte="thc", concentration_ng_ml=120, noise_std=0.015):
    """
    Generates synthetic DPV voltammogram using standard math library.
    THC oxidation ~ +0.44V vs Ag/AgCl
    Opioids (Morphine) ~ +0.82V vs Ag/AgCl
    """
    potentials = [round(v * 0.01, 2) for v in range(131)] # 0.00 to 1.30 V
    currents = []
    baselines = []
    
    peaks = {
        "thc": 0.44,
        "opioid": 0.82,
        "synthetic": 1.15,
        "none": 0.0
    }
    ep = peaks.get(analyte, 0.0)
    
    for v in potentials:
        # Background capacitive baseline current
        base = 0.15 + (v * 0.12) + (math.sin(v * 4.0) * 0.02)
        baselines.append(round(base, 4))
        
        # Faradaic oxidation Gaussian peak
        faradaic = 0.0
        if analyte != "none" and concentration_ng_ml > 15:
            ip = (concentration_ng_ml / 80.0)
            width = 0.065
            faradaic = ip * math.exp(-(((v - ep) / width) ** 2))
            
        noise = random.gauss(0, noise_std)
        total = max(0.0, base + faradaic + noise)
        currents.append(round(total, 4))
        
    return potentials, currents, baselines

def extract_features(potentials, current, baseline, duration_s, max_pressure_kpa, voc_interferent_ppm):
    """
    Extracts multimodal feature vector for Edge TinyML.
    """
    net_current = [c - b for c, b in zip(current, baseline)]
    max_net = max(net_current)
    peak_idx = net_current.index(max_net)
    
    if max_net > 0.15: # Above analytical noise floor
        ep = potentials[peak_idx]
        ip = max_net
        # Numerical trapezoidal integration for charge Q
        charge_q = sum(max(0.0, n) * 0.01 for n in net_current)
    else:
        ep = 0.0
        ip = 0.0
        charge_q = 0.0
        
    return {
        "ep_volts": round(ep, 2),
        "ip_microamps": round(ip, 2),
        "charge_q": round(charge_q, 3),
        "duration_s": float(duration_s),
        "pressure_kpa": float(max_pressure_kpa),
        "voc_interferent_ppm": float(voc_interferent_ppm)
    }

def evaluate_decision_engine(features, target_analyte="thc"):
    """
    3-Tier Calibrated Decision Gate Logic matching SIH Requirements.
    """
    # Tier 1: Breath Quality Check
    if features["duration_s"] < 2.5 or features["pressure_kpa"] < 0.8:
        return {
            "verdict": "INCONCLUSIVE",
            "tier_failed": "Tier 1 (Breath Quality)",
            "reason": "Shallow exhalation (<2.5s) or insufficient alveolar pressure.",
            "led": "AMBER (FLASHING)",
            "confidence": 0.0
        }
        
    # Tier 2: Ambient / Solvent Gate
    if features["voc_interferent_ppm"] >= 45:
        return {
            "verdict": "INCONCLUSIVE",
            "tier_failed": "Tier 2 (Matrix Gate)",
            "reason": f"High volatile interferent ({features['voc_interferent_ppm']} ppm). Potential mouthwash or vaping solvent.",
            "led": "AMBER (STEADY)",
            "confidence": 15.0
        }
        
    # Tier 3: ML Calibrated Impairment Score
    target_windows = {
        "thc": (0.38, 0.50),
        "opioid": (0.76, 0.88),
        "synthetic": (1.10, 1.20)
    }
    
    w_min, w_max = target_windows.get(target_analyte, (0.0, 0.0))
    
    if w_min <= features["ep_volts"] <= w_max and features["ip_microamps"] >= 0.25:
        confidence = min(99.0, 85.0 + (features["ip_microamps"] / 5.0) * 12.0)
        return {
            "verdict": "POSITIVE",
            "tier_passed": "All Tiers (1, 2, 3)",
            "reason": f"Characteristic Faradaic oxidation identified at +{features['ep_volts']}V. Target analyte present.",
            "led": "RED (ALERT)",
            "confidence": round(confidence, 1)
        }
    else:
        return {
            "verdict": "NEGATIVE",
            "tier_passed": "All Tiers (1, 2, 3)",
            "reason": "Baseline flat; no Faradaic redox peaks above limit of detection (LOD).",
            "led": "GREEN (CLEAR)",
            "confidence": 96.0
        }

if __name__ == "__main__":
    print("=" * 65)
    print("  AEROSCREEN (SIH PS-230) - 3-TIER DECISION ENGINE VERIFICATION")
    print("=" * 65)
    
    test_cases = [
        {"name": "Cannabis (THC) Impairment", "analyte": "thc", "conc": 160, "dur": 3.4, "pres": 2.1, "voc": 5},
        {"name": "Opioid Class Detection", "analyte": "opioid", "conc": 210, "dur": 3.2, "pres": 1.9, "voc": 8},
        {"name": "Clean Breath (Non-impaired)", "analyte": "none", "conc": 0, "dur": 3.5, "pres": 2.0, "voc": 4},
        {"name": "Shallow Exhalation Attempt", "analyte": "thc", "conc": 150, "dur": 1.2, "pres": 0.5, "voc": 2},
        {"name": "Mouthwash / Alcohol Confounder", "analyte": "none", "conc": 0, "dur": 3.2, "pres": 1.8, "voc": 85},
    ]
    
    for tc in test_cases:
        pot, cur, base = generate_dpv_curve(analyte=tc["analyte"], concentration_ng_ml=tc["conc"])
        feat = extract_features(pot, cur, base, duration_s=tc["dur"], max_pressure_kpa=tc["pres"], voc_interferent_ppm=tc["voc"])
        res = evaluate_decision_engine(feat, target_analyte=tc["analyte"] if tc["analyte"] != "none" else "thc")
        
        print(f"\n[SCENARIO]: {tc['name']}")
        print(f"  Features: Ep={feat['ep_volts']}V | Ip={feat['ip_microamps']}µA | Dur={feat['duration_s']}s | Pres={feat['pressure_kpa']}kPa | VOC={feat['voc_interferent_ppm']}ppm")
        print(f"  Verdict:  >> {res['verdict']} << (Confidence: {res['confidence']}%)")
        print(f"  Hardware: LED={res['led']}")
        print(f"  Detail:   {res['reason']}")
    print("\n" + "=" * 65)
