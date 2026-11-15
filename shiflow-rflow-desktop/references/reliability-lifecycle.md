# Reliability & business layer (`message_lifecycle.py` + P2 UI)

Added by P1 (reliability skeleton) + P2 (business IA). All **stdlib, zero new deps**. Code lives in `shiflow_mini/message_lifecycle.py`; wired into `watcher.py` (trigger points) and `server.py` (endpoints). Distilled here so a session editing agent/watcher/server knows this layer exists and what invariants protect it.

## Subsystems (one module)
- **ReceptionStore** — one structured record per reception (`ReceptionRecord`, a dict subclass, 12 fields + `state_history`), persisted `data/message_lifecycle/<rid>.json`. `recover_unfinished()` returns every non-terminal record → crash-recovery. Dedup fingerprint file `_verified.json`.
- **ControlState** — global emergency-stop + per-contact takeover locks, persisted `data/control.json`. `send_allowed(contact) -> (bool, reason)` is THE pre-send gate.
- **CustomerStore** (P2) — customer CRM panel, persisted `data/customers.json`. **Stores ONLY user-entered fields** (`note / tags / source / intent / need_summary / followup`); `first_seen`/`last_contact` are factual event timestamps ("a reception for this name occurred"), never model-inferred PII. `upsert(name, fields)` whitelists to `CustomerStore.FIELDS` and preserves tags you don't resend.

## State machine (string constants)
`NEW → RECOGNIZED → ANALYZED → GENERATED → PENDING_SEND → SENT → VERIFIED`; exceptions `RETRY_PENDING / NEEDS_HUMAN / FAILED / IGNORED`. `TERMINAL = {VERIFIED, FAILED, IGNORED, NEEDS_HUMAN}`; `_IN_PROGRESS` = the rest. `finish()` derives state from `verified / sent / fail_reason` if not given.

## The two invariants (each prevents one of the two worst bugs)
1. **Lock a dedup/ACK fingerprint ONLY on a verified send.** `last_replied` / message-hash / `reply_count` update **only when `send_ok=True`** (`_verify_sent` confirmed the screen actually changed after `press_enter`). On a failed send: bounded immediate retry + re-kick on a stable screen. Symptom if you lock on attempt: "回两句就哑" — a transient fail permanently poisons the fingerprint so dedup skips that line forever.
2. **Gate EVERY send path behind `ControlState.send_allowed`, not just the main trigger.** The main trigger AND the periodic `_kick_unanswered` re-kick AND the retry path must all check the gate. An emergency-stop that still lets the periodic kick fire is not a real stop — "急停 = 真停" was violated until the kick + retry paths were gated.

## Endpoints (`server.py`, all inside `create_app(...)`)
- `GET  /api/lifecycle/control` → `{emergency_stop, taken_over{...}}`
- `POST /api/lifecycle/stop` `{on, note}` — global emergency-stop toggle
- `POST /api/lifecycle/takeover` `{contact, on}` — per-contact takeover lock
- `GET  /api/lifecycle/records?limit=N` → `{count, records[], unfinished[]}`
- `GET  /api/receptions` — finished receptions (transcript summaries for the UI list)
- `GET /api/customers`, `POST /api/customers` `{name, …fields}` — CRM (P2); POST 400s without `name`

## Gotchas that cost time
- **Module-level `_cache` singletons outlive the backing file.** `get_store(base)` / `get_control(base)` / `get_customers(base)` each cache one instance keyed by `abspath(base)` in a module-level `_cache` dict, shared by server endpoints and the watcher. **Deleting `data/customers.json` or `control.json` does NOT reset the running process's in-memory state** — the cached store still holds it and re-writes the file on the next mutation. To reset to disk truth, **restart the app**. In unit tests, drive the stores against a `tempfile.mkdtemp()` base, never the real `data/`, and remember two `get_*` calls with the same base return the same cached instance.
- **New backend routes require an app restart, not just a reload.** `index.html` is served per-request (reload picks up UI edits), but `server.py` loads at process start — add a route, and the *currently running* `app.py` still 404s it until you kill + relaunch (a quick curl of the new endpoint returning 404 = stale process, not a routing bug).
- **Post Chinese/JSON bodies via a temp file + Python urllib, not bare `curl -d` in MSYS bash.** Chinese + JSON via `curl --data` in git-bash mangles quotes ("error parsing the body") and native `curl` can't read MSYS `/tmp` paths; use `.venv\Scripts\python.exe` + `urllib.request` to exercise the endpoint end-to-end.
- **Two re-trigger paths must not reset each other's retry bound.** When a line is unsendable (WeChat on the list-view with no input box, window occluded, etc.), the bounded 重发点 kick (`_kick_unanswered`, capped at `unanswered_max`) AND the stable-screen OCR backstop can BOTH fire on the same line. If the backstop re-enters the same settlement that resets `_unanswered_kicks=0`, `unanswered_max` is never reached → `rx`/`fail_count` climb forever on one line (live symptom: both counters ticking up every poll, `status` stuck `watching`). Make ONE path own the retry: gate the backstop on the 'retry-in-progress' marker (`_unanswered_msg`) so it stands down while the kick owns the line. On bound-exhaustion formally abandon that line: clear `_unanswered_msg` (so NEW messages still trigger the backstop) AND lock THAT specific text's hash (so the same failed line does not re-trigger). Stays consistent with invariant #1 — 'lock the fingerprint only on a confirmed send' governs each *attempt*; on *final give-up* you DO lock the specific text, bounded, not forever.

## P2 UI wiring (`index.html`)
- **4-group nav**: 工作区(工作台 / 客户会话 / 客户管理) · AI 中心(对话中心 / 智能体 / 知识中心 / 自动化工作流 / 任务中心) · 分析(接待记录 / 数据分析) · 系统(运行监控 / 模型管理 / 设置与关于).
- **接待记录** page = the control bar (急停 / 接管 buttons → `/api/lifecycle/*`) + lifecycle records + finished receptions.
- **客户会话** = 3-column (client list / chat bubbles + 人工接管 button + AI toggle / editable customer panel), sourced from `/api/receptions` + `/api/customers` + `/api/lifecycle/control`.
- **客户管理** = list + editor → `/api/customers`. **数据分析** = CSS/SVG charts (7-day trend bars, auto/manual ratio, frequent client lines, KB hit-rate) from `/api/receptions` + `/api/lifecycle/records` + `/api/stats` — **no fabricated numbers; every chart has a friendly empty state when there's no data yet.**
- Every `index.html` JS edit: `node --check` the extracted `<script>` (see `html-js-syntax-gate`), and verify nav↔view alignment (every `data-view` has a matching `id="view-<v>"` section) + tag balance (div/section open=close).
