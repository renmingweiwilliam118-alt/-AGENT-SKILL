# Verify a UI change by driving Playwright against the running dev host

Use this path when a change is CSS/JS (geometry, animation state, DOM classes, live inline styles) and there is a **running local dev host** plus a venv with `playwright` installed. It is more powerful than the static `--dump-dom` approach in the main skill: it settles real `requestAnimationFrame`/async work, lets you inject mouse moves, and asserts against *rendered* state rather than markup.

## Before writing the probe

- Confirm `playwright` actually imports under the host's Python: `import playwright; playwright.sync_api` — run it with the same interpreter that runs the app (often a project venv, e.g. `<proj>/.venv*/bin/python` or `<proj>/.venv*/Scripts/python.exe` on Windows). If it's not there, fall back to the Edge-headless `--dump-dom` path in the main skill.
- Confirm the host is up (`health` 200) and note its URL. The probe points at that URL, not a static file.

## The restart-vs-reload rule (decide this FIRST, it costs a restart otherwise)

- A data/config file read **once at process start** (e.g. a JSONL/JSON loaded into a module at import, a settings snapshot) requires a **full host restart** before a re-verify sees the new content.
- A page/template re-read **per request** (an HTML served from disk each request, `Cache-Control: no-store`) needs only a **frontend reload**.
- Before re-verifying after editing a content file, check which class it is. Verifying a stale host and concluding "the edit didn't take" is the classic false-negative here.

## Probe skeleton (copy, adapt the selectors)

Write the probe to a scratch `.py` and run it with the host's interpreter:

```python
from playwright.sync_api import sync_playwright
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:PORT/", wait_until="domcontentloaded")
    pg.wait_for_timeout(4000)          # let rAF/async settle; match the app's real load time
    out = pg.evaluate("""() => {
      const el = document.querySelector('SELECTOR');
      if (!el) return {found: false};
      const r = el.getBoundingClientRect();
      return {found: true,
        w: Math.round(r.width), h: Math.round(r.height),
        cls: el.className,
        style: el.style.transform,
        hasMarker: document.body.innerHTML.includes('NEW_MARKER_SUBSTRING')};
    }""")
    print(out)
    print("pageerrors:", errs or "none")
    pg.screenshot(path="PROBE_SHOT.png")   # for vision_analyze of a layout change
    b.close()
```

## Assert state, not narrative

- **Geometry / sizing change** → read `getBoundingClientRect()` width/height and compare to the expected numbers; assert a computed-style or CSS-marker substring proves the CSS landed in the served HTML.
- **rAF-driven live style** (tilt, parallax, waveform, anything the JS writes to `el.style` each frame) → a static read shows the *initial* value only. To prove the loop is applying: `pg.mouse.move(x, y)` into the element, `wait_for_timeout(500+)`, then re-read `el.style.transform` / the class flag the loop sets. A non-zero/updated value is the confirmation.
- **Error-free render** → the `pageerror` capture list must be empty for a claim of "it works." Assert on the **served** HTML (what the browser fetched), not the source file: old markers → 0 occurrences, new markers → expected count. Divergence between source and served means the host is stale (see the restart rule).
- **Layout / visual** → save a screenshot and hand it to a vision pass rather than eyeballing a description.

## Pointer/cursor layer assertions (custom-cursor apps)

When the app hides the native cursor and draws a JS pointer layer:

- **`cursor: none` / custom `cursor:url(...)` landed?** Read computed style on `body` AND representative element types (a button, an input, a hot control), asserting each `cursor` value equals the rule, not `auto`/the element's default. One computed value per type is enough.
- **Pointer layers track the mouse?** `pg.mouse.move(x, y)`, `wait_for_timeout(200+)`, then read each layer's inline `transform`. An accurate-following dot layer should equal `(x, y)`; a rAF-eased trailing layer will legitimately lag — assert it is near the target, not equal.
- **Fallback guard healthy?** If the shipped guard is a marker class on `<html>` that restores the native cursor when the JS layer fails, assert the class is ABSENT in a good run (its presence means the fallback fired and the user is on the system cursor).
- New interactive elements only work if their selector is in the hover-detection `closest(...)` list of the pointer/tilt loop — a dead-on-arrival control is a probe miss, not a styling miss.

## Pitfalls

- `pageerror` on the Playwright page catches uncaught script errors, but not failed `fetch`/XHR — a 404 on a data endpoint still renders. Assert the data actually populated (a counter > 0), not just "no exception."
- A too-short `wait_for_timeout` reads the pre-animation DOM (transform still at the initial value), giving a false "rAF isn't working." Lengthen it past the loop's first frames; the app's real load settles at a known time.
- Pointing the probe at a `file://` copy of the HTML instead of the live host misses server-injected content and the real data endpoints — the whole point of this path is the running backend. Point it at `http://127.0.0.1:PORT/`.
- One probe, one assertion set per iteration; re-running the same probe after each fix makes runs comparable. Don't hand-change selectors each pass or the before/after comparison is meaningless.
