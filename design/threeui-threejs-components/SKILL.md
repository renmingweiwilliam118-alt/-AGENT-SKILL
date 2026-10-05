---
name: threeui-threejs-components
description: 47 个现成 Three.js / WebGL shader 组件素材库（来自 MengTo/threeui，MIT）。落地页背景、3D 场景、shader 按钮/开关、CRT、粒子场、地球、织物、文字特效等。做 threejs 场景、WebGL 背景、创意 UI 时优先查这里找现成实现再改造，而不是从零写 shader。
license: MIT
---

# ThreeUI Three.js 组件素材库

来源：[MengTo/threeui](https://github.com/MengTo/threeui)（MIT 协议）。
素材已下载到本地：`C:\Users\mwr_w\skills-repo\threeui\`（47 个组件目录，每个含 .tsx/.ts 源码，另有 `_inventory.json` 清单）。

## 使用流程

1. **先查素材库**：读 `C:\Users\mwr_w\skills-repo\threeui\_inventory.json`，或列目录找最接近目标的组件（关键词对照见下表）
2. **读源码改造**：组件都是 React + Three.js（部分纯 TS renderer + GLSL），把需要的逻辑摘进项目；非 React 项目把渲染逻辑（`*Renderer.ts`/`*Shaders.ts`）抽出来包进原生 Three.js
3. **注意依赖**：部分组件用了旧版 three 的导出方式（见 structure-flow 目录里的 `three128.d.ts` 类型垫片）；如果用户项目 three 版本不同，检查 import 路径（`three/examples/jsm/...` vs `three/addons/...`）
4. 改完必须跑起来验证（浏览器 / 用户项目 dev server），不要只交代码

## 组件关键词对照（47 个）

| 想要的效果 | 组件目录 |
|---|---|
| WebGL 落地页背景（通用粒子/光效） | brand-orbs, energy-orb, warp-field, ribbon-field, stream-convergence, orbital-sphere, condensation, dot-matrix |
| 3D 地球 / 天体 | globe, orbital-sphere |
| CRT / 复古扫描屏 | crt |
| 星座 / 星空粒子场 | constellation-field, bell-field |
| 液体 / 流体 / 虹彩织物 | liquid-form, woven-cloth（含 3 个变体：atelier/iridescent/washi） |
| 3D 场景（景深/氛围） | landscape, japanese-tower, temple-night, sylva-living-world, bookshelf |
| Shader 按钮 / 开关 / 徽章 | shader-buttons, circle-buttons, rectangle-buttons, liquid-metal-button, skeuomorphic-toggle（玻璃/现代/Shader 三款开关）, spark-badge |
| 文字动效 / 标题特效 | article-headings（decode 解码动画）, text-path-studies, typography-vortex, semantic-bloom |
| 加载器 / 数据可视化 | uplink-loader, data-pixel-arc, predictive-arc, lumen-cta |
| 3D 生物 / 角色 | character-carousel, koi-studies（锦鲤） |
| 导航 / Dock | animated-top-dock（玻璃 + 复古像素两种粒子底） |
| 落地页整版参考 | landing-pages（3 版 recipe + typography 方案）, gallery |
| 元素 / 生长特效 | elements, structure-flow, neuform-isolated |
| 门户 / 传送门 | portal-field |
| 激光 / 光束 | laser |
| 手稿 / 草图感 | sketchbook, section-elements |

## 坑

- `fonts/fragment-mono.woff2` 是 SIL OFL 字体，其他代码是 MIT（见素材库内 LICENSE）
- 组件里的图片/视频资源在 `threeui.com` 远端，仓库只含代码——要完整跑原站需 `npm install && npm run dev`（源仓库）
- React 组件直接拷进非 React 项目会缺 JSX 运行时，优先取其中的 renderer/shader 逻辑重写
- `woven-cloth`、`liquid-metal-button`、`spark-badge`、`uplink-loader` 各带一个独立 `.html` 演示，是最好的最小复现样本
