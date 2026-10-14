#!/usr/bin/env python3
"""Generate Editorial Data Visualization & Benchmark Infographics in CC-lineart style.

Outputs in /Users/wu/CC-lineart/examples/dataviz/:
  - benchmark-comparison.svg
  - telemetry-kpi-card.svg
"""
import math
import os
import random
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from lineart import COLORS, INK, PAPER, fmt, handify, sparkle, wobbly_circle  # noqa: E402


def wash_filter_defs(seed_a=19, seed_b=53, ink_seed=71):
    """512x512 scaled watercolor wash & ink displacement filters."""
    return f"""<defs>
<filter id="wash-a" x="-12%" y="-12%" width="124%" height="124%">
  <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="4" seed="{seed_a}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="13" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.05 1.42" result="a"/>
  <feComposite in="d" in2="a" operator="in"/>
</filter>
<filter id="wash-b" x="-12%" y="-12%" width="124%" height="124%">
  <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="{seed_b}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.0 1.38" result="a"/>
  <feComposite in="d" in2="a" operator="in"/>
</filter>
<filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="{ink_seed}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6.2" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>"""


def build_benchmark_comparison():
    """Editorial Bar/Column + Trend Curve Chart (512x512 viewBox).

    Subject: Coding velocity & reasoning benchmark across 4 model generations,
    culminating in a 2.4x leap on the frontier column.
    Washes:
      - Cool sky wash lower-left/center behind baseline & mid-tier columns
      - Warm clay wash upper-right behind the frontier breakout column & callout badge
    """
    sky_fill, sky_edge = COLORS["sky"]
    clay_fill, clay_edge = COLORS["clay"]
    kraft_fill, _ = COLORS["kraft"]

    # Two offset organic quadrilateral washes (warm clay + cool sky) overlapping in the middle
    sky_block = handify("M 58 195 L 318 176 L 334 432 L 72 448 Z", amount=5.5, seed="sky-wash")
    clay_block = handify("M 238 78 L 468 64 L 454 346 L 222 330 Z", amount=5.5, seed="clay-wash")

    elements = []

    # 1. Background elements behind paper shapes:
    # Subtle hand-drawn horizontal reference grid lines (dashed via bowed segments)
    grid_y1 = handify("M 92 312 L 436 309", amount=3.2, seed="grid-1")
    grid_y2 = handify("M 92 214 L 436 211", amount=3.2, seed="grid-2")
    elements.append(
        f'<path d="{grid_y1} {grid_y2}" stroke-width="5.0" stroke-dasharray="14 18" stroke-opacity="0.42"/>'
    )

    # Threshold / baseline target band line passing behind the bars
    target_line = handify("M 84 156 L 448 152", amount=3.8, seed="target-line")
    elements.append(f'<path d="{target_line}" stroke-width="5.5" stroke-dasharray="22 14"/>')

    # 2. Paper-filled data columns (4 generations: Gen 1, Gen 2, Gen 3, Gen 4 Frontier)
    # Each bar has a slight upward right-hand tilt on its top edge and an asymmetric side knot
    # so no bar or color cap is a mirror-symmetric rectangle.
    bars_spec = [
        # (x0, y_top_l, y_top_r, width, seed, highlight_top)
        (110, 326, 319, 60, "bar-1", None),
        (190, 272, 264, 60, "bar-2", None),
        (270, 218, 210, 62, "bar-3", kraft_fill),
        (352, 126, 118, 66, "bar-4", clay_fill),
    ]

    for idx, (bx, by_l, by_r, bw, bseed, accent_color) in enumerate(bars_spec):
        by_bot = 408
        mid_y = int((by_l + by_bot) * 0.58)
        # Closed paper fill for the column with an asymmetric left-wall inflection point
        bar_fill_d = handify(
            f"M {bx} {by_bot} L {bx - 2} {mid_y} L {bx} {by_l} L {bx + bw} {by_r} L {bx + bw} {by_bot} Z",
            amount=2.8,
            seed=f"{bseed}-fill",
        )
        elements.append(f'<path d="{bar_fill_d}" fill="{PAPER}" stroke="none"/>')

        # Asymmetric slanted color cap on top of key columns (drawn after paper fill, before outline)
        if accent_color:
            cap_h_l = 38 if idx == 3 else 26
            cap_h_r = 24 if idx == 3 else 16
            cap_d = handify(
                f"M {bx + 2} {by_l + cap_h_l} L {bx + 2} {by_l + 2} L {bx + bw - 2} {by_r + 2} L {bx + bw - 3} {by_r + cap_h_r} Z",
                amount=2.2,
                seed=f"{bseed}-cap",
            )
            elements.append(f'<path d="{cap_d}" fill="{accent_color}" fill-opacity="0.82" stroke="none"/>')

        # Hand-drawn column outline with architect corner overshoot
        bar_stroke_d = handify(
            f"M {bx} {by_bot} L {bx - 2} {mid_y} L {bx} {by_l} L {bx + bw} {by_r} L {bx + bw} {by_bot}",
            amount=2.8,
            overshoot=5.5,
            seed=f"{bseed}-stroke",
        )
        elements.append(f'<path d="{bar_stroke_d}" stroke-width="8.5"/>')

    # Partial diagonal pen-shading hatch lines along the left side of the frontier column
    # (stopping ~65% across so they shade the column without slicing it into closed cells)
    hatch_lines = [
        handify("M 356 218 L 392 192", amount=1.8, seed="h1"),
        handify("M 356 262 L 396 232", amount=1.8, seed="h2"),
        handify("M 356 308 L 390 282", amount=1.8, seed="h3"),
        handify("M 356 354 L 394 326", amount=1.8, seed="h4"),
    ]
    elements.append(f'<path d="{" ".join(hatch_lines)}" stroke-width="5.2"/>')

    # 3. Callout card ("2.4x" annotation badge in upper-left/center overlapping wash edge)
    # Leave a small breathing gap at the bottom-left corner of the badge outline (ends & gaps rule)
    badge_fill = handify("M 104 72 L 268 64 L 274 162 L 110 168 Z", amount=4.0, seed="badge-fill")
    badge_rim = handify(
        "M 104 144 L 104 72 L 268 64 L 274 162 L 128 168",
        amount=4.0,
        overshoot=8.5,
        seed="badge-rim",
    )
    elements.append(f'<path d="{badge_fill}" fill="{PAPER}" stroke="none"/>')
    elements.append(f'<path d="{badge_rim}" stroke-width="8.5"/>')

    # Hand-drawn centerline glyphs for "2.4x" inside the callout badge
    glyph_2 = handify("M 128 100 C 132 82 162 82 162 102 C 162 118 128 132 126 146 L 166 145", amount=1.8, seed="g2")
    glyph_dot = wobbly_circle(181, 143, 4.5, seed="gdot", wobble=0.08)
    glyph_4a = handify("M 218 88 L 194 128 L 228 127", amount=1.8, seed="g4a")
    glyph_4b = handify("M 218 88 L 217 147", amount=1.8, seed="g4b")
    # Asymmetric "x" (one stroke longer and tilted more than the other)
    glyph_x1 = handify("M 236 106 L 260 146", amount=1.8, seed="gx1")
    glyph_x2 = handify("M 258 109 L 234 141", amount=1.8, seed="gx2")
    elements.append(
        f'<path d="{glyph_2} {glyph_4a} {glyph_4b} {glyph_x1} {glyph_x2}" stroke-width="6.8"/>'
    )
    elements.append(f'<path d="{glyph_dot}" fill="{INK}" stroke-width="4.0"/>')

    # Curved pointer arrow from callout badge to the frontier peak node
    arrow_curve = handify("M 276 112 C 312 96 340 92 364 100", amount=3.0, seed="callout-arrow")
    arrow_head = handify("M 346 84 L 367 101 L 349 113", amount=2.0, seed="callout-head")
    elements.append(f'<path d="{arrow_curve} {arrow_head}" stroke-width="6.0"/>')

    # 4. Axes with architect-style corner overshoot and varied tick marks
    y_axis = handify("M 92 64 L 92 430", amount=3.5, seed="y-axis")
    x_axis = handify("M 70 408 L 456 408", amount=3.5, seed="x-axis")
    y_axis_cap = handify("M 79 84 L 92 62 L 103 80", amount=2.2, seed="y-cap")
    elements.append(f'<path d="{y_axis} {x_axis} {y_axis_cap}" stroke-width="9.0"/>')

    # Varied tick marks along Y and X axes
    ticks = [
        handify("M 81 312 L 101 311", amount=1.8, seed="ty1"),
        handify("M 79 214 L 102 213", amount=1.8, seed="ty2"),
        handify("M 82 126 L 100 127", amount=1.8, seed="ty3"),
        handify("M 140 402 L 139 421", amount=1.8, seed="tx1"),
        handify("M 220 403 L 221 423", amount=1.8, seed="tx2"),
        handify("M 301 401 L 300 420", amount=1.8, seed="tx3"),
        handify("M 385 402 L 386 424", amount=1.8, seed="tx4"),
    ]
    elements.append(f'<path d="{" ".join(ticks)}" stroke-width="6.0"/>')

    # 5. Rising hand-drawn growth trajectory curve + wobbly data nodes in front of the columns
    nodes = [(140, 298), (220, 244), (301, 186), (385, 96)]
    curve_d = handify(
        "M 140 298 C 172 282 194 262 220 244 C 252 222 274 208 301 186 C 332 160 358 126 385 96",
        amount=3.5,
        seed="growth-curve",
    )
    elements.append(f'<path d="{curve_d}" stroke-width="8.5"/>')

    for i, (nx, ny) in enumerate(nodes):
        r = 12.0 if i == 3 else 10.5
        node_d = wobbly_circle(nx, ny, r, seed=f"node-{i}", wobble=0.09)
        node_fill = clay_fill if i == 3 else PAPER
        elements.append(f'<path d="{node_d}" fill="{node_fill}" stroke-width="8.0"/>')

    # 6. Clustered sparkle accent at the peak data point (3 sparkles in 1 : 0.65 : 0.45 ratio + 1 small dot)
    sp1 = sparkle(436, 64, 21, seed="sp-peak-1")
    sp2 = sparkle(468, 100, 13.5, seed="sp-peak-2")
    sp3 = sparkle(410, 44, 10.0, seed="sp-peak-3")
    dot1 = wobbly_circle(456, 60, 3.8, seed="dot-peak-1")
    elements.append(f'<path d="{sp1} {sp2} {sp3}" stroke-width="5.5"/>')
    elements.append(f'<path d="{dot1}" fill="{INK}" stroke-width="3.5"/>')

    ink_markup = "\n  ".join(elements)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{wash_filter_defs(seed_a=23, seed_b=61, ink_seed=83)}
<g id="layer-block" style="isolation:isolate">
  <g filter="url(#wash-a)">
    <path d="{sky_block}" fill="{sky_fill}"/>
    <path d="{sky_block}" fill="none" stroke="{sky_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g filter="url(#wash-b)" style="mix-blend-mode:multiply">
    <path d="{clay_block}" fill="{clay_fill}"/>
    <path d="{clay_block}" fill="none" stroke="{clay_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  {ink_markup}
</g>
</svg>
"""


def wobbly_arc(cx, cy, r, deg_start, deg_end, steps=7, wobble=0.035, seed="arc"):
    """Hand-drawn circular arc path from deg_start to deg_end."""
    rng = random.Random(f"{seed}:{cx}:{cy}:{r}:{deg_start}:{deg_end}")
    pts = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        ri = r * (1.0 + rng.uniform(-wobble, wobble))
        pts.append((cx + ri * math.cos(ang), cy + ri * math.sin(ang)))
    d_raw = f"M {fmt(pts[0])} " + " ".join(f"L {fmt(p)}" for p in pts[1:])
    return handify(d_raw, amount=2.6, seed=f"{seed}-h")


def build_telemetry_kpi_card():
    """Editorial KPI / Gauge & Sparkline Summary Card (512x512 viewBox).

    Subject: Layered telemetry card pairing a semicircle velocity gauge dial
    (upper-left card) with a rising area/line sparkline card (lower-right card)
    and a status pill tag.
    Washes:
      - Cool mineral wash tilted behind the upper-left gauge card
      - Warm peach wash behind the lower-right sparkline card, overlapping with multiply
    """
    mineral_fill, mineral_edge = COLORS["mineral"]
    peach_fill, peach_edge = COLORS["peach"]
    clay_fill, _ = COLORS["clay"]

    mineral_block = handify("M 48 68 L 336 52 L 318 326 L 64 344 Z", amount=5.5, seed="mineral-wash")
    peach_block = handify("M 188 198 L 464 182 L 448 456 L 172 442 Z", amount=5.5, seed="peach-wash")

    elements = []

    # 1. Background element behind the main cards:
    # A tilted secondary reference sheet / shadow card peeking out at top-right and left leads
    back_sheet = handify("M 96 46 L 372 38 L 376 112", amount=4.0, overshoot=8.0, seed="back-sheet-top")
    back_cables = handify("M 48 228 L 82 226 M 44 264 L 82 262", amount=2.5, seed="telemetry-leads")
    elements.append(f'<path d="{back_sheet} {back_cables}" stroke-width="6.0"/>')

    # 2. Primary Paper Card A (Upper-Left: Gauge / Dial Card)
    card_a_fill = handify("M 74 78 L 358 72 L 364 304 L 78 310 Z", amount=4.2, seed="card-a-fill")
    card_a_stroke = handify(
        "M 74 78 L 358 72 L 364 304 L 78 310 L 74 78",
        amount=4.2,
        overshoot=10.0,
        seed="card-a-stroke",
    )
    elements.append(f'<path d="{card_a_fill}" fill="{PAPER}" stroke="none"/>')
    elements.append(f'<path d="{card_a_stroke}" stroke-width="8.5"/>')

    # Gauge Dial inside Card A (center at cx=218, cy=242)
    gx, gy = 218, 242
    # Coloured active zone wedge on the right side of the gauge (from -58 deg to -10 deg)
    wedge_outer = wobbly_arc(gx, gy, 104, -58, -10, steps=5, seed="wedge-out")
    wedge_inner_pts = []
    for ang_d in (-10, -34, -58):
        ang = math.radians(ang_d)
        wedge_inner_pts.append((gx + 66 * math.cos(ang), gy + 66 * math.sin(ang)))
    wedge_fill_d = (
        f"{wedge_outer} L {fmt(wedge_inner_pts[0])} "
        f"L {fmt(wedge_inner_pts[1])} L {fmt(wedge_inner_pts[2])} Z"
    )
    elements.append(f'<path d="{wedge_fill_d}" fill="{clay_fill}" fill-opacity="0.85" stroke="none"/>')

    # Outer and inner hand-drawn gauge arcs: inner arc stops before the needle (-56 deg) for breathing room
    outer_arc = wobbly_arc(gx, gy, 104, -172, -8, steps=9, seed="gauge-outer")
    inner_arc = wobbly_arc(gx, gy, 62, -168, -56, steps=6, seed="gauge-inner")
    # Radial scale ticks sitting along the outer gauge rim
    gauge_ticks = []
    for idx, ang_d in enumerate((-168, -132, -92, -54, -12)):
        a = math.radians(ang_d)
        r0 = 90 if idx % 2 == 0 else 93
        r1 = 116 if idx % 2 == 0 else 113
        p0 = (gx + r0 * math.cos(a), gy + r0 * math.sin(a))
        p1 = (gx + r1 * math.cos(a), gy + r1 * math.sin(a))
        gauge_ticks.append(handify(f"M {fmt(p0)} L {fmt(p1)}", amount=1.6, seed=f"gtick-{idx}"))

    elements.append(f'<path d="{outer_arc}" stroke-width="8.5"/>')
    elements.append(f'<path d="{inner_arc} {" ".join(gauge_ticks)}" stroke-width="5.8"/>')

    # Hand-drawn gauge needle pointing into the high-velocity zone (-34 deg)
    needle_ang = math.radians(-34)
    nx_tip = gx + 96 * math.cos(needle_ang)
    ny_tip = gy + 96 * math.sin(needle_ang)
    nx_tail = gx - 22 * math.cos(needle_ang)
    ny_tail = gy - 22 * math.sin(needle_ang)
    needle_d = handify(f"M {fmt((nx_tail, ny_tail))} L {fmt((nx_tip, ny_tip))}", amount=2.2, seed="needle")
    hub_d = wobbly_circle(gx, gy, 11.5, seed="gauge-hub", wobble=0.09)
    elements.append(f'<path d="{needle_d}" stroke-width="8.5"/>')
    elements.append(f'<path d="{hub_d}" fill="{PAPER}" stroke-width="8.0"/>')

    # Small header bars / telemetry readout marks inside top-left of Card A
    hdr_1 = handify("M 102 104 L 166 102", amount=2.0, seed="hdr-1")
    hdr_2 = handify("M 104 124 L 146 123", amount=2.0, seed="hdr-2")
    elements.append(f'<path d="{hdr_1} {hdr_2}" stroke-width="6.0"/>')

    # 3. Primary Paper Card B (Lower-Right overlapping Card A: Sparkline & KPI trend card)
    card_b_fill = handify("M 164 258 L 444 250 L 450 436 L 170 442 Z", amount=4.2, seed="card-b-fill")
    card_b_stroke = handify(
        "M 164 258 L 444 250 L 450 436 L 170 442 L 164 258",
        amount=4.2,
        overshoot=10.0,
        seed="card-b-stroke",
    )
    elements.append(f'<path d="{card_b_fill}" fill="{PAPER}" stroke="none"/>')
    elements.append(f'<path d="{card_b_stroke}" stroke-width="8.5"/>')

    # Soft tinted area fill under the sparkline inside Card B
    area_raw = (
        "M 194 408 L 194 392 L 242 366 L 288 380 L 338 332 L 384 342 L 420 292 L 420 408 Z"
    )
    area_d = handify(area_raw, amount=2.8, seed="spark-area")
    elements.append(f'<path d="{area_d}" fill="{mineral_fill}" fill-opacity="0.35" stroke="none"/>')

    # Sparkline baseline & rising jagged trajectory
    spark_base = handify("M 188 408 L 428 406", amount=2.5, seed="spark-base")
    spark_line = handify(
        "M 194 392 L 242 366 L 288 380 L 338 332 L 384 342 L 420 292",
        amount=2.8,
        seed="spark-line",
    )
    elements.append(f'<path d="{spark_base}" stroke-width="5.2"/>')
    elements.append(f'<path d="{spark_line}" stroke-width="8.0"/>')

    # Prominent peak node and start/mid nodes on the sparkline
    sp_node_start = wobbly_circle(194, 392, 9.5, seed="sp-node-0", wobble=0.08)
    sp_node_mid = wobbly_circle(338, 332, 10.0, seed="sp-node-1", wobble=0.08)
    sp_node_peak = wobbly_circle(420, 292, 11.5, seed="sp-node-2", wobble=0.09)
    elements.append(f'<path d="{sp_node_start} {sp_node_mid}" fill="{PAPER}" stroke-width="7.0"/>')
    elements.append(f'<path d="{sp_node_peak}" fill="{clay_fill}" stroke-width="8.0"/>')

    # Asymmetric tilted "+" and diagonal north-east trend arrow in the upper-left corner of Card B
    plus_v = handify("M 201 280 L 195 316", amount=1.6, seed="plus-v")
    plus_h = handify("M 185 301 L 216 293", amount=1.6, seed="plus-h")
    up_stem = handify("M 234 320 L 262 282", amount=1.8, seed="up-stem")
    up_arrow = handify("M 240 286 L 263 281 L 260 306", amount=1.8, seed="up-arr")
    metric_bar1 = handify("M 284 290 L 356 287", amount=2.0, seed="mbar-1")
    metric_bar2 = handify("M 286 310 L 332 308", amount=2.0, seed="mbar-2")
    elements.append(
        f'<path d="{plus_v} {plus_h} {up_stem} {up_arrow} {metric_bar1} {metric_bar2}" stroke-width="6.2"/>'
    )

    # 4. Foreground overlapping status badge pill across Card A / Card B seam (left side)
    # Leave a small breathing gap at the bottom-left of the pill outline (ends & gaps rule)
    pill_fill = handify("M 56 342 L 144 338 L 146 392 L 58 396 Z", amount=3.2, seed="pill-fill")
    pill_stroke = handify(
        "M 56 376 L 56 342 L 144 338 L 146 392 L 74 396",
        amount=3.2,
        overshoot=5.0,
        seed="pill-stroke",
    )
    check_mark = handify("M 78 368 L 94 382 L 126 352", amount=2.0, seed="pill-check")
    elements.append(f'<path d="{pill_fill}" fill="{PAPER}" stroke="none"/>')
    elements.append(f'<path d="{pill_stroke}" stroke-width="8.0"/>')
    elements.append(f'<path d="{check_mark}" stroke-width="6.5"/>')

    # 5. Clustered sparkles in the upper-right quiet space (3 sparkles + 1 small dot)
    sp1 = sparkle(422, 96, 20, seed="kpi-sp-1")
    sp2 = sparkle(454, 130, 13, seed="kpi-sp-2")
    sp3 = sparkle(396, 128, 9.5, seed="kpi-sp-3")
    dot = wobbly_circle(444, 86, 4.0, seed="kpi-dot-1")
    elements.append(f'<path d="{sp1} {sp2} {sp3}" stroke-width="5.5"/>')
    elements.append(f'<path d="{dot}" fill="{INK}" stroke-width="3.5"/>')

    ink_markup = "\n  ".join(elements)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{wash_filter_defs(seed_a=31, seed_b=67, ink_seed=89)}
<g id="layer-block" style="isolation:isolate">
  <g filter="url(#wash-a)">
    <path d="{mineral_block}" fill="{mineral_fill}"/>
    <path d="{mineral_block}" fill="none" stroke="{mineral_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g filter="url(#wash-b)" style="mix-blend-mode:multiply">
    <path d="{peach_block}" fill="{peach_fill}"/>
    <path d="{peach_block}" fill="none" stroke="{peach_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  {ink_markup}
</g>
</svg>
"""


def main():
    out_dir = SCRIPT_DIR
    bench_path = os.path.join(out_dir, "benchmark-comparison.svg")
    kpi_path = os.path.join(out_dir, "telemetry-kpi-card.svg")

    with open(bench_path, "w") as f:
        f.write(build_benchmark_comparison())
    print(f"Wrote {bench_path}")

    with open(kpi_path, "w") as f:
        f.write(build_telemetry_kpi_card())
    print(f"Wrote {kpi_path}")


if __name__ == "__main__":
    main()
