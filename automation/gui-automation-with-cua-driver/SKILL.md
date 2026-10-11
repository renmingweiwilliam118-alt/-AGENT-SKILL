---
name: gui-automation-with-cua-driver
description: Automate GUI apps via cua-driver. WeChat/Qt control-level.
tags: [automation, cua-driver, wechat, gui, pyinstaller, desktop]
---

# GUI Automation with cua-driver

## When to Use

- Automating Windows desktop apps that use self-drawn UI (Qt Quick, Electron, Chromium)
- Standard UIAutomation returns empty control trees for the target app
- Need control-level (semantic) interaction instead of coordinate-guessing
- Building a standalone desktop app that embeds automation capabilities

## Core Architecture

cua-driver is a standalone Rust binary (`cua-driver.exe` + `cua-driver-uia.exe`).
It runs as a background daemon and accepts CLI calls. Unlike raw `uiautomation`
library, it can read control trees from self-drawn apps that expose no standard
UIA controls.

## Setup

```bash
# Start daemon (must run before any calls)
cua-driver.exe serve &

# Verify daemon is running
cua-driver.exe status
# Expected: "Cua Driver daemon is running"
```

## CLI Invocation

All tool calls follow: `cua-driver call <tool_name> --args '<JSON>'`

### Key Tools

| Tool | Purpose |
|------|---------|
| `list_windows` | Enumerate top-level windows (pid, window_id, title, bounds) |
| `get_window_state` | Read control tree (structured elements + screenshot) |
| `click` | Click by element_token (UIA invoke) |
| `set_value` | Write text directly to input controls (bypasses IME) |
| `hotkey` | Press key combinations (e.g. ["enter"], ["ctrl", "c"]) |
| `bring_to_front` | Activate + restore a window (pid, optional window_id) |
| `set_window_frame` | Set one window's exact frame in desktop coords |
| `type_text` | Character-by-character PostMessage(WM_CHAR) insert |

### Critical Rules

1. **When the user reports a bug you already fixed, suspect a stale process FIRST.**
   PyInstaller onefile users often keep the old exe running (or double-click an
   old copy) after a rebuild. Before re-debugging: kill ALL app processes,
   verify the exe file timestamp matches the latest build, and tell the user to
   re-launch. A visible behavioral difference (e.g. selector frame color
   changed from white to blue) is the fastest proof the new binary is running.

2. **Always use `element_token`, never bare `element_index`.**
   cua-driver refuses bare indices with `snapshot_id_required` error.
   The token carries both snapshot_id and window_id.

2. **Re-read the tree after `set_value`.**
   The control tree changes after writing text (buttons become enabled,
   tokens become stale). Always call `get_window_state` again before
   the next action.

3. **Treat `status: "refused"` as failure.**
   Check the response for `_error` or `status == "refused"`. Do not
   treat a response without explicit `ok: true` as success.

4. **`get_window_state` `query` parameter is too aggressive.**
   It only returns matching rows + ancestor chain, dropping sibling
   controls. Read the full tree (typically <200 elements) and filter
   in your code instead.

5. **All subprocess calls to cua-driver MUST use `creationflags=CREATE_NO_WINDOW` on Windows.**
   Without it, every `cua-driver call` spawns a visible console window that
   flashes on screen. Define `_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)`
   and pass `creationflags=_NOWIN` to every `subprocess.run()` and `subprocess.Popen()`.

6. **cua-driver has NO `id` field on elements.**
   Automation IDs (like `chat_input_field`) are stored in the `label`
   field. Match by substring in label, not by a separate id field.

7. **Clicks fail with `window_minimized` when the target window is minimized — restore it with `bring_to_front` first.**
   A minimized window's elements resolve to the Win32 iconic sentinel
   coordinates (e.g. (1151,871)) which is off-screen for every display, so
   cua-driver refuses the click with `effect: "refused"` and code
   `window_minimized`. There is NO `show_window` tool — the tool that
   activates and restores is `bring_to_front` (`{pid, window_id}`; it
   reports `raised`/`restored`/`now_fg_hwnd`). Call it before ANY click on
   a window the user may have minimized (session switches, background
   clicks in a monitoring loop), then sleep ~0.25s and retry. Check the
   response for `effect == "refused"` — it is a failure even when the
   command exits 0.

## WeChat-Specific Notes

WeChat 4.x uses Qt Quick self-drawn rendering. Standard `uiautomation`
library sees only an empty shell (1 PaneControl). cua-driver reads the
full tree (161 elements) including:

- `chat_input_field` — the message input Edit control
- `发送` — the send button (label exactly "发送", not "发送表情" etc.)
- `session_item_<name>` — session list items
- `chat_message_list` — message history container

### Reliable Send Pattern

```python
# 1. Read tree, find input box (role=Edit, largest frame, or label contains chat_input_field)
els = get_elements(pid, wid)
box = find_element(els, role="Edit", label="chat_input_field", min_w=200)

# 2. Write text via set_value
set_value(pid, box, text)
time.sleep(0.25)

# 3. Re-read tree (tokens are now stale)
els2 = get_elements(pid, wid)
box2 = find_element(els2, role="Edit", label="chat_input_field", min_w=200)

# 4. Send via Enter key (clicking send button often fails in background mode)
_call("hotkey", {"pid": pid, "element_token": box2["element_token"], "keys": ["enter"]})

# 5. Verify: re-read tree, check message list contains the text
#    AND input box value is now empty
```

**Why Enter instead of clicking send button:**
- Background click on send button returns `effect: unverifiable` and often no-ops
- Foreground click fails with `foreground_unavailable` (can't steal focus)
- Enter key via `hotkey` with `element_token` reliably triggers WeChat's send

## PyInstaller Packaging

```bash
# Include cua-driver binaries in the bundle
PyInstaller --onefile --noconsole \
  --add-binary "path/to/cua-driver.exe;cua-driver" \
  --add-binary "path/to/cua-driver-uia.exe;cua-driver" \
  your_app.py
```

In your Python code, find the bundled binary:

```python
import sys, os
if getattr(sys, 'frozen', False):
    cua_path = os.path.join(sys._MEIPASS, 'cua-driver', 'cua-driver.exe')
else:
    cua_path = 'cua-driver.exe'  # dev mode
```

## Multi-threaded Crash Prevention

**Problem:** PyInstaller + multi-threaded ctypes/mss calls cause
`python314.dll 0xc0000005` access violations. Multiple threads calling
mss screenshot or Win32 APIs concurrently corrupts the C extension state.

**Solution:** Global lock around ALL native calls.

```python
import threading
_native_lock = threading.RLock()  # RLock, not Lock — reentrant

def grab_screenshot():
    with _native_lock:
        # mss call here
        pass

def inject_click(xy):
    with _native_lock:
        # Win32 SendInput here
        pass
```

**Additional rule:** Pause background monitoring threads during GUI
operations that also touch native APIs (region selection, screenshot
capture). For heavy Win32 window operations, stop the thread entirely.

## Coordinate Mapping (Preview Thumbnail → Screen)

When displaying a scaled screenshot and letting user drag-select regions:

```javascript
// Single-pass: mouse event → screen pixels
function thumbPos(e) {
  const img = document.getElementById('thumb');
  const box = img.getBoundingClientRect();
  const nw = img.naturalWidth, nh = img.naturalHeight;
  const inv = window._inv;  // real_px / thumbnail_px
  const ox = window._ox, oy = window._oy;  // virtual screen origin
  const fx = (e.clientX - box.left) / img.clientWidth;  // 0..1
  const fy = (e.clientY - box.top) / img.clientHeight;   // 0..1
  return { x: fx * nw * inv + ox, y: fy * nh * inv + oy };
}
```

**Pitfall:** Do NOT multiply by `inv` in multiple places. Calculate screen
coordinates once in `thumbPos`, then use `screenToCss()` (reverse mapping)
for drawing overlay rectangles. Double-multiplying by scale factors causes
drift on non-square images.

## Desktop Overlay Region Selection

For "click a button, then drag on the desktop to pick a region" flows
(e.g. hide app, rubber-band select a chat window), build the overlay with
Win32 topmost windows and keep the UI minimal:

- **No dark mask, no dimming.** Draw only 4 thin border windows (blue,
   `#3E8BFF`-ish) that follow the drag. A full-screen dark mask with a
   transparent "hole" shows as a black screen before the first drag pixel
   (the hole is 0-sized at mousedown) — users report this as "the screen
   goes black". Plain desktop + blue frame is the requested UX.
- Hide the app main window (`ShowWindow(hwnd, 0)`) during picking, restore
  after; the rubber band must be click-through and not steal focus.
- Register window classes in the MAIN thread once (process-level); create/
  destroy overlay windows on a short-lived per-pick thread.
- Stop the monitoring thread entirely during the pick (not just a skip
  flag) — see pyinstaller-native-crash.md.

## LLM Integration (Vision Models)

For screen understanding, use OpenAI-compatible vision APIs:

- SiliconFlow: `https://api.siliconflow.cn/v1` with `Qwen/Qwen3-VL-32B-Instruct`
- Handle 429 (rate limit) with exponential backoff + model fallback
- Handle 500/502/503 with retry (transient server errors)
- Reasoning models (step-5): answer may be in `reasoning` field, not `content`

```python
# Parse response trying all possible fields
txt = (m.get("content") or m.get("reasoning")
       or m.get("reasoning_content") or "").strip()
```

## Fallback Strategy

Always implement a fallback when cua-driver is unavailable:

```python
def send_message(text):
    if cua_available():
        return cua_send(text)  # control-level, reliable
    else:
        return legacy_inject(text)  # coordinate-based, less reliable
```

Configuration flag: `send_engine: "cua"` or `"legacy"` in agent config.

## References

- `references/wechat-automation.md` — WeChat control tree layout, send patterns, session switching
- `references/chat-automation.md` — Conversation memory, self-message re-recognition, vision/agent separation, bubble-position prompt rule, region validation + live re-read, speed optimization, WeCom compliant channel
- `references/pyinstaller-native-crash.md` — Crash analysis, lock patterns, debugging