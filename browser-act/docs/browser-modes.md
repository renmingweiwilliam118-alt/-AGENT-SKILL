# Browser Modes

Three browser modes by use case, all running on your machine:

| Mode | Scenario | Key trait |
|------|----------|-----------|
| **chrome** | Reuse local Chrome login state | Two sub-modes: Profile import / CDP attach |
| **stealth · privacy mode** | Frictionless batch scraping without login | Fresh fingerprint per session + proxy rotation, zero residue |
| **stealth · fixed identity** | Logged-in accounts · multi-browser parallel | Stable fingerprint + stable IP, stable account identity, not flagged as bots |

## chrome: Reuse Local Chrome Login State

Best for already-logged-in sites (Gmail, GitHub, Jira, etc.) when you don't want to log in again. Two sub-modes are available.

### Sub-mode 1: Import Local Profile

Extract a Profile (cookies, localStorage, IndexedDB) from local Chrome into a standalone Chromium instance:

```bash
# List importable profiles
browser-act browser list-profiles

# Create a chrome browser with the chosen profile
browser-act browser create --type chrome --name "work" \
  --desc "Work Chrome: logged into GitHub, Jira, Gmail" \
  --source-profile <profile-id>
```

**Properties:**
- A standalone Chromium instance, isolated from your local Chrome
- Import is a one-time snapshot — later changes in local Chrome do not sync
- Quota: up to 20 browsers
- Suitable for long-running automation tasks

#### You can also import after creation

If the browser already exists, import separately:

```bash
browser-act browser import-profile <browser_id> <profile_id>

# If Chrome needs to be restarted to enable CDP
browser-act browser import-profile <browser_id> <profile_id> --allow-restart-chrome
```

#### What is imported

| Included | Excluded |
|----------|----------|
| Cookies | Browsing history |
| localStorage | Bookmarks |
| IndexedDB | Extensions |
| Session storage | Cache |
| | Saved passwords |

#### Two import modes

| Mode | Path | Trait |
|------|------|-------|
| **Local mode** | chrome → chrome | Direct file copy. Fastest, most complete |
| **CDP mode** | any → stealth, cross-type | Network extraction via DevTools Protocol |

#### Prerequisites

- Must call `browser list-profiles` first to discover Profile IDs
- The target browser must already exist (created via `browser create`)
- The source browser (Chrome) may need to be closed for local import

#### Risk Notes

Profile import has inherent risks the agent must communicate to users:

1. **The source browser may be closed during import.**
2. **An IP change at the new location may trigger re-verification on some sites.**
3. **Environment differences (fingerprint, location) may trigger re-login.**
4. **Import is a snapshot — later changes at the source do not propagate.**

### Sub-mode 2: CDP Direct Attach

Directly drive your running local Chrome — extensions, certificates, and SSO are all in place:

```bash
browser-act browser create --type chrome-direct --name "live" --desc "Direct attach to local Chrome"
browser-act --session work browser open <browser-id> https://internal.corp.com
```

**Properties:**
- Zero configuration — no Profile import required
- Full inheritance of local Chrome's extensions, bookmarks, certificates, and SSO cookies
- Quota: 1 chrome-direct browser globally
- While running, your Chrome is being automated (you can't use it manually)
- Headed mode is not supported (since it's already your browser)

**Best for:** Enterprise SSO, sites that depend on specific extensions or certificates, quick operations that don't require isolation.

### Comparing the Two Sub-modes

| | Profile import | CDP attach |
|---|---|---|
| Setup | Choose a profile to import | Zero config |
| Isolation | Standalone process | Your actual Chrome |
| Extensions / certs | Excluded from import | Fully inherited |
| Quota | 20 | 1 (global) |
| User's Chrome occupied? | No | Yes |
| Long-running tasks | ✓ | ✗ (occupies your Chrome) |

## stealth · Privacy Mode: Login-Free Batch Scraping

Fresh fingerprint per session + auto-rotating proxy IPs, zero residue. Ideal for monitoring competitor sites at scale — prices, SKUs, new arrivals — with no traces left behind.

```bash
# Create a stealth browser with privacy mode + dynamic proxy
browser-act browser create --type stealth --name "monitor" \
  --desc "Competitor price monitoring" \
  --dynamic-proxy US \
  --private true
```

**Properties:**
- Each `browser open` session gets a fresh fingerprint and an empty profile, nothing persisted
- Dynamic proxy auto-rotates IPs by region
- Passes anti-detection in headless mode with full spoofing intact
- Best for one-off tasks, high-anonymity needs, and avoiding fingerprint accumulation

**Trade-off:** Login state is not retained; requires an API Key (managed service).

## stealth · Fixed Identity: Logged-In Multi-Browser

Each browser keeps a stable fingerprint + stable IP, so the account looks like a real user. Scale to multiple independent browsers — accounts cannot be correlated across them.

Requires fixed IPs (dynamic proxies rotate). Recommended: use managed static proxies:

```bash
# List purchased static proxies
browser-act proxy list

# Each store gets its own stealth browser with a dedicated static proxy
browser-act browser create --type stealth --name "shop-1" \
  --desc "Taobao store 1: women's clothing" \
  --static-proxy <proxy_id_1>

browser-act browser create --type stealth --name "shop-2" \
  --desc "Taobao store 2: electronics" \
  --static-proxy <proxy_id_2>
```

Also supports `--custom-proxy socks5://host:port` if you bring your own fixed proxy.

**Properties:**
- Each browser has independent fingerprint, fixed proxy, and independent cookies
- Same browser keeps the same IP across uses — sites treat it as a stable real user
- Sites cannot correlate across browsers
- Login state persists; subsequent operations skip the login flow
- Best for multi-store management, multi-account operations, and multi-account competitive monitoring

**Trade-off:** Requires an API Key (managed service). Managed static proxies require purchase; custom proxies are bring-your-own.

## Picking a Mode by Task

| Task | Pick |
|------|------|
| Automate a site you're already logged into in Chrome | **chrome with Profile import** |
| Need local extensions, certificates, or SSO | **chrome-direct (CDP)** |
| Scrape public content protected by anti-scraping | **stealth privacy mode** + proxy |
| Run multiple independent accounts long-term | **stealth fixed identity** (one browser per account) |
| Just need to read a page once | **stealth-extract** (no browser to create) |

## Real-World Switching Paths

**Scenario 1: From chrome to stealth**

> You automate an e-commerce site with chrome. After a few days, captchas start appearing. Switch to stealth privacy mode — a "clean identity" continues, avoiding correlation.

**Scenario 2: From stealth to chrome-direct**

> You log into an enterprise system with stealth, but it depends on a specific browser extension. Switch to chrome-direct to attach to your local Chrome (with the extension already installed).

**Scenario 3: From chrome-direct to chrome**

> You ran a task with chrome-direct successfully. But chrome-direct has only one quota and you don't want to occupy your local Chrome each time. Import the login state into a chrome browser and use chrome from then on.

## Quotas

| Type | Max | Notes |
|------|-----|-------|
| `chrome` (incl. chrome-direct) | 20 + 1 | chrome: 20 standalone processes; chrome-direct: 1 global |
| `stealth` | Per account | Allocated based on the account |

## Unified Data Model

Regardless of mode, every browser shares the same structure:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier, auto-generated |
| `name` | Human-readable name |
| `type` | `chrome` / `chrome-direct` / `stealth` |
| `desc` | Natural-language purpose description (see [Agent Design](agent-design.md#desc-semantic-memory)) |
| `dynamic_proxy` | Managed proxy region code (stealth only) |
| `static_proxy` | Managed static proxy ID (stealth only) |
| `custom_proxy` | Custom proxy URL (stealth only) |
| `private` | Privacy mode toggle, default false (stealth only) |
| `confirm_before_use` | Whether to ask the user before each use |

## Next Steps

- [Anti-Blocking](anti-blocking.md) — Anti-scraping deep dive for stealth browsers
- [Concurrency & Isolation](concurrency.md) — Multi-browser parallel patterns
- [Agent Design](agent-design.md) — desc semantic memory and browser selection logic
