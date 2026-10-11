---
name: strip-project-authorship
description: Use when stripping original author branding from a project.
---

# Stripping authorship & branding from a project

## When to Use
- Before distributing a repackaged / white-labelled build of a cloned open-source project
- When an end-user deliverable must carry no original-author attribution
- Sweeping a whole repo, not just the files you opened in this session

Goal: zero remaining author attribution/branding while keeping legally protective text intact. Works across a whole repo, not just the files you opened.

## Procedure
1. Define the protected set first — what stays: the license body, usage/disclaimer clauses, third-party upstream credits. Everything else author-identifying goes.
2. Sweep every author-identifying line programmatically (Python `re` per file). A header-only regex misses in-code signatures — use a line-level filter that DROPS only lines matching author patterns (`Copyright (c) <name>`, repo/GitHub URL lines, author email, `author=` in pyproject) while keeping the rest.
3. Delete the dedicated authorship artifacts: `.github/FUNDING.yml`, `.github/CODEOWNERS`, ad/banner components, paid-course / 剖析课 / Pro links, GA/analytics snippets, author-intro blocks in docs config.
4. Rewrite the LICENSE copyright line to a neutral project name and drop the author email (both en & zh copies).
5. Strip UI author components (footer, GitHub Star button, license link) and any i18n fields that carry author name/GitHub.
6. Verify end-to-end: compile/import the touched modules, byte-level grep the whole repo for each author identifier (names in both scripts, emails) — expect zero hits, EXCEPT intentional upstream credits (e.g. a forked library).

## Pitfalls
- De-branded ≠ de-licensed: the license body itself (incl. any NON-COMMERCIAL clause) must survive; only author-identifying lines are removed.
- Reuse a small `strip_author_lines(text, patterns)` helper for the sweep so the rule set lives in one place.
