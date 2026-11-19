---
name: skill-router
description: Use when picking which skill to load for a task.
triggers:
  - route a task to a skill
  - which skill should I use
  - find the best skill for this task
  - auto-select / pick a skill
  - skill router
---

# skill-router — auto-discover the right skill for any task

**Why it exists:** there are 2,000+ installed skills and the user does not know (and should not have to know) which prompt words trigger which one. This skill turns that into a deterministic lookup: I run a keyword router over the whole library, get the top ~12 candidates, pick the best, and load it. **I do the searching; the user just states the task.**

## When to use it
- At the start of most substantive tasks (before doing the work ad-hoc).
- Whenever you're unsure which installed skill (if any) applies.
- Skip it for trivially small requests that need no skill.

## Workflow
1. **Extract 3-6 keyword seeds for the task in ENGLISH.** The library's descriptions are mostly English, so translate the task if it's in Chinese/Japanese/etc. Keep the core noun + 1-2 qualifiers (e.g. \"做个 PPT\" → \"powerpoint presentation deck\"; \"把视频教程变成技能\" → \"turn video tutorial into skill\"). Add synonyms for recall (e.g. \"ppt powerpoint slides deck\").
2. **Run the router:**
   ```
   python <skills_dir>/skill-router/scripts/route.py "seed1 seed2 seed3" --top 12
   ```
   - `skills_dir` = `C:/Users/mwr_w/AppData/Local/hermes/skills` on this host (pass `--dir` to point elsewhere, e.g. a skill-library backup repo).
   - Fast (~2s over 2,000 skills), deterministic, no LLM.
3. **Pick the best of the returned list.** This is the judgment call: prefer a skill named exactly for the concrete artifact, or the most specific one. `skill_view(name)` it and follow its instructions.
4. **Report the choice in one line** ("used skill X because …") so the user learns the task→skill mapping.

## Notes / caveats
- The router is a **coarse keyword narrowing** (name > triggers > description, weighted). It gets you from 2,000 → ~12; the final pick is on you (the LLM), not the score alone.
- If the top score is < ~3, no skill is a clear fit — proceed ad-hoc and say so.
- To see the full record for a candidate: `skill_view(name)`, or read `<skills_dir>/<path from router output>`.
