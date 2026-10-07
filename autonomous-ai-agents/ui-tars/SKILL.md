---
name: ui-tars
description: UI-TARS GUI agent — drive mouse/keyboard on a desktop via a vision LLM (HuggingFace/vLLM endpoint). Use when asked to automate a desktop app, click through a GUI, or run a "look at the screen, think, act" loop with UI-TARS-1.5.
---

# UI-TARS Desktop GUI Agent

字节跳动 UI-TARS（开源 7B 视觉 agent 模型）的桌面执行层。本技能 = 上游动作解析器（`ui_tars/`，零依赖）+ agent 循环脚本（`scripts/ui_tars_agent.py`）+ pyautogui 执行器。

## 它做什么
1. 截屏（mss，主显示器）
2. 把 任务 + 历史 Thought/Action + 当前截图 发给一个 **OpenAI 兼容视觉端点**
3. 用 `ui_tars.action_parser.parse_action_to_structure_output()` 解析模型输出（`Thought:...\nAction: click(start_box='(x,y)')` 等）
4. 用 pyautogui 真实执行（点击/双击/右键/拖拽/滚动/打字/组合键/等待/完成）
5. 循环到 `finished` 或步数用尽

## 前置依赖（本机已装, 若换机重装）
```bash
pip install pyautogui pillow mss openai pyperclip
```

## 推理端点（关键）
本技能**不含模型权重**。UI-TARS-1.5-7B 需 ~14GB 显存（fp16），本机 1050 Ti 4GB 跑不动，必须用远程端点：
- **HuggingFace Inference Endpoint**（官方推荐, 付费）：按 `references/deploy.md` 部署 `UI-TARS-1.5-7B`，TGI 容器 `ghcr.io/huggingface/text-generation-inference:3.2.1`，环境变量 `CUDA_GRAPHS=0`、`PAYLOAD_LIMIT=8000000`；然后 `--base-url https://<endpoint> --api-key hf_... --model tgi`
- **本地 vLLM / SGLang**（有 ≥24GB 显存的机器）：加载 `ByteDance-Seed/UI-TARS-1.5-7B`，`--base-url http://host:port/v1 --api-key x --model vllm`
- 任何 OpenAI 兼容视觉端点均可（模型须会输出 UI-TARS 的 Thought/Action 格式）。

坐标处理：Qwen2.5-VL 系输出**绝对坐标**（0–1000 尺度），`parse_action_to_structure_output(model_type="qwen25vl")` 内部 `smart_resize` + 比例换算回真实屏幕像素。详见 `references/coordinates.md`。

## 运行
```bash
cd <skill_dir>
python scripts/ui_tars_agent.py "在记事本里新建文件并输入 hello 并保存" \
  --steps 12 \
  --base-url https://xxx.hf.space --api-key hf_xxx --model tgi
```
每步打印 `[thought][action]` 与执行结果。
**安全**：`pyautogui.FAILSAFE=True` —— 执行中把鼠标甩到屏幕左上角即刻中止。

## 文件
- `ui_tars/action_parser.py` / `prompt.py` — 上游 Bytedance 源码（Apache-2.0，见 `LICENSE`）
- `scripts/ui_tars_agent.py` — agent 循环（本技能新增）
- `references/coordinates.md` / `deploy.md` — 上游坐标与部署文档
- `tests` — 上游单元测试（`action_parser_test.py`）

## 何时不用它
- 已有 cua-driver / `computer_use` 工具且无需视觉模型决策 → 直接用它，不必绕 UI-TARS
- 纯浏览器任务 → `browser_use` / Playwright 更快更稳
- 没有可用视觉推理端点（无 HF 端点、无大显存机、无 API）→ 本技能无法运行，先解决端点
