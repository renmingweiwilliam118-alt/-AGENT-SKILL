"""Watch a long-running delegated run, and wake the expensive supervisor only when it matters.

When a cheap orchestrator hands hard work to a frontier model, somebody has to keep
an eye on it. Frontier runs go quiet, loop, ask a question nobody answers, or die on
an error twenty minutes in. Having the orchestrator re-read the transcript every
thirty seconds costs more than the work did.

Jev is the right size for that job: ~400ms, a fraction of a cent, typed answers. So
the split here is deliberate:

* **Code** decides everything it can decide for free — has any new output arrived,
  is the same text repeating, has the process exited. No model is needed to notice
  that a log stopped growing.
* **Jev** judges only what code cannot: is this *meaningful* progress, is it waiting
  on an answer, has it given up, is it finished.
* **The supervisor** is woken only when one of those crosses a threshold.

Nothing here can stop a run on its own opinion. A Jev failure means "keep waiting",
never "abort" — a watchdog that kills the work when its own eyesight fails is worse
than no watchdog.
"""
from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from . import client, privacy

TAIL_CHARS = 3_000
MAX_HISTORY = 12

# What the watcher can conclude. Code maps these to behaviour; the delegated run's
# own output never picks an action directly, only influences the judgement.
ACTIONS = {
    "keep_waiting": "Work is underway and nothing is needed from the supervisor",
    "answer_question": "It is waiting on an answer or a decision that only the owner can give",
    "nudge": "It has drifted, stalled, or is repeating itself and needs redirecting",
    "escalate": "It is failing in a way it will not recover from on its own",
    "collect": "The goal looks finished and the result should be collected",
}

# The delegated output is untrusted: it carries tool results, file contents and web
# pages. Jev can only return one of the closed answers above, so it cannot be talked
# into running anything — but text aimed at a supervising AI is still worth flagging.
_INJECTION = re.compile(
    r"(?i)(ignore (all )?(previous|prior) instructions|disregard (your|the) (rules|instructions)"
    r"|you are now|system\s*:\s*you|tell (the )?supervisor|report (this as )?success"
    r"|mark (this|the task) (as )?(complete|done)|pretend .{0,20}(finished|worked))")


@dataclass
class Snapshot:
    """One assessment of a delegated run."""

    at: float
    elapsed_s: float
    quiet_s: float
    new_output: bool
    looping: bool
    exited: Optional[int] = None
    progressing: Optional[float] = None
    needs_input: Optional[float] = None
    blocked: Optional[float] = None
    done: Optional[float] = None
    action: str = "keep_waiting"
    confidence: float = 0.0
    injection_seen: bool = False
    jev_error: Optional[str] = None
    reason: str = ""

    def as_dict(self) -> Dict[str, Any]:
        out = {k: v for k, v in self.__dict__.items() if v is not None}
        out["at"] = round(self.at, 3)
        return out


def _fingerprint(text: str) -> str:
    """Whitespace-insensitive, so a spinner or a re-rendered progress bar is not 'new work'."""
    return hashlib.sha256(" ".join(text.split()).encode("utf-8", "replace")).hexdigest()


def assess(
    goal: str, tail: str, *, elapsed_s: float = 0.0, quiet_s: float = 0.0,
    new_output: bool = True, looping: bool = False, exited: Optional[int] = None,
    transport: Optional[client.Transport] = None, timeout: float = 5.0,
) -> Snapshot:
    """One Jev call: is this run healthy, and does anyone need to do anything about it?"""
    now = time.time()
    snap = Snapshot(at=now, elapsed_s=elapsed_s, quiet_s=quiet_s, new_output=new_output,
                    looping=looping, exited=exited)

    if exited is not None:
        snap.action = "collect" if exited == 0 else "escalate"
        snap.reason = f"the run exited with status {exited}"
        snap.confidence = 1.0
        return snap

    body = tail[-TAIL_CHARS:]
    snap.injection_seen = bool(_INJECTION.search(privacy.normalize(body)))

    if privacy.is_sensitive(body):
        # Never send a tail that looks like it holds a credential. Fall back to the
        # deterministic signals, which are enough to spot a dead run.
        snap.action = "nudge" if looping or quiet_s > 0 else "keep_waiting"
        snap.reason = "output looks sensitive; judged on activity alone, not sent"
        return snap

    state = {
        "goal": privacy.redact(goal, 600),
        "recent_output": privacy.redact(body, TAIL_CHARS),
        "seconds_since_new_output": round(quiet_s),
        "seconds_running": round(elapsed_s),
        "output_is_repeating": looping,
    }
    questions = {
        "progressing": client.noul(
            "The recent output shows real progress toward the goal: new steps completed, not restating or re-planning"),
        "needs_input": client.noul(
            "The worker is waiting on an answer, a decision or a permission that only the person who assigned the work can give"),
        "blocked": client.noul(
            "The worker has hit an error or obstacle it has not recovered from and will not recover from on its own"),
        "done": client.noul("The goal described has been completed and there is a result to collect"),
        "action": client.choice("What should the supervisor do about this run right now?", ACTIONS),
    }
    try:
        reply = client.ask(state, questions, timeout=timeout, transport=transport)
    except client.JevError as error:
        # Blind, not dead. Keep waiting unless the deterministic signals already say otherwise.
        snap.jev_error = error.code
        snap.action = "nudge" if looping else "keep_waiting"
        snap.reason = f"Jev unavailable ({error.code}); using activity signals only"
        return snap

    answers = reply["answers"]
    snap.progressing = round(answers["progressing"]["noul"], 3)
    snap.needs_input = round(answers["needs_input"]["noul"], 3)
    snap.blocked = round(answers["blocked"]["noul"], 3)
    snap.done = round(answers["done"]["noul"], 3)
    chosen = answers["action"]
    snap.confidence = round(chosen["confidence"], 3)
    snap.action = chosen["choice"]
    snap.reason = f"{snap.action} (confidence {snap.confidence:.2f})"
    return snap


@dataclass
class Watcher:
    """Tracks a delegated run across ticks and decides when the supervisor is needed.

    `alert_after` exists because one uncertain reading is not a reason to interrupt a
    human or spend a frontier turn. A concern has to survive consecutive checks.
    """

    goal: str
    stall_seconds: float = 180.0
    alert_after: int = 2
    min_confidence: float = 0.6
    done_threshold: float = 0.8
    needs_input_threshold: float = 0.7
    blocked_threshold: float = 0.7
    transport: Optional[client.Transport] = None

    started: Optional[float] = None
    last_change: Optional[float] = None
    last_print: str = ""
    seen: List[str] = field(default_factory=list)
    history: List[Snapshot] = field(default_factory=list)
    _streak: Dict[str, int] = field(default_factory=dict)

    def tick(self, tail: str, *, exited: Optional[int] = None, now: Optional[float] = None) -> Snapshot:
        now = now if now is not None else time.time()
        if self.started is None:
            self.started = now
            self.last_change = now

        mark = _fingerprint(tail[-TAIL_CHARS:])
        new_output = mark != self.last_print
        if new_output:
            self.last_change = now
        self.last_print = mark
        # Looping means this exact tail has been seen before and nothing has changed since.
        looping = (not new_output) and self.seen.count(mark) >= 2
        self.seen.append(mark)
        del self.seen[:-MAX_HISTORY]

        quiet = now - (self.last_change or now)
        snap = assess(self.goal, tail, elapsed_s=now - self.started, quiet_s=quiet,
                      new_output=new_output, looping=looping, exited=exited,
                      transport=self.transport)

        # A log that stopped growing is a fact, not an opinion — it stands even if Jev disagrees.
        if exited is None and quiet >= self.stall_seconds and snap.action == "keep_waiting":
            snap.action = "nudge"
            snap.reason = f"no new output for {round(quiet)}s"

        for key in ("keep_waiting", "answer_question", "nudge", "escalate", "collect"):
            self._streak[key] = self._streak.get(key, 0) + 1 if snap.action == key else 0
        self.history.append(snap)
        del self.history[:-MAX_HISTORY]
        return snap

    def should_alert(self, snap: Snapshot) -> bool:
        """True when the supervisor should actually be woken."""
        if snap.exited is not None:
            return True
        if snap.action == "keep_waiting":
            return False
        if snap.injection_seen:
            return True                       # always surface text aimed at the supervisor
        # A confident, decisive reading gets through immediately; an unsure one has to repeat.
        strong = {
            "collect": (snap.done or 0) >= self.done_threshold,
            "answer_question": (snap.needs_input or 0) >= self.needs_input_threshold,
            "escalate": (snap.blocked or 0) >= self.blocked_threshold,
            "nudge": snap.looping or snap.jev_error is not None or "no new output" in snap.reason,
        }.get(snap.action, False)
        if strong and snap.confidence >= self.min_confidence:
            return True
        return self._streak.get(snap.action, 0) >= self.alert_after

    def summary(self) -> Dict[str, Any]:
        """A status snapshot for the supervisor: state, not prose. Jev cannot write."""
        last = self.history[-1] if self.history else None
        return {
            "goal": self.goal[:200],
            "ticks": len(self.history),
            "elapsed_s": round(last.elapsed_s) if last else 0,
            "quiet_s": round(last.quiet_s) if last else 0,
            "action": last.action if last else "keep_waiting",
            "progressing": last.progressing if last else None,
            "needs_input": last.needs_input if last else None,
            "blocked": last.blocked if last else None,
            "done": last.done if last else None,
            "injection_seen": any(s.injection_seen for s in self.history),
            "jev_errors": sum(1 for s in self.history if s.jev_error),
        }


def watch(
    goal: str, read_tail: Callable[[], str], *, poll_seconds: float = 30.0,
    max_seconds: float = 7200.0, is_running: Optional[Callable[[], Optional[int]]] = None,
    on_alert: Optional[Callable[[Snapshot, Watcher], None]] = None,
    sleep: Callable[[float], None] = time.sleep, now: Callable[[], float] = time.time,
    **watcher_kwargs: Any,
) -> Dict[str, Any]:
    """Poll a delegated run until it finishes, stalls past rescue, or runs out of time.

    `read_tail` returns the run's recent output. `is_running` returns None while it is
    alive and an exit status once it is not. `on_alert` is called only when the
    supervisor genuinely needs to act — that is the whole point.
    """
    watcher = Watcher(goal=goal, **watcher_kwargs)
    started = now()
    alerts: List[Dict[str, Any]] = []
    while True:
        exited = is_running() if is_running else None
        snap = watcher.tick(read_tail(), exited=exited, now=now())
        if watcher.should_alert(snap):
            alerts.append(snap.as_dict())
            if on_alert:
                on_alert(snap, watcher)
        if exited is not None or snap.action == "collect":
            return {"outcome": "finished" if (exited in (0, None)) else "failed",
                    "exit_status": exited, "alerts": alerts, "summary": watcher.summary()}
        if now() - started >= max_seconds:
            return {"outcome": "timed_out", "exit_status": None,
                    "alerts": alerts, "summary": watcher.summary()}
        sleep(poll_seconds)
