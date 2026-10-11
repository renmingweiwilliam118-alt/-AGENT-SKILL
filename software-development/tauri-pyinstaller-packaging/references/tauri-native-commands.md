# Tauri 2 native commands & plugins (shell side)

Depth for adding a native OS feature (file/folder/save-as dialog, file copy to a user-chosen location) through the Tauri shell, callable from the bundled webview.

## Verifying the exact plugin API (do this before writing code)

Method names differ across tauri-plugin-* major versions; guessing costs a full recompile each miss.

1. Lock the version: `cargo add tauri-plugin-dialog` picks the latest 2.x; confirm in `Cargo.lock` (must align with the tauri core minor, e.g. plugin 2.8.1 ↔ tauri 2.12.x).
2. Read the real source rather than guessing:
   ```bash
   curl -sL "https://static.crates.io/crates/<name>/<ver>.crate" -o /tmp/x.crate
   tar xzf /tmp/x.crate -C /tmp/ && grep -n "pub fn" /tmp/<name>-<ver>/src/*.rs
   ```
   This works even when `cargo fetch` refuses to unpack the crate locally and docs.rs is unreachable. `find ~/.cargo/registry -iname '*<name>*'` can also return empty right after a build (registry cache may not retain unpacked sources) — don't conclude the dependency is absent; check `Cargo.lock` first.
3. `cargo build --release` is the final check — expect 0 misses if you read the source.

## Tauri 2 command patterns (verified shapes)

```rust
#[tauri::command]
fn export_data_file(app: tauri::AppHandle, file_path: String) -> Result<String, String> { ... }
```
- `AppHandle` is an INJECTED first parameter. `AppHandle::try_current()` / `::get()` do not exist in Tauri 2 (those are Tauri 1 APIs).
- Register: `.plugin(tauri_plugin_dialog::init()).invoke_handler(tauri::generate_handler![export_data_file])`.
- Enable JS-side access: `"app": { "withGlobalTauri": true }` in `tauri.conf.json`. There is NO `with-global-tauri` Cargo feature on the tauri crate — `features = ["with-global-tauri"]` fails the build. **Caveat:** `withGlobalTauri` alone only grants access when the webview runs on Tauri's SAME-ORIGIN `tauri://` custom protocol. If the shell points the webview at an EXTERNAL origin (`WebviewUrl::External` → `http://127.0.0.1:<port>/`, the normal case for this architecture's free-port backend), you MUST additionally whitelist that origin in the capability's `remote.urls` — see the section below.
- Frontend (webview): `window.__TAURI__.invoke('export_data_file', { filePath })` — args are camelCase in JS, snake_case params in Rust (Tauri auto-converts). Guard with `if (window.__TAURI__?.invoke)` so the same webview degrades to a plain browser download in dev mode.

## Dynamic / external webview origin → declare `remote.urls` (else invoke is silently dropped)

Symptom that costs a whole debug loop: native `invoke` commands (save dialog, export) do nothing — the JS Promise never settles, no error, no dialog. Root cause: Tauri 2's capability/ACL system DROPS `invoke` from any webview origin not in the capability's `remote.urls`. A `tauri://` (same-origin) webview is always allowed; an EXTERNAL origin is not. This architecture opens the webview at `http://127.0.0.1:<free-port>/` (the backend picks the port at runtime), so every launch is an external origin and a bare `core:default` capability silently blocks all IPC.

Fix, in `desktop/capabilities/*.json` (capability object):
1. Add the origin to the capability top-level `remote.urls` (sibling of `windows`/`permissions`). Wildcards work: `["http://127.0.0.1:*", "http://localhost:*"]` matches any free port. If you can pin the backend to a FIXED port instead, list it exactly (`http://127.0.0.1:8765`) — deterministic, no glob to reason about.
2. Add the plugin permission you need, e.g. `"dialog:default"`, to the same capability's `permissions` (a Save dialog without it will not open even with remote.urls).
3. `WebviewUrl::External(url)` in `main.rs` + `withGlobalTauri: true` + the capability above are ALL three required; any one missing and invoke dies.

Make the failure VISIBLE instead of silent, so end users never see a dead button:
- Add a trivial `#[tauri::command] fn desktop_ping() -> String { "ok".into() }` and invoke it at startup as a bridge self-test.
- JS bridge: wrap every invoke in a hard `Promise` timeout (a dead bridge must not hang the UI); cache the detected handle ONLY on a POSITIVE detection (Tauri injects `__TAURI__` a beat after boot — a too-early negative read must stay re-pollable); on a failed ping, surface a clear "native export unavailable" state on the buttons instead of doing nothing.
- The fix lives in the compiled shell + webview: it requires the full re-build/re-freeze loop (rebuild webui → `cargo build` the shell → re-zip) before the user sees it.

## tauri-plugin-dialog 2.x concrete shapes (2.8.1)
- `app.dialog().file()` → `FileDialogBuilder` (methods: `set_title`, `set_file_name`, `set_directory`, `add_filter`, …).
- Save dialog: `builder.blocking_save_file() -> Option<FilePath>` (sync; run on the command thread, it does not block the UI main thread). The async callback form is the free function `tauri_plugin_dialog::save_file(builder, |opt_path| …)` — `FileDialogBuilder` has NO `.save()` method (that shape is from older Tauri 1 plugin docs/examples).
- `FilePath` comes from `tauri-plugin-fs` and is an ENUM (`Url(url)` | `Path(PathBuf)`), not a path: it has `into_path() -> Result<PathBuf>`, `as_path()`, `simplified()`, `Display` — but NO `has_extension` / `with_extension` / `to_string_lossy`. Convert first: `let p = fp.into_path()?; p.extension().is_some()`, `p.with_extension(ext)`.
- RUST gotcha: `file_path.replace('\\', "/").trim_start_matches('/')` as one expression triggers E0716 (temporary dropped) — split into two `let`s.
- If the save-file callback runs via `tauri::async_runtime::spawn` + a `tokio::sync::oneshot` channel (to keep the blocking dialog off the main thread while awaiting the result), add `tokio = { version = "1", features = ["sync", "rt"] }` to the shell crate's `Cargo.toml`.

## Security pattern for "copy data file to user-chosen dir" commands
- Resolve source under the app data dir, `canonicalize()` both source and the data dir, require `source.starts_with(&data_dir_canonical)` (note `starts_with` returns `bool`, not `Result` — `if !source.starts_with(&dir)`).
- Never delete the source; `fs::copy` and return the destination path string to the UI for a success toast.
- Under freeze, the data dir is `<project_root>/data` where `project_root()` = shell exe dir in packaged layout — keep it in sync with where the crawler's CWD writes output (see the SKILL.md CWD pitfall).
