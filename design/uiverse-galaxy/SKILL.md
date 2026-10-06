---
name: uiverse-galaxy
description: 3802 个零依赖 UI 组件素材库（uiverse-io/galaxy，UIVerse，MIT，13k star）。按钮/卡片/加载器/表单/开关等，每个 HTML 文件同时含 CSS 版和 Tailwind 版两段代码，copy-paste 即用。做 UI 需要现成按钮、卡片、loader、checkbox 等静态/微交互控件时，先查这里海量备选，不用从零写 CSS。
license: MIT
---

# UIVerse Galaxy 组件素材库

来源：[uiverse-io/galaxy](https://github.com/uiverse-io/galaxy)（MIT，社区投稿）。
素材已下载：`C:\Users\mwr_w\skills-repo\uiverse-galaxy\`（11 个分类目录，3802 个 HTML 组件文件，约 10MB），清单见 `skills-repo\uiverse-galaxy\_components.md`。

## 分类与数量

| 分类 | 数量 |
|---|---|
| Buttons | 1231 |
| Cards | 726 |
| loaders（加载器） | 718 |
| Toggle-switches | 260 |
| Inputs | 226 |
| Forms | 180 |
| Checkboxes | 171 |
| Patterns | 103 |
| Radio-buttons | 102 |
| Tooltips | 62 |
| Notifications | 23 |

## 文件结构与取法

- 每个组件一个文件：`Buttons/0xnihilism_fast-cat-82.html`（`作者_随机名-编号.html`）
- 文件里有两段可取代码：
  - **CSS 版**：`<style>...</style>` 块 + 下方 HTML（适合没有 Tailwind 的项目）
  - **Tailwind 版**：`<style type="text/tailwindcss">` 块 + HTML（适合 Tailwind 项目）
- 取对应版本 + HTML 结构，粘进项目，改类名/配色适配设计系统

## 使用流程

1. 按分类进 `skills-repo/uiverse-galaxy/<分类>/`，或 `grep -l "关键词" *.html` 找组件
2. 挑 2-3 个候选（看 HTML 里的 style 块），选最接近设计方向的
3. 拷进项目 → 改色板/圆角/阴影匹配用户的设计系统 → 在 dev server 里验证
4. 这些组件是纯展示级（hover 动画为主），需要 framer-motion 级复杂动画找 react-bits / magic-ui

## 与其他素材库的分工

| 需求 | 用 |
|---|---|
| 海量零依赖按钮/卡片/loader/开关（静态+微交互） | **UIVerse Galaxy（本库）** |
| 带 JS/framer-motion 的 React 动画组件 | react-bits（213 个）/ magic-ui（75 个） |
| 3D/WebGL 背景（shader） | threeui / shadergradient |

## 坑

- 社区投稿质量参差：文件多但风格不一，**挑选比生成重要**——一次给 3 个候选让用户挑
- 部分组件的 CSS 是固定色值，要全局搜文件内的颜色替换成设计 token
- Tailwind 版依赖项目 Tailwind ≥3，且部分类名（如自定义动画）需要把 style 块里的 CSS 变量拷进 tailwind.config 或保留内联
- 组件只含 UI 不含行为逻辑：表单验证、a11y 焦点管理要自己补
