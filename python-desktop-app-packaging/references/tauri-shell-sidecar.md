# Tauri 2.x shell → PyInstaller sidecar

Shape: the Tauri shell is the double-click target. It (a) locates the frozen backend, (b) spawns it, (c) polls a ready file for the port, (d) opens the backend's own URL same-origin, (e) stops the backend with CTRL_BREAK on exit.

## Find the co-located backend (zero env vars)
`find_bundled_backend()`: look, in order, for the frozen backend named `<Backend>` → generic `Backend.exe`/`Backend`:
- Windows onedir: `<exe_dir>/Backend/Backend.exe` (a sibling onedir folder), or `<exe_dir>/Backend.exe` (onefile).
- Linux: name has no `.exe`.
Fall back to a `project_root()` that resolves to the shell's own directory when a bundled backend exists (dev override via env still supported). This is what lets the end user set **zero env vars**.

## Spawn + handoff
- `runtime_dir()` → OS temp dir (e.g. `<temp>/appname-desktop/`).
- `spawn_backend(cwd, ready_file, log_file)`: `std::process::Command` the frozen backend, set env `*_READY_FILE` (the port file) and, if you keep a role flag, the role env. Set `Stdio::null()` on stdin; point stdout **and** stderr at `File::create(log_file)` — **never** `Stdio::piped()` on the backend's stdout (a piped stdout whose reader the shell dropped later turns every `print` into `OSError Errno 22`).
- After spawn, **poll** `ready_file` (120s timeout) reading the port, then `webview.open(http://127.0.0.1:PORT/)`.

## Process state + stop
- Keep the child in `static BACKEND: OnceLock<Mutex<Option<Child>>>` (a `State` impl loses it; `OnceLock` + `Mutex` is the simple correct shape). `child.kill()` needs `mut`.
- On exit, stop the sidecar with **CTRL_BREAK** (`CTRL_BREAK_EVENT`), not SIGTERM — SIGTERM is a no-op on Windows.
- Tauri 2.12.2 is the verified stable line; do not ship 3.x.

## Backend-side ready file (server.py)
Only when the `*_READY_FILE` env var is set, write the bound port to that file (trailing newline ok); otherwise still `print` for dev. Uvicorn: `log_level="warning"`, websocket `"websockets"`.
