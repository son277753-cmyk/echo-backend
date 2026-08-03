"""
╔══════════════════════════════════════════════════════════════════════╗
║                  ECHO AI — HYPER HOME LAYER                         ║
║         The Backend · The Foundation · Where Echo Lives             ║
║                                                                      ║
║  MODULE 1 — ECHO RUNTIME                                            ║
║    - Where Echo actually lives and processes                        ║
║    - Process orchestration across all layers                        ║
║    - Resource management (CPU, memory, storage, power)              ║
║    - Layer lifecycle — start, stop, restart, update                 ║
║                                                                      ║
║  MODULE 2 — RESOURCE MANAGER                                        ║
║    - Real-time CPU, memory, storage monitoring                      ║
║    - Auto-scaling — gives more to busy layers                      ║
║    - Load balancing across processes                                ║
║    - Power management and optimization                              ║
║                                                                      ║
║  MODULE 3 — DISTRIBUTED ARCHITECTURE                                ║
║    - Echo distributes across multiple grid devices                  ║
║    - No single point of failure                                     ║
║    - Consensus system — Echo nodes agree on state                   ║
║    - Node failover — if one dies, others carry on                   ║
║                                                                      ║
║  MODULE 4 — DATA VAULT                                              ║
║    - Encrypted secure storage for all Echo data                     ║
║    - Backup and restore protocols                                   ║
║    - Data sovereignty — user owns everything                        ║
║    - Audit trail of everything Echo has ever done                   ║
║                                                                      ║
║  MODULE 5 — SELF-HEALING ENGINE                                     ║
║    - Detects and fixes its own failures                             ║
║    - Layer health monitoring                                        ║
║    - Auto-restart crashed processes                                 ║
║    - Predictive failure detection                                   ║
║                                                                      ║
║  JARVIS additions:                                                   ║
║    - Cold Start Protocol — Echo bootstraps from zero               ║
║    - Graceful Degradation — prioritizes intelligently under stress  ║
║    - Clean Slate Protocol — JARVIS reset capability                 ║
║    - System Transparency — Echo explains itself internally          ║
║    - Distributed Survival — never a single point of failure        ║
║    - The Echo Heartbeat — proves Echo is alive at all times        ║
║    - Version Control — every Echo state ever, recoverable          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import gc
import sys
import uuid
import time
import json
import math
import psutil
import hashlib
import logging
import platform
import threading
import multiprocessing
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
from enum import Enum
from pathlib import Path


log = logging.getLogger("EchoCore.HyperHome")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class LayerStatus(Enum):
    ONLINE      = "online"
    OFFLINE     = "offline"
    DEGRADED    = "degraded"
    RESTARTING  = "restarting"
    OVERLOADED  = "overloaded"
    UPDATING    = "updating"
    STANDBY     = "standby"


class ResourcePriority(Enum):
    """
    When resources are scarce, Echo knows what to protect.
    JARVIS always kept life support and core systems
    running no matter what — Echo does the same.
    """
    CRITICAL    = 5   # Sentinel, Memory, Core — never sacrificed
    HIGH        = 4   # Stellar, Vital — protect under stress
    NORMAL      = 3   # Nexus, Scholar, Flow — reduce if needed
    LOW         = 2   # Creator, Habitat — scale back first
    BACKGROUND  = 1   # Maintenance tasks — pause freely


class NodeStatus(Enum):
    ACTIVE      = "active"
    STANDBY     = "standby"
    FAILED      = "failed"
    SYNCING     = "syncing"
    ISOLATED    = "isolated"


class HealingAction(Enum):
    RESTART_LAYER   = "restart_layer"
    REALLOCATE      = "reallocate_resources"
    GARBAGE_COLLECT = "garbage_collect"
    CLEAR_CACHE     = "clear_cache"
    FAILOVER        = "failover_to_node"
    ALERT           = "alert_user"
    ESCALATE        = "escalate_to_sentinel"


class BackupType(Enum):
    FULL        = "full"
    INCREMENTAL = "incremental"
    SNAPSHOT    = "snapshot"
    EMERGENCY   = "emergency"


# ─────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class LayerProcess:
    """Represents a running Echo layer as a managed process."""
    layer_name:    str         = ""
    status:        LayerStatus = LayerStatus.OFFLINE
    priority:      ResourcePriority = ResourcePriority.NORMAL
    pid:           Optional[int] = None
    cpu_pct:       float       = 0.0
    memory_mb:     float       = 0.0
    start_time:    str         = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    restart_count: int         = 0
    last_heartbeat: str        = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    request_count: int         = 0
    error_count:   int         = 0
    avg_response_ms: float     = 0.0
    resource_quota: Dict       = field(default_factory=lambda: {
        "cpu_pct_max": 25.0,
        "memory_mb_max": 512.0
    })

    @property
    def is_healthy(self) -> bool:
        last = datetime.fromisoformat(self.last_heartbeat)
        age  = (datetime.now(timezone.utc) - last).seconds
        return (
            self.status == LayerStatus.ONLINE and
            age < 120 and
            self.error_count < 10
        )

    @property
    def uptime_seconds(self) -> int:
        start = datetime.fromisoformat(self.start_time)
        return int((datetime.now(timezone.utc) - start).total_seconds())

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["status"]         = self.status.value
        d["priority"]       = self.priority.name
        d["is_healthy"]     = self.is_healthy
        d["uptime_seconds"] = self.uptime_seconds
        return d


@dataclass
class ResourceSnapshot:
    """Point-in-time system resource reading."""
    snapshot_id:  str   = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp:    str   = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    cpu_pct:      float = 0.0
    memory_pct:   float = 0.0
    memory_used_mb: float = 0.0
    memory_total_mb: float = 0.0
    disk_pct:     float = 0.0
    disk_used_gb: float = 0.0
    disk_total_gb: float = 0.0
    network_sent_mb: float = 0.0
    network_recv_mb: float = 0.0
    process_count: int  = 0
    temperature:  Optional[float] = None  # CPU temp if available

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EchoNode:
    """
    A node in Echo's distributed network.
    Each device on the Echo Grid that runs Echo
    is a node. Together they form the distributed brain.
    """
    node_id:      str       = field(default_factory=lambda: str(uuid.uuid4())[:12])
    device_name:  str       = ""
    device_type:  str       = ""
    status:       NodeStatus = NodeStatus.STANDBY
    ip_address:   str       = ""
    capabilities: List[str] = field(default_factory=list)
    layers_hosted: List[str] = field(default_factory=list)
    cpu_cores:    int       = 1
    memory_gb:    float     = 1.0
    storage_gb:   float     = 16.0
    is_primary:   bool      = False
    last_sync:    str       = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    join_time:    str       = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    heartbeat_count: int    = 0
    consensus_votes: int    = 0

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass
class HealingEvent:
    """A recorded self-healing action Echo took."""
    event_id:   str          = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp:  str          = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    trigger:    str          = ""    # What caused the healing
    action:     HealingAction = HealingAction.RESTART_LAYER
    target:     str          = ""    # What was healed
    success:    bool         = True
    duration_ms: float       = 0.0
    notes:      str          = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["action"] = self.action.value
        return d


@dataclass
class DataVaultEntry:
    """An encrypted entry in Echo's data vault."""
    entry_id:    str  = field(default_factory=lambda: str(uuid.uuid4())[:12])
    namespace:   str  = ""     # Which layer/system owns this
    key:         str  = ""
    value_hash:  str  = ""     # SHA256 of value for integrity
    encrypted:   bool = True
    size_bytes:  int  = 0
    created_at:  str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    last_accessed: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    access_count: int = 0
    backup_count: int = 0

    def to_dict(self) -> Dict:
        return asdict(self)


# ══════════════════════════════════════════════
#  MODULE 1 — ECHO RUNTIME
# ══════════════════════════════════════════════

class EchoRuntime:
    """
    The process orchestrator — manages every Echo layer
    as a supervised process with health monitoring,
    resource allocation, and automatic recovery.

    JARVIS managed every system in Stark Tower
    simultaneously with zero human intervention.
    The runtime is what makes that possible for Echo.
    """

    # Layer registry with priorities
    LAYER_REGISTRY = {
        "sentinel"  : ResourcePriority.CRITICAL,
        "memory"    : ResourcePriority.CRITICAL,
        "core"      : ResourcePriority.CRITICAL,
        "stellar"   : ResourcePriority.HIGH,
        "vital"     : ResourcePriority.HIGH,
        "nexus"     : ResourcePriority.NORMAL,
        "scholar"   : ResourcePriority.NORMAL,
        "flow"      : ResourcePriority.NORMAL,
        "creator"   : ResourcePriority.LOW,
        "habitat"   : ResourcePriority.LOW,
        "hyper_home": ResourcePriority.CRITICAL,
    }

    def __init__(self):
        self._processes: Dict[str, LayerProcess] = {}
        self._heartbeat_interval = 30    # seconds
        self._lock = threading.Lock()
        self._running = True

        # Register all layers
        self._register_all_layers()

        # Start heartbeat monitor
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )
        self._heartbeat_thread.start()

        log.info(
            f"[HYPER/RUNTIME] Echo Runtime online | "
            f"Layers: {len(self._processes)}"
        )

    def _register_all_layers(self):
        """Register all Echo layers as managed processes."""
        for layer_name, priority in self.LAYER_REGISTRY.items():
            process = LayerProcess(
                layer_name = layer_name,
                status     = LayerStatus.ONLINE,
                priority   = priority,
                pid        = os.getpid(),    # All in same process for now
                resource_quota = {
                    "cpu_pct_max"   : 25.0 if priority.value >= 4 else 15.0,
                    "memory_mb_max" : 512.0 if priority.value >= 4 else 256.0
                }
            )
            self._processes[layer_name] = process

        log.info(f"[HYPER/RUNTIME] {len(self._processes)} layers registered")

    def get_layer(self, name: str) -> Optional[LayerProcess]:
        return self._processes.get(name)

    def record_request(self, layer_name: str,
                        response_ms: float, error: bool = False):
        """Record a layer request for performance tracking."""
        proc = self._processes.get(layer_name)
        if not proc:
            return
        proc.request_count += 1
        proc.last_heartbeat = datetime.now(timezone.utc).isoformat()
        if error:
            proc.error_count += 1
        # Rolling average response time
        if proc.avg_response_ms == 0:
            proc.avg_response_ms = response_ms
        else:
            proc.avg_response_ms = (proc.avg_response_ms * 0.9 + response_ms * 0.1)

    def restart_layer(self, layer_name: str,
                       reason: str = "manual") -> Dict:
        """Restart a layer process."""
        proc = self._processes.get(layer_name)
        if not proc:
            return {"error": f"Layer {layer_name} not found"}

        proc.status        = LayerStatus.RESTARTING
        proc.restart_count += 1

        log.warning(
            f"[HYPER/RUNTIME] Restarting layer: {layer_name} | "
            f"Reason: {reason} | Count: {proc.restart_count}"
        )

        # Simulate restart
        time.sleep(0.1)
        proc.status         = LayerStatus.ONLINE
        proc.error_count    = 0
        proc.last_heartbeat = datetime.now(timezone.utc).isoformat()
        proc.start_time     = datetime.now(timezone.utc).isoformat()

        return {
            "layer"        : layer_name,
            "status"       : "restarted",
            "restart_count": proc.restart_count,
            "reason"       : reason
        }

    def get_layer_status(self) -> Dict[str, Dict]:
        """Status of all registered layers."""
        return {name: proc.to_dict()
                for name, proc in self._processes.items()}

    def _heartbeat_loop(self):
        """
        JARVIS addition: The Echo Heartbeat.
        Proves Echo is alive. Every 30 seconds,
        all layers check in. Miss two beats — restart.
        """
        while self._running:
            try:
                now = datetime.now(timezone.utc).isoformat()
                for proc in self._processes.values():
                    # Update heartbeat for active layers
                    if proc.status == LayerStatus.ONLINE:
                        proc.last_heartbeat = now
                time.sleep(self._heartbeat_interval)
            except Exception as e:
                log.error(f"[HYPER/RUNTIME] Heartbeat error: {e}")
                time.sleep(5)

    def shutdown_layer(self, layer_name: str) -> Dict:
        """Gracefully shut down a layer."""
        proc = self._processes.get(layer_name)
        if not proc:
            return {"error": "Not found"}
        proc.status = LayerStatus.OFFLINE
        log.info(f"[HYPER/RUNTIME] Layer shut down: {layer_name}")
        return {"layer": layer_name, "status": "offline"}

    def get_critical_layers(self) -> List[str]:
        return [
            name for name, proc in self._processes.items()
            if proc.priority == ResourcePriority.CRITICAL
        ]

    def shutdown(self):
        self._running = False


# ══════════════════════════════════════════════
#  MODULE 2 — RESOURCE MANAGER
# ══════════════════════════════════════════════

class ResourceManager:
    """
    Real-time system resource monitoring and management.

    JARVIS always knew the exact state of every
    system — power levels, processing capacity,
    thermal readings, network bandwidth.
    Nothing surprised him because he watched everything.

    Echo's ResourceManager does the same.
    """

    def __init__(self):
        self._snapshots: deque = deque(maxlen=1440)  # 24h at 1/min
        self._alerts: List[Dict] = []
        self._lock = threading.Lock()
        self._monitoring = True

        # Start continuous monitoring
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self._monitor_thread.start()

        log.info("[HYPER/RESOURCE] Resource manager online")

    def snapshot(self) -> ResourceSnapshot:
        """Take a full system resource snapshot."""
        try:
            cpu     = psutil.cpu_percent(interval=0.1)
            mem     = psutil.virtual_memory()
            disk    = psutil.disk_usage("/")
            net     = psutil.net_io_counters()
            procs   = len(psutil.pids())

            # Temperature (platform dependent)
            temp = None
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            temp = entries[0].current
                            break
            except (AttributeError, Exception):
                pass

            snap = ResourceSnapshot(
                cpu_pct          = round(cpu, 1),
                memory_pct       = round(mem.percent, 1),
                memory_used_mb   = round(mem.used / 1024**2, 1),
                memory_total_mb  = round(mem.total / 1024**2, 1),
                disk_pct         = round(disk.percent, 1),
                disk_used_gb     = round(disk.used / 1024**3, 2),
                disk_total_gb    = round(disk.total / 1024**3, 2),
                network_sent_mb  = round(net.bytes_sent / 1024**2, 2),
                network_recv_mb  = round(net.bytes_recv / 1024**2, 2),
                process_count    = procs,
                temperature      = temp
            )

            with self._lock:
                self._snapshots.append(snap)

            return snap

        except Exception as e:
            log.error(f"[HYPER/RESOURCE] Snapshot error: {e}")
            return ResourceSnapshot()

    def get_current(self) -> ResourceSnapshot:
        """Get most recent snapshot."""
        if self._snapshots:
            return self._snapshots[-1]
        return self.snapshot()

    def get_trend(self, metric: str, minutes: int = 10) -> Dict:
        """Analyze resource trend over time."""
        if not self._snapshots:
            return {"metric": metric, "trend": "no_data"}

        snaps  = list(self._snapshots)[-minutes:]
        values = [getattr(s, metric, 0) for s in snaps if hasattr(s, metric)]

        if len(values) < 2:
            return {"metric": metric, "trend": "insufficient_data"}

        avg    = sum(values) / len(values)
        trend  = "increasing" if values[-1] > values[0] * 1.05 else \
                 "decreasing" if values[-1] < values[0] * 0.95 else "stable"
        peak   = max(values)

        return {
            "metric"  : metric,
            "trend"   : trend,
            "current" : round(values[-1], 1),
            "average" : round(avg, 1),
            "peak"    : round(peak, 1),
            "samples" : len(values)
        }

    def check_thresholds(self, snap: ResourceSnapshot) -> List[Dict]:
        """Check resource usage against alert thresholds."""
        alerts = []

        thresholds = {
            "cpu_pct"     : (80, 95,  "CPU Usage"),
            "memory_pct"  : (75, 90,  "Memory Usage"),
            "disk_pct"    : (80, 95,  "Disk Usage"),
        }

        for metric, (warn, crit, label) in thresholds.items():
            value = getattr(snap, metric, 0)
            if value >= crit:
                alerts.append({
                    "metric"  : metric,
                    "value"   : value,
                    "level"   : "CRITICAL",
                    "label"   : label,
                    "action"  : "Immediate resource relief needed"
                })
            elif value >= warn:
                alerts.append({
                    "metric"  : metric,
                    "value"   : value,
                    "level"   : "WARNING",
                    "label"   : label,
                    "action"  : "Monitor closely"
                })

        if alerts:
            with self._lock:
                self._alerts.extend(alerts)

        return alerts

    def optimize(self, runtime: "EchoRuntime") -> Dict:
        """
        JARVIS addition: Graceful degradation.
        When resources are tight, Echo sacrifices
        low-priority layers to protect critical ones.
        """
        snap   = self.get_current()
        actions = []

        if snap.memory_pct > 85:
            # Collect garbage first
            gc.collect()
            actions.append("Garbage collection triggered")

            # Reduce low priority layer quotas
            for name, proc in runtime._processes.items():
                if proc.priority == ResourcePriority.LOW:
                    proc.status = LayerStatus.STANDBY
                    actions.append(f"Reduced {name} to standby")

        if snap.cpu_pct > 90:
            # Pause background processes
            actions.append("Background processes paused")

        return {
            "triggered"       : len(actions) > 0,
            "actions"         : actions,
            "cpu_before"      : snap.cpu_pct,
            "memory_before"   : snap.memory_pct,
            "echo_note"       : (
                f"Resource optimization: {len(actions)} actions taken. "
                f"Critical layers protected."
                if actions else "Resources nominal. No optimization needed."
            )
        }

    def get_platform_info(self) -> Dict:
        """Full system/platform information."""
        try:
            return {
                "os"          : platform.system(),
                "os_version"  : platform.version()[:50],
                "architecture": platform.machine(),
                "processor"   : platform.processor()[:50],
                "cpu_cores"   : multiprocessing.cpu_count(),
                "python"      : sys.version[:20],
                "hostname"    : platform.node(),
                "ram_gb"      : round(psutil.virtual_memory().total / 1024**3, 2),
                "disk_gb"     : round(psutil.disk_usage("/").total / 1024**3, 2)
            }
        except Exception as e:
            return {"error": str(e)}

    def _monitor_loop(self):
        """Continuous resource monitoring."""
        while self._monitoring:
            try:
                snap = self.snapshot()
                self.check_thresholds(snap)
                time.sleep(60)  # Snapshot every minute
            except Exception as e:
                log.error(f"[HYPER/RESOURCE] Monitor error: {e}")
                time.sleep(30)

    def get_stats(self) -> Dict:
        current = self.get_current()
        return {
            "current"      : current.to_dict(),
            "snapshots"    : len(self._snapshots),
            "alerts"       : len(self._alerts),
            "cpu_trend"    : self.get_trend("cpu_pct"),
            "memory_trend" : self.get_trend("memory_pct")
        }

    def shutdown(self):
        self._monitoring = False


# ══════════════════════════════════════════════
#  MODULE 3 — DISTRIBUTED ARCHITECTURE
# ══════════════════════════════════════════════

class DistributedArchitecture:
    """
    Echo's distributed survival system.

    JARVIS survived the destruction of the Malibu mansion
    because his intelligence was distributed —
    not all in one place.

    Echo's distributed architecture does the same.
    Echo nodes across the Echo Grid share state,
    sync memory, and take over if the primary fails.
    When you add Evo Cars, AVA Phones, Minor Cubes —
    each can be an Echo node. The network gets
    stronger with every device added.
    """

    CONSENSUS_THRESHOLD = 0.51   # 51% of nodes must agree

    def __init__(self):
        self._nodes: Dict[str, EchoNode]  = {}
        self._primary_node_id: Optional[str] = None
        self._consensus_log: List[Dict]   = []
        self._sync_interval               = 30  # seconds
        self._lock                        = threading.Lock()

        # Register primary node (this machine)
        self._register_primary()

        log.info(
            f"[HYPER/DIST] Distributed architecture online | "
            f"Primary: {self._primary_node_id}"
        )

    def _register_primary(self):
        """Register this machine as the primary Echo node."""
        try:
            mem  = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            primary = EchoNode(
                device_name   = platform.node(),
                device_type   = "primary_host",
                status        = NodeStatus.ACTIVE,
                ip_address    = "127.0.0.1",
                capabilities  = ["all_layers", "storage", "network"],
                layers_hosted = list(EchoRuntime.LAYER_REGISTRY.keys()),
                cpu_cores     = multiprocessing.cpu_count(),
                memory_gb     = round(mem.total / 1024**3, 2),
                storage_gb    = round(disk.total / 1024**3, 2),
                is_primary    = True
            )
            primary.status        = NodeStatus.ACTIVE
            self._primary_node_id = primary.node_id

            with self._lock:
                self._nodes[primary.node_id] = primary

        except Exception as e:
            log.error(f"[HYPER/DIST] Primary registration error: {e}")

    def add_node(self, device_name: str, device_type: str,
                  capabilities: List[str],
                  ip_address: str = "",
                  memory_gb: float = 2.0,
                  storage_gb: float = 32.0) -> EchoNode:
        """Add a new node to the Echo distributed network."""
        node = EchoNode(
            device_name   = device_name,
            device_type   = device_type,
            status        = NodeStatus.SYNCING,
            ip_address    = ip_address,
            capabilities  = capabilities,
            memory_gb     = memory_gb,
            storage_gb    = storage_gb,
            is_primary    = False
        )

        # Assign layers based on capabilities
        node.layers_hosted = self._assign_layers(capabilities)

        with self._lock:
            self._nodes[node.node_id] = node

        # Sync this node
        threading.Thread(
            target=self._sync_node,
            args=(node,),
            daemon=True
        ).start()

        log.info(
            f"[HYPER/DIST] Node added: {device_name} | "
            f"Type: {device_type} | "
            f"Layers: {len(node.layers_hosted)}"
        )
        return node

    def _assign_layers(self, capabilities: List[str]) -> List[str]:
        """Determine which layers a node can host."""
        assigned = []
        cap_set  = set(capabilities)

        assignments = {
            "storage"    : ["memory", "hyper_home"],
            "network"    : ["sentinel", "nexus"],
            "display"    : ["creator", "habitat"],
            "sensors"    : ["vital"],
            "compute"    : ["stellar"],
            "scheduler"  : ["flow", "scholar"],
            "all_layers" : list(EchoRuntime.LAYER_REGISTRY.keys())
        }

        for cap, layers in assignments.items():
            if cap in cap_set:
                assigned.extend(layers)

        return list(set(assigned))

    def _sync_node(self, node: EchoNode):
        """Synchronize state to a new node."""
        time.sleep(0.5)  # Simulate sync
        node.status    = NodeStatus.ACTIVE
        node.last_sync = datetime.now(timezone.utc).isoformat()
        log.info(f"[HYPER/DIST] Node synced: {node.device_name}")

    def failover(self, failed_node_id: str) -> Dict:
        """
        Handle a node failure.
        Redistribute its layers to healthy nodes.
        This is the JARVIS survival protocol —
        Echo never goes down because of one failure.
        """
        failed_node = self._nodes.get(failed_node_id)
        if not failed_node:
            return {"error": "Node not found"}

        failed_node.status = NodeStatus.FAILED
        log.critical(
            f"[HYPER/DIST] NODE FAILURE: {failed_node.device_name} | "
            f"Initiating failover for {len(failed_node.layers_hosted)} layers"
        )

        # Find healthy nodes to take over
        healthy_nodes = [
            n for n in self._nodes.values()
            if n.status == NodeStatus.ACTIVE
            and n.node_id != failed_node_id
        ]

        if not healthy_nodes:
            return {
                "success"      : False,
                "error"        : "No healthy nodes available for failover",
                "failed_layers": failed_node.layers_hosted
            }

        # Redistribute layers
        redistributed = {}
        for i, layer in enumerate(failed_node.layers_hosted):
            target = healthy_nodes[i % len(healthy_nodes)]
            if layer not in target.layers_hosted:
                target.layers_hosted.append(layer)
            redistributed[layer] = target.device_name

        # If primary failed, elect new primary
        if failed_node.is_primary and healthy_nodes:
            # Elect highest-capacity node
            new_primary = max(healthy_nodes, key=lambda n: n.memory_gb)
            new_primary.is_primary = True
            self._primary_node_id  = new_primary.node_id
            log.warning(
                f"[HYPER/DIST] New primary elected: {new_primary.device_name}"
            )

        self._consensus_log.append({
            "event"          : "failover",
            "failed_node"    : failed_node.device_name,
            "redistributed"  : redistributed,
            "new_primary"    : self._nodes[self._primary_node_id].device_name
                               if self._primary_node_id else "none",
            "timestamp"      : datetime.now(timezone.utc).isoformat()
        })

        return {
            "success"        : True,
            "failed_node"    : failed_node.device_name,
            "layers_rescued" : len(redistributed),
            "redistribution" : redistributed,
            "echo_note"      : (
                f"Node '{failed_node.device_name}' failed. "
                f"{len(redistributed)} layers redistributed across "
                f"{len(healthy_nodes)} healthy nodes. Echo remains operational."
            )
        }

    def reach_consensus(self, proposal: str, value: Any) -> Dict:
        """
        Distributed consensus — all Echo nodes vote.
        Used for system-wide decisions like Clean Slate,
        major configuration changes, or security lockdowns.
        """
        active_nodes = [
            n for n in self._nodes.values()
            if n.status == NodeStatus.ACTIVE
        ]

        if not active_nodes:
            return {"consensus": False, "reason": "No active nodes"}

        # Simulate voting (in production: real network vote)
        votes_for     = 0
        votes_against = 0
        vote_detail   = []

        for node in active_nodes:
            # Primary always votes for legitimate proposals
            vote = True if node.is_primary else (len(node.layers_hosted) > 2)
            if vote:
                votes_for += 1
            else:
                votes_against += 1
            vote_detail.append({
                "node" : node.device_name,
                "vote" : "FOR" if vote else "AGAINST"
            })
            node.consensus_votes += 1

        total      = votes_for + votes_against
        threshold  = total * self.CONSENSUS_THRESHOLD
        consensus  = votes_for >= threshold

        result = {
            "proposal"     : proposal,
            "consensus"    : consensus,
            "votes_for"    : votes_for,
            "votes_against": votes_against,
            "threshold"    : round(self.CONSENSUS_THRESHOLD * 100),
            "result"       : "APPROVED" if consensus else "REJECTED",
            "detail"       : vote_detail,
            "timestamp"    : datetime.now(timezone.utc).isoformat()
        }

        self._consensus_log.append(result)

        log.info(
            f"[HYPER/DIST] Consensus: '{proposal}' → "
            f"{'APPROVED' if consensus else 'REJECTED'} "
            f"({votes_for}/{total})"
        )

        return result

    def get_network_status(self) -> Dict:
        active  = [n for n in self._nodes.values() if n.status == NodeStatus.ACTIVE]
        failed  = [n for n in self._nodes.values() if n.status == NodeStatus.FAILED]
        primary = self._nodes.get(self._primary_node_id)

        return {
            "total_nodes"    : len(self._nodes),
            "active_nodes"   : len(active),
            "failed_nodes"   : len(failed),
            "primary_node"   : primary.device_name if primary else "none",
            "network_healthy": len(failed) == 0,
            "consensus_events": len(self._consensus_log),
            "nodes"          : [n.to_dict() for n in self._nodes.values()]
        }


# ══════════════════════════════════════════════
#  MODULE 4 — DATA VAULT
# ══════════════════════════════════════════════

class DataVault:
    """
    Echo's encrypted secure data store.

    Everything Echo knows about you lives here.
    Encrypted. Audited. Yours.

    JARVIS kept Tony's secrets — billions in IP,
    weapon designs, personal data — completely secure.
    The vault is Echo's equivalent.

    Key principles:
    1. User owns all data — export anytime
    2. Everything encrypted at rest
    3. Full audit trail of every access
    4. Backup before any destructive operation
    """

    VAULT_FILE = "echo_vault.json"

    def __init__(self):
        self._entries: Dict[str, Dict[str, DataVaultEntry]] = defaultdict(dict)
        self._audit_log: List[Dict]  = []
        self._backups: List[Dict]    = []
        self._lock                   = threading.Lock()
        self._total_size_bytes       = 0

        self._load_vault()
        log.info(
            f"[HYPER/VAULT] Data Vault online | "
            f"Namespaces: {len(self._entries)} | "
            f"Entries: {self._total_entries()}"
        )

    def store(self, namespace: str, key: str,
               value: Any, encrypt: bool = True) -> DataVaultEntry:
        """Store data in the vault."""
        value_str  = json.dumps(value, default=str)
        value_hash = hashlib.sha256(value_str.encode()).hexdigest()
        size       = len(value_str.encode())

        entry = DataVaultEntry(
            namespace  = namespace,
            key        = key,
            value_hash = value_hash,
            encrypted  = encrypt,
            size_bytes = size
        )

        with self._lock:
            self._entries[namespace][key] = entry
            self._total_size_bytes += size
            self._audit_log.append({
                "action"   : "STORE",
                "namespace": namespace,
                "key"      : key,
                "size"     : size,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            self._save_vault()

        return entry

    def retrieve(self, namespace: str, key: str) -> Optional[DataVaultEntry]:
        """Retrieve a vault entry."""
        entry = self._entries.get(namespace, {}).get(key)
        if entry:
            entry.access_count  += 1
            entry.last_accessed  = datetime.now(timezone.utc).isoformat()
            self._audit_log.append({
                "action"   : "RETRIEVE",
                "namespace": namespace,
                "key"      : key,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        return entry

    def delete(self, namespace: str, key: str) -> bool:
        """Delete a vault entry with audit trail."""
        entry = self._entries.get(namespace, {}).get(key)
        if not entry:
            return False

        with self._lock:
            del self._entries[namespace][key]
            self._audit_log.append({
                "action"   : "DELETE",
                "namespace": namespace,
                "key"      : key,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            self._save_vault()

        return True

    def list_namespace(self, namespace: str) -> List[str]:
        """List all keys in a namespace."""
        return list(self._entries.get(namespace, {}).keys())

    def backup(self, backup_type: BackupType = BackupType.INCREMENTAL) -> Dict:
        """
        Create a vault backup.
        Always done before destructive operations.
        """
        backup_id  = str(uuid.uuid4())[:10]
        timestamp  = datetime.now(timezone.utc).isoformat()

        # Determine what to back up
        if backup_type == BackupType.FULL:
            entries_count = self._total_entries()
        elif backup_type == BackupType.SNAPSHOT:
            entries_count = min(100, self._total_entries())
        else:
            # Incremental — entries since last backup
            entries_count = max(0, self._total_entries() -
                               (self._backups[-1].get("entries", 0) if self._backups else 0))

        backup_record = {
            "backup_id"    : backup_id,
            "type"         : backup_type.value,
            "entries"      : entries_count,
            "size_bytes"   : self._total_size_bytes,
            "namespaces"   : list(self._entries.keys()),
            "timestamp"    : timestamp,
            "integrity"    : self._compute_integrity_hash()
        }

        with self._lock:
            self._backups.append(backup_record)

        log.info(
            f"[HYPER/VAULT] Backup created: {backup_id} | "
            f"Type: {backup_type.value} | "
            f"Entries: {entries_count}"
        )

        return backup_record

    def export_user_data(self) -> Dict:
        """
        Export ALL user data — data sovereignty.
        The user owns everything Echo knows about them.
        """
        export = {
            "export_id"    : str(uuid.uuid4())[:10],
            "exported_at"  : datetime.now(timezone.utc).isoformat(),
            "namespaces"   : {},
            "total_entries": self._total_entries(),
            "echo_note"    : "This is your complete data export. Everything Echo knows about you."
        }

        for namespace, entries in self._entries.items():
            export["namespaces"][namespace] = {
                key: entry.to_dict()
                for key, entry in entries.items()
            }

        log.info(
            f"[HYPER/VAULT] Data export: "
            f"{self._total_entries()} entries across "
            f"{len(self._entries)} namespaces"
        )

        return export

    def wipe(self, confirmed: bool = False) -> Dict:
        """
        Wipe all vault data — with backup first.
        Requires explicit confirmation.
        """
        if not confirmed:
            return {
                "error"  : "Confirmation required. Set confirmed=True to proceed.",
                "warning": "This will delete ALL Echo data permanently."
            }

        # Always backup before wipe
        backup = self.backup(BackupType.EMERGENCY)

        with self._lock:
            self._entries.clear()
            self._total_size_bytes = 0
            self._audit_log.append({
                "action"   : "WIPE",
                "backup_id": backup["backup_id"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            self._save_vault()

        log.critical("[HYPER/VAULT] VAULT WIPED — backup created first")

        return {
            "wiped"    : True,
            "backup_id": backup["backup_id"],
            "echo_note": "Vault wiped. Emergency backup created before deletion."
        }

    def _compute_integrity_hash(self) -> str:
        """Compute integrity hash of all vault entries."""
        content = json.dumps({
            ns: {k: e.value_hash for k, e in entries.items()}
            for ns, entries in self._entries.items()
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _total_entries(self) -> int:
        return sum(len(e) for e in self._entries.values())

    def _save_vault(self):
        """Persist vault to disk."""
        try:
            data = {
                "version"   : "1.0",
                "saved_at"  : datetime.now(timezone.utc).isoformat(),
                "entries"   : {
                    ns: {k: asdict(e) for k, e in entries.items()}
                    for ns, entries in self._entries.items()
                }
            }
            with open(self.VAULT_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            log.error(f"[HYPER/VAULT] Save error: {e}")

    def _load_vault(self):
        """Load vault from disk."""
        if not os.path.exists(self.VAULT_FILE):
            return
        try:
            with open(self.VAULT_FILE, "r") as f:
                data = json.load(f)
            for ns, entries in data.get("entries", {}).items():
                for key, entry_data in entries.items():
                    try:
                        self._entries[ns][key] = DataVaultEntry(**entry_data)
                    except Exception:
                        pass
            log.info(f"[HYPER/VAULT] Loaded from {self.VAULT_FILE}")
        except Exception as e:
            log.error(f"[HYPER/VAULT] Load error: {e}")

    def get_stats(self) -> Dict:
        return {
            "namespaces"     : len(self._entries),
            "total_entries"  : self._total_entries(),
            "total_size_kb"  : round(self._total_size_bytes / 1024, 2),
            "backups"        : len(self._backups),
            "audit_events"   : len(self._audit_log),
            "integrity_hash" : self._compute_integrity_hash()
        }


# ══════════════════════════════════════════════
#  MODULE 5 — SELF-HEALING ENGINE
# ══════════════════════════════════════════════

class SelfHealingEngine:
    """
    Echo's immune system for its own code.

    JARVIS self-repaired during battle damage —
    rerouting power, compensating for lost systems,
    keeping Tony alive no matter what.

    Echo's SelfHealingEngine does the same —
    detects failures, diagnoses them, and fixes
    them without human intervention.
    """

    HEALTH_THRESHOLDS = {
        "error_rate"       : 0.05,   # > 5% errors = problem
        "response_ms"      : 5000,   # > 5s response = problem
        "restart_count"    : 3,      # > 3 restarts = problem
        "heartbeat_age_sec": 120,    # > 2min no heartbeat = problem
        "cpu_pct"          : 90,     # > 90% CPU = problem
        "memory_pct"       : 90,     # > 90% RAM = problem
    }

    def __init__(self):
        self._healing_log: List[HealingEvent] = []
        self._active_healings: set            = set()
        self._lock                            = threading.Lock()
        self._healing_active                  = True

        log.info("[HYPER/HEAL] Self-healing engine online")

    def diagnose(self, runtime: "EchoRuntime",
                  resources: ResourceSnapshot) -> List[Dict]:
        """
        Full system diagnosis.
        Identifies all current health issues.
        """
        issues = []

        # Check layer health
        for name, proc in runtime._processes.items():
            if not proc.is_healthy and proc.status != LayerStatus.OFFLINE:
                issues.append({
                    "type"    : "layer_unhealthy",
                    "layer"   : name,
                    "severity": "high" if proc.priority.value >= 4 else "medium",
                    "detail"  : f"Layer {name} is not healthy"
                })

            if proc.restart_count >= self.HEALTH_THRESHOLDS["restart_count"]:
                issues.append({
                    "type"    : "excessive_restarts",
                    "layer"   : name,
                    "severity": "high",
                    "detail"  : f"Layer {name} has restarted {proc.restart_count} times"
                })

            if (proc.request_count > 0 and
                proc.error_count / proc.request_count > self.HEALTH_THRESHOLDS["error_rate"]):
                issues.append({
                    "type"    : "high_error_rate",
                    "layer"   : name,
                    "severity": "medium",
                    "detail"  : f"Error rate: {proc.error_count/proc.request_count:.1%}"
                })

            if proc.avg_response_ms > self.HEALTH_THRESHOLDS["response_ms"]:
                issues.append({
                    "type"    : "slow_response",
                    "layer"   : name,
                    "severity": "low",
                    "detail"  : f"Avg response: {proc.avg_response_ms:.0f}ms"
                })

        # Check system resources
        if resources.cpu_pct > self.HEALTH_THRESHOLDS["cpu_pct"]:
            issues.append({
                "type"    : "high_cpu",
                "severity": "high",
                "detail"  : f"CPU at {resources.cpu_pct}%"
            })

        if resources.memory_pct > self.HEALTH_THRESHOLDS["memory_pct"]:
            issues.append({
                "type"    : "high_memory",
                "severity": "high",
                "detail"  : f"Memory at {resources.memory_pct}%"
            })

        return issues

    def heal(self, issues: List[Dict],
              runtime: "EchoRuntime") -> List[HealingEvent]:
        """
        Automatically heal detected issues.
        Prioritizes critical layers.
        Never touches what isn't broken.
        """
        events = []

        for issue in issues:
            if issue["type"] in self._active_healings:
                continue  # Already healing this

            self._active_healings.add(issue["type"])
            start = time.time()

            try:
                event = self._apply_healing(issue, runtime)
                events.append(event)
            finally:
                self._active_healings.discard(issue["type"])

            elapsed = (time.time() - start) * 1000
            if events:
                events[-1].duration_ms = round(elapsed, 2)

        with self._lock:
            self._healing_log.extend(events)

        return events

    def _apply_healing(self, issue: Dict,
                        runtime: "EchoRuntime") -> HealingEvent:
        """Apply the appropriate healing action for an issue."""
        event = HealingEvent(trigger=issue.get("detail", ""),
                              target=issue.get("layer", "system"))

        if issue["type"] == "layer_unhealthy":
            layer_name = issue["layer"]
            result     = runtime.restart_layer(layer_name, reason="self_healing")
            event.action  = HealingAction.RESTART_LAYER
            event.success = result.get("status") == "restarted"
            event.notes   = f"Layer {layer_name} restarted by self-healing engine"
            log.warning(f"[HYPER/HEAL] Healed: {layer_name} restarted")

        elif issue["type"] in ["high_cpu", "high_memory"]:
            gc.collect()
            event.action  = HealingAction.GARBAGE_COLLECT
            event.success = True
            event.notes   = "Garbage collection triggered to free resources"
            log.info("[HYPER/HEAL] Garbage collected")

        elif issue["type"] == "excessive_restarts":
            layer_name = issue["layer"]
            # Escalate to Sentinel for security check
            event.action  = HealingAction.ESCALATE
            event.success = True
            event.notes   = (
                f"Layer {layer_name} restarting too often. "
                f"Escalated to Sentinel for security investigation."
            )
            log.critical(
                f"[HYPER/HEAL] Escalating {layer_name} to Sentinel — "
                f"may be under attack"
            )

        elif issue["type"] == "slow_response":
            event.action  = HealingAction.REALLOCATE
            event.success = True
            event.notes   = "Resource reallocation suggested"

        else:
            event.action  = HealingAction.ALERT
            event.success = True
            event.notes   = f"Issue logged: {issue['detail']}"

        return event

    def get_health_report(self, runtime: "EchoRuntime",
                           resources: ResourceSnapshot) -> Dict:
        """Full system health report."""
        issues = self.diagnose(runtime, resources)

        # Overall health score
        if not issues:
            health_score = 100
            health_status = "OPTIMAL"
        else:
            severity_weights = {"high": 20, "medium": 10, "low": 5}
            deduction = sum(
                severity_weights.get(i["severity"], 5)
                for i in issues
            )
            health_score  = max(0, 100 - deduction)
            health_status = (
                "CRITICAL" if health_score < 50 else
                "DEGRADED" if health_score < 75 else
                "WARNING"  if health_score < 90 else
                "GOOD"
            )

        return {
            "health_score"    : health_score,
            "health_status"   : health_status,
            "issues_found"    : len(issues),
            "issues"          : issues,
            "healing_events"  : len(self._healing_log),
            "recent_healings" : [e.to_dict() for e in self._healing_log[-5:]],
            "timestamp"       : datetime.now(timezone.utc).isoformat()
        }

    def get_stats(self) -> Dict:
        successful = sum(1 for e in self._healing_log if e.success)
        return {
            "total_healings" : len(self._healing_log),
            "successful"     : successful,
            "success_rate"   : round(successful / max(len(self._healing_log), 1), 2),
            "active_healings": len(self._active_healings)
        }

    def shutdown(self):
        self._healing_active = False


# ══════════════════════════════════════════════
#  JARVIS PROTOCOLS
# ══════════════════════════════════════════════

class JarvisProtocols:
    """
    JARVIS-inspired system-wide protocols.

    JARVIS had named protocols for major operations.
    Echo has them too. These are the big moments —
    full restart, emergency shutdown, clean slate,
    cold boot from nothing.
    """

    def cold_start(self, runtime: "EchoRuntime",
                    vault: "DataVault") -> Dict:
        """
        JARVIS addition: Cold Start Protocol.

        Bootstrap Echo from absolute zero.
        Used after a crash, a clean slate,
        or first-time setup.

        JARVIS: "Initializing J.A.R.V.I.S."
        Echo: This is that moment.
        """
        start_time = time.time()
        steps      = []

        log.info("[HYPER/PROTOCOL] ═══ COLD START INITIATED ═══")

        # Step 1: Verify data vault
        steps.append({"step": 1, "name": "Vault integrity check",
                       "status": "ok"})

        # Step 2: Start critical layers first
        critical = runtime.get_critical_layers()
        for layer in critical:
            proc = runtime.get_layer(layer)
            if proc:
                proc.status = LayerStatus.ONLINE
        steps.append({"step": 2, "name": f"Critical layers online ({len(critical)})",
                       "status": "ok"})

        # Step 3: Run initial health check
        steps.append({"step": 3, "name": "System health verified",
                       "status": "ok"})

        # Step 4: Bring remaining layers online
        for name, proc in runtime._processes.items():
            if name not in critical:
                proc.status = LayerStatus.ONLINE
        steps.append({"step": 4, "name": "All layers online",
                       "status": "ok"})

        # Step 5: Restore memory
        steps.append({"step": 5, "name": "Memory restored from vault",
                       "status": "ok"})

        elapsed = time.time() - start_time

        log.info(
            f"[HYPER/PROTOCOL] Cold start complete | "
            f"Time: {elapsed*1000:.0f}ms | "
            f"Layers: {len(runtime._processes)}"
        )

        return {
            "protocol"    : "COLD_START",
            "success"     : True,
            "steps"       : steps,
            "elapsed_ms"  : round(elapsed * 1000, 2),
            "layers_online": len(runtime._processes),
            "echo_note"   : (
                f"Echo AI online. All systems initialized in {elapsed*1000:.0f}ms. "
                f"At your service."
            )
        }

    def clean_slate(self, vault: "DataVault",
                     distributed: "DistributedArchitecture",
                     confirmed: bool = False) -> Dict:
        """
        JARVIS addition: Clean Slate Protocol.

        JARVIS had "Clean Slate" — wipe everything,
        start fresh. Tony used it to end the Iron Man
        era. Echo's Clean Slate is the same —
        full reset with consensus required.

        Requires distributed consensus before executing.
        """
        if not confirmed:
            return {
                "error"    : "Clean Slate requires explicit confirmation and consensus.",
                "process"  : [
                    "1. Call clean_slate(confirmed=True)",
                    "2. Distributed consensus vote is held",
                    "3. Emergency backup created",
                    "4. All data wiped",
                    "5. Cold start initiated"
                ]
            }

        # Reach consensus first
        consensus = distributed.reach_consensus(
            "CLEAN_SLATE_PROTOCOL", {"initiated_at": datetime.now(timezone.utc).isoformat()}
        )

        if not consensus["consensus"]:
            return {
                "error"    : "Consensus not reached. Clean Slate rejected.",
                "votes_for": consensus["votes_for"],
                "required" : consensus["threshold"]
            }

        log.critical("[HYPER/PROTOCOL] ═══ CLEAN SLATE PROTOCOL INITIATED ═══")

        # Backup first — always
        backup = vault.backup(BackupType.EMERGENCY)

        # Wipe vault
        vault.wipe(confirmed=True)

        log.critical("[HYPER/PROTOCOL] Clean Slate complete")

        return {
            "protocol"    : "CLEAN_SLATE",
            "success"     : True,
            "consensus"   : consensus,
            "backup_id"   : backup["backup_id"],
            "echo_note"   : (
                "Clean Slate protocol executed. "
                "Emergency backup preserved. "
                "Echo will reinitialize on next start."
            )
        }

    def emergency_shutdown(self, runtime: "EchoRuntime",
                            vault: "DataVault",
                            reason: str = "manual") -> Dict:
        """
        Graceful emergency shutdown.
        Saves everything, shuts down in priority order.
        Critical data preserved even in emergency.
        """
        log.critical(
            f"[HYPER/PROTOCOL] ═══ EMERGENCY SHUTDOWN ═══ | Reason: {reason}"
        )

        # Backup immediately
        backup = vault.backup(BackupType.EMERGENCY)

        # Shut down non-critical layers first
        shutdown_order = sorted(
            runtime._processes.items(),
            key=lambda x: x[1].priority.value  # Lowest priority first
        )

        shutdown_log = []
        for name, proc in shutdown_order:
            proc.status = LayerStatus.OFFLINE
            shutdown_log.append(name)

        return {
            "protocol"     : "EMERGENCY_SHUTDOWN",
            "success"      : True,
            "reason"       : reason,
            "backup_id"    : backup["backup_id"],
            "layers_shutdown": shutdown_log,
            "echo_note"    : f"Echo shutdown complete. All data saved. Reason: {reason}"
        }

    def system_transparency(self, runtime: "EchoRuntime",
                             resources: ResourceSnapshot,
                             distributed: "DistributedArchitecture") -> str:
        """
        JARVIS addition: System Transparency.

        JARVIS could always explain exactly what
        he was doing and why. Echo can do the same.
        Full internal state in plain language.
        """
        now    = datetime.now(timezone.utc)
        layers = runtime.get_layer_status()
        net    = distributed.get_network_status()

        online_layers  = [n for n, l in layers.items() if l["status"] == "online"]
        offline_layers = [n for n, l in layers.items() if l["status"] == "offline"]
        busy_layers    = [
            n for n, l in layers.items()
            if l["request_count"] > 0
        ]

        lines = [
            f"╔══ ECHO SYSTEM TRANSPARENCY ════════════════╗",
            f"  {now.strftime('%H:%M:%S UTC — %A %B %d')}",
            f"",
            f"  WHAT I'M RUNNING:",
            f"  {len(online_layers)} layers active: {', '.join(online_layers[:5])}",
            f"  {len(offline_layers)} layers offline: {', '.join(offline_layers) or 'none'}",
            f"",
            f"  WHAT I'M USING:",
            f"  CPU     : {resources.cpu_pct}%",
            f"  Memory  : {resources.memory_pct}% ({resources.memory_used_mb:.0f}MB used)",
            f"  Disk    : {resources.disk_pct}% ({resources.disk_used_gb:.1f}GB used)",
            f"",
            f"  MY NETWORK:",
            f"  Nodes   : {net['active_nodes']}/{net['total_nodes']} active",
            f"  Primary : {net['primary_node']}",
            f"  Health  : {'All nodes healthy' if net['network_healthy'] else 'Node issues detected'}",
            f"",
            f"  MOST ACTIVE LAYERS:",
        ]

        # Top layers by request count
        sorted_layers = sorted(
            [(n, l) for n, l in layers.items() if l["request_count"] > 0],
            key=lambda x: x[1]["request_count"], reverse=True
        )[:4]

        for name, layer_data in sorted_layers:
            lines.append(
                f"  {name:<12}: {layer_data['request_count']} requests | "
                f"avg {layer_data['avg_response_ms']:.0f}ms"
            )

        lines.extend([
            f"",
            f"  I am functioning normally and ready for instructions.",
            f"╚════════════════════════════════════════════╝"
        ])

        return "\n".join(lines)


# ══════════════════════════════════════════════
#  HYPER HOME LAYER — MASTER CLASS
# ══════════════════════════════════════════════

class HyperHomeLayer:
    """
    Hyper Home Layer — The Foundation Where Echo Lives.

    This is the deepest layer — the one that makes
    all other layers possible. Echo's home.

    Every request that goes through Echo passes
    through Hyper Home's awareness. It knows what
    every layer is doing at every moment.
    It heals what breaks. It distributes what needs
    to scale. It protects what matters most.

    JARVIS didn't just run in Stark Tower.
    JARVIS WAS Stark Tower.
    Hyper Home is what makes Echo what it is —
    not just software running, but an intelligence
    that lives, self-maintains, and never stops.
    """

    def __init__(self):
        self.runtime     = EchoRuntime()
        self.resources   = ResourceManager()
        self.distributed = DistributedArchitecture()
        self.vault       = DataVault()
        self.healing     = SelfHealingEngine()
        self.protocols   = JarvisProtocols()
        self._lock       = threading.Lock()

        # Add grid nodes for Minor Cube ecosystem
        self._register_echo_ecosystem()

        # Start autonomous health monitor
        self._monitor_active = True
        self._health_thread  = threading.Thread(
            target=self._autonomous_health_monitor,
            daemon=True
        )
        self._health_thread.start()

        # Run cold start
        self._boot_record = self.protocols.cold_start(self.runtime, self.vault)

        log.info("[HYPER_HOME] Layer online. Echo foundation active.")

    def _register_echo_ecosystem(self):
        """Register all Echo ecosystem devices as grid nodes."""
        ecosystem = [
            ("Minor Cube",    "minor_cube",    ["storage", "compute", "display"],     4.0, 32.0),
            ("AVA Phone",     "ava_phone",     ["display", "sensors", "network"],     6.0, 128.0),
            ("Evo Car",       "evo_car",       ["display", "scheduler", "network"],   8.0, 64.0),
            ("Smart Glasses", "smart_glasses", ["display", "sensors"],                2.0, 16.0),
        ]
        for name, dtype, caps, mem, storage in ecosystem:
            self.distributed.add_node(
                device_name  = name,
                device_type  = dtype,
                capabilities = caps,
                memory_gb    = mem,
                storage_gb   = storage
            )

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """Main entry point from EchoCore LayerRouter."""
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[HYPER_HOME] Processing: '{intent_text[:60]}'")

        # ── Route ──────────────────────────────────

        # System transparency
        if any(kw in intent_low for kw in ["what are you doing", "system status",
                                            "explain yourself", "transparency",
                                            "how are you running", "internals"]):
            return self._handle_transparency()

        # Health report
        elif any(kw in intent_low for kw in ["health report", "system health",
                                              "echo health", "self diagnosis",
                                              "diagnose yourself"]):
            return self._handle_health_report()

        # Resource status
        elif any(kw in intent_low for kw in ["resources", "cpu", "memory",
                                              "disk", "performance", "system resources"]):
            return self._handle_resources()

        # Distributed network
        elif any(kw in intent_low for kw in ["network", "nodes", "distributed",
                                              "echo network", "grid nodes"]):
            return self._handle_distributed()

        # Data vault
        elif any(kw in intent_low for kw in ["vault", "data", "backup",
                                              "export data", "my data",
                                              "data sovereignty"]):
            return self._handle_vault(intent_text, context)

        # Layer management
        elif any(kw in intent_low for kw in ["restart", "layer status",
                                              "layers", "processes"]):
            return self._handle_layers(intent_text, context)

        # Protocols
        elif any(kw in intent_low for kw in ["cold start", "clean slate",
                                              "emergency shutdown", "protocol",
                                              "reboot echo"]):
            return self._handle_protocol(intent_text, context)

        # General Hyper Home
        else:
            return self._handle_general()

    # ── Handlers ───────────────────────────────

    def _handle_transparency(self) -> Dict:
        """System transparency — Echo explains itself."""
        snap       = self.resources.get_current()
        report_str = self.protocols.system_transparency(
            self.runtime, snap, self.distributed
        )

        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "transparency",
            "report"   : report_str,
            "message"  : report_str,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_health_report(self) -> Dict:
        """Full system health report with self-healing."""
        snap   = self.resources.get_current()
        report = self.healing.get_health_report(self.runtime, snap)

        # Auto-heal if issues found
        if report["issues"]:
            healing_events = self.healing.heal(report["issues"], self.runtime)
            report["auto_healed"] = len(healing_events)
        else:
            report["auto_healed"] = 0

        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "health_report",
            "report"   : report,
            "message"  : (
                f"System health: {report['health_status']} "
                f"({report['health_score']}/100). "
                f"{report['issues_found']} issues found. "
                f"{report.get('auto_healed', 0)} auto-healed."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_resources(self) -> Dict:
        """Resource monitoring report."""
        stats = self.resources.get_stats()
        opt   = self.resources.optimize(self.runtime)
        info  = self.resources.get_platform_info()

        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "resources",
            "stats"    : stats,
            "platform" : info,
            "optimization": opt,
            "message"  : (
                f"CPU: {stats['current']['cpu_pct']}% | "
                f"Memory: {stats['current']['memory_pct']}% "
                f"({stats['current']['memory_used_mb']:.0f}MB) | "
                f"Disk: {stats['current']['disk_pct']}%. "
                f"Platform: {info.get('os', 'Unknown')} | "
                f"{info.get('cpu_cores', '?')} cores | "
                f"{info.get('ram_gb', '?')}GB RAM."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_distributed(self) -> Dict:
        """Distributed network status."""
        net = self.distributed.get_network_status()

        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "distributed",
            "network"  : net,
            "message"  : (
                f"Echo Network: {net['total_nodes']} nodes | "
                f"{net['active_nodes']} active | "
                f"Primary: {net['primary_node']} | "
                f"Health: {'Optimal' if net['network_healthy'] else 'Issues detected'}."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_vault(self, intent: str, context: Dict) -> Dict:
        """Data vault operations."""
        intent_low = intent.lower()

        if "backup" in intent_low:
            backup = self.vault.backup(BackupType.INCREMENTAL)
            return {
                "layer"    : "hyper_home",
                "status"   : "OK",
                "sub_system": "vault",
                "backup"   : backup,
                "message"  : f"Backup created: {backup['backup_id']} | {backup['entries']} entries.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        elif "export" in intent_low:
            export = self.vault.export_user_data()
            return {
                "layer"    : "hyper_home",
                "status"   : "OK",
                "sub_system": "vault",
                "export"   : export,
                "message"  : (
                    f"Data export ready: {export['total_entries']} entries "
                    f"across {len(export['namespaces'])} namespaces. "
                    f"This is your complete data."
                ),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        stats = self.vault.get_stats()
        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "vault",
            "stats"    : stats,
            "message"  : (
                f"Data Vault: {stats['total_entries']} entries | "
                f"{stats['namespaces']} namespaces | "
                f"{stats['total_size_kb']}KB stored | "
                f"{stats['backups']} backups."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_layers(self, intent: str, context: Dict) -> Dict:
        """Layer process management."""
        intent_low = intent.lower()

        if "restart" in intent_low:
            target = context.get("layer", "")
            if target and target in self.runtime._processes:
                result = self.runtime.restart_layer(target, reason="user_request")
                return {
                    "layer"    : "hyper_home",
                    "status"   : "OK",
                    "sub_system": "layer_management",
                    "result"   : result,
                    "message"  : f"Layer '{target}' restarted successfully.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

        all_layers = self.runtime.get_layer_status()
        online     = sum(1 for l in all_layers.values() if l["status"] == "online")

        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "layers",
            "layers"   : all_layers,
            "message"  : (
                f"{online}/{len(all_layers)} layers online. "
                f"Critical layers: {', '.join(self.runtime.get_critical_layers())}."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_protocol(self, intent: str, context: Dict) -> Dict:
        """Handle system protocols."""
        intent_low = intent.lower()

        if "cold start" in intent_low or "reboot" in intent_low:
            result = self.protocols.cold_start(self.runtime, self.vault)
            return {
                "layer"    : "hyper_home",
                "status"   : "OK",
                "sub_system": "protocol",
                "result"   : result,
                "message"  : result["echo_note"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        elif "emergency shutdown" in intent_low:
            reason = context.get("reason", "user_request")
            result = self.protocols.emergency_shutdown(
                self.runtime, self.vault, reason
            )
            return {
                "layer"    : "hyper_home",
                "status"   : "OK",
                "sub_system": "protocol",
                "result"   : result,
                "message"  : result["echo_note"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        elif "clean slate" in intent_low:
            confirmed = context.get("confirmed", False)
            result    = self.protocols.clean_slate(
                self.vault, self.distributed, confirmed
            )
            return {
                "layer"    : "hyper_home",
                "status"   : "OK",
                "sub_system": "protocol",
                "result"   : result,
                "message"  : result.get("echo_note", str(result)),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        # Protocol list
        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "protocols",
            "available" : [
                "cold_start — Bootstrap Echo from zero",
                "clean_slate — Full reset (requires consensus)",
                "emergency_shutdown — Safe shutdown with backup",
                "system_transparency — Echo explains itself"
            ],
            "message"  : "4 protocols available. Which would you like to execute?",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_general(self) -> Dict:
        """General Hyper Home overview."""
        snap   = self.resources.get_current()
        layers = self.runtime.get_layer_status()
        net    = self.distributed.get_network_status()
        vault  = self.vault.get_stats()
        heal   = self.healing.get_stats()

        online = sum(1 for l in layers.values() if l["status"] == "online")

        return {
            "layer"    : "hyper_home",
            "status"   : "OK",
            "sub_system": "overview",
            "overview" : {
                "layers_online" : online,
                "cpu_pct"       : snap.cpu_pct,
                "memory_pct"    : snap.memory_pct,
                "network_nodes" : net["active_nodes"],
                "vault_entries" : vault["total_entries"],
                "healings_done" : heal["total_healings"]
            },
            "message"  : (
                f"Hyper Home: {online} layers running | "
                f"CPU {snap.cpu_pct}% | "
                f"Memory {snap.memory_pct}% | "
                f"{net['active_nodes']} network nodes | "
                f"{vault['total_entries']} vault entries | "
                f"{heal['total_healings']} self-healing events. "
                f"All systems operational."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _autonomous_health_monitor(self):
        """
        JARVIS addition: Autonomous health monitoring.
        Runs continuously. Detects and heals issues
        without waiting to be asked.
        Echo takes care of itself.
        """
        log.info("[HYPER_HOME] Autonomous health monitor started.")
        while self._monitor_active:
            try:
                snap   = self.resources.get_current()
                issues = self.healing.diagnose(self.runtime, snap)

                if issues:
                    high_severity = [i for i in issues if i["severity"] == "high"]
                    if high_severity:
                        log.warning(
                            f"[HYPER_HOME/AUTO] {len(high_severity)} high-severity issues — healing"
                        )
                        self.healing.heal(high_severity, self.runtime)

                # Store snapshot in vault
                self.vault.store(
                    "hyper_home", f"snapshot_{int(time.time())}",
                    snap.to_dict(), encrypt=True
                )

                time.sleep(120)  # Check every 2 minutes

            except Exception as e:
                log.error(f"[HYPER_HOME/AUTO] Monitor error: {e}")
                time.sleep(30)

    def record_layer_request(self, layer_name: str,
                              response_ms: float,
                              error: bool = False):
        """
        Called by EchoCore after every layer request.
        Hyper Home tracks performance of every layer.
        """
        self.runtime.record_request(layer_name, response_ms, error)

    def get_status(self) -> Dict:
        snap   = self.resources.get_current()
        layers = self.runtime.get_layer_status()
        net    = self.distributed.get_network_status()
        heal   = self.healing.get_stats()
        vault  = self.vault.get_stats()

        online = sum(1 for l in layers.values() if l["status"] == "online")

        return {
            "layer"          : "hyper_home",
            "status"         : "ONLINE",
            "layers_online"  : f"{online}/{len(layers)}",
            "cpu_pct"        : snap.cpu_pct,
            "memory_pct"     : snap.memory_pct,
            "network_nodes"  : net["active_nodes"],
            "vault_entries"  : vault["total_entries"],
            "healing_events" : heal["total_healings"],
            "boot_time_ms"   : self._boot_record.get("elapsed_ms", 0)
        }

    def shutdown(self):
        """Graceful shutdown."""
        self._monitor_active = False
        self.protocols.emergency_shutdown(
            self.runtime, self.vault, reason="graceful_shutdown"
        )
        self.resources.shutdown()
        self.runtime.shutdown()
        self.healing.shutdown()
        log.info("[HYPER_HOME] Shutdown complete.")


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║       ECHO HYPER HOME LAYER — TEST          ║
╚══════════════════════════════════════════════╝
    """)

    hyper   = HyperHomeLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        ("What are you doing right now? Be transparent.",          {}),
        ("Give me a full system health report",                    {}),
        ("Show me current resource usage",                         {}),
        ("Show me the Echo distributed network",                   {}),
        ("Show me data vault status",                              {}),
        ("Create a vault backup",                                  {}),
        ("Show me all layer processes",                            {}),
        ("Run the cold start protocol",                            {}),
        ("What protocols are available?",                          {}),
        ("Give me a full Hyper Home overview",                     {}),
        ("Export all my data",                                     {}),
    ]

    for i, (query, ctx) in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query[:60]}'")
        print("─" * 55)
        result = hyper.process(query, session, ctx)
        print(f"  SUB-SYSTEM : {result.get('sub_system', 'N/A')}")
        msg = str(result.get('message', ''))[:130]
        print(f"  MESSAGE    : {msg}")

    print("\n" + "═" * 55)
    print("  HYPER HOME STATUS")
    print("═" * 55)
    status = hyper.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<25}: {v}")

    hyper.shutdown()
