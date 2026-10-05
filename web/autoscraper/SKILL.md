---
name: autoscraper
description: Auto-scrape HTML without writing selectors — use AutoScraper's AutoScraper.get_selectors() to learn a selector from one sample element and apply it across many similar elements (installed, v1.1, Python 3.14). Use when the user has repeated DOM elements (product cards, list rows) and wants to grab fields with minimal selector effort, or as a quick alternative to hand-writing CSS selectors.
license: Apache-2.0 (AutoScraper)
---

# AutoScraper

Python scraper that **learns the selector from a sample element** instead of you hand-writing CSS. Good for repeated structures (cards, table rows, list items).

## 本机已装
- `autoscraper 1.1.14`，Python 3.14。
- 解释器：`/c/Users/mwr_w/AppData/Local/hermes/tools/python-3.14.7+20260901-win32-x64/python.exe`

## 基本用法
```python
import autoscraper
import requests, re
from lxml.html import fromstring

html = requests.get("https://quotes.toscrape.com/").text
# 拿一个样本元素，学习选择器
sample = fromstring(html).css("div.quote")[0]
selectors = autoscraper.AutoScraper().get_selectors(sample, fromstring(html))
# 应用选择器到整页
items = [el for el in selectors.get_values_from_html(fromstring(html))]
```
配合 lxml；也可 `get_selectors(sample_element, root)` 处理子树。

## 什么时候用哪个
| 需求 | 选 |
|---|---|
| 重复 DOM 结构、想少写选择器 | **AutoScraper** |
| 精确控制/复杂 XPath | 直接 CSS/XPath（Scrapy/Scrapling/BS4） |
| 整站爬 | Scrapy / Scrapling / Crawlee |

## 坑
- 学习式选择器对"结构变化剧烈"的页面可能学歪；关键字段最好人工复核。
- 它只做选择器学习 + 取文本，不负责请求/JS 渲染。
