# Full-project e2e suite (`tests/run_all_e2e.py`)

One command runs the whole ladder: it spawns an ISOLATED service instance
(`main.py --port 8790 --no-browser` with `RFLOW_DATA_DIR=<tempdir>`) and runs
every e2e script against its own fake windows, then tears both down and
deletes the tempdir. Takes ~5–8 min; the LLM calls are real (the configured
brain drives them), so it spends tokens.

## Isolation rules (hard requirements)

- **Every spawned test service instance MUST set `RFLOW_DATA_DIR` to a tempdir.**
  `paths.data_dir()` honors the env var in dev too, and `Agent` sets
  `agent.data_dir` so `watcher._data_dir()` doesn't fall back to the repo dir.
  Without it, test sessions write `session_checkpoint.json` / `crash.log` /
  `heartbeat.json` into the PRODUCTION `data/` AND an e2e `unwatch` deletes the
  production `duty.flag` — one suite run silently disarmed 无人值守 (that was a
  real incident class, not a theory).
- e2e scripts accept `RFLOW_TEST_BASE` (e.g. `http://127.0.0.1:8790`) to reuse
  the orchestrator's instance instead of self-hatching on their own fixed
  ports (8791 `e2e_http`, 8792 `e2e_watch`).
- **Target selection: only fake windows** (title contains 模拟客服窗口 / mock)
  or an explicit `RFLOW_E2E_HWND`. NEVER auto-pick the biggest visible window —
  on the production box that is often the REAL WeChat, and an assist-mode run
  will genuinely click and type into it.

## Procedure

1. Fast deterministic gates first: the three unit scripts + `main.py --selftest`
   (see SKILL.md — plain scripts, run the file, not pytest/unittest).
2. `.venv/Scripts/python.exe -u tests/run_all_e2e.py`.
3. Expect the summary: `e2e_test / e2e_sse / e2e_sse2` must pass; send-path
   tests (`e2e_http`, `e2e_watch`) pass on an idle desktop and are retried once
   automatically on failure.

## Why send-path e2e can FAIL on a busy desktop (and why that is correct)

`e2e_http` / `e2e_watch` drive a real fake Tk window with real clicks, typing,
and Enter. The production safety guards (foreground re-check + occlusion
check before `insert_text`) deliberately SKIP the action when something else
holds the foreground or covers the click point — an IME candidate window, a
foreground steal mid-test, or the user actively working. A FAIL of this shape
means the guard protected the user's window; treat it as "rerun later", not a
regression. Verifying the cause: the event stream shows `点击点 (x,y) 被其它窗口遮挡，已跳过`.

## e2e vs the production watch

The suite's send tests fight the production duty watch for foreground: while
a test holds foreground, the production watch's own sends get skipped and its
live customer messages can be starved. Before a full e2e run: either
`rflow.py duty off` (and back on afterwards), or warn the user and run
off-peak. Never run a full e2e pass silently while a real 值守 is armed.

## Timing facts (calibrated)

- The fake Tk window needs ~6 s after appearing before clicks/typing are
  reliable — at ~3.5 s every send failed, at ~10 s everything passed. Give a
  fresh fake window a real delay before running the agent against it.
- VLM first response can exceed 45 s — dialog/message endpoints need
  `timeout=90`, and session-wait loops ≥75 s.
- The orchestrator retries send-path failures once each.

## Ground truth when diagnosing a send-path FAIL

- `targets/fake_window.state.json` `messages[]` is the truth: a
  `who=agent` entry = the reply actually landed.
- `reply_count` counts `_verify_sent`-confirmed sends only; if it disagrees
  with state.json, suspect the verify path (frame-source consistency rule in
  SKILL.md), not the send.
- Real-time event capture recipe: spawn a poller that watches
  `/api/sessions` for NEW sids and subscribes `/api/events?sid=<id>` each.
  Drain in 512-byte chunks and split frames on `b"\n\n"` — an str/bytes mix
  (`"\n\n" in bytes_acc`) kills the drain thread instantly and reads back as
  "zero data frames" (a test bug that looks like a server bug).
- The fake window is created `WS_EX_TOPMOST` at (200,120) 800×660 with a real
  EDIT composer; the send-sweep candidates (x .40–.72, y .82–.94 of the
  window) cover it.
