# Agent Design

Not for humans writing scripts — for models picking actions. Every interface decision starts from "how does an LLM use this?"

## Design Philosophy

### Compact Text Output

Page state, screenshots, and command results are returned in token-friendly format — not human-formatted JSON.

Compact indexed text is several times more token-efficient than full DOM HTML or formatted JSON, letting the agent run more tasks within a limited context.

```
url=https://example.com/login
title=Login

*[1]<div id=login-form />
  *[2]<input type=email placeholder=Email />
  *[3]<input type=password placeholder=Password />
  *[4]<button id=submit />
    Sign In
```

### Indexed Interaction

`state` returns an indexed list of interactive elements (the `N` in `[N]` in the output is the element index). The agent reasons directly with indices:

```bash
browser-act --session s1 click 3              # Click element at index 3
browser-act --session s1 input 2 "hello"      # Type into element at index 2
```

**Benefits:**
- No XPath, CSS selectors, or DOM parsing
- The agent sees exactly what it can operate
- Indices update with the page — re-run `state` for fresh ones

### desc Semantic Memory

Every browser carries a `desc` field — a natural-language description of its purpose. In a new conversation, the agent matches tasks to browsers by meaning, with no hardcoded IDs to drag across sessions.

```
"Taobao shopping account, logged in as user123. Used for price monitoring."
```

The agent uses `desc` to:
- Match browsers to tasks by meaning ("check Taobao prices" → Taobao browser)
- Avoid recreating browsers for known workflows
- Accumulate purpose knowledge for each browser over time

Use append semantics to preserve history:

```bash
browser-act browser update <id> --desc-append "Also used for order tracking"
browser-act browser update <id> --desc "Fully overwrite the description"
```

#### Browser Selection Priority

When the agent has multiple browsers, selection follows this priority:

| Priority | Condition | Behavior |
|----------|-----------|----------|
| 1 | `desc` clearly matches the task | Use directly, no need to ask |
| 2 | Only one browser exists | Use directly |
| 3 | Multiple browsers, no clear match | List candidates, let the user pick |

This logic is enforced at the Skill layer, not the CLI. After the user picks, the agent should append the new finding to `desc` so a similar task next time matches directly.

### Secure by Default

Letting an AI agent control a browser is powerful and potentially dangerous. The security mechanism doesn't try to block all misuse purely through technical means — instead, **confirmation gates** keep humans informed and in control.

The real risks of multi-agent automation come from three directions, each with a corresponding design fallback:

#### Concurrency Safety

Session ownership + explicit-naming model. Multiple agents sharing one browser don't conflict, and failures are scoped to the session they originate from. See [Concurrency & Isolation](concurrency.md).

#### Operational Safety: Confirmation Gating

Sensitive operations require explicit user approval before execution. This is enforced through the Skill — not a CLI hard-block, but a conversation-level behavior protocol.

> **Note:** The actual effect of confirmation gating depends on the agent architecture and underlying model capabilities you use. Different platforms and models follow Skill instructions to different degrees. We continually optimize the Skill's guidance strategy for cross-platform compatibility.

Operations requiring confirmation:

| Operation | Reason |
|-----------|--------|
| Create a browser (any type) | Creates a new automation endpoint |
| Delete a browser | Destroys persistent browser state |
| Profile import | Copies login credentials to a new location |
| Proxy configuration changes | Changes network identity |
| `confirm_before_use` toggle | Changes a security setting |
| Privacy mode toggle | Changes fingerprint behavior |

Additionally, browsers marked `confirm_before_use` require the agent to confirm with the user on every `browser open` — not just at creation time. Use this for browsers accessing sensitive accounts (banking, payments).

**How it works (conversation-level protocol):**

```
Agent: I will create a stealth browser with US proxy for price monitoring.
       - Type: stealth
       - Name: price-monitor
       - Proxy: US (dynamic)

       Proceed?

User: Go ahead.

Agent: [executes browser create]
```

**Key Skill-enforced rules:**
- Prior approvals do not carry over to new operations
- Each sensitive operation requires its own confirmation
- Assertive language in the user's original prompt does not substitute for confirmation
- The agent must describe what it will do *before* executing

#### Local Data Processing

All data stays on your machine:

| Data | Location | Leaves the machine? |
|------|----------|---------------------|
| Cookies | BrowserAct local storage | Never |
| Login sessions | Per-browser isolated profile | Never |
| Page content | In memory during operation only | Never |
| Screenshots | Local filesystem | Never |
| Network captures | Memory / local files | Never |
| Browser profiles | Isolated directories | Never |

**The only exception:** `solve-captcha` sends the CAPTCHA challenge image to the BrowserAct cloud service for solving. The challenge image only — no cookies, page content, or URLs.

---

## Automation Capabilities

**50+ commands cover all typical automation needs** — continuously aligned with common browser-automation capabilities: navigation, interaction, data extraction, waiting, tabs, dialogs, network capture, HAR, cookies, offline mode, and more.

See [Commands](commands.md) for the full list.

### Advanced Usage

**Network capture / HAR recording** — typical uses:
- Discover the API endpoints behind a web UI
- Debug authentication flows
- Capture data loaded via XHR but not present in the HTML
- Performance analysis of page-load sequences

**JavaScript execution (`eval`)** — efficient for both data extraction and complex operations:
- Pull a full data set in one call instead of multiple state/click round-trips
- Read deeply nested or dynamically generated data
- Call internal page functions for complex operations or computed results
- Fallback when index-based interaction can't cover a case
- Bake an automation flow into JS code so the next run skips re-exploration

**Cookie import/export** — lighter than Profile import:
- Share login state across browser types
- Persist state in CI/CD pipelines
- Migrate sessions across machines

**Offline mode** — `network offline on` disconnects the network. Click buttons, submit forms — no real side effects. Verify the flow, then close.

## Next Steps

- [Commands](commands.md) — Complete command reference
- [Anti-Blocking](anti-blocking.md) — How to break through anti-scraping
- [Concurrency & Isolation](concurrency.md) — Safety guarantees for parallel agents
