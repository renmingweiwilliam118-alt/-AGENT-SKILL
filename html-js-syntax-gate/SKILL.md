---
name: html-js-syntax-gate
description: Syntax-gate HTML JS with node --check before delivery.
version: 1
author: hermes
license: MIT
metadata:
  tags: [frontend, debugging, verification, html, js]
  related_skills: [frontend-ui-error-probes, dogfood, webapp-testing]
---

# HTML inline-<script> syntax gate

## When to Use
Use before delivering or debugging any HTML file that ships inline `<script>` JS, and before claiming a page or demo "works" or "renders." If you are already past the parse stage and only probing runtime DOM state, use `frontend-ui-error-probes` instead.

Before you claim an HTML/CSS/JS demo or artifact "works" or "renders," gate the JavaScript. The standing user rule is: deliver an artifact that is *actually verified*, never a description of one. A syntax gate is the cheapest reliable proof that the JS even parses.

## Procedure
1. Extract the inline `<script>` body to a standalone `.js` file (regex the `<script>...</script>` block out of the HTML), then run `node --check <file>.js`.
2. If clean, the syntax gate passed. Pair it with a *structural* check so the feature list is proven present, not assumed: every element id the JS references (`getElementById(...)`) exists in the DOM, and the count of effect/section blocks matches the spec.
3. Only after the gate passes, attempt browser/headless runtime verification. If a real browser can't be driven in this moment, say plainly that runtime render was NOT verified — do not let a passing `node --check` stand in for "it works."

## Pitfalls (these cost ~20 minutes in this task class)
- `node --check` reports where the parser **gives up**, not where the bug **is**. A shifted extra/missing `{`/`}` surfaces later as `Unexpected token '}'` several lines *after* the real imbalance. Do NOT chase the reported line. To find the true origin, use a real parser (acorn/esprima) or run it and read the runtime stack — not grep and not the check line.
- **Never hand-roll a brace counter** to locate a JS imbalance. Template literals `${...}` and literal `{`/`}` inside string/comment text make per-line or cumulative counting meaningless: it will report "balanced" while the code is genuinely broken. Two independent hand-rolled scanners (naive cumulative + a string-aware one) both came back wrong here, while `node --check` was the only signal that matched the truth. Trust the real parser, not the homemade matcher.
- Do not make a net-zero edit "to fix" a reported line without re-running the gate — an early compensating imbalance means a +1/−1 edit can look like it changes nothing or makes it worse. Always re-run `node --check` after each fix and confirm the gate flips clean.

## Why this shape
Fast, authoritative, and honest: one reliable gate (`node --check`) + one structural check + an explicit statement of what was *not* verified (runtime render) — instead of burning time on untrustworthy hand-rolled scanners.

## Nearest existing skill
`frontend-ui-error-probes` (runtime headless DOM probing). This skill is its *prerequisite*: if the inline JS doesn't parse, you cannot probe the DOM. If a syntax gate is ever added there, consolidate the two.
