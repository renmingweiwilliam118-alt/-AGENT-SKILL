# Auditing a Mirrored Library Against Upstream

How to choose the counting method, diff, and verify completeness of a skill mirror. All of this session's false alarms came from mixing counting methods; pick ONE canonical root and diff against it only.

## Choosing the canonical skill root

Per library, use the upstream's authoritative skill directory:

| Upstream layout | Canonical root | Strip prefix when diffing |
|---|---|---|
| `repo/.agents/skills/` (OpenMontage-style) | `.agents/skills/` | `.agents/skills/` |
| `repo/skills/` | `skills/` | `skills/` |
| `repo/plugins/<lib>/` (Trail of Bits style) | `plugins/` | `plugins/` |
| repo root is the skill dir | repo root | none |

Adapter directories are NOT sources of truth: `.claude/skills/`, `.gemini/`, `.github/` are generated copies of the canonical root (often stale or partial). If the same skill name exists in both, count the canonical root only. The inflated count from summing SKILL.md over all dot-dirs is duplicate adapters, not extra skills.

## Exclusion set (never copy, never count)

`.git` `node_modules` `dist` `build` `coverage` `.next` `site` `__pycache__` `.venv` `.github` `.changeset`

Plus the common junk files: `*.zip` `*.lock` `*.log` `*.pyc`.

## Diff recipe (Python, set difference on relative paths)

```python
import os
EXCL = {'.git','node_modules','dist','build','coverage','.next','site','__pycache__','.venv','.github','.changeset'}

def walk(root):
    out = set()
    if not os.path.isdir(root):
        return out
    for r, d, f in os.walk(root):
        d[:] = [x for x in d if x not in EXCL]
        for x in f:
            if x.endswith(('.zip','.lock','.log','.pyc')):
                continue
            out.add(os.path.relpath(os.path.join(r, x), root).replace('\\', '/'))
    return out

upstream = walk(canonical_root)   # strip the layout prefix first if needed
vault    = walk(vault_category_dir)
missing  = sorted(upstream - vault)
print(f'upstream {len(upstream)} | vault {len(vault)} | missing {len(missing)}')
for p in missing[:10]:
    print('   ', p)
```

A non-empty `missing` set is the only red flag; `vault - upstream` files are usually intentional local additions (do not delete them).

## Fresh-fetch rule

Audit in the SAME run that produced the source: fetch the upstream file list or clone from the ORIGINAL URL in that run. Never diff against a cache, an old clone, or the installed copy itself — the mirror was made from upstream, so a partial mirror lacks exactly the same files and the diff falsely reports zero gaps (broken ruler).

## Post-mirror verification (before deleting the temp source)

1. Assert destination SKILL.md count and file count are non-zero AND equal to the source counts.
2. Spot-check one relative reference (e.g. `../references/x.md` or `../../scripts/y.sh`) resolves from its new location.
3. Only then delete the temp clone/zip directory — and only after asserting the `rm -rf` target variable is non-empty and the path exists.

## Push-sync verification

Declare a git push synced only when `$(git rev-parse HEAD) == $(git ls-remote origin HEAD | cut -f1)`; a push command exiting 0 does not prove the transfer completed on flaky TLS links.
