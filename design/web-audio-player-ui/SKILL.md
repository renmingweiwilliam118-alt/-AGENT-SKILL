---
name: web-audio-player-ui
description: "In-page audio player UI: pause, seek, waveform sync."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-audio, audio-player, progress-bar, waveform, pause-resume, js-ui]
    related_skills: [pywebview-windows]
---

# In-page Audio Player UI (Web Audio + progress + synced waveform)

Task class: building/iterating an HTML player card for audio (generated TTS, uploads, `<audio>` blobs) where the user wants real playback controls — not just a fire-and-forget `new Audio().play()` — in a browser or pywebview web UI. This is about the UI layer; getting the file to a blob/URL is out of scope.

## When to use

- A "play" button that must also be **pause / resume** (not restart-from-zero).
- A **progress bar** that tracks `currentTime` and is **click/drag seekable**.
- A **waveform** that looks like a real (frozen) waveform when idle, animates while playing, and colorizes to show how far into the text has been read.

## Always-on rules

1. **`AudioBufferSourceNode` has no `pause()` — you stop it and re-start from an offset.** Capture the resume position, then build a fresh source node and call `start(0, offsetSeconds)`. The offset formula: `offset = offsetSoFar + (performance.now() - startedAt)/1000`, clamped to `buffer.duration`. If the audio is the `<audio>`-element fallback instead, pausing is just `.pause()` and the resume position is `.currentTime` (set it before the next `.play()`). Exact snippets: `references/audio-player-card.md`.
2. **Gate the waveform animation on a `.playing` class, and freeze it to random per-bar heights when idle.** Give each bar a random fixed `height` (looks like a real waveform), run the CSS keyframe only while `.playing` is present, and set `transform-origin:50% 100%` + animate `transform:scaleY` so bars pulse from their base instead of jumping. Colorize by index: `passed` for `i < nowIdx`, `now` for `i === nowIdx`, where `nowIdx = round(progressFraction * barCount)`.
3. **Seek + duration: don't assume `audio.duration` is ready.** Track progress on `timeupdate`; compute the seek fraction from the bar's `getBoundingClientRect()` on mousedown/mousemove/mouseup and set `currentTime = frac * duration`. Fall back to byte-length when `duration` is `Infinity`/`NaN` (common for blobs): `dur = (blobBytes.length - 44) / sampleRate / channels` for a 16-bit WAV (44-byte header).
4. **One global player at a time.** Keep a single module-level player state (id, mode `web`/`audio`, offset, startedAt, node/audio ref). Clicking a *new* card hard-stops the previous one; clicking the *same* card while `on` toggles pause. Clear the node's `onended`/stop refs before reusing so an old source's ended handler doesn't flip the wrong card's button.
5. **Verify the UI change landed in the live app — don't eyeball it.** Run a headless Playwright probe against the running host: read the element's `getBoundingClientRect()` (assert the new size/markup), assert the global player object and helper functions exist, and collect `pageerror` (must be empty). A freshly generated result card only exists after the user actually synthesizes once, so probe the *markup-generation path* or generate one first.
6. **Confirm which data layer you edited is cached vs re-read per request.** HTML/JS served per request → a page reload suffices. Data loaded once at startup (e.g. a JSONL read in the app builder) → a host restart is required; a reload shows stale data. Say the right thing before telling the user "just reload."
