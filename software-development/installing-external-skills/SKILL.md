---
name: installing-external-skills
description: "Install GitHub repos as Hermes skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, skills, installation, github]
    related_skills: [hermes-agent]
---

# Installing External Skills into Hermes

## When to Use

User says "把这项项目变成技能加给你自己" / "install this repo as a skill" / "add this to your skills" with a GitHub URL or repo name.

## Workflow

### Step 1 — Clone the repo

```bash
cd $TMPDIR && git clone --depth 1 <repo-url> 2>&1 | tail -5
```

If clone fails with SSL/network errors, retry once. If it still fails, try `git clone --depth 1 --config http.sslVerify=false <repo-url>`.

For large repos on flaky networks, prefer a ZIP download over shallow clone: a reset connection frequently leaves a shallow clone with a broken `.git` and an empty working tree, while the codeload ZIP endpoint tolerates retries and lands intact.

```bash
curl -sL --retry 3 --retry-delay 5 -o repo.zip "https://codeload.github.com/<owner>/<repo>/zip/refs/heads/main"
python -c "import zipfile; zipfile.ZipFile('repo.zip').extractall()"
```

Check the default branch via the GitHub API (`api.github.com/repos/<owner>/<repo>` → `default_branch`) before assembling the URL.

### Step 2 — Inspect the structure

```bash
find /tmp/<repo> -name "SKILL.md" | sort
find /tmp/<repo> -type d -name "skills" -o -type d -name "skill"
```

Read every SKILL.md to understand what the repo provides. Check for `references/`, `scripts/`, `templates/` subdirectories.

### Step 3 — Choose a category

Place skills under `$HERMES_HOME/skills/<category>/`. Existing categories:
- `software-development` — coding, debugging, planning, code review
- `design` — UI/UX, branding, visual design
- `productivity` — documents, spreadsheets, notes
- `research` — academic, literature review
- `creative` — art, music, video

If the repo has a single skill, place it directly under the category. If it has multiple skills, create a subdirectory per skill.

### Step 4 — Copy files

```bash
mkdir -p "$HERMES_HOME/skills/<category>/<skill-name>"
cp -r /tmp/<repo>/.claude/skills/<skill-name>/* "$HERMES_HOME/skills/<category>/<skill-name>/"
```

If the repo has a flat structure (SKILL.md at root), copy the whole repo content.

### Step 5 — Verify against a FRESH upstream fetch

```bash
skill_view(name="<skill-name>")
skills_list(category="<category>")
```

Confirm the skill appears in the list and its `SKILL.md` is readable. Then prove completeness — see `references/upstream-layouts.md`: fetch the authoritative file list from the ORIGINAL URL **in this same run**, strip each library's known prefix, diff against the mirrored copy, and copy in every file upstream has that local does not.

## Pitfalls

- **`hermes plugins install` fails on Windows** with `CRYPT_E_REVOCATION_OFFLINE` / schannel errors. Do not retry it — go straight to manual file copy. The plugin installer's certificate revocation check fails when the machine is offline or behind certain proxies.
- **Path translation**: `read_file` is a Windows program — `/tmp` resolves to `C:\tmp`, not the git-bash `/tmp`. Use `cygpath -w /tmp/<path>` to get the correct Windows path before calling `read_file`.
- **Category matters**: skills in the wrong category won't trigger. A debugging skill in `creative` won't fire when the user reports a bug.
- **Don't skip reading SKILL.md**: the description field determines when the skill triggers. If the description is wrong or missing, the skill won't fire when it should.
- **Clean up**: remove the cloned repo from `$TMPDIR` after installation to avoid clutter.
- **NEVER flatten multi-skill packages into one level.** Many upstream repos (claude-skills, Trail of Bits plugins, OpenMontage, marketing-skills, gstack) ship a *package-level shared layer* (`agents/ references/ scripts/ shared/ data/` + docs like `AGENTS.md`, `GLOSSARY.md`) that skills reference via relative paths (`../../references/x.md`, `../bin/y.sh`). Copying only each skill folder into `category/<skill>/` strips that layer and silently breaks hundreds of cross-references. Rule: **mirror the upstream layout** — if skills sit in `<repo>/skills/<cat>/<name>/` with a root shared dir, recreate that nesting under `category/` and copy the shared layer at the same relative depth (verify with a grep of `../` refs before/after).
- **Audit after big installs.** Grep every copied `.md/.py/.sh` for relative refs (`\.\./`, backtick-wrapped `scripts/|references/|assets/` paths), resolve each from the file's own directory, and diff the missing set against the upstream root: missing-but-upstream-has = our leak (fix by copying); missing-in-upstream-too = author's own dead link (do NOT fabricate files to satisfy it).
- **Zip skills**: some repos ship bundled sub-skills as `.zip` (e.g. `c-level-advisor/ceo-advisor.zip`). Unzip them in place during install or they become empty dirs.
- **Never audit by diffing against a cache or an earlier clone.** A local copy produced by a partial/flattened install is missing exactly the same files, so the diff falsely reports zero gaps — you end up declaring success measured with a broken ruler. Fetch the authoritative list fresh from the ORIGINAL URL in the run you audit, then diff.
- **Verify a background batch by counting files actually written, not by exit code.** A batch pointed at a typo'd script path exits 0 while downloading nothing; check the changed-file count before believing the result.
- **Use absolute paths with `cp -r`; never `cp -r . <dest>`.** A background shell can land in an unexpected CWD (home or drive root), and copying `.` silently drags unrelated private app data into the backup.
- **Never delete the upstream source before the mirror is verified.** Cleaning up temp clone/zip-extract directories while the copy is still pending (or failed) wipes the whole mirrored library — the mirror then reads empty and any 'recovery' re-copies nothing. After mirroring, assert the destination counts (file count and SKILL.md count) are non-zero and equal the source counts; only then delete the temp source. Also: assert every `rm -rf` target variable is non-empty and the directory actually exists before running it.
- **Inspect dot-directories before excluding them.** Canonical skills may live in `.agents/skills/`, while `.gemini/`, `.claude/`, `.github/` are generated adapter copies; a blanket `*/.*` exclusion either misses the real source or double-counts adapters. When a repo carries both a canonical root and adapter copies with overlapping names (e.g. 90 skills in `.agents/skills/` plus 49 of those same names duplicated in `.claude/skills/`), count only the canonical root — the inflated total is duplicate adapters, not extra skills.
- **Diff using ONE canonical root, and only one counting method.** Mixing criteria (whole-project file count, reference-path regex, canonical-root file count) produces wildly different 'missing' numbers across rounds of the same audit. Pick the canonical skill root for the library, set-diff relative paths against it, and treat its result as the only truth; see `references/upstream-layouts.md`.
- **Probe both proxy and direct connectivity before a batch**, and retry through the other path when clone/push dies with TLS EOF or connection reset — which path works can flip between sessions.
- **Declare a push 'synced' only by SHA equality, never by exit code.** Loop `GIT_SSL_NO_VERIFY=1 git push origin master` up to ~8 attempts with short sleeps; after each attempt verify `$(git rev-parse HEAD) == $(git ls-remote origin HEAD | cut -f1)`. A push can exit successfully-looking while TLS EOFs mid-transfer, and `ls-remote` confirms what actually landed. TLS EOF and connection resets are transient on flaky networks — retrying through proxy/direct alternately is the fix, not a reason to stop.

## After Installation

Tell the user:
1. What was installed (skill names + count)
2. What each skill does (one line each)
3. The core workflow if the skills form a pipeline
4. Any prerequisites (CLI tools, API keys, Python packages)

Use Chinese if the user has been communicating in Chinese.