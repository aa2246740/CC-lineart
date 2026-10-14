---
name: cc-lineart
description: >-
  Draw SVG illustrations, project icons, AI-designed Hero landing pages,
  boutique e-commerce storefronts, tactile UI component kits, empty states,
  system architecture diagrams, editorial data visualizations, repo
  branding/badges, and animated stroke-draw presentation visuals in a
  hand-drawn ink + watercolor style (bold #141413 charcoal ink line art with
  #FAF9F5 paper-white cutout fills over mottled watercolor color blocks: clay,
  sky, cactus, heather, plum, mineral, peach, kraft, olive).
  手绘炭黑墨水线稿 + 暖白剪纸填充 + 斑驳水彩块 SVG 与网页全场景设计系统（claude.com
  杂志插画风格）。适用于：项目侧边栏图标（64×64）、AI 产品 Hero 落地页 / 主页设计、精品插画商城 /
  创作者市集页、触感 UI 组件库与空状态插画、系统架构与多智能体拓扑图、杂志感数据可视化与跑分图表、开源仓库
  Banner 与火漆徽章、一笔画自绘动效与幻灯片。当用户提到 line-art / 线稿 / 水彩 /
  Claude 官网风格插画、图标、Hero 页面、商城页面、UI 组件、架构图、数据图表，或说“给项目画个图标”、“新项目没图标”、“补图标”时触发。
---

# CC-lineart · Bilingual Agent Skill Guide / 手绘线稿与水彩全场景技能指南

**🇺🇸 English**: Hand-drawn `#141413` ink + `#FAF9F5` paper cutout + mottled watercolor SVG & Web design system for AI coding agents — scaling from **64×64 project icons** to **512×512+ full-page Hero landing pages, boutique e-commerce storefronts, tactile UI kits, empty states, architecture diagrams, benchmark charts, repo branding, and animated presentation visuals**.  
**🇨🇳 中文**：面向 AI 编程智能体的手绘墨水线稿与水彩设计系统——既能绘制 **64×64 项目与侧边栏小图标**，又能无缝扩展至 **512×512+ 的 AI 产品 Hero 落地页、精品插画商城页、触感 UI 组件库、空状态插画、系统架构图、数据可视化图表、开源品牌头图与一笔画自绘动效幻灯片**。

Copy this folder into your agent's skills directory (e.g. `~/.claude/skills/cc-lineart` or `~/.codex/skills/cc-lineart`). Needs `python3`, `rsvg-convert`, ImageMagick (`magick`), and Pillow for `lint`.  
将本目录复制到智能体的 skills 目录即可使用。依赖 `python3`、`rsvg-convert`、ImageMagick (`magick`) 与 Pillow：

```bash
apt-get install librsvg2-bin imagemagick   # or macOS: brew install librsvg imagemagick
pip install Pillow
```

---

## The Three-Layer Physical Structure / 三层物理空间法则

Every piece is built from three layers, bottom to top / 每一件作品都由自下而上的三层结构组成：

1. **Watercolor block / 偏置水彩渲染层 (`<g id="layer-block">`)**  
   - **EN**: One or two irregular quadrilaterals in brand colors (`clay`, `sky`, `cactus`, `heather`, `plum`, `mineral`, `peach`, `kraft`, `olive`), offset `10–25%` to one side of the subject, never centered. A noise filter mottles its alpha (`#wash`) and a darker rim at 55% opacity mimics pigment pooling at the edge. On larger pieces (`>= 256px`), overlap a warm wash and a cool wash with `mix-blend-mode: multiply` inside `<g id="layer-block" style="isolation: isolate">` so the intersection glazes a third tone.  
   - **ZH**：1～2 个不规则四边形品牌水彩块，中心偏离主体 `10%–25%`（切忌死板居中）。分形噪声滤镜（`#wash`）制造斑驳纸纹，55% 不透明度的深色描边模拟水彩边缘的色素沉积。在 `>= 256px` 的大画布上，将一暖一冷两块水彩以 `mix-blend-mode: multiply` 置于 `isolation: isolate` 组内叠印，交界处会自然罩染出第三色调。
2. **Paper shapes / 暖白剪纸遮罩层 (`{PAPER}` / `#FAF9F5`)**  
   - **EN**: The subject's closed outlines filled with `{PAPER}` (`#FAF9F5`). They sit on top of the wash and background construction lines, keeping **≥ 30% of the wash visible** while **≥ 20% of the line art breaks outside the wash boundary**.  
   - **ZH**：主体的闭合轮廓填充暖白纸色 `#FAF9F5`，遮挡下方的水彩与背景辅助线；同时必须保留 **≥ 30% 的水彩块外露可见**，且让 **≥ 20% 的线条破出（Break out）水彩边界**。
3. **Charcoal Ink / 手绘炭黑墨水层 (`<g id="layer-ink">`, `{INK}` / `#141413`)**  
   - **EN**: `#141413` strokes with `round` caps and joins, shallow Bezier bows (`handify`), architect corner overshoots (`--overshoot`), and a slight displacement wobble (`#ink`) so nothing is ruler-straight.  
   - **ZH**：`#141413` 圆头圆角钢笔笔触，所有直线经由 `handify` 转化为微弧曲线，转角保留建筑手稿式的出锋交叉（`--overshoot`），并叠加微弱的墨水抖动滤镜（`#ink`）。

---

## CLI Toolkit / 命令行工具速查 (`scripts/lineart.py`)

`scripts/lineart.py` holds the palette, filters, path generators (`handify`, `wobbly_circle`, `sparkle`), and size presets. Run with `python3 -I` from any directory:  
`scripts/lineart.py` 内置了品牌色板、滤镜、路径生成器与尺寸预设，可在任意目录下通过 `python3 -I` 调用：

```bash
python3 -I scripts/lineart.py list                    # List existing 64x64 motifs / 查看内置图标库
python3 -I scripts/lineart.py palette                 # Show brand watercolor hexes / 查看水彩色板
python3 -I scripts/lineart.py suggest "<keywords>"    # Rank motifs by keywords / 按关键词推荐图标
python3 -I scripts/lineart.py render <motif|draft.json> -o out.svg [--color sky] [--size lg|sm]
python3 -I scripts/lineart.py preview a.svg b.svg -o sheet.png   # Side-by-side 256px & 28px preview / 双尺寸对比预览
python3 -I scripts/lineart.py add draft.json          # Validate & save motif to library / 校验并入库新图标
python3 -I scripts/lineart.py handify "M10 10 L54 10 L54 40" [--amount 0.8] [--overshoot 2]
python3 -I scripts/lineart.py circle 32 32 12         # Hand-drawn wobbly circle path / 手绘不规则圆路径
python3 -I scripts/lineart.py sparkle 50 14 5         # Tilted unequal-arm sparkle path / 倾斜不等长星芒路径
python3 -I scripts/lineart.py lint out.svg            # Mechanical + raster style check / 运行机械与光栅双重质检
```

> **Note on `lint` / 关于 `lint` 质检器**：`lint` checks markup (primitives, ruler lines, mirror-symmetric marks, single-weight large pieces, confetti) and the raster render (wash visibility `>= 30%`, breakout `<= 80%` over wash, 28px hole survival). It requires `<g id="layer-block">` and `<g id="layer-ink">`.  
> `lint` 同时检查 SVG 源码（禁止几何原语、尺规直线、镜像对称图形、大图单一线宽、碎屑式撒点）与光栅渲染结果（水彩可见度 `>= 30%`、水彩覆盖率 `10%–50%`、线稿破出率），要求必须包含 `<g id="layer-block">` 与 `<g id="layer-ink">`。

---

## Workflow A: Draw a 64×64 Icon Motif / 工作流 A：绘制 64×64 项目图标

Read both references first / 动笔前请先阅读两份核心参考文档：
- [`references/art-direction.md`](references/art-direction.md) — 7-step drawing process, line quality rules, and 10-point critique checklist / 七步作画法、线条质量准则与十点自检清单
- [`references/drawing-guide.md`](references/drawing-guide.md) — 64 vs. 512 grid scaling, paint order, and double-stroke lettering / 网格规范、绘制先后顺序与双描边剪纸字技法

1. **Brief & Layer Plan / 一句话立意与图层规划**：Write the brief, 2–3 layout thumbnails in words, and the bottom-to-top layer plan before writing any coordinates. / 在写任何坐标前，先写出画面立意、2～3 个构图草案以及从底到顶的图层顺序（至少一个元素在主体后方、一个在主体前方）。
2. **Draft JSON / 编写图标草稿 JSON**：Fields: `name`, `description`, `tags` (English keywords for `suggest`), `color`, `block`, `ink`. Build round shapes with `circle`, straight segments with `handify`, and sparkles with `sparkle`. / 使用 `{PAPER}` 和 `{INK}` 颜色占位符，所有圆用 `circle`、直线用 `handify`、星芒用 `sparkle` 生成。
3. **Render, Lint & Preview / 渲染、质检与并排预览**：Render at `lg` and `sm`, run `lint` on the `lg` render, and `preview` both alongside two existing motifs to verify stroke weight and density. / 渲染 `lg` 与 `sm` 两个版本，对 `lg` 运行 `lint`，并与两个现有图标一起生成 `preview` 对比图。
4. **Critique & Revise / 逐项自检与迭代**：Answer the 10-point critique checklist in `references/art-direction.md` in writing, fix the weakest part, and re-render. / 书面回答十点自检清单，修正最薄弱的一处后重新渲染。
5. **Save / 入库**：Run `python3 -I scripts/lineart.py add draft.json`.

---

## Workflow B: Full-Page Web Design & 512×512+ Scenarios / 工作流 B：AI 整页网页设计与 512×512+ 全场景拓展

On larger canvases (`512×512` or `800×480`) and full HTML/CSS web pages, import `handify`, `wobbly_circle`, `sparkle`, `COLORS`, `INK`, and `PAPER` from `scripts/lineart.py`. Scale stroke widths (`8–9` primary outlines, `5.5–6.5` secondary details, `4–5` fine accents) and filter parameters (`wash` `scale=13, baseFrequency=0.011`; `ink` `scale=6.2, baseFrequency=0.013`).  
在大画布（`512×512` 或 `800×480`）及完整 HTML 网页设计中，直接从 `scripts/lineart.py` 导入路径生成函数，并使用三级线宽层次（主轮廓 `8–9`、次级细节 `5.5–6.5`、点缀线条 `4–5`）以通过 `lint` 的多线宽检查。

### 7 Expanded Scenario Reference Suites / 7 大拓展场景参考实现 (`examples/`)

1. **AI-Designed Editorial Product Hero Landing Pages / AI 产品 Hero 落地页与主页 (`examples/pages-hero/`)**
   - **EN**: Solves the "generic dark-mode SaaS template / broken stock photo" problem. Combines an editorial split Hero with a self-drawing `512×512` centerpiece (`hero-centerpiece.svg`), live watercolor palette switcher, handwritten margin annotations, a 3-card Bento feature grid with mini-illustrations and hover wash parallax, and a 2-tier pricing section with a tilted terracotta wax-seal stamp (`hero-landing-page.html`).
   - **ZH**：解决 AI 写落地页“深色紫光渐变模板感 + 缺乏主视觉插画”的痛点。提供左文右图分栏 Hero、支持一笔画回放与水彩主题实时切换的 `512×512` 主视觉（`hero-centerpiece.svg`）、手写旁注箭头、悬停水彩视差 Bento 特性网格，以及带陶土火漆印章的双档定价区（`hero-landing-page.html`）。
2. **Boutique E-Commerce & Creator Storefronts / 精品插画商城与创作者市集页 (`examples/pages-storefront/`)**
   - **EN**: Enables AI agents to design complete physical or digital goods storefronts without needing product photography. Every SKU card features a bespoke inline `CC-lineart` product illustration (ceramic pour-over dripper, field monograph, keycap set, canvas satchel, prompt deck, brass lamp) over its own watercolor wash, paired with tilted hanging price tags (`$42`, `$24`), stamp badges (`BESTSELLER`, `LIMITED`), category filter pills, and a live shopping bag drawer with a custom empty-bag illustration (`marketplace-storefront.html`).
   - **ZH**：无需真实商品摄影图即可构建高质感电商/文创市集页。每个 SKU 商品卡均配有专属手绘矢量商品插画与独立水彩底色、打孔倾斜价格吊牌（`$42`、`$24`）、印章角标（`BESTSELLER`、`LIMITED`）、分类筛选胶囊，以及清空后展示手绘空袋插画的实时购物车（`marketplace-storefront.html`）。
3. **Product UI Kits, Empty States & Interactive Web UI / 触感 UI 组件库与空状态插画 (`examples/ui-kit/`)**
   - **EN & ZH**: Zero-inbox empty-state panels (`empty-state-inbox.svg`), 5-primitive UI sticker sheets (`ui-component-sheet.svg`: `⌘K` search bar, toggle, status pill, notification card, radial gauge), and interactive HTML/CSS surfaces (`interactive-demo.html`) powered by a shared zero-size SVG `<defs>` filter bank (`#ui-wash`, `#ui-ink`) and `vector-effect="non-scaling-stroke"`.
4. **Editorial Architecture & Multi-Agent Diagrams / 系统架构与多智能体工作流图 (`examples/diagrams/`)**
   - **EN & ZH**: Multi-agent orchestration (`agent-orchestration.svg`, `800×480`) and RAG vector pipelines (`rag-pipeline.svg`, `512×512`). Uses warm + cool glazed watercolor blocks to group stages without noisy dashed bounding boxes, routes S-curve `handify` buses behind `{PAPER}` node cards, and replaces font `<text>` with miniature motifs and varied scribble bars.
5. **Editorial Data Visualization & Benchmark Infographics / 杂志感数据可视化与跑分图表 (`examples/dataviz/`)**
   - **EN & ZH**: Generational benchmark charts (`benchmark-comparison.svg`) and telemetry KPI cards (`telemetry-kpi-card.svg`). Uses a tiered `handify` hierarchy (`1.6–2.0` ticks/glyphs, `2.8–3.0` bars, `3.5` splines, `5.5` washes) to keep quantitative values accurate while passing `lint` with 0 warnings.
6. **Open-Source Repo Branding, Hero Banners & Badges / 开源仓库品牌头图与火漆徽章 (`examples/branding/`)**
   - **EN & ZH**: Release launch hero banners (`release-hero-card.svg`) and artisanal repo stamps/badges (`editorial-badges.svg`). Uses the centerline double-stroke paper cutout technique (`W + 2t` ink spines drawn before `W` paper cores) for display lettering (`v2.0`, `v2`, `✓`).
7. **Animated Stroke-Draw Line Art & Slide Deck Visuals / 一笔画自绘动效与演示幻灯片 (`examples/motion-and-slides/`)**
   - **EN & ZH**: 3-act presentation storytelling (`slide-editorial-story.svg`), animated creative desk (`animated-creative-desk.svg`), and interactive motion player (`motion-showcase.html`) using `pathLength="1"` and sequential `data-step` CSS `stroke-dashoffset` choreography.

## Notes / 注意事项

- `preview` needs `rsvg-convert` and `magick` (`brew install librsvg imagemagick`).
- These are original drawings in the style of `claude.com`'s illustrations. Do not copy Anthropic's own illustration SVGs into the library. / 本仓库所有图形均为遵循该美学规则的原创手绘矢量路径，切勿直接复制 Anthropic 官网现成的 SVG 文件。
