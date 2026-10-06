#!/usr/bin/env python3
"""Reference adapter: wire `jev triage` into a pipeline that already carries real traffic.

This is the working version from a live support-mail router, genericised. Copy it next
to your own pipeline and repoint the constants below. Read
`docs/wiring-triage-into-a-live-pipeline.md` first — the four rules there are why this
file is shaped the way it is, and each one is a failure somebody already had.

The host calls three things: `mode_from_config(cfg)` and `Budget()` once per cycle, and
`classify_brief(...)` per message. The rest is plumbing you can replace.

Classify every message as it lands: work now, today, queue, or ignore.

The router already decides *whose* message this is. It does not decide how much it
matters, and the thing it uses instead — a regex over the subject line — only fires on
words like "urgent" and "down". A customer who writes "I cannot open any of today's orders" is completely stuck and matches none of them.

So each newly-seen message gets one Jev call: a five-level urgency rubric, a kind, and a
few yes/no readings. About 400-800ms and roughly six cents per thousand messages, which
is cheap enough to run on every message rather than on the ones somebody remembers to
look at.

Three rules this module exists to enforce:

  * **Fail open, always.** No key, no network, a slow answer, a bad answer — the cycle
    carries on exactly as it did before. Triage is an opinion about mail, not a
    dependency of collecting it. Every entry point here returns ``None`` rather than
    raising, and the caller treats ``None`` as "no opinion".

  * **Shadow by default.** In ``shadow`` the classification is recorded and changes
    nothing. Only in ``on`` does a "now" verdict join the router's urgent path. A
    classifier that starts steering traffic before a person has read its output is how
    you end up paging someone about a newsletter.

  * **Honour the router's emit contract.** The host router promises to
    persist "never bodies, never subjects, never addresses beyond domain". A body is
    read here to classify it and is then dropped; what lands on disk is an id, a domain,
    a route and some numbers. ``review`` re-joins those ids against the local intake
    tree when a human wants to read the pile, so the subjects stay where they already
    are instead of being copied somewhere new.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

# Where jevkit lives. The repo is the canonical copy; an override lets a different host
# point somewhere else without editing code.
JEVKIT_HOME = Path(os.environ.get("JEVKIT_HOME", str(Path(__file__).resolve().parents[1])))

MODES = ("off", "shadow", "on")
DEFAULT_MODE = "shadow"

# The router runs as a subprocess the cycle wrapper kills at 180s. If that kill lands
# mid-loop, every message already marked seen but not yet routed is lost silently —
# seen.json is written before routing, so there is no retry. A count cap alone does not
# prevent that: 40 calls at a 6s timeout is 240s, over the ceiling on its own. So the
# clock is the real budget and the count is a courtesy.
MAX_PER_CYCLE = 25          # mirrors the intake script's MAX_MESSAGES_PER_RUN
MAX_SECONDS_PER_CYCLE = 45.0
TIMEOUT_S = 5.0

BODY_LIMIT = 8_000          # trimmed again inside jevkit; this just bounds what we read


def _log(message: str) -> None:
    # stderr only, never stdout: the cycle wrapper parses the router's entire stdout as
    # one JSON object, so a single stray print takes the whole pipeline down.
    sys.stderr.write(f"[support-triage] {message}\n")


class Budget:
    """How much triage one cycle may spend, in messages and in seconds.

    ``take()`` is asked before each message and answers False once either limit is
    reached. Whatever is left unclassified is still *routed* — it simply has no opinion
    attached, and the next cycle will not revisit it. Losing an opinion is cheap; losing
    the message is not.
    """

    def __init__(self, messages: int = MAX_PER_CYCLE, seconds: float = MAX_SECONDS_PER_CYCLE):
        self.messages = int(messages)
        self.deadline = time.monotonic() + float(seconds)
        self.skipped = 0

    def take(self) -> bool:
        if self.messages <= 0 or self.remaining_s() <= 0.5:
            self.skipped += 1
            return False
        self.messages -= 1
        return True

    def remaining_s(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    def timeout(self) -> float:
        """Never wait longer than the cycle has left."""
        return max(1.0, min(TIMEOUT_S, self.remaining_s()))


def _load():
    """Import jevkit.triage, or return None if this host has no Jev toolkit."""
    if str(JEVKIT_HOME) not in sys.path:
        sys.path.insert(0, str(JEVKIT_HOME))
    try:
        from jevkit import triage as _triage  # type: ignore
        return _triage
    except Exception as error:  # noqa: BLE001 - absence of jevkit is a normal state
        _log(f"jevkit unavailable ({type(error).__name__}); triage disabled for this cycle")
        return None


def mode_from_config(cfg: Mapping[str, Any]) -> str:
    """Read the mode out of the router config, defaulting to shadow."""
    block = cfg.get("triage")
    value = block.get("mode") if isinstance(block, Mapping) else block
    value = str(value or DEFAULT_MODE).strip().lower()
    return value if value in MODES else DEFAULT_MODE


def known_domains(cfg: Mapping[str, Any]) -> List[str]:
    """Every tenant domain, so a customer's message can be told from a stranger's."""
    out: List[str] = []
    for block in (cfg.get("tenants") or {}).values():
        if isinstance(block, Mapping):
            out.extend(str(d).strip().lower().lstrip(".") for d in block.get("domains", []) if d)
    return sorted({d for d in out if d})


def _read_body(intake_file: Any) -> str:
    """The message body from the intake document the brief came from.

    The brief the router carries has no body — it was never meant to. The intake doc on
    disk does, and reading it here keeps the body inside this process.
    """
    if not intake_file:
        return ""
    try:
        doc = json.loads(Path(str(intake_file)).read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return ""
    body = doc.get("body")
    return str(body)[:BODY_LIMIT] if isinstance(body, str) else ""


def _fingerprint(message_id: Any) -> str:
    return hashlib.sha256(str(message_id or "").encode("utf-8", "replace")).hexdigest()[:16]


def classify_brief(
    brief: Mapping[str, Any], *, tenant: Optional[str], domains: List[str],
    module: Any = None, timeout: float = TIMEOUT_S,
) -> Optional[Dict[str, Any]]:
    """One message in, one routing opinion out. Never raises."""
    engine = module or _load()
    if engine is None:
        return None
    sender = str(brief.get("from") or "")
    try:
        verdict = engine.classify(
            str(brief.get("subject") or ""),
            _read_body(brief.get("intake_file")),
            sender=sender,
            to=str(brief.get("mailbox") or ""),
            known_customer=(tenant is not None) or any(d in sender.lower() for d in domains),
            timeout=timeout,
        )
    except Exception as error:  # noqa: BLE001 - a classifier must not break intake
        _log(f"classify failed ({type(error).__name__}); message left unclassified")
        return None
    if not isinstance(verdict, Mapping):
        return None

    # What lands on disk: an identity, a domain, a route, and numbers. No subject, no
    # body, no full address — the router's contract, kept.
    sender_domain = sender.rsplit("@", 1)[-1].strip(">").lower() if "@" in sender else ""
    return {
        "id": _fingerprint(brief.get("id")),
        "message_id": str(brief.get("id") or "")[:200],
        "domain": sender_domain,
        "tenant": tenant,
        "route": verdict.get("route"),
        "urgency": verdict.get("urgency"),
        "kind": verdict.get("kind"),
        "confidence": verdict.get("confidence"),
        "blocked": verdict.get("blocked"),
        "needs_human": verdict.get("needs_human"),
        "sent_to_jev": bool(verdict.get("sent_to_jev")),
        "reason": str(verdict.get("reason") or "")[:200],
        "latency_ms": verdict.get("latency_ms"),
        "received_utc": str(brief.get("received_utc") or ""),
    }


def record(path: Path, entry: Mapping[str, Any], *, mode: str) -> None:
    """Append one classification. A failure to write is not a failure to route."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        line = dict(entry)
        line["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        line["mode"] = mode
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(line, sort_keys=True) + "\n")
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    except Exception as error:  # noqa: BLE001
        _log(f"could not record classification ({type(error).__name__})")


# ── reading the pile back ────────────────────────────────────────────────────

def review(triage_file: Path, intake_root: Path, *, limit: int = 50,
           routes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Join recorded classifications back to their subjects, for a person to read.

    The subjects are not stored with the classifications on purpose. They already exist
    in the local intake tree; this walks that tree once and joins by message id, so the
    readable view is built on demand and nothing is duplicated onto disk.
    """
    rows: List[Dict[str, Any]] = []
    try:
        for line in triage_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        return []

    wanted = {r.get("message_id") for r in rows if r.get("message_id")}
    subjects: Dict[str, str] = {}
    if wanted and intake_root.is_dir():
        for path in intake_root.glob("*/*/intake.json"):
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            message_id = doc.get("message_id")
            if message_id in wanted:
                subjects[str(message_id)] = str(doc.get("subject") or "")[:160]

    keep = set(routes) if routes else None
    order = {"now": 0, "today": 1, "queue": 2, "ignore": 3}
    out = [dict(r, subject=subjects.get(str(r.get("message_id")), "")) for r in rows
           if keep is None or r.get("route") in keep]
    out.sort(key=lambda r: (order.get(r.get("route"), 9), -(r.get("urgency") or 0)))
    return out[:limit]


def _cli(argv: List[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Inspect recorded support-mail classifications.")
    parser.add_argument("--state", default=os.environ.get("TRIAGE_STATE", "./state"))
    parser.add_argument("--intake", default=os.environ.get("TRIAGE_INTAKE", "./mail"))
    parser.add_argument("--route", action="append", choices=["now", "today", "queue", "ignore"])
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    rows = review(Path(args.state) / "triage.jsonl", Path(args.intake),
                  limit=args.limit, routes=args.route)
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
        return 0
    if not rows:
        print("no classifications recorded yet")
        return 0
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.get("route", "?")] = counts.get(row.get("route", "?"), 0) + 1
    print("  ".join(f"{route}={counts[route]}" for route in ("now", "today", "queue", "ignore")
                    if route in counts))
    print()
    for row in rows:
        urgency = row.get("urgency")
        print(f"{str(row.get('route')):6} u={urgency if urgency is not None else '  - ':>4}  "
              f"{str(row.get('kind') or '-'):10} {str(row.get('domain') or '-'):28} "
              f"{row.get('subject') or '(subject not in local intake)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
