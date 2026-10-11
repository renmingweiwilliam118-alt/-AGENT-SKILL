---
name: renvox-moss-tts
description: "RENVOX (G:/MOSS-TTS-Nano): host/UI/audio work and probes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [renvox, moss-tts, pywebview, tts, onnx, ffmpeg, desktop-app]
    related_skills: [pywebview-windows, frontend-ui-error-probes, windows-process-inspection]
---

# RENVOX / MOSS-TTS-Nano desktop app

The user's own sci-fi-themed voice-cloning TTS desktop app (pywebview + local onnx/torch runtime + FastAPI backend). Task class: UI iteration (glassmorphism/3D), feature wiring (audio upload, dialogs, window controls), and verification of both — for THIS user's standing spec.

## When to Use

- Iterating the RENVOX UI (cards, carousel, tilt, cursor, layout ratios) — user asks are relative and must end with measured numbers.
- Wiring app features (audio formats, save dialogs, window controls, consent popups) into `G:/MOSS-TTS-Nano`.
- Restarting the 18097 host after backend edits, or proving a change worked headlessly against the running app.

## Always-on (project facts — trust, don't re-derive)

- Paths: repo `G:/MOSS-TTS-Nano`; UI `ui/renvox.html` (served per-request → **window «↻ 重载» reload suffices, no restart**); backend `app.py` / `onnx_tts_runtime.py` (read at host start → **host restart required**); venv `G:/MOSS-TTS-Nano/.venv-onnx/Scripts/python.exe`; desktop launcher `rvox_desktop.py`; backend port `127.0.0.1:18097`.
- Two TTS runtime paths (torch + ONNX) share the upload layer — audio-format support changes belong in the upload/persistence layer (`audio_compat.py`) so both are covered; runtime-only fixes leave the other path broken.
- Visual lock-in: dark `#05060f`, glassmorphism, 3D tilt cards, no white borders, grid `.cols` left col fixed 480px with equal-height stretch on wide viewports (`@media(min-width:1101px)`); voice carousel vitems size via `height:calc(100% - 96px)` (top/bottom margin 48px = left/right margin to the card border — the user's stated rule: symmetric margins).
- Pointer layer: native cursor fully hidden (`cursor:none` app-wide) + two JS layers — `#cdot` precision dot (no easing, the click-accuracy core) and `#cring` trailing aim ring. New interactive classes must be appended to the hover-loop `closest(...)` selector list or the control is dead to the pointer/tilt loops. JS-failure fallback restores the native cursor via a marker class on `<html>` — assert its absence in healthy probes.

## Verification (the user's hard gate)

Every deliverable must be **exercised, not described**: headless Playwright probe against the RUNNING host (per the `frontend-ui-error-probes` skill's live-host verify reference — run the probe with the venv python, wait ~4.5s for rAF settle, read computed style + `getBoundingClientRect`, screenshot → vision_analyze), plus end-to-end API tests when wiring I/O (e.g. upload a real m4a to the stream-start endpoint and grep the host log for the transcode line). Self-check every user-named element before reporting; this user rejects "description instead of artifact".

## Workflow order (what actually works here)

1. Measure first, patch second: for geometry asks, run a Playwright geometry probe BEFORE editing CSS; after, re-run the same probe and diff the numbers. User asks are relative ("make top/bottom gap equal the side gap") — only a measurement pins the target.
2. Edit UI → reload-only; edit backend → restart the host (kill the whole process tree behind port 18097, relaunch `rvox_desktop.py` from the repo dir, wait for log readiness, health-check 200) BEFORE verifying. Windows process/shell pitfalls that cost real time on every host restart: `references/windows-process-shell.md`.
3. Audio-feature work: unit-test `audio_compat` directly (convert a fixture m4a → wav → soundfile), then test through the live host API, then re-check `build.spec` ships the new binary/module (ffmpeg datas + hiddenimports).
4. Report with measured before/after numbers (px, font-size, gaps), a PASS/FAIL per user-named element, and the reload/restart step the user must take.

## References

- `references/windows-process-shell.md` — host restart mechanics + MSYS/PowerShell pitfalls.
- `references/audio-format-support.md` — adding an audio input format end-to-end.
