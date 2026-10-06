---
name: react-bits
description: 213 个动画 React 组件素材库（DavidHDev/react-bits，MIT+CC，48k star）。文字动画/背景/UI 组件/微交互，每个 4 变体（JS-CSS/JS-TW/TS-CSS/TS-TW）。做 React/Next.js 页面要加动画效果、炫酷背景、微交互时，先查这里的现成组件 copy-paste，不从零写 CSS/JS 动画。
license: MIT + Commons Clause
---

# React Bits 组件素材库

来源：[DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)（200+ 组件，每周增长）。
素材已下载到本地：`C:\Users\mwr_w\skills-repo\react-bits\`（3 个变体源码目录 + 清单）。

## 使用流程

1. **查清单**：`C:\Users\mwr_w\skills-repo\react-bits\_components.md`（213 个组件按 5 类分组 + 说明），或 `_components.json`（机器可读）
2. **取源码**：变体目录 `ts-tailwind/`（首选，TS + Tailwind）、`ts-default/`、`tailwind/`。组件路径模式：`<变体>/<分类>/<组件名>/<组件名>.tsx`
3. **copy-paste 进用户项目**：react-bits 不是 npm 包，组件直接拷进项目；依赖它的本地 `hooks/` 和 `utils/`（素材库没带全，缺什么就从 145MB 完整仓库解压目录补：`C:\Users\mwr_w\AppData\Local\Temp\react-bits-main\react-bits-main\src\`）
4. **跑起来验证**：在用户项目的 dev server 里看效果，别只交代码

## 分类速查（213 个）

| 分类 | 数量 | 代表组件 |
|---|---|---|
| **TextAnimations** | 33 | SplitText、ScrambleText、Wave、LiquidFill、Typewriter、MorphingText |
| **Backgrounds** | 59 | Aurora、ParticleField、Starfield、Metaballs、GridPattern、DitherVeil、MagneticBorder |
| **Components** | 47 | GlassDirectionalHover、ShinyButton、GizmoDock、TiltCard、CommandMenu、LaserCursor |
| **Animations** | 40 | Antigravity、BlobCursor、Cubes、Crosshair、ElectricBorder、ElasticMesh |
| **Micro**（微交互） | 34 | ClickSpark、CursorGlow、HoverScroll、Magnetic、Ripple、ButtonSpotlight |

## 与其他素材库的分工

- 要 **3D/WebGL shader**（地球、织物、CRT）→ `threeui-threejs-components`
- 要 **shadcn 一键装**（`npx shadcn add @magicui/...`）→ `magic-ui`（75 个组件）
- 要 **copy-paste 无依赖、纯 CSS/JS 动画** → **React Bits**（本库，最轻）
- 整体前端品味把关 → `taste-skill` / `gpt-taste`

## 坑

- 变体目录里组件文件名和导入名一致（PascalCase），但个别组件依赖 `src/hooks/useXxx` 本地 hook，拷了组件要连 hook 一起拷
- `ts-tailwind` 需要项目已有 Tailwind（v3+）；`ts-default` 是纯 CSS 版，项目没有 Tailwind 就用它
- 组件的 `meta` 字段里有 `deps`（第三方依赖如 framer-motion），装组件前先确认项目里有没有
- License 是 MIT + Commons Clause：可免费商用，但禁止提供"与 react-bits 竞争"的服务（不影响正常用在你的产品里）
