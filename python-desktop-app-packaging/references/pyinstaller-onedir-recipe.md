# PyInstaller onedir + frozen webui + single-exe multi-role

## Build
- Onedir (default `--onedir`), not onefile, for heavy dynamic-import projects. Output: `dist/<Name>/<Name>.exe` + `dist/<Name>/_internal/`.
- Hooks / `--collect` for `playwright`, `cryptography`, `numpy` if the project uses them.
- A uv-managed venv has **no pip** — install build deps with `uv pip install pyinstaller`, not `pip install`.
- Run the freeze from `terminal` with the project venv interpreter, not the execute_code kernel: the kernel's managed-runtime site-packages can shadow the project venv and abort PyInstaller mid-run.
- Frozen webui: `add_data = [(ROOT/api/webui, "webui")]` puts the built frontend into `_internal/webui`.

## Resolve the frozen webui at runtime
`_resolve_webui_dir()` in the API entrypoint:
```python
def _resolve_webui_dir():
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            cand = Path(meipass) / "webui"
            if cand.exists():
                return cand
    return Path(__file__).resolve().parent.parent / "webui"  # source tree fallback
```
The frozen backend must serve its **own** bundled UI.

## Serving the webui (FastAPI / Starlette StaticFiles)
Mount the webui **root**, not just its subdirectories, or root-level files the frontend references (`/favicon.ico`, logo PNGs) 404:
- Register all API routes first, then `app.mount("/", StaticFiles(directory=WEBUI_DIR, html=True))` — mounts match in order but explicit routes take precedence, and `html=True` gives the SPA fallback to `index.html` for unknown paths.
- Subdir-only mounts (`/assets`, `/logos`, `/static`) never cover files sitting in the webui root.
- This code lives in the API entrypoint → it ships inside the frozen backend exe: after changing it, re-freeze + reassemble + rezip, then verify `/favicon.ico` and the logo return 200 with the correct byte size (byte-level, not a live tab).

## Single-exe multi-role self-restart
One binary plays two roles via an env flag (`*_ROLE` = server | crawler). `_resolve_python()`:
- dev (not frozen): `uv run python` or venv python + the role flag to spawn the crawler subprocess.
- frozen: `sys.executable` (the exe itself) + the role env, so the crawler role re-launches **the same frozen binary** with no Python. Confirm the role flag is what distinguishes the two boots.

## Verify the frozen exe standalone
Set the role env + port + ready-file env, run `dist/<Name>/<Name>.exe` with no interpreter on the assumption, wait for the ready file, curl `/api/health` and `/`, and confirm the served `index.html` `<title>` + an `assets/index-*.js` download match the freshly built frontend. Byte-scan the bundle's `index.html` for any author residue you must prove gone.
