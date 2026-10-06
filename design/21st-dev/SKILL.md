---
name: 21st-dev
description: 21st.dev 在线 UI 目录操作技能：搜索 1.2 万+ 真实设计工程做的 React/Tailwind/shadcn 组件、模板、主题，取码进项目；或 AI 生成新 UI；或搜品牌 logo（JSX）。做落地页/组件需要"有品味的人写过的 UI"时优先查这里，比从零生成强。需要免费 API key（21st.dev/mcp 即时申请），走 HTTP MCP 或 curl。
---

# 21st.dev（在线 UI 目录 + AI 生成）

**21st.dev**：12,000+ 由真人设计工程师发布的 React + Tailwind + shadcn/ui 组件、完整模板、主题、shader、渐变。理念是"从真实 UI 起步，而不是 AI 平均值"。
官方 agent 文档（已下载存档）：`C:\Users\mwr_w\skills-repo\21st\`（`official-21st-ui-skill.md` = 官方 skill 全文、`llms-install.md` = MCP 安装指南、`README-magic-mcp.md`）。

## 接入方式（二选一）

**A. HTTP MCP（推荐，任何支持 MCP 的 agent）**
```json
{ "mcpServers": { "21st": { "url": "https://21st.dev/api/mcp", "headers": { "x-api-key": "YOUR_KEY" } } } }
```
**B. 没有 MCP 时直接 curl（Hermes 默认路径）**
```bash
# 搜索组件
curl -s -X POST https://21st.dev/api/mcp ... # 或走 stdio 代理
# 更简单：npx -y @21st-dev/magic@latest API_KEY="..."（官方兼容代理，stdio 转发到 21st MCP）
```

**API key**：`https://21st.dev/mcp` 免费即时申请（旧 Magic console 的 key 已作废，必须重新申请）。环境变量名 `API_KEY_21ST`。

> **本机已配置**：key 存在 `C:\Users\mwr_w\.21st\api-key`（权限 600，不在任何 git 仓库里），并已 `setx API_KEY_21ST`（用户级环境变量，新终端/新会话生效）。取 key：`cat /c/Users/mwr_w/.21st/api-key`。验证通过：`tools/list` 返回 34 个工具。

## 核心工具（已验证：该 key 实际返回 34 个工具，列常用）

| 工具 | 用途 |
|------|------|
| `search` | 自然语言搜组件/模板/主题/shader/渐变（"pricing table"、"animated hero"），返回名称+预览+安装 id |
| `search_picker` | 同 `search`，但在支持内嵌 UI 的客户端渲染选择器 |
| `get_component` | 取所选组件完整代码 + demo + 安装说明 |
| `get_theme` | 取主题完整 CSS（:root/.dark token，直接塞进 Tailwind） |
| `get_inspiration` | 设计灵感候选（元数据 rerank，适合先看看再定方向） |
| `generate` | AI 从描述生成新 UI（消耗 credit；需账号开启 AI，先查 `get_usage.aiGenerationEnabled`） |
| `get_generation` / `get_take` / `get_generation_job` | 读/取/轮询 AI 草稿的 take（`get_generation_job` 免费） |
| `search_logo` | 品牌/UI SVG logo（开库，如 'discord'、'nextjs'），返回可粘 JSX，一次一个品牌 |
| `bookmark` / `list_bookmarks` / 团队库系列 | 收藏 + 团队共享库管理 |
| `get_usage` | 查取码档位/配额 + AI 是否开启 |
| `submit_component` / `edit_*` / `delete_*` / `get_profile` 等 | 发布/管理自己的组件、主题、模板、bento 主页 |

**验证方式**（key 有效 + 工具全开）：node 脚本走 MCP 流式 HTTP 握手 initialize → tools/list，返回 34 工具。curl 直连/代理打 21st.dev 会被 Cloudflare TLS 指纹挡死（http=000），必须用 node fetch 或官方代理。

## 标准工作流

1. 用户要 UI（"加个定价区"、"做个 testimonial 块"）→ 先 `search` 查现成的，**不要直接手写**
2. 挑 1-3 个最贴合用户风格的候选给用户看预览
3. `get_component` 取码 → 按返回的安装说明进项目（shadcn registry add 或直接写文件）
4. 适配项目的设计 token（`cn` helper、Tailwind 配置、组件目录约定）
5. 目录里没有合适的才走 `generate`（确认 `aiGenerationEnabled`；off 就用 search+get_component 拿参考再自己实现，别重试 `ai_subscription_required`）

## 额度注意

- 免费档：目录搜索不限次 + 每天 2 次组件安装；付费组件要解锁后 `get_component` 才给代码
- `generate` 单独计 AI credit；`get_usage` 的 flag 只表示"有没有权限"，不是余额

## 与其他 UI 素材库的分工

| 场景 | 用 |
|------|----|
| 要"有品味真人做的" React 组件/完整模板（在线取码） | **21st.dev（本技能）** |
| 本地离线素材（零依赖按钮/loader/卡片 3802 个） | uiverse-galaxy |
| React 动画组件（framer-motion 级，本地 copy-paste） | react-bits / magic-ui |
| 3D 背景 | threeui / shadergradient |

## 坑

- 21st.dev 页面直连 curl 常被重置（Cloudflare）；API key 和 MCP 端点走 `https://21st.dev/api/mcp`，代理 `http://127.0.0.1:10808` 或直连试
- 取码前确认项目有 shadcn/ui + Tailwind（21st 组件默认吃这两者 + 设计 token）；纯 CSS 项目找 uiverse-galaxy 的 CSS 段
- `search_logo` 一次只能查一个品牌
- 官方 skill 原文在素材库 `official-21st-ui-skill.md`，细节以它为准
