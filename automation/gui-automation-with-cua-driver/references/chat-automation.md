# Chat Automation Patterns

## Conversation Memory & Deduplication

When building a chat monitoring/auto-reply system, maintain a rolling
conversation buffer with deduplication. Vision models re-read the entire
visible screen every cycle, so the same message appears multiple times.

```python
class Core:
    def __init__(self):
        self._conv = []          # [{"sender": "对方"/"我", "text": "..."}]
        self._own_replies = []   # texts the agent has sent

    @staticmethod
    def _norm(t):
        """Normalize for dedup: strip whitespace, first 24 chars."""
        return re.sub(r"\s+", "", (t or ""))[:24]

    def _merge_conv(self, new_msgs):
        """Merge vision-read messages into conversation buffer.
        Returns count of NEW incoming messages (sender != 我)."""
        recent = {self._norm(m["text"]) for m in self._conv[-30:]}
        # Own replies recognized LOOSELY: rendered screenshot text is not the
        # sent draft (line breaks, truncation, punctuation) — ≈10 chars is the
        # reliable signal. Never rely on vision's sender field.
        own_prefixes = [re.sub(r"\s+", "", r)[:10] for r in self._own_replies[-20:]]
        added = 0
        for m in new_msgs:
            t = (m.get("text") or "").strip()
            if not t:
                continue
            if self._replied_fuzzy(t):  # fuzzy vs recent tail of _replied
                continue
            t10 = re.sub(r"\s+", "", t)[:10]
            if t10 and any(t10.startswith(p) or p.startswith(t10)
                           for p in own_prefixes):
                self._conv.append({"sender": "我", "text": t})
                recent.add(self._norm(t))
                continue
            sender = m.get("sender") or "对方"
            self._conv.append({"sender": sender, "text": t})
            recent.add(self._norm(t))
            if sender != "我":
                added += 1
                self._replied.add(re.sub(r"\s+", "", t))  # mark at merge time
        if len(self._conv) > 40:
            self._conv = self._conv[-40:]
        return added
```

`_replied_fuzzy`: compare against the recent tail of `_replied` (≈50 entries):
24-char prefix overlap OR `difflib.SequenceMatcher` ratio ≥ 0.8 on the first
120 chars → treated as already replied. Exact full-text keys miss because
vision re-reads of the same on-screen message jitter (line breaks,
truncation, punctuation).

```python
self._replied = set()   # persistent, capped (~500, drop oldest)
```

**Gate rule:** Only generate a reply when `added > 0`. This prevents the
system from replying to the same screen contents repeatedly.

**Manual override:** Add a `force=True` parameter for user-triggered
recognition (button click) to bypass the dedup gate.

## Self-Message Re-Recognition (Replying to Yourself)

The bot's own sent replies re-enter the monitored region and get re-read by
vision as new 「对方」messages — the user sees one relevant reply plus one
"irrelevant" reply, or the same thing answered repeatedly. Three layers kill
it:

1. **Recognize own messages by loose prefix, not exact key.** The rendered
text in the screenshot is not the sent draft; a 24-char exact key against
`_own_replies` misses. Compare ≈10 leading chars (whitespace-stripped),
both directions.
2. **Fuzzy membership in the persistent replied set.** Vision/OCR re-reads of
the same on-screen message jitter; exact full-text keys miss. Compare against
the recent tail: 24-char prefix overlap or `difflib` ratio ≥ 0.8 ⇒ replied.
3. **Hard-code the bubble-position rule in the vision prompt.** Vision's
`sender` field is unreliable — it labels right-aligned bubbles 「对方」 by
content tone. Prompt rule: left-aligned bubbles = 对方, right-aligned = 我,
judge by position ONLY, never by content; when there is no new 对方 message,
`draft` must be an empty string; never fabricate product details the
dialogue never mentioned.

## Separation of Concerns: Vision vs. Agent

**Do NOT let the vision model write the reply.** The vision model should
only extract structured data (messages, input box position). A separate
LLM call with the agent's persona should generate the reply.

```python
# Vision prompt: extract only, do not compose
vision_prompt = (
    "You only read dialogue and locate the input box. "
    "Do NOT write a reply — the customer service agent generates it separately."
)

# Agent prompt: compose with persona, tone, knowledge base, conversation history
def compose_draft(conversation, context, kb, agent_config, llm_config):
    system = (
        f"You are {agent_config['name']}, a {agent_config['role']}.\n"
        f"Tone: {agent_config['tone']}.\n"
    )
    if agent_config.get("persona"):
        system += f"Persona: {agent_config['persona']}\n"
    if agent_config.get("banned"):
        system += f"Forbidden words: {agent_config['banned']}\n"
    if kb:
        system += "Base answers on the knowledge base.\n"
    system += (
        "Write a complete, natural reply based on the conversation. "
        "Do not write a single lazy sentence. Output only the reply text."
    )
    convo = "\n".join(f"{m['sender']}: {m['text']}" for m in conversation[-8:])
    user_msg = f"[Conversation]\n{convo}\n\n[Context]\n{context}\n"
    if kb:
        user_msg += f"\n[Knowledge Base]\n{kb}\n"
    user_msg += "\nYour reply:"
    # ... call LLM with temperature=0.5, max_tokens=400
```

**Why:** If the vision model writes the draft, it defaults to short generic
responses regardless of agent persona settings. The persona only takes effect
when a dedicated LLM call uses it in the system prompt.

## User-Authored Reply Instruction (custom prompt override)

Let the user write the whole reply instruction. A `custom_prompt` config
key that, when non-empty, REPLACES the persona/tone/length template
entirely — the field-based template only runs when it's empty. Support
placeholder substitution so the user's instruction can reference live data:
`{persona} {role} {tone} {banned} {greeting} {convo} {context} {kb}`.

```python
custom = (agent.get("custom_prompt") or "").strip()
if custom:
    fields = {"persona": persona or "（未设置）", "role": agent.get("role"),
              "tone": agent.get("tone"), "banned": banned or "（无）",
              "convo": convo, "context": context or "（无）", "kb": kb or "（无）"}
    try:
        system = custom.format(**fields)
    except (KeyError, IndexError, ValueError):
        system = custom   # bad placeholder ≠ crash: use it verbatim
```

**Apply the override in BOTH generation paths.** A chat pipeline that has a
fast path (vision call returns a `draft` field) and a slow fallback
(composer call) must honor `custom_prompt` in both, or the custom instruction
silently works only half the time. In the vision path, keep the JSON output
framework (`messages`/`input_box`/`draft`) mandatory and splice the custom
instruction in as the system head before it. Drive `max_tokens` from the
same `reply_len` key in both paths so length behaves identically.

**Test both branches with the real LLM before shipping** — empty custom
prompt (default behavior) AND a custom one — and confirm the outputs
actually differ in the expected way.

## Region Selection Validation

**Always verify the selected screen region contains the expected content**
before starting monitoring. Users frequently select the wrong window
(e.g., a code editor next to the chat app), causing the system to respond
to irrelevant text.

**Diagnostic approach:**
1. Capture the current region as a screenshot
2. Use the vision model to describe what's in the region
3. If the content doesn't match expectations (e.g., technical text instead
   of chat messages), alert the user to re-select the region

**Programmatic check:** Compare the region bounds against the target
window's bounds from `list_windows`. The region should be fully contained
within the target window.

**Triage rule: when the reply is off-persona and mentions technical terms,
check the selected region before suspecting the agent config.** A region
that overlaps a code editor / chat with the developer makes the agent
respond to code snippets and jargon — the user reads this as "the persona
isn't being applied", but the config is fine; the wrong pixels are being
read. Verify by capturing the current region and asking the vision model
what it contains. If the saved region doesn't exactly match the target
window, the fix is to re-select (or set the region to the window bounds
from `list_windows`), not to change the prompt. A saved region is only
valid while the window sits where it did when picked — if the user moved
the window, the coordinates are stale.

**The running app must re-read the region from config each monitor cycle, not cache it at startup.**
A startup-cached region means a re-pick in the app (or window move + re-pick)
takes effect only after a restart — the user tests, sees old behavior, and
re-reports. One line at the top of each loop iteration:
`self.region = load_cfg().get("region")`, which makes external config edits
apply live. Negative-x region coordinates (virtual desktop spanning a second
monitor) are themselves a stale-region signal: re-verify against the target's
`list_windows` bounds before blaming the model.

## Speed Optimization

Each `get_window_state` call takes ~1.3s (process spawn + pipe IPC).
Minimize tree reads:

- **Send without verify:** 2 tree reads (~3.5s)
- **Send with verify:** 3 tree reads (~5s)

Make verification optional (default off) for speed. Enable it when
reliability matters more than latency.

```python
def send(self, text, verify=False):
    els = self._els()           # read 1: find input box
    box = self._input_box(els)
    set_value(self.pid, box, text)
    time.sleep(0.15)
    els2 = self._els()          # read 2: get fresh token (stale after set_value)
    box2 = self._input_box(els2)
    _call("hotkey", {"pid": self.pid,
                      "element_token": box2["element_token"],
                      "keys": ["enter"]})
    if verify:
        time.sleep(0.6)
        els3 = self._els()      # read 3: check message list
        # ... verify logic
```

## Desktop Region-Picker UX (hide-app → drag → restore)

When the user clicks "pick region on desktop": hide the app window, let them
drag a selection, restore the app, then apply the region.

**Overlay design rule (verified with the user): NO dark mask at all.**
A 4-panel dark mask with a transparent "hole" renders as a fully black screen
between mousedown and the first ~6px of drag, because the hole is zero-sized
at mousedown. The user explicitly rejected this ("the screen goes black").
The accepted design is: **normal desktop the whole time, only 4 thin blue
border windows following the cursor.** If a top hint bar is wanted, keep it
small and semi-transparent — never a full-screen layer.

```python
# Only blue borders — no RFlowPickDark / mask panels at all
for key, bx, by, bw, bh in (
        ("bt", l-2, t-2, w+4, 3), ("bb", l-2, t+h, w+4, 3),
        ("bl", l-2, t, 3, h),   ("br", l+w, t, 3, h)):
    hh = ensure(key, "RFlowPickBlue")   # thin solid topmost windows
    if hh:
        SetWindowPos(hh, None, bx, by, bw, bh, SWP_NOZORDER|NOACTIVATE|SHOWWINDOW)
```

## Build → Ship → Verify (stale-process trap)

After every rebuild, the most common "your fix didn't work" report is the
user running the OLD exe. Standard closeout sequence:

1. Kill ALL app processes (`Get-Process -Name <app>* | Stop-Process -Force`),
   including any tray/background copies and leftover webview children.
2. Copy the fresh exe to the delivery path; verify with `ls -l` that the
   timestamp/length actually changed.
3. Tell the user to re-launch explicitly, and give ONE observable proof that
   the new build is live (a log line with a build marker, a color change,
   a version string) — ask them to confirm that specific proof.

Ship the proof, not a description. "Rebuilt, please test" invites the stale
process failure; "restart, then check the log shows `build-...-marker`"
does not.

## LLM Error Handling for Chat Pipelines

Beyond 429 (rate limit), also retry on 500/502/503:

```python
if e.code in (500, 502, 503) and attempt < retries - 1:
    time.sleep(3 * (attempt + 1))
    continue
```

SiliconFlow and similar providers return transient 500s under load.

## Why Enter Key Instead of Send Button

For WeChat and similar Qt Quick apps:
- Background click on send button: `effect: unverifiable`, often no-ops
- Foreground click: `foreground_unavailable` (can't steal focus)
- Enter key via `hotkey` with `element_token`: reliable

This is specific to self-drawn Qt apps. Standard Win32 apps may work
fine with button clicks.

## Compliant Channel: WeCom (企业微信) Official API

When the user wants a zero-ban-risk channel alongside (or instead of)
personal-WeChat GUI simulation, add the WeCom 智能机器人 long connection:
an OUTBOUND websocket — no public IP, domain, or callback server required.
Credentials: 企微管理后台 → 智能机器人 → API 模式 → 使用长连接 → Bot ID +
Secret. Keep the channel fully independent in code (separate config, UI
card, start/stop) so the personal-WeChat automation keeps working while
WeCom is unconfigured. Two diagnostics: the WeCom admin console has its own
built-in AI/keyword engine that can answer the same message in parallel with
your bot's API reply — "double reply" on the WeCom channel usually means 回复
设置/欢迎语/知识集 in the backend is also enabled; and when WeCom is
UNCONFIGURED, double-reply / irrelevant-reply reports come from the personal
channel's self-message re-recognition (section above), not from WeCom.