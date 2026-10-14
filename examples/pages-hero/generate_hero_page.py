#!/usr/bin/env python3
"""Generate Track 6 deliverables: AI-Designed Editorial Product Hero Landing Page.

Produces inside /Users/wu/CC-lineart/examples/pages-hero/:
  1. hero-centerpiece.svg     (512x512 flagship illustration: "The Sketchbook Cloud / Autonomous Studio")
  2. hero-centerpiece.png     (512x512 rasterized preview via rsvg-convert)
  3. hero-landing-page.html   (Complete interactive Editorial Product Hero Landing Page)
"""
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lineart import COLORS, INK, PAPER, fmt, handify, sparkle, wobbly_circle  # noqa: E402


def hpath(d, amount=5.0, overshoot=0.0, seed="hero"):
    """512-grid wrapper around lineart.handify."""
    return handify(d, amount=amount, overshoot=overshoot, seed=seed)


def poly_d(pts, closed=True):
    head = f"M{fmt(pts[0])}"
    body = " ".join(f"L{fmt(p)}" for p in pts[1:])
    return f"{head} {body}" + (" Z" if closed else "")


def starburst_rays(cx, cy, r_inner, r_outer, seed="burst"):
    """7-ray Claude-style irregular starburst computed via trig."""
    angles = [-92, -36, 10, 54, 101, 148, 198]
    scales = [1.15, 0.85, 1.10, 0.89, 1.17, 0.84, 1.04]
    segs = []
    for idx, (deg, sc) in enumerate(zip(angles, scales)):
        rad = math.radians(deg)
        r0 = r_inner * (0.87 + 0.05 * (idx % 3))
        r1 = r_outer * sc
        x0, y0 = cx + r0 * math.cos(rad), cy + r0 * math.sin(rad)
        x1, y1 = cx + r1 * math.cos(rad), cy + r1 * math.sin(rad)
        segs.append(hpath(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", amount=2.2, seed=f"{seed}-{idx}"))
    return " ".join(segs)


def build_defs(seed_wash=41, seed_ink=59):
    """512x512 scaled watercolor wash and ink wobble filters."""
    return f"""<defs>
<filter id="wash" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="4" seed="{seed_wash}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="13" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.1 1.45" result="a"/>
  <feComposite in="d" in2="a" operator="in"/>
</filter>
<filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="{seed_ink}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6.2" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>"""


def build_hero_centerpiece_svg():
    """Generate `hero-centerpiece.svg` (512x512): 'The Sketchbook Cloud / Autonomous Studio'.

    Composition:
      - Layer 1 (`#layer-block`): Overlapping cool `sky` wash (lower-left/center), warm `peach`
        wash (upper-right/center) with `mix-blend-mode: multiply`, and a focal `clay` pool
        behind the verification badge.
      - Layer 2 & 3 (`#layer-ink`):
        1. Tilted Architect's Sketchbook + Drafting Fountain Pen breaking out lower-left.
        2. Autonomous Studio Cloud Workbench window in the center (skewed quadrilateral,
           reasoning starburst, asymmetric node flow & scribble bars).
        3. Floating Shipped UI Artifact Card + Wobbly Verification Seal breaking out upper-right.
    """
    sky_fill, sky_edge = COLORS["sky"]
    peach_fill, peach_edge = COLORS["peach"]
    clay_fill, clay_edge = COLORS["clay"]
    olive_fill, _ = COLORS["olive"]

    # Layer 1: Glazed watercolor blocks (coverage ~28%, offset from center)
    wash_sky = hpath("M 64 238 L 284 212 L 298 446 L 78 462 Z", amount=7.2, seed="hc-wash-sky")
    wash_peach = hpath("M 188 106 L 434 86 L 448 326 L 204 344 Z", amount=7.2, seed="hc-wash-peach")
    wash_clay = wobbly_circle(406, 118, 44, seed="hc-wash-clay", wobble=0.07, overlap=14)

    # Background drafting arcs & connector splines passing behind paper shapes
    bg_orbit_arc = hpath("M 32 426 C 118 446 196 394 252 324", amount=4.0, seed="hc-bg-arc")
    conn_sketch_to_studio = hpath("M 172 332 C 208 314 220 274 246 254", amount=3.8, seed="hc-conn-1")
    conn_studio_to_ship = hpath("M 336 194 C 364 168 378 138 400 124", amount=3.8, seed="hc-conn-2")
    horizon_reg = hpath("M 424 78 C 454 52 476 36 496 22", amount=3.2, seed="hc-swoosh")

    # 1. Lower-Left: Tilted Architect's Sketchbook + Fountain Pen (breaks out lower-left of wash)
    sketch_fill = hpath("M 30 288 L 182 268 L 198 458 L 46 476 Z", amount=5.4, seed="hc-sk-fill")
    sketch_out_a = hpath("M 28 294 L 30 288 L 182 268 L 198 458", amount=4.8, overshoot=11.0, seed="hc-sk-oa")
    sketch_out_b = hpath("M 198 458 L 46 476 L 30 288", amount=4.8, overshoot=10.0, seed="hc-sk-ob")
    sketch_spine = hpath("M 56 286 L 70 468", amount=3.2, seed="hc-sk-spine")
    sketch_dogear = hpath("M 150 272 L 156 306 L 188 298", amount=3.0, seed="hc-sk-dog")
    sketch_scribble_1 = hpath("M 78 332 C 106 318 134 342 164 326", amount=2.8, seed="hc-sk-w1")
    sketch_scribble_2 = hpath("M 82 366 C 110 354 132 374 156 362", amount=2.8, seed="hc-sk-w2")
    sketch_box = hpath("M 84 398 L 128 388 L 118 428 L 78 418", amount=3.0, overshoot=5.0, seed="hc-sk-box")
    sketch_curve = hpath("M 124 408 C 140 398 152 416 168 402", amount=2.4, seed="hc-sk-crv")

    # Drafting Fountain Pen crossing lower-right of sketchbook
    pen_body = hpath("M 138 440 L 226 366 L 242 382 L 154 456 Z", amount=3.4, seed="hc-pen-b")
    pen_nib = hpath("M 138 440 L 114 470 L 154 456", amount=2.5, seed="hc-pen-nib")
    pen_ring = hpath("M 200 388 L 216 404", amount=2.0, seed="hc-pen-ring")
    pen_clip = hpath("M 214 374 L 244 350 L 250 358", amount=2.2, seed="hc-pen-clip")

    # 2. Center: Autonomous Studio Cloud Workbench Window (skewed quadrilateral)
    studio_fill = hpath("M 174 162 L 362 146 L 376 320 L 188 336 Z", amount=5.6, seed="hc-st-fill")
    studio_out_top = hpath("M 174 162 L 362 146 L 376 320", amount=4.8, overshoot=12.0, seed="hc-st-ot")
    studio_out_bot = hpath("M 376 320 L 188 336 L 174 162", amount=4.8, overshoot=11.0, seed="hc-st-ob")
    studio_hdr = hpath("M 180 200 L 364 184", amount=3.8, seed="hc-st-hdr")
    # Terminal prompt chevron & baseline
    prompt_chev = hpath("M 202 232 L 224 246 L 204 264", amount=2.6, seed="hc-st-chev")
    prompt_base = hpath("M 234 266 L 268 262", amount=2.4, seed="hc-st-base")
    # Claude reasoning starburst inside studio workbench
    burst_d = starburst_rays(312, 248, 12, 35, seed="hc-st-burst")
    studio_bar_1 = hpath("M 204 292 L 278 286", amount=2.8, seed="hc-st-b1")
    studio_bar_2 = hpath("M 206 310 L 258 306", amount=2.8, seed="hc-st-b2")

    # 3. Upper-Right: Floating Shipped UI Artifact Card + Verification Seal
    ship_fill = hpath("M 302 38 L 486 22 L 498 178 L 314 194 Z", amount=5.4, seed="hc-sh-fill")
    ship_out_1 = hpath("M 302 38 L 486 22 L 498 178", amount=4.8, overshoot=11.0, seed="hc-sh-o1")
    ship_out_2 = hpath("M 498 178 L 314 194 L 302 38", amount=4.8, overshoot=10.0, seed="hc-sh-o2")
    seal_circle = wobbly_circle(416, 102, 38, seed="hc-seal-c", wobble=0.06, overlap=15)
    seal_check = hpath("M 398 104 L 412 118 L 438 84", amount=2.6, seed="hc-seal-chk")
    ship_line_1 = hpath("M 324 74 L 364 70", amount=2.5, seed="hc-sh-l1")
    ship_line_2 = hpath("M 326 102 L 356 98", amount=2.5, seed="hc-sh-l2")
    ship_line_3 = hpath("M 330 154 L 466 142", amount=3.4, seed="hc-sh-l3")

    # 4. Foreground flow arrows bridging the 3 tiers
    fg_arr_1 = hpath("M 162 314 C 190 282 212 266 238 254", amount=3.4, seed="hc-fga1")
    fg_arr_1_h = hpath("M 222 248 L 240 253 L 228 270", amount=2.2, seed="hc-fga1-h")
    fg_arr_2 = hpath("M 326 194 C 346 166 362 142 380 126", amount=3.4, seed="hc-fga2")
    fg_arr_2_h = hpath("M 362 124 L 382 124 L 374 142", amount=2.2, seed="hc-fga2-h")

    # 5. Quiet-area sparkles (Upper-Left cluster + 1 echo lower-right)
    sp_1 = sparkle(86, 94, 22, seed="hc-sp1")
    sp_2 = sparkle(128, 72, 14, seed="hc-sp2")
    sp_3 = sparkle(66, 134, 10, seed="hc-sp3")
    sp_4 = sparkle(448, 418, 13, seed="hc-sp4")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{build_defs(seed_wash=41, seed_ink=59)}
<g id="layer-block" filter="url(#wash)" style="isolation: isolate">
  <g class="wash-blob wash-cool">
    <path id="hero-wash-cool-fill" d="{wash_sky}" fill="{sky_fill}"/>
    <path id="hero-wash-cool-edge" d="{wash_sky}" fill="none" stroke="{sky_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g class="wash-blob wash-warm" style="mix-blend-mode: multiply">
    <path id="hero-wash-warm-fill" d="{wash_peach}" fill="{peach_fill}"/>
    <path id="hero-wash-warm-edge" d="{wash_peach}" fill="none" stroke="{peach_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g class="wash-blob wash-focal">
    <path id="hero-wash-focal-fill" d="{wash_clay}" fill="{clay_fill}"/>
    <path id="hero-wash-focal-edge" d="{wash_clay}" fill="none" stroke="{clay_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Background trajectory & registration arcs -->
  <path class="draw-stroke" data-step="1" pathLength="1" d="{bg_orbit_arc}" stroke-width="4.5" stroke-dasharray="14 16"/>
  <path class="draw-stroke" data-step="2" pathLength="1" d="{conn_sketch_to_studio}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="3" pathLength="1" d="{conn_studio_to_ship}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="4" pathLength="1" d="{horizon_reg}" stroke-width="4.5"/>

  <!-- Act I: Tilted Architect's Sketchbook (Lower-Left) -->
  <path class="paper-fill" data-step="5" d="{sketch_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="6" pathLength="1" d="{sketch_out_a}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="7" pathLength="1" d="{sketch_out_b}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="8" pathLength="1" d="{sketch_spine}" stroke-width="4.5"/>
  <path class="draw-stroke" data-step="9" pathLength="1" d="{sketch_dogear}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="10" pathLength="1" d="{sketch_scribble_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="11" pathLength="1" d="{sketch_scribble_2}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="12" pathLength="1" d="{sketch_box}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="13" pathLength="1" d="{sketch_curve}" stroke-width="4.5"/>

  <!-- Drafting Fountain Pen -->
  <path class="paper-fill" data-step="14" d="{pen_body}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="15" pathLength="1" d="{pen_body}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="16" pathLength="1" d="{pen_nib}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="17" pathLength="1" d="{pen_ring}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="18" pathLength="1" d="{pen_clip}" stroke-width="4.5"/>

  <!-- Act II: Autonomous Studio Cloud Workbench (Center) -->
  <path class="paper-fill" data-step="19" d="{studio_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="20" pathLength="1" d="{studio_out_top}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="21" pathLength="1" d="{studio_out_bot}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="22" pathLength="1" d="{studio_hdr}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="23" pathLength="1" d="{prompt_chev}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="24" pathLength="1" d="{prompt_base}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="25" pathLength="1" d="{burst_d}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="26" pathLength="1" d="{studio_bar_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="27" pathLength="1" d="{studio_bar_2}" stroke-width="4.5"/>

  <!-- Act III: Shipped UI Artifact Card + Verification Seal (Upper-Right) -->
  <path class="paper-fill" data-step="28" d="{ship_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="29" pathLength="1" d="{ship_out_1}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="30" pathLength="1" d="{ship_out_2}" stroke-width="8.5"/>
  <path class="paper-fill" data-step="31" id="hero-seal-tint" d="{seal_circle}" fill="{clay_fill}" fill-opacity="0.28" stroke="none"/>
  <path class="draw-stroke" data-step="32" pathLength="1" d="{seal_circle}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="33" pathLength="1" d="{seal_check}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="34" pathLength="1" d="{ship_line_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="35" pathLength="1" d="{ship_line_2}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="36" pathLength="1" d="{ship_line_3}" stroke-width="6.0"/>

  <!-- Foreground bridging arrows -->
  <path class="draw-stroke" data-step="37" pathLength="1" d="{fg_arr_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="38" pathLength="1" d="{fg_arr_1_h}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="39" pathLength="1" d="{fg_arr_2}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="40" pathLength="1" d="{fg_arr_2_h}" stroke-width="6.0"/>

  <!-- Quiet-area sparkles & ink dots -->
  <path class="draw-stroke" data-step="41" pathLength="1" d="{sp_1}" stroke-width="4.5"/>
  <path class="draw-stroke" data-step="42" pathLength="1" d="{sp_2}" stroke-width="4.5"/>
  <path class="draw-stroke" data-step="43" pathLength="1" d="{sp_3}" stroke-width="4.5"/>
  <path class="draw-stroke" data-step="44" pathLength="1" d="{sp_4}" stroke-width="4.5"/>
  <circle class="paper-fill" data-step="45" cx="148" cy="112" r="4.5" fill="{INK}" stroke="none"/>
  <circle class="paper-fill" data-step="46" cx="56" cy="92" r="3.8" fill="{olive_fill}" stroke="none"/>
</g>
</svg>
"""


def build_bento_mini_svg_1():
    """Mini CC-lineart illustration for Card 1: Zero-Template Vector Synthesis."""
    w_sky = handify("M 18 24 L 116 16 L 124 88 L 24 96 Z", amount=2.2, seed="b1-w")
    card_d = handify("M 32 22 L 138 14 L 146 86 L 38 94 Z", amount=1.8, seed="b1-c")
    curve_d = handify("M 46 72 C 68 32 104 82 128 36", amount=1.5, seed="b1-crv")
    handle_1 = handify("M 46 72 L 66 36", amount=1.2, seed="b1-h1")
    handle_2 = handify("M 128 36 L 106 72", amount=1.2, seed="b1-h2")
    pt_a = wobbly_circle(66, 36, 5.5, seed="b1-pa")
    pt_b = wobbly_circle(106, 72, 5.5, seed="b1-pb")
    sp = sparkle(22, 26, 7, seed="b1-sp")
    return f"""<svg viewBox="0 0 168 112" class="bento-mini-svg" aria-hidden="true">
  <g class="mini-wash" filter="url(#ui-wash)">
    <path d="{w_sky}" fill="{COLORS['sky'][0]}"/>
    <path d="{w_sky}" fill="none" stroke="{COLORS['sky'][1]}" stroke-width="1.8" stroke-opacity="0.55"/>
  </g>
  <g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{card_d}" fill="{PAPER}" stroke-width="3.0"/>
    <path d="{handle_1}" stroke-width="2.0" stroke-dasharray="4 4"/>
    <path d="{handle_2}" stroke-width="2.0" stroke-dasharray="4 4"/>
    <path d="{curve_d}" stroke-width="3.2"/>
    <path d="{pt_a}" fill="{COLORS['clay'][0]}" stroke-width="2.4"/>
    <path d="{pt_b}" fill="{COLORS['peach'][0]}" stroke-width="2.4"/>
    <path d="{sp}" stroke-width="2.0"/>
  </g>
</svg>"""


def build_bento_mini_svg_2():
    """Mini CC-lineart illustration for Card 2: Glazed Watercolor Layers."""
    w_warm = handify("M 20 26 L 106 16 L 114 86 L 28 94 Z", amount=2.4, seed="b2-w1")
    w_cool = handify("M 56 18 L 146 28 L 138 96 L 48 86 Z", amount=2.4, seed="b2-w2")
    swatch_card = handify("M 42 32 L 128 24 L 134 82 L 48 90 Z", amount=1.8, seed="b2-card")
    drop = wobbly_circle(88, 56, 15, seed="b2-drop")
    wave = handify("M 62 72 C 78 64 98 76 116 66", amount=1.4, seed="b2-wv")
    sp = sparkle(144, 22, 7.5, seed="b2-sp")
    return f"""<svg viewBox="0 0 168 112" class="bento-mini-svg" aria-hidden="true">
  <g class="mini-wash" filter="url(#ui-wash)" style="isolation:isolate">
    <path d="{w_warm}" fill="{COLORS['clay'][0]}"/>
    <path d="{w_cool}" fill="{COLORS['sky'][0]}" style="mix-blend-mode:multiply"/>
  </g>
  <g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{swatch_card}" fill="{PAPER}" stroke-width="3.0"/>
    <path d="{drop}" fill="{COLORS['peach'][0]}" stroke-width="2.6"/>
    <path d="{wave}" stroke-width="2.2"/>
    <path d="{sp}" stroke-width="2.0"/>
  </g>
</svg>"""


def build_bento_mini_svg_3():
    """Mini CC-lineart illustration for Card 3: Deterministic Lint Gate."""
    w_cac = handify("M 22 20 L 126 14 L 134 88 L 30 96 Z", amount=2.2, seed="b3-w")
    frame_d = handify("M 34 18 L 142 26 L 134 92 L 28 84 Z", amount=1.8, seed="b3-f")
    seal_d = wobbly_circle(86, 54, 21, seed="b3-seal")
    chk_d = handify("M 75 55 L 84 64 L 100 43", amount=1.5, seed="b3-chk")
    sp = sparkle(148, 26, 7.5, seed="b3-sp")
    return f"""<svg viewBox="0 0 168 112" class="bento-mini-svg" aria-hidden="true">
  <g class="mini-wash" filter="url(#ui-wash)">
    <path d="{w_cac}" fill="{COLORS['cactus'][0]}"/>
    <path d="{w_cac}" fill="none" stroke="{COLORS['cactus'][1]}" stroke-width="1.8" stroke-opacity="0.55"/>
  </g>
  <g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{frame_d}" fill="{PAPER}" stroke-width="3.0"/>
    <path d="{seal_d}" fill="{COLORS['olive'][0]}" fill-opacity="0.25" stroke-width="2.8"/>
    <path d="{chk_d}" stroke-width="3.2"/>
    <path d="{sp}" stroke-width="2.0"/>
  </g>
</svg>"""


def build_landing_page_html(centerpiece_svg):
    """Build `hero-landing-page.html` embedding the live self-drawing centerpiece SVG and UI kit."""
    # Hand-drawn container paths for buttons, badges, bento cards, pricing cards, and wax seal
    badge_wash = handify("M 10 8 L 258 4 L 264 38 L 14 42 Z", amount=1.8, seed="lp-bdg-w")
    badge_box = handify("M 6 6 L 254 4 L 258 36 L 8 38 Z", amount=1.5, seed="lp-bdg-b")

    cta_pri_wash = handify("M 12 10 L 236 6 L 242 54 L 16 58 Z", amount=2.2, seed="lp-ctap-w")
    cta_pri_box = handify("M 6 6 L 232 4 L 236 50 L 8 52 Z", amount=1.8, seed="lp-ctap-b")

    cta_sec_wash = handify("M 12 10 L 206 6 L 212 54 L 16 58 Z", amount=2.2, seed="lp-ctas-w")
    cta_sec_box = handify("M 6 6 L 202 4 L 206 50 L 8 52 Z", amount=1.8, seed="lp-ctas-b")

    bento_wash_1 = handify("M 18 16 L 352 10 L 362 268 L 24 276 Z", amount=3.2, seed="lp-bw1")
    bento_box_1 = handify("M 10 10 L 346 6 L 352 260 L 12 266 Z", amount=2.5, seed="lp-bb1")

    bento_wash_2 = handify("M 16 14 L 354 18 L 348 274 L 20 268 Z", amount=3.2, seed="lp-bw2")
    bento_box_2 = handify("M 10 8 L 348 12 L 344 264 L 12 260 Z", amount=2.5, seed="lp-bb2")

    bento_wash_3 = handify("M 20 14 L 356 10 L 360 272 L 18 276 Z", amount=3.2, seed="lp-bw3")
    bento_box_3 = handify("M 10 10 L 346 6 L 350 262 L 14 266 Z", amount=2.5, seed="lp-bb3")

    price_wash_1 = handify("M 18 16 L 432 10 L 440 368 L 24 376 Z", amount=3.6, seed="lp-pw1")
    price_box_1 = handify("M 10 10 L 424 6 L 430 358 L 14 364 Z", amount=2.8, seed="lp-pb1")

    price_wash_2 = handify("M 18 14 L 436 18 L 430 374 L 16 368 Z", amount=3.6, seed="lp-pw2")
    price_box_2 = handify("M 10 8 L 428 12 L 422 362 L 12 356 Z", amount=2.8, seed="lp-pb2")

    wax_outer = wobbly_circle(58, 58, 44, seed="wax-out", wobble=0.08, overlap=16)
    wax_inner = wobbly_circle(58, 58, 33, seed="wax-in", wobble=0.05, overlap=12)
    wax_star = sparkle(58, 42, 9, seed="wax-sp")

    nav_ul = handify("M 2 6 C 28 2 62 9 94 4", amount=1.2, seed="nav-ul")
    margin_arr_1 = handify("M 6 28 C 28 10 56 8 82 20", amount=1.8, seed="m-arr-1")
    margin_arr_1_h = handify("M 70 12 L 84 21 L 68 27", amount=1.2, seed="m-arr-1h")
    margin_arr_2 = handify("M 8 10 C 34 26 62 28 88 14", amount=1.8, seed="m-arr-2")
    margin_arr_2_h = handify("M 74 9 L 90 13 L 78 24", amount=1.2, seed="m-arr-2h")

    chk_path = handify("M 4 11 L 9 16 L 19 5", amount=1.1, seed="chk-item")

    bento_svg_1 = build_bento_mini_svg_1()
    bento_svg_2 = build_bento_mini_svg_2()
    bento_svg_3 = build_bento_mini_svg_3()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Atelier Claude — Autonomous Design &amp; Reasoning Studio (CC-lineart Track 6)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<style>
  :root {{
    --bg-cream: #FAF6F0;
    --paper: #FAF9F5;
    --paper-card: #FFFEFA;
    --ink: #141413;
    --ink-muted: #57544E;
    --clay: #D97757;
    --clay-edge: #B85C3E;
    --sky: #6A9BCC;
    --sky-edge: #4C7FB3;
    --cactus: #BCD1CA;
    --cactus-edge: #93B0A6;
    --heather: #CBCADB;
    --plum: #827DBD;
    --mineral: #629987;
    --peach: #EBC9B7;
    --kraft: #D4A27F;
    --olive: #788C5D;
    --serif: 'Newsreader', 'Source Serif 4', Georgia, serif;
    --sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono: 'IBM Plex Mono', monospace;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    margin: 0;
    background-color: var(--bg-cream);
    background-image:
      radial-gradient(rgba(20, 20, 19, 0.04) 1px, transparent 0),
      radial-gradient(rgba(217, 119, 87, 0.05) 1px, transparent 0);
    background-size: 28px 28px;
    background-position: 0 0, 14px 14px;
    color: var(--ink);
    font-family: var(--sans);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
  }}

  .svg-defs-bank {{
    position: absolute;
    width: 0;
    height: 0;
    overflow: hidden;
    pointer-events: none;
  }}

  .page-wrap {{
    max-width: 1220px;
    margin: 0 auto;
    padding: 24px 32px 84px;
  }}

  /* 1. Editorial Navbar */
  .editorial-nav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 14px 0 22px;
    border-bottom: 2px solid rgba(20, 20, 19, 0.14);
    margin-bottom: 42px;
  }}

  .brand-lockup {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: var(--ink);
  }}

  .brand-title {{
    font-family: var(--serif);
    font-size: 1.45rem;
    font-weight: 600;
    letter-spacing: -0.02em;
  }}

  .brand-sub {{
    font-family: var(--mono);
    font-size: 11px;
    padding: 2px 8px;
    border: 1.6px solid var(--ink);
    border-radius: 999px;
    background: var(--paper-card);
  }}

  .nav-links {{
    display: flex;
    align-items: center;
    gap: 28px;
  }}

  .nav-link {{
    position: relative;
    text-decoration: none;
    color: var(--ink);
    font-weight: 500;
    font-size: 0.95rem;
    padding-bottom: 6px;
  }}

  .nav-link svg {{
    position: absolute;
    left: 0;
    bottom: -2px;
    width: 100%;
    height: 9px;
    overflow: visible;
  }}

  .nav-link svg path {{
    stroke-dasharray: 1;
    stroke-dashoffset: 1;
    transition: stroke-dashoffset 0.28s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .nav-link:hover svg path {{
    stroke-dashoffset: 0;
  }}

  .nav-pill-btn {{
    font-family: var(--mono);
    font-size: 12.5px;
    font-weight: 600;
    color: var(--ink);
    background: var(--paper-card);
    border: 2.2px solid var(--ink);
    border-radius: 999px;
    padding: 8px 18px;
    cursor: pointer;
    box-shadow: 4px 4px 0 var(--clay);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }}

  .nav-pill-btn:hover {{
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0 var(--clay);
  }}

  /* 2. Split Above-the-Fold Hero Section */
  .hero-split {{
    display: grid;
    grid-template-columns: 1.06fr 0.94fr;
    gap: 44px;
    align-items: center;
    margin-bottom: 72px;
  }}

  @media (max-width: 980px) {{
    .hero-split {{
      grid-template-columns: 1fr;
    }}
    .nav-links {{
      display: none;
    }}
  }}

  .release-badge {{
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 18px;
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 22px;
    isolation: isolate;
  }}

  .release-badge svg.badge-bg {{
    position: absolute;
    inset: -4px;
    width: calc(100% + 8px);
    height: calc(100% + 8px);
    z-index: -1;
  }}

  .badge-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--clay);
    border: 1.5px solid var(--ink);
  }}

  .hero-headline {{
    font-family: var(--serif);
    font-size: clamp(2.55rem, 4.4vw, 3.85rem);
    font-weight: 500;
    line-height: 1.07;
    letter-spacing: -0.025em;
    margin: 0 0 20px;
  }}

  .hero-headline em {{
    font-style: italic;
    font-weight: 400;
    background: linear-gradient(180deg, transparent 62%, rgba(217, 119, 87, 0.28) 62%);
    padding: 0 4px;
  }}

  .hero-lead {{
    font-size: 1.12rem;
    color: var(--ink-muted);
    max-width: 56ch;
    margin: 0 0 28px;
  }}

  .cta-row {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 18px;
    margin-bottom: 28px;
  }}

  .tactile-cta {{
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 15px 26px;
    font-family: var(--sans);
    font-weight: 600;
    font-size: 0.98rem;
    border: none;
    background: transparent;
    cursor: pointer;
    isolation: isolate;
    transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .tactile-cta.primary {{
    color: var(--paper);
  }}

  .tactile-cta.secondary {{
    color: var(--ink);
  }}

  .tactile-cta svg.cta-bg {{
    position: absolute;
    inset: -6px;
    width: calc(100% + 12px);
    height: calc(100% + 12px);
    z-index: -1;
    overflow: visible;
  }}

  .tactile-cta .cta-wash {{
    transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
    transform: translate(5px, 5px);
  }}

  .tactile-cta:hover {{
    transform: translate(-2px, -3px);
  }}

  .tactile-cta:hover .cta-wash {{
    transform: translate(11px, 10px) scale(1.03) rotate(-0.8deg);
  }}

  /* Hand-drawn Margin Annotations */
  .margin-notes {{
    display: flex;
    flex-wrap: wrap;
    gap: 28px;
    padding-top: 8px;
  }}

  .margin-note {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-family: var(--serif);
    font-style: italic;
    font-size: 1rem;
    color: var(--ink);
  }}

  .margin-note code {{
    font-family: var(--mono);
    font-style: normal;
    font-size: 11.5px;
    background: var(--paper-card);
    border: 1.5px solid var(--ink);
    border-radius: 6px;
    padding: 2px 7px;
  }}

  /* Right Column: Interactive Self-Drawing Hero Centerpiece Stage */
  .hero-stage-card {{
    background: var(--paper-card);
    border: 2.6px solid var(--ink);
    border-radius: 20px;
    padding: 20px 20px 18px;
    box-shadow: 10px 10px 0 rgba(20, 20, 19, 0.08);
    position: relative;
  }}

  .stage-toolbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    padding-bottom: 12px;
    margin-bottom: 14px;
    border-bottom: 1.8px dashed rgba(20, 20, 19, 0.2);
  }}

  .stage-label {{
    font-family: var(--mono);
    font-size: 11.5px;
    display: inline-flex;
    align-items: center;
    gap: 7px;
  }}

  .stage-label-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--olive);
    border: 1.5px solid var(--ink);
  }}

  .replay-btn {{
    font-family: var(--mono);
    font-size: 11.5px;
    font-weight: 600;
    background: var(--paper);
    color: var(--ink);
    border: 1.8px solid var(--ink);
    border-radius: 999px;
    padding: 5px 13px;
    cursor: pointer;
    box-shadow: 3px 3px 0 var(--peach);
    transition: transform 0.18s ease;
  }}

  .replay-btn:hover {{
    transform: translate(-1px, -1px);
  }}

  .centerpiece-viewport {{
    background: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 14px;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}

  .centerpiece-viewport svg {{
    width: 100%;
    max-width: 468px;
    height: auto;
    display: block;
  }}

  /* Self-Drawing Stroke Animation Keyframes */
  @keyframes penDraw {{
    0% {{
      stroke-dashoffset: 1;
    }}
    100% {{
      stroke-dashoffset: 0;
    }}
  }}

  @keyframes paperReveal {{
    0% {{
      opacity: 0;
    }}
    100% {{
      opacity: 1;
    }}
  }}

  .centerpiece-viewport.is-drawing path.draw-stroke {{
    stroke-dasharray: 1;
    stroke-dashoffset: 1;
    animation: penDraw 0.55s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    animation-delay: calc(var(--step, 1) * 28ms);
  }}

  .centerpiece-viewport.is-drawing .paper-fill {{
    opacity: 0;
    animation: paperReveal 0.4s ease forwards;
    animation-delay: calc(var(--step, 1) * 26ms);
  }}

  .theme-switcher {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
  }}

  .theme-pill {{
    flex: 1;
    min-width: 130px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    font-family: var(--mono);
    font-size: 11px;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1.8px solid var(--ink);
    background: var(--paper);
    cursor: pointer;
    transition: transform 0.18s ease, background 0.18s ease;
  }}

  .theme-pill[aria-pressed="true"] {{
    background: var(--ink);
    color: var(--paper);
  }}

  .swatch-pair {{
    display: inline-flex;
    gap: 3px;
  }}

  .swatch-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    border: 1.2px solid var(--ink);
  }}

  /* 3. 3-Card Feature Bento Grid */
  .section-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 28px;
  }}

  .section-eyebrow {{
    font-family: var(--mono);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--ink-muted);
    margin-bottom: 6px;
  }}

  .section-title {{
    font-family: var(--serif);
    font-size: clamp(1.85rem, 3vw, 2.5rem);
    font-weight: 500;
    margin: 0;
  }}

  .bento-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 28px;
    margin-bottom: 76px;
  }}

  @media (max-width: 960px) {{
    .bento-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .bento-card {{
    position: relative;
    padding: 26px 24px 24px;
    isolation: isolate;
    cursor: pointer;
    transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .bento-card svg.bento-bg {{
    position: absolute;
    inset: -10px;
    width: calc(100% + 20px);
    height: calc(100% + 20px);
    z-index: -1;
    overflow: visible;
  }}

  .bento-card .bento-wash,
  .bento-card .mini-wash {{
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .bento-card .bento-wash {{
    transform: translate(7px, 7px);
  }}

  .bento-card:hover {{
    transform: translate(-3px, -4px);
  }}

  .bento-card:hover .bento-wash {{
    transform: translate(15px, 13px) scale(1.03) rotate(-0.9deg);
  }}

  .bento-card:hover .mini-wash {{
    transform: translate(6px, -4px) scale(1.07) rotate(1.5deg);
  }}

  .bento-mini-svg {{
    width: 100%;
    max-width: 186px;
    height: auto;
    display: block;
    margin-bottom: 14px;
  }}

  .bento-tag {{
    display: inline-block;
    font-family: var(--mono);
    font-size: 11px;
    padding: 3px 10px;
    border: 1.6px solid var(--ink);
    border-radius: 999px;
    background: var(--paper);
    margin-bottom: 10px;
  }}

  .bento-card h3 {{
    font-family: var(--serif);
    font-size: 1.35rem;
    margin: 0 0 8px;
  }}

  .bento-card p {{
    margin: 0 0 14px;
    font-size: 0.94rem;
    color: var(--ink-muted);
  }}

  .bento-meta {{
    font-family: var(--mono);
    font-size: 11.5px;
    padding-top: 10px;
    border-top: 1.5px dashed rgba(20, 20, 19, 0.22);
    display: flex;
    justify-content: space-between;
  }}

  /* 4. 2-Tier Editorial Pricing Section */
  .pricing-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 36px;
    align-items: stretch;
  }}

  @media (max-width: 880px) {{
    .pricing-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .pricing-card {{
    position: relative;
    padding: 34px 32px 30px;
    isolation: isolate;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .pricing-card svg.pricing-bg {{
    position: absolute;
    inset: -10px;
    width: calc(100% + 20px);
    height: calc(100% + 20px);
    z-index: -1;
    overflow: visible;
  }}

  .pricing-card .pricing-wash {{
    transform: translate(8px, 8px);
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .pricing-card:hover .pricing-wash {{
    transform: translate(15px, 14px) scale(1.02) rotate(-0.6deg);
  }}

  .tier-name {{
    font-family: var(--mono);
    font-size: 12.5px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
  }}

  .tier-price {{
    font-family: var(--serif);
    font-size: 2.8rem;
    font-weight: 600;
    line-height: 1;
    margin: 0 0 8px;
  }}

  .tier-price span {{
    font-size: 1.05rem;
    font-weight: 400;
    color: var(--ink-muted);
  }}

  .tier-desc {{
    font-size: 0.95rem;
    color: var(--ink-muted);
    margin: 0 0 20px;
  }}

  .feature-list {{
    list-style: none;
    padding: 0;
    margin: 0 0 26px;
    display: flex;
    flex-direction: column;
    gap: 11px;
  }}

  .feature-list li {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.95rem;
  }}

  .feature-list svg {{
    flex-shrink: 0;
  }}

  .wax-seal-stamp {{
    position: absolute;
    top: -18px;
    right: 18px;
    width: 116px;
    height: 116px;
    transform: rotate(9deg);
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
    pointer-events: none;
  }}

  .pricing-card:hover .wax-seal-stamp {{
    transform: rotate(15deg) scale(1.06);
  }}
</style>
</head>
<body>

<!-- Shared SVG Filter Defs Bank for DOM UI Components -->
<svg class="svg-defs-bank" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="ui-wash" x="-12%" y="-12%" width="124%" height="124%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="29" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 1.42" result="a"/>
      <feComposite in="d" in2="a" operator="in"/>
    </filter>
    <filter id="ui-ink" x="-8%" y="-8%" width="116%" height="116%">
      <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="43" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
</svg>

<div class="page-wrap">
  <!-- 1. Editorial Navbar -->
  <nav class="editorial-nav" aria-label="Primary Editorial Navigation">
    <a href="#top" class="brand-lockup">
      <svg width="40" height="40" viewBox="0 0 64 64" aria-hidden="true">
        <g filter="url(#ui-wash)">
          <path d="{handify('M 10 18 L 52 12 L 56 50 L 14 54 Z', amount=1.6, seed='nav-em-w')}" fill="{COLORS['clay'][0]}"/>
        </g>
        <g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="{handify('M 14 14 L 50 10 L 54 48 L 16 52 Z', amount=1.2, seed='nav-em-b')}" fill="{PAPER}"/>
          <path d="{sparkle(34, 31, 11, seed='nav-em-s')}" stroke-width="2.8"/>
        </g>
      </svg>
      <span class="brand-title">Atelier Claude</span>
      <span class="brand-sub">CC-lineart v2.4</span>
    </a>

    <div class="nav-links">
      <a href="#workbench" class="nav-link">
        Studio Workbench
        <svg viewBox="0 0 96 10" preserveAspectRatio="none"><path pathLength="1" d="{nav_ul}" fill="none" stroke="{COLORS['clay'][0]}" stroke-width="2.6" stroke-linecap="round"/></svg>
      </a>
      <a href="#bento-features" class="nav-link">
        3-Layer Architecture
        <svg viewBox="0 0 96 10" preserveAspectRatio="none"><path pathLength="1" d="{nav_ul}" fill="none" stroke="{COLORS['sky'][0]}" stroke-width="2.6" stroke-linecap="round"/></svg>
      </a>
      <a href="#pricing-section" class="nav-link">
        Editorial Pricing
        <svg viewBox="0 0 96 10" preserveAspectRatio="none"><path pathLength="1" d="{nav_ul}" fill="none" stroke="{COLORS['olive'][0]}" stroke-width="2.6" stroke-linecap="round"/></svg>
      </a>
    </div>

    <button type="button" class="nav-pill-btn" onclick="document.getElementById('btn-replay-draw').click()">
      Replay Ink Stroke ↻
    </button>
  </nav>

  <!-- 2. Split Above-the-Fold Hero Section -->
  <section class="hero-split" id="workbench">
    <div class="hero-copy-col">
      <div class="release-badge">
        <svg class="badge-bg" viewBox="0 0 268 44" preserveAspectRatio="none">
          <g filter="url(#ui-wash)">
            <path d="{badge_wash}" fill="{COLORS['peach'][0]}"/>
          </g>
          <g filter="url(#ui-ink)">
            <path d="{badge_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.2" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>
        <span class="badge-dot"></span>
        <span>v2.4 — Hand-Drawn UI Engine</span>
      </div>

      <h1 class="hero-headline">
        Autonomous design &amp; reasoning, <em>drawn in real ink</em>.
      </h1>

      <p class="hero-lead">
        Atelier Claude replaces sterile SaaS stock photos and rigid bounding boxes with deterministic <code>#141413</code> fountain-pen vectors, warm <code>#FAF9F5</code> paper cutouts, and glazed watercolor washes that pass automated visual lint checks.
      </p>

      <div class="cta-row">
        <button type="button" class="tactile-cta primary" id="cta-launch-studio">
          <svg class="cta-bg" viewBox="0 0 248 62" preserveAspectRatio="none">
            <g class="cta-wash" filter="url(#ui-wash)">
              <path d="{cta_pri_wash}" fill="{COLORS['clay'][0]}"/>
              <path d="{cta_pri_wash}" fill="none" stroke="{COLORS['clay'][1]}" stroke-width="2" stroke-opacity="0.55"/>
            </g>
            <g filter="url(#ui-ink)">
              <path d="{cta_pri_box}" fill="{INK}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
            </g>
          </svg>
          <span>Launch Autonomous Studio →</span>
        </button>

        <button type="button" class="tactile-cta secondary" id="cta-inspect-lint">
          <svg class="cta-bg" viewBox="0 0 218 62" preserveAspectRatio="none">
            <g class="cta-wash" filter="url(#ui-wash)">
              <path d="{cta_sec_wash}" fill="{COLORS['sky'][0]}"/>
            </g>
            <g filter="url(#ui-ink)">
              <path d="{cta_sec_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
            </g>
          </svg>
          <span id="lint-btn-label">Inspect Lint: 0 Warnings</span>
        </button>
      </div>

      <!-- Hand-drawn Margin Annotation Arrows -->
      <div class="margin-notes">
        <div class="margin-note">
          <svg width="92" height="34" viewBox="0 0 92 34" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#ui-ink)">
            <path d="{margin_arr_1}"/>
            <path d="{margin_arr_1_h}"/>
          </svg>
          <span>100% Vector Ink <code>8.5 / 6.0 / 4.5</code></span>
        </div>

        <div class="margin-note">
          <svg width="96" height="34" viewBox="0 0 96 34" fill="none" stroke="{COLORS['clay'][1]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#ui-ink)">
            <path d="{margin_arr_2}"/>
            <path d="{margin_arr_2_h}"/>
          </svg>
          <span>Zero Stock Photos <code>100% SVG</code></span>
        </div>
      </div>
    </div>

    <!-- Right Column: Interactive Self-Drawing Hero Centerpiece SVG -->
    <div class="hero-stage-card">
      <div class="stage-toolbar">
        <span class="stage-label">
          <span class="stage-label-dot"></span>
          <span>hero-centerpiece.svg · 512×512 · 0 Lint Warnings</span>
        </span>
        <button type="button" class="replay-btn" id="btn-replay-draw">
          Replay Pen Draw ✎
        </button>
      </div>

      <div class="centerpiece-viewport" id="hero-svg-viewport">
        {centerpiece_svg}
      </div>

      <!-- Watercolor Wash Theme Switcher -->
      <div class="theme-switcher" role="group" aria-label="Watercolor Wash Theme Switcher">
        <button type="button" class="theme-pill" data-theme="warm" aria-pressed="true">
          <span class="swatch-pair">
            <span class="swatch-dot" style="background:#D97757"></span>
            <span class="swatch-dot" style="background:#6A9BCC"></span>
          </span>
          <span>Warm Clay &amp; Sky</span>
        </button>

        <button type="button" class="theme-pill" data-theme="sage" aria-pressed="false">
          <span class="swatch-pair">
            <span class="swatch-dot" style="background:#BCD1CA"></span>
            <span class="swatch-dot" style="background:#D4A27F"></span>
          </span>
          <span>Sage Cactus &amp; Oat</span>
        </button>

        <button type="button" class="theme-pill" data-theme="botanical" aria-pressed="false">
          <span class="swatch-pair">
            <span class="swatch-dot" style="background:#827DBD"></span>
            <span class="swatch-dot" style="background:#CBCADB"></span>
          </span>
          <span>Botanical Fig &amp; Heather</span>
        </button>
      </div>
    </div>
  </section>

  <!-- 3. 3-Card Feature Bento Grid -->
  <section id="bento-features">
    <div class="section-header">
      <div>
        <div class="section-eyebrow">Three-Layer Craftsmanship</div>
        <h2 class="section-title">Why AI-Designed Hero Pages Need Ink &amp; Paper</h2>
      </div>
      <span class="brand-sub">Hover any bento card to shift its wet watercolor wash</span>
    </div>

    <div class="bento-grid">
      <!-- Card 1 -->
      <article class="bento-card">
        <svg class="bento-bg" viewBox="0 0 370 284" preserveAspectRatio="none">
          <g class="bento-wash" filter="url(#ui-wash)">
            <path d="{bento_wash_1}" fill="{COLORS['sky'][0]}"/>
            <path d="{bento_wash_1}" fill="none" stroke="{COLORS['sky'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
          </g>
          <g filter="url(#ui-ink)">
            <path d="{bento_box_1}" fill="#FFFEFA" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>
        {bento_svg_1}
        <span class="bento-tag">01 · Bowed Cubic Paths</span>
        <h3>Zero-Template Vector Synthesis</h3>
        <p>Every container, connector, and icon is synthesized directly in Python via <code>handify()</code> with controlled bow and corner overshoots—never generic stock imagery.</p>
        <div class="bento-meta">
          <span>Skewed Quadrilaterals</span>
          <span>0 Ruler Lines</span>
        </div>
      </article>

      <!-- Card 2 -->
      <article class="bento-card">
        <svg class="bento-bg" viewBox="0 0 370 284" preserveAspectRatio="none">
          <g class="bento-wash" filter="url(#ui-wash)">
            <path d="{bento_wash_2}" fill="{COLORS['peach'][0]}"/>
            <path d="{bento_wash_2}" fill="none" stroke="{COLORS['peach'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
          </g>
          <g filter="url(#ui-ink)">
            <path d="{bento_box_2}" fill="#FFFEFA" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>
        {bento_svg_2}
        <span class="bento-tag">02 · Multiply Glaze</span>
        <h3>Glazed Watercolor Layers</h3>
        <p>Overlapping warm <code>clay</code>/<code>peach</code> and cool <code>sky</code>/<code>cactus</code> washes blend with <code>mix-blend-mode: multiply</code> and fractal-noise pigment pooling.</p>
        <div class="bento-meta">
          <span>Coverage: 15–45%</span>
          <span>Breakout ≥ 20%</span>
        </div>
      </article>

      <!-- Card 3 -->
      <article class="bento-card">
        <svg class="bento-bg" viewBox="0 0 370 284" preserveAspectRatio="none">
          <g class="bento-wash" filter="url(#ui-wash)">
            <path d="{bento_wash_3}" fill="{COLORS['cactus'][0]}"/>
            <path d="{bento_wash_3}" fill="none" stroke="{COLORS['cactus'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
          </g>
          <g filter="url(#ui-ink)">
            <path d="{bento_box_3}" fill="#FFFEFA" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>
        {bento_svg_3}
        <span class="bento-tag">03 · Automated Quality Gate</span>
        <h3>Deterministic Lint Gate</h3>
        <p>Every centerpiece SVG is audited by <code>lineart.py lint</code> for mirror-symmetry tells, stroke hierarchy (<code>8.5 / 6.0 / 4.5</code>), wash visibility, and 28px hole survival.</p>
        <div class="bento-meta">
          <span>Markup + Raster Audit</span>
          <span>0 Warnings</span>
        </div>
      </article>
    </div>
  </section>

  <!-- 4. 2-Tier Editorial Pricing Section -->
  <section id="pricing-section">
    <div class="section-header">
      <div>
        <div class="section-eyebrow">Transparent Studio Editions</div>
        <h2 class="section-title">Editorial Pricing for Craft-Minded Teams</h2>
      </div>
      <span class="brand-sub">Hand-stamped wax seal marks our recommended team tier</span>
    </div>

    <div class="pricing-grid">
      <!-- Tier 1: Studio Pass -->
      <article class="pricing-card">
        <svg class="pricing-bg" viewBox="0 0 452 388" preserveAspectRatio="none">
          <g class="pricing-wash" filter="url(#ui-wash)">
            <path d="{price_wash_1}" fill="{COLORS['cactus'][0]}"/>
            <path d="{price_wash_1}" fill="none" stroke="{COLORS['cactus'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
          </g>
          <g filter="url(#ui-ink)">
            <path d="{price_box_1}" fill="#FFFEFA" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>

        <div>
          <div class="tier-name">Studio Pass · Local CLI</div>
          <div class="tier-price">$0 <span>/ local forever</span></div>
          <p class="tier-desc">Full offline access to <code>scripts/lineart.py</code>, motif library, and deterministic SVG/PNG rendering.</p>

          <ul class="feature-list">
            <li>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="{COLORS['olive'][0]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{chk_path}"/></svg>
              <span>Unlimited 64×64 motifs &amp; 512×512 hero scenes</span>
            </li>
            <li>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="{COLORS['olive'][0]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{chk_path}"/></svg>
              <span>Built-in <code>lineart.py lint</code> markup &amp; raster checks</span>
            </li>
            <li>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="{COLORS['olive'][0]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{chk_path}"/></svg>
              <span>Self-drawing <code>pathLength="1"</code> stroke animation ready</span>
            </li>
          </ul>
        </div>

        <button type="button" class="nav-pill-btn" style="align-self:flex-start; box-shadow: 4px 4px 0 var(--cactus-edge);">
          Clone Local Skill →
        </button>
      </article>

      <!-- Tier 2: Atelier Pro with Wax-Seal Stamp -->
      <article class="pricing-card">
        <svg class="pricing-bg" viewBox="0 0 452 388" preserveAspectRatio="none">
          <g class="pricing-wash" filter="url(#ui-wash)">
            <path d="{price_wash_2}" fill="{COLORS['clay'][0]}"/>
            <path d="{price_wash_2}" fill="none" stroke="{COLORS['clay'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
          </g>
          <g filter="url(#ui-ink)">
            <path d="{price_box_2}" fill="#FFFEFA" stroke="{INK}" stroke-width="2.8" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>

        <!-- Hand-Drawn Wax-Seal Stamp (RECOMMENDED) -->
        <svg class="wax-seal-stamp" viewBox="0 0 116 116" aria-label="Recommended Tier Wax Seal">
          <g filter="url(#ui-wash)">
            <path d="{wax_outer}" fill="{COLORS['clay'][0]}"/>
            <path d="{wax_outer}" fill="none" stroke="{COLORS['clay'][1]}" stroke-width="2.5" stroke-opacity="0.7"/>
          </g>
          <g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">
            <path d="{wax_outer}" stroke-width="2.8"/>
            <path d="{wax_inner}" fill="{PAPER}" stroke-width="2.2"/>
            <path d="{wax_star}" stroke-width="2.2"/>
          </g>
          <text x="58" y="64" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="8.5" font-weight="600" fill="{INK}" letter-spacing="0.06em">RECOMMENDED</text>
          <text x="58" y="75" text-anchor="middle" font-family="Newsreader, serif" font-style="italic" font-size="8" fill="{COLORS['clay'][1]}">Atelier Seal</text>
        </svg>

        <div>
          <div class="tier-name" style="color: var(--clay-edge); font-weight: 600;">Atelier Pro · Multi-Agent Studio</div>
          <div class="tier-price">$29 <span>/ seat / month</span></div>
          <p class="tier-desc">Shared brand motif registries, live multi-theme watercolor tokens, and automated CI visual lint gates.</p>

          <ul class="feature-list">
            <li>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="{COLORS['clay'][0]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{chk_path}"/></svg>
              <span>Everything in Studio Pass + team motif syncing</span>
            </li>
            <li>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="{COLORS['clay'][0]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{chk_path}"/></svg>
              <span>Interactive watercolor glaze switcher &amp; CSS tokens</span>
            </li>
            <li>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="{COLORS['clay'][0]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{chk_path}"/></svg>
              <span>Zero-stock-photo editorial hero &amp; slide deck pipelines</span>
            </li>
          </ul>
        </div>

        <button type="button" class="nav-pill-btn" style="align-self:flex-start; background: var(--ink); color: var(--paper);">
          Start 14-Day Atelier Trial →
        </button>
      </article>
    </div>
  </section>
</div>

<script>
  // 1. Assign sequential --step CSS custom properties for stroke-draw replay
  const viewport = document.getElementById('hero-svg-viewport');
  const stepNodes = viewport.querySelectorAll('[data-step]');
  stepNodes.forEach((node) => {{
    node.style.setProperty('--step', node.getAttribute('data-step'));
  }});

  function triggerPenReplay() {{
    viewport.classList.remove('is-drawing');
    void viewport.offsetWidth; // Force reflow
    viewport.classList.add('is-drawing');
  }}

  document.getElementById('btn-replay-draw').addEventListener('click', triggerPenReplay);
  document.getElementById('cta-launch-studio').addEventListener('click', triggerPenReplay);

  // Run initial pen draw on page load
  window.addEventListener('DOMContentLoaded', () => {{
    setTimeout(triggerPenReplay, 120);
  }});

  // 2. Watercolor Wash Theme Switcher
  const themes = {{
    warm: {{
      coolFill: '#6A9BCC', coolEdge: '#4C7FB3',
      warmFill: '#EBC9B7', warmEdge: '#D3A58D',
      focalFill: '#D97757', focalEdge: '#B85C3E',
    }},
    sage: {{
      coolFill: '#BCD1CA', coolEdge: '#93B0A6',
      warmFill: '#D4A27F', warmEdge: '#B9845F',
      focalFill: '#788C5D', focalEdge: '#5D7046',
    }},
    botanical: {{
      coolFill: '#CBCADB', coolEdge: '#A4A2BF',
      warmFill: '#827DBD', warmEdge: '#635DA3',
      focalFill: '#D97757', focalEdge: '#B85C3E',
    }}
  }};

  const themeBtns = document.querySelectorAll('.theme-pill');
  themeBtns.forEach((btn) => {{
    btn.addEventListener('click', () => {{
      const key = btn.getAttribute('data-theme');
      const t = themes[key];
      if (!t) return;
      themeBtns.forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
      document.getElementById('hero-wash-cool-fill').setAttribute('fill', t.coolFill);
      document.getElementById('hero-wash-cool-edge').setAttribute('stroke', t.coolEdge);
      document.getElementById('hero-wash-warm-fill').setAttribute('fill', t.warmFill);
      document.getElementById('hero-wash-warm-edge').setAttribute('stroke', t.warmEdge);
      document.getElementById('hero-wash-focal-fill').setAttribute('fill', t.focalFill);
      document.getElementById('hero-wash-focal-edge').setAttribute('stroke', t.focalEdge);
      document.getElementById('hero-seal-tint').setAttribute('fill', t.focalFill);
    }});
  }});

  // 3. Lint button feedback
  const lintBtn = document.getElementById('cta-inspect-lint');
  const lintLabel = document.getElementById('lint-btn-label');
  lintBtn.addEventListener('click', () => {{
    lintLabel.textContent = '✓ Verified: 0 Warnings (36% Wash)';
    setTimeout(() => {{
      lintLabel.textContent = 'Inspect Lint: 0 Warnings';
    }}, 2600);
  }});
</script>
</body>
</html>
"""


def render_png(svg_path, png_path, size=512):
    """Render a 512x512 PNG preview with paper background via rsvg-convert."""
    if not shutil.which("rsvg-convert"):
        return
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), "-b", PAPER, svg_path, "-o", png_path],
        check=True,
    )
    print(f"Wrote {png_path}")


def main():
    centerpiece_svg = build_hero_centerpiece_svg()
    svg_path = os.path.join(HERE, "hero-centerpiece.svg")
    png_path = os.path.join(HERE, "hero-centerpiece.png")
    html_path = os.path.join(HERE, "hero-landing-page.html")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(centerpiece_svg)
    print(f"Wrote {svg_path}")

    render_png(svg_path, png_path, size=512)

    html_doc = build_landing_page_html(centerpiece_svg)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"Wrote {html_path}")


if __name__ == "__main__":
    main()
