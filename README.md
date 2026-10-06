# Agent Skill Vault

Hermes Agent 技能库备份。共 **572 个技能**，19 个类别。每个技能的用途从 SKILL.md 自动提取。

## 目录

- **design**（设计，107 个）- UI/动效/品牌/图表设计类技能。含 taste-skill 反模板化前端方法论（v2/v1/gpt 版）、Emil Kowalski 动效体系（animate/apple-design/review-animations）、44 种图表（...
- **browser-act**（浏览器自动化，103 个）- Browser Use CLI 浏览器操作技能。103 个技能覆盖电商抓取（淘宝/1688/Amazon/Walmart/eBay/Etsy/闲鱼/Airbnb）、社媒监听（X/Instagram/Threads/Reddit/Facebo...
- **openmontage**（视频/多媒体制作，90 个）- OpenMontage 视频创作体系。AI 视频生成（Kling/Seedance/LTX/Manim/Remotion/GSAP）、TTS/音乐（ElevenLabs/ACE-Step）、图像生成（FLUX/DashScope）、3D、字...
- **marketing**（营销，58 个）- 58 个营销技能：A/B 测试、广告投放、SEO（AI/传统/程序化）、ASO、归因分析、流失预防、联名营销、冷邮件、社区营销、竞品分析、内容策略、文案、CRO、目录提交、邮件序列、活动运营、定价、公关、推荐体系、RevOps、销售赋能、上...
- **gstack**（GStack 运营工具箱，55 个）- Garry Tan 的运营与工程工具箱。CEO 视角（cso/plan-ceo-review/office-hours）、工程流程（qa/ship/retro/review/investigate/benchmark）、设计（design-...
- **media**（媒体资产，35 个）- 图像/视频/音频生成类技能：Fal 全家桶（图像/视频/3D/唇形/试穿/超分/视觉）、Venice 多模态、Sora、Replicate、YouTube 下载/剪辑、GIF 贴纸、截图、3D 设备 mockup、AI 音乐专辑。
- **software-development**（软件开发，35 个）- 35 个软件工程方法论技能。Superpowers 全套（brainstorming/writing-plans/test-driven-development/systematic-debugging/subagent-driven-de...
- **productivity**（生产力，29 个）- 29 个生产力技能：文档（docx/pdf/pptx/minimax 系列）、周度回顾规划、会议行动项、文档义务提取、Notion/Airtable/Google Workspace、ADHD 友好输出、文件规划、地图/路线、价格监控、Te...
- **claude-mem**（持久记忆，22 个）- claude-mem 记忆体系（22 个）：跨会话记忆压缩检索（mem-search）、项目周报/时间线报告、PR 看护、GitHub issue 根因聚类、会话诊断、模式创建、成本报告、云同步、代码库预学习等。
- **creative**（创意内容，10 个）- 10 个创意技能：ASCII 艺术/视频、SVG 架构图、Manim 数学动画、p5.js 生成艺术、信息图（21 布局 x 21 风格）、Claude Design 原型、DESIGN.md 规范、音乐创作。
- **autonomous-ai-agents**（多智能体，7 个）- 7 个多智能体编排技能：Claude Code/Codex/OpenCode 委托、桌面计算机操作、多代理团队、Hermes 插件开发、workspace-dispatch 任务编排。
- **research**（研究，6 个）- 6 个研究技能：arXiv 检索、竞品新闻监控、引用核验、last30days 舆论研究、LLM Wiki 知识库、D3 数据可视化。
- **web**（网页，5 个）- 5 个网页技能：被封锁页面恢复（WAF/paywall/403 应对）、web-clone 整站复刻、网页工件构建、agent-browser。
- **apple**（Apple 生态，4 个）- 4 个 Apple 设备技能：Apple Notes/Reminders/iMessage/FindMy 操作。
- **email**（邮件，2 个）- 2 个邮件技能：Himalaya CLI（IMAP/SMTP）、收件箱分诊。
- **devops**（DevOps，1 个）- DevOps 基础技能。
- **note-taking**（笔记，1 个）- Obsidian vault 读写检索。
- **social-media**（社媒，1 个）- X URL 抓取技能。
- **writing**（写作，1 个）- humanizer：去除 AI 腔，让文本读起来像人写的。

---

# design / 设计

UI/动效/品牌/图表设计类技能。含 taste-skill 反模板化前端方法论（v2/v1/gpt 版）、Emil Kowalski 动效体系（animate/apple-design/review-animations）、44 种图表（diagram-design）、OpenDesign 设计模板库、GSAP 全套、SwiftUI/Flutter、shadcn、3D/shader。

**来源**: obra/superpowers, emilkowalski/skills, Leonxlnx/taste-skill, cathrynlavery/diagram-design, tt-a1i/archify, nexu-io/open-design, Graphify-Labs/graphify

| 技能 | 用途 |
|------|------|
| `8-bit-orbit-video-template` | \| Hyperframes-based video template for retro pixel deck motion design. Use when users want a high-fidelity, multi-scene HTML-to-video composition with advanced transitions, interactive preview controls, and ready-to-render default style. |
| `after-hours-editorial-template` | \| Luxury dark-editorial HyperFrames template for three-page cinematic storyboards, inspired by haute couture title cards and magazine chapter spreads. Use when the user asks for premium fashion-style motion pages, moody serif-led storytelling, or a high-end... |
| `algorithmic-art` | \| Create generative art using p5.js with seeded randomness so every render is reproducible. Useful for procedural posters, motion-style stills, and artistic frame studies. |
| `animate` | Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, what purpose, which tool, which properties, which curve and duration, how it interrupts, how it exits. Writes the implement... |
| `animate-expo` | Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it animate, which thread it runs on, which properties, spring or timing, how the gesture hands off, how it degrades. Writes the imp... |
| `animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). Use when the user asks "what's it called when…"... |
| `apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI, spring animations, drag/swipe/sheet interactions, momentum and interruptible transitions, translucent materials and de... |
| `apple-hig` | \| Apple Human Interface Guidelines as 14 agent skills covering platforms, foundations, components, patterns, inputs, and technologies for iOS, macOS, visionOS, watchOS, and tvOS. |
| `archify` | Create polished, validated architecture, workflow, sequence, data-flow, and lifecycle/state diagrams as explorable standalone HTML with inline SVG, dark/light themes, optional trace motion, and PNG/JPEG/WebP/SVG/WebM export. Accept plain-language requiremen... |
| `article-magazine` | Huashu / huashu-md-html-inspired magazine article layout for turning Markdown or notes into a polished long-form HTML essay. |
| `ask-sonner` | Guide to Sonner, the React toast library — install and wire up the Toaster, pick the right toast() call, promise and loading toasts, updating, dismissing and persisting toasts, styling, theming and icons, positioning and multiple toasters. Use when working ... |
| `banner-design` | Design banners for social media, ads, website heroes, creative assets, and print. Multiple art direction options with optional generated or supplied visuals. Actions: design, create, generate banner. Platforms: Facebook, Twitter/X, LinkedIn, YouTube, Instag... |
| `brand` | Brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voice, marketing assets, brand compliance, style guides. argument-hint: "[update\|review\|create] [args] |
| `brand-extract` | \| Extract a complete Brand Kit from a live website by driving the in-app browser. Use when a brand-extraction project opens with a site in the Browser tab, or when the user asks to "extract a brand", "pull the brand from <url>", "get the colors/fonts/logo f... |
| `brand-guidelines` | \| Apply Anthropic's official brand colors and typography to artifacts for consistent visual identity and professional design standards. A reference for shaping your own. |
| `brandkit` | Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks, and visual-world presentations. Trained for minimalist, cinematic, editorial, dark-tech, luxury, cultural, security, gaming, developer-tool... |
| `break-ui` | Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts, zero items, long labels, non-Latin text, emoji, extreme numbers — then render it behind a "Demo data / Worst case" togg... |
| `brutalist-skill` | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects. For data-heavy dashboards, portfolios, or editorial sites that need to feel ... |
| `canvas-design` | \| Create beautiful visual art in PNG and PDF documents using design philosophy and aesthetic principles for posters, illustrations, and static pieces. |
| `chat-motion-overlay` | Generate configurable chat motion overlays from a transcript or screenshot, including plain bubble scenes, app-style chat containers, optional device frames, preset or uploaded avatars, nickname display rules, and transparent-video-ready Remotion bundles. U... |
| `color-expert` | \| Color science expert skill with 286K words of reference material covering OKLCH/OKLAB, palette generation, accessibility/contrast, color naming, pigment mixing, and historical color theory. |
| `creative-director` | \| AI creative director with recursive self-assessment: 20+ methodologies (SIT, TRIZ, Bisociation, SCAMPER, Synectics), 3-axis evaluation calibrated against Cannes/D&AD/HumanKind, 5-phase process from brief to presentation. |
| `deck-guizang-editorial` | Editorial magazine meets e-ink: 10 layouts and 5 palettes (Ink, Indigo Porcelain, Forest Ink, Kraft Paper, Dune). |
| `deck-open-slide-canvas` | Locked 1920x1080 canvas deck with React component-level free composition, not bound to a fixed template. |
| `deck-swiss-international` | 16-column grid, one saturated accent, and 22 locked layouts (Klein Blue, Lemon, Mint, Safety Orange). |
| `design` | Comprehensive design skill: brand identity, design tokens, UI styling, logo generation (55 styles, Gemini, Atlas Cloud, or MuAPI AI), corporate identity program (50 deliverables, CIP mockups), HTML presentations (Chart.js), banner design (22 styles, social/... |
| `design-brief` | \| Parse a structured design brief written in I-Lang protocol format into a concrete design spec. Eliminates ambiguity from vague requests like "make it professional" by requiring explicit dimensions: palette, typography, layout, mood, density, and constrain... |
| `design-consultation` | \| Build a complete design system from scratch with creative risks and realistic product mockups. Useful for kickoff workshops and brand-from-zero work. |
| `design-review` | \| Designer Who Codes: visual audit then fixes with atomic commits and before/after screenshots. Useful for tightening shipped UI before launch. |
| `design-system` | Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variables, spacing/typography scales, component specs, strategic slide creation. Use for design tokens, systematic design, brand-compl... |
| `diagram-design` | Create branded architecture, architecture delta, IT current-state, flowchart, sequence, state machine, ER/data model, timeline, swimlane, quadrant, radar/spider, polar chart (polar/radial lollipop), loop/flywheel, nested, tree, org chart, layer stack, explo... |
| `digits-fintech-swiss-template` | \| Swiss-grid fintech deck template in black / warm paper / neon-lime contrast. Use when users ask for premium data-story slides with strict modular layout, bold numeric cards, restrained motion, and keyboard/click navigation in one HTML file. |
| `doc-kami-parchment` | Warm parchment canvas (#f5f4ed), monochrome ink-blue accent (#1B365D), one serif family, and editorial-grade typography. |
| `ecommerce-image-workflow` | \| Reference-product ecommerce image workflow for generating a compact set of product-faithful main, feature, and lifestyle images from real product reference photos. V1 requires uploaded product imagery and intentionally defers brief-only concept generation... |
| `editorial-burgundy-principles-template` | \| Editorial studio deck template in burgundy / blush / muted-gold palette. Use when users ask for premium manifesto or culture slides with pill tags, large typographic statements, principle cards, and guided keyboard/click navigation. |
| `emil-design-eng` | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great. |
| `emilkowalski-motion` | \| Motion-design follow-up skill inspired by Emil Kowalski's animation guidance. Use after an interface exists to add tasteful micro-interactions, state transitions, and page motion with product-grade restraint. |
| `enhance-prompt` | \| Improve prompts with design specs and UI/UX vocabulary. Useful for design-to-code workflows and clarifying requests for visual output. |
| `export-download-debugging` | \| Diagnose and fix browser, preview, or Electron export/download failures, especially image export issues involving Save As, Blob/Data URLs, the File System Access API, createWritable failures, and 0 KB files. |
| `field-notes-editorial-template` | \| Editorial "Field Notes" report template with soft paper background, serif hero typography, rounded pastel insight cards, and a retention chart panel. Use when users ask for a premium magazine-style business report, board memo one-pager, or elegant data st... |
| `figma-code-connect-components` | \| Connect Figma design components to code components using Code Connect so design-system updates flow into the codebase automatically. |
| `figma-create-design-system-rules` | \| Generate project-specific design system rules for Figma-to-code workflows. Useful for capturing tokens, naming, and lint rules in one source. |
| `figma-create-new-file` | \| Create a new blank Figma Design or FigJam file. Useful as the first step in scripted design-system or workshop workflows. |
| `figma-generate-design` | \| Build or update screens in Figma from code or description using design system components. Translate app pages into Figma using design tokens. |
| `figma-generate-library` | \| Build or update a professional-grade design system library in Figma from a codebase. Useful for keeping the Figma source of truth in sync with shipped components. |
| `figma-implement-design` | \| Translate Figma designs into production-ready code with 1:1 visual fidelity. Useful for handing off Figma frames straight to a frontend agent. |
| `figma-use` | \| Run Figma Plugin API scripts for canvas writes, inspections, variables, and design-system work. Prerequisite for every other Figma skill in this catalogue. |
| `find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion with exact values, it does not implement it. Use when the user asks "what could be animated here?" or wants to "make this f... |
| `flutter-animating-apps` | \| Implement animated effects, transitions, and motion in Flutter apps. Useful for native iOS/Android motion design. |
| `frame-data-chart-nyt` | NYT-newsroom typography, staggered reveal animation, and editorial-grade charts (line, bar, or range band). |
| `frame-flowchart-sticky` | SVG curve connectors, sticky-note nodes, and cursor interaction with a whiteboard-brainstorm feel. |
| `frame-glitch-title` | Digital glitch, chromatic offset, and data-corruption title frame for video transitions or cyberpunk heroes. |
| `frame-light-leak-cinema` | Film light leaks, grain, 16:9 letterbox, and large serif type for cinematic openings or chapter cards. |
| `frame-liquid-bg-hero` | WebGL-style fluid displacement background with a quote overlay, suited to video intros, landing heroes, or posters. |
| `frame-logo-outro` | Segmented logo assembly, glow bloom, and tagline reveal for video outros or brand closing frames. |
| `frame-macos-notification` | Realistic macOS notification banner with app icon, title, and body, suited to video overlays or product teasers. |
| `frontend-design` | \| Create distinctive, production-grade frontend interfaces with strong visual direction, polished typography, considered layout, and working HTML/CSS/JS or framework code. Use for websites, landing pages, dashboards, React components, application screens, a... |
| `frontend-dev` | \| Full-stack frontend with cinematic animations, AI-generated media via MiniMax API, and generative art. Useful for hero pages and showcase sites. |
| `frontend-skill` | \| Create visually strong landing pages, websites, and app UIs with restrained composition. OpenAI's production frontend playbook. |
| `frontend-slides` | \| Generate animation-rich HTML presentations with visual style previews. Useful for online keynotes, embedded talks, and interactive briefs. |
| `gpt-tasteskill` | Elite UX/UI & Advanced GSAP Motion Engineer. Enforces Python-driven true randomization for layout variance, strict AIDA page structure, wide editorial typography (bans 6-line wraps), gapless bento grids, strict GSAP ScrollTriggers (pinning, stacking, scrubb... |
| `hand-drawn-diagrams` | \| Generate hand-drawn Excalidraw diagrams from a prompt — animated SVG, hosted edit link, and PNG export. Works with Claude Code, Codex, Gemini CLI, and any agent supporting standard skill paths. |
| `hatch-pet` | Create, repair, validate, preview, and package Codex-compatible animated pet spritesheets from character art, screenshots, generated images, or visual references. Use when a user wants to hatch a Codex pet, create a custom animated pet, or build a built-in ... |
| `html-ppt-retro-quarterly-review` | \| Retro Quarterly Review presentation template in a bold blue + orange editorial language. Use when users ask for a high-impact quarterly review / roadmap deck with heavyweight slab headlines, clean cream paper sections, structured grids, and fast premium m... |
| `image-to-code-skill` | Elite website image-to-code skill for Codex. For visually important web tasks, it must first generate the design image(s) itself, deeply analyze them, then implement the website to match them as closely as possible. In Codex, it must prefer large, readable,... |
| `imagegen-frontend-mobile` | Elite mobile app image-generation skill for creating premium, app-native screen concepts and flows. Designed for iOS, Android, and cross-platform mobile products. Prioritizes clean hierarchy, comfortably readable text, strong multi-screen consistency, contr... |
| `imagegen-frontend-web` | Elite frontend image-direction skill for generating premium, conversion-aware website design references. CRITICAL OUTPUT RULE — generate ONE separate horizontal image FOR EVERY section. A landing page with 8 sections produces 8 images. Never compress multip... |
| `impeccable-design-polish` | \| Follow-up design polish skill inspired by Impeccable. Use after a web or HTML artifact exists to audit, critique, polish, animate, harden, and prepare the page for a live/share pass. |
| `improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. Read-only on source code — it plans improvements, it does not... |
| `library-curator` | \| Search the OD Library (the global asset registry) and apply matching assets into the current project mid-task. Use when the user asks to reuse an image they captured/uploaded earlier, "pull a logo/screenshot from my library", or to find and drop a stored ... |
| `login-flow` | Mobile login and authentication flow screens |
| `minimalist-skill` | Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows. |
| `mobile-native` | Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something that feels installed. Covers sticky hover states, tap highlight flashes, the 100vh bug, inputs that zoom the page, laggy taps, pul... |
| `od-next-media-inputs` | \| Prepare required media inputs within an existing OD Next plan. Reuse capability evidence, acquire and measure assets efficiently, and resolve asynchronous jobs without removing required content or weakening quality standards. |
| `output-skill` | Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any task requiring exhaustive, unabridged output. |
| `pick-ui-library` | Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop, toasts, state, styling, and more. Only runs when explicitly invoked; it does not trigger on its ow... |
| `plan-design-review` | \| Senior Designer review: rates each design dimension 0-10, explains what a 10 looks like, and flags AI Slop signals. Useful as a gate before merging UI work. |
| `platform-design` | \| 300+ design rules from Apple HIG, Material Design 3, and WCAG 2.2 for cross-platform apps. Useful when shipping a single design across iOS, Android, and the web. |
| `poster-hero` | Vertical poster or Moments-style share image with strong visual impact. |
| `pptx-html-fidelity-audit` | Audit a python-pptx export against its source HTML deck, identify layout/content drift (footer overflow, cropped content, missing italic/em, lost styling, off-rhythm spacing), and re-export with strict footer-rail + cursor-flow layout discipline. Use this s... |
| `pr-feedback-quality-gate` | \| Safely track pull request feedback, resolve review comments or merge conflicts, validate fixes, and use a read-only cross-review before committing or pushing follow-up changes. |
| `prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote the one that feels right. Only runs when explicitly invoked; it does not trigger on its own. disable-model-... |
| `redesign-skill` | Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS. |
| `reference-design-contract` | \| Turn vague taste, screenshots, URLs, product notes, or "make it feel like this" references into a grounded DESIGN.md plus an implementation handoff. Use it before prototypes, decks, redesigns, or image remix work when the user needs a reusable visual dire... |
| `review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned. disable-model-invocation: true |
| `shadcn-ui` | \| Build UI components with shadcn/ui. Pairs with the Stitch design loop to ship structured, accessible components quickly. |
| `shader-dev` | \| GLSL shader techniques for ray marching, fluid simulation, particle systems, and procedural generation. Useful for hero visuals and motion stills. |
| `slack-gif-creator` | \| Create animated GIFs optimized for Slack with validators for size constraints and composable animation primitives. |
| `slides` | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies. argument-hint: "[topic] [slide-count] |
| `soft-skill` | Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that make a website feel expensive. Blocks all the common defaults that make AI designs look cheap or generic. |
| `stitch-loop` | \| Iterative design-to-code feedback loop. Critique → adjust → ship cycle for tightening visual fidelity between brief and built UI. |
| `stitch-skill` | Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI standards — strict typography, calibrated color, asymmetric layouts, perpetual micro-motion, and hardware-accelerated performance. |
| `swiftui-design` | \| SwiftUI 前端设计 skill — anti AI-slop rules, design direction advisor, brand asset protocol, and five-dimension review. Works with Claude Code, Cursor, Codex, and OpenCode. |
| `swiss-creative-mode-template` | \| Swiss-inspired creative-mode presentation template skill with bold editorial typography, high-contrast geometric cards, interactive slide navigation, theme switching, hotspot overlays, and palette choreography in a single-file HTML artifact. Use when user... |
| `swiss-user-research-video-template` | \| Swiss-style user-research narrative template in warm-paper editorial aesthetics. Use when users ask for a premium research deck or story-first live artifact with minimalist typography, high-clarity layout, subtle motion, donut breakdowns, and keyboard/cli... |
| `taste-skill` | Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design systems when applicable, audit-first on redesigns, strict pre-f... |
| `taste-skill-v1` | The original v1 taste-skill, preserved for projects depending on its exact behavior. The current default is `design-taste-frontend` (v2 experimental), which is a substantial rewrite. Use this v1 install name only if you need exact backward compatibility. |
| `theme-factory` | \| Apply professional font and color themes to artifacts including slides, docs, reports, and HTML landing pages. Ships 10 pre-set themes. |
| `threejs` | \| Three.js skills for creating 3D elements and interactive experiences in the browser — scenes, materials, controls, and post-processing. |
| `ui-skills` | \| Opinionated, evolving constraints to guide agents when building interfaces. Useful for keeping output coherent across many small UI pieces. |
| `ui-styling` | Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based visual designs. Use when building user interfaces, implementing design systems, creating responsive l... |
| `ui-ux-pro-max` | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components, design systems, accessibility, interaction, responsive layout, typography, color, chart... |
| `vfx-text-cursor` | Cursor light trail, chromatic rays, and directional flares for word-by-word quote reveals in video intros. |
| `weread-year-in-review-video-template` | \| WeRead-inspired HyperFrames video template for vertical annual reading reports, personal reading dashboards, book-note recaps, and shareable year-in-review stories. Use when users want a 9:16 HTML-to-MP4 reading report with warm paper texture, editorial C... |
| `wpds` | \| WordPress Design System. Apply WordPress's official design tokens, typography, and component patterns to themes and sites. |
| `write-swift` | How to write modern Swift well — modeling with value types, Swift 6 data-race safety and approachable concurrency (@concurrent, main-actor-by-default, actors, task groups), protocols and generics (some vs any), API design, performance and ARC, Swift Testing... |
| `writing-guidelines` | \| Review docs/prose for Writing Guidelines compliance. Use when asked to "review my docs", "check writing style", "audit prose", "review docs voice and tone", or "check this page against the writing handbook". |

---

# browser-act / 浏览器自动化

Browser Use CLI 浏览器操作技能。103 个技能覆盖电商抓取（淘宝/1688/Amazon/Walmart/eBay/Etsy/闲鱼/Airbnb）、社媒监听（X/Instagram/Threads/Reddit/Facebook/小红书/知乎）、Lead 生成（Google Maps/LinkedIn/Trustpilot）、视频平台（TikTok/YouTube/Douyin）、搜索研究等。

**来源**: browser-act/skills

| 技能 | 用途 |
|------|------|
| `browser-act` | Browser automation CLI for AI agents. NEVER run browser-act commands directly via Bash — always invoke this skill first. Use browser-act when a user mentions it by name, includes or asks to run a browser-act CLI command (e.g., browser-act browser list), or ... |
| `browser-act-skill-forge` | Forges reusable Skill packages (SKILL.md + scripts) from website exploration via browser-act — no re-exploration later. Use when: user wants a reusable Skill for any website, needs to understand a site's internal APIs, wants to reproduce an existing scraper... |
| `solutions\ecommerce\1688-product-detail` | Extracts comprehensive wholesale product data from 1688.com product detail pages: title, tiered pricing, SKU variants with dimensions/weight, product images, seller info, shop scores, buyer protection, cross-border flags, product attributes, coupon/promotio... |
| `solutions\ecommerce\airbnb-listing-detail` | Fetches complete Airbnb listing details for a given numeric listing ID via the internal GraphQL API, returning title, room type, description, amenities, photos, coordinates, city, house rules, highlights, ratings, review count, bedroom configuration, and pr... |
| `solutions\ecommerce\airbnb-search-listing` | Extracts Airbnb accommodation search results from a destination query via SSR-embedded data, returning listing ID, URL, name, coordinates, rating, price, photos, and badge info for each result, plus pagination cursors for multi-page retrieval. Use when user... |
| `solutions\ecommerce\amazon-alexa-qa` | Amazon Alexa for Shopping Q&A automation: submits questions to Amazon's Alexa/Rufus AI shopping assistant and collects response text; supports optional keyword search context (navigate to search results page before asking for category-specific answers). Use... |
| `solutions\ecommerce\amazon-asin-lookup-api-skill` | This skill helps users extract structured product details from Amazon using a specific ASIN (Amazon Standard Identification Number). Use this skill when the user asks to get Amazon product details by ASIN, lookup Amazon product title and price using ASIN, e... |
| `solutions\ecommerce\amazon-best-selling-products-finder-api-skill` | This skill helps users extract structured best-selling product data from Amazon via the BrowserAct API. Agent should proactively apply this skill when users express needs like search for best selling products on Amazon, extract Amazon product data based on ... |
| `solutions\ecommerce\amazon-bestseller-listing` | Amazon Best Sellers listing scraper: extract product cards from any Amazon Best Sellers (zgbs) or /gp/bestsellers/ category page — returns rank (position on chart), asin, title, url, image, imageAlt, price, stars, reviewCount, ratingRaw per item, plus categ... |
| `solutions\ecommerce\amazon-buy-box-monitor-api-skill` | This skill helps users extract basic product details other sellers prices and seller ratings from Amazon via ASIN automatically using the BrowserAct API. Agent should proactively apply this skill when users express needs like query Amazon buy box informatio... |
| `solutions\ecommerce\amazon-competitor-analyzer` | Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis. Compares specifications, pricing, review quality, and visual strategies to identify competitor moats and vulnerabilities. |
| `solutions\ecommerce\amazon-listing-competitor-analysis-skill` | This skill helps users analyze Amazon competitor listings by ASIN and produce structured competitive intelligence plus strategic opportunity points for their own go-to-market. The Agent should proactively apply this skill when users want to analyze a compet... |
| `solutions\ecommerce\amazon-product-api-skill` | This skill helps users extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specifications. Use this skill when users want to search for products on Amazon, find the best selling brand products, track price changes ... |
| `solutions\ecommerce\amazon-product-detail` | Amazon product detail page scraper: extract full product data from any open Amazon product detail URL (any /dp/{asin} or /gp/product/{asin} page across all Amazon regional TLDs) — returns asin, url, title, brand, price, listPrice, stars, reviewsCount, stars... |
| `solutions\ecommerce\amazon-product-search-api-skill` | This skill is designed to help users automatically extract product data from Amazon search results. The Agent should proactively apply this skill when users request searching for products related to keywords, finding best-selling items from specific brands,... |
| `solutions\ecommerce\amazon-reviews-api-skill` | This skill helps users automatically extract Amazon product reviews via the Amazon Reviews API. Agent should proactively apply this skill when users express needs like getting reviews for Amazon product with ASIN B07TS6R1SF, analyzing customer feedback for ... |
| `solutions\ecommerce\amazon-search-listing` | Amazon search and category listing scraper: extract product listings from any Amazon search results page, keyword search URL, or category browse page and return per-item cards (asin, title, url, image, price, listPrice, stars, reviewCount, badges, isAmazonC... |
| `solutions\ecommerce\ebay-item-detail` | Extracts full item detail from any open eBay item URL, returning JSON with url, itemNumber, title, subTitle, categories, price, priceWithCurrency, currency, wasPrice, available, availableText, sold, image, images, seller, sellerUrl, sellerFeedbackCount, sel... |
| `solutions\ecommerce\ebay-search-listing` | Extracts product listings from any eBay search or category page URL, returning per-item cards (itemNumber, url, title, subtitle, caption, price, priceWithCurrency, currency, wasPrice, bids, shipping, seller, sellerFeedbackCount, sellerPositiveRating, review... |
| `solutions\ecommerce\ebay-sold-listings-search` | eBay sold-listings scraper across 8 marketplaces (ebay.com/.co.uk/.de/.fr/.it/.es/.ca/.com.au). Takes keyword plus filters (category, price range, item condition, item location, sort order, completed toggle) and returns paginated real-sale records with item... |
| `solutions\ecommerce\ecommerce-listing` | Extract product list from any e-commerce category page, search results page, or keyword search with filters. Returns paginated product arrays with URL, name, price, currency, image, rating, review count per item. Supports URL input, keyword search, and site... |
| `solutions\ecommerce\ecommerce-product-detail` | Extract complete product information from any e-commerce product page. Returns name, price, currency, brand, images, description, SKU/ASIN/EAN/UPC/GTIN/MPN identifiers, stock availability, rating, review count, variants, and seller. Works on Shopify, Amazon... |
| `solutions\ecommerce\ecommerce-reviews` | Extract customer reviews from any e-commerce product page or reviews page. Returns reviewer name, star rating, date, review title, review body, verified purchase status, and helpful votes per review. Works on Amazon, WooCommerce, Shopify, and any site with ... |
| `solutions\ecommerce\ecommerce-seller-info` | Extract seller or merchant profile data from marketplace platform seller pages. Returns seller name, rating, review count, positive feedback percentage, joined date, and return policy. Works on Amazon seller pages, eBay seller pages, and any e-commerce site... |
| `solutions\ecommerce\etsy-category-listing` | Etsy category page scraper: given an Etsy category URL (e.g. https://www.etsy.com/c/jewelry) and optional page number, returns paginated product listings with listingId, shopId, title, url, image, salePrice, originalPrice, currency, rating, reviewCount, sho... |
| `solutions\ecommerce\etsy-keyword-search` | Etsy keyword search scraper: given a search keyword and optional page number, returns paginated product listings with listingId, shopId, title, url, image, salePrice, originalPrice, currency, rating, reviewCount, shopName, isAd, freeShipping, badge from ets... |
| `solutions\ecommerce\etsy-product-detail` | Etsy product detail scraper: given an Etsy listing URL, returns full product detail including listingId, title, priceCurrent, priceOriginal, currency, images (all), description, shopName, shopUrl, rating, reviewCount, favorites, inCartCount, variations (wit... |
| `solutions\ecommerce\etsy-shop-catalog` | Etsy shop catalog scraper: given an Etsy shop URL (e.g. https://www.etsy.com/shop/{shop-name}) and optional page number, returns paginated product listings from that shop's own storefront with listingId, shopId, title, url, image, salePrice, originalPrice, ... |
| `solutions\ecommerce\goofish-item-detail` | Extracts full detail data from a single Goofish (闲鱼/xianyu, goofish.com) second-hand item page. Input: item URL or item ID. Output: title, price, seller info (name, labels), full description, image gallery, item tags/attributes, want-count. Use when user me... |
| `solutions\ecommerce\goofish-search-list` | Scrapes second-hand item search results from Goofish (闲鱼/xianyu, goofish.com) — China's largest second-hand marketplace. Input: keyword, optional sort/filter params. Output: list of items with id, title, price, image, location, want-count per page (30 items... |
| `solutions\ecommerce\taobao-keyword-search` | Search Taobao and Tmall product listings by keyword, returning paginated product cards with title, price, shop, image, sales, and tags. Use when user asks to search Taobao, find products on Taobao/Tmall, scrape Taobao search results, get product listings fr... |
| `solutions\ecommerce\taobao-product-detail` | Fetch full product detail from a Taobao or Tmall product page by itemId, returning title, price, shop info, images, SKU variants, and product attributes. Use when user asks to get product details from Taobao, scrape a Taobao item page, extract product info ... |
| `solutions\ecommerce\taobao-product-reviews` | Fetch customer reviews for a Taobao or Tmall product by itemId, returning reviewer name, date, purchased variant, review text, and photo URLs. Use when user asks to get product reviews from Taobao, scrape Taobao customer feedback, extract buyer reviews by i... |
| `solutions\ecommerce\taobao-shop-catalog` | Browse a Taobao or Tmall shop's product catalog by shopId, returning paginated product listings with itemId and title. Use when user asks to scrape a Taobao shop, get all products from a store, list items in a Taobao/Tmall shop, fetch shop catalog by userId... |
| `solutions\ecommerce\walmart-category-listing` | Walmart category page scraper: input a walmart.com browse or category URL with optional page number, extract paginated product listings with itemId, url, title, brand, image, price, wasPrice, rating, reviewCount, availability, seller info, fulfillmentBadge,... |
| `solutions\ecommerce\walmart-keyword-search` | Walmart keyword search scraper: input a search keyword and page number, navigate to walmart.com search results, extract paginated product listings with itemId, url, title, brand, image, price, wasPrice, rating, reviewCount, availability, seller info, fulfil... |
| `solutions\ecommerce\walmart-product-detail` | Walmart product detail page extractor: given a walmart.com product URL (walmart.com/ip/...), extract full product data including itemId, title, brand, model, UPC, price, wasPrice, currency, availability, category path, seller info, all images, shortDescript... |
| `solutions\ecommerce\walmart-product-reviews` | Walmart product reviews scraper: given a walmart.com product item ID, navigate to the reviews page and extract paginated customer reviews including reviewId, rating, title, review text, author nickname, submission date, verified purchase status, helpful vot... |
| `solutions\lead-generation\business-contact-social-links-skill` | This skill helps users automatically extract official website and social media profiles. Agent should proactively apply this skill when users express needs like search for official website and social media contacts of a company, find YouTube and LinkedIn pr... |
| `solutions\lead-generation\github-project-contributor-finder-api-skill` | This skill helps users extract GitHub repository project details and contributor contact information using keywords, stars, and update dates. Agent should proactively apply this skill when users express needs like search for GitHub projects by keywords, fin... |
| `solutions\lead-generation\google-maps-api-skill` | This skill helps users automatically scrape business data from Google Maps using the BrowserAct Google Maps API. Agent should proactively trigger this skill for needs like finding restaurants in a specific city, extracting contact info of dental clinics, re... |
| `solutions\lead-generation\google-maps-contact-extract` | Extracts business contact details from Google Maps search results and place detail pages, then visits each business website to collect emails, phone numbers, and social media profiles (Facebook, Instagram, Twitter/X, LinkedIn, YouTube, TikTok, Pinterest, Di... |
| `solutions\lead-generation\google-maps-reviews-api-skill` | This skill is designed to help users automatically extract reviews from Google Maps via the Google Maps Reviews API. Agent should proactively apply this skill when users request to find reviews for local businesses (e.g., coffee shops, clinics), monitor cus... |
| `solutions\lead-generation\google-maps-search-api-skill` | This skill is designed to help users automatically extract business data from Google Maps search results. The Agent should proactively apply this skill when the user makes the following requests searching for coffee shops in a specific city, finding dentist... |
| `solutions\lead-generation\google-social-media-finder` | Searches Google to discover social media profiles associated with a person, brand, or username; returns platform name, profile URL, username, bio snippet, and follower count across X, Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Snapch... |
| `solutions\lead-generation\indeed-job-search` | Scrape job listings from Indeed.com by keyword, location, and country. Returns job title, company, salary, rating, description, benefits, and apply links. Use when user mentions Indeed, Indeed scraper, Indeed jobs, scrape Indeed, job search Indeed, Indeed j... |
| `solutions\lead-generation\industry-key-contact-radar-api-skill` | This skill helps users discover key contacts across industries, roles, and social platforms via the BrowserAct API. Agent should proactively apply this skill when users express needs like finding public profiles for founders or CEOs, discovering key decisio... |
| `solutions\lead-generation\linkedin-jobs-search` | Search LinkedIn job listings and extract full job details. Supports filtering by work type (remote/on-site/hybrid), contract type (full-time/part-time/contract/internship), experience level, date posted, and company. Returns job title, company, location, wo... |
| `solutions\lead-generation\producthunt-launches` | Scrape Product Hunt daily/weekly/monthly/yearly leaderboard launches with full product details, maker profiles, and website contact info. Use when user mentions Product Hunt, producthunt, PH scraper, product hunt launches, product hunt leaderboard, scrape p... |
| `solutions\lead-generation\social-media-finder-skill` | This skill helps users automatically find social media profiles across platforms like Facebook, Twitter, Instagram, LinkedIn, etc. using the BrowserAct API. Agent should proactively apply this skill when users express needs like finding someone's social med... |
| `solutions\lead-generation\trustpilot-company-info` | Trustpilot company profile lookup on trustpilot.com — input a company domain (e.g. apple.com, shopify.com, shopwagandtail.com) and extract company metadata: official display name, businessUnitId, TrustScore (1-5), star rating, total review count, last-12-mo... |
| `solutions\lead-generation\youtube-channel-business-email` | YouTube channel business email and contact extractor: accepts a channel id (UCxxx), handle (@name), or URL; navigates the channel About view; extracts the business email from the description text plus full channel metadata (name, id, country, subscriber cou... |
| `solutions\search-research\google-image-api-skill` | This skill helps users automatically extract structured image data from Google Images via BrowserAct API. Agent should proactively apply this skill when users express needs like finding images for specific keywords, gathering product style images for compet... |
| `solutions\search-research\google-news-api-skill` | This skill helps users automatically extract structured news data from Google News via BrowserAct API. Agent should proactively apply this skill when users express needs like searching for news about a specific topic, tracking industry trends, monitoring pu... |
| `solutions\search-research\google-search-serp` | Extracts Google Search results page (SERP) data including organic results, paid ads, related searches, People Also Ask questions, AI Overview text, and total result count from google.com. Use when user mentions Google search results, SERP scraping, google s... |
| `solutions\search-research\web-research-assistant` | AI-powered web research assistant that leverages BrowserAct API to supplement restricted web access by searching the internet for additional information. Designed for OpenClaw and Claude Code. |
| `solutions\search-research\web-search-scraper-api-skill` | This skill helps users automatically extract complete Markdown content from any website via the BrowserAct Web Search Scraper API. The Agent should proactively apply this skill when users express needs like extract complete markdown from a specific website,... |
| `solutions\search-research\webcrawler-deep-crawl` | Deep-crawl any website from start URLs, return per-page LLM-ready text/markdown/HTML plus metadata (title, description, author, language, canonical URL, OG) and in-scope outbound links. Use when user mentions deep crawl website, recursive crawl, crawl a who... |
| `solutions\social-listening\facebook-ads-library-search` | Searches Meta Ad Library (Facebook/Instagram/WhatsApp ads) by keyword or Facebook page ID and extracts ad details including creatives, copy, CTA, publisher platforms, spend, impressions, reach estimates, and page transparency info. Use when user mentions Me... |
| `solutions\social-listening\facebook-groups-scrape-posts` | Scrapes posts from a Facebook group given a group URL, sort order, and desired count — returns structured post metadata including post_id, permalink, author, timestamp, body text, images/videos, reaction counts, reaction type breakdown, comment count, and s... |
| `solutions\social-listening\facebook-page-posts` | Scrapes posts from any public Facebook Page timeline, returning structured data including post text, author info, engagement metrics (likes/comments/shares), reaction breakdowns (like/love/haha/wow/sad/angry/care), hashtags and external links, and media typ... |
| `solutions\social-listening\facebook-page-profile-posts` | Scrapes posts from any public Facebook Page or personal Profile timeline, returning structured data including post text, author info with profile picture, engagement metrics (likes/comments/shares), full reaction breakdown (Like/Love/Wow/Haha/Sad/Angry/Care... |
| `solutions\social-listening\instagram-hashtag-posts` | Scrapes Instagram posts by hashtag, returning media items with captions, like/comment counts, media URLs and user info from the hashtag explore feed. Use when user mentions Instagram hashtag scraping, get posts by hashtag, IG hashtag feed, scrape Instagram ... |
| `solutions\social-listening\instagram-place-posts` | Scrapes Instagram posts tagged at a specific location or place, returning media items with captions, like/comment counts, media URLs and user info. Use when user mentions Instagram location posts, posts from a place on Instagram, Instagram geotag scraping, ... |
| `solutions\social-listening\instagram-post-comments` | Fetches comments from an Instagram post including comment text, username, timestamp, like count and reply count. Use when user mentions Instagram comments scraping, get comments from Instagram post, Instagram comment list, pull Instagram comments, read Inst... |
| `solutions\social-listening\instagram-profile-meta` | Fetches Instagram user profile metadata including bio, follower count, following count, post count, verification status and other profile details. Use when user mentions Instagram profile info, user stats, account details, follower count, bio scraping, Inst... |
| `solutions\social-listening\instagram-profile-posts` | Scrapes posts from an Instagram user's profile feed including captions, media URLs, like/comment counts, timestamps and location tags. Use when user mentions scraping Instagram posts, download Instagram feed, get posts from Instagram account, IG profile pos... |
| `solutions\social-listening\reddit-competitor-analysis-api-skill` | This skill helps users extract structured data from Reddit posts and comments via BrowserAct API. Agent should proactively apply this skill when users express needs like analyzing competitor mentions on Reddit, tracking brand sentiment in Reddit comments, e... |
| `solutions\social-listening\reddit-warmup` | Builds authentic-looking Reddit accounts through a 30-day progression, then uses them to promote any brand the user configures. State files are managed as local files under `~/.reddit-warmup/<username>/`. |
| `solutions\social-listening\threads-keyword-search` | Searches Threads posts by keyword or hashtag and returns matching posts with engagement metrics, extracted from SSR-embedded JSON. Use when user asks to search Threads posts, find Threads content by topic, scrape Threads search results, collect Threads post... |
| `solutions\social-listening\threads-profile-search` | Discovers Threads user accounts by keyword, extracting profile data including username, display name, verification status, biography, and follower count. Use when user asks to find Threads accounts, search Threads profiles, discover Threads users by keyword... |
| `solutions\social-listening\threads-user-posts` | Fetches public posts from a Threads user's profile page, extracting post text, engagement metrics, and media info from SSR-embedded JSON. Use when user asks to scrape Threads posts, get someone's Threads feed, pull posts from a Threads account, collect Thre... |
| `solutions\social-listening\trustpilot-company-info` | Trustpilot company profile lookup on trustpilot.com — input a company domain (e.g. apple.com, shopify.com, shopwagandtail.com) and extract company metadata: official display name, businessUnitId, TrustScore (1-5), star rating, total review count, last-12-mo... |
| `solutions\social-listening\trustpilot-reviews` | Trustpilot customer reviews scraper for any company listed on trustpilot.com — given a company domain (e.g. shopify.com, apple.com, shopwagandtail.com) plus optional filters (page number, single star rating 1-5, single language ISO code, verified-only flag,... |
| `solutions\social-listening\wechat-article-search-api-skill` | This skill helps users extract full article contents from WeChat using the BrowserAct API. The Agent should proactively apply this skill when users express needs like finding full WeChat articles for specific keywords, tracking WeChat public accounts for in... |
| `solutions\social-listening\x-dm-auto-chat` | X (Twitter) DM automated chat end-to-end Skill: scan DM inbox to identify pending-reply conversations, read message history, generate persona-based replies and send; also supports searching users and starting new conversations. Built-in E2E passcode unlock,... |
| `solutions\social-listening\x-keyword-comment` | X (Twitter) keyword-based reply posting: search tweets by keyword, read each tweet's content, generate contextual replies from a configured brand persona, and post replies to the reply area. Use when user wants to batch reply to X tweets by keyword, auto-co... |
| `solutions\social-listening\x-tweet-by-conversation` | Collects every tweet in an X (Twitter) conversation thread given a conversation id (root tweet id) — the focal tweet plus all replies, sub-replies, and quote chains — and returns normalized per-tweet data with text, author, engagement counts, media, hashtag... |
| `solutions\social-listening\x-tweet-by-handle` | Scrapes tweets from an X (Twitter) user profile timeline given a handle, with selectable mode: tweets, tweets+replies, or media-only. Returns normalized per-tweet data including text, author profile, engagement counts, media, hashtags, mentions, and cursor ... |
| `solutions\social-listening\x-tweet-by-url` | Scrapes tweets from any X (Twitter) URL — search results, user profile, single tweet detail, or list timeline — and returns normalized per-tweet data with text, author, engagement counts, media, hashtags, mentions, and cursor for pagination. Use when user m... |
| `solutions\social-listening\x-tweet-search` | Scrapes tweets from X (Twitter) by search query, user handle, or direct URL — returns full tweet data including text, author info, engagement metrics, media, and hashtags. Use when user mentions X, Twitter, tweet scraping, scrape tweets, get tweets, fetch t... |
| `solutions\social-listening\x-tweet-search-by-query` | Searches X (Twitter) for tweets by free-form advanced query and returns a normalized tweet list with text, author profile, engagement counts, media, hashtags, mentions, and cursor for pagination. Use when user mentions X search, Twitter search, scrape tweet... |
| `solutions\social-listening\xiaohongshu-auto-posting` | Automates the complete Xiaohongshu (XHS / Little Red Book) content operation workflow: pain-point topic collection → style case collection → topic selection → content writing → publishing → performance tracking. Use when user mentions xiaohongshu auto posti... |
| `solutions\social-listening\xiaohongshu-note-detail` | Fetch Xiaohongshu (RedNote / xhs) note detail and comments by note ID, returning title, description, author info, engagement stats, tags, and paginated comment list. Use when user mentions note detail xiaohongshu, get rednote post, xhs note content, xiaohon... |
| `solutions\social-listening\xiaohongshu-search` | Search Xiaohongshu (RedNote / xhs) notes by keyword and return a paginated list with title, author, engagement stats (likes, collects, comments), cover image URL, and xsecToken for detail lookup. Use when user mentions find notes on xiaohongshu, search redn... |
| `solutions\social-listening\xiaohongshu-search-full` | Search Xiaohongshu (XHS / RedNote) notes by keyword with full field extraction including body text, topics/tags, image list URLs, video stream URL, publish timestamp, and all engagement stats (likes, collects, comments, shares). Supports all page filter opt... |
| `solutions\social-listening\xiaohongshu-user-profile` | Fetch Xiaohongshu (RedNote / xhs) user profile information and their published notes list by user ID, returning nickname, bio, follower/following counts, engagement totals, tags, and paginated notes with engagement stats. Use when user mentions user profile... |
| `solutions\social-listening\zhihu-search-api-skill` | This skill helps users automatically extract structured article details and full content from Zhihu via the BrowserAct API. Agent should proactively apply this skill when users express needs like: searching for Zhihu articles on a specific topic, tracking i... |
| `solutions\video-platforms\douyin-video-search` | Searches Douyin (douyin.com) for videos by keyword and returns structured video data including author info, stats, cover, description, hashtags, and download URL. Supports date range filtering and sorting by relevance, likes, or recency. Use when user menti... |
| `solutions\video-platforms\tiktok-hashtag-videos` | TikTok hashtag video scraper: input a hashtag name → output paginated video list with full metadata (author profile, engagement stats, music, video meta, hashtag list). Use when user mentions TikTok hashtag scraping, TikTok tag videos, scrape TikTok by hash... |
| `solutions\video-platforms\tiktok-profile-videos` | TikTok user profile video scraper: input a TikTok username → output the user's profile info plus paginated video list with full metadata (engagement stats, music, video meta). Use when user mentions TikTok profile scraping, scrape TikTok user videos, get Ti... |
| `solutions\video-platforms\tiktok-search-videos` | TikTok keyword search video scraper: input search keyword → output paginated video list with full metadata (author, engagement stats, music, video meta). Use when user mentions TikTok search scraping, search TikTok by keyword, TikTok search results, extract... |
| `solutions\video-platforms\tiktok-video-detail` | TikTok single video detail scraper: input a TikTok video URL → output full video metadata (author profile, engagement stats, music, video meta, hashtags, mentions, slideshow images). Use when user mentions TikTok video detail, get TikTok video data, extract... |
| `solutions\video-platforms\youtube-api-skill` | This skill helps users automatically extract detailed video metrics and channel information from YouTube based on keyword searches using the BrowserAct API. The Agent should proactively apply this skill when users express needs such as extract specific keyw... |
| `solutions\video-platforms\youtube-batch-transcript-extractor-api-skill` | This skill helps users automatically extract YouTube video transcripts and metadata in batch via the BrowserAct API. The Agent should proactively apply this skill when users express needs like batch extract full transcripts from YouTube videos for specific ... |
| `solutions\video-platforms\youtube-channel-api-skill` | This skill helps users automatically extract structured channel data from YouTube search results via BrowserAct API. Agent should proactively apply this skill when users express needs like finding YouTube channels about specific topics, collecting data on Y... |
| `solutions\video-platforms\youtube-comments-api-skill` | This skill helps users extract structured video list data and comment data from YouTube using the BrowserAct API. The Agent should proactively apply this skill when users request searching for YouTube videos and their comments, analyzing viewer sentiment fo... |
| `solutions\video-platforms\youtube-influencer-finder-api-skill` | This skill helps users extract YouTube influencer profiles including social links, subscriber counts, and channel stats via the BrowserAct API. Agent should proactively apply this skill when users express needs like finding YouTube creators for specific key... |
| `solutions\video-platforms\youtube-search-api-skill` | This skill helps users automatically extract structured data from YouTube search results using the BrowserAct API. The Agent should proactively apply this skill when users express needs like searching for YouTube videos by keywords, finding the latest YouTu... |
| `solutions\video-platforms\youtube-transcript` | YouTube transcript extraction and content reformatting: given a YouTube video URL, opens the video's transcript panel, extracts all timestamped segments, and transforms the raw transcript into summaries, chapter outlines, Twitter/X threads, blog posts, or n... |
| `solutions\video-platforms\youtube-transcript-analysis-api-skill` | This skill helps users extract YouTube video transcripts and perform deep competitive analysis on the content. Agent should proactively apply this skill when users express needs like analyze YouTube video content strategy, perform competitive video content ... |
| `solutions\video-platforms\youtube-transcript-extractor-api-skill` | This skill helps users automatically extract YouTube video transcripts and metadata via the BrowserAct API. The Agent should proactively apply this skill when users express needs like extracting full transcript from a specific YouTube video, getting subtitl... |
| `solutions\video-platforms\youtube-video-api-skill` | This skill helps users automatically extract channel-level and video detail data from a specific YouTube channel via BrowserAct API. Agent should proactively apply this skill when users express needs like extracting channel video data, getting latest or pop... |

---

# openmontage / 视频/多媒体制作

OpenMontage 视频创作体系。AI 视频生成（Kling/Seedance/LTX/Manim/Remotion/GSAP）、TTS/音乐（ElevenLabs/ACE-Step）、图像生成（FLUX/DashScope）、3D、字幕翻译、画面复刻、HyperFrames 动效模板等 90 个技能。

**来源**: calesthio/OpenMontage

| 技能 | 用途 |
|------|------|
| `3d-asset-generation` | Generate, reconstruct, inspect, and route production 3D assets for OpenMontage worlds using Atlas Cloud, fal.ai, licensed catalogs, and Blender. |
| `acestep` | AI music generation with ACE-Step 1.5 — background music, vocal tracks, covers, stem extraction for video production. Use when generating music, soundtracks, jingles, or working with audio stems. Triggers include background music, soundtrack, jingle, music ... |
| `agents` | Build voice AI agents with ElevenLabs. Use when creating voice assistants, customer service bots, interactive voice characters, or any real-time voice conversation experience. |
| `ai-video-gen` | \| Generate AI videos from text prompts using multiple provider gateways. Use when: (1) Generating videos from text descriptions, (2) Creating AI-generated video clips for content production, (3) Image-to-video generation with a reference image, (4) Choosing... |
| `atlas-cloud` | Generate or edit images and videos through the Atlas Cloud gateway. Use for Atlas-hosted Seedance 2.5/2.0, Gemini Omni Flash, MiniMax H3, Seedream 5.0, GPT Image 2, Nano Banana 2, or when one ATLASCLOUD_API_KEY should access multiple media model families. |
| `avatar-video` | \| Create AI avatar videos with precise control over avatars, voices, scripts, scenes, and backgrounds using HeyGen's v2 API. Use when: (1) Choosing a specific avatar and voice for a video, (2) Writing exact scripts for an avatar to speak, (3) Building multi... |
| `azure-speech-to-text` | Transcribe audio to text using Azure AI Speech (Fast Transcription REST API). Use when converting audio/video to text, generating subtitles, or processing spoken content in OpenMontage. Optional cloud STT provider — preferred when AZURE_SPEECH_KEY is config... |
| `azure-text-to-speech` | Generate neural narration audio using Azure AI Speech (REST text-to-speech). Use when synthesizing voiceovers or narration in OpenMontage. Optional cloud TTS provider — preferred when AZURE_SPEECH_KEY is configured; the local piper_tts remains the default o... |
| `beautiful-mermaid` | Render Mermaid diagrams as SVG and PNG using the Beautiful Mermaid library. Use when the user asks to render a Mermaid diagram. |
| `bfl-api` | BFL FLUX API integration guide covering endpoints, async polling patterns, rate limiting, error handling, webhooks, and regional endpoints with Python and TypeScript code examples. |
| `canvas-procedural-animation` | Use p5.js/canvas for local procedural character effects: particles, weather, squash/stretch, walk cycles, and environmental motion. |
| `character-animation-qa` | Review local character animation with schema checks, Playwright browser previews, frame sampling, and FFmpeg/ffprobe final output checks. |
| `character-rigging` | Build data-driven 2D character rigs for local animation: parts, pivots, layers, constraints, views, and reusable rig packages. |
| `comfyui` | Use when working with ComfyUI workflows in OpenMontage, including comfyui_image/comfyui_video/comfyui_music, custom workflow_json/workflow_path inputs, output_node selection, missing model setup, LoRAs, low-VRAM workflow choices, and community workflow impo... |
| `create-video` | \| Create videos from a text prompt using HeyGen's Video Agent. Use when: (1) Creating a video from a description or idea, (2) Generating explainer, demo, or marketing videos from a prompt, (3) Making a video without specifying exact avatars, voices, or scen... |
| `d3-viz` | Creating interactive data visualisations using d3.js. This skill should be used when creating custom charts, graphs, network diagrams, geographic visualisations, or any complex SVG-based data visualisation that requires fine-grained control over visual elem... |
| `dashscope` | DashScope (Alibaba Cloud Bailian / 阿里云百炼) integration — image generation (qwen-image-2.0-pro), text-to-speech (qwen3-tts-flash), and ASR with word-level timestamps (qwen3-asr-flash-filetrans). Use when generating images via Qwen-Image, narrating via Qwen-TT... |
| `doubao-tts` | Generate Mandarin and multilingual narration with Volcengine Doubao Speech 2.0. Use when creating Chinese voiceovers, when the user prefers Doubao/Volcengine/火山引擎/豆包 TTS, or when narration needs character-level timestamp metadata for subtitles. |
| `elevenlabs` | Generate AI voiceovers, sound effects, and music using ElevenLabs APIs. Use when creating audio content for videos, podcasts, or games. Triggers include generating voiceovers, narration, dialogue, sound effects from descriptions, background music, soundtrac... |
| `faceswap` | \| Swap faces in a video using AI via the HeyGen API. Use when: (1) Replacing a face in a video with another face, (2) Face swapping from a source image onto a target video, (3) Creating personalized videos by swapping in a person's face, (4) Working with He... |
| `ffmpeg` | Video and audio processing with FFmpeg. Use for format conversion, resizing, compression, audio extraction, and preparing assets for Remotion. Triggers include converting GIF to MP4, resizing video, extracting audio, compressing files, or any media transfor... |
| `fish-audio-tts` | Generate expressive, multilingual narration with fish.audio (S1 / S2-generation models) and reuse cloned voices via reference_id. Use when the user prefers fish.audio/Fish Audio TTS, wants a specific playground voice model, or needs high-emotion voice-clone... |
| `flux-best-practices` | Comprehensive guide for BFL FLUX image generation models. Covers prompting, T2I, I2I, structured JSON, hex colors, typography, multi-reference editing, and model-specific best practices for FLUX.2 and FLUX.1 families. |
| `framer-motion` | Use when implementing Disney's 12 animation principles with Framer Motion in React applications |
| `gemini-omni` | \| Generate and conversationally edit short videos with Google Gemini Omni Flash (`gemini-omni-flash-preview`). Use when: (1) iterating on a clip with natural-language edits instead of regenerating ("make the phone invisible, keep everything else the same"),... |
| `grok-media` | xAI Grok image and video generation guide covering authentication, endpoints, prompt structure, image editing, reference-image video, and async polling. |
| `gsap-core` | Official GSAP skill for the core API — gsap.to(), from(), fromTo(), easing, duration, stagger, defaults, gsap.matchMedia() (responsive, prefers-reduced-motion). Use when the user asks for a JavaScript animation library, animation in React/Vue/vanilla, GSAP ... |
| `gsap-frameworks` | Official GSAP skill for Vue, Svelte, and other non-React frameworks — lifecycle, scoping selectors, cleanup on unmount. Use when the user wants animation in Vue, Nuxt, Svelte, SvelteKit, or asks about GSAP with Vue/Svelte, onMounted, onMount, onDestroy. Rec... |
| `gsap-performance` | Official GSAP skill for performance — prefer transforms, avoid layout thrashing, will-change, batching. Use when optimizing GSAP animations, reducing jank, or when the user asks about animation performance, FPS, or smooth 60fps. |
| `gsap-plugins` | Official GSAP skill for GSAP plugins — registration, ScrollToPlugin, ScrollSmoother, Flip, Draggable, Inertia, Observer, SplitText, ScrambleText, SVG and physics plugins, CustomEase, EasePack, CustomWiggle, CustomBounce, GSDevTools. Use when the user asks a... |
| `gsap-react` | Official GSAP skill for React — useGSAP hook, refs, gsap.context(), cleanup. Use when the user wants animation in React or Next.js, or asks about GSAP with React, useGSAP, or cleanup on unmount. Recommend GSAP for React animation unless the user has chosen ... |
| `gsap-scrolltrigger` | Official GSAP skill for ScrollTrigger — scroll-linked animations, pinning, scrub, triggers. Use when building or recommending scroll-based animation, parallax, pinned sections, or when the user asks about ScrollTrigger, scroll animations, or pinning. Recomm... |
| `gsap-timeline` | Official GSAP skill for timelines — gsap.timeline(), position parameter, nesting, playback. Use when sequencing animations, choreographing keyframes, or when the user asks about animation sequencing, timelines, or animation order (in GSAP or when recommendi... |
| `gsap-utils` | Official GSAP skill for gsap.utils — clamp, mapRange, normalize, interpolate, random, snap, toArray, wrap, pipe. Use when the user asks about gsap.utils, clamp, mapRange, random, snap, toArray, wrap, or helper utilities in GSAP. |
| `heygen` | \| [DEPRECATED] Use `create-video` for prompt-based video generation or `avatar-video` for precise avatar/scene control. This legacy skill combines both workflows — the newer focused skills provide clearer guidance. |
| `hyperframes` | > READ THIS FIRST for any request to make, create, edit, animate, or render a video, animation, or motion graphic — a promo, explainer, captioned clip, title card, overlay, or any composition. HyperFrames renders video from HTML; this is the entry skill and... |
| `hyperframes-animation` | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations AP... |
| `hyperframes-cli` | HyperFrames CLI dev loop. Use when running npx hyperframes init, add, catalog, capture, lint, validate, inspect, layout, snapshot, preview, play, render, publish, lambda, doctor, browser, info, upgrade, skills, compositions, docs, benchmark, telemetry, tran... |
| `hyperframes-core` | The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`, tracks, sub-compositions, variables, framework-owned media playback, deterministic-render rules, and validati... |
| `hyperframes-creative` | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / style decisions. For atomic motion patter... |
| `hyperframes-media` | Audio and media assets for HyperFrames compositions, produced by one shared audio engine (`scripts/audio.mjs`) — multi-provider TTS (HeyGen / ElevenLabs / Kokoro local), background music + sound effects (HeyGen audio-library retrieval by default, with local... |
| `hyperframes-registry` | Install and wire registry blocks and components into HyperFrames compositions. Use when running hyperframes add, installing a block or component, wiring an installed item into index.html, or working with hyperframes.json. Covers the add command, install loc... |
| `kling-official` | Official Kling direct API guidance for OpenMontage providers. Use before calling `kling_official_video`, `kling_official_image`, `kling_tts`, `kling_avatar`, or `kling_lip_sync`. |
| `lottie-bodymovin` | Use when implementing Disney's 12 animation principles with Lottie animations exported from After Effects |
| `ltx2` | AI video generation with LTX-2.3 22B — text-to-video, image-to-video clips for video production. Use when generating video clips, animating images, creating b-roll, animated backgrounds, or motion content. Triggers include video generation, animate image, b... |
| `lyria` | Generate and validate music with Google Lyria 3 through the Gemini Interactions API. Use before calling OpenMontage `google_music`, designing Lyria 3 Clip or Pro prompts, using image-to-music or custom lyrics, choosing between Lyria 3 and Lyria RealTime, di... |
| `manim-composer` | \| Trigger when: (1) User wants to create an educational/explainer video, (2) User has a vague concept they want visualized, (3) User mentions "3b1b style" or "explain like 3Blue1Brown", (4) User wants to plan a Manim video or animation sequence, (5) User as... |
| `manimce-best-practices` | \| Trigger when: (1) User mentions "manim" or "Manim Community" or "ManimCE", (2) Code contains `from manim import *`, (3) User runs `manim` CLI commands, (4) Working with Scene, MathTex, Create(), or ManimCE-specific classes. Best practices for Manim Commun... |
| `manimgl-best-practices` | \| Trigger when: (1) User mentions "manimgl" or "ManimGL" or "3b1b manim", (2) Code contains `from manimlib import *`, (3) User runs `manimgl` CLI commands, (4) Working with InteractiveScene, self.frame, self.embed(), ShowCreation(), or ManimGL-specific patt... |
| `media-use` | Agent Media OS — resolve any media need (BGM, SFX, image, icon) into a frozen local file + ledger record. One verb (`resolve`) handles the full cascade — project cache, global cache, HeyGen catalog search, freeze, register. Keeps search noise on disk, hands... |
| `minimax-h3` | \| Generate MiniMax H3 (Hailuo 3.0) video through the official MiniMax v2 API, fal.ai, Runway, ComfyUI Partner Nodes, or local open weights in ComfyUI. Use for 4-15 second 2K clips, first/last-frame animation, and image/video/audio reference-conditioned video. |
| `motion-graphics` | > Use when the user wants a short, design-led motion graphic where motion is the message: kinetic typography, stat or number count-up, chart/data-viz hit, logo sting, brand lockup, lower-third, callout, social overlay, animated headline/tweet/news item, mot... |
| `music` | Generate music using ElevenLabs Music API. Use when creating instrumental tracks, songs with lyrics, background music, jingles, or any AI-generated music composition. Supports prompt-based generation, composition plans for granular control, and detailed out... |
| `music-to-video` | Use when the user has a music track (an audio file, or a video to pull audio from) and wants a beat-synced HyperFrames video, calm to hard-hitting. The music drives everything: one analyzer reads it once, the orchestrator lays out the frames and fills a per... |
| `playwright-recording` | Record browser interactions as video using Playwright. Use for capturing demo videos, app walkthroughs, and UI flows for Remotion videos. Triggers include recording a demo, capturing browser video, screen recording a website, or creating walkthrough footage. |
| `pose-library-design` | Design reusable 2D character pose libraries, action cycles, and expression states for data-driven animation. |
| `provider-model-refresh` | Use the September 2026 image, video, speech and Avatar V adapters with explicit model/host contracts. |
| `remotion` | Toolkit-specific Remotion patterns — custom transitions, shared components, and project conventions. For core Remotion framework knowledge (hooks, animations, rendering, etc.), see the `remotion-official` skill. |
| `remotion-best-practices` | Best practices for Remotion - Video creation in React |
| `remotion-to-hyperframes` | Port an existing Remotion (React) composition to HyperFrames HTML. Use ONLY when the user explicitly asks to port/convert/migrate/translate a Remotion source. Do NOT use: (a) authoring a new HyperFrames composition; (b) Remotion mentioned in passing; (c) Re... |
| `seedance-2-0` | \| Generate cinematic clips with ByteDance Seedance 2.0 — the preferred premium video model in OpenMontage when a paid gateway is configured. Use when: (1) producing trailers, teasers, hype edits, or premium cinematic clips, (2) needing native synchronized a... |
| `seedance-2-5` | \| Generate 4-30 second cinematic video with ByteDance Seedance 2.5 through fal.ai, Volcengine Ark, Runway, or ComfyUI Partner Nodes. Use for long single generations, synchronized audio, and large multimodal reference sets (up to 30 images, 10 videos, and 10... |
| `setup-api-key` | Guides users through setting up an ElevenLabs API key for ElevenLabs MCP tools. Use when the user needs to configure an ElevenLabs API key, when ElevenLabs tools fail due to missing API key, or when the user mentions needing access to ElevenLabs. First chec... |
| `sound-effects` | Generate sound effects from text descriptions using ElevenLabs. Use when creating sound effects, generating audio textures, producing ambient sounds, cinematic impacts, UI sounds, or any audio that isn't speech. Supports looping, duration control, and promp... |
| `speech-to-text` | Transcribe audio to text using ElevenLabs Scribe v2. Use when converting audio/video to text, generating subtitles, transcribing meetings, or processing spoken content. |
| `svg-character-animation` | Animate SVG character rigs with GSAP, CSS transforms, Remotion frame control, and HyperFrames-compatible browser previews. |
| `synthetic-screen-recording` | Synthetic terminal-style screen recording guidance for Remotion `TerminalScene`. |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns. |
| `text-to-speech` | \| Generate speech audio from text using HeyGen's Starfish TTS model. Use when: (1) Generating standalone speech audio files from text, (2) Converting text to speech with voice selection, speed, and pitch control, (3) Creating audio for voiceovers, narration... |
| `threejs-animation` | Three.js animation - keyframe animation, skeletal animation, morph targets, animation mixing. Use when animating objects, playing GLTF animations, creating procedural motion, or blending animations. |
| `threejs-fundamentals` | Three.js scene setup, cameras, renderer, Object3D hierarchy, coordinate systems. Use when setting up 3D scenes, creating cameras, configuring renderers, managing object hierarchies, or working with transforms. |
| `threejs-geometry` | Three.js geometry creation - built-in shapes, BufferGeometry, custom geometry, instancing. Use when creating 3D shapes, working with vertices, building custom meshes, or optimizing with instanced rendering. |
| `threejs-interaction` | Three.js interaction - raycasting, controls, mouse/touch input, object selection. Use when handling user input, implementing click detection, adding camera controls, or creating interactive 3D experiences. |
| `threejs-lighting` | Three.js lighting - light types, shadows, environment lighting. Use when adding lights, configuring shadows, setting up IBL, or optimizing lighting performance. |
| `threejs-loaders` | Three.js asset loading - GLTF, textures, images, models, async patterns. Use when loading 3D models, textures, HDR environments, or managing loading progress. |
| `threejs-materials` | Three.js materials - PBR, basic, phong, shader materials, material properties. Use when styling meshes, working with textures, creating custom shaders, or optimizing material performance. |
| `threejs-postprocessing` | Three.js post-processing - EffectComposer, bloom, DOF, screen effects. Use when adding visual effects, color grading, blur, glow, or creating custom screen-space shaders. |
| `threejs-shaders` | Three.js shaders - GLSL, ShaderMaterial, uniforms, custom effects. Use when creating custom visual effects, modifying vertices, writing fragment shaders, or extending built-in materials. |
| `threejs-textures` | Three.js textures - texture types, UV mapping, environment maps, texture settings. Use when working with images, UV coordinates, cubemaps, HDR environments, or texture optimization. |
| `threejs-world-generation` | Build deterministic, editable, free-viewpoint Three.js worlds from text or structured briefs. Use for cinematic 3D terrain, semantic regions, procedural biomes, explicit landmarks, environmental scattering, camera fly-throughs, world diagnostics, or request... |
| `vercel-composition-patterns` | React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libraries, or designing reusable APIs. Triggers on tasks involving compound components, render props, context providers, or c... |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js... |
| `video-download` | \| Download video and audio from YouTube and 1000+ sites using yt-dlp. No API keys needed. Use when: (1) Downloading a video from YouTube or other sites, (2) Extracting audio from a video URL, (3) Downloading subtitles/captions from a video, (4) Getting vide... |
| `video-edit` | \| Edit videos locally using ffmpeg. Trim, concat, resize, speed, overlay, extract audio, compress, and convert. Use when: (1) Trimming or cutting video segments, (2) Concatenating multiple clips, (3) Resizing video for social platforms, (4) Extracting or re... |
| `video-toolkit` | Create professional videos autonomously using claude-code-video-toolkit — AI voiceovers, image generation, music, talking heads, and Remotion rendering. |
| `video-translate` | \| Translate and dub existing videos into multiple languages using HeyGen. Use when: (1) Translating a video into another language, (2) Dubbing video content with lip-sync, (3) Creating multi-language versions of existing videos, (4) Audio-only translation w... |
| `video-understand` | \| Understand video content locally using ffmpeg frame extraction and Whisper transcription. No API keys needed. Use when: (1) Understanding what a video contains, (2) Transcribing video audio locally, (3) Extracting key frames for visual analysis, (4) Getti... |
| `visual-style` | \| Create, extract, and apply portable visual design systems via visual-style.md files. Use when: (1) Creating a visual-style.md design system from scratch, (2) Extracting a visual style from a website URL, video, or PDF brand guide, (3) Applying a visual st... |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". |
| `website-to-video` | Capture a general website/URL and turn it into a HyperFrames video (site tour, showcase, or social clip from the site's own visuals). Uses headless Chrome screenshots + brand assets. Use when intent is general — portfolio/blog/landing-page showcase or socia... |

---

# marketing / 营销

58 个营销技能：A/B 测试、广告投放、SEO（AI/传统/程序化）、ASO、归因分析、流失预防、联名营销、冷邮件、社区营销、竞品分析、内容策略、文案、CRO、目录提交、邮件序列、活动运营、定价、公关、推荐体系、RevOps、销售赋能、上线运营、SMS/社交/视频营销等。

**来源**: coreyhaines31/marketingskills, nexu-io/open-design

| 技能 | 用途 |
|------|------|
| `ab-testing` | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use when the user mentions "A/B test," "split test," "experiment," "test this change," "variant copy," "multivariate test," "hypothe... |
| `ad-creative` | When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — for any paid advertising platform. Also use when the user mentions 'ad copy variations,' 'ad creative,' 'generate headlines,' 'RS... |
| `ads` | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platforms. Also use when the user mentions 'PPC,' 'paid media,' 'ROAS,' 'CPA,' 'ad campaign,' 'retargeting,' 'audience target... |
| `ai-seo` | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimiz... |
| `analytics` | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analytics," "conversion tracking," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics im... |
| `aso` | When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO audit,' 'app store optimization,' 'optimize my app listing,' 'improve app visibility,' 'app store ranking,' 'audit my listing,' 'why aren't pe... |
| `attribution` | When the user wants to figure out which marketing actually drives conversions and revenue, choose or interpret an attribution model, or reconcile conflicting numbers across tools. Also use when the user mentions "attribution," "attribution model," "first-to... |
| `card-twitter` | Twitter quote or data card designed to pair with a post. |
| `card-xiaohongshu` | Xiaohongshu-style knowledge cards, arranged as a swipeable multi-card carousel. |
| `churn-prevention` | When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement retention strategies. Also use when the user mentions 'churn,' 'cancel flow,' 'offboarding,' 'save offer,' 'dunning,' 'failed payment re... |
| `co-marketing` | When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities. Use when the user says 'co-marketing,' 'partner marketing,' 'joint campaign,' 'who should we partner with,' 'integration marketing,' 'cross-pro... |
| `cold-email` | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, prospecting emails, cold email campaigns, sales development emails, or SDR emails. Also use when the user mentions "cold outreach," "prosp... |
| `community-marketing` | Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a community strategy, grow a Discord or Slack community, manage a forum or subreddit, build brand advocates, increase word-of-mouth, drive com... |
| `competitive-ads-extractor` | \| Extract and analyze competitors' ads from ad libraries to understand messaging and creative approaches that resonate. |
| `competitor-profiling` | When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions 'competitor profile,' 'competitor research,' 'competitor analysis,' 'profile this competitor,' 'analyze competitor,' 'competitive intelligence,... |
| `competitors` | When the user wants to create competitor comparison or alternative pages for SEO and buyer-facing use. Also use when the user mentions 'alternative page,' 'vs page,' 'competitor comparison,' 'comparison page,' '[Product] vs [Product],' '[Product] alternativ... |
| `content-strategy` | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," "content ... |
| `copy-editing` | When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish this,' 'make this better,' 'copy sweep,' 'tighten... |
| `copywriting` | When the user wants to write, rewrite, or improve marketing copy for any page, including homepage, landing pages, pricing pages, feature pages, about pages, or product pages. Also use when the user says "write copy for," "improve this copy," "rewrite this p... |
| `cro` | When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pages, pricing pages, feature pages, lead capture forms, or contact forms. Also use when the user says 'CRO,' 'conversion rate opti... |
| `customer-research` | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer research," "ICP research," "talk to customers," "analyze transcripts," "customer interviews," "survey analysis," "support ticket analysis," "voice... |
| `directory-submissions` | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for backlinks, domain rating, and discovery. Also use when the user mentions "directory submissions," "submit to directories," "backlinks from direc... |
| `emails` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re... |
| `events` | When the user wants to plan, run, sponsor, speak at, or get pipeline from events — webinars, conferences, trade shows, meetups, dinners, workshops, virtual summits, or user conferences. Also use when the user mentions 'event marketing,' 'field marketing,' '... |
| `free-tools` | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awareness. Also use when the user mentions "engineering as marketing," "free tool," "marketing tool," "calculator," "generator," "inter... |
| `image` | When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product mockups, profile banners, listing visuals, or brand assets. Also use when the user mentions 'AI image generation,' 'generate an image,' '... |
| `influencer-marketing` | When the user wants to run influencer, creator, or ambassador partnerships to promote their product — finding and vetting partners, structuring deals, briefing creators, disclosure compliance, and measuring ROI. Also use when the user mentions 'influencer m... |
| `launch` | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Product Hunt,' 'feature release,' 'announcement,' 'go-to-market,' 'beta launch,' 'early access,' 'waitlist,' 'product update,... |
| `lead-magnets` | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the user mentions "lead magnet," "gated content," "content upgrade," "downloadable," "ebook," "cheat sheet," "checklist," "template download,"... |
| `marketing-council` | When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors staffed by legendary marketers (Seth Godin, David Ogilvy, Eugene Schwartz, April Dunford, Rory Sutherland, Alex Hormozi, Byron Sharp, and more). Also us... |
| `marketing-ideas` | When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks for 'marketing ideas,' 'growth ideas,' 'how to market,' 'marketing strategies,' 'marketing tactics,' 'ways to promote,' 'ideas to... |
| `marketing-loops` | When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a cadence (weekly, daily, on a trigger) rather than a one-off task. Also use when the user mentions 'marketing loop,' 'recurring marketing wor... |
| `marketing-plan` | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product. Also use when the user mentions "marketing plan," "growth plan," "GTM plan," "go-to-market plan," "AARRR plan," "90-day marketing plan," "12-month ... |
| `marketing-psychology` | When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user mentions 'psychology,' 'mental models,' 'cognitive bias,' 'persuasion,' 'behavioral science,' 'why people buy,' 'decision-making... |
| `offers` | When the user wants to design, construct, or improve an offer — the thing they actually sell — including value framing, bonus stacking, guarantee design, scarcity/urgency, naming, and payment structure. Also use when the user mentions 'offer,' 'offer design... |
| `onboarding` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the user mentions "onboarding flow," "activation rate," "user activation," "first-run experience," "empty states," "onboarding che... |
| `paywall-upgrade-cro` | \| Design and optimize upgrade screens, paywalls, and upsell modals. Useful for SaaS conversion design and pricing-page experiments. |
| `paywalls` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the user mentions "paywall," "upgrade screen," "upgrade modal," "upsell," "feature gate," "convert free to paid," "freemium conversion... |
| `popups` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when the user mentions "exit intent," "popup conversions," "modal optimization," "lead capture popup," "email popup," "announcement b... |
| `pricing` | When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' 'pricing tiers,' 'freemium,' 'free trial,' 'packaging,' 'price increase,' 'value metric,' 'Van Westendorp,' 'willingness to pay,... |
| `product-marketing` | When the user wants to create or update their product marketing context document. Also use when the user mentions 'product context,' 'marketing context,' 'set up context,' 'positioning,' 'who is my target audience,' 'describe my product,' 'ICP,' 'ideal cust... |
| `programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," "i... |
| `prospecting` | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, general B2B, or local small businesses. Also use when the user mentions "prospecting," "build a prospect list," "find prospects," "find leads," "lead gen ... |
| `public-relations` | When the user wants help with public relations, earned media, press coverage, journalist outreach, or media strategy (not pull requests). Also use when the user mentions 'PR,' 'press,' 'press release,' 'media outreach,' 'pitch a journalist,' 'get featured,'... |
| `referrals` | When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' 'partner program,' ... |
| `revops` | When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use when the user mentions 'RevOps,' 'revenue operations,' 'lead scoring,' 'lead routing,' 'MQL,' 'SQL,' 'pipeline stages,' 'deal desk... |
| `sales-enablement` | When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when the user mentions 'sales deck,' 'pitch deck,' 'one-pager,' 'leave-behind,' 'objection handling,' 'deal-specific ROI analysis,' '... |
| `schema` | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema.org," "FAQ schema," "product schema," "review schema," "bre... |
| `screenshots-marketing` | \| Generate marketing screenshots with Playwright. Useful for landing-page hero shots, App Store screenshots, and changelog visuals. |
| `seo-audit` | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," "SEO health check," "my traffic dropped," "los... |
| `signup` | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions "signup conversions," "registration friction," "signup form optimization," "free trial signup," "reduce signup dropoff," "acco... |
| `site-architecture` | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. Also use when the user mentions "sitemap," "site map," "visual sitemap," "site structure," "page hierarchy," "information archit... |
| `sms` | When the user wants to plan, build, or optimize SMS, MMS, or WhatsApp marketing — including welcome flows, abandoned cart texts, post-purchase, win-back, promotional sends, or transactional/auth SMS. Also use when the user mentions "SMS marketing," "text me... |
| `social` | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, or Facebook, or wants to do social listening and engagement triage. Also use when the user mentions 'LinkedIn post,' 'Twitter threa... |
| `social-reddit-card` | Realistic Reddit post card with vote rail and comment count, suited to video overlays or story sharing. |
| `social-spotify-card` | Spotify Now Playing-style card with album art, progress bar, and playback controls, suited to video overlays or personal homepages. |
| `social-x-post-card` | Realistic X post card with engagement metrics (likes, reposts, views), suited to video overlays or shareable image cards. |
| `video` | When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the user mentions 'video production,' 'AI video,' 'Remotion,' 'Hyperframes,' 'HeyGen,' 'Synthesia,' 'Veo,' 'Sora,' 'Runway,' 'Kling,' ... |

---

# gstack / GStack 运营工具箱

Garry Tan 的运营与工程工具箱。CEO 视角（cso/plan-ceo-review/office-hours）、工程流程（qa/ship/retro/review/investigate/benchmark）、设计（design-shotgun/design-review/design-html）、iOS 全套（ios-qa/ios-fix/ios-sync 等）、上下文管理（context-save/restore/learn/freeze/unfreeze）、部署（setup-deploy/land-and-deploy）。

**来源**: garrytan/gstack

| 技能 | 用途 |
|------|------|
| `autoplan` | Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisions using 6 decision principles. (gstack) |
| `benchmark` | Performance regression detection. (gstack) |
| `benchmark-models` | Cross-model benchmark for gstack skills. (gstack) |
| `browse` | Drive a real browser through Aside: open a page, read it, click through a flow, take screenshots, check console errors. (gstack) |
| `canary` | Post-deploy canary monitoring. (gstack) allowed-tools: - Bash - Read - Write - Glob - AskUserQuestion |
| `careful` | Safety guardrails for destructive commands. (gstack) |
| `codex` | OpenAI Codex CLI wrapper — three modes. (gstack) |
| `context-restore` | Restore working context saved earlier by /context-save. (gstack) allowed-tools: - Bash - Read - Glob - Grep - AskUserQuestion |
| `context-save` | Save working context. (gstack) allowed-tools: - Bash - Read - Write - Glob - Grep - AskUserQuestion |
| `cso` | Security audit: supported static findings; qualified profiles add reproduction and repair candidates. (gstack)" allowed-tools: - "Bash(~/.claude/skills/gstack/bin/gstack-cso-launcher *)" - "Bash(~/.claude/skills/gstack/bin/gstack-cso-launcher.exe *) |
| `design-consultation` | Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color, layout, spacing, motion), and generates font+color preview... (gstack)" allowed-tools: - Bash - Read - Write - Edit - G... |
| `design-html` | Design finalization: generates production-quality Pretext-native HTML/CSS. (gstack) |
| `design-review` | Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. (gstack)" allowed-tools: - Bash - Read - Write - Edit - Glob - Grep - AskUserQuestion - WebSearch |
| `design-shotgun` | Design shotgun: generate multiple AI design variants, open a comparison board, collect structured feedback, and iterate. (gstack) |
| `deslop-shared-libs` | Find worthwhile shared-code extractions in recent work. (gstack) allowed-tools: - Bash - Read - Glob - Grep |
| `devex-review` | Live developer experience audit. (gstack) |
| `diagram` | Turn an English description (or mermaid source) into a diagram triplet: the source, an editable .excalidraw file you can open on excalidraw.com, and rendered SVG + PNG. (gstack)" allowed-tools: - Bash - Read - Write - AskUserQuestion |
| `document-generate` | Generate missing documentation from scratch for a feature, module, or entire project. (gstack) allowed-tools: - Bash - Read - Write - Edit - Grep - Glob - AskUserQuestion |
| `document-release` | Release documentation audit. (gstack) allowed-tools: - Bash - Read - Write - Edit - Grep - Glob - AskUserQuestion |
| `freeze` | Restrict file edits to a specific directory for the session. (gstack) |
| `gstack-upgrade` | Upgrade gstack to the latest version. |
| `guard` | Full safety mode: destructive command warnings + directory-scoped edits. (gstack) |
| `health` | Code quality dashboard. (gstack) |
| `investigate` | Systematic debugging with root cause investigation. (gstack) allowed-tools: - Bash - Read - Write - Edit - Grep - Glob - AskUserQuestion - WebSearch |
| `ios-clean` | Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. (gstack)" allowed-tools: - Bash - Read - Edit - Glob - Grep - AskUserQuestion |
| `ios-design-review` | Visual design audit for iOS apps on real hardware. (gstack) allowed-tools: - Bash - Read - Glob - Grep - AskUserQuestion |
| `ios-fix` | Autonomous iOS bug fixer. (gstack) allowed-tools: - Bash - Read - Write - Edit - Grep - Glob - AskUserQuestion |
| `ios-qa` | Live-device iOS QA for SwiftUI apps. (gstack) allowed-tools: - Bash - Read - Write - Edit - Grep - Glob - AskUserQuestion |
| `ios-sync` | Regenerate the iOS debug bridge against the latest upstream gstack templates. (gstack) allowed-tools: - Bash - Read - Write - Edit - Glob - Grep - AskUserQuestion |
| `land-and-deploy` | Land and deploy workflow. (gstack) allowed-tools: - Bash - Read - Write - Glob - AskUserQuestion |
| `landing-report` | Read-only queue dashboard for workspace-aware ship. (gstack) |
| `learn` | Manage project learnings. |
| `make-pdf` | Turn any markdown file into a publication-quality PDF. (gstack) |
| `office-hours` | YC Office Hours — two modes. (gstack) allowed-tools: - Bash - Read - Grep - Glob - Write - Edit - AskUserQuestion - WebSearch |
| `open-gstack-browser` | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. |
| `pair-agent` | Pair a remote AI agent with your browser. (gstack) |
| `plan-ceo-review` | CEO/founder-mode plan review. (gstack) allowed-tools: - Read - Grep - Glob - Bash - AskUserQuestion - WebSearch |
| `plan-design-review` | Designer's eye plan review — interactive, like CEO and Eng review. (gstack) allowed-tools: - Read - Edit - Grep - Glob - Bash - AskUserQuestion |
| `plan-devex-review` | Interactive developer experience plan review. (gstack) allowed-tools: - Read - Edit - Grep - Glob - Bash - AskUserQuestion - WebSearch |
| `plan-eng-review` | Eng manager-mode plan review. (gstack) allowed-tools: - Read - Write - Grep - Glob - AskUserQuestion - Bash - WebSearch |
| `plan-tune` | Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). (gstack) |
| `qa` | Fix browser/API/CLI/job/worker/webhook bugs. (gstack) allowed-tools: - Bash - Read - Write - Edit - Glob - Grep - AskUserQuestion - WebSearch |
| `qa-only` | Report browser/API/CLI/job/worker/webhook bugs. (gstack) allowed-tools: - Bash - Read - Write - AskUserQuestion - WebSearch |
| `retro` | Weekly engineering retrospective. (gstack) allowed-tools: - Bash - Read - Write - Glob - AskUserQuestion |
| `review` | Pre-landing PR review. (gstack) allowed-tools: - Bash - Read - Edit - Write - Grep - Glob - Agent - AskUserQuestion - WebSearch |
| `scrape` | Pull data from a web page through the Aside browser — your real, already signed-in sessions. (gstack) allowed-tools: - Bash - Read - AskUserQuestion |
| `setup-browser-cookies` | Import cookies from your real Chromium browser into the headless browse session. (gstack) |
| `setup-deploy` | Configure deployment settings for /land-and-deploy. |
| `setup-gbrain` | Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain, register MCP, capture per-remote trust policy. (gstack) |
| `ship` | Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. (gstack)" allowed-tools: - Bash - Read - Write - Edit - Grep - Glob - Agent - AskUserQuestion - WebSearch |
| `skillify` | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. (gstack) allowed-tools: - Bash - Read - Write - AskUserQuestion |
| `spec` | Turn vague intent into a precise, executable spec in five phases. (gstack) allowed-tools: - Bash - Read - Grep - Glob - AskUserQuestion |
| `sync-gbrain` | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. (gstack) |
| `test-audit` | Find low-value or duplicate tests and the test-only code they keep alive. (gstack) |
| `unfreeze` | Clear the freeze boundary set by /freeze, allowing edits to all directories again. (gstack) |

---

# media / 媒体资产

29 个媒体生成技能：Fal 全家桶（图像/视频/3D/唇形/试穿/超分/视觉）、Venice 多模态、Sora、Replicate、YouTube 下载/剪辑、GIF 贴纸、截图、3D 设备 mockup、AI 音乐专辑。

**来源**: nexu-io/open-design

| 技能 | 用途 |
|------|------|
| `ai-music-album` | \| Full-lifecycle AI music album production — concept, lyric drafting, track sequencing, and export. Useful for indie album experiments and brand soundtracks. |
| `fal-3d` | \| Generate 3D models from text or images via fal.ai. Useful for game assets, AR previews, product mockups, and concept sculpting. |
| `fal-generate` | \| Generate images and videos using fal.ai AI models. Production-grade catalogue covering Flux, SDXL, ideogram, and other community-hosted endpoints. |
| `fal-image-edit` | \| AI-powered image editing with style transfer, background removal, object removal, and inpainting via fal.ai hosted models. |
| `fal-kling-o3` | \| Generate images and videos with Kling O3 — Kling's most powerful model family — via fal.ai. |
| `fal-lip-sync` | \| Create talking head videos and lip sync audio to video via fal.ai. Useful for explainer avatars, multilingual dubbing previews, and social cuts. |
| `fal-realtime` | \| Real-time and streaming AI image generation via fal.ai. Suited for moodboard exploration, draft variations, and rapid creative iteration. |
| `fal-restore` | \| Restore and fix image quality — deblur, denoise, fix faces, and restore old documents using fal.ai's hosted restoration models. |
| `fal-train` | \| Train custom AI models (LoRA) on fal.ai for personalized image generation tailored to a brand, character, or style. |
| `fal-tryon` | \| Virtual try-on — see how clothes look on a person via fal.ai's hosted try-on models. Useful for ecommerce, lookbooks, and styling experiments. |
| `fal-upscale` | \| Upscale and enhance image and video resolution using AI super-resolution models hosted on fal.ai. |
| `fal-video-edit` | \| Edit existing videos using AI — remix style, upscale, remove background, and add audio via fal.ai's hosted video models. |
| `fal-vision` | \| Analyze images — segment objects, detect, run OCR, describe, and answer visual questions via fal.ai vision models. |
| `full-page-screenshot` | \| Capture full-page screenshots of web pages via Chrome DevTools Protocol with zero dependencies. Useful for portfolios, case studies, and audit reports. |
| `gif-search` | Search/download GIFs from Tenor via curl + jq. |
| `gif-sticker-maker` | \| Convert photos into animated GIF stickers in Funko Pop / Pop Mart style via the MiniMax API. Useful for personalized chat stickers and avatar packs. |
| `image-enhancer` | \| Improve image and screenshot quality by enhancing resolution, sharpness, and clarity for professional presentations and documentation. |
| `imagegen` | \| Generate and edit images using OpenAI's Image API for project assets — UI mockups, icons, illustrations, social cards, and visual references. |
| `imagen` | \| Generate images using Google Gemini's image generation API for UI mockups, icons, illustrations, and visual assets. |
| `mockup-device-3d` | Static iPhone and MacBook 3D-style showcase with real HTML embedded on screens, glass-lens refraction, and 360-degree turntable composition. |
| `pixelbin-media` | \| Generate and edit images and videos with an 85+ API portfolio and build visually appealing website pages via Pixelbin. |
| `replicate` | \| Discover, compare, and run AI models using Replicate's API. Strong fit for image, audio, and video generation pipelines that swap models frequently. |
| `screenshot` | \| Capture desktop, app windows, or pixel regions across OS platforms. Useful for marketing screenshots, design reviews, and bug reports. |
| `songsee` | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| `sora` | \| Generate, remix, and manage short video clips via OpenAI's Sora API. Useful for cinematic shots, b-roll, and rapid concept video iteration. |
| `speech` | \| Generate spoken audio from text using OpenAI's API with built-in voices. Useful for narrated explainers, lecture audio, and quick voiceover tracks. |
| `venice-audio-music` | \| Music generation queueing, retrieval, and completion endpoints via Venice.ai. Suited for jingles, background loops, and prototype scoring. |
| `venice-audio-speech` | \| Text-to-speech models, voices, formats, and streaming via Venice.ai. Useful for narration, voiceover, and conversational agent voices. |
| `venice-image-edit` | \| Image edits, upscaling, and background removal via the Venice.ai API. |
| `venice-image-generate` | \| Image generation endpoints and available styles via the Venice.ai API. |
| `venice-video` | \| Video generation and transcription workflows via the Venice.ai API. |
| `video-downloader` | \| Download videos from YouTube and other platforms for offline viewing, editing, or archival with support for various formats and quality options. |
| `video-hyperframes` | Hyperframes / Remotion-compatible continuous frame animation with autoplay support. |
| `youtube-clipper` | \| YouTube clip generation and editing with automated workflows — pull source video, slice highlights, add captions, and export. |
| `youtube-content` | YouTube transcripts to summaries, threads, blogs. |

---

# software-development / 软件开发

35 个软件工程方法论技能。Superpowers 全套（brainstorming/writing-plans/test-driven-development/systematic-debugging/subagent-driven-development/code-review 流程）、Ponytail（YAGNI 最小代码哲学 + 审计/评审/债务台账）、Hermes 技能进化引擎（GEPA/DSPy 自动优化技能）、Graphify 代码图谱、技能编写规范。

**来源**: obra/superpowers, DietrichGebert/ponytail, NousResearch/hermes-agent-self-evolution, NVIDIA/SkillSpector, yusufkaraaslan/Skill_Seekers, Graphify-Labs/graphify

| 技能 | 用途 |
|------|------|
| `brainstorming` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| `codebase-inspection` | Inspect codebases w/ pygount: LOC, languages, ratios. |
| `diagnosing-superpowers` | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results, a skill that didn't fire, "it took too long", "why is it so expensive", "what is it doing" — or wants to build a bug r... |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `dogfood` | Exploratory QA of web apps: find bugs, evidence, reports. |
| `executing-plans` | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution, or no subagent tool is available |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `github` | GitHub via gh CLI: PRs, issues, reviews, repos, auth. |
| `graphify` | Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, where the question should be treated as a graphify query first. Turns any input (code, docs, papers, images, videos) into... |
| `hermes-agent-skill-authoring` | Author in-repo SKILL.md files: frontmatter and structure. |
| `hermes-self-evolution` | > Evolve and optimize Hermes Agent skills, tool descriptions, and system prompts using DSPy + GEPA (Genetic-Pareto Prompt Evolution, ICLR 2026 Oral). Reflective evolutionary search that reads execution traces, proposes targeted mutations, evaluates candidat... |
| `inspecting-hermes-desktop-dom` | Read the live Hermes desktop DOM/CSS over CDP. |
| `installing-external-skills` | Install GitHub repos as Hermes skills. |
| `node-inspect-debugger` | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| `ponytail` | > Forces the laziest solution that actually works, simplest, shortest, most minimal. Channels a senior dev who has seen everything: question whether the task needs to exist at all (YAGNI), reach for the standard library before custom code, native platform f... |
| `ponytail-audit` | > Whole-repo audit for over-engineering. Like ponytail-review, but scans the entire codebase instead of a diff: a ranked list of what to delete, simplify, or replace with stdlib/native equivalents. Use when the user says "audit this codebase", "audit for ov... |
| `ponytail-debt` | > Harvest every `ponytail:` comment in the codebase into a debt ledger, so the deliberate shortcuts and deferrals ponytail leaves behind get tracked instead of rotting into "later means never". Use when the user says "ponytail debt", "/ponytail-debt", "what... |
| `ponytail-gain` | > Show ponytail's measured impact as a compact scoreboard: less code, less cost, more speed, from the agentic benchmark averages. One-shot display, not a persistent mode, and not a per-repo number. Trigger: /ponytail-gain, "ponytail gain", "what does ponyta... |
| `ponytail-help` | > Quick-reference card for all ponytail modes, skills, and commands. One-shot display, not a persistent mode. Trigger: /ponytail-help, "ponytail help", "what ponytail commands", "how do I use ponytail". |
| `ponytail-review` | > Code review focused exclusively on over-engineering. Finds what to delete: reinvented standard library, unneeded dependencies, speculative abstractions, dead flexibility. One line per finding: location, what to cut, what replaces it. Use when the user say... |
| `python-debugpy` | Debug Python: pdb REPL + debugpy remote (DAP). |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `simplify-code` | Parallel 4-agent cleanup of recent code changes. |
| `skill-builder` | Automatically detect source types and build AI skills using Skill Seekers. Use when the user wants to create skills from documentation, repos, PDFs, videos, or other knowledge sources. |
| `skill-inspector` | Review AI agent skills before installation using NVIDIA SkillSpector and source-aware semantic review. Use when asked whether a skill or downloaded skill folder is safe, trustworthy, installable, over-permissioned, or malicious. |
| `spike` | Throwaway experiments to validate an idea before build. |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

---

# productivity / 生产力

29 个生产力技能：文档（docx/pdf/pptx/minimax 系列）、周度回顾规划、会议行动项、文档义务提取、Notion/Airtable/Google Workspace、ADHD 友好输出、文件规划、地图/路线、价格监控、Teams 会议管道、Obsidian 笔记。

**来源**: built-in, nexu-io/open-design, ayghri/i-have-adhd, Other/Planning-with-Files

| 技能 | 用途 |
|------|------|
| `airtable` | Airtable REST API via curl. Records CRUD, filters, upserts. |
| `box` | Box manages cloud files, sharing, search, and metadata. |
| `data-report` | Turns CSV, Excel, or JSON data into a polished visual report page. |
| `doc` | \| Read, create, and edit .docx documents with formatting and layout fidelity via OpenAI's document skill. |
| `document-to-action-items` | Extract cited obligations, deadlines, tasks from documents. |
| `docx` | Create, read, edit, template, and review Word .docx files. |
| `domain-name-brainstormer` | \| Generate creative domain name ideas and check availability across multiple TLDs including .com, .io, .dev, and .ai. |
| `faq-page` | \| A Frequently Asked Questions (FAQ) page with collapsible accordion sections, search functionality, and category filtering. Use when the brief asks for "FAQ", "help center", "questions", or "support page". |
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| `i-have-adhd` | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Invoke with /i-have-adhd; stays on until "stop adhd mode".' disable-model... |
| `maps` | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| `meeting-action-items` | Turn meeting notes into cited decisions, owners, tickets. |
| `minimax-docx` | \| Professional DOCX document creation and editing using OpenXML SDK. Useful for branded reports, polished proposals, and template-based authoring. |
| `minimax-pdf` | \| Generate, fill, and reformat PDFs with a token-based design system and 15 cover styles. Useful for branded PDFs, e-guides, and reports. |
| `nanobanana-ppt` | \| AI-powered PPT generation with document analysis and styled images via the NanoBanana stack. Combines image generation with structured deck output. |
| `notion` | Notion API + ntn CLI: pages, databases, markdown, Workers. |
| `pdf` | PDF files: create, read, merge, fill, OCR, edit text. |
| `planning-with-files` | Persistent file-based planning for multi-step AI-agent work. Keeps task_plan.md, findings.md, and progress.md on disk; lifecycle hooks inject selected project planning context. Automatic recovery reads project planning files only. Explicit session-catchup.p... |
| `powerpoint` | Create, read, edit .pptx decks with python-pptx. |
| `ppt-keynote` | Apple Keynote-quality slides, one card per screen, with keyboard left/right navigation. |
| `pptx` | \| Read, generate, and adjust PowerPoint slides, layouts, and templates. Useful for executive decks, training material, and product reviews. |
| `pptx-generator` | \| Create and edit PowerPoint presentations from scratch with PptxGenJS — MiniMax's production-tested deck pipeline. |
| `product-price-monitor` | Watch product, flight, or listing prices; alert on target. |
| `release-notes-one-pager` | \| Release notes one-page HTML with highlights, Added, Fixed, Breaking changes, Known issues, and Upgrade note. Writes explicit "None" style sections whenever the user does not provide details. |
| `research-decision-room` | \| Turn messy user research notes, interviews, support tickets, surveys, and product context into an evidence-backed decision room: a single HTML artifact with an evidence ledger, theme map, confidence heatmap, opportunity matrix, decision memo, and experime... |
| `resume-modern` | Modern minimal resume, single A4 page, ready for print or PDF export. |
| `teams-meeting-pipeline` | Teams meeting summaries, job replay, Graph subscriptions. |
| `weekly-review-planning` | Weekly reset: commitments, stalled work, next-week plan. |
| `xlsx` | Create, read, edit Excel .xlsx workbooks and CSVs. |

---

# claude-mem / 持久记忆

claude-mem 记忆体系（22 个）：跨会话记忆压缩检索（mem-search）、项目周报/时间线报告、PR 看护、GitHub issue 根因聚类、会话诊断、模式创建、成本报告、云同步、代码库预学习等。

**来源**: thedotmack/claude-mem

| 技能 | 用途 |
|------|------|
| `agent-cost-report` | >- Believable agent cost report for any period, default the last 7 full days PT, not counting today. Measured tokens from Claude Code transcripts priced at OpenRouter list prices (ESTIMATED), measured provider spend when a sanctioned source exists, note-tak... |
| `babysit` | Watch a pull request or review cycle until it is ready to merge. Use when asked to babysit, monitor, or keep checking PR comments, reviews, and CI until all actionable issues are resolved. |
| `ccs-align` | Run the CCS Align seat's hourly breathing cycle — prove the local claude-mem worker is healthy, pull needle observations through search → timeline → get_observations, land them in a seat-owned middle cache via atomic grab → append → filter exclude-marks → r... |
| `cloud-sync` | Set up or check claude-mem cloud sync with cmem.ai Pro. Use when the user says "set up cloud sync", "sync my memories", "cmem pro", "cloud backup", "sync status", or wants their memory database backed up or synced to their cmem.ai account. allowed-tools: - ... |
| `design-is` | Audit a design against Dieter Rams' ten "Good design is..." principles, then hand off a /make-plan prompt for one of three outcomes — new design, refine design, or redesign. Use when the user says "audit this design", "design review", "check this UI against... |
| `do` | Execute a phased implementation plan using subagents. Use when asked to execute, run, or carry out a plan — especially one created by make-plan. |
| `handoff` | Generate a HANDOFF.md that captures goal, current state, files touched, failed attempts, and next steps — so a fresh Claude session can continue exactly where this one left off. Use when sessions are getting long, Claude keeps retrying the same broken solut... |
| `how-it-works` | Explain how claude-mem captures observations, when memory injection kicks in, and where data lives. Use when the user asks "how does claude-mem work?" or "what is this thing doing?". |
| `knowledge-agent` | Build and query AI-powered knowledge bases from claude-mem observations. Use when users want to create focused "brains" from their observation history, ask questions about past work patterns, or compile expertise on specific topics. |
| `learn-codebase` | Prime a codebase by reading every source file in full. Use when starting work on a new or unfamiliar project, or when the user asks to "learn the codebase", "read the codebase", "prime", or "get up to speed". |
| `make-plan` | Create a detailed, phased implementation plan with documentation discovery. Use when asked to plan a feature, task, or multi-step implementation — especially before executing with do. |
| `mem-search` | Search claude-mem's persistent cross-session memory database. Use when user asks "did we already solve this?", "how did we do X last time?", or needs work from previous sessions. |
| `mode-creator` | Interactively create, install, activate, and verify custom claude-mem modes, including domain-specific observation types, concept tags, optional Telegram alerts, bot setup, worker restart, and startup-context verification. Use this whenever someone asks to ... |
| `oh-my-issues` | Cluster a GitHub issue backlog by root cause into a small set of plan-master issues, redirect children with a standardized comment, and bundle architectural-fix PRs that close clusters atomically. Use when an issue tracker has accumulated dozens of reports ... |
| `pathfinder` | Map a codebase into feature-grouped flowcharts, identify duplicated concerns across features, and propose a unified architecture. Use when asked to "find the ideal path," unify duplicated systems, or audit architecture before a refactor. Emits a proposed un... |
| `smart-explore` | Token-optimized structural code search using tree-sitter AST parsing. Use instead of reading full files when you need to understand code structure, find functions, or explore a codebase efficiently. |
| `standup` | Facilitate a read-only standup across git worktrees, branches, or PRs to compare changes and produce one consolidation plan. allowed-tools: - Bash - Read - Edit - Task - AskUserQuestion |
| `timeline-report` | Generate a "Journey Into [Project]" narrative report analyzing a project's entire development history from claude-mem's timeline. Use when asked for a timeline report, project history analysis, development journey, or full project report. |
| `version-bump` | Automated semantic versioning and release workflow for Claude Code plugins. Handles version increments across package.json, marketplace.json, plugin.json manifests, build verification, git tagging, GitHub releases, and changelog generation. NPM publishing i... |
| `weekly-digests` | Generate a serial week-by-week narrative digest of a project's full claude-mem timeline. Splits the timeline into per-ISO-week files, then runs one consecutive subagent per week — each receiving the prior week's carry-forward block — to produce one chapter ... |
| `what-the` | What the? Use when the user wants a plain-English breakdown of something technical — the who, what, where, why, and when. |
| `wowerpoint` | Turn one document into a kawaii NotebookLM slide-deck PDF. Use for "wowerpoint this", "make a deck about <file>", "turn this report into slides", or any request to render a single document as shareable narrative slides. |

---

# creative / 创意内容

10 个创意技能：ASCII 艺术/视频、SVG 架构图、Manim 数学动画、p5.js 生成艺术、信息图（21 布局 x 21 风格）、Claude Design 原型、DESIGN.md 规范、音乐创作。

**来源**: built-in + OpenMontage

| 技能 | 用途 |
|------|------|
| `architecture-diagram` | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| `ascii-video` | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| `baoyu-infographic` | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| `claude-design` | Design one-off HTML artifacts (landing, deck, prototype). |
| `design-md` | Author/validate/export Google's DESIGN.md token spec files. |
| `humanizer` | Humanize text: strip AI-isms and add real voice. |
| `manim-video` | Manim CE animations: 3Blue1Brown math/algo videos. |
| `p5js` | p5.js sketches: gen art, shaders, interactive, 3D. |
| `popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| `songwriting-and-ai-music` | Songwriting craft and Suno AI music prompts. |

---

# autonomous-ai-agents / 多智能体

7 个多智能体编排技能：Claude Code/Codex/OpenCode 委托、桌面计算机操作、多代理团队、Hermes 插件开发、workspace-dispatch 任务编排。

**来源**: outsourc-e/hermes-workspace, built-in

| 技能 | 用途 |
|------|------|
| `claude-code` | Delegate coding to Claude Code CLI (features, PRs). |
| `codex` | Delegate coding to OpenAI Codex CLI (features, PRs). |
| `computer-use` | Drive the desktop background-first; escalate on signal. |
| `hermes-agent` | Use, configure, theme, extend, and orchestrate Hermes Agent. |
| `multi-agent-teams` | Compose Hermes bot groups and multi-agent dev pipelines. |
| `opencode` | Delegate coding to OpenCode CLI (features, PR review). |
| `workspace-dispatch` | \| Single-agent mission orchestrator. Decomposes a mission into tasks, spawns one worker per task using the default model, verifies exit criteria, and chains tasks with retry. No critic pattern — each worker self-verifies. Simple, fast, works with any model ... |

---

# research / 研究

6 个研究技能：arXiv 检索、竞品新闻监控、引用核验、last30days 舆论研究、LLM Wiki 知识库、D3 数据可视化。

**来源**: Graphify-Labs/graphify, mvanhorn/last30days-skill, nexu-io/open-design

| 技能 | 用途 |
|------|------|
| `arxiv` | Search arXiv papers by keyword, author, category, or ID. |
| `competitor-news-monitor` | Watch named companies for material news; cited digests. |
| `d3-visualization` | \| Teaches the agent to produce D3 charts and interactive data visualizations. A comprehensive D3.js skill with examples across chart types and techniques giving the agent expert-level knowledge to generate complex, interactive visualizations. Useful for edi... |
| `grounded-citations` | Ground answers and documents in cited, verifiable sources. |
| `last30days` | Research what people actually say about any topic in the last 30 days. Pulls posts and engagement from Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the web. Includes a doctor health check to diagnose broken or missing sources." argument-... |
| `llm-wiki` | Karpathy's LLM Wiki: build/query interlinked markdown KB. |

---

# web / 网页

5 个网页技能：被封锁页面恢复（WAF/paywall/403 应对）、web-clone 整站复刻、网页工件构建、agent-browser。

**来源**: nexu-io/open-design, built-in

| 技能 | 用途 |
|------|------|
| `agent-browser` | \| Browser automation CLI for AI agents. Use when the user needs to inspect, test, or automate browser behavior: navigating pages, filling forms, clicking buttons, taking screenshots, extracting page data, reading selected OpenDesign browser-tab context, tes... |
| `artifacts-builder` | \| Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). |
| `blocked-page-recovery` | Use when a fetch fails: 403/429, paywall, WAF, bot wall. |
| `web-artifacts-builder` | \| Build complex claude.ai HTML artifacts with React and Tailwind. Anthropic's reference workflow for shipping rich, embeddable artifacts. |
| `web-clone` | > 网站复刻 / 克隆方法论。USE WHEN 用户说 复刻网站、克隆网站、clone website、抄个站、仿站、 照着这个站做一个、reproduce site、还原某个网页效果、把这个站搬下来改成我的、 复刻某个交互/WebGL/Canvas/Three.js 效果。提供「先拿真源码 → 判路径 → 逆向拆解 → 搭工程 → 替换内容」的可移植决策树，覆盖静态站 / React-Vue-Next 内容站 / WebGL-Canvas 重前端站三大分支，并强制核对任何 AI 二手分析里的可执行代码。 |

---

# apple / Apple 生态

4 个 Apple 设备技能：Apple Notes/Reminders/iMessage/FindMy 操作。

**来源**: built-in

| 技能 | 用途 |
|------|------|
| `apple-notes` | Manage Apple Notes via memo CLI: create, search, edit. |
| `apple-reminders` | Apple Reminders via remindctl: add, list, complete. |
| `findmy` | Track Apple devices/AirTags via FindMy.app on macOS. |
| `imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. |

---

# email / 邮件

2 个邮件技能：Himalaya CLI（IMAP/SMTP）、收件箱分诊。

**来源**: built-in

| 技能 | 用途 |
|------|------|
| `email-inbox-triage` | Triage an inbox: prioritize threads, draft replies safely. |
| `himalaya` | Himalaya CLI: IMAP/SMTP email from terminal. |

---

# devops / DevOps

DevOps 基础技能。

**来源**: built-in

| 技能 | 用途 |
|------|------|
| `sdlc-review` | Review Kanban handoffs and route verified outcomes. |

---

# note-taking / 笔记

Obsidian vault 读写检索。

**来源**: built-in (obsidian)

| 技能 | 用途 |
|------|------|
| `obsidian` | Read, search, create, and edit notes in the Obsidian vault. |

---

# social-media / 社媒

X URL 抓取技能。

**来源**: nexu-io/open-design

| 技能 | 用途 |
|------|------|
| `xurl` | X/Twitter via xurl CLI: raw post search, posting, DM, media. |

---

# writing / 写作

humanizer：去除 AI 腔，让文本读起来像人写的。

**来源**: blader/humanizer

| 技能 | 用途 |
|------|------|
| `humanizer` | \| Rewrite AI-sounding text so it reads like the writer without changing what it says. Use when editing or reviewing prose for AI tells: not-X-but-Y contrasts, one-line closers, staged openers, forced triads, dashes everywhere, inflated claims, sales languag... |

---

## 给其他智能体安装（分平台说明）

本仓库的技能遵循 **Agent Skills** 通用格式（每个技能是一个文件夹，核心是带 YAML frontmatter 的 `SKILL.md`，含 name/description）。不同平台安装方式如下：

### Hermes Agent（即"源主"环境）

```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
cd -AGENT-SKILL && ./restore.sh   # 拷贝到 ~/.hermes/skills/
```

Hermes 会自动按 SKILL.md 的 description 触发对应技能，无需额外配置。重启会话后生效。

### Claude Code

```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
mkdir -p ~/.claude/skills
# 把需要的类别目录拷进去（SKILL.md 格式兼容）
cp -r -AGENT-SKILL/design ~/.claude/skills/
cp -r -AGENT-SKILL/software-development ~/.claude/skills/
```

Claude Code 会自动发现 `~/.claude/skills/` 下的技能。也可以用 `/plugin` 机制安装（若对方配了本仓库为 plugin source）。

### Cursor / Codex / OpenCode / 通用 Agent Skills 平台

这些平台遵循 Agent Skills 标准，技能目录位置各有不同（如 Codex 的 `~/.codex/skills/`、OpenCode 的 skills 路径、Cursor 的 `.cursor/skills/`）。步骤统一：

```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
cp -r -AGENT-SKILL/<类别> <平台的技能目录>/
```

### 不支持 Skills 的纯聊天模型

没有可安装位置。做法：把所需技能的 `SKILL.md` 全文（frontmatter + 正文）作为系统提示词的一部分粘贴进对话，或让模型通过 RAG 检索该文件。效果取决于模型上下文长度和遵守程度。

### 依赖说明（哪些技能"装了能跑"取决于环境）

| 技能群 | 依赖 | 缺失时的表现 |
|---|---|---|
| browser-act（103 个） | Browser Use CLI 环境 | 技能文件可装，但执行抓取需要浏览器自动化后端 |
| open-design 媒体类（fal/venice/sora 等） | 对应厂商 API 密钥（FAL_KEY、VENICE_KEY 等） | 调用返回 401，需先配 key |
| gstack 部分（ios-qa/ios-fix 等） | iOS 真机 / Xcode 环境 | 仅 macOS + Xcode 下可用 |
| openmontage 视频类 | 各模型 API 或本地 ffmpeg | 按具体技能的依赖走 |
| 纯方法论（taste-skill、superpowers、ponytail、systematic-debugging 等） | 无 | 任何平台即用 |

## 需要 API Key 的技能（128 个）

> 这些技能文件可安装，但**实际运行需要对应厂商的 API 密钥**。密钥不要提交到仓库；
> 安装后在环境变量或各平台的设置里配置即可。

| 类别 | 技能 | 需要的密钥 | 在哪里申请 |
|------|------|-----------|-----------|
| autonomous-ai-agents | `claude-code` | ANTHROPIC_API_KEY | Anthropic — console.anthropic.com → API keys |
|  | `codex` | OPENAI_API_KEY | OpenAI — platform.openai.com → API keys |
|  | `opencode` | OPENROUTER_API_KEY | OpenRouter — openrouter.ai → Keys（聚合多家模型） |
| browser-act | `solutions\ecommerce\amazon-asin-lookup-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-best-selling-products-finder-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-buy-box-monitor-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-competitor-analyzer` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-listing-competitor-analysis-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-product-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-product-search-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\ecommerce\amazon-reviews-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\business-contact-social-links-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\github-project-contributor-finder-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\google-maps-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\google-maps-reviews-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\google-maps-search-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\industry-key-contact-radar-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\lead-generation\social-media-finder-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\search-research\google-image-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\search-research\google-news-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\search-research\web-research-assistant` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\search-research\web-search-scraper-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\social-listening\reddit-competitor-analysis-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\social-listening\wechat-article-search-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\social-listening\zhihu-search-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-batch-transcript-extractor-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-channel-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-comments-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-influencer-finder-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-search-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-transcript-analysis-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-transcript-extractor-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
|  | `solutions\video-platforms\youtube-video-api-skill` | BROWSERACT_API_KEY | Browser Act — browseract.ai 注册（新用户送积分） |
| claude-mem | `agent-cost-report` | OPENROUTER_API_KEY | OpenRouter — openrouter.ai → Keys（聚合多家模型） |
| design | `design` | GEMINI_API_KEY<br>MUAPI_API_KEY | Google Gemini — aistudio.google.com → Get API key<br>厂商官方 API 平台注册后生成 key |
|  | `21st-dev` | API_KEY_21ST | 21st.dev — https://21st.dev/mcp 免费即时申请（旧 Magic console key 已作废）
|  | `hatch-pet` | OPENAI_API_KEY | OpenAI — platform.openai.com → API keys |
|  | `taste-skill` | SHOPIFY_API_KEY | 厂商官方 API 平台注册后生成 key |
| gstack | `autoplan` | CODEX_API_KEY<br>SHORT_KEY | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `benchmark` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `benchmark-models` | ANTHROPIC_API_KEY<br>GOOGLE_API_KEY<br>SHORT_KEY | Anthropic — console.anthropic.com → API keys<br>Google API — console.cloud.google.com → API 与凭据<br>厂商官方 API 平台注册后生成 key |
|  | `browse` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `canary` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `codex` | CODEX_API_KEY<br>OPENAI_API_KEY<br>SHORT_KEY | 厂商官方 API 平台注册后生成 key<br>OpenAI — platform.openai.com → API keys<br>厂商官方 API 平台注册后生成 key |
|  | `context-restore` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `context-save` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `design-consultation` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `design-html` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `design-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `design-shotgun` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `devex-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `diagram` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `document-generate` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `document-release` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `health` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `investigate` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `ios-clean` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `ios-design-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `ios-fix` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `ios-qa` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `ios-sync` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `land-and-deploy` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `landing-report` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `learn` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `make-pdf` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `office-hours` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `open-gstack-browser` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `pair-agent` | SHORT_KEY<br>YOUR_TOKEN | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `plan-ceo-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `plan-design-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `plan-devex-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `plan-eng-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `plan-tune` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `qa` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `qa-only` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `retro` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `scrape` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `setup-browser-cookies` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `setup-deploy` | RENDER_API_KEY<br>SHORT_KEY | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `setup-gbrain` | SHORT_KEY<br>SUPABASE_ACCESS_TOKEN<br>YOUR_TOKEN | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `ship` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `skillify` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `spec` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
|  | `sync-gbrain` | SHORT_KEY<br>VOYAGE_API_KEY | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `test-audit` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| media | `gif-search` | TENOR_API_KEY | 厂商官方 API 平台注册后生成 key |
| openmontage | `acestep` | RUNPOD_API_KEY | 厂商官方 API 平台注册后生成 key |
|  | `agents` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
|  | `ai-video-gen` | FAL_KEY<br>GEMINI_API_KEY<br>GOOGLE_API_KEY<br>HEYGEN_API_KEY<br>KLING_API_KEY | fal.ai — fal.ai → Dashboards → Keys<br>Google Gemini — aistudio.google.com → Get API key<br>Google API — console.cloud.google.com → API 与凭据<br>HeyGen — platform.heygen.com → API 设置<br>厂商官方 API 平台注册后生成 key |
|  | `atlas-cloud` | ATLASCLOUD_API_KEY<br>ATLAS_API_KEY | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `avatar-video` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
|  | `bfl-api` | BFL_API_KEY<br>YOUR_API_KEY | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `create-video` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
|  | `dashscope` | DASHSCOPE_API_KEY | 阿里云百炼/DashScope — bailian.console.aliyun.com → API-KEY 管理 |
|  | `elevenlabs` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
|  | `faceswap` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
|  | `gemini-omni` | GEMINI_API_KEY<br>GOOGLE_API_KEY | Google Gemini — aistudio.google.com → Get API key<br>Google API — console.cloud.google.com → API 与凭据 |
|  | `grok-media` | XAI_API_KEY | xAI — console.x.ai → API Keys |
|  | `heygen` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
|  | `hyperframes-media` | ELEVENLABS_API_KEY<br>HEYGEN_API_KEY<br>HYPERFRAMES_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys<br>HeyGen — platform.heygen.com → API 设置<br>厂商官方 API 平台注册后生成 key |
|  | `kling-official` | FAL_KEY<br>KLING_API_KEY | fal.ai — fal.ai → Dashboards → Keys<br>厂商官方 API 平台注册后生成 key |
|  | `lyria` | GEMINI_API_KEY<br>GOOGLE_API_KEY | Google Gemini — aistudio.google.com → Get API key<br>Google API — console.cloud.google.com → API 与凭据 |
|  | `media-use` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
|  | `motion-graphics` | GEMINI_API_KEY<br>GOOGLE_API_KEY | Google Gemini — aistudio.google.com → Get API key<br>Google API — console.cloud.google.com → API 与凭据 |
|  | `music` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
|  | `seedance-2-0` | FAL_KEY<br>HEYGEN_API_KEY<br>HIGGSFIELD_API_KEY<br>RUNWAY_API_KEY | fal.ai — fal.ai → Dashboards → Keys<br>HeyGen — platform.heygen.com → API 设置<br>厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key |
|  | `setup-api-key` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
|  | `sound-effects` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
|  | `speech-to-text` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
|  | `text-to-speech` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
|  | `video-translate` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| productivity | `airtable` | AIRTABLE_API_KEY | 厂商官方 API 平台注册后生成 key |
|  | `notion` | NOTION_API_KEY | 厂商官方 API 平台注册后生成 key |
|  | `teams-meeting-pipeline` | MSGRAPH_CLIENT_ID | 厂商官方 API 平台注册后生成 key |
| research | `last30days` | AUTH_TOKEN<br>BRAVE_API_KEY<br>EXA_API_KEY<br>LAST30DAYS_API_KEY<br>OPENAI_API_KEY<br>OPENROUTER_API_KEY<br>PARALLEL_API_KEY<br>PERPLEXITY_API_KEY<br>SCRAPECREATORS_API_KEY<br>SERPER_API_KEY<br>TRUTHSOCIAL_TOKEN<br>XAI_API_KEY<br>XQUIK_API_KEY | 厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key<br>Exa — exa.ai → API Keys<br>厂商官方 API 平台注册后生成 key<br>OpenAI — platform.openai.com → API keys<br>OpenRouter — openrouter.ai → Keys（聚合多家模型）<br>厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key<br>厂商官方 API 平台注册后生成 key<br>Serper.dev — serper.dev → API Keys（Google 搜索代理）<br>厂商官方 API 平台注册后生成 key<br>xAI — console.x.ai → API Keys<br>厂商官方 API 平台注册后生成 key |
| social-media | `xurl` | YOUR_CLIENT_ID | 厂商官方 API 平台注册后生成 key |
| software-development | `graphify` | ANTHROPIC_API_KEY<br>GEMINI_API_KEY<br>GOOGLE_API_KEY<br>OPENAI_API_KEY | Anthropic — console.anthropic.com → API keys<br>Google Gemini — aistudio.google.com → Get API key<br>Google API — console.cloud.google.com → API 与凭据<br>OpenAI — platform.openai.com → API keys |
| web | `agent-reach` | TWITTER_AUTH_TOKEN | 厂商官方 API 平台注册后生成 key |
|  | `blocked-page-recovery` | JINA_API_KEY | Jina — jina.ai → Dashboard → API Keys（r.jina.ai 支持匿名） |
|  | `firecrawl` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
|  | `firecrawl-build` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
|  | `firecrawl-build-interact` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
|  | `firecrawl-build-onboarding` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
|  | `firecrawl-build-scrape` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
|  | `firecrawl-build-search` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
|  | `firecrawl-developer-index` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |

---

## 抓网页 / 爬虫工具选择表（本机实测可用）

> 本机已装好一套互补的爬虫工具链（Python 3.14 + Node），覆盖从"取单页"到"整站批量"到"绕过 anti-bot"。按场景挑，别乱起浏览器。

| 场景 | 首选工具 | 本机状态 |
|------|---------|---------|
| 单页快速取内容（喂 LLM/RAG，最轻） | 内置 `web_extract` / `agent-reach` | ✅ 零依赖，不起浏览器 |
| 整站批量、上千 URL、要并发/节流/重试 | **Scrapy** | ✅ 已装 v2.19 |
| anti-bot / Cloudflare / TLS 指纹拦截 | **Scrapling**（`impersonate`/`StealthyFetcher`） | ✅ 已装 0.4.15 + curl_cffi + browserforge，实测抓 200 |
| 重复 DOM 结构、少写选择器 | **AutoScraper** | ✅ 已装 1.1 |
| Node/TS 技术栈爬虫 | **Crawlee** | ✅ 已装（`tools/node-packages`） |
| 文档/Office/PDF → markdown | **MarkItDown** | ✅ 已装 0.1.8 [all] |
| 让 AI 自动开浏览器做多步操作 | **browser-use** | ⚠️ 库已装 0.13，但需 LLM key（OpenAI/Anthropic/本地 Ollama）才跑得动 |
| 手机投屏/键鼠控制 Android | **scrcpy** | ✅ 已装 v5.0（`tools/scrcpy`），需实体手机+USB 调试 |
| TLS/HTTP2 指纹对抗（知识） | **curl-impersonate** | ⚠️ 无 Windows 二进制，本机用 Scrapling 的 `impersonate` 替代 |

**分工原则**：能用 `web_extract` 解决就别起爬虫；静态整站爬用 Scrapy；被指纹/anti-bot 拦就上 Scrapling；要 AI 自主操作浏览器才动用 browser-use（并先配好 LLM 后端）。

## 恢复方法

```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
cd -AGENT-SKILL && ./restore.sh
```

## 更新方法

```bash
cp -r $HERMES_HOME/skills/. ./   # 把新技能复制进来
git add -A && git commit -m "更新" && git push
```

## 技能来源仓库

- `github.com/obra/superpowers`
- `github.com/emilkowalski/skills`
- `github.com/Leonxlnx/taste-skill`
- `github.com/cathrynlavery/diagram-design`
- `github.com/tt-a1i/archify`
- `github.com/nexu-io/open-design`
- `github.com/Graphify-Labs/graphify`
- `github.com/browser-act/skills`
- `github.com/calesthio/OpenMontage`
- `github.com/coreyhaines31/marketingskills`
- `github.com/garrytan/gstack`
- `github.com/DietrichGebert/ponytail`
- `github.com/NousResearch/hermes-agent-self-evolution`
- `github.com/NVIDIA/SkillSpector`
- `github.com/yusufkaraaslan/Skill_Seekers`
- `github.com/built-in`
- `github.com/ayghri/i-have-adhd`
- `github.com/Other/Planning-with-Files`
- `github.com/thedotmack/claude-mem`
- `github.com/built-in + OpenMontage`
- `github.com/outsourc-e/hermes-workspace`
- `github.com/mvanhorn/last30days-skill`
- `github.com/built-in (obsidian)`
- `github.com/blader/humanizer`
