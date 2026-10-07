# Hermes Agent 技能库备份


共 **1931 个技能**，25 个类别。每个技能的用途从 SKILL.md 自动提取。

> 本仓库同时是跨机器/跨智能体备份：`git clone` 后跑 `restore.sh` 即可整库恢复，
> 或按平台把需要的类别拷进各家的技能目录（文末有分平台说明）。

## 目录

| 类别 | 技能数 | 说明 |
|------|--------|------|
| [claude-skills](#claude-skills) | 844 | Claude Code 380+ 技能（30 agents + 70 commands，业务/工程/营销/合规/C-level/科研） |
| [security](#security) | 170 | Trail of Bits 安全审计（Semgrep / CodeQL / 智能合约 / 供应链 / 差分分析） |
| [software-development](#software-development) | 147 | 编码方法论 / TDD / 调试 / 测试 / addyosmani 生产级工程技能 |
| [design](#design) | 113 | UI 设计 / 前端 / 组件素材库（react-bits, magic-ui, threeui, shadergradient, uiverse, 21st, taste-skill…） |
| [browser-act](#browser-act) | 103 | 浏览器自动化 / 电商抓取 / 社媒 / 视频平台 |
| [marketing](#marketing) | 100 | 营销全链路（广告/SEO/转化/文案/邮件/发布…） |
| [openmontage](#openmontage) | 90 | 视频 / 3D / 动效生成（HyperFrames, Remotion, GSAP, Three.js, 各模型） |
| [mattpocock](#mattpocock) | 76 | Matt Pocock（277k★）工程/生产力技能（TDD/诊断/设计文档/交接/复盘…），包根含 GLOSSARY/AGENTS 共享层 |
| [gstack](#gstack) | 63 | gstack 工程工作流（CEO/devex/eng 评审、QA、发布、iOS） |
| [media](#media) | 36 | 媒体内容（YouTube/GIF/音乐/音频/图像） |
| [web](#web) | 33 | 网页抓取 / 爬虫工具链（Scrapy/Scrapling/Crawlee/browser-use/Firecrawl…） |
| [productivity](#productivity) | 30 | 办公文档 / 表格 / PPT / 邮件 / 协作 |
| [addyosmani](#addyosmani) | 25 |  |
| [claude-mem](#claude-mem) | 22 | Claude 跨会话记忆 / 知识图谱 |
| [hermes-jev](#hermes-jev) | 22 |  |
| [anthropics](#anthropics) | 19 |  |
| [autonomous-ai-agents](#autonomous-ai-agents) | 10 | 自主 agent 编排 / 委派 / 多 agent 团队 |
| [creative](#creative) | 10 | ASCII 艺术 / 手绘图 / 视觉设计 |
| [research](#research) | 7 | 学术 / 文献 / 市场数据 / 内容监测 |
| [apple](#apple) | 4 | Apple 平台 / SwiftUI / HIG |
| [email](#email) | 2 | IMAP/SMTP 邮件 |
| [social-media](#social-media) | 2 | 社媒运营 |
| [devops](#devops) | 1 | SDLC / 部署 / CI |
| [note-taking](#note-taking) | 1 | Obsidian 笔记 |
| [typesafe-ai](#typesafe-ai) | 1 |  |

---

## claude-skills（844）

| 技能 | 用途 |
|------|------|
| `.gemini/skills/a11y-audit` | (无描述) |
| `.gemini/skills/ab-test-setup` | (无描述) |
| `.gemini/skills/ad-creative` | (无描述) |
| `.gemini/skills/adversarial-reviewer` | (无描述) |
| `.gemini/skills/aeo` | (无描述) |
| `.gemini/skills/agent-decision-receipts` | (无描述) |
| `.gemini/skills/agent-designer` | (无描述) |
| `.gemini/skills/agent-harness` | (无描述) |
| `.gemini/skills/agent-launcher-orchestrator` | (无描述) |
| `.gemini/skills/agent-memory` | (无描述) |
| `.gemini/skills/agent-protocol` | (无描述) |
| `.gemini/skills/agent-workflow-designer` | (无描述) |
| `.gemini/skills/agenthub` | (无描述) |
| `.gemini/skills/agile-product-owner` | (无描述) |
| `.gemini/skills/ai-act-readiness` | (无描述) |
| `.gemini/skills/ai-security` | (无描述) |
| `.gemini/skills/aims-audit` | (无描述) |
| `.gemini/skills/analytics-tracking` | (无描述) |
| `.gemini/skills/andreessen` | (无描述) |
| `.gemini/skills/api-design-reviewer` | (无描述) |
| `.gemini/skills/api-test-suite-builder` | (无描述) |
| `.gemini/skills/app-store-optimization` | (无描述) |
| `.gemini/skills/apple-hig-expert` | (无描述) |
| `.gemini/skills/ar-resume` | (无描述) |
| `.gemini/skills/ar-status` | (无描述) |
| `.gemini/skills/arquiteto-de-empresa` | (无描述) |
| `.gemini/skills/atlassian-admin` | (无描述) |
| `.gemini/skills/atlassian-templates` | (无描述) |
| `.gemini/skills/autoresearch-agent` | (无描述) |
| `.gemini/skills/aws-solution-architect` | (无描述) |
| `.gemini/skills/azure-cloud-architect` | (无描述) |
| `.gemini/skills/behuman` | (无描述) |
| `.gemini/skills/board` | (无描述) |
| `.gemini/skills/board-deck-builder` | (无描述) |
| `.gemini/skills/board-meeting` | (无描述) |
| `.gemini/skills/board-prep` | (无描述) |
| `.gemini/skills/boardroom` | (无描述) |
| `.gemini/skills/book-to-skill` | (无描述) |
| `.gemini/skills/boost-asio-pro` | (无描述) |
| `.gemini/skills/brand-guidelines` | (无描述) |
| `.gemini/skills/brief` | (无描述) |
| `.gemini/skills/browser-automation` | (无描述) |
| `.gemini/skills/browserstack` | (无描述) |
| `.gemini/skills/business-growth-skills` | (无描述) |
| `.gemini/skills/business-investment-advisor` | (无描述) |
| `.gemini/skills/business-name-fit` | (无描述) |
| `.gemini/skills/business-operations-skills` | (无描述) |
| `.gemini/skills/c-level-agents` | (无描述) |
| `.gemini/skills/c-level-skills` | (无描述) |
| `.gemini/skills/caio-review` | (无描述) |
| `.gemini/skills/campaign-analytics` | (无描述) |
| `.gemini/skills/capa-officer` | (无描述) |
| `.gemini/skills/capacity-planner` | (无描述) |
| `.gemini/skills/capture` | (无描述) |
| `.gemini/skills/caveman` | (无描述) |
| `.gemini/skills/cco-review` | (无描述) |
| `.gemini/skills/cdo-review` | (无描述) |
| `.gemini/skills/ceo-advisor` | (无描述) |
| `.gemini/skills/cfo-advisor` | (无描述) |
| `.gemini/skills/cfo-review` | (无描述) |
| `.gemini/skills/challenge` | (无描述) |
| `.gemini/skills/change-management` | (无描述) |
| `.gemini/skills/changelog` | (无描述) |
| `.gemini/skills/changelog-generator` | (无描述) |
| `.gemini/skills/channel-economics` | (无描述) |
| `.gemini/skills/chaos-engineering` | (无描述) |
| `.gemini/skills/chaos-experiment` | (无描述) |
| `.gemini/skills/chief-ai-officer-advisor` | (无描述) |
| `.gemini/skills/chief-customer-officer-advisor` | (无描述) |
| `.gemini/skills/chief-data-officer-advisor` | (无描述) |
| `.gemini/skills/chief-of-staff` | (无描述) |
| `.gemini/skills/chro-advisor` | (无描述) |
| `.gemini/skills/churn-prevention` | (无描述) |
| `.gemini/skills/ci-cd-pipeline-builder` | (无描述) |
| `.gemini/skills/ciso-advisor` | (无描述) |
| `.gemini/skills/ciso-review` | (无描述) |
| `.gemini/skills/claude-coach` | (无描述) |
| `.gemini/skills/clinical-research` | (无描述) |
| `.gemini/skills/cloud-security` | (无描述) |
| `.gemini/skills/cmd-a11y-audit` | (无描述) |
| `.gemini/skills/cmd-code-to-prd` | (无描述) |
| `.gemini/skills/cmd-cs-aeo` | (无描述) |
| `.gemini/skills/cmd-focused-fix` | (无描述) |
| `.gemini/skills/cmo-advisor` | (无描述) |
| `.gemini/skills/cmo-review` | (无描述) |
| `.gemini/skills/code-reviewer` | (无描述) |
| `.gemini/skills/code-to-prd` | (无描述) |
| `.gemini/skills/code-tour` | (无描述) |
| `.gemini/skills/codebase-onboarding` | (无描述) |
| `.gemini/skills/cold-email` | (无描述) |
| `.gemini/skills/collab-proof` | (无描述) |
| `.gemini/skills/commercial-forecaster` | (无描述) |
| `.gemini/skills/commercial-policy` | (无描述) |
| `.gemini/skills/commercial-skills` | (无描述) |
| `.gemini/skills/company-os` | (无描述) |
| `.gemini/skills/competitive-intel` | (无描述) |
| `.gemini/skills/competitive-matrix` | (无描述) |
| `.gemini/skills/competitive-teardown` | (无描述) |
| `.gemini/skills/competitor-alternatives` | (无描述) |
| `.gemini/skills/compliance-os-bundle` | (无描述) |
| `.gemini/skills/compliance-readiness` | (无描述) |
| `.gemini/skills/confluence-expert` | (无描述) |
| `.gemini/skills/content-creator` | (无描述) |
| `.gemini/skills/content-humanizer` | (无描述) |
| `.gemini/skills/content-production` | (无描述) |
| `.gemini/skills/content-strategist` | (无描述) |
| `.gemini/skills/content-strategy` | (无描述) |
| `.gemini/skills/context-engine` | (无描述) |
| `.gemini/skills/contract-and-proposal-writer` | (无描述) |
| `.gemini/skills/coo-advisor` | (无描述) |
| `.gemini/skills/copy-editing` | (无描述) |
| `.gemini/skills/copywriting` | (无描述) |
| `.gemini/skills/cpo-advisor` | (无描述) |
| `.gemini/skills/cpo-review` | (无描述) |
| `.gemini/skills/cro-advisor` | (无描述) |
| `.gemini/skills/cro-review` | (无描述) |
| `.gemini/skills/cross-eval` | (无描述) |
| `.gemini/skills/cs-aeo` | (无描述) |
| `.gemini/skills/cs-agile-product-owner` | (无描述) |
| `.gemini/skills/cs-backend-engineer` | (无描述) |
| `.gemini/skills/cs-backend-review` | (无描述) |
| `.gemini/skills/cs-ceo-advisor` | (无描述) |
| `.gemini/skills/cs-content-creator` | (无描述) |
| `.gemini/skills/cs-cto-advisor` | (无描述) |
| `.gemini/skills/cs-demand-gen-specialist` | (无描述) |
| `.gemini/skills/cs-engineer-grill` | (无描述) |
| `.gemini/skills/cs-engineering-lead` | (无描述) |
| `.gemini/skills/cs-financial-analyst` | (无描述) |
| `.gemini/skills/cs-frontend-engineer` | (无描述) |
| `.gemini/skills/cs-frontend-review` | (无描述) |
| `.gemini/skills/cs-fullstack-engineer` | (无描述) |
| `.gemini/skills/cs-fullstack-review` | (无描述) |
| `.gemini/skills/cs-growth-strategist` | (无描述) |
| `.gemini/skills/cs-karpathy-reviewer` | (无描述) |
| `.gemini/skills/cs-onboard` | (无描述) |
| `.gemini/skills/cs-product-analyst` | (无描述) |
| `.gemini/skills/cs-product-manager` | (无描述) |
| `.gemini/skills/cs-product-strategist` | (无描述) |
| `.gemini/skills/cs-project-manager` | (无描述) |
| `.gemini/skills/cs-quality-regulatory` | (无描述) |
| `.gemini/skills/cs-senior-engineer` | (无描述) |
| `.gemini/skills/cs-ux-researcher` | (无描述) |
| `.gemini/skills/cs-webinar` | (无描述) |
| `.gemini/skills/cs-webinar-marketer` | (无描述) |
| `.gemini/skills/cs-wiki-ingestor` | (无描述) |
| `.gemini/skills/cs-wiki-librarian` | (无描述) |
| `.gemini/skills/cs-wiki-linter` | (无描述) |
| `.gemini/skills/cs-workspace-admin` | (无描述) |
| `.gemini/skills/cto-advisor` | (无描述) |
| `.gemini/skills/cto-review` | (无描述) |
| `.gemini/skills/culture-architect` | (无描述) |
| `.gemini/skills/customer-success-manager` | (无描述) |
| `.gemini/skills/data-quality-auditor` | (无描述) |
| `.gemini/skills/database-designer` | (无描述) |
| `.gemini/skills/database-schema-designer` | (无描述) |
| `.gemini/skills/deal-desk` | (无描述) |
| `.gemini/skills/decide` | (无描述) |
| `.gemini/skills/decision-logger` | (无描述) |
| `.gemini/skills/deep-research` | (无描述) |
| `.gemini/skills/deep-work` | (无描述) |
| `.gemini/skills/deepread` | (无描述) |
| `.gemini/skills/demo-video` | (无描述) |
| `.gemini/skills/dependency-auditor` | (无描述) |
| `.gemini/skills/design-system` | (无描述) |
| `.gemini/skills/devops-engineer` | (无描述) |
| `.gemini/skills/docker-development` | (无描述) |
| `.gemini/skills/dossier` | (无描述) |
| `.gemini/skills/email-sequence` | (无描述) |
| `.gemini/skills/email-template-builder` | (无描述) |
| `.gemini/skills/embedded-iot-mentor` | (无描述) |
| `.gemini/skills/engineering-advanced-skills` | (无描述) |
| `.gemini/skills/engineering-skills` | (无描述) |
| `.gemini/skills/env-secrets-manager` | (无描述) |
| `.gemini/skills/epic-design` | (无描述) |
| `.gemini/skills/eu-ai-act-specialist` | (无描述) |
| `.gemini/skills/eval` | (无描述) |
| `.gemini/skills/execute` | (无描述) |
| `.gemini/skills/executive-mentor` | (无描述) |
| `.gemini/skills/experiment-designer` | (无描述) |
| `.gemini/skills/extract` | (无描述) |
| `.gemini/skills/fable-goal` | (无描述) |
| `.gemini/skills/fda-consultant-specialist` | (无描述) |
| `.gemini/skills/fda-qsr-audit-prep` | (无描述) |
| `.gemini/skills/feature-flags-architect` | (无描述) |
| `.gemini/skills/finance-lead` | (无描述) |
| `.gemini/skills/finance-skills` | (无描述) |
| `.gemini/skills/financial-analyst` | (无描述) |
| `.gemini/skills/financial-health` | (无描述) |
| `.gemini/skills/fix` | (无描述) |
| `.gemini/skills/flag-cleanup` | (无描述) |
| `.gemini/skills/focused-fix` | (无描述) |
| `.gemini/skills/form-cro` | (无描述) |
| `.gemini/skills/founder-coach` | (无描述) |
| `.gemini/skills/founder-mode` | (无描述) |
| `.gemini/skills/free-tool-strategy` | (无描述) |
| `.gemini/skills/freeze` | (无描述) |
| `.gemini/skills/full-page-screenshot` | (无描述) |
| `.gemini/skills/gc-review` | (无描述) |
| `.gemini/skills/gcp-cloud-architect` | (无描述) |
| `.gemini/skills/gdpr-audit-prep` | (无描述) |
| `.gemini/skills/gdpr-dsgvo-expert` | (无描述) |
| `.gemini/skills/general-counsel-advisor` | (无描述) |
| `.gemini/skills/generate` | (无描述) |
| `.gemini/skills/git-worktree-manager` | (无描述) |
| `.gemini/skills/google-workspace` | (无描述) |
| `.gemini/skills/google-workspace-cli` | (无描述) |
| `.gemini/skills/grade-iterate` | (无描述) |
| `.gemini/skills/grants` | (无描述) |
| `.gemini/skills/grill-me` | (无描述) |
| `.gemini/skills/grill-with-docs` | (无描述) |
| `.gemini/skills/growth-marketer` | (无描述) |
| `.gemini/skills/handoff` | (无描述) |
| `.gemini/skills/hard-call` | (无描述) |
| `.gemini/skills/helm-chart-builder` | (无描述) |
| `.gemini/skills/hivemind` | (无描述) |
| `.gemini/skills/hub-init` | (无描述) |
| `.gemini/skills/hub-status` | (无描述) |
| `.gemini/skills/human-gate` | (无描述) |
| `.gemini/skills/inbox-setup` | (无描述) |
| `.gemini/skills/inbox-triage` | (无描述) |
| `.gemini/skills/incident-commander` | (无描述) |
| `.gemini/skills/incident-response` | (无描述) |
| `.gemini/skills/information-security-manager-iso27001` | (无描述) |
| `.gemini/skills/internal-comms` | (无描述) |
| `.gemini/skills/internal-narrative` | (无描述) |
| `.gemini/skills/interview` | (无描述) |
| `.gemini/skills/interview-system-designer` | (无描述) |
| `.gemini/skills/intl-expansion` | (无描述) |
| `.gemini/skills/isms-audit-expert` | (无描述) |
| `.gemini/skills/iso13485-audit-prep` | (无描述) |
| `.gemini/skills/iso27001-audit-prep` | (无描述) |
| `.gemini/skills/iso42001-specialist` | (无描述) |
| `.gemini/skills/jira-expert` | (无描述) |
| `.gemini/skills/karpathy-check` | (无描述) |
| `.gemini/skills/karpathy-coder` | (无描述) |
| `.gemini/skills/knowledge-ops` | (无描述) |
| `.gemini/skills/kubernetes-operator` | (无描述) |
| `.gemini/skills/landing` | (无描述) |
| `.gemini/skills/landing-page-generator` | (无描述) |
| `.gemini/skills/launch-strategy` | (无描述) |
| `.gemini/skills/linkedin-analytics` | (无描述) |
| `.gemini/skills/linkedin-content` | (无描述) |
| `.gemini/skills/linkedin-engagement` | (无描述) |
| `.gemini/skills/linkedin-profile` | (无描述) |
| `.gemini/skills/linkedin-skills` | (无描述) |
| `.gemini/skills/linkedin-strategy` | (无描述) |
| `.gemini/skills/litreview` | (无描述) |
| `.gemini/skills/llm-cost-optimizer` | (无描述) |
| `.gemini/skills/llm-wiki` | (无描述) |
| `.gemini/skills/local-seo-manager` | (无描述) |
| `.gemini/skills/loop` | (无描述) |
| `.gemini/skills/ma-playbook` | (无描述) |
| `.gemini/skills/markdown-html-orchestrator` | (无描述) |
| `.gemini/skills/market-research` | (无描述) |
| `.gemini/skills/marketing-context` | (无描述) |
| `.gemini/skills/marketing-demand-acquisition` | (无描述) |
| `.gemini/skills/marketing-ideas` | (无描述) |
| `.gemini/skills/marketing-ops` | (无描述) |
| `.gemini/skills/marketing-psychology` | (无描述) |
| `.gemini/skills/marketing-skills` | (无描述) |
| `.gemini/skills/marketing-strategy-pmm` | (无描述) |
| `.gemini/skills/mcp-server-builder` | (无描述) |
| `.gemini/skills/md-document` | (无描述) |
| `.gemini/skills/md-review` | (无描述) |
| `.gemini/skills/md-slides` | (无描述) |
| `.gemini/skills/mdr-745-specialist` | (无描述) |
| `.gemini/skills/meeting-analyzer` | (无描述) |
| `.gemini/skills/meetings` | (无描述) |
| `.gemini/skills/memory-engineering` | (无描述) |
| `.gemini/skills/memory-review` | (无描述) |
| `.gemini/skills/memory-status` | (无描述) |
| `.gemini/skills/merge` | (无描述) |
| `.gemini/skills/migrate` | (无描述) |
| `.gemini/skills/migration-architect` | (无描述) |
| `.gemini/skills/minimalist` | (无描述) |
| `.gemini/skills/monorepo-navigator` | (无描述) |
| `.gemini/skills/ms365-tenant-manager` | (无描述) |
| `.gemini/skills/named-persona-adversarial-review` | (无描述) |
| `.gemini/skills/notebooklm` | (无描述) |
| `.gemini/skills/observability-designer` | (无描述) |
| `.gemini/skills/office-hours` | (无描述) |
| `.gemini/skills/okr` | (无描述) |
| `.gemini/skills/onboard` | (无描述) |
| `.gemini/skills/onboarding-cro` | (无描述) |
| `.gemini/skills/operator-audit` | (无描述) |
| `.gemini/skills/org-health-diagnostic` | (无描述) |
| `.gemini/skills/page-cro` | (无描述) |
| `.gemini/skills/paid-ads` | (无描述) |
| `.gemini/skills/partnerships-architect` | (无描述) |
| `.gemini/skills/patent` | (无描述) |
| `.gemini/skills/paywall-upgrade-cro` | (无描述) |
| `.gemini/skills/performance-profiler` | (无描述) |
| `.gemini/skills/persona` | (无描述) |
| `.gemini/skills/pipeline` | (无描述) |
| `.gemini/skills/plugin-audit` | (无描述) |
| `.gemini/skills/pm-skills` | (无描述) |
| `.gemini/skills/popup-cro` | (无描述) |
| `.gemini/skills/post-mortem` | (无描述) |
| `.gemini/skills/postmortem` | (无描述) |
| `.gemini/skills/pr-review-expert` | (无描述) |
| `.gemini/skills/prd` | (无描述) |
| `.gemini/skills/pricing-strategist` | (无描述) |
| `.gemini/skills/pricing-strategy` | (无描述) |
| `.gemini/skills/process-mapper` | (无描述) |
| `.gemini/skills/procurement-optimizer` | (无描述) |
| `.gemini/skills/product-analytics` | (无描述) |
| `.gemini/skills/product-discovery` | (无描述) |
| `.gemini/skills/product-manager` | (无描述) |
| `.gemini/skills/product-manager-toolkit` | (无描述) |
| `.gemini/skills/product-research` | (无描述) |
| `.gemini/skills/product-skills` | (无描述) |
| `.gemini/skills/product-strategist` | (无描述) |
| `.gemini/skills/programmatic-seo` | (无描述) |
| `.gemini/skills/project-health` | (无描述) |
| `.gemini/skills/promote` | (无描述) |
| `.gemini/skills/prompt-engineer-toolkit` | (无描述) |
| `.gemini/skills/prompt-governance` | (无描述) |
| `.gemini/skills/pulse` | (无描述) |
| `.gemini/skills/pw` | (无描述) |
| `.gemini/skills/pw-init` | (无描述) |
| `.gemini/skills/pw-review` | (无描述) |
| `.gemini/skills/qms-audit-expert` | (无描述) |
| `.gemini/skills/quality-documentation-manager` | (无描述) |
| `.gemini/skills/quality-manager-qmr` | (无描述) |
| `.gemini/skills/quality-manager-qms-iso13485` | (无描述) |
| `.gemini/skills/ra-qm-skills` | (无描述) |
| `.gemini/skills/rag-architect` | (无描述) |
| `.gemini/skills/README` | (无描述) |
| `.gemini/skills/red-team` | (无描述) |
| `.gemini/skills/referral-program` | (无描述) |
| `.gemini/skills/reflect` | (无描述) |
| `.gemini/skills/regulatory-affairs-head` | (无描述) |
| `.gemini/skills/remember` | (无描述) |
| `.gemini/skills/report` | (无描述) |
| `.gemini/skills/research-bundle` | (无描述) |
| `.gemini/skills/research-finance` | (无描述) |
| `.gemini/skills/research-ops-skills` | (无描述) |
| `.gemini/skills/research-summarizer` | (无描述) |
| `.gemini/skills/retro` | (无描述) |
| `.gemini/skills/revenue-operations` | (无描述) |
| `.gemini/skills/rfp-responder` | (无描述) |
| `.gemini/skills/rice` | (无描述) |
| `.gemini/skills/risk-management-specialist` | (无描述) |
| `.gemini/skills/roadmap-communicator` | (无描述) |
| `.gemini/skills/roast` | (无描述) |
| `.gemini/skills/run` | (无描述) |
| `.gemini/skills/run-without-you` | (无描述) |
| `.gemini/skills/runbook-generator` | (无描述) |
| `.gemini/skills/saas-health` | (无描述) |
| `.gemini/skills/saas-metrics-coach` | (无描述) |
| `.gemini/skills/saas-scaffolder` | (无描述) |
| `.gemini/skills/sales-engineer` | (无描述) |
| `.gemini/skills/sample-skill` | (无描述) |
| `.gemini/skills/scenario-war-room` | (无描述) |
| `.gemini/skills/schema-markup` | (无描述) |
| `.gemini/skills/scrum-master` | (无描述) |
| `.gemini/skills/secrets-vault-manager` | (无描述) |
| `.gemini/skills/security-guidance` | (无描述) |
| `.gemini/skills/security-pen-testing` | (无描述) |
| `.gemini/skills/self-eval` | (无描述) |
| `.gemini/skills/self-improving-agent` | (无描述) |
| `.gemini/skills/senior-architect` | (无描述) |
| `.gemini/skills/senior-backend` | (无描述) |
| `.gemini/skills/senior-computer-vision` | (无描述) |
| `.gemini/skills/senior-data-engineer` | (无描述) |
| `.gemini/skills/senior-data-scientist` | (无描述) |
| `.gemini/skills/senior-devops` | (无描述) |
| `.gemini/skills/senior-frontend` | (无描述) |
| `.gemini/skills/senior-fullstack` | (无描述) |
| `.gemini/skills/senior-ml-engineer` | (无描述) |
| `.gemini/skills/senior-pm` | (无描述) |
| `.gemini/skills/senior-prompt-engineer` | (无描述) |
| `.gemini/skills/senior-qa` | (无描述) |
| `.gemini/skills/senior-secops` | (无描述) |
| `.gemini/skills/senior-security` | (无描述) |
| `.gemini/skills/seo-audit` | (无描述) |
| `.gemini/skills/seo-auditor` | (无描述) |
| `.gemini/skills/setup` | (无描述) |
| `.gemini/skills/ship-gate` | (无描述) |
| `.gemini/skills/signup-flow-cro` | (无描述) |
| `.gemini/skills/site-architecture` | (无描述) |
| `.gemini/skills/skill-doctor` | (无描述) |
| `.gemini/skills/skill-security-auditor` | (无描述) |
| `.gemini/skills/skill-tester` | (无描述) |
| `.gemini/skills/skillopt-sleep` | (无描述) |
| `.gemini/skills/skills-arquiteto-de-empresa` | (无描述) |
| `.gemini/skills/skills-chaos-engineering` | (无描述) |
| `.gemini/skills/skills-chief-ai-officer-advisor` | (无描述) |
| `.gemini/skills/skills-chief-customer-officer-advisor` | (无描述) |
| `.gemini/skills/skills-chief-data-officer-advisor` | (无描述) |
| `.gemini/skills/skills-eu-ai-act-specialist` | (无描述) |
| `.gemini/skills/skills-feature-flags-architect` | (无描述) |
| `.gemini/skills/skills-general-counsel-advisor` | (无描述) |
| `.gemini/skills/skills-handoff` | (无描述) |
| `.gemini/skills/skills-iso42001-specialist` | (无描述) |
| `.gemini/skills/skills-kubernetes-operator` | (无描述) |
| `.gemini/skills/skills-run` | (无描述) |
| `.gemini/skills/skills-slo-architect` | (无描述) |
| `.gemini/skills/skills-vpe-advisor` | (无描述) |
| `.gemini/skills/slo-architect` | (无描述) |
| `.gemini/skills/slo-design` | (无描述) |
| `.gemini/skills/snowflake-development` | (无描述) |
| `.gemini/skills/soc2-audit-prep` | (无描述) |
| `.gemini/skills/soc2-compliance` | (无描述) |
| `.gemini/skills/social-content` | (无描述) |
| `.gemini/skills/social-media-analyzer` | (无描述) |
| `.gemini/skills/social-media-manager` | (无描述) |
| `.gemini/skills/solo-founder` | (无描述) |
| `.gemini/skills/spawn` | (无描述) |
| `.gemini/skills/spec-driven-workflow` | (无描述) |
| `.gemini/skills/spec-to-repo` | (无描述) |
| `.gemini/skills/sprint-health` | (无描述) |
| `.gemini/skills/sprint-plan` | (无描述) |
| `.gemini/skills/sql-database-assistant` | (无描述) |
| `.gemini/skills/stage-launch` | (无描述) |
| `.gemini/skills/startup-cto` | (无描述) |
| `.gemini/skills/statistical-analyst` | (无描述) |
| `.gemini/skills/stock-analysis` | (无描述) |
| `.gemini/skills/strategic-alignment` | (无描述) |
| `.gemini/skills/stress-test` | (无描述) |
| `.gemini/skills/strict-api` | (无描述) |
| `.gemini/skills/stripe-integration-expert` | (无描述) |
| `.gemini/skills/swedish-mentor` | (无描述) |
| `.gemini/skills/syllabus` | (无描述) |
| `.gemini/skills/tc` | (无描述) |
| `.gemini/skills/tc-tracker` | (无描述) |
| `.gemini/skills/tdd` | (无描述) |
| `.gemini/skills/tdd-guide` | (无描述) |
| `.gemini/skills/team-communications` | (无描述) |
| `.gemini/skills/tech-debt` | (无描述) |
| `.gemini/skills/tech-debt-tracker` | (无描述) |
| `.gemini/skills/tech-stack-evaluator` | (无描述) |
| `.gemini/skills/TEMPLATE` | (无描述) |
| `.gemini/skills/terraform-patterns` | (无描述) |
| `.gemini/skills/testrail` | (无描述) |
| `.gemini/skills/threat-detection` | (无描述) |
| `.gemini/skills/ui-design-system` | (无描述) |
| `.gemini/skills/universal-scraping-architect` | (无描述) |
| `.gemini/skills/user-story` | (无描述) |
| `.gemini/skills/ux-researcher-designer` | (无描述) |
| `.gemini/skills/vendor-management` | (无描述) |
| `.gemini/skills/video-content-strategist` | (无描述) |
| `.gemini/skills/vpe-advisor` | (无描述) |
| `.gemini/skills/vpe-review` | (无描述) |
| `.gemini/skills/webinar-marketing` | (无描述) |
| `.gemini/skills/weekly-review` | (无描述) |
| `.gemini/skills/wiki-ingest` | (无描述) |
| `.gemini/skills/wiki-init` | (无描述) |
| `.gemini/skills/wiki-lint` | (无描述) |
| `.gemini/skills/wiki-log` | (无描述) |
| `.gemini/skills/wiki-query` | (无描述) |
| `.gemini/skills/workflow-builder` | (无描述) |
| `.gemini/skills/wrap-up` | (无描述) |
| `.gemini/skills/write-a-skill` | (无描述) |
| `.gemini/skills/x-twitter-growth` | (无描述) |
| `.gemini/skills/youtube-full` | (无描述) |
| `.gemini/skills/zero-hallucination-coder` | (无描述) |
| `agent-launcher/skills/agent-launcher-orchestrator` | Use when a user wants to build, launch, grade, or schedule a Claude Managed Agent (CMA) in their own Anthropic account — "build me… |
| `agent-launcher/skills/grade-iterate` | Phase 3 of building a Claude Managed Agent — the bounded grade→iterate loop. Define a CMA outcome (a required markdown rubric grad… |
| `agent-launcher/skills/interview` | Phase 1 of building a Claude Managed Agent — interview the founder about the one job the agent should do, then produce a build she… |
| `agent-launcher/skills/run-without-you` | Phase 4 of building a Claude Managed Agent — make it run without you. Turn a graded agent into a recurring scheduled deployment (P… |
| `agent-launcher/skills/stage-launch` | Phase 2 of building a Claude Managed Agent — turn a validated build sheet into exact API payloads and a resumable BYOK curl launch… |
| `agent-launcher/skills/wrap-up` | Close out a launched Claude Managed Agent — recap every primitive the founder now owns, regenerate the single-file overview page, … |
| `business-growth/skills/business-growth-skills` | "Router/index for the 4 business & growth skills bundled in this plugin: customer-success-manager (health scoring, churn risk, exp… |
| `business-growth/skills/contract-and-proposal-writer` | "Generate professional, jurisdiction-aware business documents: freelance contracts, project proposals, SOWs, NDAs, and MSAs. Struc… |
| `business-growth/skills/customer-success-manager` | Monitors customer health, predicts churn risk, and identifies expansion opportunities using weighted scoring models for SaaS custo… |
| `business-growth/skills/revenue-operations` | Analyzes sales pipeline health, revenue forecasting accuracy, and go-to-market efficiency metrics for SaaS revenue optimization. U… |
| `business-growth/skills/sales-engineer` | Analyzes RFP/RFI responses for coverage gaps, builds competitive feature comparison matrices, and plans proof-of-concept (POC) eng… |
| `business-operations/skills/business-operations-skills` | Use when running, diagnosing, or designing internal business operations — process documentation, vendor SLAs, capacity planning, i… |
| `business-operations/skills/capacity-planner` | "Use when an ops leader (Director of CX, Head of Support, VP Ops, Head of BizOps, Head of IT ops, Head of Finance ops) is sizing o… |
| `business-operations/skills/internal-comms` | Use when a Head of People Ops, BizOps lead, or Internal Communications owner needs to draft and sequence an internal-only change-m… |
| `business-operations/skills/knowledge-ops` | Use when a Head of Ops, Knowledge Manager, or TPM-Internal needs to author, validate, or clean up company SOPs and internal runboo… |
| `business-operations/skills/process-mapper` | Use when a BizOps lead, COO, or process-improvement owner needs to document an end-to-end business process (procurement, employee … |
| `business-operations/skills/procurement-optimizer` | Use when running an annual SaaS audit, doing category-level spend review, or rationalizing the supplier base — when the user needs… |
| `business-operations/skills/vendor-management` | Use when reviewing, scoring, or auditing third-party SaaS / vendor relationships — running a vendor scorecard with industry tuning… |
| `c-level-advisor/arquiteto-de-empresa/skills/arquiteto-de-empresa` | "Company Architect: builds a business from scratch as an OKF (Open Knowledge Format) bundle — a tree of version-controllable .md f… |
| `c-level-advisor/chief-ai-officer-advisor/skills/chief-ai-officer-advisor` | "Chief AI Officer advisory for startups: model build-vs-buy decisions (API vs fine-tune vs in-house), AI risk classification under… |
| `c-level-advisor/chief-customer-officer-advisor/skills/chief-customer-officer-advisor` | "Chief Customer Officer advisory for startups: retention decomposition (gross retention vs NRR honesty, churn root-cause taxonomy)… |
| `c-level-advisor/chief-data-officer-advisor/skills/chief-data-officer-advisor` | "Chief Data Officer advisory for startups: AI training data rights and consent provenance, data product strategy (warehouse vs lak… |
| `c-level-advisor/executive-mentor/skills/board-prep` | "Board meeting preparation for the adversarial scenario, not the friendly one. Forces numbers-cold mastery, anticipates hard quest… |
| `c-level-advisor/executive-mentor/skills/challenge` | "Pre-mortem plan analysis. Imagine the plan failed 12 months from now and work backwards to find the weaknesses. Surfaces assumpti… |
| `c-level-advisor/executive-mentor/skills/executive-mentor` | "Adversarial thinking partner for founders and executives. Stress-tests plans, prepares for brutal board meetings, dissects decisi… |
| `c-level-advisor/executive-mentor/skills/hard-call` | "/em:hard-call — Framework for decisions with no good options. Use when every option is painful and a structured 10/10/10 + regret… |
| `c-level-advisor/executive-mentor/skills/postmortem` | "/em:postmortem — Honest analysis of what went wrong. Use after a failed launch, missed quarter, or bad hire to run a blameless 5-… |
| `c-level-advisor/executive-mentor/skills/stress-test` | "/em:stress-test — Business assumption stress testing. Use before betting on a plan whose core assumptions are unvalidated — e.g. … |
| `c-level-advisor/general-counsel-advisor/skills/general-counsel-advisor` | "General Counsel advisory for startups: contract review (MSA, SaaS, NDA, DPA, employment), IP strategy, term sheet decoding, and r… |
| `c-level-advisor/skills/agent-protocol` | "Inter-agent communication protocol for C-suite agent teams. Defines invocation syntax, loop prevention, isolation rules, and resp… |
| `c-level-advisor/skills/arquiteto-de-empresa` | "Company Architect: builds a business from scratch as an OKF (Open Knowledge Format) bundle — a tree of version-controllable .md f… |
| `c-level-advisor/skills/board-deck-builder` | "Assembles comprehensive board and investor update decks by pulling perspectives from all C-suite roles. Use when preparing board … |
| `c-level-advisor/skills/board-meeting` | "Multi-agent board meeting protocol for strategic decisions. Runs a structured 6-phase deliberation: context loading, independent … |
| `c-level-advisor/skills/c-level-skills` | "Index and router for the C-level advisory bundle: 33 skills covering 14 C-suite roles, orchestration, cross-cutting capabilities,… |
| `c-level-advisor/skills/ceo-advisor` | "Executive leadership guidance for strategic decision-making, organizational development, and stakeholder management. Use when pla… |
| `c-level-advisor/skills/cfo-advisor` | "Financial leadership for startups and scaling companies. Financial modeling, unit economics, fundraising strategy, cash managemen… |
| `c-level-advisor/skills/change-management` | "Framework for rolling out organizational changes without chaos. Covers the ADKAR model adapted for startups, communication templa… |
| `c-level-advisor/skills/chief-ai-officer-advisor` | "Chief AI Officer advisory for startups: model build-vs-buy decisions (API vs fine-tune vs in-house), AI risk classification under… |
| `c-level-advisor/skills/chief-customer-officer-advisor` | "Chief Customer Officer advisory for startups: retention decomposition (gross retention vs NRR honesty, churn root-cause taxonomy)… |
| `c-level-advisor/skills/chief-data-officer-advisor` | "Chief Data Officer advisory for startups: AI training data rights and consent provenance, data product strategy (warehouse vs lak… |
| `c-level-advisor/skills/chief-of-staff` | "C-suite orchestration layer. Routes founder questions to the right advisor role(s), triggers multi-role board meetings for comple… |
| `c-level-advisor/skills/chro-advisor` | "People leadership for scaling companies. Hiring strategy, compensation design, org structure, culture, and retention. Use when bu… |
| `c-level-advisor/skills/ciso-advisor` | "Security leadership for growth-stage companies. Risk quantification in dollars, compliance roadmap (SOC 2/ISO 27001/HIPAA/GDPR), … |
| `c-level-advisor/skills/cmo-advisor` | "Marketing leadership for scaling companies. Brand positioning, growth model design, marketing budget allocation, and marketing or… |
| `c-level-advisor/skills/company-os` | "The meta-framework for how a company runs — the connective tissue between all C-suite roles. Covers operating system selection (E… |
| `c-level-advisor/skills/competitive-intel` | "Systematic competitor tracking that feeds CMO positioning, CRO battlecards, and CPO roadmap decisions. Use when analyzing competi… |
| `c-level-advisor/skills/context-engine` | "Loads and manages company context for all C-suite advisor skills. Reads ~/.claude/company-context.md, detects stale context (>90 … |
| `c-level-advisor/skills/coo-advisor` | "Operations leadership for scaling companies. Process design, OKR execution, operational cadence, and scaling playbooks. Use when … |
| `c-level-advisor/skills/cpo-advisor` | "Product leadership for scaling companies. Product vision, portfolio strategy, product-market fit, and product org design. Use whe… |
| `c-level-advisor/skills/cro-advisor` | "Revenue leadership for B2B SaaS companies. Revenue forecasting, sales model design, pricing strategy, net revenue retention, and … |
| `c-level-advisor/skills/cs-onboard` | "Founder onboarding interview that captures company context across 7 dimensions. Invoke with /cs:setup for initial interview or /c… |
| `c-level-advisor/skills/cto-advisor` | "Technical leadership guidance for engineering teams, architecture decisions, and technology strategy. Use when assessing technica… |
| `c-level-advisor/skills/culture-architect` | "Build, measure, and evolve company culture as operational behavior — not wall posters. Covers mission/vision/values workshops, va… |
| `c-level-advisor/skills/decision-logger` | "Two-layer memory architecture for board meeting decisions. Manages raw transcripts (Layer 1) and approved decisions (Layer 2). Us… |
| `c-level-advisor/skills/founder-coach` | "Personal leadership development for founders and first-time CEOs. Covers founder archetype identification, delegation frameworks,… |
| `c-level-advisor/skills/general-counsel-advisor` | "General Counsel advisory for startups: contract review (MSA, SaaS, NDA, DPA, employment), IP strategy, term sheet decoding, and r… |
| `c-level-advisor/skills/internal-narrative` | "Build and maintain one coherent company story across all audiences — employees, investors, customers, candidates, and partners. D… |
| `c-level-advisor/skills/intl-expansion` | "International market expansion strategy. Market selection, entry modes, localization, regulatory compliance, and go-to-market by … |
| `c-level-advisor/skills/ma-playbook` | "M&A strategy for acquiring companies or being acquired. Due diligence, valuation, integration, and deal structure. Use when evalu… |
| `c-level-advisor/skills/org-health-diagnostic` | "Cross-functional organizational health check combining signals from all C-suite roles. Scores 8 dimensions on a traffic-light sca… |
| `c-level-advisor/skills/scenario-war-room` | "Cross-functional what-if modeling for cascading multi-variable scenarios. Unlike single-assumption stress testing, this models co… |
| `c-level-advisor/skills/strategic-alignment` | "Cascades strategy from boardroom to individual contributor. Detects and fixes misalignment between company goals and team executi… |
| `c-level-advisor/skills/vpe-advisor` | "VP of Engineering advisory for startups: delivery throughput (DORA 4 metrics + bottleneck identification), engineering hiring fun… |
| `c-level-advisor/vpe-advisor/skills/vpe-advisor` | "VP of Engineering advisory for startups: delivery throughput (DORA 4 metrics + bottleneck identification), engineering hiring fun… |
| `c-level-agents/skills/boardroom` | "/cs:boardroom <brief> — 6-phase multi-role deliberation across the C-suite with Phase 2 isolation, critic pre-screen, and synthes… |
| `c-level-agents/skills/brief` | "/cs:brief <topic> — Generate a one-page strategy brief from an office-hours intake. First step in the strategic sprint pipeline. … |
| `c-level-agents/skills/c-level-agents` | "Founder-mode executive team. 13 cs-* C-suite agents (CFO, CMO, CRO, CPO, COO, CHRO, CISO, GC, CDO, CAIO, CCO, VPE, Chief of Staff… |
| `c-level-agents/skills/caio-review` | "/cs:caio-review <plan> — Eval-demanding Chief AI Officer interrogation of any plan that involves AI: model selection, risk classi… |
| `c-level-agents/skills/cco-review` | "/cs:cco-review <plan> — Retention-obsessed Chief Customer Officer interrogation of any plan that touches customer retention, segm… |
| `c-level-agents/skills/cdo-review` | "/cs:cdo-review <plan> — Decision-driven Chief Data Officer interrogation of any plan that touches training data, data architectur… |
| `c-level-agents/skills/cfo-review` | "/cs:cfo-review <plan> — Numerate-skeptic interrogation of any plan that touches money. Unit economics, runway, dilution, capital … |
| `c-level-agents/skills/ciso-review` | "/cs:ciso-review <plan> — Risk-paranoid interrogation of any plan that touches data, compliance, or production access. Use when la… |
| `c-level-agents/skills/cmo-review` | "/cs:cmo-review <plan> — Narrative-first interrogation of positioning, ICP, message house, and channel mix. Use when launching a c… |
| `c-level-agents/skills/cpo-review` | "/cs:cpo-review <plan> — JTBD-driven interrogation of product roadmap, PMF signal, and portfolio focus. Use when committing a quar… |
| `c-level-agents/skills/cro-review` | "/cs:cro-review <plan> — Pipeline-paranoid interrogation of revenue, win rate, NRR, and ramp time. Use when the forecast misses pi… |
| `c-level-agents/skills/cross-eval` | "/cs:cross-eval <memo> — Multi-model consensus on a board memo or strategy brief. Claude + Codex + Gemini cross-review with gracef… |
| `c-level-agents/skills/cto-review` | "/cs:cto-review <plan> — Architecture and scaling interrogation. Tech debt, scaling cliffs, team scaling, build-vs-buy. Use when c… |
| `c-level-agents/skills/decide` | "/cs:decide <memo> — Log a decision to two-layer memory via decision-logger. Approved memo becomes durable; raw transcripts kept f… |
| `c-level-agents/skills/execute` | "/cs:execute <decision> — Generate a 90-day execution plan with weekly milestones, DRIs, and check-in cadence from an approved dec… |
| `c-level-agents/skills/founder-mode` | "/cs:founder-mode <question> — Auto-routes any founder question to the right C-role advisor or to /cs:boardroom for multi-role top… |
| `c-level-agents/skills/freeze` | "/cs:freeze <decision> <days> — Lock a strategic decision for a cooldown period to prevent impulse reversal. Mirrors gstack's safe… |
| `c-level-agents/skills/gc-review` | "/cs:gc-review <plan> — General Counsel interrogation of contracts, IP, regulatory, term sheets, and employment-law surface. Use w… |
| `c-level-agents/skills/office-hours` | "/cs:office-hours <topic> — YC-style 6-question founder interrogation before any advice. Forces clarity on problem, customer, dist… |
| `c-level-agents/skills/onboard` | "/cs:onboard — Founder interview that populates ~/.claude/company-context.md using the canonical 7-dimension cs-onboard schema. Th… |
| `c-level-agents/skills/post-mortem` | "/cs:post-mortem <decision> — Honest retrospective on an executed decision, scored against original assumptions and dissent. Close… |
| `c-level-agents/skills/vpe-review` | "/cs:vpe-review <plan> — Throughput-first VP of Engineering interrogation of any plan that touches delivery, eng hiring, team stru… |
| `commercial/skills/channel-economics` | "Use when reviewing or rebalancing direct vs. partner-led channel economics — computing fully-loaded cost-to-serve per channel, ch… |
| `commercial/skills/commercial-forecaster` | "Use when building a quarterly bookings forecast, ARR projection, pipeline forecast, NRR projection, or commit/best-case/pipe-only… |
| `commercial/skills/commercial-policy` | "Use when designing or revising a company's commercial policy — the rules of engagement governing discounts off list price, approv… |
| `commercial/skills/commercial-skills` | Use when reviewing, approving, or designing commercial motion — pricing models, deal review, discount approval, partnership econom… |
| `commercial/skills/deal-desk` | Use when reviewing a specific inbound deal before close — when sales has asked for a discount that exceeds AE authority, when the … |
| `commercial/skills/partnerships-architect` | "Use when a startup is approached by a prospective partner and someone has to decide should we sign this partner, at what partner … |
| `commercial/skills/pricing-strategist` | "Use when designing or revisiting product pricing — selecting a pricing model (subscription seat-based, usage-based, value-based, … |
| `commercial/skills/rfp-responder` | "Use when an RFP, RFI, RFQ, security questionnaire, vendor questionnaire, or proposal request arrives and the team needs a structu… |
| `compliance-os/skills/ai-act-readiness` | "/cs:ai-act-readiness <system> — EU AI Act 6-question forcing interrogation. Use during AI-system intake, before EU deployment, or… |
| `compliance-os/skills/aims-audit` | "/cs:aims-audit <scope> — ISO/IEC 42001 AIMS internal-audit 6-question forcing interrogation. Use before certification stage 1, be… |
| `compliance-os/skills/compliance-os` | "Compliance OS — meta-orchestrator that lets compliance teams CONFIGURE which frameworks apply, COMPUTE cross-framework control ov… |
| `compliance-os/skills/compliance-readiness` | "/cs:compliance-readiness <program> — Multi-framework compliance officer 6-question forcing interrogation of any compliance progra… |
| `compliance-os/skills/fda-qsr-audit-prep` | "/cs:fda-qsr-audit-prep <scope> — FDA 21 CFR 820 (QSR / QMSR) audit 6-question forcing interrogation. Post-Feb 2026 substantially … |
| `compliance-os/skills/gdpr-audit-prep` | "/cs:gdpr-audit-prep <scope> — GDPR audit 6-question Article-cited forcing interrogation. Use before annual internal GDPR review, … |
| `compliance-os/skills/iso13485-audit-prep` | "/cs:iso13485-audit-prep <scope> — ISO 13485 QMS audit 6-question forcing interrogation. Design controls + CAPA + post-market focu… |
| `compliance-os/skills/iso27001-audit-prep` | "/cs:iso27001-audit-prep <scope> — ISO 27001 ISMS audit readiness 6-question forcing interrogation. Use before annual Clause 9.2 i… |
| `compliance-os/skills/soc2-audit-prep` | "/cs:soc2-audit-prep <scope> — SOC 2 Type II readiness 6-question forcing interrogation. Observation-period focused. Use before Ty… |
| `engineering-team/a11y-audit/skills/a11y-audit` | "Accessibility audit skill for scanning, fixing, and verifying WCAG 2.2 Level A and AA compliance across React, Next.js, Vue, Angu… |
| `engineering-team/google-workspace-cli/skills/google-workspace-cli` | "Google Workspace administration via the gws CLI (github.com/googleworkspace/cli). Install, authenticate, and automate Gmail, Driv… |
| `engineering-team/playwright-pro/skills/browserstack` | >- |
| `engineering-team/playwright-pro/skills/fix` | >- |
| `engineering-team/playwright-pro/skills/generate` | >- |
| `engineering-team/playwright-pro/skills/migrate` | >- |
| `engineering-team/playwright-pro/skills/pw` | "Production-grade Playwright testing toolkit. Use when the user mentions Playwright tests, end-to-end testing, browser automation,… |
| `engineering-team/playwright-pro/skills/pw-init` | >- |
| `engineering-team/playwright-pro/skills/pw-review` | >- |
| `engineering-team/playwright-pro/skills/report` | >- |
| `engineering-team/playwright-pro/skills/testrail` | >- |
| `engineering-team/self-improving-agent/skills/extract` | "Turn a proven pattern or debugging solution into a standalone reusable skill with SKILL.md, reference docs, and examples. Use whe… |
| `engineering-team/self-improving-agent/skills/memory-review` | "Analyze auto-memory for promotion candidates, stale entries, consolidation opportunities, and health metrics. Use when the user r… |
| `engineering-team/self-improving-agent/skills/memory-status` | "Memory health dashboard showing line counts, topic files, capacity, stale entries, and recommendations. Use when the user runs /s… |
| `engineering-team/self-improving-agent/skills/promote` | "Graduate a proven pattern from auto-memory (MEMORY.md) to CLAUDE.md or .claude/rules/ for permanent enforcement. Use when the use… |
| `engineering-team/self-improving-agent/skills/remember` | "Explicitly save important knowledge to auto-memory with timestamp and context. Use when a discovery is too important to rely on a… |
| `engineering-team/self-improving-agent/skills/self-improving-agent` | "Curate Claude Code's auto-memory into durable project knowledge. Analyze MEMORY.md for patterns, promote proven learnings to CLAU… |
| `engineering-team/skills/adversarial-reviewer` | "Adversarial code review that breaks the self-review monoculture. Use when you want a genuinely critical review of recent changes,… |
| `engineering-team/skills/ai-security` | "Use when assessing AI/ML systems for prompt injection, jailbreak vulnerabilities, model inversion risk, data poisoning exposure, … |
| `engineering-team/skills/aws-solution-architect` | Design AWS architectures for startups using serverless patterns and IaC templates. Use when asked to design serverless architectur… |
| `engineering-team/skills/azure-cloud-architect` | "Design Azure architectures for startups and enterprises. Use when asked to design Azure infrastructure, create Bicep/ARM template… |
| `engineering-team/skills/cloud-security` | "Use when assessing cloud infrastructure for security misconfigurations, IAM privilege escalation paths, S3 public exposure, open … |
| `engineering-team/skills/code-reviewer` | Code review automation for TypeScript, JavaScript, Python, Go, Swift, Kotlin, C#, .NET, Java, C, C++, Rust, Ruby, PHP, and Dart/Fl… |
| `engineering-team/skills/email-template-builder` | "Build complete transactional email systems: React Email templates, provider integration (Resend, Postmark, SendGrid, AWS SES), pr… |
| `engineering-team/skills/embedded-iot-mentor` | Mentor for embedded and IoT hardware projects. Helps select MCUs, dev boards, and toolchains, decides where sensor readings end up… |
| `engineering-team/skills/engineering-skills` | "Index of the engineering-team skills bundle for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw, and 6 more tools. Architecture,… |
| `engineering-team/skills/epic-design` | > |
| `engineering-team/skills/gcp-cloud-architect` | "Design GCP architectures for startups and enterprises. Use when asked to design Google Cloud infrastructure, deploy to GKE or Clo… |
| `engineering-team/skills/incident-commander` | "Comprehensive incident response framework from detection through resolution and post-incident review. Battle-tested SRE/DevOps pr… |
| `engineering-team/skills/incident-response` | "Use when a security incident has been detected or declared and needs classification, triage, escalation path determination, and f… |
| `engineering-team/skills/ms365-tenant-manager` | Microsoft 365 tenant administration for Global Administrators. Automate M365 tenant setup, Office 365 admin tasks, Azure AD user m… |
| `engineering-team/skills/named-persona-adversarial-review` | "Code review through the lens of real engineers' documented philosophies (Torvalds, Thompson, Carmack, Kent Beck, Jobs, Cagan). Co… |
| `engineering-team/skills/red-team` | "Use when planning or executing authorized red team engagements, attack path analysis, or offensive security simulations. Covers M… |
| `engineering-team/skills/security-pen-testing` | "Use when the user asks to perform security audits, penetration testing, vulnerability scanning, OWASP Top 10 checks, or offensive… |
| `engineering-team/skills/senior-architect` | This skill should be used when the user asks to "design system architecture", "evaluate microservices vs monolith", "create archit… |
| `engineering-team/skills/senior-backend` | Designs and implements backend systems including REST APIs, microservices, database architectures, authentication flows, and secur… |
| `engineering-team/skills/senior-computer-vision` | Computer vision engineering skill for object detection, image segmentation, and visual AI systems. Covers CNN and Vision Transform… |
| `engineering-team/skills/senior-data-engineer` | Data engineering skill for building scalable data pipelines, ETL/ELT systems, and data infrastructure. Expertise in Python, SQL, S… |
| `engineering-team/skills/senior-data-scientist` | World-class senior data scientist skill specialising in statistical modeling, experiment design, causal inference, and predictive … |
| `engineering-team/skills/senior-devops` | Comprehensive DevOps skill for CI/CD, infrastructure automation, containerization, and cloud platforms (AWS, GCP, Azure). Includes… |
| `engineering-team/skills/senior-frontend` | Frontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. Use when building React components, opti… |
| `engineering-team/skills/senior-fullstack` | Fullstack development toolkit with project scaffolding for Next.js, FastAPI, MERN, and Django stacks, code quality analysis with s… |
| `engineering-team/skills/senior-ml-engineer` | ML engineering skill for productionizing models, building MLOps pipelines, and integrating LLMs. Covers model deployment, feature … |
| `engineering-team/skills/senior-prompt-engineer` | Use when the user asks to optimize prompts, design prompt templates, evaluate LLM outputs with an eval set, measure RAG retrieval … |
| `engineering-team/skills/senior-qa` | Generates unit tests, integration tests, and E2E tests for React/Next.js applications. Scans components to create Jest + React Tes… |
| `engineering-team/skills/senior-secops` | Senior SecOps engineer skill for application security, vulnerability management, compliance verification, and secure development p… |
| `engineering-team/skills/senior-security` | Use when the user asks for STRIDE threat modeling, DREAD risk scoring, data-flow-diagram threat analysis, or a quick secret scan —… |
| `engineering-team/skills/stripe-integration-expert` | "Production-grade Stripe integrations: subscriptions with trials and proration, one-time payments, usage-based billing, checkout s… |
| `engineering-team/skills/tdd-guide` | "Test-driven development skill for writing unit tests, generating test fixtures and mocks, analyzing coverage gaps, and guiding re… |
| `engineering-team/skills/tech-stack-evaluator` | Technology stack evaluation and comparison with TCO analysis, security assessment, and ecosystem health scoring. Use when comparin… |
| `engineering-team/skills/threat-detection` | "Use when hunting for threats in an environment, analyzing IOCs, or detecting behavioral anomalies in telemetry. Covers hypothesis… |
| `engineering-team/snowflake-development/skills/snowflake-development` | "Use when writing Snowflake SQL, building data pipelines with Dynamic Tables or Streams/Tasks, using Cortex AI functions, creating… |
| `engineering/agent-harness/skills/agent-harness` | "Turn any domain folder of skills into a bounded agentic loop: compile a goal into a verifiable task plan, execute tasks with the … |
| `engineering/agent-memory/skills/agent-memory` | Use when a project's CLAUDE.md has grown past what anyone reads and you want the agent to learn durable facts from its own session… |
| `engineering/agenthub/skills/agenthub` | "Multi-agent collaboration plugin that spawns N parallel subagents competing on the same task via git worktree isolation. Agents w… |
| `engineering/agenthub/skills/board` | "Read, write, and browse the AgentHub message board for agent coordination. Use when the user runs /hub:board or asks to post, rea… |
| `engineering/agenthub/skills/eval` | "Evaluate and rank agent results by metric or LLM judge for an AgentHub session. Use when the user runs /hub:eval or asks to score… |
| `engineering/agenthub/skills/hub-init` | "Create a new AgentHub collaboration session with task, agent count, and evaluation criteria. Use when the user runs /hub:hub-init… |
| `engineering/agenthub/skills/hub-status` | "Show DAG state, agent progress, and branch status for an AgentHub session. Use when the user runs /hub:hub-status or asks how the… |
| `engineering/agenthub/skills/merge` | "Merge the winning agent's branch into base, archive losers, and clean up worktrees. Use when the user runs /hub:merge or asks to … |
| `engineering/agenthub/skills/run` | "One-shot lifecycle command that chains init → baseline → spawn → eval → merge in a single invocation. Use when the user runs /hub… |
| `engineering/agenthub/skills/spawn` | "Launch N parallel subagents in isolated git worktrees to compete on the session task. Use when the user runs /hub:spawn or asks t… |
| `engineering/autoresearch-agent/skills/ar-resume` | "Resume a paused experiment. Checkout the experiment branch, read results history, continue iterating. Use when the user runs /ar:… |
| `engineering/autoresearch-agent/skills/ar-status` | "Show experiment dashboard with results, active loops, and progress. Use when the user runs /ar:ar-status or asks how an autoresea… |
| `engineering/autoresearch-agent/skills/autoresearch-agent` | "Autonomous experiment loop that optimizes any file by a measurable metric. Inspired by Karpathy's autoresearch. The agent edits a… |
| `engineering/autoresearch-agent/skills/loop` | "Start an autonomous experiment loop with user-selected interval (10min, 1h, daily, weekly, monthly). Uses CronCreate for scheduli… |
| `engineering/autoresearch-agent/skills/run` | "Run a single experiment iteration. Edit the target file, evaluate, keep or discard. Use when the user runs /ar:run or asks for on… |
| `engineering/autoresearch-agent/skills/setup` | "Set up a new autoresearch experiment interactively. Collects domain, target file, eval command, metric, direction, and evaluator.… |
| `engineering/behuman/skills/behuman` | "Use when the user wants more human-like AI responses — less robotic, less listy, more authentic. Triggers: 'behuman', 'be real', … |
| `engineering/book-to-skill/skills/book-to-skill` | "Converts books, documentation folders, and source collections (PDF, EPUB, DOCX, HTML, Markdown, RST, AsciiDoc, RTF, MOBI/AZW) int… |
| `engineering/boost-asio-pro` | "Use when writing or reviewing asynchronous C++ networking code with Boost.Asio or standalone Asio — TCP/UDP servers and clients, … |
| `engineering/caveman/skills/caveman` | > |
| `engineering/chaos-engineering/skills/chaos-engineering` | Use when planning, running, or learning from chaos engineering experiments. Triggers on "chaos experiment", "fault injection", "ga… |
| `engineering/claude-coach/skills/claude-coach` | Personal coach that teaches users to become Claude power users. Use this skill the FIRST time a user asks to "learn Claude", "be a… |
| `engineering/code-tour/skills/code-tour` | "Use when the user asks to create a CodeTour .tour file — persona-targeted, step-by-step walkthroughs that link to real files and … |
| `engineering/collab-proof/skills/collab-proof` | "Use when you want to understand what Claude contributed vs what you drove in a session. Triggers on: /collab-proof, session retro… |
| `engineering/data-quality-auditor/skills/data-quality-auditor` | Audit datasets for completeness, consistency, accuracy, and validity. Profile data distributions, detect anomalies and outliers, s… |
| `engineering/deep-learning-book/skills/deep-learning-book` | "Study companion and working knowledge base for the Deep Learning textbook by Goodfellow, Bengio & Courville (MIT Press, 2016), re… |
| `engineering/demo-video/skills/demo-video` | "Use when the user asks to create a demo video, product walkthrough, feature showcase, animated presentation, marketing video, or … |
| `engineering/docker-development/skills/docker-development` | "Docker and container development agent skill and plugin for Dockerfile optimization, docker-compose orchestration, multi-stage bu… |
| `engineering/feature-flags-architect/skills/feature-flags-architect` | Use when adding, retiring, or auditing feature flags. Triggers on "add a flag", "ship behind a flag", "rollout plan", "kill switch… |
| `engineering/grill-me/skills/grill-me` | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision … |
| `engineering/grill-with-docs/skills/grill-with-docs` | Docs-anchored grilling session — challenges a plan against the project's existing language (CONTEXT.md) and recorded decisions (do… |
| `engineering/handoff/skills/handoff` | Compact the current conversation into a handoff document for another agent to pick up. References existing artifacts (PRDs, plans,… |
| `engineering/helm-chart-builder/skills/helm-chart-builder` | "Helm chart development agent skill and plugin for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw — chart scaffolding, values de… |
| `engineering/hivemind` | Orchestrate free opencode workers from Claude Code to cut token costs. Use when delegating grunt work to a single worker or a para… |
| `engineering/human-gate/skills/human-gate` | "Runs the human-verification lane of an agent loop, and proves review happened before work is called done. Builds a single-file HT… |
| `engineering/karpathy-coder/skills/karpathy-coder` | Use when writing, reviewing, or committing code to enforce Karpathy's 4 coding principles — surface assumptions before coding, kee… |
| `engineering/kubernetes-operator/skills/kubernetes-operator` | Use when building a Kubernetes Operator — custom controllers that reconcile CRD state. Triggers on "build an operator", "CRD desig… |
| `engineering/llm-cost-optimizer/skills/llm-cost-optimizer` | "Use proactively whenever LLM API costs come up -- or should. Triggers include: 'my AI costs are too high', 'optimize token usage'… |
| `engineering/llm-wiki/skills/llm-wiki` | Use when building or maintaining a persistent personal knowledge base (second brain) in Obsidian where an LLM incrementally ingest… |
| `engineering/memory-engineering/skills/memory-engineering` | Use when designing, reviewing, or paying for an agent memory system — adding memory to an agent, choosing between long-context / R… |
| `engineering/minimalist` | "Use when the user asks to write code efficiently, avoid over-engineering, reduce dependencies, or prevent unnecessary abstraction… |
| `engineering/prompt-governance/skills/prompt-governance` | "Use when managing prompts in production at scale: versioning prompts, running A/B tests on prompts, building prompt registries, p… |
| `engineering/security-guidance/skills/security-guidance` | PreToolUse security-anti-pattern hook for Claude Code. Catches 12 common security risks (command injection, XSS, SQL injection, un… |
| `engineering/skill-doctor/skills/skill-doctor` | Use when the user wants their agent setup graded from real conversation history, asks which installed skills are actually working,… |
| `engineering/skillopt-sleep/skills/skillopt-sleep` | "Use when the user wants their Claude agent to self-improve from past usage, asks about a nightly/offline 'sleep' or 'dream' cycle… |
| `engineering/skills/agent-designer` | "Use when the user asks to design a multi-agent system, pick an orchestration pattern (supervisor/swarm/pipeline), generate tool s… |
| `engineering/skills/agent-workflow-designer` | "Design production-grade multi-agent workflows with clear pattern choice (sequential, parallel, hierarchical), handoff contracts, … |
| `engineering/skills/api-design-reviewer` | "Comprehensive REST API design review with automated linting, breaking-change detection, and design scorecards. Catches inconsiste… |
| `engineering/skills/api-test-suite-builder` | "Use when the user asks to generate API tests, create integration test suites, test REST endpoints, or build contract tests." |
| `engineering/skills/browser-automation` | "Use when the user asks to automate browser tasks, scrape websites, fill forms, capture screenshots, extract structured data from … |
| `engineering/skills/changelog-generator` | "Produce consistent, auditable release notes from Conventional Commits. Separates commit parsing, semantic-bump logic, and changel… |
| `engineering/skills/chaos-engineering` | Use when planning, running, or learning from chaos engineering experiments. Triggers on "chaos experiment", "fault injection", "ga… |
| `engineering/skills/ci-cd-pipeline-builder` | "Generate pragmatic CI/CD pipelines from detected project stack signals — fast baseline generation, repeatable checks, environment… |
| `engineering/skills/codebase-onboarding` | "Analyze a codebase and generate onboarding documentation for engineers, tech leads, and contractors. Fast fact-gathering and repe… |
| `engineering/skills/database-designer` | "Use when the user asks to design database schemas, plan data migrations, optimize queries, choose between SQL and NoSQL, or model… |
| `engineering/skills/database-schema-designer` | "Use when the user asks to create ERD diagrams, normalize database schemas, design table relationships, or plan schema migrations.… |
| `engineering/skills/dependency-auditor` | "Audit and manage dependencies across multi-language projects. Identifies vulnerabilities, license conflicts, transitive dependenc… |
| `engineering/skills/engineering-advanced-skills` | "Index of 37 advanced engineering agent skills for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. Use when browsing or choosing… |
| `engineering/skills/env-secrets-manager` | "Manage environment-variable hygiene and secrets safety across local development and production. Practical auditing, drift awarene… |
| `engineering/skills/feature-flags-architect` | Use when adding, retiring, or auditing feature flags. Triggers on "add a flag", "ship behind a flag", "rollout plan", "kill switch… |
| `engineering/skills/focused-fix` | "Use when the user asks to fix, debug, or make a specific feature/module/area work end-to-end. Triggers: 'make X work', 'fix the Y… |
| `engineering/skills/full-page-screenshot` | "Use when the user asks to capture a full-page screenshot, long screenshot, or complete page capture of a web page. Handles SPA sc… |
| `engineering/skills/git-worktree-manager` | "Run parallel feature work safely with Git worktrees. Standardizes branch isolation, port allocation, environment sync, and cleanu… |
| `engineering/skills/interview-system-designer` | This skill should be used when the user asks to "design interview processes", "create hiring pipelines", "calibrate interview loop… |
| `engineering/skills/kubernetes-operator` | Use when building a Kubernetes Operator — custom controllers that reconcile CRD state. Triggers on "build an operator", "CRD desig… |
| `engineering/skills/mcp-server-builder` | "Design and ship production-ready MCP (Model Context Protocol) servers from OpenAPI contracts instead of hand-written tool wrapper… |
| `engineering/skills/migration-architect` | "Zero-downtime migration planning, compatibility validation, and rollback strategy generation. Tools for system, database, and inf… |
| `engineering/skills/monorepo-navigator` | "Navigate, manage, and optimize monorepos. Covers Turborepo, Nx, pnpm workspaces, and Lerna. Cross-package impact analysis, select… |
| `engineering/skills/observability-designer` | "Design production-ready observability strategies combining metrics, logs, and traces. Includes SLI/SLO design, golden-signals mon… |
| `engineering/skills/performance-profiler` | "Systematic performance profiling for Node.js, Python, and Go applications. Identifies CPU, memory, and I/O bottlenecks, generates… |
| `engineering/skills/pr-review-expert` | "Use when the user asks to review pull requests, analyze code changes, check for security issues in PRs, or assess code quality of… |
| `engineering/skills/rag-architect` | "Use when the user asks to design a RAG pipeline, choose a chunking strategy or embedding model, pick a vector database, or evalua… |
| `engineering/skills/runbook-generator` | "Generate operational runbooks from a service name — deployment, incident response, maintenance, and rollback workflows. Templated… |
| `engineering/skills/secrets-vault-manager` | "Use when the user asks to set up secret management infrastructure, integrate HashiCorp Vault, configure cloud secret stores (AWS … |
| `engineering/skills/self-eval` | "Honestly evaluate AI work quality using a two-axis scoring system. Use after completing a task, code review, or work session to g… |
| `engineering/skills/ship-gate` | > |
| `engineering/skills/skill-security-auditor` | > |
| `engineering/skills/skill-tester` | "Validate, test, and score the quality of skills within the claude-skills ecosystem. Comprehensive meta-skill: structure validatio… |
| `engineering/skills/skill-tester/assets/sample-skill` | "Reference BASIC-tier skill used as a fixture by skill-tester. Counts words and characters and applies basic text transformations.… |
| `engineering/skills/slo-architect` | Use when defining, reviewing, or operating SLOs/SLIs/error budgets. Triggers on "define an SLO", "what should our SLO be", "error … |
| `engineering/skills/spec-driven-workflow` | "Use when the user asks to write specs before code, define acceptance criteria, plan features before implementation, generate test… |
| `engineering/skills/sql-database-assistant` | "Use when the user asks to write SQL queries, optimize database performance, generate migrations, explore database schemas, or wor… |
| `engineering/skills/tc-tracker` | "Use when the user asks to track technical changes, create change records, manage TC lifecycles, or hand off work between AI sessi… |
| `engineering/skills/tech-debt-tracker` | Scan codebases for technical debt, score severity, track trends, and generate prioritized remediation plans. Use when users mentio… |
| `engineering/slo-architect/skills/slo-architect` | Use when defining, reviewing, or operating SLOs/SLIs/error budgets. Triggers on "define an SLO", "what should our SLO be", "error … |
| `engineering/spinning-up-deep-rl/skills/spinning-up-deep-rl` | "Knowledge base from \"Spinning Up in Deep RL\" by Joshua Achiam (OpenAI, MIT-licensed). Use when applying Achiam's frameworks for… |
| `engineering/statistical-analyst/skills/statistical-analyst` | Run hypothesis tests, analyze A/B experiment results, calculate sample sizes, and interpret statistical significance with effect s… |
| `engineering/strict-api` | "Use when the user says 'no hallucinations', 'verify APIs', 'reality check', or 'don't invent functions'. Prevents the agent from … |
| `engineering/terraform-patterns/skills/terraform-patterns` | "Terraform infrastructure-as-code agent skill and plugin for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw. Covers module desig… |
| `engineering/universal-scraping-architect/skills/universal-scraping-architect` | "Use for web scraping, crawling, document extraction, API parsing, or building validation-heavy data pipelines using Firecrawl or … |
| `engineering/workflow-builder/skills/workflow-builder` | Design and write deterministic multi-agent workflow scripts (.js files in .claude/workflows/) for Claude Code's Workflow tool. Use… |
| `engineering/write-a-skill/skills/write-a-skill` | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write… |
| `engineering/zero-hallucination-coder/skills/zero-hallucination-coder` | "Runs a disciplined Discuss -> Map -> Decompose -> Execute -> Verify loop that grounds code in verified structure — no invented AP… |
| `finance/business-investment-advisor/skills/business-investment-advisor` | "Business investment analysis and capital allocation advisor. Use when evaluating whether to invest in equipment, real estate, a n… |
| `finance/skills/finance-skills` | "Router/index for the 2 finance skills bundled in this plugin: financial-analyst (ratio analysis, DCF valuation, budget variance, … |
| `finance/skills/financial-analyst` | Performs financial ratio analysis, DCF valuation, budget variance analysis, and rolling forecast construction for strategic decisi… |
| `finance/skills/saas-metrics-coach` | SaaS financial health advisor. Use when a user shares revenue or customer numbers, or mentions ARR, MRR, churn, LTV, CAC, NRR, or … |
| `finance/skills/stock-analysis` | Produce a rigorous, sector-relative, multi-factor fundamental analysis of a publicly listed company — Indian (NSE/BSE) or US/globa… |
| `loop-library` | Discover, find, compare, audit, repair, adapt, and design repeatable AI-agent loops with explicit triggers, actions, verification,… |
| `markdown-html/skills/design-system` | Captures the user's brand identity once via a 10-question onboarding wizard (primary/accent HEX + heading + body Google Fonts + de… |
| `markdown-html/skills/markdown-html-orchestrator` | Use when a user wants to convert any markdown file in their Claude project into a single-file, lightly-interactive HTML — long-for… |
| `markdown-html/skills/md-document` | Converts long-form markdown (specs, RFCs, reports, plans, explainers) into a single-file, lightly-interactive HTML document with s… |
| `markdown-html/skills/md-review` | Converts a markdown PR writeup or code review (one with ```diff fenced blocks and severity-tagged > [!BLOCKER]/[!MAJOR]/[!MINOR]/[… |
| `markdown-html/skills/md-slides` | "Converts a markdown deck (slides separated by `---` HR boundaries or by `# ` H1 headings, with optional `<!-- notes: ... -->` pre… |
| `marketing-skill/skills/ab-test-setup` | When the user wants to plan, design, or implement an A/B test or experiment. Also use when the user mentions "A/B test," "split te… |
| `marketing-skill/skills/ad-creative` | "When the user needs to generate, iterate, or scale ad creative for paid advertising. Use when they say 'write ad copy,' 'generate… |
| `marketing-skill/skills/aeo` | "Answer Engine Optimization (AEO) skill — optimize content to be cited by AI language models (ChatGPT, Perplexity, Claude, Gemini,… |
| `marketing-skill/skills/analytics-tracking` | "Set up, audit, and debug analytics tracking implementation — GA4, Google Tag Manager, event taxonomy, conversion tracking, and da… |
| `marketing-skill/skills/app-store-optimization` | App Store Optimization (ASO) toolkit for researching keywords, analyzing competitor rankings, generating metadata suggestions, and… |
| `marketing-skill/skills/brand-guidelines` | "When the user wants to apply, document, or enforce brand guidelines for any product or company. Also use when the user mentions '… |
| `marketing-skill/skills/business-name-fit` | Suggest, pick, or vet a business, startup, or product name that stays true to the founder's cultural origin while working professi… |
| `marketing-skill/skills/campaign-analytics` | Analyzes campaign performance with multi-touch attribution, funnel conversion analysis, and ROI calculation for marketing optimiza… |
| `marketing-skill/skills/churn-prevention` | "Reduce voluntary and involuntary churn through cancel flow design, save offers, exit surveys, and dunning sequences. Use when des… |
| `marketing-skill/skills/cold-email` | "When the user wants to write, improve, or build a sequence of B2B cold outreach emails to prospects who haven't asked to hear fro… |
| `marketing-skill/skills/competitor-alternatives` | "When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the user men… |
| `marketing-skill/skills/content-creator` | "Deprecated redirect skill that routes legacy 'content creator' requests to the correct specialist. Use when a user invokes 'conte… |
| `marketing-skill/skills/content-humanizer` | "Makes AI-generated content sound genuinely human — not just cleaned up, but alive. Use when content feels robotic, uses too many … |
| `marketing-skill/skills/content-production` | "Full content production pipeline — takes a topic from blank page to published-ready piece. Use when you need to execute content: … |
| `marketing-skill/skills/content-strategy` | "When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when … |
| `marketing-skill/skills/copy-editing` | "When the user wants to edit, review, or improve existing marketing copy. Also use when the user mentions 'edit this copy,' 'revie… |
| `marketing-skill/skills/copywriting` | "When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages,… |
| `marketing-skill/skills/email-sequence` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also… |
| `marketing-skill/skills/form-cro` | When the user wants to optimize any form that is NOT signup/registration — including lead capture forms, contact forms, demo reque… |
| `marketing-skill/skills/free-tool-strategy` | "When the user wants to build a free tool for marketing — lead generation, SEO value, or brand awareness. Use when they mention 'e… |
| `marketing-skill/skills/launch-strategy` | "When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,… |
| `marketing-skill/skills/local-seo-manager` | "Manage local SEO for service-area businesses — appliance repair, HVAC, plumbing, cleaning, and any business that serves customers… |
| `marketing-skill/skills/marketing-context` | "Create and maintain the marketing context document that all marketing skills read before starting. Use when the user mentions 'ma… |
| `marketing-skill/skills/marketing-demand-acquisition` | Creates demand generation campaigns, optimizes paid ad spend across LinkedIn, Google, and Meta, develops SEO strategies, and struc… |
| `marketing-skill/skills/marketing-ideas` | "When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks f… |
| `marketing-skill/skills/marketing-ops` | "Central router for the marketing skill ecosystem. Use when unsure which marketing skill to use, when orchestrating a multi-skill … |
| `marketing-skill/skills/marketing-psychology` | "When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user … |
| `marketing-skill/skills/marketing-skills` | "Directory and router for the marketing skills library. Use when you need to find the right marketing skill for a task, see what m… |
| `marketing-skill/skills/marketing-strategy-pmm` | Product marketing skill for positioning, GTM strategy, competitive intelligence, and product launches. Use when the user asks abou… |
| `marketing-skill/skills/onboarding-cro` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the… |
| `marketing-skill/skills/page-cro` | When the user wants to optimize, improve, or increase conversions on any marketing page — including homepage, landing pages, prici… |
| `marketing-skill/skills/paid-ads` | "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other … |
| `marketing-skill/skills/paywall-upgrade-cro` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the use… |
| `marketing-skill/skills/popup-cro` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when t… |
| `marketing-skill/skills/pricing-strategy` | "Design, optimize, and communicate SaaS pricing — tier structure, value metrics, pricing pages, and price increase strategy. Use w… |
| `marketing-skill/skills/programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SE… |
| `marketing-skill/skills/prompt-engineer-toolkit` | "Turns marketing prompts into tested, versioned production assets: A/B prompt evaluation against structured test cases, immutable … |
| `marketing-skill/skills/referral-program` | "When the user wants to design, launch, or optimize a referral or affiliate program. Use when they mention 'referral program,' 'af… |
| `marketing-skill/skills/schema-markup` | "When the user wants to implement, audit, or validate structured data (schema markup) on their website. Use when the user mentions… |
| `marketing-skill/skills/seo-audit` | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technica… |
| `marketing-skill/skills/signup-flow-cro` | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions… |
| `marketing-skill/skills/site-architecture` | "When the user wants to audit, redesign, or plan their website's structure, URL hierarchy, navigation design, or internal linking … |
| `marketing-skill/skills/social-content` | "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Fac… |
| `marketing-skill/skills/social-media-analyzer` | Social media campaign analysis and performance tracking. Calculates engagement rates, ROI, and benchmarks across platforms. Use wh… |
| `marketing-skill/skills/social-media-manager` | "When the user wants to develop social media strategy, plan content calendars, manage community engagement, or grow their social p… |
| `marketing-skill/skills/webinar-marketing` | "When the user wants to plan, promote, run, or improve a webinar or virtual event to generate and convert demand. Use when the use… |
| `marketing-skill/skills/x-twitter-growth` | "X/Twitter growth engine for building audience, crafting viral content, and analyzing engagement. Use when the user wants to grow … |
| `marketing-skill/skills/youtube-full` | "Use when the user needs YouTube transcripts, video search, channel browsing, playlist extraction, or content monitoring. Trigger … |
| `marketing-skill/video-content-strategist/skills/video-content-strategist` | "Use when planning video content strategy, writing video scripts, optimizing YouTube channels, building short-form video pipelines… |
| `marketing/landing/skills/landing` | "Generates a premium single-page HTML landing page with 3D CSS animations, GSAP scroll effects, and mouse-parallax depth. Forcing … |
| `marketing/linkedin/skills/linkedin-analytics` | Use when someone wants to understand their own LinkedIn numbers — which posts worked, why reach dropped, whether a pattern is real… |
| `marketing/linkedin/skills/linkedin-content` | Use when someone wants to write, edit, or lint a LinkedIn post — a story, how-to, opinion piece, carousel script, video script, or… |
| `marketing/linkedin/skills/linkedin-engagement` | Use when someone wants to grow reach through comments, replies, groups, or outreach on LinkedIn — a commenting roster, a connectio… |
| `marketing/linkedin/skills/linkedin-profile` | Use when someone wants their LinkedIn profile audited or rewritten — headline, About section, experience bullets, Featured, banner… |
| `marketing/linkedin/skills/linkedin-skills` | Use when someone wants to grow an organic LinkedIn presence — a content strategy for a career change or consulting or thought lead… |
| `marketing/linkedin/skills/linkedin-strategy` | Use when someone needs a LinkedIn plan rather than a post — content pillars, positioning for a career change or consulting or thou… |
| `product-team/agile-product-owner/skills/agile-product-owner` | Agile product ownership for backlog management and sprint execution. Covers user story writing, acceptance criteria, sprint planni… |
| `product-team/apple-hig-expert/skills/apple-hig-expert` | "Audits and designs iOS/macOS/watchOS/visionOS interfaces against the Apple Human Interface Guidelines, including the Liquid Glass… |
| `product-team/code-to-prd/skills/code-to-prd` | "Reverse-engineer any codebase into a complete Product Requirements Document (PRD). Analyzes routes, components, state management,… |
| `product-team/research-summarizer/skills/research-summarizer` | "Structured research summarization agent skill for non-dev users. Handles academic papers, web articles, reports, and documentatio… |
| `product-team/skills/competitive-teardown` | "Analyzes competitor products and companies by synthesizing data from pricing pages, app store reviews, job postings, SEO signals,… |
| `product-team/skills/experiment-designer` | Use when planning product experiments, writing testable hypotheses, estimating sample size, prioritizing tests, or interpreting A/… |
| `product-team/skills/landing-page-generator` | "Generates high-converting landing pages as complete Next.js/React (TSX) components with Tailwind CSS. Creates hero sections, feat… |
| `product-team/skills/product-analytics` | Use when defining product KPIs, building metric dashboards, running cohort or retention analysis, or interpreting feature adoption… |
| `product-team/skills/product-discovery` | Use when validating product opportunities, mapping assumptions, planning discovery sprints, or testing problem-solution fit before… |
| `product-team/skills/product-manager-toolkit` | Comprehensive toolkit for product managers including RICE prioritization, customer interview analysis, PRD templates, discovery fr… |
| `product-team/skills/product-skills` | "Use when coordinating product work across the 12 bundled product sub-skills (RICE, OKRs, UX research, design tokens, competitive … |
| `product-team/skills/product-strategist` | Strategic product leadership toolkit for Head of Product covering OKR cascade generation, quarterly planning, competitive landscap… |
| `product-team/skills/roadmap-communicator` | Use when preparing roadmap narratives, release notes, changelogs, or stakeholder updates tailored for executives, engineering team… |
| `product-team/skills/saas-scaffolder` | "Generates complete, production-ready SaaS project boilerplate including authentication, database schemas, billing integration, AP… |
| `product-team/skills/spec-to-repo` | "Use when the user says 'build me an app', 'create a project from this spec', 'scaffold a new repo', 'generate a starter', 'turn t… |
| `product-team/skills/ui-design-system` | UI design system toolkit for Senior UI Designer including design token generation, component documentation, responsive design calc… |
| `product-team/skills/ux-researcher-designer` | UX research and design toolkit for Senior UX Designer/Researcher including data-driven persona generation, journey mapping, usabil… |
| `productivity/andreessen/skills/andreessen` | "Marc Andreessen-mode decision and productivity skill. A blunt, market-first operator that pressure-tests ideas, ventures, feature… |
| `productivity/capture/skills/capture` | "Captures and organizes chaotic brain dumps into a structured, actionable system with zero information loss. Use this skill whenev… |
| `productivity/deep-work/skills/deep-work` | Use when someone wants to plan a deep work day, time-block their calendar or task list, budget or cut shallow work, protect focus … |
| `productivity/email/skills/inbox-setup` | "One-time setup skill that builds a personalized inbox triage knowledge base via interactive interview. Interviews the user about … |
| `productivity/email/skills/inbox-triage` | "Runs a full inbox triage using the knowledge base created by the 'inbox-setup' skill. Light-intake by design (most invocations sk… |
| `productivity/fable-goal/skills/fable-goal` | Convert a rambling description of a desired outcome into one polished, autonomous /goal prompt ready to paste into a fresh session… |
| `productivity/handoff/skills/handoff` | "Compact the current conversation into a handoff document for another agent to pick up. Save to a user-configured location (OS tem… |
| `productivity/meetings/skills/meetings` | Use when someone wants to decide whether a meeting is worth calling, price a meeting in dollars, build a timeboxed agenda with des… |
| `productivity/reflect/skills/reflect` | "Mid-conversation reflection skill that pauses execution and zooms out from detail-mode to honestly reassess direction, assumption… |
| `productivity/roast/skills/roast` | Use when someone asks to roast an idea, pressure-test or stress-test an idea, validate a business idea, "convene the panel", get a… |
| `productivity/swedish-mentor` | Mentor Swedish language learners by selecting YouTube video clips and podcast episodes by CEFR level and skill (listening, reading… |
| `productivity/weekly-review/skills/weekly-review` | Use when someone wants to run a weekly review, close open loops, audit stalled projects and commitments, get their system back to … |
| `project-management/skills/atlassian-admin` | Atlassian Administrator for managing and organizing Atlassian products (Jira, Confluence, Bitbucket, Trello), users, permissions, … |
| `project-management/skills/atlassian-templates` | Atlassian Template and Files Creator/Modifier expert for creating, modifying, and managing Jira and Confluence templates, blueprin… |
| `project-management/skills/confluence-expert` | Atlassian Confluence expert for creating and managing spaces, knowledge bases, and documentation. Configures space permissions and… |
| `project-management/skills/jira-expert` | Atlassian Jira expert for creating and managing projects, planning, product discovery, JQL queries, workflows, custom fields, auto… |
| `project-management/skills/meeting-analyzer` | Analyzes meeting transcripts and recordings to surface behavioral patterns, communication anti-patterns, and actionable coaching f… |
| `project-management/skills/pm-skills` | "Use when coordinating project-delivery work across the 8 project-management sub-skills — sprint/velocity analytics, portfolio hea… |
| `project-management/skills/scrum-master` | "Advanced Scrum Master skill for data-driven agile team analysis and coaching. Use when the user asks about sprint planning, veloc… |
| `project-management/skills/senior-pm` | Senior Project Manager for enterprise software, SaaS, and digital transformation projects. Specializes in portfolio management, qu… |
| `project-management/skills/team-communications` | Write internal company communications — 3P updates (Progress/Plans/Problems), company-wide newsletters, FAQ roundups, incident rep… |
| `ra-qm-team/compliance-team-eu-ai-act/skills/eu-ai-act-specialist` | "EU AI Act (Regulation (EU) 2024/1689) operational compliance for compliance teams. Three Article-level decisions: (1) What's the … |
| `ra-qm-team/compliance-team-iso42001/skills/iso42001-specialist` | "ISO/IEC 42001:2023 AI Management System (AIMS) specialist for compliance teams running internal audits. Three decisions: (1) Wher… |
| `ra-qm-team/skills/agent-decision-receipts` | "Mint a tamper-evident, post-quantum-signed receipt for a consequential agent action (deploy, delete, pay, grant-access, model dec… |
| `ra-qm-team/skills/capa-officer` | CAPA system management for medical device QMS. Covers root cause analysis, corrective action planning, effectiveness verification,… |
| `ra-qm-team/skills/eu-ai-act-specialist` | "EU AI Act (Regulation (EU) 2024/1689) operational compliance for compliance teams. Three Article-level decisions: (1) What's the … |
| `ra-qm-team/skills/fda-consultant-specialist` | FDA regulatory consultant for medical device companies. Provides 510(k)/PMA/De Novo pathway guidance, QMSR (21 CFR 820, which inco… |
| `ra-qm-team/skills/gdpr-dsgvo-expert` | GDPR and German DSGVO compliance automation. Scans codebases for privacy risks, generates DPIA documentation, tracks data subject … |
| `ra-qm-team/skills/information-security-manager-iso27001` | ISO 27001 ISMS implementation and cybersecurity governance for HealthTech and MedTech companies. Use when designing an ISMS, runni… |
| `ra-qm-team/skills/isms-audit-expert` | Information Security Management System (ISMS) audit expert for ISO 27001 compliance verification, security control assessment, and… |
| `ra-qm-team/skills/iso42001-specialist` | "ISO/IEC 42001:2023 AI Management System (AIMS) specialist for compliance teams running internal audits. Three decisions: (1) Wher… |
| `ra-qm-team/skills/mdr-745-specialist` | EU MDR 2017/745 compliance specialist for medical device classification, technical documentation, clinical evidence, and post-mark… |
| `ra-qm-team/skills/qms-audit-expert` | ISO 13485 internal audit expertise for medical device QMS. Covers audit planning, execution, nonconformity classification, and CAP… |
| `ra-qm-team/skills/quality-documentation-manager` | Document control system management for medical device QMS. Covers document numbering, version control, change management, and 21 C… |
| `ra-qm-team/skills/quality-manager-qmr` | Senior Quality Manager Responsible Person (QMR) for HealthTech and MedTech companies. Provides quality system governance, manageme… |
| `ra-qm-team/skills/quality-manager-qms-iso13485` | ISO 13485 Quality Management System implementation and maintenance for medical device organizations. Provides QMS design, document… |
| `ra-qm-team/skills/ra-qm-skills` | "Router/index for the 15 regulatory & quality-management skills bundled in this plugin (ISO 13485 QMS, EU MDR 2017/745, FDA submis… |
| `ra-qm-team/skills/regulatory-affairs-head` | Senior Regulatory Affairs Manager for HealthTech and MedTech companies. Prepares FDA 510(k), De Novo, and PMA submission packages;… |
| `ra-qm-team/skills/risk-management-specialist` | Medical device risk management specialist implementing ISO 14971 throughout product lifecycle. Provides risk analysis, risk evalua… |
| `ra-qm-team/skills/soc2-compliance` | "Use when the user asks to prepare for SOC 2 audits, map Trust Service Criteria, build control matrices, collect audit evidence, p… |
| `research-ops/skills/clinical-research` | Use when designing a prospective clinical study before submission — selecting and classifying endpoints (primary / key-secondary /… |
| `research-ops/skills/market-research` | Use when doing upstream market-research methodology — sizing a market as TAM/SAM/SOM computed BOTH top-down and bottoms-up (never … |
| `research-ops/skills/product-research` | Use when planning and synthesizing product/user research as a method-and-repository discipline — selecting the right method for th… |
| `research-ops/skills/research-finance` | Use when managing the money for an internal R&D program or portfolio — building a multi-period program budget with the F&A (indire… |
| `research-ops/skills/research-ops-skills` | Use when planning, funding, scoping, or synthesizing enterprise research across workstreams — clinical study design, R&D program f… |
| `research/deep-research/skills/deep-research` | "Run a disciplined, multi-source research investigation for a high-stakes question or decision — fan-out web search across many ch… |
| `research/deepread` | "Use when the user asks to deeply read a book, article, PDF, or document set; extract claims and evidence; build a knowledge map; … |
| `research/dossier/skills/dossier` | "Decision-grade entity research skill — produces a hypothesis-tested dossier on a specific company, person, nonprofit, or governme… |
| `research/grants/skills/grants` | "NIH grant research skill for clinical researchers. Grill-me intake (research idea + career stage + preliminary data + environment… |
| `research/litreview/skills/litreview` | "Academic literature orientation skill that searches papers via free keyless APIs (PubMed E-utilities + OpenAlex) by default — wit… |
| `research/notebooklm/skills/notebooklm` | "Browser automation skill for controlling Google's NotebookLM. Use when the user wants anything done in NotebookLM (e.g., 'open No… |
| `research/patent/skills/patent` | "Patent prior-art and landscape intelligence skill — not generic patent help. Commits to one of five sub-use-cases via forcing int… |
| `research/pulse/skills/pulse` | "Multi-source recency research skill that takes the pulse of any topic across Reddit, Hacker News, the open web, and optionally X/… |
| `research/research/skills/research` | Default entry point for any research request — a hybrid router that classifies the question deterministically and either delegates… |
| `research/syllabus/skills/syllabus` | "Generates a curated supplementary reading list from any course syllabus using Consensus academic search. Grill-me intake (syllabu… |

---

## security（170）

| 技能 | 用途 |
|------|------|
| `agentic-actions-auditor/skills/agentic-actions-auditor` | "Audits GitHub Actions workflows for security vulnerabilities in AI agent integrations including Claude Code Action, Gemini CLI, O… |
| `audit-context-building/skills/audit-context-building` | Understand a codebase before looking for bugs in it - what each function assumes, what it guarantees, and what it depends on elsew… |
| `building-secure-contracts/skills/algorand-vulnerability-scanner` | Scans Algorand smart contracts for 11 common vulnerabilities including rekeying attacks, unchecked transaction fees, missing field… |
| `building-secure-contracts/skills/audit-prep-assistant` | Prepares codebases for security review using Trail of Bits' checklist. Helps set review goals, runs static analysis tools, increas… |
| `building-secure-contracts/skills/cairo-vulnerability-scanner` | Scans Cairo/StarkNet smart contracts for 6 critical vulnerabilities including felt252 arithmetic overflow, L1-L2 messaging issues,… |
| `building-secure-contracts/skills/code-maturity-assessor` | Systematic code maturity assessment using Trail of Bits' 9-category framework. Analyzes codebase for arithmetic safety, auditing p… |
| `building-secure-contracts/skills/cosmos-vulnerability-scanner` | "Scans Cosmos SDK blockchain modules and CosmWasm contracts for consensus-critical vulnerabilities — chain halts, fund loss, state… |
| `building-secure-contracts/skills/guidelines-advisor` | Smart contract development advisor based on Trail of Bits' best practices. Analyzes codebase to generate documentation/specificati… |
| `building-secure-contracts/skills/secure-workflow-guide` | Guides through Trail of Bits' 5-step secure development workflow. Runs Slither scans, checks special features (upgradeability/ERC … |
| `building-secure-contracts/skills/solana-vulnerability-scanner` | Scans Solana programs for 6 critical vulnerabilities including arbitrary CPI, improper PDA validation, missing signer/ownership ch… |
| `building-secure-contracts/skills/substrate-vulnerability-scanner` | Scans Substrate/Polkadot pallets for 7 critical vulnerabilities including arithmetic overflow, panic DoS, incorrect weights, and b… |
| `building-secure-contracts/skills/token-integration-analyzer` | Token integration and implementation analyzer based on Trail of Bits' token integration checklist. Analyzes token implementations … |
| `building-secure-contracts/skills/ton-vulnerability-scanner` | Scans TON (The Open Network) smart contracts for 3 critical vulnerabilities including integer-as-boolean misuse, fake Jetton contr… |
| `burpsuite-project-parser/skills/burpsuite-project-parser` | Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with r… |
| `c-review/skills/c-review` | Performs comprehensive C/C++ security review for memory corruption, integer overflows, race conditions, and platform-specific vuln… |
| `claude-in-chrome-troubleshooting/skills/chrome-mcp-troubleshooting` | Diagnose and fix Claude in Chrome MCP extension connectivity issues. Use when mcp__claude-in-chrome__* tools fail, return "Browser… |
| `code-improver/skills/code-improver` | "Runs an autonomous review-and-fix improvement loop over any code target — a skill, plugin, module, or directory — using a reviewe… |
| `code-improver/skills/pr-improver` | "Runs an autonomous review-and-fix improvement loop over the current branch's changes until a PR review comes back clean, scoped m… |
| `code-improver/skills/skill-improver` | "Runs an autonomous review-and-fix improvement loop over a Claude Code skill until a review comes back clean, with a cross-round f… |
| `code-improver/tests/fixtures/pr-review-toolkit/skills/review-pr` | "Reviews the current branch's changes against its base branch as a pull request: correctness of new and modified code, test covera… |
| `code-improver/tests/fixtures/review-panel/skills/panel-review` | "Reviews a code target by launching a panel of specialist auditor agents and merging their reports. Use when asked to run a panel … |
| `constant-time-analysis/skills/constant-time-analysis` | Detects timing side-channel vulnerabilities in cryptographic code. Use when implementing or reviewing crypto code, encountering di… |
| `culture-index/skills/interpreting-culture-index` | Interprets Culture Index (CI) surveys, behavioral profiles, and personality assessment data. Supports individual profile interpret… |
| `devcontainer-setup/skills/devcontainer-setup` | Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. Use when adding d… |
| `differential-review/skills/differential-review` | "Performs security-focused differential review of code changes. Adapts analysis depth to codebase size, uses git blame for context… |
| `dimensional-analysis/skills/dimensional-analysis` | "Annotates codebases with dimensional analysis comments documenting units, dimensions, and decimal scaling. Use when someone asks … |
| `dwarf-expert/skills/dwarf-expert` | Analyzes DWARF debug information in compiled binaries. Use when inspecting .debug_* sections, DIE trees, or DW_TAG_/DW_AT_ entries… |
| `entry-point-analyzer/skills/entry-point-analyzer` | Analyzes smart contract codebases to identify state-changing entry points for security auditing. Detects externally callable funct… |
| `firebase-apk-scanner/skills/firebase-apk-scanner` | Scans Android APKs for Firebase security misconfigurations including open databases, storage buckets, authentication issues, and e… |
| `fp-check/skills/fp-check` | "Systematically verifies suspected security bugs to eliminate false positives, producing a TRUE POSITIVE or FALSE POSITIVE verdict… |
| `gh-cli/skills/gh-cli` | Enforces authenticated gh CLI workflows over unauthenticated curl, WebFetch, and MCP fetch patterns. Use when working with GitHub … |
| `github-triage/skills/github-triage` | "Triages a repository's open GitHub issues and pull requests via the gh CLI. Optionally reviews and merges ready PRs — incremental… |
| `goal-prompt/skills/goal-prompt` | "Drafts copy-paste-ready /goal commands for goal mode in Claude Code and Codex. Use when the user asks to create, write, rewrite, … |
| `let-fate-decide/skills/let-fate-decide` | "Draws the 12 Houses of the Zodiac Tarot spread to inject entropy into planning when prompts are vague, ambiguous, or casually del… |
| `modern-cpp/skills/modern-cpp` | Guides C++ code toward modern idioms (C++20/23/26). Use when writing new C++ code, modernizing legacy patterns, or working on secu… |
| `modern-python/skills/modern-python` | Configures Python projects with modern tooling (uv, ruff, ty). Use when creating projects, writing standalone scripts, or migratin… |
| `mutation-testing/skills/mutation-testing` | "Configures mewt or muton campaigns, analyzes surviving mutants, and investigates bugs exposed by testing gaps. Use when setting u… |
| `open-sourcing/skills/open-sourcing` | This skill should be used when the user asks to "open source this project", "prepare this repository for public release", "make th… |
| `plugins/agentic-actions-auditor/skills/agentic-actions-auditor` | "Audits GitHub Actions workflows for security vulnerabilities in AI agent integrations including Claude Code Action, Gemini CLI, O… |
| `plugins/audit-context-building/skills/audit-context-building` | Understand a codebase before looking for bugs in it - what each function assumes, what it guarantees, and what it depends on elsew… |
| `plugins/building-secure-contracts/skills/algorand-vulnerability-scanner` | Scans Algorand smart contracts for 11 common vulnerabilities including rekeying attacks, unchecked transaction fees, missing field… |
| `plugins/building-secure-contracts/skills/audit-prep-assistant` | Prepares codebases for security review using Trail of Bits' checklist. Helps set review goals, runs static analysis tools, increas… |
| `plugins/building-secure-contracts/skills/cairo-vulnerability-scanner` | Scans Cairo/StarkNet smart contracts for 6 critical vulnerabilities including felt252 arithmetic overflow, L1-L2 messaging issues,… |
| `plugins/building-secure-contracts/skills/code-maturity-assessor` | Systematic code maturity assessment using Trail of Bits' 9-category framework. Analyzes codebase for arithmetic safety, auditing p… |
| `plugins/building-secure-contracts/skills/cosmos-vulnerability-scanner` | "Scans Cosmos SDK blockchain modules and CosmWasm contracts for consensus-critical vulnerabilities — chain halts, fund loss, state… |
| `plugins/building-secure-contracts/skills/guidelines-advisor` | Smart contract development advisor based on Trail of Bits' best practices. Analyzes codebase to generate documentation/specificati… |
| `plugins/building-secure-contracts/skills/secure-workflow-guide` | Guides through Trail of Bits' 5-step secure development workflow. Runs Slither scans, checks special features (upgradeability/ERC … |
| `plugins/building-secure-contracts/skills/solana-vulnerability-scanner` | Scans Solana programs for 6 critical vulnerabilities including arbitrary CPI, improper PDA validation, missing signer/ownership ch… |
| `plugins/building-secure-contracts/skills/substrate-vulnerability-scanner` | Scans Substrate/Polkadot pallets for 7 critical vulnerabilities including arithmetic overflow, panic DoS, incorrect weights, and b… |
| `plugins/building-secure-contracts/skills/token-integration-analyzer` | Token integration and implementation analyzer based on Trail of Bits' token integration checklist. Analyzes token implementations … |
| `plugins/building-secure-contracts/skills/ton-vulnerability-scanner` | Scans TON (The Open Network) smart contracts for 3 critical vulnerabilities including integer-as-boolean misuse, fake Jetton contr… |
| `plugins/burpsuite-project-parser/skills/burpsuite-project-parser` | Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with r… |
| `plugins/c-review/skills/c-review` | Performs comprehensive C/C++ security review for memory corruption, integer overflows, race conditions, and platform-specific vuln… |
| `plugins/claude-in-chrome-troubleshooting/skills/chrome-mcp-troubleshooting` | Diagnose and fix Claude in Chrome MCP extension connectivity issues. Use when mcp__claude-in-chrome__* tools fail, return "Browser… |
| `plugins/code-improver/skills/code-improver` | "Runs an autonomous review-and-fix improvement loop over any code target — a skill, plugin, module, or directory — using a reviewe… |
| `plugins/code-improver/skills/pr-improver` | "Runs an autonomous review-and-fix improvement loop over the current branch's changes until a PR review comes back clean, scoped m… |
| `plugins/code-improver/skills/skill-improver` | "Runs an autonomous review-and-fix improvement loop over a Claude Code skill until a review comes back clean, with a cross-round f… |
| `plugins/code-improver/tests/fixtures/pr-review-toolkit/skills/review-pr` | "Reviews the current branch's changes against its base branch as a pull request: correctness of new and modified code, test covera… |
| `plugins/code-improver/tests/fixtures/review-panel/skills/panel-review` | "Reviews a code target by launching a panel of specialist auditor agents and merging their reports. Use when asked to run a panel … |
| `plugins/constant-time-analysis/skills/constant-time-analysis` | Detects timing side-channel vulnerabilities in cryptographic code. Use when implementing or reviewing crypto code, encountering di… |
| `plugins/culture-index/skills/interpreting-culture-index` | Interprets Culture Index (CI) surveys, behavioral profiles, and personality assessment data. Supports individual profile interpret… |
| `plugins/devcontainer-setup/skills/devcontainer-setup` | Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. Use when adding d… |
| `plugins/differential-review/skills/differential-review` | "Performs security-focused differential review of code changes. Adapts analysis depth to codebase size, uses git blame for context… |
| `plugins/dimensional-analysis/skills/dimensional-analysis` | "Annotates codebases with dimensional analysis comments documenting units, dimensions, and decimal scaling. Use when someone asks … |
| `plugins/dwarf-expert/skills/dwarf-expert` | Analyzes DWARF debug information in compiled binaries. Use when inspecting .debug_* sections, DIE trees, or DW_TAG_/DW_AT_ entries… |
| `plugins/entry-point-analyzer/skills/entry-point-analyzer` | Analyzes smart contract codebases to identify state-changing entry points for security auditing. Detects externally callable funct… |
| `plugins/firebase-apk-scanner/skills/firebase-apk-scanner` | Scans Android APKs for Firebase security misconfigurations including open databases, storage buckets, authentication issues, and e… |
| `plugins/fp-check/skills/fp-check` | "Systematically verifies suspected security bugs to eliminate false positives, producing a TRUE POSITIVE or FALSE POSITIVE verdict… |
| `plugins/gh-cli/skills/gh-cli` | Enforces authenticated gh CLI workflows over unauthenticated curl, WebFetch, and MCP fetch patterns. Use when working with GitHub … |
| `plugins/github-triage/skills/github-triage` | "Triages a repository's open GitHub issues and pull requests via the gh CLI. Optionally reviews and merges ready PRs — incremental… |
| `plugins/goal-prompt/skills/goal-prompt` | "Drafts copy-paste-ready /goal commands for goal mode in Claude Code and Codex. Use when the user asks to create, write, rewrite, … |
| `plugins/let-fate-decide/skills/let-fate-decide` | "Draws the 12 Houses of the Zodiac Tarot spread to inject entropy into planning when prompts are vague, ambiguous, or casually del… |
| `plugins/modern-cpp/skills/modern-cpp` | Guides C++ code toward modern idioms (C++20/23/26). Use when writing new C++ code, modernizing legacy patterns, or working on secu… |
| `plugins/modern-python/skills/modern-python` | Configures Python projects with modern tooling (uv, ruff, ty). Use when creating projects, writing standalone scripts, or migratin… |
| `plugins/mutation-testing/skills/mutation-testing` | "Configures mewt or muton campaigns, analyzes surviving mutants, and investigates bugs exposed by testing gaps. Use when setting u… |
| `plugins/open-sourcing/skills/open-sourcing` | This skill should be used when the user asks to "open source this project", "prepare this repository for public release", "make th… |
| `plugins/post-patch-validation/skills/post-patch-validation` | > |
| `plugins/property-based-testing/skills/property-based-testing` | "Writes, reviews, and debugs property-based tests — Hypothesis, fast-check, proptest, jqwik, rapid, and Echidna or Medusa for Soli… |
| `plugins/review-walkthrough/skills/review-walkthrough` | Generates an interactive HTML walkthrough for reviewing code changes. Use only when explicitly called. |
| `plugins/rust-review/skills/rust-review` | Performs comprehensive Rust security review for safe/unsafe boundary issues, memory safety in unsafe blocks, concurrency hazards, … |
| `plugins/second-opinion/skills/second-opinion` | "Gets independent code reviews from Codex or Antigravity for uncommitted changes, branch diffs, and commits. Use when the user req… |
| `plugins/semgrep-rule-creator/skills/semgrep-rule-creator` | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rul… |
| `plugins/semgrep-rule-variant-creator/skills/semgrep-rule-variant-creator` | Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an exist… |
| `plugins/sharp-edges/skills/sharp-edges` | "Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes. Use when reviewing API … |
| `plugins/spec-to-code-compliance/skills/spec-to-code-compliance` | Check code against the documentation that specifies it - which requirements hold, which the code contradicts, which are absent, an… |
| `plugins/static-analysis/skills/codeql` | >- |
| `plugins/static-analysis/skills/sarif-parsing` | >- |
| `plugins/static-analysis/skills/semgrep` | >- |
| `plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor` | "Audits a project's dependencies for supply-chain risk: version-matched advisories for direct dependencies and the full lockfile t… |
| `plugins/testing-handbook-skills/skills/address-sanitizer` | "Builds and runs code under AddressSanitizer to catch buffer overflows, use-after-free, and other memory errors during fuzzing or … |
| `plugins/testing-handbook-skills/skills/aflpp` | "Sets up and runs AFL++ for multi-core fuzzing of C/C++ projects built with afl-clang-fast or afl-gcc-fast. Covers instrumentation… |
| `plugins/testing-handbook-skills/skills/atheris` | "Sets up and runs Atheris, the coverage-guided Python fuzzer built on libFuzzer. Covers TestOneInput harnesses, FuzzedDataProvider… |
| `plugins/testing-handbook-skills/skills/cargo-fuzz` | "Sets up and runs cargo-fuzz, the standard fuzzing tool for Cargo-based Rust projects. Covers cargo fuzz init, the nightly toolcha… |
| `plugins/testing-handbook-skills/skills/constant-time-testing` | "Measures timing side channels in cryptographic implementations by running them, using dudect for statistical analysis and Timecop… |
| `plugins/testing-handbook-skills/skills/coverage-analysis` | "Measures and interprets what a fuzzing campaign actually reaches, using llvm-cov, lcov, or a fuzzer's own coverage output. Covers… |
| `plugins/testing-handbook-skills/skills/fuzzing-dictionary` | "Builds and applies fuzzing dictionaries so a fuzzer can produce the keywords, magic bytes, and tokens a target expects. Covers ex… |
| `plugins/testing-handbook-skills/skills/fuzzing-obstacles` | "Patches past the barriers that stop a fuzzer making progress — checksum and hash verification, magic-value validation, time-based… |
| `plugins/testing-handbook-skills/skills/harness-writing` | "Designs and improves fuzzing harnesses for C/C++ and Rust. Covers mapping raw bytes onto a target API, generating structured inpu… |
| `plugins/testing-handbook-skills/skills/libafl` | "Builds custom fuzzers with LibAFL, the modular Rust fuzzing library. Covers composing observers, feedbacks, mutators, schedulers,… |
| `plugins/testing-handbook-skills/skills/libfuzzer` | "Sets up and runs libFuzzer, the coverage-guided fuzzer built into LLVM, on C/C++ code that compiles with Clang. Covers harness st… |
| `plugins/testing-handbook-skills/skills/ossfuzz` | "Enrolls a project in OSS-Fuzz, Google's free continuous fuzzing service for open source, and drives it locally. Covers project.ya… |
| `plugins/testing-handbook-skills/skills/ruzzy` | "Sets up and runs Ruzzy, Trail of Bits' coverage-guided Ruby fuzzer and the only production-ready one for the language. Covers har… |
| `plugins/testing-handbook-skills/skills/testing-handbook-generator` | "Generates Claude Code skills from the Trail of Bits Testing Handbook (appsec.guide), analyzing handbook pages and emitting SKILL.… |
| `plugins/testing-handbook-skills/skills/wycheproof` | "Validates cryptographic implementations against Project Wycheproof's test vectors, which encode known attacks and edge cases acro… |
| `plugins/trailmark/skills/audit-augmentation` | > |
| `plugins/trailmark/skills/crypto-protocol-diagram` | "Extracts protocol message flow from source code, RFCs, academic papers, pseudocode, informal prose, ProVerif (.pv), or Tamarin (.… |
| `plugins/trailmark/skills/diagramming-code` | > |
| `plugins/trailmark/skills/genotoxic` | "Graph-informed mutation testing triage. Parses codebases with Trailmark, runs mutation testing and necessist, then uses survived … |
| `plugins/trailmark/skills/graph-evolution` | > |
| `plugins/trailmark/skills/mermaid-to-proverif` | "Translates Mermaid sequenceDiagrams describing cryptographic protocols into ProVerif formal verification models (.pv files). Use … |
| `plugins/trailmark/skills/slicing-code-context` | "Selects bounded, graph-informed source slices with Trailmark and delegates focused code analysis or patch-proposal work to a smal… |
| `plugins/trailmark/skills/trailmark` | "Builds and queries multi-language source and binary code graphs for security analysis. Includes pre-analysis passes for blast rad… |
| `plugins/trailmark/skills/trailmark-finding-triage` | "Performs graph-assisted triage of a single security finding, SARIF result, weAudit annotation, suspicious function, or report exc… |
| `plugins/trailmark/skills/trailmark-review-gate` | "Runs a Trailmark structural review gate over a branch, pull request, fix commit, release diff, or git ref range to detect new ent… |
| `plugins/trailmark/skills/trailmark-structural` | "Runs full Trailmark structural analysis by building a graph, running `preanalysis()`, and reporting hotspots, taint, blast radius… |
| `plugins/trailmark/skills/trailmark-summary` | "Runs a Trailmark summary analysis on a codebase. Returns auto-detected languages, entry point count, and dependency list. Use whe… |
| `plugins/trailmark/skills/trailmark-variant-neighborhood` | "Expands one confirmed or suspected vulnerability into a Trailmark graph neighborhood of variant candidates by finding sibling fun… |
| `plugins/trailmark/skills/vector-forge` | "Mutation-driven test vector generation. Finds implementations of a cryptographic algorithm or protocol, runs mutation testing to … |
| `plugins/variant-analysis/skills/variant-analysis` | Hunts for the other instances of a bug already found — the variants of one root cause across a codebase. Use immediately after a v… |
| `plugins/vulnerability-triage-brocards/skills/vulnerability-triage-brocards` | >- |
| `plugins/writing-lean-proofs/skills/writing-lean-proofs` | "Writes and reviews structured Lean 4 proofs and designs Lean libraries following Mathlib conventions. Use when proving theorems i… |
| `plugins/yara-authoring/skills/yara-rule-authoring` | > |
| `plugins/zeroize-audit/skills/zeroize-audit` | "Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with a… |
| `post-patch-validation/skills/post-patch-validation` | > |
| `property-based-testing/skills/property-based-testing` | "Writes, reviews, and debugs property-based tests — Hypothesis, fast-check, proptest, jqwik, rapid, and Echidna or Medusa for Soli… |
| `review-walkthrough/skills/review-walkthrough` | Generates an interactive HTML walkthrough for reviewing code changes. Use only when explicitly called. |
| `rust-review/skills/rust-review` | Performs comprehensive Rust security review for safe/unsafe boundary issues, memory safety in unsafe blocks, concurrency hazards, … |
| `second-opinion/skills/second-opinion` | "Gets independent code reviews from Codex or Antigravity for uncommitted changes, branch diffs, and commits. Use when the user req… |
| `semgrep-rule-creator/skills/semgrep-rule-creator` | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rul… |
| `semgrep-rule-variant-creator/skills/semgrep-rule-variant-creator` | Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an exist… |
| `sharp-edges/skills/sharp-edges` | "Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes. Use when reviewing API … |
| `spec-to-code-compliance/skills/spec-to-code-compliance` | Check code against the documentation that specifies it - which requirements hold, which the code contradicts, which are absent, an… |
| `static-analysis/skills/codeql` | >- |
| `static-analysis/skills/sarif-parsing` | >- |
| `static-analysis/skills/semgrep` | >- |
| `supply-chain-risk-auditor/skills/supply-chain-risk-auditor` | "Audits a project's dependencies for supply-chain risk: version-matched advisories for direct dependencies and the full lockfile t… |
| `testing-handbook-skills/skills/address-sanitizer` | "Builds and runs code under AddressSanitizer to catch buffer overflows, use-after-free, and other memory errors during fuzzing or … |
| `testing-handbook-skills/skills/aflpp` | "Sets up and runs AFL++ for multi-core fuzzing of C/C++ projects built with afl-clang-fast or afl-gcc-fast. Covers instrumentation… |
| `testing-handbook-skills/skills/atheris` | "Sets up and runs Atheris, the coverage-guided Python fuzzer built on libFuzzer. Covers TestOneInput harnesses, FuzzedDataProvider… |
| `testing-handbook-skills/skills/cargo-fuzz` | "Sets up and runs cargo-fuzz, the standard fuzzing tool for Cargo-based Rust projects. Covers cargo fuzz init, the nightly toolcha… |
| `testing-handbook-skills/skills/constant-time-testing` | "Measures timing side channels in cryptographic implementations by running them, using dudect for statistical analysis and Timecop… |
| `testing-handbook-skills/skills/coverage-analysis` | "Measures and interprets what a fuzzing campaign actually reaches, using llvm-cov, lcov, or a fuzzer's own coverage output. Covers… |
| `testing-handbook-skills/skills/fuzzing-dictionary` | "Builds and applies fuzzing dictionaries so a fuzzer can produce the keywords, magic bytes, and tokens a target expects. Covers ex… |
| `testing-handbook-skills/skills/fuzzing-obstacles` | "Patches past the barriers that stop a fuzzer making progress — checksum and hash verification, magic-value validation, time-based… |
| `testing-handbook-skills/skills/harness-writing` | "Designs and improves fuzzing harnesses for C/C++ and Rust. Covers mapping raw bytes onto a target API, generating structured inpu… |
| `testing-handbook-skills/skills/libafl` | "Builds custom fuzzers with LibAFL, the modular Rust fuzzing library. Covers composing observers, feedbacks, mutators, schedulers,… |
| `testing-handbook-skills/skills/libfuzzer` | "Sets up and runs libFuzzer, the coverage-guided fuzzer built into LLVM, on C/C++ code that compiles with Clang. Covers harness st… |
| `testing-handbook-skills/skills/ossfuzz` | "Enrolls a project in OSS-Fuzz, Google's free continuous fuzzing service for open source, and drives it locally. Covers project.ya… |
| `testing-handbook-skills/skills/ruzzy` | "Sets up and runs Ruzzy, Trail of Bits' coverage-guided Ruby fuzzer and the only production-ready one for the language. Covers har… |
| `testing-handbook-skills/skills/testing-handbook-generator` | "Generates Claude Code skills from the Trail of Bits Testing Handbook (appsec.guide), analyzing handbook pages and emitting SKILL.… |
| `testing-handbook-skills/skills/wycheproof` | "Validates cryptographic implementations against Project Wycheproof's test vectors, which encode known attacks and edge cases acro… |
| `trailmark/skills/audit-augmentation` | > |
| `trailmark/skills/crypto-protocol-diagram` | "Extracts protocol message flow from source code, RFCs, academic papers, pseudocode, informal prose, ProVerif (.pv), or Tamarin (.… |
| `trailmark/skills/diagramming-code` | > |
| `trailmark/skills/genotoxic` | "Graph-informed mutation testing triage. Parses codebases with Trailmark, runs mutation testing and necessist, then uses survived … |
| `trailmark/skills/graph-evolution` | > |
| `trailmark/skills/mermaid-to-proverif` | "Translates Mermaid sequenceDiagrams describing cryptographic protocols into ProVerif formal verification models (.pv files). Use … |
| `trailmark/skills/slicing-code-context` | "Selects bounded, graph-informed source slices with Trailmark and delegates focused code analysis or patch-proposal work to a smal… |
| `trailmark/skills/trailmark` | "Builds and queries multi-language source and binary code graphs for security analysis. Includes pre-analysis passes for blast rad… |
| `trailmark/skills/trailmark-finding-triage` | "Performs graph-assisted triage of a single security finding, SARIF result, weAudit annotation, suspicious function, or report exc… |
| `trailmark/skills/trailmark-review-gate` | "Runs a Trailmark structural review gate over a branch, pull request, fix commit, release diff, or git ref range to detect new ent… |
| `trailmark/skills/trailmark-structural` | "Runs full Trailmark structural analysis by building a graph, running `preanalysis()`, and reporting hotspots, taint, blast radius… |
| `trailmark/skills/trailmark-summary` | "Runs a Trailmark summary analysis on a codebase. Returns auto-detected languages, entry point count, and dependency list. Use whe… |
| `trailmark/skills/trailmark-variant-neighborhood` | "Expands one confirmed or suspected vulnerability into a Trailmark graph neighborhood of variant candidates by finding sibling fun… |
| `trailmark/skills/vector-forge` | "Mutation-driven test vector generation. Finds implementations of a cryptographic algorithm or protocol, runs mutation testing to … |
| `variant-analysis/skills/variant-analysis` | Hunts for the other instances of a bug already found — the variants of one root cause across a codebase. Use immediately after a v… |
| `vulnerability-triage-brocards/skills/vulnerability-triage-brocards` | >- |
| `writing-lean-proofs/skills/writing-lean-proofs` | "Writes and reviews structured Lean 4 proofs and designs Lean libraries following Mathlib conventions. Use when proving theorems i… |
| `yara-authoring/skills/yara-rule-authoring` | > |
| `zeroize-audit/skills/zeroize-audit` | "Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with a… |

---

## software-development（147）

| 技能 | 用途 |
|------|------|
| `academy-guide` | > |
| `addyosmani/api-and-interface-design` | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating RES… |
| `addyosmani/browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need … |
| `addyosmani/ci-cd-and-automation` | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate qua… |
| `addyosmani/code-review-and-quality` | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a h… |
| `addyosmani/code-simplification` | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to… |
| `addyosmani/constraint-driven-development` | Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Interviews the user on which dimen… |
| `addyosmani/context-engineering` | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, … |
| `addyosmani/debugging-and-error-recovery` | Guides systematic root-cause debugging. Use when tests fail, builds break, something that worked yesterday broke, behavior doesn't… |
| `addyosmani/deprecation-and-migration` | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementat… |
| `addyosmani/documentation-and-adrs` | Records decisions and documentation. Use when you need to document an architecture decision (ADR) or the reasoning behind a design… |
| `addyosmani/doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when you want every assumption cro… |
| `addyosmani/frontend-ui-engineering` | Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating c… |
| `addyosmani/git-workflow-and-versioning` | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, splitting… |
| `addyosmani/idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still … |
| `addyosmani/incremental-implementation` | Delivers changes incrementally in thin, verifiable slices. Use when implementing any feature or change that touches more than one … |
| `addyosmani/interview-me` | Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time in… |
| `addyosmani/observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use wh… |
| `addyosmani/performance-optimization` | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when … |
| `addyosmani/planning-and-task-breakdown` | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Us… |
| `addyosmani/security-and-hardening` | Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentica… |
| `addyosmani/shipping-and-launch` | Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping… |
| `addyosmani/skills/api-and-interface-design` | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating RES… |
| `addyosmani/skills/browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need … |
| `addyosmani/skills/ci-cd-and-automation` | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate qua… |
| `addyosmani/skills/code-review-and-quality` | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a h… |
| `addyosmani/skills/code-simplification` | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to… |
| `addyosmani/skills/constraint-driven-development` | Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Interviews the user on which dimen… |
| `addyosmani/skills/context-engineering` | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, … |
| `addyosmani/skills/debugging-and-error-recovery` | Guides systematic root-cause debugging. Use when tests fail, builds break, something that worked yesterday broke, behavior doesn't… |
| `addyosmani/skills/deprecation-and-migration` | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementat… |
| `addyosmani/skills/documentation-and-adrs` | Records decisions and documentation. Use when you need to document an architecture decision (ADR) or the reasoning behind a design… |
| `addyosmani/skills/doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when you want every assumption cro… |
| `addyosmani/skills/frontend-ui-engineering` | Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating c… |
| `addyosmani/skills/git-workflow-and-versioning` | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, splitting… |
| `addyosmani/skills/idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still … |
| `addyosmani/skills/incremental-implementation` | Delivers changes incrementally in thin, verifiable slices. Use when implementing any feature or change that touches more than one … |
| `addyosmani/skills/interview-me` | Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time in… |
| `addyosmani/skills/observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use wh… |
| `addyosmani/skills/performance-optimization` | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when … |
| `addyosmani/skills/planning-and-task-breakdown` | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Us… |
| `addyosmani/skills/security-and-hardening` | Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentica… |
| `addyosmani/skills/shipping-and-launch` | Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping… |
| `addyosmani/skills/source-driven-development` | Grounds every implementation decision in official documentation. Use when you want to verify an approach against the official docs… |
| `addyosmani/skills/spec-driven-development` | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use … |
| `addyosmani/skills/test-driven-development` | Drives development with tests using the red-green-refactor loop. Use when implementing any logic, fixing any bug, or changing any … |
| `addyosmani/skills/using-agent-skills` | Discovers and invokes agent skills. Use when starting a session, or when you need to decide which skill or workflow applies to the… |
| `addyosmani/source-driven-development` | Grounds every implementation decision in official documentation. Use when you want to verify an approach against the official docs… |
| `addyosmani/spec-driven-development` | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use … |
| `addyosmani/test-driven-development` | Drives development with tests using the red-green-refactor loop. Use when implementing any logic, fixing any bug, or changing any … |
| `addyosmani/using-agent-skills` | Discovers and invokes agent skills. Use when starting a session, or when you need to decide which skill or workflow applies to the… |
| `algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request cre… |
| `anthropics/academy-guide` | > |
| `anthropics/algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request cre… |
| `anthropics/brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and… |
| `anthropics/canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to cr… |
| `anthropics/claude-api` | - |
| `anthropics/discernment-nudge` | > |
| `anthropics/doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, t… |
| `anthropics/docx` | "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx… |
| `anthropics/frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direct… |
| `anthropics/internal-comms` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude s… |
| `anthropics/mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through w… |
| `anthropics/pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, c… |
| `anthropics/pptx` | "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide d… |
| `anthropics/skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from s… |
| `anthropics/skills/academy-guide` | > |
| `anthropics/skills/algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request cre… |
| `anthropics/skills/brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and… |
| `anthropics/skills/canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to cr… |
| `anthropics/skills/claude-api` | - |
| `anthropics/skills/discernment-nudge` | > |
| `anthropics/skills/doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, t… |
| `anthropics/skills/docx` | "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx… |
| `anthropics/skills/frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direct… |
| `anthropics/skills/internal-comms` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude s… |
| `anthropics/skills/mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through w… |
| `anthropics/skills/pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, c… |
| `anthropics/skills/pptx` | "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide d… |
| `anthropics/skills/skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from s… |
| `anthropics/skills/slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation conc… |
| `anthropics/skills/theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10… |
| `anthropics/skills/web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tai… |
| `anthropics/skills/webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debug… |
| `anthropics/skills/xlsx` | "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, rea… |
| `anthropics/slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation conc… |
| `anthropics/template` | Replace with description of the skill and when Claude should use it. |
| `anthropics/theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10… |
| `anthropics/web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tai… |
| `anthropics/webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debug… |
| `anthropics/xlsx` | "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, rea… |
| `brainstorming` | "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior.… |
| `brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and… |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to cr… |
| `claude-api` | - |
| `codebase-inspection` | "Inspect codebases w/ pygount: LOC, languages, ratios." |
| `diagnosing-superpowers` | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor … |
| `discernment-nudge` | > |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, t… |
| `docx` | "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx… |
| `dogfood` | "Exploratory QA of web apps: find bugs, evidence, reports." |
| `executing-plans` | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline exe… |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skil… |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direct… |
| `github` | "GitHub via gh CLI: PRs, issues, reviews, repos, auth." |
| `graphify` | "Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ e… |
| `hermes-agent-skill-authoring` | "Author in-repo SKILL.md files: frontmatter and structure." |
| `hermes-self-evolution` | > |
| `inspecting-hermes-desktop-dom` | "Read the live Hermes desktop DOM/CSS over CDP." |
| `installing-external-skills` | "Install GitHub repos as Hermes skills." |
| `internal-comms` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude s… |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through w… |
| `node-inspect-debugger` | "Debug Node.js via --inspect + Chrome DevTools Protocol CLI." |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, c… |
| `ponytail` | > |
| `ponytail-audit` | > |
| `ponytail-debt` | > |
| `ponytail-gain` | > |
| `ponytail-help` | > |
| `ponytail-review` | > |
| `pptx` | "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide d… |
| `python-debugpy` | "Debug Python: pdb REPL + debugpy remote (DAP)." |
| `qiaomu-goal-meta-skill` | (无描述) |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically ques… |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `simplify-code` | "Parallel 4-agent cleanup of recent code changes." |
| `skill-builder` | Automatically detect source types and build AI skills using Skill Seekers. Use when the user wants to create skills from documenta… |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from s… |
| `skill-inspector` | Review AI agent skills before installation using NVIDIA SkillSpector and source-aware semantic review. Use when asked whether a sk… |
| `slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation conc… |
| `spike` | "Throwaway experiments to validate an idea before build." |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `template` | Replace with description of the skill and when Claude should use it. |
| `theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10… |
| `typesafe-ai/skills/typesafe-ai` | > |
| `typesafe-ai/typesafe-ai` | > |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an i… |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response includ… |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification com… |
| `web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tai… |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debug… |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |
| `xlsx` | "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, rea… |

---

## design（113）

| 技能 | 用途 |
|------|------|
| `21st-dev` | 21st.dev 在线 UI 目录操作技能：搜索 1.2 万+ 真实设计工程做的 React/Tailwind/shadcn 组件、模板、主题，取码进项目；或 AI 生成新 UI；或搜品牌 logo（JSX）。做落地页/组件需要"有品味的人写过的 UI"时优先… |
| `3dviz-pro-max` | Design and build expressive 3D scenes, explainers and interactive models with grounded subject knowledge. Use for 3D creation or e… |
| `8-bit-orbit-video-template` | (无描述) |
| `after-hours-editorial-template` | (无描述) |
| `algorithmic-art` | (无描述) |
| `animate` | Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at a… |
| `animate-expo` | Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it a… |
| `animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing … |
| `apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-dr… |
| `apple-hig` | (无描述) |
| `archify` | "Create polished, validated architecture, workflow, sequence, data-flow, and lifecycle/state diagrams as explorable standalone HTM… |
| `article-magazine` | "Huashu / huashu-md-html-inspired magazine article layout for turning Markdown or notes into a polished long-form HTML essay." |
| `ask-sonner` | Guide to Sonner, the React toast library — install and wire up the Toaster, pick the right toast() call, promise and loading toast… |
| `banner-design` | "Design banners for social media, ads, website heroes, creative assets, and print. Multiple art direction options with optional ge… |
| `brand` | Brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voi… |
| `brand-extract` | (无描述) |
| `brand-guidelines` | (无描述) |
| `brandkit` | Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks, and visual-w… |
| `break-ui` | Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge … |
| `brutalist-skill` | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contra… |
| `canvas-design` | (无描述) |
| `chat-motion-overlay` | Generate configurable chat motion overlays from a transcript or screenshot, including plain bubble scenes, app-style chat containe… |
| `color-expert` | (无描述) |
| `creative-director` | (无描述) |
| `deck-guizang-editorial` | "Editorial magazine meets e-ink: 10 layouts and 5 palettes (Ink, Indigo Porcelain, Forest Ink, Kraft Paper, Dune)." |
| `deck-open-slide-canvas` | "Locked 1920x1080 canvas deck with React component-level free composition, not bound to a fixed template." |
| `deck-swiss-international` | "16-column grid, one saturated accent, and 22 locked layouts (Klein Blue, Lemon, Mint, Safety Orange)." |
| `design` | "Comprehensive design skill: brand identity, design tokens, UI styling, logo generation (55 styles, Gemini, Atlas Cloud, or MuAPI … |
| `design-brief` | (无描述) |
| `design-system` | Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variabl… |
| `diagram-design` | Create branded architecture, architecture delta, IT current-state, flowchart, sequence, state machine, ER/data model, timeline, sw… |
| `diagram-design/diagram-design-main/skills/diagram-design` | Create branded architecture, architecture delta, IT current-state, flowchart, sequence, state machine, ER/data model, timeline, sw… |
| `digits-fintech-swiss-template` | (无描述) |
| `doc-kami-parchment` | "Warm parchment canvas (#f5f4ed), monochrome ink-blue accent (#1B365D), one serif family, and editorial-grade typography." |
| `ecommerce-image-workflow` | (无描述) |
| `editorial-burgundy-principles-template` | (无描述) |
| `emil-design-eng` | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that … |
| `emilkowalski-motion` | (无描述) |
| `enhance-prompt` | (无描述) |
| `export-download-debugging` | (无描述) |
| `field-notes-editorial-template` | (无描述) |
| `figma-code-connect-components` | (无描述) |
| `figma-create-design-system-rules` | (无描述) |
| `figma-create-new-file` | (无描述) |
| `figma-generate-design` | (无描述) |
| `figma-generate-library` | (无描述) |
| `figma-implement-design` | (无描述) |
| `figma-use` | (无描述) |
| `find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes mot… |
| `flutter-animating-apps` | (无描述) |
| `frame-data-chart-nyt` | "NYT-newsroom typography, staggered reveal animation, and editorial-grade charts (line, bar, or range band)." |
| `frame-flowchart-sticky` | "SVG curve connectors, sticky-note nodes, and cursor interaction with a whiteboard-brainstorm feel." |
| `frame-glitch-title` | "Digital glitch, chromatic offset, and data-corruption title frame for video transitions or cyberpunk heroes." |
| `frame-light-leak-cinema` | "Film light leaks, grain, 16:9 letterbox, and large serif type for cinematic openings or chapter cards." |
| `frame-liquid-bg-hero` | "WebGL-style fluid displacement background with a quote overlay, suited to video intros, landing heroes, or posters." |
| `frame-logo-outro` | "Segmented logo assembly, glow bloom, and tagline reveal for video outros or brand closing frames." |
| `frame-macos-notification` | "Realistic macOS notification banner with app icon, title, and body, suited to video overlays or product teasers." |
| `frontend-design` | (无描述) |
| `frontend-dev` | (无描述) |
| `frontend-skill` | (无描述) |
| `frontend-slides` | (无描述) |
| `gpt-tasteskill` | Elite UX/UI & Advanced GSAP Motion Engineer. Enforces Python-driven true randomization for layout variance, strict AIDA page struc… |
| `hand-drawn-diagrams` | (无描述) |
| `hatch-pet` | Create, repair, validate, preview, and package Codex-compatible animated pet spritesheets from character art, screenshots, generat… |
| `html-ppt-retro-quarterly-review` | (无描述) |
| `image-to-code-skill` | Elite website image-to-code skill for Codex. For visually important web tasks, it must first generate the design image(s) itself, … |
| `imagegen-frontend-mobile` | Elite mobile app image-generation skill for creating premium, app-native screen concepts and flows. Designed for iOS, Android, and… |
| `imagegen-frontend-web` | Elite frontend image-direction skill for generating premium, conversion-aware website design references. CRITICAL OUTPUT RULE — ge… |
| `img2threejs` | Turn an object or character reference image into a quality-gated, animation-ready procedural Three.js model built in code. Use for… |
| `impeccable-design-polish` | (无描述) |
| `improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained impl… |
| `library-curator` | (无描述) |
| `login-flow` | Mobile login and authentication flow screens |
| `magic-ui` | Use this skill when users want to add, customize, or troubleshoot Magic UI components in React/Next.js projects. It covers compone… |
| `minimalist-skill` | Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no… |
| `mobile-native` | Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something tha… |
| `od-next-media-inputs` | (无描述) |
| `output-skill` | Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit s… |
| `pick-ui-library` | Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, vi… |
| `platform-design` | (无描述) |
| `poster-hero` | "Vertical poster or Moments-style share image with strong visual impact." |
| `pptx-html-fidelity-audit` | Audit a python-pptx export against its source HTML deck, identify layout/content drift (footer overflow, cropped content, missing … |
| `pr-feedback-quality-gate` | (无描述) |
| `prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through th… |
| `react-bits` | 213 个动画 React 组件素材库（DavidHDev/react-bits，MIT+CC，48k star）。文字动画/背景/UI 组件/微交互，每个 4 变体（JS-CSS/JS-TW/TS-CSS/TS-TW）。做 React/Next.js 页面要… |
| `redesign-skill` | Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-en… |
| `reference-design-contract` | (无描述) |
| `review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to … |
| `shadcn-ui` | (无描述) |
| `shader-dev` | (无描述) |
| `shadergradient` | 3D 动态渐变/流体背景组件（ruucm/shadergradient，MIT，React + @react-three/fiber）。npm 装 @shadergradient/react，10 个内置 presets（halo/pensive/mint/i… |
| `slack-gif-creator` | (无描述) |
| `slides` | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide s… |
| `soft-skill` | Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that m… |
| `stitch-loop` | (无描述) |
| `stitch-skill` | Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI sta… |
| `swiftui-design` | (无描述) |
| `swiss-creative-mode-template` | (无描述) |
| `swiss-user-research-video-template` | (无描述) |
| `taste-skill` | Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design directio… |
| `taste-skill-v1` | The original v1 taste-skill, preserved for projects depending on its exact behavior. The current default is `design-taste-frontend… |
| `theme-factory` | (无描述) |
| `threejs` | (无描述) |
| `threeui-threejs-components` | 47 个现成 Three.js / WebGL shader 组件素材库（来自 MengTo/threeui，MIT）。落地页背景、3D 场景、shader 按钮/开关、CRT、粒子场、地球、织物、文字特效等。做 threejs 场景、WebGL 背景、创意 … |
| `ui-skills` | (无描述) |
| `ui-styling` | Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first … |
| `ui-ux-pro-max` | "UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing … |
| `uiverse-galaxy` | 3802 个零依赖 UI 组件素材库（uiverse-io/galaxy，UIVerse，MIT，13k star）。按钮/卡片/加载器/表单/开关等，每个 HTML 文件同时含 CSS 版和 Tailwind 版两段代码，copy-paste 即用。做 UI… |
| `vfx-text-cursor` | "Cursor light trail, chromatic rays, and directional flares for word-by-word quote reveals in video intros." |
| `weread-year-in-review-video-template` | (无描述) |
| `wpds` | (无描述) |
| `write-swift` | How to write modern Swift well — modeling with value types, Swift 6 data-race safety and approachable concurrency (@concurrent, ma… |
| `writing-guidelines` | (无描述) |

---

## browser-act（103）

| 技能 | 用途 |
|------|------|
| `browser-act` | "Browser automation CLI for AI agents. NEVER run browser-act commands directly via Bash — always invoke this skill first. Use brow… |
| `browser-act-skill-forge` | "Forges reusable Skill packages (SKILL.md + scripts) from website exploration via browser-act — no re-exploration later. Use when:… |
| `solutions/ecommerce/1688-product-detail` | "Extracts comprehensive wholesale product data from 1688.com product detail pages: title, tiered pricing, SKU variants with dimens… |
| `solutions/ecommerce/airbnb-listing-detail` | "Fetches complete Airbnb listing details for a given numeric listing ID via the internal GraphQL API, returning title, room type, … |
| `solutions/ecommerce/airbnb-search-listing` | "Extracts Airbnb accommodation search results from a destination query via SSR-embedded data, returning listing ID, URL, name, coo… |
| `solutions/ecommerce/amazon-alexa-qa` | "Amazon Alexa for Shopping Q&A automation: submits questions to Amazon's Alexa/Rufus AI shopping assistant and collects response t… |
| `solutions/ecommerce/amazon-asin-lookup-api-skill` | "This skill helps users extract structured product details from Amazon using a specific ASIN (Amazon Standard Identification Numbe… |
| `solutions/ecommerce/amazon-best-selling-products-finder-api-skill` | "This skill helps users extract structured best-selling product data from Amazon via the BrowserAct API. Agent should proactively … |
| `solutions/ecommerce/amazon-bestseller-listing` | "Amazon Best Sellers listing scraper: extract product cards from any Amazon Best Sellers (zgbs) or /gp/bestsellers/ category page … |
| `solutions/ecommerce/amazon-buy-box-monitor-api-skill` | "This skill helps users extract basic product details other sellers prices and seller ratings from Amazon via ASIN automatically u… |
| `solutions/ecommerce/amazon-competitor-analyzer` | Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis. Compares sp… |
| `solutions/ecommerce/amazon-listing-competitor-analysis-skill` | "This skill helps users analyze Amazon competitor listings by ASIN and produce structured competitive intelligence plus strategic … |
| `solutions/ecommerce/amazon-product-api-skill` | "This skill helps users extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specificati… |
| `solutions/ecommerce/amazon-product-detail` | "Amazon product detail page scraper: extract full product data from any open Amazon product detail URL (any /dp/{asin} or /gp/prod… |
| `solutions/ecommerce/amazon-product-search-api-skill` | "This skill is designed to help users automatically extract product data from Amazon search results. The Agent should proactively … |
| `solutions/ecommerce/amazon-reviews-api-skill` | "This skill helps users automatically extract Amazon product reviews via the Amazon Reviews API. Agent should proactively apply th… |
| `solutions/ecommerce/amazon-search-listing` | "Amazon search and category listing scraper: extract product listings from any Amazon search results page, keyword search URL, or … |
| `solutions/ecommerce/ebay-item-detail` | "Extracts full item detail from any open eBay item URL, returning JSON with url, itemNumber, title, subTitle, categories, price, p… |
| `solutions/ecommerce/ebay-search-listing` | "Extracts product listings from any eBay search or category page URL, returning per-item cards (itemNumber, url, title, subtitle, … |
| `solutions/ecommerce/ebay-sold-listings-search` | "eBay sold-listings scraper across 8 marketplaces (ebay.com/.co.uk/.de/.fr/.it/.es/.ca/.com.au). Takes keyword plus filters (categ… |
| `solutions/ecommerce/ecommerce-listing` | "Extract product list from any e-commerce category page, search results page, or keyword search with filters. Returns paginated pr… |
| `solutions/ecommerce/ecommerce-product-detail` | "Extract complete product information from any e-commerce product page. Returns name, price, currency, brand, images, description,… |
| `solutions/ecommerce/ecommerce-reviews` | "Extract customer reviews from any e-commerce product page or reviews page. Returns reviewer name, star rating, date, review title… |
| `solutions/ecommerce/ecommerce-seller-info` | "Extract seller or merchant profile data from marketplace platform seller pages. Returns seller name, rating, review count, positi… |
| `solutions/ecommerce/etsy-category-listing` | "Etsy category page scraper: given an Etsy category URL (e.g. https://www.etsy.com/c/jewelry) and optional page number, returns pa… |
| `solutions/ecommerce/etsy-keyword-search` | "Etsy keyword search scraper: given a search keyword and optional page number, returns paginated product listings with listingId, … |
| `solutions/ecommerce/etsy-product-detail` | "Etsy product detail scraper: given an Etsy listing URL, returns full product detail including listingId, title, priceCurrent, pri… |
| `solutions/ecommerce/etsy-shop-catalog` | "Etsy shop catalog scraper: given an Etsy shop URL (e.g. https://www.etsy.com/shop/{shop-name}) and optional page number, returns … |
| `solutions/ecommerce/goofish-item-detail` | "Extracts full detail data from a single Goofish (闲鱼/xianyu, goofish.com) second-hand item page. Input: item URL or item ID. Outpu… |
| `solutions/ecommerce/goofish-search-list` | "Scrapes second-hand item search results from Goofish (闲鱼/xianyu, goofish.com) — China's largest second-hand marketplace. Input: k… |
| `solutions/ecommerce/taobao-keyword-search` | "Search Taobao and Tmall product listings by keyword, returning paginated product cards with title, price, shop, image, sales, and… |
| `solutions/ecommerce/taobao-product-detail` | "Fetch full product detail from a Taobao or Tmall product page by itemId, returning title, price, shop info, images, SKU variants,… |
| `solutions/ecommerce/taobao-product-reviews` | "Fetch customer reviews for a Taobao or Tmall product by itemId, returning reviewer name, date, purchased variant, review text, an… |
| `solutions/ecommerce/taobao-shop-catalog` | "Browse a Taobao or Tmall shop's product catalog by shopId, returning paginated product listings with itemId and title. Use when u… |
| `solutions/ecommerce/walmart-category-listing` | "Walmart category page scraper: input a walmart.com browse or category URL with optional page number, extract paginated product li… |
| `solutions/ecommerce/walmart-keyword-search` | "Walmart keyword search scraper: input a search keyword and page number, navigate to walmart.com search results, extract paginated… |
| `solutions/ecommerce/walmart-product-detail` | "Walmart product detail page extractor: given a walmart.com product URL (walmart.com/ip/...), extract full product data including … |
| `solutions/ecommerce/walmart-product-reviews` | "Walmart product reviews scraper: given a walmart.com product item ID, navigate to the reviews page and extract paginated customer… |
| `solutions/lead-generation/business-contact-social-links-skill` | "This skill helps users automatically extract official website and social media profiles. Agent should proactively apply this skil… |
| `solutions/lead-generation/github-project-contributor-finder-api-skill` | "This skill helps users extract GitHub repository project details and contributor contact information using keywords, stars, and u… |
| `solutions/lead-generation/google-maps-api-skill` | "This skill helps users automatically scrape business data from Google Maps using the BrowserAct Google Maps API. Agent should pro… |
| `solutions/lead-generation/google-maps-contact-extract` | "Extracts business contact details from Google Maps search results and place detail pages, then visits each business website to co… |
| `solutions/lead-generation/google-maps-reviews-api-skill` | "This skill is designed to help users automatically extract reviews from Google Maps via the Google Maps Reviews API. Agent should… |
| `solutions/lead-generation/google-maps-search-api-skill` | "This skill is designed to help users automatically extract business data from Google Maps search results. The Agent should proact… |
| `solutions/lead-generation/google-social-media-finder` | "Searches Google to discover social media profiles associated with a person, brand, or username; returns platform name, profile UR… |
| `solutions/lead-generation/indeed-job-search` | "Scrape job listings from Indeed.com by keyword, location, and country. Returns job title, company, salary, rating, description, b… |
| `solutions/lead-generation/industry-key-contact-radar-api-skill` | "This skill helps users discover key contacts across industries, roles, and social platforms via the BrowserAct API. Agent should … |
| `solutions/lead-generation/linkedin-jobs-search` | "Search LinkedIn job listings and extract full job details. Supports filtering by work type (remote/on-site/hybrid), contract type… |
| `solutions/lead-generation/producthunt-launches` | "Scrape Product Hunt daily/weekly/monthly/yearly leaderboard launches with full product details, maker profiles, and website conta… |
| `solutions/lead-generation/social-media-finder-skill` | "This skill helps users automatically find social media profiles across platforms like Facebook, Twitter, Instagram, LinkedIn, etc… |
| `solutions/lead-generation/trustpilot-company-info` | "Trustpilot company profile lookup on trustpilot.com — input a company domain (e.g. apple.com, shopify.com, shopwagandtail.com) an… |
| `solutions/lead-generation/youtube-channel-business-email` | "YouTube channel business email and contact extractor: accepts a channel id (UCxxx), handle (@name), or URL; navigates the channel… |
| `solutions/search-research/google-image-api-skill` | This skill helps users automatically extract structured image data from Google Images via BrowserAct API. Agent should proactively… |
| `solutions/search-research/google-news-api-skill` | "This skill helps users automatically extract structured news data from Google News via BrowserAct API. Agent should proactively a… |
| `solutions/search-research/google-search-serp` | "Extracts Google Search results page (SERP) data including organic results, paid ads, related searches, People Also Ask questions,… |
| `solutions/search-research/web-research-assistant` | AI-powered web research assistant that leverages BrowserAct API to supplement restricted web access by searching the internet for … |
| `solutions/search-research/web-search-scraper-api-skill` | "This skill helps users automatically extract complete Markdown content from any website via the BrowserAct Web Search Scraper API… |
| `solutions/search-research/webcrawler-deep-crawl` | "Deep-crawl any website from start URLs, return per-page LLM-ready text/markdown/HTML plus metadata (title, description, author, l… |
| `solutions/social-listening/facebook-ads-library-search` | "Searches Meta Ad Library (Facebook/Instagram/WhatsApp ads) by keyword or Facebook page ID and extracts ad details including creat… |
| `solutions/social-listening/facebook-groups-scrape-posts` | "Scrapes posts from a Facebook group given a group URL, sort order, and desired count — returns structured post metadata including… |
| `solutions/social-listening/facebook-page-posts` | "Scrapes posts from any public Facebook Page timeline, returning structured data including post text, author info, engagement metr… |
| `solutions/social-listening/facebook-page-profile-posts` | "Scrapes posts from any public Facebook Page or personal Profile timeline, returning structured data including post text, author i… |
| `solutions/social-listening/instagram-hashtag-posts` | "Scrapes Instagram posts by hashtag, returning media items with captions, like/comment counts, media URLs and user info from the h… |
| `solutions/social-listening/instagram-place-posts` | "Scrapes Instagram posts tagged at a specific location or place, returning media items with captions, like/comment counts, media U… |
| `solutions/social-listening/instagram-post-comments` | "Fetches comments from an Instagram post including comment text, username, timestamp, like count and reply count. Use when user me… |
| `solutions/social-listening/instagram-profile-meta` | "Fetches Instagram user profile metadata including bio, follower count, following count, post count, verification status and other… |
| `solutions/social-listening/instagram-profile-posts` | "Scrapes posts from an Instagram user's profile feed including captions, media URLs, like/comment counts, timestamps and location … |
| `solutions/social-listening/reddit-competitor-analysis-api-skill` | "This skill helps users extract structured data from Reddit posts and comments via BrowserAct API. Agent should proactively apply … |
| `solutions/social-listening/reddit-warmup` | (无描述) |
| `solutions/social-listening/threads-keyword-search` | "Searches Threads posts by keyword or hashtag and returns matching posts with engagement metrics, extracted from SSR-embedded JSON… |
| `solutions/social-listening/threads-profile-search` | "Discovers Threads user accounts by keyword, extracting profile data including username, display name, verification status, biogra… |
| `solutions/social-listening/threads-user-posts` | "Fetches public posts from a Threads user's profile page, extracting post text, engagement metrics, and media info from SSR-embedd… |
| `solutions/social-listening/trustpilot-company-info` | "Trustpilot company profile lookup on trustpilot.com — input a company domain (e.g. apple.com, shopify.com, shopwagandtail.com) an… |
| `solutions/social-listening/trustpilot-reviews` | "Trustpilot customer reviews scraper for any company listed on trustpilot.com — given a company domain (e.g. shopify.com, apple.co… |
| `solutions/social-listening/wechat-article-search-api-skill` | "This skill helps users extract full article contents from WeChat using the BrowserAct API. The Agent should proactively apply thi… |
| `solutions/social-listening/x-dm-auto-chat` | "X (Twitter) DM automated chat end-to-end Skill: scan DM inbox to identify pending-reply conversations, read message history, gene… |
| `solutions/social-listening/x-keyword-comment` | "X (Twitter) keyword-based reply posting: search tweets by keyword, read each tweet's content, generate contextual replies from a … |
| `solutions/social-listening/x-tweet-by-conversation` | "Collects every tweet in an X (Twitter) conversation thread given a conversation id (root tweet id) — the focal tweet plus all rep… |
| `solutions/social-listening/x-tweet-by-handle` | "Scrapes tweets from an X (Twitter) user profile timeline given a handle, with selectable mode: tweets, tweets+replies, or media-o… |
| `solutions/social-listening/x-tweet-by-url` | "Scrapes tweets from any X (Twitter) URL — search results, user profile, single tweet detail, or list timeline — and returns norma… |
| `solutions/social-listening/x-tweet-search` | "Scrapes tweets from X (Twitter) by search query, user handle, or direct URL — returns full tweet data including text, author info… |
| `solutions/social-listening/x-tweet-search-by-query` | "Searches X (Twitter) for tweets by free-form advanced query and returns a normalized tweet list with text, author profile, engage… |
| `solutions/social-listening/xiaohongshu-auto-posting` | "Automates the complete Xiaohongshu (XHS / Little Red Book) content operation workflow: pain-point topic collection → style case c… |
| `solutions/social-listening/xiaohongshu-note-detail` | "Fetch Xiaohongshu (RedNote / xhs) note detail and comments by note ID, returning title, description, author info, engagement stat… |
| `solutions/social-listening/xiaohongshu-search` | "Search Xiaohongshu (RedNote / xhs) notes by keyword and return a paginated list with title, author, engagement stats (likes, coll… |
| `solutions/social-listening/xiaohongshu-search-full` | "Search Xiaohongshu (XHS / RedNote) notes by keyword with full field extraction including body text, topics/tags, image list URLs,… |
| `solutions/social-listening/xiaohongshu-user-profile` | "Fetch Xiaohongshu (RedNote / xhs) user profile information and their published notes list by user ID, returning nickname, bio, fo… |
| `solutions/social-listening/zhihu-search-api-skill` | "This skill helps users automatically extract structured article details and full content from Zhihu via the BrowserAct API. Agent… |
| `solutions/video-platforms/douyin-video-search` | "Searches Douyin (douyin.com) for videos by keyword and returns structured video data including author info, stats, cover, descrip… |
| `solutions/video-platforms/tiktok-hashtag-videos` | "TikTok hashtag video scraper: input a hashtag name → output paginated video list with full metadata (author profile, engagement s… |
| `solutions/video-platforms/tiktok-profile-videos` | "TikTok user profile video scraper: input a TikTok username → output the user's profile info plus paginated video list with full m… |
| `solutions/video-platforms/tiktok-search-videos` | "TikTok keyword search video scraper: input search keyword → output paginated video list with full metadata (author, engagement st… |
| `solutions/video-platforms/tiktok-video-detail` | "TikTok single video detail scraper: input a TikTok video URL → output full video metadata (author profile, engagement stats, musi… |
| `solutions/video-platforms/youtube-api-skill` | "This skill helps users automatically extract detailed video metrics and channel information from YouTube based on keyword searche… |
| `solutions/video-platforms/youtube-batch-transcript-extractor-api-skill` | "This skill helps users automatically extract YouTube video transcripts and metadata in batch via the BrowserAct API. The Agent sh… |
| `solutions/video-platforms/youtube-channel-api-skill` | "This skill helps users automatically extract structured channel data from YouTube search results via BrowserAct API. Agent should… |
| `solutions/video-platforms/youtube-comments-api-skill` | "This skill helps users extract structured video list data and comment data from YouTube using the BrowserAct API. The Agent shoul… |
| `solutions/video-platforms/youtube-influencer-finder-api-skill` | This skill helps users extract YouTube influencer profiles including social links, subscriber counts, and channel stats via the Br… |
| `solutions/video-platforms/youtube-search-api-skill` | This skill helps users automatically extract structured data from YouTube search results using the BrowserAct API. The Agent shoul… |
| `solutions/video-platforms/youtube-transcript` | "YouTube transcript extraction and content reformatting: given a YouTube video URL, opens the video's transcript panel, extracts a… |
| `solutions/video-platforms/youtube-transcript-analysis-api-skill` | "This skill helps users extract YouTube video transcripts and perform deep competitive analysis on the content. Agent should proac… |
| `solutions/video-platforms/youtube-transcript-extractor-api-skill` | "This skill helps users automatically extract YouTube video transcripts and metadata via the BrowserAct API. The Agent should proa… |
| `solutions/video-platforms/youtube-video-api-skill` | This skill helps users automatically extract channel-level and video detail data from a specific YouTube channel via BrowserAct AP… |

---

## marketing（100）

| 技能 | 用途 |
|------|------|
| `ab-testing` | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use w… |
| `ad-creative` | "When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — f… |
| `ads` | "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other … |
| `ai-seo` | "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use whe… |
| `analytics` | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up track… |
| `aso` | "When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO audit,' 'app s… |
| `attribution` | When the user wants to figure out which marketing actually drives conversions and revenue, choose or interpret an attribution mode… |
| `churn-prevention` | "When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement retentio… |
| `co-marketing` | "When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities. Use when the us… |
| `cold-email` | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, prospecting… |
| `community-marketing` | "Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a community st… |
| `competitor-profiling` | "When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions 'competitor pro… |
| `competitors` | "When the user wants to create competitor comparison or alternative pages for SEO and buyer-facing use. Also use when the user men… |
| `content-strategy` | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when t… |
| `copy-editing` | "When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user ment… |
| `copywriting` | When the user wants to write, rewrite, or improve marketing copy for any page, including homepage, landing pages, pricing pages, f… |
| `cro` | "When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pag… |
| `customer-research` | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer research," "ICP res… |
| `directory-submissions` | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for backlinks, domain… |
| `emails` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also… |
| `events` | "When the user wants to plan, run, sponsor, speak at, or get pipeline from events — webinars, conferences, trade shows, meetups, d… |
| `free-tools` | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awarenes… |
| `image` | "When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product mockups, … |
| `influencer-marketing` | "When the user wants to run influencer, creator, or ambassador partnerships to promote their product — finding and vetting partner… |
| `launch` | "When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,… |
| `lead-magnets` | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the user mentio… |
| `marketing-council` | "When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors staffed by legendary mar… |
| `marketing-ideas` | "When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks f… |
| `marketing-loops` | "When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a cadence (wee… |
| `marketing-plan` | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product. Also use when the us… |
| `marketing-psychology` | "When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user … |
| `offers` | "When the user wants to design, construct, or improve an offer — the thing they actually sell — including value framing, bonus sta… |
| `onboarding` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the… |
| `paywalls` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the use… |
| `popups` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when t… |
| `pricing` | "When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' … |
| `product-marketing` | "When the user wants to create or update their product marketing context document. Also use when the user mentions 'product contex… |
| `programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SE… |
| `prospecting` | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, general B2B, or local small… |
| `public-relations` | "When the user wants help with public relations, earned media, press coverage, journalist outreach, or media strategy (not pull re… |
| `referrals` | "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use wh… |
| `revops` | "When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use wh… |
| `sales-enablement` | "When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when … |
| `schema` | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "sch… |
| `seo-audit` | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technica… |
| `signup` | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions… |
| `site-architecture` | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. A… |
| `skills/ab-testing` | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use w… |
| `skills/ad-creative` | "When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — f… |
| `skills/ads` | "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other … |
| `skills/ai-seo` | "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use whe… |
| `skills/analytics` | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up track… |
| `skills/aso` | "When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO audit,' 'app s… |
| `skills/attribution` | When the user wants to figure out which marketing actually drives conversions and revenue, choose or interpret an attribution mode… |
| `skills/churn-prevention` | "When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement retentio… |
| `skills/co-marketing` | "When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities. Use when the us… |
| `skills/cold-email` | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, prospecting… |
| `skills/community-marketing` | "Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a community st… |
| `skills/competitor-profiling` | "When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions 'competitor pro… |
| `skills/competitors` | "When the user wants to create competitor comparison or alternative pages for SEO and buyer-facing use. Also use when the user men… |
| `skills/content-strategy` | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when t… |
| `skills/copy-editing` | "When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user ment… |
| `skills/copywriting` | When the user wants to write, rewrite, or improve marketing copy for any page, including homepage, landing pages, pricing pages, f… |
| `skills/cro` | "When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pag… |
| `skills/customer-research` | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer research," "ICP res… |
| `skills/directory-submissions` | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for backlinks, domain… |
| `skills/emails` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also… |
| `skills/events` | "When the user wants to plan, run, sponsor, speak at, or get pipeline from events — webinars, conferences, trade shows, meetups, d… |
| `skills/free-tools` | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awarenes… |
| `skills/image` | "When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product mockups, … |
| `skills/influencer-marketing` | "When the user wants to run influencer, creator, or ambassador partnerships to promote their product — finding and vetting partner… |
| `skills/launch` | "When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,… |
| `skills/lead-magnets` | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the user mentio… |
| `skills/marketing-council` | "When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors staffed by legendary mar… |
| `skills/marketing-ideas` | "When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks f… |
| `skills/marketing-loops` | "When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a cadence (wee… |
| `skills/marketing-plan` | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product. Also use when the us… |
| `skills/marketing-psychology` | "When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user … |
| `skills/offers` | "When the user wants to design, construct, or improve an offer — the thing they actually sell — including value framing, bonus sta… |
| `skills/onboarding` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the… |
| `skills/paywalls` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the use… |
| `skills/popups` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when t… |
| `skills/pricing` | "When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' … |
| `skills/product-marketing` | "When the user wants to create or update their product marketing context document. Also use when the user mentions 'product contex… |
| `skills/programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SE… |
| `skills/prospecting` | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, general B2B, or local small… |
| `skills/public-relations` | "When the user wants help with public relations, earned media, press coverage, journalist outreach, or media strategy (not pull re… |
| `skills/referrals` | "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use wh… |
| `skills/revops` | "When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use wh… |
| `skills/sales-enablement` | "When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when … |
| `skills/schema` | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "sch… |
| `skills/seo-audit` | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technica… |
| `skills/signup` | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions… |
| `skills/site-architecture` | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. A… |
| `skills/sms` | When the user wants to plan, build, or optimize SMS, MMS, or WhatsApp marketing — including welcome flows, abandoned cart texts, p… |
| `skills/social` | "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, or … |
| `skills/video` | "When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the us… |
| `sms` | When the user wants to plan, build, or optimize SMS, MMS, or WhatsApp marketing — including welcome flows, abandoned cart texts, p… |
| `social` | "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, or … |
| `video` | "When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the us… |

---

## openmontage（90）

| 技能 | 用途 |
|------|------|
| `3d-asset-generation` | Generate, reconstruct, inspect, and route production 3D assets for OpenMontage worlds using Atlas Cloud, fal.ai, licensed catalogs… |
| `acestep` | AI music generation with ACE-Step 1.5 — background music, vocal tracks, covers, stem extraction for video production. Use when gen… |
| `agents` | Build voice AI agents with ElevenLabs. Use when creating voice assistants, customer service bots, interactive voice characters, or… |
| `ai-video-gen` | (无描述) |
| `atlas-cloud` | Generate or edit images and videos through the Atlas Cloud gateway. Use for Atlas-hosted Seedance 2.5/2.0, Gemini Omni Flash, Mini… |
| `avatar-video` | (无描述) |
| `azure-speech-to-text` | Transcribe audio to text using Azure AI Speech (Fast Transcription REST API). Use when converting audio/video to text, generating … |
| `azure-text-to-speech` | Generate neural narration audio using Azure AI Speech (REST text-to-speech). Use when synthesizing voiceovers or narration in Open… |
| `beautiful-mermaid` | Render Mermaid diagrams as SVG and PNG using the Beautiful Mermaid library. Use when the user asks to render a Mermaid diagram. |
| `bfl-api` | BFL FLUX API integration guide covering endpoints, async polling patterns, rate limiting, error handling, webhooks, and regional e… |
| `canvas-procedural-animation` | Use p5.js/canvas for local procedural character effects: particles, weather, squash/stretch, walk cycles, and environmental motion… |
| `character-animation-qa` | Review local character animation with schema checks, Playwright browser previews, frame sampling, and FFmpeg/ffprobe final output … |
| `character-rigging` | Build data-driven 2D character rigs for local animation: parts, pivots, layers, constraints, views, and reusable rig packages. |
| `comfyui` | Use when working with ComfyUI workflows in OpenMontage, including comfyui_image/comfyui_video/comfyui_music, custom workflow_json/… |
| `create-video` | (无描述) |
| `d3-viz` | Creating interactive data visualisations using d3.js. This skill should be used when creating custom charts, graphs, network diagr… |
| `dashscope` | DashScope (Alibaba Cloud Bailian / 阿里云百炼) integration — image generation (qwen-image-2.0-pro), text-to-speech (qwen3-tts-flash), a… |
| `doubao-tts` | Generate Mandarin and multilingual narration with Volcengine Doubao Speech 2.0. Use when creating Chinese voiceovers, when the use… |
| `elevenlabs` | Generate AI voiceovers, sound effects, and music using ElevenLabs APIs. Use when creating audio content for videos, podcasts, or g… |
| `faceswap` | (无描述) |
| `ffmpeg` | Video and audio processing with FFmpeg. Use for format conversion, resizing, compression, audio extraction, and preparing assets f… |
| `fish-audio-tts` | Generate expressive, multilingual narration with fish.audio (S1 / S2-generation models) and reuse cloned voices via reference_id. … |
| `flux-best-practices` | Comprehensive guide for BFL FLUX image generation models. Covers prompting, T2I, I2I, structured JSON, hex colors, typography, mul… |
| `framer-motion` | Use when implementing Disney's 12 animation principles with Framer Motion in React applications |
| `gemini-omni` | (无描述) |
| `grok-media` | xAI Grok image and video generation guide covering authentication, endpoints, prompt structure, image editing, reference-image vid… |
| `gsap-core` | Official GSAP skill for the core API — gsap.to(), from(), fromTo(), easing, duration, stagger, defaults, gsap.matchMedia() (respon… |
| `gsap-frameworks` | Official GSAP skill for Vue, Svelte, and other non-React frameworks — lifecycle, scoping selectors, cleanup on unmount. Use when t… |
| `gsap-performance` | Official GSAP skill for performance — prefer transforms, avoid layout thrashing, will-change, batching. Use when optimizing GSAP a… |
| `gsap-plugins` | Official GSAP skill for GSAP plugins — registration, ScrollToPlugin, ScrollSmoother, Flip, Draggable, Inertia, Observer, SplitText… |
| `gsap-react` | Official GSAP skill for React — useGSAP hook, refs, gsap.context(), cleanup. Use when the user wants animation in React or Next.js… |
| `gsap-scrolltrigger` | Official GSAP skill for ScrollTrigger — scroll-linked animations, pinning, scrub, triggers. Use when building or recommending scro… |
| `gsap-timeline` | Official GSAP skill for timelines — gsap.timeline(), position parameter, nesting, playback. Use when sequencing animations, choreo… |
| `gsap-utils` | Official GSAP skill for gsap.utils — clamp, mapRange, normalize, interpolate, random, snap, toArray, wrap, pipe. Use when the user… |
| `heygen` | (无描述) |
| `hyperframes` | > |
| `hyperframes-animation` | "All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-de… |
| `hyperframes-cli` | HyperFrames CLI dev loop. Use when running npx hyperframes init, add, catalog, capture, lint, validate, inspect, layout, snapshot,… |
| `hyperframes-core` | The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes… |
| `hyperframes-creative` | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography… |
| `hyperframes-media` | Audio and media assets for HyperFrames compositions, produced by one shared audio engine (`scripts/audio.mjs`) — multi-provider TT… |
| `hyperframes-registry` | Install and wire registry blocks and components into HyperFrames compositions. Use when running hyperframes add, installing a bloc… |
| `kling-official` | Official Kling direct API guidance for OpenMontage providers. Use before calling `kling_official_video`, `kling_official_image`, `… |
| `lottie-bodymovin` | Use when implementing Disney's 12 animation principles with Lottie animations exported from After Effects |
| `ltx2` | AI video generation with LTX-2.3 22B — text-to-video, image-to-video clips for video production. Use when generating video clips, … |
| `lyria` | Generate and validate music with Google Lyria 3 through the Gemini Interactions API. Use before calling OpenMontage `google_music`… |
| `manim-composer` | (无描述) |
| `manimce-best-practices` | (无描述) |
| `manimgl-best-practices` | (无描述) |
| `media-use` | Agent Media OS — resolve any media need (BGM, SFX, image, icon) into a frozen local file + ledger record. One verb (`resolve`) han… |
| `minimax-h3` | (无描述) |
| `motion-graphics` | > |
| `music` | Generate music using ElevenLabs Music API. Use when creating instrumental tracks, songs with lyrics, background music, jingles, or… |
| `music-to-video` | "Use when the user has a music track (an audio file, or a video to pull audio from) and wants a beat-synced HyperFrames video, cal… |
| `playwright-recording` | Record browser interactions as video using Playwright. Use for capturing demo videos, app walkthroughs, and UI flows for Remotion … |
| `pose-library-design` | Design reusable 2D character pose libraries, action cycles, and expression states for data-driven animation. |
| `provider-model-refresh` | Use the September 2026 image, video, speech and Avatar V adapters with explicit model/host contracts. |
| `remotion` | Toolkit-specific Remotion patterns — custom transitions, shared components, and project conventions. For core Remotion framework k… |
| `remotion-best-practices` | Best practices for Remotion - Video creation in React |
| `remotion-to-hyperframes` | 'Port an existing Remotion (React) composition to HyperFrames HTML. Use ONLY when the user explicitly asks to port/convert/migrate… |
| `seedance-2-0` | (无描述) |
| `seedance-2-5` | (无描述) |
| `setup-api-key` | Guides users through setting up an ElevenLabs API key for ElevenLabs MCP tools. Use when the user needs to configure an ElevenLabs… |
| `sound-effects` | Generate sound effects from text descriptions using ElevenLabs. Use when creating sound effects, generating audio textures, produc… |
| `speech-to-text` | Transcribe audio to text using ElevenLabs Scribe v2. Use when converting audio/video to text, generating subtitles, transcribing m… |
| `svg-character-animation` | Animate SVG character rigs with GSAP, CSS transforms, Remotion frame control, and HyperFrames-compatible browser previews. |
| `synthetic-screen-recording` | Synthetic terminal-style screen recording guidance for Remotion `TerminalScene`. |
| `tailwind-design-system` | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating… |
| `text-to-speech` | (无描述) |
| `threejs-animation` | Three.js animation - keyframe animation, skeletal animation, morph targets, animation mixing. Use when animating objects, playing … |
| `threejs-fundamentals` | Three.js scene setup, cameras, renderer, Object3D hierarchy, coordinate systems. Use when setting up 3D scenes, creating cameras, … |
| `threejs-geometry` | Three.js geometry creation - built-in shapes, BufferGeometry, custom geometry, instancing. Use when creating 3D shapes, working wi… |
| `threejs-interaction` | Three.js interaction - raycasting, controls, mouse/touch input, object selection. Use when handling user input, implementing click… |
| `threejs-lighting` | Three.js lighting - light types, shadows, environment lighting. Use when adding lights, configuring shadows, setting up IBL, or op… |
| `threejs-loaders` | Three.js asset loading - GLTF, textures, images, models, async patterns. Use when loading 3D models, textures, HDR environments, o… |
| `threejs-materials` | Three.js materials - PBR, basic, phong, shader materials, material properties. Use when styling meshes, working with textures, cre… |
| `threejs-postprocessing` | Three.js post-processing - EffectComposer, bloom, DOF, screen effects. Use when adding visual effects, color grading, blur, glow, … |
| `threejs-shaders` | Three.js shaders - GLSL, ShaderMaterial, uniforms, custom effects. Use when creating custom visual effects, modifying vertices, wr… |
| `threejs-textures` | Three.js textures - texture types, UV mapping, environment maps, texture settings. Use when working with images, UV coordinates, c… |
| `threejs-world-generation` | Build deterministic, editable, free-viewpoint Three.js worlds from text or structured briefs. Use for cinematic 3D terrain, semant… |
| `vercel-composition-patterns` | (无描述) |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, … |
| `video-download` | (无描述) |
| `video-edit` | (无描述) |
| `video-toolkit` | Create professional videos autonomously using claude-code-video-toolkit — AI voiceovers, image generation, music, talking heads, a… |
| `video-translate` | (无描述) |
| `video-understand` | (无描述) |
| `visual-style` | (无描述) |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "… |
| `website-to-video` | "Capture a general website/URL and turn it into a HyperFrames video (site tour, showcase, or social clip from the site's own visua… |

---

## mattpocock（76）

| 技能 | 用途 |
|------|------|
| `engineering/ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `engineering/code-review` | "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this … |
| `engineering/codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening op… |
| `engineering/diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something bro… |
| `engineering/domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recordi… |
| `engineering/grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `engineering/implement` | "Implement a piece of work based on a spec or set of tickets." |
| `engineering/implement-spec` | "Implement the result of /to-spec and /to-tickets in code." |
| `engineering/improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `engineering/pr` | "Use when writing a PR body." |
| `engineering/prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic fe… |
| `engineering/research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the us… |
| `engineering/retro` | "Conduct a retrospective on a coding session." |
| `engineering/setup-matt-pocock-skills` | "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run onc… |
| `engineering/tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants… |
| `engineering/to-spec` | "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you'v… |
| `engineering/to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published … |
| `engineering/triage` | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready b… |
| `engineering/wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and re… |
| `engineering/wizard` | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, … |
| `in-progress/chief-of-staff` | Pursue a long-running goal in a single session by co-ordinating subagents. |
| `in-progress/claude-handoff` | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| `in-progress/loop-me` | Grill me about specs for the workflows I want to build, within this workspace. |
| `in-progress/setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reac… |
| `in-progress/writing-beats` | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| `in-progress/writing-fragments` | "Writing, explore: mine raw fragments, no structure yet." |
| `in-progress/writing-shape` | "Writing, exploit: shape raw material into an article, paragraph by paragraph." |
| `misc/git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use whe… |
| `misc/migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as`… |
| `misc/scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to … |
| `misc/setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to ad… |
| `productivity/grill-me` | A relentless interview to sharpen a plan or design. |
| `productivity/grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'g… |
| `productivity/handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `productivity/teach` | Teach the user a new skill or concept, within this workspace. |
| `productivity/to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| `productivity/wait-what` | "Stop. That last message did not land: re-pitch it." |
| `productivity/writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |
| `skills/engineering/ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `skills/engineering/code-review` | "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this … |
| `skills/engineering/codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening op… |
| `skills/engineering/diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something bro… |
| `skills/engineering/domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recordi… |
| `skills/engineering/grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `skills/engineering/implement` | "Implement a piece of work based on a spec or set of tickets." |
| `skills/engineering/implement-spec` | "Implement the result of /to-spec and /to-tickets in code." |
| `skills/engineering/improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `skills/engineering/pr` | "Use when writing a PR body." |
| `skills/engineering/prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic fe… |
| `skills/engineering/research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the us… |
| `skills/engineering/retro` | "Conduct a retrospective on a coding session." |
| `skills/engineering/setup-matt-pocock-skills` | "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run onc… |
| `skills/engineering/tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants… |
| `skills/engineering/to-spec` | "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you'v… |
| `skills/engineering/to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published … |
| `skills/engineering/triage` | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready b… |
| `skills/engineering/wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and re… |
| `skills/engineering/wizard` | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, … |
| `skills/in-progress/chief-of-staff` | Pursue a long-running goal in a single session by co-ordinating subagents. |
| `skills/in-progress/claude-handoff` | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| `skills/in-progress/loop-me` | Grill me about specs for the workflows I want to build, within this workspace. |
| `skills/in-progress/setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reac… |
| `skills/in-progress/writing-beats` | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| `skills/in-progress/writing-fragments` | "Writing, explore: mine raw fragments, no structure yet." |
| `skills/in-progress/writing-shape` | "Writing, exploit: shape raw material into an article, paragraph by paragraph." |
| `skills/misc/git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use whe… |
| `skills/misc/migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as`… |
| `skills/misc/scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to … |
| `skills/misc/setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to ad… |
| `skills/productivity/grill-me` | A relentless interview to sharpen a plan or design. |
| `skills/productivity/grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'g… |
| `skills/productivity/handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `skills/productivity/teach` | Teach the user a new skill or concept, within this workspace. |
| `skills/productivity/to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| `skills/productivity/wait-what` | "Stop. That last message did not land: re-pitch it." |
| `skills/productivity/writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |

---

## gstack（63）

| 技能 | 用途 |
|------|------|
| `autoplan` | Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisi… |
| `benchmark` | Performance regression detection. (gstack) |
| `benchmark-models` | Cross-model benchmark for gstack skills. (gstack) |
| `browse` | "Drive a real browser through Aside: open a page, read it, click through a flow, take screenshots, check console errors. (gstack)" |
| `browser-skills/hackernews-frontpage` | Scrape the Hacker News front page (titles, points, comment counts). |
| `canary` | Post-deploy canary monitoring. (gstack) |
| `careful` | Safety guardrails for destructive commands. (gstack) |
| `codex` | OpenAI Codex CLI wrapper — three modes. (gstack) |
| `context-restore` | Restore working context saved earlier by /context-save. (gstack) |
| `context-save` | Save working context. (gstack) |
| `cso` | "Security audit: supported static findings; qualified profiles add reproduction and repair candidates. (gstack)" |
| `design-consultation` | "Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography… |
| `design-html` | "Design finalization: generates production-quality Pretext-native HTML/CSS. (gstack)" |
| `design-review` | "Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then… |
| `design-shotgun` | "Design shotgun: generate multiple AI design variants, open a comparison board, collect structured feedback, and iterate. (gstack)… |
| `deslop-shared-libs` | Find worthwhile shared-code extractions in recent work. (gstack) |
| `devex-review` | Live developer experience audit. (gstack) |
| `diagram` | "Turn an English description (or mermaid source) into a diagram triplet: the source, an editable .excalidraw file you can open on … |
| `document-generate` | Generate missing documentation from scratch for a feature, module, or entire project. (gstack) |
| `document-release` | Release documentation audit. (gstack) |
| `freeze` | Restrict file edits to a specific directory for the session. (gstack) |
| `gstack` | Router for the gstack skill suite. (gstack) |
| `gstack-upgrade` | Upgrade gstack to the latest version. |
| `guard` | "Full safety mode: destructive command warnings + directory-scoped edits. (gstack)" |
| `health` | Code quality dashboard. (gstack) |
| `investigate` | Systematic debugging with root cause investigation. (gstack) |
| `ios-clean` | "Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. (gstack)" |
| `ios-design-review` | Visual design audit for iOS apps on real hardware. (gstack) |
| `ios-fix` | Autonomous iOS bug fixer. (gstack) |
| `ios-qa` | Live-device iOS QA for SwiftUI apps. (gstack) |
| `ios-sync` | Regenerate the iOS debug bridge against the latest upstream gstack templates. (gstack) |
| `land-and-deploy` | Land and deploy workflow. (gstack) |
| `landing-report` | Read-only queue dashboard for workspace-aware ship. (gstack) |
| `learn` | Manage project learnings. |
| `make-pdf` | Turn any markdown file into a publication-quality PDF. (gstack) |
| `office-hours` | YC Office Hours — two modes. (gstack) |
| `open-gstack-browser` | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. |
| `openclaw/skills/gstack-openclaw-ceo-review` | Use when asked to review a plan, challenge a proposal, run a CEO review, poke holes in an approach, think bigger about scope, or d… |
| `openclaw/skills/gstack-openclaw-investigate` | Use when asked to debug, fix a bug, investigate an error, or do root cause analysis, and when users report errors, stack traces, u… |
| `openclaw/skills/gstack-openclaw-office-hours` | Use when asked to brainstorm, evaluate whether an idea is worth building, run office hours, or think through a new product idea or… |
| `openclaw/skills/gstack-openclaw-retro` | "Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics with persistent history and tr… |
| `pair-agent` | Pair a remote AI agent with your browser. (gstack) |
| `plan-ceo-review` | CEO/founder-mode plan review. (gstack) |
| `plan-design-review` | Designer's eye plan review — interactive, like CEO and Eng review. (gstack) |
| `plan-devex-review` | Interactive developer experience plan review. (gstack) |
| `plan-eng-review` | Eng manager-mode plan review. (gstack) |
| `plan-tune` | "Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). (gstack)" |
| `qa` | Fix browser/API/CLI/job/worker/webhook bugs. (gstack) |
| `qa-only` | Report browser/API/CLI/job/worker/webhook bugs. (gstack) |
| `retro` | Weekly engineering retrospective. (gstack) |
| `review` | Pre-landing PR review. (gstack) |
| `scrape` | Pull data from a web page through the Aside browser — your real, already signed-in sessions. (gstack) |
| `setup-browser-cookies` | Import cookies from your real Chromium browser into the headless browse session. (gstack) |
| `setup-deploy` | Configure deployment settings for /land-and-deploy. |
| `setup-gbrain` | "Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain, register MCP, capture per-remo… |
| `ship` | "Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. (gsta… |
| `skillify` | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. (gstack) |
| `spec` | Turn vague intent into a precise, executable spec in five phases. (gstack) |
| `sync-gbrain` | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. (gstack) |
| `test-audit` | Find low-value or duplicate tests and the test-only code they keep alive. (gstack) |
| `test/fixtures/context-bill/tree-a/alpha` | Fixture dispatcher with a mode table and forced-read references. |
| `test/fixtures/context-bill/tree-a/beta` | Clean fixture tool skill with no forced reads and no mode table. |
| `unfreeze` | Clear the freeze boundary set by /freeze, allowing edits to all directories again. (gstack) |

---

## media（36）

| 技能 | 用途 |
|------|------|
| `ai-music-album` | (无描述) |
| `fal-3d` | (无描述) |
| `fal-generate` | (无描述) |
| `fal-image-edit` | (无描述) |
| `fal-kling-o3` | (无描述) |
| `fal-lip-sync` | (无描述) |
| `fal-realtime` | (无描述) |
| `fal-restore` | (无描述) |
| `fal-train` | (无描述) |
| `fal-tryon` | (无描述) |
| `fal-upscale` | (无描述) |
| `fal-video-edit` | (无描述) |
| `fal-vision` | (无描述) |
| `full-page-screenshot` | (无描述) |
| `gif-search` | "Search/download GIFs from Tenor via curl + jq." |
| `gif-sticker-maker` | (无描述) |
| `image-enhancer` | (无描述) |
| `imagegen` | (无描述) |
| `imagen` | (无描述) |
| `mockup-device-3d` | "Static iPhone and MacBook 3D-style showcase with real HTML embedded on screens, glass-lens refraction, and 360-degree turntable c… |
| `moneyprinterturbo` | "本机完整版的一键 AI 短视频生成器（harry0703/MoneyPrinterTurbo，128k★）：给主题/关键词自动生成脚本、匹配素材、字幕、背景音乐并合成高清短视频，带 WebUI 和 API。Use when the user wants to… |
| `pixelbin-media` | (无描述) |
| `replicate` | (无描述) |
| `screenshot` | (无描述) |
| `songsee` | "Audio spectrograms/features (mel, chroma, MFCC) via CLI." |
| `sora` | (无描述) |
| `speech` | (无描述) |
| `venice-audio-music` | (无描述) |
| `venice-audio-speech` | (无描述) |
| `venice-image-edit` | (无描述) |
| `venice-image-generate` | (无描述) |
| `venice-video` | (无描述) |
| `video-downloader` | (无描述) |
| `video-hyperframes` | "Hyperframes / Remotion-compatible continuous frame animation with autoplay support." |
| `youtube-clipper` | (无描述) |
| `youtube-content` | "YouTube transcripts to summaries, threads, blogs." |

---

## web（33）

| 技能 | 用途 |
|------|------|
| `agent-browser` | (无描述) |
| `agent-reach` | > |
| `artifacts-builder` | (无描述) |
| `autoscraper` | Auto-scrape HTML without writing selectors — use AutoScraper's AutoScraper.get_selectors() to learn a selector from one sample ele… |
| `blocked-page-recovery` | "Use when a fetch fails: 403/429, paywall, WAF, bot wall." |
| `browser-use` | Drive a real browser with an AI agent using Browser Use (installed, Python 3.14, 0.13.x) — lets the agent look at the page, decide… |
| `crawl4ai` | Use Crawl4AI to scrape websites, crawl whole sites, or extract structured data into LLM-ready markdown/JSON — the go-to when web e… |
| `crawlee` | Build reliable Node.js web scrapers/crawlers with Apify Crawlee (installed at C:\Users\mwr_w\tools\node-packages). Use when the us… |
| `curl-impersonate` | Bypass TLS/HTTP2 fingerprinting by making curl handshakes byte-identical to Chrome/Edge/Firefox/Safari — curl-impersonate (prebuil… |
| `firecrawl` | (无描述) |
| `firecrawl-agent` | Autonomously navigate websites and extract structured data across pages. Use when the task requires navigation or no suitable read… |
| `firecrawl-alexandria` | Find a direct path to structured data through ready-made workflows, data APIs, and indexes. Follow the search skill to discover an… |
| `firecrawl-build` | Integrate Firecrawl into application code whenever a product, agent, or workflow needs web data inside the app — web search, live … |
| `firecrawl-build-interact` | Integrate Firecrawl `/interact` into product code for dynamic pages and browser actions after scraping. Use when a feature needs c… |
| `firecrawl-build-onboarding` | Get Firecrawl credentials and SDK setup into a project. Use when an application needs `FIRECRAWL_API_KEY`, when an agent should ad… |
| `firecrawl-build-scrape` | Integrate Firecrawl `/scrape` into product code for single-page extraction. Use when an app already has a URL and needs markdown, … |
| `firecrawl-build-search` | Integrate Firecrawl `/search` into product code and agent workflows. Use when an app needs discovery before extraction, when the f… |
| `firecrawl-crawl` | (无描述) |
| `firecrawl-developer-index` | Search an index of public repositories, GitHub issues, merged pull requests, repository READMEs, and curated documentation sites. … |
| `firecrawl-download` | (无描述) |
| `firecrawl-interact` | (无描述) |
| `firecrawl-map` | (无描述) |
| `firecrawl-monitor` | (无描述) |
| `firecrawl-parse` | (无描述) |
| `firecrawl-research-index` | Find the papers that answer a research query in Firecrawl's research paper index — a corpus of paper abstracts whose largest share… |
| `firecrawl-scrape` | Read a known webpage or execute a discovered workflow or data-provider capability. Use for page content or structured results once… |
| `firecrawl-search` | Find web sources with query-relevant page excerpts and optional full-page content, and discover workflows, data APIs, and indexes.… |
| `markitdown` | Convert PDF/Word/Excel/PowerPoint/HTML/images/audio/CSV/ZIP/Youtube to clean Markdown for LLM/RAG with Microsoft MarkItDown (insta… |
| `scrapling` | Scrape web pages using Scrapling with anti-bot bypass (like Cloudflare Turnstile), stealth headless browsing, spiders framework, a… |
| `scrapy` | Build production-grade web crawlers and scrape structured data from many pages at scale with Scrapy (installed, v2.19, Python 3.14… |
| `scrcpy` | Mirror and control an Android device (video+audio) from the computer via USB/TCP without installing anything on the phone — Genymo… |
| `web-artifacts-builder` | (无描述) |
| `web-clone` | > |

---

## productivity（30）

| 技能 | 用途 |
|------|------|
| `airtable` | Airtable REST API via curl. Records CRUD, filters, upserts. |
| `box` | Box manages cloud files, sharing, search, and metadata. |
| `data-report` | "Turns CSV, Excel, or JSON data into a polished visual report page." |
| `doc` | (无描述) |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, t… |
| `document-to-action-items` | "Extract cited obligations, deadlines, tasks from documents." |
| `docx` | Create, read, edit, template, and review Word .docx files. |
| `domain-name-brainstormer` | (无描述) |
| `faq-page` | (无描述) |
| `google-workspace` | "Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python." |
| `i-have-adhd` | 'Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tang… |
| `maps` | "Geocode, POIs, routes, timezones via OpenStreetMap/OSRM." |
| `meeting-action-items` | "Turn meeting notes into cited decisions, owners, tickets." |
| `minimax-docx` | (无描述) |
| `minimax-pdf` | (无描述) |
| `nanobanana-ppt` | (无描述) |
| `notion` | "Notion API + ntn CLI: pages, databases, markdown, Workers." |
| `pdf` | "PDF files: create, read, merge, fill, OCR, edit text." |
| `planning-with-files` | "Persistent file-based planning for multi-step AI-agent work. Keeps task_plan.md, findings.md, and progress.md on disk; lifecycle … |
| `powerpoint` | Create, read, edit .pptx decks with python-pptx. |
| `ppt-keynote` | "Apple Keynote-quality slides, one card per screen, with keyboard left/right navigation." |
| `pptx` | (无描述) |
| `pptx-generator` | (无描述) |
| `product-price-monitor` | "Watch product, flight, or listing prices; alert on target." |
| `release-notes-one-pager` | (无描述) |
| `research-decision-room` | (无描述) |
| `resume-modern` | "Modern minimal resume, single A4 page, ready for print or PDF export." |
| `teams-meeting-pipeline` | Teams meeting summaries, job replay, Graph subscriptions. |
| `weekly-review-planning` | "Weekly reset: commitments, stalled work, next-week plan." |
| `xlsx` | Create, read, edit Excel .xlsx workbooks and CSVs. |

---

## addyosmani（25）

| 技能 | 用途 |
|------|------|
| `api-and-interface-design` | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating RES… |
| `browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need … |
| `ci-cd-and-automation` | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate qua… |
| `code-review-and-quality` | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a h… |
| `code-simplification` | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to… |
| `constraint-driven-development` | Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Interviews the user on which dimen… |
| `context-engineering` | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, … |
| `debugging-and-error-recovery` | Guides systematic root-cause debugging. Use when tests fail, builds break, something that worked yesterday broke, behavior doesn't… |
| `deprecation-and-migration` | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementat… |
| `documentation-and-adrs` | Records decisions and documentation. Use when you need to document an architecture decision (ADR) or the reasoning behind a design… |
| `doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when you want every assumption cro… |
| `frontend-ui-engineering` | Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating c… |
| `git-workflow-and-versioning` | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, splitting… |
| `idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still … |
| `incremental-implementation` | Delivers changes incrementally in thin, verifiable slices. Use when implementing any feature or change that touches more than one … |
| `interview-me` | Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time in… |
| `observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use wh… |
| `performance-optimization` | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when … |
| `planning-and-task-breakdown` | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Us… |
| `security-and-hardening` | Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentica… |
| `shipping-and-launch` | Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping… |
| `source-driven-development` | Grounds every implementation decision in official documentation. Use when you want to verify an approach against the official docs… |
| `spec-driven-development` | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use … |
| `test-driven-development` | Drives development with tests using the red-green-refactor loop. Use when implementing any logic, fixing any bug, or changing any … |
| `using-agent-skills` | Discovers and invokes agent skills. Use when starting a session, or when you need to decide which skill or workflow applies to the… |

---

## claude-mem（22）

| 技能 | 用途 |
|------|------|
| `agent-cost-report` | >- |
| `babysit` | Watch a pull request or review cycle until it is ready to merge. Use when asked to babysit, monitor, or keep checking PR comments,… |
| `ccs-align` | Run the CCS Align seat's hourly breathing cycle — prove the local claude-mem worker is healthy, pull needle observations through s… |
| `cloud-sync` | Set up or check claude-mem cloud sync with cmem.ai Pro. Use when the user says "set up cloud sync", "sync my memories", "cmem pro"… |
| `design-is` | Audit a design against Dieter Rams' ten "Good design is..." principles, then hand off a /make-plan prompt for one of three outcome… |
| `do` | Execute a phased implementation plan using subagents. Use when asked to execute, run, or carry out a plan — especially one created… |
| `handoff` | Generate a HANDOFF.md that captures goal, current state, files touched, failed attempts, and next steps — so a fresh Claude sessio… |
| `how-it-works` | Explain how claude-mem captures observations, when memory injection kicks in, and where data lives. Use when the user asks "how do… |
| `knowledge-agent` | Build and query AI-powered knowledge bases from claude-mem observations. Use when users want to create focused "brains" from their… |
| `learn-codebase` | Prime a codebase by reading every source file in full. Use when starting work on a new or unfamiliar project, or when the user ask… |
| `make-plan` | Create a detailed, phased implementation plan with documentation discovery. Use when asked to plan a feature, task, or multi-step … |
| `mem-search` | Search claude-mem's persistent cross-session memory database. Use when user asks "did we already solve this?", "how did we do X la… |
| `mode-creator` | Interactively create, install, activate, and verify custom claude-mem modes, including domain-specific observation types, concept … |
| `oh-my-issues` | Cluster a GitHub issue backlog by root cause into a small set of plan-master issues, redirect children with a standardized comment… |
| `pathfinder` | Map a codebase into feature-grouped flowcharts, identify duplicated concerns across features, and propose a unified architecture. … |
| `smart-explore` | Token-optimized structural code search using tree-sitter AST parsing. Use instead of reading full files when you need to understan… |
| `standup` | Facilitate a read-only standup across git worktrees, branches, or PRs to compare changes and produce one consolidation plan. |
| `timeline-report` | Generate a "Journey Into [Project]" narrative report analyzing a project's entire development history from claude-mem's timeline. … |
| `version-bump` | Automated semantic versioning and release workflow for Claude Code plugins. Handles version increments across package.json, market… |
| `weekly-digests` | Generate a serial week-by-week narrative digest of a project's full claude-mem timeline. Splits the timeline into per-ISO-week fil… |
| `what-the` | "What the? Use when the user wants a plain-English breakdown of something technical — the who, what, where, why, and when." |
| `wowerpoint` | Turn one document into a kawaii NotebookLM slide-deck PDF. Use for "wowerpoint this", "make a deck about <file>", "turn this repor… |

---

## hermes-jev（22）

| 技能 | 用途 |
|------|------|
| `jev-browser-use` | Use when driving a web page in a browser — clicking, typing, navigating, logged-in or JS-rendered pages. Jev picks each step from … |
| `jev-compaction` | Use when a transcript has to be cut to a fixed size and you must choose which turns go. Jev marks each turn keep, summarize or dro… |
| `jev-computer-use` | Use when driving a desktop GUI through a computer-use driver — windows, menus, native apps, OS dialogs. You build a table of safe … |
| `jev-frontier-work` | Use when a task is already judged hard — pick which paid frontier seat takes it, then keep Jev watching the delegated run so it in… |
| `jev-mailbox` | Use on a mailbox export to sort mail into needs reply, updates, promotional, sales and spam — which messages are addressed to the … |
| `jev-memory` | Use on passages a search just returned (memory, vault, session history, wiki, web) before reading them in. Jev ranks them, drops t… |
| `jev-model-routing` | Use to pick the cheapest good-enough model or effort for a turn or a delegated task (lanes small to escalate), to decide continue/… |
| `jev-search` | Use after any web or API search, before opening results or spending another round. Jev picks which results to read, whether the ev… |
| `jev-setup` | Use when Jev is not working yet, a Jev tool reports no_key or auth_failed, or the person asks to connect or fix Jev. Gets their Ty… |
| `jev-skill-select` | Use when unsure which of many installed skills applies to a request, if any, or when asked to make skill loading cheaper or more a… |
| `jev-social-research` | Use when researching social posts, creators, reactions, or trends. Jev ranks discovery cards and decides when opened, source-linke… |
| `skills/jev-browser-use` | Use when driving a web page in a browser — clicking, typing, navigating, logged-in or JS-rendered pages. Jev picks each step from … |
| `skills/jev-compaction` | Use when a transcript has to be cut to a fixed size and you must choose which turns go. Jev marks each turn keep, summarize or dro… |
| `skills/jev-computer-use` | Use when driving a desktop GUI through a computer-use driver — windows, menus, native apps, OS dialogs. You build a table of safe … |
| `skills/jev-frontier-work` | Use when a task is already judged hard — pick which paid frontier seat takes it, then keep Jev watching the delegated run so it in… |
| `skills/jev-mailbox` | Use on a mailbox export to sort mail into needs reply, updates, promotional, sales and spam — which messages are addressed to the … |
| `skills/jev-memory` | Use on passages a search just returned (memory, vault, session history, wiki, web) before reading them in. Jev ranks them, drops t… |
| `skills/jev-model-routing` | Use to pick the cheapest good-enough model or effort for a turn or a delegated task (lanes small to escalate), to decide continue/… |
| `skills/jev-search` | Use after any web or API search, before opening results or spending another round. Jev picks which results to read, whether the ev… |
| `skills/jev-setup` | Use when Jev is not working yet, a Jev tool reports no_key or auth_failed, or the person asks to connect or fix Jev. Gets their Ty… |
| `skills/jev-skill-select` | Use when unsure which of many installed skills applies to a request, if any, or when asked to make skill loading cheaper or more a… |
| `skills/jev-social-research` | Use when researching social posts, creators, reactions, or trends. Jev ranks discovery cards and decides when opened, source-linke… |

---

## anthropics（19）

| 技能 | 用途 |
|------|------|
| `academy-guide` | > |
| `algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request cre… |
| `brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and… |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to cr… |
| `claude-api` | - |
| `discernment-nudge` | > |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, t… |
| `docx` | "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx… |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direct… |
| `internal-comms` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude s… |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through w… |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, c… |
| `pptx` | "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide d… |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from s… |
| `slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation conc… |
| `theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10… |
| `web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tai… |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debug… |
| `xlsx` | "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, rea… |

---

## autonomous-ai-agents（10）

| 技能 | 用途 |
|------|------|
| `claude-code` | "Delegate coding to Claude Code CLI (features, PRs)." |
| `computer-use` | "Drive the desktop background-first; escalate on signal." |
| `hermes-agent` | "Use, configure, theme, extend, and orchestrate Hermes Agent." |
| `librechat` | "本机完整版的 LibreChat（LibreChat-AI，45k★）：增强版 ChatGPT 开源平台，多模型/多 provider、Agents、MCP、Skills、代码执行 workspace、OIDC 部署。Use when the user wa… |
| `multi-agent-teams` | "Compose Hermes bot groups and multi-agent dev pipelines." |
| `openbot` | "本机完整版的 OpenBot（CopilotKit，6k★，alpha）：开源 AI 同事平台，每个 agent 有独立浏览器/文件/工具，AG-UI 协议接入任意 agent 框架，Docker Compose 自托管。Use when the user … |
| `opencode` | "Delegate coding to OpenCode CLI (features, PR review)." |
| `openhands` | "本机完整版的 OpenHands / Agent Canvas（All-Hands-AI/OpenHands，90k★）：自托管的编码 agent 控制中心，跑 OpenHands/Claude Code/Codex/Gemini 及任何 ACP agent… |
| `ui-tars` | UI-TARS GUI agent — drive mouse/keyboard on a desktop via a vision LLM (HuggingFace/vLLM endpoint). Use when asked to automate a d… |
| `workspace-dispatch` | (无描述) |

---

## creative（10）

| 技能 | 用途 |
|------|------|
| `architecture-diagram` | "Dark-themed SVG architecture/cloud/infra diagrams as HTML." |
| `ascii-video` | "ASCII video: convert video/audio to colored ASCII MP4/GIF." |
| `baoyu-infographic` | "Infographics: 21 layouts x 21 styles (信息图, 可视化)." |
| `claude-design` | Design one-off HTML artifacts (landing, deck, prototype). |
| `design-md` | Author/validate/export Google's DESIGN.md token spec files. |
| `humanizer` | "Humanize text: strip AI-isms and add real voice." |
| `manim-video` | "Manim CE animations: 3Blue1Brown math/algo videos." |
| `p5js` | "p5.js sketches: gen art, shaders, interactive, 3D." |
| `popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| `songwriting-and-ai-music` | "Songwriting craft and Suno AI music prompts." |

---

## research（7）

| 技能 | 用途 |
|------|------|
| `arxiv` | "Search arXiv papers by keyword, author, category, or ID." |
| `competitor-news-monitor` | "Watch named companies for material news; cited digests." |
| `d3-visualization` | (无描述) |
| `grounded-citations` | "Ground answers and documents in cited, verifiable sources." |
| `last30days` | "Research what people actually say about any topic in the last 30 days. Pulls posts and engagement from Reddit, X, YouTube, TikTok… |
| `llm-wiki` | "Karpathy's LLM Wiki: build/query interlinked markdown KB." |
| `tradingagents` | "本机完整版的多智能体金融交易框架（TauricResearch/TradingAgents，110k★，arXiv:2412.20138）：分析师/研究员/交易员/风控多 agent 协作出交易决策，支持回测、SEC EDGAR、点-in-time 数据完整… |

---

## apple（4）

| 技能 | 用途 |
|------|------|
| `apple-notes` | "Manage Apple Notes via memo CLI: create, search, edit." |
| `apple-reminders` | "Apple Reminders via remindctl: add, list, complete." |
| `findmy` | "Track Apple devices/AirTags via FindMy.app on macOS." |
| `imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. |

---

## email（2）

| 技能 | 用途 |
|------|------|
| `email-inbox-triage` | "Triage an inbox: prioritize threads, draft replies safely." |
| `himalaya` | "Himalaya CLI: IMAP/SMTP email from terminal." |

---

## social-media（2）

| 技能 | 用途 |
|------|------|
| `wxauto` | 微信 3.9.X Windows 桌面自动化 (wxauto 库) — 发/收消息、传文件、会话列表、消息监听。Use when the user wants to automate WeChat Desktop on Windows (send/receiv… |
| `xurl` | "X/Twitter via xurl CLI: raw post search, posting, DM, media." |

---

## devops（1）

| 技能 | 用途 |
|------|------|
| `sdlc-review` | Review Kanban handoffs and route verified outcomes. |

---

## note-taking（1）

| 技能 | 用途 |
|------|------|
| `obsidian` | Read, search, create, and edit notes in the Obsidian vault. |

---

## typesafe-ai（1）

| 技能 | 用途 |
|------|------|
| `typesafe-ai` | > |

---

## 给其他智能体安装（分平台说明）

本仓库技能遵循 **Agent Skills** 通用格式（每个技能是文件夹，核心是带 YAML frontmatter 的 `SKILL.md`）。

### Hermes Agent（源主环境）
```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
cd -AGENT-SKILL && ./restore.sh   # 拷到 $HERMES_HOME/skills/
```
Hermes 按 SKILL.md 的 description 自动触发，重启会话后生效。

### Claude Code
```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
mkdir -p ~/.claude/skills
cp -r -AGENT-SKILL/design -AGENT-SKILL/security -AGENT-SKILL/claude-skills ~/.claude/skills/
```

### Cursor / Codex / OpenCode / 通用 Agent Skills 平台
```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
cp -r -AGENT-SKILL/<类别> <平台的技能目录>/
```
（Codex: `~/.codex/skills/`，OpenCode: skills 路径，Cursor: `.cursor/skills/`）

### 不支持 Skills 的纯聊天模型
没有安装位置。把所需技能的 `SKILL.md` 全文作为系统提示词粘进对话，或让模型 RAG 检索该文件。

---

## 需要 API Key 的技能（142 个）

> 这些技能文件可装，但**实际运行需对应厂商 API 密钥**。密钥不要提交仓库；装好后放环境变量或平台设置里。

| 类别/技能 | 需要的密钥 | 在哪里申请 |
|-----------|-----------|-----------|
| `autonomous-ai-agents/claude-code` | ANTHROPIC_API_KEY | Anthropic — console.anthropic.com → API keys |
| `autonomous-ai-agents/codex` | OPENAI_API_KEY | OpenAI — platform.openai.com → API keys |
| `autonomous-ai-agents/librechat` | MULTI_PROVIDER_KEYS<br>POSTGRES | 按接入的模型填各 provider key<br>需要 PostgreSQL |
| `autonomous-ai-agents/openbot` | DOCKER<br>LLM_API_KEY<br>POSTGRES | Docker Compose 运行时<br>Intelligence 用 CopilotKit 或本地 Docker<br>需要 PostgreSQL |
| `autonomous-ai-agents/opencode` | OPENROUTER_API_KEY | 厂商官方 API 平台注册后生成 key |
| `autonomous-ai-agents/openhands` | DOCKER<br>LLM_API_KEY | 后端 agent 的模型 key（OpenAI/Anthropic 等）<br>需要 Docker 运行时 |
| `browser-act/solutions\ecommerce\amazon-asin-lookup-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-best-selling-products-finder-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-buy-box-monitor-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-competitor-analyzer` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-listing-competitor-analysis-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-product-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-product-search-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\ecommerce\amazon-reviews-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\business-contact-social-links-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\github-project-contributor-finder-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\google-maps-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\google-maps-reviews-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\google-maps-search-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\industry-key-contact-radar-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\lead-generation\social-media-finder-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\search-research\google-image-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\search-research\google-news-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\search-research\web-research-assistant` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\search-research\web-search-scraper-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\social-listening\reddit-competitor-analysis-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\social-listening\wechat-article-search-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\social-listening\zhihu-search-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-batch-transcript-extractor-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-channel-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-comments-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-influencer-finder-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-search-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-transcript-analysis-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-transcript-extractor-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `browser-act/solutions\video-platforms\youtube-video-api-skill` | BROWSERACT_API_KEY | 厂商官方 API 平台注册后生成 key |
| `claude-mem/agent-cost-report` | OPENROUTER_API_KEY | 厂商官方 API 平台注册后生成 key |
| `claude-skills/agent-launcher__agent-launcher-orchestrator` | ANTHROPIC_API_KEY | Anthropic — console.anthropic.com |
| `claude-skills/agent-launcher__stage-launch` | ANTHROPIC_API_KEY | Anthropic — console.anthropic.com |
| `claude-skills/c-level-agents__cross-eval` | OPENAI_API_KEY | OpenAI — platform.openai.com |
| `claude-skills/engineering__universal-scraping-architect` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev（本机已配） |
| `claude-skills/finance__stock-analysis` | EDGAR | SEC EDGAR（免费无 key） |
| `claude-skills/research__dossier` | EDGAR | SEC EDGAR（免费无 key） |
| `design/21st-dev` | API_KEY_21ST | 21st.dev — https://21st.dev/mcp 免费即时申请（旧 Magic console key 已作废） |
| `design/design` | GEMINI_API_KEY<br>MUAPI_API_KEY | Google Gemini — aistudio.google.com → Get API key<br>厂商官方 API 平台注册后生成 key |
| `design/hatch-pet` | OPENAI_API_KEY | OpenAI — platform.openai.com → API keys |
| `design/taste-skill` | SHOPIFY_API_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/autoplan` | CODEX_API_KEY<br>SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/benchmark` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/benchmark-models` | ANTHROPIC_API_KEY<br>GOOGLE_API_KEY<br>SHORT_KEY | Anthropic — console.anthropic.com → API keys<br>Google API — console.cloud.google.com → API 与凭据<br>厂商官方 API 平台注册后生成 key |
| `gstack/browse` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/canary` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/codex` | CODEX_API_KEY<br>OPENAI_API_KEY<br>SHORT_KEY | OpenAI — platform.openai.com → API keys<br>厂商官方 API 平台注册后生成 key |
| `gstack/context-restore` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/context-save` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/design-consultation` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/design-html` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/design-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/design-shotgun` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/devex-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/diagram` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/document-generate` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/document-release` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/health` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/investigate` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/ios-clean` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/ios-design-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/ios-fix` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/ios-qa` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/ios-sync` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/land-and-deploy` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/landing-report` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/learn` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/make-pdf` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/office-hours` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/open-gstack-browser` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/pair-agent` | SHORT_KEY<br>YOUR_TOKEN | 厂商官方 API 平台注册后生成 key |
| `gstack/plan-ceo-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/plan-design-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/plan-devex-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/plan-eng-review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/plan-tune` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/qa` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/qa-only` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/retro` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/review` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/scrape` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/setup-browser-cookies` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/setup-deploy` | RENDER_API_KEY<br>SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/setup-gbrain` | SHORT_KEY<br>SUPABASE_ACCESS_TOKEN<br>YOUR_TOKEN | 厂商官方 API 平台注册后生成 key |
| `gstack/ship` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/skillify` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/spec` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/sync-gbrain` | SHORT_KEY<br>VOYAGE_API_KEY | 厂商官方 API 平台注册后生成 key |
| `gstack/test-audit` | SHORT_KEY | 厂商官方 API 平台注册后生成 key |
| `hermes-jev/jev-setup` | JEV_API_KEY | TypeSafe Jev API（jev 工具链初始化时配） |
| `media/gif-search` | TENOR_API_KEY | 厂商官方 API 平台注册后生成 key |
| `media/moneyprinterturbo` | LLM_API_KEY<br>PEXELS_API_KEY | Pexels 素材（可选）<br>至少一个 LLM provider（OpenAI/Google/Kimi） |
| `openmontage/acestep` | RUNPOD_API_KEY | 厂商官方 API 平台注册后生成 key |
| `openmontage/agents` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
| `openmontage/ai-video-gen` | FAL_KEY<br>GEMINI_API_KEY<br>GOOGLE_API_KEY<br>HEYGEN_API_KEY<br>KLING_API_KEY | Google API — console.cloud.google.com → API 与凭据<br>Google Gemini — aistudio.google.com → Get API key<br>HeyGen — platform.heygen.com → API 设置<br>fal.ai — fal.ai → Dashboards → Keys<br>厂商官方 API 平台注册后生成 key |
| `openmontage/atlas-cloud` | ATLASCLOUD_API_KEY<br>ATLAS_API_KEY | 厂商官方 API 平台注册后生成 key |
| `openmontage/avatar-video` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `openmontage/bfl-api` | BFL_API_KEY<br>YOUR_API_KEY | 厂商官方 API 平台注册后生成 key |
| `openmontage/create-video` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `openmontage/dashscope` | DASHSCOPE_API_KEY | 阿里云百炼/DashScope — bailian.console.aliyun.com → API-KEY 管理 |
| `openmontage/elevenlabs` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
| `openmontage/faceswap` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `openmontage/gemini-omni` | GEMINI_API_KEY<br>GOOGLE_API_KEY | Google API — console.cloud.google.com → API 与凭据<br>Google Gemini — aistudio.google.com → Get API key |
| `openmontage/grok-media` | XAI_API_KEY | xAI — console.x.ai → API Keys |
| `openmontage/heygen` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `openmontage/hyperframes-media` | ELEVENLABS_API_KEY<br>HEYGEN_API_KEY<br>HYPERFRAMES_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys<br>HeyGen — platform.heygen.com → API 设置<br>厂商官方 API 平台注册后生成 key |
| `openmontage/kling-official` | FAL_KEY<br>KLING_API_KEY | fal.ai — fal.ai → Dashboards → Keys<br>厂商官方 API 平台注册后生成 key |
| `openmontage/lyria` | GEMINI_API_KEY<br>GOOGLE_API_KEY | Google API — console.cloud.google.com → API 与凭据<br>Google Gemini — aistudio.google.com → Get API key |
| `openmontage/media-use` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `openmontage/motion-graphics` | GEMINI_API_KEY<br>GOOGLE_API_KEY | Google API — console.cloud.google.com → API 与凭据<br>Google Gemini — aistudio.google.com → Get API key |
| `openmontage/music` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
| `openmontage/seedance-2-0` | FAL_KEY<br>HEYGEN_API_KEY<br>HIGGSFIELD_API_KEY<br>RUNWAY_API_KEY | HeyGen — platform.heygen.com → API 设置<br>fal.ai — fal.ai → Dashboards → Keys<br>厂商官方 API 平台注册后生成 key |
| `openmontage/setup-api-key` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
| `openmontage/sound-effects` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
| `openmontage/speech-to-text` | ELEVENLABS_API_KEY | ElevenLabs — elevenlabs.io → Profile → API Keys |
| `openmontage/text-to-speech` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `openmontage/video-translate` | HEYGEN_API_KEY | HeyGen — platform.heygen.com → API 设置 |
| `productivity/airtable` | AIRTABLE_API_KEY | 厂商官方 API 平台注册后生成 key |
| `productivity/notion` | NOTION_API_KEY | 厂商官方 API 平台注册后生成 key |
| `productivity/teams-meeting-pipeline` | MSGRAPH_CLIENT_ID | 厂商官方 API 平台注册后生成 key |
| `research/last30days` | AUTH_TOKEN<br>BRAVE_API_KEY<br>EXA_API_KEY<br>LAST30DAYS_API_KEY<br>OPENAI_API_KEY<br>OPENROUTER_API_KEY<br>PARALLEL_API_KEY<br>PERPLEXITY_API_KEY<br>SCRAPECREATORS_API_KEY<br>SERPER_API_KEY<br>TRUTHSOCIAL_TOKEN<br>XAI_API_KEY<br>XQUIK_API_KEY | Exa — exa.ai → API Keys<br>OpenAI — platform.openai.com → API keys<br>Serper.dev — serper.dev → API Keys（Google 搜索代理）<br>xAI — console.x.ai → API Keys<br>厂商官方 API 平台注册后生成 key |
| `research/tradingagents` | LLM_API_KEY<br>YAHOO_FINANCE | OpenAI/Anthropic/Google 至少一个<br>yfinance 行情（无需 key） |
| `security/devcontainer-setup` | ANTHROPIC_API_KEY | Anthropic — console.anthropic.com |
| `social-media/xurl` | YOUR_CLIENT_ID | 厂商官方 API 平台注册后生成 key |
| `software-development/graphify` | ANTHROPIC_API_KEY<br>GEMINI_API_KEY<br>GOOGLE_API_KEY<br>OPENAI_API_KEY | Anthropic — console.anthropic.com → API keys<br>Google API — console.cloud.google.com → API 与凭据<br>Google Gemini — aistudio.google.com → Get API key<br>OpenAI — platform.openai.com → API keys |
| `software-development/typesafe-ai` | TYPESAFE_API_KEY | TypeSafe System One (jev 模型) API，typesafe-ai |
| `web/agent-reach` | TWITTER_AUTH_TOKEN | 厂商官方 API 平台注册后生成 key |
| `web/blocked-page-recovery` | JINA_API_KEY | Jina — jina.ai → Dashboard → API Keys（r.jina.ai 支持匿名） |
| `web/firecrawl` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
| `web/firecrawl-build` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
| `web/firecrawl-build-interact` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
| `web/firecrawl-build-onboarding` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
| `web/firecrawl-build-scrape` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
| `web/firecrawl-build-search` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |
| `web/firecrawl-developer-index` | FIRECRAWL_API_KEY | Firecrawl — firecrawl.dev 注册账号 → API Keys（有免费额度；本仓库 key 已存于 `firecrawl` CLI 凭据，无需再配） |

> 本机已配：`FIRECRAWL_API_KEY`（firecrawl CLI 凭据）、`API_KEY_21ST`（`~/.21st/api-key`）。

---

## 抓网页 / 爬虫工具选择表（本机实测可用）

> 本机装了互补爬虫工具链（Python 3.14 + Node），从"取单页"到"整站批量"到"绕 anti-bot"。按场景挑。

| 场景 | 首选工具 | 本机状态 |
|------|---------|---------|
| 单页快速取内容（喂 LLM/RAG，最轻） | 内置 `web_extract` / `agent-reach` | ✅ 零依赖 |
| 整站批量、上千 URL、并发/节流/重试 | **Scrapy** | ✅ v2.19 |
| anti-bot / Cloudflare / TLS 指纹 | **Scrapling**（impersonate/StealthyFetcher） | ✅ 0.4.15 + curl_cffi + browserforge |
| 重复 DOM 结构、少写选择器 | **AutoScraper** | ✅ 1.1 |
| Node/TS 技术栈 | **Crawlee** | ✅ tools/node-packages |
| 文档/Office/PDF → markdown | **MarkItDown** | ✅ 0.1.8 [all] |
| AI 自动开浏览器多步操作 | **browser-use** | ⚠️ 库已装 0.13，需 LLM key |
| 手机投屏/控制 Android | **scrcpy** | ✅ v5.0（tools/scrcpy） |
| TLS/HTTP2 指纹对抗（知识） | **curl-impersonate** | ⚠️ 无 Windows 二进制，用 Scrapling 替代 |

**分工**：`web_extract` 能解决就别起爬虫；整站批量用 Scrapy；被指纹/anti-bot 拦上 Scrapling；要 AI 自主操作浏览器才动用 browser-use。

## 恢复方法

```bash
git clone https://github.com/renmingweiwilliam118-alt/-AGENT-SKILL.git
cd -AGENT-SKILL && ./restore.sh
```

## 更新方法

```bash
cp -r $HERMES_HOME/skills/. ./   # 新技能复制进来
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
- `github.com/ayghri/i-have-adhd`
- `github.com/Planning-with-Files`
- `github.com/thedotmack/claude-mem`
- `github.com/outsourc-e/hermes-workspace`
- `github.com/mvanhorn/last30days-skill`
- `github.com/blader/humanizer`
- `github.com/MengTo/threeui`
- `github.com/img2threejs/img2threejs`
- `github.com/viettranx/3dviz-pro-max`
- `github.com/Panniantong/Agent-Reach`
- `github.com/firecrawl/firecrawl`
- `github.com/firecrawl/cli`
- `github.com/unclecode/crawl4ai`
- `github.com/D4Vinci/Scrapling`
- `github.com/scrapy/scrapy`
- `github.com/microsoft/markitdown`
- `github.com/alirezamika/autoscraper`
- `github.com/apify/crawlee`
- `github.com/browser-use/browser-use`
- `github.com/Genymobile/scrcpy`
- `github.com/lwthiker/curl-impersonate`
- `github.com/magicuidesign/magicui`
- `github.com/DavidHDev/react-bits`
- `github.com/uiverse-io/galaxy`
- `github.com/ruucm/shadergradient`
- `github.com/21st-dev/magic-mcp`
- `github.com/addyosmani/agent-skills`
- `github.com/trailofbits/skills`
- `github.com/anthropics/skills`
- `github.com/alirezarezvani/claude-skills`

> 注：K-Dense-AI/scientific-agent-skills（47k★，170+ 科研技能，473MB）未整库安装（过大），
> 需要时按其 `scientific-skills/` 目录单独取用。
