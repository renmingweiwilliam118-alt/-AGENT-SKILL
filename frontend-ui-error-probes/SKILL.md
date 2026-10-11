---
name: frontend-ui-error-probes
description: Probe web UI errors; verify fixes via headless DOM dumps.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [frontend, debugging, web, headless, qa]
    related_skills: [systematic-debugging, verification-before-completion]
---

# Frontend UI Error Probes

Debug and verify front-end behavior WITHOUT needing an interactive browser session. Covers: proving where a script block actually dies (runtime, not syntax), verifying rendering state after JS, and a safe no-op fallback pattern for optional shared modules.

## When to Use

- A page shows clustered UI symptoms — blank/empty region, dead or missing controls, stuck status widget — and the root cause is unknown.
- You must verify a front-end fix but cannot drive an interactive browser (profile locked, headless host, no GUI available).
- You CAN drive Playwright against a running local dev host (a CSS/JS change to check in rendered state — geometry, rAF-driven inline styles, error-free render) rather than only in markup: `references/playwright-live-verify.md`.
- Before claiming any UI fix, when evidence of post-JS-execution DOM state is required.

## Standing rule

Syntax checks are NOT UI verification. Before claiming a UI fix, prove post-JS-execution DOM state (rendered elements, populated text, engine status, probe output) from a headless run or a user screenshot. Syntax-only validation (e.g. `node --check`) cannot catch missing-method / missing-undefined runtime errors, and an uncaught error in one script block silently kills every later top-level statement in that same block — so "my patch looks right" is not evidence the page ever reaches `loadDemos()` / `pollEngine()` / control bindings. The deliverable is a root-cause retrospective (the single error that explains the clustered symptoms) backed by that self-tested headless evidence — never a "try again" hand-off that makes the user the test harness.

## Why this exists (the pattern behind the class)

When MULTIPLE unrelated UI symptoms cluster (empty content region + dead window buttons + stuck "connecting" status), suspect a single uncaught exception earlier in the shared script block rather than N independent bugs. Diagnose the first runtime error first; fix the shared module it touched; only then re-check symptoms.

## Workflow

1. **Inject a runtime probe** (zero side effects, removable):
   - `scripts/inject-probe.js` prepends a probe `<script>` to the target page: captures `error` / `unhandledrejection` into `window.__errs`, then at a fixed delay (≈6s) appends a visible `pre#errdump` node listing all errors + key counters (e.g. rendered item count, status text).
   - The probe output MUST be in the DOM, not just the console: `dump-dom`-based headless capture can only read the DOM.
   - Adjust the two counter selectors in the probe to the page's symptom markers before trusting the dump.
   - Add a boot sentinel to disambiguate the two failure hypotheses: set `window.__BOOT_OK = true;` as the LAST statement of the main script block, and have the probe print its `typeof` value. `undefined` means the script aborted early (an uncaught error above it); `true` with empty/zero counters means it ran but async fetch / `requestAnimationFrame` work simply hasn't settled yet — lengthen the virtual-time budget rather than re-editing the code.
2. **Headless-verify post-JS DOM** (no profile lock, no user interaction needed):
   - `scripts/headless-dump-dom.mjs URL [out.html]` runs Edge headless with a fresh throwaway `--user-data-dir` + `--virtual-time-budget` so all inline scripts settle, then writes the post-JS DOM to a file. Extract the probe node + symptom counters from that file with Python multiline regex — line-based `search_files` patterns fail on `<pre>` multi-line probe content.
   - Repeat after each fix: item counts > 0, status text off the stuck value, probe reports `(no runtime errors)`.
   - When the probe writes JSON into a DOM `<pre>`, dump-dom output arrives HTML-escaped: `html.unescape` the `<pre>` content before `json.loads`, and when the JSON is followed by more DOM text, parse with `json.JSONDecoder().raw_decode` — a greedy `re.search` for `JSON{...}` over-matches the rest of the page.
3. **Fix the shared-module gap**: when a globally-reachable module is created only on a success path (e.g. WebGL/Three init inside a `try`) but accessed from code that runs regardless, make every call site unthrowable. A top-level `window.mod = window.mod || { fn1(){}, fn2(){} }` guard is NOT enough: a later code path can reassign `window.mod` to a partial object missing some methods, and `||` preserves that earlier truthy-but-incomplete value — the original error then still fires. Instead (a) after the guard, force-complete every method you actually call: `["fn1","fn2"].forEach(k => { if (typeof window.mod[k] !== "function") window.mod[k] = function(){}; })`, and (b) route hot calls through a guard wrapper `const modCall = (fn, ...a) => { const f = window.mod && window.mod[fn]; if (typeof f === "function") f(...a); }` so a missing method can never throw and abort the block.
4. **Remove the probe** once the fix is verified, then re-run the headless dump to confirm clean state (probe gone, counters correct).

## No-Playwright headless loop (Chrome/Edge + a stub-injected page copy)

When Playwright is not installed but a headless Chrome/Edge binary is (Windows: `C:/Program Files/Google/Chrome/Application/chrome.exe`, `C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`), run the same post-JS verification with zero browser-automation dependency:

1. **Stub copy:** copy the target page and inject (a) a bridge stub at the top of `<body>` — a plain object whose methods return the page's failure-safe shape (e.g. `{ok:false}`), so long-poll `whenReady`-style loops succeed instantly and the UI renders safe defaults instead of hitting a real backend — and (b) a measurement probe on `load` that, after a fixed delay, writes one `PROBE_DONE <json>` line into a new `<pre>` appended to the DOM.
2. **Run:** `chrome --headless=new --disable-gpu --no-sandbox --virtual-time-budget=12000 --dump-dom file:///<copy> > out.html`. Extract the `PROBE_DONE` line from `out.html` — the dump is HTML-escaped: unescape, then `json.JSONDecoder().raw_decode` (a greedy regex over-matches the rest of the page).
3. **Geometry claims:** for clipping/overflow questions, measure `document.documentElement.scrollWidth - clientWidth` (0 = no overflow) and `getBoundingClientRect()` right edges vs `innerWidth` in the probe — never trust a vision read of a window capture for edge-clipping claims.
4. **Cross-check:** compare headless DOM values against the live app capture at the SAME viewport width; they must agree before a fix is declared.

No-Playwright loop pitfalls:
- file:// iframes cannot be bridged from a host page: `contentDocument` is cross-origin `null`, so a stub injected on a parent page's iframe-`load` event never lands. Stub injection must happen INTO the copy itself.
- The stub must make every method the page calls callable and return the page's failure-safe shape; throwing stubs turn one runtime error into N.
- Chrome headless on Windows: pass ABSOLUTE paths to `--screenshot` (relative paths fail with access-denied), and make the virtual-time budget ≥ 3× the probe delay.

## Pitfalls

- Don't ship probes: they are throwaway diagnostics; a verification pass that forgets step 4 leaves dev tooling in the artifact.
- The virtual-time budget must exceed the probe delay, or the dump captures the pre-probe DOM (node absent, counters missing).
- A fresh `--user-data-dir` avoids profile-lock conflicts with a running browser; never fight for the user's live profile to run a dump.
- One fixed probe delay + one fixed counter set per iteration: re-injecting with different counters each run makes runs incomparable.
- Do not trust screenshots or vision reads for clipping/overflow claims: layered soft `box-shadow` (e.g. `0 24px 48px -26px`) spreads 40px+ past the element border and its falloff reaches the viewport edge, so a vision analysis of a window capture will report cards "cut off at the right edge" when nothing is clipped. Measure instead: probe `getBoundingClientRect().right` vs `innerWidth` and the scroller's `scrollWidth === clientWidth` (equal = zero horizontal overflow). "Content touches the edge" defaults to shadow bleed until geometry says otherwise.

## Related

- `systematic-debugging` (hub) governs the broader root-cause process; this skill is the concrete front-end tooling around it.
- Live-host Playwright verification (rendered geometry, rAF-driven `style` values, empty `pageerror`, and the data-file-restart-vs-HTML-reload rule): `references/playwright-live-verify.md`.
- Windows-side process cleanup needed to reproduce the exact stale-backend symptom: see `windows-process-inspection` skill.
