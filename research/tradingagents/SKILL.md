---
name: tradingagents
description: "本机完整版的多智能体金融交易框架（TauricResearch/TradingAgents，110k★，arXiv:2412.20138）：分析师/研究员/交易员/风控多 agent 协作出交易决策，支持回测、SEC EDGAR、点-in-time 数据完整性。Use when the user wants LLM-driven equity analysis, trading decisions, or backtesting."
---

# TradingAgents（本机完整版）

源码：`C:\Users\mwr_w\skills-repo\TradingAgents`（238 文件，8.9MB，git@1394a3f，v0.6.0）

## 架构
- 多 agent 分工：市场/舆情/新闻/基本面分析师 → 研究员多空辩论 → 交易员 → 风控经理 → 组合经理
- 每层可配不同模型；决策报告存为单 HTML；支持 CLI 免交互（`--ticker` `--date`）；回测只见"当时已发布"的数据（无未来函数）
- 数据源：Yahoo、SEC EDGAR（按申报原样）、FRED 宏观、社媒情绪（可选 Jev 筛选）

## 运行（Python 3.13）
```bash
cd C:\Users\mwr_w\skills-repo\TradingAgents
uv venv --python 3.13 && source .venv/Scripts/activate  # Windows
pip install .
# .env 配 LLM/API key 后：
python main.py --ticker AAPL --date 2026-10-05   # 或 docker compose run --rm tradingagents
```
- 报告/记忆/缓存在 `tradingagents_data` 卷（宿主目录可挂载）

## 关键目录
- `tradingagents/` 包本体（按模块分包：models、agents、flows、data、graph）
- 多 provider 支持：OpenAI/Anthropic/Google 等，默认 GPT-6 Sol/Luna（见 CHANGELOG）
