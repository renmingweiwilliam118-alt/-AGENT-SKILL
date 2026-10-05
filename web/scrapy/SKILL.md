---
name: scrapy
description: Build production-grade web crawlers and scrape structured data from many pages at scale with Scrapy (installed, v2.19, Python 3.14). Use when the user wants a full crawler (hundreds/thousands of URLs), needs concurrent + throttled + retry + auto-download-middleware behavior, wants Scrapy spiders/items/pipelines, or needs to follow links across a site. For single-page quick grabs prefer web_extract/curl; for JS-heavy or anti-bot pages prefer Scrapling/browser-use.
license: BSD-3-Clause (Scrapy)
---

# Scrapy

Full-featured Python web-scraping/crawling framework. Installed on this machine (Python 3.14, Hermes built-in interpreter). Use it when you need to **crawl a whole site** with concurrency, throttling, retries, and structured item pipelines — not for a one-off single page.

## 本机已装
- `scrapy 2.19.0` + 依赖（parsel/twisted/w3lib/queuelib…），装在 Hermes Python 3.14。
- 用 3.14 解释器跑：`/c/Users/mwr_w/AppData/Local/hermes/tools/python-3.14.7+20260901-win32-x64/python.exe`（裸 `python` 是 3.11，别混用）。
- 脚手架：`scrapy startproject mybot`，`scrapy genspider myspider example.com`。

## 最小可用 spider
```python
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    def parse(self, response):
        for q in response.css("div.quote"):
            yield {"text": q.css("span.text::text").get(),
                   "author": q.css("small.author::text").get()}
        next = response.css("li.next a::attr(href)").get()
        if next:
            yield response.follow(next, self.parse)
```

## 什么时候用哪个
| 场景 | 选 |
|---|---|
| 整站批量爬、上千 URL、要并发/节流/重试 | **Scrapy** |
| JS 渲染 / anti-bot / Cloudflare | **Scrapling**（`StealthyFetcher`）或 **browser-use** |
| 单页快速取内容喂 LLM | 内置 `web_extract` / `curl` |
| 结构化字段进 pipeline 存 DB/JSON | Scrapy `Item` + `Pipeline` |

## 坑
- 静态 HTTP 抓取强；要渲染 JS 的页面需 `scrapy-playwright` 或换 Scrapling。
- 注意目标站点 robots/速率限制，加 `AUTOTHROTTLE`（`scrapy.downloadermiddlewares.throttle.AutoThrottle`)。
- 代理不稳/被 403 时配 `DOWNLOAD_DELAY`、`ROBOTSTXT_OBEY`。
