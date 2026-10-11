#!/usr/bin/env python3
"""Materialize git-flattened symlink-text SKILL.md files.

When a skill-library repo dedups across categories with symlinks and is
cloned/copied on a platform where git does not preserve symlinks (e.g. Windows),
a symlinked SKILL.md becomes a plain file whose whole content is the relative
path of its target (one line, no frontmatter). This script finds those files
and replaces their content with the target's real content (targets were copied
alongside). Idempotent and safe: it only touches files that look like a
flattened symlink AND whose target exists.

Usage:
  materialize_symlinks.py [SKILLS_DIR]        # default $HERMES_HOME/skills
  materialize_symlinks.py --dry-run [SKILLS_DIR]
"""
import os
import sys


def is_symlink_text(stripped, firstline):
    return ("../" in firstline or firstline.endswith("/SKILL.md")) and \
        len(stripped) < 300 and "\n" not in firstline


def resolve(target, self_abs):
    """Follow chained flattened-symlink targets up to 4 levels."""
    for _ in range(4):
        with open(target, encoding="utf-8-sig", errors="ignore") as f:
            tc = f.read()
        ts = tc.lstrip("\ufeff").strip()
        tf = ts.split("\n", 1)[0].strip()
        if is_symlink_text(ts, tf):
            nxt = os.path.normpath(os.path.join(os.path.dirname(target), tf))
            if os.path.isfile(nxt) and os.path.abspath(nxt) != self_abs:
                target = nxt
                continue
        break
    return target


def main():
    args = list(sys.argv[1:])
    dry = "--dry-run" in args
    if dry:
        args.remove("--dry-run")
    base = args[0] if args else os.path.join(
        os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "skills")
    base = os.path.normpath(base)

    fixed = 0
    unresolvable = []
    for root, _, files in os.walk(base):
        if "SKILL.md" not in files:
            continue
        p = os.path.join(root, "SKILL.md")
        with open(p, encoding="utf-8-sig", errors="ignore") as f:
            raw = f.read()
        stripped = raw.lstrip("\ufeff").strip()
        firstline = stripped.split("\n", 1)[0].strip()
        if not is_symlink_text(stripped, firstline):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), firstline))
        if not os.path.isfile(target) or os.path.abspath(target) == os.path.abspath(p):
            unresolvable.append((p, target))
            continue
        target = resolve(target, os.path.abspath(p))
        if not os.path.isfile(target):
            unresolvable.append((p, target))
            continue
        if dry:
            print(f"[dry-run] {os.path.relpath(p, base)} -> {os.path.relpath(target, base)}")
            continue
        with open(target, encoding="utf-8-sig", errors="ignore") as f:
            content = f.read()
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        fixed += 1

    print(f"materialized: {fixed}" + (" (dry-run)" if dry else ""))
    if unresolvable:
        print(f"unresolvable: {len(unresolvable)}")
        for p, t in unresolvable:
            print(f"  UNRESOLVED {os.path.relpath(p, base)} -> {t}")


if __name__ == "__main__":
    main()
