"""Exact-match memo for calls whose answer is a function of their input.

Why this exists: ``jev plan`` asks a text model the same question every time the same
command is given. That is about a second and a fraction of a cent per run, for an answer
that was already on this machine. A memo keyed on exactly what decides the answer returns it
in under a millisecond. It is not a response cache: it never sees a request body, a prompt
or a reply, only the small validated value a caller chose to keep.

Two ideas are borrowed from rohanarun/computer-use-cache (MIT licence,
https://github.com/rohanarun/computer-use-cache): the key carries the SCOPE an answer came
from, so an entry written for one endpoint never answers for another, and ANY failure is a
miss. No code is taken from it. The store, the limits and the modes below are our own, and
so is putting a rules version in the key: upstream keys on the whole request, which carries
the prompt; a caller here keys on its input, so it has to fold its own rules in (see
``jevkit/plan.py``).

The contract with callers is that nothing here raises. A missing directory, a read-only
disk, a file someone edited by hand, a file from a newer version: each is a miss on read and
a no-op on write, so the caller makes the call it would have made without a memo.

Nothing here decides what is safe to keep. The caller must not pass in anything sensitive,
and must treat what comes back as untrusted: the file sits in the person's cache directory
and anything that can write there can write an entry.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

SCHEMA = "jev.memo_v1"
MODES = ("off", "shadow", "on")
MAX_ENTRIES = 256
MAX_VALUE_BYTES = 16 * 1024
# 256 entries of 16 KB would be twice this, so the writer trims to fit (see _save). A reader
# that meets a bigger file did not write it, and parsing whatever is found in a cache
# directory is how a memo turns into a way to stall the program that uses it.
MAX_FILE_BYTES = 2 * 1024 * 1024
# An entry dated further ahead than this is a miss. Without it a hand-written "at" in the
# far future is an entry that never expires.
_CLOCK_SKEW_S = 60
# The namespace becomes a file name. Anything outside this set is refused, so "../x" can
# never be a path.
_NAMESPACE = re.compile(r"[a-z0-9_-]{1,32}")
_KEY = re.compile(r"[0-9a-f]{64}")


def mode() -> str:
    """``JEV_MEMO``: off, shadow or on. Unset, empty or misspelt is ``shadow``.

    Shadow is the default because it changes nothing: the caller still makes the real call
    and only records whether the memo would have agreed. A typo must not switch reuse on.
    """
    value = (os.environ.get("JEV_MEMO") or "").strip().lower()
    return value if value in MODES else "shadow"


def key(namespace: str, *parts: Any) -> str:
    """sha256 over the schema, the namespace and every part, NUL-separated. "" on failure.

    The schema is in the key so that a change to the stored shape orphans old entries
    instead of misreading them.
    """
    try:
        # A part can never contain the separator, or ("a<NUL>b", "c") and ("a", "b<NUL>c")
        # would be the same key.
        fields = [SCHEMA, str(namespace)] + [str(part).replace("\x00", "\ufffd") for part in parts]
        return hashlib.sha256("\x00".join(fields).encode("utf-8", "surrogatepass")).hexdigest()
    except Exception:  # noqa: BLE001 - no key means no memo for this call, never a crash
        return ""


def directory() -> Path:
    """Where the namespace files live. The same base ``jevkit/catalog.py`` caches under."""
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "jev" / "memo"


def _path(namespace: Any) -> Optional[Path]:
    if not isinstance(namespace, str) or not _NAMESPACE.fullmatch(namespace):
        return None
    return directory() / f"{namespace}.json"


def _at(entry: Any) -> float:
    """When an entry was written. Anything malformed counts as oldest, so it is evicted first."""
    at = entry.get("at") if isinstance(entry, dict) else None
    if isinstance(at, bool) or not isinstance(at, (int, float)) or at != at:
        return float("-inf")
    return float(at)


def _load(path: Path) -> Dict[str, Any]:
    """The entries in one namespace file. Empty for anything that is not a file we wrote."""
    # O_NONBLOCK and the regular-file check: a named pipe left where the file should be
    # makes a plain open() wait for a writer that never comes, and "any failure is a miss"
    # has to include the failure that never returns.
    fd = os.open(str(path), os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            return {}
        raw = handle.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES:
        return {}
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        return {}
    entries = data.get("entries")
    return entries if isinstance(entries, dict) else {}


def _save(path: Path, entries: Dict[str, Any]) -> None:
    """Write the whole namespace to a private temp file, then swap it in.

    Two processes can both read, both add an entry and both write; the second replace wins
    and the first entry is gone. That is a miss next time, which costs one call. A lock
    would cost every caller a way to hang, and a half-written file would cost every entry.
    """
    order = sorted(entries, key=lambda name: _at(entries[name]))
    cut = max(0, len(order) - MAX_ENTRIES)
    while True:
        kept = {name: entries[name] for name in order[cut:]}
        raw = json.dumps({"schema": SCHEMA, "entries": kept}, separators=(",", ":")).encode("utf-8")
        if len(raw) <= MAX_FILE_BYTES or not kept:
            break
        cut += max(1, len(kept) // 4)      # still too big to be read back: drop more of the oldest
    # 0700 and 0600: the entries are a record of what this person asked their computer to
    # do. makedirs applies the mode to a directory it creates and not to one it finds, and a
    # umask can widen either, so both are set again explicitly.
    os.makedirs(path.parent, mode=0o700, exist_ok=True)
    os.chmod(path.parent, 0o700)
    # The thread is in the name as well as the process: two threads sharing one temp file
    # truncate each other's half-written bytes, and nearly every write is lost.
    temp = path.with_name(f"{path.name}.tmp.{os.getpid()}.{threading.get_ident()}")
    try:
        fd = os.open(str(temp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "wb") as handle:
            os.chmod(str(temp), 0o600)
            handle.write(raw)
        os.replace(str(temp), str(path))
    except Exception:
        try:
            os.unlink(str(temp))
        except OSError:
            pass
        raise


def get(namespace: str, k: str, ttl_s: float) -> Optional[Dict[str, Any]]:
    """The stored value, or None. None is the answer to every kind of trouble."""
    try:
        path = _path(namespace)
        if path is None or not isinstance(k, str) or not _KEY.fullmatch(k):
            return None
        entry = _load(path).get(k)
        if not isinstance(entry, dict):
            return None
        age = time.time() - _at(entry)
        # Written as the range that passes, so a NaN, an infinity or a date in the future
        # all fall outside it.
        if not -_CLOCK_SKEW_S <= age <= float(ttl_s):
            return None
        value = entry.get("v")
        return value if isinstance(value, dict) else None
    except Exception:  # noqa: BLE001 - unreadable, not JSON, nested too deep to parse: a miss
        return None


def put(namespace: str, k: str, value: Dict[str, Any], ttl_s: Optional[float] = None) -> None:
    """Remember ``value``. Silently does nothing when it cannot, or when the value is too big.

    With ``ttl_s``, entries older than that leave the file in the same write. ``get`` only
    refuses to SERVE an expired entry; without this it stayed on disk until 256 newer ones
    pushed it out, which for most people is never, while the docs said "for 7 days".
    """
    try:
        path = _path(namespace)
        if path is None or not isinstance(k, str) or not _KEY.fullmatch(k) or not isinstance(value, dict):
            return
        if len(json.dumps(value, separators=(",", ":")).encode("utf-8")) > MAX_VALUE_BYTES:
            return
        try:
            entries = _load(path)
        except Exception:  # noqa: BLE001 - a file that cannot be read is replaced, which repairs it
            entries = {}
        now = time.time()
        if ttl_s is not None:
            entries = {name: entry for name, entry in entries.items()
                       if -_CLOCK_SKEW_S <= now - _at(entry) <= float(ttl_s)}
        entries[k] = {"at": round(now, 3), "v": value}
        _save(path, entries)
    except Exception:  # noqa: BLE001 - a full disk or a read-only home costs the memo, not the call
        return


def purge(namespace: str, ttl_s: float) -> int:
    """Remove every entry past ``ttl_s``, and say how many went. 0 for any kind of trouble.

    ``get`` refusing to SERVE an expired entry is not the same as the entry being gone, and
    an entry holds whatever the caller kept -- for the plan cache, the words a person
    dictated. ``put(ttl_s=...)`` clears the expired ones out as a side effect of storing
    something new, which is no help on the runs that store nothing: a shadow run whose
    stored plan already agreed, a plan whose steps looked sensitive, an outage. So a caller
    that is about to do the slow thing anyway calls this on the way past. The file is only
    rewritten when something actually expired, so the usual case costs one read.
    """
    try:
        path = _path(namespace)
        if path is None or not path.is_file():
            return 0
        entries = _load(path)
        now = time.time()
        kept = {name: entry for name, entry in entries.items()
                if -_CLOCK_SKEW_S <= now - _at(entry) <= float(ttl_s)}
        if len(kept) == len(entries):
            return 0
        _save(path, kept)
        return len(entries) - len(kept)
    except Exception:  # noqa: BLE001 - housekeeping never costs the caller the call it was making
        return 0


def drop(namespace: str, k: str) -> None:
    """Forget one entry. Used when what was stored turned out to be wrong."""
    try:
        path = _path(namespace)
        if path is None or not path.is_file():
            return
        entries = _load(path)
        if entries.pop(k, None) is not None:
            _save(path, entries)
    except Exception:  # noqa: BLE001
        return


def _files() -> Dict[str, Path]:
    """namespace -> file, for the files this module could have written and no others."""
    found: Dict[str, Path] = {}
    for path in sorted(directory().glob("*.json")):
        if _NAMESPACE.fullmatch(path.stem) and path.is_file() and not path.is_symlink():
            found[path.stem] = path
    return found


def clear() -> int:
    """Delete every namespace file. Returns how many entries went with them."""
    removed = 0
    try:
        for namespace, path in _files().items():
            try:
                count = len(_load(path))
            except Exception:  # noqa: BLE001 - a corrupt file holds nothing usable; it still goes
                count = 0
            try:
                path.unlink()
                removed += count
            except OSError:
                continue
        for stray in directory().glob("*.json.tmp.*"):      # left by a process killed mid-write
            try:
                stray.unlink()
            except OSError:
                continue
    except Exception:  # noqa: BLE001
        pass
    return removed


def stats() -> Dict[str, Any]:
    """Entry counts and file sizes per namespace. Never a key and never a value."""
    out: Dict[str, Any] = {"schema": SCHEMA, "mode": mode(), "dir": "", "namespaces": {}}
    try:
        out["dir"] = str(directory())
        for namespace, path in _files().items():
            try:
                count = len(_load(path))
            except Exception:  # noqa: BLE001
                count = 0
            out["namespaces"][namespace] = {"entries": count, "bytes": path.stat().st_size}
    except Exception:  # noqa: BLE001
        pass
    return out
