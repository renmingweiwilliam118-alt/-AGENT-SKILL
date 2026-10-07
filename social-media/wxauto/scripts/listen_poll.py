#!/usr/bin/env python3
"""wxauto 示例: 轮询监听某会话的新消息, 文本落盘, 图片/文件可另存。

用法:
    python listen_poll.py "张三" [--out msgs.txt] [--poll 3]

说明:
    - 先把目标会话 AddListenChat 注册为监听对象
    - 每 poll 秒取一次 GetListenMessage, 打印并追加到输出文件
    - Ctrl+C 退出; 退出时自动 RemoveListenChat
"""
import sys, os, time, argparse

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_DIR)

from wxauto import WeChat  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("who", help="要监听的会话名/群名")
    ap.add_argument("--out", default="wxauto_msgs.txt")
    ap.add_argument("--poll", type=float, default=3.0, help="轮询间隔秒")
    a = ap.parse_args()

    wx = WeChat(language="cn")
    wx.AddListenChat(a.who)
    print(f"已监听 {a.who!r}, 每 {a.poll}s 取一次消息 (Ctrl+C 退出)")

    try:
        while True:
            msgs = wx.GetListenMessage(a.who)
            for m in msgs:
                line = f"[{m.time}] {m.sender}: {m.content}"
                print(line)
                with open(a.out, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            time.sleep(a.poll)
    except KeyboardInterrupt:
        print("\n退出")
    finally:
        wx.RemoveListenChat(a.who)
    return 0


if __name__ == "__main__":
    sys.exit(main())
