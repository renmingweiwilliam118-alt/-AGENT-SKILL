#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wechat_cua_probe.py — verify (and drive) WeChat through cua-driver's UIA tree.

Why this exists: bare `uiautomation` reads an EMPTY shell on WeChat 4.x
(Qt Quick, no per-control HWND), while cua-driver reads the full ~161-element
tree including the chat input, the session list and the message list.
This script is the measurement step that proves which case you are in before
any send code is written, and doubles as a minimal reference driver.

Usage:
    python wechat_cua_probe.py probe                 # read-only: tree + control map
    python wechat_cua_probe.py send "你好" 文件传输助手   # open session, send, verify
    python wechat_cua_probe.py messages               # dump current conversation

Requires: cua-driver on PATH (or RFLOW_CUA_DIR pointing at its directory).
Python 3.9+, stdlib only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time


def find_cua():
    env = os.environ.get("RFLOW_CUA_DIR")
    if env:
        p = os.path.join(env, "cua-driver.exe")
        if os.path.isfile(p):
            return p
    return shutil.which("cua-driver")


CUA = find_cua()

# Every subprocess needs this or a black console box flashes per call.
_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def call(tool, args, timeout=45):
    """Invoke `cua-driver call <tool> --args '<JSON>'`.

    Two traps handled here:
      1. stdout starts with a telemetry line -> extract the last balanced
         JSON span instead of parsing the whole stream.
      2. a refusal is ordinary-looking JSON -> surface it as _error so a
         caller can never mistake "refused" for "done".
    """
    cmd = [CUA, "call", tool, "--args", json.dumps(args, ensure_ascii=False)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace",
                       creationflags=_NOWIN)
    out = r.stdout or ""
    last, depth, start = None, 0, None
    for i, ch in enumerate(out):
        if ch in "{[":
            if depth == 0:
                start = i
            depth += 1
        elif ch in "}]":
            depth -= 1
            if depth == 0 and start is not None:
                last = out[start:i + 1]
    if not last:
        return {"_error": "no json in output: %s" % out[:200]}
    try:
        d = json.loads(last)
    except Exception:
        return {"_error": "unparseable json: %s" % last[:200]}
    if isinstance(d, dict) and d.get("status") == "refused":
        d["_error"] = (d.get("refusal") or {}).get("message") or "refused"
    return d


def ensure_daemon():
    """`call` hangs forever with no daemon; bootstrap one and wait for it."""
    for _ in range(2):
        st = subprocess.run([CUA, "status"], capture_output=True, text=True, timeout=10,
                            creationflags=_NOWIN)
        if "is running" in (st.stdout or ""):
            return True
        subprocess.Popen([CUA, "serve"], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         creationflags=_NOWIN)
        for _ in range(20):
            time.sleep(0.5)
            try:
                st = subprocess.run([CUA, "status"], capture_output=True, text=True, timeout=8,
                                    creationflags=_NOWIN)
                if "is running" in (st.stdout or ""):
                    return True
            except Exception:
                continue
    return False


def find_wechat():
    """-> (pid, window_id) for the WeChat main window, or None."""
    d = call("list_windows", {})
    wins = (d.get("windows") or d.get("structuredContent", {}).get("windows")
            or d.get("result", {}).get("windows") or [])
    for w in wins:
        s = json.dumps(w, ensure_ascii=False)
        if "Weixin" in s or "微信" in s:
            pid = w.get("pid") or w.get("process_id")
            wid = w.get("window_id") or w.get("id")
            if pid and wid:
                return int(pid), int(wid)
    return None


def elements(pid, wid):
    """Full element tree. Never pass `query` -- the projection deletes siblings."""
    d = call("get_window_state",
             {"pid": pid, "window_id": wid, "include_screenshot": False}, timeout=50)
    return (d.get("elements") or d.get("structuredContent", {}).get("elements")
            or d.get("result", {}).get("elements") or [])


def find_input(els):
    """The chat input: role=Edit with a wide frame.

    NOTE there is no `id` field -- the automation-id lives in `label`, and
    the input's own label is the CONTACT NAME. Width is what separates it
    from the small top-right search box.
    """
    for e in els:
        if (e.get("role") or "") == "Edit" and "chat_input_field" in (e.get("label") or ""):
            if (e.get("frame") or {}).get("w", 0) >= 200:
                return e
    edits = [e for e in els if (e.get("role") or "") == "Edit"]
    if not edits:
        return None
    return max(edits, key=lambda e: (e.get("frame") or {}).get("w", 0)
               * (e.get("frame") or {}).get("h", 0))


def message_items(els):
    """ListItems inside the message-list container (NOT the session list)."""
    box = None
    for e in els:
        lbl = e.get("label") or ""
        if "chat_message_list" in lbl or ((e.get("role") or "") == "List" and lbl == "消息"):
            box = e
            break
    if not box:
        return []
    return [e for e in els
            if (e.get("role") or "") == "ListItem"
            and e.get("element_index", 0) > box["element_index"]
            and e.get("depth", 0) > box.get("depth", 0)]


def open_session(pid, wid, name):
    """Click the session whose ListItem label starts with `name`."""
    els = elements(pid, wid)
    el = None
    for e in els:
        if (e.get("role") or "") == "ListItem" and (e.get("label") or "").strip().startswith(name):
            el = e
            break
    if not el:
        return False
    r = call("click", {"pid": pid, "element_token": el["element_token"]})
    time.sleep(0.4)
    return not r.get("_error")


def send(pid, wid, text, verify=True):
    """Verified send: set_value -> re-read (token goes stale) -> hotkey enter.

    verify=False skips the read-back (2 tree reads instead of 3, ~3.5 s
    instead of ~5 s) for latency-sensitive callers.
    """
    box = find_input(elements(pid, wid))
    if not box:
        return False, "no chat input found"
    # pass ONLY pid + element_token: the schema is additionalProperties:false
    # and extra ids must agree with the token or the call is refused
    r = call("set_value", {"pid": pid, "element_token": box["element_token"], "value": text})
    if r.get("_error"):
        return False, "set_value: " + r["_error"]
    time.sleep(0.15)
    # set_value mutates the tree -> the previous token is stale
    box2 = find_input(elements(pid, wid))
    if not box2:
        return False, "input vanished after set_value"
    r2 = call("hotkey", {"pid": pid, "element_token": box2["element_token"],
                          "keys": ["enter"]})
    if r2.get("_error"):
        return False, "hotkey: " + r2["_error"]
    if not verify:
        return True, "sent (no read-back)"
    time.sleep(0.6)
    els = elements(pid, wid)
    fp = text.strip()[:20]
    if any(fp in (e.get("label") or "") for e in message_items(els)):
        return True, "message confirmed in message list"
    box3 = find_input(els)
    if box3 and not (box3.get("value") or "").strip():
        return True, "input cleared (send-side confirmation)"
    return False, "not confirmed: message absent and input not cleared"


def main():
    if not CUA:
        print("cua-driver not found (set RFLOW_CUA_DIR)")
        return 2
    if not ensure_daemon():
        print("cua-driver daemon would not start")
        return 2
    loc = find_wechat()
    if not loc:
        print("WeChat window not found -- is it running and logged in?")
        return 2
    pid, wid = loc
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"

    if mode == "probe":
        els = elements(pid, wid)
        print("pid=%s window_id=%s elements=%d" % (pid, wid, len(els)))
        box = find_input(els)
        print("chat input : %s" % ("#%s token=%s value=%r" % (
            box["element_index"], box.get("element_token"), (box.get("value") or "")[:40])
            if box else "NOT FOUND (bare-UIA shell or unsupported build)"))
        sess = [e for e in els if (e.get("role") or "") == "ListItem"
                and "session_item" in json.dumps(e, ensure_ascii=False)]
        print("sessions   : %d" % len(sess))
        msgs = message_items(els)
        print("messages   : %d" % len(msgs))
        for m in msgs[-5:]:
            print("   ", repr((m.get("label") or "")[:60]))
        return 0 if box else 1

    if mode == "messages":
        for m in message_items(elements(pid, wid)):
            print(repr((m.get("label") or "")[:80]))
        return 0

    if mode == "send":
        text = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) > 3 else None
        if name:
            print("open_session %r: %s" % (name, open_session(pid, wid, name)))
        ok, note = send(pid, wid, text)
        print("send: %s | %s" % ("OK" if ok else "FAIL", note))
        return 0 if ok else 1

    print("usage: wechat_cua_probe.py [probe|messages|send TEXT [SESSION]]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
