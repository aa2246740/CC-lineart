# Drawing & Scaling Guide / 绘图网格、大图缩放与整页设计指南 (Bilingual)

## 1. The 64×64 Icon Grid / 64×64 图标网格规范

- **🇺🇸 English**: Icons use a `64×64` `viewBox`. Keep the subject inside roughly `6..58` on both axes; strokes are `3.2` units wide at `lg` and `4.3` at `sm`, so anything finer than ~3 units between parallel lines merges at small sizes. Put the watercolor block in one quadrant-ish region with four slightly different corner offsets so it never reads as a digital rectangle, and let the subject overlap it by about half.
- **🇨🇳 中文**：图标使用 `64×64` 的 `viewBox`，主体应控制在 `6..58` 范围内；`lg` 预设线宽为 `3.2`，`sm`（侧边栏极小尺寸）预设线宽为 `4.3`，因此平行线间距不可小于 3 个单位，否则缩小时会糊成一团。水彩块四个角应带有各不相同的微小偏移（避免形成死板的数字矩形），并与主体保持约一半的偏置交叠：

```text
block   M5 18 L43 15.5 L45.5 55 L7 57 Z     (lower-left / 左下偏置水彩块)
subject window from (15,9.5) to (57.5,47.6) (upper-right / 右上主体窗口)
```

---

## 2. Making Lines Look Drawn / 用代码生成真实手绘笔触

`scripts/lineart.py` provides `handify`, `wobbly_circle` (`circle`), and `sparkle` to generate organic vector geometry / `scripts/lineart.py` 提供了三大核心路径生成函数：

- **Shallow Bezier bows / 微弧曲线替代直线 (`handify`)**: Converts straight segments into gentle cubic Beziers (`M15 9.5 C29 8.8 44 9.2 57.5 10` instead of `L57.5 9.5`), with optional architect corner overshoots (`--overshoot`). / 将生硬直线转化为带有细微弧度的三次贝塞尔曲线，并支持转角出锋（`--overshoot`）。
- **Wobbly circles with visible seam / 带接缝漂移的手绘圆 (`wobbly_circle` / `circle`)**: Radius drifts ±5% and the stroke runs `10–25°` past its start so the pen seam shows. / 半径随机漂移 ±5%，且收笔越过起笔 `10°–25°`，自然露出手绘接缝。
- **Tilted unequal-arm sparkles / 倾斜不等长星芒 (`sparkle`)**: Two crossing bowed strokes with unequal arms. / 由两笔长短不一、带倾斜角的微弧线交叉而成。
- **Claude 7-ray starburst / 7 芒非对称星辉**: 7 rays at irregular angles (`-90, -38, 8, 52, 98, 146, 196°`) with lengths varying ±15%, starting slightly away from the center. / 采用 7 个非均匀角度与 ±15% 参差长度通过三角函数计算生成，切勿画成中心对称的几何星形。

---

## 3. Paint Order Inside `<g id="layer-ink">` / 墨水层内的绘制先后顺序（画家算法）

Later SVG elements cover earlier ones, so paint order inside `<g id="layer-ink">` is critical / SVG 遵循“后画遮先画”原则，因此 `<g id="layer-ink">` 内部必须严格遵循以下顺序：

1. **Background strokes behind paper / 穿过主体背后的背景线条**：Easel legs, mug steam, orbital trajectory arcs, S-curve diagram buses, shelf brackets. / 画架后腿、杯口蒸汽、轨道虚线、架构图连接总线、货架托架等。
2. **Paper cutout shapes (`fill="{PAPER}" stroke="none"`) / 暖白剪纸闭合块（由远及近）**：Occlude the watercolor wash and background lines underneath. / 填充 `#FAF9F5` 且无描边，遮挡下方的水彩与背景线。
3. **Optional tinted interior patches / 局部水彩淡彩填充块**：E.g., a pencil eraser, status badge fill, or book spine label drawn right on top of the `{PAPER}` fill with `stroke="none"`. / 如铅笔橡皮头、书封签条、印章浅色底衬等。
4. **Primary & interior ink strokes (`fill="none"`) / 主轮廓与内部结构墨线**：Multi-weight pen strokes drawn on top of the paper shapes. / 在剪纸块上方绘制具有粗细层次的钢笔轮廓与内部细节。

---

## 4. Scaling Up (`512×512` & `800×480` Canvases) / 大尺寸画布缩放参数表

For `512×512` or `800×480` illustrations, diagrams, charts, Hero centerpieces, and storefront banners, scale parameters by ~8× from the `64` icon grid / 当绘制 `512×512` 或 `800×480` 的大图、Hero 主视觉、商城横幅、架构图或数据图表时，按以下比例放大滤镜与多级线宽参数：

| Parameter / 参数项 | `64×64` Icon Grid / 图标网格 | `512×512+` Canvas / 大画布规范 |
| :--- | :--- | :--- |
| **Primary outline `stroke-width` / 主轮廓线宽** | `3.2` (`lg`) / `4.3` (`sm`) | **`8.0 – 9.0`** |
| **Secondary detail `stroke-width` / 次级结构线宽** | `3.2` | **`5.5 – 6.5`** |
| **Fine accent `stroke-width` / 点缀与刻度线宽** | `3.2` | **`4.0 – 5.0`** |
| **Ink wobble filter (`#ink`) / 墨水抖动滤镜** | `scale="1.5"`, `baseFrequency="0.09"` | `scale="6.0–6.5"`, `baseFrequency="0.013"`, `numOctaves="2"` |
| **Watercolor wash filter (`#wash`) / 水彩置换滤镜** | `scale="2.6"`, `baseFrequency="0.08"` | `scale="12–14"`, `baseFrequency="0.011"`, `numOctaves="4"` |
| **Wash pooling rim width / 水彩积水边线宽** | `1.4` | **`4.0 – 5.0`** (`stroke-opacity="0.55"`) |

---

## 5. Scenario-Specific Engineering Recipes / 各拓展场景核心工程秘籍

### A. Centerline Double-Stroke Paper Cutout Lettering / 中心线双描边剪纸字（Branding & DataViz）
- **EN**: Never trace outlined polygon letters by hand. Instead, define each character (`v2.0`, `v2`, `✓`, `$28`) as centerline `<path>` strokes and render all `INK` spines first at width `W + 2t` (e.g. `22px`), followed by all `PAPER` (`#FAF9F5`) cores second at width `W` (e.g. `10px`). Intersecting strokes merge into a seamless paper cutout with a uniform `t` (`6px`) ink border.
- **ZH**：绘制大号手绘字标或数字时，切勿手描多边形外轮廓。应定义字符中心线路径，**第一遍先以 `W + 2t`（如 `22px`）绘制所有字符的炭黑墨骨，第二遍再以 `W`（如 `10px`）叠加所有字符的暖白纸芯**，交叉笔画会自动融合成无缝的暖白剪纸字。

### B. Tiered `handify` Hierarchy for Charts / 数据可视化的分级抖动体系（DataViz）
- **EN & ZH**: Use smaller `handify` amounts for quantitative elements (`1.6–2.0` for axis ticks & glyphs, `2.8–3.0` for data bars so heights remain accurate, `3.5` for trend splines, and `4.2–5.5` for card frames & watercolor washes). / 对刻度与数字使用极小抖动（`1.6–2.0`），对数据柱使用中等抖动（`2.8–3.0`）并微倾顶边 `1.5–2.5px` 以打破镜像对称，既保留手绘感又不失数据准确性。

### C. Full-Page Web Design: Hero Pages & Boutique Storefronts / AI 整页网页设计（Hero 落地页与精品商城）
- **Shared Filter Bank / 页面级共享 SVG 滤镜池**：Place a single `<svg width="0" height="0" style="position:absolute">` containing `<filter id="ui-wash">` and `<filter id="ui-ink">` at the top of `<body>`, and reference it across all Hero cards, Bento mini-illustrations, storefront SKU illustrations, price tags, and empty-cart graphics. / 在 HTML 顶部放置一个零尺寸 `<svg>` 统一声明 `#ui-wash` 与 `#ui-ink` 滤镜，供全页所有插画、商品卡、吊牌价签与按钮复用。
- **Hover Watercolor Parallax / 悬停水彩微视差交互**：On `.bento-card:hover .mini-wash` or `.product-card:hover .prod-wash`, apply `transform: translate(5px, -4px) scale(1.05)` so the watercolor block shifts independently behind the ink layer. / 当鼠标悬停在 Bento 特性卡或商城商品卡上时，让底层水彩块产生微小的位移与缩放，模拟多层实体纸张的物理视差。
- **Sequenced Stroke-Draw (`pathLength="1"`) / 一笔画自绘动效**：Set `pathLength="1"` and sequential `data-step` attributes on `<path>` elements so CSS `stroke-dasharray: 1; stroke-dashoffset: 1 -> 0` can animate the drawing pen-stroke by pen-stroke on page load or slide transition. / 为墨水路径添加 `pathLength="1"`，即可用纯 CSS 驱动钢笔按序落笔动画，同时完全不影响静态 PNG/PDF 导出。
