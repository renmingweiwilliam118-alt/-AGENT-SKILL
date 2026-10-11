# Pywebview file/window dialogs on Windows (EdgeChromium backend)

All facts verified by reading the installed pywebview source under `Lib/site-packages/webview/` — re-check versions: the pipeline locations move between releases.

## Download → Save-as pipeline (the reliable "save as" path; no pywin32 needed)

- `webview/__init__.py`: `settings` is an `ImmutableDict` with `'ALLOW_DOWNLOADS': False` by default. `ImmutableDict` forbids adding/removing keys but existing keys ARE mutable — so `webview.settings['ALLOW_DOWNLOADS'] = True` (before `webview.start()`) is the documented toggle.
- `platforms/edgechromium.py` `on_download_starting`: when `ALLOW_DOWNLOADS` is False → `args.Cancel = True` (silent no-save). When True → shows `WinForms.SaveFileDialog` on the GUI thread, with `InitialDirectory` read from registry `HKCU\...\Shell Folders` key `{374DE290-123F-4565-9164-39C4925E467B}` (user's Downloads). User pick → `args.ResultFilePath` is rewritten; cancel → `args.Cancel = True`.
- Practical pattern: frontend triggers a real browser download (Blob + `<a download>`); Python just flips the setting. This sidesteps every worker-thread Win32 dialog failure.

## `window.create_file_dialog` (open / import a file from JS)

- Signature (pywebview 6.x): `Window.create_file_dialog(dialog_type: int = 10, directory: str = '', allow_multiple: bool = False, save_filename: str = '', file_types: Sequence[str] = tuple()) -> Sequence[str] | None`. Wrapped in `@_shown_call`, so a call from a `js_api` worker method is marshaled to the shown/main context — this IS the supported path for **user-initiated "open/import file"** (let the user pick a local doc and load it), unlike raw WinForms dialogs which are not thread-safe. Confirm the exact signature with `inspect.signature(Window.create_file_dialog)` on the installed version before wiring it; it has moved across releases.
- Pass `dialog_type=webview.FileDialog.OPEN` (enum `OPEN=10, FOLDER=20, SAVE=30`). Module-level aliases `webview.OPEN_DIALOG`/`SAVE_DIALOG`/`FOLDER_DIALOG` also exist in 6.x, but `ALL_FILE_DIALOG`/`TEXT_FILE_DIALOG` do NOT — `file_types` takes filter strings like `("*.txt", "*.md")` or can be omitted entirely.
- The return is a **list of path strings** (`[path, ...]`) or empty/`None` on cancel — NOT a `{"filename": ...}` dict. Read the first pick as `files[0]` after a truthiness check.
- Verify at runtime that the dialog actually appeared before relying on it (SKILL rule 4): a `None`/empty result means "no file" (cancel), so log the cancel case and the exception case distinctly so the frontend shows the right message.
- For **save-as** still prefer the `ALLOW_DOWNLOADS` download pipeline (SKILL rule 2); use `create_file_dialog` specifically for the open/import direction.

## js_api threading model

- Methods on the `js_api` object are invoked on pywebview worker threads. Anything touching WinForms/CoreWebView2 state from there → crashes or silent failures. Keep js_api methods to: file I/O, base64→disk writes, Win32 PostMessage/ShowWindow, and HTTP calls.
- If `bindNative()` on the frontend never finds `window.pywebview.api` (bridge injection fails), the whole UI dead-ends — that is why the in-process-backend HTTP endpoint pattern exists.

## Window control (minimize/maximize/close from JS)

- `window.minimize()/maximize()/close()` are GUI-thread-bound; calling them through the JS bridge from worker threads is unreliable on the EdgeChromium backend.
- Thread-safe alternatives (both used successfully in the RENVOX project, `G:/MOSS-TTS-Nano/rvox_desktop.py`):
  1. Win32: `FindWindow` the app's main HWND, then `ShowWindow` / `PostMessage(WM_SYSCOMMAND, SC_MINIMIZE|SC_MAXIMIZE|SC_RESTORE)` / `PostMessage(WM_CLOSE)` — callable from any thread.
  2. HTTP: mount `/api/win?cmd=minimize|maximize|restore|close` on the in-process FastAPI app and `fetch` it from JS — works even if the pywebview JS bridge never injected.
- Frameless pywebview windows: find the HWND by title, then walk CIM process ancestry to confirm it belongs to the right host process; a bare `FindWindow(None, title)` can hit another app's window with the same title.
