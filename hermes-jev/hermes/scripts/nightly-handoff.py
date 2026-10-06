#!/usr/bin/env python3
"""Close every live conversation for the night and leave tomorrow a capsule.

An agent that is never given a fresh start accumulates. One of the conversations this
was written for had 2,255 messages and seventeen days of history, and every single turn
re-sent all of it. Nobody chose that; it is just what happens when a session never ends.

So this runs once a night. For each conversation that is actually alive, it writes a
handoff capsule and marks the session closed. The next morning's first message opens a
new session and receives the capsule, so the agent knows what it was doing without
carrying the transcript that proves it.

Deliberately conservative:
  * Only sessions with recent activity and enough substance to be worth summarising.
  * A capsule must be written BEFORE a session is closed. If the capsule fails, the
    session is left open — losing the thread is worse than a large context.
  * One capsule per conversation, from its most recent session. Older sessions still
    open on the same conversation are closed with it, never summarised over it.
  * --dry-run shows exactly what would happen and touches nothing: no capsule, no
    closed session, no report file, not even a bytecode cache. The plan goes to stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

MIN_MESSAGES = 6            # below this there is nothing worth carrying forward
ACTIVE_WITHIN_S = 3 * 86400  # a conversation nobody has touched in days needs no capsule
MAX_PER_PROFILE = 40        # a runaway night must not mean hundreds of model calls


def log(message: str) -> None:
    sys.stderr.write(f"[nightly-handoff] {message}\n")
    sys.stderr.flush()


ROOT_PROFILE = "default"    # what Hermes calls the profile that is the home itself
# Every cron job's sessions resolve to one platform-wide lane, so a capsule written from one
# job's stale run would be handed to whichever job ran next as "context you established".
NOT_CONVERSATIONS = frozenset({"cron"})


def profiles(home: Path, names: Optional[List[str]] = None) -> List[Tuple[str, Path]]:
    """Every session store under this home, as (name, directory)."""
    found: List[Tuple[str, Path]] = []
    # The home is a profile too, and on an install that never made a named one it is the
    # only profile there is. Looking only under profiles/ made this script a no-op there.
    if (home / "state.db").is_file():
        found.append((ROOT_PROFILE, home))
    root = home / "profiles"
    if root.is_dir():
        found += [(p.name, p) for p in sorted(root.iterdir()) if (p / "state.db").is_file()]
    if names:
        wanted = set(names)
        found = [(name, path) for name, path in found if name in wanted]
    return found


def live_sessions(db: Path, *, now: float, min_messages: int, within_s: float, limit: int) -> List[Dict[str, Any]]:
    """Open sessions with recent activity and real content, newest first."""
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=20)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as error:
        log(f"  cannot read {db}: {error}")
        return []
    try:
        # sqlite opens lazily, so a database that cannot be read fails here, not above.
        columns = {r[1] for r in conn.execute("pragma table_info(sessions)")}
    except sqlite3.Error as error:
        log(f"  cannot read {db}: {error}")
        conn.close()
        return []
    if not {"id", "ended_at"} <= columns:
        conn.close()
        return []
    activity = "last_activity_at" if "last_activity_at" in columns else "started_at"
    optional = [c for c in ("session_key", "chat_id", "thread_id", "source", "message_count", "title") if c in columns]
    select = ", ".join(["id", activity + " as activity_at"] + optional)
    rows: List[Dict[str, Any]] = []
    try:
        for row in conn.execute(
                f"select {select} from sessions where ended_at is null and {activity} is not null "
                f"and {activity} > ? order by {activity} desc limit ?", (now - within_s, limit * 4)):
            entry = dict(row)
            count = entry.get("message_count")
            if count is None:
                count = conn.execute("select count(*) from messages where session_id=?", (entry["id"],)).fetchone()[0]
            entry["messages"] = int(count or 0)
            if entry["messages"] >= min_messages:
                rows.append(entry)
            if len(rows) >= limit:
                break
    except sqlite3.Error as error:
        log(f"  query failed on {db}: {error}")
    finally:
        conn.close()
    return rows


def close_session(db: Path, session_id: str, *, now: float, reason: str) -> bool:
    """Mark the session ended so the next message opens a fresh one."""
    try:
        conn = sqlite3.connect(str(db), timeout=30)
        conn.execute("pragma busy_timeout=30000")
        columns = {r[1] for r in conn.execute("pragma table_info(sessions)")}
        if "end_reason" in columns:
            conn.execute("update sessions set ended_at=?, end_reason=? where id=? and ended_at is null",
                         (now, reason, session_id))
        else:
            conn.execute("update sessions set ended_at=? where id=? and ended_at is null", (now, session_id))
        conn.commit()
        changed = conn.total_changes > 0
        conn.close()
        return changed
    except sqlite3.Error as error:
        log(f"  could not close {session_id}: {error}")
        return False


def conversation_of(session: Dict[str, Any]) -> Optional[tuple]:
    """What makes two session rows the same conversation, or None when nothing does.

    The gateway's own routing key is the authority when the store records it. A chat id
    is the next best thing. A row with neither (a CLI session) has no identity to share,
    so it is never treated as a stale copy of another one.
    """
    if session.get("session_key"):
        return ("key", str(session["session_key"]))
    if session.get("chat_id"):
        return ("chat", str(session.get("source") or ""), str(session["chat_id"]),
                str(session.get("thread_id") or ""))
    return None


def group_by_lane(sessions: List[Dict[str, Any]], lane_for: Callable[[Dict[str, Any]], str]
                  ) -> List[Tuple[str, List[Dict[str, Any]]]]:
    """Sessions per capsule file, each group most recent first.

    A lane is one file. Rows that were rotated without being marked ended pile up on it:
    one Telegram topic had four. Written one after another, newest first, the capsule
    that survived was the OLDEST session's, and all four were then closed on top of it.
    """
    lanes: Dict[str, List[Dict[str, Any]]] = {}
    for session in sessions:
        lanes.setdefault(lane_for(session), []).append(session)
    # Sorted here rather than trusted from the query: which session wins the lane is the
    # whole point, and it should not depend on a caller remembering an ORDER BY.
    return [(lane, sorted(group, key=lambda s: float(s.get("activity_at") or 0), reverse=True))
            for lane, group in lanes.items()]


def hand_off_profile(db: Path, sessions: List[Dict[str, Any]], *, lane_for: Callable[[Dict[str, Any]], str],
                     build: Callable[[str, str], Dict[str, Any]], dry_run: bool, now: float
                     ) -> List[Dict[str, Any]]:
    """One capsule per lane, from its newest session. Returns a report entry per session."""
    done: List[Dict[str, Any]] = []
    unattended = [s for s in sessions if str(s.get("source") or "") in NOT_CONVERSATIONS]
    for session in unattended:
        skipped: Dict[str, Any] = {"session": session["id"], "messages": session["messages"]}
        skipped.update({"action": "would skip; not a conversation"} if dry_run
                       else {"handoff": "skipped", "closed": False})
        log(f"  {'[dry-run] ' if dry_run else ''}skipped ({session.get('source')} is not a conversation): {session['id']}")
        done.append(skipped)
    sessions = [s for s in sessions if s not in unattended]
    for lane, group in group_by_lane(sessions, lane_for):
        newest, rest = group[0], group[1:]
        entry: Dict[str, Any] = {"session": newest["id"], "lane": lane, "messages": newest["messages"]}
        stale = [s for s in rest if conversation_of(s) is not None
                 and conversation_of(s) == conversation_of(newest)]
        # Same file, different conversation: two people with their own sessions in one
        # group chat, or CLI sessions that share a platform-wide lane. Their thread is not
        # in the newest session's capsule, so closing them would lose it.
        separate = [s for s in rest if s not in stale]
        if dry_run:
            entry["action"] = "would hand off and close"
            log(f"  [dry-run] {newest['id']}  lane={lane}  msgs={newest['messages']}")
        else:
            try:
                built = build(newest["id"], lane)
            except Exception as error:  # noqa: BLE001
                built = {"status": "error", "error": str(error)[:200]}
            entry["handoff"] = built.get("status")
            entry["jev"] = built.get("jev")
            # Only close a session whose thread has actually been preserved.
            if built.get("status") == "ok":
                entry["closed"] = close_session(db, newest["id"], now=now, reason="nightly-handoff")
            else:
                entry["closed"] = False
                log(f"  kept open (capsule {built.get('status')}): {newest['id']}")
        done.append(entry)

        for session in stale:
            older = {"session": session["id"], "lane": lane, "messages": session["messages"],
                     "capsule_from": newest["id"]}
            if dry_run:
                older["action"] = "would close; the capsule comes from the newer session"
                log(f"  [dry-run] {session['id']}  lane={lane}  older copy of {newest['id']}")
            elif entry.get("handoff") == "ok":
                # No capsule of its own: it would be written over the newer one.
                older["handoff"] = "superseded"
                older["closed"] = close_session(db, session["id"], now=now, reason="nightly-handoff-superseded")
            else:
                older["handoff"] = "superseded"
                older["closed"] = False
            done.append(older)
        for session in separate:
            other: Dict[str, Any] = {"session": session["id"], "lane": lane, "messages": session["messages"]}
            if dry_run:
                other["action"] = "would keep open; a different, newer conversation has this lane"
            else:
                other.update({"handoff": "lane_shared", "closed": False})
            log(f"  {'[dry-run] ' if dry_run else ''}kept open (lane {lane} goes to {newest['id']}): {session['id']}")
            done.append(other)
    return done


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME") or str(Path.home() / ".hermes"))
    parser.add_argument("--profile", action="append", help="limit to these profiles (repeatable)")
    parser.add_argument("--plugin", help="path to the hermes-handoff plugin (default: <home>/plugins/hermes-handoff)")
    parser.add_argument("--min-messages", type=int, default=MIN_MESSAGES)
    parser.add_argument("--within-hours", type=float, default=ACTIVE_WITHIN_S / 3600)
    parser.add_argument("--limit", type=int, default=MAX_PER_PROFILE)
    parser.add_argument("--dry-run", action="store_true", help="report only; write and close nothing")
    parser.add_argument("--confidential", action="store_true",
                        help="capsules carry no customer detail (required where a continuity "
                             "rule forbids persisting it); a capsule that cannot meet the "
                             "contract is not written at all")
    args = parser.parse_args(argv)

    home = Path(args.hermes_home).expanduser()
    plugin = Path(args.plugin) if args.plugin else home / "plugins" / "hermes-handoff"
    if not (plugin / "handoff.py").is_file():
        log(f"no handoff plugin at {plugin}")
        return 2
    if args.dry_run:
        # Importing the plugin would otherwise leave a __pycache__ beside it, which is a
        # small thing to find after a command that said it would touch nothing.
        sys.dont_write_bytecode = True
    sys.path.insert(0, str(plugin))
    os.environ.setdefault("HERMES_HOME", str(home))
    # The .env holds the Jev key; the CLI loads it per-process, a plain script does not.
    env_file = home / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
            name, sep, value = line.partition("=")
            if sep and name.strip().isidentifier() and name.strip() not in os.environ:
                os.environ[name.strip()] = value.strip()

    import handoff as ho  # noqa: E402
    compact = None
    try:
        from jevkit import compact as _compact  # noqa: E402
        compact = _compact
    except Exception as error:  # noqa: BLE001
        log(f"jevkit unavailable ({error}); every turn will be treated as background")

    def writer(prompt: str) -> str:
        from agent.auxiliary_client import call_llm  # type: ignore
        return ho.extract_text(call_llm(task="compression", messages=[{"role": "user", "content": prompt}]))

    def lane_for(session: Dict[str, Any]) -> str:
        # Deliberately the plugin's own function: two implementations of this rule would
        # drift, and a capsule keyed differently from how it is read is a silent no-op
        # that looks like the feature simply not working.
        return ho.lane_key({**session, "session_id": session["id"]})

    now = time.time()
    report: Dict[str, Any] = {"at": now, "dry_run": args.dry_run, "profiles": []}
    for name, profile in profiles(home, args.profile):
        db = profile / "state.db"
        sessions = live_sessions(db, now=now, min_messages=args.min_messages,
                                 within_s=args.within_hours * 3600, limit=args.limit)
        log(f"{name}: {len(sessions)} live session(s) to hand off")
        # Capsules live beside their own profile. Moved before anything is keyed: a session
        # with no chat id is resolved through HERMES_HOME's database, and with this set
        # later the first one in every profile was looked up in the previous profile's.
        os.environ["HERMES_HOME"] = str(profile)
        # Checked per profile, after HERMES_HOME moves: one profile may be bound by a
        # continuity rule its neighbour is not.
        confidential = args.confidential or ho.confidential_here()

        def build(session_id: str, lane: str, confidential: bool = confidential) -> Dict[str, Any]:
            return ho.build(session_id, lane, write=writer,
                            select=(compact.select if (compact and ho.jev_prepass_enabled()) else None),
                            digest=(compact.digest if (compact and ho.jev_prepass_enabled()) else None),
                            prompt_for=(compact.handoff_prompt if compact else None),
                            valid=(compact.looks_like_capsule if compact else None),
                            confidential=confidential,
                            scrub=(compact.redact_capsule if (compact and confidential) else None))

        done = hand_off_profile(db, sessions, lane_for=lane_for, build=build,
                                dry_run=args.dry_run, now=now)
        report["profiles"].append({"profile": name, "confidential": confidential, "sessions": done})

    os.environ["HERMES_HOME"] = str(home)
    if not args.dry_run:
        out = home / "logs" / "nightly-handoff.json"
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        except OSError:
            pass
    rows = [s for p in report["profiles"] for s in p["sessions"]]
    if args.dry_run:
        log(f"dry run: {sum(1 for s in rows if 'would hand off' in s.get('action', ''))} capsule(s) "
            f"would be written; nothing was changed")
    else:
        log(f"done: {sum(1 for s in rows if s.get('handoff') == 'ok')} capsule(s) written, "
            f"{sum(1 for s in rows if s.get('closed'))} session(s) closed")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
