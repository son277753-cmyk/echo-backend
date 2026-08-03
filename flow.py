"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ECHO AI — FLOW LAYER                             ║
║         Automation · Routines · Scheduling · Workflow Engine        ║
║                                                                      ║
║  MODULE 1 — ROUTINE ENGINE                                          ║
║    - Morning, evening, custom routines                              ║
║    - Auto-triggered by time, event, or condition                    ║
║    - Chains tasks into seamless sequences                           ║
║    - Adapts routines based on context                               ║
║                                                                      ║
║  MODULE 2 — TASK & SCHEDULE MANAGER                                 ║
║    - Full calendar and reminder system                              ║
║    - Priority queuing — Echo knows what matters most               ║
║    - Deadline tracking with proactive alerts                        ║
║    - Recurring task management                                      ║
║                                                                      ║
║  MODULE 3 — WORKFLOW ENGINE                                         ║
║    - Multi-step automated workflows                                 ║
║    - If-this-then-that conditional logic                            ║
║    - Cross-layer triggers (Flow → Nexus, Vital, Scholar, Creator)  ║
║    - Parallel and sequential execution                              ║
║                                                                      ║
║  MODULE 4 — NOTIFICATION & ALERT SYSTEM                            ║
║    - Smart notification batching                                    ║
║    - Priority-based delivery                                        ║
║    - Do Not Disturb / Focus mode                                    ║
║                                                                      ║
║  JARVIS additions:                                                   ║
║    - Predictive scheduling — Echo suggests routines from patterns   ║
║    - Habit formation engine — builds positive routines over time    ║
║    - Energy-aware scheduling — matches tasks to energy levels       ║
║    - Interruption management — guards your focus time              ║
║    - Proactive briefings — daily summary before you ask            ║
║    - Autonomous execution — Flow runs without being asked          ║
║    - Cross-layer automation — triggers other Echo layers           ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import uuid
import time
import json
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


log = logging.getLogger("EchoCore.Flow")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class Priority(Enum):
    LOW      = 1
    NORMAL   = 2
    HIGH     = 3
    URGENT   = 4
    CRITICAL = 5


class TaskStatus(Enum):
    PENDING     = "pending"
    IN_PROGRESS = "in_progress"
    DONE        = "done"
    SKIPPED     = "skipped"
    FAILED      = "failed"
    CANCELLED   = "cancelled"


class TriggerType(Enum):
    TIME        = "time"         # At a specific time
    INTERVAL    = "interval"     # Every N minutes/hours
    EVENT       = "event"        # When something happens
    CONDITION   = "condition"    # When condition is true
    MANUAL      = "manual"       # User triggered
    LAYER       = "layer"        # Triggered by another layer


class EnergyLevel(Enum):
    """
    JARVIS addition: Energy-aware scheduling.
    Tasks are matched to the user's energy level.
    High-focus work goes in high-energy windows.
    """
    PEAK        = 5   # Full focus — deep work
    HIGH        = 4   # Good energy — complex tasks
    MODERATE    = 3   # Average — meetings, emails
    LOW         = 2   # Tired — light tasks, admin
    REST        = 1   # Recovery — no work tasks


class RecurrenceType(Enum):
    NONE        = "none"
    DAILY       = "daily"
    WEEKDAYS    = "weekdays"
    WEEKENDS    = "weekends"
    WEEKLY      = "weekly"
    MONTHLY     = "monthly"
    CUSTOM      = "custom"


# ─────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class Task:
    """A single unit of work to be done."""
    task_id:      str         = field(default_factory=lambda: str(uuid.uuid4())[:10])
    title:        str         = ""
    description:  str         = ""
    priority:     Priority    = Priority.NORMAL
    status:       TaskStatus  = TaskStatus.PENDING
    due_at:       Optional[str] = None
    created_at:   str         = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: Optional[str] = None
    tags:         List[str]   = field(default_factory=list)
    recurrence:   RecurrenceType = RecurrenceType.NONE
    layer_trigger: Optional[str] = None   # Which layer to call on completion
    estimated_minutes: int    = 15
    energy_required: int      = 3         # 1-5

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["priority"]   = self.priority.name
        d["status"]     = self.status.value
        d["recurrence"] = self.recurrence.value
        return d


@dataclass
class Reminder:
    """A time-based alert."""
    reminder_id:  str   = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title:        str   = ""
    message:      str   = ""
    remind_at:    str   = ""
    recurrence:   RecurrenceType = RecurrenceType.NONE
    priority:     Priority = Priority.NORMAL
    triggered:    bool  = False
    snoozed_until: Optional[str] = None
    created_at:   str   = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["priority"]   = self.priority.name
        d["recurrence"] = self.recurrence.value
        return d


@dataclass
class RoutineStep:
    """One step inside a routine."""
    step_id:      str   = field(default_factory=lambda: str(uuid.uuid4())[:6])
    order:        int   = 0
    title:        str   = ""
    action:       str   = ""          # What Echo does
    duration_min: int   = 5
    layer_call:   Optional[str] = None  # Which Echo layer handles this
    params:       Dict  = field(default_factory=dict)
    optional:     bool  = False
    completed:    bool  = False

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Routine:
    """
    A named sequence of steps that runs automatically.
    JARVIS managed Tony's entire schedule through routines.
    """
    routine_id:   str   = field(default_factory=lambda: str(uuid.uuid4())[:10])
    name:         str   = ""
    description:  str   = ""
    trigger_type: TriggerType = TriggerType.TIME
    trigger_value: str  = ""          # Time, interval, or event name
    steps:        List[RoutineStep] = field(default_factory=list)
    active:       bool  = True
    last_run:     Optional[str] = None
    run_count:    int   = 0
    recurrence:   RecurrenceType = RecurrenceType.DAILY
    tags:         List[str] = field(default_factory=list)
    created_at:   str   = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def total_duration(self) -> int:
        return sum(s.duration_min for s in self.steps)

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["trigger_type"] = self.trigger_type.value
        d["recurrence"]   = self.recurrence.value
        d["total_minutes"]= self.total_duration()
        return d


@dataclass
class WorkflowStep:
    """One step in an automated workflow."""
    step_id:     str  = field(default_factory=lambda: str(uuid.uuid4())[:6])
    name:        str  = ""
    action:      str  = ""
    layer:       str  = "core"
    params:      Dict = field(default_factory=dict)
    condition:   Optional[str] = None   # Run only if condition met
    on_success:  Optional[str] = None   # Next step on success
    on_failure:  Optional[str] = None   # Next step on failure
    timeout_sec: int  = 30
    result:      Optional[Dict] = None
    status:      str  = "pending"


@dataclass
class Workflow:
    """
    A multi-step automated process.
    Workflows connect multiple Echo layers together
    into a single automated pipeline.

    Example: Market Opens →
      Nexus scans portfolio →
      Stellar analyzes risks →
      Flow sends morning briefing
    """
    workflow_id:  str  = field(default_factory=lambda: str(uuid.uuid4())[:10])
    name:         str  = ""
    description:  str  = ""
    trigger:      str  = ""
    steps:        List[WorkflowStep] = field(default_factory=list)
    active:       bool = True
    parallel:     bool = False    # Run steps in parallel or sequence
    last_run:     Optional[str] = None
    run_count:    int  = 0
    created_at:   str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        return asdict(self)


# ══════════════════════════════════════════════
#  MODULE 1 — ROUTINE ENGINE
# ══════════════════════════════════════════════

class RoutineEngine:
    """
    Builds and executes life routines automatically.

    JARVIS managed Tony's entire schedule —
    the Malibu house had protocols for everything.
    Wake protocol. Suit-up protocol. Party protocol.

    Echo's RoutineEngine does the same —
    runs sequences of actions automatically,
    adapts them to context, and learns what
    works best for the user over time.
    """

    # Pre-built routine templates
    ROUTINE_TEMPLATES = {
        "morning_power"  : {
            "name"       : "Morning Power Routine",
            "description": "Start the day at full capacity",
            "trigger"    : "06:00",
            "steps"      : [
                ("Wake up check",      "vital",   "Check overnight health metrics",              2),
                ("Morning brief",      "nexus",   "Market overview + overnight alerts",          3),
                ("Daily priorities",   "flow",    "Top 3 tasks for today",                       2),
                ("Weather + news",     "stellar", "Today's context — weather, news, key events", 3),
                ("Study session",      "scholar", "15min learning — topic from your queue",      15),
                ("Workout reminder",   "vital",   "Today's fitness plan",                        1),
            ]
        },
        "morning_chill"  : {
            "name"       : "Morning Ease-In",
            "description": "Gentle start — no rush",
            "trigger"    : "08:00",
            "steps"      : [
                ("Health check",       "vital",   "Quick vitals scan",                           1),
                ("Affirmation",        "creator", "Today's motivational message",                1),
                ("Light brief",        "nexus",   "Key numbers only",                            2),
                ("Today's plan",       "flow",    "Schedule overview",                           2),
            ]
        },
        "focus_block"    : {
            "name"       : "Deep Focus Protocol",
            "description": "Maximum concentration mode — zero interruptions",
            "trigger"    : "manual",
            "steps"      : [
                ("Focus mode on",      "flow",    "Block all non-critical notifications",        1),
                ("Task load",          "flow",    "Load highest priority task",                  1),
                ("Pomodoro start",     "flow",    "Start 25-minute focus timer",                 25),
                ("Break",              "vital",   "5-minute movement break",                     5),
                ("Repeat or end",      "flow",    "Continue or close focus session",             1),
            ]
        },
        "evening_wind"   : {
            "name"       : "Evening Wind Down",
            "description": "End the day right — process, reflect, prepare",
            "trigger"    : "21:00",
            "steps"      : [
                ("Day review",         "flow",    "Tasks completed vs planned",                  3),
                ("Tomorrow prep",      "flow",    "Top 3 for tomorrow — set now",                3),
                ("Portfolio check",    "nexus",   "End-of-day financial summary",                2),
                ("Health summary",     "vital",   "Today's health metrics review",               2),
                ("Learning recap",     "scholar", "What did you learn today?",                   2),
                ("Sleep prep",         "vital",   "Wind-down recommendations",                   2),
            ]
        },
        "workout"        : {
            "name"       : "Workout Protocol",
            "description": "Pre and post workout automation",
            "trigger"    : "manual",
            "steps"      : [
                ("Pre-workout check",  "vital",   "Heart rate + energy level check",             1),
                ("Workout plan",       "vital",   "Today's session based on recovery data",      2),
                ("Music",              "creator", "DJ Mode — workout playlist",                  1),
                ("Timer set",          "flow",    "Workout timer started",                       45),
                ("Cool down",          "vital",   "Cool-down protocol",                          10),
                ("Log results",        "vital",   "Record workout metrics",                      2),
            ]
        },
        "security_check" : {
            "name"       : "Security Sweep",
            "description": "JARVIS-level system security check",
            "trigger"    : "03:00",
            "steps"      : [
                ("System scan",        "vital",   "Full Echo system health scan",                3),
                ("Threat check",       "sentinel","Active threat assessment",                    2),
                ("Port audit",         "sentinel","USB and connection audit",                    2),
                ("Memory optimize",    "flow",    "Clear temp data, optimize storage",           3),
                ("Report",             "flow",    "Security report ready for morning",           1),
            ]
        }
    }

    def __init__(self):
        self._routines: Dict[str, Routine]  = {}
        self._running: set                  = set()
        self._execution_log: List[Dict]     = []
        self._lock                          = threading.Lock()

        # Load default routines
        self._load_default_routines()

    def _load_default_routines(self):
        """Pre-load useful default routines."""
        for template_key, template in self.ROUTINE_TEMPLATES.items():
            routine = self._build_from_template(template)
            self._routines[routine.routine_id] = routine

        log.info(f"[FLOW/ROUTINE] Loaded {len(self._routines)} default routines")

    def _build_from_template(self, template: Dict) -> Routine:
        """Build a Routine from a template dict."""
        steps = []
        for i, (title, layer, action, duration) in enumerate(template["steps"]):
            steps.append(RoutineStep(
                order        = i,
                title        = title,
                action       = action,
                layer_call   = layer,
                duration_min = duration
            ))

        trigger = template["trigger"]
        trigger_type = TriggerType.MANUAL if trigger == "manual" else TriggerType.TIME

        return Routine(
            name         = template["name"],
            description  = template["description"],
            trigger_type = trigger_type,
            trigger_value= trigger,
            steps        = steps,
            recurrence   = RecurrenceType.DAILY,
            tags         = [template["name"].lower().replace(" ", "_")]
        )

    def create_routine(self, name: str, trigger_time: str,
                       steps: List[Dict],
                       recurrence: RecurrenceType = RecurrenceType.DAILY) -> Routine:
        """Create a custom routine."""
        routine_steps = []
        for i, step_data in enumerate(steps):
            routine_steps.append(RoutineStep(
                order        = i,
                title        = step_data.get("title", f"Step {i+1}"),
                action       = step_data.get("action", ""),
                layer_call   = step_data.get("layer", "flow"),
                duration_min = step_data.get("duration", 5),
                optional     = step_data.get("optional", False)
            ))

        routine = Routine(
            name         = name,
            trigger_type = TriggerType.TIME,
            trigger_value= trigger_time,
            steps        = routine_steps,
            recurrence   = recurrence
        )

        with self._lock:
            self._routines[routine.routine_id] = routine

        log.info(
            f"[FLOW/ROUTINE] Created: '{name}' | "
            f"Trigger: {trigger_time} | Steps: {len(routine_steps)}"
        )
        return routine

    def execute_routine(self, routine_id: str,
                         layer_executor: Optional[Callable] = None) -> Dict:
        """
        Execute a routine — runs all steps in sequence.
        Optionally calls real layer handlers for each step.
        """
        routine = self._routines.get(routine_id)
        if not routine:
            return {"error": f"Routine {routine_id} not found"}

        if routine_id in self._running:
            return {"status": "already_running", "routine": routine.name}

        start_time = time.time()
        self._running.add(routine_id)

        log.info(f"[FLOW/ROUTINE] Starting: '{routine.name}' ({len(routine.steps)} steps)")

        results = []
        for step in sorted(routine.steps, key=lambda s: s.order):
            step_result = self._execute_step(step, layer_executor)
            results.append(step_result)
            step.completed = step_result.get("success", False)

            # Small delay between steps
            time.sleep(0.05)

        elapsed = time.time() - start_time
        routine.last_run  = datetime.now(timezone.utc).isoformat()
        routine.run_count += 1

        self._running.discard(routine_id)

        execution_record = {
            "routine_id"  : routine_id,
            "name"        : routine.name,
            "steps_total" : len(routine.steps),
            "steps_done"  : sum(1 for r in results if r.get("success")),
            "elapsed_ms"  : round(elapsed * 1000, 2),
            "timestamp"   : routine.last_run,
            "results"     : results
        }

        with self._lock:
            self._execution_log.append(execution_record)

        log.info(
            f"[FLOW/ROUTINE] Complete: '{routine.name}' | "
            f"{execution_record['steps_done']}/{execution_record['steps_total']} steps | "
            f"{elapsed*1000:.0f}ms"
        )

        return execution_record

    def _execute_step(self, step: RoutineStep,
                       layer_executor: Optional[Callable]) -> Dict:
        """Execute one routine step."""
        log.debug(f"[FLOW/ROUTINE] Step: '{step.title}' → [{step.layer_call}]")

        result = {
            "step"    : step.title,
            "layer"   : step.layer_call,
            "action"  : step.action,
            "success" : True
        }

        if layer_executor and step.layer_call:
            try:
                layer_result = layer_executor(
                    layer  = step.layer_call,
                    action = step.action,
                    params = step.params
                )
                result["layer_response"] = layer_result
            except Exception as e:
                result["success"] = False
                result["error"]   = str(e)
                log.error(f"[FLOW/ROUTINE] Step failed: {step.title} — {e}")

        return result

    def get_due_routines(self) -> List[Routine]:
        """Get routines that should run now."""
        now     = datetime.now(timezone.utc)
        now_str = now.strftime("%H:%M")
        due     = []

        for routine in self._routines.values():
            if not routine.active:
                continue
            if routine.trigger_type == TriggerType.TIME:
                if routine.trigger_value == now_str:
                    # Check if already run today
                    if routine.last_run:
                        last = datetime.fromisoformat(routine.last_run)
                        if last.date() == now.date():
                            continue
                    due.append(routine)

        return due

    def get_all_routines(self) -> List[Dict]:
        return [r.to_dict() for r in self._routines.values()]

    def get_routine_by_name(self, name: str) -> Optional[Routine]:
        for r in self._routines.values():
            if name.lower() in r.name.lower():
                return r
        return None

    def toggle_routine(self, routine_id: str) -> Dict:
        routine = self._routines.get(routine_id)
        if not routine:
            return {"error": "Not found"}
        routine.active = not routine.active
        return {"routine": routine.name, "active": routine.active}

    def get_stats(self) -> Dict:
        active   = sum(1 for r in self._routines.values() if r.active)
        total_runs = sum(r.run_count for r in self._routines.values())
        return {
            "total_routines" : len(self._routines),
            "active"         : active,
            "total_runs"     : total_runs,
            "currently_running": len(self._running)
        }


# ══════════════════════════════════════════════
#  MODULE 2 — TASK & SCHEDULE MANAGER
# ══════════════════════════════════════════════

class TaskManager:
    """
    Full task and schedule management.

    JARVIS kept Tony's entire life organized —
    meetings, deadlines, priorities — without
    Tony having to think about it.

    Echo's TaskManager does the same —
    captures tasks, prioritizes intelligently,
    tracks deadlines proactively, and surfaces
    the right task at the right time.
    """

    def __init__(self):
        self._tasks: Dict[str, Task]          = {}
        self._reminders: Dict[str, Reminder]  = {}
        self._completed: List[Task]           = []
        self._lock                            = threading.Lock()

        # Load demo tasks
        self._load_demo_tasks()

    def _load_demo_tasks(self):
        """Seed with realistic default tasks."""
        demo_tasks = [
            Task(title="Review portfolio performance",
                 priority=Priority.HIGH, tags=["finance", "nexus"],
                 estimated_minutes=30, energy_required=3),
            Task(title="Study session — quantum computing",
                 priority=Priority.NORMAL, tags=["learning", "scholar"],
                 estimated_minutes=45, energy_required=4),
            Task(title="Morning workout",
                 priority=Priority.HIGH, tags=["health", "vital"],
                 recurrence=RecurrenceType.DAILY, estimated_minutes=45,
                 energy_required=3),
            Task(title="Team check-in",
                 priority=Priority.NORMAL, tags=["work", "nexus"],
                 estimated_minutes=30, energy_required=2),
            Task(title="Read and respond to emails",
                 priority=Priority.NORMAL, tags=["admin"],
                 recurrence=RecurrenceType.DAILY, estimated_minutes=20,
                 energy_required=2),
        ]
        for task in demo_tasks:
            self._tasks[task.task_id] = task

    def add_task(self, title: str,
                  priority: Priority = Priority.NORMAL,
                  due_at: Optional[str] = None,
                  tags: Optional[List[str]] = None,
                  recurrence: RecurrenceType = RecurrenceType.NONE,
                  estimated_minutes: int = 15,
                  energy_required: int = 3) -> Task:
        """Add a new task."""
        task = Task(
            title             = title,
            priority          = priority,
            due_at            = due_at,
            tags              = tags or [],
            recurrence        = recurrence,
            estimated_minutes = estimated_minutes,
            energy_required   = energy_required
        )
        with self._lock:
            self._tasks[task.task_id] = task

        log.info(
            f"[FLOW/TASK] Added: '{title}' | "
            f"Priority: {priority.name} | Due: {due_at or 'none'}"
        )
        return task

    def complete_task(self, task_id: str) -> Dict:
        """Mark a task complete."""
        task = self._tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}

        task.status       = TaskStatus.DONE
        task.completed_at = datetime.now(timezone.utc).isoformat()

        # Handle recurring tasks
        if task.recurrence != RecurrenceType.NONE:
            self._reschedule_recurring(task)

        with self._lock:
            self._completed.append(task)

        log.info(f"[FLOW/TASK] Completed: '{task.title}'")
        return {"task": task.title, "status": "done", "completed_at": task.completed_at}

    def _reschedule_recurring(self, task: Task):
        """Create next occurrence of a recurring task."""
        new_task = Task(
            title             = task.title,
            priority          = task.priority,
            tags              = task.tags,
            recurrence        = task.recurrence,
            estimated_minutes = task.estimated_minutes,
            energy_required   = task.energy_required
        )
        # Set next due date
        if task.recurrence == RecurrenceType.DAILY:
            new_task.due_at = (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat()
        elif task.recurrence == RecurrenceType.WEEKLY:
            new_task.due_at = (
                datetime.now(timezone.utc) + timedelta(weeks=1)
            ).isoformat()

        self._tasks[new_task.task_id] = new_task
        log.debug(f"[FLOW/TASK] Rescheduled: '{task.title}'")

    def add_reminder(self, title: str, message: str,
                      remind_at: str,
                      priority: Priority = Priority.NORMAL,
                      recurrence: RecurrenceType = RecurrenceType.NONE) -> Reminder:
        """Set a reminder."""
        reminder = Reminder(
            title      = title,
            message    = message,
            remind_at  = remind_at,
            priority   = priority,
            recurrence = recurrence
        )
        with self._lock:
            self._reminders[reminder.reminder_id] = reminder

        log.info(f"[FLOW/REMINDER] Set: '{title}' at {remind_at}")
        return reminder

    def get_due_reminders(self) -> List[Reminder]:
        """Get reminders that are due now."""
        now = datetime.now(timezone.utc).isoformat()
        due = []
        for reminder in self._reminders.values():
            if not reminder.triggered and reminder.remind_at <= now:
                due.append(reminder)
                reminder.triggered = True
        return due

    def get_pending_tasks(self, limit: int = 10,
                           priority_filter: Optional[Priority] = None) -> List[Task]:
        """Get pending tasks, sorted by priority."""
        tasks = [
            t for t in self._tasks.values()
            if t.status == TaskStatus.PENDING
            and (not priority_filter or t.priority == priority_filter)
        ]
        tasks.sort(key=lambda t: (t.priority.value, t.due_at or "9"), reverse=True)
        return tasks[:limit]

    def get_overdue_tasks(self) -> List[Task]:
        """Get tasks past their due date."""
        now   = datetime.now(timezone.utc).isoformat()
        return [
            t for t in self._tasks.values()
            if t.status == TaskStatus.PENDING
            and t.due_at and t.due_at < now
        ]

    def get_today_tasks(self) -> List[Task]:
        """Get tasks due today."""
        today = datetime.now(timezone.utc).date().isoformat()
        return [
            t for t in self._tasks.values()
            if t.status == TaskStatus.PENDING
            and (not t.due_at or t.due_at[:10] == today)
        ]

    def prioritize(self) -> List[Dict]:
        """
        JARVIS addition: Intelligent task prioritization.
        Echo figures out the right order for you —
        considering priority, deadlines, energy, and context.
        """
        pending  = self.get_pending_tasks(limit=20)
        overdue  = self.get_overdue_tasks()
        today    = self.get_today_tasks()

        prioritized = []

        # First: overdue critical/urgent
        for task in overdue:
            if task.priority.value >= Priority.HIGH.value:
                prioritized.append({
                    "task"    : task.to_dict(),
                    "reason"  : "OVERDUE — do this now",
                    "urgency" : "immediate"
                })

        # Then: today's high priority
        for task in today:
            if task.priority.value >= Priority.HIGH.value and task not in overdue:
                prioritized.append({
                    "task"    : task.to_dict(),
                    "reason"  : "High priority — due today",
                    "urgency" : "today"
                })

        # Then: normal pending
        for task in pending:
            if task not in overdue and task not in today:
                prioritized.append({
                    "task"    : task.to_dict(),
                    "reason"  : "Pending — schedule when ready",
                    "urgency" : "soon"
                })

        return prioritized[:8]

    def get_stats(self) -> Dict:
        pending   = sum(1 for t in self._tasks.values() if t.status == TaskStatus.PENDING)
        done      = len(self._completed)
        overdue   = len(self.get_overdue_tasks())

        return {
            "total_tasks"    : len(self._tasks),
            "pending"        : pending,
            "completed"      : done,
            "overdue"        : overdue,
            "reminders_set"  : len(self._reminders),
            "completion_rate": round(done / max(done + pending, 1) * 100, 1)
        }


# ══════════════════════════════════════════════
#  MODULE 3 — WORKFLOW ENGINE
# ══════════════════════════════════════════════

class WorkflowEngine:
    """
    Multi-step automated workflows connecting Echo layers.

    This is where Flow becomes truly powerful —
    it doesn't just manage tasks, it automates
    complex multi-layer processes.

    JARVIS ran complex protocols automatically:
    "Initializing Mark VII. Repulsor systems online.
    Targeting systems engaged." — all automated.

    Echo's WorkflowEngine does the same for your life.
    """

    # Pre-built workflow templates
    WORKFLOW_TEMPLATES = {
        "morning_intelligence": {
            "name"       : "Morning Intelligence Brief",
            "description": "JARVIS-style morning briefing — everything before you ask",
            "trigger"    : "06:30",
            "steps"      : [
                {"name": "Health Check",      "layer": "vital",    "action": "Show overnight health metrics"},
                {"name": "Market Brief",      "layer": "nexus",    "action": "Get market overview and alerts"},
                {"name": "Weather + Context", "layer": "stellar",  "action": "Today's context analysis"},
                {"name": "Task Priority",     "layer": "flow",     "action": "Get today's priority tasks"},
                {"name": "Security Report",   "layer": "sentinel", "action": "Overnight security summary"},
            ]
        },
        "deal_analysis": {
            "name"       : "Deal Analysis Pipeline",
            "description": "Analyze a business deal across all relevant layers",
            "trigger"    : "manual",
            "steps"      : [
                {"name": "Financial Analysis", "layer": "nexus",   "action": "Analyze deal financials"},
                {"name": "Risk Assessment",    "layer": "stellar",  "action": "Deep risk reasoning"},
                {"name": "Security Check",     "layer": "sentinel", "action": "Counterparty background check"},
                {"name": "Legal Framework",    "layer": "scholar",  "action": "Relevant legal context"},
                {"name": "Recommendation",     "layer": "stellar",  "action": "Final synthesis and recommendation"},
            ]
        },
        "health_protocol": {
            "name"       : "Full Health Protocol",
            "description": "Complete health assessment pipeline",
            "trigger"    : "manual",
            "steps"      : [
                {"name": "Vitals Scan",       "layer": "vital",    "action": "Full biometric reading"},
                {"name": "Symptom Analysis",  "layer": "vital",    "action": "Symptom assessment if any"},
                {"name": "Pattern Analysis",  "layer": "stellar",  "action": "Health trend analysis"},
                {"name": "Recommendations",   "layer": "vital",    "action": "Health recommendations"},
                {"name": "Schedule Adjust",   "layer": "flow",     "action": "Adjust today's tasks for health"},
            ]
        },
        "creative_pipeline": {
            "name"       : "Creative Production Pipeline",
            "description": "Full creative project from concept to output",
            "trigger"    : "manual",
            "steps"      : [
                {"name": "Brief Generation",  "layer": "creator",  "action": "Generate creative brief"},
                {"name": "Research",          "layer": "scholar",  "action": "Research relevant context"},
                {"name": "Creation",          "layer": "creator",  "action": "Execute creative output"},
                {"name": "Review",            "layer": "stellar",  "action": "Quality and coherence check"},
            ]
        },
        "security_response": {
            "name"       : "Security Incident Response",
            "description": "Automated response to detected threats",
            "trigger"    : "event:threat_detected",
            "steps"      : [
                {"name": "Threat Assessment", "layer": "sentinel", "action": "Full threat classification"},
                {"name": "System Lockdown",   "layer": "vital",    "action": "Lock non-essential systems"},
                {"name": "Evidence Package",  "layer": "sentinel", "action": "Compile evidence"},
                {"name": "Intelligence",      "layer": "stellar",  "action": "Analyze threat origin and intent"},
                {"name": "Authority Alert",   "layer": "sentinel", "action": "Alert relevant authorities"},
                {"name": "Report",            "layer": "flow",     "action": "Generate incident report"},
            ]
        }
    }

    def __init__(self):
        self._workflows: Dict[str, Workflow] = {}
        self._execution_history: List[Dict]  = []
        self._lock                           = threading.Lock()

        self._load_default_workflows()

    def _load_default_workflows(self):
        """Load pre-built workflow templates."""
        for key, template in self.WORKFLOW_TEMPLATES.items():
            workflow = self._build_from_template(template)
            self._workflows[workflow.workflow_id] = workflow

        log.info(f"[FLOW/WORKFLOW] Loaded {len(self._workflows)} workflows")

    def _build_from_template(self, template: Dict) -> Workflow:
        steps = [
            WorkflowStep(
                name   = s["name"],
                action = s["action"],
                layer  = s["layer"]
            )
            for s in template["steps"]
        ]
        return Workflow(
            name        = template["name"],
            description = template["description"],
            trigger     = template["trigger"],
            steps       = steps
        )

    def create_workflow(self, name: str, trigger: str,
                         steps: List[Dict],
                         parallel: bool = False) -> Workflow:
        """Create a custom workflow."""
        workflow_steps = [
            WorkflowStep(
                name      = s.get("name", f"Step {i+1}"),
                action    = s.get("action", ""),
                layer     = s.get("layer", "core"),
                condition = s.get("condition"),
                params    = s.get("params", {})
            )
            for i, s in enumerate(steps)
        ]

        workflow = Workflow(
            name     = name,
            trigger  = trigger,
            steps    = workflow_steps,
            parallel = parallel
        )

        with self._lock:
            self._workflows[workflow.workflow_id] = workflow

        log.info(f"[FLOW/WORKFLOW] Created: '{name}' ({len(workflow_steps)} steps)")
        return workflow

    def execute_workflow(self, workflow_id: str,
                          layer_executor: Optional[Callable] = None,
                          context: Optional[Dict] = None) -> Dict:
        """Execute a workflow — sequential or parallel."""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return {"error": f"Workflow {workflow_id} not found"}

        start_time = time.time()
        context    = context or {}

        log.info(
            f"[FLOW/WORKFLOW] Starting: '{workflow.name}' | "
            f"{'Parallel' if workflow.parallel else 'Sequential'}"
        )

        results = []
        if workflow.parallel:
            results = self._run_parallel(workflow.steps, layer_executor, context)
        else:
            results = self._run_sequential(workflow.steps, layer_executor, context)

        elapsed = time.time() - start_time
        workflow.last_run  = datetime.now(timezone.utc).isoformat()
        workflow.run_count += 1

        execution = {
            "workflow_id" : workflow_id,
            "name"        : workflow.name,
            "steps_total" : len(workflow.steps),
            "steps_done"  : sum(1 for r in results if r.get("success")),
            "parallel"    : workflow.parallel,
            "elapsed_ms"  : round(elapsed * 1000, 2),
            "results"     : results,
            "timestamp"   : workflow.last_run
        }

        with self._lock:
            self._execution_history.append(execution)

        log.info(
            f"[FLOW/WORKFLOW] Complete: '{workflow.name}' | "
            f"{execution['steps_done']}/{execution['steps_total']} | "
            f"{elapsed*1000:.0f}ms"
        )

        return execution

    def _run_sequential(self, steps: List[WorkflowStep],
                         executor: Optional[Callable],
                         context: Dict) -> List[Dict]:
        """Run steps one after another."""
        results = []
        for step in steps:
            # Check condition
            if step.condition and not self._evaluate_condition(step.condition, context):
                results.append({
                    "step"   : step.name,
                    "skipped": True,
                    "reason" : f"Condition not met: {step.condition}"
                })
                continue

            result = self._run_step(step, executor, context)
            results.append(result)

            # Update context with result for next steps
            context[step.name] = result

            # Stop on critical failure unless step has failure handler
            if not result.get("success") and not step.on_failure:
                log.warning(f"[FLOW/WORKFLOW] Step failed, stopping: {step.name}")
                break

        return results

    def _run_parallel(self, steps: List[WorkflowStep],
                       executor: Optional[Callable],
                       context: Dict) -> List[Dict]:
        """Run all steps simultaneously using threads."""
        results = [None] * len(steps)
        threads = []

        def run_step_threaded(i, step):
            results[i] = self._run_step(step, executor, context)

        for i, step in enumerate(steps):
            t = threading.Thread(target=run_step_threaded, args=(i, step))
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=30)

        return [r for r in results if r is not None]

    def _run_step(self, step: WorkflowStep,
                   executor: Optional[Callable],
                   context: Dict) -> Dict:
        """Execute one workflow step."""
        result = {
            "step"   : step.name,
            "layer"  : step.layer,
            "action" : step.action,
            "success": True
        }

        if executor:
            try:
                layer_result = executor(
                    layer  = step.layer,
                    action = step.action,
                    params = {**step.params, **context}
                )
                result["response"] = layer_result
            except Exception as e:
                result["success"] = False
                result["error"]   = str(e)

        return result

    def _evaluate_condition(self, condition: str, context: Dict) -> bool:
        """Simple condition evaluation."""
        # In production: full expression parser
        if "energy_high" in condition:
            return context.get("energy_level", 3) >= 4
        if "market_open" in condition:
            hour = datetime.now(timezone.utc).hour
            return 9 <= hour <= 16
        return True

    def get_workflow_by_name(self, name: str) -> Optional[Workflow]:
        for w in self._workflows.values():
            if name.lower() in w.name.lower():
                return w
        return None

    def get_all_workflows(self) -> List[Dict]:
        return [w.to_dict() for w in self._workflows.values()]

    def get_stats(self) -> Dict:
        return {
            "total_workflows": len(self._workflows),
            "active"         : sum(1 for w in self._workflows.values() if w.active),
            "total_runs"     : sum(w.run_count for w in self._workflows.values()),
            "executions_log" : len(self._execution_history)
        }


# ══════════════════════════════════════════════
#  MODULE 4 — NOTIFICATION SYSTEM
# ══════════════════════════════════════════════

class NotificationSystem:
    """
    Smart notification management.

    JARVIS only interrupted Tony when it mattered.
    He batched low-priority updates, held non-urgent
    alerts during focus time, and escalated genuinely
    critical information immediately.

    Echo does the same — intelligent notification
    filtering that respects your attention.
    """

    def __init__(self):
        self._notifications: List[Dict]  = []
        self._focus_mode: bool           = False
        self._dnd_until: Optional[str]   = None
        self._batched: List[Dict]        = []
        self._lock                       = threading.Lock()

    def send(self, title: str, message: str,
              priority: Priority = Priority.NORMAL,
              layer: str = "flow") -> Dict:
        """
        Send a notification through the smart filter.
        Low priority → batched.
        High priority → immediate.
        Critical → always immediate, even in focus mode.
        """
        notification = {
            "id"       : str(uuid.uuid4())[:8],
            "title"    : title,
            "message"  : message,
            "priority" : priority.name,
            "layer"    : layer,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "delivered": False
        }

        # Critical always gets through
        if priority == Priority.CRITICAL:
            notification["delivered"] = True
            with self._lock:
                self._notifications.append(notification)
            log.critical(f"[FLOW/NOTIFY] CRITICAL: {title}")
            return {"status": "delivered_immediately", "notification": notification}

        # Check focus/DND mode
        if self._focus_mode and priority.value < Priority.URGENT.value:
            with self._lock:
                self._batched.append(notification)
            log.info(f"[FLOW/NOTIFY] Batched (focus mode): {title}")
            return {"status": "batched", "notification": notification}

        # Normal delivery
        notification["delivered"] = True
        with self._lock:
            self._notifications.append(notification)

        log.info(f"[FLOW/NOTIFY] [{priority.name}] {title}")
        return {"status": "delivered", "notification": notification}

    def enable_focus_mode(self, duration_minutes: int = 25) -> Dict:
        """
        Enable focus mode — protect concentration.
        JARVIS-style interruption management.
        """
        self._focus_mode  = True
        end_time          = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
        self._dnd_until   = end_time.isoformat()

        log.info(f"[FLOW/NOTIFY] Focus mode ON — {duration_minutes} minutes")

        # Auto-disable after duration
        def disable_after():
            time.sleep(duration_minutes * 60)
            self._focus_mode = False
            self._dnd_until  = None
            log.info("[FLOW/NOTIFY] Focus mode OFF — releasing batched notifications")

        t = threading.Thread(target=disable_after, daemon=True)
        t.start()

        return {
            "status"      : "focus_mode_active",
            "duration_min": duration_minutes,
            "ends_at"     : self._dnd_until,
            "batched"     : len(self._batched),
            "echo_note"   : (
                f"Focus mode active for {duration_minutes} minutes. "
                f"Only critical alerts will reach you. "
                f"{len(self._batched)} notifications are waiting."
            )
        }

    def disable_focus_mode(self) -> Dict:
        """Disable focus mode and deliver batched notifications."""
        self._focus_mode = False
        batched_count    = len(self._batched)

        # Deliver batched notifications
        with self._lock:
            for notif in self._batched:
                notif["delivered"] = True
                self._notifications.append(notif)
            self._batched.clear()

        return {
            "status"             : "focus_mode_disabled",
            "delivered_batched"  : batched_count,
            "echo_note"          : f"Focus mode off. {batched_count} held notifications delivered."
        }

    def get_unread(self, limit: int = 10) -> List[Dict]:
        """Get recent unread notifications."""
        return [n for n in self._notifications[-20:] if n["delivered"]][-limit:]

    def get_stats(self) -> Dict:
        return {
            "total_sent"   : len(self._notifications),
            "batched"      : len(self._batched),
            "focus_mode"   : self._focus_mode,
            "dnd_until"    : self._dnd_until
        }


# ══════════════════════════════════════════════
#  JARVIS ADDITIONS
# ══════════════════════════════════════════════

class HabitEngine:
    """
    JARVIS addition: Habit formation and tracking.

    JARVIS tracked Tony's patterns and optimized
    his environment for peak performance.

    Echo's HabitEngine builds positive habits
    through consistent tracking, streak motivation,
    and smart reminders timed to the user's patterns.
    """

    def __init__(self):
        self._habits: Dict[str, Dict]    = {}
        self._streaks: Dict[str, int]    = defaultdict(int)
        self._history: Dict[str, List]   = defaultdict(list)

        # Pre-load useful habits
        self._habits["morning_workout"] = {
            "name"       : "Morning Workout",
            "frequency"  : "daily",
            "best_time"  : "07:00",
            "category"   : "health",
            "streak"     : 0,
            "record"     : 0
        }
        self._habits["daily_learning"] = {
            "name"       : "Daily Learning (15min)",
            "frequency"  : "daily",
            "best_time"  : "08:00",
            "category"   : "growth",
            "streak"     : 0,
            "record"     : 0
        }
        self._habits["evening_review"] = {
            "name"       : "Evening Review",
            "frequency"  : "daily",
            "best_time"  : "21:00",
            "category"   : "productivity",
            "streak"     : 0,
            "record"     : 0
        }

    def add_habit(self, name: str, frequency: str = "daily",
                   best_time: str = "08:00",
                   category: str = "general") -> Dict:
        habit_id = name.lower().replace(" ", "_")
        self._habits[habit_id] = {
            "name"    : name,
            "frequency": frequency,
            "best_time": best_time,
            "category": category,
            "streak"  : 0,
            "record"  : 0,
            "created" : datetime.now(timezone.utc).isoformat()
        }
        log.info(f"[FLOW/HABIT] Added: '{name}'")
        return self._habits[habit_id]

    def log_completion(self, habit_id: str) -> Dict:
        """Log a habit as completed today."""
        habit = self._habits.get(habit_id)
        if not habit:
            return {"error": "Habit not found"}

        today  = datetime.now(timezone.utc).date().isoformat()
        log_entry = {"date": today, "completed": True}
        self._history[habit_id].append(log_entry)

        # Update streak
        self._streaks[habit_id] += 1
        habit["streak"] = self._streaks[habit_id]
        habit["record"] = max(habit["record"], habit["streak"])

        log.info(
            f"[FLOW/HABIT] Completed: '{habit['name']}' | "
            f"Streak: {habit['streak']} days"
        )

        return {
            "habit"   : habit["name"],
            "streak"  : habit["streak"],
            "record"  : habit["record"],
            "message" : (
                f"🔥 {habit['streak']} day streak!" if habit["streak"] > 1
                else "Great start! Keep it going."
            )
        }

    def get_habits_summary(self) -> Dict:
        return {
            "total_habits": len(self._habits),
            "habits"      : list(self._habits.values()),
            "top_streak"  : max(
                (h["streak"] for h in self._habits.values()), default=0
            ),
            "categories"  : list(set(h["category"] for h in self._habits.values()))
        }


class EnergyScheduler:
    """
    JARVIS addition: Energy-aware task scheduling.

    JARVIS knew when Tony was at peak cognitive
    performance and scheduled demanding work accordingly.

    Echo maps tasks to energy windows —
    deep work when you're sharp,
    admin when you're not.
    """

    ENERGY_SCHEDULE = {
        "05:00-07:00": EnergyLevel.LOW,      # Just waking up
        "07:00-09:00": EnergyLevel.MODERATE, # Coming online
        "09:00-12:00": EnergyLevel.PEAK,     # Morning peak
        "12:00-14:00": EnergyLevel.MODERATE, # Post-lunch dip incoming
        "14:00-15:00": EnergyLevel.LOW,      # Afternoon slump
        "15:00-18:00": EnergyLevel.HIGH,     # Second wind
        "18:00-20:00": EnergyLevel.MODERATE, # Evening
        "20:00-22:00": EnergyLevel.LOW,      # Winding down
        "22:00-05:00": EnergyLevel.REST      # Sleep
    }

    TASK_ENERGY_MAP = {
        5: ["Deep work", "Complex problem solving", "Creative creation", "Learning"],
        4: ["Strategic planning", "Important meetings", "Research", "Writing"],
        3: ["Regular meetings", "Email", "Planning", "Calls"],
        2: ["Admin", "Filing", "Simple reviews", "Scheduling"],
        1: ["Rest", "Light reading", "Reflection"]
    }

    def get_current_energy(self) -> Dict:
        """Get current energy level based on time of day."""
        now     = datetime.now(timezone.utc)
        now_str = now.strftime("%H:%M")

        level = EnergyLevel.MODERATE  # Default

        for time_range, energy in self.ENERGY_SCHEDULE.items():
            start, end = time_range.split("-")
            if start <= now_str < end or (end < start and (now_str >= start or now_str < end)):
                level = energy
                break

        return {
            "time"          : now_str,
            "energy_level"  : level.name,
            "energy_value"  : level.value,
            "best_for"      : self.TASK_ENERGY_MAP.get(level.value, ["General work"]),
            "echo_note"     : self._get_energy_note(level)
        }

    def _get_energy_note(self, level: EnergyLevel) -> str:
        notes = {
            EnergyLevel.PEAK    : "Peak cognitive window. Attack your hardest task now.",
            EnergyLevel.HIGH    : "Good energy. Solid work time — handle important items.",
            EnergyLevel.MODERATE: "Moderate energy. Meetings and collaborative work fit well here.",
            EnergyLevel.LOW     : "Energy dip. Admin, light tasks, or a short break.",
            EnergyLevel.REST    : "Rest window. Sleep or genuine recovery — not productive work."
        }
        return notes.get(level, "Schedule according to how you feel.")

    def suggest_task(self, tasks: List[Task]) -> Optional[Dict]:
        """
        JARVIS addition: Suggest the right task for right now.
        Matches task energy requirement to current energy.
        """
        current = self.get_current_energy()
        current_energy = current["energy_value"]

        # Find tasks that match current energy
        matched = [
            t for t in tasks
            if t.status == TaskStatus.PENDING
            and abs(t.energy_required - current_energy) <= 1
        ]

        if not matched:
            matched = tasks[:1] if tasks else []

        if not matched:
            return None

        # Pick highest priority match
        best = max(matched, key=lambda t: t.priority.value)

        return {
            "suggested_task" : best.to_dict(),
            "current_energy" : current,
            "reason"         : (
                f"This task requires {best.energy_required}/5 energy. "
                f"You're currently at {current_energy}/5 ({current['energy_level']}). "
                f"Good match."
            )
        }


class DailyBriefingEngine:
    """
    JARVIS addition: Proactive daily briefings.

    JARVIS gave Tony a full situational briefing
    the moment he entered any room.
    Echo does the same every morning before you ask.
    """

    def generate(self, task_stats: Dict, workflow_stats: Dict,
                  routine_stats: Dict, habit_summary: Dict,
                  energy: Dict, notifications: Dict) -> Dict:
        """Generate a full daily briefing."""

        now    = datetime.now(timezone.utc)
        greeting = (
            "Good morning" if 5 <= now.hour < 12 else
            "Good afternoon" if 12 <= now.hour < 17 else
            "Good evening"
        )

        briefing_lines = [
            f"╔══ ECHO — DAILY BRIEFING ══════════════╗",
            f"  {greeting}. {now.strftime('%A, %B %d')}",
            f"  {now.strftime('%H:%M')} UTC",
            f"",
            f"  ENERGY    : {energy.get('energy_level', 'N/A')} — {energy.get('echo_note', '')[:40]}",
            f"",
            f"  TASKS",
            f"  ├─ Pending  : {task_stats.get('pending', 0)}",
            f"  ├─ Overdue  : {task_stats.get('overdue', 0)}",
            f"  └─ Done     : {task_stats.get('completed', 0)} total",
            f"",
            f"  ROUTINES  : {routine_stats.get('active', 0)} active",
            f"  WORKFLOWS : {workflow_stats.get('active', 0)} active",
            f"  HABITS    : {habit_summary.get('total_habits', 0)} tracked",
            f"  ALERTS    : {notifications.get('total_sent', 0)} total",
            f"",
            f"  Ready for your instructions.",
            f"╚═══════════════════════════════════════╝"
        ]

        return {
            "briefing"      : "\n".join(briefing_lines),
            "greeting"      : greeting,
            "energy"        : energy,
            "task_summary"  : task_stats,
            "habits"        : habit_summary,
            "echo_note"     : "Full briefing ready. What would you like to focus on?"
        }


# ══════════════════════════════════════════════
#  FLOW LAYER — MASTER CLASS
# ══════════════════════════════════════════════

class FlowLayer:
    """
    Flow Layer — Echo's Automation & Routine Engine.

    Runs your life so you can live it.
    Automates the mundane, optimizes the meaningful,
    and connects all Echo layers into seamless workflows.

    JARVIS ran Stark Industries and the mansion
    simultaneously without Tony thinking about it.
    Flow makes Echo do the same for you.
    """

    def __init__(self):
        self.routines      = RoutineEngine()
        self.tasks         = TaskManager()
        self.workflows     = WorkflowEngine()
        self.notifications = NotificationSystem()
        self.habits        = HabitEngine()
        self.energy        = EnergyScheduler()
        self.briefing      = DailyBriefingEngine()
        self._lock         = threading.Lock()

        # Start background scheduler
        self._scheduler_active = True
        self._scheduler = threading.Thread(
            target=self._background_scheduler,
            daemon=True
        )
        self._scheduler.start()

        log.info("[FLOW] Layer online. Automation engine active.")

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """Main entry point from EchoCore LayerRouter."""
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[FLOW] Processing: '{intent_text[:60]}'")

        # ── Route to module ────────────────────────

        # Daily briefing
        if any(kw in intent_low for kw in ["briefing", "morning brief", "daily brief",
                                            "what's today", "whats today", "good morning",
                                            "status report"]):
            return self._handle_briefing()

        # Routine management
        elif any(kw in intent_low for kw in ["routine", "morning routine", "evening routine",
                                              "run routine", "start routine", "my routines"]):
            return self._handle_routines(intent_text, context)

        # Task management
        elif any(kw in intent_low for kw in ["task", "todo", "to do", "prioritize",
                                              "what should i do", "my tasks"]):
            return self._handle_tasks(intent_text, context)

        # Reminders and alarms
        elif any(kw in intent_low for kw in ["remind", "reminder", "alarm", "alert",
                                              "set a reminder", "don't forget"]):
            return self._handle_reminder(intent_text, context)

        # Workflow
        elif any(kw in intent_low for kw in ["workflow", "automate", "pipeline",
                                              "run workflow", "automation"]):
            return self._handle_workflows(intent_text, context)

        # Focus mode
        elif any(kw in intent_low for kw in ["focus", "do not disturb", "dnd",
                                              "no interruptions", "deep work",
                                              "focus mode", "pomodoro"]):
            return self._handle_focus(intent_text, context)

        # Habits
        elif any(kw in intent_low for kw in ["habit", "streak", "track habit",
                                              "log habit", "my habits"]):
            return self._handle_habits(intent_text, context)

        # Energy
        elif any(kw in intent_low for kw in ["energy", "what should i work on",
                                              "suggest task", "right now task"]):
            return self._handle_energy(intent_text, context)

        # Schedule
        elif any(kw in intent_low for kw in ["schedule", "calendar", "plan",
                                              "today's plan", "my schedule"]):
            return self._handle_schedule(intent_text, context)

        # General Flow
        else:
            return self._handle_general(intent_text, context)

    # ── Handlers ───────────────────────────────

    def _handle_briefing(self) -> Dict:
        """Generate full daily briefing."""
        briefing = self.briefing.generate(
            task_stats     = self.tasks.get_stats(),
            workflow_stats = self.workflows.get_stats(),
            routine_stats  = self.routines.get_stats(),
            habit_summary  = self.habits.get_habits_summary(),
            energy         = self.energy.get_current_energy(),
            notifications  = self.notifications.get_stats()
        )

        return {
            "layer"    : "flow",
            "status"   : "OK",
            "sub_system": "briefing",
            "briefing" : briefing,
            "message"  : briefing["briefing"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_routines(self, intent: str, context: Dict) -> Dict:
        """Handle routine queries and execution."""
        intent_low = intent.lower()

        # Run specific routine
        if any(kw in intent_low for kw in ["run", "start", "execute", "activate"]):
            for name in ["morning", "evening", "focus", "workout", "security"]:
                if name in intent_low:
                    routine = self.routines.get_routine_by_name(name)
                    if routine:
                        result = self.routines.execute_routine(routine.routine_id)
                        return {
                            "layer"    : "flow",
                            "status"   : "OK",
                            "sub_system": "routine_execution",
                            "result"   : result,
                            "message"  : (
                                f"Routine '{result['name']}' complete. "
                                f"{result['steps_done']}/{result['steps_total']} steps "
                                f"in {result['elapsed_ms']}ms."
                            ),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }

        # List routines
        all_routines = self.routines.get_all_routines()
        return {
            "layer"     : "flow",
            "status"    : "OK",
            "sub_system": "routines",
            "routines"  : all_routines,
            "stats"     : self.routines.get_stats(),
            "message"   : (
                f"{len(all_routines)} routines configured. "
                f"{self.routines.get_stats()['active']} active. "
                f"Say 'run morning routine' to execute one."
            ),
            "timestamp" : datetime.now(timezone.utc).isoformat()
        }

    def _handle_tasks(self, intent: str, context: Dict) -> Dict:
        """Handle task management."""
        intent_low = intent.lower()

        # Add task
        if any(kw in intent_low for kw in ["add task", "new task", "create task"]):
            title    = context.get("title", intent.replace("add task", "").strip())
            priority = Priority.HIGH if "urgent" in intent_low else Priority.NORMAL
            task     = self.tasks.add_task(title, priority)
            return {
                "layer"    : "flow",
                "status"   : "OK",
                "sub_system": "task_added",
                "task"     : task.to_dict(),
                "message"  : f"Task added: '{task.title}' | Priority: {task.priority.name}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        # Prioritize
        if any(kw in intent_low for kw in ["prioritize", "what should i do",
                                            "top tasks", "most important"]):
            prioritized = self.tasks.prioritize()
            return {
                "layer"     : "flow",
                "status"    : "OK",
                "sub_system": "task_priority",
                "priorities": prioritized,
                "message"   : (
                    f"Top {len(prioritized)} tasks prioritized. "
                    f"Most urgent: {prioritized[0]['task']['title'] if prioritized else 'none'}."
                ),
                "timestamp" : datetime.now(timezone.utc).isoformat()
            }

        # General task overview
        stats   = self.tasks.get_stats()
        pending = self.tasks.get_pending_tasks(limit=5)
        overdue = self.tasks.get_overdue_tasks()

        return {
            "layer"     : "flow",
            "status"    : "OK",
            "sub_system": "tasks",
            "stats"     : stats,
            "pending"   : [t.to_dict() for t in pending],
            "overdue"   : [t.to_dict() for t in overdue],
            "message"   : (
                f"{stats['pending']} tasks pending. "
                f"{stats['overdue']} overdue. "
                f"Completion rate: {stats['completion_rate']}%."
            ),
            "timestamp" : datetime.now(timezone.utc).isoformat()
        }

    def _handle_reminder(self, intent: str, context: Dict) -> Dict:
        """Set or view reminders."""
        # Extract time from context or use default
        remind_at = context.get("time", (
            datetime.now(timezone.utc) + timedelta(hours=1)
        ).isoformat())

        title   = context.get("title", intent[:50])
        message = context.get("message", intent)

        reminder = self.tasks.add_reminder(
            title     = title,
            message   = message,
            remind_at = remind_at
        )

        # Also send via notification system
        self.notifications.send(
            title    = f"Reminder Set: {title}",
            message  = f"Will remind you at {remind_at[:16]}",
            priority = Priority.NORMAL
        )

        return {
            "layer"    : "flow",
            "status"   : "OK",
            "sub_system": "reminder",
            "reminder" : reminder.to_dict(),
            "message"  : f"Reminder set: '{title}' — I'll alert you at {remind_at[:16]}.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_workflows(self, intent: str, context: Dict) -> Dict:
        """Handle workflow queries and execution."""
        intent_low = intent.lower()

        # Run workflow
        if any(kw in intent_low for kw in ["run", "execute", "start"]):
            workflow_names = [
                "morning intelligence", "deal analysis",
                "health protocol", "creative pipeline", "security response"
            ]
            for name in workflow_names:
                if any(word in intent_low for word in name.split()):
                    workflow = self.workflows.get_workflow_by_name(name)
                    if workflow:
                        result = self.workflows.execute_workflow(workflow.workflow_id)
                        return {
                            "layer"    : "flow",
                            "status"   : "OK",
                            "sub_system": "workflow_execution",
                            "result"   : result,
                            "message"  : (
                                f"Workflow '{result['name']}' complete. "
                                f"{result['steps_done']}/{result['steps_total']} steps."
                            ),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }

        all_workflows = self.workflows.get_all_workflows()
        return {
            "layer"    : "flow",
            "status"   : "OK",
            "sub_system": "workflows",
            "workflows": all_workflows,
            "stats"    : self.workflows.get_stats(),
            "message"  : (
                f"{len(all_workflows)} workflows available. "
                f"Say 'run morning intelligence' to execute."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_focus(self, intent: str, context: Dict) -> Dict:
        """Enable/disable focus mode."""
        intent_low = intent.lower()

        if any(kw in intent_low for kw in ["off", "disable", "end", "stop"]):
            result = self.notifications.disable_focus_mode()
        else:
            minutes = context.get("duration_minutes", 25)
            # Extract duration from intent
            for word in intent.split():
                if word.isdigit():
                    minutes = int(word)
                    break
            result = self.notifications.enable_focus_mode(minutes)

        return {
            "layer"    : "flow",
            "status"   : "OK",
            "sub_system": "focus_mode",
            "result"   : result,
            "message"  : result.get("echo_note", str(result)),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_habits(self, intent: str, context: Dict) -> Dict:
        """Habit tracking and management."""
        intent_low = intent.lower()

        if any(kw in intent_low for kw in ["log", "done", "completed", "finished", "did"]):
            habit_id = context.get("habit_id", "morning_workout")
            result   = self.habits.log_completion(habit_id)
            return {
                "layer"    : "flow",
                "status"   : "OK",
                "sub_system": "habit_log",
                "result"   : result,
                "message"  : result.get("message", "Habit logged"),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        summary = self.habits.get_habits_summary()
        return {
            "layer"    : "flow",
            "status"   : "OK",
            "sub_system": "habits",
            "summary"  : summary,
            "message"  : (
                f"{summary['total_habits']} habits tracked. "
                f"Top streak: {summary['top_streak']} days. "
                f"Categories: {', '.join(summary['categories'])}."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_energy(self, intent: str, context: Dict) -> Dict:
        """Energy-aware task suggestion."""
        current  = self.energy.get_current_energy()
        tasks    = self.tasks.get_pending_tasks(limit=10)
        suggest  = self.energy.suggest_task(tasks)

        return {
            "layer"     : "flow",
            "status"    : "OK",
            "sub_system": "energy_scheduling",
            "energy"    : current,
            "suggestion": suggest,
            "message"   : (
                f"Current energy: {current['energy_level']}. "
                f"Best for: {', '.join(current['best_for'][:2])}. "
                + (
                    f"Suggested task: '{suggest['suggested_task']['title']}'"
                    if suggest else "No matching tasks right now."
                )
            ),
            "timestamp" : datetime.now(timezone.utc).isoformat()
        }

    def _handle_schedule(self, intent: str, context: Dict) -> Dict:
        """Schedule overview."""
        tasks   = self.tasks.get_today_tasks()
        energy  = self.energy.get_current_energy()
        due_routines = self.routines.get_due_routines()

        return {
            "layer"      : "flow",
            "status"     : "OK",
            "sub_system" : "schedule",
            "today_tasks": [t.to_dict() for t in tasks],
            "energy"     : energy,
            "due_routines": [r.to_dict() for r in due_routines],
            "message"    : (
                f"Today: {len(tasks)} tasks. "
                f"Energy: {energy['energy_level']}. "
                f"Due routines: {len(due_routines)}."
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _handle_general(self, intent: str, context: Dict) -> Dict:
        """General Flow overview."""
        stats = {
            "tasks"    : self.tasks.get_stats(),
            "routines" : self.routines.get_stats(),
            "workflows": self.workflows.get_stats(),
            "habits"   : self.habits.get_habits_summary(),
            "energy"   : self.energy.get_current_energy()
        }

        return {
            "layer"    : "flow",
            "status"   : "OK",
            "sub_system": "general",
            "stats"    : stats,
            "message"  : (
                f"Flow online. "
                f"Tasks: {stats['tasks']['pending']} pending. "
                f"Routines: {stats['routines']['active']} active. "
                f"Energy: {stats['energy']['energy_level']}. "
                f"Say 'morning brief' for full daily overview."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _background_scheduler(self):
        """
        JARVIS addition: Autonomous background execution.
        Flow checks for due routines and reminders continuously.
        You don't have to ask — Echo just runs things.
        """
        log.info("[FLOW] Background scheduler started.")
        while self._scheduler_active:
            try:
                # Check due routines
                due = self.routines.get_due_routines()
                for routine in due:
                    log.info(f"[FLOW/BG] Auto-executing routine: {routine.name}")
                    self.notifications.send(
                        title    = f"Routine Starting: {routine.name}",
                        message  = routine.description,
                        priority = Priority.NORMAL
                    )

                # Check due reminders
                due_reminders = self.tasks.get_due_reminders()
                for reminder in due_reminders:
                    self.notifications.send(
                        title    = reminder.title,
                        message  = reminder.message,
                        priority = reminder.priority
                    )
                    log.info(f"[FLOW/BG] Reminder triggered: {reminder.title}")

                time.sleep(60)  # Check every minute

            except Exception as e:
                log.error(f"[FLOW/BG] Scheduler error: {e}")
                time.sleep(30)

    def get_status(self) -> Dict:
        return {
            "layer"          : "flow",
            "status"         : "ONLINE",
            "scheduler"      : "ACTIVE",
            "tasks"          : self.tasks.get_stats(),
            "routines"       : self.routines.get_stats(),
            "workflows"      : self.workflows.get_stats(),
            "focus_mode"     : self.notifications.get_stats()["focus_mode"],
            "habits"         : self.habits.get_habits_summary()["total_habits"],
            "energy_now"     : self.energy.get_current_energy()["energy_level"]
        }

    def shutdown(self):
        self._scheduler_active = False
        log.info("[FLOW] Shutdown complete.")


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║         ECHO FLOW LAYER — TEST              ║
╚══════════════════════════════════════════════╝
    """)

    flow    = FlowLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        ("Good morning Echo, give me my daily briefing",          {}),
        ("What are my current tasks and priorities?",             {}),
        ("Show me my routines",                                   {}),
        ("Run the morning power routine",                         {}),
        ("Enable focus mode for 30 minutes",                      {"duration_minutes": 30}),
        ("What should I work on right now?",                      {}),
        ("Show me my habits and streaks",                         {}),
        ("Set a reminder to review portfolio",                    {"title": "Review portfolio", "time": "17:00"}),
        ("Show me available workflows",                           {}),
        ("What's my schedule for today?",                         {}),
        ("Add a task: Prepare Echo investor pitch",               {"title": "Prepare Echo investor pitch"}),
        ("Prioritize my tasks",                                   {}),
    ]

    for i, (query, ctx) in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query[:60]}'")
        print("─" * 55)
        result = flow.process(query, session, ctx)
        print(f"  SUB-SYSTEM : {result.get('sub_system', 'N/A')}")
        msg = str(result.get('message', ''))[:130]
        print(f"  MESSAGE    : {msg}")

    print("\n" + "═" * 55)
    print("  FLOW STATUS")
    print("═" * 55)
    status = flow.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<25}: {v}")

    flow.shutdown()
