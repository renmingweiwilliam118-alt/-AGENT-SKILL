---
name: moneyprinterturbo
description: "本机完整版的一键 AI 短视频生成器（harry0703/MoneyPrinterTurbo，128k★）：给主题/关键词自动生成脚本、匹配素材、字幕、背景音乐并合成高清短视频，带 WebUI 和 API。Use when the user wants to batch-generate short videos from topics or keywords."
---

# MoneyPrinterTurbo（本机完整版）

源码：`C:\Users\mwr_w\skills-repo\MoneyPrinterTurbo`（346 文件，338MB，git@68eb5a6，含 .git 可增量更新）

## 能干什么
- 输入主题/关键词 → 自动写视频脚本（LLM）→ 搜素材（Pexels 等）→ 生成字幕（whisper）+ 背景音乐 → ffmpeg 合成高清短视频
- WebUI（Streamlit）+ 本地 API 两种用法
- 支持 LLM/TTS/素材源可换（OpenAI、Google、阿里、Kimi 等）

## 运行（Python 3.11+，项目根目录）
```powershell
# Windows 一键（先装依赖）
cd C:\Users\mwr_w\skills-repo\MoneyPrinterTurbo
pip install -r requirements.txt   # 或 uv sync --frozen
.\webui.bat                      # 起 WebUI
```
- 依赖：`.env` 里配 LLM API Key（openai 或 google 至少一个）；whisper 模型可选装
- 硬件建议：CPU 4 核 8GB 即可跑（主要用云端 LLM/TTS）

## 关键目录
- `core/` 主流程，`app/` WebUI/API 入口，`utils/` 素材/字幕/音频
- `docs/` 官方 Skill 文档（可喂给别的 agent 一键安装运行）
