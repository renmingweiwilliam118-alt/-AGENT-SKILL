# WeChat Automation on Windows: What Works and What Doesn't

## The Qt Quick Barrier (WeChat 4.0.5+)

WeChat PC migrated from Qt Widgets to Qt Quick/QML around version 4.0.5.
In the old architecture every UI control had its own Win32 HWND, so
UIAutomation could enumerate the full control tree. In the new architecture
the entire UI is rendered via OpenGL onto 1-2 canvas windows — controls no
longer have independent HWNDs, and UIAutomation sees only an empty shell.

### How to confirm

```python
import uiautomation as auto
win = auto.WindowControl(ClassName="Qt51514QWindowIcon", searchDepth=1)
# Walk the tree; if total accessible nodes <= 2, it's Qt Quick
```

Observed on a live WeChat 4.x: total accessible nodes = 1, a single
`PaneControl` at 1×1 pixels. No EditControl, no buttons, no lists.

### Process name

The main WeChat process on Windows is `Weixin` (not `WeChat`). Child
processes are `WeChatAppEx`. Find the main window by pid or by class
`Qt51514QWindowIcon`.

## Three Escalation Tiers

### Tier 1: Force Software Rendering (non-invasive, try first)

Qt Quick uses GPU-accelerated rendering by default, which triggers the
composite-window path that hides controls. Forcing CPU software rendering
makes Qt fall back to QWidget mode where controls are individually
addressable.

**Method A — environment variables** (before launching WeChat):
```
set QT_ANGLE_PLATFORM=software
set QT_OPENGL=software
WeChat.exe
```

**Method B — compatibility settings**:
Right-click WeChat.exe → Properties → Compatibility → "Change high DPI
settings" → check "Override high DPI scaling" → set to "System" or
"System (Enhanced)".

**Method C — disable discrete GPU** for WeChat in NVIDIA/AMD control panel.

**Trade-off**: slightly higher CPU usage. Fully reversible: remove the env
vars or compatibility flag and WeChat returns to normal.

### Tier 2: Activate the Qt Accessibility Gate (non-invasive, high success)

WeChat 4.1.x has a conditional accessibility provider: it only exposes the
full `mmui::*` control tree (including `chat_input_field`) when it detects
that a screen reader or UIAutomation client is attached to the process.

**Approaches**:
- Write a minimal UIAutomation client that attaches to the WeChat process
  (reference `UIAutomationClient.dll` + `UIAutomationTypes.dll`).
- Temporarily enable Windows Narrator while the automation runs.
- Industry projects (e.g. `wechatauto-replica`) write the screen-reader
  flag directly into `Weixin.dll` via RVA scan to "hot-activate" the gate.

**Result**: the full control tree materializes, and you can locate the
input field by name/automation-id instead of guessing pixel coordinates.

### Tier 3: DLL Injection / Protocol Hook (gray-area, highest risk)

Projects like `WeChatFerry` (≈6.4k stars) reverse-engineer WeChat's internal
function addresses and inject a DLL to intercept calls. This provides:
- Real message callbacks (no polling)
- Works when WeChat window is minimized
- Full operations: send text/image/file/@mention/forward

**Downsides**: version-pinned (breaks on every WeChat update), legal gray
area, account ban risk. Only use if the user explicitly requires real-time
bidirectional message monitoring.

## Reading messages: local database decryption (verified working)

**WeChat stores everything locally in SQLCipher-4-encrypted databases**
under `xwechat_files/<wxid>/db_storage/`:

- `contact.db` — contacts
- `message_N.db` — message shards (a conversation's history is split
  horizontally across shards, and `local_id` restarts at 1 **per shard**,
  so `(user, local_id)` is NOT a unique key — carry the `shard` filename
  with every row or a by-id read returns the wrong shard's message)
- `sns.db` — Moments (朋友圈)

The account id, DB key and image key are all extractable locally with the
WeChat client running and logged in. `wechatauto-replica` implements this
(`from wechatauto import WeChatDB`) and on a live 4.1.15 client reported
19/19 databases decryptable, image key obtained.

**This path is version-insensitive** (it never touches the UI) and is far
more accurate than screenshot-OCR for reading messages: exact text, full
history, no per-frame vision calls, no coordinate math.

### Install note

```
pip install wechatauto-replica cryptography pycryptodome psutil pyperclip
```
The full dependency set includes `winsdk`, `opencv-python`, `zstandard`;
`winsdk` requires Microsoft Visual Studio (scikit-build) to compile a
wheel and fails on machines without it — install with `--no-deps` plus the
specific deps you need, and expect the OCR sending channel to be
unavailable without `winsdk`.

## Hot-activation measured: the ceiling is version-pinning

The accessibility gate is real and writable, but the *control-address
layout* that follows it is version-specific. Measured on WeChat 4.1.15:

- Hot-activation **works**: writing the gate byte in `Weixin.dll`
  (`Weixin.dll+0xb135c38: 0 -> 1`) materializes the tree — window class
  changes from `Qt51514QWindowIcon` (empty shell) to `mmui::MainWindow`
  (real main window), and accessible nodes go from 1 to 40-50 real
  controls (buttons, groups, toolbars).
- **With that tool, no standard `EditControl` ever appears** for the chat input
  box, even with a conversation open: the input is custom-painted and the
  RVA tables used to locate it are pinned to a specific WeChat build
  (`wechatauto-replica` documents 4.1.12; the user's client was 4.1.15).
  **This is a limit of that tool's RVA table, not of UIA itself** — cua-driver
  reads the same input box on the same client as `role=Edit` (next section).
- `open_chat("文件传输助手")` returned `False` — its UIA search depends on
  the OCR channel, which is dead without `winsdk`.

**Rule**: hot-activation buys you a *real control tree*, but locating the
input box inside it is only reliable on the exact WeChat build the tool's
RVA table was made for. A minor WeChat update re-breaks it — the same
version-pinning weakness as Tier 3, just at a smaller blast radius. Always
measure the user's actual WeChat version before promising a UIA-based send.
The exception is cua-driver, below — it resolves the input box by role/label
rather than by a hardcoded RVA, and was verified on 4.1.15.

## cua-driver CLI: the verified working UIA path (measured on WeChat 4.1.15)

Where bare `uiautomation` reads an empty shell (1 node) — or, after
hot-activation, ~50 controls with no addressable input — **cua-driver**
(the trycua computer-use driver, `cua-driver` + `cua-driver-uia`, a
standalone pair of Windows executables, ~20-29 MB each) walks the **full
161-element** WeChat tree including the chat input, the session list and the
message list. Being plain executables, it embeds into a PyInstaller bundle
with no Python dependency — that is what makes an independent desktop app
able to drive WeChat without Hermes running.

A ready-to-run distilled implementation ships with this skill:
`scripts/wechat_cua_probe.py` (`probe` = read-only tree dump + control
location; `send "文字"` = open a session, send, verify).

### Setup: the daemon must be running or `call` hangs forever

`cua-driver call <tool>` blocks indefinitely when no daemon is up (this is
the classic "the CLI just hangs" trap). Bootstrap it first:

```
cua-driver status                 # "daemon is not running" -> serve it
cua-driver serve                  # background; named pipe \.\pipe\cua-driver
cua-driver status                 # poll until "is running"
```

### CLI form and output parsing

```
cua-driver call list_windows --args '{}'
cua-driver call get_window_state --args '{"pid":9208,"window_id":656648,"include_screenshot":false}'
cua-driver call set_value --args '{"pid":9208,"element_token":"s00000025:76","value":"hi"}'
cua-driver call hotkey --args '{"pid":9208,"element_token":"s00000036:76","keys":["enter"]}'
```

- Args are a **single JSON object** after `--args` (not `--pid 9208` flags).
- `get_window_state` requires BOTH `pid` and `window_id`; get them from
  `list_windows` (match `app_name`/`title` for Weixin/微信).
- stdout is prefixed by a telemetry line, so it is **not** pure JSON:
  extract the last balanced `{...}`/`[...]` span, don't `json.loads` the
  whole stream.
- **Treat `status: "refused"` as a hard failure.** A refusal (e.g.
  `snapshot_id_required`) is a normal-looking JSON object; returning it as
  success is how a send logs "已写入并点击发送" while nothing happened.
  Hoist `refusal.message` into an `_error` field the moment you parse.

### Element shape — there is no `id` field

```json
{"element_index": 76, "element_token": "s00000025:76", "role": "Edit",
 "label": "Peerless", "value": "…", "frame": {"x":1155,"y":687,"w":437,"h":98},
 "depth": 18, "parent_index": 75, "enabled": true}
```

- The automation-id (`chat_input_field`, `chat_message_list`,
  `session_item_<name>`) lives **inside `label`** — match by substring, not
  by an `id` key.
- `element_token` (`s<snapshot>:<index>`) is the only address that actions
  accept; it carries the window id and snapshot id.
- The chat input's own `label` is the **contact name**; the string
  `chat_input_field` appears on its child `Group`. Locate the input as
  `role=Edit` **and** `frame.w >= 200` (the chat input is ~437 px wide),
  which excludes the small top-right search `Edit`; fall back to the
  largest Edit by area.

### The verified send sequence

1. `get_window_state` → find the input `Edit` (role + width, or label
   containing `chat_input_field`).
2. `set_value` with the element's `element_token` → text lands in the input
   (UIA write, so it is IME-safe for Chinese; confirmed by re-reading
   `value`).
3. **Re-read the tree.** `set_value` mutates the control tree, so the old
   token is stale — the next action with it fails `stale_element_token`.
4. `hotkey` with `keys:["enter"]` and the FRESH input token → WeChat sends.
5. Verify: the message appears as a `ListItem` inside the message-list
   container, and the input's `value` is now empty.

Pitfalls proven on the way there:

- **Clicking the 发送 button does not work.** Background invoke is a
  verified no-op (`effect: unverifiable`, input box unchanged); foreground
  escalation fails with `foreground_unavailable` because WeChat's HWND
  cannot take the OS foreground while another window is active. Enter via
  `hotkey` is the reliable send.
- **Do not pass `query` to `get_window_state`.** The projection returns only
  matching rows plus their ancestor chain, which *deletes sibling controls*
  — with `query="chat_input"` the input and the whole session list vanish.
  The tree is ~161 elements; read it whole and filter in Python.
- `hotkey` takes `keys` as an **array** (`["enter"]`, `["ctrl","c"]`), not
  a `"ctrl+c"` string.
- Scope message reads to the message-list container: its `ListItem`s have
  `element_index > container.index` and `depth > container.depth`; without
  that filter you read the left-hand **session** list instead and "verify"
  against the wrong list.
- **Pass only `pid` + `element_token` to an action.** The schema is
  `additionalProperties: false` and the doc states that when
  `element_index`/`snapshot_id`/`window_id` are supplied alongside the token
  they *must agree* — sending all of them gets the call rejected even with a
  valid token. The token alone carries the window and snapshot.
- **`element_token` embeds the snapshot id** (`s00000025:76`), so it goes
  stale the moment the tree changes — hence the mandatory re-read at step 3.

### Cost model — and the one knob that matters for latency

Measured per call on a live client: `get_window_state` ≈ 1.3 s,
`set_value` ≈ 0.8 s, `hotkey` ≈ 0.7 s. The tree read is pure process-spawn
plus named-pipe round trip, and it dominates: a send with read-back is
**3 reads ≈ 4 s** of its total.

- `max_depth`/`max_elements` shave only ~0.15 s (1.50 → 1.17 s at
  `max_depth=12`) and truncate the tree, risking loss of deep controls like
  the input box — **not worth it**. Don't offer them as a speed fix.
- The real lever is **how many reads you do**. Fold verification into
  `send()` so the post-send read is the verify read (3 reads → 3, but no
  separate round trip), and expose `send(text, verify=False)` as the
  default for latency-sensitive callers: 2 reads ≈ 3.5 s instead of ≈ 5 s.
  Verification is then an opt-in, not a tax on every send.
- A send that must also `open_session` first pays one extra read
  (~1.3 s) for the session lookup. In a monitoring flow the conversation is
  usually already open — make session switching conditional rather than
  per-send.
- First call in a process pays daemon bootstrap (~7 s); reuse one
  `WeChatCua` singleton thereafter.

### What this replaces

With cua-driver in place, the screenshot → vision-coordinate → `SendInput`
path (rules 16-17) is no longer needed for WeChat: no coordinate guessing,
no focus theft, no per-frame vision call, and a read-back that proves the
send. Keep the native-lock discipline for the app's own remaining ctypes
code, and keep the vision path only for apps cua-driver cannot address.

### Embedding cua-driver into a desktop app (verified integration pattern)

The bridge module that wraps everything above (`probe`/`send`/`messages`
from the shipped script) is a ~150-line stdlib-only module:

```python
class WeChatCua:
    def connect(self): ...          # find_wechat() -> (pid, wid); reuses across calls
    def open_session(self, name): ...  # click the ListItem whose label startswith name
    def send(self, text): ...       # the verified sequence: set_value -> re-read -> hotkey enter
    def verify_sent(self, text): ...  # message-list containment + input-cleared check
    def read_messages(self, limit): ...  # ListItems scoped to the message-list container
    def _els(self): ...             # get_window_state full tree, NEVER with `query`
```

**Locate the exe in this order**: `RFLOW_CUA_DIR` env var → `sys._MEIPASS/cua-driver/`
(frozen build) → exe's own directory (frozen) → `shutil.which`. The frozen
build must bundle it or the app can't run standalone.

**PyInstaller packaging** (verified, builds to ~40 MB from ~20 MB):
```
--add-binary "C:/path/to/cua-driver.exe;cua-driver" --add-binary "C:/path/to/cua-driver-uia.exe;cua-driver"
```
Both binaries must be included — `cua-driver.exe` alone fails at runtime.
Verify the bundle actually contains them by grepping the generated
`rflow_desktop.spec` for `binaries=[` — the build log itself will NOT
mention cua-driver, so absence from the log is not evidence of absence.

**Send-layer integration**: the app's existing execute path becomes
cua-first with legacy fallback. Add a `send_engine` config key (default
`"cua"`, fallback `"legacy"`). The new path:

```python
def _cua_ready():
    return _cua is not None and _cua.available() and load_agent().get("send_engine", "cua") == "cua"

def _cua_send(draft):
    # connect once, reuse via a module-level singleton ([None] box)
    # on exception, reset the singleton so the next call reconnects
    # returns (ok, note) — never fake success
    ...

def _execute(click_pt, draft, mode):
    if mode == "dry-run": return
    def w():
        if _cua_ready():
            ok, note = _cua_send(draft)
            if ok: log("exec", "[cua] 已发送并确认"); return
            log("llm", f"cua 通道未成功（{note}），回退旧注入")
        # legacy: screenshot-coordinate injection — but click_pt may be None
        # in cua mode, so guard BEFORE the native-lock block
        if not click_pt:
            log("error", "无法发送：cua 不可用且无点击坐标"); return
        with _inject_lock: ...  # existing legacy code
```

The legacy path's caller (`run_send`) has a hard `if not click_pt: return`
gate that must be relaxed to `if not click_pt and not _cua_ready(): return`
— cua mode doesn't need a click point, and without this relaxation the
button is dead in cua mode.

**Test the integration synchronously** before packaging: `_execute` runs
its work in a daemon thread, so a test that calls `_execute` and sleeps
will see nothing in the log if the daemon took >6 s to start. Call the
underlying `_cua_send(draft)` directly in a test — it's synchronous and
returns `(ok, note)` — to prove the logic, then trust the async wrapper.
(First call also pays the daemon bootstrap, ~7 s; subsequent calls reuse the
singleton connection.)

**Suppress the console windows.** An embedded cua-driver is invoked via
`subprocess` on *every* action, so each call flashes a black console box
unless every invocation carries `creationflags=CREATE_NO_WINDOW`. Define
one module constant and pass it to all three: the `call` fast path, the
`status` poll, and the `serve` Popen. Getting this on only the `Popen` is
the usual mistake — the user reports "一直弹命令框" while the daemon startup
looks clean. See SKILL.md rule 21.

### Multi-contact auto-switching (scan sessions → reply → switch)

Everything needed to serve many contacts in one loop is addressable on the
same tree. Measured working on WeChat 4.1.15:

**Enumerate the session list.** Session `ListItem`s live in the LEFT column;
message `ListItem`s in the right. Distinguish them by `frame.x` — measured
session column ≈ x 1001, message column ≈ x 1301. Measure on the client
you ship to; do NOT hardcode a threshold like `x < 600` (the WeChat window
may be positioned anywhere, and `frame.x` is window-local, not screen — a
wrong cutoff silently returns an empty session list).

**Element fields worth using:**

- Label format is `名字\n最新消息预览\n时间\n[消息免打扰]` — take the first line as the contact name.
- Unread count appears INSIDE the label as `[N条]`; parse it with a regex (`[\[（](\d+)\s*条?[\]）]`). There is no dedicated unread boolean.
- `selected: true` marks the conversation currently open.

**Clicking a session while WeChat is MINIMIZED is refused**:
`{"code":"window_minimized","effect":"refused"}` — the element resolves to
the Win32 iconic sentinel rather than a display location, so the click is
dropped on purpose. Fix by activating the window first:

```
cua-driver call bring_to_front --args '{"pid":9208,"window_id":656648}'
# → {"restored":true,"raised":true,...}; clicks succeed after this
```

There is no `show_window` tool — discover the real tool set with
`cua-driver list-tools` (useful names: `bring_to_front`, `set_window_frame`,
`press_key`, `type_text`, `list_windows`, `verify_state`) instead of guessing
argument shapes.

**The loop that worked** (one round per cycle):

1. Reuse a single `WeChatCua` connection (first call pays daemon bootstrap).
2. `bring_to_front` — always, before any click, or the whole round silently
   no-ops on a minimized client.
3. `find_unread()` — session list filtered to `unread > 0`, sorted descending.
4. Per contact: skip service accounts (腾讯新闻 / 公众号 / 微信游戏 /
   微信支付 / 订阅号) — auto-replying to a news digest is a visible bug.
5. `open_session(<element dict>)` — pass the element captured from the list
   read (its token), not a re-match by name; the tree changed since the
   snapshot. Accept either a name or an element in the bridge signature.
6. `read_messages(6)` → filter out messages already replied to, keyed per
   contact (`{session_name: set(norm keys)}` in the app core) — without this,
   every cycle re-replies the same unread thread.
7. `compose_draft(conv, ctx, kb, agent, llmc)` → `send(draft)` → record the
   replied keys.

Each `open_session` costs one extra tree read (~1.3 s), so make session
switching conditional on there being unread contacts — a round with zero
unread costs exactly one `bring_to_front` + one list read.

### Post-embedding crash: the picker/monitor race surfaces only in the packaged app

Embedding cua-driver does not touch the app's existing screenshot picker, so
the pre-existing native-call races of SKILL.md rules 17/19 become *more*
visible: the app now has more threads in native code. Measured after
integration: clicking "桌面圈选" produced a successful pick in the log and
then killed the process ~5 s later with `python314.dll 0xC0000005` — the
picker's window churn racing the monitor loop's `grab_png`. Fix with the
`core.picking` mode flag (SKILL.md rule 19); the cua integration itself was
not the cause and needed no change.

### Embedding order that worked

1. Write the bridge module and verify it **standalone** with a synchronous
   test of `WeChatCua.send` (not through the app).
2. Integrate into the send layer (cua-first + legacy fallback, `send_engine`
   key, relax the `click_pt` gate).
3. Verify `_cua_send` synchronously **before** packaging — the async wrapper
   hides failures (see above).
4. Package with `--add-binary` and verify via the generated `.spec`.
5. Fix the pre-existing native races (rules 17/19/20) and re-verify in the
   packaged binary — step 3's clean result does not predict the packaged
   app's behaviour, because the races only bite when all threads are live.

## Fallback: Vision + Simulated Input

When none of the above are acceptable, the fallback is screenshot → vision
model (OCR + coordinate estimation) → `SendInput` mouse/keyboard simulation.
This is what the current RFlow app uses. Its ceiling is the vision model's
coordinate accuracy — see the region-picker-rubberband reference for
clamping and focus-management techniques.

For **sending**, the only genuinely stable, legal, receipt-backed option is
the **WeCom (企业微信) official HTTP API** — no UI, no coordinates, no
version pinning. If the user has `corpid` + app `secret`, that is strictly
better than every GUI tier above for the send direction.

## Python libraries available

- `uiautomation` — Windows UIAutomation bindings (installed in Hermes env);
  reads only the empty Qt Quick shell on WeChat 4.x
- `comtypes` — COM interop (installed)
- `pywinauto` — NOT installed in Hermes env; `pip install pywinauto` if needed
- `wechatauto-replica` — DB-decryption reader + UIA/OCR hybrid sender
- `cua-driver` / `cua-driver-uia` — standalone trycua executables shipped
  with Hermes under `tools/cua-driver-*/`; the only UIA client measured to
  read WeChat's full tree and to complete a verified send. Locate with
  `where cua-driver` or the `RFLOW_CUA_DIR` env override.

## Source references

- WeChat 4.0.5 Qt migration analysis: vidibot.com/2129
- Qt framework research: vidibot.com/2115
- Cross-platform feasibility survey: yage.ai
- wechatauto-replica (PyPI + github.com/fanyuantaier/wechatauto-replica)
- cua-driver: github.com/trycua/cua — `call`/`describe`/`serve` subcommands;
  run `cua-driver describe <tool>` for any tool's authoritative input schema
  (cheaper than guessing arg names and getting `invalid arguments` back)

