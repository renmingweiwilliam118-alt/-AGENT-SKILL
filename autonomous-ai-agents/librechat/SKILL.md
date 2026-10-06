---
name: librechat
description: "本机完整版的 LibreChat（LibreChat-AI，45k★）：增强版 ChatGPT 开源平台，多模型/多 provider、Agents、MCP、Skills、代码执行 workspace、OIDC 部署。Use when the user wants to self-host a multi-model chat + agent platform or study its agent/skill architecture."
---

# LibreChat（本机完整版）

源码：`C:\Users\mwr_w\skills-repo\LibreChat`（111MB，git@e1dfc10，v0.8.x）

## 是什么
- 自托管聊天平台：OpenAI/Anthropic/AWS/DeepSeek/Gemini 等多 provider 统一前端
- v0.8.8 重点能力：**Agent 管理 API**（CRUD agent、agent 文件与 Skills、OIDC 机器身份）、**附加工作区**（agent 可查树/读文件/执行 Bash，有界超时）、代码审批（Ask/Allow/Deny/Full access）、手动上下文压缩
- 支持 MCP、Skills、浏览器工具、子 agent

## 运行（Docker 官方模板最简）
```sh
cd C:\Users\mwr_w\skills-repo\LibreChat
docker compose up -d   # 用其 docker 模板（含 PostgreSQL）
# 或开发模式：client/ 用 pnpm，server/ 用 npm
```
- 生产部署需配 `.env`（各 provider key、OIDC）；Railway/Zeabur 一键模板见 README

## 关键目录
- `api/` 核心后端（agents/skills/tools 子系统在这里，值得精读做参考架构）
- `client/` 前端，`middleware/` 反向代理
