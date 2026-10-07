---
name: wxauto
description: 微信 3.9.X Windows 桌面自动化 (wxauto 库) — 发/收消息、传文件、会话列表、消息监听。Use when the user wants to automate WeChat Desktop on Windows (send/receive messages, file transfer, listen chats).
---

# wxauto — 微信桌面自动化

[cluic/wxauto](https://github.com/cluic/wxauto)（Apache-2.0）：基于 UIAutomation 操控 **Windows 版微信 3.9.X**。
包源码在本技能 `wxauto/` 目录（零构建，直接 import），已本机实测 `import wxauto` 通过（v3.9.11.17，Python 3.14）。

## 硬限制（先确认再动手）
- **只支持 Windows 版微信 3.9.X**（Mac/手机/其他大版本不行）
- 需要**微信进程在运行**；操作时别动鼠标键盘（UIAutomation 会抢占）
- 本机实测：库 import 级验证通过；完整发消息链路需微信在线时才能端到端验证

## 依赖（本机已装好）
```bash
pip install wxauto  # 或: pip install tenacity pywin32 pyperclip pillow psutil colorama comtypes uiautomation
```

## 核心 API（v3.9.11 实测签名）
```python
from wxauto import WeChat
wx = WeChat(language='cn')            # 也可 'en'/'cn_t'

wx.SendMsg("你好", who="张三")        # 发消息(会话名/群昵称)
wx.SendFiles(r"C:\x.png", who="张三") # 传文件
wx.AtAll(msg="开会了")                # 群里 @所有人
wx.ChatWith("张三")                   # 切到某会话
wx.GetSessionList()                  # 会话列表(含未读)
wx.GetAllMessage()                   # 当前会话全部消息
wx.CurrentChat()                     # 当前会话名
wx.GetAllFriends(keywords="张")       # 好友列表
wx.GetGroupMembers()                 # 当前群成员

# 监听: 注册后 GetListenMessage 轮询, 不是回调
wx.AddListenChat("张三")
msgs = wx.GetListenMessage("张三")    # 取出后自动清掉
wx.RemoveListenChat("张三")
```
`GetAllMessage` / `GetListenMessage` 返回 Message 对象：`msg.type`（text/image/file...）、`msg.content`、`msg.time`、`msg.sender`；图片类 `msg.save(filepath)` 可落盘。

## 示例脚本
- `scripts/send_msg.py` — 给指定会话发消息 + 传文件
- `scripts/listen_poll.py` — 轮询监听某会话新消息并落盘（后台监听模式）

运行前把 `scripts/` 的 sys.path 指向本技能目录即可：
```python
import sys; sys.path.insert(0, r"<skill_dir>")
```

## 踩坑
- `WeChat()` 初始化会**把微信主窗口拉到前台并刷新**（约 2s），别在这期间动鼠标
- 中文会话名要精确匹配；群消息用 `who="群名"`，@ 用 `at="昵称"`
- 旧文档（`references/README-upstream.md`）里的 `KeepRunning`/`msgs` 回调 API 是旧版，v3.9.11 已改为 `AddListenChat`+`GetListenMessage` 轮询模式——以本技能实测签名为准
