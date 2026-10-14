---
name: cc-lineart
description: >-
  Draw SVG illustrations, icons, product UI components, empty states,
  architecture diagrams, editorial data visualizations, repo branding/badges,
  and animated stroke-draw slide visuals in a hand-drawn ink + watercolor style
  (bold #141413 ink line art with #FAF9F5 paper-white fills over a mottled
  watercolor color block: clay, sky, cactus, heather, plum, mineral, peach,
  kraft, olive). Use when the user asks for a line-art / 线稿 / 水彩 /
  claude.com-style illustration, icon, logo, UI kit, empty state, diagram,
  chart, banner, or 插画, or says "给项目画个图标", "新项目没图标", "补图标".
---

# CC line art

Hand-drawn ink + watercolor SVG design system for coding agents — scaling from **64×64 project icons** to **512×512+ product UI kits, empty states, architecture diagrams, benchmark charts, repo branding, and animated presentation visuals**. Copy this folder into your agent's skills directory (for example Claude Code `~/.claude/skills/cc-lineart` or your Cursor/Codex skills path), then run commands from this folder. Needs `python3`, `rsvg-convert`, ImageMagick (`magick`), and Pillow for `lint`.

```
apt-get install librsvg2-bin imagemagick   # or: brew install librsvg imagemagick
pip install Pillow
```

Every piece is three layers, bottom to top:

1. **Watercolor block** — one or two irregular quadrilaterals in brand colors, offset to one side of the subject, never centered. A noise filter mottles its alpha (the wash) and a darker rim at 55% opacity mimics pigment pooling at the edge. On larger pieces (`>= 256px`), overlap a warm wash and a cool wash with `mix-blend-mode: multiply` inside `<g id="layer-block" style="isolation: isolate">` so the intersection glazes a third tone.
2. **Paper shapes** — the subject's closed outlines filled `{PAPER}` (`#FAF9F5`). They sit on the block and hide part of it while 20%+ of the line art breaks outside the wash boundary.
3. **Ink** — `#141413` strokes, round caps and joins, with a slight displacement wobble so nothing is ruler-straight.

`scripts/lineart.py` holds the palette, filters, path generators (`handify`, `wobbly_circle`, `sparkle`), and size presets, so a motif only supplies `block` and `ink`. The icon library lives in `motifs/*.json` and grows every time something new is drawn; full multi-scenario reference generators live in `examples/*/`. Run the script with `python3 -I` from any directory.

```
python3 -I scripts/lineart.py list                    # what already exists
python3 -I scripts/lineart.py suggest "<name, README words>"
python3 -I scripts/lineart.py render <motif|draft.json> -o out.svg [--color sky] [--size lg|sm]
python3 -I scripts/lineart.py preview a.svg b.svg -o sheet.png   # then open sheet.png and look
python3 -I scripts/lineart.py add draft.json          # save a new motif into the library
python3 -I scripts/lineart.py handify "M10 10 L54 10 L54 40" [--amount 0.8] [--overshoot 2]
python3 -I scripts/lineart.py circle 32 32 12          # hand-drawn circle path data
python3 -I scripts/lineart.py sparkle 50 14 5          # tilted, unequal-arm sparkle path data
python3 -I scripts/lineart.py lint out.svg            # style checks; needs layer ids, Pillow, rsvg-convert
```

`lint` judges the markup (primitives, ruler lines, symmetric marks, single-weight large pieces, confetti) and the render (how much of the wash shows, whether the art breaks out of it, whether the piece smudges at 28px). It only works when the wash sits in `<g id="layer-block">` and the line art in `<g id="layer-ink">`; `render` adds both. It catches mechanical tells only: a piece with no warnings can still be dull.

## Draw a new motif (64×64 icons)

Read both references first: `references/art-direction.md` (the process, and the rules that decide whether a piece looks drawn or like clip-art) and `references/drawing-guide.md` (the grid, curve tricks and paint order). Then:

1. Write the brief, two or three layout thumbnails in words, and the layer plan (art direction, steps 1–3) before any coordinates.
2. Write a draft JSON: `name`, `description`, `tags` (English keywords for `suggest`), `color`, `block`, `ink`. `ink` is SVG markup on a 64×64 grid using only `path`, `circle`, `ellipse`, `line`, `polyline`, `polygon`, `rect`, `g`. Use `{PAPER}` and `{INK}` as color tokens. Inherited defaults are already stroke ink, no fill, round caps. Build round shapes with `circle`, straight runs with `handify`, and sparkles with `sparkle`, instead of primitives.
3. Render at `lg` and `sm`, run `lint` on the `lg` render, and `preview` both **together with two existing motifs** so the weight and density match the set. Look at the sheet.
4. Answer the critique checklist in art direction in writing, fix what fails, and render again. At least one revision round. Every `lint` warning is fixed or explained.
5. `add` it to the library.

## Larger pieces & expanded scenarios (512×512+ canvases & web UI)

Same three layers on a bigger canvas (`512×512` or `800×480`), importing `handify`, `wobbly_circle`, `sparkle`, `COLORS`, `INK`, and `PAPER` from `scripts/lineart.py`. Scale stroke widths (`8–9` primary, `5.5–6.5` details, `4–5` accents) and filter parameters (`wash` `scale=13, baseFrequency=0.011`; `ink` `scale=6.2, baseFrequency=0.013`) per `references/drawing-guide.md`.

Reference implementations and evaluations in `examples/`:

1. **Product UI Kits, Empty States & Interactive Web UI (`examples/ui-kit/`)**
   - Use for zero-inbox / empty-state panels, onboarding cards, tactile buttons, `⌘K` command bars, toggles, and interactive HTML/CSS surfaces where a shared zero-size SVG `<defs>` filter bank (`#ui-wash`, `#ui-ink`) and `vector-effect="non-scaling-stroke"` power hover-parallax watercolor washes.
2. **Editorial Architecture & Multi-Agent Diagrams (`examples/diagrams/`)**
   - Use for RFC headers, multi-agent orchestration topologies, and RAG/system pipelines. Group logical stages with warm + cool glazed watercolor blocks instead of sterile bounding boxes; route connectors as `handify()` cubic curves passing behind `{PAPER}` node cards; replace font `<text>` with miniature `CC-lineart` motifs and varied scribble bars.
3. **Editorial Data Visualization & Benchmark Infographics (`examples/dataviz/`)**
   - Use for model launch benchmark charts, growth curves, and telemetry KPI gauges. Apply a tiered `handify` hierarchy (`1.6–2.0` for ticks/glyphs, `2.8–3.0` for data columns, `3.5` for axes/splines, `4.2–5.5` for cards/washes) so quantitative heights stay faithful while passing `lint` with 0 symmetry or ruler-line warnings.
4. **Open-Source Repo Branding, Hero Banners & Artisanal Badges (`examples/branding/`)**
   - Use for GitHub README hero cards, release headers (`v2.0`), wax seals, and verification stamps. Draw display lettering and version numbers with the centerline double-stroke cutout technique (all `INK` spines at `W + 2t` first, then all `PAPER` cores at `W` second).
5. **Animated Stroke-Draw Line Art & Slide Deck Visuals (`examples/motion-and-slides/`)**
   - Because every `<path>` is authored as a single pen movement, adding `pathLength="1"` and sequential `data-step` indices enables choreographed CSS `stroke-dashoffset` pen drawing, delayed `{PAPER}` fill reveals, and gently breathing watercolor washes — while exporting bit-identically to static PNG/PDF via `rsvg-convert`.

## Notes

- `preview` needs `rsvg-convert` and `magick` (`brew install librsvg imagemagick`).
- These are original drawings in the style of claude.com's illustrations. Do not copy Anthropic's own illustration SVGs into the library.
