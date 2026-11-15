---
name: fastapi-blocking-i-o
description: "Use when a FastAPI handler blocks the event loop."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fastapi, uvicorn, async, sse, event-loop, python]
    related_skills: [pywebview-windows, python-desktop-app-packaging]
---

# FastAPI / uvicorn: blocking I/O in async handlers

Class of task: a FastAPI (uvicorn) backend — commonly a desktop app whose UI is a WebView over a local server — whose `async def` handlers or SSE generators make blocking calls: native Win32 syscalls, LLM/HTTP client calls, or `queue.get(timeout=…)` waits.

## When to Use

- A FastAPI/uvicorn server freezes entirely (every route, static files, and SSE stop at once), or one route is mysteriously slow.
- You are about to add a native/Win32 syscall, an LLM/HTTP client call, or a `queue.get(timeout=…)` wait into an `async def` handler or streaming generator.
- A user-triggered run/agent/do-it action that calls a blocking model or captures the screen must stay responsive to an abort.

## The core failure (costs a whole session if missed)

uvicorn runs **one** event loop. A blocking call inside an `async def` handler or an async generator blocks that loop, so the freeze is TOTAL, not local: every other route, the static root, and all SSE streams stop responding until the process is killed. The symptom is misleading — it looks like "one slow endpoint" or "the UI is stuck." The tell: **if even a static `/` endpoint hangs, the loop itself is blocked — stop hunting for a single slow route and look for blocking calls inside async handlers.** A second tell: any UI panel that fills *only* from server-pushed SSE/event frames sits at its idle/placeholder state whenever the loop is wedged or a reconnect missed the first frame -- an empty "screenshot / status / 看" panel is a wedge symptom, not proof the feature never ran. Seed such a panel from the last persisted value (e.g. a session's `last_shot`) so it also survives reconnects.

## Rules

1. **Offload every blocking call in an `async def` handler/generator to the thread pool.** `await asyncio.to_thread(fn, *args)` for: native Win32 calls (window enumeration, key/mouse injection, root-owner resolution), LLM/HTTP client calls (`model_test`, chat `send_message`), and — the easy one to miss — `queue.get(timeout=…)` inside an SSE / `StreamingResponse` generator. For long-lived producers use a non-blocking `asyncio.Queue` instead of a bare `queue.Queue`.
2. **Bound any enumeration or native call that can hang on a wedged target.** A target app that stops pumping messages can hang a window-enumeration or `PrintWindow` call; cap it with a timeout wrapper (~12s) so one dead window can't drag the whole server down.
3. **Diagnose a wedged server by probing several endpoints, not one.** If `/`, a health route, and an SSE endpoint all time out together, the loop is blocked. Confirm the fix by re-probing: the routes that used to hang must return 200 fast again.
4. **Verify SSE/streaming endpoints with `curl -N`, not Python `urllib`.** `urllib` buffers streaming responses, so an SSE endpoint looks like "no events ever arrive" even when frames are flowing; `curl -N` (or a raw socket) shows them live.
5. **Make user-triggered long-running actions interruptible.** A run/agent/do-it endpoint that calls a blocking LLM or captures the screen must time-bound each step and poll an abort flag on a timer (≈1s) so the user's abort actually takes effect mid-call — check the flag between AND inside long steps, otherwise the abort request never gets processed.
6. **A polled / server-pushed *image or telemetry* endpoint must fail-soft, not 500.** The tell is a monitor `<img>` that blanks to black while its timestamp/labels keep ticking: the data source errored (a poisoned native call, a hung capture) but the timer is a separate JS loop, so the frame died while everything else still moved. When the capture/IO behind `asyncio.to_thread` raises, return **503** (or 200 with the last persisted frame) and never let it propagate a 500/exception that blanks the client; the frontend holds its last good frame and re-polls, so a transient/clobbered read degrades to "stale, still showing" instead of black. (The native-cause half — a shared GDI/ctypes capture silently poisoned by a re-declared `argtypes`/struct — is diagnosed and cured in ctypes-win32-windows rule 8.)

## Self-check before delivery
- Grep the server module for blocking calls sitting directly in `async def` / `async for` bodies (`time.sleep`, blocking `requests`, `windll`/`gdi32` syscalls, `queue.get`) — each must be behind `asyncio.to_thread` or a non-blocking queue.
- After the fix, re-probe the routes that used to hang (fast 200s) and stream SSE with `curl -N` to confirm frames flow.
- **Validate against the code you just changed.** A live server process keeps its in-memory version, so restart it before testing; and probe the port the startup banner actually bound -- a loopback app that can't take its preferred port silently falls back to a random one, and testing that old port means you validated the stale instance and the fix "still doesn't work."
