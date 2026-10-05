---
name: scrcpy
description: Mirror and control an Android device (video+audio) from the computer via USB/TCP without installing anything on the phone — Genymobile scrcpy (Windows prebuilt available). Use when the user wants to mirror/drive an Android phone from the PC, record the screen, or use the phone as an input source. Requires a physical Android device + ADB; NOT something to run headless.
license: MIT (scrcpy)
---

# scrcpy

Display & control an **Android device** from a computer (USB or TCP/IP). No root, no app on the phone. Light, low-latency (35–70ms), 30–120fps.

## 本机情况
- 这是**设备/二进制工具**，不是 Python/Node 库：需要 ① 一台 Android 手机连 USB ② Android 开 USB 调试 ③ ADB。
- Windows 上下载预构建包（`scrcpy-win64-v4.x.7z`）从官方 release 解压，`scrcpy.exe` 直接跑。
- 常见命令：`scrcpy`（镜像+控制）、`scrcpy --record screen.mp4`、`scrcpy --no-control`（只看）。

## 什么时候用哪个
| 需求 | 选 |
|---|---|
| 把安卓手机投到电脑/用键鼠控 | **scrcpy** |
| 没有实体 Android 设备 | 用不了（scrcpy 必须有真机） |
| 自动化安卓 App | 用 ADB / uiautomator2 更合适 |

## 坑
- 小米等机型需额外开「USB 调试(安全设置)」才能注入按键。
- 音频转发要 Android 11+。
- 只认官方仓库的 release；第三方"scrcpy"下载有风险。
