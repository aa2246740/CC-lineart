#!/usr/bin/env python3
"""Generate Track 7 deliverables: AI-Designed Boutique E-Commerce & Marketplace Storefront.

Produces inside /Users/wu/CC-lineart/examples/pages-storefront/:
  1. storefront-showcase.svg   (512x512 Boutique Curated Shelf & Tote Showcase)
  2. storefront-showcase.png   (512x512 rasterized preview via rsvg-convert)
  3. marketplace-storefront.html (Interactive E-Commerce & Digital Goods Storefront Page)
"""
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lineart import COLORS, INK, PAPER, handify, sparkle, wobbly_circle  # noqa: E402


def hpath(d, amount=5.0, overshoot=0.0, seed="store"):
    return handify(d, amount=amount, overshoot=overshoot, seed=seed)


def build_defs(seed_wash=37, seed_ink=61):
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


def build_storefront_showcase_svg():
    """Generate 512x512 `storefront-showcase.svg`: 'Claudette Goods — Curated Boutique Shelf & Tote'.

    Composition:
      - Layer 1 (`#layer-block`): Warm `kraft` + `clay` glazed wash behind upper-left/center shelf
        and `cactus` wash behind lower-right tote & price tag (~27% canvas coverage).
      - Layer 2 & 3 (`#layer-ink`):
        1. Tilted wooden boutique display shelf (upper-left to center) holding:
           - Artisan Ceramic V60 Pour-Over Dripper + Carafe (skewed trapezoid + tilted handle).
           - Spiral-Bound Field Monograph Notebook (tilted quadrilateral + dog-ear + cover lines).
        2. Tactile Canvas Tote Bag & Keycap Artisan Box (lower-right, breaking outside the wash)
           with a hanging hand-drawn Price Tag (`$28` glyph strokes) and Wax-Seal Quality Stamp.
    """
    kraft_fill, kraft_edge = COLORS["kraft"]
    clay_fill, clay_edge = COLORS["clay"]
    cactus_fill, cactus_edge = COLORS["cactus"]
    sky_fill, _ = COLORS["sky"]

    # Layer 1: Glazed watercolor blocks
    wash_kraft = hpath("M 66 112 L 328 86 L 344 316 L 82 338 Z", amount=7.2, seed="st-w-kraft")
    wash_cactus = hpath("M 188 214 L 432 192 L 446 426 L 202 448 Z", amount=7.2, seed="st-w-cactus")
    wash_clay = wobbly_circle(384, 138, 42, seed="st-w-clay", wobble=0.07, overlap=14)

    # Background architectural awning / shelf bracket lines
    bg_awning_arc = hpath("M 36 86 C 124 44 248 48 346 82", amount=4.0, seed="st-bg-awn")
    bg_bracket_l = hpath("M 74 268 L 78 332 L 122 266", amount=3.2, seed="st-bg-brl")
    bg_bracket_r = hpath("M 312 246 L 316 308 L 274 250", amount=3.2, seed="st-bg-brr")
    bg_dotted_flow = hpath("M 152 342 C 176 392 216 422 258 418", amount=3.8, seed="st-bg-flow")

    # 1. Boutique Display Shelfplank (tilted quadrilateral)
    shelf_fill = hpath("M 26 248 L 356 218 L 362 246 L 32 276 Z", amount=4.5, seed="st-sh-fill")
    shelf_out = hpath("M 26 248 L 356 218 L 362 246 L 32 276 L 26 248", amount=4.5, overshoot=11.0, seed="st-sh-out")

    # Item A on Shelf (Left, breaking out left of wash): Artisan Ceramic Pour-Over Dripper
    drip_fill = hpath("M 38 136 L 146 124 L 126 238 L 62 244 Z", amount=4.8, seed="st-dr-fill")
    drip_out_a = hpath("M 38 136 L 146 124 L 126 238", amount=4.6, overshoot=10.0, seed="st-dr-oa")
    drip_out_b = hpath("M 126 238 L 62 244 L 38 136", amount=4.6, overshoot=10.0, seed="st-dr-ob")
    drip_handle = hpath("M 138 148 C 172 146 170 202 130 208", amount=3.2, seed="st-dr-hdl")
    drip_rib_1 = hpath("M 64 156 L 76 222", amount=2.4, seed="st-dr-r1")
    drip_rib_2 = hpath("M 92 152 L 96 220", amount=2.4, seed="st-dr-r2")
    drip_rib_3 = hpath("M 118 148 L 112 216", amount=2.4, seed="st-dr-r3")
    steam_1 = hpath("M 74 112 C 66 92 86 76 76 56", amount=2.6, seed="st-stm-1")
    steam_2 = hpath("M 106 106 C 98 86 118 70 108 50", amount=2.6, seed="st-stm-2")

    # Item B on Shelf (Center-Right): Tilted Field Monograph Notebook
    book_fill = hpath("M 178 92 L 314 76 L 328 222 L 192 236 Z", amount=5.0, seed="st-bk-fill")
    book_out_a = hpath("M 178 92 L 314 76 L 328 222", amount=4.8, overshoot=11.0, seed="st-bk-oa")
    book_out_b = hpath("M 328 222 L 192 236 L 178 92", amount=4.8, overshoot=10.0, seed="st-bk-ob")
    book_spine = hpath("M 204 92 L 216 230", amount=3.0, seed="st-bk-sp")
    book_label = hpath("M 226 118 L 294 110 L 298 152 L 230 160 Z", amount=3.2, seed="st-bk-lbl")
    book_line_1 = hpath("M 232 180 L 296 174", amount=2.5, seed="st-bk-l1")
    book_line_2 = hpath("M 234 198 L 278 194", amount=2.5, seed="st-bk-l2")

    # 2. Foreground Right/Lower-Right: Canvas Supply Tote Bag (breaking out bottom-right)
    tote_fill = hpath("M 248 252 L 468 230 L 488 468 L 264 486 Z", amount=5.6, seed="st-tt-fill")
    tote_out_1 = hpath("M 248 252 L 468 230 L 488 468", amount=4.8, overshoot=12.0, seed="st-tt-o1")
    tote_out_2 = hpath("M 488 468 L 264 486 L 248 252", amount=4.8, overshoot=11.0, seed="st-tt-o2")
    tote_strap_l = hpath("M 296 248 C 292 174 358 166 368 240", amount=3.8, seed="st-tt-sl")
    tote_strap_r = hpath("M 342 242 C 344 182 406 174 414 234", amount=3.8, seed="st-tt-sr")
    tote_pocket = hpath("M 294 334 L 424 320 L 432 426 L 302 438 Z", amount=4.0, seed="st-tt-pck")
    tote_stitch_1 = hpath("M 312 364 L 404 354", amount=2.6, seed="st-tt-st1")
    tote_stitch_2 = hpath("M 316 390 L 382 384", amount=2.6, seed="st-tt-st2")

    # 3. Hanging Boutique Price Tag (tilted polygon overlapping left edge of Tote)
    tag_string = hpath("M 296 248 C 254 262 224 294 212 324", amount=3.0, seed="st-tg-str")
    tag_fill = hpath("M 152 318 L 242 296 L 262 396 L 172 418 Z", amount=4.4, seed="st-tg-fill")
    tag_out = hpath("M 152 318 L 242 296 L 262 396 L 172 418 L 152 318", amount=4.2, overshoot=9.5, seed="st-tg-out")
    tag_hole = wobbly_circle(198, 326, 6.0, seed="st-tg-hole", wobble=0.08)
    tag_bar_1 = hpath("M 176 356 L 234 342", amount=2.4, seed="st-tg-b1")
    tag_bar_2 = hpath("M 182 378 L 224 368", amount=2.4, seed="st-tg-b2")

    # 4. Upper-Right Quality Seal Badge (breaking out upper-right)
    seal_ring = wobbly_circle(418, 116, 42, seed="st-seal-r", wobble=0.07, overlap=15)
    seal_star = sparkle(418, 116, 18, seed="st-seal-s")
    seal_ribbon_l = hpath("M 398 154 L 384 196 L 410 182", amount=2.5, seed="st-seal-rl")
    seal_ribbon_r = hpath("M 436 152 L 454 192 L 426 180", amount=2.5, seed="st-seal-rr")

    # 5. Quiet-area sparkles (Lower-left open paper area)
    sp_1 = sparkle(78, 396, 21, seed="st-sp-1")
    sp_2 = sparkle(116, 434, 14, seed="st-sp-2")
    sp_3 = sparkle(54, 442, 10, seed="st-sp-3")
    sp_4 = sparkle(456, 56, 13, seed="st-sp-4")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
{build_defs(seed_wash=37, seed_ink=61)}
<g id="layer-block" filter="url(#wash)" style="isolation: isolate">
  <g class="wash-blob">
    <path d="{wash_kraft}" fill="{kraft_fill}"/>
    <path d="{wash_kraft}" fill="none" stroke="{kraft_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g class="wash-blob" style="mix-blend-mode: multiply">
    <path d="{wash_cactus}" fill="{cactus_fill}"/>
    <path d="{wash_cactus}" fill="none" stroke="{cactus_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
  <g class="wash-blob">
    <path d="{wash_clay}" fill="{clay_fill}"/>
    <path d="{wash_clay}" fill="none" stroke="{clay_edge}" stroke-width="4.5" stroke-opacity="0.55" stroke-linejoin="round"/>
  </g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Background awning & brackets -->
  <path d="{bg_awning_arc}" stroke-width="4.5" stroke-dasharray="14 16"/>
  <path d="{bg_bracket_l}" stroke-width="6.0"/>
  <path d="{bg_bracket_r}" stroke-width="6.0"/>
  <path d="{bg_dotted_flow}" stroke-width="4.5" stroke-dasharray="10 14"/>

  <!-- Item A: Ceramic Pour-Over Dripper -->
  <path d="{drip_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{drip_out_a}" stroke-width="8.5"/>
  <path d="{drip_out_b}" stroke-width="8.5"/>
  <path d="{drip_handle}" stroke-width="8.5"/>
  <path d="{drip_rib_1}" stroke-width="4.5"/>
  <path d="{drip_rib_2}" stroke-width="4.5"/>
  <path d="{drip_rib_3}" stroke-width="4.5"/>
  <path d="{steam_1}" stroke-width="4.5"/>
  <path d="{steam_2}" stroke-width="4.5"/>

  <!-- Item B: Spiral Field Monograph Notebook -->
  <path d="{book_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{book_label}" fill="{clay_fill}" fill-opacity="0.32" stroke="none"/>
  <path d="{book_out_a}" stroke-width="8.5"/>
  <path d="{book_out_b}" stroke-width="8.5"/>
  <path d="{book_spine}" stroke-width="6.0"/>
  <path d="{book_label}" stroke-width="6.0"/>
  <path d="{book_line_1}" stroke-width="6.0"/>
  <path d="{book_line_2}" stroke-width="4.5"/>

  <!-- Wooden Boutique Shelf Plank -->
  <path d="{shelf_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{shelf_out}" stroke-width="8.5"/>

  <!-- Item C: Canvas Supply Tote Bag -->
  <path d="{tote_strap_l}" stroke-width="8.5"/>
  <path d="{tote_strap_r}" stroke-width="8.5"/>
  <path d="{tote_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{tote_pocket}" fill="{cactus_fill}" fill-opacity="0.28" stroke="none"/>
  <path d="{tote_out_1}" stroke-width="8.5"/>
  <path d="{tote_out_2}" stroke-width="8.5"/>
  <path d="{tote_pocket}" stroke-width="6.0"/>
  <path d="{tote_stitch_1}" stroke-width="6.0"/>
  <path d="{tote_stitch_2}" stroke-width="4.5"/>

  <!-- Hanging Boutique Price Tag -->
  <path d="{tag_string}" stroke-width="6.0"/>
  <path d="{tag_fill}" fill="{PAPER}" stroke="none"/>
  <path d="{tag_out}" stroke-width="8.5"/>
  <path d="{tag_hole}" stroke-width="4.5"/>
  <path d="{tag_bar_1}" stroke-width="6.0"/>
  <path d="{tag_bar_2}" stroke-width="6.0"/>

  <!-- Upper-Right Quality Seal Badge -->
  <path d="{seal_ring}" fill="{PAPER}" stroke="none"/>
  <path d="{seal_ring}" stroke-width="8.5"/>
  <path d="{seal_star}" stroke-width="6.0"/>
  <path d="{seal_ribbon_l}" stroke-width="6.0"/>
  <path d="{seal_ribbon_r}" stroke-width="6.0"/>

  <!-- Quiet-area sparkles -->
  <path d="{sp_1}" stroke-width="4.5"/>
  <path d="{sp_2}" stroke-width="4.5"/>
  <path d="{sp_3}" stroke-width="4.5"/>
  <path d="{sp_4}" stroke-width="4.5"/>
  <circle cx="136" cy="382" r="4.5" fill="{INK}" stroke="none"/>
  <circle cx="52" cy="364" r="3.8" fill="{sky_fill}" stroke="none"/>
</g>
</svg>
"""


def build_product_svg(kind):
    """Build custom 200x160 inline CC-lineart SVG illustration for each of the 6 storefront products."""
    if kind == "dripper":
        w = handify("M 34 26 L 154 16 L 166 132 L 44 142 Z", amount=2.5, seed="p1-w")
        body = handify("M 56 38 L 142 28 L 126 124 L 74 130 Z", amount=2.0, seed="p1-b")
        hdl = handify("M 136 48 C 166 48 164 96 128 102", amount=1.6, seed="p1-h")
        base = handify("M 54 128 L 144 120 L 146 134 L 52 142 Z", amount=1.6, seed="p1-bs")
        rib1 = handify("M 78 52 L 86 112", amount=1.2, seed="p1-r1")
        rib2 = handify("M 104 48 L 106 110", amount=1.2, seed="p1-r2")
        sp = sparkle(38, 42, 9, seed="p1-sp")
        c_fill, c_edge = COLORS["clay"]
        return f"""<svg viewBox="0 0 200 160" class="prod-svg"><g class="prod-wash" filter="url(#ui-wash)"><path d="{w}" fill="{c_fill}"/><path d="{w}" fill="none" stroke="{c_edge}" stroke-width="2" stroke-opacity="0.5"/></g><g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"><path d="{hdl}" stroke-width="3.4"/><path d="{body}" fill="{PAPER}" stroke-width="3.4"/><path d="{base}" fill="{PAPER}" stroke-width="3.2"/><path d="{rib1}" stroke-width="2.2"/><path d="{rib2}" stroke-width="2.2"/><path d="{sp}" stroke-width="2.0"/></g></svg>"""

    if kind == "notebook":
        w = handify("M 36 22 L 158 14 L 168 136 L 46 144 Z", amount=2.5, seed="p2-w")
        cov = handify("M 54 20 L 148 12 L 158 138 L 64 146 Z", amount=2.0, seed="p2-c")
        lbl = handify("M 76 42 L 132 36 L 136 74 L 80 80 Z", amount=1.5, seed="p2-l")
        l1 = handify("M 80 100 L 134 94", amount=1.2, seed="p2-l1")
        l2 = handify("M 82 116 L 118 112", amount=1.2, seed="p2-l2")
        sp = sparkle(34, 38, 8.5, seed="p2-sp")
        c_fill, c_edge = COLORS["cactus"]
        return f"""<svg viewBox="0 0 200 160" class="prod-svg"><g class="prod-wash" filter="url(#ui-wash)"><path d="{w}" fill="{c_fill}"/><path d="{w}" fill="none" stroke="{c_edge}" stroke-width="2" stroke-opacity="0.5"/></g><g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"><path d="{cov}" fill="{PAPER}" stroke-width="3.4"/><path d="{lbl}" fill="{COLORS['peach'][0]}" stroke-width="2.4"/><path d="{l1}" stroke-width="2.2"/><path d="{l2}" stroke-width="2.2"/><path d="{sp}" stroke-width="2.0"/></g></svg>"""

    if kind == "keycaps":
        w = handify("M 32 28 L 164 18 L 172 132 L 40 142 Z", amount=2.5, seed="p3-w")
        tray = handify("M 38 42 L 162 30 L 170 124 L 46 136 Z", amount=2.0, seed="p3-t")
        k1 = handify("M 56 58 L 94 54 L 98 92 L 60 96 Z", amount=1.5, seed="p3-k1")
        k2 = handify("M 108 52 L 148 48 L 152 86 L 112 90 Z", amount=1.5, seed="p3-k2")
        star = sparkle(128, 68, 8, seed="p3-st")
        sp = sparkle(28, 30, 8.5, seed="p3-sp")
        c_fill, c_edge = COLORS["sky"]
        return f"""<svg viewBox="0 0 200 160" class="prod-svg"><g class="prod-wash" filter="url(#ui-wash)"><path d="{w}" fill="{c_fill}"/><path d="{w}" fill="none" stroke="{c_edge}" stroke-width="2" stroke-opacity="0.5"/></g><g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"><path d="{tray}" fill="{PAPER}" stroke-width="3.4"/><path d="{k1}" fill="{COLORS['clay'][0]}" fill-opacity="0.35" stroke-width="2.6"/><path d="{k2}" fill="{COLORS['peach'][0]}" fill-opacity="0.45" stroke-width="2.6"/><path d="{star}" stroke-width="2.0"/><path d="{sp}" stroke-width="2.0"/></g></svg>"""

    if kind == "satchel":
        w = handify("M 34 26 L 160 16 L 168 134 L 42 144 Z", amount=2.5, seed="p4-w")
        bag = handify("M 46 48 L 154 38 L 162 132 L 54 142 Z", amount=2.0, seed="p4-b")
        flap = handify("M 46 48 L 154 38 L 146 88 L 58 96 Z", amount=1.8, seed="p4-f")
        strap = handify("M 78 44 C 78 16 124 14 128 40", amount=1.6, seed="p4-s")
        buckle = handify("M 96 78 L 112 76 L 114 98 L 98 100 Z", amount=1.2, seed="p4-bk")
        sp = sparkle(32, 34, 8.5, seed="p4-sp")
        c_fill, c_edge = COLORS["kraft"]
        return f"""<svg viewBox="0 0 200 160" class="prod-svg"><g class="prod-wash" filter="url(#ui-wash)"><path d="{w}" fill="{c_fill}"/><path d="{w}" fill="none" stroke="{c_edge}" stroke-width="2" stroke-opacity="0.5"/></g><g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"><path d="{strap}" stroke-width="3.4"/><path d="{bag}" fill="{PAPER}" stroke-width="3.4"/><path d="{flap}" fill="{PAPER}" stroke-width="3.0"/><path d="{buckle}" fill="{COLORS['clay'][0]}" stroke-width="2.4"/><path d="{sp}" stroke-width="2.0"/></g></svg>"""

    if kind == "deck":
        w = handify("M 38 24 L 162 14 L 170 134 L 46 144 Z", amount=2.5, seed="p5-w")
        c_back = handify("M 48 34 L 122 22 L 136 118 L 62 130 Z", amount=1.8, seed="p5-cb")
        c_front = handify("M 74 28 L 152 36 L 142 134 L 64 126 Z", amount=1.8, seed="p5-cf")
        seal = wobbly_circle(108, 78, 18, seed="p5-sl")
        sp = sparkle(108, 78, 9, seed="p5-sp")
        c_fill, c_edge = COLORS["heather"]
        return f"""<svg viewBox="0 0 200 160" class="prod-svg"><g class="prod-wash" filter="url(#ui-wash)"><path d="{w}" fill="{c_fill}"/><path d="{w}" fill="none" stroke="{c_edge}" stroke-width="2" stroke-opacity="0.5"/></g><g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"><path d="{c_back}" fill="{PAPER}" stroke-width="3.0"/><path d="{c_front}" fill="{PAPER}" stroke-width="3.4"/><path d="{seal}" fill="{COLORS['plum'][0]}" fill-opacity="0.28" stroke-width="2.6"/><path d="{sp}" stroke-width="2.2"/></g></svg>"""

    # lamp
    w = handify("M 36 24 L 158 16 L 166 134 L 44 142 Z", amount=2.5, seed="p6-w")
    shade = handify("M 52 58 C 62 20 138 16 148 52 Z", amount=2.0, seed="p6-sh")
    stem = handify("M 102 54 L 106 124", amount=1.5, seed="p6-st")
    base = handify("M 68 124 L 138 118 L 144 136 L 64 142 Z", amount=1.8, seed="p6-bs")
    pull = handify("M 124 54 L 126 82", amount=1.2, seed="p6-pl")
    sp = sparkle(40, 34, 8.5, seed="p6-sp")
    c_fill, c_edge = COLORS["olive"]
    return f"""<svg viewBox="0 0 200 160" class="prod-svg"><g class="prod-wash" filter="url(#ui-wash)"><path d="{w}" fill="{c_fill}"/><path d="{w}" fill="none" stroke="{c_edge}" stroke-width="2" stroke-opacity="0.5"/></g><g filter="url(#ui-ink)" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"><path d="{stem}" stroke-width="3.4"/><path d="{pull}" stroke-width="2.2"/><path d="{shade}" fill="{PAPER}" stroke-width="3.4"/><path d="{base}" fill="{PAPER}" stroke-width="3.2"/><path d="{sp}" stroke-width="2.0"/></g></svg>"""


def build_storefront_html(showcase_svg):
    products = [
        {
            "id": "dripper",
            "name": "Artisan Ceramic V60 Dripper",
            "cat": "hardware",
            "cat_label": "Desk Hardware",
            "price": 42,
            "badge": "BESTSELLER",
            "badge_color": "#D4714E",
            "desc": "Hand-thrown stoneware pour-over cone with spiral internal ribs for late-night debugging sessions.",
            "svg": build_product_svg("dripper"),
        },
        {
            "id": "notebook",
            "name": "Dot-Grid Field Monograph",
            "cat": "stationery",
            "cat_label": "Field Stationery",
            "price": 24,
            "badge": "NEW EDITION",
            "badge_color": "#6F8F6B",
            "desc": "160gsm warm cream archival paper (`#FAF9F5`) with lay-flat thread binding and architecture index.",
            "svg": build_product_svg("notebook"),
        },
        {
            "id": "keycaps",
            "name": "Tactile Terracotta Keycap Set",
            "cat": "hardware",
            "cat_label": "Desk Hardware",
            "price": 68,
            "badge": "LIMITED",
            "badge_color": "#5B8FA8",
            "desc": "PBT dye-sublimated keycaps featuring hand-drawn Claude starburst & wobbly return legends.",
            "svg": build_product_svg("keycaps"),
        },
        {
            "id": "satchel",
            "name": "Waxed Canvas Cable Satchel",
            "cat": "stationery",
            "cat_label": "Field Stationery",
            "price": 54,
            "badge": "CRAFT SERIES",
            "badge_color": "#A87E52",
            "desc": "Structured kraft-dyed organizer pouch for adapters, fountain pens, and SSD field drives.",
            "svg": build_product_svg("satchel"),
        },
        {
            "id": "deck",
            "name": "Visual Architecture Prompt Deck",
            "cat": "digital",
            "cat_label": "Digital Packs",
            "price": 29,
            "badge": "DIGITAL + PRINT",
            "badge_color": "#8E72A8",
            "desc": "52 tactile reference cards + SVG generator recipes for diagrams, UI kits, and hero illustrations.",
            "svg": build_product_svg("deck"),
        },
        {
            "id": "lamp",
            "name": "Atelier Brass Studio Lamp",
            "cat": "hardware",
            "cat_label": "Desk Hardware",
            "price": 86,
            "badge": "STUDIO PICK",
            "badge_color": "#7D8B52",
            "desc": "Warm 2700K parchment-diffused task lamp with tactile brass pull-chain and weighted base.",
            "svg": build_product_svg("lamp"),
        },
    ]

    cards_html = []
    for idx, p in enumerate(products):
        tag_d = handify("M 8 6 L 78 4 L 84 36 L 12 38 Z", amount=1.4, seed=f"ptag-{idx}")
        cards_html.append(f"""
        <article class="product-card" data-category="{p['cat']}" data-id="{p['id']}" data-name="{p['name']}" data-price="{p['price']}">
          <div class="product-visual">
            <span class="stamp-badge" style="--badge-tint: {p['badge_color']}">{p['badge']}</span>
            {p['svg']}
            <div class="price-tag-wrap" aria-label="Price ${p['price']}">
              <svg viewBox="0 0 92 44" class="price-tag-svg">
                <path d="{tag_d}" fill="#FFFEFA" stroke="#141413" stroke-width="2.4" stroke-linejoin="round"/>
                <circle cx="18" cy="22" r="3.2" fill="#FAF6F0" stroke="#141413" stroke-width="2"/>
              </svg>
              <span class="price-tag-val">${p['price']}</span>
            </div>
          </div>
          <div class="product-body">
            <div class="product-cat">{p['cat_label']}</div>
            <h3 class="product-title">{p['name']}</h3>
            <p class="product-desc">{p['desc']}</p>
            <div class="product-footer">
              <span class="stock-note">In Stock · Ships in 24h</span>
              <button type="button" class="add-bag-btn" onclick="addToBag('{p['id']}', '{p['name']}', {p['price']})">
                <span>+ Add to Bag</span>
              </button>
            </div>
          </div>
        </article>
        """)

    empty_bag_d = handify("M 36 42 L 104 36 L 112 114 L 42 120 Z", amount=2.2, seed="empty-bag")
    empty_strap = handify("M 54 40 C 54 18 86 16 88 38", amount=1.6, seed="empty-strap")
    empty_sp = sparkle(24, 30, 8, seed="empty-sp")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Claudette Goods & Field Supply — CC-lineart Boutique Storefront</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --paper-bg: #FAF6F0;
      --paper-card: #FFFEFA;
      --ink: #141413;
      --ink-muted: #57524B;
      --clay: #D4714E;
      --cactus: #A8C4A2;
      --sky: #9BB8D3;
      --kraft: #D4B896;
      --border: rgba(20, 20, 19, 0.16);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--paper-bg);
      color: var(--ink);
      font-family: 'Inter', -apple-system, sans-serif;
      line-height: 1.55;
      padding-bottom: 64px;
    }}
    .announce-bar {{
      background: var(--ink);
      color: var(--paper-bg);
      text-align: center;
      padding: 8px 16px;
      font-size: 12.5px;
      letter-spacing: 0.04em;
    }}
    .announce-bar span {{ color: #E8A87C; font-weight: 600; }}
    .container {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 24px;
    }}
    /* Store Header */
    .store-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 22px 0;
      border-bottom: 2px solid var(--ink);
      gap: 16px;
      flex-wrap: wrap;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--ink);
    }}
    .brand-title {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: 26px;
      font-weight: 600;
      letter-spacing: -0.02em;
    }}
    .brand-sub {{
      font-family: 'Caveat', cursive;
      font-size: 18px;
      color: var(--clay);
      margin-left: 6px;
    }}
    .header-controls {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .filter-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .filter-pill {{
      background: var(--paper-card);
      border: 2px solid var(--ink);
      border-radius: 999px;
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: transform 0.18s ease, background 0.18s ease;
    }}
    .filter-pill:hover {{ transform: translateY(-2px); }}
    .filter-pill.active {{
      background: var(--ink);
      color: var(--paper-card);
    }}
    .bag-toggle-btn {{
      background: #E8A87C;
      border: 2px solid var(--ink);
      border-radius: 12px;
      padding: 8px 16px;
      font-weight: 600;
      font-size: 13.5px;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 3px 3px 0 var(--ink);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .bag-toggle-btn:hover {{
      transform: translate(-1px, -1px);
      box-shadow: 4px 4px 0 var(--ink);
    }}
    .bag-count {{
      background: var(--ink);
      color: var(--paper-card);
      border-radius: 999px;
      padding: 1px 8px;
      font-size: 12px;
    }}

    /* Seasonal Promo Split Banner */
    .promo-banner {{
      margin: 28px 0 32px;
      background: var(--paper-card);
      border: 2.5px solid var(--ink);
      border-radius: 18px;
      box-shadow: 6px 6px 0 var(--ink);
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      overflow: hidden;
      position: relative;
    }}
    .promo-copy {{
      padding: 36px 38px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 14px;
    }}
    .promo-eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'Caveat', cursive;
      font-size: 22px;
      color: var(--clay);
    }}
    .promo-headline {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: clamp(28px, 3.4vw, 42px);
      line-height: 1.12;
      font-weight: 600;
      letter-spacing: -0.02em;
    }}
    .promo-lead {{
      color: var(--ink-muted);
      font-size: 15.5px;
      max-width: 52ch;
    }}
    .promo-meta {{
      display: flex;
      align-items: center;
      gap: 18px;
      margin-top: 6px;
      flex-wrap: wrap;
      font-size: 13px;
      font-weight: 500;
    }}
    .promo-art {{
      background: linear-gradient(135deg, rgba(212, 184, 150, 0.22), rgba(168, 196, 162, 0.22));
      border-left: 2px dashed rgba(20, 20, 19, 0.25);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 18px;
    }}
    .promo-art svg {{
      width: 100%;
      max-width: 320px;
      height: auto;
      display: block;
    }}

    /* Main Storefront Layout: Grid + Bag Sidebar */
    .store-layout {{
      display: grid;
      grid-template-columns: 1fr 330px;
      gap: 28px;
      align-items: start;
    }}
    @media (max-width: 960px) {{
      .promo-banner {{ grid-template-columns: 1fr; }}
      .store-layout {{ grid-template-columns: 1fr; }}
    }}
    .product-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(248px, 1fr));
      gap: 22px;
    }}
    .product-card {{
      background: var(--paper-card);
      border: 2.2px solid var(--ink);
      border-radius: 16px;
      box-shadow: 4px 4px 0 var(--ink);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .product-card:hover {{
      transform: translateY(-4px);
      box-shadow: 7px 7px 0 var(--ink);
    }}
    .product-card:hover .prod-wash {{
      transform: translate(5px, -4px) scale(1.05);
    }}
    .prod-wash {{
      transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
      transform-origin: center;
    }}
    .product-visual {{
      position: relative;
      background: #FAF8F3;
      border-bottom: 2px solid var(--ink);
      padding: 14px;
      height: 176px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .prod-svg {{
      width: 100%;
      height: 148px;
      display: block;
    }}
    .stamp-badge {{
      position: absolute;
      top: 10px;
      left: 10px;
      background: var(--paper-card);
      color: var(--ink);
      border: 1.8px solid var(--ink);
      padding: 2px 9px;
      border-radius: 6px;
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      transform: rotate(-3deg);
      box-shadow: 2px 2px 0 var(--badge-tint, #D4714E);
    }}
    .price-tag-wrap {{
      position: absolute;
      bottom: 8px;
      right: 10px;
      width: 78px;
      height: 38px;
      transform: rotate(4deg);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .price-tag-svg {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
    }}
    .price-tag-val {{
      position: relative;
      font-family: 'Newsreader', Georgia, serif;
      font-weight: 600;
      font-size: 16px;
      padding-left: 8px;
    }}
    .product-body {{
      padding: 16px 18px 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 6px;
    }}
    .product-cat {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--ink-muted);
      font-weight: 600;
    }}
    .product-title {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: 19px;
      font-weight: 600;
      line-height: 1.25;
    }}
    .product-desc {{
      font-size: 13px;
      color: var(--ink-muted);
      flex: 1;
      margin-bottom: 10px;
    }}
    .product-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 10px;
      border-top: 1.5px dashed rgba(20, 20, 19, 0.18);
    }}
    .stock-note {{
      font-family: 'Caveat', cursive;
      font-size: 16px;
      color: #4A6B46;
    }}
    .add-bag-btn {{
      background: var(--ink);
      color: var(--paper-card);
      border: 2px solid var(--ink);
      border-radius: 10px;
      padding: 6px 12px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease;
    }}
    .add-bag-btn:hover {{
      background: var(--clay);
      color: var(--ink);
    }}

    /* Tactile Shopping Bag Drawer / Panel */
    .bag-panel {{
      background: var(--paper-card);
      border: 2.5px solid var(--ink);
      border-radius: 16px;
      box-shadow: 5px 5px 0 var(--ink);
      padding: 20px;
      position: sticky;
      top: 20px;
    }}
    .bag-panel-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 12px;
      border-bottom: 2px solid var(--ink);
      margin-bottom: 14px;
    }}
    .bag-panel-title {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: 20px;
      font-weight: 600;
    }}
    .bag-clear-btn {{
      background: none;
      border: none;
      font-size: 12px;
      text-decoration: underline;
      color: var(--ink-muted);
      cursor: pointer;
    }}
    .bag-items {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 280px;
      overflow-y: auto;
    }}
    .bag-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #FAF6F0;
      border: 1.6px solid var(--ink);
      border-radius: 10px;
      padding: 8px 12px;
      font-size: 13px;
    }}
    .bag-item-name {{ font-weight: 600; }}
    .bag-item-meta {{ color: var(--ink-muted); font-size: 12px; }}
    .bag-empty {{
      text-align: center;
      padding: 18px 8px;
      color: var(--ink-muted);
      font-size: 13.5px;
    }}
    .bag-empty svg {{
      width: 110px;
      height: 110px;
      margin: 0 auto 8px;
      display: block;
    }}
    .bag-summary {{
      margin-top: 16px;
      padding-top: 14px;
      border-top: 2px dashed rgba(20, 20, 19, 0.25);
    }}
    .bag-row {{
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      margin-bottom: 6px;
    }}
    .bag-total {{
      font-family: 'Newsreader', Georgia, serif;
      font-size: 20px;
      font-weight: 600;
      margin-top: 6px;
    }}
    .checkout-btn {{
      width: 100%;
      margin-top: 12px;
      background: var(--clay);
      color: var(--paper-card);
      border: 2px solid var(--ink);
      border-radius: 12px;
      padding: 11px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 3px 3px 0 var(--ink);
    }}
  </style>
</head>
<body>
  <!-- Shared SVG Filters for Product Cards -->
  <svg width="0" height="0" style="position:absolute">
    <defs>
      <filter id="ui-wash" x="-15%" y="-15%" width="130%" height="130%">
        <feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="3" seed="19" result="n"/>
        <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/>
      </filter>
      <filter id="ui-ink" x="-8%" y="-8%" width="116%" height="116%">
        <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="29" result="n"/>
        <feDisplacementMap in="SourceGraphic" in2="n" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
      </filter>
    </defs>
  </svg>

  <div class="announce-bar">
    <span>AUTUMN MONOGRAPH DROP</span> · Free global courier on orders over $75 · Every item illustrated in 100% vector ink
  </div>

  <div class="container">
    <header class="store-header">
      <a href="#" class="brand">
        <span class="brand-title">Claudette Goods &amp; Field Supply</span>
        <span class="brand-sub">Est. Vol IV</span>
      </a>
      <div class="header-controls">
        <div class="filter-pills" role="tablist" aria-label="Product categories">
          <button class="filter-pill active" onclick="filterCategory('all', this)">All Goods (6)</button>
          <button class="filter-pill" onclick="filterCategory('stationery', this)">Field Stationery</button>
          <button class="filter-pill" onclick="filterCategory('hardware', this)">Desk Hardware</button>
          <button class="filter-pill" onclick="filterCategory('digital', this)">Digital Packs</button>
        </div>
        <button class="bag-toggle-btn" onclick="document.getElementById('bag-panel').scrollIntoView({{behavior:'smooth'}})">
          <span>Field Bag</span>
          <span class="bag-count" id="header-bag-count">2</span>
        </button>
      </div>
    </header>

    <section class="promo-banner">
      <div class="promo-copy">
        <div class="promo-eyebrow">★ Curated Objects for Thoughtful Builders</div>
        <h1 class="promo-headline">Tactile tools &amp; field monographs, drawn in warm ink &amp; watercolor.</h1>
        <p class="promo-lead">
          No stock photography, no sterile white-box renders. Every product card, hanging price tag, and quality seal on this storefront is synthesized deterministically with <strong>CC-lineart</strong>.
        </p>
        <div class="promo-meta">
          <span>✓ 100% Vector Product Art</span>
          <span>✓ Hover Watercolor Parallax</span>
          <span>✓ Interactive Field Bag</span>
        </div>
      </div>
      <div class="promo-art">
        {showcase_svg}
      </div>
    </section>

    <div class="store-layout">
      <main class="product-grid" id="product-grid">
        {''.join(cards_html)}
      </main>

      <aside class="bag-panel" id="bag-panel" aria-label="Shopping Bag">
        <div class="bag-panel-head">
          <h2 class="bag-panel-title">Your Field Bag</h2>
          <button class="bag-clear-btn" onclick="clearBag()">Empty bag</button>
        </div>
        <div id="bag-items" class="bag-items"></div>
        <div id="bag-empty" class="bag-empty" style="display:none">
          <svg viewBox="0 0 140 140">
            <g filter="url(#ui-wash)">
              <circle cx="72" cy="78" r="38" fill="#E8C99B" opacity="0.55"/>
            </g>
            <g filter="url(#ui-ink)" fill="none" stroke="#141413" stroke-linecap="round" stroke-linejoin="round">
              <path d="{empty_strap}" stroke-width="3.2"/>
              <path d="{empty_bag_d}" fill="#FFFEFA" stroke-width="3.2"/>
              <path d="{empty_sp}" stroke-width="2.0"/>
            </g>
          </svg>
          <p><strong>Your field bag is empty</strong><br/>Add a notebook, dripper, or keycap set from the shelf.</p>
        </div>
        <div class="bag-summary">
          <div class="bag-row"><span>Complimentary Monograph Bookmark</span><span>FREE</span></div>
          <div class="bag-row bag-total"><span>Subtotal</span><span id="bag-subtotal">$66</span></div>
          <button class="checkout-btn" onclick="alert('Demo Checkout — All storefront illustrations generated by CC-lineart!')">
            Proceed to Atelier Checkout →
          </button>
        </div>
      </aside>
    </div>
  </div>

  <script>
    let bag = [
      {{ id: 'dripper', name: 'Artisan Ceramic V60 Dripper', price: 42, qty: 1 }},
      {{ id: 'notebook', name: 'Dot-Grid Field Monograph', price: 24, qty: 1 }}
    ];

    function renderBag() {{
      const listEl = document.getElementById('bag-items');
      const emptyEl = document.getElementById('bag-empty');
      const countEl = document.getElementById('header-bag-count');
      const subEl = document.getElementById('bag-subtotal');

      const totalQty = bag.reduce((s, item) => s + item.qty, 0);
      const totalPrice = bag.reduce((s, item) => s + item.price * item.qty, 0);
      countEl.textContent = totalQty;
      subEl.textContent = '$' + totalPrice;

      if (bag.length === 0) {{
        listEl.style.display = 'none';
        emptyEl.style.display = 'block';
        return;
      }}
      listEl.style.display = 'flex';
      emptyEl.style.display = 'none';
      listEl.innerHTML = bag.map(item => `
        <div class="bag-item">
          <div>
            <div class="bag-item-name">${{item.name}}</div>
            <div class="bag-item-meta">Qty ${{item.qty}} × $${{item.price}}</div>
          </div>
          <strong>$${{item.qty * item.price}}</strong>
        </div>
      `).join('');
    }}

    function addToBag(id, name, price) {{
      const found = bag.find(x => x.id === id);
      if (found) found.qty += 1;
      else bag.push({{ id, name, price, qty: 1 }});
      renderBag();
    }}

    function clearBag() {{
      bag = [];
      renderBag();
    }}

    function filterCategory(cat, btn) {{
      document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.product-card').forEach(card => {{
        if (cat === 'all' || card.dataset.category === cat) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    renderBag();
  </script>
</body>
</html>
"""


def render_png(svg_path, png_path, size=512):
    if not shutil.which("rsvg-convert"):
        return
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), "-b", PAPER, svg_path, "-o", png_path],
        check=True,
    )
    print(f"Wrote {png_path}")


def main():
    showcase_svg = build_storefront_showcase_svg()
    svg_path = os.path.join(HERE, "storefront-showcase.svg")
    png_path = os.path.join(HERE, "storefront-showcase.png")
    html_path = os.path.join(HERE, "marketplace-storefront.html")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(showcase_svg)
    print(f"Wrote {svg_path}")

    render_png(svg_path, png_path, size=512)

    html_doc = build_storefront_html(showcase_svg)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"Wrote {html_path}")


if __name__ == "__main__":
    main()
