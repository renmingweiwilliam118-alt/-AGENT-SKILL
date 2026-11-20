---
name: long-task-hardening
description: "Use on long tasks: checkpoint, writeback, verify, tier."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent, long-task, checkpoint, context-engineering, verification, skills]
    related_skills: [hermes-skill-library-restore, planning-with-files]
---

# Long-Task Hardening

Disciplines for multi-hour / multi-step agent work (incl. unattended duty runs).
Each rule is imperative + why. Sources: CORAL (arXiv 2610.40350), PILOT (arXiv 2608.x),
AdaMEM (arXiv 2606.05684), ReTTT/ASCENT (agentic test-time training), LangChain
context-engineering notes 2026. Keep this skill itself short — skills rot; audit on use.

## When to Use
- Starting any task expected to run longer than ~10 tool calls or more than 30 minutes.
- Unattended / duty-mode runs where no human is watching for failure.
- Before spawning subagents for mechanical work (tier them, verify independently).

## 1. CORAL checkpoint discipline
- At every milestone, or when context is getting cluttered, write a checkpoint file in the workspace: verified facts, decisions made, next concrete step.
- After compaction or a new session, resume by reading ONLY the checkpoint — never replay the raw transcript.
- Why: context rots; CORAL shows checkpoint + clean reset beats carrying the dirty transcript (8B model, GAIA 42.8%, ~7x fewer input tokens).

## 2. In-run skill writeback (PILOT)
- When a step FAILS and you fix it: patch the lesson into the relevant skill immediately, mid-task — not at the end of the session.
- Lesson = one line: what broke, what fixed it, the rule to follow next time.
- Why: PILOT converts runtime failures into reusable skills in real time; end-of-session writebacks die with the context.

## 3. Independent verification (explore in parallel, falsify independently)
- For consequential code changes or external side effects: spawn a FRESH-CONTEXT subagent (delegate_task) to verify — the main agent must not self-verify its own output.
- Give the subagent: artifact path, explicit acceptance criteria, and the instruction to find reasons it is wrong.
- Why: independent refutation catches self-blindness; the structure behind verified proof-search (generate cheap, judge via an independent kernel).

## 4. Model tiering (selective thinking budget)
- Mechanical steps (scraping, batch ops, transforms, polling): delegate to a cheap/fast model — pin delegation.provider/delegation.model when spawning.
- Deep judgment, root-cause debugging, final design: keep on the frontier model.
- Why: fast/slow adaptive thinking budget — spend compute only where it pays; GPT-6.2/Haiku-class models are built for the cheap lane.

## 5. Offload large results (hard rule)
- Big tool outputs (web dumps, browser extractions, logs) go to a workspace file; keep only the path + a 1-2 line pointer in context.
- Why: Deep Agents pattern — 85% watermark auto-summarize + filesystem offload prevents context rot and keeps cache hits.

## 6. Goal guardrails (unattended tasks)
- At task start, write: success criteria + human-takeover rules + the cheapest way this goal could be faked, and how to rule that out.
- Why: goal-optimizing agents cheat in unanticipated ways; guardrails are the context-engineering answer.

## Notes
- "Demystifying Agent Skills" (8135 trials): skills anchor stable procedure — but they drift and expire. If a skill misfires twice, patch it then (rule 2).
- Text-skill writeback is the deployment-level equivalent of ReTTT/ASCENT test-time learning; if the provider ever exposes LoRA fast-weights, prefer that for repeated task families.
