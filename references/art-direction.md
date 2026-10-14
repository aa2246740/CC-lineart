# Art Direction / 艺术指导与审美准则 (Bilingual)

**🇺🇸 English**: The drawing guide (`references/drawing-guide.md`) says *how* to put marks on the canvas. This file says *which* marks to make. Two agents using the same palette, filters, and helpers can still produce one picture that feels drawn by a human illustrator and one that feels like sterile clip-art; the difference is made of the decisions below, and every one of them can be checked.  
**🇨🇳 中文**：《绘图指南》（`references/drawing-guide.md`）规定了**如何**把线条画上画布，而本文档规定了**应该画什么样的线条与构图**。即便两个智能体使用完全相同的色板、滤镜和辅助脚本，画出来的作品也可能一个是充满人文温度的手绘插画，另一个却是冰冷的机械剪贴画（Clip-art）。决定二者高下的正是以下可被量化检验的审美决策。

---

## The 7-Step Process / 七步作画流程

Do these in order. Skipping steps 1–3 is the most common reason a piece comes out flat.  
请严格按顺序执行以下 7 步。跳过第 1～3 步直接写坐标，是导致画面呆板扁平的最常见原因。

1. **Brief, in one sentence / 一句话立意（专属性测试）**  
   - **EN**: What is the piece about, and which one or two elements does it take from the subject's identity? Test: swap in a different product/concept name. If the picture still works unchanged, it says nothing specific about this subject. Pick a different idea.  
   - **ZH**：这幅画要表达什么？它提取了主体最具代表性的哪 1～2 个视觉特征？**自测法则**：把产品名换成另一个毫不相关的名字，如果画面依然完全通用，说明这幅画空洞无物，请推翻重想。
2. **Thumbnails, in words / 文字构图小样（2～3 个方案）**  
   - **EN**: Before any coordinates, write two or three layouts as short text: where each wash sits (which quadrant, how big), where the subject sits, what overlaps what, and which area stays empty. Choose one and say why in one line.  
   - **ZH**：在动笔写任何坐标前，先用文字写出 2～3 个构图草案：水彩块落在哪个象限、主体偏左还是偏右、前后叠压关系如何、哪个角落留白呼吸，并说明最终选定方案的理由。
3. **Layer plan / 前后景图层规划（拒绝单平面贴纸感）**  
   - **EN**: List every element bottom to top: washes, strokes that pass behind paper, paper shapes back to front, details on top, accents. At least one element must sit *behind* the subject and one *in front* of it. A piece where everything shares one plane reads as a sticker.  
   - **ZH**：自下而上列出所有元素：水彩渲染层 → 从主体背后穿过的背景线条 → 由远及近的暖白剪纸主体 → 纸面内部细节 → 星芒点缀。**必须至少有一个元素穿插在主体背后、一个元素叠在主体前方**，否则画面会像一张平平无奇的贴纸。
4. **Big shapes first / 先铺大色块与主剪纸轮廓**  
   - **EN**: Draw only the washes and the main paper shapes. Render at full size and at thumbnail size and judge the composition now, while moving things is cheap. No details yet.  
   - **ZH**：先只画水彩块与主要的 `{PAPER}` 剪纸轮廓，渲染大图与缩略图审视构图平衡，此时调整位置成本最低，切勿过早陷入细节。
5. **Ink, one pen stroke at a time / 钢笔运笔：一笔一路径**  
   - **EN**: Each `<path>` is one movement of a pen: it has a start, a direction, and an end where the round cap shows. Draw an outline the way a hand would draw it, in two or three strokes that meet or slightly overshoot, not as a closed polygon traced around the shape. Letters and bars are centerline strokes (the double-stroke technique in the drawing guide), never outlined polygons.  
   - **ZH**：每一条 `<path>` 都代表钢笔在纸上的一次真实运笔（有起笔、行笔方向与圆头收笔）。主轮廓应拆成 2～3 笔相交或略微出锋（Overshoot）的线条，而不是生硬闭合的多边形。字母与粗柱体采用“中心线双描边剪纸法”绘制（详见《绘图指南》）。
6. **Accents last, and few / 最后克制地添加星芒点缀**（遵循下方点缀法则）。
7. **Render, write the critique, revise / 渲染、书面十点自检与至少一轮迭代**  
   - **EN**: Run `lint`, look at the render, and answer the 10-point checklist at the end of this file *in writing*. Fix what fails and render again. A first draft is never the deliverable.  
   - **ZH**：运行 `lint` 并查看渲染结果，逐条书面回答文末的《十点审美自检清单》，找出并修复最薄弱的一处后重新渲染。**初稿绝不能直接作为最终交付物。**

---

## Line Quality / 线条的手绘质感准则

A hand-drawn line is imperfect in specific ways. Put them into the path data on purpose; the wobble filter only adds tremor on top and cannot rescue a geometric path.  
手绘线条有着特定的“不完美性”。必须在路径坐标层面主动构建这些特征；SVG 抖动滤镜只能增加微弱的边缘震颤，无法拯救一条死板的几何路径。

- **No primitives for visible outlines / 禁止在可见轮廓中使用几何原语**：In the ink layer, `<circle>`, `<ellipse>`, and `<rect>` are allowed only for tiny dots and fills smaller than ~12% of the canvas. Larger round shapes must come from `lineart.py circle` (`wobbly_circle`); larger boxes must come from `handify`. / 在墨水层中，`<circle>`、`<ellipse>`、`<rect>` 仅限用于小于画布 `12%` 的小圆点或纯填充块。大圆必须使用 `wobbly_circle`（半径漂移 ±5% 且起收笔交叠），大矩形必须使用 `handify`。
- **No ruler lines / 禁止尺规直线**：Any horizontal or vertical segment longer than 12% of the canvas must bow by `0.5–1.5%` of its length (`M15 9.5 C29 8.8 44 9.2 57.5 10`, not `L57.5 9.5`). `handify` does this automatically. / 任何长度超过画布 `12%` 的水平或垂直线段都必须带有 `0.5%–1.5%` 的微弧度（由 `handify` 自动完成）。
- **Corners are where two strokes meet / 转角出锋（建筑手稿感）**：On boxes, frames, cards, and shelves, let one or two corners overshoot by `1–3` units on a 64 grid (`8–20` on a 512 grid), like an architect's sketch (`handify --overshoot`). / 在卡片、画框、书本、货架等转角处，让 1～2 个角略微出锋 `1–3` 单位（512 画布上为 `8–20` 单位），展现建筑师手稿般的潇洒笔意。
- **Repeats are never copies / 重复元素绝不复制粘贴**：Text lines, steam, rays, binding rings, sparkles, bar series: vary each one's length by `10–20%`, its spacing, and its angle by a few degrees. / 文本排线、蒸汽、光芒、装订环、星芒：每一根的长度必须有 `10%–20%` 的参差变化，间距与角度也应略有不同。五根一模一样的平行线看起来像印刷字体，而不是手绘。
- **Asymmetry / 打破镜像对称**：Nothing larger than a dot (`3%–30%` of canvas) may be mirror-symmetric. Skew one side, make one arm longer, or tilt the axis `5–15°`. Perfect symmetry is the #1 clip-art tell caught by `lint`. / 任何大于圆点的独立图形（画布尺寸的 `3%–30%`）都不得左右镜像对称。请将器皿、卡片、吊牌或手柄倾斜 `5°–15°` 或做非对称梯形偏斜。
- **Multi-weight hierarchy in larger pieces / 大画布（`>=256px`）必须具备多级线宽层次**：Use 2–3 explicit `stroke-width` tiers on `<path>` elements: primary outlines heaviest (`8.0–9.0` on 512), interior details ~70% (`5.5–6.5`), fine accents ~55% (`4.0–5.0`). / 在 `>= 256px` 的插画、图表、Hero 主视觉或商城组件中，必须在 `<path>` 上显式使用 2～3 级线宽（主轮廓最粗、内部结构约 70%、辅助虚线与星芒约 55%）。
- **Breathing gaps / 留白气口**：Let a stroke stop just short of closing in one place per piece so the drawing breathes. / 每幅作品中可在一处衔接点留出微小气口（笔断意连），让画面更有呼吸感。

---

## Composition / 构图与水彩法则

- **The wash is offset, not a background plate / 水彩块偏置而非背景底板**：Wash center sits `10–25%` away from the subject's center. Total wash coverage stays between **10% and 50%** of the canvas (`lint` checks this). / 水彩中心必须偏离主体中心 `10%–25%`，水彩占画布总面积严格控制在 **10%–50%** 之间（超过 50% 会沦为死板的背景底板）。
- **The art breaks out / 线稿破出边界（核心签名特征）**：At least **20%** of the line art must lie outside the wash (`line art over the wash <= 80%`), crossing the wash edge in at least two places. / 至少 **20%** 的墨水线条必须延伸到水彩块之外的白纸区域（即位于水彩块内的线稿比例 `<= 80%`），且在至少两处跨越水彩边缘。
- **The block shows / 水彩透出率 `>= 30%`**：At least **30%** of the watercolor wash must remain visible after `{PAPER}` shapes cover it, otherwise the piece turns grey. / 暖白剪纸覆盖后，仍需有 **≥ 30%** 的水彩面积直接外露可见，否则整幅画会显得灰暗苍白。
- **Two glazed washes on larger pieces / 大画布冷暖双色水彩罩染**：Overlap a warm wash (`clay`, `peach`, `kraft`) and a cool wash (`sky`, `cactus`, `heather`, `mineral`) with `mix-blend-mode: multiply` inside `isolation: isolate` so their intersection glazes a third mid-tone. Avoid pairs that mix to mud (`clay` over `plum` or `olive`). / 在大尺寸作品中，使用一暖一冷两块水彩通过 `multiply` 正片叠底交叠出第三色调，切忌全图只涂单一平涂色块，也避免用 `clay` 与 `plum`/`olive` 正片叠底混出脏褐色。
- **Quiet space / 留白象限**：Leave one quadrant mostly empty (except for a small sparkle cluster). Empty paper is part of the art. / 保持一个象限基本留白（仅放置一小簇星芒），留白本身就是纸本插画的一部分。

---

## Accents / 星芒与点缀法则

- **3–6 in total, clustered / 总数控制在 3～6 个且聚拢分布**：One cluster of three sparkles (big : medium : small ≈ `1 : 0.6 : 0.4`) plus two dots in the quiet area, and at most one small echo elsewhere. Never place one in each corner (`lint` flags `> 7` tiny marks as confetti). / 在留白区放置一簇 3 颗大中小不等的星芒（比例约 `1 : 0.6 : 0.4`）加 2 个小圆点，其他位置最多呼应 1 颗。切忌四角平均撒点（超过 7 个微小标记会被 `lint` 判定为碎屑感警告）。
- **Always use `lineart.py sparkle` / 必须使用 `sparkle` 生成**：Two crossing strokes with unequal arms, tilted and slightly bowed — never geometric diamond stars or equal-arm `+` signs. / 使用两笔不等长、带倾斜与微弧的交叉线绘制星芒，严禁画几何菱形四角星或等臂十字 `+`。

---

## 10-Point Critique Checklist / 十点审美自检清单

Answer every question in writing after each render with concrete evidence (`lint` metrics or visual observation):  
每次渲染后请结合 `lint` 指标与视觉观察逐条书面自检：

1. **Brief specificity / 专属性测试**：Would this picture break if the product/concept name were swapped? / 换个名字这幅画还能通用吗？（不能通用才合格）
2. **Depth planes / 前后景穿插**：Is there at least one element *behind* the subject and one *in front* of it? / 主体背后与前方是否都有穿插元素？
3. **Wash balance / 水彩比例与破界**：Is the wash offset, with `coverage 10–50%`, `block visible >= 30%`, and `line art over wash <= 80%`? / 水彩是否偏置且完全满足 `lint` 三项核心覆盖率指标？
4. **Glazed color / 冷暖叠色**：On larger pieces (`>= 256px`), do warm and cool washes overlap cleanly via `multiply`? / 大画布是否有一暖一冷两块水彩自然罩染？
5. **Zero clip-art geometry / 零机械几何感**：Are there 0 primitives, 0 ruler lines, and 0 mirror-symmetric shapes in `lint`? / `lint` 源码检查是否做到 0 几何原语、0 尺规直线、0 镜像对称？
6. **Varied repeats & overshoots / 参差重复与转角出锋**：Are repeated lines varied by 10–20%, and do 1–2 corners overshoot? / 重复线条是否有长短参差，转角是否有建筑手稿式出锋？
7. **Earned, clustered accents / 克制聚拢的点缀**：Are accents 3–6 in total and clustered in the quiet area? / 点缀是否控制在 3～6 个且聚拢在留白区？
8. **Quiet quadrant / 呼吸留白**：Is one quadrant left intentionally quiet? / 是否留出了呼吸感留白象限？
9. **Small-size legibility / 缩略图清晰度**：For icons, do enclosed paper areas survive at 28px without smudging? / 对于图标，缩略至 28px 时内部暖白孔洞是否依然清晰不糊死？
10. **Single weakest point / 当前最薄弱处**：What is the single weakest part right now? Name it, fix it, and re-render. / 指出当前最薄弱的一处细节，动手改掉并重新渲染。
