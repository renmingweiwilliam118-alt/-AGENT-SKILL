---
name: premium-design
description: "Use when the user asks for premium design with no spec."
---

# Premium Design Intake (模糊 \"高级美观\" → 可交付)

The user often says only \"做一个高级且美观的 X\" — a quality word, not a spec.
Do NOT ask them to describe design (that's the burden we're removing) and do NOT
pick a skill blindly. Do this instead:

## 1. Parse the two fields that are actually in the sentence
- **Object**: what the deliverable is (落地页 / 后台 / 卡片 / 海报 / 3D 场景 / 动效 demo /
  「随便做个」→ pick the object that best shows 高级: a single hero card or a
  landing hero). If truly absent, state which one you chose and why, one line.
- **Quality bar**: the word they used (高级/美观/质感/克制/luxe). 高级+美观 = run the
  full checklist below. 只说 \"好看\" = run a reduced set (color, type, spacing).

## 2. Pick ONE concrete skill and say so
Route the object to a real skill, then actually `skill_view()` it before building.
Name it in your reply: \"这一步我用了 X。\" Never build the whole thing on this skill
alone if a concrete skill owns that domain.

| Object | 首选技能 | 备选 |
|---|---|---|
| 落地页 / 官网 / 营销页 / 原型 | `design/frontend-design` | `creative/claude-design`, `high-end-visual-design` |
| 后台 / 组件 / 数据面板 | `shadcn-ui` | `ui-styling`, `ui-ux-pro-max` |
| 去 AI 味的干净前端 | `design-taste-frontend` | `impeccable-design-polish` |
| 高级质感 / 像设计代理出品 | `high-end-visual-design` | `gpt-taste` |
| 真实 3D 场景 / 交互装置 | `3dviz-pro-max` | `threejs`, `design/algorithmic-art` |
| 会跟随指针的等轴线描图 | `hairline-create` | — |
| 海报 / 卡片 / 视觉稿 | `design/canvas-design` | `creative/baoyu-infographic` |

## 3. The \"高级\" acceptance checklist — run every item, self-audit before delivery
These are the thing that turns \"高级\" from a word into a verdict. Tick each:
- [ ] **配色**: ≤ 3 主色 + 1 中性阶；有明确对比度；不碰纯 #000/#fff；有理由的主色
- [ ] **字体**: 一套有性格的组合（非裸 system-ui）；字阶成体系（有明确级差）
- [ ] **间距/留白**: 4 或 8 的倍数基准；呼吸感够，不挤
- [ ] **层次/材质**: 深度是\"有理由的\"（阴影、层叠、毛玻璃服务于焦点，不炫技）
- [ ] **动效**: 全页一套缓动曲线 + 统一节奏；克制（不是每处都弹）；该停就停
- [ ] **细节对齐**: 网格对齐；圆角/描边/间距一致；hover/active 有反馈
- [ ] **去 AI 味**: 不堆 emoji、不用 stock 占位图、不写营销套话、颜色不随机撞
- [ ] **可验证**: 真的渲染/跑通了（不是描述），附截图或可开文件

## 4. Deliver in this shape (short)
- 一句：做了什么对象 + 用了哪个技能
- 验收表：上面对勾的项（打勾 or 一句说明为什么省）
- 交付物：可开文件 / MEDIA 截图，说明在哪

If the user says \"不行，再高级一点 / 太素了 / 太花了\"，that is the only signal you
need: 再高级 = 提留白+降饱和+减元素；太素 = 加一处有理由的材质或动效；太花 = 砍到 ≤3 色。
