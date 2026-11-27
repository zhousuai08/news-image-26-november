#!/usr/bin/env python3
"""Render the 26 November 2026 front page: THE WORLD IN ONE PICTURE.

Draws a 1024x1024 newspaper front page with Pillow, using only vector shapes
and text set in DejaVu fonts. No photo or web image is used anywhere: every
picture on the page is drawn by this script. The headlines are the real news
of Thursday 26 November 2026, checked against NDTV, WION, Daily Mirror,
UN News and Qatar Tribune on 27 November 2026 (see news-sources.md).

Run: python3 tools/render.py  ->  writes entry.png beside main.ts
Deterministic: same input, same bytes (PNG writer is deterministic here;
no timestamps are embedded).
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (246, 241, 227)
INK = (25, 23, 19)
RED = (158, 27, 27)
BLUE = (32, 69, 107)
GREY = (90, 86, 76)
LIGHT_RULE = (180, 172, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit `width` pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=1.28):
    """Draw a wrapped paragraph; returns the y just below it."""
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text):
    f = font(SANS_B, 19)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + 26


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.text((W // 2, 30), "THE WORLD", font=font(SERIF_B, 96), fill=INK, anchor="ma")
rule(d, MARGIN, W - MARGIN, 138, width=3)
d.text((W // 2, 150), "IN ONE PICTURE  ·  THURSDAY, 26 NOVEMBER 2026",
       font=font(SANS_B, 23), fill=INK, anchor="ma")
rule(d, MARGIN, W - MARGIN, 188, width=2)
rule(d, MARGIN, W - MARGIN, 193, width=1)

# ---------------------------------------------------------------- lead story
# Storm picture, drawn: dark sky, rain, a sagging parade balloon over a skyline.
LX, LY, LW, LH = MARGIN, 208, 540, 268
SKY = (44, 58, 74)
d.rectangle([LX, LY, LX + LW, LY + LH], fill=SKY)
# distant skyline
for i, (bx, bw, bh) in enumerate([(0, 52, 70), (58, 40, 110), (104, 62, 84), (172, 44, 126),
                                  (222, 58, 92), (286, 40, 140), (332, 66, 100), (404, 48, 118),
                                  (458, 76, 80)]):
    d.rectangle([LX + bx, LY + LH - bh, LX + bx + bw, LY + LH], fill=(30, 40, 52))
    for wy in range(LY + LH - bh + 12, LY + LH - 8, 22):
        for wx in range(LX + bx + 8, LX + bx + bw - 6, 16):
            d.rectangle([wx, wy, wx + 5, wy + 7], fill=(232, 196, 90))
# storm clouds
for cx, cy, cr in [(90, 60, 52), (150, 44, 64), (230, 62, 56), (320, 48, 60),
                   (410, 64, 54), (480, 52, 46)]:
    d.ellipse([LX + cx - cr, LY + cy - cr // 2, LX + cx + cr, LY + cy + cr // 2],
              fill=(24, 32, 44))
# lightning
d.line([(LX + 470, LY + 90), (LX + 448, LY + 140), (LX + 466, LY + 140),
        (LX + 440, LY + 196)], fill=(250, 220, 90), width=5)
# rain
for rx in range(LX + 12, LX + LW - 8, 26):
    d.line([(rx, LY + 120), (rx - 8, LY + 150)], fill=(170, 195, 215), width=2)
    d.line([(rx + 12, LY + 180), (rx + 4, LY + 210)], fill=(170, 195, 215), width=2)
# sagging parade balloon: a big tilted balloon with ropes, drooping low
d.ellipse([LX + 150, LY + 118, LX + 330, LY + 208], fill=(196, 44, 44))
d.ellipse([LX + 150, LY + 118, LX + 330, LY + 208], outline=(120, 20, 20), width=3)
d.line([(LX + 190, LY + 200), (LX + 176, LY + 246)], fill=(220, 220, 210), width=2)
d.line([(LX + 240, LY + 206), (LX + 240, LY + 250)], fill=(220, 220, 210), width=2)
d.line([(LX + 292, LY + 200), (LX + 308, LY + 246)], fill=(220, 220, 210), width=2)
d.rectangle([LX + 168, LY + 244, LX + 316, LY + 262], fill=(120, 20, 20))
d.text((LX + 240, LY + 163), "GROUNDED", font=font(SANS_B, 15),
       fill=(255, 255, 255), anchor="mm")
# caption strip under the picture
d.rectangle([LX, LY + LH, LX + LW, LY + LH + 26], fill=(25, 23, 19))
d.text((LX + 10, LY + LH + 5), "NEW YORK  ·  THE PARADE THAT NEVER MARCHED",
       font=font(SANS_B, 15), fill=(246, 241, 227))

# Lead text, right of the picture
TX = LX + LW + 24
TW = W - MARGIN - TX
y = kicker(d, TX, LY + 2, "Thanksgiving  ·  United States")
y = para(d, TX, y + 2, TW, "STORM STOPS THANKSGIVING",
         font(SERIF_B, 38), leading=1.08)
y = para(d, TX, y + 8, TW,
         "A powerful storm lashed the US East Coast on the holiday, "
         "postponing the Macy's Parade for the first time in 100 years "
         "— and leaving 900,000 homes without power.",
         font(SERIF, 21), leading=1.3)
rule(d, MARGIN, W - MARGIN, LY + LH + 44, fill=LIGHT_RULE, width=1)

# ---------------------------------------------------------------- middle row
MY = LY + LH + 62  # 538
COLW = (W - 2 * MARGIN - 24) // 2  # 464
# --- left: tariffs, with a small bar chart
x = MARGIN
y = kicker(d, x, MY, "Trade  ·  Washington")
y = para(d, x, y + 2, COLW, "TRUMP TARIFFS HIT 14 NATIONS",
         font(SERIF_B, 30), leading=1.1)
y = para(d, x, y + 6, COLW,
         "New duties of up to 20% on China, the EU and 12 others "
         "reignite the trade fight.",
         font(SERIF, 19), leading=1.3)
by = y + 10
for label, pct, bar in [("CHINA", "20%", 150), ("EU", "20%", 150), ("12 OTHERS", "up to 20%", 150)]:
    d.text((x, by), label, font=font(SANS_B, 16), fill=INK)
    d.rectangle([x + 110, by + 2, x + 110 + bar, by + 18], fill=RED)
    d.text((x + 110 + bar + 10, by), pct, font=font(SANS_B, 16), fill=RED)
    by += 26
# --- right: Houthis / oil
x = MARGIN + COLW + 24
d.line([(x - 12, MY + 4), (x - 12, MY + 232)], fill=LIGHT_RULE, width=1)
y = kicker(d, x, MY, "Middle East  ·  Energy")
y = para(d, x, y + 2, COLW, "HOUTHIS HIT SAUDI REFINERY",
         font(SERIF_B, 30), leading=1.1)
y = para(d, x, y + 6, COLW,
         "Oil climbs as Houthis strike Jizan port and mines hit ships "
         "in the Strait of Hormuz.",
         font(SERIF, 19), leading=1.3)
# oil barrel with flame, drawn (small)
ox, oy = x + 8, y + 8
d.rectangle([ox, oy + 14, ox + 62, oy + 62], fill=(52, 52, 58))
d.rectangle([ox, oy + 14, ox + 62, oy + 20], fill=(70, 70, 78))
d.rectangle([ox, oy + 36, ox + 62, oy + 42], fill=(70, 70, 78))
d.polygon([(ox + 76, oy + 62), (ox + 86, oy + 34), (ox + 94, oy + 48),
           (ox + 104, oy + 20), (ox + 114, oy + 62)], fill=(226, 110, 30))
d.polygon([(ox + 86, oy + 62), (ox + 93, oy + 44), (ox + 102, oy + 62)],
          fill=(250, 200, 60))
d.text((ox + 130, oy + 16), "OIL UP ON", font=font(SANS_B, 18), fill=INK)
d.text((ox + 130, oy + 40), "SUPPLY FEARS", font=font(SANS_B, 18), fill=INK)
rule(d, MARGIN, W - MARGIN, MY + 236, fill=LIGHT_RULE, width=1)

# ---------------------------------------------------------------- bottom row
BY = MY + 236 + 16  # ~790
BW = (W - 2 * MARGIN - 48) // 3  # 301


def mini_icon(draw, x, y, kind, s=34):
    """A small drawn icon in an s-by-s box."""
    if kind == "flame":
        draw.polygon([(x + 5, y + s - 2), (x + 13, y + 12), (x + 18, y + 21),
                      (x + 25, y + 4), (x + 31, y + s - 2)], fill=(226, 110, 30))
        draw.polygon([(x + 12, y + s - 2), (x + 17, y + 20), (x + 24, y + s - 2)],
                     fill=(250, 200, 60))
    elif kind == "rocket":
        draw.polygon([(x + s // 2, y + 1), (x + s - 7, y + 17), (x + s // 2, y + 22),
                      (x + 7, y + 17)], fill=(200, 40, 40))
        draw.rectangle([x + 13, y + 20, x + 21, y + 28], fill=(70, 70, 78))
        draw.polygon([(x + s // 2, y + 28), (x + 13, y + s), (x + 21, y + s)],
                     fill=(250, 200, 60))
        for sx, sy in [(x + 3, y + 7), (x + s - 3, y + 12), (x + 5, y + 26)]:
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=BLUE)
    elif kind == "key":
        draw.ellipse([x + 4, y + 5, x + 20, y + 21], outline=INK, width=3)
        draw.line([(x + 17, y + 18), (x + 32, y + 32)], fill=INK, width=3)
        draw.line([(x + 26, y + 26), (x + 26, y + 33)], fill=INK, width=3)


stories = [
    ("flame", "CAIRO",
     "TANKER FIRE KILLS 31",
     "A fuel tanker crash sets a Giza highway ablaze; 31 dead, 21 hurt."),
    ("rocket", "SPACE",
     "SPACEX GETS 1M SATELLITES",
     "US regulators approve a fleet of space data centres, a first."),
    ("key", "TECH",
     "3.5BN PASSWORDS LEAKED",
     "A massive leak spills billions of passwords and personal records."),
]
for i, (kind, kick, head, body) in enumerate(stories):
    x = MARGIN + i * (BW + 24)
    mini_icon(d, x, BY + 2, kind)
    y = kicker(d, x + 42, BY, kick)
    y = para(d, x, BY + 30, BW, head, font(SERIF_B, 22), leading=1.12)
    y = para(d, x, y + 6, BW, body, font(SANS, 16), fill=GREY, leading=1.3)
    if i < 2:
        d.line([(x + BW + 12, BY + 4), (x + BW + 12, BY + 128)], fill=LIGHT_RULE, width=1)

# ---------------------------------------------------------------- also + footer
AY = BY + 138
rule(d, MARGIN, W - MARGIN, AY, width=2)
d.text((MARGIN, AY + 10), "ALSO ON 26 NOVEMBER",
       font=font(SANS_B, 18), fill=RED)
para(d, MARGIN, AY + 36, W - 2 * MARGIN,
     "Bangkok blast injures 7  ·  Kim widens nuclear arsenal  ·  UK calls up "
     "100,000 reservists  ·  26/11 remembered",
     font(SANS, 16), leading=1.35)
rule(d, MARGIN, W - MARGIN, H - 32, width=1)
d.text((W // 2, H - 26),
       "Sources: NDTV · WION · Daily Mirror · UN News · Qatar Tribune — 26 November 2026",
       font=font(SANS, 13), fill=GREY, anchor="ma")

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)

