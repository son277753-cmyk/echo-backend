"""
app.py — Web entrypoint for Echo AI / PCOS prototype.

Wraps the existing EchoCore engine (all layers) in a small HTTP API and
adds two things that weren't in the original files yet:

  1. Multi-layer combination ("new entity") — EchoCore's built-in
     IntentParser only ever returns ONE top-scoring layer. This adds a
     detector that finds every layer that plausibly applies to a request
     (e.g. "create an educational website" -> CREATOR + SCHOLAR), runs
     each one for real, and treats their combined structured output as
     the "deliberation."

  2. Consensus caching + LLM synthesis — once layers have deliberated,
     a free model writes the actual final answer grounded in what they
     decided (instead of returning raw template output). The result is
     cached by (layers + normalized question), so a repeat/similar ask
     skips both steps and returns instantly — this is the "Echo gets
     faster the more Orho is used" behavior.

Sentinel's passive scan and the Asimov gate run on every request first,
exactly as in EchoCore.process().
"""

import os
import hashlib
import logging
from collections import defaultdict

import requests
from flask import Flask, request, jsonify

from echo_core import EchoCore, Layer, IntentParser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("echo_app")

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    # Manual CORS so the Vercel-hosted frontend (a different origin) can
    # call this API without needing the flask-cors package.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/api/echo", methods=["OPTIONS"])
@app.route("/api/status", methods=["OPTIONS"])
def cors_preflight():
    return "", 204

# One long-lived EchoCore instance for the life of this process — this is
# what makes the in-memory consensus cache actually work between requests.
echo = EchoCore()

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")

# The free-tier lineup on OpenRouter rotates often (sometimes within days),
# so instead of one hardcoded model, try a short list in order and fall
# back automatically if one has been pulled from the free tier. An env var
# override always goes first if set.
DEFAULT_MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "openai/gpt-oss-20b:free",
    "google/gemma-4-31b-it:free",
]


def get_model_list():
    override = os.environ.get("ECHO_MODEL")
    if override:
        return [override] + [m for m in DEFAULT_MODELS if m != override]
    return DEFAULT_MODELS

CONSENSUS_CACHE = {}

LAYER_ATTR = {
    Layer.SENTINEL: "sentinel",
    Layer.NEXUS: "nexus",
    Layer.STELLAR: "stellar",
    Layer.VITAL: "vital",
    Layer.SCHOLAR: "scholar",
    Layer.CREATOR: "creator",
    Layer.FLOW: "flow",
    Layer.HABITAT: "habitat",
    Layer.HYPER: "hyper",
}


def detect_layers(text, max_layers=3):
    """Score every layer's keywords against the input and return every
    layer within 1 point of the top score (capped at max_layers). This is
    the 'which layers form the new entity' step."""
    text_low = text.lower()
    scores = defaultdict(int)
    for layer, keywords in IntentParser.LAYER_KEYWORDS.items():
        for kw in keywords:
            if kw in text_low:
                scores[layer] += 1

    if not scores:
        return [Layer.STELLAR]

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_score = ranked[0][1]
    chosen = [layer for layer, score in ranked if score >= max(1, top_score - 1)]
    return chosen[:max_layers]


def cache_key(text, layers):
    norm = " ".join(sorted(l.value for l in layers)) + "::" + text.strip().lower()
    return hashlib.sha256(norm.encode()).hexdigest()[:16]


DEAD_MODELS = set()  # models that failed once this process — skip them on future requests


def call_llm(system_prompt, user_prompt):
    if not OPENROUTER_KEY:
        return None, "OPENROUTER_API_KEY not set on the server."

    candidates = [m for m in get_model_list() if m not in DEAD_MODELS] or get_model_list()

    last_err = None
    for model in candidates:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "HTTP-Referer": "https://pcos-prototype.vercel.app",
                    "X-Title": "PCOS/Echo Prototype",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 600,
                },
                timeout=15,
            )
            data = r.json()
            if not r.ok or "error" in data:
                last_err = (data.get("error") or {}).get("message", f"Upstream error {r.status_code}")
                log.warning("Model %s unavailable: %s", model, last_err)
                DEAD_MODELS.add(model)
                continue
            return data["choices"][0]["message"]["content"], None
        except Exception as e:
            last_err = str(e)
            log.warning("Model %s raised: %s", model, last_err)
            DEAD_MODELS.add(model)
            continue
    return None, f"All fallback models unavailable. Last error: {last_err}"


@app.route("/api/echo", methods=["POST"])
def echo_endpoint():
    body = request.get_json(force=True, silent=True) or {}
    user_input = (body.get("message") or "").strip()
    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    # ── Gate 1: Sentinel passive scan (every request, silent) ──
    threat = echo.sentinel.passive_scan(user_input, echo.session_id, {})
    if threat:
        action = threat.get("action")
        if action == "FARCE_GAMBIT_ACTIVE":
            return jsonify({
                "reply": "…",
                "layers": [],
                "cached": False,
            })
        if action not in ["MONITORING", "ELEVATED_MONITORING"]:
            return jsonify({"error": "Security check blocked this request.", "blocked": True})

    # ── Gate 2: Asimov ethics check ──
    safe, reason = echo.asimov.evaluate(user_input, {})
    if not safe:
        return jsonify({"error": reason, "blocked": True})

    # ── Which layers form the "new entity" for this request ──
    layers = detect_layers(user_input)
    key = cache_key(user_input, layers)

    cached = CONSENSUS_CACHE.get(key)
    if cached:
        return jsonify({
            "reply": cached["reply"],
            "layers": [l.value for l in layers],
            "cached": True,
        })

    # ── Run each matched layer for real — this IS the deliberation input ──
    deliberation = []
    for layer in layers:
        attr = LAYER_ATTR.get(layer)
        instance = getattr(echo, attr, None) if attr else None
        if instance and hasattr(instance, "process"):
            try:
                result = instance.process(intent_text=user_input, session_id=echo.session_id, context={})
            except Exception as e:
                log.exception("Layer %s raised", layer.value)
                result = {"status": "ERROR", "error": str(e)}
        else:
            result = {"status": "LAYER_COMING_SOON"}
        deliberation.append({"layer": layer.value, "output": result})

    layer_names = ", ".join(d["layer"].upper() for d in deliberation)
    context_summary = "\n\n".join(
        f"[{d['layer'].upper()} layer's findings]\n{str(d['output'])[:1200]}"
        for d in deliberation
    )

    system_prompt = (
        "You are Echo, the AI running on the user's Orho device (the PCOS "
        f"architecture). For this request these layers were activated: {layer_names}. "
        "Each layer already did its own structured reasoning, shown below. Synthesize "
        "their findings into one clear, complete, genuinely useful answer, as if "
        "reporting the consensus those layers just reached. Don't mention JSON, "
        "layer names, or internal system details — just answer naturally."
    )
    user_prompt = f"User asked: {user_input}\n\n{context_summary}"

    reply, err = call_llm(system_prompt, user_prompt)
    if err:
        reply = (
            f"[{layer_names} activated. Language model step unavailable: {err}]\n\n"
            + context_summary[:600]
        )

    CONSENSUS_CACHE[key] = {"reply": reply}

    return jsonify({
        "reply": reply,
        "layers": [d["layer"] for d in deliberation],
        "cached": False,
    })


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "version": echo.VERSION,
        "session": echo.session_id,
        "cache_size": len(CONSENSUS_CACHE),
        "llm_configured": bool(OPENROUTER_KEY),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
