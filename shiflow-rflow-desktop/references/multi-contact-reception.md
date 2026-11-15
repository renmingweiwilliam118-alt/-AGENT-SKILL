# Multi-contact reception — the sidebar-unread path

When WeChat delivers a message from a contact whose conversation is NOT the open one (a brand-new contact, or any non-open chat), the only evidence is in the LEFT conversation list: an unread badge (~RGB #FA5151 → r>180, g<120, b<120), a rewritten preview line + timestamp on that row, or the row re-inserting at the top of the list. The open conversation band does not change at all — any mechanism watching only the band is structurally blind to this event. THREE layers must all know about it; each missing layer has its own symptom (table at the end).

## Layer 1 — watcher trigger: watch the list strip alongside the band

- ONE `snapshot()` grab, TWO crops: the message band (primary, x from ≈28 % of width) + a list strip over the rows only — skip the icon rail (~6 % left) and the search/toolbar header (~8 % top). Working fractions on an 800 px-wide WeChat grab: `WATCH_SIDE = (0.065, 0.08, 0.28, 0.92)`. Stash the strip crop on the session (`s._side_img`) — zero extra capture cost.
- Own baseline dict (`_side_base`) + `side_threshold`, diffed with the same `capture.changed_ratio`. `set_baseline`/`reset` must refresh BOTH baselines from the SAME poll crops, else a sidebar event re-fires every poll; a strip-size change (window resize) → relearn the side baseline, never diff across sizes.
- OR the side trigger into the existing gate (`if diff < threshold and not side_trig`) so debounce / fast-path / cooldown are shared — do not build a parallel trigger path. Give sidebar triggers their own log line (e.g. 左侧会话列表出现新未读) so the path is observable live.

## Layer 2 — vision prompt: the left list is scanned FIRST

- A badge on a row OTHER than the open conversation ⇒ this round outputs ONLY `click` on that row + `wait ~1 s`, with `heard=null` / `reply=null` — NEVER guess a reply from the row preview text; the NEXT round reads the real message and answers.
- Multiple unread → click the topmost (newest) row. Skip non-human rows: 订阅号消息 / 腾讯新闻 / 文件传输助手 / 系统通知 / 邮件提醒. A friend-request panel (接受/拒绝 buttons, no input box) → click 接受 first, greet next round.
- Same flow covers the no-conversation-open case (empty right pane): click the unread row, THEN type.

## Layer 3 — post-DECIDE gate: strip sends, never navigation

The `no_new_msg` screen-diff gate (current band vs `_answered_img`, ≈0.02–0.025) fires no-new-message exactly when the badge is the only change (a badge is ~2 % of the band). It must remove ONLY `type_text`/`press_enter` and KEEP `click`/`wait` — otherwise the model correct open-the-conversation decision is silently erased and the contact is never opened.

## Settlement

`_tried_send` counts `type_text`/`press_enter` ONLY. A round that opened a conversation and sent nothing is a normal IGNORED settle (no retry, no re-kick); counting bare clicks as send attempts turns every harmless sidebar-triggered open into bounded-retry + re-kick loops that burn model calls.

## Threshold calibration — against the REAL window, never guessed

1. Grab a live frame at the watcher capture width; crop the proposed strip; verify the strip covers the list: count badge-colored pixels (a real window with any unread shows hundreds) and/or read the column-brightness profile (avatar column darker, text column lighter).
2. Measure idle noise: two grabs a few seconds apart → expect ≈0.000–0.001 (timestamps tick slowly).
3. Synthesize the candidate events ON the real frame (PIL draw onto a copy) and measure each with `capture.changed_ratio`:
   - badge + preview-line repaint (the common case): ≈0.015–0.02;
   - entry re-inserted at top (whole strip shifts one row-height): ≈0.3–0.5;
   - badge alone (dot, no text change): ≈0.001 — BELOW threshold; acceptable only because a real message ALWAYS rewrites the row preview too, i.e. the threshold rides on the preview change, not the dot.
4. Pick the threshold with ≥2× separation from BOTH idle noise and the smallest real event. Working value: `side_threshold = 0.008` (vs noise ≤0.001, common event ≈0.017).

## Symptom → missing layer

| Symptom | Missing layer |
|---|---|
| Run never fires, `rx` flat while the badge sits in the list | 1 — trigger strip |
| Fires but `heard`/`reply` null every round; stares at the open conversation | 2 — prompt unread-scan rules |
| Trace reasoning says it clicked, but no click ever lands / contact never opens | 3 — gate wiping navigation clicks |

## Live verification

Regressions green; then with a conversation open, send a message from a DIFFERENT contact → sidebar log line → row click → NEXT round answers; `rx`/`reply` climb. Negative: minutes of idle produce no sidebar re-triggers (a too-low threshold shows up as constant re-triggers resolving to IGNORED settles).
