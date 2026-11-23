#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Built 23 Nov 2026 for make.fun bounty news-image-20261122.
Same newspaper layout as the 20261120 entry (proven format), but all
content is the NEW day's news, fact-checked 23 Nov 2026 against:
OneTurn (oneturn.news), Open Chronicle, AP wire via KIRO 7, Euronews,
Reuters (BepiColombo), Europe Says / Kyiv Independent live blog,
Al Jazeera / BBC (El Chapo Isidro), NEMA via Emirates News Agency.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (15, 42, 68)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREY = (90, 90, 90)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((32, 18), "THE WORLD IN ONE DAY", font=font(FB, 62), fill=(255, 255, 255))
d.text((32, 96), "SUNDAY  -  22 NOVEMBER 2026", font=font(FB, 40), fill=GOLD)
d.line([0, 148, W, 148], fill=GOLD, width=6)

# ---- lead story: COP31 collapses ----
d.rectangle([24, 168, 1000, 488], outline=INK, width=3)
d.rectangle([24, 168, 1000, 206], fill=RED)
d.text((40, 174), "LEAD STORY  -  CLIMATE SUMMIT COLLAPSES", font=font(FB, 26), fill=(255, 255, 255))
yy = 222
for line in ["COP31 ends with", "no deal as talks", "fail on fossil fuels"]:
    d.text((40, yy), line, font=font(FB, 42), fill=INK)
    yy += 48
text_block(d, 40, 372, "EU and others reject a text with no mention of fossil "
           "fuels. The Antalya summit closes two days late with no "
           "agreement from nearly 200 countries.",
           font(FR, 23), INK, 600, 28)
# lead illustration: globe with a red crack / no-deal slash
cx, cy, r = 818, 337, 105
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 60, 90))
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=4)
d.ellipse([cx - 34, cy - r, cx + 34, cy + r], outline=(120, 200, 220), width=3)
d.line([cx - r, cy, cx + r, cy], fill=(120, 200, 220), width=3)
d.ellipse([cx - 88, cy - 70, cx - 18, cy - 6], fill=(60, 160, 90))
d.ellipse([cx + 8, cy + 22, cx + 82, cy + 82], fill=(60, 160, 90))
d.line([cx - 74, cy + 74, cx + 74, cy - 74], fill=RED, width=12)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=8)
d.text((668, 448), "NO DEAL", font=font(FB, 30), fill=RED)

# ---- six story cells, 2 cols x 3 rows ----
cells = [
    ("WAR AT SEA", NAVY, "Ukrainian sea drones\nstrike Russian warship",
     "Corvette Merkury badly damaged at Benghazi, Libya; a cargo ship also hit.", "ship"),
    ("WAR IN EUROPE", RED, "Russian strike flattens\nKyiv apartment block",
     "Dymer, near Kyiv: at least 3 killed, people trapped under the rubble.", "rubble"),
    ("POLITICS", (60, 40, 110), "Democrats win 258\nHouse seats",
     "Largest US House majority for any party since 1992.", "ballot"),
    ("SPACE", (10, 60, 90), "BepiColombo reaches\nMercury after 8 years",
     "ESA-JAXA probe enters orbit; thruster glitch, craft safe.", "planet"),
    ("JUSTICE", (120, 40, 40), "Mexico captures\n'El Chapo Isidro'",
     "FBI Most Wanted cartel boss seized in Sinaloa; 11 killed in raid.", "badge"),
    ("DISASTER", TEAL, "Candy factory fire kills\n3 in Indonesia",
     "Blaze at Cikande, Banten; dozens of workers still missing.", "flame"),
]

CELL_W, CELL_H = 478, 148
X0, Y0 = 24, 508
GAP = 14


def pictogram(cx, cy, kind):
    if kind == "ship":
        d.polygon([(cx - 42, cy + 6), (cx + 42, cy + 6), (cx + 30, cy + 30),
                   (cx - 30, cy + 30)], fill=INK)
        d.rectangle([cx - 18, cy - 18, cx + 6, cy + 6], fill=INK)
        d.line([cx - 30, cy - 18, cx - 30, cy - 2], fill=INK, width=3)
        d.line([cx - 40, cy + 34, cx - 20, cy + 26, cx, cy + 34,
                cx + 20, cy + 26, cx + 40, cy + 34], fill=TEAL, width=3)
        for sx, sy in [(cx + 18, cy - 34)]:
            for k in range(8):
                ang = k * math.pi / 4
                d.line([sx, sy, sx + 18 * math.cos(ang),
                        sy + 18 * math.sin(ang)], fill=(255, 180, 60), width=3)
            d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 220, 100))
    elif kind == "rubble":
        d.polygon([(cx - 40, cy + 30), (cx - 40, cy - 10), (cx - 14, cy - 34),
                   (cx + 6, cy - 14), (cx + 22, cy - 30), (cx + 40, cy - 6),
                   (cx + 40, cy + 30)], fill=(70, 70, 70))
        d.line([cx - 40, cy + 30, cx + 40, cy + 30], fill=INK, width=4)
        d.line([cx - 26, cy + 30, cx - 14, cy + 14, cx + 2, cy + 30,
                cx + 16, cy + 18, cx + 30, cy + 30], fill=RED, width=3)
    elif kind == "ballot":
        d.rectangle([cx - 34, cy - 20, cx + 34, cy + 30], outline=INK, width=4)
        d.rectangle([cx - 14, cy - 34, cx + 14, cy - 20], outline=INK, width=4)
        d.line([cx - 22, cy + 4, cx - 6, cy + 18, cx + 26, cy - 14],
               fill=RED, width=6)
    elif kind == "planet":
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(200, 120, 40))
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=INK, width=3)
        d.ellipse([cx - 44, cy - 6, cx + 44, cy + 6], outline=TEAL, width=4)
        d.polygon([(cx + 34, cy - 28), (cx + 44, cy - 36), (cx + 40, cy - 20)],
                  fill=(255, 220, 100))
    elif kind == "badge":
        d.polygon([(cx, cy - 34), (cx + 30, cy - 22), (cx + 30, cy + 8),
                   (cx, cy + 34), (cx - 30, cy + 8), (cx - 30, cy - 22)],
                  outline=INK, width=4)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=INK, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    elif kind == "flame":
        d.polygon([(cx, cy - 36), (cx + 22, cy - 4), (cx + 14, cy + 12),
                   (cx + 26, cy + 2), (cx + 18, cy + 30), (cx - 18, cy + 30),
                   (cx - 26, cy + 2), (cx - 14, cy + 12), (cx - 22, cy - 4)],
                  fill=(230, 90, 20))
        d.ellipse([cx - 10, cy + 6, cx + 10, cy + 28], fill=(255, 200, 60))


for i, (kicker, col, head, body, kind) in enumerate(cells):
    x = X0 + (i % 2) * (CELL_W + GAP)
    y = Y0 + (i // 2) * (CELL_H + GAP)
    d.rectangle([x, y, x + CELL_W, y + CELL_H], outline=INK, width=2)
    d.rectangle([x, y, x + CELL_W, y + 30], fill=col)
    d.text((x + 12, y + 3), kicker, font=font(FB, 22), fill=(255, 255, 255))
    pictogram(x + 62, y + 90, kind)
    tx = x + 118
    yy = y + 36
    for line in head.split("\n"):
        d.text((tx, yy), line, font=font(FB, 25), fill=INK)
        yy += 28
    text_block(d, tx, yy + 2, body, font(FR, 18), (60, 60, 60), CELL_W - 130, 22)

# ---- footer ----
d.line([24, 990, 1000, 990], fill=GREY, width=2)
d.text((24, 996), "Also: Nigeria boat sinks, 24 dead  -  Iran hits 3 tankers near Hormuz",
       font=font(FR, 18), fill=GREY)

img.save("/home/hatch/workspace/makefun/news-image-20261122/entry.png", optimize=True)
print("saved")
