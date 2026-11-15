# Vision chat replies: 分清谁在说话 · 不重复回答 · 提速

Applies to the 看·想·做 reception loop where 想 (`brain.decide`) reads a chat screenshot and must answer the OTHER party. Three failures cluster here and share one cause: the model is never told how a chat UI encodes who spoke, so it reads its own sent message back as the customer's line and answers itself.

## 1. Speaker attribution — put it in the system prompt
Add an explicit block above the JSON schema:
- The other party's messages sit **left** with neutral (grey/white) bubbles; the app's own sent messages sit **right** and are **coloured** (green/blue/theme).
- `heard` may ONLY be the other party's **newest** left-side line, quoted verbatim. Never a right-side bubble, never the previous assistant turn.
- If the last message in the conversation is right-side/ours, set **both `heard` and `reply` to null** — nothing new to answer.
- When the other party sent several lines, `heard` = the newest one only, not a concatenation.

Without these rules a 32B-class VL model reliably reports its own reply as `heard` and re-answers it.

## 2. Don't answer the same message twice
Model-level "don't repeat" is not enough, and **the model's `heard` cannot be the primary gate**: it often returns `heard=null` together with a non-null `reply`. `last_replied` then never gets set, dedup never fires, and the run re-thinks and re-sends the same answer every ~10 s (symptom: the UI sits on 「想」 and no new reply appears).

Primary gate — screen change since the last send:
- After a reply is actually sent (`send_ok=True`), **re-capture the screen** via `grab_window` and update `Session._answered_img` to the **post-send** image (the reply bubble has appeared in the chat; the pre-send image is stale and would make the next watcher trigger see the reply's appearance as a "new message" → duplicate reply).
- On the next 想, diff that region against the fresh capture: `< ~0.025` ⇒ **no new message** → log it, force `reply=None, actions=[], stop=True`, and do **not** call the model.
- Region changed ⇒ allow the reply **even when `heard` is null**, so a new customer line is never dropped just because attribution was fuzzy. (A message already on screen when the session opens is not a *change* — run once on open, see §5.)

Second net — text fingerprint (only meaningful when `heard` is present):
- `_norm(text)` strips whitespace and ALL punctuation (including ？ and !) and lowercases — punctuation-variants ("多少钱" vs "多少钱？") collapse to ONE fingerprint, which matches the user's preference (a re-send with a different ？! must not re-trigger an answer). Trade-off: a message whose entire content is punctuation normalizes empty, and that residual falls to the last-4 reply-dup guard; do NOT re-add punctuation preservation. `_dedup(heard, last_replied) -> (already, norm)`.
- `Session.last_replied` round-trips through `to_dict`/`from_dict` so a restart still dedups.
- On `already`: log, `reply=None`, `actions=[]`, `stop=True`; do **not** append the duplicate customer turn to history.
- Set `last_replied` wherever a reply is produced — the send path and the `needs_human` draft path — so a resumed run does not re-draft the same answer.

## 3. Speed — one decision, one round
Every extra round is a full screenshot + a full vision call. Default prompts say "decide one or two actions" → 3 rounds ≈ 3× latency.

**Diagnose slowness by measuring, not guessing.** End-to-end latency per event = poll interval + debounce + cooldown + (N × per-vision-call latency), where N is the LLM calls per event. Find N from the `/api/sessions` trace step count, and time ONE real vision call to the configured model (read model + `base_url` from `config.json→brain`; a trivial text ping is NOT the number — send a real image at the current `detail` setting). The per-call vision latency is the floor; everything stacked above it is fixable, in leverage order: drop a redundant probe LLM call when a downstream authority already dedups, skip the 2-poll debounce on an unambiguous change, keep the cooldown short.
- Instruct: when replying, emit the **complete** sequence in one decision — `click(input box)` → `type_text(reply)` → `press_enter`. Only fall back to a probe action when the input box is unlocatable or scrolling is needed.
- Keep `max_tokens` modest (~600); replies are short.

### Model choice — the synthetic-chat probe is NOT the same test as a real WeChat screenshot
A model that passes attribution on clean synthetic bubbles may fail MISERABLY on dense multi-bubble real screenshots. Benchmark on BOTH: one synthetic-chat probe + one real WeChat capture with 3+ bubbles. **Treat per-model quality claims as per-serving-generation:** the verified daily driver is `Qwen3-VL-30B-A3B-Instruct` (MoE, 3B active) — downgraded to for speed, then live-validated on real screens (correct `heard`/`reply` across many live receptions); an older note that this same model garbles real screenshots did not hold for the current serving generation. So re-validate the LIVE-CONFIGURED model before trusting either an old claim or a new downgrade. The model receives the full-window image (no crop, §6); `Qwen3-VL-32B` (dense) remains the fallback quality floor at ~5–8 s/step.

### Speed levers (and their quality cost)
When the user wants faster reception, these levers cut end-to-end latency. The model / detail / poll levers trade against the "only 32B reads real screens" floor above, so apply any of them **only with a live-WeChat re-validation** — a text-only latency call proves speed, NOT that the smaller model / lower detail still reads a real multi-bubble screen. The remaining levers (drop a redundant probe call, skip debounce on an unambiguous change, short cooldown) are pure latency cuts that do NOT touch the model — safe without a quality re-test, but re-run the fast-path regression (`tests/test_reception.py`). All knobs are `config.json→reception`-tunable:
- **Model.** SiliconFlow's served VLMs include `Qwen3-VL-8B`, `Qwen3-VL-30B-A3B` (MoE, 3B active), `Qwen3-VL-32B` (dense, quality floor). **Smaller is NOT faster: with the REAL reception prompt + a real `data/shots` frame, answering generations measured 30B-A3B ≈ 4–5.2 s (nothing-to-say ≈ 2–3 s) while the DENSE 8B measured SLOWER at ≈ 5.6–7.5 s** — an MoE with 3B active beats a dense 8B. Benchmark any candidate with the real prompt and a real frame, ≥2 runs each (server-side variance dominates single readings); a text-only latency ping is not a datapoint. Any model change still requires the live-WeChat heard/reply re-validation above.
- **Vision `detail` high→low** (in `brain.py` `OpenAIVisionBrain.decide` + `AnthropicBrain.decide`). Cuts the screenshot prefill hard but lowers visual fidelity, compounding the small-model risk. When the task is reading SMALL on-screen text (short chat bubbles), `detail:low` makes the bubbles unreadable → the triage/decide misreads 'no new message' and drops the 2nd line; keep `detail:high` for small-text reads. The model-SIZE switch (not the detail downgrade) is the latency win that matters — restore `detail:high` the moment you chase quality.
- **Watcher poll** 1.5s→0.5s (detection latency only; cheap). Typing is clipboard (`insert_text`) — NOT a latency source; don't "optimize" it.
- **Drop the redundant probe call.** When a cheap gate (e.g. `triage`) runs before an authoritative decision that already de-dups (`DECIDE` via `last_replied`/`_answered_img`), the gate is pure overhead on every real event (~0.6 s on the SiliconFlow 30B-A3B). Skip it on unambiguous pixel changes (`diff≥~0.03` = a new bubble, not a cursor blink) and let `DECIDE` be the sole gate; backfill the dedup fingerprint from the authority's state on success (lock the message hash from `last_replied`) so downstream dedup / OCR-backstop stay consistent. Keep the gate only for the small/ambiguous band. Ship it behind a config knob (e.g. `reception.skip_triage`).
- **Skip the 2-poll debounce when the delta is unambiguous** (`fast_diff≈0.03`): a new bubble persists, so it need not wait out the flicker-confirm poll; small deltas keep the debounce (cursor blink / our-own-reply settle).
- **Cooldown can be short** (shipped `reception.cooldown_s` = 0.8): duplicate-reply protection is content-based (the post-send `_answered_img` baseline + `last_replied`), not cooldown duration, so a short cooldown only tightens the gap between a customer's rapid follow-ups without reintroducing loops. Make `cooldown_s` / `fast_diff` / `skip_triage` all `config.json→reception`-tunable so the user can push further without a code edit.
- **Background (`pin_wechat=false`) mode: the THINK phase must not raise the window — `_act` owns the one raise, at typing time.** The watcher's trigger frame is the SAME PrintWindow source `_think` reads, so an `ensure_front` during think adds 0.15–4 s (longer when the user's foreground must be fought) and steals the user's active window for zero information gain. Gate the think-phase raise on `watcher.pin_wechat`.
- **Cap the prompt's `reasoning` field (≤40 字).** Generation length is the one LLM-visible latency lever in the prompt: a bounded reasoning cuts answering time and shrinks the long-reasoning text the §10 echo detector must sweep.

**Verify a provider model ID via `/v1/models` + a live timed call, never from web/blog recommendations.** Marketing pages list `Qwen2.5-VL-7B-Instruct` as SiliconFlow's "fastest VLM" but it 400s ("Model does not exist"); the served set is what `client.models.list()` returns. Never write a model into `config.json` from a blog — confirm the ID resolves and time a short call (read the live key from config, don't echo it).

## 4. A correct decision must actually land
A full `click→type_text→press_enter` in the trace does **not** mean the chat received the message:
- `bring_to_front()` returns a bool, and older call sites ignored it — `insert_text` then typed into whatever held focus (UI logs action after action, the chat shows nothing). Check the bool (retry a few times) and, if focus cannot be won, skip typing with a warning instead of typing into the wrong window.
- **No-click send first, click-sweep only as the fallback.** When `_verify_sent()` reports not-sent, run `_robust_send(s, text, rect, sx, sy)`:
  1. `_send_no_click`: `bring_to_front → insert_text(full reply)`, then try `Enter` and `Ctrl+Enter` (ordered by `send_mode`), verifying each via `_verify_sent`. WeChat 1:1 chat default-focuses the input box, so this usually succeeds with **zero clicks** — immune to size/DPI/layout drift.
  2. On failure: `native.clear_input()`, then `_input_send_sweep` — for each point in `Session._input_pt` (remembered) → the `_INPUT_CANDIDATES` grid (full-window fractions, chat pane only — x 0.40–0.72, y 0.82–0.94, avoiding the left contact-list panel and the right send button), do `clear_input → bring_to_front → click → insert_text → Enter/Ctrl+Enter → _verify_sent`; the first point that verifies is stored back on `s._input_pt` so later sends go straight to it. This one-time calibration 'sticks'.
- **Verify by the send, never by the typed characters.** `_verify_sent` confirms a **new message bubble** appeared (a large, machine/DPI-agnostic pixel change) — the one reliable "it landed" signal. Do NOT build a focus-detection that checks whether a few typed characters appeared in the input via whole-window `diff_ratio`/`changed_ratio`: for a short probe they read ~0.0000 even with the window foreground, and will misroute you. If you must detect typing, crop to the input row AND type a long probe string; otherwise just verify the send.
- Surface the outcome: `Session.last_verify{ok,text,at}` (exposed via `to_dict`) and `heard` in every `trace` entry. Since commit 7bb43b9, trace entries also carry `sent`(bool) and `verify`({ok,text,at}) so a successful send is provable directly from the trace without a separate API call. `Session.reply_count` is incremented once per confirmed `send_ok` — `0` means nothing has ever been verified as sent.

## 5. Continuous conversation = one run on open, watcher started by the run tail
The run loop answers one turn and exits; nothing re-triggers on its own. Opening a session must `agent.run(sid)` ONCE (a message already on screen is not a pixel *change*, so watching alone misses it). The watcher starts in the `_run` tail AFTER that first run finishes — starting BOTH at open is a race: the watcher's baseline is captured pre-reply, sees the post-reply screen 2.5 s later as a change, and triggers a duplicate run while the first is alive (same message answered twice + `/run` 409). The watcher poll must re-trigger `done`/`idle`/`watching` — only `running`/`paused`/`error` are skipped. Watching is a cheap region diff: it calls the model only when the region changed.

## 6. No crop — model sees the full window
The earlier chat-area crop (left 25 % + top 10 % removed) was removed because the crop coordinate space broke click targeting: the model returned y values in 0..1024 normalized space that exceeded the crop height, causing off-image clamps that landed the click in the window border instead of the input box. The full-window image (≈ 901×691) makes the coordinate space unambiguous and the model's input-box clicks land correctly. `s._crop_rect` now equals `s._orig_rect` (no crop); `s._crop_sx/_crop_sy` are simple image-to-screen scale factors (≈ 1.0). The contact list and title bar are still visible to the model but do not cause misreads in practice with a 32B model.

## 7. Qwen3-VL 0..1024 normalized coordinate detection
Qwen3-VL-32B occasionally emits click x/y in 0..1024 normalized space instead of the image pixel space the prompt asks for. Symptom: model returns `y=970` for a 691 px tall image — a plain clamp gives `y=690` (window border), missing the input box at ~y=640–670.

**Detection rule (in `brain.py _parse_json_decision`, called with `image_size=img.size`):**
```python
if x >= img_w or y >= img_h:
    # 0..1024 normalized space detected
    x = x * img_w // 1024
    y = y * img_h // 1024
# final clamp to valid pixel range
x = max(0, min(x, img_w - 1))
y = max(0, min(y, img_h - 1))
```
Both `OpenAIVisionBrain.decide` and `AnthropicBrain.decide` must pass `image_size=img.size` to the parser. NEVER apply a plain clamp without the 1024-scale check — the clamped value is still in the wrong spot.

## 8. Don't fabricate un-verifiable real-time facts
When the customer asks about real-time / verifiable data the model cannot access (weather, stock/FX prices, live scores), it will invent specific numbers and the customer calls it out (symptom: "胡说八道?"). Add a standing rule to the 行为准则 block (near §1) in `brain.py`: you have **no network access** — for such topics never state a specific value; say honestly "这个我这边查不到实时数据，你看下 XX 更准" or give common-sense / general advice instead. A confident wrong number is worse than declining. (Fabrication, not dedup, was the real cause of the "same question answered twice with two different made-up numbers" symptom.)

## 9. Don't echo the last reply onto a DIFFERENT question (model anchoring)
§2's dedup stops re-answering the *same* line. It does **not** stop a small/MoE model from anchoring on its last answer and re-sending it when the customer asks something *new* (symptom: "天气" → "查不到实时天气", then "你还能做什么" and "怎么又回答一遍？" all get that same weather line). Dense 32B rarely does this; the 30B-A3B (3B-active) speed model does it reliably, so it only surfaces *after* a speed downgrade. Two-part fix:
- **Prompt** (行为准则 block in `brain.py`, near §8): "每次只针对【左侧最新那条】客户消息本身作答；即使你刚回复过、客户换了话题，也按新话题给不同的答复；禁止照搬/复述上一条的措辞。" AND scope the §8 real-time-decline rule to real-time topics only ("只有客户确实在问实时数据时才这么答，别把上一条'查不到实时数据'套到不相关的问题上") — anchoring usually *generalizes* the model's last safe-fallback phrase onto unrelated questions.
- **Mechanical guard** (in `agent._think`, right after the §2 dedup block, operating on the `Decision` `d`): a re-asked *same* question may pass, but a *different* question must not get the same answer. `_last_qa_texts(s) -> (last_assistant_reply, the_customer_question_it_answered)` walks `s.turns` for the last assistant turn + the customer turn immediately before it; `_is_dup_reply(new, old)` = normalized equality, OR containment (shorter ≥ 6 chars inside longer), OR `difflib.SequenceMatcher.ratio() > 0.86`. If `_is_dup_reply(d.reply, last_assistant) AND NOT _is_dup_reply(d.heard, last_question)` the model is echoing → re-think **once** via `brain.decide` with a `ctx["_repeat_nudge"]` (a "客户这次问的是 X，你上一条是 Y，针对 X 给不同答复" line that `build_prompt` appends as a `# ⚠ 更正提示` block); if the re-think is still a duplicate, **block it** (`d.reply=None, d.actions=[]`) rather than send the repeat. The `NOT _is_dup_reply(heard, last_question)` clause is what keeps legitimate re-asks flowing.
- **Diagnose (confirm it's the model, not the send layer):** vision-analyze the exact frames RFlow fed the model in `data/shots/` (the `*.png` the watcher wrote) + the session trace. If the input box in that capture is **empty**, the repeat was MODEL-GENERATED (this bug); if it held leftover text, it was a stale `insert_text` re-send (§4). The captures are ground truth of what the model saw — don't theorize. Re-validate reception after *any* model change, since this only shows up with the weaker model.

- **Alternation trap (A→B→A) — compare against the last N replies, not just the previous one.** The §9 guard above keys off the *single* immediately-previous assistant reply. A small/MoE model evades that by **alternating between two variants** (e.g. a generic greeting and a topical answer): each fresh reply differs from its immediate predecessor, so an any-over-one-previous never fires and the model re-issues the same line every other turn (the user sees '同一句反复刷 / 拿旧话答新问题'). Fix: compare the candidate against the **last 4** assistant replies — helper `_recent_replies(s, n=4)` returns the recent assistant `turns` reversed (most-recent first); the echo check becomes `any(_is_dup_reply(d.reply, r) for r in recent)`, and a still-duplicate re-think is **blocked** (`d.reply=None, d.actions=[]; d.stop=True`, 宁缺毋滥). Point the `_repeat_nudge` at the customer's **newest** line (`s.last_new_text or d.heard`, *not* the old one) so a corrected re-think answers the actual current question. This is the user's standing requirement: every reply must be grounded on the customer's *latest* message — a stale, re-issued generic line reads as 'didn't answer my question'.

## Live probe (verify attribution + no-repeat without a real chat)
Render two synthetic screenshots with PIL (use a CJK font such as `C:/Windows/Fonts/msyh.ttc`): left grey rounded bubble = customer line, right green bubble = our reply.
- **A**: customer asked, nothing sent → expect `heard` == the customer line and a non-empty `reply`.
- **B**: customer asked, then our reply is last (right) → expect `reply is None` and `stop is True`.
Call `build_chat_brain(cfg)` from `config.json` (masked key is fine — read it, never rewrite the file) and print `intent/heard/reply/stop/actions`. Both assertions passing means the prompt + dedup design is sound for THAT model — but ALSO probe a real WeChat screenshot (see model choice above): a model that passes synthetic can still fail on real bubbles.

## 10. History anchoring: type misread + self-echo (mechanical gates)

§1 attributes WHO spoke and §2/§9 gate WHAT we answer. A third family leaks through both: the model's reading of the newest left bubble is biased by the conversation HISTORY itself. Both sub-failures land on the same user-visible symptom — the bot answers one customer line five-plus times — and both are fixed as prompt-rule + mechanical-gate PAIRS (a prompt rule alone always leaks under a long enough history).

### Type misread — `heard='语音消息'` for a readable TEXT bubble
After `s.turns` has accumulated several `语音消息` labels from an earlier voice-message period, the model keeps labeling every new readable text bubble as `语音消息` and replies with the media_ack fixed phrase instead of answering the text. Telling detail that proves the source is history, not the image: the model's `reasoning` can ANSWER the text's actual content (it replies “是的，打字就可以啦” to “我这不就是打字吗？” while `heard` still says 语音消息).

Prompt rules (ship in `brain.py`):
- **heard 只认图，不认历史**: `heard` is the verbatim transcription of the newest left bubble in the CURRENT capture. A `语音消息`-style entry in the conversation history is bookkeeping from a past turn, not evidence about the current bubble — even after ten prior voice labels, a bubble with readable text is that text.
- **Type classification is 从严 (text > everything)**: voice = capsule/round icon + a displayed seconds count + NO readable text inside; image = photographic content. Any readable character ⇒ it is a text message. 看不清小字 ≠ 语音 — transcribe what is readable, or set `needs_human=true`; never degrade an unclear read into "voice" and fire the fixed phrase.

### Self-echo — our own reply read back as the customer's line
The mirror failure: the model reads a RIGHT-side own reply as a LEFT customer line. Long fixed phrases are the most-read-back (they stay on screen bubble after bubble), and read-backs are NOT verbatim — the vision pass elides characters (吞字) and introduces typos, so exact-match detection misses them. Each read-back gets answered; the answer becomes a new right bubble; the loop repeats — the user's "一句话回答了五六遍".

Mechanical FIRST gate in `agent._think`, running BEFORE the screen-change/no-new-message gate: `_looks_like_own_reply(heard, _recent_replies(s, 5))`:
- enabled only for `len(norm(heard)) >= 10` — short genuine quotes of our own phrasing must pass;
- echo if substring containment either way (truncated echo), OR `SequenceMatcher.ratio() > 0.85` (verbatim echo), OR `ratio() > 0.55` AND longest common block `>= 14` chars (vision-elision echo — this third fence is load-bearing: the vision pass doesn't just drop characters, it SHRINKS/rephrases our long replies when reading them back, pulling the overall ratio down toward ~0.6x while the leading block survives. The original 0.70/12 fence leaked exactly that family live — a shrunken echo measured ratio=0.65 with a 15-char common block; re-calibrate on live `turns` strings before moving any of these fences in either direction);
- on echo: `reply=None, actions=[], stop=True`, and do NOT append a customer turn.

**Calibrate any such detector on the REAL incident strings before trusting it**: pull the live session's `turns` from `/api/sessions`; every observed echo variant (verbatim / elided / typo'd) is must-catch, every genuine customer line is must-pass — especially short quotes of your own phrasing, which must NOT share a ≥12-char block. Fences moved without that calibration either leak echoes or eat genuine quotes.

### Same-sentence 60 s cooldown (adjacent gate)
The §2 escape hatch — "screen changed + model reports the *old* `heard` ⇒ clear the fingerprint and allow the reply" — is NOT unconditional: our own reply bubble appearing also changes the message band. Within 60 s of the last confirmed send of that same line, block instead (宁可晚答，不可刷屏); only past the cooldown does the fingerprint clear fire. The timestamp is `Session.last_replied_at`, written on every confirmed send and persisted through `to_dict`/`from_dict` so a restart keeps the cooldown.

### Diagnosis + fix-verification protocol (any suspected misread)
1. **Neutral-prompt re-read** (generalizes §9's `data/shots/` diagnosis into a controlled contrast). Send the SAME saved frame (`data/shots/*.png` written for that round) to the SAME configured brain with a neutral instruction — 只描述事实： is the newest LEFT bubble text / voice (capsule + seconds) / image; if text, transcribe verbatim. Same model, same pixels, different prompt. Neutral read correct + reception-prompt read wrong ⇒ prompt anchoring → fix the prompt. Both wrong ⇒ capture/image problem → go to the capture layer, not `brain.py`.
2. **Replay verification of the fix.** Rebuild the real `ctx` — `window_title` + the POLLUTED last-8 `s.turns` from the live session + the real saved shot — and call `brain.decide(img, ctx)` twice through the patched `build_prompt`; assert `heard` flipped from the misread to the verbatim text. Synthetic probes cannot reproduce history anchoring — only the real polluted history can.
3. Re-run the three regression scripts, restart the backend, then confirm on the live session that subsequent rounds read text as text.

## 11. One answer per question — the answered-ledger hard gate

The user's standing rule: **每一个问题只回答一遍**. The soft family above (screen-change gate, last-N reply suppression, re-think nudge) still leaks one shape: the SAME customer line re-heard minutes later gets answered again with a near-identical reply — the retry exemption (which must let identical answers through for unsent lines) is exactly what lets the duplicate greeting out, and to the customer it reads as spam.

Hard gate in `agent._think`, placed with the §10 gates and BEFORE any reply is allowed — `_question_handled(s, heard_norm)`:
- `'answered'` → the normalized line is in the 30-min success ledger (`Session._recent_answered`, capped ~20 entries, written on every CONFIRMED send in both send paths, and rebuilt from `turns` after a restart — a customer line followed by an assistant reply within 30 min counts as answered) → skip the round (`reply=None, actions=[], stop=True`).
- `'noise'` → the same line already recorded within 5 min (echo / re-trigger of an instance that was already handled) → skip, and do not append another copy to `turns`.
- `None` → a genuinely new question → answer.

**Two exemptions are load-bearing** — removing either re-introduces a fixed bug:
1. While `_unanswered_msg` is set, the gate is disabled: that line has NOT been successfully sent, and a ledger/noise entry would permanently mute it (the classic 回两句就哑 regression).
2. `step > 1` mid-run re-looks (open the conversation → look again) legitimately re-read the same line; gating them would strangle the multi-step flow.

- Calibration follows §10's protocol: replay the live session's real strings — must-catch every re-answered line (including one re-heard ~12 min later), must-pass every genuine new question, every short quote of our own phrasing, and an answered line older than the 30-min window (a customer genuinely re-asking after the window SHOULD get a fresh answer).

## 12. Compound spam: official-account wandering, sidebar previews, broken frames

The §1/§2/§9/§10/§11 gates can ALL pass and the customer still gets one line answered five-plus times — when the WATCH ITSELF has wandered off the conversation. Four failure layers stack; fixing only the one you first spot leaves the other three live:

1. **Official-account wandering (prompt).** Following the "scan the left list for unread badges" instruction, the model clicked a 公众号/官方号 row (observed: 微信游戏 — absent from the naive name blacklist). The right pane becomes an article feed with no input box; every subsequent round mis-reads or wants to re-greet, for a dozen-plus wasted rounds. Two rules: (a) the non-human skip rule must be a *shape* rule, not a name list — ANY row whose preview is article-push style (【公号名】标题 / 标题+摘要 / 图文卡片) is a 官方号, never click it; (b) when the right pane already shows a feed/game page (no chat bubbles, no input box) → `reply=null`, no actions, `stop=true` — never navigate away, wait for the next human unread.
2. **Sidebar preview ≠ heard (prompt).** With no conversation open, the model reads the LEFT list's preview snippets as if they were incoming messages — one preview reading 你好 became `heard='你好'` for 15+ consecutive rounds, each round wanting to send the greeting again. `heard` may ONLY come from a bubble in the RIGHT-side chat pane; a left-list preview is another conversation's summary, never this session's message source.
3. **Bad frames must never reach the model (think layer).** PrintWindow during window animation or minimize returns tiny frames (observed 159×27 — the VLM endpoint rejects it: "height(27) or width(159) must be larger than 28") or uniform near-blank frames (a 12-step run on blank frames = 12 full-price vision calls all concluding 窗口为空白，需等待加载). Guard in `_think` BEFORE `brain.decide`, mirrored by `Agent._frame_broken` for the readback path: width < ~200 or height < ~120 → skip the round (60 s throttled warn); 32×24 grayscale downsample variance < ~16 → uniform/blank → skip the round. Both the model-input frame and the `_verify_sent` after-frame need this test.
4. **Broken readback must never re-type (send layer).** `_verify_sent`'s after-frame can be broken (animation/minimize moment); the diff then reads "not sent" while the message MAY have landed. The sweep retry RE-TYPES a message the customer already received — this is the physical duplicate-send mechanism, invisible to every text-level dedup gate because the send DID succeed. Guard: re-capture the readback ~3× on a broken frame; if still broken set `s._readback_broken` → `_robust_send` skips the sweep entirely and `_input_send_sweep` aborts on the flag. The genuinely-unsent line is not lost: the stable-screen kick path and the next DECIDE round re-judge from a clean frame and re-send only if the bubble truly never appeared.

**Test corollary:** a fake frame injected into a `_think` test must have large-block structure (dark left panel / light chat pane / input band). A pure-white or sparse-dotted fake image is *correctly* rejected by the blank-frame guard — sparse dots average out under the 32×24 downsample — and the test then crashes on `s._d is None` instead of exercising the logic under test.

**Diagnosis walk for any "still replies N times" report** (before touching code): pull `/api/sessions` turns + trace for the window and correlate — (a) `reasoning` describing article content = layer 1; (b) `heard` equal to a left-list preview string, or repeated ~15 s apart with no customer activity = layer 2; (c) `reasoning` saying 窗口为空白 or an HTTP-400 trace entry = layer 3; (d) multiple type/enter attempts for one customer line = layer 4. Then neutral-prompt re-read the saved `data/shots/` frames (§10 protocol) to confirm what the model actually saw before writing the fix.
