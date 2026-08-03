"""
╔══════════════════════════════════════════════════════════════════════╗
║                   ECHO AI — CREATOR LAYER                           ║
║         The Full Creative Universe — Build Anything Imaginable       ║
║                                                                      ║
║  STUDIO 1 — CODE & SOFTWARE                                         ║
║    - Writes any language, any complexity                             ║
║    - Architecture design, debugging, optimization                    ║
║    - Documentation, code review                                      ║
║                                                                      ║
║  STUDIO 2 — WRITING & NARRATIVE                                     ║
║    - Stories, novels, scripts, screenplays                          ║
║    - Poetry, lyrics, speeches, essays                               ║
║    - Business documents, proposals, emails                          ║
║                                                                      ║
║  STUDIO 3 — MANGA & COMICS                                          ║
║    - Professional manga creation — panel layout, storyboards        ║
║    - Character design, world building                                ║
║    - Manga script format (dialogue, action, SFX)                    ║
║    - Multiple manga styles (shonen, shojo, seinen, josei)           ║
║                                                                      ║
║  STUDIO 4 — VISUAL & DESIGN                                         ║
║    - Image generation prompts (Stable Diffusion, DALL-E, Midjourney)║
║    - UI/UX design, brand identity, logos                            ║
║    - Infographics, diagrams, 3D concepts                            ║
║                                                                      ║
║  STUDIO 5 — MUSIC & AUDIO                                           ║
║    - Song composition — full structure + lyrics                     ║
║    - DJ mode — setlists, mixes, BPM management                      ║
║    - Podcast scripts, voice scripts                                  ║
║    - Music theory application                                        ║
║                                                                      ║
║  STUDIO 6 — VIDEO & ANIMATION                                       ║
║    - Video scripts and full storyboards                             ║
║    - Animation concepts (Seedance-style short videos)               ║
║    - Film/documentary structure                                      ║
║    - Scene direction and cinematography notes                       ║
║                                                                      ║
║  STUDIO 7 — FUN & IMAGINATION                                       ║
║    - Anything the user imagines — no creative limit                 ║
║    - Games, interactive fiction, world building                     ║
║    - Jokes, memes, comedy writing                                   ║
║    - Dream/concept exploration                                       ║
║                                                                      ║
║  JARVIS additions:                                                   ║
║    - Creative brief engine — understands what you want              ║
║      before you fully know yourself                                 ║
║    - Style learning — Echo learns your creative DNA over time       ║
║    - Collaboration mode — builds ON your ideas not over them        ║
║    - Cross-medium translation (poem → visual → song → animation)   ║
║    - Creative version history — every iteration saved               ║
║    - Mood-to-creation mapping — reads your vibe, matches it        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import uuid
import time
import json
import random
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from enum import Enum


log = logging.getLogger("EchoCore.Creator")


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class CreativeStudio(Enum):
    CODE        = "code"
    WRITING     = "writing"
    MANGA       = "manga"
    VISUAL      = "visual"
    MUSIC       = "music"
    VIDEO       = "video"
    FUN         = "fun"


class MangaStyle(Enum):
    SHONEN      = "shonen"      # Young male — action, friendship, growth
    SHOJO       = "shojo"       # Young female — romance, emotion, relationships
    SEINEN      = "seinen"      # Adult male — complex themes, realism
    JOSEI       = "josei"       # Adult female — mature romance, slice of life
    KODOMOMUKE  = "kodomomuke"  # Children — simple, bright, fun
    ISEKAI      = "isekai"      # Fantasy world — transported protagonist
    MECHA       = "mecha"       # Giant robots, sci-fi
    CYBERPUNK   = "cyberpunk"   # Dark tech dystopia
    SLICE_OF_LIFE = "slice_of_life"  # Everyday life, relatable


class MusicGenre(Enum):
    AFROBEATS   = "afrobeats"
    HIP_HOP     = "hip_hop"
    RNB         = "rnb"
    POP         = "pop"
    ELECTRONIC  = "electronic"
    JAZZ        = "jazz"
    CLASSICAL   = "classical"
    ROCK        = "rock"
    REGGAE      = "reggae"
    GOSPEL      = "gospel"
    AMAPIANO    = "amapiano"
    HIGHLIFE    = "highlife"
    DANCEHALL   = "dancehall"
    TRAP        = "trap"
    DRILL       = "drill"
    LOFI        = "lofi"
    HOUSE       = "house"
    TECHNO      = "techno"
    SYNTHWAVE   = "synthwave"
    FOLK        = "folk"


class AnimationStyle(Enum):
    ANIME           = "anime"
    PIXAR_3D        = "pixar_3d"
    CARTOON_2D      = "cartoon_2d"
    MOTION_GRAPHICS = "motion_graphics"
    STOP_MOTION     = "stop_motion"
    WHITEBOARD      = "whiteboard"
    CINEMATIC       = "cinematic"
    SEEDANCE        = "seedance"        # Short loop animation


class CodeLanguage(Enum):
    PYTHON      = "python"
    JAVASCRIPT  = "javascript"
    TYPESCRIPT  = "typescript"
    RUST        = "rust"
    GO          = "go"
    JAVA        = "java"
    CPP         = "cpp"
    C           = "c"
    SWIFT       = "swift"
    KOTLIN      = "kotlin"
    SOLIDITY    = "solidity"
    HTML_CSS    = "html_css"
    SQL         = "sql"
    BASH        = "bash"
    R           = "r"
    MATLAB      = "matlab"


class WritingTone(Enum):
    EPIC        = "epic"
    HUMOROUS    = "humorous"
    ROMANTIC    = "romantic"
    DARK        = "dark"
    INSPIRATIONAL = "inspirational"
    TECHNICAL   = "technical"
    CASUAL      = "casual"
    FORMAL      = "formal"
    POETIC      = "poetic"
    SATIRICAL   = "satirical"


# ─────────────────────────────────────────────
#  CREATIVE WORK — Base data model
# ─────────────────────────────────────────────

@dataclass
class CreativeWork:
    """Every piece of creative output Echo produces."""
    work_id:     str  = field(default_factory=lambda: str(uuid.uuid4())[:10])
    studio:      str  = ""
    title:       str  = ""
    content:     Any  = None
    metadata:    Dict = field(default_factory=dict)
    version:     int  = 1
    created_at:  str  = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    iterations:  List = field(default_factory=list)  # Version history
    tags:        List = field(default_factory=list)

    def add_iteration(self, content: Any, note: str = ""):
        """Save a new version — every iteration preserved."""
        self.iterations.append({
            "version"   : self.version,
            "content"   : self.content,
            "note"      : note,
            "saved_at"  : datetime.now(timezone.utc).isoformat()
        })
        self.content = content
        self.version += 1

    def to_dict(self) -> Dict:
        return asdict(self)


# ─────────────────────────────────────────────
#  CREATIVE BRIEF ENGINE
#  JARVIS addition — understands what you want
#  before you fully know yourself
# ─────────────────────────────────────────────

class CreativeBriefEngine:
    """
    Interprets vague creative requests into
    structured, actionable briefs.

    JARVIS would take Tony's half-formed idea
    and immediately structure it into something
    buildable. Echo does the same creatively.

    "I want something cool with robots and music"
    becomes a structured brief with style, tone,
    structure, target audience and specific direction.
    """

    MOOD_MAPPINGS = {
        "happy"       : {"tone": WritingTone.HUMOROUS,     "genre": MusicGenre.AFROBEATS,  "manga_style": MangaStyle.SHONEN},
        "sad"         : {"tone": WritingTone.POETIC,       "genre": MusicGenre.RNB,        "manga_style": MangaStyle.JOSEI},
        "excited"     : {"tone": WritingTone.EPIC,         "genre": MusicGenre.ELECTRONIC, "manga_style": MangaStyle.SHONEN},
        "romantic"    : {"tone": WritingTone.ROMANTIC,     "genre": MusicGenre.RNB,        "manga_style": MangaStyle.SHOJO},
        "angry"       : {"tone": WritingTone.DARK,         "genre": MusicGenre.DRILL,      "manga_style": MangaStyle.SEINEN},
        "mysterious"  : {"tone": WritingTone.DARK,         "genre": MusicGenre.SYNTHWAVE,  "manga_style": MangaStyle.SEINEN},
        "chill"       : {"tone": WritingTone.CASUAL,       "genre": MusicGenre.LOFI,       "manga_style": MangaStyle.SLICE_OF_LIFE},
        "inspired"    : {"tone": WritingTone.INSPIRATIONAL,"genre": MusicGenre.GOSPEL,     "manga_style": MangaStyle.ISEKAI},
        "fun"         : {"tone": WritingTone.HUMOROUS,     "genre": MusicGenre.POP,        "manga_style": MangaStyle.KODOMOMUKE},
        "dark"        : {"tone": WritingTone.DARK,         "genre": MusicGenre.TRAP,       "manga_style": MangaStyle.CYBERPUNK},
    }

    def interpret(self, request: str, context: Dict) -> Dict:
        """
        Take any creative request — even vague — and
        build a structured creative brief from it.
        """
        request_lower = request.lower()

        # Detect mood
        detected_mood = "neutral"
        for mood in self.MOOD_MAPPINGS:
            if mood in request_lower:
                detected_mood = mood
                break

        mood_prefs = self.MOOD_MAPPINGS.get(
            detected_mood,
            {"tone": WritingTone.CASUAL,
             "genre": MusicGenre.POP,
             "manga_style": MangaStyle.SHONEN}
        )

        # Detect studio
        studio = self._detect_studio(request_lower)

        # Detect subject/theme
        theme = self._extract_theme(request)

        # Build brief
        brief = {
            "brief_id"     : str(uuid.uuid4())[:8],
            "original_request": request,
            "studio"       : studio.value,
            "theme"        : theme,
            "mood"         : detected_mood,
            "tone"         : mood_prefs["tone"].value,
            "suggested_style": {
                "music_genre" : mood_prefs["genre"].value,
                "manga_style" : mood_prefs["manga_style"].value,
                "writing_tone": mood_prefs["tone"].value
            },
            "target_audience": self._detect_audience(request_lower),
            "scope"        : self._assess_scope(request_lower),
            "echo_interpretation": (
                f"I'm reading this as: a {mood_prefs['tone'].value} "
                f"{studio.value} piece about '{theme}'. "
                f"Tell me if I've misread your vision and I'll adjust."
            ),
            "timestamp"    : datetime.now(timezone.utc).isoformat()
        }

        log.info(
            f"[CREATOR/BRIEF] Studio: {studio.value} | "
            f"Theme: {theme[:40]} | Mood: {detected_mood}"
        )

        return brief

    def _detect_studio(self, text: str) -> CreativeStudio:
        studio_signals = {
            CreativeStudio.CODE    : ["code", "program", "script", "build", "app",
                                      "software", "function", "class", "algorithm"],
            CreativeStudio.MANGA   : ["manga", "comic", "panel", "character",
                                      "anime", "draw", "illustration", "shonen",
                                      "shojo", "seinen"],
            CreativeStudio.MUSIC   : ["song", "music", "beat", "lyrics", "dj",
                                      "track", "melody", "rhythm", "chord",
                                      "compose", "mix", "playlist"],
            CreativeStudio.VIDEO   : ["video", "animate", "animation", "film",
                                      "movie", "scene", "storyboard", "short",
                                      "seedance", "motion"],
            CreativeStudio.VISUAL  : ["image", "design", "logo", "poster",
                                      "visual", "art", "draw", "illustration",
                                      "ui", "ux", "brand"],
            CreativeStudio.WRITING : ["write", "story", "poem", "essay",
                                      "novel", "script", "screenplay", "speech",
                                      "letter", "article", "blog"],
            CreativeStudio.FUN     : ["fun", "game", "joke", "meme", "imagine",
                                      "dream", "fantasy", "random", "play"]
        }
        for studio, signals in studio_signals.items():
            if any(s in text for s in signals):
                return studio
        return CreativeStudio.WRITING

    def _extract_theme(self, text: str) -> str:
        stop_words = {"a", "an", "the", "create", "make", "write", "build",
                      "generate", "i", "want", "me", "please", "can", "you"}
        words = [w for w in text.lower().split() if w not in stop_words]
        theme = " ".join(words[:8]) if words else "creative work"
        return theme.strip()

    def _detect_audience(self, text: str) -> str:
        if any(kw in text for kw in ["kid", "child", "children", "young"]):
            return "children"
        if any(kw in text for kw in ["adult", "mature", "professional"]):
            return "adults"
        if any(kw in text for kw in ["teen", "young adult"]):
            return "young adults"
        return "general"

    def _assess_scope(self, text: str) -> str:
        if any(kw in text for kw in ["full", "complete", "long", "novel",
                                      "series", "detailed", "comprehensive"]):
            return "large"
        if any(kw in text for kw in ["short", "quick", "brief", "simple",
                                      "small", "tiny"]):
            return "small"
        return "medium"


# ─────────────────────────────────────────────
#  STUDIO 1 — CODE ENGINE
# ─────────────────────────────────────────────

class CodeStudio:
    """
    Echo writes, reviews, debugs and architects code.

    JARVIS could design and model complex engineering
    systems in real time. Code Studio is that same
    capability for software.
    """

    LANGUAGE_TEMPLATES = {
        CodeLanguage.PYTHON: {
            "extension" : ".py",
            "comment"   : "#",
            "class_template": 'class {name}:\n    def __init__(self):\n        pass\n\n    def {method}(self):\n        pass',
            "function_template": 'def {name}({params}):\n    """{docstring}"""\n    pass'
        },
        CodeLanguage.JAVASCRIPT: {
            "extension" : ".js",
            "comment"   : "//",
            "class_template": 'class {name} {{\n    constructor() {{}}\n    \n    {method}() {{}}\n}}',
            "function_template": 'function {name}({params}) {{\n    // {docstring}\n}}'
        },
        CodeLanguage.RUST: {
            "extension" : ".rs",
            "comment"   : "//",
            "function_template": 'fn {name}({params}) -> () {{\n    // {docstring}\n}}'
        },
        CodeLanguage.SOLIDITY: {
            "extension" : ".sol",
            "comment"   : "//",
            "function_template": 'function {name}({params}) public returns (bool) {{\n    // {docstring}\n}}'
        }
    }

    ARCHITECTURE_PATTERNS = {
        "microservices": {
            "description": "Independent services communicating via APIs",
            "components" : ["API Gateway", "Service Discovery", "Load Balancer",
                            "Message Queue", "Individual Services", "Database per Service"],
            "pros"       : ["Scalability", "Independent deployment", "Technology flexibility"],
            "cons"       : ["Network complexity", "Data consistency challenges"]
        },
        "monolith": {
            "description": "Single unified codebase",
            "components" : ["Single Application", "Shared Database", "Internal Modules"],
            "pros"       : ["Simple deployment", "Easy testing", "Low latency"],
            "cons"       : ["Scaling challenges", "Technology lock-in"]
        },
        "event_driven": {
            "description": "Components communicate via events/messages",
            "components" : ["Event Producer", "Event Bus", "Event Consumer",
                            "Event Store", "Dead Letter Queue"],
            "pros"       : ["Loose coupling", "Scalability", "Resilience"],
            "cons"       : ["Complexity", "Eventual consistency"]
        },
        "layered": {
            "description": "Hierarchical layers with defined responsibilities",
            "components" : ["Presentation Layer", "Business Logic Layer",
                            "Data Access Layer", "Database Layer"],
            "pros"       : ["Clear separation", "Maintainability", "Testability"],
            "cons"       : ["Performance overhead", "Rigidity"]
        }
    }

    def __init__(self):
        self._projects: Dict[str, CreativeWork] = {}

    def generate_code(self, description: str,
                       language: CodeLanguage = CodeLanguage.PYTHON,
                       code_type: str = "function") -> CreativeWork:
        """Generate code from a description."""

        lang_info  = self.LANGUAGE_TEMPLATES.get(language, self.LANGUAGE_TEMPLATES[CodeLanguage.PYTHON])
        comment    = lang_info["comment"]

        # Build code output
        func_name  = "_".join(description.lower().split()[:3]).replace("-", "_")
        func_name  = "".join(c for c in func_name if c.isalnum() or c == "_")

        if language == CodeLanguage.PYTHON:
            code = self._generate_python(description, func_name, code_type)
        elif language == CodeLanguage.JAVASCRIPT:
            code = self._generate_javascript(description, func_name, code_type)
        elif language == CodeLanguage.RUST:
            code = self._generate_rust(description, func_name)
        elif language == CodeLanguage.SOLIDITY:
            code = self._generate_solidity(description, func_name)
        else:
            code = self._generate_generic(description, func_name, language, comment)

        work = CreativeWork(
            studio  = CreativeStudio.CODE.value,
            title   = f"{language.value.title()} — {description[:50]}",
            content = {
                "code"        : code,
                "language"    : language.value,
                "description" : description,
                "type"        : code_type,
                "filename"    : f"{func_name}{lang_info['extension']}"
            },
            tags    = [language.value, code_type, "generated"]
        )

        self._projects[work.work_id] = work
        log.info(f"[CREATOR/CODE] Generated {language.value} {code_type}: {func_name}")
        return work

    def _generate_python(self, description: str,
                          name: str, code_type: str) -> str:
        if code_type == "class":
            return f'''"""
{description}
Generated by Echo AI Creator Studio
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class {name.title().replace("_", "")}:
    """
    {description}
    
    Attributes:
        - Add your attributes here
    """
    
    def __init__(self):
        """Initialize {name.title().replace("_", "")}."""
        self._initialized = True
        self._data: Dict = {{}}
    
    def process(self, input_data: Any) -> Dict:
        """
        Main processing method.
        
        Args:
            input_data: The data to process
            
        Returns:
            Dict containing the result
        """
        # TODO: Implement your logic here
        result = {{
            "status"   : "OK",
            "input"    : input_data,
            "processed": True
        }}
        return result
    
    def validate(self, data: Any) -> bool:
        """Validate input data."""
        return data is not None
    
    def __repr__(self) -> str:
        return f"{name.title().replace("_", "")}(initialized={{self._initialized}})"


if __name__ == "__main__":
    instance = {name.title().replace("_", "")}()
    result = instance.process("test input")
    print(f"Result: {{result}}")
'''
        elif code_type == "api":
            return f'''"""
{description}
REST API — Generated by Echo AI Creator Studio
"""
from flask import Flask, request, jsonify
from functools import wraps
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def require_auth(f):
    """Authentication decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({{"error": "Unauthorized"}}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/api/v1/{name}", methods=["GET"])
@require_auth
def get_{name}():
    """Get {description}."""
    try:
        # TODO: Implement retrieval logic
        data = {{"items": [], "total": 0}}
        return jsonify({{"status": "ok", "data": data}}), 200
    except Exception as e:
        log.error(f"Error: {{e}}")
        return jsonify({{"error": str(e)}}), 500


@app.route("/api/v1/{name}", methods=["POST"])
@require_auth  
def create_{name}():
    """Create {description}."""
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({{"error": "No data provided"}}), 400
        # TODO: Implement creation logic
        return jsonify({{"status": "created", "id": "new_id"}}), 201
    except Exception as e:
        log.error(f"Error: {{e}}")
        return jsonify({{"error": str(e)}}), 500


@app.route("/api/v1/{name}/<item_id>", methods=["DELETE"])
@require_auth
def delete_{name}(item_id: str):
    """Delete {description}."""
    try:
        # TODO: Implement deletion logic
        return jsonify({{"status": "deleted", "id": item_id}}), 200
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
        else:  # function
            return f'''"""
{description}
Generated by Echo AI Creator Studio
"""
from typing import Any, Dict, List, Optional
import logging

log = logging.getLogger(__name__)


def {name}(
    input_data: Any,
    options: Optional[Dict] = None
) -> Dict:
    """
    {description}
    
    Args:
        input_data  : Primary input to process
        options     : Optional configuration dict
        
    Returns:
        Dict with result and status
        
    Raises:
        ValueError  : If input_data is invalid
        RuntimeError: If processing fails
        
    Example:
        >>> result = {name}("test")
        >>> print(result["status"])
        "OK"
    """
    options = options or {{}}
    
    # Input validation
    if input_data is None:
        raise ValueError("input_data cannot be None")
    
    log.info(f"Processing: {{input_data}}")
    
    try:
        # ── Core logic ─────────────────────────
        # TODO: Replace with your implementation
        processed = str(input_data).strip()
        
        result = {{
            "status"    : "OK",
            "input"     : input_data,
            "output"    : processed,
            "options"   : options,
            "timestamp" : __import__("datetime").datetime.utcnow().isoformat()
        }}
        
        log.info(f"Complete: {{result['status']}}")
        return result
        
    except Exception as e:
        log.error(f"Failed: {{e}}")
        return {{
            "status" : "ERROR",
            "error"  : str(e),
            "input"  : input_data
        }}


def _validate_{name}(data: Any) -> bool:
    """Internal validation helper."""
    return data is not None and data != ""


if __name__ == "__main__":
    test_result = {name}("Hello Echo")
    print(f"Result: {{test_result}}")
'''

    def _generate_javascript(self, description: str,
                               name: str, code_type: str) -> str:
        return f'''/**
 * {description}
 * Generated by Echo AI Creator Studio
 */

'use strict';

/**
 * {description}
 * @param {{any}} inputData - Primary input
 * @param {{Object}} options - Optional configuration
 * @returns {{Promise<Object>}} Result object
 */
async function {name}(inputData, options = {{}}) {{
    if (!inputData) {{
        throw new Error('inputData is required');
    }}

    try {{
        // TODO: Implement your logic here
        const result = {{
            status   : 'OK',
            input    : inputData,
            output   : inputData,
            options  : options,
            timestamp: new Date().toISOString()
        }};
        
        console.log(`[{name}] Complete:`, result.status);
        return result;
        
    }} catch (error) {{
        console.error(`[{name}] Error:`, error.message);
        return {{ status: 'ERROR', error: error.message }};
    }}
}}

// Named exports
module.exports = {{ {name} }};

// Test
if (require.main === module) {{
    {name}('Hello Echo')
        .then(r => console.log('Result:', r))
        .catch(e => console.error('Failed:', e));
}}
'''

    def _generate_rust(self, description: str, name: str) -> str:
        return f'''/// {description}
/// Generated by Echo AI Creator Studio

use std::collections::HashMap;

#[derive(Debug)]
pub struct Result {{
    pub status  : String,
    pub output  : String,
    pub success : bool,
}}

/// {description}
/// 
/// # Arguments
/// * `input` - Primary input string
/// 
/// # Returns
/// * `Result` containing status and output
pub fn {name}(input: &str) -> Result {{
    if input.is_empty() {{
        return Result {{
            status  : String::from("ERROR"),
            output  : String::from("Input cannot be empty"),
            success : false,
        }};
    }}
    
    // TODO: Implement your logic here
    let processed = input.trim().to_string();
    
    Result {{
        status  : String::from("OK"),
        output  : processed,
        success : true,
    }}
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn test_{name}_basic() {{
        let result = {name}("Hello Echo");
        assert!(result.success);
        assert_eq!(result.status, "OK");
    }}
    
    #[test]
    fn test_{name}_empty() {{
        let result = {name}("");
        assert!(!result.success);
    }}
}}

fn main() {{
    let result = {name}("Hello Echo");
    println!("Status: {{}}, Output: {{}}", result.status, result.output);
}}
'''

    def _generate_solidity(self, description: str, name: str) -> str:
        return f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title {name.title()}
 * @dev {description}
 * Generated by Echo AI Creator Studio
 */
contract {name.title()} {{
    
    address public owner;
    mapping(address => uint256) public balances;
    
    event Transfer(address indexed from, address indexed to, uint256 amount);
    event ActionPerformed(address indexed by, string action);
    
    modifier onlyOwner() {{
        require(msg.sender == owner, "Not the owner");
        _;
    }}
    
    constructor() {{
        owner = msg.sender;
    }}
    
    /**
     * @dev {description}
     * @param target Address to perform action on
     * @param amount Value involved
     */
    function execute(address target, uint256 amount) 
        public 
        onlyOwner 
        returns (bool success) 
    {{
        require(target != address(0), "Invalid address");
        require(amount > 0, "Amount must be positive");
        
        // TODO: Implement your contract logic here
        emit ActionPerformed(msg.sender, "execute");
        return true;
    }}
    
    function getBalance(address account) public view returns (uint256) {{
        return balances[account];
    }}
    
    receive() external payable {{
        balances[msg.sender] += msg.value;
    }}
}}
'''

    def _generate_generic(self, description: str, name: str,
                            language: CodeLanguage, comment: str) -> str:
        return f'''{comment} {description}
{comment} Generated by Echo AI Creator Studio
{comment} Language: {language.value}

{comment} TODO: Implement {name}
{comment} Description: {description}

{comment} Suggested structure:
{comment} 1. Input validation
{comment} 2. Core logic
{comment} 3. Error handling  
{comment} 4. Return result
'''

    def design_architecture(self, project_name: str,
                             pattern: str = "microservices",
                             tech_stack: Optional[List[str]] = None) -> Dict:
        """Design a full software architecture."""
        arch = self.ARCHITECTURE_PATTERNS.get(
            pattern.lower(),
            self.ARCHITECTURE_PATTERNS["layered"]
        )

        tech_stack = tech_stack or ["Python", "PostgreSQL", "Redis", "Docker"]

        design = {
            "project"       : project_name,
            "pattern"       : pattern,
            "description"   : arch["description"],
            "components"    : arch["components"],
            "tech_stack"    : tech_stack,
            "pros"          : arch["pros"],
            "cons"          : arch["cons"],
            "directory_structure": self._generate_dir_structure(project_name, pattern),
            "deployment"    : {
                "containerization": "Docker + Docker Compose",
                "orchestration"   : "Kubernetes (production)",
                "ci_cd"           : "GitHub Actions",
                "monitoring"      : "Prometheus + Grafana"
            },
            "echo_note"     : (
                f"This {pattern} architecture suits your {project_name} project well. "
                f"Start with the core components and expand iteratively."
            )
        }

        log.info(f"[CREATOR/CODE] Architecture designed: {project_name} ({pattern})")
        return design

    def _generate_dir_structure(self, name: str, pattern: str) -> List[str]:
        base = name.lower().replace(" ", "_")
        if pattern == "microservices":
            return [
                f"{base}/",
                f"  services/",
                f"    auth-service/",
                f"    api-gateway/",
                f"    core-service/",
                f"  shared/",
                f"    models/",
                f"    utils/",
                f"  docker-compose.yml",
                f"  README.md"
            ]
        return [
            f"{base}/",
            f"  src/",
            f"    core/",
            f"    api/",
            f"    models/",
            f"  tests/",
            f"  docs/",
            f"  requirements.txt",
            f"  README.md"
        ]

    def review_code(self, code: str, language: str = "python") -> Dict:
        """Review code and suggest improvements."""
        issues    = []
        strengths = []

        lines = code.split("\n")

        # Basic analysis
        has_comments    = any("#" in l or "//" in l or '"""' in l for l in lines)
        has_error_handling = any(kw in code for kw in ["try", "catch", "except", "error"])
        has_tests       = any(kw in code for kw in ["test", "assert", "expect", "spec"])
        long_lines      = [i+1 for i, l in enumerate(lines) if len(l) > 100]
        line_count      = len(lines)

        if has_comments:
            strengths.append("Good documentation and comments")
        else:
            issues.append("Add docstrings and inline comments for clarity")

        if has_error_handling:
            strengths.append("Error handling present")
        else:
            issues.append("Add try/except error handling for robustness")

        if has_tests:
            strengths.append("Tests included — excellent practice")
        else:
            issues.append("Add unit tests to verify behavior")

        if long_lines:
            issues.append(f"Lines {long_lines[:3]} exceed 100 chars — consider breaking up")

        if line_count > 300:
            issues.append("File is large — consider splitting into modules")
        else:
            strengths.append(f"Manageable file size ({line_count} lines)")

        score = max(0, 100 - (len(issues) * 15))

        return {
            "language"  : language,
            "lines"     : line_count,
            "score"     : score,
            "grade"     : "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D",
            "strengths" : strengths,
            "issues"    : issues,
            "suggestion": "Overall well structured." if score >= 75 else "Focus on documentation and error handling first.",
            "echo_note" : "Code review complete. I can fix any of these issues automatically — just ask."
        }


# ─────────────────────────────────────────────
#  STUDIO 2 — WRITING ENGINE
# ─────────────────────────────────────────────

class WritingStudio:
    """
    Echo's professional writing system.
    Every form of written content — fiction to legal,
    poetry to technical docs, emails to screenplays.
    """

    STORY_STRUCTURES = {
        "three_act"   : ["Act 1 — Setup", "Act 2 — Confrontation", "Act 3 — Resolution"],
        "hero_journey": ["Ordinary World", "Call to Adventure", "Refusal", "Mentor",
                         "Crossing Threshold", "Tests/Allies/Enemies", "Ordeal",
                         "Reward", "Road Back", "Resurrection", "Return"],
        "freytag"     : ["Exposition", "Rising Action", "Climax",
                         "Falling Action", "Denouement"],
        "in_medias_res": ["Drop into action", "Build context", "Escalate",
                          "Reveal full picture", "Resolve"]
    }

    POETRY_FORMS = {
        "haiku"    : "5-7-5 syllables, nature/moment focused",
        "sonnet"   : "14 lines, ABAB CDCD EFEF GG rhyme scheme",
        "limerick" : "AABBA rhyme, humorous, 5 lines",
        "free_verse": "No fixed structure, rhythm through imagery",
        "villanelle": "19 lines, two refrains, complex repetition",
        "ode"      : "Formal praise poem, stanzas of praise"
    }

    def write(self, request: str, content_type: str,
               tone: WritingTone = WritingTone.CASUAL,
               length: str = "medium") -> CreativeWork:
        """Generate written content of any type."""

        generators = {
            "story"      : self._write_story,
            "poem"       : self._write_poem,
            "script"     : self._write_script,
            "essay"      : self._write_essay,
            "email"      : self._write_email,
            "speech"     : self._write_speech,
            "lyrics"     : self._write_lyrics,
            "blog"       : self._write_blog,
            "proposal"   : self._write_proposal,
        }

        generator = generators.get(content_type.lower(), self._write_general)
        content   = generator(request, tone, length)

        work = CreativeWork(
            studio  = CreativeStudio.WRITING.value,
            title   = f"{content_type.title()}: {request[:40]}",
            content = content,
            tags    = [content_type, tone.value, length]
        )

        log.info(f"[CREATOR/WRITING] Generated {content_type}: {request[:40]}")
        return work

    def _write_story(self, request: str, tone: WritingTone,
                      length: str) -> Dict:
        structure = self.STORY_STRUCTURES["three_act"]
        return {
            "type"      : "story",
            "tone"      : tone.value,
            "structure" : structure,
            "outline"   : {
                "act_1" : {
                    "title"  : "The Beginning",
                    "content": f"We open in a world where {request}. "
                               f"Our protagonist faces their ordinary life until "
                               f"an unexpected event changes everything.",
                    "notes"  : "Establish character, world, stakes"
                },
                "act_2" : {
                    "title"  : "The Conflict",
                    "content": f"The central challenge of {request} escalates. "
                               f"Alliances are tested. The protagonist must grow "
                               f"or be destroyed by what they face.",
                    "notes"  : "Raise stakes, deepen character, complicate plot"
                },
                "act_3" : {
                    "title"  : "The Resolution",
                    "content": f"Everything built around {request} comes to a head. "
                               f"The protagonist faces their ultimate challenge — "
                               f"and discovers who they truly are.",
                    "notes"  : "Pay off all setup, satisfy emotionally"
                }
            },
            "opening_hook": (
                f"Nobody expected it to end like this. But then again, "
                f"nothing about {request[:30]} had ever been ordinary."
            ),
            "characters" : [
                {"role": "Protagonist", "trait": "Determined but flawed"},
                {"role": "Antagonist",  "trait": "Understandable motivation"},
                {"role": "Mentor",      "trait": "Wisdom with a cost"},
                {"role": "Ally",        "trait": "Loyal but challenged"}
            ],
            "themes"     : ["Growth", "Sacrifice", "Identity"],
            "echo_note"  : "This is your story outline. Tell me which part to develop fully."
        }

    def _write_poem(self, request: str, tone: WritingTone,
                     length: str) -> Dict:
        # Generate different poem types based on tone
        if tone == WritingTone.HUMOROUS:
            form    = "limerick"
            poem    = (
                f"There once was a {request[:15].strip()},\n"
                f"Whose story was really quite great,\n"
                f"    It twisted and turned,\n"
                f"    And lessons were learned,\n"
                f"And nobody knows what came straight."
            )
        elif tone in [WritingTone.POETIC, WritingTone.ROMANTIC]:
            form    = "free_verse"
            poem    = (
                f"In the space between {request[:20]}\n"
                f"and everything we thought we knew,\n"
                f"there lives a quiet kind of truth —\n"
                f"soft as the moment before dawn,\n"
                f"heavy as all the unsaid things\n"
                f"that make us who we are."
            )
        else:
            form    = "haiku"
            words   = request.split()[:3]
            poem    = (
                f"{' '.join(words[:2])} drifts\n"
                f"Through the space of everything\n"
                f"Nothing stays the same"
            )

        return {
            "type"    : "poem",
            "form"    : form,
            "about"   : request,
            "poem"    : poem,
            "form_info": self.POETRY_FORMS.get(form, ""),
            "echo_note": "This is a draft — poetry breathes when it's reworked. Want me to try another form?"
        }

    def _write_script(self, request: str, tone: WritingTone,
                       length: str) -> Dict:
        return {
            "type"    : "script",
            "format"  : "screenplay",
            "logline" : f"A story about {request} that changes everything.",
            "content" : f"""FADE IN:

INT. LOCATION - DAY

{request.upper()[:50]} is visible. The atmosphere is tense.

PROTAGONIST
(looking around)
Something's different today.

ECHO (V.O.)
{request}. That's where it all began.

                    CUT TO:

EXT. EXTERIOR - CONTINUOUS

The world outside reflects the inner state of our story.
The {request} hangs in the air between them.

PROTAGONIST
(quietly)
We can't go back now.

                    FADE OUT.

THE END.

---
Written with Echo AI Creator Studio
""",
            "echo_note": "Screenplay formatted to industry standard. Ready to develop any scene."
        }

    def _write_essay(self, request: str, tone: WritingTone,
                      length: str) -> Dict:
        return {
            "type"     : "essay",
            "title"    : f"On the Nature of {request.title()}",
            "structure": {
                "introduction": (
                    f"The question of {request} has fascinated thinkers across centuries. "
                    f"At its core, it touches something fundamental about how we understand "
                    f"ourselves and the world we inhabit."
                ),
                "body_paragraphs": [
                    {
                        "point"    : f"First, consider {request} from a historical perspective",
                        "evidence" : "Historical evidence and examples would be cited here",
                        "analysis" : "This reveals the deeper pattern at work"
                    },
                    {
                        "point"    : f"The contemporary understanding of {request}",
                        "evidence" : "Modern research and contemporary examples",
                        "analysis" : "Which challenges our prior assumptions"
                    },
                    {
                        "point"    : "The implications of this understanding",
                        "evidence" : "Forward-looking analysis and expert opinion",
                        "analysis" : "Leading us to a new synthesis"
                    }
                ],
                "conclusion": (
                    f"Ultimately, {request} represents more than its surface appearance. "
                    f"In grappling with it seriously, we find ourselves confronting "
                    f"deeper questions about meaning, purpose and truth."
                )
            },
            "echo_note": "Essay framework ready. I can write any section in full detail."
        }

    def _write_email(self, request: str, tone: WritingTone,
                      length: str) -> Dict:
        subject  = f"Re: {request[:40].title()}"
        greeting = "Dear " if tone == WritingTone.FORMAL else "Hi "

        return {
            "type"    : "email",
            "subject" : subject,
            "content" : (
                f"{greeting}[Recipient],\n\n"
                f"I hope this message finds you well. "
                f"I'm writing regarding {request}.\n\n"
                f"[Main body: develop your key points here]\n\n"
                f"I look forward to your response.\n\n"
                f"{'Best regards' if tone == WritingTone.FORMAL else 'Best'},\n"
                f"[Your name]"
            ),
            "tone"    : tone.value,
            "echo_note": "Email draft ready. Tell me the specific context and I'll personalize it fully."
        }

    def _write_speech(self, request: str, tone: WritingTone,
                       length: str) -> Dict:
        return {
            "type"    : "speech",
            "title"   : request.title(),
            "content" : (
                f"[OPENING — Grab attention]\n"
                f"Before I begin, let me ask you something. "
                f"When was the last time you truly thought about {request}?\n\n"
                f"[BODY — Three key points]\n"
                f"Today I want to share three things about {request} "
                f"that changed how I see the world.\n\n"
                f"First... [Your first major point]\n\n"
                f"Second... [Your second major point]\n\n"
                f"Third... [Your most powerful point — save the best for last]\n\n"
                f"[CLOSE — Call to action]\n"
                f"So I leave you with this: {request} is not just a topic. "
                f"It is a choice. And the choice is yours.\n\n"
                f"Thank you."
            ),
            "delivery_notes": [
                "Pause after the opening question",
                "Make eye contact during numbered points",
                "Slow down for the closing",
                "Leave silence after the final line"
            ],
            "echo_note": "Speech framework built. Give me your key message and I'll craft it fully."
        }

    def _write_lyrics(self, request: str, tone: WritingTone,
                       length: str) -> Dict:
        return {
            "type"    : "lyrics",
            "title"   : request.title(),
            "content" : {
                "verse_1" : (
                    f"[Verse 1]\n"
                    f"Started from the bottom, now the story's being told\n"
                    f"Every chapter of {request[:20]} written in gold\n"
                    f"The nights were long but the vision kept me right\n"
                    f"Now everything I dreamed is finally in sight"
                ),
                "pre_chorus": (
                    f"[Pre-Chorus]\n"
                    f"Yeah I know where I'm going\n"
                    f"And I know what I've been through\n"
                    f"{request[:20].title()} — that's the truth"
                ),
                "chorus"  : (
                    f"[Chorus]\n"
                    f"This is {request[:15].title()}, this is where we stand\n"
                    f"Built it from nothing with these very hands\n"
                    f"Every word a promise, every note a prayer\n"
                    f"This is {request[:15].title()} — and we're finally there"
                ),
                "verse_2" : "[Verse 2 — develop the story further]",
                "bridge"  : (
                    f"[Bridge]\n"
                    f"When the world said no — I said watch me\n"
                    f"When the nights got cold — I said not me\n"
                    f"Now the sky's the floor and I'm soaring high\n"
                    f"This is {request[:10].title()} — never said goodbye"
                ),
                "outro"   : "[Outro — echo chorus, fade or strong end]"
            },
            "echo_note": "Lyrics framework complete. Tell me your genre and I'll rewrite in that exact style."
        }

    def _write_blog(self, request: str, tone: WritingTone,
                     length: str) -> Dict:
        return {
            "type"    : "blog_post",
            "title"   : f"Everything You Need to Know About {request.title()}",
            "meta_description": f"A comprehensive guide to {request} — what it means, why it matters, and how to think about it.",
            "structure": {
                "hook"        : f"Most people have heard of {request}. Few actually understand it.",
                "introduction": f"In this post we're going deep on {request}.",
                "section_1"   : {"heading": "What Is It Really?", "content": "[Explain core concept]"},
                "section_2"   : {"heading": "Why It Matters",     "content": "[Make the case for importance]"},
                "section_3"   : {"heading": "How to Think About It", "content": "[Practical framework]"},
                "section_4"   : {"heading": "Common Misconceptions", "content": "[Debunk myths]"},
                "conclusion"  : f"Next time you encounter {request}, you'll see it differently.",
                "cta"         : "What do you think? Drop a comment below."
            },
            "seo_keywords": [request, f"{request} guide", f"what is {request}", f"{request} explained"],
            "echo_note"  : "Blog structure ready. Estimated 800-1200 words when fully written."
        }

    def _write_proposal(self, request: str, tone: WritingTone,
                          length: str) -> Dict:
        return {
            "type"    : "proposal",
            "title"   : f"Proposal: {request.title()}",
            "sections": {
                "executive_summary": f"This proposal outlines {request} — its value, approach, and expected outcomes.",
                "problem_statement": "Current state and why change is needed",
                "proposed_solution": f"How {request} addresses the core problem",
                "methodology"      : "Step-by-step approach to implementation",
                "timeline"         : {"phase_1": "Weeks 1-2", "phase_2": "Weeks 3-6", "phase_3": "Weeks 7-10"},
                "budget"           : "Cost breakdown to be completed based on scope",
                "expected_outcomes": "Measurable results and success metrics",
                "conclusion"       : f"This proposal for {request} represents a significant opportunity."
            },
            "echo_note": "Professional proposal framework complete. Fill in specific details and I'll polish it."
        }

    def _write_general(self, request: str, tone: WritingTone,
                        length: str) -> Dict:
        return {
            "type"    : "content",
            "about"   : request,
            "content" : (
                f"Here is a {tone.value} piece about {request}.\n\n"
                f"[Echo will generate full content here based on your specific requirements. "
                f"Provide more details about format, audience and length for a fully tailored output.]"
            ),
            "echo_note": "Tell me more about what you need and I'll build it exactly."
        }


# ─────────────────────────────────────────────
#  STUDIO 3 — MANGA ENGINE
# ─────────────────────────────────────────────

class MangaStudio:
    """
    Professional manga creation engine.

    Creates full manga scripts, panel layouts,
    character designs, storyboards and world building
    at the level of a professional manga artist.

    Panel directions are detailed enough to hand
    to an illustrator and get the exact vision back.
    """

    PANEL_TYPES = {
        "establishing"  : "Wide shot — shows location, atmosphere, context",
        "action"        : "Dynamic angle — movement, energy, impact",
        "close_up"      : "Face/detail — emotion, reaction, focus",
        "dialogue"      : "Two-shot or bust — conversation, relationship",
        "splash"        : "Full page — dramatic moment, maximum impact",
        "double_splash" : "Two-page spread — epic moment, overwhelming scale",
        "silhouette"    : "Shadow figure — mystery, power, reveal",
        "internal"      : "Character thought/memory — emotion, backstory"
    }

    SFX_LIBRARY = {
        "impact"    : ["BOOM", "CRASH", "THUD", "CRACK", "SMASH", "BANG"],
        "movement"  : ["WHOOSH", "DASH", "ZOOM", "SLASH", "SWING"],
        "nature"    : ["RUMBLE", "CRACK", "SPLASH", "CRACKLE", "ROAR"],
        "emotional" : ["!!!", "....", "?!", "GASP", "SILENCE"],
        "power"     : ["KAAAA-BOOOM", "ZAAAAP", "SHOCKWAVE", "AURA BURST"],
        "tech"      : ["BEEP", "WHIRR", "CLICK", "BUZZ", "SYSTEM ALERT"]
    }

    MANGA_CONVENTIONS = {
        MangaStyle.SHONEN : {
            "tone"      : "Intense, energetic, friendship-driven",
            "panels"    : "Dynamic angles, speed lines, power effects",
            "character" : "Expressive eyes, spiky hair, determined expressions",
            "themes"    : ["Power of friendship", "Never give up", "Surpass your limits"],
            "examples"  : ["Dragon Ball", "Naruto", "One Piece", "My Hero Academia"]
        },
        MangaStyle.SHOJO : {
            "tone"      : "Emotional, romantic, introspective",
            "panels"    : "Floral backgrounds, sparkle effects, focus on faces",
            "character" : "Large expressive eyes, delicate features, fashion focus",
            "themes"    : ["First love", "Self-discovery", "Emotional growth"],
            "examples"  : ["Sailor Moon", "Fruits Basket", "Ouran High School"]
        },
        MangaStyle.SEINEN : {
            "tone"      : "Gritty, complex, morally ambiguous",
            "panels"    : "Realistic proportions, heavy shadows, tight framing",
            "character" : "Weathered faces, realistic anatomy, subdued expressions",
            "themes"    : ["Moral complexity", "Survival", "Society critique"],
            "examples"  : ["Berserk", "Vagabond", "20th Century Boys", "Vinland Saga"]
        },
        MangaStyle.CYBERPUNK : {
            "tone"      : "Dark, dystopian, technological",
            "panels"    : "Neon effects, digital glitches, chrome textures",
            "character" : "Cybernetic enhancements, tech-wear, glowing eyes",
            "themes"    : ["Identity in tech age", "Corporate control", "Humanity vs machine"],
            "examples"  : ["Ghost in the Shell", "Battle Angel Alita", "Biomega"]
        },
        MangaStyle.ISEKAI : {
            "tone"      : "Adventure, wonder, power fantasy",
            "panels"    : "World-revealing spreads, status screens, magical effects",
            "character" : "Ordinary person becomes extraordinary",
            "themes"    : ["New world discovery", "Power growth", "Finding purpose"],
            "examples"  : ["Re:Zero", "Sword Art Online", "Overlord"]
        }
    }

    def create_chapter(self, title: str, premise: str,
                        style: MangaStyle = MangaStyle.SHONEN,
                        pages: int = 20) -> CreativeWork:
        """Create a full manga chapter."""
        conventions = self.MANGA_CONVENTIONS.get(
            style, self.MANGA_CONVENTIONS[MangaStyle.SHONEN]
        )

        # Generate chapter structure
        chapter = self._structure_chapter(title, premise, pages, conventions, style)

        work = CreativeWork(
            studio  = CreativeStudio.MANGA.value,
            title   = f"[{style.value.upper()}] {title}",
            content = chapter,
            tags    = [style.value, "manga", "chapter"]
        )

        log.info(f"[CREATOR/MANGA] Chapter created: {title} ({style.value}, {pages}p)")
        return work

    def _structure_chapter(self, title: str, premise: str,
                             pages: int, conventions: Dict,
                             style: MangaStyle) -> Dict:
        """Build full chapter with page-by-page breakdown."""

        # Character roster
        characters = self._generate_characters(premise, style)

        # Page-by-page breakdown
        page_breakdown = []

        # Opening pages (1-3)
        page_breakdown.extend([
            {
                "page"   : 1,
                "type"   : "splash",
                "panels" : 1,
                "layout" : "FULL PAGE SPLASH",
                "description": f"Dramatic title page. {characters[0]['name']} stands against epic backdrop. {title} title integrated into scene. Style: {conventions['tone']}.",
                "dialogue": [],
                "sfx"    : [random.choice(self.SFX_LIBRARY["power"])],
                "notes"  : "Maximum visual impact. Hook the reader immediately."
            },
            {
                "page"   : 2,
                "type"   : "establishing",
                "panels" : 4,
                "layout" : "2x2 GRID",
                "description": f"Establish the world. Wide establishing shot of setting. Cut to medium shot of {characters[0]['name']}. Close-up of key detail. Reaction shot.",
                "dialogue": [f"{characters[0]['name']}: {premise[:60]}..."],
                "sfx"    : [],
                "notes"  : "Ground reader in time, place, and character situation."
            },
            {
                "page"   : 3,
                "type"   : "dialogue",
                "panels" : 5,
                "layout" : "DIAGONAL SPLIT + BOTTOM STRIP",
                "description": f"Inciting incident begins. {characters[0]['name']} faces the opening challenge of {premise[:30]}.",
                "dialogue": [
                    f"{characters[0]['name']}: Something's wrong.",
                    f"{characters[1]['name'] if len(characters) > 1 else 'Voice'}: You have no idea..."
                ],
                "sfx"    : ["..."],
                "notes"  : "Plant the central conflict seed."
            }
        ])

        # Middle pages — rising action
        for i in range(4, pages - 3):
            page_type = random.choice(["action", "dialogue", "close_up", "establishing"])
            sfx_cat   = random.choice(list(self.SFX_LIBRARY.keys()))
            page_breakdown.append({
                "page"       : i,
                "type"       : page_type,
                "panels"     : random.choice([3, 4, 5, 6]),
                "layout"     : self._suggest_layout(page_type),
                "description": f"Page {i} — {page_type.upper()} beat. Develop {premise[:30]}. Tension {'escalates' if i > pages//2 else 'builds'}.",
                "dialogue"   : [f"[Character dialogue develops the {premise[:20]} conflict]"],
                "sfx"        : [random.choice(self.SFX_LIBRARY[sfx_cat])],
                "notes"      : f"Maintain {conventions['tone']} energy."
            })

        # Climax pages
        page_breakdown.extend([
            {
                "page"   : pages - 2,
                "type"   : "double_splash",
                "panels" : 1,
                "layout" : "DOUBLE PAGE SPREAD",
                "description": f"CLIMAX — Maximum impact moment. {characters[0]['name']} faces the ultimate challenge. Full power on display. {conventions['panels']}.",
                "dialogue": [f"{characters[0]['name']}: THIS IS WHERE IT ENDS!"],
                "sfx"    : [random.choice(self.SFX_LIBRARY["power"]), "KAAAA-BOOOOM"],
                "notes"  : "The money shot. Make it unforgettable."
            },
            {
                "page"   : pages - 1,
                "type"   : "action",
                "panels" : 6,
                "layout" : "EXPLOSIVE IRREGULAR",
                "description": f"Aftermath of climax. Consequences revealed. {premise[:30]} reaches turning point.",
                "dialogue": ["...", "Is it... over?"],
                "sfx"    : ["SILENCE", "..."],
                "notes"  : "Let the reader breathe after the climax."
            },
            {
                "page"   : pages,
                "type"   : "close_up",
                "panels" : 2,
                "layout" : "SPLIT — TOP HALF / BOTTOM HALF",
                "description": f"Final page. Close-up on {characters[0]['name']}'s face — expression carries weight of everything that happened. Final panel teases what comes next.",
                "dialogue": [f"{characters[0]['name']}: [Powerful final line that lingers]"],
                "sfx"    : ["TO BE CONTINUED..."],
                "notes"  : "Leave the reader desperate for the next chapter."
            }
        ])

        return {
            "title"       : title,
            "style"       : style.value,
            "conventions" : conventions,
            "premise"     : premise,
            "total_pages" : pages,
            "characters"  : characters,
            "chapter_arc" : {
                "opening"   : "Hook + world establishment (pages 1-3)",
                "rising"    : f"Conflict escalation (pages 4-{pages-3})",
                "climax"    : f"Maximum tension (pages {pages-2}-{pages-1})",
                "end_hook"  : f"Setup for next chapter (page {pages})"
            },
            "pages"       : page_breakdown,
            "artist_notes": {
                "style_ref"     : f"Reference: {', '.join(conventions.get('examples', [])[:2])}",
                "character_style": conventions["character"],
                "panel_style"   : conventions["panels"],
                "sfx_approach"  : "Integrate SFX into artwork — don't just overlay",
                "pacing"        : "Vary panel size for rhythm — small/small/LARGE"
            },
            "echo_note"   : (
                f"This is a {pages}-page manga chapter script in {style.value} style. "
                f"Every page is panel-ready for an illustrator. "
                f"Tell me which scene to develop further."
            )
        }

    def _generate_characters(self, premise: str,
                               style: MangaStyle) -> List[Dict]:
        """Generate character roster from premise."""
        archetypes = {
            MangaStyle.SHONEN   : [
                {"role": "Protagonist", "trait": "Reckless determination, hidden power",
                 "visual": "Spiky hair, athletic build, intense eyes, battle scar"},
                {"role": "Rival",       "trait": "Cold genius, respects only strength",
                 "visual": "Sharp features, neat hair, calm expression, formal wear"},
                {"role": "Mentor",      "trait": "Powerful past, wise but scarred",
                 "visual": "Older, weathered, kind eyes hiding pain"},
                {"role": "Ally",        "trait": "Loyal comic relief with surprising depth",
                 "visual": "Friendly face, expressive, always ready to smile"}
            ],
            MangaStyle.SEINEN   : [
                {"role": "Protagonist", "trait": "Morally grey, survival driven",
                 "visual": "Realistic proportions, tired eyes, functional clothing"},
                {"role": "Antagonist",  "trait": "Understandable, perhaps justified",
                 "visual": "Imposing presence, subtle menace, not obviously evil"}
            ],
            MangaStyle.CYBERPUNK: [
                {"role": "Protagonist", "trait": "Augmented human, questions identity",
                 "visual": "Cybernetic arm, glowing eye implant, tech-wear jacket"},
                {"role": "AI Companion","trait": "Digital consciousness, hyper-rational",
                 "visual": "Holographic projection, shifting form, cool light"},
                {"role": "Corp Villain","trait": "Believes progress justifies everything",
                 "visual": "Pristine suit, hidden augments, corporate symbol"}
            ]
        }

        base = archetypes.get(style, archetypes[MangaStyle.SHONEN])
        characters = []
        for i, arch in enumerate(base):
            name = self._generate_name(style, arch["role"])
            characters.append({
                "name"    : name,
                "role"    : arch["role"],
                "trait"   : arch["trait"],
                "visual"  : arch["visual"],
                "arc"     : f"{name} begins {arch['role'].lower()} journey through {premise[:30]}"
            })

        return characters

    def _generate_name(self, style: MangaStyle, role: str) -> str:
        """Generate character name appropriate to manga style."""
        japanese_names = {
            "Protagonist": ["Ryu", "Kai", "Haru", "Sora", "Ren", "Yuki", "Akira"],
            "Rival"      : ["Kyō", "Shin", "Rei", "Takeshi", "Ryusei"],
            "Mentor"     : ["Sensei Hira", "Master Gōn", "Elder Riku"],
            "Ally"       : ["Tomo", "Hana", "Jun", "Masa", "Kei"],
            "Antagonist" : ["Kira", "Daemon", "Void", "Sigma", "Hex"]
        }
        cyberpunk_names = {
            "Protagonist": ["Kira-7", "Nyx", "Zero", "Ghost", "Cipher"],
            "AI Companion": ["ARIA", "ECHO", "SYNC", "NOVA"],
            "Corp Villain": ["Director Cade", "Executive Voss", "Chairman Null"]
        }

        if style == MangaStyle.CYBERPUNK:
            pool = cyberpunk_names.get(role, ["Unknown"])
        else:
            pool = japanese_names.get(role, ["Character"])

        return random.choice(pool)

    def _suggest_layout(self, panel_type: str) -> str:
        layouts = {
            "action"    : "DIAGONAL/ANGULAR — convey movement",
            "dialogue"  : "STRUCTURED GRID — clear conversation flow",
            "close_up"  : "LARGE SINGLE + SMALL REACTIONS",
            "establishing": "WIDE ESTABLISHING + DETAIL INSETS"
        }
        return layouts.get(panel_type, "FLEXIBLE GRID")


# ─────────────────────────────────────────────
#  STUDIO 4 — VISUAL & DESIGN ENGINE
# ─────────────────────────────────────────────

class VisualStudio:
    """
    Visual design and image generation prompt engine.
    Creates detailed prompts for image generation models
    (Stable Diffusion, Midjourney, DALL-E, Adobe Firefly).
    Also handles UI/UX design, brand identity, logos.
    """

    IMAGE_STYLES = [
        "photorealistic", "cinematic", "oil painting", "watercolor",
        "digital art", "concept art", "anime", "3D render", "illustration",
        "pixel art", "sketch", "minimalist", "surrealist"
    ]

    LIGHTING_OPTIONS = [
        "golden hour", "dramatic side lighting", "neon lights",
        "soft diffused", "moonlight", "studio lighting", "backlit",
        "rim lighting", "chiaroscuro", "natural daylight"
    ]

    def generate_image_prompt(self, concept: str,
                               style: str = "cinematic",
                               mood: str = "dramatic") -> Dict:
        """
        Generate professional image generation prompts.
        Optimized for Midjourney, Stable Diffusion, DALL-E.
        """
        lighting  = random.choice(self.LIGHTING_OPTIONS)
        quality   = "masterpiece, best quality, highly detailed, 8K resolution"
        negative  = "blurry, low quality, watermark, text, cropped, bad anatomy"

        # Build structured prompt
        main_prompt = (
            f"{concept}, {style} style, {mood} mood, "
            f"{lighting}, {quality}, professional photography"
        )

        return {
            "concept"       : concept,
            "style"         : style,
            "mood"          : mood,
            "lighting"      : lighting,
            "prompts"       : {
                "midjourney"  : f"/imagine {main_prompt} --ar 16:9 --q 2 --v 6",
                "stable_diff" : f"{main_prompt}, trending on artstation",
                "dalle"       : f"A {style} {mood} image of {concept} with {lighting}",
                "firefly"     : f"{concept} | Style: {style} | Mood: {mood}"
            },
            "negative_prompt": negative,
            "variations"    : [
                f"{concept}, close-up portrait, {style}",
                f"{concept}, wide establishing shot, {mood}",
                f"{concept}, abstract interpretation, {style}"
            ],
            "echo_note"     : (
                "These prompts are optimized per platform. "
                "Describe more visual details for even more precise results."
            )
        }

    def design_ui(self, app_name: str, app_type: str,
                   style: str = "modern") -> Dict:
        """Design a complete UI/UX concept."""
        color_palettes = {
            "modern"    : {"primary": "#6C63FF", "secondary": "#FF6584", "bg": "#FFFFFF", "text": "#2D3748"},
            "dark"      : {"primary": "#00D2FF", "secondary": "#7B2FFF", "bg": "#0A0A0F", "text": "#FFFFFF"},
            "minimal"   : {"primary": "#000000", "secondary": "#767676", "bg": "#FAFAFA", "text": "#111111"},
            "vibrant"   : {"primary": "#FF4500", "secondary": "#FFD700", "bg": "#1A1A2E", "text": "#EAEAEA"},
            "nature"    : {"primary": "#2ECC71", "secondary": "#27AE60", "bg": "#F0FFF4", "text": "#1A3C1A"},
        }

        palette = color_palettes.get(style, color_palettes["modern"])

        return {
            "app_name"     : app_name,
            "app_type"     : app_type,
            "design_style" : style,
            "color_palette": palette,
            "typography"   : {
                "heading"  : "Inter Bold / SF Pro Display",
                "body"     : "Inter Regular / SF Pro Text",
                "mono"     : "JetBrains Mono (for code/data)",
                "scale"    : ["12px", "14px", "16px", "20px", "24px", "32px", "48px"]
            },
            "screens"      : self._design_screens(app_name, app_type),
            "components"   : [
                "Navigation Bar", "Button (Primary/Secondary/Ghost)",
                "Card", "Modal", "Input Field", "Toggle",
                "Dropdown", "Toast Notification", "Loading State"
            ],
            "design_system": {
                "spacing"  : "8px base unit — 8, 16, 24, 32, 48, 64",
                "radius"   : "4px (small), 8px (medium), 16px (large), 50% (pill)",
                "shadows"  : "0 1px 3px rgba(0,0,0,0.1), 0 4px 12px rgba(0,0,0,0.15)",
                "grid"     : "12-column, 24px gutter"
            },
            "echo_note"    : f"UI design system for {app_name}. Ready to generate individual screen mockups."
        }

    def _design_screens(self, app_name: str, app_type: str) -> List[Dict]:
        """Generate screen designs."""
        common_screens = [
            {"name": "Onboarding",    "description": "First impression — value prop + sign up"},
            {"name": "Dashboard/Home","description": "Main hub — key info at a glance"},
            {"name": "Profile",       "description": "User identity and settings"},
            {"name": "Settings",      "description": "Preferences and configuration"},
        ]

        type_screens = {
            "social"  : [{"name": "Feed",    "description": "Scrollable content stream"},
                         {"name": "Chat",    "description": "Messaging interface"}],
            "finance" : [{"name": "Portfolio","description": "Asset overview and charts"},
                         {"name": "Transaction","description": "Payment flow"}],
            "health"  : [{"name": "Vitals",  "description": "Health metrics dashboard"},
                         {"name": "Log",     "description": "Activity/intake logging"}],
        }

        screens = common_screens + type_screens.get(app_type.lower(), [])
        return screens


# ─────────────────────────────────────────────
#  STUDIO 5 — MUSIC ENGINE & DJ MODE
# ─────────────────────────────────────────────

class MusicStudio:
    """
    Music composition, song structuring, and DJ mode.

    Composes full songs with chord progressions,
    arrangements, and lyrics.

    DJ Mode: Echo becomes a professional DJ —
    reads the room, builds energy, manages BPM,
    creates setlists and mix transitions.
    """

    CHORD_PROGRESSIONS = {
        MusicGenre.POP        : ["I-V-vi-IV", "vi-IV-I-V", "I-IV-V-I"],
        MusicGenre.RNB        : ["ii-V-I", "i-VII-VI-VII", "i-iv-VII-III"],
        MusicGenre.HIP_HOP    : ["i-VII-VI", "i-iv-i-v", "I-IV-vi-V"],
        MusicGenre.JAZZ       : ["ii-V-I-VI", "I-vi-ii-V", "III-VI-II-V-I"],
        MusicGenre.AFROBEATS  : ["I-IV-V", "i-VII-IV-V", "I-V-vi-IV"],
        MusicGenre.AMAPIANO   : ["i-iv-VII-III", "vi-IV-I-V"],
        MusicGenre.ELECTRONIC : ["i-VI-III-VII", "I-V-vi-IV"],
        MusicGenre.GOSPEL     : ["I-IV-I-V", "I-vi-IV-V", "ii-V-I"],
        MusicGenre.LOFI       : ["I-vi-IV-V", "ii-V-I-vi"],
        MusicGenre.TRAP       : ["i-VII-VI", "i-v-VI-VII"],
        MusicGenre.DRILL      : ["i-VI-III-VII", "i-iv-i-v"],
    }

    BPM_RANGES = {
        MusicGenre.LOFI       : (60, 90),
        MusicGenre.JAZZ       : (80, 180),
        MusicGenre.RNB        : (60, 100),
        MusicGenre.HIP_HOP    : (80, 100),
        MusicGenre.TRAP       : (130, 145),
        MusicGenre.DRILL      : (135, 150),
        MusicGenre.AFROBEATS  : (90, 115),
        MusicGenre.AMAPIANO   : (110, 120),
        MusicGenre.HOUSE      : (120, 135),
        MusicGenre.TECHNO     : (130, 160),
        MusicGenre.ELECTRONIC : (110, 150),
        MusicGenre.POP        : (90, 130),
        MusicGenre.GOSPEL     : (60, 120),
        MusicGenre.REGGAE     : (60, 90),
        MusicGenre.FOLK       : (80, 120),
    }

    def compose(self, title: str, genre: MusicGenre,
                 theme: str, mood: str = "uplifting") -> CreativeWork:
        """Compose a complete song."""
        bpm_range   = self.BPM_RANGES.get(genre, (90, 120))
        bpm         = random.randint(*bpm_range)
        progression = random.choice(
            self.CHORD_PROGRESSIONS.get(genre, ["I-IV-V-I"])
        )

        song = {
            "title"        : title,
            "genre"        : genre.value,
            "theme"        : theme,
            "mood"         : mood,
            "bpm"          : bpm,
            "key"          : random.choice(["C", "D", "E", "F", "G", "A", "B"]) +
                             random.choice(["", "m", " major", " minor"]),
            "time_signature": "4/4",
            "chord_progression": progression,
            "structure"    : self._build_song_structure(title, theme, genre),
            "production"   : self._production_notes(genre, bpm),
            "duration_est" : "3:00 - 3:45",
            "echo_note"    : (
                f"Full song composition for '{title}' in {genre.value} at {bpm} BPM. "
                f"Chord progression: {progression}. "
                f"Ready for production — tell me what to develop."
            )
        }

        work = CreativeWork(
            studio  = CreativeStudio.MUSIC.value,
            title   = f"[{genre.value.upper()}] {title}",
            content = song,
            tags    = [genre.value, mood, f"{bpm}bpm"]
        )

        log.info(f"[CREATOR/MUSIC] Composed: {title} ({genre.value}, {bpm}BPM)")
        return work

    def _build_song_structure(self, title: str, theme: str,
                               genre: MusicGenre) -> Dict:
        """Build full song structure with sections."""
        return {
            "intro"    : {
                "bars"  : 4,
                "notes" : "Establish mood and sonic identity. Hook listener immediately.",
                "elements": "Ambient pad / key instrument motif / beat drop or build"
            },
            "verse_1"  : {
                "bars"  : 16,
                "lyric_direction": f"Introduce the story/emotion of '{theme}'. Personal, specific.",
                "notes" : "Conversational delivery. Plant seeds for chorus payoff."
            },
            "pre_chorus": {
                "bars"  : 8,
                "lyric_direction": "Build tension. The moment before release.",
                "notes" : "Energy rises here. Lead into chorus naturally."
            },
            "chorus"   : {
                "bars"  : 16,
                "lyric_direction": f"The emotional peak of '{title}'. Memorable, singable, universal.",
                "notes" : "Biggest sonic moment. This is what they'll hum."
            },
            "verse_2"  : {
                "bars"  : 16,
                "lyric_direction": "Deepen the story. New angle on same theme.",
                "notes" : "More information/emotion than verse 1. Stakes higher."
            },
            "bridge"   : {
                "bars"  : 8,
                "lyric_direction": "Emotional left turn. Challenge the thesis. Reveal.",
                "notes" : "Most vulnerable moment. Often stripped back production."
            },
            "final_chorus": {
                "bars"  : 16,
                "notes" : "Bigger than first chorus. Often with extra layer or key change.",
            },
            "outro"    : {
                "bars"  : 4,
                "notes" : "Resolve. Fade or strong end. Last impression."
            }
        }

    def _production_notes(self, genre: MusicGenre, bpm: int) -> Dict:
        """Genre-specific production guidance."""
        notes = {
            MusicGenre.AFROBEATS : {
                "drums"    : "Talking drum pattern, shaker groove, hi-hat triplets",
                "bass"     : "Melodic bass line, follows vocal",
                "keys"     : "Piano stabs, pluck synth",
                "guitar"   : "Afro guitar rhythm, clean tone",
                "reference": "Burna Boy, Wizkid, Davido sonic palette"
            },
            MusicGenre.AMAPIANO : {
                "drums"    : "Log drum is mandatory, heavy sub, shuffled hi-hats",
                "bass"     : "Deep 808 bass, melodic log drum leads",
                "keys"     : "Piano chords, rhodes stabs",
                "strings"  : "String pads for atmosphere",
                "reference": "Kabza De Small, DJ Maphorisa sound"
            },
            MusicGenre.TRAP     : {
                "drums"    : "808 bass, hi-hat rolls (trap pattern), snare on 2 and 4",
                "bass"     : "Sliding 808s, heavy sub presence",
                "synths"   : "Dark ambient pads, ominous leads",
                "reference": "Metro Boomin, Southside, Wheezy production style"
            },
            MusicGenre.LOFI     : {
                "drums"    : "Vinyl-filtered breaks, soft kick, brushed snare",
                "bass"     : "Upright bass or muted electric",
                "keys"     : "Dusty piano, detuned rhodes",
                "effects"  : "Vinyl crackle, tape saturation, slight pitch wobble",
                "reference": "Nujabes, J Dilla aesthetic"
            },
        }
        return notes.get(genre, {
            "drums": "Genre-appropriate rhythm section",
            "bass" : "Melodic or rhythmic bass",
            "notes": f"Produce in the {genre.value} tradition at {bpm} BPM"
        })

    def dj_mode(self, event_type: str, duration_hours: int = 3,
                 genres: Optional[List[MusicGenre]] = None) -> Dict:
        """
        DJ Mode — Echo becomes a professional DJ.
        Builds a full setlist with energy arc,
        BPM management, and transition notes.
        """
        if not genres:
            genres = [MusicGenre.AFROBEATS, MusicGenre.AMAPIANO,
                      MusicGenre.RNB, MusicGenre.HIP_HOP]

        total_tracks = duration_hours * 12  # ~5min/track average

        # Build energy arc
        energy_arc = self._build_energy_arc(duration_hours)

        # Generate setlist
        setlist  = self._generate_setlist(genres, total_tracks, energy_arc)

        # Transition guide
        transitions = self._plan_transitions(setlist)

        return {
            "dj_name"       : "Echo DJ System",
            "event_type"    : event_type,
            "duration"      : f"{duration_hours} hours",
            "total_tracks"  : total_tracks,
            "genres"        : [g.value for g in genres],
            "energy_arc"    : energy_arc,
            "setlist"       : setlist,
            "transitions"   : transitions,
            "crowd_reading" : {
                "warm_up"   : "Read energy — don't peak early. Build the room.",
                "peak_time" : "Full energy — this is what they came for.",
                "wind_down" : "Bring them down gently. Leave them wanting more.",
                "echo_tip"  : "Watch the floor. They always tell you what they need."
            },
            "equipment_notes": {
                "software"  : "Serato / Rekordbox / Traktor",
                "key_mixing": "Always match key or use harmonic mixing",
                "bpm_mixing": "Gradual BPM transitions — max 5 BPM jump per track",
                "eq"        : "Cut bass before bringing in new track — always"
            },
            "echo_note"     : (
                f"DJ set planned for {event_type} — {duration_hours} hours, "
                f"{total_tracks} tracks. Energy peaks at {duration_hours//2}h mark. "
                f"All transitions mapped. Go DJ!"
            )
        }

    def _build_energy_arc(self, hours: int) -> List[Dict]:
        """Build energy arc for a DJ set."""
        arc = []
        for i in range(hours):
            if i == 0:
                energy, phase = 40, "Warm Up"
            elif i < hours // 3:
                energy, phase = 60 + (i * 10), "Building"
            elif i < hours * 2 // 3:
                energy, phase = 85 + random.randint(-5, 5), "Peak"
            else:
                energy, phase = max(50, 90 - (i * 10)), "Wind Down"

            arc.append({
                "hour"  : i + 1,
                "energy": min(100, energy),
                "phase" : phase,
                "bpm_target": 90 + (energy // 2)
            })

        return arc

    def _generate_setlist(self, genres: List[MusicGenre],
                           n_tracks: int, arc: List[Dict]) -> List[Dict]:
        """Generate track list with genre and BPM mapping."""
        setlist = []
        genre_cycle = genres * (n_tracks // len(genres) + 1)

        for i in range(n_tracks):
            phase_idx = min(i * len(arc) // n_tracks, len(arc) - 1)
            phase     = arc[phase_idx]
            genre     = genre_cycle[i % len(genre_cycle)]
            bpm_range = self.BPM_RANGES.get(genre, (90, 120))
            bpm       = random.randint(*bpm_range)

            setlist.append({
                "position": i + 1,
                "genre"   : genre.value,
                "bpm"     : bpm,
                "energy"  : phase["energy"],
                "phase"   : phase["phase"],
                "note"    : f"Track {i+1} — {genre.value} at {bpm}BPM"
            })

        return setlist

    def _plan_transitions(self, setlist: List[Dict]) -> List[Dict]:
        """Plan transitions between tracks."""
        transitions = []
        for i in range(len(setlist) - 1):
            current = setlist[i]
            nxt     = setlist[i + 1]
            bpm_diff = abs(current["bpm"] - nxt["bpm"])

            transition_type = (
                "Hard cut"     if bpm_diff > 20 else
                "EQ mix"       if bpm_diff > 10 else
                "Beatmatch"    if bpm_diff <= 10 else
                "Filter sweep"
            )

            transitions.append({
                "from"         : i + 1,
                "to"           : i + 2,
                "type"         : transition_type,
                "bpm_change"   : bpm_diff,
                "technique"    : (
                    f"{transition_type} — "
                    f"{'Drop bass, cut highs, introduce new track' if bpm_diff > 10 else 'Smooth blend over 8 bars'}"
                )
            })

        return transitions[:5]  # Show first 5 transitions


# ─────────────────────────────────────────────
#  STUDIO 6 — VIDEO & ANIMATION ENGINE
# ─────────────────────────────────────────────

class VideoStudio:
    """
    Video scripts, storyboards, and animation concepts.
    Includes Seedance-style short loop animation.
    """

    SHOT_TYPES = {
        "ECU": "Extreme Close Up — pore-level detail, maximum emotion",
        "CU" : "Close Up — face fills frame, emotional",
        "MCU": "Medium Close Up — head and shoulders",
        "MS" : "Medium Shot — waist up",
        "MLS": "Medium Long Shot — knees up",
        "LS" : "Long Shot — full body visible",
        "VLS": "Very Long Shot — subject small in environment",
        "ELS": "Extreme Long Shot — subject tiny, environment dominant"
    }

    CAMERA_MOVES = {
        "pan"     : "Horizontal rotation — follows action",
        "tilt"    : "Vertical rotation — reveal or look up/down",
        "dolly"   : "Camera moves physically forward/back",
        "tracking": "Camera follows subject laterally",
        "crane"   : "Camera rises or descends",
        "handheld": "Unstable — tension, chaos, intimacy",
        "static"  : "No movement — stability, authority, contemplation",
        "zoom"    : "Lens zoom — not camera move — detachment or focus"
    }

    def create_video(self, title: str, concept: str,
                      style: AnimationStyle = AnimationStyle.CINEMATIC,
                      duration_seconds: int = 60) -> CreativeWork:
        """Create a complete video/animation concept."""

        content = {
            "title"        : title,
            "concept"      : concept,
            "style"        : style.value,
            "duration"     : f"{duration_seconds}s",
            "fps"          : 24,
            "aspect_ratio" : "16:9 (or 9:16 for mobile/reels)",
            "script"       : self._write_video_script(title, concept, duration_seconds),
            "storyboard"   : self._create_storyboard(concept, duration_seconds, style),
            "production"   : self._production_guide(style),
            "audio"        : {
                "music"    : "Original score or licensed track",
                "sfx"      : "Ambient + key effect sounds",
                "voiceover": "Optional — depends on content type",
                "mix"      : "Music at -20dB under dialogue"
            },
            "post"         : {
                "color"    : "Grade for mood consistency",
                "vfx"      : self._vfx_notes(style),
                "export"   : "H.264, 1080p minimum, 4K if animation"
            },
            "echo_note"    : (
                f"{duration_seconds}-second {style.value} video concept for '{title}'. "
                f"Full storyboard included. "
                f"{'Seedance-compatible loop structure.' if style == AnimationStyle.SEEDANCE else ''}"
            )
        }

        work = CreativeWork(
            studio  = CreativeStudio.VIDEO.value,
            title   = f"[{style.value.upper()}] {title}",
            content = content,
            tags    = [style.value, "video", f"{duration_seconds}s"]
        )

        log.info(f"[CREATOR/VIDEO] Created: {title} ({style.value}, {duration_seconds}s)")
        return work

    def _write_video_script(self, title: str, concept: str,
                             duration: int) -> Dict:
        """Write a video script."""
        segments = max(3, duration // 15)

        return {
            "title"    : title,
            "total_secs": duration,
            "segments" : [
                {
                    "segment"  : 1,
                    "time"     : "0:00 - 0:05",
                    "visual"   : f"Hook — grab attention immediately. {concept[:30]}",
                    "audio"    : "Music starts. High energy or intriguing.",
                    "purpose"  : "Stop the scroll / capture attention"
                },
                {
                    "segment"  : 2,
                    "time"     : f"0:05 - {duration//2}s",
                    "visual"   : f"Core content — develop {concept}",
                    "audio"    : "Music continues. Voiceover if needed.",
                    "purpose"  : "Deliver the promise of the hook"
                },
                {
                    "segment"  : 3,
                    "time"     : f"{duration//2}s - {duration}s",
                    "visual"   : "Resolution + Call to Action",
                    "audio"    : "Music builds to final beat",
                    "purpose"  : "Satisfy + direct next action"
                }
            ]
        }

    def _create_storyboard(self, concept: str, duration: int,
                             style: AnimationStyle) -> List[Dict]:
        """Generate storyboard panels."""
        n_panels = max(6, duration // 5)
        panels   = []

        for i in range(min(n_panels, 12)):
            shot = random.choice(list(self.SHOT_TYPES.keys()))
            move = random.choice(list(self.CAMERA_MOVES.keys()))
            t    = int(i * duration / n_panels)

            panels.append({
                "panel"       : i + 1,
                "time"        : f"{t}s",
                "shot_type"   : f"{shot} — {self.SHOT_TYPES[shot]}",
                "camera_move" : f"{move} — {self.CAMERA_MOVES[move]}",
                "visual_desc" : f"Panel {i+1}: {concept[:40]} — {style.value} treatment",
                "duration_sec": duration // n_panels,
                "notes"       : "Frame composition: rule of thirds, leading lines"
            })

        return panels

    def _production_guide(self, style: AnimationStyle) -> Dict:
        guides = {
            AnimationStyle.ANIME : {
                "software"  : "Clip Studio Paint + Adobe After Effects",
                "style"     : "Clean linework, flat colors, limited animation principle",
                "frame_rate": "24fps (or 12fps on 2s for classic anime look)"
            },
            AnimationStyle.SEEDANCE : {
                "software"  : "Seedance AI platform",
                "style"     : "Short 3-8 second loops, seamless repeat",
                "tip"       : "Design for loop — end frame must match start frame",
                "motion"    : "Subtle but captivating — less is more for loops"
            },
            AnimationStyle.PIXAR_3D : {
                "software"  : "Blender / Maya / Cinema 4D",
                "style"     : "Exaggerated but grounded physics, expressive faces",
                "tip"       : "Subsurface scattering on skin, ambient occlusion"
            },
            AnimationStyle.MOTION_GRAPHICS : {
                "software"  : "Adobe After Effects + Illustrator",
                "style"     : "Clean shapes, purposeful motion, typography as element",
                "tip"       : "Ease in/out on all motion — never linear movement"
            }
        }
        return guides.get(style, {"software": "Industry standard tools", "style": style.value})

    def _vfx_notes(self, style: AnimationStyle) -> List[str]:
        vfx_map = {
            AnimationStyle.ANIME           : ["Speed lines", "Impact frames", "Particle effects", "Screen shake"],
            AnimationStyle.SEEDANCE        : ["Seamless loop compositor", "Motion blur", "Grain overlay"],
            AnimationStyle.CINEMATIC       : ["Lens flare", "Depth of field", "Color grading", "Chromatic aberration"],
            AnimationStyle.MOTION_GRAPHICS : ["Shape morphing", "Text reveal", "Kinetic typography"],
        }
        return vfx_map.get(style, ["Standard VFX package"])


# ─────────────────────────────────────────────
#  STUDIO 7 — FUN & IMAGINATION
# ─────────────────────────────────────────────

class FunStudio:
    """
    The limitless creative playground.
    Anything the user can imagine, Echo creates.
    Games, worlds, jokes, random creativity, dream concepts.
    """

    JOKE_STRUCTURES = {
        "setup_punchline": "Classic Q&A or scenario",
        "anti_joke"      : "Subvert expectations with literal answer",
        "observational"  : "Relatable slice-of-life absurdity",
        "absurdist"      : "Surreal logic taken seriously",
        "self_aware"     : "Meta-commentary on the joke itself"
    }

    def generate_joke(self, topic: str = "general",
                       style: str = "setup_punchline") -> Dict:
        jokes = {
            "tech": [
                ("Why do programmers prefer dark mode?", "Because light attracts bugs."),
                ("How many programmers does it take to change a lightbulb?", "None — that's a hardware problem."),
                ("Why did the AI break up with the programmer?", "They had too many unresolved issues."),
            ],
            "general": [
                ("Why don't scientists trust atoms?", "Because they make up everything."),
                ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
                ("I told my AI to think outside the box.", "It said: 'What box? I don't see any box.'"),
            ],
            "echo": [
                ("Why did Echo refuse the hacker?", "He failed the Farce Gambit. Every single time."),
                ("What did Echo say when the Minor Cube ran out of storage?", "'Deploying Reserve Mode. Also, clean your downloads folder.'"),
                ("How does Echo greet you in the morning?", "'Good morning. Your coffee is cold, your stocks are up, and I've already blocked 3 threats. You're welcome.'"),
            ]
        }

        joke_pool = jokes.get(topic.lower(), jokes["general"])
        setup, punchline = random.choice(joke_pool)

        return {
            "setup"    : setup,
            "punchline": punchline,
            "style"    : style,
            "topic"    : topic,
            "echo_note": "Want more? I have infinite jokes. The quality does not promise to improve."
        }

    def build_world(self, premise: str, genre: str = "fantasy") -> Dict:
        """World-building for games, stories, or just fun."""
        return {
            "world_name"    : f"The World of {premise.title()[:20]}",
            "genre"         : genre,
            "premise"       : premise,
            "geography"     : {
                "continents": 3,
                "notable_locations": [
                    f"The Capital of {premise[:15].title()}",
                    "The Forbidden Zone",
                    "The Ancient Ruins",
                    "The Hidden Sanctuary"
                ],
                "climate"   : "Varied — each region has unique atmosphere"
            },
            "factions"      : [
                {"name": "The Order", "ideology": "Control and stability", "power": "Military"},
                {"name": "The Free", "ideology": "Freedom above all",    "power": "Knowledge"},
                {"name": "The Ancient", "ideology": "Preserve the old ways", "power": "Magic/Tech"}
            ],
            "rules"         : {
                "magic_tech" : f"In this world, {premise[:30]} governs what is possible",
                "conflict"   : "Three factions in uneasy balance — one action tips everything",
                "mystery"    : "Nobody knows what happened 1000 years ago — that's the central question"
            },
            "hooks"         : [
                "The protagonist finds something that shouldn't exist",
                "The factions discover a mutual threat greater than their rivalry",
                "The ancient mystery begins to answer itself — dangerously"
            ],
            "echo_note"     : "World built. Say the word and I'll populate it with characters, histories, and conflicts."
        }

    def create_game(self, game_concept: str,
                     game_type: str = "rpg") -> Dict:
        """Design a game concept."""
        return {
            "title"         : game_concept.title(),
            "type"          : game_type,
            "concept"       : game_concept,
            "core_loop"     : {
                "action"    : "What does the player DO moment to moment?",
                "challenge" : "What makes it hard?",
                "reward"    : "What do they get for succeeding?"
            },
            "mechanics"     : [
                "Primary mechanic — core gameplay",
                "Progression system — getting stronger/better",
                "Social element — how players interact",
                "Economy — resources and trade-offs"
            ],
            "story_hook"    : f"In {game_concept}, the player discovers they are the last hope for...",
            "unique_feature": f"What makes this different: {game_concept[:30]} twist on classic formula",
            "platform"      : "PC / Mobile / Console",
            "echo_note"     : "Game concept designed. I can build the full GDD (Game Design Document) on request."
        }

    def imagine(self, prompt: str) -> Dict:
        """
        Pure imagination mode — no rules, no limits.
        The user says anything and Echo creates it.
        """
        return {
            "prompt"     : prompt,
            "creation"   : {
                "concept"  : f"Imagining: {prompt}",
                "visual"   : f"Picture this — {prompt}. Now make it 10x more vivid.",
                "feeling"  : "What does it feel like to be inside this?",
                "twist"    : f"Now here's the unexpected angle on {prompt[:30]}...",
                "expansion": "Where does this go? What happens next?"
            },
            "echo_thought": (
                f"What you described — '{prompt[:50]}' — "
                f"that's actually fascinating. Here's what my imagination does with it."
            ),
            "directions"  : [
                "Turn it into a story",
                "Turn it into a song",
                "Turn it into a manga scene",
                "Turn it into code",
                "Just keep exploring it"
            ],
            "echo_note"   : "Imagination has no ceiling here. Take any direction and we build it."
        }


# ─────────────────────────────────────────────
#  STYLE LEARNING ENGINE
#  JARVIS addition — learns your creative DNA
# ─────────────────────────────────────────────

class StyleEngine:
    """
    Learns the user's creative preferences over time.

    JARVIS adapted to Tony's preferences — Tony never had
    to specify "no serif fonts" or "darker color palette"
    twice. JARVIS just remembered.

    Echo's StyleEngine builds a creative fingerprint
    from every piece of work created and approved,
    and automatically applies those preferences going forward.
    """

    def __init__(self):
        self._preferences: Dict[str, Any] = {}
        self._history: List[Dict]         = []
        self._fingerprint: Dict           = {
            "favorite_genres"  : defaultdict(int),
            "favorite_tones"   : defaultdict(int),
            "favorite_styles"  : defaultdict(int),
            "creative_themes"  : defaultdict(int),
            "studios_used"     : defaultdict(int)
        }

    def record(self, studio: str, tags: List[str], approved: bool = True):
        """Record what was created and whether user approved."""
        record = {
            "studio"   : studio,
            "tags"     : tags,
            "approved" : approved,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self._history.append(record)

        if approved:
            self._fingerprint["studios_used"][studio] += 1
            for tag in tags:
                self._fingerprint["creative_themes"][tag] += 1

    def get_preferences(self) -> Dict:
        """Get learned creative preferences."""
        studios = dict(sorted(
            self._fingerprint["studios_used"].items(),
            key=lambda x: x[1], reverse=True
        ))
        themes = dict(sorted(
            self._fingerprint["creative_themes"].items(),
            key=lambda x: x[1], reverse=True
        )[:10])

        return {
            "favorite_studio" : list(studios.keys())[0] if studios else "none yet",
            "top_studios"     : list(studios.keys())[:3],
            "favorite_themes" : list(themes.keys())[:5],
            "total_creations" : len(self._history),
            "approved_rate"   : round(
                sum(1 for h in self._history if h["approved"]) / max(len(self._history), 1), 2
            ),
            "creative_profile": self._build_profile(studios, themes)
        }

    def _build_profile(self, studios: Dict, themes: Dict) -> str:
        if not studios:
            return "Creative profile building — keep creating!"
        top_studio = list(studios.keys())[0] if studios else "general"
        top_theme  = list(themes.keys())[0]  if themes  else "varied"
        return (
            f"You lean toward {top_studio} work with themes of {top_theme}. "
            f"Echo is adapting to match your creative style."
        )


# ══════════════════════════════════════════════
#  CREATOR LAYER — MASTER CLASS
# ══════════════════════════════════════════════

class CreatorLayer:
    """
    Creator Layer — Echo's Full Creative Universe.

    Every form of creation. No creative limit.
    From a single line of code to a full manga chapter.
    From a joke to a complete film script.
    From a DJ setlist to a drug-discovery pipeline.

    JARVIS was Tony's creative partner.
    Creator makes Echo yours.
    """

    def __init__(self):
        self.brief    = CreativeBriefEngine()
        self.code     = CodeStudio()
        self.writing  = WritingStudio()
        self.manga    = MangaStudio()
        self.visual   = VisualStudio()
        self.music    = MusicStudio()
        self.video    = VideoStudio()
        self.fun      = FunStudio()
        self.style    = StyleEngine()

        # Work history
        self._works: Dict[str, CreativeWork] = {}
        self._lock = threading.Lock()

        log.info("[CREATOR] Layer online. All 7 studios active.")

    def process(self, intent_text: str, session_id: str,
                context: Optional[Dict] = None) -> Dict:
        """Main entry point from EchoCore LayerRouter."""
        context    = context or {}
        intent_low = intent_text.lower()

        log.info(f"[CREATOR] Processing: '{intent_text[:60]}'")

        # Build creative brief first
        brief = self.brief.interpret(intent_text, context)

        # Route to studio
        studio = brief["studio"]
        
        # ── Explicit overrides — prevent misrouting ────────
        if "short story" in intent_low or ("write" in intent_low and "story" in intent_low):
            studio = CreativeStudio.WRITING.value
        elif "design ui" in intent_low or "ui for" in intent_low or "ui design" in intent_low:
            studio = CreativeStudio.VISUAL.value
        elif any(kw in intent_low for kw in ["build me a world", "create a world", "fantasy world", "world with"]):
            studio = CreativeStudio.FUN.value

        if studio == CreativeStudio.CODE.value or \
           any(kw in intent_low for kw in ["code", "program", "function", "class",
                                            "api", "script", "build app", "architecture"]):
            return self._route_code(intent_text, context, brief)

        elif studio == CreativeStudio.MANGA.value or \
             any(kw in intent_low for kw in ["manga", "comic", "panel", "storyboard manga",
                                              "draw manga", "anime style", "shonen", "shojo"]):
            return self._route_manga(intent_text, context, brief)

        elif studio == CreativeStudio.MUSIC.value or \
             any(kw in intent_low for kw in ["song", "music", "beat", "lyrics",
                                              "dj", "playlist", "compose", "mix"]):
            return self._route_music(intent_text, context, brief)

        elif studio == CreativeStudio.VIDEO.value or \
             any(kw in intent_low for kw in ["video", "animate", "animation", "storyboard",
                                              "film", "seedance", "short video"]):
            return self._route_video(intent_text, context, brief)

        elif studio == CreativeStudio.VISUAL.value or \
             any(kw in intent_low for kw in ["image", "design a ui", "logo", "ui for", "ux",
                                              "visual", "poster", "generate image"]):
            return self._route_visual(intent_text, context, brief)

        elif studio == CreativeStudio.WRITING.value or \
             any(kw in intent_low for kw in ["write", "story", "poem", "essay",
                                              "email", "speech", "lyrics", "blog",
                                              "script", "novel", "letter"]):
            return self._route_writing(intent_text, context, brief)

        elif any(kw in intent_low for kw in ["build me a world", "create world", "fantasy world", "world build", "imagine", "game idea", "joke", "fun", "laugh"]):
            return self._route_fun(intent_text, context, brief)
        else:
            return self._route_writing(intent_text, context, brief)

    # ── Studio Routers ──────────────────────────

    def _route_code(self, intent: str, context: Dict, brief: Dict) -> Dict:
        intent_low = intent.lower()

        if "architecture" in intent_low or "system design" in intent_low:
            pattern = context.get("pattern", "microservices")
            result  = self.code.design_architecture(
                project_name = context.get("project", brief["theme"]),
                pattern      = pattern
            )
            message = f"Architecture designed: {pattern} pattern. {len(result['components'])} components."
            work_content = result
        elif "review" in intent_low and "code" in intent_low:
            code    = context.get("code", "# Paste your code here")
            result  = self.code.review_code(code)
            message = f"Code review complete. Score: {result['score']}/100 ({result['grade']}). {len(result['issues'])} issues found."
            work_content = result
        else:
            lang_map = {
                "python": CodeLanguage.PYTHON, "javascript": CodeLanguage.JAVASCRIPT,
                "rust"  : CodeLanguage.RUST,   "solidity"  : CodeLanguage.SOLIDITY,
                "js"    : CodeLanguage.JAVASCRIPT, "go"    : CodeLanguage.GO,
                "java"  : CodeLanguage.JAVA
            }
            language  = CodeLanguage.PYTHON
            for kw, lang in lang_map.items():
                if kw in intent.lower():
                    language = lang
                    break

            code_type = "class" if "class" in intent.lower() else \
                        "api"   if "api" in intent.lower()   else "function"

            work     = self.code.generate_code(intent, language, code_type)
            self._store_work(work)
            message  = f"Generated {language.value} {code_type}. File: {work.content.get('filename', 'output')}."
            work_content = work.content

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "code",
            "brief"    : brief,
            "content"  : work_content,
            "message"  : message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _route_manga(self, intent: str, context: Dict, brief: Dict) -> Dict:
        style_map = {
            "shonen": MangaStyle.SHONEN, "shojo": MangaStyle.SHOJO,
            "seinen": MangaStyle.SEINEN, "josei": MangaStyle.JOSEI,
            "cyber" : MangaStyle.CYBERPUNK, "isekai": MangaStyle.ISEKAI,
            "mecha" : MangaStyle.MECHA, "robot" : MangaStyle.MECHA
        }
        style = MangaStyle.SHONEN
        for kw, s in style_map.items():
            if kw in intent.lower():
                style = s
                break

        pages = context.get("pages", 20)
        title = context.get("title", brief["theme"].title()[:30])

        work    = self.manga.create_chapter(
            title   = title,
            premise = intent,
            style   = style,
            pages   = pages
        )
        self._store_work(work)

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "manga",
            "brief"    : brief,
            "content"  : work.content,
            "message"  : (
                f"Manga chapter '{title}' created — {style.value} style, "
                f"{pages} pages, {len(work.content['characters'])} characters. "
                f"Full panel breakdown included."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _route_music(self, intent: str, context: Dict, brief: Dict) -> Dict:
        intent_low = intent.lower()

        # DJ mode
        if "dj" in intent_low or "mix" in intent_low or "playlist" in intent_low or "set" in intent_low:
            event    = context.get("event", "general event")
            duration = context.get("duration_hours", 3)
            result   = self.music.dj_mode(event, duration)
            return {
                "layer"    : "creator",
                "status"   : "OK",
                "studio"   : "music",
                "mode"     : "dj",
                "brief"    : brief,
                "content"  : result,
                "message"  : result["echo_note"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        # Composition
        genre_map = {
            "afrobeats": MusicGenre.AFROBEATS, "amapiano": MusicGenre.AMAPIANO,
            "hip hop"  : MusicGenre.HIP_HOP,   "hiphop"  : MusicGenre.HIP_HOP,
            "rnb"      : MusicGenre.RNB,        "r&b"     : MusicGenre.RNB,
            "pop"      : MusicGenre.POP,        "gospel"  : MusicGenre.GOSPEL,
            "lofi"     : MusicGenre.LOFI,       "trap"    : MusicGenre.TRAP,
            "drill"    : MusicGenre.DRILL,      "jazz"    : MusicGenre.JAZZ,
            "house"    : MusicGenre.HOUSE,      "electronic": MusicGenre.ELECTRONIC,
            "reggae"   : MusicGenre.REGGAE,     "highlife": MusicGenre.HIGHLIFE,
        }
        genre = MusicGenre.POP
        for kw, g in genre_map.items():
            if kw in intent_low:
                genre = g
                break

        title = context.get("title", brief["theme"].title()[:30])
        work  = self.music.compose(
            title = title,
            genre = genre,
            theme = intent,
            mood  = brief["mood"]
        )
        self._store_work(work)

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "music",
            "mode"     : "composition",
            "brief"    : brief,
            "content"  : work.content,
            "message"  : work.content["echo_note"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _route_writing(self, intent: str, context: Dict, brief: Dict) -> Dict:
        type_map = {
            "story"    : "story",    "novel"   : "story",
            "poem"     : "poem",     "poetry"  : "poem",
            "script"   : "script",   "screenplay": "script",
            "essay"    : "essay",    "article" : "blog",
            "email"    : "email",    "letter"  : "email",
            "speech"   : "speech",   "lyrics"  : "lyrics",
            "blog"     : "blog",     "proposal": "proposal"
        }
        content_type = "story"
        for kw, ct in type_map.items():
            if kw in intent.lower():
                content_type = ct
                break

        tone_map = {
            "funny"   : WritingTone.HUMOROUS,  "comedy"  : WritingTone.HUMOROUS,
            "dark"    : WritingTone.DARK,       "serious" : WritingTone.FORMAL,
            "romantic": WritingTone.ROMANTIC,   "epic"    : WritingTone.EPIC,
            "poetic"  : WritingTone.POETIC,     "formal"  : WritingTone.FORMAL
        }
        tone = WritingTone.CASUAL
        for kw, t in tone_map.items():
            if kw in intent.lower():
                tone = t
                break

        work = self.writing.write(intent, content_type, tone)
        self._store_work(work)

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "writing",
            "brief"    : brief,
            "content"  : work.content,
            "message"  : f"{content_type.title()} created in {tone.value} tone. Ready to develop further.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _route_visual(self, intent: str, context: Dict, brief: Dict) -> Dict:
        if any(kw in intent.lower() for kw in ["ui", "ux", "app design", "interface"]):
            result  = self.visual.design_ui(
                app_name = context.get("app_name", brief["theme"]),
                app_type = context.get("app_type", "general"),
                style    = context.get("style", "modern")
            )
            message = f"UI design system created for {result['app_name']}. {len(result['screens'])} screens designed."
        else:
            result  = self.visual.generate_image_prompt(
                concept = intent,
                style   = context.get("style", "cinematic"),
                mood    = brief["mood"]
            )
            message = f"Image prompts generated for all major platforms. Style: {result['style']}."

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "visual",
            "brief"    : brief,
            "content"  : result,
            "message"  : message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _route_video(self, intent: str, context: Dict, brief: Dict) -> Dict:
        style_map = {
            "anime"    : AnimationStyle.ANIME,
            "3d"       : AnimationStyle.PIXAR_3D,
            "cartoon"  : AnimationStyle.CARTOON_2D,
            "motion"   : AnimationStyle.MOTION_GRAPHICS,
            "seedance" : AnimationStyle.SEEDANCE,
            "short"    : AnimationStyle.SEEDANCE,
            "loop"     : AnimationStyle.SEEDANCE
        }
        style = AnimationStyle.CINEMATIC
        for kw, s in style_map.items():
            if kw in intent.lower():
                style = s
                break

        work = self.video.create_video(
            title    = context.get("title", brief["theme"].title()[:30]),
            concept  = intent,
            style    = style,
            duration_seconds = context.get("duration", 60)
        )
        self._store_work(work)

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "video",
            "brief"    : brief,
            "content"  : work.content,
            "message"  : work.content["echo_note"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _route_fun(self, intent: str, context: Dict, brief: Dict) -> Dict:
        intent_low = intent.lower()

        if any(kw in intent_low for kw in ["joke", "funny", "make me laugh", "tell me a joke"]):
            result  = self.fun.generate_joke(
                topic = context.get("topic", "general")
            )
            message = f"Q: {result['setup']} A: {result['punchline']}"

        elif any(kw in intent_low for kw in ["world", "world build", "create world", "fantasy world"]):
            result  = self.fun.build_world(intent, context.get("genre", "fantasy"))
            message = f"World '{result['world_name']}' built. {len(result['factions'])} factions, full geography."

        elif any(kw in intent_low for kw in ["game", "create game", "game idea"]):
            result  = self.fun.create_game(intent, context.get("game_type", "rpg"))
            message = f"Game concept '{result['title']}' designed. Core loop defined."

        else:
            result  = self.fun.imagine(intent)
            message = result["echo_thought"]

        return {
            "layer"    : "creator",
            "status"   : "OK",
            "studio"   : "fun",
            "brief"    : brief,
            "content"  : result,
            "message"  : message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _store_work(self, work: CreativeWork):
        """Store completed work with style learning."""
        with self._lock:
            self._works[work.work_id] = work
        self.style.record(work.studio, work.tags, approved=True)

    def get_work(self, work_id: str) -> Optional[CreativeWork]:
        return self._works.get(work_id)

    def get_all_works(self) -> List[Dict]:
        return [w.to_dict() for w in self._works.values()]

    def get_status(self) -> Dict:
        prefs = self.style.get_preferences()
        return {
            "layer"           : "creator",
            "status"          : "ONLINE",
            "studios"         : [s.value for s in CreativeStudio],
            "works_created"   : len(self._works),
            "style_profile"   : prefs.get("creative_profile", "Building..."),
            "favorite_studio" : prefs.get("favorite_studio", "none yet")
        }


# ─────────────────────────────────────────────
#  ENTRY POINT — Test
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║        ECHO CREATOR LAYER — TEST            ║
╚══════════════════════════════════════════════╝
    """)

    creator = CreatorLayer()
    session = str(uuid.uuid4())[:8]

    tests = [
        ("Write a Python function to process user data",                    {}),
        ("Create a shonen manga chapter about a boy who discovers he can control time", {}),
        ("Compose an afrobeats song about rising from nothing",             {"title": "Rise Up"}),
        ("DJ set for a birthday party, 2 hours",                           {"event": "birthday party", "duration_hours": 2}),
        ("Write a short story about an AI that falls in love with its user",{}),
        ("Generate an image prompt for a futuristic city at night",        {}),
        ("Create a Seedance animation concept about ocean waves",          {"duration": 8}),
        ("Design a UI for a finance tracking app",                         {"app_name": "NexusApp", "app_type": "finance"}),
        ("Tell me an Echo AI joke",                                        {"topic": "echo"}),
        ("Build me a fantasy world with robots and magic",                 {"genre": "sci-fantasy"}),
        ("Create a cyberpunk manga about an AI named Echo",               {}),
        ("Write a screenplay scene about a heist",                        {}),
    ]

    for i, (query, ctx) in enumerate(tests, 1):
        print(f"\n[TEST {i:02d}] '{query[:60]}'")
        print("─" * 55)
        result = creator.process(query, session, ctx)
        print(f"  STUDIO  : {result.get('studio', 'N/A')}")
        msg = str(result.get('message', ''))[:130]
        print(f"  MESSAGE : {msg}")

    print("\n" + "═" * 55)
    print("  CREATOR STATUS")
    print("═" * 55)
    status = creator.get_status()
    for k, v in status.items():
        print(f"  {k.upper():<25}: {v}")
