# RFlow launch / kill / verify

## Kill all RFlow instances

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$LOCALAPPDATA/Temp/kill_app.ps1"
```

The script matches `Name='python.exe' OR Name='pythonw.exe'` with `CommandLine -match 'shiflow-mini' -and -match 'app.py'`. It kills both the main process and the uvicorn worker child.

## Start RFlow (Hermes: no console)

```powershell
powershell -NoProfile -Command "Start-Process -FilePath 'C:/Users/mwr_w/shiflow-mini/.venv/Scripts/pythonw.exe' -ArgumentList 'app.py' -WorkingDirectory 'C:/Users/mwr_w/shiflow-mini'"
```

- Use `pythonw.exe` (GUI subsystem — physically no console). `-WindowStyle Hidden` covers ONLY the direct child: it does not cover Task-Scheduler fires or DETACHED-parent respawns, which each allocate a fresh visible console for a `python.exe` child — the console-subsystem rule the whole supervision chain follows.
- pythonw leaves no stderr on death → diagnose via `data/crash.log` + port 8765 instead of relaunching blindly.
- Two `pythonw.exe` PIDs are expected: the launcher stub + the re-exec'd real interpreter (same CommandLine). Both are normal.
- Wait ~12 s before probing the port (pywebview + uvicorn startup).
- `启动RFlow.vbs` in repo root uses `pythonw.exe` for the user's own double-click startup (works in production; don't use it in dev/test contexts where you need to observe output).

## Verify it's alive

```bash
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8765/api/health
# expect: 200
```

Also check the process:

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe'" | Where-Object {
  $_.CommandLine -match 'shiflow-mini' -and $_.CommandLine -match 'app.py'
} | Select-Object ProcessId, ParentProcessId
# the chain runs pythonw.exe — a python.exe-only filter reads EMPTY and looks like 'app dead'
```

## Zombie-window / stale-port check

After a kill+start cycle, 8765 may respond 200 from the OLD process if the kill missed. Always: kill → wait 1 s → start → wait 12 s → probe 8765.

## Crash log

`C:\Users\mwr_w\shiflow-mini\data\crash.log` — written by `sys.excepthook` + `threading.excepthook` in `app.py`. Append-only, never truncated. If the RFlow window disappears, read this file BEFORE restarting to find the root cause. Format: `=== Thread <name>: <ExceptionType>: <msg>` + full traceback lines. A per-minute `另一个看门狗已在值守…→ 本实例退出` wall = `ensure_watchdog`'s liveness probe is broken (import failure swallowed as 'dead') and every task fire spawns a spurious watchdog — fix the probe, don't just kill the processes.

## WebView2 cache-bust

Every `app.py` launch generates a fresh `uuid4().hex[:16]` in the URL query string. The HTML also has `<meta http-equiv="Cache-Control">` no-cache three-slash. If the window shows a stale build, close the window and relaunch — WebView2 does not hot-swap the URL mid-session.

## `kill_app.ps1` location

`C:\Users\mwr_w\AppData\Local\Temp\kill_app.ps1` — created by Hermes. Recreate if missing:

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe'" |
  Where-Object { $_.CommandLine -match 'shiflow-mini' -and $_.CommandLine -match 'app.py' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force; "killed $($_.ProcessId)" }
```

## Probing a live module / reasoning about where a click lands (no vision needed)

- **Run module probes with the project's own interpreter, NOT the Hermes `execute_code` kernel.** The kernel lacks the project's deps (`mss`, which `shiflow_mini.capture` imports) → `ModuleNotFoundError`. Write the probe to scratch and run it with `cd <repo> && .venv/Scripts/python.exe probe.py`, with `sys.path.insert(0, <repo>)` then `from shiflow_mini import native, capture`.
- **Split a click-drift into *mapping* vs. *model-estimate*.** `r = native.get_rect(hwnd)`; `sx=(r[2]-r[0])/img.width`, `sy=(r[3]-r[1])/img.height` where `img` comes from the SAME `grab_window(hwnd, max_width=1200, prefer_screen=True)` the agent uses. The model's image-point `(ix,iy)` lands on screen at `px=r[0]+ix*sx`, `py=r[1]+iy*sy`. If `sx≈sy≈1.0` the capture is 1:1 with the window rect (DPI-unaware, no scaling) → a wrong landing is the **model's pixel estimate**, not a DPI/mapping bug — so the fix is to stop trusting the model pixel (self-calibrate the input point), not to chase scaling.
- **Locate a UI region without vision (rate-limited or unavailable).** Downsample the bottom ~35 % of the capture to an ASCII grid (`#`=light, `.`=dark, by luminance+saturation thresholds) and print it, or map each candidate point to screen and cross-check `native.top_level(native.window_at(px,py)) == hwnd` (read-only; see SKILL.md §verify). This is how you confirm "the input box is at ≈0.52w/0.90h" before trusting the self-calibration candidate grid.

## Capture integrity (ensure_front)

Before ANY `prefer_screen` capture of a target window — the model frame in `agent._think`, the trigger/baseline frame in `watcher.snapshot` — assert the window is actually foregrounded and un-occluded. `prefer_screen` grabs the pixels of whatever window is on top of the screen rect, so if RFlow/terminal/editor covers WeChat the agent silently captures the *wrong app* and the model "sees" a non-WeChat UI and refuses to reply.

`native.ensure_front(hwnd) -> bool` (bring to front, then verify it is the top-level at its center):
```python
def ensure_front(hwnd):
    if not bring_to_front(hwnd):
        time.sleep(0.15)
        if not bring_to_front(hwnd):
            return False
    r = get_rect(hwnd)
    if not r:
        return False
    time.sleep(0.15)
    return not is_occluded(hwnd, r)   # is_occluded: top_level(window_at(cx,cy)) != hwnd
```
Wiring — identical in `agent._think` and `watcher.snapshot`:
```python
front = native.ensure_front(s.hwnd)
img = capture.grab_window(s.hwnd, max_width=…, prefer_screen=front)
```
- `front=True` → `prefer_screen=True`: fresh screen pixels (window is foreground + repainting).
- `front=False` (a fullscreen app covers it, or the hwnd went stale) → `prefer_screen=False`: a DC/PrintWindow of the window BODY. Still the target's content (never RFlow/terminal), just possibly a stale frame — an acceptable degradation that must never mis-read the wrong app.

Standing rules:
- The **watcher re-asserts on every poll**, not only at `start()`: foreground is stolen between polls and each stolen poll both captures the occluder AND folds a wrong-app frame into the baseline, so later diffs are wrong-app-vs-wrong-app and miss real messages.
- **Poisoned baseline:** once a wrong-app frame has entered the baseline, restart the watch (`POST /api/auto/wechat`) to rebuild it from a clean WeChat frame.
- **Diagnose before touching code:** `GET /api/sessions/{sid}` → `trace[].reasoning` narrates exactly what the model saw. A non-WeChat description ("RFlow 运营指令 / 文本编辑器 / 纯文本 / 代码") = capture grabbed the wrong app → fix foreground/capture; do NOT edit the prompt or blame the model.

## Unattended self-heal (three-layer guard) + schtasks ops

For the standing "never silently dies / survives a reboot" spec, a lone `run_forever.py` is not enough (it can itself crash or not survive a reboot). The full stack:

1. `run_forever.py` — respawns `app.py` within seconds on any exit/segfault. It exits on its own when `data/closing.flag` exists (user closed) or `data/duty.flag` is absent — checked at startup AND every ~5 s probe tick — so it is no longer an unconditional respawn engine.
2. **Task Scheduler** task `RFlow Watchdog` (repeating, `/SC MINUTE`) runs `ensure_watchdog.py`. `ensure_watchdog.py` checks `closing.flag` FIRST (no-op on a deliberate close), checks `duty.flag` second, then probes watchdog liveness via the `single_instance` mutexes — `OpenMutexW(0x1, …)` on **BOTH names from `_mutex_names()`** (a LIST: Global\ + Local\), with a `run_forever.py` process-count fallback — and only then (re)launches `run_forever.py` **detached** (`creationflags = DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP`). The import must be `_mutex_names` (plural, returns a list); importing a name that does not exist makes the probe throw, the `except: return False` swallows it, and the task then spawns a spurious watchdog on EVERY fire. `ensure_watchdog.py` self-locates repo+venv from `__file__` → cwd-independent, works on any machine.
3. **Startup-folder `.vbs`** in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\` runs the same `ensure_watchdog.py` at logon (hidden window) for instant reboot recovery.

Register/delete all of it:
```bash
cd <repo> && .venv/Scripts/python.exe rflow.py install     # create task + .vbs
.venv/Scripts/python.exe rflow.py uninstall                 # remove both
```

**Prove it before reporting (real execution, not a description):** kill the entire process tree (`rflow.py stop` or the kill loop matching `*shiflow-mini*`/`run_forever.py`/`app.py`) → `curl 127.0.0.1:8765/api/health` must FAIL (down) → run `.venv/Scripts/python.exe ensure_watchdog.py` → wait ~12 s → `curl` must return `200 {"ok":true}` again and a `run_forever.py`/`app.py` pair is back.

### Prove a deliberate CLOSE stays closed (shutdown E2E)

A shutdown change is verified through the REAL close path (the user clicking X), never via `rflow.py stop` alone:

1. Find the pywebview window — plain `EnumWindows` over visible top-level titles containing `RFlow` (`native.list_windows` may not surface it; a raw ctypes EnumWindows does) — and `PostMessageW(hwnd, 0x0010, 0, 0)` (WM_CLOSE).
2. Sample the markers: **~T+12 s** → `data/closing.flag` present, `duty.flag` AND `app.pid` gone (cleanup ran in the pre-kill segment; a leftover `duty.flag` here = the closer died before its cleanup — re-order cleanup earlier, don't widen the kill); **~T+35 s** → 0 RFlow processes (count by CommandLine role, excluding your own probe scripts) + 8765 dead; **~T+95 s** → still 0 processes across at least one task-minute PLUS a manual `schtasks /Run /TN 'RFlow Watchdog'` (the OS refuses to run a Disabled task — that refusal message is itself the pass signal).
3. The closing process dying mid-kill-loop is EXPECTED (the tree-kill takes its own process down) — that is exactly why cleanup runs before the loop and the kill child is an independent PowerShell.
4. Re-arm check: `rflow.py duty on` must clear `closing.flag`, restore the process, and resume 值守 — revive-when-asked is the other half of the contract.

### schtasks pitfalls on this CJK-locale machine
- **Use `schtasks`, not PowerShell `Register-ScheduledTask`.** The latter's repeating-trigger DateTime binding throws `PositionalParameterNotFound` ("positional parameter … not in correct format") here; `schtasks /Create …` works natively.
- **Permissions:** a repeating `/SC MINUTE` task is creatable **without admin**. `/SC ONSTART` and `/SC ONLOGON` are **admin-only** — a normal user gets `拒绝访问` (access denied). That is why reboot recovery is the Startup-folder `.vbs`, not an ONSTART/ONLOGON task.
- **Encoding:** `schtasks` prints **GBK(cp936)**. Judge success by `returncode == 0`, never by grepping the (garbled-under-UTF8) Chinese output; decode bytes via `cp936` only when you must display them.
- **Command line:** the task action MUST be `<venv>/Scripts/pythonw.exe <repo>\ensure_watchdog.py` (GUI subsystem — a `python.exe` action flashes a console box on the user's desktop every fire; no inner quotes unless the path contains a space). `rflow._ensure_cmd()` builds exactly this (PYW with `python.exe` fallback); after changing it, re-register the task (`rflow.py install` / `duty on`) or the OLD command line keeps firing.

### Process-tree note (expected, not a bug)
On some launch paths the tree shows a `wf→wf→app→app` stack of 4 processes (all `pythonw.exe` since the console fix). The `.py` sources contain **no** `run_forever.py` launch string — the extra layer comes from a shell/`Start-Process` shim outside the repo. It is harmless: the named mutex (`single_instance`) guarantees only one real watchdog and only one `app.py` actually holds 8765 + does 值守, and the 3-min task + mutex make re-launches idempotent. Always start via `rflow.py start` (one detached watchdog), never a hand `Start-Process`.
