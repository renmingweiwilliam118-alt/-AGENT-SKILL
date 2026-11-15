# Verifying changes to RFlow / shiflow-mini

Run this ladder after any change to agent.py / watcher.py / brain.py / server.py; a step is only "done" when its runner says PASS.

1. `python -m compileall -q . -x ".venv|__pycache__"` — syntax gate over everything.
2. Unit trio (PYTHONPATH=<repo>): `tests/test_reception.py` (16), `tests/test_lifecycle.py` (3), `tests/test_resume_learn.py`. A failure here is always real — but first check the fixture models a NEW guard (e.g. a fake frame image must now be non-uniform to pass a blank-frame gate; solid-color or sparse-dot fixtures get correctly vetoed).
3. `python main.py --selftest` — offline engineering checks (window enum, clipboard, KB, parsing).
4. `python tests/run_all_e2e.py` — spawns ONE isolated server (port 8790, `RFLOW_DATA_DIR=<tempdir>`, `--no-browser`), runs all e2e scripts against it via `RFLOW_TEST_BASE`, then tears it down. Individual scripts accept `RFLOW_TEST_BASE` to reuse a shared instance.
5. Production reload: kill ONLY app.py — the watchdog revives it with the new code within seconds; killing run_forever for a reload disarms duty mode. Verify: 8765 health, checkpoint restored (session watching), heartbeat ticking.

## e2e safety rules

- NEVER auto-pick "the biggest visible window" as a session target — on this machine that can be the user's live WeChat. Select mock-titled windows only, or an explicit `RFLOW_E2E_HWND` override; otherwise fall back to hwnd=0 safe-degradation (session checks that only think+abort).
- Never share the production data dir with a test instance: checkpoint / duty.flag / crash.log / heartbeat are single-slot shared state — a test session can evict the watch session's crash-recovery point or delete the duty flag. `RFLOW_DATA_DIR` isolation is the fix; the write_checkpoint guard (a non-watch session must not evict a live watch session's checkpoint) is the runtime backstop.
- Send-path e2e needs real keyboard focus: on a busy desktop (user typing, IME candidate window up) the act-phase foreground/occlusion guards correctly refuse to click and the test fails — that is the guard working, not a regression. Retest on an idle desktop; the orchestrator retries send tests once for transient occlusion.
- Heavy e2e competes with the production watch for the foreground — run it when the user is not live-testing reception, or their test messages get starved during the run.
- Tests must read artifacts (e.g. `last_shot`) from the session JSON, never glob the local `data/shots` of a different instance (cross-instance reads 404 or grab the WRONG session's screenshot).

## API convention learned the hard way

- GET endpoints that mask secrets (`api_key: "sk-1…(51 位)"`) must treat the masked value as "not provided" on the write path — clients echo the GET body back on POST, and storing the mask as the key makes every later auth call die inside the HTTP header with a latin-1 encode error that surfaces as a baffling "connection failed".

## Debugging a reported reception bug — the decisive pattern

Pull live state, don't guess:
- `/api/sessions` → full `turns` + `trace` (heard / sent / reply / reasoning per step) shows what the agent BELIEVED; counters (rx / replied / fails) show what the watcher did. Mismatches between them (rx+5, no new turns) = the gate chain fired — find which gate by its log line.
- To separate "the image really shows X" from "the prompt anchored on history": re-send the SAME screenshot to the SAME vision model with a NEUTRAL prompt ("describe the latest left bubble verbatim"). Neutral-read disagrees with reception-read ⇒ prompt/history bug (fix brain.py rules); both agree ⇒ capture bug (fix capture/targeting). This single comparison settles every misread dispute faster than any other probe.
