# Anti-Blocking

Reach places standard tools can't. **Three progressive layers, escalating only as needed.** The vast majority of blocks never reach the agent — they're absorbed at the environment layer. The few that trigger get auto-resolved at the execution layer. Only extreme cases escalate to a human.

## The Three-Layer System

```
Environment layer (look like a real user)
   ↓ triggered?
Execution layer (auto-solve verification)
   ↓ can't be solved?
Human layer (let a human jump in — see "Remote Assist")
```

| Layer | What it solves | Key capabilities |
|-------|----------------|------------------|
| **Environment** | Prevent verification from triggering at all | Fingerprint spoofing, TLS rotation, residential proxies, privacy mode |
| **Execution** | Auto-resolve when triggered | `solve-captcha` auto CAPTCHA, `stealth-extract` one-command extraction |
| **Human** | Cases automation can't handle | `remote-assist` remote handoff (see [Better Headless](headless.md)) |

## Environment Layer: Look Like a Real User

stealth browsers ship with a complete anti-detection stack, ensuring the site sees no difference from a real browser.

| Technique | Purpose |
|-----------|---------|
| **Fingerprint spoofing** | Canvas / WebGL / fonts / plugins — consistently faked, all components tell the same story |
| **Navigator patching** | `webdriver` / `chrome.runtime` / plugin array all normalized |
| **TLS fingerprint rotation** | Matches real-browser TLS signatures |
| **Headless concealment** | Run headless to save resources AND pass detection — both at once |
| **Proxy system** | Dynamic proxy (auto-rotated regional IPs) / Static proxy (managed fixed IP) / Custom proxy (BYO) |
| **Privacy mode** | Fresh fingerprint + empty profile per session, no persistence |

### Proxy System

Only stealth browsers support proxies. The three modes are mutually exclusive:

**Dynamic proxy (managed)**

```bash
browser-act browser create --type stealth --name s1 --desc "..." --dynamic-proxy US
```

- IP auto-rotates on every browser restart
- List available regions: `browser-act browser regions`

**Static proxy (managed fixed IP)**

```bash
browser-act browser create --type stealth --name s1 --desc "..." --static-proxy <proxy_id>
```

- Fixed IP, stable across sessions
- Best for account warm-up, login persistence, API allowlists, and any scenario that requires being bound to the same IP long-term
- List purchased proxies: `browser-act proxy list`
- Purchase a new proxy: `browser-act proxy buy-request` (returns a purchase URL)

**Custom proxy (BYO)**

```bash
browser-act browser create --type stealth --name s1 --desc "..." --custom-proxy socks5://user:pass@host:port
```

- Supports HTTP / SOCKS5
- Your proxy, your IPs

### Privacy Mode

When enabled, each session uses a fresh fingerprint and empty profile, with no data persisted:

```bash
browser-act browser create --type stealth --name "ephemeral" --desc "One-off task" --private true
```

Or toggle on an existing browser:

```bash
browser-act browser update <stealth-id> --private true
```

Use cases: multi-account isolation, preventing fingerprint accumulation, one-off operations. Trade-off: cannot retain login state.

## Execution Layer: Auto-Resolve Verification

### stealth-extract (WebFetch Replacement)

Read-only content extraction with zero session management:

```bash
browser-act stealth-extract https://protected-site.com
```

**What it does:**
1. Launches an anti-detection browser with full fingerprint spoofing
2. Navigates to the target URL and waits for JS to render
3. Returns the page in markdown (or HTML)
4. Closes the browser — no cleanup required

**No session, no browser management, no state.** URL in, content out.

```bash
# HTML output
browser-act stealth-extract https://example.com --content-type html

# Use a managed proxy (region-specific IP)
browser-act stealth-extract https://example.com --dynamic-proxy US

# Use a managed static proxy (fixed IP)
browser-act stealth-extract https://example.com --static-proxy <proxy_id>

# Use a custom proxy
browser-act stealth-extract https://example.com --custom-proxy socks5://host:port

# Custom timeout (default 30s)
browser-act stealth-extract https://example.com --timeout 60

# Save to file
browser-act stealth-extract https://example.com --output ./result.md
```

**Rule:** Only need to *read*? Use `stealth-extract`. Need to *interact*? Use a stealth browser.

### solve-captcha Auto CAPTCHA

Automatically identifies and solves common CAPTCHA types (image selection, text recognition, etc.):

```bash
browser-act --session s1 solve-captcha
```

Returns `solved=True` when it goes through automatically.

#### Escalation when auto-solving fails

```bash
# Try automatic first
browser-act --session s1 solve-captcha

# If it fails, show it to the user locally
browser-act --session s1 browser open <id> <url> --headed

# Or escalate to remote handoff
browser-act --session s1 remote-assist --objective "Please solve the CAPTCHA"
```

## Human Layer: Hand It to a Person

When environment + execution still can't solve it, escalate to a human — `remote-assist` generates a live URL that the user opens on any device to take over. See [Remote Assist](remote-assist.md).

## Escalation Strategy

```
1. Default chrome / chrome-direct + no proxy → fits most everyday sites
2. Anti-scraping triggered → upgrade to stealth + configure a proxy
3. CAPTCHA still appearing → solve-captcha auto-resolves
4. Auto-resolution fails → remote-assist hands off to a human
```

## Comparison with Baseline Tools

| | curl / WebFetch | Standard Puppeteer / Playwright | BrowserAct |
|---|---|---|---|
| Handles JS rendering | ✗ | ✓ | ✓ |
| Anti-scraping bypass | ✗ | ✗ | ✓ (environment layer) |
| Auto CAPTCHA | ✗ | ✗ | ✓ (execution layer) |
| Human handoff when stuck | ✗ | ✗ | ✓ (human layer) |
| Headless without detection | N/A | ✗ (headless easily detected) | ✓ (stealth headless) |

## Next Steps

- [Better Headless](headless.md) — Default headless + remote handoff
- [Browser Modes](browser-modes.md) — Pick the right browser
- [Skill Forge](skill-forge.md) — Bake anti-scraping experience into reusable Skills
