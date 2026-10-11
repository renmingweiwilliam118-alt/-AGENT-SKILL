---
name: python-desktop-app-packaging
description: Package a Python web app as a zero-env desktop app.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [packaging, desktop, tauri, pyinstaller, python, distribution]
    related_skills: []
---

## When to Use
When the user wants a Python backend + web-frontend project to run as a standalone app on any machine with **no environment to install** ("double-click to run", "给电脑小白用", "不需要装任何环境"). Also when a frozen/PyInstaller Python process must be managed by a native shell, or when a third-party app is being re-skinned + de-branded for redistribution.

# Python Desktop App Packaging (zero-env, for non-technical users)

Turn a Python backend + web-frontend project into one folder the user double-clicks, needing **no Python / uv / Node / Rust installed**. The end user installs nothing; the only system dependency you may rely on is a browser that ships with the OS (Windows ships Edge).

## Architecture (the shape that works)
- A thin **desktop shell** (Tauri 2.x, Rust) is the thing the user double-clicks. It spawns the app's real backend as a **sidecar** and loads the frontend same-origin from that backend's own port (zero CORS).
- The backend is frozen with **PyInstaller** into a co-located onedir folder. The shell auto-locates that frozen backend next to itself, so the user sets **zero env vars**.
- A frozen backend can self-restart itself for a second role (e.g. a crawler role) via `sys.executable` + an env role flag — one binary, two roles.

## Decision gates (always-on)
- **Tauri version**: pin to **Tauri 2.x**; Tauri 3 is alpha/unstable — do not ship it.
- **Never assume Tauri plugin / framework API names** — fetch the exact pinned crate version's source (crates.io download endpoint via `curl -sL https://static.crates.io/crates/<name>/<name>-<ver>.crate`, tar, read the impl blocks) *before* writing Rust that calls it. Dialog/save APIs in particular are easy to get subtly wrong (method names, param types); one wrong guess costs a ~50s release build cycle. See `references/windows-toolchain-quirks.md` (Rust/Tauri section) for the concrete dialog-API facts.
- **PyInstaller layout**: for a project with heavy dynamic imports, use **onedir, not onefile**. onefile unpacks to a temp dir per launch and is fragile/slow; onedir is a folder you ship as a zip. ~100–200MB is normal.
- **Frontend bundling**: build the web frontend into the frozen backend's `_MEIPASS` (add-data) and resolve it at runtime via a `_resolve_webui_dir()` that prefers `sys._MEIPASS/webui` when frozen, else the source tree. The frozen backend must serve its own UI.
- **Port handoff (critical pitfall)**: do **NOT** pipe the backend's stdout into the shell. A dead pipe makes every subsequent `print` raise `OSError [Errno 22]` and crash the stream. Hand off the chosen port via a **ready file** (backend writes the port to a file only when a `*_READY_FILE` env var is set; still prints for dev) and redirect the backend's stdout/stderr to a **log file**. The shell polls the ready file, then opens `http://127.0.0.1:PORT/`.
- **Graceful stop on Windows**: a sidecar must be stopped with `CTRL_BREAK_EVENT`, not `SIGTERM` (SIGTERM no-ops on Windows). See `references/tauri-shell-sidecar.md`.

## Workflow order
1. Freeze the backend (PyInstaller onedir). Verify the frozen exe boots standalone, writes its ready file, and serves the frozen frontend. Do this **before** wiring the shell so you know the sidecar is sound. → `references/pyinstaller-onedir-recipe.md`
2. Build the Tauri shell: spawn the co-located frozen backend, poll the ready file, open the same-origin URL, stop with CTRL_BREAK. Auto-locate the backend so no env vars are needed. → `references/tauri-shell-sidecar.md`
3. If redistributing a third-party project: de-brand before shipping. → `references/debranding-redistribution.md`
4. If the audience is non-technical: redesign toward a clean SaaS look; remove hacker-neon. Keep all motion. UI note is in `references/windows-toolchain-quirks.md`.
5. Assemble the delivery folder: shell `.exe` + frozen backend onedir + a plain-language `使用说明.txt` for the novice. Zip it. Any **frozen-mode path resolution must not use `__file__`** — under PyInstaller `__file__` lies inside `_internal/`, so e.g. `Path(__file__).parents[N]/"data"` silently points at the wrong data dir; branch on `sys.frozen` and resolve from `Path.cwd()` (the shell sets CWD to the app folder) or an env override.
   Frontend changes (including i18n/locale JSON, which is inlined into the JS bundle at `vite build` time) require **rebuilding the frontend BEFORE re-freezing** — the PYZ embeds whatever `api/webui` held at freeze time. Verify the shipped artifact by byte-scanning the frozen bundle (grep the new i18n string inside `MediaCrawlerBackend/_internal/webui/assets/*.js`), not the source tree.
6. **End-to-end verify by launching the shell with NO env vars** (simulate the novice), then confirm window + frozen-backend process + ready-file port + `/api/health`=200.

## Pitfalls that cost time
- Live stdout pipe to sidecar → dead-pipe `Errno 22`. Use ready-file + log-file. (gate above)
- Trusting a stale browser tab to represent the shipped artifact. A tab may hold an old cached title/emoji. **Verify the artifact by byte-scanning the built files**, not the live tab.
- `cmd | tail` in a background/notify terminal run **masks the real exit code** (tail's 0 comes back as the command's). After piping a long build, append `echo "EXIT=${PIPESTATUS[0]}"` or you will re-diagnose a failed build that looks successful.
- Re-freezing with a stale `api/webui` — the PYZ embeds whatever was built at freeze time, so a frontend change made *after* the last `vite build` silently ships old UI. Rebuild frontend first, byte-scan the frozen bundle to confirm.
- Root-level static assets the frontend references (`/favicon.ico`, logo PNGs) 404 when the frozen backend only mounts webui SUBDIRECTORIES (e.g. `/assets`): mount the webui root LAST with `StaticFiles(directory=WEBUI_DIR, html=True)` — routes registered earlier win, unknown paths fall back to index.html. The mount code lives in the API entrypoint, so it ships only with a re-frozen backend exe; verify the logo/favicon return 200 with the right byte size. See `references/pyinstaller-onedir-recipe.md`.
- Run PyInstaller freezes from `terminal` with the project venv, not from the execute_code kernel: the kernel's managed-runtime site-packages can shadow the project venv (a broken PIL in the managed env aborts PyInstaller's matplotlib hook mid-freeze while the project venv is fine).
- A bare `python` (no venv) starts the server then dies (missing deps like uvicorn) — a "working" log can be a stale still-alive old backend. Restart with the project's `uv run` / venv.
- Toolchain quirks on this machine (uv has no pip, npm blocks remote, MSYS curl misreports localhost) are in `references/windows-toolchain-quirks.md` — consult before debugging "why did that fail".

## References
- `references/tauri-shell-sidecar.md` — shell: spawn/poll/stop, `find_bundled_backend`, `static BACKEND`, CTRL_BREAK.
- `references/pyinstaller-onedir-recipe.md` — onedir recipe, `_MEIPASS` frozen webui, single-exe multi-role self-restart, hooks.
- `references/debranding-redistribution.md` — strip author while keeping license + third-party credits.
- `references/windows-toolchain-quirks.md` — uv/npm/MSYS/curl/UI-for-novices notes.
