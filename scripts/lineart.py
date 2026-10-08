#!/usr/bin/env python3
"""Ink + watercolor line art: black ink strokes over a watercolor block, as SVG.

Commands:
  list                         motifs in the library
  palette                      brand colors
  suggest TEXT                 rank motifs by keyword overlap with TEXT
  render MOTIF -o OUT.svg      MOTIF is a library name or a motif .json path
  preview SVG... -o SHEET.png  render at 256px and 28px side by side (needs rsvg-convert, magick)
  add DRAFT.json               validate a drawn motif and save it into the library
  t3-icon MOTIF --project NAME write a sidebar-sized icon for a T3 project, print its absolute path
  assigned                     project -> motif/color map of icons made with t3-icon
  handify "PATH_D"             roughen a geometric path so it reads as drawn by hand
  circle CX CY R               a hand-drawn circle as path data (uneven radius, visible seam)
  sparkle X Y R                a hand-drawn sparkle: two crossing strokes, unequal arms, tilted
  lint SVG                     measure an SVG against the style rules (needs Pillow for raster checks)
"""
import argparse
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTIF_DIR = os.path.join(SKILL_DIR, "motifs")
# Optional T3 Code sidebar-icon output. Override with CC_LINEART_T3_ASSETS.
T3_ASSETS = os.path.expanduser(
    os.environ.get("CC_LINEART_T3_ASSETS", "~/.t3/userdata/theme-assets/claude-watercolor")
)
PROJECT_ICON_DIR = os.path.join(T3_ASSETS, "projects")
INDEX_PATH = os.path.join(PROJECT_ICON_DIR, "index.json")

INK = "#141413"
PAPER = "#FAF9F5"
# fill, edge (the darker rim watercolor pools into)
COLORS = {
    "clay": ("#D97757", "#B85C3E"),
    "sky": ("#6A9BCC", "#4C7FB3"),
    "cactus": ("#BCD1CA", "#93B0A6"),
    "heather": ("#CBCADB", "#A4A2BF"),
    "plum": ("#827DBD", "#635DA3"),
    "mineral": ("#629987", "#4A7D6C"),
    "peach": ("#EBC9B7", "#D3A58D"),
    "kraft": ("#D4A27F", "#B9845F"),
    "olive": ("#788C5D", "#5D7046"),
}
# lg: detailed, for galleries and anything >= 48px. sm: the 14px T3 sidebar slot.
SIZES = {
    "lg": {"stroke": 3.2, "wash_alpha": "-1.1 1.45", "block_scale": 1.0, "ink_wobble": 1.5},
    "sm": {"stroke": 4.3, "wash_alpha": "-0.45 1.3", "block_scale": 1.14, "ink_wobble": 1.2},
}
ALLOWED_TAGS = {"path", "circle", "ellipse", "line", "polyline", "polygon", "rect", "g"}


def load_motif(ref):
    path = ref if ref.endswith(".json") else os.path.join(MOTIF_DIR, f"{ref}.json")
    if not os.path.exists(path):
        sys.exit(f"no motif '{ref}'. Run `lineart.py list`.")
    with open(path) as f:
        return json.load(f)


def all_motifs():
    return [load_motif(os.path.join(MOTIF_DIR, n)) for n in sorted(os.listdir(MOTIF_DIR)) if n.endswith(".json")]


def validate(m):
    for key in ("name", "description", "tags", "color", "block", "ink"):
        if key not in m:
            sys.exit(f"motif missing '{key}'")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", m["name"]):
        sys.exit("name must be lowercase letters, digits, hyphens")
    if m["color"] not in COLORS:
        sys.exit(f"color must be one of {', '.join(COLORS)}")
    tags = set(re.findall(r"<\s*([a-zA-Z]+)", m["ink"]))
    if not tags <= ALLOWED_TAGS:
        sys.exit(f"ink may only use {sorted(ALLOWED_TAGS)}; found {sorted(tags - ALLOWED_TAGS)}")
    if re.search(r"\b(on\w+|href|style)\s*=", m["ink"]):
        sys.exit("ink must not carry event handlers, hrefs or style attributes")
    if "{PAPER}" not in m["ink"]:
        print("warning: no {PAPER} fill — the style needs at least one paper-white shape over the block", file=sys.stderr)


def build_svg(m, color=None, size="lg", seed_key=None):
    fill, edge = COLORS[color or m["color"]]
    p = SIZES[size]
    seed = int(hashlib.sha1((seed_key or m["name"]).encode()).hexdigest(), 16) % 97
    ink = m["ink"].replace("{PAPER}", PAPER).replace("{INK}", INK)
    block = m["block"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
<defs>
<filter id="wash" x="-8%" y="-8%" width="116%" height="116%">
<feTurbulence type="fractalNoise" baseFrequency="0.07" numOctaves="3" seed="{seed}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 {p["wash_alpha"]}" result="a"/>
<feComposite in="d" in2="a" operator="in"/>
</filter>
<filter id="ink" x="-8%" y="-8%" width="116%" height="116%">
<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed + 11}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="{p["ink_wobble"]}" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>
<g id="layer-block" filter="url(#wash)"><g transform="translate(32 32) scale({p["block_scale"]}) translate(-32 -32)">
<path d="{block}" fill="{fill}"/>
<path d="{block}" fill="none" stroke="{edge}" stroke-width="1.4" stroke-opacity="0.55" stroke-linejoin="round"/>
</g></g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="{p["stroke"]}" stroke-linecap="round" stroke-linejoin="round">
{ink}
</g>
</svg>
"""


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "project"


# ---------------------------------------------------------------- path geometry

PATH_TOKEN = re.compile(r"[MLHVCSQTAZmlhvcsqtaz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
ARITY = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


def parse_path(d):
    """Path data -> subpaths of absolute segments.

    Segments: ("M", p) ("L", p) ("C", c1, c2, p) ("Q", c, p) ("A", (rx, ry, rot, large, sweep), p) ("Z",).
    H/V become L, S/T become C/Q with reflected controls, relative commands become absolute.
    """
    tokens = PATH_TOKEN.findall(d)
    subpaths, segs = [], []
    cur = start = (0.0, 0.0)
    last_c = last_q = None
    cmd, i = None, 0
    while i < len(tokens):
        if tokens[i].isalpha():
            cmd = tokens[i]
            i += 1
            if cmd in "Zz":
                segs.append(("Z",))
                cur, last_c, last_q = start, None, None
                continue
        elif cmd is None:
            raise ValueError("path must start with a command")
        n = ARITY[cmd.upper()]
        args = [float(t) for t in tokens[i:i + n]]
        if len(args) < n:
            raise ValueError(f"not enough numbers for {cmd}")
        i += n
        rel = cmd.islower()
        up = cmd.upper()

        def pt(x, y):
            return (cur[0] + x, cur[1] + y) if rel else (x, y)

        if up == "M":
            if segs:
                subpaths.append(segs)
            p = pt(*args)
            segs, cur, start = [("M", p)], p, p
            cmd = "l" if rel else "L"  # extra pairs after M are lineto
            last_c = last_q = None
            continue
        if up == "L":
            p = pt(*args)
            segs.append(("L", p))
        elif up == "H":
            p = (cur[0] + args[0], cur[1]) if rel else (args[0], cur[1])
            segs.append(("L", p))
        elif up == "V":
            p = (cur[0], cur[1] + args[0]) if rel else (cur[0], args[0])
            segs.append(("L", p))
        elif up == "C":
            c1, c2, p = pt(*args[0:2]), pt(*args[2:4]), pt(*args[4:6])
            segs.append(("C", c1, c2, p))
            last_c = c2
        elif up == "S":
            c1 = (2 * cur[0] - last_c[0], 2 * cur[1] - last_c[1]) if last_c else cur
            c2, p = pt(*args[0:2]), pt(*args[2:4])
            segs.append(("C", c1, c2, p))
            last_c = c2
        elif up == "Q":
            c, p = pt(*args[0:2]), pt(*args[2:4])
            segs.append(("Q", c, p))
            last_q = c
        elif up == "T":
            c = (2 * cur[0] - last_q[0], 2 * cur[1] - last_q[1]) if last_q else cur
            p = pt(*args)
            segs.append(("Q", c, p))
            last_q = c
        elif up == "A":
            p = pt(*args[5:7])
            segs.append(("A", tuple(args[0:5]), p))
        if up not in "CS":
            last_c = None
        if up not in "QT":
            last_q = None
        cur = segs[-1][-1]
    if segs:
        subpaths.append(segs)
    return subpaths


def path_points(subpaths):
    """Every endpoint and control point, a cheap stand-in for the outline."""
    pts = []
    for segs in subpaths:
        for s in segs:
            if s[0] == "A":
                pts.append(s[2])
            elif s[0] != "Z":
                pts.extend(s[1:])
    return pts


def fmt(p):
    return f"{p[0]:.1f} {p[1]:.1f}"


def handify(d, amount=0.8, overshoot=0.0, seed="sketch"):
    """Make a geometric path read as hand-drawn.

    amount is in path units (0.8 suits a 64 grid, 6 a 512 grid). Straight segments become
    shallow arcs, every point drifts a little, and with overshoot > 0 the corners of open
    polylines are drawn as separate strokes that run slightly past each other.
    """
    rng = random.Random(seed)

    def jitter(p, k=0.5):
        return (p[0] + rng.uniform(-1, 1) * amount * k, p[1] + rng.uniform(-1, 1) * amount * k)

    def bowed(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length, dx / length
        bow = rng.choice((-1, 1)) * rng.uniform(0.35, 1.0) * min(amount * 1.4, length * 0.03)
        c1 = (a[0] + dx / 3 + nx * bow * rng.uniform(0.7, 1.2), a[1] + dy / 3 + ny * bow * rng.uniform(0.7, 1.2))
        c2 = (a[0] + 2 * dx / 3 + nx * bow * rng.uniform(0.7, 1.2), a[1] + 2 * dy / 3 + ny * bow * rng.uniform(0.7, 1.2))
        return c1, c2

    out = []
    for segs in parse_path(d):
        closed = any(s[0] == "Z" for s in segs)
        lines_only = all(s[0] in ("M", "L") for s in segs)
        if overshoot > 0 and not closed and lines_only and len(segs) > 2:
            pts = [jitter(s[1]) for s in segs]
            for a, b in zip(pts, pts[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                length = math.hypot(dx, dy) or 1.0
                ux, uy = dx / length, dy / length
                e0, e1 = overshoot * rng.uniform(0.4, 1.1), overshoot * rng.uniform(0.4, 1.1)
                a2, b2 = (a[0] - ux * e0, a[1] - uy * e0), (b[0] + ux * e1, b[1] + uy * e1)
                c1, c2 = bowed(a2, b2)
                out.append(f"M{fmt(a2)} C{fmt(c1)} {fmt(c2)} {fmt(b2)}")
            continue
        parts, cur = [], None
        for s in segs:
            if s[0] == "M":
                cur = jitter(s[1])
                parts.append(f"M{fmt(cur)}")
            elif s[0] == "L":
                p = jitter(s[1])
                c1, c2 = bowed(cur, p)
                parts.append(f"C{fmt(c1)} {fmt(c2)} {fmt(p)}")
                cur = p
            elif s[0] == "C":
                c1, c2, p = jitter(s[1], 0.6), jitter(s[2], 0.6), jitter(s[3])
                parts.append(f"C{fmt(c1)} {fmt(c2)} {fmt(p)}")
                cur = p
            elif s[0] == "Q":
                c, p = jitter(s[1], 0.6), jitter(s[2])
                parts.append(f"Q{fmt(c)} {fmt(p)}")
                cur = p
            elif s[0] == "A":
                p = jitter(s[2])
                rx, ry, rot, large, sweep = s[1]
                parts.append(f"A{rx:.1f} {ry:.1f} {rot:.0f} {int(large)} {int(sweep)} {fmt(p)}")
                cur = p
            else:
                parts.append("Z")
        out.append(" ".join(parts))
    return " ".join(out)


def wobbly_circle(cx, cy, r, seed="circle", wobble=0.05, overlap=14):
    """A circle the way a hand draws one: the radius drifts, and the stroke runs
    `overlap` degrees past its start so the seam shows. Filled, it still closes."""
    rng = random.Random(f"{seed}:{cx}:{cy}:{r}")
    start = rng.uniform(0, 360)
    knots = 5
    sweep = 360 + overlap
    step = sweep / knots
    radii = [r * (1 + rng.uniform(-wobble, wobble)) for _ in range(knots + 1)]
    radii[-1] = radii[0] * (1 + rng.choice((-1, 1)) * wobble * 0.8)  # the overlap lands off the start
    def at(i):
        a = math.radians(start + i * step)
        return a, (cx + radii[i] * math.cos(a), cy + radii[i] * math.sin(a))
    k = 4 / 3 * math.tan(math.radians(step) / 4)
    a0, p0 = at(0)
    parts = [f"M{fmt(p0)}"]
    for i in range(knots):
        a, p = at(i)
        b, q = at(i + 1)
        c1 = (p[0] - k * radii[i] * math.sin(a), p[1] + k * radii[i] * math.cos(a))
        c2 = (q[0] + k * radii[i + 1] * math.sin(b), q[1] - k * radii[i + 1] * math.cos(b))
        parts.append(f"C{fmt(c1)} {fmt(c2)} {fmt(q)}")
    return " ".join(parts)


def sparkle(x, y, r, seed="sparkle"):
    """Two crossing strokes with unequal arms, a tilt, and a slight bow: never a perfect +."""
    rng = random.Random(f"{seed}:{x}:{y}:{r}")
    tilt = math.radians(rng.uniform(-14, 14))
    out = []
    for axis in (0, 90):
        a = tilt + math.radians(axis)
        ux, uy = math.cos(a), math.sin(a)
        back, fwd = r * rng.uniform(0.5, 0.75), r * rng.uniform(0.95, 1.2)
        if axis:
            back, fwd = back * 1.15, fwd * 1.1  # the vertical stroke is the longer one
        p0 = (x - ux * back, y - uy * back)
        p1 = (x + ux * fwd, y + uy * fwd)
        bow = r * rng.uniform(0.06, 0.14) * rng.choice((-1, 1))
        mid = ((p0[0] + p1[0]) / 2 - uy * bow, (p0[1] + p1[1]) / 2 + ux * bow)
        out.append(f"M{fmt(p0)} Q{fmt(mid)} {fmt(p1)}")
    return " ".join(out)


# ---------------------------------------------------------------- lint

SHAPE_TAG = re.compile(r"<(path|circle|ellipse|rect|line|polyline|polygon)\b([^>]*?)/?>", re.S)
ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')


def element_points(tag, attrs):
    num = lambda k, default=0.0: float(attrs.get(k, default))  # noqa: E731
    if tag == "path":
        return parse_path(attrs.get("d", ""))
    if tag in ("circle", "ellipse"):
        cx, cy = num("cx"), num("cy")
        rx = num("r") if tag == "circle" else num("rx")
        ry = num("r") if tag == "circle" else num("ry")
        return [[("M", (cx - rx, cy - ry)), ("L", (cx + rx, cy + ry))]]
    if tag == "rect":
        x, y, w, h = num("x"), num("y"), num("width"), num("height")
        return [[("M", (x, y)), ("L", (x + w, y)), ("L", (x + w, y + h)), ("L", (x, y + h)), ("Z",)]]
    if tag == "line":
        return [[("M", (num("x1"), num("y1"))), ("L", (num("x2"), num("y2")))]]
    nums = [float(v) for v in re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)", attrs.get("points", ""))]
    pts = list(zip(nums[0::2], nums[1::2]))
    return [[("M", pts[0])] + [("L", p) for p in pts[1:]]] if pts else []


def marks(subpaths, gap=0.0):
    """Group subpaths into visual marks: a "+" is two subpaths whose boxes touch,
    a starburst is seven rays whose boxes come within `gap` of each other."""
    groups = []
    for segs in subpaths:
        pts = path_points([segs])
        if not pts:
            continue
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        if groups:
            g = groups[-1]
            b = g["box"]
            if box[0] <= b[2] + gap and box[2] >= b[0] - gap and box[1] <= b[3] + gap and box[3] >= b[1] - gap:
                g["pts"] += pts
                g["box"] = (min(b[0], box[0]), min(b[1], box[1]), max(b[2], box[2]), max(b[3], box[3]))
                continue
        groups.append({"pts": pts, "box": box})
    return [g["pts"] for g in groups]


def mirror_symmetric(pts, tol):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx = (min(xs) + max(xs)) / 2
    return all(min(math.hypot((2 * cx - x) - x2, y - y2) for x2, y2 in pts) < tol for x, y in pts)


def source_checks(svg):
    """Heuristics on the markup itself: the tells of clip-art geometry."""
    m = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)', svg)
    size = float(m.group(1)) if m else 64.0
    body = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.S)
    ink_at = body.find('id="layer-ink"')
    if ink_at >= 0:
        body = body[ink_at:]  # the wash is displaced by its filter; judge only the line art
    findings = []
    perfect, straight, symmetric, widths, total = [], 0, 0, set(), 0
    tiny, frames = [], []
    for tag, raw in SHAPE_TAG.findall(body):
        attrs = dict(ATTR.findall(raw))
        if "stroke-width" in attrs:
            widths.add(attrs["stroke-width"])
        try:
            subpaths = element_points(tag, attrs)
        except (ValueError, IndexError):
            continue
        pts = path_points(subpaths)
        if not pts:
            continue
        total += 1
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        extent = max(max(xs) - min(xs), max(ys) - min(ys))
        if tag in ("circle", "ellipse") and extent >= 0.12 * size and attrs.get("stroke") != "none":
            perfect.append(f"{tag} ~{extent:.0f} wide")
        for mk in marks(subpaths, 0.03 * size):
            mx, my = [p[0] for p in mk], [p[1] for p in mk]
            mext = max(max(mx) - min(mx), max(my) - min(my))
            if mext < 0.07 * size:
                tiny.append(((min(mx) + max(mx)) / 2, (min(my) + max(my)) / 2))
            else:
                frames.append((min(mx), min(my), max(mx), max(my)))
            thin = min(max(mx) - min(mx), max(my) - min(my)) < 0.15 * mext  # a line, not a shape
            if (0.03 * size < mext < 0.3 * size and len(mk) >= 4 and not thin
                    and mirror_symmetric(mk, max(0.08 * mext, 0.004 * size))):
                symmetric += 1
        for segs in subpaths:
            prev = None
            for s in segs:
                if s[0] == "L" and prev is not None:
                    dx, dy = s[1][0] - prev[0], s[1][1] - prev[1]
                    if (abs(dx) < 1e-6 or abs(dy) < 1e-6) and math.hypot(dx, dy) > 0.12 * size:
                        straight += 1
                if s[0] != "Z":
                    prev = s[-1] if s[0] != "A" else s[2]
    if perfect:
        findings.append(("warn", f"perfect geometric outlines: {', '.join(perfect[:4])} — draw them as paths and handify"))
    if straight:
        findings.append(("warn", f"{straight} ruler-straight horizontal/vertical segment(s) longer than 12% of the canvas — bow them (handify)"))
    if symmetric:
        findings.append(("warn", f"{symmetric} mirror-symmetric mark(s) — clip-art tell; skew one side, vary the arms"))
    if size >= 256 and total > 5 and len(widths) <= 1:
        findings.append(("warn", "every stroke has the same weight — give outlines, details and accents different widths"))
    # letters inside a window or rays inside a bubble are detail, not confetti
    free = [c for c in tiny if not any(b[0] <= c[0] <= b[2] and b[1] <= c[1] <= b[3] for b in frames)]
    # the two arms of a sparkle drawn as separate elements are still one mark
    small = sum(1 for i, c in enumerate(free)
                if not any(math.hypot(c[0] - d[0], c[1] - d[1]) < 0.03 * size for d in free[:i]))
    if small > 7:
        findings.append(("warn", f"{small} tiny marks — reads as confetti; keep 3–6, clustered"))
    if not findings:
        findings.append(("ok", "no clip-art geometry found in the markup"))
    return findings


def holes(pixels, px, min_area):
    """Count connected non-ink regions (paper or wash) at least min_area pixels big."""
    light = [sum(c) / 3 >= 100 for c in pixels]
    seen = [False] * len(light)
    count = 0
    for i, ok in enumerate(light):
        if seen[i] or not ok:
            continue
        stack, area = [i], 0
        seen[i] = True
        while stack:
            j = stack.pop()
            area += 1
            x = j % px
            for k in (j - 1 if x > 0 else -1, j + 1 if x < px - 1 else -1, j - px, j + px):
                if 0 <= k < len(light) and light[k] and not seen[k]:
                    seen[k] = True
                    stack.append(k)
        count += area >= min_area
    return count


def raster_checks(svg_path, svg):
    if 'id="layer-block"' not in svg or 'id="layer-ink"' not in svg:
        return [("note", 'wrap the wash in <g id="layer-block"> and the line art in <g id="layer-ink"> to enable raster checks')]
    try:
        from PIL import Image
    except ImportError:
        return [("note", "raster checks need Pillow (pip install pillow)")]
    if not shutil.which("rsvg-convert"):
        return [("note", "raster checks need rsvg-convert")]
    tmp = tempfile.mkdtemp()

    def render(hide, px):
        src = svg
        if hide:
            src = src.replace("</svg>", f"<style>#{hide}{{display:none}}</style></svg>")
        path = os.path.join(tmp, f"{hide or 'full'}-{px}.svg")
        with open(path, "w") as f:
            f.write(src)
        out = path.replace(".svg", ".png")
        subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), "-b", PAPER, path, "-o", out], check=True)
        img = Image.open(out).convert("RGB")
        raw = img.tobytes()
        return [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]

    paper = tuple(int(PAPER[i:i + 2], 16) for i in (1, 3, 5))
    off_paper = lambda c: sum(abs(a - b) for a, b in zip(c, paper)) > 45  # noqa: E731
    dark = lambda c: sum(c) / 3 < 70  # noqa: E731
    full, block_only, ink_only = render(None, 160), render("layer-ink", 160), render("layer-block", 160)
    n = len(full)
    block = [off_paper(c) for c in block_only]
    block_px = sum(block) or 1
    visible = sum(1 for i in range(n) if block[i] and off_paper(full[i]) and not dark(full[i]))
    ink = [dark(c) for c in ink_only]
    ink_px = sum(ink) or 1
    ink_on_block = sum(1 for i in range(n) if ink[i] and block[i])
    big_holes = holes(render(None, 168), 168, 72)
    small_holes = holes(render(None, 28), 28, 2)

    findings = []
    vis, cover, inside = visible / block_px, visible / n, ink_on_block / ink_px
    findings.append(("warn" if vis < 0.3 else "ok", f"block visible: {vis:.0%} of the wash shows (want ≥ 30%)"))
    findings.append(("warn" if not 0.1 <= cover <= 0.5 else "ok",
                     f"color coverage: {cover:.0%} of the canvas (want 10–50%; above that the wash turns into a background plate)"))
    findings.append(("warn" if inside > 0.8 else "ok",
                     f"line art over the wash: {inside:.0%} (want ≤ 80%; the art should break out of the block)"))
    m = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)', svg)
    is_icon = (float(m.group(1)) if m else 64) < 256
    lost = big_holes - small_holes
    if lost > max(1, big_holes * 0.4):
        level = "warn" if is_icon else "note"
        findings.append((level, f"at 28px {lost} of {big_holes} enclosed paper areas close up — the drawing smudges; "
                                "fewer, bigger shapes" + ("" if is_icon else " (fine if this piece is never shown that small)")))
    else:
        findings.append(("ok", f"at 28px the paper areas survive ({big_holes} -> {small_holes})"))
    return findings


def cmd_list(_):
    for m in all_motifs():
        print(f"{m['name']:<12} {m['color']:<8} {m['description']}  [{' '.join(m['tags'])}]")


def cmd_palette(_):
    for name, (fill, edge) in COLORS.items():
        print(f"{name:<8} {fill}  rim {edge}")
    print(f"ink      {INK}\npaper    {PAPER}")


def cmd_suggest(a):
    words = set(re.findall(r"[a-z0-9]+", a.text.lower()))
    scored = []
    for m in all_motifs():
        vocab = set(m["tags"]) | {m["name"]}
        # Substring matches only between longer words, so "ui" does not hit "build".
        hits = sum(1 for w in words for v in vocab
                   if w == v or (len(w) > 3 and len(v) > 3 and (w in v or v in w)))
        scored.append((hits, m["name"], m["description"]))
    for hits, name, desc in sorted(scored, key=lambda s: -s[0])[:5]:
        print(f"{hits}  {name:<12} {desc}")
    if not any(s[0] for s in scored):
        print("no keyword match: pick by meaning, or draw a new motif (see SKILL.md)")


def cmd_render(a):
    m = load_motif(a.motif)
    validate(m)
    with open(a.out, "w") as f:
        f.write(build_svg(m, a.color, a.size, a.seed))
    print(os.path.abspath(a.out))


def cmd_preview(a):
    for tool in ("rsvg-convert", "magick"):
        if not shutil.which(tool):
            sys.exit(f"preview needs {tool} (brew install librsvg imagemagick)")
    tmp = tempfile.mkdtemp()
    rows = []
    for i, svg in enumerate(a.svgs):
        big, small = f"{tmp}/{i}-b.png", f"{tmp}/{i}-s.png"
        subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", "-b", PAPER, svg, "-o", big], check=True)
        subprocess.run(["rsvg-convert", "-w", "28", "-h", "28", "-b", "#F3F1EA", svg, "-o", small], check=True)
        # 28px is the real 14pt sidebar slot on a 2x display; upscale it blocky so it can be judged.
        subprocess.run(["magick", small, "-filter", "point", "-resize", "400%", "-gravity", "center",
                        "-background", "#F3F1EA", "-extent", "128x256", small], check=True)
        row = f"{tmp}/{i}.png"
        subprocess.run(["magick", big, small, "+append", row], check=True)
        rows.append(row)
    subprocess.run(["magick", *rows, "+append", a.out], check=True)
    print(os.path.abspath(a.out))


def cmd_add(a):
    with open(a.draft) as f:
        m = json.load(f)
    validate(m)
    dest = os.path.join(MOTIF_DIR, f"{m['name']}.json")
    if os.path.exists(dest) and not a.force:
        sys.exit(f"motif '{m['name']}' exists; pass --force to replace it")
    with open(dest, "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print(dest)


def read_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH) as f:
            return json.load(f)
    return {}


def cmd_t3_icon(a):
    m = load_motif(a.motif)
    validate(m)
    color = a.color or m["color"]
    os.makedirs(PROJECT_ICON_DIR, exist_ok=True)
    slug = slugify(a.project)
    out = os.path.join(PROJECT_ICON_DIR, f"{slug}.svg")
    with open(out, "w") as f:
        f.write(build_svg(m, color, "sm", seed_key=slug))
    with open(os.path.join(PROJECT_ICON_DIR, f"{slug}-lg.svg"), "w") as f:
        f.write(build_svg(m, color, "lg", seed_key=slug))
    index = read_index()
    index[a.project] = {"motif": m["name"], "color": color, "file": out}
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(out)


def cmd_handify(a):
    print(handify(a.d, a.amount, a.overshoot, a.seed))


def cmd_circle(a):
    print(wobbly_circle(a.cx, a.cy, a.r, a.seed, a.wobble))


def cmd_sparkle(a):
    print(sparkle(a.x, a.y, a.r, a.seed))


def cmd_lint(a):
    with open(a.svg) as f:
        svg = f.read()
    findings = source_checks(svg) + raster_checks(a.svg, svg)
    for level, msg in findings:
        print(f"{level.upper():<5} {msg}")
    warns = sum(1 for level, _ in findings if level == "warn")
    print(f"\n{warns} warning(s). Lint catches mechanical tells only; it cannot tell you the piece is good.")


def cmd_assigned(_):
    index = read_index()
    if not index:
        print("no icons recorded yet")
    counts = {}
    for project, info in index.items():
        counts[info["color"]] = counts.get(info["color"], 0) + 1
        print(f"{project:<28} {info['motif']:<12} {info['color']}")
    if counts:
        unused = [c for c in COLORS if c not in counts]
        print("\ncolor use:", ", ".join(f"{c}={n}" for c, n in sorted(counts.items(), key=lambda x: -x[1])))
        print("unused:", ", ".join(unused) or "none")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("palette").set_defaults(fn=cmd_palette)
    s = sub.add_parser("suggest")
    s.add_argument("text")
    s.set_defaults(fn=cmd_suggest)
    r = sub.add_parser("render")
    r.add_argument("motif")
    r.add_argument("-o", "--out", required=True)
    r.add_argument("--color", choices=COLORS)
    r.add_argument("--size", choices=SIZES, default="lg")
    r.add_argument("--seed", help="any string; changes the wobble and wash pattern")
    r.set_defaults(fn=cmd_render)
    p = sub.add_parser("preview")
    p.add_argument("svgs", nargs="+")
    p.add_argument("-o", "--out", required=True)
    p.set_defaults(fn=cmd_preview)
    d = sub.add_parser("add")
    d.add_argument("draft")
    d.add_argument("--force", action="store_true")
    d.set_defaults(fn=cmd_add)
    t = sub.add_parser("t3-icon")
    t.add_argument("motif")
    t.add_argument("--project", required=True, help="project title, used for the file name and wobble seed")
    t.add_argument("--color", choices=COLORS)
    t.set_defaults(fn=cmd_t3_icon)
    sub.add_parser("assigned").set_defaults(fn=cmd_assigned)
    h = sub.add_parser("handify")
    h.add_argument("d", help="SVG path data")
    h.add_argument("--amount", type=float, default=0.8, help="drift in path units: ~0.8 on a 64 grid, ~6 on 512")
    h.add_argument("--overshoot", type=float, default=0.0, help="let corners of open polylines run past each other")
    h.add_argument("--seed", default="sketch")
    h.set_defaults(fn=cmd_handify)
    c = sub.add_parser("circle")
    c.add_argument("cx", type=float)
    c.add_argument("cy", type=float)
    c.add_argument("r", type=float)
    c.add_argument("--wobble", type=float, default=0.05, help="radius drift as a fraction of r")
    c.add_argument("--seed", default="circle")
    c.set_defaults(fn=cmd_circle)
    k = sub.add_parser("sparkle")
    k.add_argument("x", type=float)
    k.add_argument("y", type=float)
    k.add_argument("r", type=float)
    k.add_argument("--seed", default="sparkle")
    k.set_defaults(fn=cmd_sparkle)
    li = sub.add_parser("lint")
    li.add_argument("svg")
    li.set_defaults(fn=cmd_lint)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
