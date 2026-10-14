#!/usr/bin/env python3
"""Generate Editorial Architecture & Technical Workflow Diagrams in the CC-lineart style.

Produces two SVG diagrams in /Users/wu/CC-lineart/examples/diagrams/:
  1. agent-orchestration.svg (800x480 viewBox)
     Orchestrator -> Subagent Fan-Out -> Synthesis / PR architecture diagram.
  2. rag-pipeline.svg (512x512 viewBox)
     Document Ingestion -> Vector Index -> Context Synthesis technical flow diagram.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lineart import COLORS, INK, PAPER, fmt, handify, sparkle, wobbly_circle  # noqa: E402


def drawn_circle(cx, cy, r, seed="circle", wobble=0.07):
    """A hand-drawn loop built on wobbly_circle with an intentional axis skew so it is
    never mechanically mirror-symmetric across the X axis."""
    rng = random.Random(f"skew:{seed}:{cx}:{cy}:{r}")
    start = rng.uniform(15, 65)
    knots = 5
    overlap = 18
    sweep = 360 + overlap
    step = sweep / knots
    # Deliberately asymmetric radial profile (right-upper side slightly fuller, left flatter)
    skew_factors = [1.08, 0.92, 0.89, 1.09, 1.16, 0.95]
    radii = [
        r * skew_factors[i] * (1 + rng.uniform(-wobble, wobble))
        for i in range(knots + 1)
    ]

    def at(i):
        a = math.radians(start + i * step)
        # Slight horizontal drift on upper vs lower half breaks X-mirror symmetry cleanly
        dx_skew = r * 0.12 * math.sin(a)
        return a, (cx + radii[i] * math.cos(a) + dx_skew, cy + radii[i] * math.sin(a))

    k = 4 / 3 * math.tan(math.radians(step) / 4)
    _, p0 = at(0)
    parts = [f"M{fmt(p0)}"]
    for i in range(knots):
        a, p = at(i)
        b, q = at(i + 1)
        c1 = (p[0] - k * radii[i] * math.sin(a), p[1] + k * radii[i] * math.cos(a))
        c2 = (q[0] + k * radii[i + 1] * math.sin(b), q[1] - k * radii[i + 1] * math.cos(b))
        parts.append(f"C{fmt(c1)} {fmt(c2)} {fmt(q)}")
    # Add a small hand-drawn tail at the end of the loop so the pen lift is visible and asymmetric
    _, pend = at(knots)
    tail = (pend[0] + r * 0.18, pend[1] - r * 0.09)
    parts.append(f"L{fmt(tail)}")
    return " ".join(parts)


def card_path(x, y, w, h, amount=4.5, seed="card"):
    """Hand-drawn quadrilateral card with slightly off-grid corners and bowed edges."""
    rng = random.Random(seed)
    p1 = (x + rng.uniform(-2.0, 2.5), y + rng.uniform(-2.0, 2.0))
    p2 = (x + w + rng.uniform(-2.0, 3.5), y + rng.uniform(-3.0, 1.5))
    p3 = (x + w + rng.uniform(-3.5, 2.0), y + h + rng.uniform(-1.5, 3.0))
    p4 = (x + rng.uniform(-3.0, 2.0), y + h + rng.uniform(-2.0, 2.5))
    raw = f"M{fmt(p1)} L{fmt(p2)} L{fmt(p3)} L{fmt(p4)} Z"
    return handify(raw, amount=amount, seed=seed + ":h"), (p1, p2, p3, p4)


def corner_overshoot(corners, which=(0, 2), amount=3.5, overshoot=11.0, seed="ov"):
    """Draw open two-segment corner strokes with architect-sketch overshoot on selected corners."""
    out = []
    for idx in which:
        p_prev = corners[(idx - 1) % 4]
        p_cur = corners[idx]
        p_next = corners[(idx + 1) % 4]
        a = (p_cur[0] + (p_prev[0] - p_cur[0]) * 0.32, p_cur[1] + (p_prev[1] - p_cur[1]) * 0.32)
        b = (p_cur[0] + (p_next[0] - p_cur[0]) * 0.38, p_cur[1] + (p_next[1] - p_cur[1]) * 0.38)
        raw = f"M{fmt(a)} L{fmt(p_cur)} L{fmt(b)}"
        out.append(handify(raw, amount=amount * 0.6, overshoot=overshoot, seed=f"{seed}:{idx}"))
    return " ".join(out)


def starburst_rays(cx, cy, r_inner, r_outer, seed="star"):
    """7-ray asymmetric Claude starburst with irregular angles and +/-15% length variation."""
    rng = random.Random(seed)
    angles = (-90, -38, 8, 52, 98, 146, 196)
    segs = []
    for i, deg in enumerate(angles):
        a = math.radians(deg + rng.uniform(-4.0, 4.0))
        r0 = r_inner * rng.uniform(0.85, 1.18)
        r1 = r_outer * rng.uniform(0.82, 1.22)
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        p1 = (cx + r1 * math.cos(a), cy + r1 * math.sin(a))
        segs.append(handify(f"M{fmt(p0)} L{fmt(p1)}", amount=1.2, seed=f"{seed}:r{i}"))
    return " ".join(segs)


def arrowhead(tip, from_pt, size=14.0, spread_deg=28.0, seed="arr"):
    """Asymmetric hand-drawn open arrowhead pointing from `from_pt` to `tip`."""
    rng = random.Random(seed)
    dx, dy = tip[0] - from_pt[0], tip[1] - from_pt[1]
    base_angle = math.atan2(dy, dx)
    a1 = base_angle + math.pi - math.radians(spread_deg + rng.uniform(-4, 5))
    a2 = base_angle + math.pi + math.radians(spread_deg * 1.15 + rng.uniform(-4, 5))
    len1 = size * rng.uniform(0.88, 1.04)
    len2 = size * rng.uniform(1.08, 1.26)  # one wing intentionally longer for asymmetry
    w1 = (tip[0] + len1 * math.cos(a1), tip[1] + len1 * math.sin(a1))
    w2 = (tip[0] + len2 * math.cos(a2), tip[1] + len2 * math.sin(a2))
    raw = f"M{fmt(w1)} L{fmt(tip)} L{fmt(w2)}"
    return handify(raw, amount=1.6, overshoot=2.2, seed=seed + ":ah")


def wash_filter_def(fid, seed, scale=13):
    """SVG filter definition for an individual watercolor wash layer."""
    return f"""  <filter id="{fid}" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="4" seed="{seed}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="{scale}" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.05 1.45" result="a"/>
    <feComposite in="d" in2="a" operator="in"/>
  </filter>"""


def wash_block(d, color_name, filter_id):
    """Single watercolor block with its own mottled filter and darker pooled edge rim."""
    fill, edge = COLORS[color_name]
    return (
        f'<g filter="url(#{filter_id})" style="mix-blend-mode: multiply">\n'
        f'    <path d="{d}" fill="{fill}"/>\n'
        f'    <path d="{d}" fill="none" stroke="{edge}" stroke-width="4.5" '
        f'stroke-opacity="0.55" stroke-linejoin="round"/>\n'
        f'  </g>'
    )


def build_agent_orchestration_svg():
    """Diagram 1: Orchestrator -> Subagent Fan-Out -> Synthesis / PR (800x480)."""
    # Stroke weight hierarchy for 800x480:
    #   heavy outlines: 8.0
    #   connectors & secondary frames: 5.6
    #   interior motifs & details: 4.2
    #   fine accents & sparkles: 3.4
    W_OUT = "8.0"
    W_CONN = "5.6"
    W_DET = "4.2"
    W_ACC = "3.4"

    # --- Layer 1: Watercolor washes (warm clay + cool sky + focal kraft spot) ---
    # Each wash uses its own turbulence seed so overlapping regions glaze with dual texture
    wash_clay = "M 68 58 L 434 44 L 448 312 L 82 332 Z"
    wash_sky = "M 336 138 L 722 122 L 738 428 L 322 444 Z"
    wash_focal = "M 556 68 L 704 58 L 716 164 L 548 174 Z"

    # --- Layer 2a: Strokes behind paper shapes (bus lines + curved fan-out & merge paths) ---
    behind = []
    # Subtle stage divider / dispatch rails passing behind the cards
    rail_left = handify("M 134 48 L 126 350", amount=4.0, seed="rail-l")
    rail_mid = handify("M 398 22 L 390 462", amount=4.5, seed="rail-m")
    behind.append(
        f'<path d="{rail_left}" stroke-width="{W_ACC}" stroke-dasharray="10 14"/>'
    )
    behind.append(
        f'<path d="{rail_mid}" stroke-width="{W_ACC}" stroke-dasharray="8 13"/>'
    )

    # Fan-out connectors from Orchestrator right edge (~225, 195) to 3 Subagents
    conn_to_s1 = handify("M 215 162 C 252 118 274 96 318 92", amount=3.5, seed="c-s1")
    conn_to_s2 = handify("M 222 198 C 258 192 282 228 314 236", amount=3.5, seed="c-s2")
    conn_to_s3 = handify("M 210 238 C 248 312 272 368 322 384", amount=3.5, seed="c-s3")

    # Convergence connectors from 3 Subagents right edges (~480) to Synthesis PR card (~575)
    conn_from_s1 = handify("M 472 96 C 518 104 536 154 574 196", amount=3.5, seed="c-f1")
    conn_from_s2 = handify("M 478 242 C 516 248 540 242 572 248", amount=3.5, seed="c-f2")
    conn_from_s3 = handify("M 482 382 C 526 374 544 332 576 296", amount=3.5, seed="c-f3")

    # Feedback review loop arching from Synthesis top back to Orchestrator top
    feedback_arc = handify("M 642 152 C 556 18 286 14 156 102", amount=4.0, seed="fb-arc")
    behind.append(
        f'<path d="{feedback_arc}" stroke-width="{W_ACC}" stroke-dasharray="12 11"/>'
    )

    for c_d in (conn_to_s1, conn_to_s2, conn_to_s3, conn_from_s1, conn_from_s2, conn_from_s3):
        behind.append(f'<path d="{c_d}" stroke-width="{W_CONN}"/>')

    # --- Layer 2b: Paper shapes (back to front) ---
    paper_and_cards = []

    # 1. Orchestrator backing card + main card (left, breaking out left of clay wash)
    orch_back_d, _ = card_path(26, 120, 184, 174, amount=4.0, seed="orch-bg")
    paper_and_cards.append(
        f'<path d="{orch_back_d}" fill="{PAPER}" stroke-width="{W_CONN}"/>'
    )
    orch_d, orch_pts = card_path(42, 102, 184, 176, amount=4.2, seed="orch-fg")
    paper_and_cards.append(
        f'<path d="{orch_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>'
    )
    paper_and_cards.append(
        f'<path d="{corner_overshoot(orch_pts, (0, 2), overshoot=12, seed="orch-ov")}" stroke-width="{W_CONN}"/>'
    )

    # 2. Subagent 1 Card (Top-Center: Search / Explorer, breaking out above clay wash)
    s1_d, s1_pts = card_path(316, 36, 160, 114, amount=3.8, seed="s1-card")
    paper_and_cards.append(
        f'<path d="{s1_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>'
    )
    paper_and_cards.append(
        f'<path d="{corner_overshoot(s1_pts, (1,), overshoot=9, seed="s1-ov")}" stroke-width="{W_CONN}"/>'
    )

    # 3. Subagent 2 Card (Mid-Center: Code / Branch Worker, sitting on clay+sky glaze)
    s2_d, s2_pts = card_path(310, 182, 170, 116, amount=3.8, seed="s2-card")
    paper_and_cards.append(
        f'<path d="{s2_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>'
    )
    paper_and_cards.append(
        f'<path d="{corner_overshoot(s2_pts, (0, 3), overshoot=9, seed="s2-ov")}" stroke-width="{W_CONN}"/>'
    )

    # 4. Subagent 3 Card (Bottom-Center: Docs / Knowledge Reader, breaking out bottom)
    s3_d, s3_pts = card_path(320, 330, 164, 114, amount=3.8, seed="s3-card")
    paper_and_cards.append(
        f'<path d="{s3_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>'
    )
    paper_and_cards.append(
        f'<path d="{corner_overshoot(s3_pts, (2,), overshoot=9, seed="s3-ov")}" stroke-width="{W_CONN}"/>'
    )

    # 5. Synthesis / PR Deliverable Card (Right: breaking out right of sky wash)
    pr_back_d, _ = card_path(588, 166, 184, 192, amount=4.0, seed="pr-bg")
    paper_and_cards.append(
        f'<path d="{pr_back_d}" fill="{PAPER}" stroke-width="{W_CONN}"/>'
    )
    pr_d, pr_pts = card_path(570, 148, 186, 194, amount=4.2, seed="pr-fg")
    paper_and_cards.append(
        f'<path d="{pr_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>'
    )
    paper_and_cards.append(
        f'<path d="{corner_overshoot(pr_pts, (0, 2), overshoot=12, seed="pr-ov")}" stroke-width="{W_CONN}"/>'
    )

    # Small in-flight message tokens sitting IN FRONT of the connector paths (asymmetric capsules)
    tok1_d, _ = card_path(254, 112, 28, 18, amount=1.8, seed="tok1")
    tok2_d, _ = card_path(252, 204, 26, 18, amount=1.8, seed="tok2")
    tok3_d, _ = card_path(514, 236, 30, 19, amount=1.8, seed="tok3")
    for td in (tok1_d, tok2_d, tok3_d):
        paper_and_cards.append(
            f'<path d="{td}" fill="{PAPER}" stroke-width="{W_DET}"/>'
        )

    # --- Layer 3: Details on top of paper & foreground elements ---
    details = []

    # Inside Orchestrator Card: terminal header divider (stops short on right so no extra closed hole),
    # window dots, prompt chevron `>_`, and Claude starburst
    orch_div = handify("M 44 138 L 208 140", amount=2.2, seed="orch-div")
    details.append(f'<path d="{orch_div}" stroke-width="{W_DET}"/>')
    details.append(f'<circle cx="62" cy="121" r="4.2" fill="{INK}" stroke="none"/>')
    details.append(f'<circle cx="79" cy="120" r="4.2" fill="{INK}" stroke="none"/>')
    # Prompt chevron >_
    chev = handify("M 62 174 L 84 190 L 64 206", amount=2.0, seed="orch-chev")
    und = handify("M 92 208 L 118 206", amount=1.8, seed="orch-und")
    details.append(f'<path d="{chev}" stroke-width="{W_CONN}"/>')
    details.append(f'<path d="{und}" stroke-width="{W_CONN}"/>')
    # Asymmetric hand-drawn clay patch + 7-ray Claude starburst in right half of Orchestrator card
    star_bg = handify("M 144 178 C 158 166 184 168 192 184 C 198 202 186 222 166 224 C 146 225 136 208 140 190 Z", amount=1.8, seed="orch-sbg")
    details.append(f'<path d="{star_bg}" fill="{COLORS["clay"][0]}" stroke="none"/>')
    details.append(f'<path d="{starburst_rays(166, 196, 8, 30, seed="orch-star")}" stroke-width="{W_DET}"/>')
    # Uneven task spec lines at bottom of Orchestrator card
    details.append(f'<path d="{handify("M 64 240 L 158 238", amount=1.8, seed="ol1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 66 256 L 130 255", amount=1.8, seed="ol2")}" stroke-width="{W_DET}"/>')

    # Inside Subagent 1 (Magnifier + search lines):
    mag_handle = handify("M 380 104 L 404 128", amount=1.8, seed="s1-mh")
    mag_lens = drawn_circle(362, 86, 22, seed="s1-ml")
    mag_glint = handify("M 351 78 C 354 71 361 68 369 69", amount=1.0, seed="s1-mg")
    details.append(f'<path d="{mag_handle}" stroke-width="{W_OUT}"/>')
    details.append(f'<path d="{mag_lens}" fill="{PAPER}" stroke-width="{W_CONN}"/>')
    details.append(f'<path d="{mag_glint}" stroke-width="{W_ACC}"/>')
    # Varied search result lines on right of S1
    details.append(f'<path d="{handify("M 406 68 L 456 66", amount=1.6, seed="s1-l1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 408 88 L 444 87", amount=1.6, seed="s1-l2")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 412 108 L 460 106", amount=1.6, seed="s1-l3")}" stroke-width="{W_DET}"/>')

    # Inside Subagent 2 (Git Branch motif + code bars):
    br_main = handify("M 344 206 L 345 274", amount=2.0, seed="s2-bm")
    br_fork = handify("M 345 228 C 366 228 374 244 388 258", amount=1.8, seed="s2-bf")
    n1 = wobbly_circle(344, 206, 8.2, seed="s2-n1")
    n2 = wobbly_circle(345, 274, 8.2, seed="s2-n2")
    n3 = wobbly_circle(388, 258, 8.2, seed="s2-n3")
    details.append(f'<path d="{br_main}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{br_fork}" stroke-width="{W_DET}"/>')
    for nd in (n1, n2, n3):
        details.append(f'<path d="{nd}" fill="{PAPER}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 410 212 L 462 210", amount=1.6, seed="s2-l1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 412 232 L 448 231", amount=1.6, seed="s2-l2")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 410 252 L 464 250", amount=1.6, seed="s2-l3")}" stroke-width="{W_DET}"/>')

    # Inside Subagent 3 (Open Book motif + doc notes):
    bk_left = handify("M 374 358 C 360 352 346 352 336 356 L 335 414 C 346 410 360 410 374 416 Z", amount=1.8, seed="s3-bl")
    bk_right = handify("M 374 358 C 388 352 402 352 412 356 L 413 414 C 402 410 388 410 374 416 Z", amount=1.8, seed="s3-br")
    details.append(f'<path d="{bk_left}" fill="{PAPER}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{bk_right}" fill="{PAPER}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 345 374 L 365 375", amount=1.2, seed="s3-p1")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 346 390 L 362 391", amount=1.2, seed="s3-p2")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 383 375 L 403 374", amount=1.2, seed="s3-p3")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 384 391 L 399 390", amount=1.2, seed="s3-p4")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 428 368 L 468 366", amount=1.5, seed="s3-r1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 430 388 L 458 387", amount=1.5, seed="s3-r2")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 428 408 L 466 406", amount=1.5, seed="s3-r3")}" stroke-width="{W_DET}"/>')

    # Inside Synthesis / PR Card + Paper Plane breaking out of top-right corner:
    # PR header badge & checkmark
    pr_badge = drawn_circle(614, 194, 17, seed="pr-badge")
    pr_check = handify("M 605 194 L 613 202 L 627 184", amount=1.5, seed="pr-chk")
    details.append(f'<path d="{pr_badge}" fill="{COLORS["cactus"][0]}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{pr_check}" stroke-width="{W_CONN}"/>')
    # PR title & diff bars (varied lengths)
    details.append(f'<path d="{handify("M 644 186 L 730 184", amount=1.8, seed="pr-t1")}" stroke-width="{W_CONN}"/>')
    details.append(f'<path d="{handify("M 646 204 L 704 203", amount=1.8, seed="pr-t2")}" stroke-width="{W_DET}"/>')
    # Synthesis merge lines inside PR card
    details.append(f'<path d="{handify("M 596 242 L 728 240", amount=2.0, seed="pr-b1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 598 266 L 710 264", amount=2.0, seed="pr-b2")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 596 290 L 734 288", amount=2.0, seed="pr-b3")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 600 314 L 676 312", amount=2.0, seed="pr-b4")}" stroke-width="{W_DET}"/>')

    # Paper plane motif breaking out across the top-right corner of the PR card (x: 680..776, y: 74..152)
    plane_outer = handify("M 682 122 L 774 82 L 736 154 L 714 132 Z", amount=2.2, seed="plane-out")
    plane_crease = handify("M 772 83 L 714 132 L 706 152", amount=1.8, seed="plane-cr")
    details.append(f'<path d="{plane_outer}" fill="{PAPER}" stroke-width="{W_OUT}"/>')
    details.append(f'<path d="{plane_crease}" stroke-width="{W_DET}"/>')

    # Arrowheads where connectors arrive at cards
    arrows = [
        arrowhead((315, 92), (274, 96), size=14, seed="ah-s1"),
        arrowhead((309, 236), (282, 228), size=14, seed="ah-s2"),
        arrowhead((319, 384), (272, 368), size=14, seed="ah-s3"),
        arrowhead((569, 196), (536, 154), size=14, seed="ah-f1"),
        arrowhead((568, 248), (540, 242), size=14, seed="ah-f2"),
        arrowhead((570, 296), (544, 332), size=14, seed="ah-f3"),
        arrowhead((154, 102), (210, 50), size=13, seed="ah-fb"),
    ]
    for ah in arrows:
        details.append(f'<path d="{ah}" stroke-width="{W_CONN}"/>')

    # --- Accents: 1 cluster of 3 sparkles + 2 dots in the quiet bottom-left area (5 total) ---
    accents = [
        f'<path d="{sparkle(108, 388, 16, seed="sp1")}" stroke-width="{W_ACC}"/>',
        f'<path d="{sparkle(144, 368, 10, seed="sp2")}" stroke-width="{W_ACC}"/>',
        f'<path d="{sparkle(128, 416, 7, seed="sp3")}" stroke-width="{W_ACC}"/>',
        f'<circle cx="84" cy="404" r="3.5" fill="{INK}" stroke="none"/>',
        f'<circle cx="164" cy="396" r="3.0" fill="{INK}" stroke="none"/>',
    ]

    ink_content = "\n  ".join(behind + paper_and_cards + details + accents)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
<defs>
{wash_filter_def("wash-1", 31, scale=13)}
{wash_filter_def("wash-2", 47, scale=13)}
{wash_filter_def("wash-3", 61, scale=12)}
  <filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
    <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="42" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="5.5" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs>
<g id="layer-block" style="isolation: isolate">
  {wash_block(wash_clay, "clay", "wash-1")}
  {wash_block(wash_sky, "sky", "wash-2")}
  {wash_block(wash_focal, "kraft", "wash-3")}
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="{W_OUT}" stroke-linecap="round" stroke-linejoin="round">
  {ink_content}
</g>
</svg>
"""


def build_rag_pipeline_svg():
    """Diagram 2: Document Ingestion -> Vector Index -> Context Synthesis (512x512)."""
    # Stroke weight hierarchy for 512x512:
    #   heavy outlines: 7.8
    #   connectors & secondary frames: 5.4
    #   interior motifs & details: 4.0
    #   fine accents & sparkles: 3.2
    W_OUT = "7.8"
    W_CONN = "5.4"
    W_DET = "4.0"
    W_ACC = "3.2"

    # --- Layer 1: Watercolor washes (warm peach + cool mineral + clay focal patch) ---
    wash_peach = "M 56 64 L 332 48 L 348 294 L 70 310 Z"
    wash_mineral = "M 200 194 L 460 178 L 476 444 L 188 458 Z"
    wash_clay_spot = "M 366 276 L 478 266 L 486 360 L 356 368 Z"

    # --- Layer 2a: Strokes behind paper shapes (pipeline tubes + query feedback arc) ---
    behind = []
    # Main ingestion flow curve from Stage 1 (top-left) into Stage 2 (center vector index)
    pipe_1_to_2a = handify("M 198 118 C 258 118 282 146 286 192", amount=3.2, seed="p12a")
    pipe_1_to_2b = handify("M 186 154 C 232 162 248 178 254 206", amount=3.2, seed="p12b")
    # Retrieval flow curve from Stage 2 (center) into Stage 3 (bottom-right synthesis)
    pipe_2_to_3a = handify("M 318 302 C 334 326 352 336 376 348", amount=3.2, seed="p23a")
    pipe_2_to_3b = handify("M 268 326 C 276 364 294 382 326 392", amount=3.2, seed="p23b")
    # Dashed query lookup arc from Stage 3 up-right back to Stage 2
    query_arc = handify("M 428 332 C 456 236 420 148 338 198", amount=3.5, seed="q-arc")

    for pd in (pipe_1_to_2a, pipe_1_to_2b, pipe_2_to_3a, pipe_2_to_3b):
        behind.append(f'<path d="{pd}" stroke-width="{W_CONN}"/>')
    behind.append(
        f'<path d="{query_arc}" stroke-width="{W_ACC}" stroke-dasharray="10 12"/>'
    )

    # Architectural background guide frame behind Stage 2
    grid_cross_h = handify("M 134 256 L 392 252", amount=3.0, seed="gch")
    grid_cross_v = handify("M 264 136 L 260 374", amount=3.0, seed="gcv")
    behind.append(f'<path d="{grid_cross_h}" stroke-width="{W_ACC}" stroke-dasharray="7 11"/>')
    behind.append(f'<path d="{grid_cross_v}" stroke-width="{W_ACC}" stroke-dasharray="7 11"/>')

    # --- Layer 2b: Paper shapes (back to front) ---
    paper_shapes = []

    # Stage 1: Document Ingestion Card (top-left, breaking out left & top of peach wash)
    doc_back_d, _ = card_path(24, 46, 174, 134, amount=3.6, seed="doc-bg")
    paper_shapes.append(f'<path d="{doc_back_d}" fill="{PAPER}" stroke-width="{W_CONN}"/>')
    doc_d, doc_pts = card_path(38, 32, 176, 136, amount=3.8, seed="doc-fg")
    paper_shapes.append(f'<path d="{doc_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>')
    paper_shapes.append(
        f'<path d="{corner_overshoot(doc_pts, (0, 2), overshoot=10, seed="doc-ov")}" stroke-width="{W_CONN}"/>'
    )

    # Floating chunk cards slicing off Stage 1 into Stage 2
    chunk1_d, _ = card_path(228, 86, 52, 36, amount=2.2, seed="chk1")
    chunk2_d, _ = card_path(254, 134, 56, 38, amount=2.2, seed="chk2")
    paper_shapes.append(f'<path d="{chunk1_d}" fill="{PAPER}" stroke-width="{W_DET}"/>')
    paper_shapes.append(f'<path d="{chunk2_d}" fill="{PAPER}" stroke-width="{W_DET}"/>')

    # Stage 2: Vector Index Manifold (center, sitting on the peach+mineral glaze)
    vec_ring_d = drawn_circle(254, 256, 76, seed="vec-ring", wobble=0.06)
    paper_shapes.append(f'<path d="{vec_ring_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>')

    # Stage 3: Context Synthesis Card (bottom-right, breaking out bottom-right of mineral wash)
    syn_back_d, _ = card_path(294, 342, 188, 142, amount=3.6, seed="syn-bg")
    paper_shapes.append(f'<path d="{syn_back_d}" fill="{PAPER}" stroke-width="{W_CONN}"/>')
    syn_d, syn_pts = card_path(278, 326, 192, 144, amount=3.8, seed="syn-fg")
    paper_shapes.append(f'<path d="{syn_d}" fill="{PAPER}" stroke-width="{W_OUT}"/>')
    paper_shapes.append(
        f'<path d="{corner_overshoot(syn_pts, (1, 3), overshoot=10, seed="syn-ov")}" stroke-width="{W_CONN}"/>'
    )

    # --- Layer 3: Details on top of paper & foreground elements ---
    details = []

    # Inside Stage 1 (Open book + raw document lines + chunk cut marks):
    bk_l = handify("M 102 60 C 86 53 68 53 56 58 L 55 132 C 68 127 86 127 102 134 Z", amount=1.8, seed="r-bkl")
    bk_r = handify("M 102 60 C 118 53 136 53 148 58 L 149 132 C 136 127 118 127 102 134 Z", amount=1.8, seed="r-bkr")
    details.append(f'<path d="{bk_l}" fill="{PAPER}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{bk_r}" fill="{PAPER}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 68 78 L 91 80", amount=1.2, seed="r-bl1")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 67 96 L 88 97", amount=1.2, seed="r-bl2")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 114 80 L 137 78", amount=1.2, seed="r-br1")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 115 97 L 134 96", amount=1.2, seed="r-br2")}" stroke-width="{W_ACC}"/>')
    # Chunking bars on right side of Stage 1 card
    details.append(f'<path d="{handify("M 164 66 L 198 65", amount=1.5, seed="r-c1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 166 88 L 192 87", amount=1.5, seed="r-c2")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 164 110 L 200 109", amount=1.5, seed="r-c3")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 166 132 L 188 131", amount=1.5, seed="r-c4")}" stroke-width="{W_DET}"/>')

    # Inside floating chunks: tiny embedding ticks
    details.append(f'<path d="{handify("M 238 104 L 268 103", amount=1.2, seed="chk1-l")}" stroke-width="{W_ACC}"/>')
    details.append(f'<path d="{handify("M 264 153 L 298 152", amount=1.2, seed="chk2-l")}" stroke-width="{W_ACC}"/>')

    # Inside Stage 2 (Vector Index constellation + PAPER-filled similarity magnifier lens in front):
    vec_edges = [
        handify("M 206 226 L 248 206 L 244 256 L 216 282 Z", amount=2.0, seed="ve-loop"),
        handify("M 248 206 L 288 232 L 244 256", amount=1.8, seed="ve-mid1"),
    ]
    for ve in vec_edges:
        details.append(f'<path d="{ve}" stroke-width="{W_ACC}"/>')

    # Background embedding nodes inside the vector drum (r <= 6.2 so mext < 15.3)
    for idx, (nx, ny, nr) in enumerate([
        (206, 226, 6.0),
        (248, 206, 6.2),
        (216, 282, 6.0),
        (244, 256, 6.2),
    ]):
        nd = wobbly_circle(nx, ny, nr, seed=f"vn-{idx}")
        details.append(f'<path d="{nd}" fill="{PAPER}" stroke-width="{W_DET}"/>')

    # Magnifier lens with PAPER fill overlapping lower-right of the vector drum (3rd plane depth!)
    mag_handle = handify("M 318 272 L 358 308", amount=2.0, seed="rag-mh")
    mag_ring = drawn_circle(288, 244, 38, seed="rag-mr", wobble=0.06)
    details.append(f'<path d="{mag_handle}" stroke-width="{W_OUT}"/>')
    details.append(f'<path d="{mag_ring}" fill="{PAPER}" stroke-width="{W_CONN}"/>')
    # Zoomed-in similarity match inside the magnifier lens: clay query node + sky match node + link
    zoom_edge = handify("M 272 236 L 302 252", amount=1.5, seed="zm-e")
    zoom_n1 = wobbly_circle(272, 236, 6.2, seed="zm-n1")
    zoom_n2 = wobbly_circle(302, 252, 6.4, seed="zm-n2")
    mag_glint = handify("M 268 220 C 274 213 284 211 294 214", amount=1.0, seed="rag-mg")
    details.append(f'<path d="{zoom_edge}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{zoom_n1}" fill="{COLORS["clay"][0]}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{zoom_n2}" fill="{COLORS["sky"][0]}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{mag_glint}" stroke-width="{W_ACC}"/>')

    # Inside Stage 3 (Context Synthesis window: header dots, retrieved context quotes, Claude starburst):
    syn_div = handify("M 282 358 L 452 360", amount=2.0, seed="syn-div")
    details.append(f'<path d="{syn_div}" stroke-width="{W_DET}"/>')
    details.append(f'<circle cx="298" cy="343" r="4.0" fill="{INK}" stroke="none"/>')
    details.append(f'<circle cx="314" cy="342" r="4.0" fill="{INK}" stroke="none"/>')

    # Left side of Synthesis card: retrieved context quote block + lines
    quote_bar = handify("M 298 378 L 297 444", amount=1.6, seed="syn-qb")
    details.append(f'<path d="{quote_bar}" stroke-width="{W_CONN}"/>')
    details.append(f'<path d="{handify("M 312 384 L 368 382", amount=1.6, seed="syn-l1")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 314 404 L 356 403", amount=1.6, seed="syn-l2")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 312 424 L 374 422", amount=1.6, seed="syn-l3")}" stroke-width="{W_DET}"/>')
    details.append(f'<path d="{handify("M 314 444 L 348 443", amount=1.6, seed="syn-l4")}" stroke-width="{W_DET}"/>')

    # Right side of Synthesis card: asymmetric warm clay highlight patch + 7-ray Claude starburst
    syn_spot = handify("M 398 394 C 412 382 438 384 446 400 C 452 418 440 438 420 440 C 400 441 390 424 394 406 Z", amount=1.8, seed="syn-spot")
    details.append(f'<path d="{syn_spot}" fill="{COLORS["clay"][0]}" stroke="none"/>')
    details.append(f'<path d="{starburst_rays(422, 412, 8, 30, seed="syn-star")}" stroke-width="{W_DET}"/>')

    # Arrowheads along the pipeline
    for ah in [
        arrowhead((286, 190), (282, 146), size=13, seed="rag-ah1"),
        arrowhead((326, 392), (294, 382), size=13, seed="rag-ah2"),
        arrowhead((336, 198), (384, 172), size=12, seed="rag-ah3"),
    ]:
        details.append(f'<path d="{ah}" stroke-width="{W_CONN}"/>')

    # --- Accents: 1 cluster of 3 sparkles + 2 dots in the quiet bottom-left area (5 total) ---
    accents = [
        f'<path d="{sparkle(86, 382, 15, seed="rsp1")}" stroke-width="{W_ACC}"/>',
        f'<path d="{sparkle(122, 362, 9.5, seed="rsp2")}" stroke-width="{W_ACC}"/>',
        f'<path d="{sparkle(104, 412, 6.5, seed="rsp3")}" stroke-width="{W_ACC}"/>',
        f'<circle cx="66" cy="398" r="3.4" fill="{INK}" stroke="none"/>',
        f'<circle cx="138" cy="394" r="3.0" fill="{INK}" stroke="none"/>',
    ]

    ink_content = "\n  ".join(behind + paper_shapes + details + accents)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<defs>
{wash_filter_def("wash-1", 19, scale=13)}
{wash_filter_def("wash-2", 37, scale=13)}
{wash_filter_def("wash-3", 53, scale=12)}
  <filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
    <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="29" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="6.0" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs>
<g id="layer-block" style="isolation: isolate">
  {wash_block(wash_peach, "peach", "wash-1")}
  {wash_block(wash_mineral, "mineral", "wash-2")}
  {wash_block(wash_clay_spot, "clay", "wash-3")}
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="{W_OUT}" stroke-linecap="round" stroke-linejoin="round">
  {ink_content}
</g>
</svg>
"""


def main():
    os.makedirs(HERE, exist_ok=True)
    orch_path = os.path.join(HERE, "agent-orchestration.svg")
    rag_path = os.path.join(HERE, "rag-pipeline.svg")

    with open(orch_path, "w") as f:
        f.write(build_agent_orchestration_svg())
    print(f"Wrote {orch_path}")

    with open(rag_path, "w") as f:
        f.write(build_rag_pipeline_svg())
    print(f"Wrote {rag_path}")


if __name__ == "__main__":
    main()
