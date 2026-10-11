# Screen-region drag-to-select picker (proven recipe)

Native drag-to-select screen-region picker in pure `ctypes`. The flow the user wants: hide the main app window → user drags a rectangle over the desktop (e.g. around a WeChat window) → windows clean up → return the absolute screen rectangle → restore the main window. No transparency needed.

## Coordinate contract
Return `(left, top, width, height)` in **absolute** screen pixels, in the same space that `mss` and `GetSystemMetrics(78..81)` use. Do NOT mix per-monitor DPI spaces. On the target machine `mss` and `GetSystemMetrics` already agree (1920×1080 logical), so no DPI awareness call was needed — verify this per-machine before adding `SetProcessDpiAwarenessContext`.

## Overlay mask (no transparency on this class of machine)
Because `SetLayeredWindowAttributes`/`UpdateLayeredWindow` return error 87 here, build the dark backdrop from **four solid topmost windows** that leave the selection rectangle as the visible "hole", plus **four 3px solid-border windows** tracing the rectangle, plus one system `Static` hint bar and one `Static` dimension readout. All use `WS_POPUP|WS_VISIBLE`, `WS_EX_TOPMOST|WS_EX_TOOLWINDOW|WS_EX_TRANSPARENT` (transparent = click-through, so the user's mouse reaches the desktop, not these windows). Reposition with `SetWindowPos` flags `SWP_NOZORDER|SWP_NOACTIVATE|SWP_SHOWWINDOW` (0x0004|0x0010|0x0040). Dark color `#0B1120` → BGR brush `0x002E1A0B`; border `#3E8BFF` → `0x00FF8B3E`.

Four dark blocks per frame (l,t,w,h = selection rect; vl,vt,vw,vh = virtual screen):
- top:    x=vl,          y=vt,          w=vw,                h=max(0, l-vt)
- bottom: x=vl,          y=t+h,         w=vw,                h=max(0, vt+vh-(t+h))
- left:   x=vl,          y=t,           w=max(0, l-vl),      h=h
- right:  x=l+w,         y=t,           w=max(0, vl+vw-(l+w)), h=h

Border bars: top/bottom 3px tall at y=t-2 and y=t+h; left/right 3px wide at x=l-2 and x=l+w.

## Drag loop (input via async key state, not window messages)
Because the overlay windows are click-through, track input globally rather than via window messages:
- `GetCursorPos` → current (cx, cy)
- `GetAsyncKeyState(0x01) & 0x8000` → left button down
- rising edge of down: `start = (cx, cy)`; falling edge: compute rect and finish
- `GetAsyncKeyState(0x1B) & 0x8000` → Esc cancels
- reposition the 8 windows every iteration; update the `Static` dimension text only when it changes
- a sub-4px rect (a click without drag) counts as cancel → return `None`

## Picker threading (exit-clean): bare `DefWindowProcW` + transient `join`ed threads
- Register the overlay window class **once on the main thread** (before any window/DC; a background-thread `RegisterClassExW` segfaults with `RC 139`). Set `lpfnWndProc` to the **bare address of `user32.DefWindowProcW`** (a `c_void_p`), not a `WINFUNCTYPE` callback: the solid overlay windows do no custom message handling — input is tracked globally via `GetAsyncKeyState`/`GetCursorPos` (click-through) and repositioned with `SetWindowPos` — so a stock `DefWindowProcW` is enough. Critically, **no trampoline means nothing for the main thread's GC to reclaim at exit.**
- Run each pick in a **transient** thread: create the solid overlay windows, run the drag loop, destroy the windows, then `thread.join()` it before the main thread proceeds or the process exits. With no trampoline in play the `join` is safe — the inverse of the old "resident daemon thread, never join" design, which is exactly what produced the exit-time `RC 0xC0000005` (main-thread GC reaped the live thread's trampoline at `Garbage-collecting`).
- Runtime is proven: every pick returns the correct rect and the overlay renders, verified headlessly. **The process now exits `RC 0`.** Always confirm with the real subprocess `returncode`, not just that the runtime pick returned the right coordinates.
- **64-bit handle gotcha (text-send path):** if the pick result is delivered through a clipboard text path, `GlobalAlloc`/`GlobalLock`/`GlobalFree` return/consume an HGLOBAL that is a 64-bit pointer. Set `GlobalAlloc.restype=c_void_p` and `GlobalLock`/`GlobalFree`/`GlobalUnlock`/`SetClipboardData` `argtypes=[c_void_p, …]`; otherwise the handle is coerced to a 32-bit int and the call raises `OverflowError: int too long to convert` ("argument 1" = the handle). `SetCursorPos` wants `argtypes=[c_long, c_long]`.

## Headless self-test (inject input, no user)
Validate before delivery by moving the real cursor and synthesizing clicks:
- `SetCursorPos(500,300)`, `SendInput` MOUSEEVENTF_LEFTDOWN (0x0002), step the cursor toward (900,600), `SendInput` MOUSEEVENTF_LEFTUP (0x0004), restore cursor
- assert the returned rect ≈ (500,300,400,300) AND that the full process exit code is `0`. With the bare-`DefWindowProcW`-address + transient-`join`ed-thread architecture above, a full app wrapped around the picker exits `RC 0` — the exit-time AV is no longer a known open issue. If you reintroduce a `WINFUNCTYPE` WndProc or a resident never-joined window thread, the exit may report `RC 0xC0000005`; re-read the "Picker threading" section.
- run without `faulthandler` so you read the true `RC`; but when a non-zero `RC` *does* appear, re-run *with* `faulthandler` and read the per-thread stack dump to find the faulting thread (it is often the main thread at `Garbage-collecting`, not the window thread).
