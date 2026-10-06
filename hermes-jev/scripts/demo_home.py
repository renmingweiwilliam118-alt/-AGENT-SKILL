#!/usr/bin/env python3
"""Build a throwaway Hermes home of invented profiles, pools and decisions.

The README screenshot has to come from somewhere. Taken from a real machine it
publishes that fleet's profile names, paths and model strategy under a caption
claiming it is a demo, which is how the current image ended up showing a real
working pool set. This makes the demo real: run it, point the dashboard at the
result, and everything on screen is from this file.

    python3 scripts/demo_home.py /tmp/jev-demo-home
    jev dashboard --hermes-home /tmp/jev-demo-home      # or: python3 router-dashboard/server.py ...

Model ids are public OpenRouter slugs. Everything else - profile names, the pool
layout, the decisions - is invented here and belongs to no one.
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

PROFILES = {
    "default": "qwen/qwen3.8-flash",
    "creative": "google/gemini-3.8-flash",
    "ops": "qwen/qwen3.8-flash",
    "research": "x-ai/grok-4.6",
    "support": "google/gemini-3.8-flash",
}

# A pool set worth looking at: every tier specialises somewhere, `hard` has no writing
# pool so the grid shows a fall-through, and simple has no research or vision pool.
ROUTING = {
    "tiers": {
        "simple": {
            "general": ["openrouter:qwen/qwen3.8-flash", "openrouter:google/gemini-3.8-flash"],
            "coding": ["openrouter:qwen/qwen3.8-flash"],
            "writing": ["openrouter:google/gemini-3.8-flash"],
        },
        "medium": {
            "general": ["openrouter:google/gemini-3.8-flash", "openrouter:qwen/qwen3.8-flash"],
            "coding": ["openrouter:deepseek/deepseek-v4.1-flash"],
            "writing": ["openrouter:anthropic/claude-haiku-4.5"],
            "research": ["openrouter:x-ai/grok-4.6"],
            "vision": ["openrouter:google/gemini-3.8-flash"],
        },
        "hard": {
            "general": ["openrouter:moonshotai/kimi-k3"],
            "coding": ["openrouter:moonshotai/kimi-k3", "openrouter:deepseek/deepseek-v4-pro-0813"],
            "research": ["openrouter:x-ai/grok-4.6"],
            "vision": ["openrouter:google/gemini-3.8-pro"],
        },
    },
    "exclude": ["*:free", "cloudflare-ai-gateway:*"],
}

# profile, tier, specialty, model picked, model it was on, confidence, images, ms
DECISIONS = [
    ("default", "medium", "coding", "deepseek/deepseek-v4.1-flash", "qwen/qwen3.8-flash", 0.88, False, 412),
    ("ops", "simple", "general", "qwen/qwen3.8-flash", "qwen/qwen3.8-flash", 0.93, False, 336),
    ("creative", "medium", "writing", "anthropic/claude-haiku-4.5", "google/gemini-3.8-flash", 0.81, False, 468),
    ("research", "hard", "research", "x-ai/grok-4.6", "x-ai/grok-4.6", 0.76, False, 559),
    ("default", "hard", "coding", "moonshotai/kimi-k3", "qwen/qwen3.8-flash", 0.91, False, 501),
    ("support", "simple", "general", "qwen/qwen3.8-flash", "google/gemini-3.8-flash", 0.87, False, 357),
    ("creative", "medium", "vision", "google/gemini-3.8-flash", "google/gemini-3.8-flash", 0.84, True, 443),
    ("ops", "medium", "general", "google/gemini-3.8-flash", "qwen/qwen3.8-flash", 0.72, False, 389),
    ("default", "simple", "coding", "qwen/qwen3.8-flash", "qwen/qwen3.8-flash", 0.90, False, 344),
    ("research", "medium", "research", "x-ai/grok-4.6", "google/gemini-3.8-flash", 0.79, False, 522),
    ("support", "medium", "general", "google/gemini-3.8-flash", "google/gemini-3.8-flash", 0.83, False, 371),
    ("default", "medium", "general", "google/gemini-3.8-flash", "qwen/qwen3.8-flash", 0.86, False, 398),
]

STATE = {"routing": "shadow", "skills": "on", "notice": "off"}


def home_for(root: Path, profile: str) -> Path:
    return root if profile == "default" else root / "profiles" / profile


def build(root: Path, now: float) -> Path:
    if root.exists():
        shutil.rmtree(root)
    for profile, model in PROFILES.items():
        home = home_for(root, profile)
        (home / "jev").mkdir(parents=True, exist_ok=True)
        (home / "logs").mkdir(parents=True, exist_ok=True)
        (home / "config.yaml").write_text(f"agent:\n  provider: openrouter\n  model: {model}\n", encoding="utf-8")
        (home / "jev" / "state.json").write_text(json.dumps(STATE), encoding="utf-8")
    (root / "jev" / "routing.json").write_text(json.dumps(ROUTING, indent=2), encoding="utf-8")

    lines = {}
    for index, (profile, tier, specialty, model, current, confidence, images, ms) in enumerate(DECISIONS):
        # Spaced about 20 s apart so the live view shows a plausible few minutes of work.
        entry = {"ts": round(now - (len(DECISIONS) - index) * 19.4, 3), "profile": profile, "kind": "route",
                 "mode": "shadow", "from": f"openrouter:{current}", "routed": model != current,
                 "model": f"openrouter:{model}", "tier": tier, "specialty": specialty, "has_images": images,
                 "confidence": confidence, "difficulty": tier, "costly_mistake": False, "private": False,
                 "reason": "", "latency_ms": ms, "policy": "tier"}
        lines.setdefault(profile, []).append(json.dumps(entry, separators=(",", ":")))
    for profile, rows in lines.items():
        path = home_for(root, profile) / "logs" / "jev-decisions.jsonl"
        path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return root


def main(argv: list) -> int:
    root = Path(argv[0] if argv else "/tmp/jev-demo-home").expanduser()
    build(root, time.time())
    print(json.dumps({"home": str(root), "profiles": sorted(PROFILES), "decisions": len(DECISIONS),
                      "next": [f"python3 router-dashboard/server.py --hermes-home {root} --port 8794",
                               "open http://127.0.0.1:8794/ and press Live"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
