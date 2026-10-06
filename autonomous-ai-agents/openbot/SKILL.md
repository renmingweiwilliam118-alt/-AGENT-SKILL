---
name: openbot
description: "本机完整版的 OpenBot（CopilotKit，6k★，alpha）：开源 AI 同事平台，每个 agent 有独立浏览器/文件/工具，AG-UI 协议接入任意 agent 框架，Docker Compose 自托管。Use when the user wants to build company-owned AI coworkers or integrate an AG-UI agent stack."
---

# OpenBot（本机完整版）

源码：`C:\Users\mwr_w\skills-repo\OpenBot`（git@f4bc60b，alpha，MIT）

## 是什么
- "AI 同事"平台：每个 agent  coworker 有自己的浏览器（独立登录态）、文件、工具白名单；动作先审后记
- 任意 AG-UI agent 进来就是一个 coworker；回复可以是组件而非纯文本
- 模板性质：clone 后把 `examples/` 换成自己的 coworkers/channels/skills 即成私有部署

## 运行
```sh
cd C:\Users\mwr_w\skills-repo\OpenBot
# .env.example 带 OPENBOT_SINGLE_USER=true（单管理员模式，开箱即跑）
# docker compose 起全部组件（PostgreSQL 数据自持）
```
- 已内置 15 个 agent 框架适配：`agent-adk`（Google ADK）、`agent-crewai`、`agent-langgraph`、`agent-pydantic-ai`、`agent-computer`、`agent-claude-sdk` 等（见顶层目录）

## 关键目录
- `agent-*` 各框架接入示例（读它知道怎么把自己的 agent 栈接进 OpenBot）
- `examples/` 示例租户包，`docs/` 完整文档（sign-in/OAuth、Intelligence 本地跑法）
