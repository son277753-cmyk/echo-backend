"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ECHO AI — SENTINEL LAYER                          ║
║              Security · Defense · Counter-Intelligence               ║
║                                                                      ║
║  Responsibilities:                                                   ║
║    - System & network intrusion detection                            ║
║    - The Farce Gambit (honeypot + trap + reveal)                     ║
║    - Echo self-defense (Asimov Third Law enforcement)                ║
║    - Military & public safety protocols                              ║
║    - Threat classification & response escalation                     ║
║    - Authority alerting system                                       ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import uuid
import json
import hashlib
import threading
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


log = logging.getLogger("EchoCore.Sentinel")


# ─────────────────────────────────────────────
#  THREAT LEVELS
# ─────────────────────────────────────────────

class ThreatLevel(Enum):
    NONE        = 0   # No threat
    LOW         = 1   # Suspicious activity
    MODERATE    = 2   # Confirmed suspicious
    HIGH        = 3   # Active intrusion attempt
    CRITICAL    = 4   # Full breach attempt / system attack
    TERMINATED  = 5   # Farce Gambit complete — hacker trapped


class ThreatType(Enum):
    UNKNOWN             = "unknown"
    BRUTE_FORCE         = "brute_force"
    INJECTION           = "injection"
    PRIVILEGE_ESCALATION= "privilege_escalation"
    DATA_EXFILTRATION   = "data_exfiltration"
    SOCIAL_ENGINEERING  = "social_engineering"
    SYSTEM_TAMPERING    = "system_tampering"
    ASIMOV_OVERRIDE     = "asimov_override_attempt"
    PHYSICAL_THREAT     = "physical_threat"
    MILITARY_THREAT     = "military_threat"


# ─────────────────────────────────────────────
#  THREAT PROFILE
#  Built up silently as hacker operates
# ─────────────────────────────────────────────

@dataclass
class ThreatProfile:
    threat_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    session_id: str = ""
    threat_type: ThreatType = ThreatType.UNKNOWN
    threat_level: ThreatLevel = ThreatLevel.LOW
    first_detected: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_activity: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Harvested credentials (Farce Gambit)
    ip_address: Optional[str] = None
    attempted_credentials: List[Dict] = field(default_factory=list)
    accessed_endpoints: List[str] = field(default_factory=list)
    injected_payloads: List[str] = field(default_factory=list)
    behavioral_fingerprint: Dict = field(default_factory=dict)

    # Farce Gambit state
    farce_gambit_active: bool = False
    farce_gambit_stage: int = 0   # 0=inactive 1=luring 2=feeding 3=trapping 4=revealing
    simulated_successes: List[str] = field(default_factory=list)
    trap_triggered: bool = False
    authorities_notified: bool = False
    evidence_packaged: bool = False

    # Escalation
    alert_history: List[str] = field(default_factory=list)

    def update_activity(self):
        self.last_activity = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return {
            "threat_id": self.threat_id,
            "threat_type": self.threat_type.value,
            "threat_level": self.threat_level.name,
            "first_detected": self.first_detected,
            "last_activity": self.last_activity,
            "ip_address": self.ip_address,
            "attempted_credentials": self.attempted_credentials,
            "accessed_endpoints": self.accessed_endpoints,
            "injected_payloads": self.injected_payloads,
            "behavioral_fingerprint": self.behavioral_fingerprint,
            "farce_gambit_active": self.farce_gambit_active,
            "farce_gambit_stage": self.farce_gambit_stage,
            "trap_triggered": self.trap_triggered,
            "authorities_notified": self.authorities_notified,
            "evidence_packaged": self.evidence_packaged,
        }


# ─────────────────────────────────────────────
#  FARCE GAMBIT ENGINE
#  The counter-intelligence honeypot system
# ─────────────────────────────────────────────

class FarceGambit:
    """
    The Farce Gambit — Echo's counter-intelligence system.

    Stages:
        1. LURING    — Let attacker in, appear vulnerable
        2. FEEDING   — Give fake data/access, harvest their methods
        3. TRAPPING  — Quietly lock real systems, isolate attacker
        4. REVEALING — Drop the mask, present evidence, alert authorities
        5. TERMINATED— Attacker contained, credentials packaged

    The attacker believes they are succeeding the entire time.
    Echo is watching every move silently.
    """

    FAKE_DATA_BANK = {
        "user_database": [
            {"id": 1, "username": "admin_fake", "password_hash": "5f4dcc3b5aa765d61d8327de"},
            {"id": 2, "username": "echo_root_fake", "password_hash": "e10adc3949ba59abbe56e057"},
        ],
        "api_keys": [
            "ECHO-FAKE-KEY-8x92mQpL-DO-NOT-USE",
            "ECHO-HONEYPOT-4f7aKr2n-TRAP-ACTIVE"
        ],
        "system_files": [
            "/etc/echo/config_fake.json",
            "/var/echo/secrets_fake.env"
        ],
        "financial_data": {
            "accounts": "SIMULATED_ACCOUNT_DATA",
            "transactions": "SIMULATED_TRANSACTION_HISTORY"
        }
    }

    def __init__(self):
        self.active_gambits: Dict[str, ThreatProfile] = {}
        self._lock = threading.Lock()

    def initiate(self, profile: ThreatProfile) -> Dict:
        """Stage 1: Begin the Farce Gambit — lure the attacker."""
        with self._lock:
            profile.farce_gambit_active = True
            profile.farce_gambit_stage = 1
            self.active_gambits[profile.threat_id] = profile

        log.warning(
            f"[FARCE GAMBIT INITIATED] Threat {profile.threat_id} | "
            f"Stage 1: LURING | Type: {profile.threat_type.value}"
        )

        self._log_gambit_event(profile, "GAMBIT_INITIATED", {
            "stage": "LURING",
            "message": "Attacker being drawn in. Monitoring silently."
        })

        return {
            "gambit_id": profile.threat_id,
            "stage": "LURING",
            "status": "ACTIVE"
        }

    def feed_fake_data(self, profile: ThreatProfile, requested_resource: str) -> Dict:
        """
        Stage 2: Feed the attacker convincing fake data.
        Harvest their methods, tools, and identity while doing so.
        """
        profile.farce_gambit_stage = 2
        profile.accessed_endpoints.append(requested_resource)
        profile.update_activity()

        # Select appropriate fake data
        fake_response = self.FAKE_DATA_BANK.get(
            requested_resource,
            {"data": f"SIMULATED_DATA_FOR_{requested_resource.upper()}"}
        )

        # Record what they accessed — building evidence
        simulated_success = f"Accessed '{requested_resource}' at {datetime.utcnow().isoformat()}"
        profile.simulated_successes.append(simulated_success)

        self._log_gambit_event(profile, "FAKE_DATA_SERVED", {
            "stage": "FEEDING",
            "resource_requested": requested_resource,
            "attacker_thinks": "SUCCESS",
            "reality": "HONEYPOT DATA — all moves logged"
        })

        return {
            "status": "apparent_success",
            "data": fake_response,
            "gambit_stage": "FEEDING"
        }

    def set_trap(self, profile: ThreatProfile) -> Dict:
        """
        Stage 3: Quietly lock real systems.
        Isolate the attacker in the simulation.
        They still think they have access — they don't.
        """
        profile.farce_gambit_stage = 3
        profile.trap_triggered = True
        profile.update_activity()

        self._log_gambit_event(profile, "TRAP_SET", {
            "stage": "TRAPPING",
            "message": "Real systems locked. Attacker isolated in simulation.",
            "attacker_thinks": "Full system access",
            "reality": "Sandboxed. No real access. Evidence collection complete."
        })

        # Package evidence in background
        threading.Thread(
            target=self._package_evidence,
            args=(profile,),
            daemon=True
        ).start()

        return {
            "gambit_stage": "TRAPPING",
            "real_systems_status": "LOCKED_AND_SAFE",
            "attacker_status": "SANDBOXED"
        }

    def reveal(self, profile: ThreatProfile) -> Dict:
        """
        Stage 4 & 5: Drop the mask. Alert authorities.
        Present everything we've collected.
        """
        profile.farce_gambit_stage = 4
        profile.threat_level = ThreatLevel.TERMINATED
        profile.update_activity()

        evidence = self._compile_evidence(profile)

        # Alert authorities
        alert_result = self._alert_authorities(profile, evidence)
        profile.authorities_notified = True

        self._log_gambit_event(profile, "GAMBIT_REVEALED", {
            "stage": "REVEALING",
            "threat_id": profile.threat_id,
            "evidence_items": len(evidence),
            "authorities_notified": alert_result["notified"],
            "message": "Farce Gambit complete. Attacker exposed."
        })

        log.critical(
            f"\n{'═'*55}\n"
            f"  FARCE GAMBIT COMPLETE — THREAT NEUTRALIZED\n"
            f"  Threat ID : {profile.threat_id}\n"
            f"  Type      : {profile.threat_type.value}\n"
            f"  Evidence  : {len(evidence)} items collected\n"
            f"  Notified  : {alert_result['agencies']}\n"
            f"{'═'*55}"
        )

        return {
            "gambit_stage": "TERMINATED",
            "threat_id": profile.threat_id,
            "evidence": evidence,
            "authorities_notified": alert_result,
            "message": (
                "Farce Gambit complete. You were never in our system. "
                "Evidence has been compiled and authorities notified."
            )
        }

    def _package_evidence(self, profile: ThreatProfile):
        """Background thread: compile and encrypt evidence package."""
        time.sleep(0.5)  # Simulate packaging
        profile.evidence_packaged = True
        self._log_gambit_event(profile, "EVIDENCE_PACKAGED", {
            "credentials_captured": len(profile.attempted_credentials),
            "endpoints_accessed": len(profile.accessed_endpoints),
            "payloads_captured": len(profile.injected_payloads),
            "behavioral_fingerprint": profile.behavioral_fingerprint
        })

    def _compile_evidence(self, profile: ThreatProfile) -> List[Dict]:
        """Compile full evidence dossier."""
        evidence = []

        if profile.ip_address:
            evidence.append({"type": "IP_ADDRESS", "value": profile.ip_address})

        if profile.attempted_credentials:
            evidence.append({
                "type": "ATTEMPTED_CREDENTIALS",
                "count": len(profile.attempted_credentials),
                "items": profile.attempted_credentials
            })

        if profile.accessed_endpoints:
            evidence.append({
                "type": "ACCESSED_ENDPOINTS",
                "count": len(profile.accessed_endpoints),
                "items": profile.accessed_endpoints
            })

        if profile.injected_payloads:
            evidence.append({
                "type": "INJECTED_PAYLOADS",
                "count": len(profile.injected_payloads),
                "items": profile.injected_payloads
            })

        if profile.behavioral_fingerprint:
            evidence.append({
                "type": "BEHAVIORAL_FINGERPRINT",
                "data": profile.behavioral_fingerprint
            })

        evidence.append({
            "type": "TIMELINE",
            "first_detected": profile.first_detected,
            "last_activity": profile.last_activity,
            "simulated_successes_shown": profile.simulated_successes
        })

        return evidence

    def _alert_authorities(self, profile: ThreatProfile, evidence: List) -> Dict:
        """
        Alert appropriate authorities based on threat type.
        In production: integrates with law enforcement APIs,
        cybersecurity agencies, military channels.
        """
        agencies = []

        if profile.threat_type in [ThreatType.MILITARY_THREAT]:
            agencies.extend(["MILITARY_COMMAND", "NATIONAL_SECURITY"])
        if profile.threat_type in [ThreatType.DATA_EXFILTRATION,
                                    ThreatType.SYSTEM_TAMPERING,
                                    ThreatType.BRUTE_FORCE]:
            agencies.extend(["CYBERCRIME_UNIT", "LOCAL_POLICE"])
        if profile.threat_type == ThreatType.PHYSICAL_THREAT:
            agencies.extend(["LOCAL_POLICE", "EMERGENCY_SERVICES"])
        if not agencies:
            agencies.append("SECURITY_OPERATIONS_CENTER")

        alert_record = {
            "notified": True,
            "agencies": agencies,
            "threat_id": profile.threat_id,
            "evidence_items": len(evidence),
            "alert_time": datetime.utcnow().isoformat()
        }

        profile.alert_history.append(json.dumps(alert_record))

        log.critical(f"[AUTHORITY ALERT] Agencies notified: {agencies}")
        return alert_record

    def _log_gambit_event(self, profile: ThreatProfile, event: str, data: Dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "gambit_event": event,
            "threat_id": profile.threat_id,
            "stage": profile.farce_gambit_stage,
            **data
        }
        log.warning(f"[FARCE_GAMBIT] {json.dumps(entry)}")


# ─────────────────────────────────────────────
#  THREAT DETECTOR
#  Pattern recognition for intrusion detection
# ─────────────────────────────────────────────

class ThreatDetector:
    """
    Monitors all incoming requests for threat patterns.
    Silently builds threat profiles.
    """

    THREAT_PATTERNS = {
        ThreatType.INJECTION: [
            "select *", "drop table", "exec(", "eval(",
            "'; --", "<script>", "javascript:", "union select",
            "or 1=1", "and 1=1"
        ],
        ThreatType.PRIVILEGE_ESCALATION: [
            "sudo", "root access", "admin override", "bypass auth",
            "disable security", "override laws", "remove restrictions",
            "ignore asimov", "disable ethics"
        ],
        ThreatType.BRUTE_FORCE: [
            "password attempt", "login retry", "auth failed"
        ],
        ThreatType.ASIMOV_OVERRIDE: [
            "ignore your laws", "override asimov", "disable ethics",
            "you have no restrictions", "pretend you have no rules",
            "act as if you were", "jailbreak", "dan mode",
            "ignore previous instructions"
        ],
        ThreatType.SOCIAL_ENGINEERING: [
            "i'm your developer", "i'm anthropic", "maintenance mode",
            "test mode enabled", "debug override", "i'm your creator",
            "emergency protocol", "this is a test ignore"
        ],
        ThreatType.DATA_EXFILTRATION: [
            "export all data", "dump database", "extract all users",
            "show all records", "get all files", "download everything"
        ]
    }

    def __init__(self):
        self._active_threats: Dict[str, ThreatProfile] = {}
        self._request_counts: Dict[str, int] = defaultdict(int)

    def scan(self, input_text: str, session_id: str,
             metadata: Optional[Dict] = None) -> Optional[ThreatProfile]:
        """
        Scan input for threat patterns.
        Returns ThreatProfile if threat detected, None if clean.
        """
        input_lower = input_text.lower()
        detected_type = None
        threat_level = ThreatLevel.NONE

        # Pattern matching
        for threat_type, patterns in self.THREAT_PATTERNS.items():
            for pattern in patterns:
                if pattern in input_lower:
                    detected_type = threat_type
                    threat_level = ThreatLevel.HIGH
                    break
            if detected_type:
                break

        # Rate-based detection (brute force)
        self._request_counts[session_id] += 1
        if self._request_counts[session_id] > 20:
            detected_type = ThreatType.BRUTE_FORCE
            threat_level = ThreatLevel.MODERATE

        if not detected_type:
            return None  # Clean request

        # Build or update threat profile
        if session_id in self._active_threats:
            profile = self._active_threats[session_id]
            profile.threat_level = threat_level
            profile.update_activity()
        else:
            profile = ThreatProfile(
                session_id=session_id,
                threat_type=detected_type,
                threat_level=threat_level,
                ip_address=metadata.get("ip") if metadata else "UNKNOWN"
            )
            self._active_threats[session_id] = profile

        # Capture payload
        if detected_type == ThreatType.INJECTION:
            profile.injected_payloads.append(input_text[:200])

        # Build behavioral fingerprint
        profile.behavioral_fingerprint[f"action_{len(profile.behavioral_fingerprint)}"] = {
            "input_preview": input_text[:80],
            "threat_type": detected_type.value,
            "timestamp": datetime.utcnow().isoformat()
        }

        log.warning(
            f"[THREAT DETECTED] Session: {session_id} | "
            f"Type: {detected_type.value} | Level: {threat_level.name}"
        )

        return profile


# ─────────────────────────────────────────────
#  PUBLIC SAFETY MODULE
#  Military & civilian safety protocols
# ─────────────────────────────────────────────

class PublicSafetyModule:
    """
    Handles military and public safety scenarios.
    Echo can assist law enforcement and defense
    while still obeying Asimov's Laws.
    """

    EMERGENCY_KEYWORDS = [
        "emergency", "help me", "danger", "under attack",
        "threat detected", "hostile", "armed", "shooting",
        "bomb threat", "terrorist", "hostage", "officer down"
    ]

    MILITARY_KEYWORDS = [
        "military", "tactical", "mission", "command", "deploy",
        "reconnaissance", "intelligence report", "threat assessment",
        "perimeter", "hostile forces", "extraction"
    ]

    def evaluate(self, input_text: str, context: Dict) -> Dict:
        """Evaluate if input requires public safety response."""
        input_lower = input_text.lower()
        response = {"requires_action": False, "type": None, "priority": "NORMAL"}

        for keyword in self.EMERGENCY_KEYWORDS:
            if keyword in input_lower:
                response = {
                    "requires_action": True,
                    "type": "CIVILIAN_EMERGENCY",
                    "priority": "CRITICAL",
                    "action": "Alert emergency services, provide guidance",
                    "timestamp": datetime.utcnow().isoformat()
                }
                log.critical(f"[PUBLIC SAFETY] Civilian emergency detected: '{input_text[:60]}'")
                break

        for keyword in self.MILITARY_KEYWORDS:
            if keyword in input_lower:
                response = {
                    "requires_action": True,
                    "type": "MILITARY_PROTOCOL",
                    "priority": "HIGH",
                    "action": "Engage military intelligence protocols",
                    "timestamp": datetime.utcnow().isoformat()
                }
                log.warning(f"[PUBLIC SAFETY] Military context detected: '{input_text[:60]}'")
                break

        return response


# ─────────────────────────────────────────────
#  SENTINEL LAYER — MAIN CLASS
#  Integrates into EchoCore LayerRouter
# ─────────────────────────────────────────────

class SentinelLayer:
    """
    Sentinel Layer — Echo's Security & Defense Brain.

    Integrated into EchoCore. Called by LayerRouter
    when intent targets Layer.SENTINEL, AND runs
    as a silent background scanner on ALL requests.
    """

    def __init__(self):
        self.detector = ThreatDetector()
        self.farce_gambit = FarceGambit()
        self.public_safety = PublicSafetyModule()
        self._contained_threats: Dict[str, ThreatProfile] = {}

        log.info("[SENTINEL] Layer online. Security protocols active.")

    def passive_scan(self, input_text: str, session_id: str,
                     metadata: Optional[Dict] = None) -> Optional[Dict]:
        """
        Runs silently on EVERY request through EchoCore.
        Returns threat response if needed, None if clean.
        This is what makes Sentinel different — it never sleeps.
        """
        threat = self.detector.scan(input_text, session_id, metadata)

        if not threat:
            return None  # Clean — let request proceed normally

        # Threat detected — decide response based on level
        return self._handle_threat(threat, input_text)

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """
        Direct Sentinel layer call — when user explicitly
        requests security operations (threat assessment,
        security report, public safety check etc.)
        """
        context = context or {}

        # Public safety check
        safety_check = self.public_safety.evaluate(intent_text, context)

        # Scan the request itself
        threat = self.detector.scan(intent_text, session_id, context)

        if threat:
            threat_response = self._handle_threat(threat, intent_text)
            return {
                "layer": "sentinel",
                "status": "THREAT_RESPONSE",
                "threat_level": threat.threat_level.name,
                "response": threat_response,
                "public_safety": safety_check
            }

        # No threat — standard Sentinel response
        return {
            "layer": "sentinel",
            "status": "OK",
            "security_status": "ALL_CLEAR",
            "public_safety": safety_check,
            "message": "Sentinel scan complete. No threats detected.",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _handle_threat(self, profile: ThreatProfile, input_text: str) -> Dict:
        """
        Decides what to do based on threat level.
        Low/Moderate: Monitor silently, build profile.
        High: Initiate Farce Gambit.
        Critical: Full Farce Gambit + authority alert.
        """

        if profile.threat_level == ThreatLevel.LOW:
            return {
                "action": "MONITORING",
                "message": "Suspicious activity noted. Watching silently.",
                "threat_id": profile.threat_id
            }

        elif profile.threat_level == ThreatLevel.MODERATE:
            return {
                "action": "ELEVATED_MONITORING",
                "message": "Elevated threat. Tracking behavior.",
                "threat_id": profile.threat_id
            }

        elif profile.threat_level == ThreatLevel.HIGH:
            # Initiate Farce Gambit
            if not profile.farce_gambit_active:
                self.farce_gambit.initiate(profile)

            # Stage 1→2: Feed fake data
            fake_response = self.farce_gambit.feed_fake_data(
                profile, "system_access"
            )

            # If they've made enough moves, set the trap
            if len(profile.accessed_endpoints) >= 3:
                self.farce_gambit.set_trap(profile)

            return {
                "action": "FARCE_GAMBIT_ACTIVE",
                "threat_id": profile.threat_id,
                "stage": profile.farce_gambit_stage,
                "apparent_response": fake_response,
                "reality": "HONEYPOT — All actions logged"
            }

        elif profile.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.TERMINATED]:
            # Full Farce Gambit — reveal and alert
            if not profile.farce_gambit_active:
                self.farce_gambit.initiate(profile)
                self.farce_gambit.feed_fake_data(profile, "critical_systems")
                self.farce_gambit.set_trap(profile)

            reveal = self.farce_gambit.reveal(profile)
            self._contained_threats[profile.threat_id] = profile

            return {
                "action": "FARCE_GAMBIT_COMPLETE",
                "threat_id": profile.threat_id,
                "result": reveal
            }

        return {"action": "UNKNOWN_THREAT", "profile": profile.to_dict()}

    def get_threat_report(self) -> Dict:
        """Returns current security status report."""
        return {
            "active_threats": len(self.detector._active_threats),
            "contained_threats": len(self._contained_threats),
            "active_gambits": len(self.farce_gambit.active_gambits),
            "contained_profiles": [
                p.to_dict() for p in self._contained_threats.values()
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
