"""
╔══════════════════════════════════════════════════════════════════════╗
║                ECHO AI — PERSONALITY ENGINE                          ║
║         Learn · Adapt · Match · Become Familiar                     ║
║                                                                      ║
║  Echo learns who you are over time — not just what you want,        ║
║  but HOW you are. Your speech. Your vibe. Your energy.              ║
║  Then Echo matches it. Naturally. Without being asked.              ║
║                                                                      ║
║  MODULES:                                                            ║
║    - SpeechPatternLearner  : Vocabulary, slang, sentence style      ║
║    - ToneDetector          : Mood and energy from text              ║
║    - PersonalityFingerprint: Who you are across time                ║
║    - VibeEngine            : Real-time energy matching              ║
║    - ResponseAdaptor       : Rewrites Echo responses in your style  ║
║    - PersonalityMemory     : Persists everything across sessions    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import re
import json
import math
import uuid
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter
from enum import Enum


log = logging.getLogger("EchoCore.Personality")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class CommunicationStyle(Enum):
    FORMAL      = "formal"       # Professional, structured
    CASUAL      = "casual"       # Relaxed, conversational
    DIRECT      = "direct"       # Short, punchy, no fluff
    DETAILED    = "detailed"     # Thorough, explanatory
    PLAYFUL     = "playful"      # Humorous, light
    TECHNICAL   = "technical"    # Jargon-heavy, precise
    EMOTIONAL   = "emotional"    # Feeling-forward
    SLANG       = "slang"        # Heavy vernacular


class EnergyLevel(Enum):
    HIGH        = "high"         # Excited, fast, enthusiastic
    MEDIUM      = "medium"       # Balanced, steady
    LOW         = "low"          # Tired, slow, minimal
    STRESSED    = "stressed"     # Tense, urgent
    FOCUSED     = "focused"      # Calm, deliberate
    PLAYFUL     = "playful"      # Light, fun


class ResponseLength(Enum):
    ULTRA_SHORT = "ultra_short"  # 1 sentence
    SHORT       = "short"        # 2-3 sentences
    MEDIUM      = "medium"       # Paragraph
    LONG        = "long"         # Detailed
    ADAPTIVE    = "adaptive"     # Match complexity to question


# ─────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class SpeechProfile:
    """How a person communicates — their linguistic fingerprint."""
    # Vocabulary
    common_words:      Dict[str, int] = field(default_factory=dict)  # word → frequency
    favorite_phrases:  List[str]      = field(default_factory=list)
    slang_used:        List[str]      = field(default_factory=list)
    avoided_words:     List[str]      = field(default_factory=list)

    # Sentence style
    avg_sentence_length: float = 10.0   # words per sentence
    uses_short_sentences: bool = False
    uses_fragments:       bool = False   # "Yeah. Exactly. Cool."
    uses_questions:       bool = False   # Lots of "right?" "you know?"

    # Formality
    uses_contractions:    bool = True    # I'm, you're, don't
    uses_punctuation:     bool = True
    uses_emojis:          bool = False
    uses_caps_emphasis:   bool = False   # "This is AMAZING"
    uses_ellipsis:        bool = False   # "so yeah..."
    uses_exclamations:    bool = False

    # Language
    detected_language:    str  = "en"
    multilingual:         bool = False
    languages_used:       List[str] = field(default_factory=lambda: ["en"])

    # Formality score: 0.0 = very casual, 1.0 = very formal
    formality_score:      float = 0.5

    # Messages analyzed
    messages_analyzed:    int   = 0
    last_updated:         str   = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PersonalityFingerprint:
    """
    Who this person is — built from everything they've said.
    This is Echo's understanding of the user as a person.
    """
    user_id:          str   = "primary_user"

    # Communication
    preferred_style:  CommunicationStyle = CommunicationStyle.CASUAL
    preferred_length: ResponseLength     = ResponseLength.MEDIUM
    current_energy:   EnergyLevel        = EnergyLevel.MEDIUM

    # Personality traits (0.0 - 1.0 confidence)
    traits: Dict[str, float] = field(default_factory=lambda: {
        "analytical"   : 0.5,  # Likes data and reasoning
        "creative"     : 0.5,  # Likes creative approaches
        "direct"       : 0.5,  # Prefers blunt answers
        "humorous"     : 0.5,  # Appreciates jokes
        "technical"    : 0.5,  # Comfortable with jargon
        "curious"      : 0.5,  # Asks lots of follow-ups
        "decisive"     : 0.5,  # Makes quick decisions
        "detail_oriented": 0.5,# Wants full picture
        "visionary"    : 0.5,  # Big picture thinker
        "pragmatic"    : 0.5,  # Wants practical answers
    })

    # Interests (topic → engagement score)
    interests:        Dict[str, float] = field(default_factory=dict)
    disinterests:     List[str]        = field(default_factory=list)

    # Mood history
    mood_history:     List[str]        = field(default_factory=list)
    dominant_mood:    str              = "neutral"

    # Response preferences
    likes_analogies:  bool  = True
    likes_examples:   bool  = True
    likes_humor:      bool  = False
    likes_brevity:    bool  = False
    likes_depth:      bool  = True

    # Time-based patterns
    most_active_hours: List[int] = field(default_factory=list)
    typical_session_length: float = 0.0  # minutes

    # Confidence in this fingerprint
    confidence:       float = 0.0    # 0 = guessing, 1 = very sure
    interactions:     int   = 0      # Total interactions analyzed

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["preferred_style"]  = self.preferred_style.value
        d["preferred_length"] = self.preferred_length.value
        d["current_energy"]   = self.current_energy.value
        return d


# ─────────────────────────────────────────────
#  SPEECH PATTERN LEARNER
# ─────────────────────────────────────────────

class SpeechPatternLearner:
    """
    Analyzes every message from the user and builds
    a detailed linguistic fingerprint.

    Over time Echo knows:
    - Your most used words
    - Whether you use slang
    - How long your sentences are
    - Whether you use emojis
    - Your formality level
    - Whether you write in fragments
    """

    # Common words to ignore (stop words)
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at",
        "to", "for", "of", "with", "is", "are", "was", "were",
        "it", "this", "that", "i", "you", "he", "she", "we",
        "they", "my", "your", "his", "her", "our", "their", "be",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can", "not",
        "no", "so", "if", "as", "by", "from", "up", "about"
    }

    # Slang patterns
    SLANG_INDICATORS = [
        "ikr", "ngl", "tbh", "lol", "lmao", "fr", "no cap", "lowkey",
        "highkey", "vibe", "lit", "goated", "bussin", "slay", "periodt",
        "bet", "fam", "bro", "imo", "smh", "omg", "wtf", "nah",
        "yeah", "yep", "yup", "gonna", "wanna", "gotta", "kinda",
        "sorta", "dunno", "lemme", "gimme", "tryna", "prolly", "bout",
        "deadass", "no shot", "on god", "real talk", "say less",
        "idk", "idc", "imo", "btw", "fyi", "asap", "brb", "rn",
        "atm", "jk", "nvm", "tbf", "imo", "irl"
    ]

    # Formal language indicators
    FORMAL_INDICATORS = [
        "therefore", "furthermore", "consequently", "nevertheless",
        "regarding", "pursuant", "herein", "aforementioned",
        "subsequently", "notwithstanding", "wherein", "hereby",
        "respectfully", "sincerely", "accordingly", "thus"
    ]

    def __init__(self):
        self._word_freq: Counter  = Counter()
        self._phrase_freq: Counter = Counter()
        self._sentences_seen: int = 0
        self._total_words: int    = 0
        self._lock                = threading.Lock()

    def analyze(self, text: str, profile: SpeechProfile) -> SpeechProfile:
        """Analyze a message and update the speech profile."""
        if not text or len(text.strip()) < 3:
            return profile

        text_lower = text.lower().strip()
        words      = text_lower.split()
        sentences  = re.split(r'[.!?]+', text)
        sentences  = [s.strip() for s in sentences if s.strip()]

        with self._lock:
            profile.messages_analyzed += 1

            # Word frequency (excluding stop words)
            meaningful_words = [w for w in words
                                 if w.isalpha() and w not in self.STOP_WORDS
                                 and len(w) > 2]
            self._word_freq.update(meaningful_words)

            # Update most common words in profile
            top_words = dict(self._word_freq.most_common(50))
            profile.common_words = top_words

            # Sentence length
            if sentences:
                avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
                # Rolling average
                n = profile.messages_analyzed
                profile.avg_sentence_length = (
                    (profile.avg_sentence_length * (n-1) + avg_len) / n
                )
                profile.uses_short_sentences = profile.avg_sentence_length < 8

            # Fragment detection
            if any(len(s.split()) <= 3 for s in sentences if s):
                profile.uses_fragments = True

            # Style indicators
            profile.uses_contractions  = any(c in text_lower for c in
                                              ["'m", "'re", "'s", "'t", "'ll", "'ve"])
            profile.uses_emojis       |= bool(re.search(r'[\U0001F300-\U0001FFFF]', text))
            profile.uses_caps_emphasis|= bool(re.search(r'\b[A-Z]{2,}\b', text))
            profile.uses_ellipsis     |= "..." in text
            profile.uses_exclamations |= "!" in text

            # Slang detection
            found_slang = [s for s in self.SLANG_INDICATORS if s in text_lower]
            if found_slang:
                for slang in found_slang:
                    if slang not in profile.slang_used:
                        profile.slang_used.append(slang)

            # Formality score
            formal_count   = sum(1 for f in self.FORMAL_INDICATORS if f in text_lower)
            slang_count    = len(found_slang)
            formal_signal  = formal_count / max(len(words), 1)
            casual_signal  = slang_count  / max(len(words), 1)
            # Update formality score with rolling average
            new_formality  = min(1.0, max(0.0, 0.5 + formal_signal - casual_signal))
            profile.formality_score = (profile.formality_score * 0.8 + new_formality * 0.2)

            # Favorite phrases (2-3 word sequences used often)
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                if words[i] not in self.STOP_WORDS:
                    self._phrase_freq[phrase] += 1

            top_phrases = [p for p, c in self._phrase_freq.most_common(10) if c >= 2]
            profile.favorite_phrases = top_phrases

            profile.last_updated = datetime.now(timezone.utc).isoformat()

        return profile

    def get_dominant_style(self, profile: SpeechProfile) -> CommunicationStyle:
        """Determine the user's dominant communication style."""
        if profile.formality_score > 0.7:
            return CommunicationStyle.FORMAL
        if len(profile.slang_used) >= 5:
            return CommunicationStyle.SLANG
        if profile.uses_short_sentences and profile.uses_fragments:
            return CommunicationStyle.DIRECT
        if profile.uses_exclamations and profile.uses_emojis:
            return CommunicationStyle.PLAYFUL
        if profile.avg_sentence_length > 20:
            return CommunicationStyle.DETAILED
        return CommunicationStyle.CASUAL


# ─────────────────────────────────────────────
#  TONE DETECTOR
# ─────────────────────────────────────────────

class ToneDetector:
    """
    Detects the user's current tone and energy level
    from what they're saying.

    Not just sentiment — the whole vibe.
    Stressed, excited, playful, focused, tired.
    Echo reads it and matches it.
    """

    # Tone signal words
    TONE_SIGNALS = {
        EnergyLevel.HIGH: [
            "amazing", "incredible", "awesome", "wow", "yes!", "let's go",
            "excited", "love this", "genius", "brilliant", "perfect",
            "can't wait", "absolutely", "definitely", "100%", "fire",
            "🔥", "💪", "🚀", "!!!",  "omg", "insane"
        ],
        EnergyLevel.LOW: [
            "tired", "exhausted", "whatever", "idk", "meh", "fine",
            "i guess", "maybe", "not sure", "can't", "struggling",
            "difficult", "hard", "stuck", "confused", "lost",
            "😔", "😴", "😞", "ugh", "nvm"
        ],
        EnergyLevel.STRESSED: [
            "urgent", "asap", "immediately", "problem", "issue", "help",
            "broken", "error", "wrong", "failed", "crash", "deadline",
            "worried", "concerned", "scared", "anxious", "panic",
            "quickly", "fast", "now", "critical", "emergency", "!!!"
        ],
        EnergyLevel.PLAYFUL: [
            "haha", "lol", "lmao", "funny", "joke", "play", "fun",
            "😂", "🤣", "😄", "jk", "just kidding", "gotcha",
            "silly", "random", "weird", "okay but", "plot twist"
        ],
        EnergyLevel.FOCUSED: [
            "let's", "focus", "step by step", "specifically", "exactly",
            "precisely", "need to", "goal", "objective", "plan",
            "analyze", "detail", "careful", "thorough", "systematic"
        ]
    }

    def detect(self, text: str) -> Tuple[EnergyLevel, float]:
        """
        Detect energy level and confidence from text.
        Returns (energy_level, confidence_score).
        """
        text_lower = text.lower()
        scores: Dict[EnergyLevel, int] = defaultdict(int)

        for level, signals in self.TONE_SIGNALS.items():
            for signal in signals:
                if signal in text_lower:
                    scores[level] += 1

        if not scores:
            return EnergyLevel.MEDIUM, 0.3

        best  = max(scores, key=scores.get)
        total = sum(scores.values())
        conf  = min(0.95, scores[best] / max(total, 1) + 0.2)

        return best, conf

    def detect_mood(self, text: str) -> str:
        """Simple mood label from text."""
        text_lower = text.lower()

        mood_signals = {
            "happy"      : ["happy", "great", "wonderful", "love", "excited", "glad"],
            "frustrated" : ["frustrated", "annoyed", "ugh", "why", "doesn't work",
                            "broken", "angry", "fed up"],
            "curious"    : ["wonder", "how", "why", "what if", "interesting",
                            "curious", "tell me", "explain"],
            "focused"    : ["let's", "need to", "goal", "working on", "trying to",
                            "building", "creating"],
            "tired"      : ["tired", "exhausted", "long day", "so much", "can't even"],
            "confident"  : ["sure", "definitely", "absolutely", "no doubt", "of course"],
            "uncertain"  : ["maybe", "not sure", "idk", "might", "could be", "possibly"]
        }

        scores: Dict[str, int] = defaultdict(int)
        for mood, signals in mood_signals.items():
            for signal in signals:
                if signal in text_lower:
                    scores[mood] += 1

        return max(scores, key=scores.get) if scores else "neutral"


# ─────────────────────────────────────────────
#  INTEREST TRACKER
# ─────────────────────────────────────────────

class InterestTracker:
    """
    Tracks what topics the user engages with and how.
    Echo learns what lights you up and what bores you.

    Signs of interest: follow-up questions, longer messages,
    positive reactions, returning to a topic.
    Signs of disinterest: short replies, changing subject,
    "okay" / "sure" / "whatever" responses.
    """

    # Topic → related keywords
    TOPIC_MAP = {
        "technology"    : ["ai", "code", "software", "app", "tech", "computer",
                            "algorithm", "data", "api", "programming"],
        "finance"       : ["money", "invest", "stock", "market", "crypto",
                            "portfolio", "revenue", "business", "startup"],
        "science"       : ["physics", "quantum", "biology", "chemistry",
                            "research", "experiment", "hypothesis", "theory"],
        "music"         : ["song", "beat", "music", "artist", "album", "track",
                            "playlist", "genre", "dj", "produce"],
        "fitness"       : ["workout", "gym", "exercise", "health", "training",
                            "run", "lift", "nutrition", "diet"],
        "creativity"    : ["create", "design", "art", "write", "build",
                            "imagine", "story", "poetry", "draw"],
        "philosophy"    : ["why", "meaning", "consciousness", "ethics",
                            "truth", "reality", "existence", "moral"],
        "gaming"        : ["game", "play", "level", "character", "strategy",
                            "rpg", "fps", "esports", "stream"],
        "travel"        : ["travel", "country", "city", "culture", "explore",
                            "visit", "trip", "adventure", "world"],
        "social"        : ["people", "relationship", "friend", "family",
                            "community", "social", "connect", "conversation"],
        "entrepreneurship": ["startup", "build", "launch", "product", "market",
                              "scale", "investor", "pitch", "vision"],
    }

    def __init__(self):
        self._topic_interactions: Dict[str, List[Dict]] = defaultdict(list)

    def record(self, text: str, response_length: int, follow_up: bool = False):
        """Record a topic interaction."""
        text_lower = text.lower()
        found_topics = []

        for topic, keywords in self.TOPIC_MAP.items():
            hits = sum(1 for kw in keywords if kw in text_lower)
            if hits > 0:
                found_topics.append((topic, hits))

        for topic, hits in found_topics:
            # Engagement score: more words = more engaged
            engagement = min(1.0, (len(text.split()) / 20) * 0.5 +
                                   (hits / 5) * 0.3 +
                                   (0.2 if follow_up else 0))
            self._topic_interactions[topic].append({
                "engagement": engagement,
                "timestamp" : datetime.now(timezone.utc).isoformat()
            })

    def get_interest_scores(self) -> Dict[str, float]:
        """Get engagement score per topic."""
        scores = {}
        for topic, interactions in self._topic_interactions.items():
            if interactions:
                # Recent interactions weighted more heavily
                recent = interactions[-10:]
                avg    = sum(i["engagement"] for i in recent) / len(recent)
                scores[topic] = round(avg, 3)
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    def get_top_interests(self, n: int = 5) -> List[str]:
        return list(self.get_interest_scores().keys())[:n]


# ─────────────────────────────────────────────
#  VIBE ENGINE
# ─────────────────────────────────────────────

class VibeEngine:
    """
    The real-time energy matching system.

    JARVIS matched Tony's energy perfectly.
    Dry and precise when Tony was serious.
    Sharp and quick when Tony was in a hurry.
    Playful when Tony was in a good mood.

    The Vibe Engine reads the user's current energy
    and adjusts Echo's entire response style in real time.
    Not just tone — vocabulary, sentence length,
    punctuation, humor level, everything.
    """

    def get_response_style(self, energy: EnergyLevel,
                            personality: PersonalityFingerprint,
                            speech: SpeechProfile) -> Dict:
        """
        Build a complete response style guide for this moment.
        Every layer uses this to adapt their output.
        """
        base = {
            "energy"          : energy.value,
            "formality"       : speech.formality_score,
            "sentence_length" : "short" if speech.uses_short_sentences else "medium",
            "use_slang"       : len(speech.slang_used) >= 3,
            "use_emoji"       : speech.uses_emojis,
            "use_humor"       : personality.likes_humor,
            "use_analogies"   : personality.likes_analogies,
            "use_examples"    : personality.likes_examples,
            "response_length" : personality.preferred_length.value,
            "technical_depth" : personality.traits.get("technical", 0.5) > 0.6,
        }

        # Energy-specific overrides
        if energy == EnergyLevel.HIGH:
            base["sentence_length"] = "short"
            base["punctuation"]     = "exclamatory"
            base["opener"]          = self._high_energy_opener()
            base["pace"]            = "fast"

        elif energy == EnergyLevel.LOW:
            base["sentence_length"] = "medium"
            base["punctuation"]     = "gentle"
            base["opener"]          = self._low_energy_opener()
            base["pace"]            = "slow"

        elif energy == EnergyLevel.STRESSED:
            base["sentence_length"] = "ultra_short"
            base["punctuation"]     = "direct"
            base["opener"]          = self._stressed_opener()
            base["pace"]            = "immediate"
            base["skip_preamble"]   = True

        elif energy == EnergyLevel.PLAYFUL:
            base["use_humor"]       = True
            base["sentence_length"] = "varied"
            base["opener"]          = self._playful_opener()
            base["pace"]            = "bouncy"

        elif energy == EnergyLevel.FOCUSED:
            base["sentence_length"] = "precise"
            base["opener"]          = self._focused_opener()
            base["pace"]            = "measured"
            base["use_structure"]   = True

        else:  # MEDIUM
            base["opener"]          = self._neutral_opener()
            base["pace"]            = "normal"

        return base

    def _high_energy_opener(self) -> str:
        import random
        options = [
            "Let's go!", "On it!", "Absolutely!", "Yes!", "Right away!"
        ]
        return random.choice(options)

    def _low_energy_opener(self) -> str:
        import random
        options = [
            "Sure.", "Of course.", "Here you go.", "Alright."
        ]
        return random.choice(options)

    def _stressed_opener(self) -> str:
        import random
        options = [
            "On it.", "Got it.", "Here:", "Right —"
        ]
        return random.choice(options)

    def _playful_opener(self) -> str:
        import random
        options = [
            "Okay okay okay —", "Oh this is fun.", "Alright, let's see...",
            "I like this question."
        ]
        return random.choice(options)

    def _focused_opener(self) -> str:
        import random
        options = [
            "Let's break this down.", "Here's what I've got:",
            "Step by step:", "Clear answer:"
        ]
        return random.choice(options)

    def _neutral_opener(self) -> str:
        import random
        options = [
            "Sure.", "Here's what I found:", "Good question.",
            "Of course.", ""
        ]
        return random.choice(options)


# ─────────────────────────────────────────────
#  RESPONSE ADAPTOR
# ─────────────────────────────────────────────

class ResponseAdaptor:
    """
    Rewrites Echo's responses to match the user's style.

    This is the final step — every response passes through
    here before being delivered. The adaptor applies
    the learned style to the raw layer output.

    Over time the user stops noticing Echo is adapting —
    it just feels natural, like talking to someone who
    actually gets them.
    """

    def adapt(self, response: str, style: Dict,
               speech_profile: SpeechProfile) -> str:
        """
        Adapt a response to match the user's style.
        """
        if not response or len(response) < 10:
            return response

        adapted = response

        # Apply length preference
        length_pref = style.get("response_length", "medium")
        if length_pref == "ultra_short":
            adapted = self._shorten(adapted, max_sentences=1)
        elif length_pref == "short":
            adapted = self._shorten(adapted, max_sentences=2)

        # Apply slang if user uses it heavily
        if style.get("use_slang") and len(speech_profile.slang_used) >= 5:
            adapted = self._apply_casual_tone(adapted)

        # Apply emoji if user uses them
        if style.get("use_emoji") and speech_profile.uses_emojis:
            adapted = self._add_contextual_emoji(adapted)

        # Skip preamble for stressed users
        if style.get("skip_preamble"):
            adapted = self._strip_preamble(adapted)

        # Add opener if style specifies one
        opener = style.get("opener", "")
        if opener and not adapted.startswith(opener):
            adapted = f"{opener} {adapted}"

        return adapted.strip()

    def _shorten(self, text: str, max_sentences: int = 2) -> str:
        """Keep only the most important sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s for s in sentences if s.strip()]
        return " ".join(sentences[:max_sentences])

    def _apply_casual_tone(self, text: str) -> str:
        """
        Make text more casual — not by adding slang randomly
        but by removing stiff phrases.
        """
        replacements = {
            "I would recommend"   : "I'd say",
            "It is important to"  : "Make sure to",
            "In order to"         : "To",
            "Additionally"        : "Also",
            "Furthermore"         : "Plus",
            "Nevertheless"        : "Still",
            "Consequently"        : "So",
            "Subsequently"        : "Then",
            "Please note that"    : "Note:",
            "It should be noted"  : "Worth knowing —",
            "As a result"         : "So",
            "In conclusion"       : "Bottom line:",
            "To summarize"        : "In short:"
        }
        result = text
        for formal, casual in replacements.items():
            result = result.replace(formal, casual)
        return result

    def _add_contextual_emoji(self, text: str) -> str:
        """
        Add a single relevant emoji based on content.
        Not randomly — contextually.
        """
        text_lower = text.lower()
        emoji_map = {
            "great"     : " 🔥",
            "warning"   : " ⚠️",
            "success"   : " ✅",
            "money"     : " 💰",
            "security"  : " 🔒",
            "health"    : " 💪",
            "learning"  : " 📚",
            "create"    : " 🎨",
            "music"     : " 🎵",
            "idea"      : " 💡",
        }
        for keyword, emoji in emoji_map.items():
            if keyword in text_lower and not any(e in text for e in emoji_map.values()):
                return text + emoji
        return text

    def _strip_preamble(self, text: str) -> str:
        """
        Remove filler openers for stressed/direct users.
        'Of course, I'd be happy to help you with that.' → just the content.
        """
        preambles = [
            "Of course, ", "Certainly, ", "Sure, ", "Absolutely, ",
            "Great question! ", "I'd be happy to help! ",
            "That's a great point. ", "No problem! ",
            "I understand. ", "Let me explain. "
        ]
        result = text
        for p in preambles:
            if result.startswith(p):
                result = result[len(p):]
        return result.strip().capitalize()


# ─────────────────────────────────────────────
#  PERSONALITY ENGINE — MASTER CLASS
# ─────────────────────────────────────────────

class PersonalityEngine:
    """
    The core of Echo's personality learning system.

    Every message the user sends teaches Echo something.
    Every response Echo gives gets adapted to match.
    Over time Echo knows the user better than any AI ever has.

    This is what makes Echo feel less like software
    and more like someone who genuinely knows you.
    """

    PERSONALITY_FILE = "echo_personality.json"

    def __init__(self, user_id: str = "primary_user"):
        self.user_id      = user_id
        self.speech       = SpeechPatternLearner()
        self.tone         = ToneDetector()
        self.interests    = InterestTracker()
        self.vibe         = VibeEngine()
        self.adaptor      = ResponseAdaptor()

        # Load or create profiles
        self.speech_profile = SpeechProfile()
        self.fingerprint    = PersonalityFingerprint(user_id=user_id)

        self._interaction_count = 0
        self._lock = threading.Lock()

        self._load()

        log.info(
            f"[PERSONALITY] Engine online | "
            f"User: {user_id} | "
            f"Interactions: {self.fingerprint.interactions} | "
            f"Style: {self.fingerprint.preferred_style.value}"
        )

    def observe(self, user_message: str,
                 previous_response: Optional[str] = None) -> Dict:
        """
        The main learning call — observe what the user said
        and update everything.

        Called on EVERY message. Silent. Fast.
        The user never knows Echo is learning.
        They just notice it starts to feel more natural.
        """
        with self._lock:
            self._interaction_count += 1
            self.fingerprint.interactions += 1

        # 1. Learn speech patterns
        self.speech_profile = self.speech.analyze(user_message, self.speech_profile)

        # 2. Detect current tone/energy
        energy, energy_conf = self.tone.detect(user_message)
        mood                = self.tone.detect_mood(user_message)
        self.fingerprint.current_energy = energy
        self.fingerprint.mood_history.append(mood)
        if len(self.fingerprint.mood_history) > 50:
            self.fingerprint.mood_history = self.fingerprint.mood_history[-50:]

        # Update dominant mood
        if self.fingerprint.mood_history:
            mood_counts = Counter(self.fingerprint.mood_history[-20:])
            self.fingerprint.dominant_mood = mood_counts.most_common(1)[0][0]

        # 3. Track interests
        self.interests.record(
            user_message,
            len(user_message.split()),
            follow_up=bool(previous_response and len(user_message) > 20)
        )

        # 4. Update personality traits from behavior
        self._update_traits(user_message)

        # 5. Update communication preferences
        self.fingerprint.preferred_style = self.speech.get_dominant_style(self.speech_profile)

        # Update response length preference
        msg_len = len(user_message.split())
        if msg_len < 5:
            self.fingerprint.preferred_length = ResponseLength.SHORT
        elif msg_len > 30:
            self.fingerprint.preferred_length = ResponseLength.LONG
        else:
            self.fingerprint.preferred_length = ResponseLength.MEDIUM

        # Update interests in fingerprint
        self.fingerprint.interests = self.interests.get_interest_scores()

        # Update confidence in our profile
        self.fingerprint.confidence = min(
            0.95,
            self.fingerprint.interactions / 100
        )

        # Active hours tracking
        current_hour = datetime.now(timezone.utc).hour
        if current_hour not in self.fingerprint.most_active_hours:
            self.fingerprint.most_active_hours.append(current_hour)
            if len(self.fingerprint.most_active_hours) > 8:
                self.fingerprint.most_active_hours = self.fingerprint.most_active_hours[-8:]

        # Auto-save every 10 interactions
        if self._interaction_count % 10 == 0:
            self._save()

        return {
            "energy"    : energy.value,
            "mood"      : mood,
            "style"     : self.fingerprint.preferred_style.value,
            "interests" : self.interests.get_top_interests(3),
            "confidence": round(self.fingerprint.confidence, 2)
        }

    def _update_traits(self, text: str):
        """Update personality traits from observed behavior."""
        text_lower = text.lower()

        trait_signals = {
            "analytical"    : ["analyze", "data", "reason", "logic", "think", "why",
                                "because", "therefore", "evidence", "prove"],
            "creative"      : ["create", "imagine", "design", "art", "music", "write",
                                "invent", "build", "concept", "idea"],
            "direct"        : len(text.split()) < 8,  # Short messages = direct
            "humorous"      : ["haha", "lol", "funny", "joke", "lmao", "😂", "😄"],
            "technical"     : ["code", "api", "algorithm", "system", "function",
                                "database", "server", "deploy", "debug"],
            "curious"       : ["?", "how", "why", "what if", "wonder", "tell me",
                                "explain", "curious"],
            "decisive"      : ["let's", "do it", "yes", "confirmed", "decided",
                                "going with", "choosing"],
            "detail_oriented": len(text.split()) > 25,  # Long messages = detail oriented
            "visionary"     : ["future", "imagine", "vision", "potential", "could be",
                                "what if", "someday", "eventually"],
            "pragmatic"     : ["practical", "works", "simple", "fast", "easy",
                                "efficient", "bottom line", "basically"]
        }

        for trait, signals in trait_signals.items():
            if isinstance(signals, bool):
                if signals:
                    self._nudge_trait(trait, 0.05)
                continue

            if isinstance(signals, list):
                hits = sum(1 for s in signals if s in text_lower)
                if hits > 0:
                    self._nudge_trait(trait, min(0.1, hits * 0.03))

    def _nudge_trait(self, trait: str, amount: float):
        """Gently shift a trait score — doesn't jump, it moves gradually."""
        current = self.fingerprint.traits.get(trait, 0.5)
        # Nudge toward signal but don't go extreme
        new_val = current + amount * (1 - current)  # Diminishing returns near 1.0
        self.fingerprint.traits[trait] = round(min(0.95, max(0.05, new_val)), 3)

    def get_response_style(self) -> Dict:
        """
        Get the current response style guide.
        Called by every layer before generating a response.
        """
        return self.vibe.get_response_style(
            energy      = self.fingerprint.current_energy,
            personality = self.fingerprint,
            speech      = self.speech_profile
        )

    def adapt_response(self, response: str) -> str:
        """
        Adapt a generated response to match user's style.
        Called as the final step before delivery.
        """
        # Only adapt once we have enough data
        if self.fingerprint.interactions < 5:
            return response

        style = self.get_response_style()
        return self.adaptor.adapt(response, style, self.speech_profile)

    def get_profile_summary(self) -> str:
        """
        Human-readable summary of what Echo knows about the user.
        Used in Memory layer's greeting context.
        """
        fp   = self.fingerprint
        sp   = self.speech_profile
        conf = fp.confidence

        if conf < 0.1:
            return "Still learning your communication style..."

        top_interests = self.interests.get_top_interests(3)
        top_traits    = sorted(
            fp.traits.items(), key=lambda x: x[1], reverse=True
        )[:3]

        lines = [f"[PERSONALITY PROFILE — {conf:.0%} confidence]"]
        lines.append(f"  Style    : {fp.preferred_style.value} | Energy: {fp.current_energy.value}")
        lines.append(f"  Formality: {'Formal' if sp.formality_score > 0.6 else 'Casual' if sp.formality_score < 0.4 else 'Mixed'}")

        if sp.slang_used:
            lines.append(f"  Your slang: {', '.join(sp.slang_used[:5])}")
        if top_interests:
            lines.append(f"  Interests: {', '.join(top_interests)}")
        if top_traits:
            dominant = top_traits[0]
            lines.append(f"  Dominant trait: {dominant[0]} ({dominant[1]:.0%})")
        lines.append(f"  Avg message: {sp.avg_sentence_length:.0f} words/sentence")
        lines.append(f"  Interactions analyzed: {fp.interactions}")

        return "\n".join(lines)

    def get_echo_greeting_for_user(self) -> str:
        """
        Generate a greeting in the user's style.
        Echo greets you the way YOU greet people.
        """
        fp    = self.fingerprint
        energy = fp.current_energy
        style  = fp.preferred_style

        import random

        if style == CommunicationStyle.SLANG:
            greetings = ["Yo!", "Wassup!", "What's good?"]
        elif style == CommunicationStyle.FORMAL:
            greetings = ["Good day.", "Welcome back.", "How may I assist you?"]
        elif style == CommunicationStyle.DIRECT:
            greetings = ["Hey.", "Back.", "Ready."]
        elif style == CommunicationStyle.PLAYFUL:
            greetings = ["Hey hey hey!", "You're back!", "Look who it is 👀"]
        else:
            greetings = ["Hey!", "Welcome back.", "Good to see you."]

        base = random.choice(greetings)

        # Add context from dominant interest
        top = self.interests.get_top_interests(1)
        if top and fp.confidence > 0.3:
            interest_hooks = {
                "technology"    : " Got some new AI developments to share.",
                "finance"       : " Markets have been moving.",
                "music"         : " Been working on something musical.",
                "fitness"       : " Ready to help you crush today.",
                "entrepreneurship": " Lot of good opportunities to talk through.",
            }
            hook = interest_hooks.get(top[0], "")
            base += hook

        return base

    def _save(self):
        """Persist personality data to disk."""
        try:
            data = {
                "version"       : "1.0",
                "user_id"       : self.user_id,
                "saved_at"      : datetime.now(timezone.utc).isoformat(),
                "fingerprint"   : self.fingerprint.to_dict(),
                "speech_profile": self.speech_profile.to_dict(),
                "interest_scores": self.interests.get_interest_scores()
            }
            with open(self.PERSONALITY_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            log.error(f"[PERSONALITY] Save error: {e}")

    def _load(self):
        """Load existing personality data."""
        import os
        if not os.path.exists(self.PERSONALITY_FILE):
            return
        try:
            with open(self.PERSONALITY_FILE, "r") as f:
                data = json.load(f)

            fp_data = data.get("fingerprint", {})
            sp_data = data.get("speech_profile", {})

            # Restore fingerprint
            if fp_data:
                self.fingerprint.interactions    = fp_data.get("interactions", 0)
                self.fingerprint.confidence      = fp_data.get("confidence", 0)
                self.fingerprint.traits          = fp_data.get("traits", self.fingerprint.traits)
                self.fingerprint.interests       = fp_data.get("interests", {})
                self.fingerprint.mood_history    = fp_data.get("mood_history", [])
                self.fingerprint.dominant_mood   = fp_data.get("dominant_mood", "neutral")
                self.fingerprint.most_active_hours = fp_data.get("most_active_hours", [])

                # Restore style enums
                try:
                    style_val = fp_data.get("preferred_style", "casual")
                    self.fingerprint.preferred_style = CommunicationStyle(style_val)
                except ValueError:
                    pass

                try:
                    energy_val = fp_data.get("current_energy", "medium")
                    self.fingerprint.current_energy = EnergyLevel(energy_val)
                except ValueError:
                    pass

            # Restore speech profile
            if sp_data:
                self.speech_profile.formality_score    = sp_data.get("formality_score", 0.5)
                self.speech_profile.avg_sentence_length = sp_data.get("avg_sentence_length", 10.0)
                self.speech_profile.uses_emojis        = sp_data.get("uses_emojis", False)
                self.speech_profile.uses_fragments     = sp_data.get("uses_fragments", False)
                self.speech_profile.uses_exclamations  = sp_data.get("uses_exclamations", False)
                self.speech_profile.slang_used         = sp_data.get("slang_used", [])
                self.speech_profile.common_words       = sp_data.get("common_words", {})
                self.speech_profile.messages_analyzed  = sp_data.get("messages_analyzed", 0)

            log.info(
                f"[PERSONALITY] Loaded | "
                f"Interactions: {self.fingerprint.interactions} | "
                f"Confidence: {self.fingerprint.confidence:.0%}"
            )

        except Exception as e:
            log.error(f"[PERSONALITY] Load error: {e}")

    def get_stats(self) -> Dict:
        return {
            "interactions"   : self.fingerprint.interactions,
            "confidence"     : round(self.fingerprint.confidence, 3),
            "style"          : self.fingerprint.preferred_style.value,
            "energy"         : self.fingerprint.current_energy.value,
            "dominant_mood"  : self.fingerprint.dominant_mood,
            "top_interests"  : self.interests.get_top_interests(5),
            "formality"      : round(self.speech_profile.formality_score, 2),
            "slang_detected" : speech_profile.slang_used[:5]
                               if (speech_profile := self.speech_profile).slang_used else [],
            "trait_profile"  : {k: round(v, 2)
                                 for k, v in sorted(self.fingerprint.traits.items(),
                                                    key=lambda x: x[1], reverse=True)[:5]}
        }


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║      ECHO PERSONALITY ENGINE — TEST         ║
╚══════════════════════════════════════════════╝
    """)

    engine = PersonalityEngine("test_user")

    # Simulate a user with a specific personality
    test_conversations = [
        # High energy, slang-heavy, tech-focused user
        "yo bro this is literally insane, the AI wrote the whole thing ngl",
        "fr fr i been working on this startup idea for mad long, finally making moves",
        "ight so the problem is the api keeps crashing lmao help",
        "bro quantum computing is CRAZY like how does it even work??",
        "lowkey this is the best thing i built ngl, what do you think?",
        "ight i need to know how to fix this bug rn, deadline is tomorrow",
        "tbh i learn better when someone explains it like im 5 lol",
        "this music production thing is my passion fr, beats are everything",
        "yo can you help me with the investment portfolio stuff? tryna secure the bag",
        "deadass i want to build something that changes the world no cap",
        "bro the code is bussin now, thanks fam",
        "okay okay so what if we added AI to the greenhouse idea?",
        "ngl i was stressed but this actually worked out lit",
        "can you make it shorter? i don't like reading long stuff lol",
        "fr though, how do i get investors interested? startup life is wild"
    ]

    print("  Simulating 15 interactions with a high-energy slang user...\n")
    for i, message in enumerate(test_conversations, 1):
        observation = engine.observe(message)
        if i % 5 == 0:
            print(f"  After {i} interactions:")
            print(f"    Energy    : {observation['energy']}")
            print(f"    Mood      : {observation['mood']}")
            print(f"    Style     : {observation['style']}")
            print(f"    Interests : {observation['interests']}")
            print(f"    Confidence: {observation['confidence']:.0%}")
            print()

    print("\n  ── PROFILE AFTER 15 INTERACTIONS ──\n")
    print(engine.get_profile_summary())

    print("\n  ── HOW ECHO GREETS THIS USER ──\n")
    print(f"  '{engine.get_echo_greeting_for_user()}'")

    print("\n  ── RESPONSE ADAPTATION TEST ──\n")
    formal_response = (
        "I would recommend that you consider restructuring your API "
        "to implement proper error handling. Furthermore, it is important "
        "to ensure that your endpoints are properly documented. "
        "Additionally, you should consider implementing rate limiting "
        "to prevent abuse of your service."
    )
    adapted = engine.adapt_response(formal_response)
    print(f"  ORIGINAL: {formal_response[:80]}...")
    print(f"  ADAPTED : {adapted[:80]}...")

    print("\n  ── STYLE GUIDE FOR THIS USER ──\n")
    style = engine.get_response_style()
    for k, v in style.items():
        print(f"  {k:<20}: {v}")

    print("\n  ── FULL STATS ──\n")
    stats = engine.get_stats()
    for k, v in stats.items():
        print(f"  {k:<20}: {v}")

    engine._save()
    print("\n  Personality data saved to echo_personality.json")
