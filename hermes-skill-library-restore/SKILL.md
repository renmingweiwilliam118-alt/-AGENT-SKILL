---
name: hermes-skill-library-restore
description: "Use when restoring a git skill-library backup into skills/."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, install, restore, backup, git, symlink]
---

# Restore a Skill-Library Backup into Hermes's skills/

## When to Use

Use this when the user points at a git repo that is a **skill-library backup** — a tree of
category directories full of `SKILL.md` trees, often shipping `restore.sh` and/or
`_api_needs.json` — and asks to install / restore / bulk-add those skills into Hermes.
Not for a single skill, and not for authoring new skills (that is `skill_manage`).

A skill-library backup repo is a git tree of **category directories**, each holding many
skill subdirs, every one with a `SKILL.md` (sometimes plus `references/`, `scripts/`,
`assets/`). These repos are built for cross-machine / cross-agent restore (they ship a
`restore.sh` and often a `_api_needs.json` mapping skill → required API key). Restoring
means **merging** the category trees into `$HERMES_HOME/skills/`.

## Procedure (in this order)

1. **Resolve the target from `$HERMES_HOME`, not a hardcoded path.** When a profile is active
   the real home is `$HERMES_HOME` (default `~/.hermes`, on Windows `AppData\\Local\\hermes`).
   Target = `$HERMES_HOME/skills/`. Count existing `SKILL.md` first so you can report the delta.

2. **Clone the repo into the scratch dir** (shallow is fine) — never into the skills dir.
   `git clone --depth 1 <repo> $SCRATCH/lib`

3. **Merge-copy each top-level category dir into `skills/`.** For every `cat/` at the repo
   root: `cp -r "$SCRATCH/lib/cat" "$TARGET/skills/"`. This merges — existing categories
   update in place, new ones are created. **Preserve the category/sub-category layout**;
   do not flatten skills directly under `skills/`, or you break the dedup structure the repo uses.

4. **Materialize any flattened symlinks.** In a symlink-heavy repo, `SKILL.md` files that
   were symlinks on the source become 1-line text files containing only the relative target
   path (Windows `git` does this — see pitfall). Since you copied the targets too, resolve
   each one. Run `scripts/materialize_symlinks.py $TARGET/skills` (or its logic).

5. **Verify.** Run `scripts/verify_skillmd.py $TARGET/skills`. Confirm total `SKILL.md`
   count and that (near-)all have valid YAML frontmatter. A `SKILL.md` that is a single
   relative path with no frontmatter is an un-materialized symlink — go back to step 4. A
   small residual of skills using `description`-only frontmatter (no `name:`) is still valid;
   flag them for review, don't treat as broken.

6. **Report and give the activation note.** Report per-category counts and the delta.
   Tell the user the new set is scanned **at session start** — a Hermes restart or `/new`
   picks it up in the live gateway/desktop. Note that key-bearing skills won't function
   until their API keys are set in `~/.hermes/.env`; read the repo's `_api_needs.json` for
   the skill→key map and list which are missing.

## Pitfalls

- **Git on Windows flattens symlinks into text files.** When a repo dedups skills across
  categories with symlinks (`cat/.x/skills/foo/SKILL.md -> ../../../real/foo/SKILL.md`),
  a Windows `git clone` (or copying a Linux-created tree) leaves them as 1-line files whose
  entire content is the relative path, with no frontmatter. Repair: read that 1 line,
  `normpath(join(dirname, path))`, and if the target exists, copy its content back; resolve
  recursively if the target is itself symlink-text. **Do not treat these as genuinely broken
  skills** — the target exists and is restorable.
- **Verify before declaring success.** A large copy looks done but a batch of symlink-text
  files still counts toward the total. The verify step (frontmatter check) is what catches
  them; trusting the copy count alone is the failure mode.
- **Don't restate the library's catalog as skill content.** This skill is the restore
  procedure, not the contents of any particular backup.

## Support scripts (re-run; both take the skills dir as `$1`, default `$HERMES_HOME/skills`)

- `scripts/materialize_symlinks.py` — find and repair git-flattened symlink-text `SKILL.md`
  files by copying in the target content (supports `--dry-run` and chained symlinks).
- `scripts/verify_skillmd.py` — count `SKILL.md`, check frontmatter, report the
  non-conforming list and per-category totals.
