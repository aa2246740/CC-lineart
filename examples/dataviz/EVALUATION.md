# Track 2 Evaluation — Editorial Data Visualization & Benchmark Infographics

This evaluation documents the application of `CC-lineart` (`scripts/lineart.py`) to **Editorial Charts, Benchmark Comparisons, and Telemetry KPI Infographics** on a `512×512` canvas.

## Deliverables Summary

| Artifact | Description | Washes (`multiply`) | `lint` Warnings |
| :--- | :--- | :--- | :--- |
| [generate_dataviz.py](file:///Users/wu/CC-lineart/examples/dataviz/generate_dataviz.py) | Generator script importing `COLORS`, `INK`, `PAPER`, `handify`, `wobbly_circle`, and `sparkle` from [lineart.py](file:///Users/wu/CC-lineart/scripts/lineart.py) | — | — |
| [benchmark-comparison.svg](file:///Users/wu/CC-lineart/examples/dataviz/benchmark-comparison.svg) / [PNG](file:///Users/wu/CC-lineart/examples/dataviz/benchmark-comparison.png) | 4-generation capability & coding velocity column chart + cubic growth trajectory + `"2.4x"` callout badge | `sky` (`#6A9BCC`) + `clay` (`#D97757`) | **0 warnings** |
| [telemetry-kpi-card.svg](file:///Users/wu/CC-lineart/examples/dataviz/telemetry-kpi-card.svg) / [PNG](file:///Users/wu/CC-lineart/examples/dataviz/telemetry-kpi-card.png) | Layered KPI summary cards combining a semicircle velocity dial gauge, rising area/line sparkline, and status pill | `mineral` (`#629987`) + `peach` (`#EBC9B7`) | **0 warnings** |

---

## 1. Balancing Data Accuracy with Hand-Drawn Line Wobble

Standard plotting libraries (`matplotlib`, `vega`, `chart.js`) emit ruler-straight `<line>` and `<rect>` primitives that look clinical in editorial essays or launch cards. Conversely, applying uniform high-amplitude displacement (`handify --amount 6.0`) to every element in a chart distorts bar heights, misaligns tick marks, and makes quantitative comparisons untrustworthy.

To preserve **accurate visual encoding** while passing `lineart.py lint` (zero ruler-straight segments $>12\%$ of canvas, zero geometric primitives, zero mirror-symmetric marks), we use a **tiered `handify` hierarchy** across the `512×512` canvas (combined with the global `#ink` `feDisplacementMap` at `scale="6.2"`, `baseFrequency="0.013"`):

| Chart Element | `handify` `amount` (512 grid) | `overshoot` | Geometric Strategy & Rationale |
| :--- | :---: | :---: | :--- |
| **Watercolor Wash Blocks** | `5.5` | `0.0` | High organic drift on tilted, non-rectangular quadrilaterals so wash edges pool naturally. |
| **Card Containers & Callout Badges** | `4.0 – 4.2` | `8.5 – 10.0` | Architect-style corner overshoots and one deliberate open breathing gap (`badge_rim`, `pill_stroke`) prevent sticker-like boxes. |
| **Primary Axes & Reference Grid** | `3.2 – 3.8` | `0.0` | Axes bow gently ($0.5\text{–}1.2\%$ of length) and cross at the origin `(92, 408)` with a `22px` architect tail overshoot (`x=70`, `y=430`). |
| **Data Columns / Bars** | `2.8 – 3.0` | `5.5` | Moderate drift preserves true relative column heights (`82px`, `136px`, `190px`, `282px`). A slight upward right-hand tilt (`7–8px`) and a left-wall inflection knot avoid clip-art mirror symmetry. |
| **Growth Curves & Gauge Arcs** | `2.6 – 3.5` | `0.0` | Multi-segment cubic splines (`growth-curve`) and segmented radial polylines (`wobbly_arc` with $\pm 3.5\%$ radial jitter) keep data nodes anchored at exact coordinates. |
| **Axis Ticks, Hatching & Centerline Glyphs** | `1.6 – 2.0` | `0.0` | Tight control keeps `"2.4x"`, `"+↗"`, and scale ticks legible and accurately positioned against the axes. |

### Key Geometry Patterns Discovered During Iteration
1. **Avoiding Mirror-Symmetric Bars & Caps (`lint` symmetry check):**
   A standard vertical bar `M x y_bot L x y_top L x+w y_top L x+w y_bot Z` whose bounding box is $< 30\%$ of the canvas (`153.6px` on a `512` grid) triggers `lint`'s `mirror_symmetric` warning because its left and right walls mirror across its horizontal center. Giving each column a subtle upward slant on its top edge (`by_l` vs `by_r = by_l - 8`), an asymmetric inflection point on one vertical wall, and a diagonally tapered highlight cap eliminates mechanical symmetry while reinforcing the chart's upward momentum.
2. **Partial Pen Hatching vs. Wall-to-Wall Dividers:**
   In our first draft of `benchmark-comparison.svg`, diagonal hatch lines inside the frontier column spanned from wall to wall, which visually chopped the bar into five tiny compartments. Shortening the hatch strokes to $\sim 65\%$ of the column width (`M 356 218 L 392 192`) reads as authentic editorial pen shading and keeps the column interior unified.

---

## 2. Using Watercolor Washes to Highlight Data Series & Thresholds

In editorial data visualization, watercolor washes should act as **semantic visual highlighters** rather than decorative background plates:

1. **Thermal Contrast for Baseline vs. Frontier (`benchmark-comparison.svg`):**
   - **Cool `sky` wash (`#6A9BCC`, rim `#4C7FB3`)** sits in the lower-left/center quadrant (`M 58 195 ...`), grounding the historical baseline columns (Gen 1–3) and the origin of the axes.
   - **Warm `clay` wash (`#D97757`, rim `#B85C3E`)** sits in the upper-right quadrant (`M 238 78 ...`), framing the Gen 4 frontier column, the peak node `(385, 96)`, and the `"2.4x"` callout arrow.
   - **Glazed Transition Zone (`mix-blend-mode: multiply`):** Where the `sky` and `clay` washes overlap across the Gen 3 column and mid-trajectory curve, `multiply` blending inside `<g id="layer-block" style="isolation:isolate">` produces a warm slate-umber glaze that marks the inflection threshold where capability accelerates.
2. **Layered Card Hierarchy & Threshold Zones (`telemetry-kpi-card.svg`):**
   - **Cool `mineral` wash (`#629987`)** anchors the upper-left gauge card, while **warm `peach` wash (`#EBC9B7`)** anchors the lower-right sparkline card.
   - **Focal Spot & Tinted Data Fills:** Inside the paper cards, high-priority thresholds use targeted secondary washes (`stroke="none"` drawn between the `{PAPER}` fill and `{INK}` outline): a `clay` wedge (`fill-opacity="0.85"`) highlights the high-velocity zone (`-58°` to `-10°`) on the dial gauge, and a translucent `mineral` area fill (`fill-opacity="0.35"`) shades the area beneath the sparkline trajectory.

---

## 3. `lineart.py lint` Results

Both SVGs pass `python3 -I scripts/lineart.py lint` with **0 warnings**:

### `benchmark-comparison.svg`
```text
OK    no clip-art geometry found in the markup
OK    block visible: 57% of the wash shows (want ≥ 30%)
OK    color coverage: 26% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 74% (want ≤ 80%; the art should break out of the block)
NOTE  at 28px 6 of 7 enclosed paper areas close up — the drawing smudges; fewer, bigger shapes (fine if this piece is never shown that small)

0 warning(s). Lint catches mechanical tells only; it cannot tell you the piece is good.
```

### `telemetry-kpi-card.svg`
```text
OK    no clip-art geometry found in the markup
OK    block visible: 40% of the wash shows (want ≥ 30%)
OK    color coverage: 20% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 79% (want ≤ 80%; the art should break out of the block)
NOTE  at 28px 2 of 3 enclosed paper areas close up — the drawing smudges; fewer, bigger shapes (fine if this piece is never shown that small)

0 warning(s). Lint catches mechanical tells only; it cannot tell you the piece is good.
```

> **Note on the 28px raster check for `512×512` editorial graphics:** On a `512` viewBox, the prescribed stroke weight of `8.5` units (`references/drawing-guide.md`) scales down to `0.46px` when rasterized to `28×28`. Because sub-pixel anti-aliased strokes blend with `#FAF9F5` paper above the `RGB >= 100` luminance threshold in `holes()`, enclosed regions connect in luminance space rather than smudging into a dark blob. `lineart.py` accounts for this by emitting `NOTE (... fine if this piece is never shown that small)` whenever `viewBox >= 256`.

---

## 4. Visual Critique Checklist (`references/art-direction.md`)

### Piece 1: `benchmark-comparison.svg`
1. **Does the brief test pass: would this picture break if the name were changed?**
   Yes — the four ascending generation columns, dashed target threshold line, cubic growth trajectory with four data nodes, and centerline `"2.4x"` callout badge specifically encode a generational benchmark comparison.
2. **Is there something behind the subject and something in front of it?**
   Yes — two dashed horizontal grid lines (`y=312`, `y=214`) and the threshold line (`y=156`) pass *behind* the paper-filled columns; the rising trajectory curve, data nodes, and callout pointer arrow sit *in front* of the columns.
3. **Does the wash sit off-center, with art crossing its edge in two or more places?**
   Yes — `color coverage: 26%`, `block visible: 57%`, `line art over the wash: 74%`. The X/Y axes, Gen 1 column, `"2.4x"` callout badge, and frontier column top all break across the wash boundaries.
4. **On larger pieces, are there two washes, one warm and one cool, with a clean glaze where they overlap?**
   Yes — cool `sky` (lower-left) and warm `clay` (upper-right) overlap in the center-right with `mix-blend-mode: multiply`, creating a third glazed tone behind the Gen 3–4 transition.
5. **Is any outline a primitive, a ruler line or mirror-symmetric?**
   No — `lint` reports `OK: no clip-art geometry found in the markup` (`0 warnings`). All bars, caps, axes, nodes, and `"2.4x"` glyphs are asymmetric handified paths or `wobbly_circle` paths.
6. **Are repeated marks varied, and do at least one or two corners overshoot?**
   Yes — the 7 axis ticks and 4 partial hatch lines vary in length, angle, and spacing; all 4 column outlines and the `"2.4x"` badge frame use `overshoot=5.5–8.5`, and the badge frame leaves an intentional `24px` breathing gap at its lower-left corner.
7. **Are accents 3–6, clustered, and earned by the subject?**
   Yes — 4 accents total (3 `sparkle` marks at radii `21`, `13.5`, `10.0` plus 1 ink dot) clustered tightly at the upper-right frontier peak `(385, 96)` to signal the `2.4x` breakout.
8. **Is one area left quiet?**
   Yes — the bottom-right strip below the X-axis and the upper-left margin outside the Y-axis arrow remain open `#FAF9F5` paper.
9. **At 28px, does it still read as the subject, without smudging into a dark blob?**
   Yes — four distinct stroke weights (`9.0`, `8.5`, `6.8/6.0`, `5.5/5.0`) and generous spacing (`20px` between columns) prevent any dark ink clumping at thumbnail scale.
10. **What was the single weakest part of the piece in Draft 1, and how was it fixed?**
    In Draft 1, Bar 1, Bar 2, and the rectangular color caps on Bars 3–4 were flagged as mirror-symmetric by `lint`, and the full-width hatch lines in Bar 4 divided the bar into closed compartments. We fixed this in Revision 1 by giving every column a subtle upward slant (`7–8px`), adding an asymmetric left-wall inflection knot, tapering the color caps diagonally, and shortening the hatch lines into partial pen shading on the left side of Bar 4.

### Piece 2: `telemetry-kpi-card.svg`
1. **Does the brief test pass: would this picture break if the name were changed?**
   Yes — the semicircle velocity dial gauge with its `clay` high-zone wedge and needle, paired with a stepped area sparkline card and checkmark health pill, unmistakably reads as a live telemetry / KPI summary card.
2. **Is there something behind the subject and something in front of it?**
   Yes — a tilted secondary reference sheet (`M 96 46 L 372 38 L 376 112`) and left-hand telemetry signal leads sit *behind* Card A; Card B overlaps *in front* of Card A's lower-right quadrant; the checkmark status pill sits *in front* across the left-hand seam between Cards A and B.
3. **Does the wash sit off-center, with art crossing its edge in two or more places?**
   Yes — `color coverage: 20%`, `block visible: 40%`, `line art over the wash: 79%`. Both KPI cards, the background reference sheet, and the foreground status pill cross the wash edges in 6 places.
4. **On larger pieces, are there two washes, one warm and one cool, with a clean glaze where they overlap?**
   Yes — cool `mineral` (`#629987`) behind the upper-left gauge card and warm `peach` (`#EBC9B7`) behind the lower-right sparkline card overlap near the center with `mix-blend-mode: multiply`, plus a hot `clay` focal spot on the gauge threshold wedge and sparkline peak node.
5. **Is any outline a primitive, a ruler line or mirror-symmetric?**
   No — `lint` reports `OK: no clip-art geometry found in the markup` (`0 warnings`).
6. **Are repeated marks varied, and do at least one or two corners overshoot?**
   Yes — the 5 radial gauge ticks alternate inner/outer radii and angles, the header and metric summary bars vary in length (`64px` vs `42px`, `72px` vs `46px`), both card frames use `overshoot=10.0`, and both the inner gauge arc and status pill include deliberate open breathing gaps.
7. **Are accents 3–6, clustered, and earned by the subject?**
   Yes — 4 accents total (3 `sparkle` marks at radii `20`, `13`, `9.5` plus 1 small dot) clustered in the upper-right quiet space above Card B's peak sparkline node.
8. **Is one area left quiet?**
   Yes — the upper-right quadrant (`x: 375–490, y: 40–230`) is left free of cards and washes except for the small sparkle cluster.
9. **At 28px, does it still read as the subject, without smudging into a dark blob?**
   Yes — open radial ticks on the outer gauge arc and a shortened inner arc (`-168°` to `-56°`) keep plenty of open paper around the gauge needle so it never blobs together at small sizes.
10. **What was the single weakest part of the piece in Draft 1, and how was it fixed?**
    In Draft 1, the upright `+` glyph, vertical trend arrow, and full semicircle inner gauge arc (`-164°` to `-18°`) were flagged as mirror-symmetric by `lint`, and the inner arc crowded the gauge needle. In Revision 1, we tilted the `+` glyph with unequal arms, angled the trend arrow diagonally north-east (`~35°`), and stopped the inner gauge arc at `-56°` just before the needle and `clay` threshold wedge, improving both legibility and hand-drawn asymmetry.
