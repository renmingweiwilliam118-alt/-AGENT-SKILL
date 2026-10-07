#!/usr/bin/env python3
"""UI-TARS 本地 GUI agent 循环。

截屏 -> 调视觉大模型端点 -> 解析 UI-TARS 动作 -> pyautogui 执行 -> 循环。

需要: 一个 OpenAI 兼容的视觉推理端点 (HuggingFace TGI 端点 / vLLM / 任意)。
      本机 GPU 显存不足 (如 1050 Ti 4GB) 时, 请指向远程端点。

环境变量 (或用 CLI 参数覆盖):
  UI_TARS_BASE_URL  端点 base_url, 如 https://xxx.hf.space 或 http://host:port/v1
  UI_TARS_API_KEY   API key (HF 端点填 hf_...; 本地 vLLM 随便填非空串)
  UI_TARS_MODEL     模型名, HF TGI 默认 "tgi"

运行示例:
  python ui_tars_agent.py "在记事本里新建文件并输入 hello" --steps 12
  python ui_tars_agent.py "打开浏览器搜索 Windows 更新" --base-url http://127.0.0.1:8000/v1 --api-key x --model vllm

安全:
  pyautogui.FAILSAFE=True —— 执行中把鼠标甩到屏幕左上角即可紧急中止。
  每步会打印 [thought][action] 与执行结果, 全程可视。
"""
import os, sys, base64, time, argparse, textwrap

# ---- 让脚本能 import 同级 ../ui_tars 解析层 ----
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_DIR)

from ui_tars.action_parser import parse_action_to_structure_output  # noqa: E402
from ui_tars.prompt import COMPUTER_USE_DOUBAO                      # noqa: E402

try:
    import pyautogui
    from PIL import Image
    from io import BytesIO
except ImportError as e:  # pragma: no cover
    sys.exit(f"缺少依赖: {e.name}。先跑  pip install pyautogui pillow mss openai")

pyautogui.FAILSAFE = True       # 甩鼠标到左上角中止
pyautogui.PAUSE = 0.15          # 每个动作间的微停顿

import mss                                                              # noqa: E402

# ---------------- 截屏 ----------------
def grab_screen() -> Image.Image:
    with mss.mss() as sct:
        mon = sct.monitors[1]            # 主显示器
        raw = sct.grab(mon)
        img = Image.frombytes("RGB", raw.size, raw.data, "raw", "BGRX")
    return img, (mon["width"], mon["height"])

# ---------------- 构建对话 ----------------
def build_messages(instruction: str, history, screenshot_b64: str):
    """UI-TARS 的 observation 风格: 每轮 Thought/Action + 新截图。"""
    prompt = COMPUTER_USE_DOUBAO.format(language="中文", instruction=instruction)
    messages = [{"role": "system", "content": prompt}]
    user_content = []
    # 历史轮 (每轮: 该轮截图 + 模型上一动作文本)
    for hist in history:
        if hist.get("img_b64"):
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{hist['img_b64']}"}
            })
        user_content.append({"type": "text", "text": f"上一动作: {hist['action_text']}"})
    # 当前轮截图
    user_content.append({
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{screenshot_b64}"}
    })
    user_content.append({"type": "text", "text": "现在请给出下一步动作 (Thought + Action)。"})
    messages.append({"role": "user", "content": user_content})
    return messages

def b64_jpeg(img: Image.Image, quality: int = 85) -> str:
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()

# ---------------- 执行解析后的动作 ----------------
def exec_parsed(parsed, w, h):
    """把 ui_tars 解析出的结构化动作直接执行 (比 eval 上游生成的代码更可控)。"""
    done = False
    for a in parsed:
        t = a.get("action_type")
        inp = a.get("action_inputs", {})
        def box(cx, cy=None):
            b = inp.get(cx)
            if not b:
                return None
            nums = [float(x) for x in b.replace("[", "").replace("]", "").replace("(", "").replace(")", "").split() if x]
            x1, y1 = nums[0], nums[1]
            x2, y2 = (nums[2], nums[3]) if len(nums) >= 4 else (x1, y1)
            return (round((x1 + x2) / 2 * w), round((y1 + y2) / 2 * h))
        if t in ("click", "left_single"):
            c = box("start_box") or box("end_box")
            if c: pyautogui.click(c[0], c[1]); print(f"    click {c}")
        elif t == "left_double":
            c = box("start_box"); c and pyautogui.doubleClick(c[0], c[1])
        elif t == "right_single":
            c = box("start_box"); c and pyautogui.click(c[0], c[1], button="right")
        elif t == "drag":
            s, e = box("start_box"), box("end_box")
            if s and e: pyautogui.moveTo(*s); pyautogui.dragTo(*e, duration=0.6)
        elif t == "scroll":
            c = box("start_box")
            d = str(inp.get("direction", "down")).lower()
            amt = -5 if "down" in d else 5
            pyautogui.scroll(amt, c[0] if c else None, c[1] if c else None)
        elif t == "type":
            content = inp.get("content", "")
            enter = content.endswith("\\n") or content.endswith("\n")
            content = content.rstrip("\\n").rstrip("\n")
            if content:
                try:
                    import pyperclip
                    pyperclip.copy(content); pyautogui.hotkey("ctrl", "v"); time.sleep(0.3)
                except ImportError:
                    pyautogui.write(content, interval=0.05)
            if enter: pyautogui.press("enter")
        elif t in ("hotkey",):
            keys = str(inp.get("key") or inp.get("hotkey", "")).split()
            if keys: pyautogui.hotkey(*keys)
        elif t in ("press", "keydown", "keyup"):
            k = inp.get("key", "")
            pyautogui.press(k) if t == "press" else (pyautogui.keyDown(k) if t == "keydown" else pyautogui.keyUp(k))
        elif t == "wait":
            time.sleep(2); print("    wait")
        elif t in ("finished", "done"):
            print(f"    FINISHED: {inp.get('content', a.get('thought',''))}")
            done = True
            break
    return done

# ---------------- 主循环 ----------------
def run(instruction, base_url, api_key, model, max_steps, verbose=True):
    from openai import OpenAI
    if not base_url:
        sys.exit("未提供推理端点。设 UI_TARS_BASE_URL 或用 --base-url。本机 4GB 显存跑不动 7B, 建议远程端点。")
    client = OpenAI(base_url=base_url, api_key=api_key or "EMPTY")
    img, (w, h) = grab_screen()
    if verbose: print(f"[init] 屏幕 {w}x{h}  端点 {base_url}  模型 {model}")
    history = []
    for i in range(1, max_steps + 1):
        b64 = b64_jpeg(img)
        msgs = build_messages(instruction, history, b64)
        try:
            resp = client.chat.completions.create(
                model=model, messages=msgs,
                temperature=0.0, top_p=None, max_tokens=512,
            )
            raw = resp.choices[0].message.content or ""
        except Exception as e:
            print(f"[step {i}] 模型调用失败: {e}")
            raise
        if verbose:
            print(f"\n=== step {i} ===")
            print(textwrap.indent(raw.strip()[:400], "    "))
        parsed = parse_action_to_structure_output(
            raw, factor=1000,
            origin_resized_height=h, origin_resized_width=w,
            model_type="qwen25vl",
        )
        done = exec_parsed(parsed, w, h)
        history.append({"img_b64": b64, "action_text": raw.strip()})
        if done:
            print(f"\n[完成] 任务结束于 step {i}")
            return
        time.sleep(0.8)
        img, (w, h) = grab_screen()
    print(f"\n[停止] 达到 max_steps={max_steps}")

def main():
    p = argparse.ArgumentParser(description="UI-TARS 本地 GUI agent")
    p.add_argument("task", help="自然语言任务, 如 '打开记事本并输入 hello'")
    p.add_argument("--steps", type=int, default=12, help="最大步数 (默认 12)")
    p.add_argument("--base-url", default=os.getenv("UI_TARS_BASE_URL"))
    p.add_argument("--api-key", default=os.getenv("UI_TARS_API_KEY"))
    p.add_argument("--model", default=os.getenv("UI_TARS_MODEL", "tgi"))
    p.add_argument("--quiet", action="store_true", help="不打印每步思考")
    a = p.parse_args()
    run(a.task, a.base_url, a.api_key, a.model, a.steps, verbose=not a.quiet)

if __name__ == "__main__":
    main()
