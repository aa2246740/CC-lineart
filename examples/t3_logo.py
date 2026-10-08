"""T3 Code logo redrawn in the claude.com line-art + watercolor style.

Read this for technique (layer order, double-stroked letters, glazed washes,
front/behind clouds), not for coordinates. Every path here was placed for this
composition; a new piece needs its own thumbnails and its own strokes.
"""
import math
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "logo"
INK = "#141413"
PAPER = "#FAF9F5"

PALETTES = {
    # Nightly: night sky in plum + sky, clay moon.
    "nightly": {"a": ("#827DBD", "#5F59A0"), "b": ("#6A9BCC", "#4A7DB0"), "moon": ("#D97757", "#B85C3E")},
    # Claude: clay + peach wash, sky moon.
    "claude": {"a": ("#D97757", "#B85C3E"), "b": ("#EBC9B7", "#CFA48C"), "moon": ("#6A9BCC", "#4A7DB0")},
}

# Letters are drawn as centerlines; an ink stroke and a narrower paper stroke
# on the same path give an outlined "paper cutout" letter with matching caps.
LETTER_W = 46
OUTLINE = 9
LETTERS = [
    ("M121 179 C160 177.5 196 178.5 233 178", "square", "round"),
    ("M177 180 C178 236 176.5 290 177.5 335", "square", "round"),
    ("M312 177 C340 176 368 177.5 394 176.5 L347 236 "
     "C390 231 408 262 407 293 C406 331 376 352 344 352 C321 352 305 345 293 334",
     "square", "round"),
]

CLOUD_FRONT = ("M58 414 C46 413 42 398 52 389 C54 371 76 362 92 371 C98 349 128 339 147 354 "
               "C160 331 199 330 213 353 C229 343 252 349 257 368 C274 364 291 377 287 395 "
               "C300 400 301 415 288 417 Z")
CLOUD_BACK = ("M352 262 C340 262 336 249 345 241 C344 226 361 216 375 224 C381 206 408 200 422 214 "
              "C432 203 455 207 458 224 C472 224 482 236 476 249 C484 255 481 266 470 266 Z")
CLOUD_SMALL = ("M372 432 C362 432 360 421 368 416 C369 404 384 399 393 406 C399 394 419 394 425 407 "
               "C437 405 446 415 441 425 C447 429 444 437 436 437 Z")

# Accents: one cluster in the quiet top-left corner (big, medium, small + two dots),
# diagonal from the moon, plus a single small echo by the lower cloud. Not one per corner.
STARS = [(88, 96, 17), (142, 56, 10), (50, 152, 7), (472, 372, 8)]
DOTS = [(126, 124), (178, 90)]

CLAUDE_RAYS = [(-90, 9, 44), (-38, 9, 38), (8, 9, 46), (52, 9, 37), (98, 9, 43), (146, 9, 39), (196, 9, 45)]


def rays(cx, cy, spec):
    out = []
    for angle, r0, r1 in spec:
        a = math.radians(angle)
        out.append(f"M{cx + r0 * math.cos(a):.1f} {cy + r0 * math.sin(a):.1f} "
                   f"L{cx + r1 * math.cos(a):.1f} {cy + r1 * math.sin(a):.1f}")
    return " ".join(out)


def sparkle(x, y, r):
    """Two crossing strokes, unequal arms, a tilt and a slight bow: never a perfect +."""
    rng = random.Random(f"{x}:{y}:{r}")
    tilt = math.radians(rng.uniform(-14, 14))
    out = []
    for axis in (0, 90):
        a = tilt + math.radians(axis)
        ux, uy = math.cos(a), math.sin(a)
        back, fwd = r * rng.uniform(0.5, 0.75), r * rng.uniform(0.95, 1.2)
        if axis:
            back, fwd = back * 1.15, fwd * 1.1
        x0, y0, x1, y1 = x - ux * back, y - uy * back, x + ux * fwd, y + uy * fwd
        bow = r * rng.uniform(0.06, 0.14) * rng.choice((-1, 1))
        mx, my = (x0 + x1) / 2 - uy * bow, (y0 + y1) / 2 + ux * bow
        out.append(f"M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}")
    return " ".join(out)


def wash(fid, seed, freq=0.011, displace=13):
    return f"""<filter id="{fid}" x="-10%" y="-10%" width="120%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="4" seed="{seed}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="{displace}" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.0 1.42" result="a"/>
<feComposite in="d" in2="a" operator="in"/>
</filter>"""


def block(points, fill, edge, fid):
    d = "M" + " L".join(f"{x} {y}" for x, y in points) + " Z"
    return (f'<g filter="url(#{fid})" style="mix-blend-mode:multiply">'
            f'<path d="{d}" fill="{fill}"/>'
            f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="5" stroke-opacity="0.5" stroke-linejoin="round"/></g>')


def logo(palette, icon_bg=False):
    p = PALETTES[palette]
    stars = " ".join(sparkle(*s) for s in STARS)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{INK}" stroke="none"/>' for x, y in DOTS)
    ink_letters = "".join(f'<path d="{d}" stroke="{INK}" stroke-width="{LETTER_W + 2 * OUTLINE}" stroke-linecap="{cap}" stroke-linejoin="{join}"/>' for d, cap, join in LETTERS)
    paper_letters = "".join(f'<path d="{d}" stroke="{PAPER}" stroke-width="{LETTER_W}" stroke-linecap="{cap}" stroke-linejoin="{join}"/>' for d, cap, join in LETTERS)
    bg = ""
    if icon_bg:
        bg = (f'<rect x="16" y="16" width="480" height="480" rx="108" fill="{PAPER}"/>'
              f'<rect x="16" y="16" width="480" height="480" rx="108" fill="none" stroke="#E3E0D5" stroke-width="3"/>')
    inset = "translate(256 256) scale(0.8) translate(-256 -256)" if icon_bg else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<defs>
{wash("washA", 7)}
{wash("washB", 23)}
{wash("washM", 41, freq=0.03, displace=8)}
<filter id="ink" x="-5%" y="-5%" width="110%" height="110%">
<feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="2" seed="5" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>
{bg}
<g transform="{inset}">
<g id="layer-block" style="isolation:isolate">
{block([(128, 116), (440, 104), (454, 352), (138, 366)], *p["a"], "washA")}
{block([(56, 248), (302, 236), (310, 452), (62, 460)], *p["b"], "washB")}
<g filter="url(#washM)"><circle cx="440" cy="84" r="40" fill="{p["moon"][0]}"/><circle cx="440" cy="84" r="40" fill="none" stroke="{p["moon"][1]}" stroke-width="4" stroke-opacity="0.5"/></g>
</g>
<g id="layer-ink" filter="url(#ink)" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
<path d="{CLOUD_BACK}" fill="{PAPER}"/>
<g fill="none">{ink_letters}{paper_letters}</g>
<path d="{CLOUD_FRONT}" fill="{PAPER}"/>
<path d="{CLOUD_SMALL}" fill="{PAPER}" stroke-width="7"/>
<path d="{rays(440, 84, CLAUDE_RAYS)}" stroke-width="8"/>
<path d="{stars}" stroke-width="6"/>
{dots}
</g>
</g>
</svg>
"""


os.makedirs(OUT, exist_ok=True)
for name in PALETTES:
    for icon in (False, True):
        fn = f"t3-{name}{'-icon' if icon else ''}.svg"
        with open(os.path.join(OUT, fn), "w") as f:
            f.write(logo(name, icon))
print("ok")
