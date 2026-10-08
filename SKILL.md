---
name: cc-lineart
description: >-
  Draw SVG illustrations and icons in a hand-drawn ink + watercolor style
  (bold black line art with paper-white fills over a mottled watercolor color
  block: clay, sky, cactus, heather, plum, mineral, peach, kraft, olive).
  Use when the user asks for a line-art / 线稿 / 水彩 / claude.com-style
  illustration, icon, logo or 插画, or says "给项目画个图标", "新项目没图标",
  "补图标".
---

# CC line art

Hand-drawn ink + watercolor SVG icons for coding agents. Copy this folder into
your agent's skills directory (for example Claude Code `~/.claude/skills/cc-lineart`
or your Cursor skills path), then run commands from this folder. Needs
`python3`, `rsvg-convert`, ImageMagick (`magick`), and Pillow for `lint`.

```
apt-get install librsvg2-bin imagemagick   # or: brew install librsvg imagemagick
pip install Pillow
```

Every piece is three layers, bottom to top:

1. **Watercolor block** — one irregular quadrilateral in a brand color, offset to one side of the subject, never centered. A noise filter mottles its alpha (the wash) and a darker rim at 55% opacity mimics pigment pooling at the edge.
2. **Paper shapes** — the subject's closed outlines filled `{PAPER}` (`#FAF9F5`). They sit on the block and hide part of it.
3. **Ink** — `#141413` strokes, round caps and joins, with a slight displacement wobble so nothing is ruler-straight.

`scripts/lineart.py` holds the palette, filters, and size presets, so a motif only supplies `block` and `ink`. The library lives in `motifs/*.json` and grows every time something new is drawn. Run the script with `python3 -I` from any directory.

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

`lint` judges the markup (primitives, ruler lines, symmetric marks, confetti) and the render (how much of the wash shows, whether the art breaks out of it, whether the piece smudges at 28px). It only works when the wash sits in `<g id="layer-block">` and the line art in `<g id="layer-ink">`; `render` adds both. It catches mechanical tells only: a piece with no warnings can still be dull.

## Draw a new motif

Read both references first: `references/art-direction.md` (the process, and the rules that decide whether a piece looks drawn or like clip-art) and `references/drawing-guide.md` (the grid, curve tricks and paint order). Then:

1. Write the brief, two or three layout thumbnails in words, and the layer plan (art direction, steps 1–3) before any coordinates.
2. Write a draft JSON: `name`, `description`, `tags` (English keywords for `suggest`), `color`, `block`, `ink`. `ink` is SVG markup on a 64×64 grid using only `path`, `circle`, `ellipse`, `line`, `polyline`, `polygon`, `rect`, `g`. Use `{PAPER}` and `{INK}` as color tokens. Inherited defaults are already stroke ink, no fill, round caps. Build round shapes with `circle`, straight runs with `handify`, and sparkles with `sparkle`, instead of primitives.
3. Render at `lg` and `sm`, run `lint` on the `lg` render, and `preview` both **together with two existing motifs** so the weight and density match the set. Look at the sheet.
4. Answer the critique checklist in art direction in writing, fix what fails, and render again. At least one revision round. Every `lint` warning is fixed or explained.
5. `add` it to the library.

## Larger pieces (logos, banners, hero art)

Same three layers on a bigger canvas, and you write the SVG directly rather than through `lineart.py`. The process in `references/art-direction.md` is mandatory here: this is where skipping the brief and thumbnails shows most.

Scale stroke widths, filter `scale` and `baseFrequency` with the canvas (notes in the drawing guide). Use the same `layer-block` / `layer-ink` group ids so `lint` can check it, and finish with the same render, critique and revise loop.

## Notes

- `preview` needs `rsvg-convert` and `magick` (`brew install librsvg imagemagick`).
- These are original drawings in the style of claude.com's illustrations. Do not copy Anthropic's own illustration SVGs into the library.
