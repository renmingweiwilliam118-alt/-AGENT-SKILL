#!/usr/bin/env python3
"""wxauto 示例: 给指定会话发消息 + 传文件。

用法:
    把本技能目录加入 sys.path (或 pip install wxauto), 微信 3.9.X 处于运行状态。
    python send_msg.py "张三" "你好" [文件路径...]

安全: 初始化 WeChat() 会把微信拉到前台约 2 秒, 期间勿动鼠标。
"""
import sys, os, glob

# ---- 把本技能的 wxauto 包指进路径 (相对脚本所在目录的上上级) ----
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_DIR)

from wxauto import WeChat  # noqa: E402


def main():
    if len(sys.argv) < 3:
        print('用法: python send_msg.py <会话名> <消息文本> [文件路径...]')
        return 1
    who, msg = sys.argv[1], sys.argv[2]
    files = sys.argv[3:]

    print(f"初始化 WeChat (主窗口会拉到前台 ~2s, 勿动鼠标) ...")
    wx = WeChat(language="cn")

    # 切到目标会话, 发送文本
    wx.ChatWith(who)
    wx.SendMsg(msg, who=who)
    print(f"已发送文本: {msg!r} -> {who}")

    # 逐个发文件
    for f in files:
        for p in glob.glob(f):  # 支持通配符
            wx.SendFiles(p, who=who)
            print(f"已发文件: {p} -> {who}")

    print("完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
