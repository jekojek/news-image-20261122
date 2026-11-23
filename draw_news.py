#!/usr/bin/env python3
"""Draw the front page of THE WORLD IN ONE DAY for Sunday 22 November 2026.

A single 1024x1024 newspaper page: masthead, one lead story about the COP31
climate summit ending with no deal, six short stories in a two-column grid,
and a one-line footer. Everything is drawn with Pillow primitives, so the
output is deterministic: the same bytes on every run.
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

CREAM = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (15, 42, 68)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

OCEAN = (16, 60, 90)
GRID_BLUE = (120, 200, 220)
LAND = (60, 160, 90)
SUN = (255, 180, 60)
PLANET = (200, 120, 40)
FLAME = (230, 90, 20)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LIB_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_masthead(draw):
    draw.rectangle([0, 0, WIDTH, 146], fill=NAVY)
    draw.rectangle([0, 146, WIDTH, 152], fill=GOLD)
    draw.text((33, 18), "THE WORLD IN ONE DAY",
              font=font(BOLD, 62), fill=WHITE)
    draw.text((32, 96), "SUNDAY - 22 NOVEMBER 2026",
              font=font(BOLD, 41), fill=GOLD)


def draw_globe(draw, cx, cy, radius):
    # Ocean disc.
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=OCEAN)
    # One equator line and two meridian arcs.
    draw.line([cx - radius, cy, cx + radius, cy], fill=GRID_BLUE, width=3)
    draw.arc([cx - 32, cy - radius, cx + 20, cy + radius], 90, 270,
             fill=GRID_BLUE, width=3)
    draw.arc([cx - 20, cy - radius, cx + 32, cy + radius], 270, 90,
             fill=GRID_BLUE, width=3)
    # Two green landmasses.
    draw.ellipse([732, 262, 800, 330], fill=LAND)
    draw.ellipse([826, 352, 900, 420], fill=LAND)
    # Thick red ring.
    draw.ellipse([cx - radius - 8, cy - radius - 8,
                  cx + radius + 8, cy + radius + 8],
                 outline=RED, width=9)
    # Prohibition slash, bottom-left to top-right, running just past
    # the ring at both ends.
    reach = radius + 8
    draw.line([cx - reach, cy + reach, cx + reach, cy - reach],
              fill=RED, width=13)


def draw_lead(draw):
    # Box outline; the red banner covers its top edge and upper sides.
    draw.rectangle([24, 168, 1000, 488], outline=INK, width=3)
    draw.rectangle([24, 168, 1000, 206], fill=RED)
    draw.text((40, 174), "LEAD STORY - CLIMATE SUMMIT COLLAPSES",
              font=font(BOLD, 27), fill=WHITE)
    # Headline, three lines.
    head = font(BOLD, 42)
    y = 221
    for line in ("COP31 ends with", "no deal as talks", "fail on fossil fuels"):
        draw.text((40, y), line, font=head, fill=INK)
        y += 48
    # Standfirst, wrapped to the left column.
    body = font(REGULAR, 23)
    text = ("EU and others reject a text with no mention of fossil fuels. "
            "The Antalya summit closes two days late with no agreement "
            "from nearly 200 countries.")
    y = 372
    for line in wrap(draw, text, body, 600):
        draw.text((40, y), line, font=body, fill=INK)
        y += 28
    # Globe graphic and its caption.
    draw_globe(draw, 818, 337, 97)
    draw.text((670, 448), "NO DEAL", font=font(BOLD, 29), fill=RED)


def draw_ship(draw, x, y):
    # Sunburst top right.
    sx, sy = x + 60, y + 11
    draw.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=SUN)
    for k in range(8):
        ang = k * math.pi / 4
        draw.line([sx + 12 * math.cos(ang), sy + 12 * math.sin(ang),
                   sx + 19 * math.cos(ang), sy + 19 * math.sin(ang)],
                  fill=SUN, width=3)
    # Superstructure and funnel.
    draw.rectangle([x + 11, y + 26, x + 48, y + 42], fill=INK)
    draw.rectangle([x + 24, y + 26, x + 48, y + 49], fill=INK)
    # Hull, wide at the top and narrowing below.
    draw.polygon([(x + 0, y + 50), (x + 84, y + 50), (x + 69, y + 74),
                  (x + 15, y + 74)], fill=INK)
    # One zigzag wave line below the hull.
    draw.line([(x + 2, y + 79), (x + 22, y + 69), (x + 42, y + 79),
               (x + 62, y + 69), (x + 82, y + 79)],
              fill=(14, 110, 110), width=3, joint="curve")


def draw_mountains(draw, x, y):
    # Two-peak silhouette with straight sides at the bottom.
    draw.polygon([(x + 2, y + 74), (x + 2, y + 50), (x + 26, y + 8),
                  (x + 46, y + 44), (x + 66, y + 12), (x + 82, y + 50),
                  (x + 82, y + 74)], fill=(70, 70, 70))
    # Red crack zigzag across the lower part, on a black baseline.
    pts = [(x + 14, y + 76), (x + 26, y + 58), (x + 38, y + 76),
           (x + 50, y + 58), (x + 62, y + 76), (x + 72, y + 60)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.line([(x + 2, y + 76), (x + 82, y + 76)], fill=INK, width=3)


def draw_ballot(draw, x, y):
    # Ballot box with a hollow handle on top and a big red tick.
    draw.rectangle([x + 8, y + 26, x + 76, y + 74], outline=INK, width=4)
    draw.rectangle([x + 28, y + 10, x + 56, y + 24], outline=INK, width=3)
    draw.line([(x + 18, y + 50), (x + 34, y + 64), (x + 64, y + 30)],
              fill=RED, width=6, joint="curve")


def draw_planet(draw, x, y):
    draw.ellipse([x + 13, y + 18, x + 71, y + 74], fill=PLANET,
                 outline=INK, width=3)
    # Wide flat ring around the planet.
    draw.ellipse([x - 2, y + 36, x + 86, y + 52], outline=(14, 110, 110),
                 width=4)
    # Small four-point sparkle top right.
    sx, sy = x + 81, y + 16
    draw.polygon([(sx, sy - 8), (sx + 2, sy - 2), (sx + 6, sy),
                  (sx + 2, sy + 2), (sx, sy + 8), (sx - 2, sy + 2),
                  (sx - 6, sy), (sx - 2, sy - 2)], fill=(255, 220, 100))


def draw_shield(draw, x, y):
    pts = [(x + 40, y + 10), (x + 72, y + 22), (x + 72, y + 58),
           (x + 40, y + 78), (x + 12, y + 58), (x + 12, y + 22)]
    draw.polygon(pts, outline=INK, width=4)
    draw.ellipse([x + 28, y + 32, x + 52, y + 56], outline=INK, width=3)
    draw.ellipse([x + 36, y + 40, x + 44, y + 48], fill=RED)


def draw_flame(draw, x, y):
    # Teardrop body with small side tongues near the bottom.
    draw.polygon([(x + 42, y + 9), (x + 30, y + 27), (x + 21, y + 42),
                  (x + 14, y + 46), (x + 20, y + 54), (x + 24, y + 76),
                  (x + 60, y + 76), (x + 64, y + 54), (x + 70, y + 46),
                  (x + 63, y + 42), (x + 54, y + 27)], fill=FLAME)
    draw.ellipse([x + 32, y + 50, x + 52, y + 72], fill=(255, 200, 60))


ICONS = {
    "ship": draw_ship,
    "mountains": draw_mountains,
    "ballot": draw_ballot,
    "planet": draw_planet,
    "shield": draw_shield,
    "flame": draw_flame,
}

STORIES = [
    # (header, colour, icon, headline lines, body)
    ("WAR AT SEA", NAVY, "ship",
     ("Ukrainian sea drones", "strike Russian warship"),
     "Corvette Merkury badly damaged at Benghazi, Libya; "
     "a cargo ship also hit."),
    ("WAR IN EUROPE", RED, "mountains",
     ("Russian strike flattens", "Kyiv apartment block"),
     "Dymer, near Kyiv: at least 3 killed, people trapped "
     "under the rubble."),
    ("POLITICS", (60, 40, 110), "ballot",
     ("Democrats win 258", "House seats"),
     "Largest US House majority for any party since 1992."),
    ("SPACE", (10, 60, 90), "planet",
     ("BepiColombo reaches", "Mercury after 8 years"),
     "ESA-JAXA probe enters orbit; thruster glitch, craft safe."),
    ("JUSTICE", (120, 40, 40), "shield",
     ("Mexico captures", "'El Chapo Isidro'"),
     "FBI Most Wanted cartel boss seized in Sinaloa; "
     "11 killed in raid."),
    ("DISASTER", (14, 110, 110), "flame",
     ("Candy factory fire kills", "3 in Indonesia"),
     "Blaze at Cikande, Banten; dozens of workers still missing."),
]

COLUMNS = [(24, 503), (516, 1000)]
ROWS = [(508, 656), (670, 818), (832, 980)]


def draw_story(draw, x0, y0, x1, y1, header, colour, icon, head_lines, body):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=3)
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 31], fill=colour)
    draw.text((x0 + 12, y0 + 3), header, font=font(BOLD, 22), fill=WHITE)
    ICONS[icon](draw, x0 + 20, y0 + 46)
    tx = x0 + 118
    max_w = x1 - 12 - tx
    head = font(BOLD, 25)
    y = y0 + 36
    for line in head_lines:
        draw.text((tx, y), line, font=head, fill=INK)
        y += 28
    body_font = font(REGULAR, 18)
    y = y0 + 93
    for line in wrap(draw, body, body_font, max_w):
        draw.text((tx, y), line, font=body_font, fill=INK)
        y += 22


def draw_footer(draw):
    draw.line([24, 990, 1000, 990], fill=GREY, width=2)
    draw.text((24, 994),
              "Also: Nigeria boat sinks, 24 dead - "
              "Iran hits 3 tankers near Hormuz",
              font=font(LIB_REG, 21), fill=GREY)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    image = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_lead(draw)
    for index, story in enumerate(STORIES):
        col = COLUMNS[index % 2]
        row = ROWS[index // 2]
        draw_story(draw, col[0], row[0], col[1], row[1], *story)
    draw_footer(draw)
    image.save(out_path, format="PNG")


if __name__ == "__main__":
    main()
