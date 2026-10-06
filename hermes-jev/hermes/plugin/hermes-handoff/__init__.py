"""Hermes plugin: `handoff` — carry the thread of one session into the next.

Three seams, all public:

* ``pre_gateway_dispatch``  the bare word "handoff" starts a capsule for this conversation
* ``/wrapup``               the same thing, for anyone who prefers a command
* ``pre_llm_call``          the next session's first turn gets the capsule as context

This plugin writes capsules. It never ends a session and never answers for the gateway:
the word "handoff" goes on to the host exactly as the person typed it. A host that rotates
the session on that word keeps doing so; on any other host the capsule waits for the next
fresh session, however that one comes about (``/new``, a reset policy, the nightly script).

The writer model is whatever the host already uses for auxiliary work, so this needs no
new credential. Jev is optional: without it every turn is treated as background and the
capsule is still written.
"""
from __future__ import annotations

import contextvars
import logging
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from . import handoff

logger = logging.getLogger(__name__)

# Not "handoff": Hermes ships a built-in /handoff (move a CLI session to a messaging
# platform), so that registration was refused on every load and the command never existed.
# No hyphen either, because Telegram rejects one in a command name.
COMMAND = "wrapup"

_CTX: Any = None

# The command handler is only given its argument string, and in a gateway the process
# environment's HERMES_SESSION_ID belongs to whichever conversation made an agent last.
# The dispatch hook sees the real event first, in the same task, so it leaves the
# conversation's identity here for the command to pick up.
_DISPATCH: "contextvars.ContextVar[Optional[Dict[str, Any]]]" = contextvars.ContextVar(
    "hermes_handoff_dispatch", default=None)

_INFLIGHT: set = set()
_INFLIGHT_LOCK = threading.Lock()


def _setting(name: str, default: Any) -> Any:
    if _CTX is not None:
        try:
            value = _CTX.get_config(name, None)
            if value is not None:
                return value
        except Exception:  # noqa: BLE001
            pass
    return default


def _jevkit():
    """jevkit from beside us, or from the hermes-jev plugin; otherwise handoff runs without Jev."""
    # Vendored copy first: it makes this plugin self-contained, which matters when it is
    # deployed to a host that does not run the rest of the Jev toolkit.
    local = Path(__file__).resolve().parent
    if (local / "jevkit" / "compact.py").is_file():
        import sys
        if str(local) not in sys.path:
            sys.path.insert(0, str(local))
        try:
            from jevkit import compact  # type: ignore
            return compact
        except Exception:  # noqa: BLE001
            pass
    try:
        from hermes_jev.jevkit import compact  # type: ignore
        return compact
    except Exception:  # noqa: BLE001
        pass
    for base in (Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes"),):
        candidate = base / "plugins" / "hermes-jev"
        if (candidate / "jevkit" / "compact.py").is_file():
            import sys
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
            try:
                from jevkit import compact  # type: ignore
                return compact
            except Exception:  # noqa: BLE001
                return None
    return None


def _writer() -> Any:
    """The host's own auxiliary model writes the capsule — no new credential, no new bill."""
    def write(prompt: str) -> str:
        from agent.auxiliary_client import call_llm  # type: ignore

        return handoff.extract_text(
            call_llm(task="compression", messages=[{"role": "user", "content": prompt}]))
    return write


def run_handoff(context: Dict[str, Any]) -> Dict[str, Any]:
    """Build and store the capsule for this conversation. Slow: an export and two models."""
    lane = handoff.lane_key(context)
    session_id = str(context.get("session_id") or "")
    if not session_id:
        return {"status": "no_session"}
    compact = _jevkit()
    # Some deployments are bound by a continuity rule that forbids carrying customer
    # detail forward. Where that is true this must be on, and the capsule becomes a
    # breadcrumb rather than a summary.
    confidential = (_setting("confidential", False) in (True, "true", "yes", "on", 1)
                    or handoff.confidential_here())
    return handoff.build(
        session_id, lane, write=_writer(),
        select=(compact.select if (compact and handoff.jev_prepass_enabled()) else None),
        digest=(compact.digest if (compact and handoff.jev_prepass_enabled()) else None),
        prompt_for=(compact.handoff_prompt if compact else None),
        valid=(compact.looks_like_capsule if compact else None),
        confidential=confidential,
        scrub=(compact.redact_capsule if (compact and confidential) else None))


def start_handoff(context: Dict[str, Any]) -> str:
    """Build the capsule on a worker thread: "started", "already_running" or "no_session".

    The gateway calls its dispatch hook, and its command handlers, synchronously on the
    event loop. The build exports a transcript and waits on two models, so run inline it
    froze every conversation on the gateway for as long as the writer took, not only the
    one that asked.
    """
    session_id = str(context.get("session_id") or "")
    if not session_id:
        return "no_session"
    with _INFLIGHT_LOCK:
        # One build per session at a time. A redelivered update, or someone sending the
        # word three times, would otherwise race three writers onto one capsule file.
        if session_id in _INFLIGHT:
            return "already_running"
        _INFLIGHT.add(session_id)

    def work() -> None:
        try:
            result = run_handoff(context)
            status = result.get("status")
            # Logged either way. The dispatch path has no reply of its own, so the log is
            # the only evidence the trigger did anything.
            if status == "ok":
                logger.info("handoff capsule written: lane=%s session=%s messages=%s jev=%s",
                            result.get("lane"), session_id, result.get("messages"), result.get("jev"))
            else:
                logger.warning("handoff capsule not written (%s): session=%s", status, session_id)
        except Exception:  # noqa: BLE001 - a handoff must never take the gateway down with it
            logger.exception("handoff capsule failed: session=%s", session_id)
        finally:
            with _INFLIGHT_LOCK:
                _INFLIGHT.discard(session_id)

    # A multiplexing host scopes the profile home and its secrets in context variables,
    # and a bare thread starts with none of them.
    scoped = contextvars.copy_context()
    threading.Thread(target=scoped.run, args=(work,), name="hermes-handoff", daemon=True).start()
    return "started"


# ── the real gateway event ───────────────────────────────────────────────────

def _platform_name(source: Any) -> str:
    platform = getattr(source, "platform", None)
    return str(getattr(platform, "value", platform) or "")


def _authorized(gateway: Any, source: Any) -> bool:
    """Whether the gateway would accept this sender. False only on an explicit no.

    This hook runs BEFORE the gateway's own authorization, so that plugins can serve
    unknown senders. Here it would mean anyone who can post in a shared chat spends the
    owner's model calls by typing one word.
    """
    for name in ("_is_user_authorized_for_source", "_is_user_authorized"):
        check = getattr(gateway, name, None)
        if not callable(check):
            continue
        try:
            return check(source) is not False
        except Exception:  # noqa: BLE001
            continue
    return True


def _live_session(source: Any, gateway: Any, session_store: Any, context: Dict[str, Any]) -> str:
    """The session this conversation is in right now, resolved before anything rotates it."""
    key = ""
    for owner, name in ((gateway, "_session_key_for_source"), (session_store, "_generate_session_key")):
        resolve = getattr(owner, name, None)
        if not callable(resolve):
            continue
        try:
            candidate = resolve(source)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(candidate, str) and candidate:
            key = candidate
            break
    peek = getattr(session_store, "peek_session_id", None)
    if key and callable(peek):
        try:
            found = peek(key)
            if isinstance(found, str) and found:
                return found
        except Exception:  # noqa: BLE001
            pass
    return handoff.open_session_for(context) or ""


def _event_context(event: Any, gateway: Any, session_store: Any) -> Dict[str, Any]:
    source = getattr(event, "source", None)
    context: Dict[str, Any] = {
        "platform": _platform_name(source),
        "chat_id": str(getattr(source, "chat_id", "") or ""),
        "thread_id": str(getattr(source, "thread_id", "") or ""),
        "sender_id": str(getattr(source, "user_id", "") or ""),
    }
    context["session_id"] = _live_session(source, gateway, session_store, context)
    return context


def _on_gateway_event(event: Any, gateway: Any, session_store: Any) -> None:
    """The gateway's real call. Always returns None, so the message continues untouched.

    The obvious result, {"action": "skip"}, is wrong twice over. The gateway drops a
    skipped message without replying, and it never reads a "message" key, so the person
    would type "handoff" and get silence. And a host with its own plain-"handoff" session
    rotation runs it later in the same dispatch: a skip pre-empts the part that already
    works. So this only starts the capsule and steps aside.
    """
    _DISPATCH.set(None)
    if getattr(event, "internal", False):
        return None
    # Proactive plugin events carry text nobody typed; it must not be able to spend a
    # model call, or reach the command below, by containing one word.
    if getattr(event, "allow_gateway_control", True) is False:
        return None
    text = getattr(event, "text", None)
    if not isinstance(text, str):
        return None
    stripped = text.strip()
    if stripped.startswith("/"):
        name = stripped.split(None, 1)[0][1:].split("@", 1)[0].lower()
        if name == COMMAND and _authorized(gateway, getattr(event, "source", None)):
            _DISPATCH.set(_event_context(event, gateway, session_store))
        return None
    if getattr(event, "media_urls", None) or not handoff.is_trigger(text):
        return None
    if not _authorized(gateway, getattr(event, "source", None)):
        return None
    outcome = start_handoff(_event_context(event, gateway, session_store))
    if outcome != "started":
        logger.info("handoff trigger ignored (%s): platform=%s", outcome,
                    _platform_name(getattr(event, "source", None)))
    return None


# ── hooks ────────────────────────────────────────────────────────────────────

def _on_dispatch(**context: Any) -> Any:
    """The bare word `handoff`. A sentence mentioning one is left alone."""
    # Hermes sends event=, gateway=, session_store= and nothing else. This hook used to
    # read text= and session_id=, which the gateway has never sent, so it returned None
    # for every message and the trigger word never wrote a capsule in production.
    if context.get("event") is not None:
        return _on_gateway_event(context["event"], context.get("gateway"), context.get("session_store"))

    # Flat keywords: a host that passes the text and session id directly, and that
    # delivers a skip's message as the reply. Hermes is not one of them.
    text = context.get("text") or context.get("message") or context.get("user_message")
    if not handoff.is_trigger(text):
        return None
    outcome = start_handoff(dict(context))
    if outcome == "no_session":
        note = "Could not write the handoff (no_session). The session is unchanged."
    else:
        # Says what is true now. The capsule is still being written when this is read.
        note = ("Writing the handoff now. The next fresh session in this conversation "
                "starts with the summary.")
    return {"action": "skip", "message": note}


def _on_pre_llm_call(session_id: str = "", **context: Any) -> Any:
    """Give the new session its capsule, once."""
    if _setting("inject", True) in (False, "false", "off"):
        return None
    lane = handoff.lane_key({**context, "session_id": session_id})
    capsule = handoff.take_pending(lane, current_session=session_id)
    if not capsule:
        return None
    return {"context": handoff.injection(capsule)}


def _cli_session_id() -> str:
    """The session a CLI command belongs to. Empty inside a gateway, on purpose."""
    try:
        # In a gateway this reads the per-task value, which is cleared at the start of
        # every message. Empty is the right answer there: the process-wide variable names
        # some other conversation's session, and summarising that one would be worse.
        from gateway.session_context import get_session_env  # type: ignore
        return str(get_session_env("HERMES_SESSION_ID", "") or "")
    except Exception:  # noqa: BLE001
        return os.environ.get("HERMES_SESSION_ID", "")


def _command(raw_args: str = "") -> str:
    dispatched = _DISPATCH.get()
    if dispatched is not None:
        # Inside a gateway. The handler runs on the event loop, so the build is handed off.
        _DISPATCH.set(None)
        outcome = start_handoff(dispatched)
        if outcome == "no_session":
            return "No handoff written (no_session): this conversation has no session yet."
        if outcome == "already_running":
            return "A handoff for this session is already being written."
        return ("Writing the handoff now. It is given to the next fresh session in this "
                "conversation; send /new when you want that session to start.")
    context = {"session_id": _cli_session_id(),
               "platform": os.environ.get("HERMES_SESSION_PLATFORM", "")}
    result = run_handoff(context)
    if result.get("status") == "ok":
        return (f"Handoff written to {result['path']} from {result['messages']} turns. "
                "The next fresh session starts with it.")
    return f"No handoff written ({result.get('status')})."


_RULE = (
    "If the person says just \"handoff\", they are closing this stretch of work. A short "
    "capsule of the conversation is being written in the background and is given to the next "
    "fresh session in this conversation. If you are answering that message, say in one line "
    "that the handoff is being saved and that /new starts the fresh session; do not begin new "
    "work in that reply. When a session opens with a [Handoff from the previous session] "
    "block, that is history you already established — do not greet again or re-ask what it "
    "settles; continue from its Next section."
)


def register(ctx: Any) -> None:
    global _CTX
    _CTX = ctx
    ctx.register_hook("pre_gateway_dispatch", _on_dispatch)
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_command(COMMAND, _command, description="Write a handoff capsule for the next session")
    ctx.register_system_prompt_section("hermes-handoff", _RULE, max_chars=700)
