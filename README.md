# CC-lineart · 手绘线稿与水彩全场景设计系统

<p align="center">
  <strong>Bilingual Documentation / 双语文档：</strong>
  <a href="#why-cc-lineart--为什么选择-cc-lineart">🇨🇳 中文 &amp; 🇺🇸 English (Side-by-Side)</a> ·
  <a href="README.zh-CN.md">🇨🇳 纯中文完整版 (README.zh-CN.md)</a> ·
  <a href="SKILL.md">🤖 Agent Skill Entry (SKILL.md)</a>
</p>

> **🇺🇸 English**: **Hand-drawn `#141413` charcoal ink + `#FAF9F5` paper cutout + mottled watercolor SVG & Web design system for AI coding agents**, inspired by the editorial warmth of `claude.com`.  
> Originally built for `64×64` project icons, **CC-lineart** now scales across **8 core scenarios**: project icons, **AI-designed Editorial Hero landing pages**, **Boutique E-Commerce & creator storefronts**, **tactile UI component kits & empty states**, **system architecture & multi-agent diagrams**, **editorial data visualization & benchmarks**, **open-source repo branding & badges**, and **choreographed `pathLength="1"` stroke-draw animations**.
>
> **🇨🇳 中文**：**面向 AI 编程智能体的手绘 `#141413` 炭黑墨水线稿 + `#FAF9F5` 暖白剪纸填充 + 斑驳水彩块 SVG 与网页全场景设计系统**（灵感源自 `claude.com` 的人文杂志插画风格）。  
> 从最初的 `64×64` 项目小图标出发，**CC-lineart** 现已全面拓展至 **8 大核心场景**：项目与侧边栏图标、**AI 设计的 Editorial Hero 产品落地页**、**精品插画电商与创作者市集页（商城）**、**触感 UI 组件库与空状态插画**、**系统架构与多智能体工作流图**、**杂志感数据可视化与跑分图表**、**开源仓库品牌 Banner 与火漆徽章**，以及**基于 `pathLength="1"` 的一笔画自绘动效与演示幻灯片**。

<p align="center"><img src="docs/hero.png" width="840" alt="CC-lineart Hero"></p>

---

## Why CC-lineart? / 为什么选择 CC-lineart？（三层物理隐喻）

**🇺🇸 English**: Most AI-generated SVGs and web pages look like sterile templates: ruler-straight `<rect>` boxes, mirror-symmetric primitives, broken Unsplash stock-photo links, and uniform 1px borders sitting on a single flat plane.  
**🇨🇳 中文**：大多数 AI 生成的 SVG 与网页天生带有“机械模板感”：尺规般笔直的 `<rect>` 矩形、完全镜像对称的几何图元、极易裂图的外部占位照片，以及毫无层次的单平面 1px 边框。

Every `CC-lineart` artifact is constructed from **three physical layers**, bottom to top / 每一件 `CC-lineart` 作品都严格遵循自下而上的**三层物理空间结构**：

1. **Layer 1 — Offset Watercolor Block / 偏置水彩渲染层 (`<g id="layer-block">`)**  
   - **EN**: One or two irregular quadrilaterals in warm/cool brand pigments (`clay`, `sky`, `cactus`, `heather`, `plum`, `mineral`, `peach`, `kraft`, `olive`), offset `10–25%` from the subject's center. A fractal-noise filter mottles its alpha (`#wash`) and a darker rim (`stroke-opacity="0.55"`) mimics pigment pooling at the wet edge. On larger canvases (`>= 256px`), overlapping a warm wash and a cool wash with `mix-blend-mode: multiply` inside `isolation: isolate` glazes a third mid-tone.  
   - **ZH**：由 1～2 个不规则四边形构成的冷暖品牌水彩块，中心相对主体偏移 `10%–25%`（绝不死板居中）。通过分形噪声滤镜（`#wash`）营造纸张纹理的透明斑驳感，配合 `55%` 不透明度的深色描边模拟水彩边缘的色素沉积（积水边）。在大画布（`>= 256px`）上，将一暖一冷两块水彩以 `mix-blend-mode: multiply` 叠印在 `isolation: isolate` 组内，可自然罩染出第三种中间色调。
2. **Layer 2 — Paper Cutout Shapes / 暖白剪纸遮罩层 (`#FAF9F5` / `{PAPER}`)**  
   - **EN**: Closed subject silhouettes filled with warm paper-white sit on top of the wash, occluding background construction lines while allowing **≥ 30% of the watercolor block to show** and **≥ 20% of the line art to break outside the wash boundary**.  
   - **ZH**：主体的闭合轮廓填充暖白纸色 `#FAF9F5`，覆盖在水彩块与背景辅助线之上；同时严格保持 **≥ 30% 的水彩块外露可见**，并让 **≥ 20% 的墨水线条破出（Break out）水彩边界进入留白纸面**。
3. **Layer 3 — Hand-Drawn Charcoal Ink / 手绘炭黑墨水层 (`<g id="layer-ink">`, `#141413` / `{INK}`)**  
   - **EN**: Intentional pen strokes with round caps and joins, shallow Bezier bows (`handify`), architect-style corner overshoots (`--overshoot`), multi-weight stroke hierarchy, and clustered unequal-arm sparkles (`sparkle`).  
   - **ZH**：采用圆头端点与圆角连接的 `#141413` 炭黑钢笔笔触，通过微弧贝塞尔曲线（`handify`）消除尺规直线，在转角保留建筑手稿式的出锋交叉（`--overshoot`），配合多级线宽层次与聚拢的不等长星芒（`sparkle`）。

---

## Scope & 8 Core Application Scenarios / 适用范围与 8 大核心应用场景

> All 12 flagship SVGs across these scenarios pass `python3 -I scripts/lineart.py lint` with **0 warnings**.  
> 下表涵盖的全部 12 幅代表性 SVG 作品均通过 `python3 -I scripts/lineart.py lint` 机械与光栅双重审美质检（**0 警告**）。

| # | Scenario / 场景名称 | Scope & Best Used For / 适用范围与典型用途 | Key Engineering Pattern / 核心工程范式 | Directory / 目录 |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Project & Sidebar Icons**<br>项目与侧边栏图标 (`64×64`) | **EN**: IDE / T3 Code project icons, CLI toolbars, category badges (`lg` 48px+ & `sm` 14–28px presets)<br>**ZH**：IDE / T3 Code 项目图标、CLI 工具栏、分类角标（含 `lg` 大图与 `sm` 14–28px 极小尺寸预设） | Single-wash offset block + `{PAPER}` silhouette + 28px hole-survival check<br>单水彩块偏置 + 暖白剪纸轮廓 + 28px 孔洞防糊死检测 | [`motifs/`](motifs/)<br>[`scripts/lineart.py`](scripts/lineart.py) |
| **2** | **AI Hero Landing Pages**<br>AI 产品 Hero 落地页与主页 | **EN**: SaaS & developer tool launches, product homepages, Bento feature grids, editorial pricing tiers<br>**ZH**：AI / SaaS 产品发布落地页、分栏 Hero 主视觉、Bento 特性网格、带火漆印章的定价方案区 | Split Hero + self-drawing 512×512 centerpiece + live wash theme switcher + hover wash parallax<br>分栏 Hero + 一笔画自绘主视觉 + 水彩主题实时切换 + 悬停视差 | [`examples/pages-hero/`](examples/pages-hero/)<br>[`EVALUATION.md`](examples/pages-hero/EVALUATION.md) |
| **3** | **Boutique Storefronts**<br>精品插画商城与创作者市集页 | **EN**: Physical/digital goods shops, creator merch, skill/template marketplaces without stock photos<br>**ZH**：无需商品实拍图的文创周边商城、数字技能包市集、独立开发者商店页面 | Bespoke inline SVG art per SKU + tilted hanging price tags (`$42`) + stamp badges + live cart drawer<br>每件商品专属手绘 SVG + 倾斜打孔吊牌价签 + 印章角标 + 实时购物车 | [`examples/pages-storefront/`](examples/pages-storefront/)<br>[`EVALUATION.md`](examples/pages-storefront/EVALUATION.md) |
| **4** | **Tactile UI Kits & Empty States**<br>触感 UI 组件库与空状态插画 | **EN**: Zero-inbox / empty states, onboarding cards, `⌘K` search bars, toggles, toasts, interactive web UI<br>**ZH**：零收件箱/空状态页、新手引导卡、`⌘K` 搜索框、拨杆开关、通知弹窗与交互工作台 | Shared zero-size SVG `<defs>` filter bank (`#ui-wash`, `#ui-ink`) + `vector-effect="non-scaling-stroke"`<br>页面级共享 SVG 滤镜池 + 非缩放描边自适应容器 | [`examples/ui-kit/`](examples/ui-kit/)<br>[`EVALUATION.md`](examples/ui-kit/EVALUATION.md) |
| **5** | **Architecture & Agent Diagrams**<br>系统架构与多智能体工作流图 | **EN**: Engineering blog diagrams, RFC topologies, multi-agent fan-out/synthesis flows, RAG pipelines<br>**ZH**：技术博客架构图、RFC 拓扑图、多智能体分发与汇总流、RAG 向量检索流水线 | Warm + cool glazed washes as logical zones + miniature motifs replacing `<text>` + S-curve buses<br>冷暖叠色水彩划分逻辑域（替代虚线框）+ 微缩图形符号替代文字 | [`examples/diagrams/`](examples/diagrams/)<br>[`EVALUATION.md`](examples/diagrams/EVALUATION.md) |
| **6** | **Editorial DataViz & Benchmarks**<br>杂志感数据可视化与跑分图表 | **EN**: Model launch comparisons, capability velocity charts, telemetry gauges, sparkline KPI cards<br>**ZH**：模型发布跑分对比图、性能演进折线图、遥测仪表盘、微趋势 KPI 卡片 | Tiered `handify` wobble (`1.6–2.0` ticks, `2.8–3.0` bars, `3.5` splines, `5.5` washes) for data fidelity<br>分级抖动系数体系：兼顾手绘质感与数据刻度精度 | [`examples/dataviz/`](examples/dataviz/)<br>[`EVALUATION.md`](examples/dataviz/EVALUATION.md) |
| **7** | **Repo Branding & Badges**<br>开源仓库品牌 Banner 与徽章 | **EN**: GitHub README banners, OpenGraph social cards, release headers (`v2.0`), wax seals & stamps<br>**ZH**：GitHub 仓库头图、社交分享卡片、版本发布横幅（`v2.0`）、火漆印章与认证徽章 | Centerline double-stroke paper cutout lettering (`W + 2t` ink spines before `W` paper cores)<br>中心线双描边剪纸字（先画全套粗墨骨，再叠全套暖白内芯） | [`examples/branding/`](examples/branding/)<br>[`EVALUATION.md`](examples/branding/EVALUATION.md) |
| **8** | **Animated Line Art & Slides**<br>一笔画动效与演示幻灯片 | **EN**: Keynote / HTML deck hero visuals, step-by-step workflow narratives, self-drawing hero scenes<br>**ZH**：Keynote / 网页幻灯片主视觉、分步叙事插画、一笔画动态书写开场动画 | `pathLength="1"` + sequential `data-step` CSS `stroke-dashoffset` + delayed `{PAPER}` fill fade-in<br>归一化路径长度 + 按序落笔动画 + 剪纸填充延迟浮现 | [`examples/motion-and-slides/`](examples/motion-and-slides/)<br>[`EVALUATION.md`](examples/motion-and-slides/EVALUATION.md) |

---

## Visual Gallery by Scenario / 八大场景视觉画廊

### 1. Project & Sidebar Icons / 项目与侧边栏图标 (`motifs/*.json`)

- **EN**: Built-in `64×64` motif library with dual rendering presets (`--size lg` for galleries/headers and `--size sm` with enlarged wash blocks and heavier `4.3` ink for `14pt–28px` sidebar slots).
- **ZH**：内置 `64×64` 图标库，支持双尺寸预设（`--size lg` 用于展示画廊与大标题；`--size sm` 自动放大水彩块并加粗墨线至 `4.3`，专为 `14pt–28px` 极小侧边栏槽位优化）。

<p align="center"><img src="docs/icons.png" width="840" alt="CC-lineart Icon Library"></p>

---

### 2 & 3. AI-Designed Full Web Pages: Editorial Hero & Boutique Storefront / AI 整页设计：产品 Hero 落地页与精品插画商城 ([`examples/pages-hero/`](examples/pages-hero/) · [`examples/pages-storefront/`](examples/pages-storefront/))

- **EN**: Standard AI-generated landing pages and e-commerce shops fail visually because agents lack bespoke hero artwork or real product photography. `CC-lineart` lets an AI agent generate **100% self-contained, custom-illustrated web pages**:
  - **Editorial Product Hero Page ([`hero-landing-page.html`](examples/pages-hero/hero-landing-page.html))**: Split Hero with a self-drawing `512×512` centerpiece (`hero-centerpiece.svg`), interactive watercolor palette switcher, handwritten margin annotations, a 3-card Bento feature grid with hover wash parallax, and a 2-tier pricing section with a terracotta wax-seal stamp.
  - **Boutique E-Commerce Storefront ([`marketplace-storefront.html`](examples/pages-storefront/marketplace-storefront.html))**: Seasonal promo banner (`storefront-showcase.svg`), category filter pills, 6 custom-illustrated SKU cards with tilted hanging price tags (`$42`, `$24`, `$68`) and stamp badges (`BESTSELLER`, `LIMITED`), plus an interactive shopping bag drawer with an illustrated empty state.
- **ZH**：传统 AI 生成的落地页和商城页之所以显得廉价，是因为缺乏定制主视觉插画与真实的商品摄影图。借助 `CC-lineart`，AI 可以直接生成**零外部图片依赖、100% 矢量手绘的完整网页**：
  - **Editorial 产品 Hero 落地页 ([`hero-landing-page.html`](examples/pages-hero/hero-landing-page.html))**：左文右图分栏 Hero、支持一笔画回放与水彩主题实时切换的 `512×512` 主视觉（`hero-centerpiece.svg`）、手写体旁注箭头、悬停时水彩产生微视差位移的 3 卡 Bento 特性网格，以及带陶土红火漆印章的双档定价区。
  - **Boutique 精品插画商城页 ([`marketplace-storefront.html`](examples/pages-storefront/marketplace-storefront.html))**：含季节大促横幅（`storefront-showcase.svg`）、分类筛选胶囊、6 款全手绘定制 SKU 商品卡（手冲滤杯、点阵手账、机械键帽、帆布收纳包、Prompt 卡组、黄铜台灯）、倾斜打孔价格吊牌与印章角标，以及清空后自动展示手绘空袋插画的交互式购物车。

| Editorial Hero Landing Page / 产品 Hero 落地页 (`hero-landing-page.html`) | Boutique E-Commerce Storefront / 精品插画商城页 (`marketplace-storefront.html`) |
| :---: | :---: |
| <img src="examples/pages-hero/hero-landing-page-preview.png" width="410" alt="Editorial Hero Landing Page Preview"> | <img src="examples/pages-storefront/marketplace-storefront-preview.png" width="410" alt="Boutique Storefront Preview"> |
| **Hero Centerpiece / 落地页主视觉 (`hero-centerpiece.svg`)** | **Storefront Shelf & Tote / 商城陈列架主视觉 (`storefront-showcase.svg`)** |
| <img src="examples/pages-hero/hero-centerpiece.png" width="360" alt="Hero Centerpiece"> | <img src="examples/pages-storefront/storefront-showcase.png" width="360" alt="Storefront Showcase"> |

---

### 4. Tactile UI Component Kit, Empty States & Interactive Web UI / 触感 UI 组件库与空状态插画 ([`examples/ui-kit/`](examples/ui-kit/))

- **EN**: Translates `CC-lineart` into reusable product UI primitives: zero-inbox empty states (`empty-state-inbox.svg`), UI sticker sheets (`ui-component-sheet.svg` with a `⌘K` search bar, tactile toggle switch, status pill, notification card, and radial gauge), and a live HTML/CSS workbench ([`interactive-demo.html`](examples/ui-kit/interactive-demo.html)).
- **ZH**：将手绘线稿与水彩延伸为可复用的产品级 UI 原语：零收件箱空状态插画（`empty-state-inbox.svg`）、5 合 1 UI 组件贴纸页（`ui-component-sheet.svg`，含 `⌘K` 搜索框、拨杆开关、状态胶囊、通知卡片、环形仪表盘），以及可交互的 HTML/CSS 组件工作台（[`interactive-demo.html`](examples/ui-kit/interactive-demo.html)）。

| Zero-Inbox Empty State / 零收件箱空状态 (`empty-state-inbox.svg`) | 5-Primitive UI Sticker Sheet / UI 组件贴纸页 (`ui-component-sheet.svg`) |
| :---: | :---: |
| <img src="examples/ui-kit/empty-state-inbox.png" width="410" alt="Empty State Inbox"> | <img src="examples/ui-kit/ui-component-sheet.png" width="410" alt="UI Component Sheet"> |

---

### 5. Editorial Architecture & Multi-Agent Workflow Diagrams / 系统架构与多智能体工作流图 ([`examples/diagrams/`](examples/diagrams/))

- **EN**: Replaces sterile Mermaid/Graphviz boxes with warm editorial system diagrams. Overlapping watercolor washes group architectural stages without noisy bounding boxes; dashed rails and curved S-connectors pass *behind* `#FAF9F5` node cards while in-flight message capsules, magnifiers, and paper planes float *in front*.
- **ZH**：用温暖的杂志感手绘架构图替代冰冷的 Mermaid / Graphviz 方框。通过冷暖水彩自然区分系统逻辑分区（无需刺眼的虚线包围框）；S 形贝塞尔连接总线从 `#FAF9F5` 节点卡片**背后**穿过，而传输中的消息胶囊、放大镜与纸飞机则浮于卡片**前景**。

| Multi-Agent Orchestration / 多智能体编排拓扑 (`agent-orchestration.svg`) | RAG Ingestion & Vector Pipeline / RAG 检索流水线 (`rag-pipeline.svg`) |
| :---: | :---: |
| <img src="examples/diagrams/agent-orchestration.png" width="460" alt="Agent Orchestration Diagram"> | <img src="examples/diagrams/rag-pipeline.png" width="360" alt="RAG Pipeline Diagram"> |

---

### 6. Editorial Data Visualization & Benchmark Infographics / 杂志感数据可视化与跑分图表 ([`examples/dataviz/`](examples/dataviz/))

- **EN**: Uses thermal contrast (`sky` baseline wash vs. `clay` frontier wash glazed via `multiply`) to highlight generational inflection points, paired with a tiered `handify` hierarchy that keeps bar heights and gauge angles quantitatively faithful while passing `lint` with zero geometric tells.
- **ZH**：利用冷暖色温对比（`sky` 基准冷色水彩 vs. `clay` 新一代暖色水彩叠印）突出技术代际跃迁，并采用“分级抖动系数体系”（刻度 `1.6`、柱体 `2.8`、趋势曲线 `3.5`、背景水彩 `5.5`），在消除机械几何感的同时确保数据高度与仪表角度真实准确。

| Generational Benchmark Chart / 代际跑分对比图 (`benchmark-comparison.svg`) | Telemetry KPI & Sparkline Card / 遥测指标卡片 (`telemetry-kpi-card.svg`) |
| :---: | :---: |
| <img src="examples/dataviz/benchmark-comparison.png" width="410" alt="Benchmark Comparison Chart"> | <img src="examples/dataviz/telemetry-kpi-card.png" width="410" alt="Telemetry KPI Card"> |

---

### 7. Open-Source Repo Branding, Release Hero Cards & Badges / 开源仓库品牌头图与火漆徽章 ([`examples/branding/`](examples/branding/))

- **EN**: Gives developer tools and repositories an unmistakable hand-crafted identity without relying on external web fonts. Display typography (`v2.0`, `v2`, `✓`) uses the **centerline double-stroke paper cutout technique** (`W + 2t` ink spines drawn before `W` paper cores) so intersecting strokes merge into seamless paper cutouts.
- **ZH**：无需依赖外部网页字体，即可为开源仓库与开发者工具打造极具辨识度的手绘品牌视觉。大号展示字（`v2.0`、`v2`、`✓`）采用**中心线双描边剪纸技法**（先绘制全套 `W + 2t` 粗墨骨，再叠加全套 `W` 暖白纸芯），让交叉笔画自然融合成无缝的剪纸字。

| Release Launch Hero / 版本发布主视觉 (`release-hero-card.svg`) | Artisanal Repo Stamps & Badges / 手绘仓库徽章组 (`editorial-badges.svg`) |
| :---: | :---: |
| <img src="examples/branding/release-hero-card.png" width="410" alt="Release Hero Card"> | <img src="examples/branding/editorial-badges.png" width="410" alt="Editorial Badges"> |

---

### 8. Animated Stroke-Draw Line Art & Presentation Visuals / 一笔画自绘动效与演示幻灯片 ([`examples/motion-and-slides/`](examples/motion-and-slides/))

- **EN**: Because `CC-lineart` requires every `<path>` to be drawn as a single intentional movement of a pen (`references/art-direction.md`, Step 5), adding `pathLength="1"` and sequential `data-step` attributes turns any illustration into a choreographed self-drawing animation ([`motion-showcase.html`](examples/motion-and-slides/motion-showcase.html)) while remaining 100% compatible with static `rsvg-convert` PNG/PDF exports.
- **ZH**：由于 `CC-lineart` 要求每一条 `<path>` 都对应钢笔的一次真实运笔（见 `references/art-direction.md` 第 5 步），只需添加 `pathLength="1"` 与按序排列的 `data-step` 属性，即可将任意插画转化为具有书写节奏的一笔画自绘动画（[`motion-showcase.html`](examples/motion-and-slides/motion-showcase.html)），且完全兼容 `rsvg-convert` 静态高清 PNG/PDF 导出。

| 3-Act Presentation Story / 三幕式幻灯片叙事 (`slide-editorial-story.svg`) | Animated Creative Desk / 动态创意工作台 (`animated-creative-desk.svg`) |
| :---: | :---: |
| <img src="examples/motion-and-slides/slide-editorial-story.png" width="410" alt="Slide Editorial Story"> | <img src="examples/motion-and-slides/animated-creative-desk.png" width="410" alt="Animated Creative Desk"> |

---

## Install / 安装方式

Copy this repository into your coding agent's skills directory (e.g. `~/.claude/skills/cc-lineart` or `~/.codex/skills/cc-lineart`) and install the raster/lint dependencies:  
将本仓库复制到你的 AI 编程智能体技能目录（如 `~/.claude/skills/cc-lineart` 或 `~/.codex/skills/cc-lineart`），并安装渲染与质检依赖：

```bash
# Debian / Ubuntu
sudo apt-get install librsvg2-bin imagemagick && pip install Pillow

# macOS
brew install librsvg imagemagick && pip install Pillow
```

---

## CLI Commands & Workflow / 命令行工具与工作流

```bash
# 1. Inspect existing 64x64 motifs and brand palette / 查看内置图标库与品牌色板
python3 -I scripts/lineart.py list
python3 -I scripts/lineart.py palette
python3 -I scripts/lineart.py suggest "terminal agent workflow"

# 2. Render a motif at lg (>=48px) or sm (14-28px sidebar icon) / 渲染大尺寸或极小侧边栏图标
python3 -I scripts/lineart.py render mac -o out/mac.svg --size lg
python3 -I scripts/lineart.py render mac -o out/mac-sm.svg --size sm --color sky

# 3. Path-building helpers for custom drawings / 手绘路径生成辅助命令
python3 -I scripts/lineart.py handify "M10 10 L54 10 L54 40" --amount 0.8 --overshoot 2
python3 -I scripts/lineart.py circle 32 32 12
python3 -I scripts/lineart.py sparkle 50 14 5

# 4. Run mechanical + raster style lint & 256px/28px side-by-side preview / 运行风格质检与双尺寸预览
python3 -I scripts/lineart.py lint out/mac.svg
python3 -I scripts/lineart.py preview out/mac.svg motifs/terminal.svg -o out/sheet.png
```

### Reproduce All 7 Expanded Scenario Suites / 一键复现全部 7 大拓展场景示例

```bash
python3 -I examples/pages-hero/generate_hero_page.py
python3 -I examples/pages-storefront/generate_storefront.py
python3 -I examples/ui-kit/generate_ui_kit.py
python3 -I examples/diagrams/generate_diagrams.py
python3 -I examples/dataviz/generate_dataviz.py
python3 -I examples/branding/generate_branding.py
python3 -I examples/motion-and-slides/generate_motion_slides.py
```

---

## Brand Palette / 品牌水彩与纸墨色板 (`scripts/lineart.py`)

| Token / 色名 | Fill Hex / 水彩填充 | Pooling Rim / 积水边描边 | Temperature & Typical Role / 冷暖属性与典型用途 |
| :--- | :--- | :--- | :--- |
| `clay` | `#D97757` | `#B85C3E` | **Warm Terracotta / 暖陶土红** — Primary focal spot, frontier bar, or wax seal / 视觉焦点、核心高亮或火漆印章 |
| `sky` | `#6A9BCC` | `#4C7FB3` | **Cool Cerulean / 冷天青蓝** — Glazes cleanly with `clay` or `peach` via `multiply` / 与 `clay` 或 `peach` 叠印出层次 |
| `cactus` | `#BCD1CA` | `#93B0A6` | **Soft Sage Mint / 鼠尾草薄荷绿** — Verified checks, active toggles, calm zones / 验证通过、激活开关、静谧分区 |
| `heather` | `#CBCADB` | `#A4A2BF` | **Soft Lavender-Grey / 薰衣草暖灰** — Quiet secondary wash or background card zone / 柔和次级水彩或卡片底衬 |
| `plum` | `#827DBD` | `#635DA3` | **Deep Cool Violet / 深紫罗兰** — Pairs with `sky` or `peach` (avoid `multiply` with `clay`) / 适合搭配 `sky` 或 `peach` |
| `mineral` | `#629987` | `#4A7D6C` | **Deep Teal-Green / 矿物青绿** — Strong architectural or telemetry anchor wash / 架构图与遥测看板主色块 |
| `peach` | `#EBC9B7` | `#D3A58D` | **Warm Sand-Blush / 暖杏桃粉** — Glazes effortlessly over `sky`, `mineral`, or `olive` / 极佳的暖色叠印过渡层 |
| `kraft` | `#D4A27F` | `#B9845F` | **Cardboard Ochre / 牛皮纸赭石** — Tactile UI cards, shelves, and storefront tags / 商城陈列架、牛皮纸吊牌与手账 |
| `olive` | `#788C5D` | `#5D7046` | **Botanical Olive / 橄榄草木绿** — Organic storytelling and OSS status badges / 自然叙事与开源状态徽章 |
| `{PAPER}` | `#FAF9F5` | — | **Warm Paper-White / 暖白纸张色** — Sits over the wash and occludes background lines / 遮挡水彩与后景线的剪纸白 |
| `{INK}` | `#141413` | — | **Warm Charcoal Ink / 炭黑钢笔墨色** — Primary hand-drawn stroke (`round` caps & joins) / 圆头圆角的主线稿墨色 |

---

## Documentation & Art Direction References / 核心规范与评估报告索引

- [`SKILL.md`](SKILL.md) — **Agent Skill Entry Point / 智能体技能主入口** (Bilingual workflow, CLI reference & scenario index)
- [`README.zh-CN.md`](README.zh-CN.md) — **Full Chinese Documentation / 纯中文完整版说明文档**
- [`references/art-direction.md`](references/art-direction.md) — **Art Direction & Critique Checklist / 艺术指导与 10 点自检清单** (The 7-step drawing process, line quality rules, composition checks)
- [`references/drawing-guide.md`](references/drawing-guide.md) — **Drawing & Scaling Guide / 绘图网格与大图缩放指南** (`64` vs. `512` grid scaling table, paint order, double-stroke cutout lettering)
- **Scenario Evaluations & Engineering Guides / 各场景工程评估报告**:
  - [`examples/pages-hero/EVALUATION.md`](examples/pages-hero/EVALUATION.md) — Editorial Product Hero landing pages (`hero-landing-page.html`)
  - [`examples/pages-storefront/EVALUATION.md`](examples/pages-storefront/EVALUATION.md) — Boutique E-Commerce & Creator Marketplace storefronts (`marketplace-storefront.html`)
  - [`examples/ui-kit/EVALUATION.md`](examples/ui-kit/EVALUATION.md) — Tactile UI components, empty states & interactive DOM + SVG filter choreography
  - [`examples/diagrams/EVALUATION.md`](examples/diagrams/EVALUATION.md) — Editorial architecture & multi-agent workflow diagrams
  - [`examples/dataviz/EVALUATION.md`](examples/dataviz/EVALUATION.md) — Editorial data visualization & tiered `handify` accuracy
  - [`examples/branding/EVALUATION.md`](examples/branding/EVALUATION.md) — Repo branding, OpenGraph/hero banners & double-stroke cutout typography
  - [`examples/motion-and-slides/EVALUATION.md`](examples/motion-and-slides/EVALUATION.md) — Sequenced `pathLength="1"` stroke-draw animation & presentation decks

## License / 开源协议

MIT
