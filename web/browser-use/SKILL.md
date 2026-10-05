---
name: browser-use
description: Drive a real browser with an AI agent using Browser Use (installed, Python 3.14, 0.13.x) — lets the agent look at the page, decide, click, type, navigate like a human. Use for multi-step browser tasks, web forms, login flows, scraping dynamic sites, or "go to X and do Y" instructions. Prefer my built-in browser tool / browser-act skills for one-off scraping; reach for browser-use when an autonomous LLM-driven browser loop is wanted.
license: MIT (browser-use)
---

# Browser Use

Python/TS framework that gives an LLM an agent loop over a real browser (CDP/Playwright). Installed on this machine.

## 本机已装
- `browser-use 0.13.x`（含 browser-harness、cdp-use、fetch-use），Python 3.14，import 验证通过。
- 解释器：`/c/Users/mwr_w/AppData/Local/hermes/tools/python-3.14.7+20260901-win32-x64/python.exe`
- 浏览器内核：本机已有 Playwright Chromium（`C:\Users\mwr_w\AppData\Local\ms-playwright`）。
- **要真正跑 agent 循环需要一个 LLM**：OpenAI/Anthropic key（本机当前未配），或本地 Ollama，或 `ChatBrowserUse` 云模型。库本体已就位，差的是推理后端。

## 基本用法
```python
from browser_use import Agent, BrowserUse, ChatOpenAI
from pydantic import BaseModel

class Steps(BaseModel):
    class Config: model_config = {"arbitrary_types_allowed": True}

async def main():
    llm = ChatOpenAI(model="gpt-4o-mini")   # 或用 ChatBrowserUse / 本地 Ollama
    agent = Agent(task="Open https://example.com and find the main heading",
                  llm=llm, browser_use=BrowserUse(headless=True))
    history = await agent.run(max_steps=10)
    print(history)
```
- 本地模型：把 llm 换成 Ollama 后端；云端：`ChatBrowserUse`（按量计费）。
- 连真实浏览器：`BrowserUse(cdp_url="http://localhost:9222")` 复用已开的 Chrome。

## 什么时候用哪个
| 需求 | 选 |
|---|---|
| 让我（agent）自己驱动浏览器做多步操作 | **browser-use** |
| 一次性抓个页面 | 内置 `web_extract` / browser-act 技能 |
| 写代码调浏览器 | Scrapling / Playwright |

## 坑
- **需要 LLM key**（OpenAI/Anthropic/本地 Ollama）。本机目前没有配 OpenAI/Anthropic key——要用云端就先去配，或走 Ollama。
- 依赖版本冲突：装它时把 click 降到 8.3.3，可能影响其他用 click>=8.4 的包；如遇 import 报错先查这里。
- 多步任务成本高、慢；能用单页抽取就别起 agent 循环。
