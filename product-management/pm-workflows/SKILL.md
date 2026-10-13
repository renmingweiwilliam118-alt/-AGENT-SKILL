---
name: pm-workflows
description: Router for 6 PM workflow commands (discover, strategy, plan-roadmap, prioritize, write-prd, leadership-transition). Use when the user wants a multi-skill PM workflow rather than a single framework.
---

# PM Workflows (6 command chains)

Upstream `deanpeters/Product-Manager-Skills` ships 6 "commands" — lightweight
orchestrations that chain 2-4 of the 77 skills in this category. This router
picks the right chain for what the user actually wants, then executes it skill
by skill. Each step skill lives in `product-management/<skill-name>/`.

## How to run

1. Match the user's request to one chain below (or skip a chain step if the
   user already supplied that input — pass it through, don't re-ask).
2. Load each step skill with `skill_view("product-management/<name>")` in
   order, and execute it.
3. Carry each step's output into the next step as its input.
4. Report progress step by step; one step at a time.

## Chains

### /discover — structured discovery flow
Problem framing -> opportunity mapping -> validation plan.
Steps: `discovery-process` -> `problem-framing-canvas` -> `discovery-interview-prep`
Use when: user has a problem/opportunity/feature area and needs to validate
it before building.

### /strategy — build product strategy
Positioning -> opportunity -> roadmap decision.
Steps: `product-strategy-session` -> `positioning-workshop` -> `problem-statement`
Use when: user needs strategy-level direction (market, positioning, bets),
not a single artifact.

### /plan-roadmap — sequenced roadmap
Strategy + validated opportunities -> sequenced roadmap with tradeoffs.
Steps: `roadmap-planning` -> `epic-hypothesis` -> `prioritization-advisor`
Use when: user has goals + candidate initiatives and needs ordering and
horizons.

### /prioritize — pick the next work
Right prioritization method for the context, investment sizing.
Steps: `prioritization-advisor` -> `feature-investment-advisor` -> `acquisition-channel-advisor`
Use when: user has a list of candidate initiatives and needs a ranked
shortlist with build/no-build calls.

### /write-prd — decision-ready PRD
Problem framing -> requirements -> story scaffolding.
Steps: `prd-development` -> `problem-statement` -> `proto-persona`
Use when: user needs an engineering-ready PRD document for a feature or
change.

### /leadership-transition — PM -> Director -> VP/CPO
Role-fit diagnostics and onboarding plan for the move.
Steps: `altitude-horizon-framework` -> `director-readiness-advisor` -> `vp-cpo-readiness-advisor`
Use when: user is transitioning roles and wants a readiness + onboarding plan.

## Single-skill fallback

If the request matches one of the 77 skills directly (e.g. "swot", "tam-sam-som",
"user-story"), don't run a chain — `skill_view("product-management/<name>")`
that one skill and use it. The chain is only for multi-step requests.
