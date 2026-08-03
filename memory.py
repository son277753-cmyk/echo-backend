"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ECHO AI — MEMORY SYSTEM                          ║
║           Persistent · Contextual · Cross-Session                   ║
║                                                                      ║
║  Modules:                                                            ║
║    - ShortTermMemory   : Current conversation context               ║
║    - LongTermMemory    : Persists across ALL sessions               ║
║    - ReserveMode       : Burst processing for heavy tasks           ║
║    - EchoMemory        : Master memory orchestrator                 ║
║                                                                      ║
║  Stores:                                                             ║
║    - Conversations     : Full dialogue history                      ║
║    - Preferences       : User likes, dislikes, settings             ║
║    - Habits            : Patterns Echo learns over time             ║
║    - Health States     : Vital layer data                           ║
║    - Emotional Context : How user felt during interactions          ║
║    - Layer Contexts    : Per-layer persistent data                  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import uuid
import logging
import threading
import multiprocessing
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum


log = logging.getLogger("EchoCore.Memory")

MEMORY_FILE      = "echo_memory.json"
SHORT_TERM_LIMIT = 50
MAX_WORKERS      = max(2, multiprocessing.cpu_count() - 1)


# ─────────────────────────────────────────────
#  TASK WEIGHT
# ─────────────────────────────────────────────

class TaskWeight(Enum):
    LIGHT    = 1
    MODERATE = 2
    HEAVY    = 3
    CRITICAL = 4


# ─────────────────────────────────────────────
#  MEMORY ENTRY
# ─────────────────────────────────────────────

@dataclass
class MemoryEntry:
    entry_id:      str  = field(default_factory=lambda: str(uuid.uuid4())[:10])
    session_id:    str  = ""
    timestamp:     str  = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    memory_type:   str  = "general"
    layer:         str  = "core"
    content:       Any  = None
    keywords:      List = field(default_factory=list)
    importance:    float = 0.5
    recall_count:  int  = 0
    last_recalled: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "MemoryEntry":
        return cls(**data)


# ─────────────────────────────────────────────
#  CONVERSATION TURN
# ─────────────────────────────────────────────

@dataclass
class ConversationTurn:
    turn_id:          str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    session_id:       str = ""
    timestamp:        str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_input:       str = ""
    echo_response:    str = ""
    layer_used:       str = ""
    emotion_detected: Optional[str] = None
    importance:       float = 0.5

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "ConversationTurn":
        return cls(**data)


# ─────────────────────────────────────────────
#  RESERVE MODE
#  Burst processing — simulates the hybrid chip's
#  extra processing layers in software
# ─────────────────────────────────────────────

class ReserveMode:
    """
    Software equivalent of the hybrid chip Reserve layer.

    When Echo detects a heavy task it activates Reserve Mode:
    - Spins up extra worker threads
    - Parallelizes the workload across CPU cores
    - Reports how much extra power was used
    - Returns to normal when done

    Simulates the physical chip diverting power
    to its reserve processing layers.
    """

    def __init__(self):
        self._active             = False
        self._activation_count   = 0
        self._tasks_boosted      = 0
        self._lock               = threading.Lock()
        self._thread_pool        = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        log.info(f"[RESERVE] Initialized. CPU workers available: {MAX_WORKERS}")

    @property
    def is_active(self) -> bool:
        return self._active

    def assess_task(self, task_description: str, data_size: int = 0) -> TaskWeight:
        """Decide how much power this task needs."""
        if data_size > 10000:
            return TaskWeight.CRITICAL
        if data_size > 1000:
            return TaskWeight.HEAVY

        heavy_kw    = ["quantum", "simulate", "trajectory", "compute all",
                       "deep analysis", "pattern match", "predict", "model"]
        moderate_kw = ["search", "find all", "history", "recall all", "summarize"]
        task_lower  = task_description.lower()

        for kw in heavy_kw:
            if kw in task_lower:
                return TaskWeight.HEAVY
        for kw in moderate_kw:
            if kw in task_lower:
                return TaskWeight.MODERATE

        return TaskWeight.LIGHT

    def execute(self, task_fn: Callable, *args,
                task_description: str = "",
                data_size: int = 0,
                **kwargs) -> Tuple[Any, Dict]:
        """
        Execute a task. Automatically activates Reserve Mode
        if the task weight demands it.
        Returns (result, execution_report).
        """
        weight     = self.assess_task(task_description, data_size)
        start_time = time.time()

        if weight in [TaskWeight.HEAVY, TaskWeight.CRITICAL]:
            result  = self._burst_execute(task_fn, *args, weight=weight, **kwargs)
            boosted = True
        else:
            result  = task_fn(*args, **kwargs)
            boosted = False

        elapsed = time.time() - start_time

        report = {
            "task_weight"      : weight.name,
            "reserve_activated": boosted,
            "workers_used"     : MAX_WORKERS if boosted else 1,
            "elapsed_ms"       : round(elapsed * 1000, 2),
            "description"      : task_description
        }

        if boosted:
            self._tasks_boosted += 1
            log.info(
                f"[RESERVE] Burst complete | "
                f"Weight: {weight.name} | "
                f"Time: {report['elapsed_ms']}ms"
            )

        return result, report

    def _burst_execute(self, task_fn: Callable, *args,
                       weight: TaskWeight = TaskWeight.HEAVY, **kwargs) -> Any:
        """Run task with boosted thread resources."""
        with self._lock:
            self._active = True
            self._activation_count += 1

        log.warning(
            f"[RESERVE MODE ACTIVATED] "
            f"Weight: {weight.name} | "
            f"Activation #{self._activation_count} | "
            f"Workers: {MAX_WORKERS}"
        )

        try:
            future = self._thread_pool.submit(task_fn, *args, **kwargs)
            result = future.result(timeout=30)
        finally:
            with self._lock:
                self._active = False

        return result

    def parallel_search(self, search_fn: Callable,
                        data_chunks: List[Any]) -> List[Any]:
        """Split a large search across multiple workers."""
        if not data_chunks:
            return []

        with self._lock:
            self._active = True

        results = []
        try:
            futures = [
                self._thread_pool.submit(search_fn, chunk)
                for chunk in data_chunks
            ]
            for future in as_completed(futures, timeout=30):
                partial = future.result()
                if partial:
                    results.extend(
                        partial if isinstance(partial, list) else [partial]
                    )
        finally:
            with self._lock:
                self._active = False

        return results

    def get_stats(self) -> Dict:
        return {
            "currently_active" : self._active,
            "total_activations": self._activation_count,
            "tasks_boosted"    : self._tasks_boosted,
            "available_workers": MAX_WORKERS
        }

    def shutdown(self):
        self._thread_pool.shutdown(wait=False)


# ─────────────────────────────────────────────
#  SHORT TERM MEMORY
# ─────────────────────────────────────────────

class ShortTermMemory:
    """
    Current conversation context.
    Fast, in-memory, limited size.
    Oldest entries roll off naturally like human working memory.
    """

    def __init__(self, session_id: str, limit: int = SHORT_TERM_LIMIT):
        self.session_id    = session_id
        self.limit         = limit
        self._turns: deque = deque(maxlen=limit)
        self._context: Dict = {}
        self._emotion_state: str = "neutral"

    def add_turn(self, user_input: str, echo_response: str,
                 layer: str = "core",
                 emotion: Optional[str] = None) -> ConversationTurn:
        turn = ConversationTurn(
            session_id       = self.session_id,
            user_input       = user_input,
            echo_response    = echo_response,
            layer_used       = layer,
            emotion_detected = emotion,
            importance       = self._assess_importance(user_input)
        )
        self._turns.append(turn)
        if emotion:
            self._emotion_state = emotion
        return turn

    def get_recent(self, n: int = 5) -> List[ConversationTurn]:
        turns = list(self._turns)
        return turns[-n:] if len(turns) >= n else turns

    def get_context_window(self) -> str:
        """
        Natural language context summary.
        Injected into Echo's processing so it knows
        what was just discussed — seamless continuity.
        """
        recent = self.get_recent(10)
        if not recent:
            return ""
        lines = []
        for turn in recent:
            lines.append(f"User: {turn.user_input}")
            if turn.echo_response:
                lines.append(f"Echo: {turn.echo_response[:100]}")
        return "\n".join(lines)

    def set_context(self, key: str, value: Any):
        self._context[key] = value

    def get_context(self, key: str) -> Optional[Any]:
        return self._context.get(key)

    def get_emotion_state(self) -> str:
        return self._emotion_state

    def _assess_importance(self, text: str) -> float:
        high = ["remember", "important", "never forget", "always",
                "critical", "urgent", "my name", "i am"]
        for kw in high:
            if kw in text.lower():
                return 0.9
        return 0.5

    def to_list(self) -> List[Dict]:
        return [t.to_dict() for t in self._turns]

    @property
    def turn_count(self) -> int:
        return len(self._turns)


# ─────────────────────────────────────────────
#  LONG TERM MEMORY
# ─────────────────────────────────────────────

class LongTermMemory:
    """
    Persistent memory — survives ALL sessions.
    Saved to disk. This is what makes Echo feel
    like it truly knows you across every conversation.
    """

    def __init__(self, memory_file: str = MEMORY_FILE):
        self._file               = memory_file
        self._memories: Dict     = defaultdict(list)
        self._facts: Dict        = {}
        self._habits: Dict       = {}
        self._layer_contexts: Dict = {}
        self._conversation_log: List[ConversationTurn] = []
        self._lock               = threading.Lock()
        self._load()

        log.info(
            f"[LONG_TERM] Online | "
            f"Entries: {self._total_entries()} | "
            f"Facts: {len(self._facts)}"
        )

    # ── Write ──────────────────────────────────

    def store(self, entry: MemoryEntry):
        with self._lock:
            self._memories[entry.memory_type].append(entry)
            self._save()

    def store_turn(self, turn: ConversationTurn):
        with self._lock:
            self._conversation_log.append(turn)
            if len(self._conversation_log) > 1000:
                self._conversation_log = self._conversation_log[-1000:]
            self._save()

    def store_fact(self, key: str, value: Any, source: str = "user"):
        with self._lock:
            self._facts[key] = {
                "value"    : value,
                "source"   : source,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self._save()
        log.info(f"[LONG_TERM] Fact stored: {key} = {value}")

    def store_preference(self, key: str, value: Any, layer: str = "core"):
        with self._lock:
            if "preferences" not in self._layer_contexts:
                self._layer_contexts["preferences"] = {}
            self._layer_contexts["preferences"][key] = {
                "value"    : value,
                "layer"    : layer,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self._save()

    def store_habit(self, habit_name: str, pattern: Dict):
        with self._lock:
            self._habits[habit_name] = {
                **pattern,
                "detected_at": datetime.now(timezone.utc).isoformat()
            }
            self._save()

    def set_layer_context(self, layer: str, key: str, value: Any):
        with self._lock:
            if layer not in self._layer_contexts:
                self._layer_contexts[layer] = {}
            self._layer_contexts[layer][key] = value
            self._save()

    # ── Read ───────────────────────────────────

    def get_fact(self, key: str) -> Optional[Any]:
        fact = self._facts.get(key)
        return fact["value"] if fact else None

    def get_all_facts(self) -> Dict:
        return {k: v["value"] for k, v in self._facts.items()}

    def get_preference(self, key: str) -> Optional[Any]:
        prefs = self._layer_contexts.get("preferences", {})
        pref  = prefs.get(key)
        return pref["value"] if pref else None

    def get_habit(self, habit_name: str) -> Optional[Dict]:
        return self._habits.get(habit_name)

    def get_all_habits(self) -> Dict:
        return dict(self._habits)

    def get_layer_context(self, layer: str) -> Dict:
        return self._layer_contexts.get(layer, {})

    def get_recent_conversations(self, n: int = 10) -> List[ConversationTurn]:
        return self._conversation_log[-n:]

    def search(self, query: str, memory_type: Optional[str] = None,
               limit: int = 10) -> List[MemoryEntry]:
        """Search long term memory by keyword."""
        query_lower = query.lower()
        results     = []

        pool = (
            self._memories.get(memory_type, [])
            if memory_type
            else [m for ml in self._memories.values() for m in ml]
        )

        for entry in pool:
            content_str   = str(entry.content).lower()
            keyword_match = any(kw in content_str for kw in query_lower.split())
            tag_match     = any(kw in entry.keywords for kw in query_lower.split())

            if keyword_match or tag_match:
                entry.recall_count  += 1
                entry.last_recalled  = datetime.now(timezone.utc).isoformat()
                results.append(entry)

        results.sort(key=lambda x: (x.importance, x.recall_count), reverse=True)
        return results[:limit]

    def build_user_summary(self) -> str:
        """
        Natural language summary of what Echo knows about the user.
        Injected into context so Echo feels like it remembers you
        across sessions — the human-like memory continuity.
        """
        lines = ["[ECHO MEMORY CONTEXT]"]

        if self._facts:
            lines.append("\nKnown Facts:")
            for key, data in self._facts.items():
                lines.append(f"  - {key}: {data['value']}")

        prefs = self._layer_contexts.get("preferences", {})
        if prefs:
            lines.append("\nYour Preferences:")
            for key, data in list(prefs.items())[:5]:
                lines.append(f"  - {key}: {data['value']}")

        if self._habits:
            lines.append("\nDetected Habits:")
            for name, data in list(self._habits.items())[:5]:
                lines.append(f"  - {name}: {data.get('description', 'detected')}")

        recent = self.get_recent_conversations(3)
        if recent:
            lines.append("\nRecent Conversations:")
            for turn in recent:
                lines.append(
                    f"  [{turn.timestamp[:10]}] "
                    f"You: {turn.user_input[:60]}"
                )

        return "\n".join(lines)

    # ── Persistence ────────────────────────────

    def _save(self):
        try:
            data = {
                "version"          : "0.2.0",
                "saved_at"         : datetime.now(timezone.utc).isoformat(),
                "facts"            : self._facts,
                "habits"           : self._habits,
                "layer_contexts"   : self._layer_contexts,
                "conversation_log" : [
                    t.to_dict() for t in self._conversation_log[-500:]
                ],
                "memories"         : {
                    k: [e.to_dict() for e in v[-200:]]
                    for k, v in self._memories.items()
                }
            }
            with open(self._file, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            log.error(f"[LONG_TERM] Save failed: {e}")

    def _load(self):
        if not os.path.exists(self._file):
            log.info("[LONG_TERM] No memory file found. Starting fresh.")
            return
        try:
            with open(self._file, "r") as f:
                data = json.load(f)

            self._facts          = data.get("facts", {})
            self._habits         = data.get("habits", {})
            self._layer_contexts = data.get("layer_contexts", {})

            for t in data.get("conversation_log", []):
                try:
                    self._conversation_log.append(ConversationTurn.from_dict(t))
                except Exception:
                    pass

            for mem_type, entries in data.get("memories", {}).items():
                for e in entries:
                    try:
                        self._memories[mem_type].append(MemoryEntry.from_dict(e))
                    except Exception:
                        pass

            log.info(f"[LONG_TERM] Loaded from {self._file}")
        except Exception as e:
            log.error(f"[LONG_TERM] Load failed: {e}")

    def _total_entries(self) -> int:
        return sum(len(v) for v in self._memories.values())

    def get_stats(self) -> Dict:
        return {
            "total_entries"      : self._total_entries(),
            "conversation_turns" : len(self._conversation_log),
            "known_facts"        : len(self._facts),
            "detected_habits"    : len(self._habits),
            "memory_file"        : self._file
        }


# ─────────────────────────────────────────────
#  ECHO MEMORY — MASTER ORCHESTRATOR
# ─────────────────────────────────────────────

class EchoMemory:
    """
    Master memory system for Echo AI.

    Manages short term (current session) and
    long term (cross-session persistent) memory.
    Automatically promotes important memories.
    Uses Reserve Mode for heavy operations.
    Auto-extracts facts from conversation.

    This is what gives Echo seamless human-like
    memory across every conversation.
    """

    def __init__(self, session_id: str):
        self.session_id    = session_id
        self.short_term    = ShortTermMemory(session_id)
        self.long_term     = LongTermMemory()
        self.reserve       = ReserveMode()
        self._fact_patterns = self._build_fact_patterns()

        log.info(
            f"[ECHO_MEMORY] Online | "
            f"Session: {session_id} | "
            f"Long term entries: {self.long_term._total_entries()}"
        )

    # ── Core Interface ─────────────────────────

    def remember(self, user_input: str, echo_response: str,
                 layer: str = "core",
                 emotion: Optional[str] = None) -> ConversationTurn:
        """
        Record a conversation exchange.
        Short term: always.
        Long term: always (promotes on importance).
        Auto-extracts facts silently.
        """
        turn = self.short_term.add_turn(
            user_input    = user_input,
            echo_response = echo_response,
            layer         = layer,
            emotion       = emotion
        )
        self.long_term.store_turn(turn)
        self._extract_facts(user_input)
        return turn

    def recall(self, query: str,
               include_long_term: bool = True) -> Dict:
        """
        Recall relevant memories for a query.
        Uses Reserve Mode if the search is heavy.
        Returns context for natural conversation continuity.
        """
        result = {
            "short_term_context": self.short_term.get_context_window(),
            "recent_turns"      : [],
            "relevant_memories" : [],
            "user_summary"      : "",
            "reserve_report"    : None
        }

        if include_long_term:
            data_size = self.long_term._total_entries()

            search_result, reserve_report = self.reserve.execute(
                self._do_search,
                query,
                task_description=f"memory recall: {query}",
                data_size=data_size
            )

            result["relevant_memories"] = [e.to_dict() for e in search_result]
            result["reserve_report"]    = reserve_report
            result["user_summary"]      = self.long_term.build_user_summary()
            result["recent_turns"]      = [
                t.to_dict() for t in
                self.long_term.get_recent_conversations(5)
            ]

        return result

    def know(self, key: str) -> Optional[Any]:
        """
        Quick fact lookup.
        echo.memory.know("name") → "Marcus"
        """
        return self.long_term.get_fact(key)

    def learn(self, key: str, value: Any,
              memory_type: str = "preference"):
        """
        Explicitly store something Echo should always remember.
        Called when user says "remember that..." or "my name is..."
        """
        self.long_term.store_fact(key, value, source="explicit")
        entry = MemoryEntry(
            session_id  = self.session_id,
            memory_type = memory_type,
            layer       = "core",
            content     = {key: value},
            keywords    = [key, str(value)[:20]],
            importance  = 0.9
        )
        self.long_term.store(entry)
        log.info(f"[ECHO_MEMORY] Learned: {key} = {value}")

    def get_greeting_context(self) -> str:
        """
        Context for Echo's opening greeting each session.
        Makes Echo say "Good morning Marcus, you mentioned
        yesterday you wanted to review your budget"
        instead of acting like you've never met.
        """
        facts  = self.long_term.get_all_facts()
        recent = self.long_term.get_recent_conversations(3)
        habits = self.long_term.get_all_habits()
        parts  = []

        if "name" in facts:
            parts.append(f"User's name: {facts['name']}")

        if recent:
            last = recent[-1]
            parts.append(
                f"Last interaction: {last.timestamp[:10]} — "
                f"Topic: {last.user_input[:80]}"
            )

        if habits:
            for name in list(habits.keys())[:2]:
                parts.append(f"Known habit: {name}")

        return "\n".join(parts) if parts else "New user — no prior history."

    def set_layer_memory(self, layer: str, key: str, value: Any):
        self.long_term.set_layer_context(layer, key, value)

    def get_layer_memory(self, layer: str) -> Dict:
        return self.long_term.get_layer_context(layer)

    # ── Fact Extraction ────────────────────────

    def _build_fact_patterns(self) -> List[Tuple[str, str]]:
        return [
            ("my name is",    "name"),
            ("i am called",   "name"),
            ("call me",       "name"),
            ("i work at",     "workplace"),
            ("i work as",     "job"),
            ("i am a",        "job"),
            ("i live in",     "location"),
            ("i'm from",      "origin"),
            ("i study",       "studying"),
            ("i go to",       "school"),
            ("i like",        "preference"),
            ("i love",        "preference"),
            ("i hate",        "dislike"),
            ("i don't like",  "dislike"),
            ("i'm allergic",  "health_alert"),
            ("my birthday",   "birthday"),
        ]

    def _extract_facts(self, text: str):
        """
        Silently extract facts from conversation.
        Like a human naturally remembering what you tell them.
        """
        text_lower = text.lower().strip()
        for pattern, fact_key in self._fact_patterns:
            if pattern in text_lower:
                idx   = text_lower.find(pattern) + len(pattern)
                value = text[idx:].strip().split(".")[0].split(",")[0].strip()
                if value and len(value) < 100:
                    existing = self.long_term.get_fact(fact_key)
                    if not existing or fact_key in ["preference", "dislike"]:
                        self.long_term.store_fact(
                            fact_key, value, source="auto_extracted"
                        )
                        log.info(
                            f"[ECHO_MEMORY] Auto-extracted: "
                            f"{fact_key} = '{value}'"
                        )

    def _do_search(self, query: str) -> List[MemoryEntry]:
        return self.long_term.search(query, limit=15)

    # ── Stats ──────────────────────────────────

    def get_stats(self) -> Dict:
        return {
            "session_id"       : self.session_id,
            "short_term_turns" : self.short_term.turn_count,
            "long_term"        : self.long_term.get_stats(),
            "reserve_mode"     : self.reserve.get_stats(),
            "emotion_state"    : self.short_term.get_emotion_state()
        }

    def shutdown(self):
        self.long_term._save()
        self.reserve.shutdown()
        log.info("[ECHO_MEMORY] Shutdown. All memories saved.")


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║        ECHO MEMORY SYSTEM — TEST            ║
╚══════════════════════════════════════════════╝
    """)

    session = str(uuid.uuid4())[:8]
    memory  = EchoMemory(session_id=session)

    print("\n[1] STORING CONVERSATIONS")
    print("─" * 45)
    memory.remember("My name is Marcus", "Nice to meet you Marcus!", "core")
    memory.remember("I work as an engineer", "Got it, I'll remember that.", "core")
    memory.remember("Help me study for my quantum physics exam",
                    "Let's start with wave functions.", "scholar")
    memory.remember("What's the market looking like?",
                    "Let me check that for you.", "nexus")
    memory.remember("I love jazz music", "Great taste!", "core")
    print("  5 turns stored")

    print("\n[2] FACT RECALL")
    print("─" * 45)
    print(f"  Name : {memory.know('name')}")
    print(f"  Job  : {memory.know('job')}")

    print("\n[3] GREETING CONTEXT (cross-session)")
    print("─" * 45)
    print(memory.get_greeting_context())

    print("\n[4] MEMORY SEARCH")
    print("─" * 45)
    results = memory.recall("quantum physics")
    print(f"  Memories found    : {len(results['relevant_memories'])}")
    print(f"  Reserve activated : {results['reserve_report']['reserve_activated']}")
    print(f"  Search time       : {results['reserve_report']['elapsed_ms']}ms")

    print("\n[5] RESERVE MODE — HEAVY TASK")
    print("─" * 45)
    result, report = memory.reserve.execute(
        lambda n: sum(i * i for i in range(n)),
        100000,
        task_description="quantum simulation compute",
        data_size=100000
    )
    print(f"  Task weight    : {report['task_weight']}")
    print(f"  Reserve used   : {report['reserve_activated']}")
    print(f"  Workers        : {report['workers_used']}")
    print(f"  Time           : {report['elapsed_ms']}ms")

    print("\n[6] EXPLICIT LEARNING")
    print("─" * 45)
    memory.learn("favorite_color", "blue")
    memory.learn("wake_time", "6:00 AM")
    print(f"  Favorite color : {memory.know('favorite_color')}")
    print(f"  Wake time      : {memory.know('wake_time')}")

    print("\n[7] FULL STATS")
    print("─" * 45)
    stats = memory.get_stats()
    print(f"  Short term turns : {stats['short_term_turns']}")
    print(f"  Long term entries: {stats['long_term']['total_entries']}")
    print(f"  Known facts      : {stats['long_term']['known_facts']}")
    print(f"  Reserve stats    : {stats['reserve_mode']}")

    memory.shutdown()
    print("\n  Memory test complete. echo_memory.json saved.")
