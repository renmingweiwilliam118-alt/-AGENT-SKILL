---
name: premium-motion-interactions
description: "Use when building premium UI motion interactions."
version: 1.0.0
metadata:
  hermes:
    tags: [motion, interaction, ui, animation, css, gesture, design, web, app]
---

# 高级交互动效设计指南(Premium Motion Interactions)

面向 App / 小程序 / Web 的 30 种高级交互动效。**高级感 = 每一次操作都有恰到好处的反馈,而非堆特效。** 落地前先读文末「速查表」和「核心原则」。

> 配合使用:做具体 UI 时叠加 `design/gpt-taste`、`design/emilkowalski-motion`、`design/animate` 等;写 React/Expo 时用 `design/animate-expo`。本技能提供的是「技法清单 + 关键数值」,直接照着实现即可。

## 一、App / 小程序 — 12 种高级交互

1. **按压回弹(SPRING)** — 按钮压过头再弹回,有重量、弹性手感。关键:缓动 `cubic-bezier(.34,1.56,.64,1)`。
2. **弹性开关(SQUASH)** — 滑块起步先横向拉长、落位再压回原宽。关键:改 `width` 而非 `scale`,保持控件比例自然。
3. **水波按钮(RIPPLE)** — 点击反馈从手指按下处散开、跟着手指走。关键:`clip-path: circle()` 从点击点扩散,父元素 `overflow: hidden`。
4. **点击爆散(BURST)** — 关键操作用粒子爆发,反馈分量匹配动作。关键:粒子从点击点向四周扩散 + 缩放 + 透明度变化。
5. **成功勾选(DRAW)** — 勾选一笔一笔画出,让成功有过程感。关键:SVG 路径动画,`stroke-dasharray` + `stroke-dashoffset`。
6. **液态滑块(LIQUID)** — 轨道、滑钮、数值三条动画同步,控件像整体。关键:三元素共享同一时长与缓动函数。
7. **数字滚动(COUNT)** — 数字慢慢停下、不突然刹住。关键:`easeOutCubic`,速度逐渐减慢。
8. **骨架落位(SHIMMER)** — 骨架屏高度必须等于真实内容高度,避免加载时跳动。关键:尺寸/位置与真实内容完全匹配,同布局结构。
9. **卡片翻面(3D)** — 正反面各藏好背面,翻转不穿帮。关键:`perspective` + `transform-style: preserve-3d` + `backface-visibility: hidden`。
10. **汉堡变叉(MORPH)** — 汉堡菜单与关闭叉用同一元件过渡,切换不丢位置。关键:旋转 + 位移变换平滑变形。
11. **卡片抽走(STACK)** — 堆叠卡片抽走时,后面压着的卡片必须可见。关键:`z-index` 控层级,抽走时调整后续卡片位置与透明度。
12. **底部抽屉(SHEET)** — 抽屉展开后在关键帧停顿,让用户读清状态。关键:在 34%–72% 位置停留。

## 二、Web — 10 种高级交互

1. **滚动钉住主图** — 产品介绍页:主图 `position: sticky` 居中固定,右侧文字分段切换,每切一段主图推近对应位置并高亮重点区域,把长介绍变随滚动发生的视觉叙事。关键:监听滚动 + 段落变化,同步调主图位置与高亮。
2. **光标变形(情境光标)** — 隐藏系统光标,小圆点跟随鼠标;悬停图片放大到 68px 填主色、融入文字标签;悬停按钮缩回。关键:`mousemove` 跟踪,动态改大小/颜色/内容。
3. **磁吸按钮** — 鼠标进入按钮 60px 范围,按钮按光标偏移量 0.35 倍跟随、内部图标随外圈 0.15 倍偏移;离开后弹性回位。关键:`mousemove` 算距离,回位用 `cubic-bezier(.54,1.15,.64,1.84)`。
4. **图标按钮展开标签** — 圆形图标按钮悬停时宽 40px→自适应,保持全圆角;标签延迟 80ms 淡入。关键:`transition` 宽度 + `opacity`/`transform` 文字淡入。
5. **导航底色跟随(滑动高亮)** — 导航项后放绝对定位圆角色块,悬停时读目标位置/宽度、弹性移动并改宽;移出后回到当前页对应项。关键:`getBoundingClientRect()` 读尺寸 + 弹性缓动。
6. **功能块悬停翻色(角落扩散)** — 以右上角箭头按钮为扩散中心,悬停用 `clip-path: circle()` 让主色从按钮处扩散至整块;文字反色、箭头转 45°。关键:`clip-path: circle()` + `transform`。
7. **分档拖动条(吸附档位滑块)** — 圆角长条轨道 + 圆形滑块;拖动按档位切换数字、已滑过轨道填主色;松手弹簧吸附最近档位。关键:`input[type=range]` + `change` 监听 + 弹簧缓动。
8. **柱状图跟手读数(扫动式)** — 柱体密集排列;鼠标横移时竖向指示线 + 圆形读数标签跟随,左侧柱主色、右侧压暗,顶部数值平滑滚动。关键:`mousemove` 跟位置 + 颜色高亮。
9. **悬停预览图片(跟随式)** — 文字列表每行绑一张图;悬停从 0.8 倍缩放淡入、带惯性跟鼠标;切行新图 0.9 倍弹入覆盖旧图;移出淡出。适合案例/作品集。关键:`mouseenter`/`mouseleave` + `transform`/`opacity`。
10. **圆形扩散换肤(主题切换)** — 以主题按钮为圆心,View Transitions + `clip-path: circle()` 让新配色从半径 0 扩散覆盖全页;太阳图标变形为月亮,再点反向收回。关键:View Transitions API + `clip-path: circle()`。

## 三、App / 小程序 — 8 种进阶动效

1. **3D 倾斜光影面板** — 按压时面板随触点 3D 俯仰微倾 + 跟随手指的径向镜面高光,松手阻尼弹性复位,平面有实体材质感。关键:`touchmove` 调 `rotateX`/`rotateY` + `box-shadow`。
2. **流体胶囊形变** — 按钮触发加载/展示时如水滴般平滑流动、延展成新面板,圆角与尺寸走高阻尼流体曲线。关键:`transition` 形变 + `border-radius`/`width`/`height`。
3. **共享元素无缝展开** — 点击列表条目原地放大膨胀成详情页,返回反向收缩,无白屏/推屏。关键:Shared Element Transition + `transform`/`opacity`。
4. **磁吸游标与滚动码表** — 折线图横滑时指示线磁吸最近数据点、交点光晕呼吸放大,顶部数据如机械码表丝滑翻滚。关键:`touchmove` 跟位置 + 数据滚动 `transform`。
5. **阻尼弹性抽屉** — 底部面板拉到顶/下拉到底带真实橡皮筋阻尼,松手按速度判断吸附对应高度。关键:`touchmove` 跟拖拽 + spring 动画。
6. **动态弥散光晕边框** — AI/核心模块加缓慢旋转的渐变流光微边框 + 背后毛玻璃弥散光晕,提升视觉层次。关键:`conic-gradient()` + 旋转 `animation` + `backdrop-filter: blur()`。
7. **物理弹簧交错流** — 列表/瀑布流加载不用整体死板淡入,设极小时间差让每项从下往上带弹性依次弹入。关键:stagger delay + `transform`/`opacity`。
8. **弹性微缩触觉反馈** — 按压不只变透明,产生 0.96 微缩压缩 + 细微内阴影加深,松手微冲过头再回弹。关键:`touchstart`/`touchend` + `cubic-bezier` 回弹。

## 四、核心设计原则(落地前必看)

1. **高级感不是堆特效,是让每一次操作都有恰到好处的反馈。**
2. **统一节奏**:所有交互保持同一套动画时长与缓动函数,整体质感才一致(别一个页面混七八种曲线)。
3. **服务体验**:避免过度设计影响性能与可用性;能用纯 CSS 别上 JS,能用 transform/opacity(合成层)别动 layout。
4. **快速实现**:调用 UI 设计 Skill + AI 描述词可加速;先选 2–3 个核心交互做精,别全上。

## 五、速查表(可直接抄进代码)

| 用途 | 值 |
|---|---|
| 按压回弹缓动 | `cubic-bezier(.34,1.56,.64,1)` |
| 磁吸回位缓动 | `cubic-bezier(.54,1.15,.64,1.84)` |
| 数字滚动停 | `easeOutCubic`(`1-(1-t)^3`) |
| 情境光标悬停图 | 放大到 **68px** 填主色 + 文字标签 |
| 磁吸按钮 | 范围 **60px**;外圈 **0.35**× 偏移,内图标 **0.15**× |
| 图标展开标签 | 宽 40px→自适应;文字延迟 **80ms** 淡入 |
| 悬停预览图 | 进入 **0.8×** 淡入;切行 **0.9×** 弹入 |
| 抽屉关键帧停顿 | **34%–72%** 位置 |
| 微缩触觉 | 压缩 **0.96** + 内阴影加深 + 回弹 |
| 成功勾选 | SVG `stroke-dasharray`/`stroke-dashoffset` 路径动画 |
| 3D 翻面 | `perspective` + `preserve-3d` + `backface-visibility:hidden` |
| 圆角扩散换肤 | View Transitions + `clip-path: circle()` |
| 光晕边框 | `conic-gradient()` 旋转 + `backdrop-filter: blur()` |

## 六、通用实现片段

**按压回弹(纯 CSS)**
```css
.btn { transition: transform .45s cubic-bezier(.34,1.56,.64,1); }
.btn:active { transform: scale(.92); } /* 压过头再弹回 */
```

**磁吸按钮(JS)**
```js
el.addEventListener('mousemove', e => {
  const r = el.getBoundingClientRect();
  if (Math.hypot(e.clientX-r.left-r.width/2, e.clientY-r.top-r.height/2) < 60) {
    const x = (e.clientX-(r.left+r.width/2))*0.35;
    const y = (e.clientY-(r.top+r.height/2))*0.35;
    el.style.transition='transform .1s'; el.style.transform=`translate(${x}px,${y}px)`;
  } else {
    el.style.transition='transform .6s cubic-bezier(.54,1.15,.64,1.84)';
    el.style.transform='';
  }
});
```

**圆形扩散换肤(View Transitions)**
```css
::view-transition-old(root), ::view-transition-new(root) { animation: none; mix-blend-mode: normal; }
::view-transition-new(root) { clip-path: circle(0 at var(--x,50%) var(--y,50%)); animation: grow .5s ease; }
@keyframes grow { to { clip-path: circle(150% at var(--x,50%) var(--y,50%)); } }
```

**数字滚动 easeOutCubic**
```js
function tween(from, to, dur, cb){ const t0=performance.now();
  function step(t){ const p=Math.min((t-t0)/dur,1), e=1-Math.pow(1-p,3);
    cb(from+(to-from)*e); if(p<1) requestAnimationFrame(step);} requestAnimationFrame(step); }
```

## 七、选型建议

- 移动端/App:优先做「按压回弹 + 阻尼抽屉 + 弹簧交错流 + 微缩触觉」这 4 个,反馈感最强、实现最省。
- Web 产品页:「滚动钉住主图 + 磁吸按钮 + 导航底色跟随 + 圆形扩散换肤」组合最能拉高质感。
- 数据/图表:「柱状图跟手读数 + 磁吸游标滚动码表」。
- 全局统一只用 2–3 条缓动曲线(默认回弹用 `.34,1.56,.64,1`),避免曲线泛滥导致廉价感。
