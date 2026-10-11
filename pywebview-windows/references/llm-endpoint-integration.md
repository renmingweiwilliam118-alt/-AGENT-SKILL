# LLM gateway integration for desktop apps (OpenAI-compatible inference endpoints)

Covers the failure modes behind a persistent "识别失败 / 执行失败" report in an app that calls an
OpenAI-compatible `/chat/completions` gateway — model IDs, free tiers, reasoning models, and OAuth
token lifetime. Read the error BODY, not just the status code, before switching anything.

## Discover model IDs — never hard-code a guess

- `GET {base_url}/models` with the bearer token lists every available id. A default model name that
  404s at runtime is the classic permanent-failure cause: the user clicks, the worker raises, the
  feature looks dead. When a 404 names a model, re-list the catalog and pick a real id instead of
  adjusting the spelling.
- **404 has two meanings on these gateways.** "does not exist in our configuration or catalog" =
  wrong id; "requires available credits … balance is too low" = the id is real but the account tier
  is paid-only. Only the first is fixed by changing the model name.
- **Read the app's persisted credential file before theorizing.** An app that lets the user fill in
  base_url/key/model in its UI stores them in a config file that **overrides the app's code
  defaults** — so "I already fixed the default model" changes nothing while that file exists, and
  the log keeps naming the user's own model. Read it (base_url / model / whether a key is present)
  to learn which endpoint is actually in play; it may be a completely different provider than the
  app's fallback gateway, and each has its own model catalog and tiers.

## Free tiers, rate limits, and the busy-flag trap

- Free-tier ids usually carry a `:free` suffix; they answer 429 under "fair-share" limits, while
  paid ids answer 404 with a balance message. Keep at least two verified free ids on hand and
  auto-fall-back to the second on 429 instead of sleeping the whole worker (see pywebview-windows
  SKILL.md rule 13 — a long backoff inside the worker holds the busy flag and makes every later
  cycle skip, which the user reads as "stuck").

## Reasoning models: the answer may not be in `content`

- Some models return `message.content = null` and put the text in `message.reasoning` (older ones:
  `reasoning_content`). Read all three fields in order — `content or reasoning or
  reasoning_content` — or the app sees an empty reply and retries forever.
- A reasoning model spends its token budget on the reasoning first: with a small `max_tokens`
  (e.g. 32) it can return nothing usable. Budget ≥ ~800 tokens for JSON-output vision prompts.
  Confirm `finish_reason == "stop"` and that the parsed payload is non-empty before treating the
  call as successful.

## OAuth access tokens expire hourly — refresh at load

- A gateway credential stored as an OAuth record (`access_token` + `refresh_token` +
  `expires_at` + `portal_base_url`) goes **401 "API key is invalid, blocked or out of funds"** about
  an hour after issue. Refresh when the remaining lifetime is under ~5 minutes:
  `POST {portal_base_url}/api/oauth/token` with `grant_type=refresh_token`, the `refresh_token`,
  and the `client_id`; the response carries new `access_token`/`refresh_token`/`expires_in` —
  write all of it back to the same json file. A refresh failure should degrade to using the old
  token, not raise.
- Triage by code: **401** ⇒ credential lifetime (refresh); **404** ⇒ model id or account tier;
  **429** ⇒ rate limit (fall back or back off). Fixing the wrong one of these wastes a rebuild cycle.
- The stored token is an OAuth JWT, not an API key: decode its payload (base64url middle segment)
  to see the real `expires_at`/scope when a 401 arrives and you need to confirm expiry vs. scope.

## Separate "read the screen" from "write the reply" — the one-sentence trap

When a vision model both reads a screenshot AND writes the draft reply, the reply is always a
terse one-liner: the vision prompt naturally asks for `"draft": "<一句简短回复>"`, and the
persona/knowledge-base only ever *polishes* that short string afterwards. The user reports "他只回复
一句话，没按智能体回复".

Split the responsibilities:
- **Vision model**: extract messages + locate the input box only. Its prompt must say explicitly
  "你只负责读出对话内容和定位输入框，不要写回复" — otherwise it keeps emitting a draft.
- **Agent composer** (always, not conditional on knowledge-base hits): a second LLM call with the
  persona, tone, banned words, knowledge base, and the extracted conversation, instructed to write
  "完整、得体、贴合人设的回复…自然分段、信息完整，不要敷衍的一句话". Budget `max_tokens` ≈ 400
  and `temperature` ≈ 0.5 (the old polish path used 200/0.3, which caps length regardless).

Gate this on nothing — the old code only composed when a knowledge-base row matched, so a user
with no KB got the bare vision one-liner. Compose always; fall back to the vision draft only if
the composer call fails. This also un-gates auto-send from a click coordinate: an agent-composed
reply doesn't depend on the vision model's `input_box` estimate.

### Two follow-ups the user asks for right after: reply length, and latency

- **Expose reply length as one agent config key** (`reply_len`: `short` / `medium` / `long`), and
  drive BOTH the prompt hint and `max_tokens` from it: short → "一两句话说清，不超过 60 字" +
  `max_tokens≈120`; medium → "100 字左右" + 300; long → "分点或分段讲全，200~300 字" + 500. Measured
  on a real gateway: 44 / 72 / 176 chars for the same question — the hint, not the token cap, is
  what does the work. Surface it as a `<select>` in the agent panel and round-trip it through the
  same fill/save functions as the other agent fields.
- **Once the composer prompt is correct, folding the draft back into the vision call is safe** and
  halves latency (two serial round trips → one; measured 62 s → 31 s on the same model). Ask the
  vision call to return `draft` in the same JSON, carrying the SAME length hint and cap as the
  composer. Guard: without an explicit length instruction the model collapses back to a one-liner
  (rule above), and the fast path has no knowledge base and no conversation memory — keep the
  composer as the fallback when `draft` is empty, and prefer it for context-heavy flows. Log which
  path ran so a latency complaint is diagnosable from the log alone.

## 5xx is a transient server fault — retry, don't rebuild

SiliconFlow (`api.siliconflow.cn`) and similar gateways return intermittent `500` with a body like
`{"code":56507,"message":"Request failed: Unknown error."}` while the same request succeeds
seconds later (verified: a failing call re-issued immediately returned normally). Treat
`500`/`502`/`503` as retryable — same class as 429 — with a short backoff (e.g. `3 * (attempt+1)`
seconds) inside the existing retry loop, before the final `raise`. A single 500 in the log is NOT
a code bug and does not justify touching the prompt or model id; re-issuing the identical request
is the diagnostic that confirms it.

Credentials read from these files are secrets: never echo the token in logs or summaries —
`[REDACTED]` with length only.
