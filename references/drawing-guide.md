# Drawing guide

## The grid

Icons use a 64×64 viewBox. Keep the subject inside roughly 6–58 on both axes; strokes are 3.2 units wide at `lg` and 4.3 at `sm`, so anything finer than about 3 units between parallel lines merges at small sizes.

A good layout puts the block in one quadrant-ish region and lets the subject overlap it by about half:

```
block   M5 18 L43 15.5 L45.5 55 L7 57 Z     (lower-left)
subject window from (15,9.5) to (57.5,47.6) (upper-right)
```

Give the block four slightly different corner offsets (e.g. `15.5`, `55`, `57`). A perfect rectangle looks digital.

## Making lines look drawn

The ink filter adds a small wobble, but the paths themselves should not be geometric either. `lineart.py handify`, `circle` and `sparkle` produce the patterns below; the full rules are in `art-direction.md` under "Line quality".

- Straight edges as very shallow curves: `M15 9.5 C29 8.8 44 9.2 57.5 10` instead of `L57.5 9.5`.
- End points a little off-grid (`57.3 18.3`, not `57 18`).
- Close shapes that should read as solid objects (window, page, bubble) and fill them `{PAPER}`. Leave decorative strokes open.
- Repeated marks (steam, text lines, sparkles) should vary slightly in length and spacing.
- Rotated objects are easiest from vectors: pick the axis endpoints, normalize the direction `d`, take the perpendicular `n`, and offset by half-width along `n` for the corners. The pencil in `motifs/pencil.json` was built this way.
- The Claude starburst is 7 rays at irregular angles (-90, -38, 8, 52, 98, 146, 196°) with lengths varying ±15%, starting a little away from the center. Compute it with trig rather than guessing.

## Paint order inside `ink`

Later elements cover earlier ones, so order matters:

1. Strokes that should pass *behind* a paper shape (easel legs, mug steam, the dashed trail of the paper plane).
2. Paper shapes, back to front.
3. Details drawn on top of the paper (text lines, chevrons, dots).

To color part of the object (the pencil's eraser), draw the paper fill, then the colored patch with `stroke="none"`, then the outline with `fill="none"`.

## Mistakes earlier drafts made

- **Block hidden** — the book and chat drafts put the block entirely behind the paper shapes, leaving them grey. Move the block so a strip of 8–15 units shows on at least two sides.
- **Too pale at small sizes** — light colors (peach, heather, cactus) almost vanish at 14px. The `sm` preset fixes most of this with a bigger, denser block and heavier ink; always preview the 28px column.
- **Muddy overlaps** — in larger pieces, `multiply` blends clay over plum into a brown. Keep complementary washes apart, or let one sit on top with normal blending.
- **Edge clipping** — an app-icon squircle cuts anything near its corners; inset the artwork to about 80%.
- **Too much detail** — two window dots read at 64px but are noise at 14px. When in doubt, drop details for the `sm` look rather than adding them.

## Scaling up

For a 512 canvas (logos, banners), multiply by 8 what the icon presets use:

| | 64 grid | 512 grid |
|---|---|---|
| ink stroke | 3.2 | 8–9 |
| ink wobble `scale` | 1.5 | 6–7, `baseFrequency` ≈ 0.013 |
| wash displacement `scale` | 2.6 | 12–14, `baseFrequency` ≈ 0.011, `numOctaves` 4 |
| block rim width | 1.4 | 4–5 |

Outlined letters: stroke each letter's centerline twice, ink at `W + 2t`, then paper at `W`, with matching caps and joins. Draw all ink passes before all paper passes so letter parts merge cleanly. 
Overlapping washes with `mix-blend-mode: multiply` inside an `isolation: isolate` group glaze like real watercolor layers.
