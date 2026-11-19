#!/usr/bin/env python3
"""skill router: rank all installed Hermes SKILL.md against a task's keywords.

Deterministic coarse narrowing (no LLM): name/trigger/description token overlap.
Feed it a handful of English keyword seeds for the task; it returns the top N
candidates WITH enough of each one's function/triggers to judge. The agent then
reads the top 2-3 fully (skill_view) and picks the best on the concrete deliverable.

Usage:
    python route.py "keyword keyword ..." [--top N] [--dir PATH] [--json]
"""
import argparse, json, re, time
from pathlib import Path
from collections import Counter

DEFAULT_DIR = r"C:\Users\mwr_w\AppData\Local\hermes\skills"
STOP = {"the","a","an","to","and","or","of","for","in","on","with","use","used",
        "when","this","that","from","into","is","it","skill","skills"}

def parse_skill(path: Path, base: Path):
    try:
        head = path.open(encoding="utf-8", errors="replace").read(8000)
    except Exception:
        return None
    m = re.match(r"\ufeff?^---\s*\n(.*?)\n---", head, re.S | re.M)
    fm = m.group(1) if m else ""
    name = None
    dm = re.search(r"^name:\s*(.+)$", fm, re.M)
    if dm:
        name = dm.group(1).strip().strip('"\'')
    desc = ""
    dl = fm.find("description:")
    if dl != -1:
        block = fm[dl + len("description:"):].strip()
        if block[:1] in (">", "|"):
            lines = []
            for line in block[1:].splitlines():
                if re.match(r"^\S+:", line):
                    break
                lines.append(line.strip())
            desc = " ".join(x for x in lines if x)
        else:
            desc = block.split("\n", 1)[0].strip().strip('"\'')
    triggers = []
    tm = re.search(r"triggers:\s*\n((?:\s+-\s+.*\n?)+)", fm)
    if tm:
        triggers = [re.sub(r"^\s*-\s*|\s*$|['\"]", "", l).strip()
                    for l in tm.group(1).splitlines() if l.strip().startswith("-")]
    body = ""
    if path.stat().st_size > 8000:
        try:
            body = path.open(encoding="utf-8", errors="replace").read(20000)
        except Exception:
            pass
    usewhen = " ".join(re.findall(r"Use when[^\n.]+", body))
    desc = f"{desc}. {usewhen}".strip()
    try:
        rel = path.relative_to(base).as_posix()
    except ValueError:
        rel = str(path)
    return {"name": name or path.parent.name, "desc": desc, "triggers": triggers, "path": rel}

def load_all(skills_dir: Path):
    out = []
    for p in skills_dir.rglob("SKILL.md"):
        parts = p.relative_to(skills_dir).parts
        if parts and parts[0] in (".hub", ".locks"):
            continue
        if ".git" in parts:
            continue
        s = parse_skill(p, skills_dir)
        if s:
            out.append(s)
    return out

def tokenize(s):
    return [w for w in re.findall(r"[a-z0-9]{2,}", s.lower()) if w not in STOP]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="English keyword seeds for the task")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--dir", default=DEFAULT_DIR)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    skills = load_all(Path(a.dir))
    qtok = Counter(tokenize(a.query))
    qset = set(qtok)
    phrases = re.findall(r"[a-z0-9]{3,}[a-z0-9\-]*[a-z0-9]{2,}|[a-z]{5,}", a.query.lower())

    scored = []
    for s in skills:
        name_toks = set(tokenize(s["name"]))
        trig_toks = set(t for tr in s["triggers"] for t in tokenize(tr))
        desc_toks = set(tokenize(s["desc"]))
        hit_name = qset & name_toks
        hit_trig = qset & trig_toks
        hit_desc = qset & desc_toks
        ph = sum(1 for p in phrases if p in s["desc"].lower())
        score = 3*len(hit_name) + 2*len(hit_trig) + 1*len(hit_desc) + 0.5*ph
        if score <= 0:
            continue
        hits = sorted(hit_name, key=lambda t: -qtok[t]) + [t for t in hit_trig if t not in hit_name]
        s2 = dict(s)
        s2["score"] = round(score, 1)
        s2["hits"] = hits[:6]
        scored.append(s2)
    scored.sort(key=lambda x: -x["score"])
    top = scored[:a.top]

    if a.json:
        print(json.dumps(top, ensure_ascii=False, indent=2))
        return
    print(f"{len(skills)} skills scanned in {time.time()-t0:.1f}s; {len(scored)} matched; top {len(top)}:")
    print("Read the top 2-3 FULLY (skill_view) before committing; pick on the concrete deliverable, not the score.\n")
    for i, s in enumerate(top, 1):
        print(f"{i:>2}. [{s['score']:>5}] {s['name']}")
        print(f"      path: {s['path']}")
        print(f"      hits: {', '.join(s['hits']) or '-'}")
        if s.get("triggers"):
            print(f"      triggers: {'; '.join(s['triggers'][:6])[:180]}")
        print(f"      function: {s['desc'].replace(chr(10),' ')[:280]}")
        print()

if __name__ == "__main__":
    main()
