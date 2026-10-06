---
name: shadergradient
description: 3D 动态渐变/流体背景组件（ruucm/shadergradient，MIT，React + @react-three/fiber）。npm 装 @shadergradient/react，10 个内置 presets（halo/pensive/mint/interstella/sunset/cottonCandy 等），可自定义颜色/频率/速度/环境贴图。落地页 hero 背景、3D 氛围背景优先查这里，不要手写 GLSL。
license: MIT
---

# Shader Gradient（3D 动态渐变背景）

来源：[ruucm/shadergradient](https://github.com/ruucm/shadergradient)（MIT）。
素材库：`C:\Users\mwr_w\skills-repo\shadergradient\`（核心 src + 18 个 GLSL frag + presets，见 `_README.md`）。

## 安装（目标 React 项目）

```bash
npm i @shadergradient/react @react-three/fiber three three-stdlib camera-controls
```

**兼容性硬约束**（装错版本 Next 直接白屏）：

| 环境 | React | R3F | three |
|---|---|---|---|
| Next 15 App Router | ^19 | ^9 | >=0.158 |
| Next 14 / Vite / 其他 | 18 或 19 | 对应 8.x / 9.x | >=0.158 |

## 基本用法

```jsx
import { Canvas } from '@react-three/fiber'
import { ShaderGradient, presets } from '@shadergradient/react'

<Canvas frameloop="always">
  <ShaderGradient preset={presets.halo} />
</Canvas>
```

## 10 个内置 presets

`halo`（白调光晕）、`pensive`、`mint`、`interstella`（星空）、`nightyNight`（夜景）、`violaOrientalis`、`universe`、`sunset`（日落）、`mandarin`（橘调）、`cottonCandy`（棉花糖粉紫）

每个 preset 的完整参数在 `skills-repo/shadergradient/src/presets.ts`：
- **颜色**：`color1/color2/color3`（改这三就出全新配色）
- **动效**：`uSpeed`（速度）、`uFrequency`（波动频率）、`uAmplitude`（振幅）、`animate: 'on'/'off'`
- **质感**：`grain`（颗粒）、`envPreset`（环境贴图：city/sunset/...）、`lightType: '3d'/'2d'/'4d'/'5d'`
- **性能**：`frameRate`（presets 默认 10，敏感页面别开 60）
- **形态**：`type: 'plane'/'sphere'/'torus'...`（渲染几何体形状）

改色不改结构：复制 preset 对象，只动 color1-3 + uSpeed，是最快的定制路径。

## 使用流程

1. 用户要"3D 动态背景/渐变 hero"→ 选 preset 起手（按气质：日落用 sunset、科技感用 interstella、柔和用 mint）
2. 在 dev server 里渲染验证（`Canvas` 需要固定高度的容器，如 `h-screen`）
3. 需要完整 UI 控件面板（让用户调参）→ 加 `@shadergradient/ui`
4. 验证必做：动效顺滑、配色贴合设计方向、`frameRate` 不烧电

## 与其他背景素材的分工

| 需求 | 用 |
|---|---|
| 3D 流体/渐变 hero 背景（Three.js） | **shadergradient（本库）** |
| 其它 WebGL 背景（CRT/星空/织物 47 个） | threeui-threejs-components |
| 纯 CSS 渐变（不需要 3D） | 直接写 CSS，别上 Three.js |
| 粒子/星空 DOM 级 | react-bits / uiverse-galaxy 的 Backgrounds |

## 坑

- 没有 R3F + three 完整依赖链就跑不起来（npm 安装命令 5 个包一个不能少）
- `embedMode: 'off'` 时组件自建 canvas；要塞进已有 canvas 场景才开 embedMode
- 移动端注意：`pixelDensity` 设 1，frameRate 10，避免 GPU 过热
- 完整仓库（Vue 版/Nuxt、Figma 插件）需要时重新 clone，素材库只含 React 核心
