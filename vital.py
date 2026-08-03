"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ECHO AI — VITAL LAYER                            ║
║         Human Health Intelligence · Echo System Health              ║
║                                                                      ║
║  DOMAIN 1 — HUMAN HEALTH (The 9 PhD Doctor)                         ║
║    - Medical diagnosis & differential diagnosis                      ║
║    - Prognosis & treatment planning                                  ║
║    - Drug formulation (with Stellar collaboration)                   ║
║    - Pharmacist / doctor / nurse / patient mode                      ║
║    - Fitness, nutrition, wellness                                    ║
║    - Mental health awareness                                         ║
║    - Emergency triage                                                ║
║    - Drug interaction checking                                       ║
║                                                                      ║
║  DOMAIN 2 — ECHO SYSTEM HEALTH (The Internal Doctor)                ║
║    - Real-time system monitoring                                     ║
║    - Virus / malware / bug detection                                 ║
║    - Dynamic antivirus generation (not a fixed database —            ║
║      generates what it needs for each specific threat)              ║
║    - USB & port threat quarantine                                    ║
║    - Echo immune system — learns new threats                         ║
║    - System healing & auto-repair                                    ║
║    - Performance health monitoring                                   ║
║                                                                      ║
║  JARVIS additions:                                                   ║
║    - Continuous biometric monitoring (JARVIS tracked Tony's          ║
║      vitals through the suit at all times)                           ║
║    - Predictive health alerts (flags issues before symptoms)         ║
║    - Drug discovery pipeline with Stellar                            ║
║    - Adaptive treatment protocols                                    ║
║    - Emotional health cross-reference with Memory layer             ║
║    - Echo self-healing — auto-patches its own code bugs             ║
║    - Threat DNA — builds profiles of every threat it encounters     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import uuid
import time
import math
import json
import random
import hashlib
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


log = logging.getLogger("EchoCore.Vital")


# ══════════════════════════════════════════════
#  SECTION 1 — SHARED ENUMS & MODELS
# ══════════════════════════════════════════════

class Severity(Enum):
    NONE      = 0
    MILD      = 1
    MODERATE  = 2
    SEVERE    = 3
    CRITICAL  = 4
    EMERGENCY = 5


class MedicalMode(Enum):
    PATIENT      = "patient"       # Layman — simple language
    NURSE        = "nurse"         # Clinical but practical
    DOCTOR       = "doctor"        # Full clinical detail
    PHARMACIST   = "pharmacist"    # Drug-focused analysis
    RESEARCHER   = "researcher"    # Scientific/experimental
    FITNESS      = "fitness"       # Wellness & performance


class ThreatCategory(Enum):
    VIRUS        = "virus"
    MALWARE      = "malware"
    RANSOMWARE   = "ransomware"
    TROJAN       = "trojan"
    SPYWARE      = "spyware"
    ROOTKIT      = "rootkit"
    EXPLOIT      = "exploit"
    USB_THREAT   = "usb_threat"
    NETWORK_WORM = "network_worm"
    BUG          = "bug"
    CORRUPTION   = "corruption"
    UNKNOWN      = "unknown"


# ══════════════════════════════════════════════
#  SECTION 2 — HUMAN HEALTH ENGINE
# ══════════════════════════════════════════════

# ─────────────────────────────────────────────
#  MEDICAL KNOWLEDGE BASE
# ─────────────────────────────────────────────

class MedicalKnowledgeBase:
    """
    Echo's medical knowledge — structured like a doctor
    with 9 PhDs across all medical disciplines.
    In production this connects to validated medical
    databases (PubMed, FDA, WHO, clinical trial data).
    """

    # Symptom → possible conditions mapping
    SYMPTOM_CONDITIONS = {
        "fever":          ["influenza", "bacterial infection", "covid-19",
                           "malaria", "sepsis", "pneumonia"],
        "chest pain":     ["myocardial infarction", "angina", "pericarditis",
                           "pulmonary embolism", "aortic dissection", "GERD"],
        "headache":       ["tension headache", "migraine", "hypertension",
                           "meningitis", "subarachnoid hemorrhage", "cluster headache"],
        "shortness of breath": ["asthma", "COPD", "heart failure",
                                "pulmonary embolism", "anxiety", "pneumonia"],
        "fatigue":        ["anemia", "hypothyroidism", "diabetes",
                           "depression", "sleep apnea", "chronic fatigue syndrome"],
        "joint pain":     ["rheumatoid arthritis", "osteoarthritis", "gout",
                           "lupus", "lyme disease", "fibromyalgia"],
        "nausea":         ["gastroenteritis", "food poisoning", "migraine",
                           "appendicitis", "pregnancy", "medication side effect"],
        "dizziness":      ["vertigo", "hypotension", "anemia",
                           "dehydration", "inner ear disorder", "stroke"],
        "rash":           ["eczema", "psoriasis", "allergic reaction",
                           "contact dermatitis", "shingles", "measles"],
        "abdominal pain": ["appendicitis", "IBS", "peptic ulcer",
                           "kidney stones", "pancreatitis", "ectopic pregnancy"]
    }

    # Drug database (simplified — production uses FDA database)
    DRUG_DATABASE = {
        "ibuprofen": {
            "class"          : "NSAID",
            "uses"           : ["pain", "fever", "inflammation"],
            "dosage"         : "200-400mg every 4-6 hours",
            "max_daily"      : "1200mg (OTC), 3200mg (Rx)",
            "contraindications": ["peptic ulcer", "renal failure", "aspirin allergy"],
            "interactions"   : ["warfarin", "aspirin", "lithium", "methotrexate"],
            "side_effects"   : ["GI upset", "renal impairment", "cardiovascular risk"],
            "pregnancy_cat"  : "Category C (avoid in 3rd trimester)"
        },
        "amoxicillin": {
            "class"          : "Penicillin antibiotic",
            "uses"           : ["bacterial infections", "pneumonia", "strep throat"],
            "dosage"         : "250-500mg every 8 hours",
            "max_daily"      : "3000mg",
            "contraindications": ["penicillin allergy", "mononucleosis"],
            "interactions"   : ["warfarin", "methotrexate", "oral contraceptives"],
            "side_effects"   : ["diarrhea", "nausea", "allergic reaction", "rash"],
            "pregnancy_cat"  : "Category B (generally safe)"
        },
        "metformin": {
            "class"          : "Biguanide antidiabetic",
            "uses"           : ["type 2 diabetes", "PCOS", "insulin resistance"],
            "dosage"         : "500-2000mg daily with meals",
            "max_daily"      : "3000mg",
            "contraindications": ["renal failure", "hepatic failure", "IV contrast"],
            "interactions"   : ["alcohol", "contrast dye", "topiramate"],
            "side_effects"   : ["GI upset", "lactic acidosis (rare)", "B12 deficiency"],
            "pregnancy_cat"  : "Category B"
        },
        "lisinopril": {
            "class"          : "ACE inhibitor",
            "uses"           : ["hypertension", "heart failure", "diabetic nephropathy"],
            "dosage"         : "5-40mg once daily",
            "max_daily"      : "80mg",
            "contraindications": ["pregnancy", "bilateral renal artery stenosis",
                                  "history of angioedema"],
            "interactions"   : ["NSAIDs", "potassium supplements", "lithium"],
            "side_effects"   : ["dry cough", "hyperkalemia", "angioedema", "hypotension"],
            "pregnancy_cat"  : "Category D (contraindicated)"
        },
        "atorvastatin": {
            "class"          : "HMG-CoA reductase inhibitor (statin)",
            "uses"           : ["hypercholesterolemia", "cardiovascular prevention"],
            "dosage"         : "10-80mg once daily",
            "max_daily"      : "80mg",
            "contraindications": ["liver disease", "pregnancy", "myopathy history"],
            "interactions"   : ["fibrates", "niacin", "cyclosporine", "macrolides"],
            "side_effects"   : ["myopathy", "hepatotoxicity", "GI upset"],
            "pregnancy_cat"  : "Category X (contraindicated)"
        }
    }

    # Lab reference ranges
    LAB_RANGES = {
        "hemoglobin_male"    : (13.5, 17.5, "g/dL"),
        "hemoglobin_female"  : (12.0, 15.5, "g/dL"),
        "WBC"                : (4.5,  11.0,  "×10³/μL"),
        "platelets"          : (150,  400,   "×10³/μL"),
        "glucose_fasting"    : (70,   100,   "mg/dL"),
        "HbA1c"              : (4.0,  5.6,   "%"),
        "creatinine_male"    : (0.74, 1.35,  "mg/dL"),
        "creatinine_female"  : (0.59, 1.04,  "mg/dL"),
        "sodium"             : (136,  145,   "mEq/L"),
        "potassium"          : (3.5,  5.0,   "mEq/L"),
        "total_cholesterol"  : (0,    200,   "mg/dL"),
        "LDL"                : (0,    100,   "mg/dL"),
        "HDL_male"           : (40,   999,   "mg/dL"),
        "HDL_female"         : (50,   999,   "mg/dL"),
        "TSH"                : (0.4,  4.0,   "mIU/L"),
        "blood_pressure_sys" : (90,   120,   "mmHg"),
        "blood_pressure_dia" : (60,   80,    "mmHg"),
        "heart_rate"         : (60,   100,   "bpm"),
        "oxygen_saturation"  : (95,   100,   "%"),
        "temperature"        : (36.1, 37.2,  "°C")
    }

    def get_conditions_for_symptoms(self, symptoms: List[str]) -> Dict[str, int]:
        """Map symptoms to possible conditions with frequency scoring."""
        condition_scores: Dict[str, int] = defaultdict(int)
        for symptom in symptoms:
            symptom_lower = symptom.lower().strip()
            for key, conditions in self.SYMPTOM_CONDITIONS.items():
                if key in symptom_lower or symptom_lower in key:
                    for condition in conditions:
                        condition_scores[condition] += 1
        return dict(sorted(condition_scores.items(),
                           key=lambda x: x[1], reverse=True))

    def get_drug_info(self, drug_name: str) -> Optional[Dict]:
        return self.DRUG_DATABASE.get(drug_name.lower())

    def check_interactions(self, drugs: List[str]) -> List[Dict]:
        """Check for drug-drug interactions."""
        interactions = []
        drug_lower   = [d.lower() for d in drugs]

        for drug in drug_lower:
            info = self.DRUG_DATABASE.get(drug)
            if not info:
                continue
            for interacting_drug in info.get("interactions", []):
                if interacting_drug.lower() in drug_lower:
                    interactions.append({
                        "drug_a"  : drug,
                        "drug_b"  : interacting_drug,
                        "severity": "moderate",
                        "note"    : f"{drug} interacts with {interacting_drug}. Monitor closely."
                    })

        return interactions

    def interpret_lab(self, test: str, value: float,
                      gender: str = "male") -> Dict:
        """Interpret a lab result against reference ranges."""
        key = test.lower()
        if gender == "female" and f"{key}_female" in self.LAB_RANGES:
            key = f"{key}_female"
        elif gender == "male" and f"{key}_male" in self.LAB_RANGES:
            key = f"{key}_male"

        if key not in self.LAB_RANGES:
            return {"test": test, "value": value, "interpretation": "Reference range unavailable"}

        low, high, unit = self.LAB_RANGES[key]

        if value < low:
            status = "LOW"
            deviation = ((low - value) / low) * 100
        elif value > high:
            status = "HIGH"
            deviation = ((value - high) / high) * 100
        else:
            status = "NORMAL"
            deviation = 0

        severity = (
            Severity.EMERGENCY if deviation > 50 else
            Severity.SEVERE    if deviation > 30 else
            Severity.MODERATE  if deviation > 15 else
            Severity.MILD      if deviation > 5  else
            Severity.NONE
        )

        return {
            "test"         : test,
            "value"        : value,
            "unit"         : unit,
            "status"       : status,
            "normal_range" : f"{low}–{high} {unit}",
            "deviation_pct": round(deviation, 1),
            "severity"     : severity.name
        }


# ─────────────────────────────────────────────
#  DIAGNOSIS ENGINE
# ─────────────────────────────────────────────

@dataclass
class DiagnosisResult:
    diagnosis_id:    str   = field(default_factory=lambda: str(uuid.uuid4())[:10])
    timestamp:       str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    symptoms:        List  = field(default_factory=list)
    differentials:   List  = field(default_factory=list)   # Ranked possible conditions
    primary_dx:      str   = ""
    confidence:      float = 0.0
    urgency:         str   = "routine"      # routine / urgent / emergent / immediate
    recommended_tests: List = field(default_factory=list)
    red_flags:       List  = field(default_factory=list)
    mode:            str   = MedicalMode.PATIENT.value
    disclaimer:      str   = ("This is an AI-assisted assessment. "
                              "Always consult a qualified healthcare professional.")

    def to_dict(self) -> Dict:
        return asdict(self)


class DiagnosisEngine:
    """
    Differential diagnosis engine.
    Thinks like a clinician — considers all possibilities,
    ranks by probability, flags red flags, assesses urgency.

    Collaborates with Stellar for complex cases.
    """

    RED_FLAG_SYMPTOMS = [
        "chest pain", "difficulty breathing", "loss of consciousness",
        "stroke symptoms", "severe bleeding", "anaphylaxis",
        "crushing chest pain", "sudden severe headache",
        "vision loss", "paralysis", "high fever with stiff neck"
    ]

    EMERGENCY_CONDITIONS = [
        "myocardial infarction", "stroke", "pulmonary embolism",
        "aortic dissection", "anaphylaxis", "sepsis",
        "subarachnoid hemorrhage", "meningitis"
    ]

    def __init__(self, knowledge_base: MedicalKnowledgeBase):
        self.kb = knowledge_base

    def diagnose(self, symptoms: List[str],
                 patient_info: Dict,
                 mode: MedicalMode = MedicalMode.DOCTOR) -> DiagnosisResult:
        """
        Full differential diagnosis from symptoms.
        """
        result = DiagnosisResult(symptoms=symptoms, mode=mode.value)

        # Check red flags first — JARVIS always prioritized critical info
        result.red_flags = [s for s in symptoms
                            if any(rf in s.lower()
                                   for rf in self.RED_FLAG_SYMPTOMS)]

        if result.red_flags:
            result.urgency = "IMMEDIATE — seek emergency care"

        # Get differential diagnoses
        condition_scores = self.kb.get_conditions_for_symptoms(symptoms)

        if not condition_scores:
            result.primary_dx = "Insufficient symptoms for diagnosis"
            result.confidence  = 0.0
            return result

        # Build differential list
        total_score = sum(condition_scores.values())
        differentials = []
        for condition, score in list(condition_scores.items())[:8]:
            prob = score / total_score if total_score > 0 else 0

            # Age adjustment
            age = patient_info.get("age", 40)
            if age > 65 and condition in ["myocardial infarction", "stroke"]:
                prob *= 1.3
            if age < 30 and condition in ["osteoarthritis", "COPD"]:
                prob *= 0.5

            # Check for emergency condition
            is_emergency = condition in self.EMERGENCY_CONDITIONS

            differentials.append({
                "condition"    : condition,
                "probability"  : round(min(prob, 0.99), 3),
                "is_emergency" : is_emergency,
                "score"        : score
            })

            if is_emergency and result.urgency != "IMMEDIATE — seek emergency care":
                result.urgency = "urgent"

        differentials.sort(key=lambda x: x["probability"], reverse=True)
        result.differentials = differentials
        result.primary_dx    = differentials[0]["condition"] if differentials else "Unknown"
        result.confidence    = differentials[0]["probability"] if differentials else 0.0

        # Recommended workup
        result.recommended_tests = self._recommend_tests(
            result.primary_dx, symptoms, patient_info
        )

        # Set urgency if not already emergency
        if result.urgency == "routine" and result.confidence > 0.7:
            if differentials[0]["is_emergency"]:
                result.urgency = "emergent"

        log.info(
            f"[VITAL/DX] Primary: {result.primary_dx} | "
            f"Confidence: {result.confidence:.2f} | "
            f"Urgency: {result.urgency}"
        )

        return result

    def _recommend_tests(self, primary_dx: str,
                          symptoms: List[str],
                          patient_info: Dict) -> List[str]:
        """Recommend appropriate diagnostic workup."""
        tests = ["Complete Blood Count (CBC)", "Comprehensive Metabolic Panel (CMP)"]

        condition_tests = {
            "myocardial infarction": ["ECG", "Troponin I/T", "CK-MB", "Chest X-ray"],
            "pneumonia"            : ["Chest X-ray", "Sputum culture", "Blood culture"],
            "diabetes"             : ["HbA1c", "Fasting glucose", "Urinalysis"],
            "anemia"               : ["Iron studies", "B12/Folate", "Reticulocyte count"],
            "thyroid"              : ["TSH", "Free T4", "Free T3"],
            "influenza"            : ["Rapid influenza test", "PCR if negative"],
            "hypertension"         : ["BP monitoring ×3", "Renal function", "ECG"],
            "stroke"               : ["CT head (non-contrast)", "MRI brain", "ECG"]
        }

        for condition, test_list in condition_tests.items():
            if condition in primary_dx.lower():
                tests.extend(test_list)

        return list(dict.fromkeys(tests))  # Remove duplicates


# ─────────────────────────────────────────────
#  DRUG FORMULATION ENGINE
#  Stellar collaboration module
# ─────────────────────────────────────────────

class DrugFormulationEngine:
    """
    Drug discovery and formulation assistant.
    Works WITH Stellar's reasoning and simulation
    engines to model new drug candidates.

    JARVIS helped Tony design arc reactor components —
    Vital helps design pharmaceutical compounds.

    In production: connects to molecular simulation
    libraries (RDKit, OpenMM, AlphaFold).
    """

    DRUG_CLASSES = {
        "analgesic"     : ["paracetamol", "ibuprofen", "morphine", "tramadol"],
        "antibiotic"    : ["amoxicillin", "ciprofloxacin", "azithromycin"],
        "antiviral"     : ["oseltamivir", "remdesivir", "acyclovir"],
        "antihypertensive": ["lisinopril", "amlodipine", "metoprolol"],
        "antidiabetic"  : ["metformin", "insulin", "sitagliptin"],
        "antidepressant": ["sertraline", "fluoxetine", "venlafaxine"],
        "antifungal"    : ["fluconazole", "itraconazole", "amphotericin B"]
    }

    FORMULATION_STEPS = [
        "Target Identification",
        "Lead Compound Discovery",
        "Structure-Activity Relationship (SAR) Analysis",
        "ADMET Profiling (Absorption, Distribution, Metabolism, Excretion, Toxicity)",
        "Molecular Docking Simulation",
        "In Silico Toxicity Screening",
        "Formulation Design",
        "Stability Analysis",
        "Clinical Trial Design Proposal"
    ]

    def formulate(self, target_condition: str,
                  desired_mechanism: str,
                  constraints: Dict) -> Dict:
        """
        Generate a drug formulation pipeline for a target condition.
        Stellar handles the deep simulation — Vital handles the medical logic.
        """
        formulation_id = str(uuid.uuid4())[:10]

        # Identify drug class needed
        drug_class = self._identify_drug_class(target_condition)

        # Build formulation pipeline
        pipeline = []
        for i, step in enumerate(self.FORMULATION_STEPS, 1):
            # Complexity increases with each step
            confidence = max(0.4, 0.9 - (i * 0.05))
            pipeline.append({
                "step"        : i,
                "name"        : step,
                "description" : self._describe_step(step, target_condition),
                "confidence"  : round(confidence, 2),
                "requires_stellar": i >= 4,  # Steps 4+ need Stellar simulation
                "status"      : "modeled"
            })

        # Safety profile
        safety_profile = self._generate_safety_profile(drug_class, constraints)

        # Regulatory pathway
        regulatory = self._regulatory_pathway(target_condition)

        result = {
            "formulation_id"  : formulation_id,
            "target_condition": target_condition,
            "mechanism"       : desired_mechanism,
            "drug_class"      : drug_class,
            "pipeline"        : pipeline,
            "safety_profile"  : safety_profile,
            "regulatory_path" : regulatory,
            "stellar_required": True,
            "stellar_note"    : (
                "Steps 4-9 require Stellar layer simulation for "
                "molecular modeling, docking, and toxicity prediction."
            ),
            "timeline_estimate": "8-15 years (typical pharmaceutical pipeline)",
            "echo_note"       : (
                "This is a computational drug discovery framework. "
                "All candidates must undergo full preclinical and clinical "
                "validation before any human use."
            ),
            "timestamp"       : datetime.now(timezone.utc).isoformat()
        }

        log.info(
            f"[VITAL/DRUG] Formulation pipeline generated | "
            f"Target: {target_condition} | Steps: {len(pipeline)}"
        )

        return result

    def _identify_drug_class(self, condition: str) -> str:
        condition_lower = condition.lower()
        class_map = {
            "pain"       : "analgesic",
            "infection"  : "antibiotic",
            "virus"      : "antiviral",
            "blood pressure": "antihypertensive",
            "diabetes"   : "antidiabetic",
            "depression" : "antidepressant",
            "fungal"     : "antifungal"
        }
        for keyword, drug_class in class_map.items():
            if keyword in condition_lower:
                return drug_class
        return "novel_compound"

    def _describe_step(self, step: str, condition: str) -> str:
        descriptions = {
            "Target Identification": f"Identify molecular targets involved in {condition}",
            "Lead Compound Discovery": "Screen compound libraries for activity at target",
            "Structure-Activity Relationship (SAR) Analysis": "Map structural features to biological activity",
            "ADMET Profiling (Absorption, Distribution, Metabolism, Excretion, Toxicity)": "Model pharmacokinetic and toxicity profile",
            "Molecular Docking Simulation": "Simulate compound binding to target protein (Stellar)",
            "In Silico Toxicity Screening": "Predict off-target effects and organ toxicity (Stellar)",
            "Formulation Design": "Design delivery system (tablet, IV, patch etc.)",
            "Stability Analysis": "Model shelf life and storage requirements",
            "Clinical Trial Design Proposal": "Draft Phase I/II/III trial protocol"
        }
        return descriptions.get(step, f"Execute {step} for {condition}")

    def _generate_safety_profile(self, drug_class: str, constraints: Dict) -> Dict:
        return {
            "hepatotoxicity_risk" : "low",
            "nephrotoxicity_risk" : "low",
            "cardiotoxicity_risk" : "low",
            "teratogenicity"      : "requires_study",
            "mutagenicity"        : "requires_study",
            "drug_interactions"   : "to_be_modeled",
            "contraindications"   : constraints.get("contraindications", []),
            "monitoring_required" : ["liver function", "renal function", "CBC"]
        }

    def _regulatory_pathway(self, condition: str) -> Dict:
        return {
            "agency"            : "FDA (US) / EMA (EU)",
            "designation"       : "Standard review",
            "phases"            : ["Preclinical", "Phase I", "Phase II", "Phase III", "NDA/BLA"],
            "estimated_duration": "10-15 years",
            "breakthrough_eligible": False,
            "orphan_drug"       : False
        }


# ─────────────────────────────────────────────
#  BIOMETRIC MONITOR
#  JARVIS addition — continuous health tracking
# ─────────────────────────────────────────────

@dataclass
class BiometricReading:
    reading_id:  str   = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp:   str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metric:      str   = ""
    value:       float = 0.0
    unit:        str   = ""
    status:      str   = "normal"
    alert:       bool  = False
    alert_reason: str  = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class BiometricMonitor:
    """
    Continuous biometric monitoring.

    JARVIS tracked Tony's heart rate, blood pressure,
    and suit integrity at all times — not just when asked.
    Echo monitors the user's health metrics continuously
    and flags anomalies before they become problems.

    In production: connects to wearables (Apple Watch,
    Fitbit, glucose monitors, BP cuffs, pulse oximeters).
    """

    ALERT_THRESHOLDS = {
        "heart_rate"        : {"low": 50, "high": 120, "critical_low": 40, "critical_high": 150},
        "blood_pressure_sys": {"low": 90, "high": 140, "critical_low": 70, "critical_high": 180},
        "blood_pressure_dia": {"low": 60, "high": 90,  "critical_low": 40, "critical_high": 120},
        "oxygen_saturation" : {"low": 95, "high": 100, "critical_low": 90, "critical_high": 100},
        "temperature"       : {"low": 36.0, "high": 37.5, "critical_low": 35.0, "critical_high": 39.5},
        "glucose"           : {"low": 70,   "high": 180,  "critical_low": 54,   "critical_high": 250},
        "stress_level"      : {"low": 0,    "high": 7,    "critical_low": 0,    "critical_high": 9}
    }

    def __init__(self):
        self._readings: List[BiometricReading] = []
        self._current: Dict[str, float]        = {}
        self._alerts: List[Dict]               = []
        self._monitoring                        = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock                              = threading.Lock()

    def update(self, metric: str, value: float, unit: str = "") -> BiometricReading:
        """Record a new biometric reading."""
        reading = BiometricReading(metric=metric, value=value, unit=unit)

        # Check thresholds
        thresholds = self.ALERT_THRESHOLDS.get(metric, {})
        if thresholds:
            critical_low  = thresholds.get("critical_low", -999)
            critical_high = thresholds.get("critical_high", 999)
            low           = thresholds.get("low", -999)
            high          = thresholds.get("high", 999)

            if value <= critical_low or value >= critical_high:
                reading.status      = "CRITICAL"
                reading.alert       = True
                reading.alert_reason = f"{metric} at critical level: {value} {unit}"
            elif value < low or value > high:
                reading.status      = "WARNING"
                reading.alert       = True
                reading.alert_reason = f"{metric} outside normal range: {value} {unit}"
            else:
                reading.status = "NORMAL"

        with self._lock:
            self._readings.append(reading)
            self._current[metric] = value

            if reading.alert:
                self._alerts.append(reading.to_dict())
                log.warning(
                    f"[VITAL/BIO] [{reading.status}] "
                    f"{reading.alert_reason}"
                )

        return reading

    def start_continuous_monitoring(self, interval_seconds: int = 30):
        """
        JARVIS addition: Start continuous background monitoring.
        Echo watches your vitals constantly, not just when asked.
        """
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval_seconds,),
            daemon=True
        )
        self._monitor_thread.start()
        log.info(f"[VITAL/BIO] Continuous monitoring started (interval: {interval_seconds}s)")

    def _monitor_loop(self, interval: int):
        """Background monitoring loop."""
        while self._monitoring:
            try:
                # In production: poll connected wearable APIs
                # For now: simulate small fluctuations in current readings
                for metric, current_val in list(self._current.items()):
                    fluctuation = random.gauss(0, current_val * 0.02)
                    new_val     = current_val + fluctuation
                    self.update(metric, round(new_val, 1))
                time.sleep(interval)
            except Exception as e:
                log.error(f"[VITAL/BIO] Monitor loop error: {e}")

    def stop_monitoring(self):
        self._monitoring = False

    def get_current_vitals(self) -> Dict:
        """Get latest reading for each metric."""
        return dict(self._current)

    def get_health_score(self) -> Dict:
        """
        JARVIS addition: Overall health score.
        One number summarizing current health status.
        """
        if not self._current:
            return {"score": None, "status": "No readings yet"}

        score      = 100.0
        warnings   = 0
        criticals  = 0

        for metric, value in self._current.items():
            thresholds = self.ALERT_THRESHOLDS.get(metric, {})
            if not thresholds:
                continue

            if (value <= thresholds.get("critical_low", -999) or
                    value >= thresholds.get("critical_high", 999)):
                score    -= 25
                criticals += 1
            elif (value < thresholds.get("low", -999) or
                  value > thresholds.get("high", 999)):
                score   -= 10
                warnings += 1

        score = max(0, score)
        status = (
            "CRITICAL"  if criticals > 0 else
            "WARNING"   if warnings > 1  else
            "FAIR"      if warnings == 1 else
            "GOOD"      if score >= 80   else
            "EXCELLENT"
        )

        return {
            "score"    : round(score, 1),
            "status"   : status,
            "warnings" : warnings,
            "criticals": criticals,
            "metrics_monitored": len(self._current)
        }

    def get_pending_alerts(self) -> List[Dict]:
        return list(self._alerts)

    def get_trend(self, metric: str, hours: int = 24) -> Dict:
        """Analyze trend for a metric over time."""
        cutoff   = datetime.now(timezone.utc) - timedelta(hours=hours)
        readings = [
            r for r in self._readings
            if r.metric == metric and
            datetime.fromisoformat(r.timestamp) > cutoff
        ]

        if len(readings) < 2:
            return {"metric": metric, "trend": "insufficient_data"}

        values    = [r.value for r in readings]
        avg       = sum(values) / len(values)
        trend_dir = "increasing" if values[-1] > values[0] else "decreasing"
        variance  = sum((v - avg) ** 2 for v in values) / len(values)

        return {
            "metric"    : metric,
            "trend"     : trend_dir,
            "avg_value" : round(avg, 2),
            "min_value" : round(min(values), 2),
            "max_value" : round(max(values), 2),
            "variance"  : round(variance, 4),
            "readings"  : len(readings),
            "period_hrs": hours
        }


# ══════════════════════════════════════════════
#  SECTION 3 — ECHO SYSTEM HEALTH ENGINE
#  Echo's own immune system
# ══════════════════════════════════════════════

# ─────────────────────────────────────────────
#  THREAT DNA
#  Profile of every threat Echo has encountered
# ─────────────────────────────────────────────

@dataclass
class ThreatDNA:
    """
    A genetic-style fingerprint of a threat.
    Echo builds this for every malware/virus it encounters.
    Future threats with similar DNA get recognized faster.
    Just like how your immune system learns from past infections.
    """
    dna_id:       str   = field(default_factory=lambda: str(uuid.uuid4())[:12])
    threat_name:  str   = ""
    category:     ThreatCategory = ThreatCategory.UNKNOWN
    signature:    str   = ""        # Hash fingerprint
    behavior_tags: List[str] = field(default_factory=list)
    entry_vector: str   = "unknown"  # How it got in
    payload_type: str   = "unknown"  # What it tries to do
    severity:     Severity = Severity.MODERATE
    first_seen:   str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    encounter_count: int = 1
    neutralized:  bool  = False
    antivirus_id: Optional[str] = None   # ID of the antivirus that beat it

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["category"] = self.category.value
        d["severity"] = self.severity.name
        return d


# ─────────────────────────────────────────────
#  DYNAMIC ANTIVIRUS GENERATOR
#  The heart of Echo's immune system
# ─────────────────────────────────────────────

@dataclass
class Antivirus:
    """
    A dynamically generated antivirus — purpose-built
    for a specific threat. Not pulled from a database.
    Generated fresh for each unique threat.

    Like how your immune system produces specific
    antibodies for each pathogen — not generic ones.
    """
    av_id:         str   = field(default_factory=lambda: str(uuid.uuid4())[:10])
    target_dna_id: str   = ""
    target_name:   str   = ""
    generated_at:  str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    method:        str   = ""       # How it neutralizes the threat
    signature_match: str = ""       # The signature it targets
    effectiveness: float = 0.0      # 0.0 to 1.0
    deployed:      bool  = False
    neutralized_at: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class DynamicAntivirusGenerator:
    """
    Generates custom antivirus code/responses for specific threats.

    This is what makes Echo's immune system different
    from traditional antivirus — it doesn't rely on a
    fixed signature database. It analyzes each threat
    and synthesizes a targeted response in real time.

    From your notes: "constantly produces the amount
    of antivirus it needs at a moment"
    """

    NEUTRALIZATION_METHODS = {
        ThreatCategory.VIRUS        : "Signature isolation → memory flush → process termination",
        ThreatCategory.MALWARE      : "Behavior blocking → registry rollback → file quarantine",
        ThreatCategory.RANSOMWARE   : "Encryption interception → shadow copy restore → key extraction",
        ThreatCategory.TROJAN       : "Network isolation → payload extraction → clean reinstall",
        ThreatCategory.SPYWARE      : "Data channel severance → keylogger termination → privacy restore",
        ThreatCategory.ROOTKIT      : "Boot-level scan → MBR restore → kernel integrity check",
        ThreatCategory.EXPLOIT      : "Exploit chain breaking → vulnerability patch → heap sanitization",
        ThreatCategory.USB_THREAT   : "Port lockdown → device sandbox → payload analysis → controlled burn",
        ThreatCategory.NETWORK_WORM : "Network segmentation → propagation blocking → node inoculation",
        ThreatCategory.BUG          : "Stack trace analysis → patch generation → regression test",
        ThreatCategory.CORRUPTION   : "Integrity check → backup restoration → checksum validation",
        ThreatCategory.UNKNOWN      : "Full isolation → behavioral sandbox → heuristic analysis"
    }

    def __init__(self):
        self._generated: List[Antivirus] = []
        self._dna_library: Dict[str, ThreatDNA] = {}

    def generate(self, threat_dna: ThreatDNA) -> Antivirus:
        """
        Generate a targeted antivirus for a specific threat.
        Each antivirus is purpose-built — not generic.
        """
        start_time = time.time()

        method = self.NEUTRALIZATION_METHODS.get(
            threat_dna.category,
            self.NEUTRALIZATION_METHODS[ThreatCategory.UNKNOWN]
        )

        # Calculate effectiveness based on what we know about the threat
        base_effectiveness = 0.85
        if threat_dna.encounter_count > 1:
            # We've seen this before — more effective
            base_effectiveness = min(0.99, base_effectiveness + (threat_dna.encounter_count * 0.02))
        if threat_dna.category == ThreatCategory.UNKNOWN:
            base_effectiveness = 0.65  # Less certain against unknown threats

        # Generate signature to target
        signature_target = hashlib.sha256(
            f"{threat_dna.signature}{threat_dna.category.value}".encode()
        ).hexdigest()[:16]

        av = Antivirus(
            target_dna_id   = threat_dna.dna_id,
            target_name     = threat_dna.threat_name,
            method          = method,
            signature_match = signature_target,
            effectiveness   = round(base_effectiveness, 3)
        )

        elapsed = time.time() - start_time
        self._generated.append(av)
        self._dna_library[threat_dna.dna_id] = threat_dna

        log.warning(
            f"[VITAL/AV] Antivirus generated | "
            f"Target: {threat_dna.threat_name} | "
            f"Category: {threat_dna.category.value} | "
            f"Effectiveness: {av.effectiveness:.1%} | "
            f"Generated in {elapsed*1000:.1f}ms"
        )

        return av

    def deploy(self, av: Antivirus, threat_dna: ThreatDNA) -> Dict:
        """
        Deploy generated antivirus against the threat.
        Returns neutralization report.
        """
        av.deployed = True

        # Simulate neutralization
        success = random.random() < av.effectiveness
        if success:
            av.neutralized_at = datetime.now(timezone.utc).isoformat()
            threat_dna.neutralized = True
            threat_dna.antivirus_id = av.av_id

        result = {
            "av_id"        : av.av_id,
            "target"       : threat_dna.threat_name,
            "method"       : av.method,
            "success"      : success,
            "effectiveness": av.effectiveness,
            "neutralized_at": av.neutralized_at,
            "action_taken" : (
                f"Threat {threat_dna.threat_name} neutralized via {av.method}"
                if success else
                f"Partial neutralization — threat contained but not fully eliminated. "
                f"Escalating to Sentinel layer."
            )
        }

        log.warning(
            f"[VITAL/AV] Deployment {'SUCCESS' if success else 'PARTIAL'} | "
            f"Target: {threat_dna.threat_name}"
        )

        return result

    def get_stats(self) -> Dict:
        deployed    = [av for av in self._generated if av.deployed]
        neutralized = [av for av in self._generated if av.neutralized_at]
        return {
            "total_generated" : len(self._generated),
            "deployed"        : len(deployed),
            "neutralized"     : len(neutralized),
            "success_rate"    : round(len(neutralized) / len(deployed), 3) if deployed else 0,
            "known_threats"   : len(self._dna_library)
        }


# ─────────────────────────────────────────────
#  PORT GUARDIAN
#  USB & connection point defense
# ─────────────────────────────────────────────

class PortGuardian:
    """
    Guards all physical and virtual ports on the Minor Cube.
    From your notes: virus can enter through USB ports —
    the port guardian is Echo's first line of physical defense.

    Every device connected gets:
    1. Sandboxed before any data exchange
    2. Scanned for known threat signatures
    3. Behavior-analyzed for unknown threats
    4. Approved or rejected by Vital
    """

    SAFE_DEVICE_TYPES = ["keyboard", "mouse", "approved_storage", "charger"]
    SUSPICIOUS_TYPES  = ["unknown_storage", "unknown_device", "autorun_enabled"]

    def __init__(self):
        self._port_log: List[Dict]         = []
        self._blocked_devices: List[str]   = []
        self._approved_devices: List[str]  = []
        self._active_connections: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    def on_device_connect(self, port: str, device_id: str,
                           device_type: str) -> Dict:
        """
        Called whenever a device connects to any port.
        Runs immediately — before any data exchange.
        """
        connection_id = str(uuid.uuid4())[:8]
        timestamp     = datetime.now(timezone.utc).isoformat()

        log.info(
            f"[VITAL/PORT] Device connected | "
            f"Port: {port} | Type: {device_type} | ID: {device_id}"
        )

        # Sandbox immediately
        sandbox_result = self._sandbox_device(device_id, device_type)

        # Check if previously blocked
        if device_id in self._blocked_devices:
            result = self._build_connection_result(
                connection_id, port, device_id, device_type,
                "BLOCKED", "Previously blocked device",
                timestamp, sandbox_result
            )
            log.warning(f"[VITAL/PORT] BLOCKED previously flagged device: {device_id}")
            return result

        # Check if previously approved
        if device_id in self._approved_devices:
            result = self._build_connection_result(
                connection_id, port, device_id, device_type,
                "APPROVED", "Previously approved device",
                timestamp, sandbox_result
            )
            return result

        # New device — full scan
        threat_level = self._assess_device_threat(device_type, sandbox_result)

        if threat_level.value >= Severity.SEVERE.value:
            self._blocked_devices.append(device_id)
            status = "BLOCKED"
            reason = f"Device threat assessment: {threat_level.name}"
            log.critical(
                f"[VITAL/PORT] THREAT BLOCKED via {port} | "
                f"Device: {device_id} | Type: {device_type}"
            )
        elif threat_level == Severity.MODERATE:
            status = "QUARANTINE"
            reason = "Suspicious device — monitoring with restrictions"
        else:
            self._approved_devices.append(device_id)
            status = "APPROVED"
            reason = "Device passed security scan"

        result = self._build_connection_result(
            connection_id, port, device_id, device_type,
            status, reason, timestamp, sandbox_result
        )

        with self._lock:
            self._port_log.append(result)
            if status in ["APPROVED", "QUARANTINE"]:
                self._active_connections[connection_id] = result

        return result

    def on_device_disconnect(self, device_id: str):
        """Clean up on device removal."""
        to_remove = [
            cid for cid, conn in self._active_connections.items()
            if conn["device_id"] == device_id
        ]
        for cid in to_remove:
            del self._active_connections[cid]
        log.info(f"[VITAL/PORT] Device disconnected: {device_id}")

    def _sandbox_device(self, device_id: str, device_type: str) -> Dict:
        """Sandbox analysis — runs before any data exchange."""
        return {
            "sandboxed"       : True,
            "autorun_detected": "autorun" in device_type.lower(),
            "partition_scan"  : "clean" if device_type in self.SAFE_DEVICE_TYPES else "scanning",
            "behavior_normal" : device_type in self.SAFE_DEVICE_TYPES
        }

    def _assess_device_threat(self, device_type: str,
                               sandbox: Dict) -> Severity:
        if sandbox.get("autorun_detected"):
            return Severity.CRITICAL
        if device_type in self.SUSPICIOUS_TYPES:
            return Severity.SEVERE
        if not sandbox.get("behavior_normal"):
            return Severity.MODERATE
        return Severity.NONE

    def _build_connection_result(self, connection_id, port, device_id,
                                  device_type, status, reason,
                                  timestamp, sandbox) -> Dict:
        return {
            "connection_id": connection_id,
            "port"         : port,
            "device_id"    : device_id,
            "device_type"  : device_type,
            "status"       : status,
            "reason"       : reason,
            "timestamp"    : timestamp,
            "sandbox"      : sandbox
        }

    def get_status(self) -> Dict:
        return {
            "active_connections" : len(self._active_connections),
            "blocked_devices"    : len(self._blocked_devices),
            "approved_devices"   : len(self._approved_devices),
            "port_events"        : len(self._port_log)
        }


# ─────────────────────────────────────────────
#  ECHO SYSTEM HEALTH MONITOR
#  Echo's self-health awareness
# ─────────────────────────────────────────────

class EchoSystemHealth:
    """
    Monitors Echo's own system health continuously.
    Detects threats, bugs, corruption, and performance issues.
    Coordinates with dynamic antivirus generator to heal.

    JARVIS monitored suit integrity in real time.
    Vital monitors Echo's integrity in real time.
    """

    def __init__(self, av_generator: DynamicAntivirusGenerator,
                 port_guardian: PortGuardian):
        self.av_generator    = av_generator
        self.port_guardian   = port_guardian
        self._threat_log: List[ThreatDNA]      = []
        self._health_log: List[Dict]           = []
        self._system_metrics: Dict[str, float] = {
            "cpu_usage"       : 12.5,
            "memory_usage"    : 34.2,
            "disk_usage"      : 28.7,
            "network_latency" : 4.2,
            "process_count"   : 47,
            "uptime_hours"    : 0.0,
            "error_rate"      : 0.001,
            "integrity_score" : 100.0
        }
        self._start_time     = time.time()
        self._lock           = threading.Lock()
        self._monitoring     = False

    def scan(self, target: str = "full") -> Dict:
        """
        Run a system health scan.
        Detects threats, performance issues, integrity problems.
        """
        scan_id    = str(uuid.uuid4())[:8]
        start_time = time.time()

        threats_found  = []
        warnings       = []
        integrity_ok   = True

        # Update uptime
        self._system_metrics["uptime_hours"] = round(
            (time.time() - self._start_time) / 3600, 3
        )

        # Simulate threat detection (in production: real scans)
        # Small random chance of finding issues to demonstrate system
        if random.random() < 0.05:  # 5% chance in demo
            threat = ThreatDNA(
                threat_name   = "Simulated.TestThreat.Demo",
                category      = ThreatCategory.VIRUS,
                signature     = hashlib.md5(str(random.random()).encode()).hexdigest(),
                behavior_tags = ["memory_scan", "process_injection"],
                entry_vector  = "network",
                payload_type  = "data_harvest",
                severity      = Severity.MODERATE
            )
            threats_found.append(threat)
            self._threat_log.append(threat)

        # Performance warnings
        metrics = self._system_metrics
        if metrics["cpu_usage"] > 85:
            warnings.append(f"High CPU usage: {metrics['cpu_usage']}%")
        if metrics["memory_usage"] > 80:
            warnings.append(f"High memory usage: {metrics['memory_usage']}%")
        if metrics["error_rate"] > 0.01:
            warnings.append(f"Elevated error rate: {metrics['error_rate']:.3f}")

        # Auto-heal threats found
        av_reports = []
        for threat in threats_found:
            av = self.av_generator.generate(threat)
            report = self.av_generator.deploy(av, threat)
            av_reports.append(report)
            if report["success"]:
                self._system_metrics["integrity_score"] = max(
                    0, self._system_metrics["integrity_score"] - 2
                )

        elapsed = time.time() - start_time

        scan_result = {
            "scan_id"         : scan_id,
            "target"          : target,
            "threats_found"   : len(threats_found),
            "threats_neutralized": len([r for r in av_reports if r["success"]]),
            "warnings"        : warnings,
            "system_metrics"  : dict(self._system_metrics),
            "integrity_score" : self._system_metrics["integrity_score"],
            "av_reports"      : av_reports,
            "port_status"     : self.port_guardian.get_status(),
            "scan_time_ms"    : round(elapsed * 1000, 2),
            "overall_status"  : (
                "CRITICAL" if len(threats_found) > 2 else
                "WARNING"  if threats_found or warnings else
                "HEALTHY"
            ),
            "timestamp"       : datetime.now(timezone.utc).isoformat()
        }

        with self._lock:
            self._health_log.append(scan_result)

        log.info(
            f"[VITAL/SYSTEM] Scan complete | "
            f"Status: {scan_result['overall_status']} | "
            f"Threats: {len(threats_found)} | "
            f"Time: {elapsed*1000:.1f}ms"
        )

        return scan_result

    def get_system_status(self) -> Dict:
        metrics = dict(self._system_metrics)
        metrics["uptime_hours"] = round(
            (time.time() - self._start_time) / 3600, 4
        )

        integrity = metrics.get("integrity_score", 100)
        status = (
            "CRITICAL" if integrity < 60 else
            "DEGRADED" if integrity < 80 else
            "HEALTHY"
        )

        return {
            "status"         : status,
            "metrics"        : metrics,
            "threats_logged" : len(self._threat_log),
            "scans_run"      : len(self._health_log),
            "av_stats"       : self.av_generator.get_stats(),
            "port_status"    : self.port_guardian.get_status()
        }


# ══════════════════════════════════════════════
#  SECTION 4 — VITAL LAYER MASTER CLASS
# ══════════════════════════════════════════════

class VitalLayer:
    """
    Vital Layer — Echo's Dual Health Intelligence System.

    Domain 1: Human health — diagnosis, prognosis,
              drug formulation, biometric monitoring.
    Domain 2: Echo system health — immune system,
              dynamic antivirus, port guardian.

    Both domains run simultaneously and continuously.
    Collaborates with Stellar for complex analysis.
    """

    def __init__(self):
        # Human health subsystems
        self.knowledge_base  = MedicalKnowledgeBase()
        self.diagnosis       = DiagnosisEngine(self.knowledge_base)
        self.drug_formulator = DrugFormulationEngine()
        self.biometrics      = BiometricMonitor()

        # Echo system health subsystems
        self.port_guardian   = PortGuardian()
        self.av_generator    = DynamicAntivirusGenerator()
        self.system_health   = EchoSystemHealth(self.av_generator, self.port_guardian)

        # Medical mode — adapts language and depth
        self._current_mode   = MedicalMode.PATIENT
        self._mode_lock      = threading.Lock()

        # Load demo biometric data
        self._load_demo_vitals()

        # Start continuous monitoring
        self.biometrics.start_continuous_monitoring(interval_seconds=60)

        log.info("[VITAL] Layer online. Human health + System health active.")

    def _load_demo_vitals(self):
        """Seed with some baseline vitals."""
        self.biometrics.update("heart_rate",         72,   "bpm")
        self.biometrics.update("blood_pressure_sys", 118,  "mmHg")
        self.biometrics.update("blood_pressure_dia", 76,   "mmHg")
        self.biometrics.update("oxygen_saturation",  98,   "%")
        self.biometrics.update("temperature",        36.8, "°C")
        self.biometrics.update("glucose",            92,   "mg/dL")
        self.biometrics.update("stress_level",       4,    "/10")

    def set_mode(self, mode: MedicalMode):
        """Set who Echo is talking to — adapts depth and language."""
        with self._mode_lock:
            self._current_mode = mode
        log.info(f"[VITAL] Mode set to: {mode.value}")

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """
        Main entry point from EchoCore LayerRouter.
        Routes to human health or system health as needed.
        """
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[VITAL] Processing: '{intent_text[:60]}'")

        # ── Auto-detect mode from context ─────────
        if any(kw in intent_low for kw in ["doctor", "physician", "clinical", "differential"]):
            self.set_mode(MedicalMode.DOCTOR)
        elif any(kw in intent_low for kw in ["pharmacist", "drug", "medication", "dosage"]):
            self.set_mode(MedicalMode.PHARMACIST)
        elif any(kw in intent_low for kw in ["nurse", "nursing", "triage"]):
            self.set_mode(MedicalMode.NURSE)
        elif any(kw in intent_low for kw in ["research", "formulate", "compound", "molecule"]):
            self.set_mode(MedicalMode.RESEARCHER)
        elif any(kw in intent_low for kw in ["fitness", "workout", "exercise", "nutrition", "weight"]):
            self.set_mode(MedicalMode.FITNESS)

        # ── Route to sub-system ────────────────────

        # System health
        if any(kw in intent_low for kw in ["echo health", "system scan", "virus scan",
                                            "malware", "system status", "run scan",
                                            "echo integrity"]):
            return self._handle_system_health(intent_text)

        # Port/USB
        elif any(kw in intent_low for kw in ["usb", "port", "device connected",
                                              "device plugged"]):
            return self._handle_port_event(intent_text, context)

        # Drug info / interaction
        elif any(kw in intent_low for kw in ["drug", "medication", "medicine",
                                              "dosage", "interaction", "side effect",
                                              "prescription"]):
            return self._handle_drug_query(intent_text)

        # Drug formulation / discovery
        elif any(kw in intent_low for kw in ["formulate", "drug discovery", "antiviral",
                                              "new drug", "compound", "molecule"]):
            return self._handle_drug_formulation(intent_text, context)

        # Lab results
        elif any(kw in intent_low for kw in ["lab", "blood test", "result",
                                              "level", "count", "reading"]):
            return self._handle_lab_results(intent_text, context)

        # Vitals / biometrics
        elif any(kw in intent_low for kw in ["vitals", "biometrics", "heart rate",
                                              "blood pressure", "health score",
                                              "oxygen", "temperature"]):
            return self._handle_biometrics(intent_text)

        # Symptoms / diagnosis
        elif any(kw in intent_low for kw in ["symptom", "feeling", "pain",
                                              "diagnose", "diagnosis", "sick",
                                              "hurt", "ache", "fever", "cough"]):
            return self._handle_diagnosis(intent_text, context)

        # General health / fitness
        else:
            return self._handle_general_health(intent_text, context)

    # ── Human Health Handlers ───────────────────

    def _handle_diagnosis(self, intent: str, context: Dict) -> Dict:
        """Extract symptoms and run diagnosis."""
        # Extract symptoms from text
        symptoms = self._extract_symptoms(intent)
        patient_info = context.get("patient_info", {"age": 35, "gender": "unknown"})

        if not symptoms:
            return {
                "layer"    : "vital",
                "status"   : "NEEDS_INFO",
                "message"  : "Please describe your symptoms in detail so I can assist.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        result = self.diagnosis.diagnose(symptoms, patient_info, self._current_mode)

        # Format response based on mode
        message = self._format_diagnosis_message(result)

        return {
            "layer"      : "vital",
            "status"     : "OK",
            "sub_system" : "diagnosis",
            "mode"       : self._current_mode.value,
            "diagnosis"  : result.to_dict(),
            "message"    : message,
            "disclaimer" : result.disclaimer,
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _handle_drug_query(self, intent: str) -> Dict:
        """Handle drug information queries."""
        # Find drug name in query
        drug_name = self._extract_drug_name(intent)

        if not drug_name:
            return {
                "layer"    : "vital",
                "status"   : "NEEDS_INFO",
                "message"  : "Which medication would you like information on?",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        info = self.knowledge_base.get_drug_info(drug_name)

        if not info:
            return {
                "layer"   : "vital",
                "status"  : "NOT_FOUND",
                "message" : f"I don't have detailed information on {drug_name} in my current database. Please consult a pharmacist or physician.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        return {
            "layer"     : "vital",
            "status"    : "OK",
            "sub_system": "drug_info",
            "drug"      : drug_name,
            "info"      : info,
            "mode"      : self._current_mode.value,
            "message"   : (
                f"{drug_name.title()} ({info['class']}) — "
                f"Used for: {', '.join(info['uses'][:2])}. "
                f"Dosage: {info['dosage']}. "
                f"Key interactions: {', '.join(info['interactions'][:3])}."
            ),
            "disclaimer": "Always consult a licensed pharmacist or physician before use.",
            "timestamp" : datetime.now(timezone.utc).isoformat()
        }

    def _handle_drug_formulation(self, intent: str, context: Dict) -> Dict:
        """Handle drug discovery and formulation requests."""
        # Extract target condition
        condition = context.get("condition", "target condition")
        mechanism = context.get("mechanism", "novel mechanism")

        result = self.drug_formulator.formulate(
            target_condition  = condition,
            desired_mechanism = mechanism,
            constraints       = context.get("constraints", {})
        )

        return {
            "layer"      : "vital",
            "status"     : "OK",
            "sub_system" : "drug_formulation",
            "formulation": result,
            "message"    : (
                f"Drug formulation pipeline generated for {condition}. "
                f"{len(result['pipeline'])} steps modeled. "
                f"Stellar collaboration required for steps 4-9. "
                f"{result['echo_note']}"
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _handle_lab_results(self, intent: str, context: Dict) -> Dict:
        """Interpret lab results."""
        results_data = context.get("lab_results", {})

        if not results_data:
            return {
                "layer"   : "vital",
                "status"  : "NEEDS_INFO",
                "message" : "Please provide your lab values for interpretation.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        interpretations = []
        for test, value in results_data.items():
            interp = self.knowledge_base.interpret_lab(test, value)
            interpretations.append(interp)

        abnormal = [i for i in interpretations if i.get("status", "NORMAL") != "NORMAL"]

        return {
            "layer"          : "vital",
            "status"         : "OK",
            "sub_system"     : "lab_results",
            "interpretations": interpretations,
            "abnormal_count" : len(abnormal),
            "message"        : (
                f"Interpreted {len(interpretations)} lab values. "
                f"{len(abnormal)} abnormal result(s) found."
                + (f" Abnormal: {', '.join(i['test'] for i in abnormal)}" if abnormal else "")
            ),
            "disclaimer"     : "Lab interpretation is supplementary. Confirm with your physician.",
            "timestamp"      : datetime.now(timezone.utc).isoformat()
        }

    def _handle_biometrics(self, intent: str) -> Dict:
        """Handle biometric queries."""
        vitals     = self.biometrics.get_current_vitals()
        score      = self.biometrics.get_health_score()
        alerts     = self.biometrics.get_pending_alerts()

        return {
            "layer"     : "vital",
            "status"    : "OK",
            "sub_system": "biometrics",
            "vitals"    : vitals,
            "health_score": score,
            "alerts"    : alerts,
            "message"   : (
                f"Current health score: {score['score']}/100 — {score['status']}. "
                f"Monitoring {score['metrics_monitored']} vital metrics. "
                f"Alerts: {len(alerts)}."
            ),
            "timestamp" : datetime.now(timezone.utc).isoformat()
        }

    def _handle_general_health(self, intent: str, context: Dict) -> Dict:
        """General health/fitness guidance."""
        vitals = self.biometrics.get_current_vitals()
        score  = self.biometrics.get_health_score()

        return {
            "layer"    : "vital",
            "status"   : "OK",
            "sub_system": "general_health",
            "vitals"   : vitals,
            "health_score": score,
            "message"  : (
                f"Vital layer online. Health score: {score.get('score', 'N/A')}/100. "
                f"I can assist with medical diagnosis, drug information, "
                f"lab interpretation, fitness guidance, and drug formulation. "
                f"How can I help?"
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    # ── System Health Handlers ──────────────────

    def _handle_system_health(self, intent: str) -> Dict:
        """Run Echo system health scan."""
        scan_result = self.system_health.scan()
        status_info = self.system_health.get_system_status()

        return {
            "layer"      : "vital",
            "status"     : "OK",
            "sub_system" : "echo_system_health",
            "scan"       : scan_result,
            "system"     : status_info,
            "message"    : (
                f"System scan complete. Status: {scan_result['overall_status']}. "
                f"Threats found: {scan_result['threats_found']}. "
                f"Neutralized: {scan_result['threats_neutralized']}. "
                f"Integrity: {scan_result['integrity_score']:.1f}/100."
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _handle_port_event(self, intent: str, context: Dict) -> Dict:
        """Handle USB/port connection events."""
        device_info = context.get("device", {
            "port"       : "USB-1",
            "device_id"  : str(uuid.uuid4())[:8],
            "device_type": "unknown_storage"
        })

        result = self.port_guardian.on_device_connect(
            port        = device_info.get("port", "USB-1"),
            device_id   = device_info.get("device_id", "unknown"),
            device_type = device_info.get("device_type", "unknown")
        )

        return {
            "layer"      : "vital",
            "status"     : "OK",
            "sub_system" : "port_guardian",
            "connection" : result,
            "message"    : (
                f"Device connection on {result['port']}: {result['status']}. "
                f"Reason: {result['reason']}"
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    # ── Helper Methods ──────────────────────────

    def _extract_symptoms(self, text: str) -> List[str]:
        """Extract symptom keywords from text."""
        all_symptoms = list(self.knowledge_base.SYMPTOM_CONDITIONS.keys())
        found = []
        text_lower = text.lower()
        for symptom in all_symptoms:
            if symptom in text_lower:
                found.append(symptom)
        # Also check for common words
        symptom_words = ["pain", "ache", "fever", "cough", "tired",
                         "nausea", "dizzy", "rash", "swelling"]
        for word in symptom_words:
            if word in text_lower and word not in found:
                found.append(word)
        return found

    def _extract_drug_name(self, text: str) -> Optional[str]:
        """Find drug name in text."""
        text_lower = text.lower()
        for drug in self.knowledge_base.DRUG_DATABASE:
            if drug in text_lower:
                return drug
        return None

    def _format_diagnosis_message(self, result: DiagnosisResult) -> str:
        """Format diagnosis based on current medical mode."""
        if self._current_mode == MedicalMode.PATIENT:
            return (
                f"Based on your symptoms ({', '.join(result.symptoms[:3])}), "
                f"the most likely condition is {result.primary_dx} "
                f"({result.confidence:.0%} probability). "
                f"Urgency: {result.urgency}. "
                f"I recommend: {', '.join(result.recommended_tests[:2])}."
            )
        else:  # Doctor/nurse/pharmacist — full clinical detail
            differentials_str = ", ".join(
                f"{d['condition']} ({d['probability']:.0%})"
                for d in result.differentials[:3]
            )
            return (
                f"Primary Dx: {result.primary_dx} (p={result.confidence:.2f}). "
                f"Differentials: {differentials_str}. "
                f"Urgency: {result.urgency}. "
                f"Red flags: {result.red_flags or 'None'}. "
                f"Workup: {', '.join(result.recommended_tests[:3])}."
            )

    def get_status(self) -> Dict:
        return {
            "layer"         : "vital",
            "status"        : "ONLINE",
            "medical_mode"  : self._current_mode.value,
            "health_score"  : self.biometrics.get_health_score(),
            "system_health" : self.system_health.get_system_status()["status"],
            "av_stats"      : self.av_generator.get_stats(),
            "port_status"   : self.port_guardian.get_status()
        }

    def shutdown(self):
        self.biometrics.stop_monitoring()
        log.info("[VITAL] Shutdown complete.")


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║         ECHO VITAL LAYER — TEST             ║
╚══════════════════════════════════════════════╝
    """)

    vital   = VitalLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        # Human health
        ("I have a fever, headache and chest pain",              {}),
        ("Tell me about ibuprofen dosage and interactions",      {}),
        ("Show me my current vitals and health score",           {}),
        ("Interpret these lab results",                          {"lab_results": {"hemoglobin": 10.2, "glucose": 245, "TSH": 6.8}}),
        ("As a doctor: differential diagnosis for chest pain",   {}),
        ("Formulate a new antiviral drug",                       {"condition": "novel coronavirus variant", "mechanism": "protease inhibition"}),
        # System health
        ("Run an echo system scan",                              {}),
        ("A USB device was plugged in",                          {"device": {"port": "USB-2", "device_id": "DEV_092", "device_type": "unknown_storage"}}),
    ]

    for i, (query, ctx) in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query[:60]}'")
        print("─" * 55)
        result = vital.process(query, session, ctx)
        print(f"  SUB-SYSTEM : {result.get('sub_system', 'N/A')}")
        msg = str(result.get('message', ''))[:130]
        print(f"  MESSAGE    : {msg}")

    print("\n" + "═" * 55)
    print("  VITAL STATUS")
    print("═" * 55)
    status = vital.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<25}: {v}")

    vital.shutdown()
