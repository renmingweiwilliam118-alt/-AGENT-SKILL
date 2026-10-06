# Better Headless

Industry-standard headless browsers have two pain points: **easy to detect** and **must switch back to headed when humans are needed**. BrowserAct solves both at once.

## Headless by Default — Why

BrowserAct runs headless by default:

- **Doesn't disturb the user's current work** — no browser windows popping up unexpectedly
- **Minimal resource use** — no UI rendering overhead, lower CPU/memory
- **The way an agent should run** — silent in the background, focused on the task

When you need local visualization for debugging, switch on `--headed`. In production, default headless.

## Undetectable Headless

**Industry pain point:** Standard headless modes are flagged as bots — `navigator.webdriver` exposed, missing plugins, abnormal Canvas fingerprints, etc. This forces many teams to run headed just to defeat anti-scraping.

**BrowserAct's approach:** stealth browsers maintain full spoofing in headless mode:

- Fingerprint spoofing remains active in headless
- Navigator properties normalized
- TLS fingerprint matches a real browser
- Passes the common headless detection tests

**Result:** You don't sacrifice resource efficiency for stealth. Run headless and still pass most anti-scraping checks. Extreme anti-scraping sites may still detect — fall back to headed in that case (see below).

## Better Headless: No Need to Switch When a Human Is Needed

**Industry convention:** Headless can't be seen → must switch to headed for the user → user's current work is disrupted, and production setups can't switch at all.

**BrowserAct's approach:** Generate a live URL via `remote-assist` while still in headless. The user opens it in any browser on any device to take over — no headed switch required.

See [Remote Assist](remote-assist.md).

## Headed vs. Headless

| Mode | When to use |
|------|-------------|
| **Default headless** | Production, autonomous agent runs, headless servers |
| **`--headed`** | Local debugging or when active visual observation is needed |
| **headless + remote-assist** | Best combination for production — silent by default, remote handoff when needed |

### When to Use Headed

```bash
browser-act --session debug browser open <id> https://example.com --headed
```

Use cases:
- Anti-scraping detected — fall back to headed for higher fidelity
- Visually debug automation issues
- User completes manual steps, agent handles the rest
- Demos and co-browsing

## Next Steps

- [Remote Assist](remote-assist.md) — The full handoff story for headless mode
- [Anti-Blocking](anti-blocking.md) — How the undetectable stealth engine works
- [Browser Modes](browser-modes.md) — Pick the right browser
