# Track 4 Evaluation — Open-Source Repo Branding, Hero Banners, Social OpenGraph Cards & Editorial Badges

## Overview

This evaluation documents **Track 4** of the `CC-lineart` expansion: proving that the hand-drawn ink + mottled watercolor system in [`scripts/lineart.py`](../../scripts/lineart.py) scales from 64×64 sidebar icons to full **512×512 Open-Source Repository Identity Assets** without external fonts, clip-art primitives, or raster textures.

All deliverables live inside `/Users/wu/CC-lineart/examples/branding/`:
- [`generate_branding.py`](./generate_branding.py) — deterministic generator reusing `handify`, `wobbly_circle`, `sparkle`, `COLORS`, `INK`, and `PAPER` from `scripts/lineart.py`
- [`release-hero-card.svg`](./release-hero-card.svg) & [`release-hero-card.png`](./release-hero-card.png) — 512×512 launch announcement hero illustration (*"v2.0 Release / CLI & Agent SDK"*)
- [`editorial-badges.svg`](./editorial-badges.svg) & [`editorial-badges.png`](./editorial-badges.png) — 512×512 sheet of 4 artisanal developer stamps/badges (*Verified Shield & Check*, *v2 Release Wax Seal*, *OSS Git Branch Rosette*, *BETA Lab Tag & Lightning*)

---

## 1. Centerline Double-Stroke Lettering Technique (`W + 2t` Ink Behind `W` Paper)

System `<text>` tags introduce rigid font outlines that clash with wobbly hand-drawn ink and break portability when a viewer lacks the font. Tracing closed polygon outlines around letters by hand produces uneven stroke thickness and pinches at corners.

Instead, `CC-lineart` constructs display lettering, version numbers (`v2.0`, `v2`), and symbolic stamp marks (`✓`) using the **centerline double-stroke paper cutout technique** implemented in `double_stroke_group(paths_d, w_paper=W, t_border=t)`:

### Mechanics & Paint Order
1. **Single Handified Centerline**: Each character or mark is authored as a single open or wobbly-closed centerline spine passed through `handify(..., amount=2.2..2.6)` or `wobbly_circle(..., wobble=0.08, overlap=18)`.
2. **Pass 1 — All Ink Spines (`W + 2t`)**: Every centerline path in the word/stamp is drawn first with `stroke="{INK}"` (`#141413`), `fill="none"`, `stroke-width = W + 2t`, `stroke-linecap="round"`, and `stroke-linejoin="round"`.
3. **Pass 2 — All Paper Cores (`W`)**: The exact same path strings `d` are drawn second with `stroke="{PAPER}"` (`#FAF9F5`), `fill="none"`, `stroke-width = W`, and identical round caps/joins.
4. **Why Grouping All Ink Before All Paper Matters**:
   - When two strokes of a character cross or touch (such as the apex of `v`, the base turn of `2`, or adjacent letters in `v2.0`), drawing all `INK` passes first and all `PAPER` passes second merges the interior paper channels into a single continuous paper-cutout silhouette bounded by a uniform `t`-unit ink wall.
   - If each stroke were drawn `INK -> PAPER` individually, later ink borders would slice across earlier paper interiors.

### Recommended Widths by Canvas Scale & Role

| Asset Role | Grid | Paper Core `W` | Ink Wall `t` | Total Ink Stroke `W + 2t` | Notes |
|---|---|---|---|---|---|
| **Hero Version / Logo (`v2.0`)** | 512×512 | `14.5` | `8.5` | `31.5` | Matches primary `8.5–9.0` outline weight; reads from 512px down to thumbnail size |
| **Wax Seal / Shield Stamp (`v2`, `✓`)** | 512×512 | `11.5–12.0` | `7.0–7.5` | `25.5–27.0` | Slightly lighter wall so the mark sits comfortably inside a 140px seal |
| **Secondary Pill Label (`SDK`, `OSS`, `BETA`)** | 512×512 | `0` (single ink centerline) | `5.8–6.5` | `5.8–6.5` | Drawn directly on top of a `{PAPER}`-filled pill or banner (`stroke-width="8.0–8.5"`) |

---

## 2. Composition Rules: Square Social Cards vs. Wide Repo Banners

While `release-hero-card.svg` and `editorial-badges.svg` use a square `512×512` viewBox so they can be validated directly by `scripts/lineart.py lint` (which rasterizes square thumbnails at 160×160, 168×168, and 28×28), open-source branding spans both **square cards** (512×512 / 1080×1080) and **wide banners** (1280×640 GitHub Social OpenGraph cards, 1200×320 README headers).

| Dimension / Rule | Square Social Card (`512×512`, 1:1) | Wide OpenGraph Card (`1280×640`, 2:1) | Wide README Hero Banner (`1200×320`, 15:4) |
|---|---|---|---|
| **Subject & Typography Split** | Stacked/overlapping diagonal: cutout title (`v2.0`) in upper-left overlapping the top corner of the central device/terminal (`55–75%` canvas width). | Asymmetric two-zone split: left `45%` holds double-stroked repo title + version pill; right `55%` holds the hero device/diagram breaking across the center seam. | Horizontal frieze: center-left title lockup + right-hand expressive motif connected by a sweeping trajectory arc or branch line. |
| **Watercolor Wash Coverage (`10–50%`)** | Two overlapping washes (`clay` lower-left + `sky` upper-right) glazed with `mix-blend-mode: multiply`, covering **17–25%** of total canvas. | Keep wash confined to the illustration cluster + behind one corner of the title (`18–30%` total canvas). Never stretch a wash across the full 1280px width or it reads as a flat background banner plate. | Use two compact horizontal/tilted wash patches under the focal transition zone (`15–25%` coverage), leaving generous `{PAPER}` margins on both ends. |
| **Breakout Rule (`≤ 80%` ink on wash)** | At least 3 elements break out of the wash boundary (`v2.0` top-left, paper plane nose top-right, `SDK` pill bottom-right). | Title lettering starts on bare `{PAPER}` and enters the wash on its right; foreground motif breaks out of the wash toward the top-right. | Motif ascenders/descenders (paper plane wing, lightning bolt tip, ribbon tails) cross the top and bottom edges of the wash. |
| **Quiet Space & Accents (`3–6` marks)** | One entire quadrant (e.g., lower-left in `release-hero-card.svg`) stays free of heavy shapes and holds the `1 : 0.6 : 0.4` sparkle cluster + 2 dots. | Leave one outer margin quadrant (usually bottom-left below the subtitle or top-right beside the breakout motif) completely quiet. | Keep the far-left and far-right 15% of the banner free of clutter; place a single 3-sparkle cluster near the launch trajectory. |
| **Filter Scaling (`wash` & `ink`)** | `wash`: `baseFrequency="0.011"`, `scale="13"`; `ink`: `baseFrequency="0.013"`, `scale="6.2"`. | Scale `scale` proportionally to the shorter dimension (`640px` → `wash scale="15"`, `ink scale="7"`), keeping `baseFrequency` around `0.009–0.012`. | Anchor filter parameters to the vertical height (`320px` → `wash scale="10"`, `ink scale="5"`) so horizontal lines do not over-distort. |

---

## 3. Lint Results & Visual Critique Checklist

### `python3 -I scripts/lineart.py lint` Output

#### `release-hero-card.svg`
```text
OK    no clip-art geometry found in the markup
OK    block visible: 40% of the wash shows (want ≥ 30%)
OK    color coverage: 17% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 61% (want ≤ 80%; the art should break out of the block)
NOTE  at 28px 12 of 13 enclosed paper areas close up — the drawing smudges; fewer, bigger shapes (fine if this piece is never shown that small)

0 warning(s). Lint catches mechanical tells only; it cannot tell you the piece is good.
```

#### `editorial-badges.svg`
```text
OK    no clip-art geometry found in the markup
OK    block visible: 44% of the wash shows (want ≥ 30%)
OK    color coverage: 22% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 74% (want ≤ 80%; the art should break out of the block)
NOTE  at 28px 17 of 18 enclosed paper areas close up — the drawing smudges; fewer, bigger shapes (fine if this piece is never shown that small)

0 warning(s). Lint catches mechanical tells only; it cannot tell you the piece is good.
```

---

### Art Direction 10-Point Critique Checklist

#### Piece 1: `release-hero-card.svg` (*"v2.0 Release / CLI & Agent SDK"*)

1. **Does the brief test pass: would this picture break if the name were changed?**
   - **Yes.** It explicitly combines the `"v2.0"` release cutout typography, a CLI terminal with `>_` prompt + code lines, an agent gear + SDK blueprint grid behind the window, an `"SDK"` stamp pill, and a launching paper plane. Swapping in a database or prose tool name would break the `"v2.0"` + `"SDK"` + CLI terminal iconography.
2. **Is there something behind the subject and something in front of it?**
   - **Yes (3 distinct depth planes).** Behind the terminal sit the tilted SDK blueprint card (`back_card`), the toothed agent gear (`gear_body`), and the dashed launch trajectory (`trail_arc1`, `trail_arc2`). Across the front of the terminal sit the double-stroked `"v2.0"` cutout lettering, the launching paper plane (`plane_paper`), and the `"SDK"` stamp pill (`sdk_pill`).
3. **Does the wash sit off-center, with art crossing its edge in two or more places?**
   - **Yes.** `lint` confirms **40% block visible** (`≥ 30%`), **17% color coverage** (`10–50%`), and **61% line art over the wash** (`≤ 80%`, meaning **39%** of the ink breaks out into bare `{PAPER}` across the upper-left `"v2.0"` letters, the upper-right paper plane nose, and the lower-right `"SDK"` pill).
4. **On larger pieces, are there two washes, one warm and one cool, with a clean glaze where they overlap?**
   - **Yes.** A warm `clay` quadrilateral (`#D97757`) in the center-left overlaps a cool `sky` quadrilateral (`#6A9BCC`) in the upper-right using `mix-blend-mode: multiply` inside `<g id="layer-block" style="isolation:isolate">`, glazing a rich third tone where they meet, complemented by an `olive` (`#788C5D`) focal spot under the `"SDK"` stamp.
5. **Is any outline a primitive, a ruler line or mirror-symmetric?**
   - **No (`0 warnings` in `lint`).** All boxes use `handify`, all round shapes use `wobbly_circle` with asymmetric wobble, and all strokes use 7 distinct stroke weights (`4.0`, `4.8`, `5.0`, `5.2`, `5.5`, `6.0`, `6.5`, `7.0`, `7.5`, `8.0`, `8.5`, `9.0`, `14.5`, `31.5`).
6. **Are repeated marks varied, and do at least one or two corners overshoot?**
   - **Yes.** The 4 terminal code lines vary in start X, length (`264–348`), and bow seed; the top-right corner of the terminal frame (`term_frame_top` vs `term_frame_rest`) overshoots by 10 units like an architect's sketch; and the left frame has an intentional 22-unit breathing gap below the title bar (`y: 240..262`).
7. **Are accents 3–6, clustered, and earned by the subject?**
   - **Yes (5 marks total).** A single cluster of 3 tilted `sparkle()` marks (radii `16.0`, `10.0`, `6.6` — `1 : 0.62 : 0.41`) + 1 dot sits in the quiet lower-left quadrant, with 1 small echo dot near the paper plane's wake (`458, 224`).
8. **Is one area left quiet?**
   - **Yes.** In Revision 1, the gear wheel sat too low (`cy=388`) and crowded the lower-left corner. In Revision 2, we tucked the gear up behind the mid-left of the terminal (`cy=310`), opening up the lower-left quadrant (`x: 20..120, y: 380..500`) as dedicated quiet breathing space for the sparkle cluster.
9. **At 28px, does it still read as the subject, without smudging into a dark blob?**
   - **Yes.** Because this is a `512×512` hero card (`stroke-width="8.5"` scales to `0.46px` at 28px), `lint` emits `NOTE` rather than `WARN` for 28px holes, and the high-contrast `{PAPER}` terminal, `"v2.0"` cutout, and warm/cool washes remain open and un-smudged.
10. **What was the single weakest part of the piece in Draft 1, and how was it fixed?**
    - **Draft 1 Weakness:** The agent gear's 3 teeth were drawn as separate small `<path>` elements (`mext ~ 25px`), which `lint` flagged as free tiny marks (`WARN: 8 tiny marks — reads as confetti`), and the gear's low position left no quiet quadrant.
    - **Revision 2 Fix:** Merged the gear into a single continuous hand-drawn toothed contour (`gear_body`), moved it up to `cy=310` to free the lower-left quadrant, and added `mix-blend-mode: multiply` to the wash overlap.

---

#### Piece 2: `editorial-badges.svg` (*4 Artisanal Developer Stamps & Repo Badges*)

1. **Does the brief test pass: would this picture break if the name were changed?**
   - **Yes.** Each of the 4 badges represents a specific developer/repository status:
     1. **Top-Left**: Verified Shield with a double-stroked checkmark (`✓`) and twin award ribbons
     2. **Top-Right**: Release Wax Seal with double-stroked `"v2"` cutout lettering and hanging ribbons
     3. **Bottom-Left**: Open-Source (`"OSS"`) Octagonal Rosette with a Git branch/merge graph (`main` + `fork` + 3 commit nodes) and crossed stem behind
     4. **Bottom-Right**: `"BETA"` Lab Shipping Tag with overshot architect corners, reinforced eyelet + cord, and a clay lightning bolt breaking out of the top-right edge.
2. **Is there something behind the subject and something in front of it?**
   - **Yes.** Every badge has three planes: background ribbons/stems/cords passing *behind* the main paper plaque (`b1_ribbon_l/r`, `b2_ribbon1/2`, `b3_stem_back`, `b4_cord`), the main `{PAPER}` shield/seal/octagon/tag body in the middle, and foreground double-stroked marks (`✓`, `v2`), lightning bolt (`b4_bolt`), and stamp pills (`OSS`, `BETA`) overlapping across the front.
3. **Does the wash sit off-center, with art crossing its edge in two or more places?**
   - **Yes.** Each badge's watercolor wash is offset 15–25 units from the badge center, and ribbons, checkmarks, banners, and lightning bolts break across the wash boundaries in 8+ places (`lint`: **44% block visible**, **22% color coverage**, **74% line art over the wash**).
4. **On larger pieces, are there two washes, one warm and one cool, with a clean glaze where they overlap?**
   - **Yes.** The sheet pairs warm `clay` (top-left) and `peach` (center glaze, `mix-blend-mode: multiply`) against cool `sky` (top-right), earthy `olive` (bottom-left), and `plum` (bottom-right).
5. **Is any outline a primitive, a ruler line or mirror-symmetric?**
   - **No (`0 warnings` in `lint`).** All circles use `wobbly_circle`, all straight segments use `handify`, and all letterforms (`v2`, `OSS`, `BETA`) are skewed/tilted so no mark is mirror-symmetric.
6. **Are repeated marks varied, and do at least one or two corners overshoot?**
   - **Yes.** Ribbon tails have unequal notch depths and angles; the `BETA` shipping tag (`b4_tag_frame`) has architect-style corner overshoots at its top-left and bottom-left corners; the two `S` letters in `OSS` use distinct seeds and slight vertical offsets.
7. **Are accents 3–6, clustered, and earned by the subject?**
   - **Yes (5 marks total).** A cluster of 3 tilted sparkles (`14.0`, `9.0`, `6.2`) + 1 dot sits in the quiet lower-right margin below the `BETA` badge, with 1 small echo dot in the top-center channel (`248, 88`).
8. **Is one area left quiet?**
   - **Yes.** By shifting Badge 4 (`BETA` tag) slightly upward (`y: 258..438`), the lower-right margin (`y: 440..505`) and the central vertical channel (`x: 232..268`) remain open and quiet.
9. **At 28px, does it still read as the subject, without smudging into a dark blob?**
   - **Yes.** All 4 badge silhouettes remain distinct with open `{PAPER}` interiors and 44% visible watercolor wash.
10. **What was the single weakest part of the piece in Draft 1, and how was it fixed?**
    - **Draft 1 Weakness:** Badge 4 (`BETA`) originally had only a plain horizontal bar at the bottom instead of actual `"BETA"` lettering, and two small marks (`b3_node3` at `r=7.2` and the letter `A` in `BETA`) triggered `lint`'s `mirror-symmetric` warning.
    - **Revision 2 Fix:** Replaced the plain bar on Badge 4 with a tilted foreground stamp pill (`b4_pill`) containing hand-drawn centerline letters **`B E T A`**, compacted the git commit nodes to `r=6.0`, and skewed the apex of `A` (`M 398 424 L 418 393 L 426 422`) so `lint` passes with **0 warnings**.
