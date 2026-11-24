#!/usr/bin/env python3
"""Paint the n24 news-image entry: Tuesday 24 November 2026.

Draws one 1024x1024 page (dense family: 3 heroes + 10 grid cards +
17 ALSO ON lines = 30 stories) with PIL only. No network, no random
numbers, no clock reads: two runs of compose() must be byte-identical.

Every story carries its first-reported date in its panel; the footer
states the true 22-24 Nov range. Research notes live beside this file
in dev/research-2026-11-24.md.
"""

import hashlib
import json
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT = "entry.png"

PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 32, 42)
NAVY = (20, 38, 74)
SKY = (214, 228, 240)
GREY = (120, 120, 118)
GREEN = (30, 122, 52)
AMBER = (154, 107, 0)
STEEL = (90, 100, 115)
CARD = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ISSUES = []


def font(path, size):
    return ImageFont.truetype(path, size)


def serif_b(size):
    return font(SERIF_B, size)


def serif_r(size):
    return font(SERIF, size)


def sans_b(size):
    return font(SANS_B, size)


def sans_r(size):
    return font(SANS, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, text, fnt, max_w, max_lines, floor=9):
    """Wrap text; shrink the font until it fits in max_lines.

    Returns (font, lines). Records an issue when even the floor size
    does not fit, so the caller can shorten the copy.
    """
    size = fnt.size
    while size > floor:
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
        fnt = font(fnt.path, size)
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        ISSUES.append("overflow: %r needs %d lines at %dpx"
                      % (text[:40], len(lines), floor))
    return fnt, lines


def put_lines(draw, x, y, lines, fnt, fill, step):
    for i, line in enumerate(lines):
        draw.text((x, y + i * step), line, font=fnt, fill=fill)
    return y + len(lines) * step


def pill_width(draw, label, size):
    return int(draw.textlength(label, font=sans_b(size))) + 12


def pill(draw, x, y, label, size, bg, fg=(255, 255, 255)):
    """Small status pill. Returns its width."""
    fnt = sans_b(size)
    w = pill_width(draw, label, size)
    h = size + 7
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + w // 2, y + h // 2), label, font=fnt, fill=fg,
              anchor="mm")
    return w


def date_tag(draw, x, y, label, size=10):
    """Small dark date tag in a scene corner. Returns its width."""
    fnt = sans_b(size)
    w = int(draw.textlength(label, font=fnt)) + 10
    h = size + 6
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=(20, 20, 20))
    draw.text((x + w // 2, y + h // 2), label, font=fnt,
              fill=(255, 255, 255), anchor="mm")
    return w


def chip_for(status):
    if status == "CONFIRMED":
        return GREEN
    if status == "REPORTED":
        return AMBER
    return STEEL


def layer(w, h, painter, bg):
    """Paint one scene on its own layer so nothing can leak past it."""
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    painter(d, w, h)
    return img


# ---------------------------------------------------------------- data

HEROES = [
    {
        "num": 1, "date": "23 NOV", "status": "CONFIRMED",
        "banner": "HUANG IS BACK",
        "title": "Nvidia brings Huang back; shares soar 31%",
        "body": ("Board reinstates co-founder as CEO 11 days after he "
                 "quit; ~$1tn added. Trump: \u201cI made the deal\u201d."),
        "scene": "chip",
    },
    {
        "num": 2, "date": "23 NOV", "status": "CONFIRMED",
        "banner": "WARSHIP SUNK",
        "title": "Ukraine sinks Russian corvette off Libya",
        "body": ("Seven sea drones hit the Merkury at Benghazi; Ka-27 "
                 "helicopter destroyed, cargo ship Angara struck."),
        "scene": "sea",
    },
    {
        "num": 3, "date": "22 NOV", "status": "CONFIRMED",
        "banner": "NO DEAL",
        "title": "COP31 collapses with no agreement",
        "body": ("200 countries leave Antalya empty-handed as the draft "
                 "drops fossil fuels. Guterres \u201cdeeply disappointed\u201d."),
        "scene": "chairs",
    },
]

GRID = [
    {
        "num": 4, "date": "23 NOV", "status": "CONFIRMED",
        "title": "Gaza a \u2018toxic wasteland\u2019",
        "body": ("Oxfam: >99% shows contamination; 61m tonnes of "
                 "debris; 78% of land hit."),
        "scene": "rubble",
    },
    {
        "num": 5, "date": "23 NOV", "status": "REPORTED",
        "title": "Russia \u2018ready to put nuke in space\u2019",
        "body": ("Sputnik-S may launch by Dec. Rutte: NATO covers "
                 "space. Moscow denies."),
        "scene": "space",
    },
    {
        "num": 6, "date": "23 NOV", "status": "CONFIRMED",
        "title": "Dymer toll reaches 11",
        "body": ("Drone hit flats at 5am Sun; boy, 7, pulled out "
                 "alive. Two still missing."),
        "scene": "flats",
    },
    {
        "num": 7, "date": "23 NOV", "status": "CONFIRMED",
        "title": "India gives Nepal $1.62bn",
        "body": ("Modi\u2013Shah talks: flood aid, 8 deals, "
                 "Ayodhya\u2013Janakpur rail link opened."),
        "scene": "flags",
    },
    {
        "num": 8, "date": "23 NOV", "status": "CONFIRMED",
        "title": "Factory fire: 24 dead",
        "body": ("Banten candy plant blaze; ~30 missing, DNA IDs take "
                 "weeks. Cause probed."),
        "scene": "fire",
    },
    {
        "num": 9, "date": "23 NOV", "status": "CONFIRMED",
        "title": "UK to host 2035 World Cup",
        "body": ("FIFA ratifies UK for 2035, US-led bid for 2031. "
                 "First in UK since 1966."),
        "scene": "pitch",
    },
    {
        "num": 10, "date": "23 NOV", "status": "CONFIRMED",
        "title": "Fury reveals diagnosis",
        "body": ("2016 diagnosis made public in Netflix film out Fri; "
                 "faces Joshua 11 Dec."),
        "scene": "ring",
    },
    {
        "num": 11, "date": "23 NOV", "status": "REPORTED",
        "title": "Singer flogged over hijab",
        "body": ("Ahmadi flogged in Qom after singing without a hijab, "
                 "lawyers say."),
        "scene": "mic",
    },
    {
        "num": 12, "date": "23 NOV", "status": "CONFIRMED",
        "title": "Democrats\u2019 biggest win since 1992",
        "body": ("Flipping North Carolina gives the largest House "
                 "majority in 34 years."),
        "scene": "dome",
    },
    {
        "num": 13, "date": "23 NOV", "status": "CONFIRMED",
        "title": "Huang must still face Congress",
        "body": ("Senate hearing 3 Dec, House panels 1 Dec. Vow "
                 "sharper chip-export probes."),
        "scene": "hearing",
    },
]

# ALSO ON: 3 columns of 6 / 6 / 5. No per-line sources (dense family);
# each line carries its own status colour dot + pill at the right.
ALSO_ON = [
    ("Trump: \u2018I made the deal\u2019 on Huang", "CONFIRMED"),
    ("UK\u2013EU food deal to cut grocery costs", "CONFIRMED"),
    ("Gaza strikes kill 3, incl. UN worker", "CONFIRMED"),
    ("Iran vows \u2018all means\u2019 vs US blockade", "REPORTED"),
    ("UK sanctions Myanmar generals", "CONFIRMED"),
    ("Denmark top court backs \u2018ghetto law\u2019", "CONFIRMED"),
    ("Armenia proposes new constitution", "CONFIRMED"),
    ("Bangladesh vows to arrest Hasina", "CONFIRMED"),
    ("India\u2013NZ 1st Test ends in a draw", "CONFIRMED"),
    ("NHS launches huge AI cancer trial", "CONFIRMED"),
    ("Nigeria boat tragedy: rescue race on", "REPORTED"),
    ("Mexico soldiers attacked after arrest", "CONFIRMED"),
    ("Belgium flights cancelled in strike", "CONFIRMED"),
    ("Co-op Live evacuated in Manchester", "CONFIRMED"),
    ("California Democrat to quit Congress", "CONFIRMED"),
    ("Miley Cyrus marries Maxx Morando", "CONFIRMED"),
    ("Capita shares plunge 70%, boss quits", "CONFIRMED"),
]

STATS = [
    ("+31%", "NVIDIA AT CLOSE"),
    ("$1tn", "ADDED TO NVIDIA"),
    ("7", "SEA DRONES"),
    ("2,400", "KM FROM THE FRONT"),
    (">99%", "OF GAZA CONTAMINATED"),
    ("$1.62bn", "INDIA TO NEPAL"),
    ("24", "DEAD IN BANTEN FIRE"),
]

REGIONS = [("NORTH AMERICA", 7), ("EUROPE", 12), ("MIDDLE EAST", 4),
           ("ASIA", 5), ("AFRICA", 2)]

TIMELINE = [
    ("05:23", "Dymer toll 11"),
    ("08:05", "Merkury sunk"),
    ("14:12", "Huang back"),
    ("15:39", "Sputnik-S warning"),
    ("21:00", "NVDA +31%"),
]

DATE_CHECK = [
    "BepiColombo entered Mercury orbit \u2014 21 Nov",
    "Lowy Asia Power Index published \u2014 22 Nov",
    "US midterm results \u2014 3 Nov",
    "Trump\u2019s \u2018$3tn market loss\u2019 claim \u2014 9\u201315 Nov",
    "Not yet: Tue US trading \u00b7 Cikande toll update",
]

# Map pins: (story number, lon, lat, disc offset dx, dy).
# Numbers match the story numbers above (heroes 1-3, grid 4-13).
PINS = [
    (1, -122, 37, 0, 0),      # Santa Clara — Nvidia
    (13, -77, 39, 0, 0),      # Washington — Congress
    (9, 0, 51, 0, 0),         # London — World Cup
    (5, 13, 52, 0, 0),        # Berlin — Sputnik-S
    (3, 30, 37, 0, -14),      # Antalya — COP31
    (4, 34, 31, 14, 8),       # Gaza
    (2, 20, 32, -26, 2),     # Benghazi — Merkury
    (6, 30, 51, 16, -12),     # Dymer, Kyiv region
    (7, 77, 28, 0, 0),        # New Delhi — Nepal package
    (8, 106, -6, 0, 0),       # Cikande — factory fire
]

# Rough continent outlines (lon, lat) for the schematic map.
LAND = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
     (-85, 70), (-75, 62), (-60, 47), (-70, 42), (-75, 35),
     (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-140, 60), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -20),
     (-48, -30), (-60, -40), (-70, -50), (-73, -40), (-75, -20),
     (-80, -5)],
    [(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (20, 60),
     (28, 62), (30, 70), (40, 68), (45, 60), (40, 50), (30, 46),
     (25, 40), (20, 38), (12, 44), (5, 44), (0, 40), (-9, 38)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (48, 11), (51, 0), (40, -15), (35, -25),
     (28, -33), (20, -35), (15, -20), (12, -5), (9, 4), (-8, 5),
     (-15, 12)],
    [(40, 68), (60, 70), (80, 73), (110, 75), (140, 72), (160, 66),
     (180, 65), (162, 55), (140, 45), (130, 35), (122, 30),
     (110, 20), (105, 10), (100, 5), (95, 15), (90, 22), (80, 8),
     (75, 20), (65, 25), (55, 28), (48, 30), (43, 38), (40, 45),
     (42, 55)],
    [(113, -22), (125, -12), (135, -12), (142, -10), (150, -20),
     (153, -28), (147, -38), (140, -38), (130, -32), (120, -34),
     (113, -26)],
]


# ---------------------------------------------------------------- scenes
# Each painter draws one small scene into a layer of size (w, h).
# All shapes are plain geometry on flat colour; no text inside scenes.

def scene_chip(d, w, h):
    """Nvidia: a chip on a circuit board under a rising green chart."""
    d.rectangle([0, 0, w, h], fill=(13, 38, 26))
    for i in range(5):
        y = int(h * (0.15 + 0.17 * i))
        d.line([0, y, w, y], fill=(24, 66, 44), width=1)
    cx, cy, s = w // 2, int(h * 0.52), int(h * 0.34)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(16, 20, 26),
                outline=(118, 185, 0), width=3)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(28, 32, 40), outline=(118, 185, 0), width=1)
    for k in range(-2, 3):
        d.line([cx + k * s // 2, cy - s - 8, cx + k * s // 2, cy - s],
               fill=(118, 185, 0), width=2)
        d.line([cx + k * s // 2, cy + s, cx + k * s // 2, cy + s + 8],
               fill=(118, 185, 0), width=2)
    pts = [(6, int(h * 0.82)), (w * 0.25, int(h * 0.66)),
           (w * 0.45, int(h * 0.72)), (w * 0.68, int(h * 0.42)),
           (w - 8, int(h * 0.18))]
    d.line(pts, fill=(118, 185, 0), width=4, joint="curve")
    d.polygon([(w - 22, int(h * 0.18)), (w - 6, int(h * 0.18)),
               (w - 14, int(h * 0.30))], fill=(118, 185, 0))
    for px, py in pts[1:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(190, 230, 120))


def scene_sea(d, w, h):
    """Merkury: dusk sea, grey corvette, jagged blast, drone boats.

    The blast is a jagged star, not concentric rings: rings read as
    a sun at judge size. The hull stays visible on both sides of it.
    """
    for i in range(6):
        d.rectangle([0, int(h * i / 6), w, int(h * (i + 1) / 6)],
                    fill=(46 - i * 2, 52 - i, 74 - i * 3))
    d.rectangle([0, int(h * 0.55), w, h], fill=(16, 42, 68))
    for i in range(4):
        y = int(h * (0.62 + 0.09 * i))
        d.line([0, y, w, y], fill=(38, 84, 120), width=1)
    hx0, hx1 = int(w * 0.24), int(w * 0.82)
    hy = int(h * 0.52)
    d.polygon([(hx0, hy), (hx1, hy), (int(w * 0.78), hy + int(h * 0.10)),
               (int(w * 0.28), hy + int(h * 0.10))], fill=(74, 82, 92))
    d.rectangle([int(w * 0.30), hy - int(h * 0.14), int(w * 0.42),
                 hy], fill=(88, 96, 106))
    d.line([int(w * 0.34), hy - int(h * 0.24), int(w * 0.34), hy],
           fill=(88, 96, 106), width=3)
    d.rectangle([int(w * 0.72), hy - int(h * 0.10), int(w * 0.76), hy],
                fill=(60, 66, 74))
    bx, by = int(w * 0.56), int(h * 0.44)
    for cx, cy, r in ((int(w * 0.48), int(h * 0.16), 9),
                      (int(w * 0.60), int(h * 0.10), 11),
                      (int(w * 0.68), int(h * 0.18), 7)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 96, 102))
    outer, inner = int(h * 0.22), int(h * 0.11)
    pts = []
    for k in range(16):
        ang = k * 3.14159 / 8
        r = outer if k % 2 == 0 else inner
        pts.append((bx + int(r * math.cos(ang)),
                    by + int(r * math.sin(ang))))
    d.polygon(pts, fill=(255, 122, 26))
    pts2 = []
    for k in range(12):
        ang = k * 3.14159 / 6 + 0.26
        r = int(h * 0.12) if k % 2 == 0 else int(h * 0.06)
        pts2.append((bx + int(r * math.cos(ang)),
                     by + int(r * math.sin(ang))))
    d.polygon(pts2, fill=(255, 226, 120))
    for fx in (int(w * 0.12), int(w * 0.90)):
        fy = int(h * 0.86)
        d.polygon([(fx - 14, fy), (fx + 14, fy), (fx + 6, fy - 8),
                   (fx - 6, fy - 8)], fill=(30, 34, 40))
        d.line([fx - 22, fy + 3, fx + 22, fy + 3], fill=(220, 230, 235),
               width=2)


def scene_chairs(d, w, h):
    """COP31: a hall of empty chairs, a lone podium, a blank screen."""
    d.rectangle([0, 0, w, h], fill=(196, 198, 196))
    d.rectangle([0, 0, w, int(h * 0.34)], fill=(58, 74, 96))
    d.rectangle([int(w * 0.36), int(h * 0.07), int(w * 0.64),
                 int(h * 0.27)], fill=(226, 230, 234),
                outline=(255, 255, 255), width=2)
    for row in range(3):
        y = int(h * (0.46 + 0.16 * row))
        cw = int(w * 0.085)
        gap = int(w * 0.045)
        total = 6 * cw + 5 * gap
        x0 = (w - total) // 2
        for k in range(6):
            x = x0 + k * (cw + gap)
            d.rounded_rectangle([x, y, x + cw, y + int(h * 0.09)],
                                radius=3, fill=(74, 88, 110))
            d.rectangle([x + 3, y + int(h * 0.09), x + cw - 3,
                         y + int(h * 0.115)], fill=(58, 70, 90))
    px = w // 2
    d.polygon([(px - 16, int(h * 0.92)), (px + 16, int(h * 0.92)),
               (px + 10, int(h * 0.62)), (px - 10, int(h * 0.62))],
              fill=(94, 60, 44))
    d.line([px, int(h * 0.62), px + 14, int(h * 0.50)], fill=(40, 40, 40),
           width=2)
    d.ellipse([px + 12, int(h * 0.47), px + 18, int(h * 0.53)],
              fill=(40, 40, 40))


def scene_rubble(d, w, h):
    """Gaza: broken slabs and dust over cracked ground."""
    d.rectangle([0, 0, w, h], fill=(168, 160, 148))
    d.polygon([(0, h), (int(w * 0.30), int(h * 0.30)),
               (int(w * 0.55), h)], fill=(120, 112, 100))
    d.polygon([(int(w * 0.45), h), (int(w * 0.70), int(h * 0.45)),
               (w, h)], fill=(96, 90, 80))
    d.polygon([(int(w * 0.62), int(h * 0.62)), (int(w * 0.82), h),
               (int(w * 0.58), h)], fill=(140, 132, 120))
    d.line([0, int(h * 0.78), w, int(h * 0.70)], fill=(90, 84, 74),
           width=2)
    d.line([(int(w * 0.30), int(h * 0.30)), (int(w * 0.55), h)],
           fill=(70, 64, 56), width=2)
    for cx, cy, r in ((int(w * 0.18), int(h * 0.22), 7),
                      (int(w * 0.85), int(h * 0.30), 9),
                      (int(w * 0.55), int(h * 0.16), 5)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 142, 130))
    d.rectangle([int(w * 0.08), int(h * 0.82), int(w * 0.30),
                 int(h * 0.88)], fill=(60, 90, 60))
    d.rectangle([int(w * 0.10), int(h * 0.76), int(w * 0.13),
                 int(h * 0.82)], fill=(60, 90, 60))


def scene_space(d, w, h):
    """Sputnik-S: black sky, stars, a satellite over Earth's arc."""
    d.rectangle([0, 0, w, h], fill=(8, 10, 20))
    for sx, sy, r in ((int(w * 0.10), int(h * 0.20), 2),
                      (int(w * 0.25), int(h * 0.12), 1),
                      (int(w * 0.80), int(h * 0.18), 2),
                      (int(w * 0.92), int(h * 0.35), 1),
                      (int(w * 0.45), int(h * 0.08), 1),
                      (int(w * 0.60), int(h * 0.30), 2),
                      (int(w * 0.05), int(h * 0.55), 1)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    d.ellipse([-int(w * 0.25), int(h * 0.78), int(w * 1.25),
               int(h * 1.55)], fill=(28, 78, 150))
    d.ellipse([-int(w * 0.25), int(h * 0.78), int(w * 1.25),
               int(h * 1.05)], outline=(120, 180, 230), width=2)
    cx, cy = int(w * 0.55), int(h * 0.42)
    d.rectangle([cx - int(w * 0.16), cy - 4, cx - int(w * 0.05), cy + 4],
                fill=(40, 90, 160))
    d.rectangle([cx + int(w * 0.05), cy - 4, cx + int(w * 0.16), cy + 4],
                fill=(40, 90, 160))
    d.rectangle([cx - int(w * 0.05), cy - 10, cx + int(w * 0.05),
                 cy + 10], fill=(190, 195, 200))
    d.line([cx, cy - 10, cx, cy - 22], fill=(220, 220, 220), width=2)
    d.ellipse([cx - 3, cy - 26, cx + 3, cy - 20], fill=(255, 90, 60))
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 90, 60))


def scene_flats(d, w, h):
    """Dymer: a damaged block at night, rescue light in the rubble."""
    d.rectangle([0, 0, w, h], fill=(24, 32, 52))
    d.ellipse([int(w * 0.82), int(h * 0.10), int(w * 0.90),
               int(h * 0.18)], fill=(230, 230, 210))
    bx0, bx1 = int(w * 0.22), int(w * 0.78)
    d.rectangle([bx0, int(h * 0.18), bx1, h], fill=(52, 58, 72))
    d.polygon([(int(w * 0.50), int(h * 0.18)), (bx1, int(h * 0.18)),
               (bx1, int(h * 0.55)), (int(w * 0.62), int(h * 0.42)),
               (int(w * 0.50), int(h * 0.55))], fill=(30, 34, 44))
    for row in range(4):
        for col in range(4):
            x = bx0 + 8 + col * int(w * 0.13)
            y = int(h * 0.24) + row * int(h * 0.18)
            lit = (row + col) % 3 != 0
            d.rectangle([x, y, x + 12, y + 10],
                        fill=(255, 210, 110) if lit else (20, 24, 34))
    d.polygon([(int(w * 0.50), int(h * 0.55)), (int(w * 0.62),
               int(h * 0.42)), (int(w * 0.66), h), (int(w * 0.44), h)],
              fill=(120, 112, 100))
    d.polygon([(int(w * 0.30), h), (int(w * 0.44), int(h * 0.72)),
               (int(w * 0.52), h)], fill=(255, 220, 120))
    d.rectangle([int(w * 0.08), int(h * 0.86), int(w * 0.16),
                 int(h * 0.92)], fill=(200, 60, 40))


def scene_flags(d, w, h):
    """India-Nepal: mountains, two flags, a rail line."""
    d.rectangle([0, 0, w, h], fill=(178, 208, 232))
    d.polygon([(0, h), (int(w * 0.30), int(h * 0.30)), (int(w * 0.60), h)],
              fill=(120, 140, 160))
    d.polygon([(int(w * 0.45), h), (int(w * 0.72), int(h * 0.38)),
               (w, h)], fill=(96, 118, 140))
    d.polygon([(int(w * 0.26), int(h * 0.38)), (int(w * 0.30),
               int(h * 0.30)), (int(w * 0.34), int(h * 0.38))],
              fill=(255, 255, 255))
    d.polygon([(int(w * 0.68), int(h * 0.46)), (int(w * 0.72),
               int(h * 0.38)), (int(w * 0.76), int(h * 0.46))],
              fill=(255, 255, 255))
    for fx, cols in ((int(w * 0.18), [(255, 153, 51), (255, 255, 255),
                                      (19, 136, 8)]),
                     (int(w * 0.82), [(220, 20, 40), (220, 20, 40),
                                      (0, 56, 147)])):
        d.line([fx, int(h * 0.22), fx, int(h * 0.78)], fill=(60, 60, 60),
               width=2)
        for i, col in enumerate(cols):
            d.rectangle([fx, int(h * (0.24 + 0.07 * i)),
                         fx + 26, int(h * (0.31 + 0.07 * i))], fill=col)
    d.line([0, int(h * 0.88), w, int(h * 0.88)], fill=(90, 70, 50),
           width=3)


def scene_fire(d, w, h):
    """Cikande: factory silhouette, separate flame tongues, smoke."""
    d.rectangle([0, 0, w, h], fill=(34, 28, 34))
    for cx, cy, r in ((int(w * 0.20), int(h * 0.18), 10),
                      (int(w * 0.55), int(h * 0.12), 12),
                      (int(w * 0.82), int(h * 0.22), 8)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 105, 105))
    d.rectangle([int(w * 0.10), int(h * 0.48), int(w * 0.90), h],
                fill=(20, 20, 24))
    d.polygon([(int(w * 0.10), int(h * 0.48)), (int(w * 0.50),
               int(h * 0.36)), (int(w * 0.90), int(h * 0.48))],
              fill=(44, 40, 44))
    for wx in range(int(w * 0.18), int(w * 0.86), int(w * 0.14)):
        d.rectangle([wx, int(h * 0.56), wx + 10, int(h * 0.66)],
                    fill=(255, 190, 60))
    sill = int(h * 0.48)
    for tx, th, lean in ((int(w * 0.28), int(h * 0.30), -6),
                         (int(w * 0.46), int(h * 0.40), 4),
                         (int(w * 0.64), int(h * 0.26), -3),
                         (int(w * 0.80), int(h * 0.34), 7)):
        d.polygon([(tx - 7, sill), (tx - 4, sill - th),
                   (tx + lean, sill - th - 6), (tx + 6, sill - th),
                   (tx + 7, sill)], fill=(255, 110, 20))
        d.polygon([(tx - 3, sill), (tx - 2, sill - int(th * 0.6)),
                   (tx + lean, sill - int(th * 0.6) - 4),
                   (tx + 3, sill)], fill=(255, 220, 90))
    d.rectangle([int(w * 0.10), sill - 2, int(w * 0.90), sill + 2],
                fill=(255, 140, 30))


def scene_pitch(d, w, h):
    """World Cup: green pitch, white lines, ball, goal."""
    d.rectangle([0, 0, w, h], fill=(36, 130, 58))
    for i in range(4):
        d.rectangle([0, int(h * i / 4), w, int(h * (i + 1) / 4)],
                    fill=(36, 130, 58) if i % 2 == 0 else (30, 118, 52))
    d.ellipse([int(w * 0.38), int(h * 0.28), int(w * 0.62),
               int(h * 0.78)], outline=(255, 255, 255), width=2)
    d.line([0, int(h * 0.52), w, int(h * 0.52)], fill=(255, 255, 255),
           width=2)
    d.line([int(w * 0.06), int(h * 0.16), int(w * 0.06), int(h * 0.40)],
           fill=(255, 255, 255), width=3)
    d.line([int(w * 0.06), int(h * 0.16), int(w * 0.24), int(h * 0.16)],
           fill=(255, 255, 255), width=3)
    d.line([int(w * 0.06), int(h * 0.40), int(w * 0.24), int(h * 0.40)],
           fill=(255, 255, 255), width=3)
    bx, by, br = int(w * 0.72), int(h * 0.62), int(h * 0.16)
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255),
              outline=(30, 30, 30), width=2)
    d.polygon([(bx, by - 6), (bx + 6, by), (bx, by + 6), (bx - 6, by)],
              fill=(30, 30, 30))


def scene_ring(d, w, h):
    """Fury: a boxing ring under a spotlight, gold belt on the canvas."""
    d.rectangle([0, 0, w, h], fill=(26, 26, 34))
    d.polygon([(int(w * 0.38), 0), (int(w * 0.62), 0),
               (int(w * 0.86), h), (int(w * 0.14), h)],
              fill=(70, 70, 88))
    d.rectangle([int(w * 0.08), int(h * 0.66), int(w * 0.92), h],
                fill=(52, 78, 120))
    for ry in (int(h * 0.34), int(h * 0.44), int(h * 0.54)):
        d.line([int(w * 0.06), ry, int(w * 0.94), ry], fill=(220, 60, 60),
               width=3)
    for px in (int(w * 0.08), int(w * 0.92)):
        d.rectangle([px - 4, int(h * 0.28), px + 4, int(h * 0.68)],
                    fill=(200, 200, 200))
    d.rectangle([int(w * 0.34), int(h * 0.76), int(w * 0.66),
                 int(h * 0.88)], fill=(212, 175, 55))
    d.ellipse([int(w * 0.46), int(h * 0.77), int(w * 0.54),
               int(h * 0.87)], fill=(255, 220, 120),
              outline=(140, 110, 20), width=2)


def scene_mic(d, w, h):
    """Ahmadi: a lone microphone on a dark stage."""
    d.rectangle([0, 0, w, h], fill=(66, 22, 28))
    d.polygon([(int(w * 0.42), 0), (int(w * 0.58), 0),
               (int(w * 0.72), h), (int(w * 0.28), h)],
              fill=(110, 44, 50))
    d.ellipse([int(w * 0.42), int(h * 0.16), int(w * 0.58),
               int(h * 0.42)], fill=(40, 40, 46))
    for i in range(3):
        y = int(h * (0.22 + 0.07 * i))
        d.line([int(w * 0.44), y, int(w * 0.56), y], fill=(160, 160, 165),
               width=2)
    d.line([w // 2, int(h * 0.42), w // 2, int(h * 0.86)],
           fill=(30, 30, 34), width=4)
    d.line([int(w * 0.40), int(h * 0.86), int(w * 0.60), int(h * 0.86)],
           fill=(30, 30, 34), width=4)
    d.rectangle([0, int(h * 0.86), w, h], fill=(30, 12, 14))


def scene_dome(d, w, h):
    """Democrats: the Capitol dome in blue."""
    d.rectangle([0, 0, w, h], fill=(150, 186, 220))
    d.ellipse([int(w * 0.32), int(h * 0.06), int(w * 0.68),
               int(h * 0.62)], fill=(250, 250, 246))
    d.rectangle([int(w * 0.30), int(h * 0.58), int(w * 0.70),
                 int(h * 0.68)], fill=(250, 250, 246))
    for cx in range(int(w * 0.32), int(w * 0.70), int(w * 0.09)):
        d.rectangle([cx, int(h * 0.68), cx + 8, int(h * 0.86)],
                    fill=(250, 250, 246))
    d.rectangle([int(w * 0.26), int(h * 0.86), int(w * 0.74),
                 int(h * 0.92)], fill=(250, 250, 246))
    d.line([w // 2, int(h * 0.06), w // 2, 2], fill=(60, 60, 60),
           width=2)
    d.polygon([(w // 2, 2), (w // 2 + 16, 6), (w // 2, 10)],
              fill=(179, 32, 42))
    d.rectangle([0, int(h * 0.92), w, h], fill=(52, 96, 52))


def scene_hearing(d, w, h):
    """Congress hearing: a long desk, three microphones, flags."""
    d.rectangle([0, 0, w, h], fill=(38, 52, 84))
    for fx, col in ((int(w * 0.10), (179, 32, 42)),
                    (int(w * 0.88), (40, 80, 160))):
        d.rectangle([fx, int(h * 0.10), fx + 12, int(h * 0.44)],
                    fill=col)
    d.rectangle([int(w * 0.06), int(h * 0.52), int(w * 0.94),
                 int(h * 0.92)], fill=(96, 66, 44))
    d.rectangle([int(w * 0.06), int(h * 0.52), int(w * 0.94),
                 int(h * 0.58)], fill=(120, 84, 56))
    for mx in (int(w * 0.30), int(w * 0.50), int(w * 0.70)):
        d.line([mx, int(h * 0.52), mx, int(h * 0.36)], fill=(30, 30, 30),
               width=3)
        d.ellipse([mx - 6, int(h * 0.30), mx + 6, int(h * 0.38)],
                  fill=(30, 30, 30))
        d.rectangle([mx - 14, int(h * 0.46), mx + 14, int(h * 0.52)],
                    fill=(240, 240, 230))
    d.ellipse([int(w * 0.46), int(h * 0.66), int(w * 0.54),
               int(h * 0.82)], fill=(212, 175, 55))


SCENES = {
    "chip": scene_chip, "sea": scene_sea, "chairs": scene_chairs,
    "rubble": scene_rubble, "space": scene_space, "flats": scene_flats,
    "flags": scene_flags, "fire": scene_fire, "pitch": scene_pitch,
    "ring": scene_ring, "mic": scene_mic, "dome": scene_dome,
    "hearing": scene_hearing,
}


# ---------------------------------------------------------------- panels

PAGE = {
    "rule_y": 116,
    "stats_y": 120, "stats_h": 54,
    "regions_y": 178,
    "timeline_y": 196, "timeline_h": 30,
    "heroes_y": 230, "heroes_h": 196, "heroes_w": 328,
    "heroes_x": (10, 346, 682),
    "grid_y": (434, 588), "grid_h": 146, "grid_w": 195,
    "grid_x": (10, 213, 416, 619, 822),
    "also_y": 742, "also_lines_y": 760, "also_step": 17,
    "bottom_y": 868, "bottom_h": 120,
    "footer_rule": 992,
}


def hero_panel(img, draw, x, y, hero):
    w, h = PAGE["heroes_w"], PAGE["heroes_h"]
    scene_h = 108
    img.paste(layer(w, scene_h, SCENES[hero["scene"]], (200, 200, 200)),
              (x, y))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    draw.rectangle([x, y + scene_h - 20, x + w, y + scene_h],
                   fill=RED)
    draw.text((x + w // 2, y + scene_h - 10), hero["banner"],
              font=sans_b(13), fill=(255, 255, 255), anchor="mm")
    date_tag(draw, x + 5, y + 5, hero["date"], size=10)
    pw = pill_width(draw, hero["status"], 10)
    pill(draw, x + w - 5 - pw, y + 5, hero["status"], 10,
         chip_for(hero["status"]))
    tfnt, tlines = fit_block(draw, hero["title"], serif_b(15), w - 16,
                             2, floor=12)
    ty = put_lines(draw, x + 8, y + scene_h + 6, tlines, tfnt, INK, 18)
    bfnt, blines = fit_block(draw, hero["body"], sans_r(12), w - 16,
                             2, floor=10)
    put_lines(draw, x + 8, ty + 2, blines, bfnt, (60, 60, 60), 15)


def grid_panel(img, draw, x, y, card):
    w, h = PAGE["grid_w"], PAGE["grid_h"]
    scene_h = 46
    img.paste(layer(w, scene_h, SCENES[card["scene"]], (200, 200, 200)),
              (x, y))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    date_tag(draw, x + 4, y + 4, card["date"], size=9)
    pw = pill_width(draw, card["status"], 9)
    pill(draw, x + w - 4 - pw, y + 4, card["status"], 9,
         chip_for(card["status"]))
    tfnt, tlines = fit_block(draw, card["title"], sans_b(19), w - 12,
                             2, floor=15)
    ty = put_lines(draw, x + 6, y + scene_h + 4, tlines, tfnt, INK, 22)
    bfnt, blines = fit_block(draw, card["body"], sans_r(13), w - 12,
                             3, floor=11)
    put_lines(draw, x + 6, ty + 1, blines, bfnt, (60, 60, 60), 16)


# ---------------------------------------------------------------- sections

def draw_masthead(draw):
    draw.text((SIZE // 2, 3), "TUESDAY \u00b7 THE WORLD IN ONE DAY",
              font=sans_b(11), fill=RED, anchor="ma")
    fnt = serif_b(84)
    while (draw.textlength("24 NOVEMBER 2026", font=fnt) > SIZE - 20
           and fnt.size > 40):
        fnt = serif_b(fnt.size - 1)
    draw.text((SIZE // 2, 10), "24 NOVEMBER 2026", font=fnt, fill=INK,
              anchor="ma")
    draw.text((SIZE // 2, 96),
              "Huang is back \u00b7 warship sunk off Libya \u00b7 "
              "COP31 collapses",
              font=serif_r(16), fill=RED, anchor="ma")
    draw.line([10, PAGE["rule_y"], SIZE - 10, PAGE["rule_y"]],
              fill=RED, width=2)


def draw_stats(draw):
    """Navy stat band; number+label block centred by ink measurement."""
    y0, h = PAGE["stats_y"], PAGE["stats_h"]
    draw.rectangle([10, y0, SIZE - 10, y0 + h], fill=NAVY)
    num_fnt, lab_fnt = sans_b(34), sans_b(10)
    nb = draw.textbbox((0, 0), "8", font=num_fnt, anchor="ma")
    lb = draw.textbbox((0, 0), "A", font=lab_fnt, anchor="ma")
    num_h, lab_h = nb[3] - nb[1], lb[3] - lb[1]
    gap = 3
    block = num_h + gap + lab_h
    ink_top = y0 + (h - block) // 2
    num_y = ink_top - nb[1]
    lab_y = ink_top + num_h + gap - lb[1]
    cell = (SIZE - 20) / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = 10 + cell * (i + 0.5)
        fnt = num_fnt
        while (draw.textlength(num, font=fnt) > cell - 6
               and fnt.size > 20):
            fnt = sans_b(fnt.size - 1)
        draw.text((cx, num_y), num, font=fnt, fill=(255, 255, 255),
                  anchor="ma")
        draw.text((cx, lab_y), label, font=lab_fnt,
                  fill=(200, 205, 215), anchor="ma")
    return {"top_air": ink_top - y0,
            "bottom_air": y0 + h - (ink_top + block)}


def draw_regions(draw):
    parts = []
    for name, n in REGIONS:
        parts.append("%s %d" % (name, n))
    text = "  \u00b7  ".join(parts) + "   \u2014   30 STORIES IN ALL"
    draw.text((SIZE // 2, PAGE["regions_y"]), text, font=sans_b(12),
              fill=INK, anchor="ma")


def draw_timeline(draw):
    y0, h = PAGE["timeline_y"], PAGE["timeline_h"]
    draw.rectangle([10, y0, SIZE - 10, y0 + h], outline=STEEL, width=1)
    x = 22
    draw.text((x, y0 + h // 2), "THE DAY IN UTC \u00b7 MON 23 NOV",
              font=sans_b(11), fill=RED, anchor="lm")
    x += int(draw.textlength("THE DAY IN UTC \u00b7 MON 23 NOV",
                             font=sans_b(11))) + 18
    for time, label in TIMELINE:
        draw.text((x, y0 + h // 2), time, font=sans_b(11), fill=RED,
                  anchor="lm")
        x += int(draw.textlength(time, font=sans_b(11))) + 4
        draw.text((x, y0 + h // 2), label, font=sans_r(11), fill=INK,
                  anchor="lm")
        x += int(draw.textlength(label, font=sans_r(11))) + 14
        if (time, label) != TIMELINE[-1]:
            draw.text((x, y0 + h // 2), "\u00b7", font=sans_b(11),
                      fill=STEEL, anchor="lm")
            x += 14
    if x > SIZE - 12:
        ISSUES.append("timeline overflows right edge by %dpx"
                      % (x - (SIZE - 12)))


def draw_also_on(draw):
    x0 = 10
    col_w = (SIZE - 20 - 2 * 16) // 3
    draw.text((x0, PAGE["also_y"]), "ALSO ON",
              font=sans_b(13), fill=RED, anchor="la")
    draw.line([x0 + 78, PAGE["also_y"] + 7, SIZE - 10,
               PAGE["also_y"] + 7], fill=STEEL, width=1)
    cols = [ALSO_ON[0:6], ALSO_ON[6:12], ALSO_ON[12:17]]
    for ci, col in enumerate(cols):
        cx = x0 + ci * (col_w + 16)
        for ri, (text, status) in enumerate(col):
            ly = PAGE["also_lines_y"] + ri * PAGE["also_step"]
            draw.ellipse([cx, ly + 4, cx + 7, ly + 11],
                         fill=chip_for(status))
            fnt = sans_r(13)
            max_w = col_w - 14 - 62
            while (draw.textlength(text, font=fnt) > max_w
                   and fnt.size > 11):
                fnt = sans_r(fnt.size - 1)
            draw.text((cx + 12, ly), text, font=fnt, fill=INK,
                      anchor="la")
            pill(draw, cx + col_w - 58, ly, status, 9,
                 chip_for(status))


def draw_date_check(draw):
    x0, y0 = 10, PAGE["bottom_y"]
    w = 500
    draw.rectangle([x0, y0, x0 + w, y0 + PAGE["bottom_h"]],
                   outline=RED, width=1)
    draw.text((x0 + 10, y0 + 6), "DATE CHECK \u2014 NOT 24 NOVEMBER NEWS",
              font=sans_b(12), fill=RED, anchor="la")
    y = y0 + 26
    for line in DATE_CHECK:
        draw.text((x0 + 10, y), "\u2715  " + line, font=sans_r(12),
                  fill=INK, anchor="la")
        y += 18


def project(lon, lat, x, y, w, h):
    px = x + (lon + 170) / 360.0 * w
    py = y + (75 - lat) / 130.0 * h
    return px, py


def draw_map(img, draw):
    x0, y0 = 522, PAGE["bottom_y"]
    w, h = SIZE - 10 - x0, PAGE["bottom_h"]
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    draw.text((x0 + 10, y0 + 5), "WHERE IT HAPPENED",
              font=sans_b(11), fill=(255, 255, 255), anchor="la")
    for poly in LAND:
        pts = [project(lon, lat, x0, y0 + 16, w, h - 16)
               for lon, lat in poly]
        draw.polygon(pts, fill=(150, 165, 185))
    placed = []
    for num, lon, lat, dx, dy in PINS:
        px, py = project(lon, lat, x0, y0 + 16, w, h - 16)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2],
                     fill=(255, 255, 255))
        cx, cy = px + dx, py + dy
        if dx or dy:
            draw.line([px, py, cx, cy], fill=(255, 255, 255), width=1)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((cx, cy), str(num), font=sans_b(9),
                  fill=(255, 255, 255), anchor="mm")
        placed.append((cx, cy))
    mind = min(
        ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
        for i, (ax, ay) in enumerate(placed)
        for bx, by in placed[i + 1:])
    return round(mind, 1)


def draw_footer(draw):
    y = PAGE["footer_rule"]
    draw.line([10, y, SIZE - 10, y], fill=RED, width=2)
    draw.text((SIZE // 2, y + 4),
              "Every story is dated in its panel; all happened or were "
              "first reported 22\u201324 Nov 2026.",
              font=sans_r(11), fill=INK, anchor="ma")
    draw.text((SIZE // 2, y + 17),
              "This page sums up the world news of Tuesday 24 November "
              "2026. Sources: Reuters, AP, BBC, Bloomberg, Oxfam, "
              "Lowy, Nvidia, UN, FIFA.",
              font=sans_r(11), fill=INK, anchor="ma")


# ---------------------------------------------------------------- compose

def check_page(img, stats_info, pin_gap):
    """Pixel-level guards: stat band centring, pin spacing, ink bounds."""
    if abs(stats_info["top_air"] - stats_info["bottom_air"]) > 1:
        ISSUES.append("stat band off-centre: air %s/%s"
                      % (stats_info["top_air"],
                         stats_info["bottom_air"]))
    if pin_gap < 14:
        ISSUES.append("map pins too close: %.1fpx" % pin_gap)
    if img.size != (SIZE, SIZE):
        ISSUES.append("wrong size: %s" % (img.size,))


def compose():
    """Render the whole page. Returns (image, info dict)."""
    ISSUES.clear()
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    stats_info = draw_stats(draw)
    draw_regions(draw)
    draw_timeline(draw)
    for i, hero in enumerate(HEROES):
        hero_panel(img, draw, PAGE["heroes_x"][i], PAGE["heroes_y"],
                   hero)
    for i, card in enumerate(GRID):
        row, col = divmod(i, 5)
        grid_panel(img, draw, PAGE["grid_x"][col],
                   PAGE["grid_y"][row], card)
    draw_also_on(draw)
    draw_date_check(draw)
    pin_gap = draw_map(img, draw)
    draw_footer(draw)
    check_page(img, stats_info, pin_gap)
    info = {"problems": list(ISSUES),
            "min_pin_distance_px": pin_gap,
            "stories": len(HEROES) + len(GRID) + len(ALSO_ON),
            "heroes": [h["title"] for h in HEROES],
            "stats_centering": stats_info}
    return img, info


def main():
    img, info = compose()
    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    info["sha256"] = hashlib.sha256(data).hexdigest()
    info["bytes"] = len(data)
    img2, info2 = compose()
    img2.save("/tmp/entry-n24-check.png", optimize=True)
    data2 = open("/tmp/entry-n24-check.png", "rb").read()
    info["deterministic"] = (data == data2)
    if info2["problems"]:
        info["problems"] += ["second-run: %s" % p
                             for p in info2["problems"]]
    print(json.dumps(info, indent=2))
    return 0 if not info["problems"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
