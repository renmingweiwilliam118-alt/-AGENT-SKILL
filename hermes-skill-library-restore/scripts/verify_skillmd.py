#!/usr/bin/env python3
"""Verify SKILL.md integrity in a skills dir.

Counts SKILL.md files, checks each has YAML frontmatter with `name:` and
`description:`, and reports non-conforming files plus per-category totals.
A file whose content is a single relative path with no frontmatter is an
un-materialized git-flattened symlink — re-run materialize_symlinks.py.
Note: a small residual of valid skills may use `description`-only frontmatter
(no `name:`); those are flagged for review, not necessarily broken.

Usage:
  verify_skillmd.py [SKILLS_DIR]   # default $HERMES_HOME/skills
"""
import os
import re
import sys
import collections


def frontmatter_ok(text):
    text = text.lstrip("\ufeff").lstrip()
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return False
    fm = m.group(1)
    return bool(re.search(r"^name\s*:", fm, re.M)) and \
        bool(re.search(r"^description\s*:", fm, re.M))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = args[0] if args else os.path.join(
        os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "skills")
    base = os.path.normpath(base)

    total = 0
    conform = 0
    bad = []
    per_cat = collections.Counter()
    for root, _, files in os.walk(base):
        if "SKILL.md" not in files:
            continue
        p = os.path.join(root, "SKILL.md")
        total += 1
        per_cat[os.path.relpath(p, base).split(os.sep)[0]] += 1
        with open(p, encoding="utf-8-sig", errors="ignore") as f:
            c = f.read(4000)
        if frontmatter_ok(c):
            conform += 1
        else:
            bad.append(os.path.relpath(p, base))

    print(f"TOTAL SKILL.md: {total}")
    pct = (100 * conform // total) if total else 0
    print(f"conform (valid name+description): {conform} ({pct}%)")
    print(f"non-conforming: {len(bad)}")
    for b in bad[:40]:
        print("  ", b)
    if len(bad) > 40:
        print(f"  ... and {len(bad) - 40} more")
    print("\nper top-level category:")
    for k, v in sorted(per_cat.items(), key=lambda x: -x[1]):
        print(f"  {k:<24} {v}")


if __name__ == "__main__":
    main()
