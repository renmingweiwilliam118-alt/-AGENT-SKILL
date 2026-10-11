# Native desktop region picker (hide → rubber-band → show)

Robust alternative to "drag on a scaled-down screen-preview thumbnail" for picking a monitor region. It operates in **real screen coordinates** so there is no scale/origin math to drift.

## When to reach for this
- A downsampled-preview drag keeps mis-selecting (mapping depends on `naturalWidth`/scale/origin that change when the preview refreshes mid-drag; Y drifts when width and height scaling are conflated).
- The user explicitly wants to point at a target window (WeChat, a terminal) on the desktop rather than on a thumbnail.

Keep the old thumbnail path working if it's cheap; add this as the primary selector and fall back to the thumbnail.

## Workflow
1. **DPI-align the process first** (rule 10). `mss` works in **physical** pixels; `GetSystemMetrics`/`GetCursorPos`/`CreateWindowExW` work in **logical** pixels unless the process is DPI-aware. If they disagree, every coordinate you save is off by the scaling factor and the bug looks like "the selection misses the window." Call `SetProcessDpiAwarenessContext` at process start, before any window/DC exists.
2. JS button → js_api method `begin_region_pick()`.
3. On the **main window HWND** (find it per rule 3): `ShowWindow(hwnd, SW_HIDE=0)`. This reveals the desktop so the user can point at the target app.
4. In a **daemon thread** (js_api runs off the GUI thread — rule 1), build a full-virtual-screen overlay and run a mouse-polling loop to draw a live rubber-band.
5. On release: the release point **is** the screen coordinate — read it straight into `set_region([x,y,w,h])`, no conversion.
6. `ShowWindow(hwnd, SW_SHOW=5)` + `SetForegroundWindow(hwnd)` in the thread's `finally` (so it always restores, even on exception/timeout).
7. Push the result back to the JS bridge (`_push_js`) so the UI refreshes and toasts. Esc cancels; a ~45 s timeout auto-restores the window.

## Overlay: full-virtual-screen layered topmost window

**Escalation tiers — pick by what this host actually allows, in this order, and stop at the first that works.** Do not skip tiers or assume a lower tier's failure is a code bug; it is usually a host restriction:

| Tier | Approach | When it fails | Cost when it works |
|---|---|---|---|
| 1 | `UpdateLayeredWindow` alpha overlay (premultiplied `AARRGGBB`) | some hosts disable layered transparency entirely — every layered API returns error `87` | full control of dimming/border |
| 2 | `SetLayeredWindowAttributes` static layered window + accent box | same error-87 host restriction | simple, no per-frame bitmap blit |
| 3 | Solid opaque Win32 windows (4 dim blocks + 4 border pieces + Static hint bar) via `CreateWindowExW` | works, but creating/destroying real windows in a transient thread inside a **PyInstaller** build triggers `python314.dll 0xC0000005` on teardown (rule 12 — the `DefWindowProcW` bare-address trick mitigates but does not eliminate this on all hosts) | no transparency APIs needed |
| 4 | **Pure global mouse tracking — ZERO window creation.** Just `GetAsyncKeyState` + `GetCursorPos` in a polling loop to read the drag rect | nothing — it never creates a window, so there is no teardown crash surface | no visible box during drag; result shows in the app's preview after release |

**Tier 4 is the correct end state on any host where tiers 1–3 crash or return error 87.** It is not a degraded fallback — it is the most robust implementation, because the crash modes above all come from window/DC lifecycle inside the packaged interpreter, and tier 4 has none. The trade-off (no live desktop box) is acceptable and often preferred: many users do not want a dimmed/overlay desktop at all, just a clean selection. When a user explicitly says "don't darken the screen / just show the box / the screen goes black," go to tier 4 directly and do not try to re-introduce dimming.

Tier-4 shape: a polling loop reading left-button state + cursor position, computing `(l,t,w,h)` on release, returning `None` if `w<4 or h<4` (click without drag = cancel), returning `None` on Esc or timeout, and always restoring the hidden main window in `finally`. Coordinate acquisition only — the visibility feedback lives in the app's own preview pane (rule 20's `screenToCss` maps the saved screen rect back to the preview).
- Register a window class ("RFlowPick"), create with `WS_POPUP|WS_VISIBLE` and `WS_EX_TOOLWINDOW|WS_EX_TOPMOST|WS_EX_LAYERED`, positioned at the mss virtual-screen rect `(vl, vt, vw, vh)`.
- `SetWindowPos(..., HWND_TOPMOST, ..., SWP_NOZORDER|SWP_SHOWWINDOW|SWP_NOMOVE)`. Because the main window is hidden and the overlay is topmost, the desktop shows through everywhere except the overlay — that's what the user points at.
- Paint with `UpdateLayeredWindow` (flag `ULW_ALPHA=0x2`), `BLENDFUNCTION = (AC_SRCOVER=0, 0, 0, AC_SRC_ALPHA=0x02)`. Draw a dim full-screen black, and while dragging draw the four "dark corners" (fullscreen minus the selection rect) so the selection area stays bright, plus a thin accent border.

## ctypes / Win32 pitfalls (these cost the most time)
- **`GetAsyncKeyState` and `GetCursorPos` are in `user32`, NOT `kernel32`.** Only `GetModuleHandleW` (hInstance for `CreateWindowExW`) is in `kernel32`. Grabbing key-state from the wrong DLL silently returns 0 and the picker never detects the mouse button.
- **Reuse one POINT instance for the cursor read.** Do `pt = POINT(); u.GetCursorPos(byref(pt)); cx, cy = pt.x, pt.y`. Reading a *fresh* instance after the call (`cx, cy = _PT().x, _PT().y`) always gives 0,0 — the byref'd instance is the one that gets filled.
- **x64 handle truncation.** `CreateWindowExW` returns an HWND; with the default `c_int` restype the upper 32 bits are lost on 64-bit and you get a garbage handle. Set `u.CreateWindowExW.restype = c_void_p`. Same for every GDI function that *returns* a handle (`CreateCompatibleDC/Bitmap`, `CreateSolidBrush`, `CreatePen`, `SelectObject`) and for `UpdateLayeredWindow` (`restype = c_bool`). Passing a handle as an *argument* also truncates under x64 — set `argtypes` where you pass handles by value, including `DestroyWindow`/`IsWindow`/`ShowWindow`/`SetForegroundWindow`/`SetLayeredWindowAttributes` (`argtypes = [c_void_p, ...]`; also `IsWindow.restype = c_bool` so a 64-bit HWND isn't misread as 0).
- **A `WNDPROC` cannot be a raw `user32.DefWindowProcW` FuncPtr assigned to a `c_void_p` struct field — it raises `TypeError: incompatible types, _FuncPtr instance instead of c_void_p`.** Wrap it in a `ctypes.WINFUNCTYPE(c_ssize_t, LPCWSTR, UINT, WPARAM, LPARAM)` and pass that callable into the `WNDPROC` field; keep a global reference to the callback so it isn't GC'd mid-`RegisterClassExW`.
- **GDI brush/pen colors are premultiplied-alpha `AARRGGBB` in little-endian byte order (i.e. `0xAABBGGRR`).** Accent `#3E8BFF` → `0x33FF8B3E` (15% alpha). Writing it as `0x333E8BFF` swaps the R and B channels. Pure black (`0x66000000`) has no R/G/B so it's unaffected.
- **`FillRect` RECT is left/top/right/bottom**, not x/y/w/h. Write a `_r(x, y, w, h) -> RECT(x, y, x+w, y+h)` helper and use it consistently for the four-corner darkening; mixing the two conventions is the usual cause of a "wrong" dim region.
- **Treat a near-zero box as a cancel**: if released `w < 4 or h < 4` (user clicked without dragging), return `None` (no region saved) rather than storing a 1px region.
- **Always `DestroyWindow(overlay)`** on the success, cancel, and timeout paths, and restore the main window in `finally` — a leaked topmost overlay hides the desktop from the user.
- **The overlay window is created on the polling thread, so pump THAT thread's message queue.** `PeekMessageW`/`DispatchMessageW` on the main thread pumps the wrong queue; the overlay's `WM_CREATE`/paint messages never dispatch and the window can stay broken/invisible. Pump inside the loop you created it in. `DestroyWindow` is asynchronous — after calling it, run a short pump-then-`IsWindow` loop (e.g. up to ~40 iterations) until `IsWindow` returns false on both overlays, otherwise the topmost layer lingers over the desktop.
- **Simpler overlay variant: two static layered windows instead of a per-frame `UpdateLayeredWindow` bitmap.** Create (1) a full-virtual-screen `WS_EX_LAYERED` window dimmed with `SetLayeredWindowAttributes(hwnd, 0, alpha≈0x55, LWA_ALPHA=0x2)` — set once, never repainted — and (2) a small accent-colored box window whose position/size you move with `SetWindowPos(box, None, l, t, w, h, SWP_NOZORDER|SWP_SHOWWINDOW)` on each mouse move. This avoids allocating and blitting a full-screen GDI bitmap every 30 ms and is far less error-prone than hand-building `UpdateLayeredWindow` `BLENDFUNCTION` structs.

- **Dimming-on-mousedown is what reads as "the screen went black."** A tier-3 overlay whose four dim blocks cover the full screen from the moment the button goes down (before the user has dragged, so the selection "hole" is still 0×0) blanks the entire desktop instantly. Two fixes, in order of preference: (a) go to tier 4 (no overlay at all — see the escalation table above); (b) if an overlay must stay, only position the dim blocks once the drag exceeds a small threshold (~6 px on each axis), and before that draw only a tiny accent box at the cursor so the desktop stays visible while the user finds their start point.

## Global-hotkey trigger (start the picker from anywhere)
A UI button is enough when the app is visible, but the user may want to start the pick with the app hidden/minimized/backgrounded. Register a system-wide hotkey and pump it on a **dedicated message-pump thread** — the main GUI thread is owned by `webview.start()`, so a hotkey registered on it never fires.

**Register a fallback chain, not one combo.** `RegisterHotKey` returns `False` when another process already owns the combination (other instances of your own app are the usual culprit, since each re-launch tries the same id). Try `Ctrl+Alt+R`, then `Ctrl+Alt+Shift+R` (`MOD_SHIFT = 0x0004`), and log which one won; if all fail, log the message "use the in-app button" and keep the button as the independent path — the button never depends on the hotkey thread, so a taken hotkey must never degrade the button.

```python
# at process start (main thread, before webview.start()):
threading.Thread(target=_hotkey_loop, args=(api,), daemon=True).start()

def _hotkey_loop(api):
    MOD_CTRL, MOD_ALT, HOTKEY_ID = 0x0002, 0x0001, 0x2A1
    u = ctypes.windll.user32
    u.RegisterHotKey(None, HOTKEY_ID, MOD_CTRL | MOD_ALT, 0x52)   # 0x52 = 'R'; log failure (likely taken)
    MSG = ctypes.Structure  # hwnd, message, wParam, lParam, time, pt
    m = MSG()
    while True:
        r = u.GetMessageW(ctypes.byref(m), None, 0, 0)            # r: 1 OK, 0 Quit, -1 error
        if r in (0, -1): break
        if m.message == 0x0312 and m.wParam == HOTKEY_ID:         # WM_HOTKEY
            threading.Thread(target=api.begin_region_pick, daemon=True).start()
        u.DispatchMessageW(ctypes.byref(m))
```

Set `restype=c_bool` on `RegisterHotKey` and `argtypes=[c_void_p,c_int,c_uint,c_uint]`; `RegisterHotKey` returning `False` means another app grabbed the combo — log it, don't crash. `GetMessageW`/`DispatchMessageW` need `restype`/`argtypes` set too. `begin_region_pick` itself stays a daemon thread that hides the main window, runs `_rubber_band`, and restores in `finally`.

## Coordinate-space sanity check (add a `screen_info` js_api method)
Before trusting a pick, compare in one dict: `mss.monitors[0]` (left/top/width/height) vs `GetSystemMetrics(78,79,80,81)` (virtual-screen left/top/width/height) vs a live `GetCursorPos` vs system DPI. If mss and GetSystemMetrics disagree, the process is **not** DPI-aligned and every save will drift — fix the awareness call first, not the picker math. A one-shot probe where mss width equals `GetSystemMetrics` is NOT proof the *app* is aligned: your probe's interpreter may have been started DPI-aware while the packaged binary was not. Always set the awareness inside the app at startup (before any window/DC) and re-probe within the running app.

## Acting inside the picked window (click → focus → paste → send)

Once a region is picked, the usual follow-up is "type the draft into the target app's input box and
send it." Two failure modes account for nearly every "the log says it worked but nothing happened"
report:

- **Focus, not coordinates.** `SetCursorPos` + a synthetic `SendInput` click never changes the
  foreground window — the click and the subsequent Ctrl+V/Enter go to your own pywebview window.
  Activate the target first:

```python
u = ctypes.windll.user32
u.WindowFromPoint.argtypes = [ctypes.c_long, ctypes.c_long]; u.WindowFromPoint.restype = ctypes.c_void_p
u.GetAncestor.argtypes = [ctypes.c_void_p, ctypes.c_uint]; u.GetAncestor.restype = ctypes.c_void_p
hwnd = u.WindowFromPoint(cx, cy)
top  = u.GetAncestor(hwnd, 2)          # GA_ROOT — the real top-level window
u.ShowWindow(top, 5); u.SetForegroundWindow(top); u.SetFocus(top)
time.sleep(0.12)                       # let the activation settle before clicking
# then SetCursorPos + click, and a second click for input boxes that only show a caret on double-click
```

- **Vision-model coordinates are estimates, not measurements.** They come back skewed, swapped, or
  in full-screen space. Do not gate execution on them being inside the region (a refusal reads as
  a broken button); instead: if a value exceeds ~1.5× the region size, normalize it modulo the
  region size; then clamp both axes to `[0.04·size, size−0.04·size]`. Every recognition then yields
  a usable click point. In the system prompt, state the screenshot's true pixel dimensions and the
  origin (`"这张截图尺寸是 W×H 像素，x∈0~W，y∈0~H，左上角为原点"`) — the model's coordinates get far
  more accurate when it knows the bounds.

- **Execution mode is a safety default, not a convenience.** Ship `exec_mode` defaulting to
  "draft" (fill, human sends) with `auto_reply` off, and expose explicit controls for "auto"
  (click → paste → Enter) and "dry-run". A user who asks for fully automatic sending must flip
  these in the settings UI once; note that a saved `agent.json` overrides the new defaults, so
  when a mode change "doesn't take", check for an existing config file before blaming the code.

## Frontend coordination
- The button calls `begin_region_pick()` and optimistically shows a "hidden, pick on desktop" hint; the JS bridge callback (`shiflowRegionPicked([x,y,w,h])` on success, a warn toast on cancel) is the source of truth — refresh state + thumbnail from it, not from the local click.

### Keeping the thumbnail-drag preview visible
If the thumbnail path is kept as a secondary selector, its live preview is a transient DOM rect drawn in `mousemove`. Two rules keep it behaving:
- **Freeze the mapping at mousedown.** Capture the scale (`clientWidth/naturalWidth`), inverse coefficient and origin once into a `_dragMap` and read from it for the whole drag; recomputing from the live image mid-drag drifts as soon as the thumbnail refreshes under the cursor.
- **Do not call the refresh routine from the mouseup/save handler.** A full repaint of the preview wipes the rect the user just drew, and the box then only reappears on the next interaction — which reads exactly like "the preview didn't show until I released." Persist state (and let the backend push or the explicit refresh button redraw); if the new region must be drawn, draw it explicitly instead of re-rendering the image.
