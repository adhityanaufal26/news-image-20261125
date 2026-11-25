#!/usr/bin/env python3
"""Draw the 25 November 2026 news front page (1024x1024 PNG).

Deterministic: fixed strings, fixed geometry, no timestamps, no randomness,
no network. Run: python3 build_image.py  ->  entry.png next to this file.
All facts come from ../news-image-20261125-research.md (sources cited there).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 24, 34)
NAVY = (14, 42, 71)
RED = (178, 34, 34)
BLUE = (24, 84, 150)
AMBER = (176, 110, 8)
GREY = (90, 96, 104)
LIGHT = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_OB = lambda s: font("DejaVuSerif.ttf", s)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, fnt, color, lh=None):
    lh = lh or int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def chip(d, x, y, text, bg, fg=LIGHT):
    f = SANS_B(11)
    w = int(d.textlength(text, font=f) + 14)
    d.rounded_rectangle([x, y, x + w, y + 18], 9, fill=bg)
    d.text((x + 7, y + 3), text, font=f, fill=fg)
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 88], fill=NAVY)
d.rectangle([0, 88, W, 92], fill=RED)
d.text((16, 10), "THE WORLD IN ONE PICTURE", font=SERIF_B(40), fill=LIGHT)
d.text((16, 58), "Wednesday 25 November 2026  ·  15 stories  ·  compiled 02:45 UTC",
       font=SANS(16), fill=(200, 212, 226))
d.text((W - 16, 58), "make.fun daily news-image", font=SANS_OB(13),
       fill=(160, 175, 195), anchor="ra")

# ---------- lead cards ----------
LEADS = [
    dict(x=12, band=RED, kicker="CYBERATTACK · WASHINGTON",
         head="CIA AND SPY CHIEF'S OFFICE HIT BY HACK",
         deck="Unclassified open-source intel system breached; no classified data hit. Early signs point to China — unconfirmed.",
         tag="TUE 24 NOV", icon="server"),
    dict(x=351, band=BLUE, kicker="PACIFIC · HONIARA",
         head="CANBERRA WINS THE SOLOMONS",
         deck="Australia signs a security pact; Canberra is the Solomons' new defence partner.",
         tag="WED 25 NOV", icon="shield"),
    dict(x=690, band=AMBER, kicker="SAUDI ARABIA · RIYADH",
         head="HOUTHI DRONE HITS RIYADH'S TALLEST TOWER",
         deck="Second strike on the PIF tower in under a week wounds 11 — two Saudis, two Indians, three Nepalese, four Egyptians.",
         tag="TUE 24 NOV", icon="tower"),
]
for L in LEADS:
    x = L["x"]
    d.rounded_rectangle([x, 100, x + 322, 330], 6, fill=CARD, outline=LINE, width=1)
    d.rounded_rectangle([x, 100, x + 322, 178], 6, fill=L["band"])
    d.rectangle([x, 160, x + 322, 178], fill=L["band"])
    # icons, drawn with shapes
    cx = x + 161
    if L["icon"] == "server":
        d.rectangle([cx - 42, 112, cx + 42, 166], outline=LIGHT, width=3)
        for yy in (122, 138, 154):
            d.line([cx - 34, yy, cx + 20, yy], fill=LIGHT, width=3)
            d.ellipse([cx + 28, yy - 3, cx + 34, yy + 3], fill=LIGHT)
        d.polygon([(cx + 52, 118), (cx + 66, 142), (cx + 38, 142)], fill=(255, 210, 60))
        d.text((cx + 50, 124), "!", font=SANS_B(16), fill=RED, anchor="mm")
    elif L["icon"] == "shield":
        d.polygon([(cx, 108), (cx + 44, 120), (cx + 44, 146), (cx, 170),
                   (cx - 44, 146), (cx - 44, 120)], outline=LIGHT, width=3)
        d.line([cx - 20, 140, cx - 6, 154, cx + 22, 126], fill=LIGHT, width=5)
    else:  # tower
        d.polygon([(cx - 26, 168), (cx - 14, 112), (cx + 14, 112), (cx + 26, 168)],
                  outline=LIGHT, width=3)
        for yy in (126, 140, 154):
            d.line([cx - 20, yy, cx + 20, yy], fill=LIGHT, width=2)
        for ang in range(0, 360, 45):
            import math
            r1, r2 = 8, 20
            a = math.radians(ang)
            d.line([cx + 52 + r1 * math.cos(a), 122 + r1 * math.sin(a),
                    cx + 52 + r2 * math.cos(a), 122 + r2 * math.sin(a)],
                   fill=(255, 210, 60), width=3)
        d.ellipse([cx + 44, 114, cx + 60, 130], fill=(255, 210, 60))
    d.text((x + 12, 188), L["kicker"], font=SANS_B(12), fill=L["band"])
    y = block(d, x + 12, 206, wrap(d, L["head"], SANS_B(19), 298), SANS_B(19), INK, 23)
    block(d, x + 12, y + 4, wrap(d, L["deck"], SANS(13), 298), SANS(13), (52, 58, 66), 16)
    chip(d, x + 12, 306, L["tag"], INK)

# ---------- map strip ----------
d.rounded_rectangle([12, 338, 1012, 470], 6, fill=CARD, outline=LINE, width=1)
d.text((24, 346), "WHERE IT HAPPENED", font=SANS_B(14), fill=NAVY)
d.text((24, 364), "8 places behind today's stories", font=SANS(11), fill=GREY)

MAP_X, MAP_Y, MAP_W, MAP_H = 24, 386, 560, 78


def proj(lon, lat):
    return (MAP_X + (lon + 180) / 360.0 * MAP_W,
            MAP_Y + (90 - lat) / 180.0 * MAP_H)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 70), (-55, 76), (-65, 70)],
    [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-50, -30), (-60, -40),
     (-70, -50), (-73, -40), (-75, -25), (-80, -15)],
    [(-10, 35), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 10),
     (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25), (12, -10),
     (8, 4), (-8, 5), (-15, 25)],
    [(-10, 36), (-5, 43), (0, 46), (5, 50), (10, 55), (15, 58), (20, 60), (25, 65),
     (30, 70), (40, 68), (45, 60), (40, 50), (30, 45), (20, 40), (15, 38), (10, 38),
     (0, 40)],
    [(40, 68), (60, 70), (80, 73), (100, 75), (120, 73), (140, 72), (160, 70),
     (178, 66), (170, 60), (160, 55), (150, 45), (140, 40), (130, 35), (127, 35),
     (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 15),
     (75, 8), (70, 20), (60, 25), (55, 28), (50, 30), (45, 30), (40, 35)],
    [(113, -22), (120, -15), (130, -12), (140, -15), (145, -20), (150, -25),
     (153, -30), (150, -37), (140, -38), (130, -32), (120, -34), (113, -30)],
]
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(214, 230, 240))
for poly in CONTINENTS:
    d.polygon([proj(lo, la) for lo, la in poly], fill=(168, 178, 158),
              outline=(120, 130, 112))
PINS = [
    (-77, 39, "Washington — CIA hack"),
    (-96, 44, "Iowa — Army blast"),
    (50, 22, "Riyadh — tower strike"),
    (33, 33, "Gaza — death toll"),
    (27, -2, "Akwe, DRC — WHO flees"),
    (160, -9, "Honiara — pact signed"),
    (-74, 41, "New York — Huawei verdict"),
    (22, 60, "Gulf of Finland — ship hit"),
]
for i, (lo, la, _label) in enumerate(PINS, 1):
    px, py = proj(lo, la)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=LIGHT, width=2)
    d.text((px, py), str(i), font=SANS_B(9), fill=LIGHT, anchor="mm")
LEGEND = [p[2] for p in PINS]
for i, label in enumerate(LEGEND):
    col, row = divmod(i, 4)
    lx = 604 + col * 204
    ly = 386 + row * 20
    d.ellipse([lx, ly + 2, lx + 13, ly + 15], fill=RED)
    d.text((lx + 6, ly + 8), str(i + 1), font=SANS_B(9), fill=LIGHT, anchor="mm")
    d.text((lx + 18, ly + 1), label, font=SANS(11), fill=INK)

# ---------- day in numbers ----------
d.text((16, 480), "THE DAY IN NUMBERS", font=SANS_B(14), fill=NAVY)
NUMS = [
    ("11", "WOUNDED IN RIYADH DRONE STRIKE"),
    ("10,000 lbs", "LEAD AZIDE TO BE BLOWN UP IN IOWA"),
    ("−5.9%", "NVIDIA, AS ASIAN STOCKS SLIDE"),
    ("74,746", "GAZA DEATH TOLL, SAYS WAFA"),
    ("266m", "FACE ACUTE FOOD INSECURITY (WFP)"),
]
for i, (big, small) in enumerate(NUMS):
    x = 12 + i * 202
    d.rounded_rectangle([x, 502, x + 194, 556], 6, fill=NAVY)
    d.text((x + 97, 510), big, font=SANS_B(22), fill=LIGHT, anchor="ma")
    d.text((x + 97, 536), small, font=SANS_B(8), fill=(190, 202, 216), anchor="ma")

# ---------- mid cards ----------
MIDS = [
    ("MARKETS · WED", RED, "Asia slides on new tariff threats",
     "Seoul −5.3%, Taipei −5.1%, Nikkei −2.9%. Brent $90.97; Bitcoin $59,258. US core PCE data due today."),
    ("HUAWEI · TUE", BLUE, "Huawei guilty on 10 of 12 counts",
     "New York jury convicts on bank fraud and trade-secret theft after a 3-month trial. Huawei rejects the verdicts."),
    ("IOWA · WED", AMBER, "Army to blast 10,000 lbs of explosives",
     "Unstable lead azide, 68 barrels, detonated Wed morning at the Iowa Army Ammunition Plant. Evacuations urged."),
    ("UKRAINE · WED", RED, "Zelenskiy owns Gulf of Finland strike",
     "Kyiv confirms it hit a Russian cargo ship; Norway urges caution. Moscow calls ship attacks “terrorism”."),
    ("EBOLA · WED", BLUE, "WHO flees fighting in Ebola zone",
     "Staff evacuated from Akwe hospital, DRC, after 3 days sheltering. Outbreak: 5,775 dead of 11,762 cases."),
    ("SPORT · TUE", AMBER, "Real Madrid hit five; England level T20s",
     "Madrid 5–1 PSV, City 2–2 Napoli, Arsenal 1–1 Dortmund. England beat Australia by 8 wickets."),
]
for i, (kick, col, head, body) in enumerate(MIDS):
    col_i, row_i = divmod(i, 3)
    x = 12 + col_i * 506
    y = 566 + row_i * 92
    d.rounded_rectangle([x, y, x + 494, y + 86], 6, fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y + 6, x + 5, y + 80], fill=col)
    d.text((x + 14, y + 7), kick, font=SANS_B(11), fill=col)
    yy = block(d, x + 14, y + 24, wrap(d, head, SANS_B(16), 466), SANS_B(16), INK, 19)
    block(d, x + 14, yy + 2, wrap(d, body, SANS(12), 466), SANS(12), (52, 58, 66), 15)

# ---------- briefs ----------
d.text((16, 850), "ALSO TODAY", font=SANS_B(14), fill=NAVY)
BRIEFS = [
    ("GAZA", "Toll reaches 74,746; WFP says 266m face acute hunger."),
    ("IRAN", "Katz: Tehran building chemical arms; Israel “will not allow it”."),
    ("USA", "Trump gives Giuliani the Medal of Freedom; pardons two turkeys."),
    ("FRANCE", "Sarkozy corruption case sent to trial; hearing 1 Apr 2027."),
    ("USA", "Fort Hood gunman Hasan seeks stay of execution due next week."),
    ("TONIGHT", "UCL: PSG–Roma, Sporting–Man Utd, Lille–Bayern; Dell lifts outlook."),
]
for i, (kick, text) in enumerate(BRIEFS):
    col_i, row_i = divmod(i, 3)
    x = 16 + col_i * 506
    y = 872 + row_i * 30
    d.text((x, y), kick + " — ", font=SANS_B(12), fill=RED)
    kw = d.textlength(kick + " — ", font=SANS_B(12))
    d.text((x + kw, y), text, font=SANS(12), fill=INK)

# ---------- footer ----------
d.rectangle([0, 968, W, H], fill=NAVY)
d.text((16, 976), "Sources: Reuters · CNN · AFP · UEFA · WHO · US Dept. of Justice · Saudi Civil Defense · WAFA · WFP",
       font=SANS(12), fill=(200, 212, 226))
d.text((16, 996), "Dates: TUE = Tue 24 Nov · WED = Wed 25 Nov 2026. Full research notes kept with the entry.",
       font=SANS(12), fill=(160, 175, 195))

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
