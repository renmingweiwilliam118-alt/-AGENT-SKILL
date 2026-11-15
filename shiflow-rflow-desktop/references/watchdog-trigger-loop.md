# '触发监听' model-driven detection loop (后台看门狗)

Reusable recipe for "watch a window/region, and when the model judges a trigger condition is met, start a reception" — without the user manually pressing 接待. Three parts; each independently testable.

## 1. Pure interpreter (no model, unit-testable) — in `agent.py`
`watch_verdict(decision: dict) -> {"matched": bool, "detail": str}` where `decision` is `Decision.to_dict()`. Rule: matched = `reply` non-empty OR (`heard` non-empty AND `intent` not in {idle, unknown, ""}); `needs_human` → not matched (存疑); `error` → not matched. Keep it a top-level function so a test can import it without a live brain.

## 2. Endpoint — `POST /api/screen/watch` (inside the `create_app` factory)
Body `WatchIn{hwnd, region, target, rule}`. Grab the target: `capture.grab_window(hwnd)` if `hwnd`, else `capture.grab_rect(region, 1000)` if `region`, else `capture.grab_desktop(1000)`. Guard `agent.brain is None` → `ok:false` "模型引擎未配置". Build a `ctx` whose `instruction` states the trigger `rule` and tells the model to keep `intent=idle` when unmet. `decision = await asyncio.to_thread(agent.brain.decide, img, ctx)`. Return `WatchOut{ok, matched, detail, reasoning, reply, heard, intent}` via `watch_verdict`. All capture/model calls on `asyncio.to_thread`.

## 3. UI — 桌面实时监控 card, shown only when `selWin!==null`
Toggle the control's visibility from `updateTargetBanner()` (it already reflects `selWin`). Fields: a 触发条件 input (`#watchRule`) + 开始/停止监听 button + an interval input (default 30s). Poll loop guarded by a `watchBusy` flag so a slow in-flight call can't start the next one. On `matched`: show a 命中 banner; its button calls `runSession()` (NOT a direct POST) so it reuses the existing 计划门/信任开关 flow.

## Cost control (mandatory)
- Each poll = one SiliconFlow call (~5–15s). Default interval 30s, clamp min to 10s. The `watchBusy` re-entrancy guard is required because a slow call must not stack a second one.
- Model-driven auto-action stays behind the standing 计划门/信任开关 spec: 命中 surfaces a confirm banner rather than firing the pipeline — matches "可控".

## Test
- Unit `watch_verdict` on synthetic `Decision.to_dict()` dicts (matched / unmatched / intent=idle / needs_human) — no model needed.
- E2E: `curl -X POST http://127.0.0.1:8765/api/screen/watch -H 'Content-Type: application/json' -d '{"rule":…}'` against the live app with a real brain; expect a structured verdict in ~5s. Send the JSON body via a file (`-d @body.json`) to avoid shell quoting breaking a longer body.