---
name: cdp-browser-crawler
description: Drive CDP crawlers on a system-browser debug port.
---

# Driving CDP-based crawlers against a system browser

Crawlers with `CDP_CONNECT_EXISTING` / connect-over-CDP modes do NOT launch a browser — they wait on a debug port (default 9222) for one the user already has. The failure mode is a silent 60s poll loop with "CDP port not accessible". Your job is to make a real browser listening on that port exist BEFORE the crawler runs.

## When to Use
- Starting any crawler/scraper that drives the user's system Chrome/Edge via CDP remote debugging (Playwright `connect_over_cdp`, MediaCrawler CDP mode).
- The crawler log shows repeated "CDP port NNNN is not accessible" / "waiting for browser" polls.
- A crawl needs to attach to an already-logged-in or dedicated browser profile instead of a bundled one.

## Procedure
1. Confirm the debug port actually has a LISTENER before starting the crawler — `curl -s http://127.0.0.1:9222/json/version` returning JSON, plus a PowerShell `Get-NetTCPConnection -LocalPort 9222 -State Listen` check. Both curl-OK and no-listener are possible; trust the listener check.
2. If nothing is listening, start a dedicated CDP browser instance. Windows/Edge from git-bash:
   ```bash
   "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
     --remote-debugging-port=9222 \
     --user-data-dir="C:/Users/<user>/AppData/Local/Edge_CDP9222" \
     --no-first-run --no-default-browser-check "about:blank"
   ```
   Launch it as a PERSISTENT background terminal (persist_on_release) — see pitfall 2.
3. Re-verify the listener (step 1). Only then start the crawler; watch its log for "CDP port NNNN is accessible" / "Successfully connected".
4. If the crawler's site requires login, hand the user the QR (see "Login handoff") instead of asking for credentials in chat.
5. After the run, kill the CDP browser session; a dedicated user-data-dir keeps it out of the user's normal session.

## Pitfalls
- Chrome/Edge silently ignore `--remote-debugging-port` when a session with the SAME profile is already running — the port never opens and the crawler times out. Always use a dedicated `--user-data-dir`; that forces a fresh instance that honors the port flag.
- A browser spawned as a plain background child of a tool/terminal session dies silently when that session is torn down, dropping the listener mid-run. Launch the CDP browser with a persistent background terminal and re-verify the listener in a SEPARATE call right before each crawler run, even if it was verified minutes ago.
- On Windows, `localhost` can resolve to `::1` first; a CDP health-check written against `localhost` can fail while `127.0.0.1` is fine (or vice versa). Probe `127.0.0.1` explicitly, and when a crawler reports "port not accessible" but curl succeeds, diff what it actually probes (read its connection-test code — often a raw socket to the literal string `localhost`) before re-running.
- MSYS/git-bash `curl` to 127.0.0.1 is flaky (000/0B); a failed curl is not proof the listener is down — use the PowerShell listener check as the arbiter.

## Login handoff (dedicated profile = no site cookies)
Never guess or type the user's site credentials. If the crawler opens a QR login page: capture the QR and hand it to the user as an image —
1. `curl -s http://127.0.0.1:9222/json` → find the target tab (page URL containing the site) and its `webSocketDebuggerUrl`.
2. Open that WS, send `{"id":2,"method":"Page.captureScreenshot","params":{"format":"png","captureBeyondViewport":true}}` after `Page.enable`; read the base64 from the matching response id; write the PNG to disk.
3. Verify with vision_analyze that the QR is present and un-expired before sending it; send the PNG (MEDIA:) with a one-line "scan this with the app" note. A crawler blocked on its login poll loop is harmless while the user scans — do not kill it.

## Project note
- MediaCrawler (C:\Users\william_r\projects\MediaCrawler) specifics: CLI flags, CDP config knobs, output dirs → see references/mediacrawler.md
