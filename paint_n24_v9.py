#!/usr/bin/env python3
"""n24 v9 painter — Tuesday 24 November 2026 in one picture.

Rebuilt in this session (v9 challenger) from the v8 painter: same 40
stories, frozen winner template — 5x2 big-type grid, 27-line ALSO ON,
11-beat UTC timeline to 21:00, DATE CHECK with 7 exclusions, region bar
summing to 40. THE TWO CHANGES — SELECTION, not discipline: (1) the
v8-vs-v7 tie flags a Gaza duplication (grid cards 4 Hamas + 9 meningitis),
so meningitis moves to ALSO ON and the PIF tower takes grid card 9;
(2) the superskie call 2 says our top tier is narrow — two Gulf/Saudi
security strikes plus a US court verdict — so the hero triptych widens:
Cartagena (Latin America, hostage crime) replaces the PIF tower as hero 3,
and Iraq oilfields take grid card 5. Same 40 stories, only rearranged.
Layout: giant serif masthead, red subhead, 7-number stat strip, 3 hero
panels with drawn scenes, 10-card grid, UTC timeline, ALSO ON, DATE CHECK,
region bar, footer. Canvas 1024x1024. Deterministic: no randomness, no
timestamps in the image.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 28
INK = (26, 26, 26)
PAPER = (247, 243, 234)
RED = (179, 32, 44)
DARKRED = (140, 20, 30)
GREY = (110, 108, 100)
LIGHT = (232, 227, 214)
MIDLINE = (200, 192, 176)
GREEN = (46, 110, 60)
AMBER = (150, 95, 20)
NAVY = (38, 62, 110)
TEAL = (24, 90, 96)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

ISSUES = []


def note(problem):
    ISSUES.append(problem)


def text_w(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def text_h(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[3] - box[1]


def wrap_lines(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, s, f, x, y, max_w, leading, fill=INK):
    lines = wrap_lines(draw, s, f, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def chip(draw, x, y, label, bg):
    f = F_SANS_B(10)
    pad = 6
    w = text_w(draw, label, f) + pad * 2
    h = 16
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def rule(draw, x, y, w, color=INK, px=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=px)


# ---------------------------------------------------------------- stories
# Every story first-reported Tue 24 Nov 2026 (UTC). Sources in dev/research.
HEROES = [
    dict(
        tag="COURT VERDICT", tag_bg=NAVY,
        title="HUAWEI GUILTY",
        body=("A US jury convicts Huawei — trade secrets, bank fraud and "
              "sanctions breaches — and clears it of racketeering."),
        scene="court",
        stat="10 of 12",
        stat_label="counts convicted",
        when="20:41 UTC",
    ),
    dict(
        tag="REPORTED", tag_bg=AMBER,
        title="HORMUZ ON FIRE",
        body=("Iran says four tankers hit naval mines in the Strait of Hormuz, "
              "and its navy attacked a container ship gone dark."),
        scene="hormuz",
        stat="4",
        stat_label="tankers hit mines*",
        when="00:00 UTC",
    ),
    dict(
        tag="REPORTED", tag_bg=AMBER,
        title="CARTAGENA SIEGE",
        body=("Gunmen seize a supermarket in Cartagena, Colombia, hold 25 "
              "people; five women freed."),
        scene="cartagena",
        stat="25",
        stat_label="hostages held",
        when="17:35 UTC",
    ),
]

GRID = [
    ("1", "DOW TOPS 50,000", "Dow closes above 50,000 for the first time, +0.9%, as tech sinks.", "MARKETS", "chart_up"),
    ("2", "NVIDIA GIVES BACK", "NVDA -5.9% to $155.38, giving back $240bn; Nasdaq -1.5%.", "MARKETS", "chart"),
    ("3", "SENEGAL WIN BACK AFCON", "Top court reinstates Senegal as champions; title stripped in March.", "COURT", "trophy"),
    ("4", "ISRAEL KILLS HAMAS CHIEF", "Air strike kills Brig-Gen. Naeem Abu Nahel in Gaza, Oct 2025 ceasefire.", "CONFIRMED", "blast"),
    ("5", "IRAQ TAKES OILFIELDS", "Baghdad orders federal control of oilfields; Kurdish PM objects.", "CONFIRMED", "derrick"),
    ("6", "TURKISH HELI CRASH", "AS-532 crashes near Eskisehir; five crew killed — second in 12 days.", "CONFIRMED", "heli"),
    ("7", "SUDAN DRONE DOWN", "Sudan's army says it shot down drones from Ethiopia in Blue Nile.", "REPORTED", "drone"),
    ("8", "WHO CHIEF VISITS CUBA", "WHO chief Tedros in Cuba pledges $2m for vaccines as system fails.", "CONFIRMED", "globe"),
    ("9", "PIF TOWER HIT", "Houthi drone hits the Saudi fund's tower in Riyadh; 11 wounded.", "REPORTED", "tower"),
    ("10", "TRUMP: IRAN 'DOABLE'", "Trump: toppling Iran's regime 'probably doable', but not his goal.", "REPORTED", "flag"),
]

ALSO_ON = [
    "UK sanctions the Houthis and four officials",
    "Houthis 60 km from Aden, ready to attack",
    "Car bomb in Villavicencio injures 23",
    "Saudi Yemen bus strikes: 25 dead, missing",
    "Gaza meningitis: 272 cases in October",
    "Congo plane missing; rebels claim shootdown",
    "Hanoi restaurant blast kills at least six",
    "Malaysia to return migrants to Myanmar",
    "Ex-PM Hasina to return to Bangladesh Dec 16",
    "Indonesia names two VP candidates",
    "China sentences official to death for spying",
    "NATO vows space defence; Libya queries Kyiv",
    "Amnesty seeks UN action on Ethiopia deaths",
    "Russian jets near Ulleungdo; shelter ordered",
    "Pentagon rebukes Canada over F-35s",
    "US blacklists Megaspeed in Nvidia scandal",
    "DOJ anti-scam surge recovers $8bn",
    "Zelensky urges four-party talks — soon",
    "Haftar visits Turkey for the first time",
    "COP31 fallout: transition package survived",
    "Progress MS-36 cargo craft launches to the ISS",
    "Australia blames minister for COP31 flop",
    "Abiy offers to host Sudan peace talks",
    "Brazil raises inflation outlook, cuts growth",
    "Kushner talks Gaza with Netanyahu",
    "Chip stocks plunge: ADI -17%, Micron -11%",
    "Bitcoin $59,500; gold -2.8%; oil $81.45",
]

TIMELINE = [
    ("00:00", "Iran: 4 tankers hit mines"),
    ("00:52", "US blacklists Megaspeed"),
    ("02:15", "NATO vows space defence"),
    ("10:13", "Progress MS-36 launches"),
    ("11:40", "Hamas security chief killed"),
    ("14:27", "PIF tower hit in Riyadh"),
    ("16:08", "Falcon 9 launches"),
    ("17:35", "Cartagena hostage siege"),
    ("18:58", "IRGC attacks container ship"),
    ("20:41", "Huawei guilty"),
    ("21:00", "Dow tops 50,000"),
]

STATS = [
    ("10 of 12", "Huawei counts convicted"),
    ("4", "tankers hit mines"),
    ("25", "hostages in Cartagena"),
    ("$240bn", "Nvidia gives back"),
    ("5", "Turkish crew killed"),
    ("50,019", "Dow tops 50,000"),
    ("60 km", "Houthis from Aden"),
]

REGIONS = [("N. AMERICA", 9), ("EUROPE", 5), ("M. EAST", 8),
           ("ASIA", 7), ("AFRICA", 6), ("S. AMERICA", 3),
           ("OCEANIA", 1), ("SPACE", 1)]

DATE_CHECK = [
    ("COP31 collapse itself", "Sun 22 Nov"),
    ("Nvidia +31% Monday", "Mon 23 Nov"),
    ("Sparta II strike", "Sat 21 Nov"),
    ("El Chapo Isidro capture", "Fri 20 Nov"),
    ("Merkury sunk off Libya", "Sun 22 Nov"),
    ("BepiColombo Mercury orbit", "Sat 21 Nov"),
    ("Trump tariff plan", "Wed 25 Nov"),
]
NOT_YET = "Not yet: Wed US trading · COP31 final text · House Nvidia hearings 1 Dec"

# ---------------------------------------------------------------- scenes
def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 68, 96))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 50, 74))
    col_w = 14
    for i in range(4):
        cx = x + 24 + i * ((w - 48 - col_w) // 3)
        d.rectangle([cx, y + 26, cx + col_w, y + h - 26], fill=(226, 220, 205))
        d.rectangle([cx - 4, y + 20, cx + col_w + 4, y + 26], fill=(226, 220, 205))
        d.rectangle([cx - 4, y + h - 32, cx + col_w + 4, y + h - 26], fill=(226, 220, 205))
    d.rectangle([x + 18, y + 8, x + w - 18, y + 20], fill=(226, 220, 205))
    # gavel: head + handle, lower right
    gx, gy = x + w - 78, y + h - 62
    d.line([(gx, gy + 34), (gx + 52, gy + 8)], fill=(196, 150, 80), width=7)
    d.rounded_rectangle([gx + 34, gy - 2, gx + 66, gy + 14], radius=4, fill=(150, 105, 55))
    d.ellipse([gx - 4, gy + 34, gx + 22, gy + 46], fill=(120, 84, 44))


def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 64, 78))
    d.rectangle([x, y, x + w, y + 42], fill=(214, 138, 62))
    d.ellipse([x + w - 66, y + 8, x + w - 22, y + 40], fill=(244, 214, 140))
    sea_y = y + h - 48
    d.rectangle([x, sea_y, x + w, y + h], fill=(10, 42, 54))
    for i in range(5):
        wx = x + 12 + i * 58
        d.arc([wx, sea_y + 8, wx + 44, sea_y + 26], 180, 360, fill=(70, 140, 150), width=3)
    # tanker: black hull + container blocks
    hx, hy = x + 34, sea_y - 26
    d.polygon([(hx, hy + 22), (hx + 8, hy), (hx + 196, hy), (hx + 210, hy + 22)],
              fill=(16, 16, 18))
    for i in range(5):
        cx = hx + 16 + i * 38
        d.rectangle([cx, hy - 20, cx + 32, hy], fill=(168, 52, 40) if i % 2 else (52, 96, 110))
    d.rectangle([hx + 176, hy - 40, hx + 196, hy], fill=(220, 220, 210))
    # smoke rising from the funnel, kept inside the scene
    d.ellipse([hx + 168, hy - 30, hx + 196, hy - 10], fill=(120, 118, 110))
    d.ellipse([hx + 180, hy - 44, hx + 204, hy - 24], fill=(150, 148, 140))
    for mx, my in ((x + w - 58, sea_y + 26), (x + 30, sea_y + 34)):
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(30, 30, 30))
        for ang in range(0, 360, 45):
            import math
            ex = mx + int(11 * math.cos(math.radians(ang)))
            ey = my + int(11 * math.sin(math.radians(ang)))
            d.line([(mx, my), (ex, ey)], fill=(30, 30, 30), width=2)


def scene_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 60, 86))
    d.rectangle([x, y, x + w, y + 30], fill=(214, 150, 90))
    d.ellipse([x + 26, y + 6, x + 58, y + 28], fill=(244, 214, 140))
    base_y = y + h
    # skyline silhouettes
    for bx, bw, bh in ((x + 6, 34, 34), (x + 46, 26, 48), (x + 228, 30, 40),
                       (x + 262, 36, 30)):
        d.rectangle([bx, base_y - bh, bx + bw, base_y], fill=(30, 36, 54))
    # the PIF tower: tall, lit windows, impact smoke mid-facade
    tx = x + w // 2 - 26
    d.rectangle([tx, y + 18, tx + 52, base_y], fill=(196, 204, 214))
    d.rectangle([tx + 22, y + 8, tx + 30, y + 18], fill=(196, 204, 214))
    for wy in range(y + 26, base_y - 8, 12):
        for wx in (tx + 8, tx + 22, tx + 36):
            d.rectangle([wx, wy, wx + 8, wy + 5], fill=(250, 210, 90))
    d.ellipse([tx + 34, y + 44, tx + 66, y + 70], fill=(120, 118, 110))
    d.ellipse([tx + 44, y + 34, tx + 68, y + 54], fill=(150, 148, 140))
    d.ellipse([tx + 30, y + 52, tx + 44, y + 66], fill=(232, 130, 30))
    # small drone with trail, upper right
    dx, dy = x + w - 52, y + 34
    d.line([(dx + 18, dy + 12), (dx, dy)], fill=(240, 240, 235), width=2)
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(20, 20, 20))
    d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(232, 130, 30))


def scene_cartagena(d, x, y, w, h):
    # dusk street, supermarket front with striped awning, police tape
    d.rectangle([x, y, x + w, y + h], fill=(214, 150, 90))
    d.ellipse([x + w - 52, y + 8, x + w - 20, y + 32], fill=(244, 214, 140))
    # side buildings
    d.rectangle([x, y + 34, x + 34, y + h], fill=(30, 36, 54))
    d.rectangle([x + w - 34, y + 28, x + w, y + h], fill=(30, 36, 54))
    # shopfront
    sx, sw = x + 34, w - 68
    d.rectangle([sx, y + 26, sx + sw, y + h], fill=(232, 227, 214))
    # awning stripes
    n = 8
    aw = sw // n
    for i in range(n):
        d.rectangle([sx + i * aw, y + 26, sx + (i + 1) * aw, y + 40],
                    fill=RED if i % 2 == 0 else (255, 255, 255))
    # warm lit windows, dark door
    d.rectangle([sx + 12, y + 48, sx + 52, y + 76], fill=(250, 210, 90))
    d.rectangle([sx + sw - 52, y + 48, sx + sw - 12, y + 76], fill=(250, 210, 90))
    d.rectangle([sx + sw // 2 - 14, y + 48, sx + sw // 2 + 14, y + h],
                fill=(38, 50, 74))
    # police tape across the front
    ty = y + h - 14
    d.rectangle([x, ty, x + w, ty + 10], fill=(240, 200, 40))
    for tx in range(x + 4, x + w - 6, 14):
        d.line([(tx, ty + 10), (tx + 8, ty)], fill=(20, 20, 20), width=2)


SCENES = {"court": scene_court, "hormuz": scene_hormuz, "tower": scene_tower,
          "cartagena": scene_cartagena}


# ---------------------------------------------------------------- grid icons
# Small pictograms for the 10 grid cards, drawn in a 32x32 box at (ox, oy).
def icon_chart(d, ox, oy):
    d.line([(ox + 3, oy + 28), (ox + 3, oy + 4)], fill=INK, width=2)
    d.line([(ox + 3, oy + 28), (ox + 29, oy + 28)], fill=INK, width=2)
    d.line([(ox + 5, oy + 8), (ox + 12, oy + 14), (ox + 18, oy + 12),
            (ox + 24, oy + 22), (ox + 29, oy + 26)], fill=RED, width=3)


def icon_chart_up(d, ox, oy):
    d.line([(ox + 3, oy + 28), (ox + 3, oy + 4)], fill=INK, width=2)
    d.line([(ox + 3, oy + 28), (ox + 29, oy + 28)], fill=INK, width=2)
    d.line([(ox + 5, oy + 24), (ox + 12, oy + 18), (ox + 18, oy + 20),
            (ox + 24, oy + 10), (ox + 29, oy + 6)], fill=GREEN, width=3)
    d.polygon([(ox + 25, oy + 4), (ox + 30, oy + 4), (ox + 29, oy + 9)],
              fill=GREEN)


def icon_flag(d, ox, oy):
    d.line([(ox + 8, oy + 3), (ox + 8, oy + 30)], fill=INK, width=2)
    d.polygon([(ox + 8, oy + 4), (ox + 27, oy + 9), (ox + 8, oy + 15)],
              fill=RED)
    d.ellipse([ox + 5, oy + 28, ox + 11, oy + 31], fill=INK)


def icon_tower(d, ox, oy):
    d.rectangle([ox + 10, oy + 10, ox + 22, oy + 30], fill=INK)
    d.line([(ox + 16, oy + 10), (ox + 16, oy + 3)], fill=INK, width=2)
    for wy in (14, 19, 24):
        d.rectangle([ox + 13, wy, ox + 19, wy + 3], fill=PAPER)


def icon_trophy(d, ox, oy):
    d.polygon([(ox + 8, oy + 6), (ox + 24, oy + 6), (ox + 22, oy + 16),
               (ox + 10, oy + 16)], fill=(176, 132, 32))
    d.arc([ox + 3, oy + 6, ox + 10, oy + 14], 90, 270, fill=(176, 132, 32), width=2)
    d.arc([ox + 22, oy + 6, ox + 29, oy + 14], 270, 90, fill=(176, 132, 32), width=2)
    d.rectangle([ox + 14, oy + 16, ox + 18, oy + 24], fill=(176, 132, 32))
    d.rectangle([ox + 10, oy + 24, ox + 22, oy + 28], fill=(176, 132, 32))


def icon_blast(d, ox, oy):
    import math
    cx, cy = ox + 16, oy + 16
    pts = []
    for k in range(16):
        ang = math.radians(k * 22.5 - 90)
        r = 13 if k % 2 == 0 else 6
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(232, 130, 30))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(250, 210, 90))


def icon_shop(d, ox, oy):
    d.rectangle([ox + 4, oy + 12, ox + 28, oy + 30], fill=INK)
    d.polygon([(ox + 3, oy + 12), (ox + 29, oy + 12), (ox + 26, oy + 5),
               (ox + 6, oy + 5)], fill=RED)
    d.rectangle([ox + 13, oy + 20, ox + 19, oy + 30], fill=PAPER)


def icon_heli(d, ox, oy):
    d.ellipse([ox + 6, oy + 12, ox + 24, oy + 22], fill=INK)
    d.polygon([(ox + 22, oy + 15), (ox + 30, oy + 12), (ox + 30, oy + 18),
               (ox + 22, oy + 19)], fill=INK)
    d.line([(ox + 4, oy + 8), (ox + 28, oy + 8)], fill=INK, width=3)
    d.line([(ox + 8, oy + 26), (ox + 22, oy + 26)], fill=INK, width=2)


def icon_pin(d, ox, oy):
    d.ellipse([ox + 8, oy + 4, ox + 24, oy + 20], fill=RED)
    d.ellipse([ox + 12, oy + 8, ox + 20, oy + 16], fill=PAPER)
    d.polygon([(ox + 11, oy + 18), (ox + 21, oy + 18), (ox + 16, oy + 30)],
              fill=RED)


def icon_derrick(d, ox, oy):
    d.line([(ox + 8, oy + 30), (ox + 14, oy + 6)], fill=INK, width=2)
    d.line([(ox + 24, oy + 30), (ox + 18, oy + 6)], fill=INK, width=2)
    d.line([(ox + 10, oy + 22), (ox + 22, oy + 22)], fill=INK, width=2)
    d.line([(ox + 12, oy + 14), (ox + 20, oy + 14)], fill=INK, width=2)
    d.ellipse([ox + 13, oy + 1, ox + 19, oy + 7], fill=(232, 130, 30))


def icon_cuffs(d, ox, oy):
    d.ellipse([ox + 4, oy + 10, ox + 14, oy + 20], outline=INK, width=3)
    d.ellipse([ox + 18, oy + 10, ox + 28, oy + 20], outline=INK, width=3)
    d.line([(ox + 14, oy + 15), (ox + 18, oy + 15)], fill=INK, width=2)


def icon_cross(d, ox, oy):
    d.ellipse([ox + 4, oy + 4, ox + 28, oy + 28], fill=RED)
    d.rectangle([ox + 13, oy + 9, ox + 19, oy + 23], fill=PAPER)
    d.rectangle([ox + 9, oy + 13, ox + 23, oy + 19], fill=PAPER)


def icon_drone(d, ox, oy):
    d.rectangle([ox + 12, oy + 13, ox + 20, oy + 19], fill=INK)
    for cx, cy in ((ox + 6, oy + 8), (ox + 26, oy + 8),
                   (ox + 6, oy + 24), (ox + 26, oy + 24)):
        d.line([(ox + 16, oy + 16), (cx, cy)], fill=INK, width=2)
        d.ellipse([cx - 4, cy - 2, cx + 4, cy + 2], outline=INK, width=2)


def icon_globe(d, ox, oy):
    d.ellipse([ox + 5, oy + 5, ox + 27, oy + 27], outline=INK, width=2)
    d.ellipse([ox + 11, oy + 5, ox + 21, oy + 27], outline=INK, width=1)
    d.line([(ox + 5, oy + 16), (ox + 27, oy + 16)], fill=INK, width=1)


ICONS = {"chart": icon_chart, "chart_up": icon_chart_up, "flag": icon_flag,
         "tower": icon_tower, "trophy": icon_trophy,
         "blast": icon_blast, "shop": icon_shop, "heli": icon_heli,
         "pin": icon_pin, "derrick": icon_derrick, "cuffs": icon_cuffs,
         "cross": icon_cross, "drone": icon_drone, "globe": icon_globe}


# ---------------------------------------------------------------- layout
def paint_header(d):
    y = 16
    f_kick = F_SANS_B(13)
    kick = "TUESDAY  ·  THE WORLD IN ONE PICTURE  ·  40 STORIES"
    kw = text_w(d, kick, f_kick)
    d.text(((W - kw) / 2, y), kick, font=f_kick, fill=GREY)
    y += 26
    f_mast = F_SERIF_B(68)
    mast = "24 NOVEMBER 2026"
    mw = text_w(d, mast, f_mast)
    if mw > W - 2 * MARGIN:
        note("masthead too wide: %d" % mw)
    d.text(((W - mw) / 2, y), mast, font=f_mast, fill=INK)
    y += 84
    rule(d, MARGIN, y, W - 2 * MARGIN, RED, 3)
    y += 10
    f_sub = F_SANS_B(17)
    sub = "HUAWEI GUILTY  ·  HORMUZ TANKERS HIT  ·  CARTAGENA SIEGE"
    sw = text_w(d, sub, f_sub)
    if sw > W - 2 * MARGIN:
        note("subhead too wide: %d" % sw)
    d.text(((W - sw) / 2, y), sub, font=f_sub, fill=RED)
    y += 26
    return y


def paint_stats(d, y):
    n = len(STATS)
    cell_w = (W - 2 * MARGIN) // n
    top = y
    for i, (num, label) in enumerate(STATS):
        x0 = MARGIN + i * cell_w
        d.rectangle([x0 + 2, top, x0 + cell_w - 2, top + 36], outline=MIDLINE, width=1)
        f_num = F_SERIF_B(20)
        f_lab = F_SANS(10)
        nw = text_w(d, num, f_num)
        d.text((x0 + (cell_w - nw) / 2, top + 2), num, font=f_num, fill=RED)
        lw = text_w(d, label, f_lab)
        if lw > cell_w - 8:
            note("stat label too wide: %s" % label)
        d.text((x0 + (cell_w - lw) / 2, top + 22), label, font=f_lab, fill=GREY)
    return top + 36 + 8


def paint_heroes(d, y):
    n = 3
    gap = 10
    cw = (W - 2 * MARGIN - gap * (n - 1)) // n
    ch = 232
    scene_h = 100
    for i, hero in enumerate(HEROES):
        x0 = MARGIN + i * (cw + gap)
        d.rectangle([x0, y, x0 + cw, y + ch], outline=INK, width=2)
        SCENES[hero["scene"]](d, x0 + 2, y + 2, cw - 4, scene_h)
        d.rectangle([x0, y + scene_h, x0 + cw, y + scene_h + 22], fill=RED)
        f_ban = F_SANS_B(12)
        ban = hero["title"]
        bw = text_w(d, ban, f_ban)
        if bw > cw - 16:
            note("hero banner too wide: %s" % ban)
        d.text((x0 + (cw - bw) / 2, y + scene_h + 4), ban, font=f_ban, fill=(255, 255, 255))
        ty = y + scene_h + 30
        chip(d, x0 + 8, ty, hero["tag"], hero["tag_bg"])
        f_when = F_SANS_B(11)
        d.text((x0 + cw - 8 - text_w(d, hero["when"], f_when), ty + 2),
               hero["when"], font=f_when, fill=GREY)
        ty += 24
        f_body = F_SANS(12)
        ty = draw_wrapped(d, hero["body"], f_body, x0 + 8, ty, cw - 16, 16)
        f_stat = F_SERIF_B(15)
        stat_line = "%s — %s" % (hero["stat"], hero["stat_label"])
        d.text((x0 + 8, y + ch - 22), stat_line, font=f_stat, fill=RED)
        if ty > y + ch - 26:
            note("hero %d body overflows" % i)
    return y + ch + 10


def paint_grid(d, y):
    cols, rows = 5, 2
    gap_x, gap_y = 10, 8
    cw = (W - 2 * MARGIN - gap_x * (cols - 1)) // cols
    ch = 118
    f_tit = F_SANS_B(20)
    f_bod = F_SANS(13)
    f_tag = F_SANS_B(9)
    for idx, (num, title, body, tag, icon) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (cw + gap_x)
        y0 = y + r * (ch + gap_y)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], outline=MIDLINE, width=1)
        # pictogram row: icon left, per-story number, tag chip right
        ICONS[icon](d, x0 + 6, y0 + 2)
        f_num = F_SANS_B(18)
        d.text((x0 + 42, y0 + 6), num, font=f_num, fill=RED)
        tag_w = text_w(d, tag, f_tag) + 10
        d.rounded_rectangle([x0 + cw - tag_w - 6, y0 + 6, x0 + cw - 6, y0 + 20],
                            radius=3, fill=LIGHT)
        d.text((x0 + cw - tag_w - 1, y0 + 8), tag, font=f_tag, fill=GREY)
        # title, max 2 lines at 20px bold
        tlines = wrap_lines(d, title, f_tit, cw - 16)
        if len(tlines) > 2:
            note("grid title too long: %s" % title)
        ty = y0 + 34
        for ln in tlines[:2]:
            d.text((x0 + 8, ty), ln, font=f_tit, fill=INK)
            ty += 20
        # body, max 3 lines at 13px
        blines = wrap_lines(d, body, f_bod, cw - 16)
        if len(blines) > 3:
            note("grid body too long: %s" % body)
        by = y0 + 76
        for ln in blines[:3]:
            d.text((x0 + 8, by), ln, font=f_bod, fill=INK)
            by += 14
    return y + rows * ch + (rows - 1) * gap_y + 6

def paint_timeline(d, y):
    f_head = F_SANS_B(12)
    head = "THE DAY IN UTC — TUESDAY 24 NOVEMBER 2026"
    d.text((MARGIN, y), head, font=f_head, fill=INK)
    y += 18
    x0, x1 = MARGIN, W - MARGIN
    d.line([(x0, y + 8), (x1, y + 8)], fill=INK, width=2)
    n = len(TIMELINE)
    for i, (hhmm, label) in enumerate(TIMELINE):
        cx = x0 + int((i + 0.5) * (x1 - x0) / n)
        d.ellipse([cx - 4, y + 4, cx + 4, y + 12], fill=RED)
        f_t = F_SANS_B(10)
        tw = text_w(d, hhmm, f_t)
        d.text((cx - tw / 2, y + 16), hhmm, font=f_t, fill=INK)
        f_l = F_SANS(9)
        # label: wrap to two short lines, centred on the tick
        words = label.split()
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if text_w(d, trial, f_l) <= 92:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        ly = y + 28
        for ln in lines[:2]:
            lw = text_w(d, ln, f_l)
            d.text((cx - lw / 2, ly), ln, font=f_l, fill=GREY)
            ly += 11
        if len(lines) > 2:
            note("timeline label too long: %s" % label)
    return y + 52


def paint_also_on(d, y):
    f_head = F_SANS_B(12)
    d.text((MARGIN, y), "ALSO ON — TUESDAY 24 NOVEMBER", font=f_head, fill=INK)
    y += 18
    cols = 3
    gap = 12
    cw = (W - 2 * MARGIN - gap * (cols - 1)) // cols
    f_item = F_SANS(13)
    per_col = 9
    for i, item in enumerate(ALSO_ON):
        c, r = divmod(i, per_col)
        x0 = MARGIN + c * (cw + gap)
        y0 = y + r * 14
        d.ellipse([x0, y0 + 3, x0 + 5, y0 + 8], fill=RED)
        line = item
        if text_w(d, line, f_item) > cw - 10:
            note("ALSO ON too wide: %s" % item)
        d.text((x0 + 9, y0), line, font=f_item, fill=INK)
    return y + per_col * 14 + 4


def paint_bottom(d, y):
    # DATE CHECK (left) + region bar (right), then the footer line.
    box_w = 700
    d.rectangle([MARGIN, y, MARGIN + box_w, y + 64], outline=INK, width=1)
    f_head = F_SANS_B(11)
    d.text((MARGIN + 8, y + 5), "DATE CHECK — LEFT OUT ON PURPOSE", font=f_head, fill=RED)
    f_dc = F_SANS(10)
    col_w = (box_w - 16) // 3
    for i, (what, when) in enumerate(DATE_CHECK):
        c = i % 3
        r = i // 3
        x0 = MARGIN + 8 + c * col_w
        y0 = y + 21 + r * 13
        line = "%s — %s" % (what, when)
        if text_w(d, line, f_dc) > col_w - 8:
            note("DATE CHECK too wide: %s" % line)
        d.text((x0, y0), line, font=f_dc, fill=INK)
    # region bar
    rx = MARGIN + box_w + 14
    rw = W - MARGIN - rx
    d.text((rx, y + 5), "WHERE THE 40 STORIES COME FROM", font=f_head, fill=INK)
    total = sum(v for _, v in REGIONS)
    if total != 40:
        note("region total is %d, not 40" % total)
    bx, by = rx, y + 22
    bar_w = rw
    for name, val in REGIONS:
        seg = int(bar_w * val / total)
        d.rectangle([bx, by, bx + seg - 1, by + 12], fill=RED)
        bx += seg
    f_rg = F_SANS(10)
    labels = ["  ".join("%s %d" % (n, v) for n, v in REGIONS[:4]),
              "  ".join("%s %d" % (n, v) for n, v in REGIONS[4:])]
    ly = by + 17
    for ln in labels:
        d.text((rx, ly), ln, font=f_rg, fill=INK)
        ly += 12
    return y + 64 + 6


def paint_footer(d, y):
    f_f = F_SANS(9)
    line1 = ("This page sums up the world news of Tuesday 24 November 2026. "
             "Every story first reported 24 Nov 2026 (UTC); times in UTC. "
             "*JMIC: mine claims unconfirmed.")
    line2 = (NOT_YET + " — Sources: Daily Summary Of · NASA · RenewEconomy · "
             "MercoPress · ENA · Reuters · AP · Investopedia · CNN.")
    for ln in (line1, line2):
        lw = text_w(d, ln, f_f)
        if lw > W - 2 * MARGIN:
            note("footer too wide: %d" % lw)
        d.text(((W - lw) / 2, y), ln, font=f_f, fill=GREY)
        y += 12
    return y


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = paint_header(d)
    y = paint_stats(d, y)
    y = paint_heroes(d, y)
    y = paint_grid(d, y)
    y = paint_timeline(d, y)
    y = paint_also_on(d, y)
    y = paint_bottom(d, y)
    y = paint_footer(d, y)
    if y > H - 4:
        note("page overflows: final y=%d" % y)
    img.save(OUT, optimize=True)
    print("saved %s (%d bytes), final y=%d" % (OUT, os.path.getsize(OUT), y))
    if ISSUES:
        print("LAYOUT ISSUES (%d):" % len(ISSUES))
        for it in ISSUES:
            print(" -", it)
        raise SystemExit(2)
    print("layout OK, no issues")


if __name__ == "__main__":
    build()
