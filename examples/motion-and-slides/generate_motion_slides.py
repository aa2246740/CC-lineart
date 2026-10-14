#!/usr/bin/env python3
"""Generate Track 5 deliverables: Animated Line-Art & Presentation Deck Visuals.

Produces inside /Users/wu/CC-lineart/examples/motion-and-slides/:
  1. slide-editorial-story.svg   (512x512, 3-act presentation visual)
  2. animated-creative-desk.svg  (512x512, editorial workspace scene)
  3. motion-showcase.html        (interactive stroke-draw, paper-reveal & breathing wash deck)
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lineart import COLORS, INK, PAPER, handify, sparkle, wobbly_circle  # noqa: E402


def hpath(d, amount=5.2, overshoot=0.0, seed="sketch"):
    """512-grid wrapper around lineart.handify."""
    return handify(d, amount=amount, overshoot=overshoot, seed=seed)


def starburst_rays(cx, cy, r_inner, r_outer, seed="burst"):
    """7-ray Claude-style irregular starburst computed via trig."""
    angles = [-90, -38, 8, 52, 98, 146, 196]
    scales = [1.14, 0.86, 1.09, 0.90, 1.16, 0.84, 1.03]
    segs = []
    for idx, (deg, sc) in enumerate(zip(angles, scales)):
        rad = math.radians(deg)
        r0 = r_inner * (0.88 + 0.05 * (idx % 3))
        r1 = r_outer * sc
        x0, y0 = cx + r0 * math.cos(rad), cy + r0 * math.sin(rad)
        x1, y1 = cx + r1 * math.cos(rad), cy + r1 * math.sin(rad)
        segs.append(hpath(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", amount=2.2, seed=f"{seed}-{idx}"))
    return " ".join(segs)


def build_defs(seed_wash=31, seed_ink=47):
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


def wash_blob(d, color_name, blend="normal", cls="wash-primary"):
    fill, edge = COLORS[color_name]
    style_attr = f' style="mix-blend-mode: {blend}"' if blend != "normal" else ""
    return f"""  <g class="{cls}"{style_attr}>
    <path d="{d}" fill="{fill}"/>
    <path d="{d}" fill="none" stroke="{edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>"""


def build_slide_editorial_story():
    """Generate slide-editorial-story.svg: 'From Sketch -> Agent Execution -> Shipped Artifact'."""
    # Revision 2: Offset washes more intentionally so ~30% of line art breaks out into paper canvas
    wash_olive = hpath("M 58 256 L 258 232 L 274 448 L 74 464 Z", amount=7.5, seed="s-olive-v2")
    wash_peach = hpath("M 196 118 L 432 96 L 448 332 L 212 350 Z", amount=7.5, seed="s-peach-v2")
    wash_clay = wobbly_circle(398, 128, 42, seed="s-clay-v2", wobble=0.07, overlap=12)

    # Background connecting paths (drawn behind paper cards so they pass under and emerge)
    bg_grid_arc = hpath("M 28 432 C 114 448 192 398 248 330", amount=4.0, seed="bg-arc-1")
    conn_1_to_2 = hpath("M 176 334 C 212 318 222 276 248 258", amount=4.0, seed="conn-12")
    conn_2_to_3 = hpath("M 332 198 C 362 172 374 142 396 128", amount=4.0, seed="conn-23")
    launch_swoosh = hpath("M 432 82 C 460 54 480 38 498 24", amount=3.5, seed="swoosh-top")

    # Act I (Lower-Left): Tilted Sketchpad + Technical Fountain Pen (breaks out lower-left of wash)
    sketch_card_fill = hpath("M 34 292 L 178 274 L 194 456 L 48 474 Z", amount=5.5, seed="act1-fill")
    sketch_card_out_1 = hpath("M 32 298 L 34 292 L 178 274 L 194 456", amount=5.0, overshoot=12.0, seed="act1-o1")
    sketch_card_out_2 = hpath("M 194 456 L 48 474 L 34 292", amount=5.0, overshoot=10.0, seed="act1-o2")
    sketch_dogear = hpath("M 148 278 L 154 310 L 184 304", amount=3.2, seed="act1-dogear")
    sketch_wave_1 = hpath("M 58 336 C 88 322 120 346 154 330", amount=3.0, seed="act1-w1")
    sketch_wave_2 = hpath("M 62 370 C 92 358 116 380 146 366", amount=3.0, seed="act1-w2")
    # Hand-drawn node + mini flow sketch on the notepad
    sketch_node = hpath("M 64 404 L 106 394 L 94 434 L 58 424", amount=3.2, overshoot=5.0, seed="act1-wf")
    sketch_flow = hpath("M 102 414 C 118 404 132 422 148 408", amount=2.5, seed="act1-flow")

    # Angled drafting fountain pen crossing lower-right of Act I card
    pen_body = hpath("M 136 442 L 222 370 L 238 386 L 152 458 Z", amount=3.5, seed="pen-body")
    pen_nib = hpath("M 136 442 L 114 472 L 152 458", amount=2.6, seed="pen-tip")
    pen_collar = hpath("M 198 390 L 214 406", amount=2.0, seed="pen-band")
    pen_clip = hpath("M 212 378 L 242 354 L 248 362", amount=2.2, seed="pen-clip")

    # Act II (Center): Agent Execution Card (Terminal + Starburst + Node Flow)
    agent_card_fill = hpath("M 176 168 L 356 154 L 368 322 L 188 336 Z", amount=5.8, seed="act2-fill")
    agent_card_top = hpath("M 176 168 L 356 154 L 368 322", amount=5.0, overshoot=12.0, seed="act2-o1")
    agent_card_bot = hpath("M 368 322 L 188 336 L 176 168", amount=5.0, overshoot=11.0, seed="act2-o2")
    agent_header_div = hpath("M 182 204 L 358 190", amount=4.0, seed="act2-hdr")
    # Terminal prompt >_
    prompt_chev = hpath("M 204 234 L 226 248 L 206 266", amount=2.8, seed="act2-chev")
    prompt_line = hpath("M 236 268 L 268 265", amount=2.5, seed="act2-pline")
    # Agent starburst inside Act II
    burst_d = starburst_rays(308, 252, 12, 34, seed="act2-burst")
    # Sub-lines inside agent card
    agent_bar_1 = hpath("M 206 294 L 274 288", amount=3.0, seed="act2-b1")
    agent_bar_2 = hpath("M 208 312 L 256 308", amount=3.0, seed="act2-b2")

    # Act III (Upper-Right): Shipped Artifact Card + Check Badge breaking out into upper-right
    ship_card_fill = hpath("M 304 42 L 484 26 L 496 180 L 316 196 Z", amount=5.5, seed="act3-fill")
    ship_card_out_1 = hpath("M 304 42 L 484 26 L 496 180", amount=5.0, overshoot=12.0, seed="act3-o1")
    ship_card_out_2 = hpath("M 496 180 L 316 196 L 304 42", amount=5.0, overshoot=10.0, seed="act3-o2")
    # Shipped badge circle (hand-drawn wobbly_circle) overlapping upper-right corner
    badge_circle = wobbly_circle(414, 106, 38, seed="act3-badge", wobble=0.06, overlap=15)
    badge_check = hpath("M 396 108 L 410 122 L 436 88", amount=2.8, seed="act3-check")
    ship_line_1 = hpath("M 326 78 L 364 74", amount=2.5, seed="act3-l1")
    ship_line_2 = hpath("M 328 106 L 356 103", amount=2.5, seed="act3-l2")
    ship_line_3 = hpath("M 332 156 L 462 146", amount=3.5, seed="act3-l3")

    # Foreground connecting arrows (crossing card boundaries)
    fg_arrow_1 = hpath("M 160 316 C 190 284 212 268 238 256", amount=3.5, seed="fg-arr1")
    fg_arrow_1_head = hpath("M 222 250 L 240 255 L 228 272", amount=2.2, seed="fg-arr1-h")
    fg_arrow_2 = hpath("M 324 196 C 344 168 360 144 378 128", amount=3.5, seed="fg-arr2")
    fg_arrow_2_head = hpath("M 360 126 L 380 126 L 372 144", amount=2.2, seed="fg-arr2-h")

    # Quiet area accents (Upper-Left quadrant: 3 clustered sparkles + 2 dots, 1 small echo bottom-right)
    sp_big = sparkle(88, 96, 22, seed="sp-s1")
    sp_med = sparkle(128, 74, 14, seed="sp-s2")
    sp_sml = sparkle(68, 134, 10, seed="sp-s3")
    sp_echo = sparkle(446, 416, 13, seed="sp-echo")

    clay_fill, _ = COLORS["clay"]
    olive_fill, _ = COLORS["olive"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{build_defs(seed_wash=31, seed_ink=47)}
<g id="layer-block" filter="url(#wash)" style="isolation: isolate">
{wash_blob(wash_olive, "olive", blend="normal", cls="wash-blob wash-1")}
{wash_blob(wash_peach, "peach", blend="multiply", cls="wash-blob wash-2")}
{wash_blob(wash_clay, "clay", blend="normal", cls="wash-blob wash-3")}
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- 1. Background trajectory strokes passing behind paper shapes -->
  <path class="draw-stroke" data-step="1" pathLength="1" d="{bg_grid_arc}" stroke-width="5.5" stroke-dasharray="14 16"/>
  <path class="draw-stroke" data-step="2" pathLength="1" d="{conn_1_to_2}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="3" pathLength="1" d="{conn_2_to_3}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="4" pathLength="1" d="{launch_swoosh}" stroke-width="5.5"/>

  <!-- 2. Act I: Sketch Card (Lower-Left) -->
  <path class="paper-fill" data-step="5" d="{sketch_card_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="6" pathLength="1" d="{sketch_card_out_1}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="7" pathLength="1" d="{sketch_card_out_2}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="8" pathLength="1" d="{sketch_dogear}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="9" pathLength="1" d="{sketch_wave_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="10" pathLength="1" d="{sketch_wave_2}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="11" pathLength="1" d="{sketch_node}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="12" pathLength="1" d="{sketch_flow}" stroke-width="5.5"/>

  <!-- Drafting Pen across Act I corner -->
  <path class="paper-fill" data-step="13" d="{pen_body}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="14" pathLength="1" d="{pen_body}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="15" pathLength="1" d="{pen_nib}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="16" pathLength="1" d="{pen_collar}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="17" pathLength="1" d="{pen_clip}" stroke-width="5.5"/>

  <!-- 3. Act II: Agent Execution Card (Center) -->
  <path class="paper-fill" data-step="18" d="{agent_card_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="19" pathLength="1" d="{agent_card_top}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="20" pathLength="1" d="{agent_card_bot}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="21" pathLength="1" d="{agent_header_div}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="22" pathLength="1" d="{prompt_chev}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="23" pathLength="1" d="{prompt_line}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="24" pathLength="1" d="{burst_d}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="25" pathLength="1" d="{agent_bar_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="26" pathLength="1" d="{agent_bar_2}" stroke-width="6.0"/>

  <!-- 4. Act III: Shipped Artifact Card (Upper-Right) -->
  <path class="paper-fill" data-step="27" d="{ship_card_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="28" pathLength="1" d="{ship_card_out_1}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="29" pathLength="1" d="{ship_card_out_2}" stroke-width="8.5"/>
  <path class="paper-fill" data-step="30" d="{badge_circle}" fill="{clay_fill}" fill-opacity="0.28" stroke="none"/>
  <path class="draw-stroke" data-step="31" pathLength="1" d="{badge_circle}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="32" pathLength="1" d="{badge_check}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="33" pathLength="1" d="{ship_line_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="34" pathLength="1" d="{ship_line_2}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="35" pathLength="1" d="{ship_line_3}" stroke-width="6.0"/>

  <!-- 5. Foreground flow connectors crossing over cards -->
  <path class="draw-stroke" data-step="36" pathLength="1" d="{fg_arrow_1}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="37" pathLength="1" d="{fg_arrow_1_head}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="38" pathLength="1" d="{fg_arrow_2}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="39" pathLength="1" d="{fg_arrow_2_head}" stroke-width="6.5"/>

  <!-- 6. Accents in quiet upper-left quadrant + 1 echo -->
  <path class="draw-stroke" data-step="40" pathLength="1" d="{sp_big}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="41" pathLength="1" d="{sp_med}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="42" pathLength="1" d="{sp_sml}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="43" pathLength="1" d="{sp_echo}" stroke-width="5.0"/>
  <circle class="paper-fill" data-step="44" cx="148" cy="112" r="4.5" fill="{INK}" stroke="none"/>
  <circle class="paper-fill" data-step="45" cx="56" cy="92" r="3.8" fill="{olive_fill}" stroke="none"/>
</g>
</svg>
"""
    return svg


def build_animated_creative_desk():
    """Generate animated-creative-desk.svg: Monitor, steaming mug, open notebook, paper plane."""
    # Revision 2: Compact & offset washes so ~30% of line art breaks out into paper canvas
    wash_sky = hpath("M 84 124 L 342 102 L 356 346 L 98 364 Z", amount=7.5, seed="d-sky-v2")
    wash_peach = hpath("M 236 238 L 448 216 L 462 442 L 248 456 Z", amount=7.5, seed="d-peach-v2")
    wash_clay = wobbly_circle(424, 112, 40, seed="d-clay-v2", wobble=0.06, overlap=12)

    # 1. Background elements (desk horizon line + paper plane trajectory passing behind monitor)
    desk_horizon_L = hpath("M 18 372 L 108 366", amount=4.0, seed="desk-hl")
    desk_horizon_R = hpath("M 424 348 L 496 342", amount=4.0, seed="desk-hr")
    plane_trail_back = hpath("M 148 392 C 198 310 268 232 376 138", amount=5.0, seed="plane-trail")

    # 2. Studio Display Monitor (tilted slightly counter-clockwise, center-left)
    mon_outer_fill = hpath("M 82 118 L 352 102 L 362 302 L 92 318 Z", amount=5.5, seed="mon-fill")
    mon_out_top = hpath("M 82 118 L 352 102 L 362 302", amount=5.0, overshoot=13.0, seed="mon-o1")
    mon_out_bot = hpath("M 362 302 L 92 318 L 82 118", amount=5.0, overshoot=11.0, seed="mon-o2")
    mon_chin = hpath("M 90 274 L 358 258", amount=4.0, seed="mon-chin")
    # Monitor stand neck & base
    stand_fill = hpath("M 204 312 L 256 308 L 268 362 L 192 366 Z", amount=3.5, seed="stand-fill")
    stand_neck_L = hpath("M 206 312 L 194 366", amount=3.0, seed="stand-l")
    stand_neck_R = hpath("M 254 308 L 266 362", amount=3.0, seed="stand-r")
    stand_base = hpath("M 162 368 L 296 360", amount=4.0, overshoot=8.0, seed="stand-base")

    # Screen interior details (code/layout blocks + waveforms)
    scr_sidebar = hpath("M 144 116 L 152 268", amount=3.5, seed="scr-side")
    scr_code_1 = hpath("M 174 148 L 258 142", amount=3.0, seed="scr-c1")
    scr_code_2 = hpath("M 176 174 L 314 164", amount=3.2, seed="scr-c2")
    scr_code_3 = hpath("M 190 200 L 282 192", amount=3.0, seed="scr-c3")
    scr_wave = hpath("M 178 238 C 212 216 244 250 278 224 C 300 208 318 230 334 216", amount=2.8, seed="scr-wave")

    # 3. Open Sketch Notebook in Foreground Lower-Left (breaks out lower-left of wash)
    nb_fill = hpath("M 28 348 L 232 332 L 248 470 L 44 488 Z", amount=5.5, seed="nb-fill")
    nb_out_1 = hpath("M 28 348 L 232 332 L 248 470", amount=4.8, overshoot=10.0, seed="nb-o1")
    nb_out_2 = hpath("M 248 470 L 44 488 L 28 348", amount=4.8, overshoot=10.0, seed="nb-o2")
    nb_spine = hpath("M 132 340 L 146 478", amount=3.5, seed="nb-spine")
    # Spiral binding stitches across spine (varied spacing/length)
    nb_ring_1 = hpath("M 122 366 C 134 360 144 362 152 368", amount=1.8, seed="nb-r1")
    nb_ring_2 = hpath("M 126 404 C 138 398 148 400 156 406", amount=1.8, seed="nb-r2")
    nb_ring_3 = hpath("M 130 442 C 142 436 152 438 160 444", amount=1.8, seed="nb-r3")
    nb_line_L1 = hpath("M 54 382 L 112 376", amount=2.5, seed="nb-ll1")
    nb_line_L2 = hpath("M 58 412 L 106 408", amount=2.5, seed="nb-ll2")
    nb_line_L3 = hpath("M 60 442 L 118 436", amount=2.5, seed="nb-ll3")
    nb_sketch_R = wobbly_circle(190, 402, 24, seed="nb-circ", wobble=0.07, overlap=14)

    # 4. Steaming Coffee Mug on Foreground Right
    steam_1 = hpath("M 366 286 C 354 262 378 242 364 218", amount=2.8, seed="stm-1")
    steam_2 = hpath("M 394 276 C 382 246 408 224 396 194", amount=2.8, seed="stm-2")
    steam_3 = hpath("M 422 290 C 412 268 432 250 422 230", amount=2.8, seed="stm-3")

    mug_fill = hpath("M 346 312 L 444 304 L 432 428 L 356 434 Z", amount=4.8, seed="mug-fill")
    # Asymmetric handified ceramic dipped-glaze wave at base of mug (fixes symmetry warning)
    mug_glaze_fill = hpath(
        "M 352 396 C 378 382 408 404 436 384 L 432 428 L 356 434 Z",
        amount=4.2,
        seed="mug-glaze",
    )
    mug_out_1 = hpath("M 346 312 L 444 304 L 432 428", amount=4.5, overshoot=8.0, seed="mug-o1")
    mug_out_2 = hpath("M 432 428 L 356 434 L 346 312", amount=4.5, overshoot=8.0, seed="mug-o2")
    mug_rim_arc = hpath("M 348 314 C 376 326 416 322 442 306", amount=2.5, seed="mug-rim")
    # Mug handle with intentional breathing gap at lower join (art-direction 'Ends and gaps')
    mug_handle = hpath("M 442 326 C 482 324 484 390 444 398", amount=3.2, seed="mug-hdl")
    mug_band = hpath("M 352 396 C 378 382 408 404 436 384", amount=3.0, seed="mug-band")

    # 5. Paper Plane taking off in Upper-Right (breaking out past clay focal wash)
    plane_fill = hpath("M 362 118 L 490 62 L 432 162 L 402 132 Z", amount=4.0, seed="pl-fill")
    plane_wing_top = hpath("M 362 118 L 490 62 L 402 132 Z", amount=3.8, seed="pl-wtop")
    plane_wing_bot = hpath("M 402 132 L 490 62 L 432 162 L 402 132", amount=3.8, seed="pl-wbot")
    plane_strut = hpath("M 402 132 L 410 158 L 424 142", amount=2.5, seed="pl-strut")

    # Motion wind lines behind paper plane (varied lengths)
    wind_1 = hpath("M 316 152 L 352 130", amount=2.2, seed="wnd-1")
    wind_2 = hpath("M 342 180 L 388 152", amount=2.2, seed="wnd-2")

    # 6. Accents: Sparkle cluster in upper-right flight zone + 1 echo
    sp_1 = sparkle(416, 42, 20, seed="d-sp1")
    sp_2 = sparkle(370, 58, 13, seed="d-sp2")
    sp_3 = sparkle(466, 132, 11, seed="d-sp3")
    sp_echo = sparkle(48, 244, 13, seed="d-specho")

    clay_fill, _ = COLORS["clay"]
    sky_fill, _ = COLORS["sky"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{build_defs(seed_wash=53, seed_ink=71)}
<g id="layer-block" filter="url(#wash)" style="isolation: isolate">
{wash_blob(wash_sky, "sky", blend="normal", cls="wash-blob wash-1")}
{wash_blob(wash_peach, "peach", blend="multiply", cls="wash-blob wash-2")}
{wash_blob(wash_clay, "clay", blend="normal", cls="wash-blob wash-3")}
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- 1. Background desk horizon & flight trail behind monitor -->
  <path class="draw-stroke" data-step="1" pathLength="1" d="{desk_horizon_L}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="2" pathLength="1" d="{desk_horizon_R}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="3" pathLength="1" d="{plane_trail_back}" stroke-width="5.5" stroke-dasharray="14 18"/>

  <!-- 2. Studio Display Monitor -->
  <path class="paper-fill" data-step="4" d="{stand_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="5" pathLength="1" d="{stand_neck_L}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="6" pathLength="1" d="{stand_neck_R}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="7" pathLength="1" d="{stand_base}" stroke-width="8.5"/>

  <path class="paper-fill" data-step="8" d="{mon_outer_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="9" pathLength="1" d="{mon_out_top}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="10" pathLength="1" d="{mon_out_bot}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="11" pathLength="1" d="{mon_chin}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="12" pathLength="1" d="{scr_sidebar}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="13" pathLength="1" d="{scr_code_1}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="14" pathLength="1" d="{scr_code_2}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="15" pathLength="1" d="{scr_code_3}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="16" pathLength="1" d="{scr_wave}" stroke-width="6.0"/>

  <!-- 3. Open Notebook in Foreground Left -->
  <path class="paper-fill" data-step="17" d="{nb_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="18" pathLength="1" d="{nb_out_1}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="19" pathLength="1" d="{nb_out_2}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="20" pathLength="1" d="{nb_spine}" stroke-width="6.5"/>
  <path class="draw-stroke" data-step="21" pathLength="1" d="{nb_ring_1}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="22" pathLength="1" d="{nb_ring_2}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="23" pathLength="1" d="{nb_ring_3}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="24" pathLength="1" d="{nb_line_L1}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="25" pathLength="1" d="{nb_line_L2}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="26" pathLength="1" d="{nb_line_L3}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="27" pathLength="1" d="{nb_sketch_R}" stroke-width="5.5"/>

  <!-- 4. Steaming Mug on Right -->
  <path class="paper-fill" data-step="28" d="{mug_fill}" fill="{PAPER}" stroke="none"/>
  <path class="paper-fill" data-step="29" d="{mug_glaze_fill}" fill="{clay_fill}" fill-opacity="0.32" stroke="none"/>
  <path class="draw-stroke" data-step="30" pathLength="1" d="{mug_out_1}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="31" pathLength="1" d="{mug_out_2}" stroke-width="8.5"/>
  <path class="draw-stroke" data-step="32" pathLength="1" d="{mug_rim_arc}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="33" pathLength="1" d="{mug_handle}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="34" pathLength="1" d="{mug_band}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="35" pathLength="1" d="{steam_1}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="36" pathLength="1" d="{steam_2}" stroke-width="5.5"/>
  <path class="draw-stroke" data-step="37" pathLength="1" d="{steam_3}" stroke-width="5.5"/>

  <!-- 5. Paper Plane Launching Across Upper-Right -->
  <path class="paper-fill" data-step="38" d="{plane_fill}" fill="{PAPER}" stroke="none"/>
  <path class="draw-stroke" data-step="39" pathLength="1" d="{plane_wing_top}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="40" pathLength="1" d="{plane_wing_bot}" stroke-width="8.0"/>
  <path class="draw-stroke" data-step="41" pathLength="1" d="{plane_strut}" stroke-width="6.0"/>
  <path class="draw-stroke" data-step="42" pathLength="1" d="{wind_1}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="43" pathLength="1" d="{wind_2}" stroke-width="5.0"/>

  <!-- 6. Accents -->
  <path class="draw-stroke" data-step="44" pathLength="1" d="{sp_1}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="45" pathLength="1" d="{sp_2}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="46" pathLength="1" d="{sp_3}" stroke-width="5.0"/>
  <path class="draw-stroke" data-step="47" pathLength="1" d="{sp_echo}" stroke-width="5.0"/>
  <circle class="paper-fill" data-step="48" cx="348" cy="50" r="4.5" fill="{INK}" stroke="none"/>
  <circle class="paper-fill" data-step="49" cx="472" cy="96" r="4.0" fill="{sky_fill}" stroke="none"/>
</g>
</svg>
"""
    return svg


def build_motion_showcase_html(slide_svg, desk_svg):
    """Build self-contained HTML presentation & motion showcase with replay controls."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CC-lineart — Motion &amp; Presentation Deck Showcase</title>
<style>
  :root {{
    --paper: #FAF9F5;
    --paper-card: #F3F1EA;
    --ink: #141413;
    --ink-muted: #5C5B56;
    --clay: #D97757;
    --olive: #788C5D;
    --sky: #6A9BCC;
    --border: rgba(20, 20, 19, 0.12);
    --speed: 1;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: "Instrument Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.5;
    padding: 32px 24px 64px;
  }}
  .container {{
    max-width: 1240px;
    margin: 0 auto;
  }}
  header {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-end;
    gap: 20px;
    padding-bottom: 24px;
    border-bottom: 1.5px solid var(--border);
    margin-bottom: 32px;
  }}
  .eyebrow {{
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--clay);
    font-weight: 700;
    margin-bottom: 6px;
  }}
  h1 {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(28px, 3.5vw, 40px);
    font-weight: 500;
    margin: 0;
    letter-spacing: -0.02em;
  }}
  .subtitle {{
    color: var(--ink-muted);
    margin: 6px 0 0;
    max-width: 660px;
    font-size: 15px;
  }}
  .toolbar {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    background: var(--paper-card);
    padding: 10px 14px;
    border-radius: 999px;
    border: 1px solid var(--border);
  }}
  button {{
    appearance: none;
    border: 1.5px solid var(--ink);
    background: var(--ink);
    color: var(--paper);
    font-size: 13px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 999px;
    cursor: pointer;
    transition: transform 0.15s ease, background 0.15s ease;
  }}
  button:hover {{
    transform: translateY(-1px);
  }}
  button.secondary {{
    background: transparent;
    color: var(--ink);
  }}
  button.secondary.active {{
    background: var(--clay);
    border-color: var(--clay);
    color: var(--paper);
  }}
  .speed-label {{
    font-size: 12px;
    color: var(--ink-muted);
    padding: 0 6px;
    font-variant-numeric: tabular-nums;
  }}
  .deck-grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 32px;
  }}
  .slide-card {{
    background: var(--paper-card);
    border: 1.5px solid var(--border);
    border-radius: 24px;
    padding: 36px;
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 36px;
    align-items: center;
    box-shadow: 0 12px 36px rgba(20, 20, 19, 0.04);
  }}
  @media (max-width: 900px) {{
    .slide-card {{
      grid-template-columns: 1fr;
      padding: 24px;
    }}
  }}
  .slide-copy {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .slide-tag {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--ink-muted);
  }}
  .slide-tag span.dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--clay);
  }}
  .slide-copy h2 {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(24px, 2.6vw, 34px);
    font-weight: 500;
    margin: 0;
    line-height: 1.2;
  }}
  .slide-copy p {{
    margin: 0;
    color: var(--ink-muted);
    font-size: 15px;
  }}
  .act-list {{
    display: grid;
    gap: 12px;
    margin-top: 8px;
  }}
  .act-item {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 12px;
    align-items: baseline;
  }}
  .act-num {{
    font-family: Georgia, serif;
    font-weight: 700;
    color: var(--clay);
    font-size: 14px;
  }}
  .act-item strong {{
    display: block;
    font-size: 14px;
    margin-bottom: 2px;
  }}
  .act-item span {{
    font-size: 13px;
    color: var(--ink-muted);
  }}
  .art-stage {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 16px;
    position: relative;
    aspect-ratio: 1 / 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}
  .art-stage svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}
  .stage-badge {{
    position: absolute;
    bottom: 14px;
    right: 16px;
    font-size: 11px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    color: var(--ink-muted);
    background: rgba(250, 249, 245, 0.88);
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid var(--border);
  }}

  /* ---- Sequenced Hand-Drawn Stroke & Breathing Wash Animations ---- */
  .animated-active .draw-stroke {{
    stroke-dasharray: 1;
    stroke-dashoffset: 1;
    animation: drawStroke calc(0.42s / var(--speed)) cubic-bezier(0.35, 0, 0.25, 1) forwards;
    animation-delay: calc(var(--step, 1) * 0.06s / var(--speed));
  }}
  .animated-active .paper-fill {{
    opacity: 0;
    animation: fadePaper calc(0.38s / var(--speed)) ease-out forwards;
    animation-delay: calc((var(--step, 1) * 0.06s + 0.14s) / var(--speed));
  }}
  .animated-active .wash-blob {{
    transform-origin: 50% 50%;
    animation: washReveal calc(0.7s / var(--speed)) ease-out forwards,
               washBreathe 7s ease-in-out infinite alternate;
  }}
  .animated-active .wash-2 {{
    animation-delay: calc(0.12s / var(--speed)), 1.4s;
  }}
  .animated-active .wash-3 {{
    animation-delay: calc(0.24s / var(--speed)), 2.8s;
  }}

  /* Wireframe-only inspection mode (hides paper fills so underlying strokes show) */
  .wireframe-mode .paper-fill {{
    opacity: 0.12 !important;
  }}

  @keyframes drawStroke {{
    0% {{ stroke-dashoffset: 1; }}
    100% {{ stroke-dashoffset: 0; }}
  }}
  @keyframes fadePaper {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 1; }}
  }}
  @keyframes washReveal {{
    0% {{ opacity: 0; transform: scale(0.94); }}
    100% {{ opacity: 1; transform: scale(1); }}
  }}
  @keyframes washBreathe {{
    0% {{ transform: translate(0px, 0px) scale(1); }}
    100% {{ transform: translate(4px, -3px) scale(1.018); }}
  }}
</style>
</head>
<body class="animated-active">
<div class="container">
  <header>
    <div>
      <div class="eyebrow">CC-lineart · Track 5 Exploration</div>
      <h1>Animated Line-Art &amp; Presentation Deck Visuals</h1>
      <p class="subtitle">
        Because every <code>&lt;path&gt;</code> in <code>CC-lineart</code> is authored as a single intentional pen stroke, adding <code>pathLength="1"</code> turns static Keynote/deck illustrations into self-drawing ink animations with zero geometry changes.
      </p>
    </div>
    <div class="toolbar">
      <button id="btn-replay" type="button">↻ Replay Ink Draw</button>
      <button id="btn-speed" class="secondary" type="button">Speed: 1×</button>
      <button id="btn-wireframe" class="secondary" type="button">Peek Under Paper</button>
      <span class="speed-label" id="status-readout">49 steps sequenced</span>
    </div>
  </header>

  <div class="deck-grid">
    <!-- Slide 1: Editorial 3-Act Story -->
    <section class="slide-card">
      <div class="slide-copy">
        <div class="slide-tag"><span class="dot"></span> Slide 01 · Architecture Narrative</div>
        <h2>From Rough Sketch to Autonomous Execution to Shipped Artifact</h2>
        <p>
          Designed as a 16:9 presentation hero slide where a 512×512 illustration anchors the right column. Three overlapping watercolor washes (<code>olive</code> + <code>peach</code> glazed via <code>multiply</code>, plus a <code>clay</code> focal spot) guide the eye diagonally upward.
        </p>
        <div class="act-list">
          <div class="act-item">
            <span class="act-num">I.</span>
            <div>
              <strong>Human Intent &amp; Sketching (Lower-Left)</strong>
              <span>Dog-eared notepad and fountain pen establish the initial specification over an earthy olive wash.</span>
            </div>
          </div>
          <div class="act-item">
            <span class="act-num">II.</span>
            <div>
              <strong>Agent Execution Loop (Center Glaze)</strong>
              <span>Terminal chevron and 7-ray starburst sit where warm peach and cool olive washes glaze together.</span>
            </div>
          </div>
          <div class="act-item">
            <span class="act-num">III.</span>
            <div>
              <strong>Verified Artifact Release (Upper-Right)</strong>
              <span>Polished release card and clay focal badge break out of the wash into open canvas.</span>
            </div>
          </div>
        </div>
      </div>
      <div class="art-stage" id="stage-story">
        {slide_svg}
        <div class="stage-badge">slide-editorial-story.svg · 512×512</div>
      </div>
    </section>

    <!-- Slide 2: Animated Creative Desk -->
    <section class="slide-card">
      <div class="slide-copy">
        <div class="slide-tag"><span class="dot"></span> Slide 02 · Editorial Scene &amp; Motion Study</div>
        <h2>The Creative Agent's Desk: Sequenced Pen Strokes &amp; Breathing Wash</h2>
        <p>
          Each element follows strict paint order: background desk horizon and dashed flight trail draw first, then paper fills fade in as the studio monitor, spiral notebook, steaming ceramic mug, and paper plane complete their outlines.
        </p>
        <div class="act-list">
          <div class="act-item">
            <span class="act-num">01</span>
            <div>
              <strong>One Pen Stroke at a Time (<code>pathLength="1"</code>)</strong>
              <span>Overshooting corners are separate open strokes, so the viewer sees each corner cross like a real felt-tip pen.</span>
            </div>
          </div>
          <div class="act-item">
            <span class="act-num">02</span>
            <div>
              <strong>Layered Depth &amp; Occlusion</strong>
              <span>Use "Peek Under Paper" above to see how the dashed trajectory and desk horizon pass cleanly behind the monitor's <code>#FAF9F5</code> paper fill.</span>
            </div>
          </div>
          <div class="act-item">
            <span class="act-num">03</span>
            <div>
              <strong>Static + Dynamic Dual Compatibility</strong>
              <span>Renders identically via <code>rsvg-convert</code> for PDF/Keynote export while animating natively in HTML decks.</span>
            </div>
          </div>
        </div>
      </div>
      <div class="art-stage" id="stage-desk">
        {desk_svg}
        <div class="stage-badge">animated-creative-desk.svg · 512×512</div>
      </div>
    </section>
  </div>
</div>

<script>
  function assignSteps() {{
    document.querySelectorAll('[data-step]').forEach(el => {{
      el.style.setProperty('--step', el.getAttribute('data-step'));
    }});
  }}
  assignSteps();

  const btnReplay = document.getElementById('btn-replay');
  const btnSpeed = document.getElementById('btn-speed');
  const btnWire = document.getElementById('btn-wireframe');
  const readout = document.getElementById('status-readout');
  const speeds = [1, 0.5, 2];
  let speedIdx = 0;

  function replayAnimation() {{
    document.body.classList.remove('animated-active');
    void document.body.offsetWidth;
    document.body.classList.add('animated-active');
    readout.textContent = 'Replaying stroke sequence (' + speeds[speedIdx] + '×)...';
  }}

  btnReplay.addEventListener('click', replayAnimation);

  btnSpeed.addEventListener('click', () => {{
    speedIdx = (speedIdx + 1) % speeds.length;
    const s = speeds[speedIdx];
    document.documentElement.style.setProperty('--speed', s);
    btnSpeed.textContent = 'Speed: ' + s + '×';
    replayAnimation();
  }});

  btnWire.addEventListener('click', () => {{
    document.body.classList.toggle('wireframe-mode');
    btnWire.classList.toggle('active');
  }});
</script>
</body>
</html>
"""


def main():
    slide_svg = build_slide_editorial_story()
    desk_svg = build_animated_creative_desk()

    slide_path = os.path.join(HERE, "slide-editorial-story.svg")
    desk_path = os.path.join(HERE, "animated-creative-desk.svg")
    html_path = os.path.join(HERE, "motion-showcase.html")

    with open(slide_path, "w", encoding="utf-8") as f:
        f.write(slide_svg)
    with open(desk_path, "w", encoding="utf-8") as f:
        f.write(desk_svg)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_motion_showcase_html(slide_svg, desk_svg))

    print("Generated:")
    print(" ", slide_path)
    print(" ", desk_path)
    print(" ", html_path)


if __name__ == "__main__":
    main()
