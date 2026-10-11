---
name: hermes-skill-library-restore
description: "Use to restore a git skill-library backup into skills/, or sync the vault↔skills/↔GitHub mirror."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, install, restore, backup, git, symlink, sync, mirror]
---

# Restore a Skill-Library Backup into Hermes's skills/

## When to Use

Use this when the user points at a git repo that is a **skill-library backup** — a tree of
category directories full of `SKILL.md` trees, often shipping `restore.sh` and/or
`_api_needs.json` — and asks to install / restore / bulk-add those skills into Hermes.
It also covers the **reverse** and **three-way** direction: this user keeps the library
mirrored across three places — a git `skill-vault/` working copy, the live
`$HERMES_HOME/skills/` dir, and a GitHub backup remote — and asks to keep them in sync
("sync my new skills to the GitHub library"). The "Reverse Sync" and "Three-way mirror sync"
sections below cover both; the one-way restore procedure is unchanged.
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

## Reverse Sync (local → backup repo)

When the user asks which skills now exist locally but not in the backup, and to push them over:

1. **Diff on `SKILL.md` relative paths.** Compute `skill_md_relpaths(local) - skill_md_relpaths(repo-clone)`
   (each = `category/.../name/SKILL.md`). Content drift is normal; only "present locally, absent in
   repo" is syncable. `git pull` the clone first so the diff is against the current remote, not a
   stale checkout.
2. **Copy each local-only skill dir into the clone** with its full subtree (`references/`,
   `scripts/`, `assets/`) — `shutil.copytree` after removing any existing target. Verify valid
   frontmatter on every one before committing (don't push a broken skill or an un-materialized
   symlink-text file left over from the restore step).
3. **Commit + push.** `git add -A`, commit naming the added skills, `git push`.
4. **Refresh the repo's index/README** (total skill count + per-category table) in the same
   commit — the count goes stale on every add.

## Three-way mirror sync (vault ↔ skills/ ↔ GitHub)

Run when the user wants new local skills backed up to the git vault + GitHub, or a
vault pull propagated into the live `skills/` dir. Goal: the three locations agree.

1. **Normalize the git proxy first.** This user's git has a loopback proxy baked into
   `.git/config` at the **local** scope. `git config --global --unset-all http.proxy`
   does NOT clear it. Before any fetch/push run:
   `for s in system global local; do git config --$s --unset-all http.proxy; git config --$s --unset-all https.proxy; done`
   then confirm `git config --get http.proxy` is empty. Symptom of skipping this: every
   push fails with `Failed to connect to github.com port 443 via 127.0.0.1` even though
   `curl` (no proxy) reaches GitHub fine — git is routing through a dead loopback proxy.
   Only set a proxy inline (`-c http.proxy=...`) if the loopback port is actually up.
2. **Handle fork, don't force.** If `push` is rejected non-fast-forward, the remote has
   commits you lack (often another session pushed). `git pull --ff-only origin master`.
   If that would create a merge (local has commits too), stop and reconcile — never
   `push --force` over the backup.
3. **Push with the multi-retry SYNCED loop**, and gate on SHA equality, not exit code:
   `local=$(git rev-parse HEAD)`; `remote=$(git ls-remote origin master|cut -f1)`;
   declare SYNCED only when `local == remote`.
4. **Propagate in both directions by skill NAME, not by path.** Dedup key is the last
   path segment (the skill folder name). A skill can live under more than one category
   path in one location; copying by relative path creates duplicates. Copy a local-only
   skill into the vault only if its NAME is absent from the vault (and vice-versa for
   vault-only → local). Report the "same name, different path, skipped" set so the user
   sees you deliberately avoided dupes.
5. **Refresh the auto-generated index** (this user ships a `gen_readme.py` that rebuilds
   `README.md` from the tree) before committing, so the committed README matches the
   new skill count; commit the README with the skill files in one commit.
6. **Verify both-way zero-diff:** recount skill names in vault vs local; both "vault-only
   names" and "local-only names" should be empty before declaring synced.

## Pitfalls

- **A loopback proxy at `local` git scope silently breaks every fetch/push** while the
  global scope looks clean. Clear all three scopes (`--system --global --local`) and
  re-check `git config --get http.proxy`; the dead `127.0.0.1` proxy symptom is
  distinguishable from a real network outage by `curl` succeeding with no proxy.
- **Dedup by skill NAME (last path segment), not relative path.** The user's "three
  places consistent" spec is name-consistent, not path-identical; a skill under two
  category dirs is one skill. Copying by path silently doubles it.
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
- **Push is credential-gated; the commit is safe.** A missing write credential (no stored
  git-credential helper, no PAT, no `gh` login) means the commit lands locally and waits. Do not
  fabricate credentials or report the push as done — say the commit exists locally and hand the
  user the exact push command or a credential method (`gh auth login --web` device code, a PAT).
- **Don't restate the library's catalog as skill content.** This skill is the restore
  procedure, not the contents of any particular backup.

## Support scripts (re-run; both take the skills dir as `$1`, default `$HERMES_HOME/skills`)

- `scripts/materialize_symlinks.py` — find and repair git-flattened symlink-text `SKILL.md`
  files by copying in the target content (supports `--dry-run` and chained symlinks).
- `scripts/verify_skillmd.py` — count `SKILL.md`, check frontmatter, report the
  non-conforming list and per-category totals.
