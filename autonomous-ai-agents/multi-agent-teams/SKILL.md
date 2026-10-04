---
name: multi-agent-teams
description: "Compose Hermes bot groups and multi-agent dev pipelines."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, multi-agent, group-chat, bots, kanban, delegate-task, coordinator]
    related_skills: [hermes-agent]
---

# Multi-Agent Teams

Use when you need to coordinate multiple Hermes profiles/bots to work
"together" — a development team, a decision group, a pipeline of
specialists, or "how do I make these N bots actually collaborate."

Covers: picking the right orchestration primitive (group chat vs kanban vs
delegate_task), the group-chat member cap, the coordinator pattern that
scales past the cap, shared-code landing so bots don't clobber each other,
and how to size the discussion roster.

## When to Use
- "Build me a 6-person dev team out of my bots" / "make these agents work together"
- "Group chat with my bots" / "can more than N join a room?"
- Deciding between a discussion group, a work queue, or fan-out delegation
- Diagnosing why a group's bots "aren't replying"

Don't use for: single-bot work, or pure provider/credential setup (that's the
`hermes-agent` skill → its `providers-and-models.md` reference).

## Choosing the primitive (decision table)

| You need… | Use | Why |
|---|---|---|
| A bounded **discussion/decision** group (≤ cap) | **Group chat** (Bots tab / `groups.create`) | Humans + bots see one thread; room is persistent, events replayable, approvals via `groups.approve` |
| Durable **work queue** across profiles, auto-dispatched | **Kanban** (`hermes kanban`, dispatcher in gateway) | Cards survive process exit; dispatcher claims + spawns assigned profiles; auto-blocks after `failure_limit` |
| Fan-out many subtasks **right now**, in parallel | **`delegate_task`** | No roster cap, isolated contexts, results return as a new turn; but NOT durable (dies with parent) |
| Long-running autonomous missions, hours | **Spawned `hermes` processes** (tmux/PTY) or `cronjob` | Outlive the parent loop |

Key rule: **the group-chat cap is ~6 members.** "More than 6" collaboration is
not "a bigger group" — it is a group **plus** delegation/kanban fanning out to
the rest. One group = one *stage*, not one monolith.

## The 6-slot "decision chain" team
A software product's decision chain is: what to build → how → who does how much
→ how to verify → how to ship → how to not break. Six slots map to six gates:

| Slot | Role | Owns the gate |
|---|---|---|
| 1 | Product | the spec / acceptance criteria ("do the right thing") |
| 2 | Software architect | module boundaries, contracts, selection ("architecture holds") + **coordinator** |
| 3 | Senior dev (full-stack) | main implementer |
| 4 | Test / QA | acceptance + gate ("may it merge") |
| 5 | DevOps | CI/CD, deploy, monitor ("may it ship / roll back") |
| 6 | Code reviewer | final quality gate ("no regression") |

Front-end / back-end / DB / security / mobile writers are **execution** roles:
pull them **out of the group** and have the architect **delegate** to them on
demand. The group holds *decision rights*; execution scales via delegation. This
is what keeps a group from being 6 voices over-talking each other, burning
tokens, and writing conflicting files.

## Coordinator pattern (scales past the cap)
- Name one bot **coordinator** (architect is the natural pick — it already
  owns the contract decisions).
- In the group, **@ only the coordinator per turn**; it does the split, then
  hands concrete work to execution bots via `delegate_task` (serial or bounded
  parallel). Others stay idle unless @-mentioned.
- One message per gate, not 6 concurrent replies — see the token note below.

## Shared-code landing (the precondition for "working together")
Bots are **isolated profiles**: separate sessions, cwd, memory. They do NOT
share a repo automatically. For real joint development:
- Point every participant's session cwd at **one shared project dir** (e.g.
  `~/projects/<name>`), and use **git as the merge arbiter** — split work by
  non-overlapping modules/dirs so two bots never write the same file.
- Without this, "collaboration" is just 6 independent agents that can't see
  each other's output.

## Token / cost note
A group turn = N bots each running a full inference pass. **Don't 6-way
parallel-reply.** Open groups only at the gates (spec, architecture, verify,
ship); run the in-between code-writing via delegation (subagents). Fewer
concurrent inference bursts also avoids the rate/quota 401s documented in
`references/group-chat-troubleshooting.md`.

## Pitfalls
- **"Make a bigger group" is not a fix.** The ~6 cap is on group chat; the
  escape hatch is coordinator + delegation + kanban, never N+1 members.
- **Everyone in the group writing code = conflicts + 401 bursts.** Keep the
  group for decisions; delegate execution. Bots don't share a repo unless you
  wire a shared dir + git.
- **Group "not replying" is usually a credential, not a group bug.** See
  `references/group-chat-troubleshooting.md`.

## Verification
- `groups.create` lists the intended members; send one message and confirm a
  signed reply lands back in the room (mechanism works).
- For delegation: a coordinator turn returns child summaries that actually
  ran (not fabricated) — check a verifiable handle (path/URL), not just "done."
