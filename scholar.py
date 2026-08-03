"""
╔══════════════════════════════════════════════════════════════════════╗
║                   ECHO AI — SCHOLAR LAYER                           ║
║     Universal Knowledge · Master Teacher · Language Engine          ║
║                                                                      ║
║  PILLAR 1 — UNIVERSAL KNOWLEDGE LIBRARY                             ║
║    - Every field of human knowledge                                  ║
║    - Online + fully offline capable                                  ║
║    - Indexed, searchable, cross-referenced                           ║
║    - Constantly expanding when online                                ║
║                                                                      ║
║  PILLAR 2 — UNIVERSAL LANGUAGE ENGINE                               ║
║    - Understands, speaks, teaches any language                       ║
║    - Real-time translation                                           ║
║    - Auto language detection                                         ║
║    - Grammar, vocabulary, pronunciation                              ║
║    - Cultural context — not just words but meaning                   ║
║    - Offline capable for core languages                              ║
║                                                                      ║
║  PILLAR 3 — MASTER TEACHER                                          ║
║    - Teaches anything to anyone at any level                         ║
║    - Socratic method — questions that build understanding            ║
║    - Detects comprehension and adapts                                ║
║    - Child → PhD level adaptation                                    ║
║                                                                      ║
║  PILLAR 4 — STUDY SYSTEM                                            ║
║    - Flashcards, quizzes, spaced repetition                         ║
║    - Knowledge gap tracking                                          ║
║    - Scheduled study with breaks                                     ║
║    - Fun mode — trivia, games, jokes                                 ║
║                                                                      ║
║  JARVIS additions:                                                   ║
║    - Cross-domain synthesis (connects physics to music to law)       ║
║    - Proactive learning suggestions from other layers                ║
║    - Knowledge gap detection — Echo notices what you don't know      ║
║    - Research synthesis — compiles multi-source answers              ║
║    - Living knowledge — Scholar learns from every interaction        ║
║    - Expertise fingerprint — tracks your mastery per domain         ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import uuid
import time
import json
import math
import random
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


log = logging.getLogger("EchoCore.Scholar")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class KnowledgeLevel(Enum):
    """
    Depth of explanation Echo provides.
    JARVIS adapted his explanations to whoever
    he was talking to — technician vs scientist vs layman.
    """
    CHILD       = 1   # Ages 5-10, simple analogies, no jargon
    BEGINNER    = 2   # New to topic, clear fundamentals
    INTERMEDIATE= 3   # Some background, moderate depth
    ADVANCED    = 4   # Strong background, full technical detail
    EXPERT      = 5   # Peer-level, assume deep domain knowledge
    RESEARCH    = 6   # Cutting edge, citations, open questions


class LearningStyle(Enum):
    VISUAL      = "visual"       # Diagrams, charts, spatial
    AUDITORY    = "auditory"     # Verbal, rhythm, pattern
    READING     = "reading"      # Text-based, structured
    KINESTHETIC = "kinesthetic"  # Examples, practice, doing
    SOCRATIC    = "socratic"     # Questions and discovery


class Domain(Enum):
    MATHEMATICS     = "mathematics"
    PHYSICS         = "physics"
    CHEMISTRY       = "chemistry"
    BIOLOGY         = "biology"
    ASTRONOMY       = "astronomy"
    COMPUTER_SCIENCE= "computer_science"
    ENGINEERING     = "engineering"
    MEDICINE        = "medicine"
    HISTORY         = "history"
    GEOGRAPHY       = "geography"
    PHILOSOPHY      = "philosophy"
    PSYCHOLOGY      = "psychology"
    ECONOMICS       = "economics"
    LAW             = "law"
    LITERATURE      = "literature"
    LINGUISTICS     = "linguistics"
    ARTS            = "arts"
    MUSIC           = "music"
    POLITICS        = "politics"
    SOCIOLOGY       = "sociology"
    ANTHROPOLOGY    = "anthropology"
    RELIGION        = "religion"
    BUSINESS        = "business"
    TECHNOLOGY      = "technology"
    ENVIRONMENT     = "environment"
    GENERAL         = "general"


# ══════════════════════════════════════════════
#  PILLAR 1 — UNIVERSAL KNOWLEDGE LIBRARY
# ══════════════════════════════════════════════

@dataclass
class KnowledgeEntry:
    """A single piece of structured knowledge."""
    entry_id:    str   = field(default_factory=lambda: str(uuid.uuid4())[:10])
    domain:      str   = Domain.GENERAL.value
    topic:       str   = ""
    subtopic:    str   = ""
    title:       str   = ""
    content:     str   = ""            # Full content
    summary:     str   = ""            # One-line summary
    keywords:    List  = field(default_factory=list)
    related:     List  = field(default_factory=list)  # Related entry_ids
    level:       int   = 3             # 1-6 complexity
    offline:     bool  = True          # Available offline
    source:      str   = "echo_base"
    last_updated: str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    access_count: int  = 0

    def to_dict(self) -> Dict:
        return asdict(self)


class UniversalLibrary:
    """
    Echo's complete knowledge base —
    every field of human knowledge, structured and indexed.

    Built to work fully offline — the entire library
    compresses into structured data on the device.
    When online, it expands and updates continuously.

    JARVIS had access to every database Tony ever built.
    Scholar gives Echo access to all of human knowledge.
    """

    def __init__(self):
        self._entries: Dict[str, KnowledgeEntry] = {}
        self._domain_index: Dict[str, List[str]] = defaultdict(list)
        self._keyword_index: Dict[str, List[str]] = defaultdict(list)
        self._offline_mode: bool = False
        self._lock = threading.Lock()

        # Build the foundational knowledge base
        self._build_core_library()

        log.info(
            f"[SCHOLAR/LIBRARY] Initialized | "
            f"Entries: {len(self._entries)} | "
            f"Domains: {len(self._domain_index)}"
        )

    def _build_core_library(self):
        """Build the core knowledge base — every major domain."""
        core_knowledge = [

            # ── MATHEMATICS ──────────────────────────
            KnowledgeEntry(
                domain="mathematics", topic="calculus", subtopic="derivatives",
                title="Derivatives and Differentiation",
                content=(
                    "A derivative measures the rate of change of a function with respect "
                    "to a variable. Formally, f'(x) = lim(h→0) [f(x+h) - f(x)] / h. "
                    "Key rules: Power rule d/dx(xⁿ) = nxⁿ⁻¹, Product rule, Chain rule. "
                    "Applications: velocity (dx/dt), optimization, curve analysis. "
                    "In physics: velocity is the derivative of position, acceleration "
                    "is the derivative of velocity."
                ),
                summary="Rate of change of a function — the slope at any point.",
                keywords=["derivative", "differentiation", "calculus", "rate of change",
                          "slope", "limit", "power rule", "chain rule"],
                level=3
            ),
            KnowledgeEntry(
                domain="mathematics", topic="calculus", subtopic="integrals",
                title="Integration and Area Under Curves",
                content=(
                    "Integration is the reverse of differentiation. The definite integral "
                    "∫ₐᵇ f(x)dx gives the area under f(x) between a and b. "
                    "Fundamental theorem of calculus: ∫ₐᵇ f(x)dx = F(b) - F(a) where F'=f. "
                    "Methods: substitution, integration by parts, partial fractions. "
                    "Applications: area, volume, work, probability distributions."
                ),
                summary="The accumulation of quantities — area under a curve.",
                keywords=["integral", "integration", "calculus", "area", "antiderivative"],
                level=3
            ),
            KnowledgeEntry(
                domain="mathematics", topic="linear algebra", subtopic="matrices",
                title="Matrices and Linear Transformations",
                content=(
                    "A matrix is a rectangular array of numbers. Matrix multiplication "
                    "(AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ. Key operations: transpose, inverse (A⁻¹A=I), "
                    "determinant (det). Eigenvalues λ satisfy Av = λv. "
                    "Applications: computer graphics, machine learning (neural networks), "
                    "quantum mechanics, cryptography, systems of equations."
                ),
                summary="Arrays of numbers encoding linear transformations.",
                keywords=["matrix", "linear algebra", "eigenvalue", "determinant",
                          "vector", "transformation"],
                level=4
            ),
            KnowledgeEntry(
                domain="mathematics", topic="statistics", subtopic="probability",
                title="Probability Theory",
                content=(
                    "Probability P(A) ∈ [0,1] measures likelihood of event A. "
                    "P(A∪B) = P(A) + P(B) - P(A∩B). Bayes theorem: "
                    "P(A|B) = P(B|A)·P(A) / P(B). Key distributions: Normal (bell curve), "
                    "Binomial, Poisson, Exponential. Central Limit Theorem: sample means "
                    "approach normal distribution regardless of population distribution."
                ),
                summary="Mathematical framework for quantifying uncertainty.",
                keywords=["probability", "statistics", "bayes", "distribution",
                          "normal", "random variable"],
                level=3
            ),

            # ── PHYSICS ──────────────────────────────
            KnowledgeEntry(
                domain="physics", topic="quantum mechanics", subtopic="fundamentals",
                title="Quantum Mechanics — Core Principles",
                content=(
                    "Quantum mechanics governs matter at atomic/subatomic scales. "
                    "Wave-particle duality: particles exhibit both wave and particle properties. "
                    "Heisenberg Uncertainty: ΔxΔp ≥ ℏ/2 — cannot know position and momentum "
                    "simultaneously with perfect precision. Schrödinger equation describes "
                    "wavefunction evolution: iℏ∂ψ/∂t = Ĥψ. Superposition: particles exist in "
                    "multiple states until measured (observation collapses wavefunction). "
                    "Entanglement: correlated particles share quantum state regardless of distance."
                ),
                summary="Physics of the very small — where classical physics breaks down.",
                keywords=["quantum", "wave-particle", "uncertainty", "superposition",
                          "entanglement", "schrödinger", "wavefunction", "heisenberg"],
                level=4
            ),
            KnowledgeEntry(
                domain="physics", topic="relativity", subtopic="special",
                title="Einstein's Special Relativity",
                content=(
                    "Special relativity (1905) rests on two postulates: laws of physics are "
                    "identical in all inertial frames; speed of light c is constant in all frames. "
                    "Consequences: time dilation (t' = t/√(1-v²/c²)), length contraction, "
                    "mass-energy equivalence E=mc². Nothing with mass can reach c. "
                    "Simultaneity is relative — two observers may disagree on event order. "
                    "GPS satellites require relativistic corrections to remain accurate."
                ),
                summary="Space, time, and mass are interconnected — E=mc².",
                keywords=["relativity", "einstein", "E=mc²", "time dilation",
                          "speed of light", "spacetime", "mass-energy"],
                level=4
            ),
            KnowledgeEntry(
                domain="physics", topic="thermodynamics", subtopic="laws",
                title="Laws of Thermodynamics",
                content=(
                    "Zeroth Law: thermal equilibrium is transitive. "
                    "First Law: energy is conserved — ΔU = Q - W (internal energy = heat - work). "
                    "Second Law: entropy of isolated system never decreases — heat flows hot→cold. "
                    "Third Law: entropy approaches constant as temperature → absolute zero. "
                    "Entropy (S) measures disorder. These laws govern engines, refrigerators, "
                    "chemical reactions, and the arrow of time itself."
                ),
                summary="Energy, heat, and the direction of natural processes.",
                keywords=["thermodynamics", "entropy", "energy", "heat", "temperature",
                          "laws", "carnot", "second law"],
                level=3
            ),

            # ── COMPUTER SCIENCE ─────────────────────
            KnowledgeEntry(
                domain="computer_science", topic="algorithms", subtopic="sorting",
                title="Sorting Algorithms",
                content=(
                    "Bubble sort O(n²): repeatedly swap adjacent elements. "
                    "Merge sort O(n log n): divide, sort halves, merge — stable. "
                    "Quick sort O(n log n) avg, O(n²) worst: pivot partition — in-place. "
                    "Heap sort O(n log n): build max-heap, extract max. "
                    "Radix sort O(nk): digit-by-digit — works for integers. "
                    "Tim sort O(n log n): Python's built-in — hybrid merge/insertion. "
                    "Choice depends on: data size, memory constraints, stability needs."
                ),
                summary="Methods for ordering data — foundational CS knowledge.",
                keywords=["sorting", "algorithm", "merge sort", "quick sort", "bubble sort",
                          "complexity", "Big O", "heap sort"],
                level=3
            ),
            KnowledgeEntry(
                domain="computer_science", topic="machine learning", subtopic="neural networks",
                title="Neural Networks and Deep Learning",
                content=(
                    "Neural networks are layered computational graphs inspired by the brain. "
                    "Layers: input → hidden(s) → output. Each neuron: output = activation(Σwᵢxᵢ + b). "
                    "Training via backpropagation: compute loss, propagate gradients, update weights. "
                    "Activation functions: ReLU, sigmoid, tanh, softmax. "
                    "Architectures: CNN (images), RNN/LSTM (sequences), Transformer (attention). "
                    "Deep learning powers: image recognition, NLP, speech, game playing, drug discovery."
                ),
                summary="Layered computation models that learn from data.",
                keywords=["neural network", "deep learning", "backpropagation", "CNN",
                          "transformer", "weights", "gradient", "AI"],
                level=4
            ),

            # ── HISTORY ──────────────────────────────
            KnowledgeEntry(
                domain="history", topic="world history", subtopic="ancient civilizations",
                title="Ancient Civilizations",
                content=(
                    "Mesopotamia (3500 BCE): Sumer — first writing (cuneiform), cities, law (Hammurabi). "
                    "Ancient Egypt (3100 BCE): Nile civilization — pharaohs, pyramids, hieroglyphics. "
                    "Indus Valley (2600 BCE): Harappa, Mohenjo-daro — advanced urban planning. "
                    "Ancient China (2000 BCE): Shang dynasty — bronze, oracle bones, early writing. "
                    "Ancient Greece (800 BCE): democracy, philosophy (Socrates, Plato, Aristotle), "
                    "mathematics, Olympic games. Rome (753 BCE): republic → empire → influence "
                    "on law, language, architecture across Western civilization."
                ),
                summary="The foundations of human civilization from 3500 BCE onwards.",
                keywords=["ancient", "civilization", "mesopotamia", "egypt", "greece",
                          "rome", "history", "bronze age", "classical"],
                level=2
            ),
            KnowledgeEntry(
                domain="history", topic="modern history", subtopic="world wars",
                title="The World Wars (1914-1945)",
                content=(
                    "WWI (1914-1918): triggered by Franz Ferdinand assassination. "
                    "Allied Powers vs Central Powers. Trench warfare, 17M dead. "
                    "Treaty of Versailles — harsh terms on Germany. "
                    "WWII (1939-1945): Hitler's Nazi Germany invades Poland. "
                    "Axis (Germany, Italy, Japan) vs Allies (UK, France, USSR, USA). "
                    "Holocaust: 6M Jews murdered. D-Day 1944. Pacific theatre: Pearl Harbor, "
                    "atomic bombs on Hiroshima and Nagasaki. 70-85M total deaths. "
                    "Led to UN, Cold War, decolonization, modern world order."
                ),
                summary="Two global conflicts that shaped the modern world.",
                keywords=["world war", "WWI", "WWII", "hitler", "holocaust", "allied",
                          "axis", "nuclear", "D-Day", "cold war"],
                level=2
            ),

            # ── PHILOSOPHY ───────────────────────────
            KnowledgeEntry(
                domain="philosophy", topic="ethics", subtopic="moral theories",
                title="Major Ethical Theories",
                content=(
                    "Consequentialism (Utilitarianism): right action maximizes good outcomes. "
                    "Bentham/Mill: greatest happiness for greatest number. "
                    "Deontology (Kant): right action follows universal moral rules (categorical imperative). "
                    "Virtue ethics (Aristotle): right action flows from good character (virtues). "
                    "Contractarianism (Rawls): morality from principles rational agents would choose "
                    "behind 'veil of ignorance'. Care ethics: relationships and context matter. "
                    "These frameworks underlie all moral reasoning and AI ethics."
                ),
                summary="How to determine right from wrong — foundational moral frameworks.",
                keywords=["ethics", "morality", "utilitarianism", "deontology", "kant",
                          "virtue", "consequentialism", "philosophy"],
                level=3
            ),

            # ── ECONOMICS ────────────────────────────
            KnowledgeEntry(
                domain="economics", topic="macroeconomics", subtopic="monetary policy",
                title="Monetary Policy and Central Banking",
                content=(
                    "Central banks (Fed, ECB, BoE) control money supply and interest rates. "
                    "Tools: federal funds rate (benchmark rate), open market operations "
                    "(buying/selling bonds), reserve requirements, quantitative easing (QE). "
                    "Raising rates: reduces inflation, slows economy, strengthens currency. "
                    "Lowering rates: stimulates growth, increases inflation risk, weakens currency. "
                    "Taylor Rule: rate = neutral rate + 1.5×(inflation - target) + 0.5×output gap. "
                    "Inflation targeting: most central banks target ~2% inflation."
                ),
                summary="How central banks manage money supply and interest rates.",
                keywords=["monetary policy", "central bank", "interest rates", "inflation",
                          "federal reserve", "quantitative easing", "money supply"],
                level=4
            ),

            # ── BIOLOGY ──────────────────────────────
            KnowledgeEntry(
                domain="biology", topic="genetics", subtopic="DNA",
                title="DNA, Genes, and Heredity",
                content=(
                    "DNA (deoxyribonucleic acid): double helix of nucleotide base pairs "
                    "(A-T, G-C). Genes: DNA sequences encoding proteins. Human genome: ~3 billion "
                    "base pairs, ~20,000 protein-coding genes. DNA → RNA (transcription) → "
                    "protein (translation). Mendel's laws: dominant/recessive alleles, "
                    "independent assortment. Mutations: changes in DNA sequence — source of "
                    "evolution and genetic disease. CRISPR: gene editing technology that "
                    "can precisely modify DNA sequences."
                ),
                summary="The molecular blueprint of life — how traits are encoded and inherited.",
                keywords=["DNA", "gene", "genetics", "heredity", "chromosome", "RNA",
                          "protein", "mutation", "CRISPR", "genome"],
                level=3
            ),

            # ── CHEMISTRY ────────────────────────────
            KnowledgeEntry(
                domain="chemistry", topic="organic chemistry", subtopic="reactions",
                title="Organic Chemistry Fundamentals",
                content=(
                    "Organic chemistry: study of carbon-containing compounds. "
                    "Functional groups determine reactivity: hydroxyl (-OH), carbonyl (C=O), "
                    "carboxyl (-COOH), amino (-NH₂), phosphate. Key reactions: "
                    "substitution (replace one group), addition (add across double bond), "
                    "elimination (remove to form double bond), oxidation-reduction. "
                    "Isomers: same formula, different structure. Chirality: mirror-image "
                    "molecules (enantiomers) — critical in drug design. "
                    "Polymers: repeating monomer units — plastics, proteins, DNA."
                ),
                summary="Chemistry of carbon compounds — the chemistry of life.",
                keywords=["organic chemistry", "carbon", "functional group", "reaction",
                          "polymer", "isomer", "chirality", "molecule"],
                level=4
            ),

            # ── ENGINEERING ──────────────────────────
            KnowledgeEntry(
                domain="engineering", topic="electrical engineering", subtopic="circuits",
                title="Electrical Circuits — Fundamentals",
                content=(
                    "Ohm's Law: V = IR (voltage = current × resistance). "
                    "Kirchhoff's Laws: KVL (voltages around loop sum to zero), "
                    "KCL (currents at node sum to zero). "
                    "Series circuit: same current, voltages add. "
                    "Parallel circuit: same voltage, currents add. "
                    "Capacitor: stores charge — C = Q/V, blocks DC, passes AC. "
                    "Inductor: stores magnetic energy — opposes current change. "
                    "AC circuits: impedance Z = √(R² + (XL-XC)²). "
                    "Power P = IV = I²R = V²/R."
                ),
                summary="How voltage, current, and resistance relate in circuits.",
                keywords=["circuit", "ohms law", "voltage", "current", "resistance",
                          "capacitor", "inductor", "electrical engineering", "kirchhoff"],
                level=3
            ),

            # ── ASTRONOMY ────────────────────────────
            KnowledgeEntry(
                domain="astronomy", topic="cosmology", subtopic="universe structure",
                title="Structure and Scale of the Universe",
                content=(
                    "Observable universe: ~93 billion light-years diameter, ~2 trillion galaxies. "
                    "Milky Way: ~100,000 light-years across, 200-400 billion stars. "
                    "Solar system: Sun + 8 planets. Earth is 1 AU from Sun (150M km). "
                    "Nearest star: Proxima Centauri (4.24 light-years). "
                    "Universe age: ~13.8 billion years (Big Bang). "
                    "Dark matter: ~27% of universe — invisible, detected by gravity. "
                    "Dark energy: ~68% — drives accelerating expansion. "
                    "Cosmic web: galaxies form filaments and voids."
                ),
                summary="The vast structure of space from planets to the observable universe.",
                keywords=["universe", "galaxy", "star", "light year", "big bang",
                          "dark matter", "dark energy", "cosmology", "milky way"],
                level=2
            ),

            # ── LAW ──────────────────────────────────
            KnowledgeEntry(
                domain="law", topic="international law", subtopic="human rights",
                title="International Human Rights Law",
                content=(
                    "Universal Declaration of Human Rights (1948): 30 articles defining "
                    "fundamental rights. Key instruments: ICCPR (civil/political rights), "
                    "ICESCR (economic/social/cultural rights), CAT (against torture), "
                    "CRC (children's rights). Enforcement: UN Human Rights Council, "
                    "International Court of Justice, regional courts (ECHR, IACtHR). "
                    "Jus cogens: peremptory norms no state can violate — "
                    "genocide, slavery, torture prohibitions. "
                    "Humanitarian law (Geneva Conventions): rules of armed conflict."
                ),
                summary="The global framework protecting fundamental human rights.",
                keywords=["human rights", "international law", "UN", "UDHR", "treaty",
                          "genocide", "humanitarian", "court", "justice"],
                level=4
            ),

            # ── PSYCHOLOGY ───────────────────────────
            KnowledgeEntry(
                domain="psychology", topic="cognitive psychology", subtopic="memory",
                title="How Human Memory Works",
                content=(
                    "Memory systems: sensory (milliseconds), working memory (20-30 seconds, "
                    "~7±2 items), long-term memory (potentially lifetime). "
                    "Encoding: attention → elaboration → meaning. "
                    "Retrieval: recall (free), recognition (cued), relearning. "
                    "Forgetting: decay, interference, retrieval failure. "
                    "Spaced repetition: review at increasing intervals — optimal learning. "
                    "Sleep consolidates memories — deep sleep transfers to long-term. "
                    "Emotional events encoded more strongly (amygdala involvement)."
                ),
                summary="How the brain stores, retains, and retrieves information.",
                keywords=["memory", "working memory", "long-term", "encoding", "recall",
                          "forgetting", "spaced repetition", "sleep", "psychology"],
                level=2
            ),

            # ── ARTS & MUSIC ─────────────────────────
            KnowledgeEntry(
                domain="music", topic="music theory", subtopic="fundamentals",
                title="Music Theory Fundamentals",
                content=(
                    "Notes: A B C D E F G + sharps/flats = 12 chromatic pitches. "
                    "Scales: major (W W H W W W H), minor (W H W W H W W). "
                    "Intervals: unison, 2nd, 3rd (minor/major), 4th, 5th, octave. "
                    "Chords: triads (root+3rd+5th), 7ths, extended. "
                    "Rhythm: beats, meter (4/4, 3/4), tempo (BPM). "
                    "Key signatures: sharps/flats indicating home key. "
                    "Harmony: consonance (stable), dissonance (tension → resolution). "
                    "The circle of fifths: all 12 keys and their relationships."
                ),
                summary="The grammar of music — how notes, rhythms and harmony work.",
                keywords=["music theory", "scale", "chord", "rhythm", "harmony",
                          "interval", "melody", "key signature", "tempo"],
                level=3
            ),

            # ── ENVIRONMENT ──────────────────────────
            KnowledgeEntry(
                domain="environment", topic="climate science", subtopic="climate change",
                title="Climate Change — Science and Impact",
                content=(
                    "Greenhouse effect: CO₂, CH₄, N₂O, H₂O trap infrared radiation. "
                    "Pre-industrial CO₂: ~280 ppm. Current: ~420 ppm (highest in 800,000 years). "
                    "Global average temperature: +1.1°C above pre-industrial. "
                    "Impacts: sea level rise, extreme weather, species extinction, "
                    "ocean acidification, Arctic ice loss, coral bleaching. "
                    "Paris Agreement: limit warming to 1.5-2°C — requires net-zero by ~2050. "
                    "Mitigation: renewable energy, efficiency, carbon capture, diet change. "
                    "Tipping points: Amazon dieback, ice sheet collapse, permafrost thaw."
                ),
                summary="How human activities are changing Earth's climate and what it means.",
                keywords=["climate change", "global warming", "CO2", "greenhouse gas",
                          "paris agreement", "renewable energy", "carbon", "temperature"],
                level=3
            ),
        ]

        for entry in core_knowledge:
            self._add_entry(entry)

    def _add_entry(self, entry: KnowledgeEntry):
        """Add an entry to the library with full indexing."""
        with self._lock:
            self._entries[entry.entry_id] = entry
            self._domain_index[entry.domain].append(entry.entry_id)
            for kw in entry.keywords:
                self._keyword_index[kw.lower()].append(entry.entry_id)

    def search(self, query: str, domain: Optional[str] = None,
               limit: int = 5) -> List[KnowledgeEntry]:
        """
        Search the library by keyword, topic, or domain.
        Returns ranked results.
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        scores: Dict[str, float] = defaultdict(float)

        # Keyword index search
        for word in query_words:
            for kw, entry_ids in self._keyword_index.items():
                if word in kw or kw in word:
                    for eid in entry_ids:
                        scores[eid] += 2.0 if word == kw else 1.0

        # Title/content search
        for eid, entry in self._entries.items():
            for word in query_words:
                if word in entry.title.lower():
                    scores[eid] += 3.0
                if word in entry.topic.lower():
                    scores[eid] += 2.0
                if word in entry.content.lower():
                    scores[eid] += 0.5

        # Domain filter
        if domain:
            for eid in list(scores.keys()):
                if self._entries[eid].domain != domain:
                    scores[eid] *= 0.3

        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for eid, score in ranked[:limit]:
            if score > 0:
                entry = self._entries[eid]
                entry.access_count += 1
                results.append(entry)

        return results

    def get_by_domain(self, domain: str,
                      limit: int = 10) -> List[KnowledgeEntry]:
        """Get all entries for a domain."""
        entry_ids = self._domain_index.get(domain, [])
        return [self._entries[eid] for eid in entry_ids[:limit]
                if eid in self._entries]

    def get_related(self, entry_id: str) -> List[KnowledgeEntry]:
        """Get related entries — cross-domain connections."""
        entry = self._entries.get(entry_id)
        if not entry:
            return []
        related = []
        for rid in entry.related:
            if rid in self._entries:
                related.append(self._entries[rid])
        return related

    def get_stats(self) -> Dict:
        return {
            "total_entries"  : len(self._entries),
            "domains_covered": len(self._domain_index),
            "keywords_indexed": len(self._keyword_index),
            "offline_entries": sum(1 for e in self._entries.values() if e.offline),
            "domains"        : list(self._domain_index.keys())
        }

    def set_offline_mode(self, offline: bool):
        self._offline_mode = offline
        log.info(f"[SCHOLAR/LIBRARY] Offline mode: {offline}")


# ══════════════════════════════════════════════
#  PILLAR 2 — UNIVERSAL LANGUAGE ENGINE
# ══════════════════════════════════════════════

@dataclass
class Language:
    """Profile of a supported language."""
    code:         str   = ""     # ISO 639-1 code (en, fr, es...)
    name:         str   = ""     # English name
    native_name:  str   = ""     # Name in that language
    family:       str   = ""     # Language family
    script:       str   = ""     # Writing system
    rtl:          bool  = False  # Right to left
    speakers_m:   int   = 0      # Million speakers
    offline:      bool  = True   # Available offline
    difficulty:   int   = 1      # 1-5 for English speakers


class LanguageEngine:
    """
    Universal Language Engine.

    Echo understands, speaks, translates, and teaches
    any human language. Adapts to cultural context —
    not just literal translation but meaning.

    JARVIS understood multiple languages and adapted
    his communication style to every person he talked to.
    Echo does the same — and teaches languages too.
    """

    # Comprehensive language database
    LANGUAGES = {
        "en": Language("en", "English",    "English",      "Germanic",   "Latin",   False, 1500, True,  1),
        "es": Language("es", "Spanish",    "Español",      "Romance",    "Latin",   False, 543,  True,  2),
        "fr": Language("fr", "French",     "Français",     "Romance",    "Latin",   False, 280,  True,  2),
        "de": Language("de", "German",     "Deutsch",      "Germanic",   "Latin",   False, 135,  True,  3),
        "zh": Language("zh", "Chinese",    "中文",          "Sino-Tibetan","Hanzi",  False, 1120, True,  5),
        "ar": Language("ar", "Arabic",     "العربية",       "Semitic",    "Arabic",  True,  422,  True,  5),
        "hi": Language("hi", "Hindi",      "हिन्दी",         "Indo-Aryan", "Devanagari",False,600, True, 4),
        "pt": Language("pt", "Portuguese", "Português",    "Romance",    "Latin",   False, 258,  True,  2),
        "ru": Language("ru", "Russian",    "Русский",      "Slavic",     "Cyrillic",False, 258,  True,  4),
        "ja": Language("ja", "Japanese",   "日本語",         "Japonic",    "Kana/Kanji",False,125, True, 5),
        "ko": Language("ko", "Korean",     "한국어",          "Koreanic",   "Hangul",  False, 82,   True,  4),
        "it": Language("it", "Italian",    "Italiano",     "Romance",    "Latin",   False, 68,   True,  2),
        "nl": Language("nl", "Dutch",      "Nederlands",   "Germanic",   "Latin",   False, 30,   True,  2),
        "sv": Language("sv", "Swedish",    "Svenska",      "Germanic",   "Latin",   False, 13,   True,  2),
        "pl": Language("pl", "Polish",     "Polski",       "Slavic",     "Latin",   False, 45,   True,  3),
        "tr": Language("tr", "Turkish",    "Türkçe",       "Turkic",     "Latin",   False, 84,   True,  3),
        "vi": Language("vi", "Vietnamese", "Tiếng Việt",   "Austroasiatic","Latin", False, 96,   True,  4),
        "fa": Language("fa", "Persian",    "فارسی",         "Indo-Iranian","Arabic", True,  80,   True,  4),
        "sw": Language("sw", "Swahili",    "Kiswahili",    "Bantu",      "Latin",   False, 200,  True,  2),
        "ha": Language("ha", "Hausa",      "Hausa",        "Afro-Asiatic","Latin",  False, 85,   True,  3),
        "yo": Language("yo", "Yoruba",     "Yorùbá",       "Niger-Congo", "Latin",  False, 50,   True,  3),
        "ig": Language("ig", "Igbo",       "Igbo",         "Niger-Congo", "Latin",  False, 44,   True,  3),
        "am": Language("am", "Amharic",    "አማርኛ",          "Semitic",    "Ethiopic",False, 60,  True,  5),
        "he": Language("he", "Hebrew",     "עברית",         "Semitic",    "Hebrew",  True,  9,    True,  4),
        "bn": Language("bn", "Bengali",    "বাংলা",          "Indo-Aryan", "Bengali", False, 230, True,  4),
        "ur": Language("ur", "Urdu",       "اردو",          "Indo-Aryan", "Arabic",  True,  170,  True,  4),
        "ta": Language("ta", "Tamil",      "தமிழ்",          "Dravidian",  "Tamil",   False, 80,   True,  4),
        "id": Language("id", "Indonesian", "Bahasa Indonesia","Austronesian","Latin",False,199, True, 2),
        "ms": Language("ms", "Malay",      "Bahasa Melayu","Austronesian","Latin",  False, 290,  True,  2),
        "th": Language("th", "Thai",       "ภาษาไทย",        "Tai-Kadai",  "Thai",    False, 61,   True,  4),
        "el": Language("el", "Greek",      "Ελληνικά",     "Hellenic",   "Greek",   False, 13,   True,  3),
        "ro": Language("ro", "Romanian",   "Română",       "Romance",    "Latin",   False, 24,   True,  2),
        "cs": Language("cs", "Czech",      "Čeština",      "Slavic",     "Latin",   False, 10,   True,  3),
        "hu": Language("hu", "Hungarian",  "Magyar",       "Uralic",     "Latin",   False, 13,   True,  4),
        "fi": Language("fi", "Finnish",    "Suomi",        "Uralic",     "Latin",   False, 5,    True,  4),
        "no": Language("no", "Norwegian",  "Norsk",        "Germanic",   "Latin",   False, 5,    True,  2),
        "da": Language("da", "Danish",     "Dansk",        "Germanic",   "Latin",   False, 6,    True,  2),
        "uk": Language("uk", "Ukrainian",  "Українська",   "Slavic",     "Cyrillic",False, 45,   True,  4),
        "zu": Language("zu", "Zulu",       "isiZulu",      "Bantu",      "Latin",   False, 28,   True,  3),
        "xh": Language("xh", "Xhosa",     "isiXhosa",     "Bantu",      "Latin",   False, 19,   True,  3),
    }

    # Sample translations for demo (production: full translation model)
    GREETINGS = {
        "en": "Hello", "es": "Hola", "fr": "Bonjour", "de": "Hallo",
        "zh": "你好", "ar": "مرحبا", "hi": "नमस्ते", "pt": "Olá",
        "ru": "Привет", "ja": "こんにちは", "ko": "안녕하세요", "it": "Ciao",
        "sw": "Habari", "ha": "Sannu", "yo": "Bawo", "am": "ሰላም",
        "tr": "Merhaba", "nl": "Hallo", "pl": "Cześć", "th": "สวัสดี",
        "he": "שלום", "bn": "হ্যালো", "ta": "வணக்கம்", "id": "Halo"
    }

    COMMON_PHRASES = {
        "thank_you": {
            "en": "Thank you", "es": "Gracias", "fr": "Merci",
            "de": "Danke", "zh": "谢谢", "ar": "شكرا", "hi": "धन्यवाद",
            "pt": "Obrigado", "ru": "Спасибо", "ja": "ありがとう",
            "ko": "감사합니다", "sw": "Asante", "yo": "Ẹ ṣeun"
        },
        "yes": {
            "en": "Yes", "es": "Sí", "fr": "Oui", "de": "Ja",
            "zh": "是", "ar": "نعم", "hi": "हाँ", "pt": "Sim",
            "ru": "Да", "ja": "はい", "ko": "네", "sw": "Ndio"
        },
        "no": {
            "en": "No", "es": "No", "fr": "Non", "de": "Nein",
            "zh": "不", "ar": "لا", "hi": "नहीं", "pt": "Não",
            "ru": "Нет", "ja": "いいえ", "ko": "아니요", "sw": "Hapana"
        }
    }

    def __init__(self):
        self._detected_language: str = "en"
        self._user_languages: List[str] = ["en"]
        self._learning_progress: Dict[str, Dict] = defaultdict(dict)

    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Auto-detect language from text.
        In production: uses character n-gram model.
        Returns (language_code, confidence).
        """
        # Script-based detection (reliable for non-Latin scripts)
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return "zh", 0.95
        if any('\u0600' <= c <= '\u06ff' for c in text):
            return "ar", 0.95
        if any('\u0900' <= c <= '\u097f' for c in text):
            return "hi", 0.93
        if any('\u0400' <= c <= '\u04ff' for c in text):
            return "ru", 0.93
        if any('\u3040' <= c <= '\u30ff' for c in text):
            return "ja", 0.95
        if any('\uac00' <= c <= '\ud7af' for c in text):
            return "ko", 0.95
        if any('\u0e00' <= c <= '\u0e7f' for c in text):
            return "th", 0.93
        if any('\u1200' <= c <= '\u137f' for c in text):
            return "am", 0.93

        # Latin script — keyword heuristics
        text_lower = text.lower()
        lang_signals = {
            "es": ["que", "está", "para", "con", "una", "del", "los", "las"],
            "fr": ["que", "est", "pas", "vous", "les", "des", "une", "dans"],
            "de": ["ist", "die", "der", "das", "und", "mit", "nicht", "ich"],
            "pt": ["que", "está", "para", "com", "uma", "dos", "não"],
            "it": ["che", "con", "sono", "della", "questo", "una"],
            "nl": ["het", "een", "van", "zijn", "niet", "voor"],
            "pl": ["jest", "nie", "że", "się", "jak", "ale"],
            "tr": ["bir", "bu", "için", "ile", "olan", "daha"],
            "id": ["yang", "dan", "ini", "dengan", "untuk"],
            "sw": ["na", "ya", "wa", "ni", "kwa", "la"]
        }

        scores: Dict[str, int] = defaultdict(int)
        words = text_lower.split()
        for lang, signals in lang_signals.items():
            for signal in signals:
                if signal in words:
                    scores[lang] += 1

        if scores:
            best = max(scores, key=scores.get)
            confidence = min(0.85, scores[best] / 5)
            if confidence > 0.3:
                return best, confidence

        return "en", 0.6

    def translate(self, text: str, target_lang: str,
                  source_lang: Optional[str] = None) -> Dict:
        """
        Translate text to target language.
        In production: Neural machine translation model.
        """
        if not source_lang:
            source_lang, confidence = self.detect_language(text)
        else:
            confidence = 1.0

        source_info = self.LANGUAGES.get(source_lang, Language(source_lang, source_lang, source_lang))
        target_info = self.LANGUAGES.get(target_lang, Language(target_lang, target_lang, target_lang))

        # Check for common phrases
        translated = self._check_common_phrases(text, target_lang)

        return {
            "original"     : text,
            "translated"   : translated or f"[Translation: {text} → {target_info.name}]",
            "source_lang"  : source_lang,
            "source_name"  : source_info.name,
            "target_lang"  : target_lang,
            "target_name"  : target_info.name,
            "confidence"   : confidence,
            "rtl_target"   : target_info.rtl,
            "note"         : (
                "Full neural translation active." if translated
                else "Translation model will provide full output in production."
            )
        }

    def _check_common_phrases(self, text: str,
                               target_lang: str) -> Optional[str]:
        """Check if text is a common phrase we have."""
        text_lower = text.lower().strip()

        # Check greetings
        for lang, greeting in self.GREETINGS.items():
            if text_lower == greeting.lower():
                return self.GREETINGS.get(target_lang)

        # Check common phrases
        for phrase_key, translations in self.COMMON_PHRASES.items():
            for lang, phrase in translations.items():
                if text_lower == phrase.lower():
                    return translations.get(target_lang)

        return None

    def get_language_lesson(self, language_code: str,
                             lesson_type: str = "basics",
                             level: int = 1) -> Dict:
        """
        Generate a language lesson.
        Echo teaches any language from scratch.
        """
        lang = self.LANGUAGES.get(language_code)
        if not lang:
            return {"error": f"Language '{language_code}' not found"}

        lessons = {
            "basics": self._lesson_basics(lang),
            "greetings": self._lesson_greetings(lang),
            "numbers": self._lesson_numbers(lang),
            "grammar": self._lesson_grammar(lang),
            "culture": self._lesson_culture(lang),
            "pronunciation": self._lesson_pronunciation(lang)
        }

        lesson = lessons.get(lesson_type, lessons["basics"])

        # Track progress
        if language_code not in self._learning_progress:
            self._learning_progress[language_code] = {
                "lessons_completed": 0,
                "started_at": datetime.now(timezone.utc).isoformat()
            }
        self._learning_progress[language_code]["lessons_completed"] += 1

        return {
            "language"       : lang.name,
            "native_name"    : lang.native_name,
            "lesson_type"    : lesson_type,
            "level"          : level,
            "content"        : lesson,
            "difficulty"     : lang.difficulty,
            "family"         : lang.family,
            "speakers"       : f"{lang.speakers_m}M speakers worldwide",
            "offline"        : lang.offline,
            "progress"       : self._learning_progress.get(language_code, {})
        }

    def _lesson_basics(self, lang: Language) -> Dict:
        greeting = self.GREETINGS.get(lang.code, "Hello")
        thank_you = self.COMMON_PHRASES["thank_you"].get(lang.code, "Thank you")
        yes = self.COMMON_PHRASES["yes"].get(lang.code, "Yes")
        no  = self.COMMON_PHRASES["no"].get(lang.code, "No")

        return {
            "title"  : f"Introduction to {lang.name}",
            "content": f"{lang.name} ({lang.native_name}) belongs to the {lang.family} language family. It uses the {lang.script} script.",
            "phrases": [
                {"english": "Hello",      "translation": greeting,  "pronunciation": f"/{greeting}/"},
                {"english": "Thank you",  "translation": thank_you, "pronunciation": f"/{thank_you}/"},
                {"english": "Yes",        "translation": yes,       "pronunciation": f"/{yes}/"},
                {"english": "No",         "translation": no,        "pronunciation": f"/{no}/"},
            ],
            "key_facts": [
                f"Written {'right to left' if lang.rtl else 'left to right'}",
                f"Approximately {lang.speakers_m} million speakers",
                f"Difficulty for English speakers: {lang.difficulty}/5"
            ],
            "echo_tip": (
                "Start with greetings and common phrases. "
                "Consistency beats intensity — 20 minutes daily is better than 3 hours weekly."
            )
        }

    def _lesson_greetings(self, lang: Language) -> Dict:
        greeting = self.GREETINGS.get(lang.code, "Hello")
        return {
            "title"  : f"{lang.name} Greetings",
            "phrases": [
                {"situation": "General greeting", "translation": greeting},
                {"situation": "Good morning",     "translation": f"[Good morning in {lang.name}]"},
                {"situation": "Good evening",     "translation": f"[Good evening in {lang.name}]"},
                {"situation": "Goodbye",          "translation": f"[Goodbye in {lang.name}]"},
                {"situation": "How are you?",     "translation": f"[How are you in {lang.name}]"},
                {"situation": "Nice to meet you", "translation": f"[Nice to meet you in {lang.name}]"},
            ],
            "cultural_note": f"Greeting customs vary in {lang.name}-speaking cultures. Context and relationship matter.",
            "echo_tip"     : "Nail greetings first — they create immediate connection with native speakers."
        }

    def _lesson_numbers(self, lang: Language) -> Dict:
        return {
            "title"  : f"Numbers in {lang.name}",
            "content": f"Learning numbers in {lang.name} ({lang.native_name})",
            "numbers": [{"numeral": str(i), "word": f"[{i} in {lang.name}]"} for i in range(11)],
            "echo_tip": "Numbers unlock dates, prices, phone numbers — high practical value early on."
        }

    def _lesson_grammar(self, lang: Language) -> Dict:
        grammar_notes = {
            "Romance": "Gendered nouns (masculine/feminine), verb conjugation by person/tense.",
            "Germanic": "Cases may apply, compound words are common, verb placement varies.",
            "Slavic" : "Cases (nominative, accusative, dative etc.), complex verb aspects.",
            "Semitic": "Root-pattern morphology — 3-letter roots modified by patterns.",
            "Sino-Tibetan": "Tonal language — pitch changes meaning. No conjugation.",
            "Japonic": "SOV word order, particles mark grammar roles, politeness levels.",
        }
        note = grammar_notes.get(lang.family, "Unique grammatical structure.")

        return {
            "title"  : f"{lang.name} Grammar Overview",
            "family" : lang.family,
            "grammar_note": note,
            "word_order"  : "Varies by language family",
            "echo_tip"    : "Don't memorize rules — absorb patterns through examples."
        }

    def _lesson_culture(self, lang: Language) -> Dict:
        return {
            "title"        : f"Cultural Context — {lang.name}",
            "content"      : f"Language and culture are inseparable. {lang.name} reflects unique worldviews.",
            "speakers"     : f"{lang.speakers_m} million people speak {lang.name} worldwide.",
            "script"       : f"Writing system: {lang.script}",
            "regions"      : f"Widely spoken across multiple regions",
            "echo_tip"     : "Cultural understanding makes you not just fluent but truly communicative."
        }

    def _lesson_pronunciation(self, lang: Language) -> Dict:
        return {
            "title"    : f"{lang.name} Pronunciation Guide",
            "script"   : lang.script,
            "rtl"      : lang.rtl,
            "content"  : f"{lang.name} uses the {lang.script} writing system.",
            "tips"     : [
                f"{'Read right to left' if lang.rtl else 'Read left to right'}",
                f"Difficulty rating: {lang.difficulty}/5 for English speakers",
                "Listen to native speakers as much as possible",
                "Record yourself and compare to native audio"
            ],
            "echo_tip" : "Pronunciation comes with ear training. Listen 10x more than you speak initially."
        }

    def get_all_languages(self) -> List[Dict]:
        """Get info on all supported languages."""
        return [
            {
                "code"       : lang.code,
                "name"       : lang.name,
                "native"     : lang.native_name,
                "family"     : lang.family,
                "speakers_m" : lang.speakers_m,
                "difficulty" : lang.difficulty,
                "offline"    : lang.offline
            }
            for lang in sorted(self.LANGUAGES.values(),
                               key=lambda l: l.speakers_m, reverse=True)
        ]

    def get_learning_progress(self) -> Dict:
        return dict(self._learning_progress)


# ══════════════════════════════════════════════
#  PILLAR 3 — MASTER TEACHER
# ══════════════════════════════════════════════

class TeachingEngine:
    """
    Echo's master teaching system.

    Adapts explanation depth, style, and pacing
    to whoever is learning. Detects comprehension.
    Uses Socratic method to build real understanding
    rather than surface memorization.

    JARVIS explained complex engineering concepts
    to Tony's guests in simple terms when needed,
    and gave Tony full technical depth when required.
    Echo does the same for any topic.
    """

    LEVEL_DESCRIPTORS = {
        KnowledgeLevel.CHILD       : "5-year-old friendly, pure analogies, zero jargon",
        KnowledgeLevel.BEGINNER    : "Clear fundamentals, everyday analogies, gentle pacing",
        KnowledgeLevel.INTERMEDIATE: "Assumes basics, introduces technical terms with explanation",
        KnowledgeLevel.ADVANCED    : "Full technical depth, assumes strong background",
        KnowledgeLevel.EXPERT      : "Peer-to-peer, nuance, edge cases, research implications",
        KnowledgeLevel.RESEARCH    : "Cutting edge, open questions, citations, novel synthesis"
    }

    SOCRATIC_QUESTIONS = {
        "physics" : [
            "What do you think would happen if you doubled the mass?",
            "Can you explain why that makes intuitive sense?",
            "How does this connect to what we discussed about energy?",
            "What would this look like at the quantum scale?"
        ],
        "mathematics": [
            "Can you walk me through your reasoning step by step?",
            "What happens if we change this variable?",
            "Is there another way to approach this problem?",
            "Can you prove this holds for all cases?"
        ],
        "history": [
            "What factors do you think led to this outcome?",
            "How might things have been different if X hadn't happened?",
            "What parallels do you see with events today?",
            "Whose perspective haven't we considered yet?"
        ],
        "general": [
            "What's your intuition telling you?",
            "How would you explain this to someone else?",
            "What question does this raise for you?",
            "Where does this idea break down or have limits?"
        ]
    }

    def teach(self, topic: str, entries: List[KnowledgeEntry],
              level: KnowledgeLevel = KnowledgeLevel.INTERMEDIATE,
              style: LearningStyle = LearningStyle.READING) -> Dict:
        """
        Generate a full teaching response for a topic.
        Adapts to level and learning style.
        """
        if not entries:
            return {
                "topic"  : topic,
                "message": f"I don't have specific entries on '{topic}' yet, but I can reason through it with you.",
                "level"  : level.name
            }

        primary = entries[0]

        # Adapt content to level
        content = self._adapt_to_level(primary.content, level, primary.domain)

        # Add learning style elements
        style_elements = self._add_style_elements(primary, style, level)

        # Socratic questions
        domain_questions = self.SOCRATIC_QUESTIONS.get(
            primary.domain,
            self.SOCRATIC_QUESTIONS["general"]
        )
        questions = random.sample(domain_questions, min(2, len(domain_questions)))

        # Key takeaways
        takeaways = self._extract_takeaways(primary, level)

        return {
            "topic"         : topic,
            "domain"        : primary.domain,
            "level"         : level.name,
            "level_note"    : self.LEVEL_DESCRIPTORS[level],
            "title"         : primary.title,
            "explanation"   : content,
            "style_elements": style_elements,
            "key_takeaways" : takeaways,
            "socratic_questions": questions,
            "related_topics": [e.title for e in entries[1:3]],
            "next_step"     : f"Ready to go deeper? Ask me about {primary.subtopic} advanced concepts.",
            "echo_note"     : "Teaching adapts to you — tell me if you want simpler or more depth."
        }

    def _adapt_to_level(self, content: str, level: KnowledgeLevel,
                         domain: str) -> str:
        """Adapt content complexity to the learner's level."""
        if level == KnowledgeLevel.CHILD:
            # Simplify — use first sentence + analogy
            first_sentence = content.split(".")[0] + "."
            return (
                f"{first_sentence} "
                f"Think of it like this: imagine you're trying to explain "
                f"this to your little brother or sister using only toys and games. "
                f"The big idea is: {content.split('.')[0].lower()}."
            )

        elif level == KnowledgeLevel.BEGINNER:
            # First 2-3 sentences, no jargon
            sentences = content.split(".")[:3]
            return ". ".join(sentences) + ". Let's build from these basics."

        elif level in [KnowledgeLevel.INTERMEDIATE, KnowledgeLevel.ADVANCED]:
            return content

        elif level in [KnowledgeLevel.EXPERT, KnowledgeLevel.RESEARCH]:
            return (
                content + "\n\n"
                "[Expert context: Consider the edge cases, current research frontiers, "
                "and open questions in this domain. I can elaborate on any specific aspect.]"
            )

        return content

    def _add_style_elements(self, entry: KnowledgeEntry,
                             style: LearningStyle,
                             level: KnowledgeLevel) -> Dict:
        """Add learning style specific elements."""
        elements = {}

        if style == LearningStyle.VISUAL:
            elements["visual_prompt"] = (
                f"Picture this: {entry.summary}. "
                f"Imagine drawing a diagram with '{entry.topic}' at the center, "
                f"and connecting these concepts: {', '.join(entry.keywords[:4])}."
            )

        elif style == LearningStyle.KINESTHETIC:
            elements["practice"] = (
                f"Try this: apply what you just learned to a real example. "
                f"Take one concept from {entry.title} and find it in the world around you."
            )

        elif style == LearningStyle.AUDITORY:
            elements["verbal_summary"] = (
                f"Say this out loud: '{entry.summary}' "
                f"Now explain it in your own words as if teaching a friend."
            )

        elif style == LearningStyle.SOCRATIC:
            elements["discovery_prompt"] = (
                f"Before I explain — what do you already know about {entry.topic}? "
                f"What would you expect based on what you know?"
            )

        return elements

    def _extract_takeaways(self, entry: KnowledgeEntry,
                            level: KnowledgeLevel) -> List[str]:
        """Extract key takeaways appropriate for level."""
        sentences = [s.strip() for s in entry.content.split(".") if len(s.strip()) > 20]
        n = min(3 if level.value <= 2 else 5, len(sentences))
        return sentences[:n]


# ══════════════════════════════════════════════
#  PILLAR 4 — STUDY SYSTEM
# ══════════════════════════════════════════════

@dataclass
class Flashcard:
    card_id:    str   = field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic:      str   = ""
    front:      str   = ""        # Question/prompt
    back:       str   = ""        # Answer
    domain:     str   = ""
    difficulty: int   = 3         # 1-5
    # Spaced repetition fields
    interval:   int   = 1         # Days until next review
    ease:       float = 2.5       # Ease factor
    next_review: str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    times_seen: int   = 0
    times_correct: int = 0

    @property
    def accuracy(self) -> float:
        return (self.times_correct / self.times_seen) if self.times_seen > 0 else 0

    def to_dict(self) -> Dict:
        return {**asdict(self), "accuracy": round(self.accuracy, 2)}


class StudySystem:
    """
    Echo's intelligent study system.

    Spaced repetition: shows cards at optimal intervals.
    Gap detection: identifies what you don't know.
    Adaptive scheduling: harder cards appear more often.

    JARVIS would have briefed Tony on key information
    before important meetings — optimally timed.
    Echo does the same for learning.
    """

    def __init__(self, library: UniversalLibrary):
        self.library         = library
        self._flashcards: Dict[str, Flashcard] = {}
        self._sessions: List[Dict]             = []
        self._expertise: Dict[str, float]      = defaultdict(float)  # domain -> mastery 0-1
        self._study_streaks: Dict[str, int]    = defaultdict(int)
        self._lock                             = threading.Lock()

        # Generate initial flashcards from library
        self._generate_flashcards_from_library()

    def _generate_flashcards_from_library(self):
        """Auto-generate flashcards from the knowledge library."""
        for entry in self.library._entries.values():
            # Create Q&A from entry
            card = Flashcard(
                topic      = entry.topic,
                front      = f"What is {entry.title}?",
                back       = entry.summary,
                domain     = entry.domain,
                difficulty = entry.level
            )
            self._flashcards[card.card_id] = card

            # Create keyword card
            if entry.keywords:
                kw_card = Flashcard(
                    topic      = entry.topic,
                    front      = f"Name 3 key concepts related to {entry.topic}",
                    back       = ", ".join(entry.keywords[:5]),
                    domain     = entry.domain,
                    difficulty = entry.level - 1
                )
                self._flashcards[kw_card.card_id] = kw_card

    def create_flashcard(self, front: str, back: str,
                          topic: str, domain: str = "general",
                          difficulty: int = 3) -> Flashcard:
        """Create a custom flashcard."""
        card = Flashcard(
            topic=topic, front=front, back=back,
            domain=domain, difficulty=difficulty
        )
        with self._lock:
            self._flashcards[card.card_id] = card
        return card

    def get_due_cards(self, domain: Optional[str] = None,
                      limit: int = 10) -> List[Flashcard]:
        """Get cards due for review — spaced repetition."""
        now = datetime.now(timezone.utc).isoformat()
        due = [
            card for card in self._flashcards.values()
            if card.next_review <= now
            and (not domain or card.domain == domain)
        ]
        # Sort: hardest first, then by due date
        due.sort(key=lambda c: (c.ease, c.next_review))
        return due[:limit]

    def record_answer(self, card_id: str, quality: int) -> Dict:
        """
        Record answer quality and update spaced repetition schedule.
        quality: 0=blackout, 1=wrong, 2=hard, 3=ok, 4=good, 5=easy
        SM-2 algorithm for optimal spacing.
        """
        card = self._flashcards.get(card_id)
        if not card:
            return {"error": "Card not found"}

        card.times_seen += 1
        if quality >= 3:
            card.times_correct += 1

        # SM-2 spacing algorithm
        if quality >= 3:
            if card.times_seen == 1:
                card.interval = 1
            elif card.times_seen == 2:
                card.interval = 6
            else:
                card.interval = round(card.interval * card.ease)
        else:
            card.interval = 1  # Reset on failure

        # Update ease factor
        card.ease = max(1.3, card.ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

        # Set next review date
        next_dt = datetime.now(timezone.utc) + timedelta(days=card.interval)
        card.next_review = next_dt.isoformat()

        # Update domain expertise
        if quality >= 3:
            self._expertise[card.domain] = min(
                1.0, self._expertise[card.domain] + 0.02
            )

        log.debug(
            f"[SCHOLAR/STUDY] Card {card_id} | Quality: {quality} | "
            f"Next review in {card.interval} days"
        )

        return {
            "card_id"     : card_id,
            "quality"     : quality,
            "next_review" : card.next_review,
            "interval_days": card.interval,
            "accuracy"    : round(card.accuracy, 2)
        }

    def generate_quiz(self, domain: Optional[str] = None,
                      n_questions: int = 5,
                      level: KnowledgeLevel = KnowledgeLevel.INTERMEDIATE) -> Dict:
        """Generate a quiz on a topic."""
        pool = [
            c for c in self._flashcards.values()
            if (not domain or c.domain == domain)
            and c.difficulty <= level.value
        ]

        if not pool:
            return {"error": "No cards available for quiz"}

        questions = random.sample(pool, min(n_questions, len(pool)))
        quiz_questions = []

        for card in questions:
            # Generate wrong answers from other cards
            wrong_pool = [c.back for c in pool if c.card_id != card.card_id]
            wrong_options = random.sample(wrong_pool, min(3, len(wrong_pool)))
            options = wrong_options + [card.back]
            random.shuffle(options)

            quiz_questions.append({
                "question"    : card.front,
                "correct"     : card.back,
                "options"     : options,
                "difficulty"  : card.difficulty,
                "domain"      : card.domain
            })

        return {
            "quiz_id"    : str(uuid.uuid4())[:8],
            "domain"     : domain or "mixed",
            "questions"  : quiz_questions,
            "total"      : len(quiz_questions),
            "level"      : level.name,
            "echo_tip"   : "Take your time — understanding beats speed in learning."
        }

    def get_knowledge_gaps(self) -> List[Dict]:
        """
        JARVIS addition: Detect what you don't know well.
        Echo proactively identifies weak areas.
        """
        gaps = []
        domain_performance: Dict[str, List[float]] = defaultdict(list)

        for card in self._flashcards.values():
            if card.times_seen > 0:
                domain_performance[card.domain].append(card.accuracy)

        for domain, accuracies in domain_performance.items():
            avg = sum(accuracies) / len(accuracies)
            if avg < 0.7:  # Below 70% — it's a gap
                gaps.append({
                    "domain"      : domain,
                    "avg_accuracy": round(avg, 2),
                    "cards_seen"  : len(accuracies),
                    "severity"    : "critical" if avg < 0.4 else "moderate",
                    "recommendation": f"Focus study sessions on {domain}. "
                                      f"Current accuracy: {avg:.0%}."
                })

        return sorted(gaps, key=lambda g: g["avg_accuracy"])

    def get_expertise_profile(self) -> Dict:
        """
        JARVIS addition: Your knowledge fingerprint.
        A map of how well Echo knows you know each domain.
        """
        profile = {}
        for domain in Domain:
            domain_cards = [
                c for c in self._flashcards.values()
                if c.domain == domain.value and c.times_seen > 0
            ]
            if domain_cards:
                avg_accuracy = sum(c.accuracy for c in domain_cards) / len(domain_cards)
                profile[domain.value] = {
                    "mastery"      : round(avg_accuracy, 2),
                    "cards_studied": len(domain_cards),
                    "level"        : (
                        "Expert"       if avg_accuracy >= 0.9 else
                        "Advanced"     if avg_accuracy >= 0.75 else
                        "Intermediate" if avg_accuracy >= 0.55 else
                        "Beginner"     if avg_accuracy >= 0.3  else
                        "Novice"
                    )
                }
            else:
                profile[domain.value] = {
                    "mastery": self._expertise.get(domain.value, 0.0),
                    "cards_studied": 0,
                    "level": "Not yet studied"
                }

        return profile

    def get_study_schedule(self, daily_minutes: int = 30) -> Dict:
        """
        Generate an optimized study schedule.
        JARVIS would have scheduled Tony's time efficiently.
        """
        due_cards   = self.get_due_cards(limit=50)
        gaps        = self.get_knowledge_gaps()

        schedule = {
            "daily_minutes"    : daily_minutes,
            "due_reviews"      : len(due_cards),
            "recommended_order": [],
            "echo_insight"     : ""
        }

        # Prioritize gaps
        if gaps:
            schedule["recommended_order"].append({
                "activity"   : f"Review weak areas: {gaps[0]['domain']}",
                "minutes"    : daily_minutes // 3,
                "priority"   : "high"
            })

        # Due reviews
        if due_cards:
            schedule["recommended_order"].append({
                "activity"   : f"Spaced repetition: {len(due_cards)} cards due",
                "minutes"    : daily_minutes // 2,
                "priority"   : "medium"
            })

        # New material
        schedule["recommended_order"].append({
            "activity"   : "New material — explore a topic you're curious about",
            "minutes"    : daily_minutes // 4,
            "priority"   : "low"
        })

        schedule["echo_insight"] = (
            f"Consistency compounds. {daily_minutes} minutes daily for a year = "
            f"{daily_minutes * 365 // 60} hours of deep learning."
        )

        return schedule

    def get_stats(self) -> Dict:
        total    = len(self._flashcards)
        seen     = sum(1 for c in self._flashcards.values() if c.times_seen > 0)
        mastered = sum(1 for c in self._flashcards.values() if c.accuracy >= 0.85)

        return {
            "total_cards" : total,
            "seen"        : seen,
            "mastered"    : mastered,
            "mastery_pct" : round(mastered / total * 100, 1) if total > 0 else 0,
            "domains_studied": len([d for d, v in self._expertise.items() if v > 0])
        }


# ══════════════════════════════════════════════
#  SCHOLAR LAYER — MASTER CLASS
# ══════════════════════════════════════════════

class ScholarLayer:
    """
    Scholar Layer — Echo's Universal Knowledge & Teaching System.

    Knows everything. Teaches anything. Speaks every language.
    Works online and offline. Gets smarter with every interaction.
    """

    def __init__(self):
        self.library  = UniversalLibrary()
        self.language = LanguageEngine()
        self.teacher  = TeachingEngine()
        self.study    = StudySystem(self.library)

        # Default teaching settings
        self._level   = KnowledgeLevel.INTERMEDIATE
        self._style   = LearningStyle.READING
        self._lock    = threading.Lock()

        log.info(
            f"[SCHOLAR] Layer online | "
            f"Library: {self.library.get_stats()['total_entries']} entries | "
            f"Languages: {len(self.language.LANGUAGES)} | "
            f"Flashcards: {self.study.get_stats()['total_cards']}"
        )

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """Main entry point from EchoCore LayerRouter."""
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[SCHOLAR] Processing: '{intent_text[:60]}'")

        # ── Auto-detect knowledge level from context ───
        if any(kw in intent_low for kw in ["phd", "expert", "research", "advanced"]):
            self._level = KnowledgeLevel.EXPERT
        elif any(kw in intent_low for kw in ["simple", "easy", "basic", "beginner"]):
            self._level = KnowledgeLevel.BEGINNER
        elif any(kw in intent_low for kw in ["kid", "child", "simple please"]):
            self._level = KnowledgeLevel.CHILD

        # ── Route to sub-system ────────────────────────

        # Language learning/translation
        if any(kw in intent_low for kw in ["translate", "translation", "how do you say",
                                            "speak", "learn language", "teach me spanish", "teach me french", "teach me german", "teach me chinese", "teach me arabic", "teach me swahili", "teach me yoruba", "teach me hausa", "teach me igbo",
                                            "what language", "languages"]):
            return self._handle_language(intent_text, context)

        # Quiz / flashcards
        elif any(kw in intent_low for kw in ["quiz", "flashcard", "test me",
                                              "flash card", "practice"]):
            return self._handle_quiz(intent_text, context)

        # Study schedule / gaps
        elif any(kw in intent_low for kw in ["study schedule", "knowledge gap",
                                              "what should i study", "study plan",
                                              "expertise"]):
            return self._handle_study_planning(intent_text, context)

        # Library / knowledge search
        elif any(kw in intent_low for kw in ["library", "all topics", "what do you know",
                                              "search", "find information"]):
            return self._handle_library_search(intent_text, context)

        # Teaching — explain/learn a topic
        else:
            return self._handle_teaching(intent_text, context)

    # ── Sub-handlers ────────────────────────────

    def _handle_teaching(self, intent: str, context: Dict) -> Dict:
        """Core teaching — explain any topic."""
        # Search library for relevant entries
        entries = self.library.search(intent, limit=5)

        lesson = self.teacher.teach(
            topic   = intent,
            entries = entries,
            level   = self._level,
            style   = self._style
        )

        # JARVIS addition: cross-domain connections
        cross_domain = self._find_cross_domain_connections(intent, entries)

        return {
            "layer"        : "scholar",
            "status"       : "OK",
            "sub_system"   : "teaching",
            "level"        : self._level.name,
            "lesson"       : lesson,
            "cross_domain" : cross_domain,
            "message"      : lesson.get("explanation", lesson.get("message", "")),
            "timestamp"    : datetime.now(timezone.utc).isoformat()
        }

    def _handle_language(self, intent: str, context: Dict) -> Dict:
        """Handle language learning and translation."""
        intent_low = intent.lower()

        # Translation request
        if "translate" in intent_low or "how do you say" in intent_low:
            target_lang = context.get("target_language", "es")
            # Try to detect source text
            text = context.get("text", intent)

            result = self.language.translate(text, target_lang)

            return {
                "layer"      : "scholar",
                "status"     : "OK",
                "sub_system" : "translation",
                "translation": result,
                "message"    : (
                    f"'{result['original']}' in {result['target_name']}: "
                    f"'{result['translated']}'"
                ),
                "timestamp"  : datetime.now(timezone.utc).isoformat()
            }

        # Language list
        elif "languages" in intent_low or "what languages" in intent_low:
            languages = self.language.get_all_languages()
            return {
                "layer"     : "scholar",
                "status"    : "OK",
                "sub_system": "language_list",
                "languages" : languages,
                "total"     : len(languages),
                "message"   : (
                    f"I support {len(languages)} languages covering "
                    f"{sum(l['speakers_m'] for l in languages):,}M+ speakers worldwide. "
                    f"All available offline."
                ),
                "timestamp" : datetime.now(timezone.utc).isoformat()
            }

        # Language lesson
        else:
            # Detect which language
            lang_code = context.get("language_code", "es")
            words = intent_low.split()
            for code, lang in self.language.LANGUAGES.items():
                if lang.name.lower() in intent_low or code in words:
                    lang_code = code
                    break

            lesson = self.language.get_language_lesson(
                lang_code,
                lesson_type = context.get("lesson_type", "basics"),
                level       = self._level.value
            )

            return {
                "layer"      : "scholar",
                "status"     : "OK",
                "sub_system" : "language_lesson",
                "lesson"     : lesson,
                "message"    : (
                    f"Starting {lesson.get('language', 'language')} lesson: "
                    f"{lesson.get('lesson_type', 'basics')}. "
                    f"{lesson.get('speakers', '')}."
                ),
                "timestamp"  : datetime.now(timezone.utc).isoformat()
            }

    def _handle_quiz(self, intent: str, context: Dict) -> Dict:
        """Generate and manage quizzes."""
        domain = context.get("domain")
        quiz   = self.study.generate_quiz(
            domain      = domain,
            n_questions = context.get("n_questions", 5),
            level       = self._level
        )

        return {
            "layer"    : "scholar",
            "status"   : "OK",
            "sub_system": "quiz",
            "quiz"     : quiz,
            "message"  : (
                f"Quiz ready: {quiz.get('total', 0)} questions on "
                f"{quiz.get('domain', 'mixed topics')} at {self._level.name} level."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _handle_study_planning(self, intent: str, context: Dict) -> Dict:
        """Study schedule and knowledge gap analysis."""
        schedule = self.study.get_study_schedule(
            daily_minutes=context.get("daily_minutes", 30)
        )
        gaps     = self.study.get_knowledge_gaps()
        expertise = self.study.get_expertise_profile()
        stats    = self.study.get_stats()

        return {
            "layer"      : "scholar",
            "status"     : "OK",
            "sub_system" : "study_planning",
            "schedule"   : schedule,
            "gaps"       : gaps,
            "expertise"  : expertise,
            "stats"      : stats,
            "message"    : (
                f"Study stats: {stats['mastered']} cards mastered "
                f"({stats['mastery_pct']}%). "
                f"Knowledge gaps: {len(gaps)}. "
                f"{schedule.get('echo_insight', '')}"
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _handle_library_search(self, intent: str, context: Dict) -> Dict:
        """Search and browse the knowledge library."""
        query   = context.get("query", intent)
        entries = self.library.search(query, limit=8)
        stats   = self.library.get_stats()

        return {
            "layer"      : "scholar",
            "status"     : "OK",
            "sub_system" : "library",
            "results"    : [e.to_dict() for e in entries],
            "total_found": len(entries),
            "library_stats": stats,
            "message"    : (
                f"Found {len(entries)} relevant entries. "
                f"Library covers {stats['total_entries']} topics "
                f"across {stats['domains_covered']} domains. "
                f"All {stats['offline_entries']} entries available offline."
            ),
            "timestamp"  : datetime.now(timezone.utc).isoformat()
        }

    def _find_cross_domain_connections(self, topic: str,
                                        entries: List[KnowledgeEntry]) -> List[Dict]:
        """
        JARVIS addition: Find surprising connections across domains.
        Echo synthesizes knowledge across fields —
        connects physics to music, math to economics,
        history to psychology — the way a brilliant mind does.
        """
        if not entries:
            return []

        primary_domain = entries[0].domain
        connections    = []

        # Search other domains for the same keywords
        for entry in entries:
            for keyword in entry.keywords[:3]:
                related = self.library.search(keyword, limit=3)
                for r in related:
                    if r.domain != primary_domain and r.entry_id != entry.entry_id:
                        connections.append({
                            "from_domain"  : primary_domain,
                            "to_domain"    : r.domain,
                            "connection"   : keyword,
                            "related_title": r.title,
                            "insight"      : (
                                f"'{keyword}' appears in both {primary_domain} "
                                f"and {r.domain} — these fields share deeper structure."
                            )
                        })

        # Deduplicate
        seen = set()
        unique = []
        for c in connections:
            key = f"{c['to_domain']}_{c['connection']}"
            if key not in seen:
                seen.add(key)
                unique.append(c)

        return unique[:3]

    def set_level(self, level: KnowledgeLevel):
        with self._lock:
            self._level = level

    def set_style(self, style: LearningStyle):
        with self._lock:
            self._style = style

    def get_status(self) -> Dict:
        return {
            "layer"          : "scholar",
            "status"         : "ONLINE",
            "library"        : self.library.get_stats(),
            "languages"      : len(self.language.LANGUAGES),
            "flashcards"     : self.study.get_stats(),
            "current_level"  : self._level.name,
            "offline_ready"  : True
        }


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║        ECHO SCHOLAR LAYER — TEST            ║
╚══════════════════════════════════════════════╝
    """)

    scholar = ScholarLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        ("Explain quantum mechanics to me",                              {}),
        ("Teach me calculus derivatives like I'm a beginner",           {}),
        ("What languages do you support?",                               {}),
        ("Teach me Spanish basics",                                      {"language_code": "es"}),
        ("Translate hello to French",                                    {"target_language": "fr", "text": "hello"}),
        ("Quiz me on physics",                                           {"domain": "physics"}),
        ("What is my study plan for 20 minutes a day?",                  {"daily_minutes": 20}),
        ("Search the library for neural networks",                       {"query": "neural networks"}),
        ("Explain the laws of thermodynamics as an expert",              {}),
        ("Teach me Swahili",                                             {"language_code": "sw"}),
    ]

    for i, (query, ctx) in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query[:60]}'")
        print("─" * 55)
        result = scholar.process(query, session, ctx)
        print(f"  SUB-SYSTEM : {result.get('sub_system', 'N/A')}")
        msg = str(result.get('message', ''))[:130]
        print(f"  MESSAGE    : {msg}")

    print("\n" + "═" * 55)
    print("  SCHOLAR STATUS")
    print("═" * 55)
    status = scholar.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<25}: {v}")
