#!/usr/bin/env python3
"""Generate the Track 3 UI Component Kit, Empty State SVG, and Interactive HTML Demo.

Reuses `handify`, `wobbly_circle`, `sparkle`, `COLORS`, `INK`, `PAPER` from
`scripts/lineart.py` to build 512x512 UI illustrations and a live interactive HTML/CSS demo.
"""
import math
import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from lineart import COLORS, INK, PAPER, fmt, handify, sparkle, wobbly_circle  # noqa: E402


def poly_d(pts, closed=True):
    """Build an SVG path string from a sequence of (x, y) points."""
    head = f"M{fmt(pts[0])}"
    body = " ".join(f"L{fmt(p)}" for p in pts[1:])
    return f"{head} {body}" + (" Z" if closed else "")


def rounded_box_d(x, y, w, h, r=14, skew_top=0.0, skew_right=0.0):
    """Asymmetric polygon approximation of a rounded UI card so handify bows every edge cleanly."""
    r_l = r * 0.82
    r_r = r * 1.28
    pts = [
        (x + r_l, y + skew_top),
        (x + w - r_r, y - skew_top * 0.9),
        (x + w + skew_right, y + r_r * 1.15),
        (x + w - skew_right * 0.7, y + h - r_r * 0.75),
        (x + w - r_r * 1.1, y + h + skew_top * 0.8),
        (x + r_l * 0.85, y + h - skew_top * 0.5),
        (x - skew_right * 0.6, y + h - r_l * 1.2),
        (x + skew_right * 0.4, y + r_l * 0.8),
    ]
    return poly_d(pts, closed=True)


def pill_d(x, y, w, h, tilt=0.0):
    """Asymmetric hand-drawn capsule path that avoids mechanical left-right mirror symmetry."""
    r_l = h * 0.41
    r_r = h * 0.52
    k_l = r_l * 0.28
    k_r = r_r * 0.40
    pts = [
        (x + r_l, y + tilt),
        (x + w - r_r, y - tilt * 1.35),
        (x + w - k_r, y + k_r - tilt),
        (x + w + abs(tilt) * 1.4, y + h * 0.43),
        (x + w - k_r * 0.8, y + h - k_r * 1.15 + tilt),
        (x + w - r_r * 1.08, y + h + tilt * 1.1),
        (x + r_l * 0.9, y + h - tilt * 0.8),
        (x + k_l, y + h - k_l * 0.85 - tilt),
        (x - abs(tilt) * 0.6, y + h * 0.57),
        (x + k_l * 1.2, y + k_l + tilt),
    ]
    return poly_d(pts, closed=True)


def defs_512(seed=23):
    """512-grid scaled SVG filter definitions matching drawing-guide.md specifications."""
    return f"""<defs>
<filter id="wash" x="-12%" y="-12%" width="124%" height="124%">
  <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="4" seed="{seed}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="13" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.05 1.48" result="a"/>
  <feComposite in="d" in2="a" operator="in"/>
</filter>
<filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="{seed + 11}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6.2" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>"""


def build_empty_state_inbox():
    """Generate `empty-state-inbox.svg` (512x512 viewBox).

    Subject: "Zero Inbox / All Tasks Done" product UI empty state.
    Layers:
      1. Warm + cool glazed watercolor blocks (`sky` lower-left + `peach` upper-right + `clay` focal spot).
      2. Tilted background card and sweeping flight trajectory passing behind the main UI frame.
      3. Paper-white main inbox window card, floating "All clear" status toast pill, and an
         origami paper plane breaking out of the top-right frame into the quiet upper-left sky.
    """
    sky_fill, sky_edge = COLORS["sky"]
    peach_fill, peach_edge = COLORS["peach"]
    clay_fill, clay_edge = COLORS["clay"]
    cactus_fill, _ = COLORS["cactus"]

    # Layer 1: Two offset watercolor washes (cool sky + warm peach/clay glaze), coverage ~18%
    wash_cool = handify("M 58 178 L 286 154 L 304 418 L 72 436 Z", amount=6.0, seed="inbox-wash-cool")
    wash_warm = handify("M 218 96 L 446 114 L 428 336 L 204 312 Z", amount=6.0, seed="inbox-wash-warm")
    wash_focal = handify("M 332 108 L 418 118 L 408 192 L 324 184 Z", amount=4.5, seed="inbox-wash-focal")

    # Background elements (behind main paper shapes)
    # 1. Peeking secondary card tilted behind the main inbox window
    back_card_d = handify(
        "M 84 182 L 318 152 L 338 358 L 106 384 Z",
        amount=4.8,
        seed="inbox-back-card",
    )
    # 2. Architectural horizon ticks & corner registration behind the UI card
    back_ticks = " ".join([
        handify("M 42 292 L 88 289", amount=3.0, seed="tick-l"),
        handify("M 412 246 L 468 242", amount=3.0, seed="tick-r"),
        handify("M 136 410 L 132 458", amount=3.0, seed="tick-b"),
    ])
    # 3. Sweeping motion trail starting inside the tray, looping behind the plane
    trail_behind = " ".join([
        handify("M 176 306 C 142 268 154 214 212 198", amount=3.5, seed="trail-1"),
        handify("M 232 192 C 266 184 294 168 318 144", amount=3.2, seed="trail-2"),
    ])

    # Main Paper Shape 1: Inbox UI Window Card (spans x: 108..396, y: 176..406)
    main_card_fill = handify(
        rounded_box_d(108, 176, 288, 230, r=16, skew_top=3.0, skew_right=2.5),
        amount=4.5,
        seed="inbox-main-fill",
    )
    # Drawn in 2 overshooting architectural strokes so corners breathe and show pen ends
    main_card_stroke_a = handify(
        "M 102 184 L 398 174 L 400 406",
        amount=4.5,
        overshoot=11.0,
        seed="inbox-main-sa",
    )
    main_card_stroke_b = handify(
        "M 402 404 L 106 408 L 108 172",
        amount=4.5,
        overshoot=11.0,
        seed="inbox-main-sb",
    )

    # Window header divider & inner inbox tray well
    header_divider = handify("M 110 222 L 394 219", amount=3.5, seed="inbox-hdr")
    tray_well_d = handify(
        "M 142 264 L 154 356 L 216 356 L 230 332 L 278 331 L 292 355 L 354 353 L 364 260",
        amount=3.8,
        seed="inbox-tray",
    )
    # Soft clay highlight strip inside the tray lip
    tray_tint_d = handify(
        "M 156 340 L 214 340 L 228 320 L 280 319 L 294 339 L 350 337 L 353 353 L 153 355 Z",
        amount=2.5,
        seed="inbox-tray-tint",
    )

    # Window chrome dots (drawn with wobbly_circle, asymmetric sizes/spacing)
    dot1 = wobbly_circle(134, 199, 5.5, seed="win-d1", wobble=0.08)
    dot2 = wobbly_circle(154, 198, 5.2, seed="win-d2", wobble=0.08)
    dot3 = wobbly_circle(175, 199, 5.8, seed="win-d3", wobble=0.08)
    header_pill = handify("M 286 196 L 366 195", amount=2.2, seed="win-hdr-bar")

    # Main Paper Shape 2: Floating Toast Pill ("0 Pending · All Clear") in lower-right, breaking out
    toast_fill_d = handify(pill_d(244, 376, 224, 66, tilt=2.8), amount=4.2, seed="toast-fill")
    toast_badge_d = wobbly_circle(282, 409, 17.5, seed="toast-check-circle", wobble=0.06)
    toast_check_d = handify("M 274 409 L 280 416 L 292 401", amount=2.0, seed="toast-check")
    toast_line_1 = handify("M 314 399 L 428 397", amount=2.5, seed="toast-l1")
    toast_line_2 = handify("M 314 419 L 392 418", amount=2.5, seed="toast-l2")

    # Main Paper Shape 3: Origami Paper Plane breaking out of top-right of the inbox card
    # Tip at (438, 86), tail at (292, 168), lower keel at (348, 210), right wing at (392, 232)
    plane_outer_fill = handify(
        "M 288 158 L 442 84 L 388 234 L 348 202 L 328 224 L 322 182 Z",
        amount=3.8,
        seed="plane-fill",
    )
    plane_wing_patch = handify(
        "M 324 181 L 436 88 L 350 201 L 329 221 Z",
        amount=2.8,
        seed="plane-patch",
    )
    plane_strokes = " ".join([
        handify("M 288 158 L 442 84 L 388 234 L 348 202", amount=3.6, overshoot=8.0, seed="plane-s1"),
        handify("M 440 86 L 322 182 L 288 158", amount=3.4, seed="plane-s2"),
        handify("M 322 182 L 328 224 L 350 201", amount=3.0, seed="plane-s3"),
        handify("M 438 87 L 348 202", amount=3.2, seed="plane-s4"),
    ])

    # Decorative UI card lines inside the inbox tray (varied lengths & angles)
    card_lines = " ".join([
        handify("M 182 284 L 268 281", amount=2.4, seed="cl-1"),
        handify("M 196 304 L 252 302", amount=2.2, seed="cl-2"),
    ])

    # Accents in the upper-left quiet space (3 sparkles in 1 : 0.65 : 0.42 ratio + 2 dots = 5 marks)
    sp_big = sparkle(116, 102, 18.0, seed="sp-inbox-1")
    sp_med = sparkle(154, 78, 11.5, seed="sp-inbox-2")
    sp_sml = sparkle(92, 134, 7.8, seed="sp-inbox-3")
    dot_a = wobbly_circle(136, 122, 3.2, seed="dot-a")
    dot_b = wobbly_circle(172, 104, 2.8, seed="dot-b")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{defs_512(seed=31)}
<g id="layer-block" filter="url(#wash)" style="isolation:isolate">
  <g>
    <path d="{wash_cool}" fill="{sky_fill}"/>
    <path d="{wash_cool}" fill="none" stroke="{sky_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g style="mix-blend-mode:multiply">
    <path d="{wash_warm}" fill="{peach_fill}"/>
    <path d="{wash_warm}" fill="none" stroke="{peach_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g style="mix-blend-mode:multiply">
    <path d="{wash_focal}" fill="{clay_fill}" fill-opacity="0.85"/>
    <path d="{wash_focal}" fill="none" stroke="{clay_edge}" stroke-width="4.0" stroke-opacity="0.5" stroke-linejoin="round"/>
  </g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Behind paper shapes: tilted archive card & registration ticks -->
  <path d="{back_card_d}" fill="{PAPER}" stroke-width="6.5"/>
  <path d="{back_ticks}" stroke-width="5.0"/>

  <!-- Main Inbox Window Card (Paper + overshooting frame) -->
  <path d="{main_card_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{tray_tint_d}" fill="{peach_fill}" stroke="none"/>
  <path d="{main_card_stroke_a}" stroke-width="8.5"/>
  <path d="{main_card_stroke_b}" stroke-width="8.5"/>
  <path d="{header_divider}" stroke-width="6.5"/>
  <path d="{tray_well_d}" stroke-width="6.5"/>

  <!-- Window controls & interior empty-tray whisper lines -->
  <path d="{dot1}" fill="{clay_fill}" stroke-width="5.0"/>
  <path d="{dot2}" fill="{peach_fill}" stroke-width="5.0"/>
  <path d="{dot3}" fill="{cactus_fill}" stroke-width="5.0"/>
  <path d="{header_pill}" stroke-width="5.5"/>
  <path d="{card_lines}" stroke-width="5.5"/>

  <!-- Sweeping flight path launching out of the tray -->
  <path d="{trail_behind}" stroke-width="5.5" stroke-dasharray="14 16"/>

  <!-- Floating Status Toast Pill ("All Clear") breaking out lower-right -->
  <path d="{toast_fill_d}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{toast_badge_d}" fill="{cactus_fill}" stroke-width="6.0"/>
  <path d="{toast_check_d}" stroke-width="6.0"/>
  <path d="{toast_line_1}" stroke-width="6.5"/>
  <path d="{toast_line_2}" stroke-width="5.0"/>

  <!-- Foreground Origami Paper Plane breaking out upper-right -->
  <path d="{plane_outer_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{plane_wing_patch}" fill="{clay_fill}" stroke="none"/>
  <path d="{plane_strokes}" stroke-width="8.5"/>

  <!-- Quiet-space sparkle cluster in upper-left -->
  <path d="{sp_big}" stroke-width="5.0"/>
  <path d="{sp_med}" stroke-width="4.5"/>
  <path d="{sp_sml}" stroke-width="4.2"/>
  <path d="{dot_a}" fill="{INK}" stroke-width="4.0"/>
  <path d="{dot_b}" fill="{INK}" stroke-width="4.0"/>
</g>
</svg>
"""


def build_ui_component_sheet():
    """Generate `ui-component-sheet.svg` (512x512 viewBox).

    A 5-component tactile UI sticker sheet drawn in the 3-layer CC-lineart system:
      1. Search Command Bar (`⌘K`) across the upper-left/center.
      2. Tactile Toggle Switch (ON state) in the upper-right.
      3. Status Pill / Badge ("LIVE · v2.4") in the middle-left.
      4. Notification Card with an interactive Action Button in the lower-left/center.
      5. Radial Progress Gauge (`78%`) in the lower-right.
    """
    mineral_fill, mineral_edge = COLORS["mineral"]
    clay_fill, clay_edge = COLORS["clay"]
    kraft_fill, kraft_edge = COLORS["kraft"]
    cactus_fill, _ = COLORS["cactus"]
    peach_fill, _ = COLORS["peach"]
    sky_fill, _ = COLORS["sky"]

    # Layer 1: Cool mineral wash (upper-left/center) + warm kraft/clay wash (lower-right), multiply glaze
    wash_mineral = handify("M 68 88 L 326 72 L 312 318 L 56 302 Z", amount=6.0, seed="kit-wash-min")
    wash_kraft = handify("M 214 212 L 456 196 L 442 438 L 198 424 Z", amount=6.0, seed="kit-wash-krf")
    wash_clay = handify("M 312 248 L 434 238 L 424 352 L 304 344 Z", amount=4.5, seed="kit-wash-cly")

    # Behind-paper structural connectors / alignment guides
    guide_strokes = " ".join([
        handify("M 164 138 L 161 178", amount=2.5, seed="g-1"),
        handify("M 278 214 L 336 211", amount=2.5, seed="g-2"),
        handify("M 294 358 L 338 355", amount=2.5, seed="g-3"),
    ])

    # 1. Search Command Bar (x: 44..318, y: 66..136) — breaks out left of mineral wash
    search_fill = handify(pill_d(44, 66, 274, 70, tilt=2.4), amount=4.2, seed="search-fill")
    search_lens = wobbly_circle(86, 100, 14.0, seed="search-lens", wobble=0.07)
    search_handle = handify("M 97 111 L 111 124", amount=2.0, seed="search-hdl")
    search_text_line = handify("M 126 101 L 224 99", amount=2.5, seed="search-txt")
    # `⌘K` keycap box inside right end of search bar (skewed quad so it is never mirror-symmetric)
    keycap_box = handify(
        "M 254 81 L 298 77 L 302 120 L 250 123 Z",
        amount=2.8,
        seed="search-keycap",
    )
    keycap_glyph = handify("M 268 92 L 267 110 M 283 92 L 270 102 L 284 111", amount=1.8, seed="search-k")

    # 2. Tactile Toggle Switch (x: 344..468, y: 74..138) — breaks out right into paper
    toggle_track = handify(
        "M 358 76 L 452 71 L 469 98 L 463 134 L 364 140 L 342 112 Z",
        amount=3.8,
        seed="toggle-trk",
    )
    toggle_fill_patch = handify(
        "M 362 82 L 448 77 L 461 100 L 456 128 L 368 133 L 349 110 Z",
        amount=3.2,
        seed="toggle-tint",
    )
    toggle_knob = wobbly_circle(432, 106, 23.0, seed="toggle-knob", wobble=0.06)
    toggle_on_tick = handify("M 374 96 L 373 116", amount=1.8, seed="toggle-tick")

    # 3. Status Pill / Badge (x: 52..276, y: 174..234)
    badge_fill = handify(pill_d(52, 174, 224, 60, tilt=2.2), amount=3.8, seed="badge-fill")
    badge_dot = wobbly_circle(86, 204, 10.5, seed="badge-dot", wobble=0.07)
    badge_line_a = handify("M 112 198 L 204 196", amount=2.2, seed="badge-la")
    badge_line_b = handify("M 112 213 L 166 212", amount=2.0, seed="badge-lb")
    badge_tag = handify(
        "M 220 189 L 258 185 L 262 218 L 216 221 Z",
        amount=2.5,
        seed="badge-tag",
    )

    # 4. Notification Card with Action Button (x: 48..296, y: 266..454) — breaks out bottom-left
    notif_fill = handify(
        rounded_box_d(48, 266, 248, 188, r=16, skew_top=2.5, skew_right=2.0),
        amount=4.2,
        seed="notif-fill",
    )
    notif_stroke_a = handify(
        "M 44 272 L 296 264 L 298 452",
        amount=4.2,
        overshoot=10.0,
        seed="notif-sa",
    )
    notif_stroke_b = handify(
        "M 300 450 L 46 456 L 48 262",
        amount=4.2,
        overshoot=10.0,
        seed="notif-sb",
    )
    notif_avatar = wobbly_circle(92, 314, 20.0, seed="notif-av", wobble=0.06)
    notif_title = handify("M 128 302 L 262 299", amount=2.5, seed="notif-t1")
    notif_sub = handify("M 128 324 L 236 322", amount=2.4, seed="notif-t2")
    notif_body = handify("M 74 358 L 264 355", amount=2.5, seed="notif-t3")
    # Interactive CTA button inside notification card (asymmetric hand-drawn capsule)
    cta_box = handify(
        "M 86 385 L 196 380 L 212 402 L 204 428 L 90 432 L 73 410 Z",
        amount=3.2,
        seed="notif-cta",
    )
    cta_label = handify("M 102 407 L 164 405 M 176 400 L 186 406 L 175 413", amount=2.0, seed="notif-cta-lbl")
    # Asymmetric hand-drawn dismiss mark (unequal arms and tilted axis)
    dismiss_x = handify("M 236 401 L 262 415 M 255 393 L 241 421", amount=2.2, seed="notif-x")

    # 5. Radial Progress Gauge Card (x: 326..472, y: 274..448) — breaks out right
    gauge_card = handify(
        rounded_box_d(326, 274, 146, 174, r=16, skew_top=-2.0, skew_right=2.0),
        amount=4.0,
        seed="gauge-card",
    )
    gauge_ring_outer = wobbly_circle(399, 348, 44.0, seed="gauge-outer", wobble=0.05)
    # 78% active arc in bold clay + ink
    gauge_arc_pts = []
    cx, cy, r_arc = 399.0, 348.0, 44.0
    for step in range(18):
        ang = math.radians(-90 + step * (280.0 / 17.0))
        gauge_arc_pts.append((cx + r_arc * math.cos(ang), cy + r_arc * math.sin(ang)))
    gauge_arc_d = handify(poly_d(gauge_arc_pts, closed=False), amount=2.2, seed="gauge-arc")
    gauge_tick = handify("M 386 350 L 396 360 L 416 336", amount=2.0, seed="gauge-check")
    gauge_caption = handify("M 358 418 L 438 416", amount=2.2, seed="gauge-cap")

    # Accents in the upper-right / mid-right quiet zone (3 sparkles + 1 dot = 4 marks)
    sp1 = sparkle(372, 178, 15.0, seed="kit-sp1")
    sp2 = sparkle(414, 164, 10.0, seed="kit-sp2")
    sp3 = sparkle(446, 186, 6.8, seed="kit-sp3")
    dot1 = wobbly_circle(394, 194, 3.0, seed="kit-d1")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{defs_512(seed=47)}
<g id="layer-block" filter="url(#wash)" style="isolation:isolate">
  <g>
    <path d="{wash_mineral}" fill="{mineral_fill}"/>
    <path d="{wash_mineral}" fill="none" stroke="{mineral_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g style="mix-blend-mode:multiply">
    <path d="{wash_kraft}" fill="{kraft_fill}"/>
    <path d="{wash_kraft}" fill="none" stroke="{kraft_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g style="mix-blend-mode:multiply">
    <path d="{wash_clay}" fill="{clay_fill}" fill-opacity="0.82"/>
    <path d="{wash_clay}" fill="none" stroke="{clay_edge}" stroke-width="4.0" stroke-opacity="0.5" stroke-linejoin="round"/>
  </g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Behind-component schematic connection guides -->
  <path d="{guide_strokes}" stroke-width="5.0" stroke-dasharray="10 12"/>

  <!-- 1. Search Command Bar (⌘K) -->
  <path d="{search_fill}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{keycap_box}" fill="{peach_fill}" stroke-width="5.5"/>
  <path d="{search_lens}" stroke-width="6.0"/>
  <path d="{search_handle}" stroke-width="6.0"/>
  <path d="{search_text_line}" stroke-width="6.5"/>
  <path d="{keycap_glyph}" stroke-width="4.8"/>

  <!-- 2. Tactile Toggle Switch (ON) -->
  <path d="{toggle_track}" fill="{PAPER}" stroke="none"/>
  <path d="{toggle_fill_patch}" fill="{cactus_fill}" stroke="none"/>
  <path d="{toggle_track}" stroke-width="8.5"/>
  <path d="{toggle_knob}" fill="{PAPER}" stroke-width="7.0"/>
  <path d="{toggle_on_tick}" stroke-width="5.5"/>

  <!-- 3. Status Pill / Badge -->
  <path d="{badge_fill}" fill="{PAPER}" stroke-width="8.0"/>
  <path d="{badge_dot}" fill="{clay_fill}" stroke-width="5.5"/>
  <path d="{badge_line_a}" stroke-width="6.0"/>
  <path d="{badge_line_b}" stroke-width="4.8"/>
  <path d="{badge_tag}" fill="{sky_fill}" stroke-width="5.0"/>

  <!-- 4. Notification Card with Action Button -->
  <path d="{notif_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{notif_stroke_a}" stroke-width="8.5"/>
  <path d="{notif_stroke_b}" stroke-width="8.5"/>
  <path d="{notif_avatar}" fill="{peach_fill}" stroke-width="6.0"/>
  <path d="{notif_title}" stroke-width="6.5"/>
  <path d="{notif_sub}" stroke-width="5.0"/>
  <path d="{notif_body}" stroke-width="5.0"/>
  <path d="{cta_box}" fill="{clay_fill}" stroke-width="6.5"/>
  <path d="{cta_label}" stroke-width="5.0"/>
  <path d="{dismiss_x}" stroke-width="5.0"/>

  <!-- 5. Radial Progress Gauge -->
  <path d="{gauge_card}" fill="{PAPER}" stroke-width="8.5"/>
  <path d="{gauge_ring_outer}" stroke-width="5.5" stroke-dasharray="10 12"/>
  <path d="{gauge_arc_d}" stroke="{clay_fill}" stroke-width="14.0"/>
  <path d="{gauge_arc_d}" stroke="{INK}" stroke-width="7.5"/>
  <path d="{gauge_tick}" stroke-width="6.0"/>
  <path d="{gauge_caption}" stroke-width="5.5"/>

  <!-- Clustered accents in quiet zone -->
  <path d="{sp1}" stroke-width="5.0"/>
  <path d="{sp2}" stroke-width="4.5"/>
  <path d="{sp3}" stroke-width="4.0"/>
  <path d="{dot1}" fill="{INK}" stroke-width="4.0"/>
</g>
</svg>
"""


def build_interactive_demo_html(empty_svg, kit_svg):
    """Build `interactive-demo.html` showcasing live CC-lineart UI components and interactive states."""
    # Pre-generate reusable hand-drawn SVG paths for the HTML UI components
    btn_primary_wash = handify("M 14 10 L 186 6 L 182 54 L 10 50 Z", amount=2.2, seed="btn-p-wash")
    btn_primary_box = handify(pill_d(8, 6, 172, 44, tilt=0.8), amount=1.8, seed="btn-p-box")

    btn_secondary_wash = handify("M 18 12 L 168 8 L 164 52 L 14 48 Z", amount=2.2, seed="btn-s-wash")
    btn_secondary_box = handify(pill_d(8, 6, 154, 44, tilt=-0.6), amount=1.8, seed="btn-s-box")

    banner_wash_a = handify("M 24 14 L 420 8 L 408 112 L 16 104 Z", amount=4.0, seed="bnr-wash-a")
    banner_wash_b = handify("M 310 18 L 760 12 L 748 116 L 296 108 Z", amount=4.0, seed="bnr-wash-b")
    banner_box = handify(rounded_box_d(8, 8, 764, 102, r=14, skew_top=1.5, skew_right=1.5), amount=3.0, seed="bnr-box")

    card_1_wash = handify("M 26 22 L 310 14 L 298 198 L 18 188 Z", amount=4.0, seed="c1-wash")
    card_1_box = handify(rounded_box_d(12, 12, 316, 196, r=14, skew_top=1.8, skew_right=1.6), amount=2.8, seed="c1-box")

    card_2_wash = handify("M 34 18 L 318 26 L 306 202 L 22 192 Z", amount=4.0, seed="c2-wash")
    card_2_box = handify(rounded_box_d(12, 12, 316, 196, r=14, skew_top=-1.6, skew_right=1.8), amount=2.8, seed="c2-box")

    card_3_wash = handify("M 20 24 L 312 16 L 302 198 L 28 190 Z", amount=4.0, seed="c3-wash")
    card_3_box = handify(rounded_box_d(12, 12, 316, 196, r=14, skew_top=1.4, skew_right=-1.5), amount=2.8, seed="c3-box")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>CC-Lineart UI Kit — Tactile Ink &amp; Watercolor Interface System</title>
<style>
  :root {{
    --paper: #FAF9F5;
    --paper-elevated: #F3F1EA;
    --paper-deep: #EAE6DC;
    --ink: #141413;
    --ink-muted: #575550;
    --ink-faint: #8A877F;
    --clay: #D97757;
    --clay-rim: #B85C3E;
    --sky: #6A9BCC;
    --sky-rim: #4C7FB3;
    --cactus: #BCD1CA;
    --cactus-rim: #93B0A6;
    --heather: #CBCADB;
    --heather-rim: #A4A2BF;
    --plum: #827DBD;
    --plum-rim: #635DA3;
    --mineral: #629987;
    --mineral-rim: #4A7D6C;
    --peach: #EBC9B7;
    --peach-rim: #D3A58D;
    --kraft: #D4A27F;
    --kraft-rim: #B9845F;
    --olive: #788C5D;
    --olive-rim: #5D7046;
    --serif: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, sans-serif;
    --mono: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    margin: 0;
    background-color: var(--paper);
    color: var(--ink);
    font-family: var(--sans);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
    background-image:
      radial-gradient(circle at 18% 12%, rgba(235, 201, 183, 0.18), transparent 38%),
      radial-gradient(circle at 84% 28%, rgba(106, 155, 204, 0.12), transparent 42%);
  }}

  /* Shared hidden SVG filter bank */
  .svg-defs-bank {{
    position: absolute;
    width: 0;
    height: 0;
    overflow: hidden;
    pointer-events: none;
  }}

  .page-shell {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 40px 28px 88px;
  }}

  /* Top Editorial Masthead */
  .masthead {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-end;
    gap: 24px;
    padding-bottom: 28px;
    border-bottom: 2px solid var(--ink);
    margin-bottom: 36px;
  }}

  .eyebrow {{
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--clay-rim);
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }}

  .eyebrow-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--clay);
    border: 1.8px solid var(--ink);
  }}

  h1 {{
    font-family: var(--serif);
    font-weight: 600;
    font-size: clamp(2rem, 3.6vw, 3.1rem);
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0 0 10px;
  }}

  .subtitle {{
    max-width: 640px;
    color: var(--ink-muted);
    font-size: 1.04rem;
    margin: 0;
  }}

  /* Interactive Tactile SVG Buttons */
  .btn-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    align-items: center;
  }}

  .sketch-btn {{
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    padding: 13px 26px;
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 600;
    color: var(--ink);
    background: transparent;
    border: none;
    cursor: pointer;
    user-select: none;
    isolation: isolate;
    transition: transform 0.2s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .sketch-btn svg.btn-bg {{
    position: absolute;
    inset: -6px -8px;
    width: calc(100% + 16px);
    height: calc(100% + 12px);
    z-index: -1;
    overflow: visible;
  }}

  .sketch-btn .wash-layer {{
    transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.24s ease;
    transform: translate(5px, 5px);
  }}

  .sketch-btn .paper-layer {{
    transition: transform 0.2s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .sketch-btn:hover {{
    transform: translate(-1px, -2px);
  }}

  .sketch-btn:hover .wash-layer {{
    transform: translate(10px, 9px) scale(1.03) rotate(-1deg);
  }}

  .sketch-btn:active {{
    transform: translate(2px, 2px);
  }}

  .sketch-btn:active .wash-layer {{
    transform: translate(2px, 2px) scale(0.98);
  }}

  /* Section Headers */
  .section-head {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 16px;
    margin: 44px 0 20px;
  }}

  .section-head h2 {{
    font-family: var(--serif);
    font-size: 1.65rem;
    font-weight: 600;
    margin: 0;
  }}

  .section-head .meta {{
    font-family: var(--mono);
    font-size: 12px;
    color: var(--ink-muted);
  }}

  /* Callout Banner */
  .callout-banner {{
    position: relative;
    padding: 24px 30px;
    margin-bottom: 36px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    isolation: isolate;
  }}

  .callout-banner svg.banner-bg {{
    position: absolute;
    inset: -8px;
    width: calc(100% + 16px);
    height: calc(100% + 16px);
    z-index: -1;
    overflow: visible;
  }}

  .callout-banner .wash-shift {{
    transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
    transform: translate(6px, 6px);
  }}

  .callout-banner:hover .wash-shift {{
    transform: translate(12px, 10px) rotate(-0.4deg);
  }}

  .callout-content {{
    display: flex;
    align-items: flex-start;
    gap: 16px;
    max-width: 680px;
  }}

  .callout-badge {{
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 4px 10px;
    background: var(--clay);
    color: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 999px;
    white-space: nowrap;
    margin-top: 2px;
  }}

  .callout-title {{
    font-family: var(--serif);
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0 0 4px;
  }}

  .callout-desc {{
    margin: 0;
    font-size: 0.94rem;
    color: var(--ink-muted);
  }}

  /* Interactive Controls Bar (Search + Toggle + Filter Pills) */
  .workbench-bar {{
    display: grid;
    grid-template-columns: 1.3fr auto auto;
    gap: 18px;
    align-items: center;
    margin-bottom: 32px;
  }}

  @media (max-width: 860px) {{
    .workbench-bar {{
      grid-template-columns: 1fr;
    }}
  }}

  .search-box {{
    position: relative;
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--paper);
    border: 2.4px solid var(--ink);
    border-radius: 999px;
    padding: 10px 18px;
    box-shadow: 6px 6px 0 var(--cactus);
    transition: box-shadow 0.22s ease, transform 0.22s ease;
  }}

  .search-box:focus-within {{
    transform: translate(-2px, -2px);
    box-shadow: 10px 9px 0 var(--sky);
  }}

  .search-box input {{
    border: none;
    background: transparent;
    font-family: var(--sans);
    font-size: 0.96rem;
    color: var(--ink);
    width: 100%;
    outline: none;
  }}

  .kbd-tag {{
    font-family: var(--mono);
    font-size: 11px;
    padding: 3px 8px;
    background: var(--peach);
    border: 1.8px solid var(--ink);
    border-radius: 6px;
    white-space: nowrap;
  }}

  /* Tactile Toggle Switch in DOM */
  .tactile-toggle {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    font-family: var(--mono);
    font-size: 12.5px;
    user-select: none;
    padding: 6px 12px;
  }}

  .toggle-track-ui {{
    width: 58px;
    height: 32px;
    border-radius: 999px;
    border: 2.4px solid var(--ink);
    background: var(--cactus);
    position: relative;
    transition: background 0.22s ease, box-shadow 0.22s ease;
    box-shadow: 4px 4px 0 var(--mineral);
  }}

  .toggle-knob-ui {{
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--paper);
    border: 2.4px solid var(--ink);
    position: absolute;
    top: 2.5px;
    left: 28px;
    transition: left 0.22s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .tactile-toggle[aria-checked="false"] .toggle-track-ui {{
    background: var(--paper-elevated);
    box-shadow: 3px 3px 0 var(--heather);
  }}

  .tactile-toggle[aria-checked="false"] .toggle-knob-ui {{
    left: 3.5px;
  }}

  /* Onboarding / Feature Cards Grid */
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 26px;
    margin-bottom: 44px;
  }}

  @media (max-width: 920px) {{
    .cards-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .sketch-card {{
    position: relative;
    padding: 26px 24px 24px;
    isolation: isolate;
    cursor: pointer;
    transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .sketch-card svg.card-bg {{
    position: absolute;
    inset: -10px;
    width: calc(100% + 20px);
    height: calc(100% + 20px);
    z-index: -1;
    overflow: visible;
  }}

  .sketch-card .card-wash {{
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);
    transform: translate(7px, 7px);
  }}

  .sketch-card:hover {{
    transform: translate(-2px, -3px);
  }}

  .sketch-card:hover .card-wash {{
    transform: translate(14px, 12px) scale(1.02) rotate(-0.8deg);
  }}

  .card-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1.8px solid var(--ink);
    background: var(--paper);
    margin-bottom: 14px;
  }}

  .sketch-card h3 {{
    font-family: var(--serif);
    font-size: 1.28rem;
    margin: 0 0 8px;
  }}

  .sketch-card p {{
    margin: 0 0 16px;
    font-size: 0.93rem;
    color: var(--ink-muted);
  }}

  .card-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--mono);
    font-size: 12px;
    padding-top: 10px;
    border-top: 1.5px dashed rgba(20, 20, 19, 0.25);
  }}

  /* Dual Showcase Grid: Interactive Empty State + Sticker Sheet */
  .showcase-grid {{
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 32px;
    align-items: stretch;
  }}

  @media (max-width: 960px) {{
    .showcase-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .showcase-panel {{
    background: var(--paper-elevated);
    border: 2.5px solid var(--ink);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 8px 8px 0 rgba(20, 20, 19, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .panel-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding-bottom: 14px;
    margin-bottom: 16px;
    border-bottom: 1.8px solid rgba(20, 20, 19, 0.14);
  }}

  .panel-title {{
    font-family: var(--serif);
    font-weight: 600;
    font-size: 1.2rem;
    margin: 0;
  }}

  .status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: var(--mono);
    font-size: 11.5px;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1.8px solid var(--ink);
    background: var(--paper);
  }}

  .status-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--olive);
    border: 1.5px solid var(--ink);
  }}

  .svg-stage {{
    background: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 14px;
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}

  .svg-stage svg {{
    width: 100%;
    max-width: 440px;
    height: auto;
    display: block;
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  }}

  .svg-stage:hover svg {{
    transform: scale(1.015);
  }}

  /* Task Simulator List inside Empty State Panel */
  .task-drawer {{
    margin-top: 16px;
    display: none;
    flex-direction: column;
    gap: 10px;
  }}

  .task-drawer.active {{
    display: flex;
  }}

  .task-item {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: var(--paper);
    border: 2px solid var(--ink);
    border-radius: 10px;
    font-size: 0.92rem;
    box-shadow: 4px 4px 0 var(--peach);
  }}

  .task-item button {{
    font-family: var(--mono);
    font-size: 11.5px;
    background: var(--cactus);
    border: 1.8px solid var(--ink);
    border-radius: 6px;
    padding: 4px 10px;
    cursor: pointer;
  }}

  .panel-caption {{
    margin-top: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    font-size: 0.9rem;
    color: var(--ink-muted);
  }}

  /* Live Wash Mode when toggled off */
  body.wash-muted .wash-layer,
  body.wash-muted .card-wash,
  body.wash-muted .wash-shift {{
    opacity: 0.18;
    transform: translate(0, 0) !important;
  }}
</style>
</head>
<body>

<!-- Shared SVG Filter Defs Bank for DOM UI Components -->
<svg class="svg-defs-bank" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="ui-wash" x="-12%" y="-12%" width="124%" height="124%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="19" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 1.42" result="a"/>
      <feComposite in="d" in2="a" operator="in"/>
    </filter>
    <filter id="ui-ink" x="-8%" y="-8%" width="116%" height="116%">
      <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="37" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
</svg>

<div class="page-shell">
  <header class="masthead">
    <div>
      <div class="eyebrow"><span class="eyebrow-dot"></span>CC-Lineart · Track 3 UI Component System</div>
      <h1>Tactile Ink &amp; Watercolor UI</h1>
      <p class="subtitle">
        Hand-drawn `#141413` ink strokes with corner overshoots, `#FAF9F5` paper surfaces, and offset watercolor washes that shift like wet pigment on hover.
      </p>
    </div>
    <div class="btn-row">
      <button class="sketch-btn" id="btn-simulate" type="button">
        <svg class="btn-bg" viewBox="0 0 196 60" preserveAspectRatio="none">
          <g class="wash-layer" filter="url(#ui-wash)">
            <path d="{btn_primary_wash}" fill="{COLORS['clay'][0]}"/>
            <path d="{btn_primary_wash}" fill="none" stroke="{COLORS['clay'][1]}" stroke-width="2" stroke-opacity="0.55"/>
          </g>
          <g class="paper-layer" filter="url(#ui-ink)">
            <path d="{btn_primary_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>
        <span id="btn-simulate-label">Simulate 2 Incoming Tasks</span>
      </button>

      <button class="sketch-btn" id="btn-cycle-palette" type="button">
        <svg class="btn-bg" viewBox="0 0 176 60" preserveAspectRatio="none">
          <g class="wash-layer" filter="url(#ui-wash)">
            <path id="cycle-wash-path" d="{btn_secondary_wash}" fill="{COLORS['sky'][0]}"/>
          </g>
          <g class="paper-layer" filter="url(#ui-ink)">
            <path d="{btn_secondary_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
          </g>
        </svg>
        <span>Cycle Wash Glaze</span>
      </button>
    </div>
  </header>

  <!-- Editorial Callout Banner -->
  <section class="callout-banner" aria-label="Architecture note">
    <svg class="banner-bg" viewBox="0 0 780 120" preserveAspectRatio="none">
      <g class="wash-shift" filter="url(#ui-wash)" style="isolation:isolate">
        <path d="{banner_wash_a}" fill="{COLORS['peach'][0]}"/>
        <path d="{banner_wash_b}" fill="{COLORS['heather'][0]}" style="mix-blend-mode:multiply"/>
      </g>
      <g filter="url(#ui-ink)">
        <path d="{banner_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
      </g>
    </svg>
    <div class="callout-content">
      <span class="callout-badge">3-Layer Rule</span>
      <div>
        <h2 class="callout-title">Every UI control is an offset watercolor block, a paper cutout, and a bowed pen stroke</h2>
        <p class="callout-desc">
          Hover any button, card, or banner below to feel the watercolor wash drift independently behind the `#FAF9F5` paper surface while `vector-effect: non-scaling-stroke` preserves crisp ink weight.
        </p>
      </div>
    </div>
    <div class="status-pill">
      <span class="status-dot"></span>
      <span>Lint: 0 Warnings</span>
    </div>
  </section>

  <!-- Interactive Workbench Controls -->
  <div class="workbench-bar">
    <label class="search-box" aria-label="Filter UI motifs">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#141413" stroke-width="2.4" stroke-linecap="round">
        <circle cx="10.5" cy="10.5" r="6.5"/>
        <path d="M15.5 15.5 L20.5 20.5"/>
      </svg>
      <input type="text" id="card-filter-input" placeholder="Filter onboarding cards (e.g. wash, stroke, empty state)..." />
      <span class="kbd-tag">⌘K</span>
    </label>

    <div class="tactile-toggle" id="wash-toggle" role="switch" aria-checked="true" tabindex="0">
      <div class="toggle-track-ui">
        <div class="toggle-knob-ui"></div>
      </div>
      <span>Offset Wash Active</span>
    </div>

    <div class="status-pill" id="active-count-pill">
      <span class="status-dot" style="background: var(--clay)"></span>
      <span id="card-count-text">3 / 3 Cards Visible</span>
    </div>
  </div>

  <!-- 3 Interactive Onboarding / System Cards -->
  <section class="cards-grid" id="onboarding-cards">
    <article class="sketch-card" data-keywords="watercolor wash glaze multiply offset">
      <svg class="card-bg" viewBox="0 0 340 220" preserveAspectRatio="none">
        <g class="card-wash" filter="url(#ui-wash)">
          <path d="{card_1_wash}" fill="{COLORS['sky'][0]}"/>
          <path d="{card_1_wash}" fill="none" stroke="{COLORS['sky'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
        </g>
        <g filter="url(#ui-ink)">
          <path d="{card_1_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
        </g>
      </svg>
      <span class="card-pill" style="background: var(--sky); color: var(--paper)">01 · Layer Block</span>
      <h3>Offset Glazed Washes</h3>
      <p>Washes never sit centered like a digital drop-shadow. They shift 10–25% off-axis and glaze warm over cool with <code>mix-blend-mode: multiply</code>.</p>
      <div class="card-footer">
        <span>Coverage: 18–22%</span>
        <span>Sky + Clay</span>
      </div>
    </article>

    <article class="sketch-card" data-keywords="paper cutout fill surface empty state">
      <svg class="card-bg" viewBox="0 0 340 220" preserveAspectRatio="none">
        <g class="card-wash" filter="url(#ui-wash)">
          <path d="{card_2_wash}" fill="{COLORS['peach'][0]}"/>
          <path d="{card_2_wash}" fill="none" stroke="{COLORS['peach'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
        </g>
        <g filter="url(#ui-ink)">
          <path d="{card_2_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
        </g>
      </svg>
      <span class="card-pill" style="background: var(--peach)">02 · Paper Cutout</span>
      <h3>Warm Paper Occlusion</h3>
      <p>Closed UI containers are filled with warm <code>#FAF9F5</code> paper so they mask part of the watercolor block while letting 30%+ of the wash breathe around the edges.</p>
      <div class="card-footer">
        <span>Surface: #FAF9F5</span>
        <span>Breakout ≥ 20%</span>
      </div>
    </article>

    <article class="sketch-card" data-keywords="ink stroke handify overshoot wobble">
      <svg class="card-bg" viewBox="0 0 340 220" preserveAspectRatio="none">
        <g class="card-wash" filter="url(#ui-wash)">
          <path d="{card_3_wash}" fill="{COLORS['cactus'][0]}"/>
          <path d="{card_3_wash}" fill="none" stroke="{COLORS['cactus'][1]}" stroke-width="2.2" stroke-opacity="0.55"/>
        </g>
        <g filter="url(#ui-ink)">
          <path d="{card_3_box}" fill="{PAPER}" stroke="{INK}" stroke-width="2.6" vector-effect="non-scaling-stroke"/>
        </g>
      </svg>
      <span class="card-pill" style="background: var(--cactus)">03 · Layer Ink</span>
      <h3>Bowed Ink &amp; Overshoots</h3>
      <p>Every straight run bows by 0.5–1.5% via <code>handify</code>, corners overshoot like an architect's pen sketch, and 3 stroke weights separate frame from detail.</p>
      <div class="card-footer">
        <span>Stroke: #141413</span>
        <span>Weights: 8.5 / 6 / 4.5</span>
      </div>
    </article>
  </section>

  <div class="section-head">
    <h2>512×512 Production SVG Deliverables</h2>
    <span class="meta">Both SVGs pass <code>python3 -I scripts/lineart.py lint</code> with 0 warnings</span>
  </div>

  <!-- Dual Live Showcase -->
  <section class="showcase-grid">
    <!-- Left: Interactive Empty State Panel -->
    <div class="showcase-panel">
      <div>
        <div class="panel-bar">
          <h3 class="panel-title">Empty State — Zero Inbox / All Clear</h3>
          <span class="status-pill" id="inbox-status-pill">
            <span class="status-dot" id="inbox-status-dot"></span>
            <span id="inbox-status-text">0 Pending · All Clear</span>
          </span>
        </div>

        <div class="svg-stage" id="empty-state-stage">
          {empty_svg}
        </div>

        <div class="task-drawer" id="task-drawer">
          <div class="task-item" data-task-id="1">
            <span><strong>Agent #14</strong> · Audit SVG stroke weights on 512 grid</span>
            <button type="button" class="resolve-btn">Complete ✓</button>
          </div>
          <div class="task-item" data-task-id="2">
            <span><strong>Agent #19</strong> · Verify watercolor wash coverage (10–50%)</span>
            <button type="button" class="resolve-btn">Complete ✓</button>
          </div>
        </div>
      </div>

      <div class="panel-caption">
        <span><code>empty-state-inbox.svg</code> · Sky + Peach + Clay glaze</span>
        <span>Layered archive card · Inbox window · Origami plane</span>
      </div>
    </div>

    <!-- Right: UI Component Sticker Sheet -->
    <div class="showcase-panel">
      <div>
        <div class="panel-bar">
          <h3 class="panel-title">UI Component Sticker Sheet</h3>
          <span class="status-pill">
            <span class="status-dot" style="background: var(--mineral)"></span>
            <span>5 Tactile Primitives</span>
          </span>
        </div>

        <div class="svg-stage">
          {kit_svg}
        </div>
      </div>

      <div class="panel-caption">
        <span><code>ui-component-sheet.svg</code> · Mineral + Kraft + Clay glaze</span>
        <span>⌘K Search · Toggle · Status Pill · Toast Card · 78% Gauge</span>
      </div>
    </div>
  </section>
</div>

<script>
  // 1. Toggle watercolor wash offset state
  const washToggle = document.getElementById('wash-toggle');
  washToggle.addEventListener('click', () => {{
    const isChecked = washToggle.getAttribute('aria-checked') === 'true';
    const next = !isChecked;
    washToggle.setAttribute('aria-checked', String(next));
    document.body.classList.toggle('wash-muted', !next);
  }});

  // 2. Filter onboarding cards via search bar (⌘K)
  const filterInput = document.getElementById('card-filter-input');
  const cards = Array.from(document.querySelectorAll('#onboarding-cards .sketch-card'));
  const cardCountText = document.getElementById('card-count-text');

  window.addEventListener('keydown', (e) => {{
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {{
      e.preventDefault();
      filterInput.focus();
    }}
  }});

  filterInput.addEventListener('input', () => {{
    const q = filterInput.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach((card) => {{
      const hay = (card.textContent + ' ' + (card.dataset.keywords || '')).toLowerCase();
      const match = !q || hay.includes(q);
      card.style.display = match ? '' : 'none';
      if (match) visible += 1;
    }});
    cardCountText.textContent = `${{visible}} / ${{cards.length}} Cards Visible`;
  }});

  // 3. Simulate incoming tasks vs Zero Inbox empty state
  const btnSimulate = document.getElementById('btn-simulate');
  const btnSimulateLabel = document.getElementById('btn-simulate-label');
  const taskDrawer = document.getElementById('task-drawer');
  const emptyStage = document.getElementById('empty-state-stage');
  const inboxStatusText = document.getElementById('inbox-status-text');
  const inboxStatusDot = document.getElementById('inbox-status-dot');

  function updateTaskState() {{
    const remaining = taskDrawer.querySelectorAll('.task-item:not([ hidden ])').length;
    if (remaining === 0) {{
      taskDrawer.classList.remove('active');
      emptyStage.style.display = 'flex';
      inboxStatusText.textContent = '0 Pending · All Clear';
      inboxStatusDot.style.background = 'var(--olive)';
      btnSimulateLabel.textContent = 'Simulate 2 Incoming Tasks';
    }} else {{
      taskDrawer.classList.add('active');
      emptyStage.style.display = 'none';
      inboxStatusText.textContent = `${{remaining}} Active Task${{remaining > 1 ? 's' : ''}}`;
      inboxStatusDot.style.background = 'var(--clay)';
      btnSimulateLabel.textContent = 'Reset to Zero Inbox';
    }}
  }}

  btnSimulate.addEventListener('click', () => {{
    const isShowingTasks = taskDrawer.classList.contains('active');
    const items = taskDrawer.querySelectorAll('.task-item');
    items.forEach((el) => {{
      if (isShowingTasks) {{
        el.setAttribute('hidden', '');
      }} else {{
        el.removeAttribute('hidden');
      }}
    }});
    updateTaskState();
  }});

  taskDrawer.addEventListener('click', (e) => {{
    const btn = e.target.closest('.resolve-btn');
    if (!btn) return;
    const item = btn.closest('.task-item');
    if (item) {{
      item.setAttribute('hidden', '');
      updateTaskState();
    }}
  }});

  // 4. Cycle wash glaze palette
  const paletteCycle = ['#6A9BCC', '#D97757', '#827DBD', '#629987', '#788C5D'];
  let paletteIdx = 0;
  const cycleBtn = document.getElementById('btn-cycle-palette');
  const cycleWashPath = document.getElementById('cycle-wash-path');
  cycleBtn.addEventListener('click', () => {{
    paletteIdx = (paletteIdx + 1) % paletteCycle.length;
    cycleWashPath.setAttribute('fill', paletteCycle[paletteIdx]);
  }});
</script>
</body>
</html>
"""


def render_png(svg_path, png_path, size=512):
    """Render a 512x512 PNG preview with paper background if rsvg-convert is available."""
    if not shutil.which("rsvg-convert"):
        return
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), "-b", PAPER, svg_path, "-o", png_path],
        check=True,
    )
    print(f"Wrote {png_path}")


def main():
    empty_svg = build_empty_state_inbox()
    kit_svg = build_ui_component_sheet()

    empty_path = os.path.join(SCRIPT_DIR, "empty-state-inbox.svg")
    empty_png = os.path.join(SCRIPT_DIR, "empty-state-inbox.png")
    kit_path = os.path.join(SCRIPT_DIR, "ui-component-sheet.svg")
    kit_png = os.path.join(SCRIPT_DIR, "ui-component-sheet.png")
    html_path = os.path.join(SCRIPT_DIR, "interactive-demo.html")

    with open(empty_path, "w", encoding="utf-8") as f:
        f.write(empty_svg)
    with open(kit_path, "w", encoding="utf-8") as f:
        f.write(kit_svg)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_interactive_demo_html(empty_svg, kit_svg))

    print(f"Wrote {empty_path}")
    print(f"Wrote {kit_path}")
    print(f"Wrote {html_path}")

    render_png(empty_path, empty_png)
    render_png(kit_path, kit_png)


if __name__ == "__main__":
    main()
