---
name: crawlee
description: Build reliable Node.js web scrapers/crawlers with Apify Crawlee (installed at C:\Users\mwr_w\tools\node-packages). Use when the user wants a Node/TS crawler, needs queue-based crawling, browser scraping via Playwright/Puppeteer, or input-keyed datasets; prefer Python (Scrapy/Scrapling/browser-use) unless the target is JS/Node or the user explicitly wants Node.
license: Apache-2.0 (Crawlee)
---

# Crawlee (Node.js)

Apify's modern crawler library for Node/TypeScript: queue-based HTTP + browser scraping, datasets, and a built-in web server for debugging. Installed as a local Node package.

## 本机已装
- Node 包装在 `C:\Users\mwr_w\tools\node-packages`（`npm install crawlee`），含 `playwright-crawlee`/`puppeteer-crawlee`。
- 运行 JS：`node script.mjs`（node 已在本机）。

## 最小可用（TypeScript/JS）
```js
import { PlaywrightCrawler, PlaywrightDataset } from 'crawlee/playwright';

const crawler = new PlaywrightCrawler();
await crawler.addRequests(['https://example.com', 'https://quotes.toscrape.com']);
crawler.addHttpContext(async ({ page, log, dataset }) => {
  const quotes = await page.$$eval('.quote .text', els => els.map(e => e.textContent));
  log.info(`${quotes.length} quotes`);
  await dataset.push({ quotes, url: page.url() });
});
await crawler.run();
console.log(await (await new PlaywrightDataset()).toList());
```

## 什么时候用哪个
| 场景 | 选 |
|---|---|
| Node/TS 技术栈里的爬虫 | **Crawlee** |
| Python 栈、整站大规模爬 | Scrapy / Scrapling |
| 需要 JS 渲染的单页 | Scrapling `DynamicFetcher` / browser-use |

## 坑
- 浏览器版需装对应 Playwright/Puppeteer 内核（`npx playwright install`）。
- 本机 node 是 LTS，跑 ES 模块用 `.mjs` 或 `"type":"module"`。
