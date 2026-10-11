---
name: ctypes-win32-windows
description: "Use when building native Win32 windows in pure ctypes."
---

# Native Win32 windows in pure ctypes (Windows)

Class of task: creating native topmost/tool windows — screen overlays, dimming masks, drag-to-select rubber-band pickers — in pure Python `ctypes`, without a GUI toolkit. (Not the common pywebview-dialog case — see pywebview-windows.)

## When to Use

Pick this when you must create real Win32 topmost/tool windows from Python without a GUI framework: a click-to-select / drag-to-select screen-region picker, a dimming or attention mask over other apps, a click-through floating overlay, or any native topmost window a toolkit won't give you. Skip it for ordinary in-app dialogs and menus (use pywebview / WinForms). The difficulty of this class is ctypes-specific — calling-convention crashes and callback lifetime, not window logic — where sessions lose the most time.

## Core rules (violating any one corrupts the process at runtime)

1. **64-bit `WNDPROC` must use `ctypes.c_size_t` / `ctypes.c_ssize_t`** for the `WPARAM` and `LPARAM` positions, and set the matching `DefWindowProcW` `argtypes`. Using 32-bit `wintypes` types here over/underflows the native calling convention and crashes with `0xC00000CD` (stack overflow) on the very first message dispatch.
   ```python
   WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.c_void_p, ctypes.c_uint,
                                 ctypes.c_size_t, ctypes.c_ssize_t)   # 64-bit
   u.DefWindowProcW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]
   ```

2. **Prefer NO Python `WNDPROC` trampoline: assign the bare C address of `user32.DefWindowProcW` to the class's `lpfnWndProc` field when the windows do no custom message handling.** The C trampoline a `WINFUNCTYPE` callable owns is freed when the Python object is GC'd, but Windows still references that address in the class table — the next dispatch on any window of that class is an access violation, and at process exit the main thread's GC can reclaim a still-alive thread's trampoline → `RC 0xC0000005`. If input is tracked via global `GetAsyncKeyState`/`GetCursorPos` (click-through overlay) and windows are repositioned with `SetWindowPos`, a stock `DefWindowProcW` is enough: set `lpfnWndProc` to `u.DefWindowProcW` directly (it is a `c_void_p` address). If you DO need custom message handling, wrap in `ctypes.WINFUNCTYPE` and retain the callable in a module-global list for as long as any window of the class exists.

3. **Windows are thread-affine: create, pump, and destroy a window on the same thread.** Whatever thread created it must run the message pump (`PeekMessageW`/`DispatchMessageW`) and `DestroyWindow` for it.

4. **Probe layering APIs before committing to a screen overlay.** Some machines return `FALSE` with `ERROR_INVALID_PARAMETER` (87) from `SetLayeredWindowAttributes`/`UpdateLayeredWindow` and will never show a transparent overlay there. Run a 5-line probe first; on failure, fall back to the solid-windows mask in `references/`. Pixel/buffer correctness is NOT your problem — validate the API call returns truthy, not the data.

5. **DPI: check before enabling awareness.** If `mss`/screen-capture and `GetSystemMetrics` are in the same coordinate space on the user's machine, do NOT call `SetProcessDpiAwarenessContext` — it shifts the coordinate system and breaks existing logic. Probe with a tiny script; only enable when the two differ.

6. **Make a window-owning picker exit-clean by killing the trampoline, then use transient `join`ed threads.** The exit-time `RC 0xC0000005` seen with a *resident* long-lived window thread comes from the main thread's GC reclaiming that thread's `WINFUNCTYPE` C trampoline at `Garbage-collecting` (faulthandler shows the fault on the main thread, not the window thread). The confirmed-clean fix has two parts: (a) register the window class **once on the main thread** with `lpfnWndProc` = bare `DefWindowProcW` address (rule 2) so there is **no trampoline to collect** — note `RegisterClassExW` must run on the main thread; calling it from a background thread segfaults (`RC 139`); (b) run each pick in a **transient** thread that creates/repositions/destroys the solid overlay windows and is then `thread.join`ed before the main thread proceeds or exits. With no trampoline in play, `join` is safe — this is the inverse of the old "resident daemon thread, never join" design, which is exactly what crashed at exit. Always measure the real subprocess `returncode` (`0`), not just that the runtime pick returned correct coordinates.

7. **faulthandler cuts both ways — use it to locate the fault, judge crashes by exit code.** `faulthandler.enable()` reports a "Windows fatal exception: access violation" at thread teardown even when the process exits `RC 0`, so a non-zero-looking dump does not prove a crash — confirm the real `subprocess` return code first. But when the process *does* die (`RC 0xC0000005`), read faulthandler's per-thread stack dump to find *which* thread and *what* it was doing: the fault is often NOT on the thread you edited (this session: main thread at `Garbage-collecting`, not the ctypes window thread). Locating the actual fault thread is what turns "something crashes at exit" into a diagnosable bug.

8. **On x64, declare `argtypes`/`restype` on every function that returns OR consumes a handle/pointer, or you get `OverflowError: int too long to convert`.** A handle (HGLOBAL, HBITMAP, HWND, HDC, HMENU) is a 64-bit pointer. Without `restype = c_void_p` a large handle is read back truncated/signed; and without `argtypes = [c_void_p, …]` on the *consumer*, passing that large int back coerces it to a 32-bit C `int` and the call raises `OverflowError: int too long to convert` naming **"argument 1" = the handle you passed (not usually a coordinate)**. This bit the clipboard text path: `h = GlobalAlloc(...)` returned `0x0000028e764a0008`, and `GlobalLock(h)` with no declared `argtypes` crashed the send. Set `restype=c_void_p` on the getter (`GlobalAlloc`, `CreateWindowExW`, `CreateBitmap`, `SelectObject`, …) and `argtypes=[c_void_p, …]` on each consumer (`GlobalLock`, `GlobalFree`, `GlobalUnlock`, `SetClipboardData`, `DestroyWindow`, `IsWindow`, `ShowWindow`, `SetForegroundWindow`, `SetLayeredWindowAttributes`, …). `SetCursorPos` takes screen coords, not a handle — declare `argtypes=[c_long, c_long]`.

9. **Clamp LLM/vision-supplied screen coordinates before `SetCursorPos`.** A model that returns a click target or `input_box` can emit values that are negative, huge, or off by the region origin. Clamp into the virtual-screen rect from `GetSystemMetrics(78..81)`, and reject a box whose relative coords are wildly out of range (treat it as "target not located", re-prompt the model) rather than flying the cursor to a wrong control.

10. **After refactoring away module-level picker state (resident thread, command queue), grep the whole module for every removed symbol before packaging.** `py_compile` does not catch this: a dangling `if _picker_cmd_q is None:` compiles clean and only explodes with `NameError` at runtime on the user's first click — which reads as "the button does nothing." Before rebuilding, search the module for each retired name (`_picker_cmd_q`, `_picker_res_q`, `_start_picker_thread`, …) and fix every surviving reference; the same sweep applies to the picker class-registration entry point that the old architecture owned.

11. **Serialize ALL native calls (capture + key/mouse injection) behind ONE module-level `threading.RLock()` when any background thread coexists with the main thread.** Concurrent `mss` grabs and `SendInput`/`SetCursorPos` dispatch from monitor, recognize, inject, and host-main threads intermittently crash the interpreter itself — the Windows event log names `python3xx.dll 0xC0000005`, not your code, and it reads as "the app dies when I click Recognize." One lock per process makes native access single-threaded while all your async work stays parallel. Use **RLock, not Lock**: an inject path that holds the lock and then triggers a re-capture (read-back verification, rule 13) re-enters the same lock on the same thread and deadlocks instantly with `Lock`.

12. **Focus the target window by removing YOUR window, not by force-focusing theirs.** Calling `SetForegroundWindow`/`SetFocus` from a worker thread races the host GUI thread's message pump and is itself an `0xC0000005` trigger. Before injecting, minimize your own window (`ShowWindow(main_hwnd, 6)`), let the target rise naturally, inject, then restore (`ShowWindow(main_hwnd, 9)`) after. A double click into the input field is more reliable than one click — single-line chat inputs often need the second click to materialize the caret.

13. **Log "sent" only after read-back verification.** An injection path that ends with `log_event("已发送")` unconditionally produces the exact failure users report as "it says sent but nothing happened in the app." After injecting (before restoring your window), capture the monitored region again and ask the vision model whether the text actually appeared; write success only on confirmation, and on failure log what was seen and why. Verification code must not throw — return `(False, reason)` on any exception rather than pretending success.

14. **On Windows, the user's "Desktop" is often OneDrive-redirected.** `C:\Users\X\Desktop` can be an empty ghost folder while the real desktop is `C:\Users\X\OneDrive\Desktop`; delivering an exe to the ghost path means the user keeps double-clicking the OLD copy and every fix looks like it never landed. Resolve the real desktop with PowerShell (`[Environment]::GetFolderPath('Desktop')`) before copying, and when a user reports "none of your changes took effect," check which path the running process actually launched from before touching code.

## Self-test loop (always verify before delivery)

Build the window logic, then drive it with a small test that injects input instead of the user's hand: move the real cursor with `SetCursorPos`, inject left-button press/release with `SendInput`, read the resulting `(l,t,w,h)`, and assert coordinates and a clean `RC`. This is how the picker in `references/rubber-band-picker.md` was validated.

## References
- `references/rubber-band-picker.md` — the proven screen-region picker recipe: class registration, 4-dark-block overlay mask + 3px border + Static hint, the `GetAsyncKeyState`/`GetCursorPos` drag loop, the resident-thread wiring, and the `SendInput` self-test.
