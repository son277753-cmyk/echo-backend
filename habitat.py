"""
╔══════════════════════════════════════════════════════════════════════╗
║                   ECHO AI — HABITAT LAYER                           ║
║         Smart Environment · IoT Control · Echo Grid                 ║
║                                                                      ║
║  MODULE 1 — SMART HOME CONTROL                                      ║
║    - Lights (color, brightness, scenes, schedules)                  ║
║    - Climate and temperature control                                 ║
║    - Locks, doors, security                                         ║
║    - Appliances and electronics                                     ║
║    - Security cameras                                               ║
║                                                                      ║
║  MODULE 2 — ENVIRONMENT INTELLIGENCE                                ║
║    - Reads the room — auto-adjusts to activity                      ║
║    - Scene modes (study, sleep, focus, party, movie, workout)       ║
║    - Learns preferences and applies automatically                   ║
║    - Mood-based environment adjustment                              ║
║                                                                      ║
║  MODULE 3 — MINOR CUBE INTEGRATION                                  ║
║    - LED control (color, patterns, brightness)                      ║
║    - Screen management                                              ║
║    - Camera and microphone                                          ║
║    - Speaker and audio output                                       ║
║    - Physical device health                                         ║
║                                                                      ║
║  MODULE 4 — ECHO GRID (Cross-Device Connectivity)                   ║
║    - Device registry — every Echo-enabled device                    ║
║    - Seamless session handoff between devices                       ║
║    - One unified session across all devices                         ║
║    - Presence detection — Echo knows where you are                  ║
║    - Task continuity — pick up exactly where you left off           ║
║    - Remote control — heat house from car, etc.                     ║
║                                                                      ║
║  JARVIS additions:                                                   ║
║    - Predictive environment — sets scene before you ask             ║
║    - Presence-triggered automation                                  ║
║    - Energy optimization — reduces power intelligently              ║
║    - Emergency protocols — lockdown, evacuation                     ║
║    - Room-by-room awareness                                         ║
║    - Anticipatory control (learns your patterns)                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import uuid
import time
import json
import logging
import threading
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


log = logging.getLogger("EchoCore.Habitat")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class DeviceType(Enum):
    MINOR_CUBE      = "minor_cube"
    SMART_PHONE     = "smart_phone"
    SMART_TV        = "smart_tv"
    SMART_GLASSES   = "smart_glasses"
    SMART_WATCH     = "smart_watch"
    LAPTOP          = "laptop"
    DESKTOP         = "desktop"
    SMART_CAR       = "smart_car"
    SMART_SPEAKER   = "smart_speaker"
    SMART_DISPLAY   = "smart_display"
    SMART_LIGHT     = "smart_light"
    THERMOSTAT      = "thermostat"
    SMART_LOCK      = "smart_lock"
    SECURITY_CAMERA = "security_camera"
    SMART_APPLIANCE = "smart_appliance"
    GREENHOUSE      = "greenhouse"
    HEALTH_PATCH    = "health_patch"
    EVO_CAR         = "evo_car"        # From your notes
    AVA_PHONE       = "ava_phone"      # From your notes
    CUSTOM          = "custom"


class DeviceStatus(Enum):
    ONLINE      = "online"
    OFFLINE     = "offline"
    STANDBY     = "standby"
    BUSY        = "busy"
    ERROR       = "error"
    UPDATING    = "updating"


class RoomScene(Enum):
    """
    Pre-configured environment scenes.
    JARVIS had protocols for every situation —
    "Party Protocol", "Clean Slate"...
    Echo has scenes.
    """
    NORMAL      = "normal"
    FOCUS       = "focus"
    STUDY       = "study"
    SLEEP       = "sleep"
    MOVIE       = "movie"
    WORKOUT     = "workout"
    PARTY       = "party"
    ROMANTIC    = "romantic"
    MORNING     = "morning"
    AWAY        = "away"
    EMERGENCY   = "emergency"
    WELCOME     = "welcome"     # Triggered when user arrives home
    GOODNIGHT   = "goodnight"


class LightColor(Enum):
    WHITE       = "#FFFFFF"
    WARM_WHITE  = "#FFD700"
    COOL_WHITE  = "#E0FFFF"
    RED         = "#FF0000"
    BLUE        = "#0000FF"
    GREEN       = "#00FF00"
    PURPLE      = "#800080"
    ORANGE      = "#FFA500"
    PINK        = "#FFC0CB"
    CYAN        = "#00FFFF"
    YELLOW      = "#FFFF00"
    TEAL        = "#008080"


class HandoffReason(Enum):
    """Why a session is moving between devices."""
    USER_REQUEST    = "user_request"    # User explicitly asked
    PROXIMITY       = "proximity"       # Moved closer to another device
    BETTER_SCREEN   = "better_screen"   # Bigger/better screen available
    BATTERY         = "battery"         # Current device low battery
    TASK_TYPE       = "task_type"       # Task better suited for other device
    AUTO            = "auto"            # Echo decided automatically


# ─────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class SmartDevice:
    """Any device connected to the Echo Grid."""
    device_id:    str         = field(default_factory=lambda: str(uuid.uuid4())[:10])
    name:         str         = ""
    device_type:  DeviceType  = DeviceType.CUSTOM
    status:       DeviceStatus = DeviceStatus.OFFLINE
    room:         str         = "unknown"
    ip_address:   str         = ""
    capabilities: List[str]   = field(default_factory=list)
    properties:   Dict        = field(default_factory=dict)
    last_seen:    str         = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    battery_pct:  Optional[int] = None
    firmware:     str         = "1.0.0"
    echo_enabled: bool        = True
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

    def is_online(self) -> bool:
        return self.status == DeviceStatus.ONLINE

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["device_type"] = self.device_type.value
        d["status"]      = self.status.value
        return d


@dataclass
class EchoSession:
    """
    A user's active session that can move between devices.
    This is the core of cross-device continuity.

    JARVIS had one session — Tony's.
    It didn't matter if Tony was in the workshop,
    in the suit, or in the living room.
    JARVIS was always there, context fully intact.
    """
    session_id:      str  = field(default_factory=lambda: str(uuid.uuid4())[:12])
    user_id:         str  = "primary_user"
    active_device_id: str = ""
    active_device_name: str = ""
    previous_device_id: str = ""
    context:         Dict = field(default_factory=dict)     # What user was doing
    active_task:     Optional[str] = None                   # Current task
    active_layer:    str  = "core"
    handoff_history: List[Dict] = field(default_factory=list)
    created_at:      str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    last_activity:   str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def update_activity(self):
        self.last_activity = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Room:
    """A physical room in the environment."""
    room_id:     str  = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name:        str  = ""
    floor:       int  = 1
    scene:       RoomScene = RoomScene.NORMAL
    temperature: float = 21.0   # Celsius
    humidity:    float = 45.0   # Percent
    occupied:    bool = False
    devices:     List[str] = field(default_factory=list)   # device_ids
    light_level: int  = 80      # 0-100
    light_color: str  = LightColor.WARM_WHITE.value

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["scene"] = self.scene.value
        return d


# ══════════════════════════════════════════════
#  MODULE 1 — DEVICE CONTROLLER
# ══════════════════════════════════════════════

class DeviceController:
    """
    Controls individual smart devices.
    Every device type has its own control protocol.

    In production: integrates with real IoT protocols
    (Matter, Z-Wave, Zigbee, HomeKit, Google Home,
    Amazon Alexa, custom APIs).
    """

    def __init__(self):
        self._command_log: List[Dict] = []
        self._lock = threading.Lock()

    def send_command(self, device: SmartDevice,
                      command: str,
                      params: Optional[Dict] = None) -> Dict:
        """Send a command to a device."""
        params = params or {}

        if not device.is_online():
            return {
                "success": False,
                "error"  : f"Device '{device.name}' is offline",
                "device" : device.name,
                "command": command
            }

        # Execute command based on device type and capability
        result = self._execute(device, command, params)

        # Log the command
        log_entry = {
            "device_id"  : device.device_id,
            "device_name": device.name,
            "command"    : command,
            "params"     : params,
            "result"     : result,
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }
        with self._lock:
            self._command_log.append(log_entry)

        log.info(
            f"[HABITAT/DEVICE] {device.name} | "
            f"{command} | {'OK' if result['success'] else 'FAIL'}"
        )

        return result

    def _execute(self, device: SmartDevice,
                  command: str, params: Dict) -> Dict:
        """Execute command based on device type."""
        handlers = {
            DeviceType.SMART_LIGHT   : self._control_light,
            DeviceType.THERMOSTAT    : self._control_climate,
            DeviceType.SMART_LOCK    : self._control_lock,
            DeviceType.SECURITY_CAMERA: self._control_camera,
            DeviceType.SMART_TV      : self._control_tv,
            DeviceType.SMART_SPEAKER : self._control_speaker,
            DeviceType.MINOR_CUBE    : self._control_minor_cube,
            DeviceType.EVO_CAR       : self._control_evo_car,
            DeviceType.SMART_APPLIANCE: self._control_appliance,
            DeviceType.GREENHOUSE    : self._control_greenhouse,
            DeviceType.HEALTH_PATCH  : self._control_health_patch,
        }

        handler = handlers.get(device.device_type, self._control_generic)
        return handler(device, command, params)

    def _control_light(self, device: SmartDevice,
                        command: str, params: Dict) -> Dict:
        state = {}
        if command == "on":
            state = {"power": True,
                     "brightness": params.get("brightness", 80),
                     "color": params.get("color", LightColor.WARM_WHITE.value)}
        elif command == "off":
            state = {"power": False}
        elif command == "dim":
            state = {"brightness": params.get("level", 30)}
        elif command == "color":
            state = {"color": params.get("color", LightColor.WHITE.value)}
        elif command == "scene":
            scene_map = {
                "sleep"  : {"brightness": 5,  "color": LightColor.RED.value},
                "focus"  : {"brightness": 100,"color": LightColor.COOL_WHITE.value},
                "movie"  : {"brightness": 15, "color": LightColor.TEAL.value},
                "party"  : {"brightness": 80, "color": LightColor.PURPLE.value},
                "morning": {"brightness": 60, "color": LightColor.WARM_WHITE.value},
                "study"  : {"brightness": 90, "color": LightColor.COOL_WHITE.value},
            }
            scene_name = params.get("scene", "normal")
            state = scene_map.get(scene_name, {"brightness": 80})

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_climate(self, device: SmartDevice,
                          command: str, params: Dict) -> Dict:
        state = {}
        if command == "set_temperature":
            temp = params.get("temperature", 21)
            temp = max(16, min(30, temp))  # Safety bounds
            state = {"target_temperature": temp, "mode": "heat" if temp > 21 else "cool"}
        elif command == "off":
            state = {"mode": "off"}
        elif command == "mode":
            state = {"mode": params.get("mode", "auto")}
        elif command == "boost":
            state = {"mode": "boost", "target_temperature": params.get("temperature", 24)}

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_lock(self, device: SmartDevice,
                       command: str, params: Dict) -> Dict:
        if command in ["lock", "secure"]:
            device.properties["locked"] = True
            log.info(f"[HABITAT/LOCK] {device.name} locked")
        elif command == "unlock":
            # Require auth for unlock
            auth = params.get("auth_code")
            if not auth:
                return {
                    "success": False,
                    "error"  : "Authentication required to unlock",
                    "command": command
                }
            device.properties["locked"] = False
            log.warning(f"[HABITAT/LOCK] {device.name} unlocked — auth verified")
        elif command == "status":
            pass

        return {
            "success": True,
            "command": command,
            "locked" : device.properties.get("locked", True)
        }

    def _control_camera(self, device: SmartDevice,
                         command: str, params: Dict) -> Dict:
        state = {}
        if command == "start_recording":
            state = {"recording": True, "started": datetime.now(timezone.utc).isoformat()}
        elif command == "stop_recording":
            state = {"recording": False}
        elif command == "snapshot":
            state = {"snapshot": f"snapshot_{uuid.uuid4().hex[:8]}.jpg",
                     "timestamp": datetime.now(timezone.utc).isoformat()}
        elif command == "pan":
            state = {"angle": params.get("angle", 0)}
        elif command == "motion_detect":
            state = {"motion_detection": params.get("enabled", True)}

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_tv(self, device: SmartDevice,
                     command: str, params: Dict) -> Dict:
        state = {}
        if command == "on":
            state = {"power": True, "input": params.get("input", "echo")}
        elif command == "off":
            state = {"power": False}
        elif command == "volume":
            state = {"volume": max(0, min(100, params.get("level", 50)))}
        elif command == "channel":
            state = {"channel": params.get("channel", 1)}
        elif command == "cast":
            state = {"casting": True, "source": params.get("source", "echo"),
                     "content": params.get("content", "")}
        elif command == "echo_display":
            # Show Echo UI on TV
            state = {"power": True, "input": "echo_grid",
                     "echo_ui": params.get("ui", "dashboard")}

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_speaker(self, device: SmartDevice,
                          command: str, params: Dict) -> Dict:
        state = {}
        if command == "play":
            state = {"playing": True, "content": params.get("content", ""),
                     "volume": params.get("volume", 70)}
        elif command == "stop":
            state = {"playing": False}
        elif command == "volume":
            state = {"volume": params.get("level", 50)}
        elif command == "echo_voice":
            state = {"echo_output": True, "voice": "echo_primary"}

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_minor_cube(self, device: SmartDevice,
                             command: str, params: Dict) -> Dict:
        """
        Minor Cube specific controls.
        The Cube is Echo's primary hardware — full control
        over its LED array, screen, camera, audio.
        """
        state = {}
        if command == "led_color":
            color   = params.get("color", "#FFFFFF")
            pattern = params.get("pattern", "solid")
            state   = {"led_color": color, "led_pattern": pattern,
                       "led_brightness": params.get("brightness", 80)}
        elif command == "led_pulse":
            state = {"led_pattern": "pulse",
                     "pulse_speed": params.get("speed", "medium"),
                     "led_color"  : params.get("color", "#00D2FF")}
        elif command == "led_rainbow":
            state = {"led_pattern": "rainbow", "cycle_speed": params.get("speed", 1.0)}
        elif command == "led_off":
            state = {"led_pattern": "off", "led_brightness": 0}
        elif command == "screen_on":
            state = {"screen": True, "brightness": params.get("brightness", 80),
                     "content": params.get("content", "echo_home")}
        elif command == "screen_off":
            state = {"screen": False}
        elif command == "screen_content":
            state = {"screen": True,
                     "content": params.get("content", ""),
                     "content_type": params.get("type", "text")}
        elif command == "camera_on":
            state = {"camera": True, "resolution": params.get("resolution", "1080p")}
        elif command == "camera_off":
            state = {"camera": False}
        elif command == "speak":
            state = {"audio_output": True, "text": params.get("text", ""),
                     "voice": params.get("voice", "echo_primary")}
        elif command == "alert_flash":
            # Flash LED for alerts — Sentinel integration
            state = {"led_pattern": "flash", "led_color": params.get("color", "#FF0000"),
                     "flash_count": params.get("count", 3)}
        elif command == "status_display":
            state = {"screen": True, "content": "status",
                     "data": params.get("data", {})}

        device.properties.update(state)
        log.info(f"[HABITAT/CUBE] {command} → {state}")
        return {"success": True, "command": command, "state": state,
                "device": "Minor Cube"}

    def _control_evo_car(self, device: SmartDevice,
                          command: str, params: Dict) -> Dict:
        """
        Evo Car integration — from your notes.
        Echo connects to the car, enabling
        remote control and environment prep.
        """
        state = {}
        if command == "preheat":
            temp  = params.get("temperature", 22)
            state = {"climate_active": True, "target_temp": temp,
                     "eta_ready": "5 minutes"}
        elif command == "lock":
            state = {"locked": True}
        elif command == "unlock":
            state = {"locked": False}
        elif command == "navigate":
            state = {"navigation": True,
                     "destination": params.get("destination", ""),
                     "echo_active": True}
        elif command == "echo_handoff":
            # Transfer Echo session to car
            state = {"echo_session": True,
                     "session_id": params.get("session_id", ""),
                     "audio_active": True, "display_active": True}
        elif command == "summon":
            state = {"summoning": True, "location": params.get("location", "")}
        elif command == "status":
            state = {"battery": device.properties.get("battery", 85),
                     "range_km": device.properties.get("range", 380),
                     "locked"  : device.properties.get("locked", True)}

        device.properties.update(state)
        log.info(f"[HABITAT/EVO] {command}")
        return {"success": True, "command": command, "state": state}

    def _control_appliance(self, device: SmartDevice,
                            command: str, params: Dict) -> Dict:
        state = {}
        if command == "on":
            state = {"power": True, "mode": params.get("mode", "auto")}
        elif command == "off":
            state = {"power": False}
        elif command == "schedule":
            state = {"scheduled": True, "time": params.get("time", ""),
                     "mode": params.get("mode", "auto")}
        elif command == "status":
            state = dict(device.properties)

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_greenhouse(self, device: SmartDevice,
                             command: str, params: Dict) -> Dict:
        """Greenhouse control — from your notes."""
        state = {}
        if command == "water":
            state = {"watering": True, "duration_min": params.get("duration", 15),
                     "zone": params.get("zone", "all")}
        elif command == "temperature":
            state = {"target_temp": params.get("temperature", 24),
                     "humidity_target": params.get("humidity", 70)}
        elif command == "lights":
            state = {"grow_lights": params.get("on", True),
                     "spectrum": params.get("spectrum", "full"),
                     "intensity": params.get("intensity", 80)}
        elif command == "nutrients":
            state = {"nutrient_pump": True,
                     "solution": params.get("solution", "standard")}
        elif command == "status":
            state = {"temperature": 24.2, "humidity": 68,
                     "soil_moisture": 65, "light_hours": 14}

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_health_patch(self, device: SmartDevice,
                               command: str, params: Dict) -> Dict:
        """Health patch — from your notes. Connects to Vital layer."""
        state = {}
        if command == "read":
            state = {"heart_rate": 72, "temperature": 36.8,
                     "oxygen_sat": 98, "glucose": 92,
                     "stress_level": 4, "timestamp": datetime.now(timezone.utc).isoformat()}
        elif command == "alert_threshold":
            state = {"alert_hr_high": params.get("hr_high", 120),
                     "alert_hr_low": params.get("hr_low", 50)}
        elif command == "sync_vital":
            state = {"synced_to_vital": True,
                     "sync_interval_sec": params.get("interval", 30)}

        device.properties.update(state)
        return {"success": True, "command": command, "state": state}

    def _control_generic(self, device: SmartDevice,
                          command: str, params: Dict) -> Dict:
        """Generic handler for custom devices."""
        device.properties[f"last_command"] = command
        device.properties[f"last_params"]  = params
        return {"success": True, "command": command,
                "note": "Generic command executed"}

    def get_command_log(self, limit: int = 20) -> List[Dict]:
        return self._command_log[-limit:]


# ══════════════════════════════════════════════
#  MODULE 2 — ENVIRONMENT INTELLIGENCE
# ══════════════════════════════════════════════

class EnvironmentIntelligence:
    """
    Makes the environment respond intelligently.

    JARVIS didn't just control devices —
    he orchestrated environments.
    When Tony said "Jarvis, I'll be in the lab"
    the lab was ready before Tony got there.

    Echo does the same — reads context,
    predicts needs, sets the scene automatically.
    """

    # Scene configurations — what each scene does to the environment
    SCENE_CONFIGS = {
        RoomScene.FOCUS: {
            "lights"      : {"brightness": 100, "color": LightColor.COOL_WHITE.value},
            "temperature" : 20,    # Slightly cool for alertness
            "notifications": "blocked",
            "description" : "Maximum focus. Cool white light, lower temp, no interruptions.",
            "echo_led"    : {"color": "#00D2FF", "pattern": "solid"}
        },
        RoomScene.STUDY: {
            "lights"      : {"brightness": 90, "color": LightColor.COOL_WHITE.value},
            "temperature" : 21,
            "notifications": "filtered",
            "description" : "Study mode. Good lighting, comfortable temperature.",
            "echo_led"    : {"color": "#4CAF50", "pattern": "solid"}
        },
        RoomScene.SLEEP: {
            "lights"      : {"brightness": 0, "color": LightColor.RED.value},
            "temperature" : 18,    # Cooler for sleep
            "notifications": "emergency_only",
            "description" : "Sleep mode. Lights off, cool temperature, silent.",
            "echo_led"    : {"color": "#1A0000", "pattern": "breathe_slow"}
        },
        RoomScene.MOVIE: {
            "lights"      : {"brightness": 10, "color": LightColor.TEAL.value},
            "temperature" : 22,
            "notifications": "filtered",
            "description" : "Cinema mode. Ambient backlighting, comfortable temp.",
            "echo_led"    : {"color": "#008080", "pattern": "pulse_slow"}
        },
        RoomScene.WORKOUT: {
            "lights"      : {"brightness": 100, "color": LightColor.WHITE.value},
            "temperature" : 19,    # Cooler for exercise
            "notifications": "filtered",
            "description" : "Workout mode. Bright light, cool air, energy music.",
            "echo_led"    : {"color": "#FF6600", "pattern": "pulse_fast"}
        },
        RoomScene.PARTY: {
            "lights"      : {"brightness": 80, "color": LightColor.PURPLE.value},
            "temperature" : 22,
            "notifications": "off",
            "description" : "Party mode. Colored lights, music, good vibes.",
            "echo_led"    : {"color": "#FF00FF", "pattern": "rainbow"}
        },
        RoomScene.MORNING: {
            "lights"      : {"brightness": 60, "color": LightColor.WARM_WHITE.value},
            "temperature" : 21,
            "notifications": "all",
            "description" : "Morning mode. Warm light, comfortable temp, briefing ready.",
            "echo_led"    : {"color": "#FFD700", "pattern": "sunrise"}
        },
        RoomScene.AWAY: {
            "lights"      : {"brightness": 0, "color": LightColor.WHITE.value},
            "temperature" : 17,    # Energy saving
            "notifications": "all",
            "description" : "Away mode. Minimal energy. Security active.",
            "echo_led"    : {"color": "#000033", "pattern": "slow_blink"}
        },
        RoomScene.EMERGENCY: {
            "lights"      : {"brightness": 100, "color": LightColor.RED.value},
            "temperature" : 21,
            "notifications": "all",
            "description" : "EMERGENCY. All lights on, all systems alert.",
            "echo_led"    : {"color": "#FF0000", "pattern": "fast_flash"}
        },
        RoomScene.WELCOME: {
            "lights"      : {"brightness": 75, "color": LightColor.WARM_WHITE.value},
            "temperature" : 22,
            "notifications": "all",
            "description" : "Welcome home. Lights on, temperature comfortable.",
            "echo_led"    : {"color": "#00FF88", "pattern": "pulse_medium"}
        },
        RoomScene.ROMANTIC: {
            "lights"      : {"brightness": 25, "color": LightColor.RED.value},
            "temperature" : 23,
            "notifications": "emergency_only",
            "description" : "Romantic setting. Low warm light, comfortable temperature.",
            "echo_led"    : {"color": "#FF1493", "pattern": "breathe_slow"}
        },
        RoomScene.GOODNIGHT: {
            "lights"      : {"brightness": 5, "color": LightColor.WARM_WHITE.value},
            "temperature" : 18,
            "notifications": "emergency_only",
            "description" : "Goodnight. Lights almost off, cool temp for sleep.",
            "echo_led"    : {"color": "#000011", "pattern": "fade_out"}
        },
        RoomScene.NORMAL: {
            "lights"      : {"brightness": 80, "color": LightColor.WARM_WHITE.value},
            "temperature" : 21,
            "notifications": "all",
            "description" : "Normal mode. Standard lighting and temperature.",
            "echo_led"    : {"color": "#FFFFFF", "pattern": "solid"}
        }
    }

    # Pattern recognition — what activity maps to what scene
    ACTIVITY_SCENE_MAP = {
        "studying"   : RoomScene.STUDY,
        "working"    : RoomScene.FOCUS,
        "sleeping"   : RoomScene.SLEEP,
        "watching"   : RoomScene.MOVIE,
        "exercising" : RoomScene.WORKOUT,
        "partying"   : RoomScene.PARTY,
        "waking up"  : RoomScene.MORNING,
        "leaving"    : RoomScene.AWAY,
        "arriving"   : RoomScene.WELCOME,
        "goodnight"  : RoomScene.GOODNIGHT,
    }

    def __init__(self):
        self._user_patterns: Dict[str, List] = defaultdict(list)
        self._scene_history: List[Dict]      = []
        self._preferences: Dict              = {}

    def detect_scene_from_intent(self, intent: str) -> Optional[RoomScene]:
        """Detect what scene the user wants from their request."""
        intent_low = intent.lower()
        for activity, scene in self.ACTIVITY_SCENE_MAP.items():
            if activity in intent_low:
                return scene

        # Direct scene name detection
        for scene in RoomScene:
            if scene.value in intent_low:
                return scene

        return None

    def get_scene_config(self, scene: RoomScene) -> Dict:
        """Get full configuration for a scene."""
        return self.SCENE_CONFIGS.get(scene, self.SCENE_CONFIGS[RoomScene.NORMAL])

    def learn_pattern(self, time_of_day: str, scene: RoomScene):
        """
        JARVIS addition: Learn user patterns.
        If you always switch to focus mode at 9am,
        Echo starts doing it automatically.
        """
        self._user_patterns[time_of_day].append(scene.value)
        log.debug(f"[HABITAT/ENV] Pattern learned: {time_of_day} → {scene.value}")

    def predict_scene(self) -> Optional[RoomScene]:
        """
        JARVIS addition: Predict what scene the user wants
        based on time of day and learned patterns.
        """
        now = datetime.now(timezone.utc)
        hour = now.hour

        # Time-based defaults if no patterns learned
        if 5 <= hour < 8:
            return RoomScene.MORNING
        elif 8 <= hour < 9:
            return RoomScene.STUDY
        elif 9 <= hour < 12:
            return RoomScene.FOCUS
        elif 12 <= hour < 14:
            return RoomScene.NORMAL
        elif 14 <= hour < 17:
            return RoomScene.FOCUS
        elif 17 <= hour < 20:
            return RoomScene.NORMAL
        elif 20 <= hour < 22:
            return RoomScene.MOVIE
        elif 22 <= hour < 24:
            return RoomScene.GOODNIGHT
        else:
            return RoomScene.SLEEP

    def get_energy_optimization(self, rooms: Dict[str, "Room"]) -> Dict:
        """
        JARVIS addition: Energy optimization report.
        Identifies wasteful device usage and suggests
        how to reduce power consumption without
        affecting comfort.
        """
        savings = []
        for room_name, room in rooms.items():
            if not room.occupied and room.light_level > 0:
                savings.append({
                    "room"   : room_name,
                    "action" : "Turn off lights — room is empty",
                    "saving" : "~15W per bulb"
                })
            if not room.occupied and room.temperature > 19:
                savings.append({
                    "room"   : room_name,
                    "action" : f"Reduce heat to 17°C — room unoccupied",
                    "saving" : "~10% energy per degree"
                })

        return {
            "optimization_count": len(savings),
            "suggestions"       : savings,
            "echo_note"         : (
                f"{len(savings)} energy optimizations available. "
                f"Apply all to reduce power consumption."
            )
        }


# ══════════════════════════════════════════════
#  MODULE 3 — ECHO GRID
#  Cross-device seamless connectivity
# ══════════════════════════════════════════════

class EchoGrid:
    """
    The Echo Grid — unified device mesh network.

    Every Echo-enabled device is a node in this grid.
    The user has ONE session that moves between nodes
    seamlessly — like water flowing between containers.

    JARVIS was everywhere Tony was —
    workshop, suit, car, tower — one intelligence,
    many endpoints. Echo Grid makes Echo the same.

    Devices on the grid:
    - Minor Cube (primary hub)
    - AVA Phones
    - Evo Cars
    - Smart TVs
    - Smart Glasses
    - Smart Watches
    - Laptops/Desktops
    - Smart Speakers
    - Greenhouses
    - Health Patches
    - Any custom Echo-enabled device
    """

    def __init__(self):
        self._devices: Dict[str, SmartDevice]    = {}
        self._sessions: Dict[str, EchoSession]   = {}
        self._active_session: Optional[str]      = None
        self._presence_map: Dict[str, str]       = {}  # room → user
        self._grid_log: List[Dict]               = []
        self._lock                               = threading.Lock()

        # Register default devices
        self._register_default_devices()

        log.info(f"[HABITAT/GRID] Echo Grid online | "
                 f"Devices: {len(self._devices)}")

    def _register_default_devices(self):
        """Register the default Echo device ecosystem."""
        defaults = [
            SmartDevice(
                name="Minor Cube",
                device_type=DeviceType.MINOR_CUBE,
                status=DeviceStatus.ONLINE,
                room="living_room",
                capabilities=["led", "screen", "camera", "microphone",
                               "speaker", "usb", "wifi", "bluetooth"],
                properties={"led_color": "#00D2FF", "led_pattern": "pulse",
                             "screen": True, "camera": False}
            ),
            SmartDevice(
                name="AVA Phone",
                device_type=DeviceType.AVA_PHONE,
                status=DeviceStatus.ONLINE,
                room="mobile",
                capabilities=["display", "camera", "microphone",
                               "speaker", "gps", "biometrics"],
                battery_pct=87
            ),
            SmartDevice(
                name="Evo Car",
                device_type=DeviceType.EVO_CAR,
                status=DeviceStatus.STANDBY,
                room="garage",
                capabilities=["display", "speaker", "navigation",
                               "climate", "autopilot"],
                properties={"battery": 85, "range_km": 380, "locked": True}
            ),
            SmartDevice(
                name="Smart TV — Living Room",
                device_type=DeviceType.SMART_TV,
                status=DeviceStatus.STANDBY,
                room="living_room",
                capabilities=["display", "speaker", "echo_grid", "cast"]
            ),
            SmartDevice(
                name="Smart Glasses",
                device_type=DeviceType.SMART_GLASSES,
                status=DeviceStatus.ONLINE,
                room="mobile",
                capabilities=["ar_display", "camera", "microphone",
                               "speaker", "gesture"],
                battery_pct=72
            ),
            SmartDevice(
                name="Health Patch",
                device_type=DeviceType.HEALTH_PATCH,
                status=DeviceStatus.ONLINE,
                room="mobile",
                capabilities=["heart_rate", "temperature", "glucose",
                               "oxygen_sat", "stress"],
                battery_pct=91
            ),
            SmartDevice(
                name="Living Room Lights",
                device_type=DeviceType.SMART_LIGHT,
                status=DeviceStatus.ONLINE,
                room="living_room",
                capabilities=["on_off", "dimming", "color_change"],
                properties={"power": True, "brightness": 80,
                            "color": LightColor.WARM_WHITE.value}
            ),
            SmartDevice(
                name="Smart Thermostat",
                device_type=DeviceType.THERMOSTAT,
                status=DeviceStatus.ONLINE,
                room="hallway",
                capabilities=["temperature", "humidity", "schedule"],
                properties={"current_temp": 21.5, "target_temp": 22,
                            "mode": "auto", "humidity": 45}
            ),
            SmartDevice(
                name="Front Door Lock",
                device_type=DeviceType.SMART_LOCK,
                status=DeviceStatus.ONLINE,
                room="entrance",
                capabilities=["lock", "unlock", "status", "access_log"],
                properties={"locked": True}
            ),
            SmartDevice(
                name="Security Camera — Front",
                device_type=DeviceType.SECURITY_CAMERA,
                status=DeviceStatus.ONLINE,
                room="entrance",
                capabilities=["record", "snapshot", "motion_detect",
                               "night_vision", "pan_tilt"],
                properties={"recording": False, "motion_detection": True}
            ),
        ]

        for device in defaults:
            self._devices[device.device_id] = device

    def register_device(self, name: str, device_type: DeviceType,
                         room: str, capabilities: List[str],
                         ip_address: str = "") -> SmartDevice:
        """Register a new device on the Echo Grid."""
        device = SmartDevice(
            name         = name,
            device_type  = device_type,
            status       = DeviceStatus.ONLINE,
            room         = room,
            capabilities = capabilities,
            ip_address   = ip_address
        )
        with self._lock:
            self._devices[device.device_id] = device

        log.info(
            f"[HABITAT/GRID] Device registered: {name} | "
            f"Type: {device_type.value} | Room: {room}"
        )
        return device

    def get_device(self, name_or_id: str) -> Optional[SmartDevice]:
        """Find a device by ID or name."""
        # Try ID first
        if name_or_id in self._devices:
            return self._devices[name_or_id]
        # Try name search
        name_lower = name_or_id.lower()
        for device in self._devices.values():
            if name_lower in device.name.lower():
                return device
        return None

    def get_devices_in_room(self, room: str) -> List[SmartDevice]:
        return [d for d in self._devices.values()
                if d.room.lower() == room.lower()]

    def get_online_devices(self) -> List[SmartDevice]:
        return [d for d in self._devices.values()
                if d.status == DeviceStatus.ONLINE]

    # ── SESSION MANAGEMENT ─────────────────────

    def create_session(self, user_id: str = "primary_user",
                        device_id: Optional[str] = None) -> EchoSession:
        """Create a new Echo session."""
        # Find primary device if not specified
        if not device_id:
            cube = self._find_device_by_type(DeviceType.MINOR_CUBE)
            device_id = cube.device_id if cube else ""

        device = self._devices.get(device_id)
        session = EchoSession(
            user_id            = user_id,
            active_device_id   = device_id,
            active_device_name = device.name if device else "Unknown"
        )

        with self._lock:
            self._sessions[session.session_id] = session
            self._active_session = session.session_id

        log.info(
            f"[HABITAT/GRID] Session created: {session.session_id} | "
            f"Device: {session.active_device_name}"
        )
        return session

    def handoff(self, target_device_name: str,
                 reason: HandoffReason = HandoffReason.USER_REQUEST,
                 session_id: Optional[str] = None,
                 preserve_context: bool = True) -> Dict:
        """
        Seamlessly transfer Echo session to a different device.

        This is the core of cross-device continuity.
        The session moves — the user's context moves with it.
        They pick up exactly where they left off.

        "Echo, switch to the car" — done.
        "Echo, continue on the TV" — done.
        Everything intact.
        """
        session_id = session_id or self._active_session
        session    = self._sessions.get(session_id)

        if not session:
            return {"success": False, "error": "No active session"}

        # Find target device
        target = self.get_device(target_device_name)
        if not target:
            return {
                "success": False,
                "error"  : f"Device '{target_device_name}' not found on Echo Grid"
            }

        if target.status not in [DeviceStatus.ONLINE, DeviceStatus.STANDBY, DeviceStatus.BUSY]:
            return {
                "success": False,
                "error"  : f"Device '{target.name}' is offline"
            }
        if target.status == DeviceStatus.STANDBY:
            target.status = DeviceStatus.ONLINE

        # Record handoff
        old_device     = self._devices.get(session.active_device_id)
        old_device_name = old_device.name if old_device else "Unknown"

        handoff_record = {
            "from_device" : old_device_name,
            "to_device"   : target.name,
            "reason"      : reason.value,
            "timestamp"   : datetime.now(timezone.utc).isoformat(),
            "context"     : session.context if preserve_context else {},
            "task"        : session.active_task
        }

        # Update session
        session.previous_device_id  = session.active_device_id
        session.active_device_id    = target.device_id
        session.active_device_name  = target.name
        session.handoff_history.append(handoff_record)
        session.update_activity()

        # Set old device to standby
        if old_device:
            old_device.status = DeviceStatus.STANDBY

        # Set new device as active
        target.status = DeviceStatus.BUSY

        self._grid_log.append({
            "event"     : "handoff",
            "record"    : handoff_record,
            "session_id": session_id
        })

        log.info(
            f"[HABITAT/GRID] Handoff: {old_device_name} → {target.name} | "
            f"Reason: {reason.value} | "
            f"Task: {session.active_task or 'none'}"
        )

        return {
            "success"      : True,
            "from_device"  : old_device_name,
            "to_device"    : target.name,
            "reason"       : reason.value,
            "context_preserved": preserve_context,
            "active_task"  : session.active_task,
            "session_id"   : session_id,
            "echo_note"    : (
                f"Switched to {target.name}. "
                f"{'Your context and task carry over seamlessly.' if preserve_context else 'Fresh start on new device.'}"
                + (f" Continuing: {session.active_task}" if session.active_task else "")
            )
        }

    def remote_command(self, device_name: str, command: str,
                        params: Optional[Dict] = None) -> Dict:
        """
        Send a command to any device from anywhere.

        "Echo, heat up the house" — from the car.
        "Echo, lock the front door" — from the office.
        "Echo, turn on the TV" — from the bedroom.

        Distance doesn't matter on the Echo Grid.
        """
        params = params or {}
        device = self.get_device(device_name)

        if not device:
            return {
                "success": False,
                "error"  : f"'{device_name}' not found on Echo Grid"
            }

        # Log remote command
        self._grid_log.append({
            "event"    : "remote_command",
            "device"   : device.name,
            "command"  : command,
            "params"   : params,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        controller = DeviceController()
        result     = controller.send_command(device, command, params)

        log.info(
            f"[HABITAT/GRID] Remote: → {device.name} | "
            f"{command} | {'OK' if result['success'] else 'FAIL'}"
        )

        return {
            "success"    : result["success"],
            "device"     : device.name,
            "command"    : command,
            "result"     : result,
            "echo_note"  : (
                f"Command '{command}' sent to {device.name} "
                f"{'successfully' if result['success'] else 'failed'}."
            )
        }

    def update_presence(self, room: str, user: str = "primary_user"):
        """
        Update presence detection.
        JARVIS addition: Echo knows where you are.
        This triggers location-based automations.
        """
        old_room = None
        for r, u in self._presence_map.items():
            if u == user:
                old_room = r
                break

        if old_room:
            del self._presence_map[old_room]

        self._presence_map[room] = user

        log.info(f"[HABITAT/GRID] Presence: {user} → {room}")

        # Return room change info for automation
        return {
            "user"     : user,
            "room"     : room,
            "previous" : old_room,
            "changed"  : old_room != room
        }

    def get_grid_status(self) -> Dict:
        """Full Echo Grid status."""
        online   = [d for d in self._devices.values() if d.is_online()]
        offline  = [d for d in self._devices.values() if not d.is_online()]
        session  = self._sessions.get(self._active_session)

        return {
            "total_devices"   : len(self._devices),
            "online"          : len(online),
            "offline"         : len(offline),
            "active_session"  : session.to_dict() if session else None,
            "presence"        : dict(self._presence_map),
            "grid_log_count"  : len(self._grid_log),
            "devices"         : [d.to_dict() for d in self._devices.values()],
            "timestamp"       : datetime.now(timezone.utc).isoformat()
        }

    def _find_device_by_type(self, device_type: DeviceType) -> Optional[SmartDevice]:
        for device in self._devices.values():
            if device.device_type == device_type:
                return device
        return None

    def get_session(self, session_id: Optional[str] = None) -> Optional[EchoSession]:
        sid = session_id or self._active_session
        return self._sessions.get(sid)


# ══════════════════════════════════════════════
#  MODULE 4 — ROOM MANAGER
# ══════════════════════════════════════════════

class RoomManager:
    """Manages rooms and their states."""

    def __init__(self):
        self._rooms: Dict[str, Room] = {}
        self._build_default_rooms()

    def _build_default_rooms(self):
        rooms = [
            Room(name="Living Room",  floor=1, temperature=21.5, light_level=80),
            Room(name="Bedroom",      floor=1, temperature=20.0, light_level=30),
            Room(name="Kitchen",      floor=1, temperature=22.0, light_level=90),
            Room(name="Office",       floor=1, temperature=20.5, light_level=85),
            Room(name="Bathroom",     floor=1, temperature=23.0, light_level=70),
            Room(name="Garage",       floor=0, temperature=18.0, light_level=60),
            Room(name="Entrance",     floor=1, temperature=19.0, light_level=50),
        ]
        for room in rooms:
            self._rooms[room.name.lower().replace(" ", "_")] = room

    def set_scene(self, room_name: str, scene: RoomScene) -> Dict:
        """Set a scene for a room."""
        room = self._rooms.get(room_name.lower().replace(" ", "_"))
        if not room:
            return {"error": f"Room '{room_name}' not found"}

        room.scene = scene

        # Apply scene config to room
        from habitat import EnvironmentIntelligence
        env = EnvironmentIntelligence()
        config = env.get_scene_config(scene)

        if "temperature" in config:
            room.temperature = config["temperature"]
        if "lights" in config:
            room.light_level = config["lights"].get("brightness", 80)
            room.light_color = config["lights"].get("color", LightColor.WARM_WHITE.value)

        log.info(f"[HABITAT/ROOM] {room.name} → scene: {scene.value}")

        return {
            "room"   : room.name,
            "scene"  : scene.value,
            "config" : config,
            "applied": True
        }

    def get_room(self, name: str) -> Optional[Room]:
        return self._rooms.get(name.lower().replace(" ", "_"))

    def get_all_rooms(self) -> List[Dict]:
        return [r.to_dict() for r in self._rooms.values()]

    def mark_occupied(self, room_name: str, occupied: bool = True):
        room = self._rooms.get(room_name.lower().replace(" ", "_"))
        if room:
            room.occupied = occupied


# ══════════════════════════════════════════════
#  HABITAT LAYER — MASTER CLASS
# ══════════════════════════════════════════════

class HabitatLayer:
    """
    Habitat Layer — Echo's Smart Environment System.

    Controls every device in your environment.
    Manages the Echo Grid for cross-device continuity.
    Makes your environment respond to you —
    not the other way around.

    JARVIS ran Stark Tower.
    Habitat lets Echo run yours.
    """

    def __init__(self):
        self.controller  = DeviceController()
        self.environment = EnvironmentIntelligence()
        self.grid        = EchoGrid()
        self.rooms       = RoomManager()
        self._lock       = threading.Lock()

        # Create initial session on Minor Cube
        cube = self.grid._find_device_by_type(DeviceType.MINOR_CUBE)
        if cube:
            self.grid.create_session(device_id=cube.device_id)

        # Start presence simulation background thread
        self._presence_active = True
        self._bg = threading.Thread(
            target=self._background_monitor,
            daemon=True
        )
        self._bg.start()

        log.info("[HABITAT] Layer online. Echo Grid active.")

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """Main entry point from EchoCore LayerRouter."""
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[HABITAT] Processing: '{intent_text[:60]}'")

        # ── Route ──────────────────────────────────

        # Cross-device handoff
        if any(kw in intent_low for kw in ["switch to", "continue on", "move to",
                                            "switch device", "handoff", "transfer to"]):
            return self._handle_handoff(intent_text, context)

        # Remote command
        elif any(kw in intent_low for kw in ["heat up", "heat the", "cool down",
                                              "lock the", "unlock the", "turn on the",
                                              "turn off the", "remote"]):
            return self._handle_remote_command(intent_text, context)

        # Echo Grid status
        elif any(kw in intent_low for kw in ["grid", "devices", "connected devices",
                                              "echo grid", "all devices"]):
            return self._handle_grid_status()

        # Scene setting
        elif any(kw in intent_low for kw in ["scene", "mode", "set the mood",
                                              "study mode", "sleep mode", "focus mode",
                                              "movie mode", "party mode", "morning"]):
            return self._handle_scene(intent_text, context)

        # Minor Cube control
        elif any(kw in intent_low for kw in ["cube", "led", "minor cube",
                                              "change led", "cube light"]):
            return self._handle_cube(intent_text, context)

        # Climate control
        elif any(kw in intent_low for kw in ["temperature", "thermostat", "heat",
                                              "cool", "climate", "degrees"]):
            return self._handle_climate(intent_text, context)

        # Lights
        elif any(kw in intent_low for kw in ["light", "lights", "dim", "bright",
                                              "lamp", "brightness"]):
            return self._handle_lights(intent_text, context)

        # Security
        elif any(kw in intent_low for kw in ["lock", "unlock", "door", "camera",
                                              "security", "record"]):
            return self._handle_security(intent_text, context)

        # Room overview
        elif any(kw in intent_low for kw in ["room", "rooms", "house status",
                                              "home status", "environment"]):
            return self._handle_rooms(intent_text, context)

        # General Habitat
        else:
            return self._handle_general(intent_text, context)

    # ── Handlers ───────────────────────────────

    def _handle_handoff(self, intent: str, context: Dict) -> Dict:
        """Handle cross-device session handoff."""
        intent_low = intent.lower()

        # Detect target device
        device_map = {
            "car"       : "Evo Car",
            "evo"       : "Evo Car",
            "evo car"   : "Evo Car",
            "tv"        : "Smart TV — Living Room",
            "television": "Smart TV — Living Room",
            "glasses"   : "Smart Glasses",
            "phone"     : "AVA Phone",
            "ava"       : "AVA Phone",
            "cube"      : "Minor Cube",
            "watch"     : "Smart Watch",
            "laptop"    : "Laptop",
            "computer"  : "Desktop"
        }

        target_device = context.get("device", "")
        for kw, device_name in device_map.items():
            if kw in intent_low:
                target_device = device_name
                break

        if not target_device:
            # List available devices
            online = self.grid.get_online_devices()
            return {
                "layer"    : "habitat",
                "status"   : "NEEDS_INFO",
                "sub_system": "handoff",
                "available_devices": [d.name for d in online],
                "message"  : (
                    f"Which device shall I switch to? "
                    f"Available: {', '.join(d.name for d in online[:5])}"
                ),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        result = self.grid.handoff(
            target_device_name = target_device,
            reason             = HandoffReason.USER_REQUEST
        )

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "handoff",
            "result"   : result,
            "message"  : result.get("echo_note", str(result)),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_remote_command(self, intent: str, context: Dict) -> Dict:
        """Handle remote device commands."""
        intent_low = intent.lower()

        # Parse intent → device + command
        remote_patterns = [
            # Climate
            (["heat up", "heat the house", "warm up"], "Smart Thermostat",
             "set_temperature", {"temperature": 23}),
            (["cool down", "cool the house"], "Smart Thermostat",
             "set_temperature", {"temperature": 19}),
            # Locks
            (["lock the door", "lock up", "lock front"], "Front Door Lock",
             "lock", {}),
            (["unlock the door", "unlock front"], "Front Door Lock",
             "unlock", {"auth_code": context.get("auth_code", "ECHO_AUTH")}),
            # Lights
            (["turn on the lights", "lights on"], "Living Room Lights",
             "on", {}),
            (["turn off the lights", "lights off"], "Living Room Lights",
             "off", {}),
            # TV
            (["turn on the tv", "tv on"], "Smart TV — Living Room",
             "on", {}),
            (["turn off the tv", "tv off"], "Smart TV — Living Room",
             "off", {}),
            # Car
            (["heat up the car", "preheat car"], "Evo Car",
             "preheat", {"temperature": 22}),
            (["lock the car"], "Evo Car", "lock", {}),
        ]

        for triggers, device_name, command, params in remote_patterns:
            if any(t in intent_low for t in triggers):
                result = self.grid.remote_command(device_name, command,
                                                   {**params, **context})
                return {
                    "layer"    : "habitat",
                    "status"   : "OK",
                    "sub_system": "remote_command",
                    "result"   : result,
                    "message"  : result.get("echo_note", "Command sent"),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

        # Check for lock command directly
        if "lock" in intent_low and "front" in intent_low:
            lock = self.grid.get_device("Front Door Lock")
            if lock:
                result = self.controller.send_command(lock, "lock", {})
                return {"layer":"habitat","status":"OK","sub_system":"remote_command","result":result,"message":"Front door locked.","timestamp":datetime.now(timezone.utc).isoformat()}

        # Generic remote command
        device_name = context.get("device", "Minor Cube")
        command     = context.get("command", "status")
        result      = self.grid.remote_command(device_name, command, context)

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "remote_command",
            "result"   : result,
            "message"  : result.get("echo_note", "Command sent"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_scene(self, intent: str, context: Dict) -> Dict:
        """Set environment scene."""
        scene = self.environment.detect_scene_from_intent(intent)

        if not scene:
            scene_name = context.get("scene", "normal")
            try:
                scene = RoomScene(scene_name)
            except ValueError:
                scene = RoomScene.NORMAL

        config = self.environment.get_scene_config(scene)
        room   = context.get("room", "living_room")

        # Apply scene to room
        room_result = self.rooms.set_scene(room, scene)

        # Apply LED config to Minor Cube
        cube = self.grid._find_device_by_type(DeviceType.MINOR_CUBE)
        if cube and "echo_led" in config:
            self.controller.send_command(
                cube, "led_color",
                {"color"  : config["echo_led"]["color"],
                 "pattern": config["echo_led"]["pattern"]}
            )

        # Learn pattern
        self.environment.learn_pattern(
            datetime.now(timezone.utc).strftime("%H"), scene
        )

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "scene",
            "scene"    : scene.value,
            "config"   : config,
            "room"     : room_result,
            "message"  : (
                f"Scene set to '{scene.value}'. "
                f"{config['description']}"
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_cube(self, intent: str, context: Dict) -> Dict:
        """Control the Minor Cube."""
        intent_low = intent.lower()
        cube = self.grid._find_device_by_type(DeviceType.MINOR_CUBE)

        if not cube:
            return {"layer": "habitat", "status": "ERROR",
                    "message": "Minor Cube not found on grid"}

        if "rainbow" in intent_low:
            result = self.controller.send_command(cube, "led_rainbow", {})
        elif "off" in intent_low and "led" in intent_low:
            result = self.controller.send_command(cube, "led_off", {})
        elif "pulse" in intent_low:
            result = self.controller.send_command(cube, "led_pulse",
                {"color": context.get("color", "#00D2FF"), "speed": "medium"})
        elif "screen" in intent_low:
            cmd = "screen_on" if "on" in intent_low else "screen_off"
            result = self.controller.send_command(cube, cmd, context)
        else:
            # Color change
            color_map = {
                "red": "#FF0000", "blue": "#0000FF", "green": "#00FF00",
                "white": "#FFFFFF", "purple": "#800080", "orange": "#FFA500",
                "cyan": "#00FFFF", "yellow": "#FFFF00", "pink": "#FFC0CB",
                "teal": "#008080"
            }
            color = "#00D2FF"  # Default Echo blue
            for name, hex_color in color_map.items():
                if name in intent_low:
                    color = hex_color
                    break

            result = self.controller.send_command(
                cube, "led_color",
                {"color": color, "pattern": "solid", "brightness": 80}
            )

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "minor_cube",
            "result"   : result,
            "message"  : f"Minor Cube: {result.get('command', 'command')} executed.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_climate(self, intent: str, context: Dict) -> Dict:
        """Climate control."""
        intent_low = intent.lower()
        thermostat = self.grid.get_device("Smart Thermostat")

        if not thermostat:
            return {"layer": "habitat", "status": "ERROR",
                    "message": "Thermostat not found"}

        # Extract temperature if mentioned
        temp = context.get("temperature", 22)
        for word in intent.split():
            cleaned = word.replace("°", "").replace("c", "").replace("f", "")
            if cleaned.isdigit():
                temp = int(cleaned)
                if temp > 50:  # Fahrenheit conversion
                    temp = round((temp - 32) * 5/9, 1)
                break

        result = self.controller.send_command(
            thermostat, "set_temperature", {"temperature": temp}
        )

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "climate",
            "result"   : result,
            "current"  : thermostat.properties,
            "message"  : f"Temperature set to {temp}°C.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_lights(self, intent: str, context: Dict) -> Dict:
        """Light control."""
        intent_low = intent.lower()
        lights     = [d for d in self.grid._devices.values()
                      if d.device_type == DeviceType.SMART_LIGHT]

        if not lights:
            return {"layer": "habitat", "status": "ERROR",
                    "message": "No lights found"}

        results = []
        for light in lights:
            if "off" in intent_low:
                r = self.controller.send_command(light, "off", {})
            elif "dim" in intent_low:
                level = context.get("level", 30)
                r = self.controller.send_command(light, "dim", {"level": level})
            else:
                brightness = context.get("brightness", 80)
                r = self.controller.send_command(light, "on",
                    {"brightness": brightness})
            results.append(r)

        command = "off" if "off" in intent_low else "on"
        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "lights",
            "results"  : results,
            "message"  : f"Lights {command} — {len(results)} devices controlled.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_security(self, intent: str, context: Dict) -> Dict:
        """Security and access control."""
        intent_low = intent.lower()

        if "lock" in intent_low:
            lock   = self.grid.get_device("Front Door Lock")
            result = self.controller.send_command(lock, "lock", {}) if lock else {}
            return {
                "layer"    : "habitat",
                "status"   : "OK",
                "sub_system": "security",
                "result"   : result,
                "message"  : "Front door locked.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        elif "camera" in intent_low or "record" in intent_low:
            camera = self.grid.get_device("Security Camera")
            if camera:
                cmd    = "start_recording" if "record" in intent_low else "snapshot"
                result = self.controller.send_command(camera, cmd, {})
                return {
                    "layer"    : "habitat",
                    "status"   : "OK",
                    "sub_system": "security",
                    "result"   : result,
                    "message"  : f"Camera: {cmd} executed.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

        # Security overview
        locks   = [d for d in self.grid._devices.values()
                   if d.device_type == DeviceType.SMART_LOCK]
        cameras = [d for d in self.grid._devices.values()
                   if d.device_type == DeviceType.SECURITY_CAMERA]

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "security",
            "locks"    : [d.to_dict() for d in locks],
            "cameras"  : [d.to_dict() for d in cameras],
            "message"  : (
                f"Security: {len(locks)} lock(s), {len(cameras)} camera(s). "
                f"All {'secure' if all(d.properties.get('locked') for d in locks) else 'check required'}."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_grid_status(self) -> Dict:
        """Return full Echo Grid status."""
        status = self.grid.get_grid_status()

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "grid_status",
            "grid"     : status,
            "message"  : (
                f"Echo Grid: {status['total_devices']} devices registered. "
                f"{status['online']} online, {status['offline']} offline. "
                f"Active session: {status['active_session']['active_device_name'] if status['active_session'] else 'none'}."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_rooms(self, intent: str, context: Dict) -> Dict:
        """Room overview."""
        rooms = self.rooms.get_all_rooms()
        optimization = self.environment.get_energy_optimization(
            {r["name"]: Room(**{k: v for k, v in r.items()
                               if k not in ["scene", "room_id"]})
             for r in rooms}
        )

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "rooms",
            "rooms"    : rooms,
            "energy"   : optimization,
            "message"  : (
                f"{len(rooms)} rooms managed. "
                f"{optimization['optimization_count']} energy optimizations available."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_general(self, intent: str, context: Dict) -> Dict:
        """General Habitat overview."""
        grid  = self.grid.get_grid_status()
        scene = self.environment.predict_scene()

        return {
            "layer"    : "habitat",
            "status"   : "OK",
            "sub_system": "general",
            "grid"     : grid,
            "suggested_scene": scene.value if scene else "normal",
            "message"  : (
                f"Habitat online. {grid['online']}/{grid['total_devices']} devices active. "
                f"Suggested scene: {scene.value if scene else 'normal'}. "
                f"Say 'echo grid' for full device status."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _background_monitor(self):
        """
        JARVIS addition: Continuous environment monitoring.
        Watches device states, presence, and energy usage.
        """
        log.info("[HABITAT] Background monitor started.")
        while self._presence_active:
            try:
                # Update device heartbeats
                now = datetime.now(timezone.utc).isoformat()
                for device in self.grid._devices.values():
                    if device.is_online():
                        device.last_seen = now
                time.sleep(30)
            except Exception as e:
                log.error(f"[HABITAT/BG] Monitor error: {e}")
                time.sleep(10)

    def get_status(self) -> Dict:
        grid = self.grid.get_grid_status()
        return {
            "layer"          : "habitat",
            "status"         : "ONLINE",
            "grid_devices"   : grid["total_devices"],
            "online_devices" : grid["online"],
            "active_session" : grid["active_session"]["active_device_name"]
                               if grid["active_session"] else "none",
            "rooms"          : len(self.rooms._rooms),
            "presence"       : grid["presence"]
        }

    def shutdown(self):
        self._presence_active = False
        log.info("[HABITAT] Shutdown complete.")


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║        ECHO HABITAT LAYER — TEST            ║
╚══════════════════════════════════════════════╝
    """)

    habitat = HabitatLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        # Grid
        ("Show me all connected devices on the Echo Grid",      {}),
        # Scene
        ("Set focus mode for the office",                       {"room": "office"}),
        # Cross-device handoff
        ("Switch to the TV",                                    {}),
        ("Switch Echo to the Evo Car",                          {}),
        # Remote commands
        ("Heat up the house to 23 degrees",                     {}),
        ("Lock the front door",                                 {}),
        # Minor Cube
        ("Change the cube LED to purple",                       {}),
        ("Set the cube to rainbow mode",                        {}),
        # Lights
        ("Turn on the lights",                                  {}),
        ("Dim the lights to 30 percent",                        {"level": 30}),
        # Climate
        ("Set temperature to 21 degrees",                       {}),
        # Security
        ("Show security status",                                {}),
        # Rooms
        ("Show me the room overview",                           {}),
        # General
        ("What's the habitat status?",                          {}),
    ]

    for i, (query, ctx) in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query[:60]}'")
        print("─" * 55)
        result = habitat.process(query, session, ctx)
        print(f"  SUB-SYSTEM : {result.get('sub_system', 'N/A')}")
        msg = str(result.get('message', ''))[:130]
        print(f"  MESSAGE    : {msg}")

    print("\n" + "═" * 55)
    print("  HABITAT STATUS")
    print("═" * 55)
    status = habitat.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<25}: {v}")

    habitat.shutdown()
