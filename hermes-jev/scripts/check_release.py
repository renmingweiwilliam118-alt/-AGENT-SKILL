#!/usr/bin/env python3
"""Refuse to ship secrets or machine-specific paths. Run before every push."""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "api key": re.compile(r"\b(apikey_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35})\b"),
    "home path": re.compile(r"/Users/[a-z][a-z0-9_-]+/|/home/[a-z][a-z0-9_-]+/"),
    "private address": re.compile(r"\b(100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+|192\.168\.\d+\.\d+|[a-z0-9-]+\.ts\.net)\b"),
}
ALLOW = {("tests/test_jevkit.py", "api key")}  # the fake key built at runtime never matches; listed for clarity

_git = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"],
                      cwd=ROOT, capture_output=True, text=True)
files = _git.stdout.split()
# A guard that cannot tell "clean" from "did not run" is worse than no guard: outside a
# git checkout this printed "clean: 0 files" and exited 0, giving a green light to a
# check that scanned nothing. The repo is distributed as a zip, so that case is real.
if _git.returncode != 0 or not files:
    sys.exit("check_release: nothing was scanned (not a git checkout, or git failed). "
             "This is not a pass.")

# Strings that must never ship, read from a file that is NOT in the repo. A real customer's
# name reached a public release inside a test fixture, copied from a live system while
# debugging it. Nothing caught it, because the only pattern this script knew was a home
# path. The list cannot live here: naming what to keep out would publish it.
_DENY_FILE = Path(os.environ.get("JEV_RELEASE_DENYLIST", Path.home() / ".config" / "jev" / "release-denylist.txt"))
_DENY = []
if _DENY_FILE.is_file():
    _DENY = [l.strip().lower() for l in _DENY_FILE.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]

problems = []
unscanned = []
for name in files:
    path = ROOT / name
    if not path.is_file():
        continue
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".pdf"}:
        # "clean" used to cover these silently. A screenshot is where a real profile name
        # or a path is most likely to ship, and no text pattern can see inside one.
        unscanned.append(name)
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for label, pattern in PATTERNS.items():
        if (name, label) in ALLOW or name == "scripts/check_release.py":
            continue
        for match in pattern.finditer(text):
            problems.append(f"{name}: {label}: {match.group(0)[:24]}…")
    lowered = text.lower()
    for entry in _DENY:
        if entry in lowered:
            # Name the file and the rule, never the string: this output lands in CI logs.
            problems.append(f"{name}: contains an entry from the release denylist (#{_DENY.index(entry) + 1})")
if unscanned:
    print(f"NOT SCANNED ({len(unscanned)} binary): {', '.join(unscanned)} - look at these by eye before pushing")
print("\n".join(problems) if problems else f"clean: {len(files) - len(unscanned)} text files")
sys.exit(1 if problems else 0)
