# Art direction

The drawing guide says how to put marks on the canvas. This file says which marks to make. Two agents using the same palette, filters and helpers can still produce one picture that feels drawn and one that feels like clip-art; the difference is made of the decisions below, and every one of them can be checked.

## The process

Do these in order. Skipping steps 1–3 is the most common reason a piece comes out flat.

1. **Brief, in one sentence.** What is the piece about, and which one or two elements does it take from the subject's existing identity? For a logo that means the original mark (its shapes, its motif, its colors); for a project icon, the thing its name or README describes. Test: swap in a different product name. If the picture still works unchanged, it says nothing about this subject. Pick a different idea.
2. **Thumbnails, in words.** Before any coordinates, write two or three layouts as short text: where each wash sits (which quadrant, how big), where the subject sits, what overlaps what, and which area stays empty. Choose one and say why in one line. Example: "Washes upper-right and lower-left, overlapping behind the subject; subject centered slightly low; one shape behind, one across the front; top-left stays empty except a sparkle cluster."
3. **Layer plan.** List every element bottom to top: washes, strokes that pass behind paper, paper shapes back to front, details on top, accents. At least one element must sit *behind* the subject and one *in front* of it. A piece where everything shares one plane reads as a sticker.
4. **Big shapes first.** Draw only the washes and the main paper shapes. Render at full size and at thumbnail size and judge the composition now, while moving things is cheap. No details yet.
5. **Ink, one pen stroke at a time.** Each `<path>` is one movement of a pen: it has a start, a direction, and an end where the round cap shows. Draw an outline the way a hand would draw it, in two or three strokes that meet or slightly overshoot, not as a polygon traced around the shape. Letters and bars are centerline strokes (the double-stroke technique in the drawing guide), never outlined polygons.
6. **Accents last, and few** (rules below).
7. **Render, write the critique, revise.** Run `lint`, look at the render, and answer the checklist at the end of this file *in writing*, one line per question with what you see. Fix what fails and render again. Do at least one revision round before showing anything. A first draft is never the deliverable.

If you cannot view images in this environment, say so to the user, rely on `lint` plus the numbers you can compute, and ask them to look. Do not claim a piece looks right when you have not seen it.

## Line quality

A hand-drawn line is imperfect in specific ways. Put them into the path data on purpose; the wobble filter only adds tremor on top and cannot rescue a geometric path.

- **No primitives for visible outlines.** In the ink layer, `<circle>`, `<ellipse>` and `<rect>` are allowed only for dots and fills smaller than ~12% of the canvas. Larger round things come from `lineart.py circle` (the radius drifts ±5% and the stroke runs past its start so the seam shows). Larger boxes come from `handify`.
- **No ruler lines.** A horizontal or vertical segment longer than 12% of the canvas bows by 0.5–1.5% of its length: `M15 9.5 C29 8.8 44 9.2 57.5 10`, not `L57.5 9.5`. `handify` does this for you.
- **Corners are where two strokes meet.** On boxes, frames and easels, let one or two corners overshoot by 1–3 units on a 64 grid (8–20 on 512), like an architect's sketch. Not every corner, or it becomes a pattern. `handify --overshoot` draws open polylines this way.
- **Repeats are never copies.** Text lines, steam, rays, log ends, sparkles: vary each one's length by 10–20%, its spacing and its angle by a few degrees. Five identical lines read as a font, not a hand.
- **Asymmetry.** Nothing larger than a dot is mirror-symmetric. Skew one side, make one arm longer, tilt the axis 5–15°. Perfect symmetry is the strongest clip-art tell.
- **Weights in larger pieces.** Use two or three stroke widths: outlines heaviest, interior details about 70% of that, accents about 60%. Icons can stay on one weight, because at 14px variation is invisible.
- **Ends and gaps.** Let a stroke stop just short of where it would close (a cup handle, a cloud's base) in one place per piece. The eye closes the gap, and the drawing breathes.

## Composition

- **The wash is offset, not a plate.** The wash's center sits 10–25% of the canvas away from the subject's center. Wash coverage stays between 10% and 50% of the canvas; above that it becomes a background plate behind everything (`lint` measures this).
- **The art breaks out.** At least 20% of the line art lies outside the wash, and lines cross the wash edge in at least two places. This overlap is the style's signature. `lint` reports "line art over the wash"; at the `sm` icon preset the block is enlarged on purpose, so lint the `lg` render.
- **The block shows.** 30% or more of the wash stays visible after the paper shapes cover it. Otherwise the piece goes grey.
- **Two washes on larger pieces.** Overlap them with `multiply` so the overlap glazes a third color. One flat color over the whole piece is what "单调" (monotonous) looks like. The two must differ in temperature or strongly in value: a warm with a cool (clay and sky, peach and heather, plum and sky). Neighbors such as clay and peach read as one color, and their overlap barely shows. Avoid pairs that mix to mud (clay over plum or olive turns brown); if a warm spot must sit near a cool wash, move it away or blend it normally.
- **One focal spot.** Optionally, one small patch of the hottest color (clay) where you want the eye to land first, away from the main wash.
- **Quiet space.** One quadrant stays mostly empty. Empty space is part of the picture, not leftover canvas to fill.
- **Scale.** The subject spans 55–75% of the canvas width. Smaller looks lost; larger leaves no room for the wash to show.

## Accents

Sparkles, dots, motion lines and the like are seasoning.

- **3–6 in total**: one cluster of three (big, medium, small, sizes roughly 1 : 0.6 : 0.4) plus two dots, placed in the quiet area, and at most one small echo somewhere else. Never one per corner; evenly spread accents read as confetti (`lint` warns above 7 tiny marks).
- **Draw them with `lineart.py sparkle`**: two crossing strokes with unequal arms, tilted and slightly bowed. No four-pointed diamond stars and no equal-arm `+`.
- **Only symbols the subject earns.** A moon and stars belong to a piece about night. Don't add them because "logos have sparkles". When unsure, leave the accent out.

## Critique checklist

Answer every line in writing after each render. "Yes" needs evidence: a number from `lint` or something specific you can see.

1. Does the brief test pass: would this picture break if the name were changed?
2. Is there something behind the subject and something in front of it?
3. Does the wash sit off-center, with art crossing its edge in two or more places? (`lint`: line art over the wash ≤ 80%, block visible ≥ 30%, coverage 10–50%)
4. On larger pieces, are there two washes, one warm and one cool, with a clean glaze where they overlap?
5. Is any outline a primitive, a ruler line or mirror-symmetric? (`lint` source checks)
6. Are repeated marks varied, and do at least one or two corners overshoot?
7. Are accents 3–6, clustered, and earned by the subject?
8. Is one area left quiet?
9. At 28px, does it still read as the subject, without smudging into a dark blob? (`preview`, `lint` 28px check)
10. What is the single weakest part of the piece right now? Name it, fix it, render again.

Question 10 always has an answer. If you can't find one, you haven't looked closely enough.

## Case study: good vs flat

Two logos can share the same filters, palette and letter technique and still look different. The flat one usually scores fine on lint's mechanical checks and still fails the rules above. Mapped:

| Flat version | Rule | Drawn version |
|---|---|---|
| One color square behind everything, centered | Wash offset, coverage ≤ 50% | Two washes, upper-right and lower-left, overlapping into a darker glaze |
| Every element on one plane | Something behind, something in front | One shape behind the subject, one across its front |
| A diamond star, a `+` in each corner, white dots inside the wash | 3–6 accents, clustered | Sparkle cluster in the quiet area and one small echo |
| A smooth geometric crescent, symmetric sparkles | No primitives, asymmetry | Starburst of uneven rays on a round wash spot, tilted sparkles |
| Generic stock symbols | Earned symbols | Motifs the subject already owns |
| One color | Two washes, focal spot | Warm + cool glazed together, with a clay spot as the focal point |

What the flat version often still gets right: legible letters, watercolor texture, and the subject crossing the wash edge. Keep those; fix the rest.
