---
name: hermes-self-evolution
description: >
  Evolve and optimize Hermes Agent skills, tool descriptions, and system prompts
  using DSPy + GEPA (Genetic-Pareto Prompt Evolution, ICLR 2026 Oral). Reflective
  evolutionary search that reads execution traces, proposes targeted mutations,
  evaluates candidates, and ships the best variant through human review.
  No GPU training; everything is API calls (~$2-10 per run). Use when the user
  says "evolve this skill", "optimize my skill", "improve the prompt", "self-evolve",
  or asks to make a skill better through measured evaluation.
license: MIT
---

# Hermes Agent Self-Evolution

The engine lives at `C:\Users\mwr_w\skills-repo\hermes-agent-self-evolution` (evolved
copy of [NousResearch/hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution)).
It uses DSPy + GEPA: it reads execution traces to understand *why* a skill fails,
mutates the SKILL.md text, evaluates the candidate against an eval dataset, and
keeps the best variant. Guardrails are built in.

## When to use

- The user asks to improve/optimize an existing skill or prompt
- A skill repeatedly produces weak results and the user wants data-driven improvement
- The user explicitly says "evolve", "self-evolve", "GEPA", or "optimize with traces"

Do NOT use for: writing a brand-new skill from scratch (use the writing-skills skill),
or one-off prompt tweaks (edit the file directly).

## Setup (first run)

```bash
cd C:/Users/mwr_w/skills-repo/hermes-agent-self-evolution
pip install -e .            # pulls dspy>=3.0, openai, pyyaml, click, rich
export HERMES_AGENT_REPO=C:/Users/mwr_w/AppData/Local/hermes   # or the source repo
```

Requires an LLM API key for the GEPA optimizer (OpenAI-compatible endpoint).
One optimization run costs roughly $2-10 in API calls. Confirm cost expectations
with the user before running more than ~10 iterations.

## Evolving a skill

```bash
# synthetic eval data (fast, no session history needed)
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source synthetic

# real session traces (higher signal, needs sessiondb)
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source sessiondb
```

Where `--skill` points to a skill name the optimizer can locate (SKILL.md).
The target skill directory should be discoverable from `HERMES_AGENT_REPO`
or pass an explicit path if the CLI supports it.

## Guardrails (non-negotiable)

Every evolved variant must pass ALL of these before shipping:

1. **Test suite** - `pytest tests/ -q` passes 100%
2. **Size limit** - evolved SKILL.md stays <= 15KB
3. **Caching safety** - no mid-conversation changes (evolution happens offline)
4. **Semantic preservation** - variant must not drift from the original purpose
5. **Human review** - the result is a diff/PR-style proposal, NEVER a direct
   overwrite. Present the diff to the user and get sign-off before writing the
   evolved SKILL.md back to `C:\Users\mwr_w\AppData\Local\hermes\skills\`

## Workflow

1. Pick the target skill (ask which one if ambiguous)
2. Confirm eval source (synthetic vs sessiondb) and iteration count
3. Run the optimizer; watch the fitness curve
4. The optimizer emits the best candidate + its eval scores in `reports/`
5. Run the guardrail checks (tests + size + semantic diff)
6. Show the user a before/after diff of SKILL.md
7. On approval: write the new version into the live skills dir AND the skill-vault
   backup (`C:\Users\mwr_w\skill-vault`), commit + push the vault
8. Log what improved (score delta) so the next evolution has a baseline

## What it optimizes (phases)

| Phase | Target | Status |
|---|---|---|
| 1 | Skill files (SKILL.md) | implemented |
| 2 | Tool descriptions | planned |
| 3 | System prompt sections | planned |
| 4 | Tool implementation code (Darwinian Evolver) | planned |
| 5 | Continuous improvement loop | planned |

Only Phase 1 is ready today. If the user asks to evolve tool descriptions or
system prompts, say those phases are not implemented yet and fall back to
manual editing guided by traces.

## Pitfalls

- GEPA is trace-driven: with zero real sessions, use `--eval-source synthetic`
  and keep iterations low, then rerun with sessiondb once real history exists.
- Do not run evolutions for many skills in one sitting; cost compounds.
- The optimizer can overfit to the eval dataset. Always spot-check the evolved
  SKILL.md by reading it, not just by its fitness score.
- If a variant scores higher but reads worse or drops key rules, reject it even
  if the number is up - semantic preservation gate wins.
