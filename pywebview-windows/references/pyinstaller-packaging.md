# PyInstaller packaging + headless UI verification for pywebview apps

## Frozen asset / data dir split

- PyInstaller `--onefile` extracts `--add-data` payloads into `sys._MEIPASS` at runtime. Bundled UI files (e.g. `ui/index.html`) must be resolved from `ASSET_DIR = getattr(sys, "_MEIPASS", project_dir)`. `--add-data "ui;ui"` (Windows separator).
- User-writable data (config json, knowledge base, logs) goes in `APP_DIR = os.path.dirname(sys.executable)` when frozen. Mixing these up is the classic white-UI bug: the HTML 404s because it was resolved next to the exe instead of in `_MEIPASS`.
- Working flags: `python -m PyInstaller --onefile --add-data "ui;ui" --collect-data pywebview --hidden-import mss app.py`. `--collect-data pywebview` is required so WebView2 runtime assets ship with the exe.
- For a packaged desktop app that must open with NO console window, add `--noconsole` (alias `--windowed`): `--onefile --noconsole --add-data "ui;ui" --collect-data pywebview --hidden-import mss app.py`. Without it, launching the exe pops a black console window behind the app window — a visible packaging defect. (Debugging a `--noconsole` build loses console log output; use the WebView2 DevTools toggle from SKILL.md or a log file instead.)
- `webview.start(gui="edgechromium")` for pages using `async/await`; keep a bare `webview.start()` fallback.
- Enable DevTools for packaged debugging with an env flag (e.g. `SHIFLOW_DEBUG=1` → `webview.start(debug=...)`) instead of rebuilding.

## Verifying the LIVE instance actually runs the newest build (deploy protocol)

A user reporting 'the UI looks unchanged' after a deploy is usually a STALE-INSTANCE problem, not a build problem. Verify in this order before touching design:

1. Kill every running instance (dev name AND deployed name) — a running EXE is file-locked on Windows; the rebuild/copy fails with a permission error, not a visible 'in use' message.
2. `md5sum` build output vs deployed copy — must match.
3. Purge stale unpacked payloads before relaunch: `_MEI*` dirs sit NEXT TO WHERE THE APP LAST RAN (often the user's Desktop when the exe was deployed there, not only in temp — check both locations), plus the app's WebView2 cache dir (EBWebView under the app's window-title-named folder, in the exe dir and under `%LOCALAPPDATA%`).
4. Relaunch exactly one instance, wait for paint, then MARKER-CHECK the newest unpacked UI copy: read it, assert the NEW design marker string is present AND the OLD marker absent (grep for both). Grep the live asset, not the source tree — the source being correct proves nothing about what the window shows.
5. Only after 1–4 all pass and the user still perceives 'no difference' is it a design-conservatism problem: escalate to a structurally different layout, not another skin pass. When doing the structural pass, leave distinct marker strings for old and new designs so step 4 stays mechanically checkable next time.

### The build interpreter must carry the RUNTIME deps too

`BUILD_DONE rc=0` from a wrapper script proves nothing (rule 22 / SKILL.md), but the converse trap
is quieter: PyInstaller can be installed in the exact interpreter the script invokes and still
produce an exe that dies at launch with `Failed to execute script 'app' due to unhandled exception:
No module named 'PIL'`. PyInstaller analyses imports from ITS interpreter's site-packages — if the
build interpreter lacks `pillow` / `mss` / `pywebview` / `cryptography` (the very modules the app
imports), they are simply not bundled, and the packaged app is born broken while the dev run is
fine. Diagnose with a one-liner before the build, not after:

```
python -c "import PIL, mss, pywebview, cryptography; print('deps ok')"
```

Install the missing ones into the SAME interpreter (`python -m pip install pillow mss pywebview
cryptography pycryptodome pyinstaller`), then rebuild and re-launch the exe to confirm it boots —
a green build log is not a boot test. Add `--hidden-import PIL --hidden-import PIL.Image` for the
image modules, which dynamic-import analysis misses most often.

### Liveness-probe and version-marker pitfalls (false 'crash' / 'no change' reports)

- **Process name is the EXE's file-base name, not the PyInstaller `--name`.** Build with `--name rflow_desktop`, deploy the copy as `RFlowDesktop.exe`, and `Get-Process -Name rflow_desktop` / `pgrep -f rflow_desktop` report NOT-ALIVE even though the app is running fine — a false 'crashed at startup' that sends you re-debugging a perfectly good build. Probe liveness by the DEPLOYED filename's base name (or window title / command line), and when killing stale instances, match BOTH the dev build name and every deployed copy name.
- **An empty stdout/stderr redirect file does not mean the exe crashed.** A `--noconsole` (or even console-subsystem) exe writes nothing to its redirect until it exits; empty capture after N seconds is inconclusive. Check process existence / `HasExited` first; only a dead process plus a non-empty traceback justifies a 'crash' conclusion.
- **Stamp the build version into a startup log line, and re-stamp it whenever the log is cleared, so persisted logs stay identifiable.** Log files live in the data dir next to the deployed exe and survive every rebuild/redeploy — a user re-reporting an old error is usually reading STALE log lines (or an old running instance), not a live bug; and the UI may show an empty log (in-memory items only, booted before the bridge) while the disk file holds the boot marker. When a user says 'the fix did nothing': read the persisted log from disk and grep the version marker FIRST — marker absent ⇒ stale running instance (kill every old-name and new-name process, relaunch, re-check); marker present ⇒ the bug survived the fix, and only then touch code. The re-stamp-on-clear keeps '0 entries' from erasing the only version evidence.
- **Verify the fix end-to-end on the freshly launched instance, not on whatever window the user last had open.** The user's open window keeps running pre-fix code with its own in-memory log even after the exe on disk is updated; 'close every instance, relaunch, then test' is part of the verification, and the version marker (previous bullet) is the mechanical proof the new code is the one running.

## Headless UI verification loop (after each rebuild)

1. Launch the exe as a background process, sleep ~10 s (the bridge boot is a 20 s long-poll — see SKILL.md rule 6).
2. Screenshot with mss + Pillow. Do NOT use PowerShell WinForms `Add-Type` capture — `System.Windows.Forms.Screen` constructor lookup fails on this host and console output comes back mojibake:
   ```python
   import mss
   with mss.mss() as s:          # newer mss: mss.MSS() — bare mss() is "module not callable"
       im = s.grab(s.monitors[1]) # monitors[0] is virtual all-screens; use per-monitor
   from PIL import Image
   Image.frombytes("RGBA", im.size, im.bgra, "raw", "BGRA").convert("RGB").save("shot.png")
   ```
   - `frombytes('RGB', ..., 'raw', 'RGBA')` raises `ValueError: unknown raw mode for given image mode` — mode must be `RGBA` with raw `BGRA`, then `.convert('RGB')`.
3. If the app window is not in the foreground, write a `.ps1` file (never inline `powershell -Command` from git-bash — adjacent `$()`/`==` text corrupts it) that P/Invokes `ShowWindow` + `SetForegroundWindow` on the HWND found by process title, run `powershell -NoProfile -ExecutionPolicy Bypass -File bring.ps1`, sleep 3 s, re-screenshot.
4. Pass the PNG to vision analysis and require the expected key text to actually be visible (status-pill values, KB count, model name) before declaring the UI verified. "It should have rendered" is not verification. Small UI text can also be misread by vision (e.g. a mis-OCR of the app title) — check the source HTML before "fixing" copy that only the screenshot got wrong.
5. Clean up: kill the app process, and when deploying a copy elsewhere, verify with `md5sum` that both sides match. Before rebuilding or overwriting a deployed copy, kill EVERY running instance (the test build AND any deployed copy) — a running exe is file-locked on Windows and the build/copy fails with a permission error, not a visible "in use" message.
6. If mss full-screen captures are blocked (lock-screen overlay returns wallpaper instead of the window) or the foreground nudge did not take, capture the window client area directly via `PrintWindow` — see the section below.

## PrintWindow window capture (fallback when mss sees the lock screen)

`PrintWindow` + `GetDIBits` captures a specific window's client area and renders WebView2/EdgeChromium content that a desktop screenshot cannot see while the session is locked. Recipe: wait ~12–15 s after launch (WebView2 paint), `EnumWindows` filter by window title to find the HWND, `GetClientRect` for the client rect, create a compatible DC + memory bitmap, `PrintWindow(hwnd, hdc, PW_RENDERFULLCONTENT=2)`, `GetDIBits` into a BGRA buffer, `PIL.Image.frombytes("RGBA", (w, h), buf, "raw", "BGRA").convert("RGB")` → save PNG. Sanity-check the capture: the non-black pixel ratio should be ~1.0; a solid-color or wallpaper image means wrong HWND or a missing flag, not a broken app.

Capture-by-pid + minimized-window recovery (use when title matching is unreliable — e.g. mojibake/garbled app titles in console output — or when title match finds nothing): enumerate windows via `GetWindowThreadProcessId` == the app pid, pick the visible one with the largest client area. If its client rect is 0×0, the window is almost certainly MINIMIZED (a minimized window parks at an off-screen rect around (-25600,-25600) and reports empty client areas to `GetClientRect`): confirm via P/Invoke `IsIconic`, restore with `ShowWindow(hwnd, 9 /* SW_RESTORE */)` (+ optional `SetForegroundWindow`), sleep ~3 s, then capture. A 0×0 client rect is a window-state signal, not a capture bug — never retry the same HWND in a loop without first checking iconic state.

Pitfalls that cost time on this path:
- The `EnumWindows` callback type is `ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)` — `ctypes.WINFARPROC` does not exist.
- `CreateCompatibleDC`, `CreateCompatibleBitmap`, `SelectObject`, `DeleteObject`, `DeleteDC`, `GetDIBits` live in **gdi32.dll**, not user32 — fetching them from `ctypes.windll.user32` raises `AttributeError` or yields junk handles; use `ctypes.windll.gdi32` for all of them.
- `PrintWindow` WITHOUT the `PW_RENDERFULLCONTENT` (0x2) flag returns a blank/black client area for GPU-composited Chromium content — always pass 2.
- `Image.frombytes` for the BGRA bits needs mode `"RGBA"` + raw mode `"BGRA"` then `.convert("RGB")` — the same frombytes pitfall as the mss step above.
