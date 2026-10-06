# Installation

## Agent Integration (Recommended)

Tell your AI agent:

> Install browser-act. Skill source: https://github.com/browser-act/skills/tree/main/browser-act . Verify it works after installation.

The agent will handle CLI installation, Skill configuration, and verify everything is working.

## Manual Installation

```bash
uv tool install browser-act-cli --python 3.12
```

Verify:

```bash
browser-act --version
```

## Authentication (Optional)

An API Key unlocks the following features:

- **stealth browsers** — Anti-detection browsing with fingerprint spoofing
- **stealth-extract** — One-command extraction of protected page content
- **Dynamic proxy** — Managed IP rotation, allocated by region
- **solve-captcha** — Automatic captcha solving

Chrome and chrome-direct browsers work without authentication.

Get an API Key:

```bash
browser-act auth login
# Opens registration link → complete signup → poll for the key
browser-act auth poll
```

Or set it directly:

```bash
browser-act auth set <your-api-key>
```

## Upgrade

```bash
uv tool upgrade browser-act-cli
```

The Skill layer automatically detects mismatches between CLI and Skill content versions and guides the upgrade.

## Platform Support

| Platform | Status |
|----------|--------|
| Windows | Supported |
| macOS | Supported |
| Linux | Supported |

## Requirements

- Python 3.12+
- Chrome/Chromium (for `chrome` and `chrome-direct` types)
- API Key (only required for `stealth` type)

## Troubleshooting

### Command not found after install

Make sure the `uv` tool directory is in your PATH:

```bash
uv tool dir
# Add the output path to your shell PATH
```

### Diagnostics

Upload logs for issue diagnosis:

```bash
browser-act report-log
```

Send improvement suggestions:

```bash
browser-act feedback "Description of the issue or suggestion"
```

## Next Steps

- [Quick Start](quick-start.md) — Run your first automation
- [Skills](skills.md) — How agents discover and use BrowserAct
