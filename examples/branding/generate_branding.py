#!/usr/bin/env python3
"""Generate Track 4 Open-Source Repo Branding & Editorial Badges in CC-lineart style.

Outputs in /Users/wu/CC-lineart/examples/branding/:
  - release-hero-card.svg (512x512)
  - editorial-badges.svg  (512x512)
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

from lineart import COLORS, INK, PAPER, handify, sparkle, wobbly_circle  # noqa: E402


def double_stroke_group(paths_d, w_paper=15.0, t_border=8.0):
    """Render centerline paths as unified paper-cutout lettering/marks.

    Draws all INK passes at width (W + 2t) first, then all PAPER passes at width W,
    so intersecting strokes merge cleanly without internal seams.
    """
    w_ink = w_paper + 2.0 * t_border
    lines = []
    for d in paths_d:
        lines.append(
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w_ink:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    for d in paths_d:
        lines.append(
            f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-width="{w_paper:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    return "\n".join(lines)


def build_defs(seed_wash=23, seed_ink=41):
    """512x512 scaled watercolor wash and ink wobble filters per drawing-guide.md."""
    return f"""<defs>
<filter id="wash" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="4" seed="{seed_wash}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="13" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.05 1.42" result="a"/>
  <feComposite in="d" in2="a" operator="in"/>
</filter>
<filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="{seed_ink}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6.2" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>"""


def generate_release_hero_card():
    """Build release-hero-card.svg (512x512): 'v2.0 Release / CLI & Agent SDK'."""
    clay_fill, clay_edge = COLORS["clay"]
    sky_fill, sky_edge = COLORS["sky"]
    olive_fill, olive_edge = COLORS["olive"]
    peach_fill, _ = COLORS["peach"]

    # 1. Watercolor washes: warm clay (center-left) + cool sky (upper-right) glazed with
    #    mix-blend-mode: multiply inside an isolated group, plus an olive focal spot lower-right.
    wash_clay = handify("M 68 158 L 312 138 L 328 398 L 84 416 Z", amount=5.5, seed="hero-wash-clay")
    wash_sky = handify("M 216 84 L 452 104 L 436 342 L 202 320 Z", amount=5.5, seed="hero-wash-sky")
    wash_olive = wobbly_circle(392, 402, 42, seed="hero-wash-olive", wobble=0.07)

    # 2. Background elements behind the main terminal subject:
    #    - SDK blueprint card tilted behind upper-left of terminal
    back_card = handify("M 74 142 L 236 122 L 248 252 L 86 268 Z", amount=4.5, seed="back-card")
    back_card_grid1 = handify("M 96 172 L 216 158", amount=3.2, seed="bc-g1")
    back_card_grid2 = handify("M 102 204 L 192 192", amount=3.2, seed="bc-g2")

    #    - Agent gear wheel tucked behind mid-left of terminal so lower-left stays quiet
    gear_body = handify(
        "M 118 256 L 94 260 L 82 244 L 64 252 L 70 272 L 58 286 "
        "L 38 280 L 32 300 L 52 310 L 54 326 L 38 336 L 48 354 "
        "L 68 346 L 84 358 L 82 376 L 104 378 L 110 360 L 132 354 Z",
        amount=2.8,
        seed="gear-body",
    )
    gear_hub = wobbly_circle(96, 310, 18, seed="gear-inner", wobble=0.12)

    #    - Sweeping trajectory trail from behind terminal up to the paper plane
    trail_arc1 = handify("M 262 244 C 304 196 338 166 368 146", amount=3.5, seed="trail-1")
    trail_arc2 = handify("M 188 308 C 216 280 238 262 248 254", amount=3.0, seed="trail-2")

    # 3. Main subject: CLI & Agent SDK Terminal Window
    #    Includes an intentional breathing gap on the left frame just below the header divider.
    term_body = handify("M 114 196 L 386 180 L 398 412 L 124 428 Z", amount=4.8, seed="term-body")
    term_frame_top = handify("M 106 197 L 396 179", amount=4.0, seed="term-ft")
    term_frame_rest = handify("M 386 174 L 398 412 L 124 428 L 116 262", amount=4.5, seed="term-fr")
    term_frame_left_top = handify("M 114 192 L 115 240", amount=2.5, seed="term-flt")
    term_header_div = handify("M 115 242 L 390 227", amount=3.5, seed="term-div")

    # Terminal window control dots (compact r=6.0 so mext < 15.3)
    dot1 = wobbly_circle(142, 218, 6.0, seed="tdot1", wobble=0.12)
    dot2 = wobbly_circle(166, 217, 5.8, seed="tdot2", wobble=0.12)
    dot3 = wobbly_circle(189, 215, 6.0, seed="tdot3", wobble=0.12)

    # Interior peach highlight strip behind the active command prompt
    prompt_patch = handify("M 134 266 L 298 256 L 301 294 L 136 304 Z", amount=3.0, seed="prompt-patch")

    # Terminal CLI chevron `>_` and varied code lines
    cli_chevron = handify("M 144 272 L 166 283 L 146 296", amount=2.2, seed="cli-chev")
    cli_cursor = handify("M 178 295 L 204 293", amount=2.0, seed="cli-cur")
    code_line1 = handify("M 218 280 L 336 272", amount=3.0, seed="code-1")
    code_line2 = handify("M 148 330 L 312 320", amount=3.2, seed="code-2")
    code_line3 = handify("M 172 360 L 348 349", amount=3.2, seed="code-3")
    code_line4 = handify("M 150 390 L 264 383", amount=3.0, seed="code-4")

    # 4. Foreground element 1: Expressive paper plane launching out of the terminal (upper-right)
    #    Spans from (318, 134) out to nose at (476, 62), breaking out of the sky wash!
    plane_paper = handify(
        "M 318 134 L 476 62 L 404 186 L 368 152 L 342 176 L 338 142 Z",
        amount=3.5,
        seed="plane-paper",
    )
    plane_outline = handify(
        "M 318 134 L 476 62 L 404 186 L 368 152 L 342 176 L 338 142 L 318 134",
        amount=3.5,
        seed="plane-out",
    )
    plane_crease1 = handify("M 472 64 L 338 142", amount=2.8, seed="plane-c1")
    plane_crease2 = handify("M 472 64 L 368 152", amount=2.8, seed="plane-c2")
    plane_wing_tint = handify("M 338 142 L 456 74 L 368 152 Z", amount=2.5, seed="plane-tint")

    # 5. Foreground element 2: Double-stroked paper-cutout lettering "v2.0"
    #    Positioned across upper-left (x: 44..294, y: 56..158), overlapping the blueprint card
    #    and terminal corner, breaking out into the upper-left paper space.
    v_path = handify("M 48 88 L 74 144 L 104 82", amount=2.6, seed="let-v")
    two_path = handify(
        "M 126 88 C 132 60 176 58 178 88 C 180 112 128 128 126 148 L 184 145",
        amount=2.6,
        seed="let-2",
    )
    dot_path = handify("M 206 142 L 210 147", amount=1.2, seed="let-dot")
    zero_path = wobbly_circle(256, 104, 38, seed="let-0", wobble=0.08, overlap=18)

    v20_cutout = double_stroke_group([v_path, two_path, dot_path, zero_path], w_paper=14.5, t_border=8.5)

    # 6. Foreground element 3: "SDK" stamp pill overlapping lower-right of terminal
    sdk_pill = handify("M 294 366 L 462 354 L 468 434 L 300 446 Z", amount=3.8, seed="sdk-pill")
    sdk_inner = handify("M 308 378 L 450 368 L 454 422 L 312 432", amount=2.8, seed="sdk-in")
    s_let = handify(
        "M 352 386 C 330 384 326 400 342 404 C 360 408 356 424 330 422",
        amount=1.6,
        seed="sdk-s",
    )
    d_let = handify(
        "M 370 384 L 372 420 C 402 420 402 382 370 384",
        amount=1.8,
        seed="sdk-d",
    )
    k_let1 = handify("M 414 382 L 414 420", amount=1.6, seed="sdk-k1")
    k_let2 = handify("M 438 382 L 416 401 L 440 420", amount=1.6, seed="sdk-k2")

    # 7. Accents: 1 cluster of 3 sparkles (sizes 1 : 0.6 : 0.4) + 2 dots in the quiet lower-left quadrant
    sp1 = sparkle(64, 424, 16.0, seed="hero-sp1")
    sp2 = sparkle(96, 452, 10.0, seed="hero-sp2")
    sp3 = sparkle(46, 462, 6.6, seed="hero-sp3")
    acc_dot1 = wobbly_circle(82, 412, 3.2, seed="hero-ad1")
    acc_dot2 = wobbly_circle(458, 224, 3.4, seed="hero-ad2")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{build_defs(seed_wash=29, seed_ink=53)}
<g id="layer-block" filter="url(#wash)" style="isolation:isolate">
  <path d="{wash_clay}" fill="{clay_fill}"/>
  <path d="{wash_clay}" fill="none" stroke="{clay_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  <path d="{wash_sky}" fill="{sky_fill}" fill-opacity="0.88" style="mix-blend-mode:multiply"/>
  <path d="{wash_sky}" fill="none" stroke="{sky_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  <path d="{wash_olive}" fill="{olive_fill}" fill-opacity="0.84"/>
  <path d="{wash_olive}" fill="none" stroke="{olive_edge}" stroke-width="4.2" stroke-opacity="0.55" stroke-linejoin="round"/>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Behind subject: SDK blueprint card & agent gear -->
  <path d="{back_card}" fill="{PAPER}" stroke-width="7.5"/>
  <path d="{back_card_grid1}" stroke-width="5.5"/>
  <path d="{back_card_grid2}" stroke-width="5.5"/>

  <path d="{gear_body}" fill="{PAPER}" stroke-width="8.0"/>
  <path d="{gear_hub}" fill="{clay_fill}" stroke-width="6.5"/>

  <!-- Sweeping launch trajectory behind terminal & plane -->
  <path d="{trail_arc1}" stroke-width="6.0" stroke-dasharray="16 18"/>
  <path d="{trail_arc2}" stroke-width="6.0" stroke-dasharray="14 18"/>

  <!-- Main Subject: CLI & Agent SDK Terminal -->
  <path d="{term_body}" fill="{PAPER}" stroke="none"/>
  <path d="{prompt_patch}" fill="{peach_fill}" stroke="none"/>
  <path d="{term_frame_top}" stroke-width="9.0"/>
  <path d="{term_frame_rest}" stroke-width="9.0"/>
  <path d="{term_frame_left_top}" stroke-width="9.0"/>
  <path d="{term_header_div}" stroke-width="7.0"/>

  <path d="{dot1}" fill="{clay_fill}" stroke-width="5.5"/>
  <path d="{dot2}" fill="{PAPER}" stroke-width="5.5"/>
  <path d="{dot3}" fill="{PAPER}" stroke-width="5.5"/>

  <path d="{cli_chevron}" stroke-width="7.5"/>
  <path d="{cli_cursor}" stroke-width="7.5"/>
  <path d="{code_line1}" stroke-width="7.0"/>
  <path d="{code_line2}" stroke-width="6.5"/>
  <path d="{code_line3}" stroke-width="6.5"/>
  <path d="{code_line4}" stroke-width="6.5"/>

  <!-- Foreground: Paper plane breaking out of upper-right wash -->
  <path d="{plane_paper}" fill="{PAPER}" stroke="none"/>
  <path d="{plane_wing_tint}" fill="{clay_fill}" stroke="none"/>
  <path d="{plane_outline}" stroke-width="8.5"/>
  <path d="{plane_crease1}" stroke-width="6.0"/>
  <path d="{plane_crease2}" stroke-width="6.0"/>

  <!-- Foreground: Double-stroked cutout lettering "v2.0" -->
  {v20_cutout}

  <!-- Foreground: SDK release stamp pill overlapping lower-right -->
  <path d="{sdk_pill}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{sdk_inner}" stroke-width="5.0"/>
  <path d="{s_let}" stroke-width="6.5"/>
  <path d="{d_let}" stroke-width="6.5"/>
  <path d="{k_let1}" stroke-width="6.5"/>
  <path d="{k_let2}" stroke-width="6.5"/>

  <!-- Quiet lower-left sparkle cluster (3 sparkles + 2 dots) -->
  <path d="{sp1}" stroke-width="5.2"/>
  <path d="{sp2}" stroke-width="5.0"/>
  <path d="{sp3}" stroke-width="4.8"/>
  <path d="{acc_dot1}" fill="{INK}" stroke-width="4.0"/>
  <path d="{acc_dot2}" fill="{INK}" stroke-width="4.0"/>
</g>
</svg>
"""
    return svg


def generate_editorial_badges():
    """Build editorial-badges.svg (512x512): 4 artisanal developer stamps/badges."""
    clay_fill, clay_edge = COLORS["clay"]
    sky_fill, sky_edge = COLORS["sky"]
    olive_fill, olive_edge = COLORS["olive"]
    plum_fill, plum_edge = COLORS["plum"]
    peach_fill, peach_edge = COLORS["peach"]
    kraft_fill, _ = COLORS["kraft"]

    # Watercolor washes: offset behind the 4 badge quadrants with warm/cool multiply glazes
    w_tl = handify("M 38 48 L 212 36 L 224 194 L 48 210 Z", amount=4.8, seed="b-wash-tl")
    w_tr = handify("M 268 62 L 444 48 L 456 212 L 282 224 Z", amount=4.8, seed="b-wash-tr")
    w_bl = handify("M 54 286 L 228 272 L 240 438 L 66 454 Z", amount=4.8, seed="b-wash-bl")
    w_br = handify("M 272 266 L 448 282 L 434 428 L 260 414 Z", amount=4.8, seed="b-wash-br")
    w_glaze = wobbly_circle(254, 244, 52, seed="b-wash-glaze", wobble=0.07)

    # =========================================================================
    # BADGE 1 (Top-Left): "OK" VERIFIED SHIELD & CHECK STAMP
    # =========================================================================
    b1_ribbon_l = handify("M 52 190 L 22 220 L 48 226 L 44 250 L 86 212", amount=3.0, seed="b1-rl")
    b1_ribbon_r = handify("M 196 182 L 232 210 L 206 220 L 214 242 L 170 206", amount=3.0, seed="b1-rr")
    b1_shield = handify(
        "M 68 56 L 194 48 L 200 144 C 200 192 136 226 132 230 C 126 226 64 194 64 148 Z",
        amount=4.0,
        seed="b1-shield",
    )
    b1_inner_arc = handify("M 84 76 L 178 70 L 182 138", amount=3.0, seed="b1-in")
    b1_check_patch = wobbly_circle(132, 134, 34, seed="b1-cpatch", wobble=0.06)
    # Centerline double-stroked checkmark breaking across the shield edge
    b1_check = handify("M 96 136 L 124 164 L 186 94", amount=2.5, seed="b1-chk")
    b1_check_cutout = double_stroke_group([b1_check], w_paper=12.0, t_border=7.5)

    # =========================================================================
    # BADGE 2 (Top-Right): "v2" WAX SEAL & RELEASE STAMP
    # =========================================================================
    b2_ribbon1 = handify("M 332 194 L 308 250 L 336 240 L 352 258 L 366 200", amount=2.8, seed="b2-r1")
    b2_ribbon2 = handify("M 384 196 L 404 254 L 418 234 L 442 244 L 412 188", amount=2.8, seed="b2-r2")
    b2_outer = wobbly_circle(376, 126, 72, seed="b2-out", wobble=0.07, overlap=18)
    b2_inner = wobbly_circle(376, 126, 52, seed="b2-in", wobble=0.05, overlap=12)
    b2_wax_tint = wobbly_circle(368, 120, 40, seed="b2-tint", wobble=0.06)
    # Double-stroked "v2" centerline stamp across the seal
    b2_v = handify("M 332 106 L 350 148 L 370 102", amount=2.2, seed="b2-v")
    b2_2 = handify(
        "M 386 108 C 390 88 420 88 420 108 C 420 124 386 134 384 148 L 424 146",
        amount=2.0,
        seed="b2-2",
    )
    b2_cutout = double_stroke_group([b2_v, b2_2], w_paper=11.5, t_border=7.0)

    # =========================================================================
    # BADGE 3 (Bottom-Left): "OSS" OPEN-SOURCE BRANCH & OCTAGONAL ROSETTE
    # =========================================================================
    b3_stem_back = handify("M 40 424 L 224 282", amount=4.0, seed="b3-stem")
    b3_plaque = handify(
        "M 86 278 L 176 270 L 216 308 L 220 392 L 180 434 L 92 440 L 52 402 L 48 318 Z",
        amount=4.0,
        seed="b3-plaque",
    )
    b3_git_main = handify("M 112 312 L 114 400", amount=2.4, seed="b3-gm")
    b3_git_fork = handify("M 114 364 C 140 362 156 348 160 322", amount=2.4, seed="b3-gf")
    # Compact r=6.0 so mext < 15.36 and never triggers mirror-symmetric clip-art warning
    b3_node1 = wobbly_circle(112, 308, 6.0, seed="b3-n1", wobble=0.12)
    b3_node2 = wobbly_circle(114, 404, 6.0, seed="b3-n2", wobble=0.12)
    b3_node3 = wobbly_circle(160, 316, 6.0, seed="b3-n3", wobble=0.12)

    # Banner ribbon across lower-right of Badge 3 with "OSS"
    b3_banner = handify("M 126 378 L 246 368 L 250 422 L 130 432 Z", amount=3.2, seed="b3-ban")
    b3_o = handify(
        "M 156 390 C 142 392 140 416 154 418 C 168 418 172 394 156 390",
        amount=1.6,
        seed="b3-o",
    )
    b3_s1 = handify("M 194 389 C 178 388 176 399 188 402 C 200 405 196 416 178 414", amount=1.5, seed="b3-s1")
    b3_s2 = handify("M 228 387 C 212 386 210 397 222 400 C 234 403 230 414 212 412", amount=1.5, seed="b3-s2")

    # =========================================================================
    # BADGE 4 (Bottom-Right): "BETA" LAB TAG & LIGHTNING STAMP
    # =========================================================================
    b4_cord = handify("M 278 286 C 254 262 262 238 292 250", amount=2.8, seed="b4-cord")
    b4_tag_fill = handify(
        "M 280 282 L 322 258 L 464 274 L 452 416 L 270 398 Z",
        amount=4.2,
        seed="b4-tag-fill",
    )
    b4_tag_frame = handify(
        "M 274 284 L 322 258 L 470 275 L 450 422 L 264 396 L 282 276",
        amount=4.2,
        seed="b4-tag-frame",
    )
    b4_hole = wobbly_circle(304, 294, 6.0, seed="b4-hole", wobble=0.12)
    # Expressive lightning bolt breaking out of top-right of the tag
    b4_bolt = handify(
        "M 394 242 L 344 322 L 384 324 L 356 394 L 434 306 L 394 304 Z",
        amount=3.0,
        seed="b4-bolt",
    )
    # Foreground "BETA" stamp pill across lower-left/bottom of Badge 4 with centerline "BETA"
    b4_pill = handify("M 284 374 L 444 386 L 440 438 L 280 426 Z", amount=3.2, seed="b4-pill")
    b4_b1 = handify("M 304 388 L 302 416", amount=1.4, seed="b4-b1")
    b4_b2 = handify(
        "M 304 388 C 322 388 322 402 304 402 C 324 402 324 418 302 416",
        amount=1.4,
        seed="b4-b2",
    )
    b4_e1 = handify("M 354 391 L 336 390 L 334 418 L 354 419", amount=1.4, seed="b4-e1")
    b4_e2 = handify("M 335 404 L 350 405", amount=1.2, seed="b4-e2")
    b4_t1 = handify("M 366 392 L 390 394", amount=1.4, seed="b4-t1")
    b4_t2 = handify("M 378 393 L 376 421", amount=1.4, seed="b4-t2")
    # Skewed/tilted A so it reads as hand-drawn and asymmetric
    b4_a1 = handify("M 398 424 L 418 393 L 426 422", amount=1.6, seed="b4-a1")
    b4_a2 = handify("M 405 412 L 423 414", amount=1.2, seed="b4-a2")

    # =========================================================================
    # Shared quiet-area sparkle cluster (lower-right / center-top quiet channel)
    # =========================================================================
    sp1 = sparkle(372, 466, 14.0, seed="ed-sp1")
    sp2 = sparkle(404, 476, 9.0, seed="ed-sp2")
    sp3 = sparkle(344, 478, 6.2, seed="ed-sp3")
    dot_a = wobbly_circle(428, 462, 3.2, seed="ed-da")
    dot_b = wobbly_circle(248, 88, 3.4, seed="ed-db")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{build_defs(seed_wash=37, seed_ink=67)}
<g id="layer-block" filter="url(#wash)" style="isolation:isolate">
  <path d="{w_tl}" fill="{clay_fill}"/>
  <path d="{w_tl}" fill="none" stroke="{clay_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  <path d="{w_tr}" fill="{sky_fill}"/>
  <path d="{w_tr}" fill="none" stroke="{sky_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  <path d="{w_bl}" fill="{olive_fill}"/>
  <path d="{w_bl}" fill="none" stroke="{olive_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  <path d="{w_br}" fill="{plum_fill}"/>
  <path d="{w_br}" fill="none" stroke="{plum_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  <path d="{w_glaze}" fill="{peach_fill}" fill-opacity="0.88" style="mix-blend-mode:multiply"/>
  <path d="{w_glaze}" fill="none" stroke="{peach_edge}" stroke-width="4.0" stroke-opacity="0.55" stroke-linejoin="round"/>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- BADGE 1 (Top-Left): Verified Shield & Check Stamp -->
  <path d="{b1_ribbon_l}" fill="{PAPER}" stroke-width="7.0"/>
  <path d="{b1_ribbon_r}" fill="{PAPER}" stroke-width="7.0"/>
  <path d="{b1_shield}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{b1_check_patch}" fill="{peach_fill}" stroke="none"/>
  <path d="{b1_inner_arc}" stroke-width="5.5"/>
  {b1_check_cutout}

  <!-- BADGE 2 (Top-Right): v2 Wax Seal & Release Stamp -->
  <path d="{b2_ribbon1}" fill="{PAPER}" stroke-width="7.0"/>
  <path d="{b2_ribbon2}" fill="{PAPER}" stroke-width="7.0"/>
  <path d="{b2_outer}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{b2_wax_tint}" fill="{clay_fill}" stroke="none"/>
  <path d="{b2_inner}" stroke-width="5.5"/>
  {b2_cutout}

  <!-- BADGE 3 (Bottom-Left): OSS Branch & Octagonal Rosette -->
  <path d="{b3_stem_back}" stroke-width="9.0"/>
  <path d="{b3_plaque}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{b3_git_main}" stroke-width="7.0"/>
  <path d="{b3_git_fork}" stroke-width="7.0"/>
  <path d="{b3_node1}" fill="{kraft_fill}" stroke-width="5.5"/>
  <path d="{b3_node2}" fill="{PAPER}" stroke-width="5.5"/>
  <path d="{b3_node3}" fill="{clay_fill}" stroke-width="5.5"/>
  <path d="{b3_banner}" fill="{PAPER}" stroke-width="8.0"/>
  <path d="{b3_o}" stroke-width="6.0"/>
  <path d="{b3_s1}" stroke-width="6.0"/>
  <path d="{b3_s2}" stroke-width="6.0"/>

  <!-- BADGE 4 (Bottom-Right): BETA Lab Tag & Lightning Bolt -->
  <path d="{b4_cord}" stroke-width="6.5"/>
  <path d="{b4_tag_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{b4_tag_frame}" stroke-width="8.5"/>
  <path d="{b4_hole}" fill="{peach_fill}" stroke-width="5.5"/>
  <path d="{b4_bolt}" fill="{clay_fill}" stroke-width="8.0"/>
  <path d="{b4_pill}" fill="{PAPER}" stroke-width="8.0"/>
  <path d="{b4_b1}" stroke-width="5.8"/>
  <path d="{b4_b2}" stroke-width="5.8"/>
  <path d="{b4_e1}" stroke-width="5.8"/>
  <path d="{b4_e2}" stroke-width="5.8"/>
  <path d="{b4_t1}" stroke-width="5.8"/>
  <path d="{b4_t2}" stroke-width="5.8"/>
  <path d="{b4_a1}" stroke-width="5.8"/>
  <path d="{b4_a2}" stroke-width="5.8"/>

  <!-- Shared quiet-channel sparkle cluster (3 sparkles + 2 dots) -->
  <path d="{sp1}" stroke-width="5.2"/>
  <path d="{sp2}" stroke-width="5.0"/>
  <path d="{sp3}" stroke-width="4.8"/>
  <path d="{dot_a}" fill="{INK}" stroke-width="4.0"/>
  <path d="{dot_b}" fill="{INK}" stroke-width="4.0"/>
</g>
</svg>
"""
    return svg


def main():
    os.makedirs(SCRIPT_DIR, exist_ok=True)
    hero_path = os.path.join(SCRIPT_DIR, "release-hero-card.svg")
    badges_path = os.path.join(SCRIPT_DIR, "editorial-badges.svg")

    with open(hero_path, "w") as f:
        f.write(generate_release_hero_card())
    print(f"Wrote {hero_path}")

    with open(badges_path, "w") as f:
        f.write(generate_editorial_badges())
    print(f"Wrote {badges_path}")


if __name__ == "__main__":
    main()
