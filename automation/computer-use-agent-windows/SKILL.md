---
name: computer-use-agent-windows
description: "Build Windows computer-use agents that drive real apps."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, ctypes, computer-use, automation, gui, win32]
    related_skills: [ctypes-win32-windows, gui-automation-with-cua-driver]
---

# Computer-use agent on Windows

## When to Use

Load this when asked to build, debug or extend an agent that operates real
desktop applications on Windows by reading the screen and injecting mouse and
keyboard input -- a "computer-use" / "AI 运营智能体" product. Also load it when
a Windows automation script needs to focus another window reliably, capture a
window that is behind others, or inject CJK text into a control.

Building an agent that operates *existing* desktop apps (chat windows, admin
consoles, CRM backends) the way a human would: read the screen, decide, then
inject real input. This is the "识流AI / shiflow.com" product shape.

## Architecture that works

```
native.py   all user32/gdi32/ctypes calls behind ONE RLock
capture.py  PrintWindow(PW_RENDERFULLCONTENT) -> PIL -> JPEG/data-URI
brain.py    pluggable: scripted | local-pixel | openai-compatible | anthropic
kb.py       dependency-free lexical retrieval (char unigrams + CJK bigrams)
agent.py    the loop: capture -> decide -> inject -> read-back verify
server.py   FastAPI + SSE console (loopback only, no auth by design)
```

## Rules (each one was paid for)

1. **Capture with `PrintWindow(PW_RENDERFULLCONTENT)`, not BitBlt.** It returns
   the window's own surface even when another window covers it. BitBlt only as
   Handle BOTH of PrintWindow's failure modes, not just one: it can return FALSE, or -- more subtly -- *succeed* but hand back an ALL-BLACK frame for GPU/WebView2/D3D-composited windows, and a bare `if got:` truthiness check passes on a black frame, so the black box ships to the user as 'the screen never shows'. After PrintWindow, run a cheap blank check (downsample to ~16x16 and read luminance mean + contrast, e.g. PIL `ImageStat.Stat`: blank if mean < ~18 AND contrast < ~42); when blank OR FALSE, fall back to a GDI on-screen read -- `GetWindowDC(NULL)` + `BitBlt` the window's rect -- which grabs the real composited pixels. Prefer that GDI read over `mss` for the on-screen fallback: GDI works in the same DPI-unaware logical coordinate space the app's windows were created in, while `mss` can report a different *physical* screen width and misalign a logical-coord rect 1:1. Verify the fallback is non-black (mean above the threshold), not merely non-None.
   Convert the bottom-up 32bpp DIB with
   `Image.frombytes("RGB", (w,h), raw, "raw", "BGRX", 0, -1)` -- the negative
   stride is what un-flips it. Verify with a synthetic pattern, not by eye.

2. **A capture is not the same as what input will hit.** `PrintWindow` sees
   through overlaps; `SendInput` does not. Guard every click with
   `WindowFromPoint` compared as a *root owner* (`GetAncestor(..., GA_ROOT)`),
   and raise the target first. See ctypes-win32-windows skill rules 16-19.

3. **Image coordinates -> screen coordinates must scale.** A capture may be
   downscaled for the API, so keep the ratio and map back
   (`screen = rect.origin + img_xy * (rect.size / img.size)`), then clamp into
   the window rect so a wild model coordinate cannot escape it.

4. **Verify "sent" by re-capturing, never by logging success.** Capture before,
   inject, sleep, capture after, compare a pixel histogram diff. Report success
   only on a real change; on failure say what was seen. This is the single most
   valuable habit in this class of work. The change that is reliably detectable is
   the CONSEQUENCE of the action (a new chat bubble, a large screen delta), not the
   act of typing itself: a handful of characters typed into an input box is far too
   small to move a full-window histogram diff -- it reads ~0.0000 -- so you CANNOT
   confirm "the text landed in the box" by diffing the whole window around a type.
   Confirm by verifying the send instead (diff a cropped input-row region only if
   you must detect the type itself).

5. **Chinese text must go through the clipboard (Ctrl+V), not key-by-key.**
   IME state and keyboard layout make per-character injection unreliable, and
   `SendInput` needs `wVk` codes -- scan codes silently do nothing (see
   ctypes-win32-windows rule 15). Clipboard access has one owner system-wide,
   so retry the open.

6. **Two modes, and default to the safe one.** *assist*: click + type, then
   stop and show the draft for a human to send. *auto*: press Enter directly.
   Ship assist as the default. Also: ESC to abort, and a max-step cap.

7. **The reasoning trace is the product.** Log intent, reasoning, confidence,
   per-step model latency and the action list, streamed to the UI. Users trust
   an agent that explains itself far more than a silent one.

8. **A pluggable brain is what makes the project honest.** `scripted` (fixed
   scenario) and `local-pixel` (genuine but crude vision) prove the whole
   pipeline with no API key; `openai`/`anthropic` plug in real vision later.
   Be explicit in the UI about which brain is active.

9. **Robust send that survives any machine / window size / DPI: locate the entry
   target by verified effect, never by a guessed or remembered click point.** A
   model pixel coordinate or a remembered screen point for the input box breaks the
   moment the window is resized or the display DPI differs -- that is exactly the
   failure that turns "works on my box" into "works everywhere." Two-tier send:
   (a) first try **no-click** -- raise the window, inject the text via clipboard,
   press Enter, and try BOTH plain Enter and Ctrl+Enter because the user has
   remapped which one sends; verify on the new-bubble re-capture; (b) only if that
   fails, **sweep a small candidate grid expressed as whole-window fractions**
   across the chat-pane input row (click -> retype -> Enter -> verify) and remember
   the fraction that succeeded, reusing it for the life of the window. Whole-window
   fractions scale to any size/DPI; absolute coordinates do not. Keep every candidate
   strictly left of the send-button zone so a stray click can't fire an accidental
   send. **A send that can't be verified is a no-op, not a guess:** if neither tier
   yields a verified new bubble, warn loudly and send nothing -- mis-sending into
   the wrong field or window is worse than not sending at all.

10. **Clear the input (Ctrl+A + Delete via SendInput) before every re-type.** When
    a no-click or a candidate's text landed but its Enter didn't fire, the stray
    characters are still sitting in the box; without wiping first, the next attempt
    attempt concatenates onto them and one send carries two messages.

    11. **A "frozen capture" is usually a window-state problem, not a capture bug.**
        Three states all read as "nothing changes on screen": the target is
        *minimized* (`IsIconic=True`), *hidden* (`IsWindowVisible=False`, set by
        `SW_HIDE`), or its handle was *recycled* because the target app restarted.
        `ShowWindow(SW_RESTORE)` ONLY undoes *minimize* — on a *hidden* window it
        silently no-ops, so the window stays dark and every frame is identical (the
        "frozen screen" loop); any model call on that stale image is wasted. Handle
        it by state: `if IsIconic(hwnd): ShowWindow(hwnd, SW_RESTORE)  elif not
        IsWindowVisible(hwnd): ShowWindow(hwnd, SW_SHOWNORMAL)` — `SW_SHOWNORMAL`(=1)
        is what actually re-shows a `SW_HIDE`'d window. And never trust a handle you
        cached at session start: the target can restart (new handle) or the user can
        hide it, so re-enumerate by window title each cycle (`EnumWindows` +
        `GetWindowText` match) and re-bind the session's target handle. If NO
        matching window exists, surface an actionable status ("target not found /
        hidden — open or restore it") instead of looping on a frozen frame.

    ## Verification: prove it on screen, not in the code path

Do not hand the user a mock and call it done. Build a **fake target window**
(`targets/fake_window.py` in the reference project): pure-GDI drawing, but with
a *real* EDIT control and a *real* BUTTON, `WS_EX_TOPMOST` so injected clicks
reach it without minimising anything the user has open. Then:

- drive a "customer" message in via `PostMessage(WM_USER+1)`
- run the agent against it
- assert the window's own state **and** the pixel read-back both show the reply

Assert on both. The target's self-reported state catches "the text went
somewhere"; the pixel diff catches "the UI actually updated".

Run the same thing once more through the HTTP API to prove the console path.

## Honest scope statement

When a user asks "can you build this too" about a commercial product, split the
answer: which layers are engineering (reproducible) and which are R&D moat
(a self-developed vision model is not). Say which is which, and say what you
can and cannot verify in the current environment (no API key = pipeline proven,
recognition accuracy unproven).

## Reference implementation

Local checkout: `C:\Users\mwr_w\shiflow-mini` (full working implementation; launch
`python app.py` for the native pywebview window or `python main.py` for the browser
console). Run `python main.py --selftest --e2e` (real window, real input) before
claiming done. Read its README before starting a new variant; it records the
dependency, config and known-boundary decisions.
