---
name: crawl4ai
description: Use Crawl4AI to scrape websites, crawl whole sites, or extract structured data into LLM-ready markdown/JSON — the go-to when web extraction is needed and Firecrawl isn't the right fit (or as a free, self-hosted, keyless alternative). Already installed and verified on this machine (Python 3.14 + Playwright Chromium headless). Use when the user wants to scrape a page/site, crawl a site into RAG/markdown, extract structured fields, or build a crawler without an external API key.
license: Apache-2.0
---

# Crawl4AI

Open-source web crawler/scraper that turns any website into clean, LLM-ready Markdown or structured JSON. No API key needed — it runs locally with Playwright.

## 已安装 & 验证（本机）

- 版本：`Crawl4AI 0.9.4`，装在 Hermes 内置 **Python 3.14**（`C:\Users\mwr_w\AppData\Local\hermes\tools\python-3.14.7+...-win32-x64`），用 `pip install -e` 从源码装的。
- Playwright Chromium headless 内核已下载到 `C:\Users\mwr_w\AppData\Local\ms-playwright\chromium_headless_shell-1243`。
- 已实测：`arun("https://firecrawl.dev")` 成功，返回 33k 字符 markdown。

**坑（务必注意）**：本机 `pip` 指向 Python 3.11，`python` 指向 3.14，两者错配。装/调 Crawl4AI 必须用 3.14 的 Python 解释器：
`/c/Users/mwr_w/AppData/Local/hermes/tools/python-3.14.7+20260901-win32-x64/python.exe`
（裸 `python -c "import crawl4ai"` 在 3.11 下会 ModuleNotFoundError，那不是真没装。）

## 基本用法（Python 3.14）

```python
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai import CacheMode, BrowserConfig

async def main():
    browser_cfg = BrowserConfig(headless=True, viewport={"width":1280,"height":800})
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 单页
        r = await crawler.arun("https://example.com", cache_dir=None)
        print(r.markdown[:2000])

        # 结构化抽取（用 JSON schema）
        from crawl4ai import ExtractionStrategy
        schema = {"type":"object","properties":{"title":{"type":"string"},"price":{"type":"number"}}}
        r2 = await crawler.arun("https://shop/x", extraction_strategy=ExtractionStrategy.JSON, extraction_schema=schema)
        print(r2.extracted_content)

        # 整站爬取
        r3 = await crawler.arun_many(["https://docs.x/a","https://docs.x/b"], limit=50)
        print([p.markdown for p in r3])

asyncio.run(main())
```

## 何时用哪个

| 需求 | 选 |
|---|---|
| 单页 → 干净 markdown（喂 RAG/LLM） | Crawl4AI `arun`，`CacheMode.NO_CACHE` 省流量 |
| 整站爬进知识库 | Crawl4AI `arun_many` / `arun` + `mode.CRAWL`（设 `limit`） |
| 抽结构化字段（title/price 等） | `ExtractionStrategy.JSON` + schema |
| 已被 JS 渲染/bot 墙 | Crawl4AI 默认 Playwright 直接过；`playwright-stealth` 已装 |
| 要"答案"而非原始数据（问答式） | 用 **Firecrawl**（本机已装 + key），或 Crawl4AI + 本地 LLM |
| 零依赖、纯 HTTP 就够的静态页 | 优先 `web_extract`（我的内置工具）或 `agent-reach`，别起浏览器 |

## 与本机其他抓网页工具的关系

- **Firecrawl**：有 key、云端、带 `/search` 和 `/interact`；要"带账号的多步交互"或"AI 直接给答案"用它。
- **Crawl4AI**：本地、免费、keyless、强在整站爬取和结构化抽取、可完全离线；要"自托管、批量、省 token"用它。
- **web_extract / agent-reach**：轻，静态页首选，不起 Playwright。

## 常见坑

- **内核缺失**：如果换机器或内核被清，先 `python -m playwright install chromium`（走代理）。
- **装到错的解释器**：确认 `sys.executable` 是 3.14 内置路径，否则重装。
- **网络不稳**：Playwright 走本机代理时偶发 reset，失败就重试或换 Firecrawl。
- **大站点**：务必设 `limit` 和 `max_depth`，避免爬爆。
- **PDF/文档**：Crawl4AI 有 `pdf` 可选依赖；纯 PDF 提取建议直接用我的 `pdf` 技能。

## 验证命令（快速自检）

```bash
PY314="/c/Users/mwr_w/AppData/Local/hermes/tools/python-3.14.7+20260901-win32-x64/python.exe"
"$PY314" -c "import crawl4ai; print(crawl4ai.__version__)"
"$PY314" -c "from playwright._impl._driver import compute_driver_path; print('kw ok')"
```
