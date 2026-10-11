# MediaCrawler specifics (C:\Users\william_r\projects\MediaCrawler)

## CDP knobs (config/base_config.py)
- `ENABLE_CDP_MODE = True` — drives the user's system browser instead of bundled Playwright Chromium.
- `CDP_DEBUG_PORT = 9222`, `CDP_CONNECT_EXISTING = True` — connects to a browser that already listens on 9222; polls up to `BROWSER_LAUNCH_TIMEOUT` (60s) and throws a RuntimeError naming the port if none. The connector first tries `ws://localhost:<port>/devtools/browser`, falls back to `/json/version` discovery on 404 — that fallback is why it CAN succeed even when the raw localhost probe logs warnings.
- `USER_DATA_DIR` only applies when `SAVE_LOGIN_STATE` is on; the CDP path uses whatever profile the user's browser runs with.

## Running a crawl from the source tree (no packaged exe needed for testing)
```bash
cd C:/Users/william_r/projects/MediaCrawler
./.venv/Scripts/python.exe main.py \
  --platform dy \
  --type detail \
  --specified_id "https://v.douyin.com/<shortlink>/" \
  --lt qrcode \
  --get_comment true \
  --get_sub_comment false \
  --save_data_option jsonl
```
- `--type detail` + `--specified_id` accepts full video URLs AND share shortlinks (`v.douyin.com/...`) — shortlinks are auto-resolved to aweme ids.
- Crawler modes: `search` (needs `--keywords`), `detail` (needs `--specified_id`), `creator` (needs `--creator_id`).
- Comment toggles: `--get_comment true/false`, `--get_sub_comment` (sub-thread replies), `--max_comments_count_singlenotes`.
- Login types: `--lt qrcode|phone|cookie`.
- Data lands in `data/<platform>_*/` (e.g. `data/dy_comments/`); wipe the platform's data dir before a re-run for a clean result.
- The crawler re-spawns the frozen exe with `MEDIA_CRAWLER_ROLE=crawler` only in the packaged build; source-tree runs are plain python.

## Env-check behavior
- `/api/env/check` short-circuits to `{success:true, "Packaged environment ready"}` in frozen mode; in dev mode it runs the `_resolve_python()` command prefix (a LIST) with `--help` under a 30s timeout. `_resolve_python()` returns `tuple[list[str], dict]` (prefix + extra env) — never treat it as a single path string.
