# Concurrency & Isolation

**Browsers are identities. Sessions are workspaces. State never bleeds between them.**

Every agent gets its own lane. Multi-agent multi-task parallel runs don't contaminate each other or get correlated by sites.

## Three Concurrency Models

| Model | Isolation | Shares | Typical use |
|-------|-----------|--------|-------------|
| **Cross-browser parallel** | Browser-level | Nothing (independent fingerprint/IP/cookies) | Multi-account monitoring, multi-identity ops |
| **Same-browser multi-session** | Session-level | Login state | Parallel tasks under the same account |
| **Privacy mode zero-residue** | Session-level | Nothing (fresh start each time) | One-off collection, high anonymity |

## Cross-Browser Parallel (Independent Identity)

Run any number of browsers simultaneously, each with independent cookies / fingerprint / proxy / login state. **Sites cannot correlate them.**

```bash
# Each session name must be globally unique — even when pointing to different browsers
browser-act --session monitor-shop-a browser open competitor1 https://shop-a.com
browser-act --session monitor-shop-b browser open competitor2 https://shop-b.com
browser-act --session monitor-shop-c browser open competitor3 https://shop-c.com
```

**Properties:**
- Each stealth browser is an independent identity
- Zero state cross-contamination
- Monitor a competitor with one identity while running internal automation with another — they don't interfere

**Use cases:** Multi-account monitoring, multi-store ops, batch identity isolation.

## Same-Browser Multi-Session (Shared Login State)

One browser, multiple sessions. **Shared login state, independent execution.**

```bash
# Two parallel tasks on the same browser
browser-act --session task-a browser open <browser-id> https://site.com/page1
browser-act --session task-b browser open <browser-id> https://site.com/page2
```

**Properties:**
- Shared cookies / login state
- Each session has its own navigation, network capture, dialog handling
- Two agents can work on different email threads in the same Gmail account without blocking each other
- Session ownership is enforced by the explicit-naming model

**Use cases:** Multiple subtasks under the same account.

### Naming Parallel Sessions (Globally Unique)

In a parallel setup every `--session <name>` must be **globally unique** — names cannot collide even across different browsers. Pick names that reflect each session's purpose:

```bash
# Same browser, multiple sessions: distinguish subtasks by name
browser-act --session monitor-prices browser open shop1 https://shop.com
browser-act --session track-orders browser open shop1 https://shop.com/orders
```

## Privacy Mode (Zero Residue)

Each session uses a fresh fingerprint and profile, with nothing persisted at the end. **Zero residue between sessions.**

```bash
# Create a stealth browser with privacy mode enabled
browser-act browser create --type stealth --name "ephemeral" \
  --desc "One-off collection" --private true
```

**Properties:**
- stealth browsers only
- Fresh fingerprint per session, avoiding fingerprint accumulation
- Suitable for one-off collection, or any multi-account scenario where state leakage is a risk

See [Anti-Blocking → Privacy Mode](anti-blocking.md#privacy-mode).

## Session Model

### What Is a Session

A session is a standalone browser window bound to a name. All interaction commands require the `--session` flag:

```bash
browser-act --session my-task browser open <id> https://example.com
browser-act --session my-task state
browser-act --session my-task click 2
browser-act session close my-task
```

The session name is your handle to a specific browser context, and persists until explicitly closed.

### Why Explicit Sessions

| Reason | Explanation |
|--------|-------------|
| **Parallel safety** | Multiple agents (or conversations) can operate simultaneously without conflicts |
| **Clear ownership** | Each session belongs to the agent that created it |
| **Controlled lifecycle** | Open with intent, close when done |
| **Multi-browser targeting** | Different sessions can point to different browsers |

### Session Lifecycle

```
Create (browser open) → Use (state/click/input/...) → Close (session close)
```

- The first `browser open` with a `--session` name starts the session
- The same `--session` name reuses the existing session, no duplicates
- Close after the work is done: `session close <name>`

### Session Ownership

- A session belongs to the agent / conversation that created it
- An agent should not reuse sessions it didn't create
- Existing sessions from other conversations are treated as "someone else's"
- New work always creates a new session

### Auto-Reclamation

Sessions that receive no commands for 8 hours are automatically reclaimed. No need to worry about forgotten sessions permanently consuming resources.

### Listing and Closing

```bash
browser-act session list             # List all active sessions
browser-act session close <name>     # Close a specific session
browser-act session close            # Close the current session
```

### Session-to-Browser Relationship

```
┌── Browser A (chrome) ───────────────────┐
│  Session "search"  → google.com        │
│  Session "monitor" → analytics.com     │
└────────────────────────────────────────┘

┌── Browser B (stealth) ─────────────────┐
│  Session "scrape"  → target-site.com   │
└────────────────────────────────────────┘
```

- A session belongs to exactly one browser
- A browser can host multiple sessions
- Sessions on the same browser share cookies/login but navigate independently

## Commands That Don't Need a Session

Browser-management or system-level commands don't require `--session`:

- `browser list`, `browser create`, `browser delete`, `browser update`
- `browser regions`, `browser list-profiles`
- `session list`
- `auth login`, `auth poll`, `auth set`, `auth clear`
- `get-skills`, `report-log`, `feedback`
- `stealth-extract` (creates and tears down its own temporary context)

## Best Practices

| Practice | Note |
|----------|------|
| **Descriptive names** | `check-price`, not `s1` |
| **Close when done** | Don't leave sessions hanging |
| **One browser, many sessions** | Prefer parallel sessions over duplicate browsers |
| **Globally unique names** | Parallel session names must not collide, even across different browsers |
| **One task, one session** | One logical task = one session |

## Next Steps

- [Browser Modes](browser-modes.md) — Browser choice determines isolation granularity
- [Agent Design](agent-design.md) — Design philosophy, automation capabilities, secure by default
