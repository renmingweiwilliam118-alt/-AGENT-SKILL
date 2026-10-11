# WeChat Automation Control Tree Reference

## WeChat 4.x Window Structure

Main window class: `mmui::MainWindow` (after cua-driver reads the tree).
Without cua-driver, standard UIAutomation sees only `Qt51514QWindowIcon`
with 1 empty PaneControl.

## Key Elements (element_index may vary)

| Role | Label/ID | Purpose |
|------|----------|---------|
| Edit | label contains `chat_input_field` | Message input box (large frame, ~437×98) |
| Button | label exactly `发送` | Send button (NOT `发送表情`, `发送收藏`, `发送文件`) |
| ListItem | label starts with contact name | Session list item |
| List | label `消息` or id `chat_message_list` | Message history container |
| ListItem | inside message list | Individual message bubbles |

## Finding the Input Box

```python
# Method 1: by label
box = find_element(els, role="Edit", label="chat_input_field", min_w=200)

# Method 2: largest Edit control (fallback)
edits = [e for e in els if e.get("role") == "Edit"]
box = max(edits, key=lambda e: e["frame"]["w"] * e["frame"]["h"])
```

## Finding the Send Button

```python
# Must match label EXACTLY "发送" — substring match hits wrong buttons
btn = None
for e in els:
    if e.get("role") == "Button" and (e.get("label") or "").strip() == "发送":
        btn = e
        break
```

## Reading Messages

```python
# Find message list container, then collect ListItems inside it
container = find_element(els, label="chat_message_list")
# or: role="List" and label="消息"

cidx = container["element_index"]
cdepth = container.get("depth", 0)
messages = []
for e in els:
    if (e.get("role") == "ListItem"
        and e.get("element_index", 0) > cidx
        and e.get("depth", 0) > cdepth):
        messages.append(e.get("label") or e.get("value") or "")
```

## Verifying Send Success

After sending, check two conditions:
1. Message list contains the sent text (as a ListItem label)
2. Input box value is now empty (WeChat clears it after send)

```python
def verify_sent(text, wait=1.5):
    time.sleep(wait)
    els = get_elements(pid, wid)
    fp = text.strip()[:20]
    # Check message list
    for e in msg_list_items(els):
        if fp in (e.get("label") or ""):
            return True
    # Check input box cleared
    box = find_input_box(els)
    if box and not (box.get("value") or "").strip():
        return True  # cleared = likely sent
    return False
```

## Switching Sessions

```python
def open_session(name):
    els = get_elements(pid, wid)
    for e in els:
        if (e.get("role") == "ListItem"
            and (e.get("label") or "").strip().startswith(name)):
            click_element(pid, e)
            time.sleep(0.4)
            return True
    return False
```

**Prerequisite: restore the window before switching.** If WeChat is
minimized, the click is refused with `window_minimized` (the session item
resolves to the iconic sentinel, off every display). Call
`bring_to_front {pid, window_id}` (it reports `raised`/`restored`), sleep
~0.25s, then click. Check `effect == "refused"` in the click response.

## Enumerating & Auto-Switching All Sessions (multi-contact mode)

To auto-reply across multiple contacts: scan the left session list, find
unread chats, switch to each, read, reply, move to the next. Session
ListItems live in the LEFT panel (frame.x ≈ 1001); message ListItems live
in the RIGHT panel (frame.x ≈ 1301) — separate them by x-coordinate, never
by element_index alone.

```python
def list_sessions(self):
    els = self._els()
    out = []
    for e in els:
        if (e.get("role") or "") != "ListItem":
            continue
        if (e.get("frame") or {}).get("x", 0) > 1100:
            continue  # right panel = message bubbles, not sessions
        lab = (e.get("label") or "").strip()
        name = lab.split("\n", 1)[0].strip()   # first line = contact name
        if not name:
            continue
        # unread count is in the label as [N条] / [N]
        un = 0
        m = re.search(r"[\[（](\d+)\s*条?[\]）]", lab)
        if m:
            un = int(m.group(1))
        out.append({"name": name, "unread": un,
                    "selected": bool(e.get("selected")), "el": e})
    return out

# Process only unread, skipping service accounts:
SKIP = {"腾讯新闻", "公众号", "微信游戏", "微信支付", "订阅号"}
```

**Key facts:**
- `selected: True` on the session element marks the currently-open chat.
- Unread badge is text inside the session label (`[N条]`), NOT a separate
  element field — parse it from the label with a regex.
- Session labels are multi-line: `name\npreview\ntime\n[免打扰]`. Take the
  first line for the name.
- Skip service/official accounts (news, public accounts, games, payment)
  — auto-replying to them is nonsense; keep a name-based skip list.
- Dedup per session: keep `{session_name: set(normalized_keys)}` of already
  replied messages so a re-scan of the same chat doesn't double-reply.
- Reuse ONE connected bridge instance across the whole loop (connect once,
  then open_session/read_messages/send per contact) — reconnecting per
  contact is slow and fragile.

## Known Limitations

- Control tree indices change on every `get_window_state` call
- `element_token` becomes stale after any state change
- Background click on buttons often no-ops; use Enter key for send
- WeChat must be running and logged in
- Session must be open (input box only exists when a chat is active)
- cua-driver reads ~161 elements; raw uiautomation reads only ~51 (no input box)
- Clicks on a minimized window are refused (`window_minimized`) — restore
  with `bring_to_front` first
