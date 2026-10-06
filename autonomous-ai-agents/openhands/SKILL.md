---
name: openhands
description: "本机完整版的 OpenHands / Agent Canvas（All-Hands-AI/OpenHands，90k★）：自托管的编码 agent 控制中心，跑 OpenHands/Claude Code/Codex/Gemini 及任何 ACP agent，支持本地/Docker/VM 后端与自动化。Use when the user wants to run coding agents on their own infrastructure or automate dev workflows."
---

# OpenHands Agent Canvas（本机完整版）

源码：`C:\Users\mwr_w\skills-repo\OpenHands`（2502 文件，32MB 浅克；git@81e8376）

## 是什么
- 自托管的"开发者控制中心"：对话式驱动编码 agent + 自动化（定时任务、GitHub issue 拆解、报告发 Slack）
- 默认本地跑，后端可接 Docker/VM/公司内网/OpenHands Cloud
- 内置开源 OpenHands agent，也能跑任何 ACP 协议第三方 agent

## 运行（Docker 最简）
```sh
export PROJECTS_PATH="$HOME/projects"   # agent 可访问的项目目录
mkdir -p "$PROJECTS_PATH" "$HOME/.openhands"
docker run -it --rm -p 127.0.0.1:8000:8000 \
  -e AGENT_CANVAS_ALLOW_LAN_SESSION_KEY=true \
  -v "$HOME/.openhands:/home/openhands/.openhands" \
  -v "${PROJECTS_PATH}:/projects" \
  ghcr.io/openhands/agent-canvas:1.25.0
# 浏览器开 http://127.0.0.1:8000
```
- Windows 等价命令见源码内 `README.windows.md`
- 本机源码可用于二次开发/读其 agent 架构（openhands 核心库在其 monorepo 中）

## 关键目录
- `frontend/` 控制面 UI，`docs/` 全部文档（SELF_HOSTING.md、backends 配置）
- 相关：ACP 协议规范（agent 互操作）可仿写自动化
