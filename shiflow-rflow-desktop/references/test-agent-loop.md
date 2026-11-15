# Fake-brain e2e for the 看·想·做 loop + the confirm-vs-abort gate rule

When the configured brain is a placeholder key (or you don't want to pay for / block on a live model), drive the agent loop with a **stub brain** that returns canned `Decision`s, and assert on the emitted events / session state instead of real model output.

## Driving it
- Build an `Agent` with `checkpoint_file` in a tempdir, then `agent.set_brain(<stub>)` where the stub implements `decide(img, ctx) -> Decision` (return `Decision(reply=..., intent=..., needs_human=..., actions=[...])`; `brain.ScriptedBrain` is an in-repo example of a non-live brain).
- Capture emits by passing a `bus`/sink to the agent, or read `Session.trace` / the emitted `thought`/`plan`/`act`/`sent`/`error` payloads. `Session.to_dict()`/`from_dict()` round-trip for resume tests.
- Run assertions without a live model: open a session, run it to a decision, check the draft/plan/needs_human transition, then confirm-plan / abort / send and check the terminal state.

## The gate rule (confirm vs abort) — keep it in any gate you add
- A pre-action gate that blocks on ONE `threading.Event` and can be released by MORE THAN ONE caller (a confirm AND an abort/close) must, **on wake, re-check the abort flag before treating the wake as "confirmed"** — otherwise a cancelled plan is indistinguishable from an approved one.
- Keep both: unblock-by-abort (so 中止 works while blocked at the gate) **and** the post-wake abort re-check.
- The 看/想 steps are time-bounded (`agent._run_bounded`) and poll the abort flag each second, so 中止 works even mid-model-call; the gate is the extra place that must honor the same flag.

## No `httpx` in the venv
- `fastapi.testclient.TestClient` needs `httpx`, which is NOT installed. For route-level checks hit the live app with `curl` (POST JSON via `-d @body.json` to dodge shell quoting); for logic, test the pure functions (e.g. `watch_verdict`, gate state) directly in a venv test script — run with `PYTHONPATH=<repo root>` so `shiflow_mini` imports.
