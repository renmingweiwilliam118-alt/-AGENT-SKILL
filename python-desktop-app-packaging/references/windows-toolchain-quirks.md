# Windows toolchain + UI-for-novices notes

These are environment quirks observed on this host; re-verify before assuming. Consult when a step "fails for no reason".

## uv-managed venv
- No `pip`: install with `uv pip install <pkg>`. Plain `pip` fails.
- A bare `python` (outside the venv) may start the server then die on a missing dep (e.g. uvicorn). A log that looks "working" can be a stale still-alive old backend. Restart with `uv run python …`.

## Running builds
- Run PyInstaller freezes / long builds through `terminal` with the project venv, NOT through the execute_code kernel: the kernel's managed-runtime site-packages can shadow the project venv (a broken PIL in the managed env aborts PyInstaller's matplotlib hook mid-freeze while the project venv is fine). `terminal` + `.venv/Scripts/python.exe` is the reliable path.

## npm
- Default npm blocks remote fetches (`EALLOWREMOTE`). Pass `--registry=https://registry.npmjs.org` for any new dependency install.

## git-bash / MSYS + curl + localhost
- `curl` to a 127.0.0.1 backend can report `000` or `0B` even on success (MSYS quirk). Confirm health with PowerShell `Invoke-WebRequest`/`curl.exe` (the real one) or a Python `urllib` probe, not the MSYS `curl`.
- `taskkill //F //PID` (double slash) is the MSYS form; use single-slash `taskkill /F /PID` under native cmd/PowerShell.

## Rust / Tauri
- `write_file` on a `.rs` file it already owns can be refused ("Refusing to overwrite"); a full-file rewrite can also stream-timeout. Break the edit into small incremental `patch` calls.
- `cargo build` debug is fast; re-run release after each `main.rs` change and re-verify e2e.
- When adding a Tauri plugin (dialog, fs, ...), do **not** rely on the crate unpacking into the local registry cache — it often doesn't. Read the exact-version source instead: `curl -sL https://static.crates.io/crates/<plugin>/<plugin>-<ver>.crate` → `tar xzf` → grep the `impl` blocks for the real method names. docs.rs HTML may be unreachable on this host; the static.crates.io download endpoint works.
- Tauri 2 native-dialog concrete API (verified against tauri-plugin-dialog 2.8.x source): builder is `app.dialog().file()` → chain `set_title() / set_file_name()` → `blocking_save_file() -> Option<FilePath>`. `FilePath` (from tauri_plugin_fs) has **no** `has_extension`/`with_extension`/`to_string_lossy` — call `.into_path() -> Result<PathBuf>` first, then std `Path` methods. `tauri::AppHandle` is injected as the first `#[tauri::command]` parameter — there is no `AppHandle::try_current()`.
- `withGlobalTauri` (exposing the `__TAURI__` JS global so the webui can `invoke` Rust commands) is a **tauri.conf.json `app` field**, not a cargo feature.

## Verifying the shipped artifact, not a live tab
A persistent browser tab may hold a stale cached `<title>` (e.g. an old emoji). To prove what a novice will see, **byte-scan the built/bundled files** (`<title>`, asset names, author tokens) rather than trusting `document.title` in the harness tab.
- LTO / release string-dedup can make a marker (a new command name, a capability string) absent from the .exe even in a CORRECT build — an inconclusive byte-check is not proof of failure. Verify by behavior: launch the shell, probe the endpoints, and compare the served bundle hash against a fresh `vite build`.

## Windows icons (exe + window + web)
- Multi-size `.ico`: recent Pillow changed the `save(format='ICO', sizes=[...])` API — when it fails, hand-write the container instead: 6-byte header (`<HHH>`: 0, 1, count), one 14-byte directory record per size (`<BBBBHHII>`), then the PNG bytes; Windows 10+ reads PNG-in-ICO entries. Re-check current Pillow behavior before assuming.
- The web-side logo + favicon live in the webui public dir → rebuild frontend + re-freeze (assets snapshot into `_internal` at freeze time). The exe/window icon lives in `desktop/icons/` + `tauri.conf.json` `bundle.icon` + `cargo build --release` — a shell-side change that ships only with the rebuilt shell .exe.

## UI for a novice audience ("太丑了")
Hacker-neon (pure black + fluorescent cyan/magenta + square corners + terminal glyphs) is frightening and over-busy for non-technical users. Convert CSS variables to a clean modern-SaaS palette: soft light default (restrained blue primary, grey neutrals, radius ~0.6rem), professional deep-grey-blue dark (not neon). Soften scrollbars, background grids, status-dot and box glows, and shadow defs (realistic depth, not black/neon). **Keep every spring / 3D / tilt / micro-interaction** — motion is the requirement, the palette is the fix. Rebuild the frontend and re-verify visually.

### The RY app's target: neo-brutalism ("野兽派")
This user's stated taste for the RY crawler app moved AWAY from clean-SaaS toward neo-brutalism when asked to redesign — confirm the target style before restyling. Recipe: warm paper-white background, 2px pure ink-black borders, hard offset shadows (`4px 4px 0 0`, zero blur), high-saturation collision accents (electric blue / hot pink / fluorescent green / bright yellow), fully square corners, 900-weight display type (e.g. Archivo Black) + monospace micro-labels. Implement at the TOKEN layer (CSS variables + tailwind config + a mechanical `[class*="rounded"]{border-radius:0 !important}`) so every component re-skins at once, and re-point legacy `glow-*`/rounded class names to the hard values for back-compat; keep all spring/tilt motion.

If the user then reports "the UI looks exactly the same" after a full rebuild, suspect the webview serving a stale cached bundle: add `<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">` to index.html and confirm the served JS hash matches a fresh `vite build`.
