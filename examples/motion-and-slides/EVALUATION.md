# Track 5 Evaluation — Animated Line-Art (Stroke-Draw & Breathing Wash) & Presentation Deck Visuals

## 1. Executive Summary

This exploration demonstrates that **`CC-lineart` is natively suited for both animated HTML/web presentation decks and static Keynote/PowerPoint/PDF exports from a single SVG source**. Because `CC-lineart` enforces a strict three-layer architecture (`#layer-block`, paper fills, `#layer-ink`) and requires every ink `<path>` to be authored as a single intentional movement of a pen (`references/art-direction.md`, Step 5), adding `pathLength="1"` and sequential `data-step` indices transforms static illustrations into choreographed hand-drawn animations without altering a single coordinate or failing `lineart.py lint`.

---

## 2. Why `CC-lineart`'s "One Pen Stroke at a Time" Rule Enables Natural Stroke-Draw Animation

In typical vector clip-art or icon libraries, outlines are authored as compound paths (`M... Z M... Z`), boolean-unioned polygons, or outlined strokes (`stroke="none" fill="#000"`). When animated with CSS `stroke-dashoffset`, those shapes trace both sides of a line simultaneously or jump erratically between disconnected subpaths.

By contrast, `CC-lineart`'s authoring rules map 1:1 to physical pen choreography:

1. **Single-Movement Centerline Paths (`art-direction.md` Step 5)**  
   Every `<path class="draw-stroke" pathLength="1">` has a clear start point, a bowed cubic Bezier trajectory (`handify`), and a round end-cap (`stroke-linecap="round"`). Setting `pathLength="1"` normalizes every stroke's arc length to `[0, 1]`, allowing a single CSS keyframe (`stroke-dasharray: 1; stroke-dashoffset: 1 -> 0`) to draw short hatches and long sweeping connectors with consistent easing.
2. **Overshooting Corners as Separate Strokes (`handify --overshoot`)**  
   When boxes and frames (such as the Sketch Card, Agent Terminal Card, or Studio Monitor) are drawn in two open L-shaped strokes with `overshoot > 0`, animating them sequentially reproduces the exact rhythm of an architect or illustrator sketching a frame—drawing two sides, lifting the pen, and crossing the corner with the closing two sides.
3. **Three-Layer Paint Order & Paper-Fill Reveal (`drawing-guide.md`)**  
   In `CC-lineart`, strokes that pass *behind* objects are placed first in `#layer-ink`, followed by `#FAF9F5` (`{PAPER}`) closed fills, followed by outline and interior detail strokes. During animation:
   - Background trajectory curves draw first across the canvas.
   - As each object's outline strokes draw (`data-step="N"`), its `{PAPER}` fill fades in (`opacity: 0 -> 1` with a `+140ms` offset), organically occluding the background strokes underneath—just like opaque gouache/paper laid over a preliminary sketch.
   - Interior details (terminal prompts, starburst rays, notebook lines, rising steam wisps) draw on top of the revealed paper shape, finishing with the quiet-space sparkle cluster.
4. **Breathing Watercolor Wash (`#layer-block`)**  
   Because the mottled watercolor blocks live inside `<g id="layer-block" filter="url(#wash)" style="isolation: isolate">`, each wash layer (`wash-1`, `wash-2` with `mix-blend-mode: multiply`, and `wash-3` focal `clay` spot) can gently scale and drift (`translate(4px, -3px) scale(1.018)` over a 7-second alternating cycle) while the ink layer remains crisp and anchored.
5. **Zero-Cost Static Fallback (`rsvg-convert` & `lint`)**  
   In static SVG renderers (`rsvg-convert`, Keynote, Figma, PDF export), `pathLength="1"` and `data-step` attributes are inert when no external animation class is active, producing bit-identical static renders that pass `lineart.py lint`.

---

## 3. Structuring Presentation Slide Visuals with `CC-lineart`

Presentation visuals on a `512×512` canvas (paired with 16:9 slide typography, as demonstrated in `motion-showcase.html`) follow four structural principles:

1. **Diagonal Multi-Act Narrative Flow**  
   Rather than centering a single oversized icon, arrange 2–3 overlapping paper planes along a diagonal axis (e.g., lower-left → center → upper-right in `slide-editorial-story.svg`) connected by both background dashed arcs and foreground handified arrows.
2. **Warm + Cool Glazed Washes + One Focal Spot**  
   Use two offset quadrilateral washes of contrasting temperature inside an `isolation: isolate` group—such as earthy `olive` (`#788C5D`) and warm `peach` (`#EBC9B7`), or cool `sky` (`#6A9BCC`) and `peach`—blended via `mix-blend-mode: multiply` so their central intersection glazes a third mid-tone. Anchor the eye at the narrative climax with a smaller `clay` (`#D97757`) wobbly circle.
3. **512-Grid Filter & Weight Hierarchy (`drawing-guide.md` "Scaling up")**  
   - **Primary outlines**: `stroke-width="8.5"` (`8.0` for secondary objects)
   - **Interior details & connectors**: `stroke-width="6.0"` to `6.5` (~70–75% of primary weight)
   - **Accents, steam, and dashed trails**: `stroke-width="5.0"` to `5.5` (~60% of primary weight)
   - **Filters**: `#wash` uses `baseFrequency="0.011" numOctaves="4" scale="13"`; `#ink` uses `baseFrequency="0.013" numOctaves="2" scale="6.2"`.
4. **Preserving Quiet Space for Slide Balance**  
   Leave one quadrant (e.g., upper-left in `slide-editorial-story.svg`, upper-left/lower-center in `animated-creative-desk.svg`) free of heavy paper shapes, seasoned only with a 3-sparkle cluster (`1 : 0.6 : 0.4` ratio) and two small pigment dots so the illustration breathes beside slide copy.

---

## 4. `lineart.py lint` Results

Both SVGs were validated with `python3 -I scripts/lineart.py lint` after our revision pass:

### `slide-editorial-story.svg`
```text
OK    no clip-art geometry found in the markup
OK    block visible: 46% of the wash shows (want ≥ 30%)
OK    color coverage: 17% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 66% (want ≤ 80%; the art should break out of the block)
NOTE  at 28px 7 of 8 enclosed paper areas close up — the drawing smudges; fewer, bigger shapes (fine if this piece is never shown that small)

0 warning(s).
```

### `animated-creative-desk.svg`
```text
OK    no clip-art geometry found in the markup
OK    block visible: 41% of the wash shows (want ≥ 30%)
OK    color coverage: 17% of the canvas (want 10–50%; above that the wash turns into a background plate)
OK    line art over the wash: 63% (want ≤ 80%; the art should break out of the block)
NOTE  at 28px 10 of 11 enclosed paper areas close up — the drawing smudges; fewer, bigger shapes (fine if this piece is never shown that small)

0 warning(s).
```

*(Note: As `lineart.py` states on 512×512 hero/slide illustrations (`size >= 256`), the 28px hole-closure note is informational because 8.5px strokes on a 512 grid scale down to 0.46px at 28px; presentation visuals are displayed at 320–512px.)*

---

## 5. Visual Critique Checklist (`art-direction.md`) & Revision Log

### Piece 1: `slide-editorial-story.svg` ("From Sketch → Agent Execution → Shipped Artifact")

- **Brief (1 sentence)**: A three-stage diagonal narrative showing a hand-sketched notepad with a fountain pen (Act I) feeding into an autonomous agent terminal with the Claude 7-ray starburst (Act II) and culminating in a verified shipped artifact card (Act III).
- **Checklist Answers**:
  1. **Brief test**: Passes — the dog-eared sketchpad + fountain pen, `>_` terminal + 7-ray agent starburst, and checkmark release card specifically depict an AI coding agent's sketch-to-ship workflow; swapping in an unrelated topic breaks the visual metaphor.
  2. **Depth (behind & in front)**: Yes — the dashed trajectory arc (`data-step="1"`) and inter-card connectors (`data-step="2..3"`) pass *behind* the `#FAF9F5` paper cards, while the fountain pen (`data-step="13..17"`) and foreground curved arrows (`data-step="36..39"`) cross *in front* of the card edges.
  3. **Wash offset & breakout**: Yes — `lint` confirms **46% block visible** ($\ge 30\%$), **17% color coverage** ($10\text{--}50\%$), and **66% line art over the wash** ($\le 80\%$, meaning **34% of the line art breaks cleanly outside the wash** in the lower-left and upper-right corners).
  4. **Two washes + glaze + focal spot**: Yes — cool/earthy `olive` in the lower-left and warm `peach` in the center-right overlap with `mix-blend-mode: multiply` under `isolation: isolate`, plus a warm `clay` focal circle beneath the Act III shipped badge.
  5. **No primitives, ruler lines, or mirror symmetry**: Yes — `lint` reports `OK no clip-art geometry found in the markup`.
  6. **Varied repeats & overshooting corners**: Yes — text/code bars vary in length and angle (`182->358`, `206->274`, `208->256`), starburst rays use 7 irregular angles and $\pm 15\%$ length scales, and all three cards use `overshoot=10..12` at their meeting corners.
  7. **Accents (3–6, clustered, earned)**: Yes — 3 tilted unequal-arm sparkles (`r=22, 14, 10`) + 2 small dots clustered in the upper-left quiet quadrant, plus 1 small echo (`r=13`) in the lower-right.
  8. **Quiet space**: Yes — the upper-left quadrant (`x: 30..165, y: 30..160`) is left open aside from the accent cluster.
  9. **Small-size legibility**: At deck thumbnail size (`160–256px`), the three stepped paper cards and diagonal progression read immediately.
  10. **Weakest part identified in Draft 1 & fixed in Revision 2**: In Draft 1, `line art over the wash` was `79%` (barely passing the `80%` threshold) because the `olive` and `peach` washes extended too far toward the corners, and Act I's interior sketch was a plain box. In Revision 2, we pulled the washes inward (`s-olive-v2`, `s-peach-v2`), pushed Act I and Act III further toward the canvas corners (reducing `line art over the wash` to `66%`), added a fountain pen clip/collar, and replaced the static box with an asymmetric wireframe + flow curve.

---

### Piece 2: `animated-creative-desk.svg` (Editorial Workspace & Motion Study)

- **Brief (1 sentence)**: An editorial creative workspace where a studio monitor running code/waveform analysis, a spiral-bound field notebook, and a steaming ceramic mug launch a folded paper plane across the canvas.
- **Checklist Answers**:
  1. **Brief test**: Passes — every element belongs to a creative developer/designer desk launching an artifact (studio display with sidebar/code/waveform, spiral sketchpad, steaming mug, paper plane on a dashed launch trajectory).
  2. **Depth (behind & in front)**: Yes — the desk horizon lines (`data-step="1..2"`) and the dashed paper-plane flight trail (`data-step="3"`) pass *behind* the studio monitor's `#FAF9F5` screen fill, while the open spiral notebook (`data-step="17..27"`) overlaps the front of the monitor base and wash edge.
  3. **Wash offset & breakout**: Yes — `lint` confirms **41% block visible** ($\ge 30\%$), **17% color coverage** ($10\text{--}50\%$), and **63% line art over the wash** ($\le 80\%$, meaning **37% of the line art breaks out of the wash** across the lower-left notebook, right mug handle, and upper-right paper plane).
  4. **Two washes + glaze + focal spot**: Yes — cool `sky` (`#6A9BCC`) behind the monitor and warm `peach` (`#EBC9B7`) behind the mug/desk glaze cleanly via `multiply`, with a `clay` focal circle (`#D97757`) highlighting the launching paper plane in the upper-right.
  5. **No primitives, ruler lines, or mirror symmetry**: Yes — `lint` reports `OK no clip-art geometry found in the markup`.
  6. **Varied repeats, overshooting corners, and intentional gap**: Yes — the 3 rising steam wisps vary in height and curvature, the 3 code lines and 3 notebook lines vary in length, the monitor and notebook corners overshoot (`overshoot=10..13`), and the mug handle intentionally stops just short of closing at its lower join (`M 442 326 C 482 324 484 390 444 398`) so the drawing breathes.
  7. **Accents (3–6, clustered, earned)**: Yes — 3 sparkles (`r=20, 13, 11`) + 2 dots clustered around the paper plane's upper-right launch zone, plus 1 small echo (`r=13`) on the left.
  8. **Quiet space**: Yes — the upper-left margin above the monitor and lower-center desk space remain uncluttered.
  9. **Small-size legibility**: The silhouette of the tilted monitor, foreground notebook, mug with handle, and diagonal paper plane remains unmistakable across sizes.
  10. **Weakest part identified in Draft 1 & fixed in Revision 2**: In Draft 1, `lint` flagged `WARN 1 mirror-symmetric mark(s)` on the mug's lower colored band (`data-step="26"`), which had been written as an un-handified 4-point polygon, and `line art over the wash` was `79%`. In Revision 2, we replaced the symmetric polygon with an asymmetric handified ceramic wave glaze (`mug_glaze_fill`), added a curved coffee rim arc at the top of the mug and spiral binding rings on the notebook spine, and tightened the `sky` and `peach` washes so `line art over the wash` improved from `79%` to `63%`.
