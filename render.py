#!/usr/bin/env python3
"""Render the news-image-20261121 entry: one 1024x1024 PNG summing up
Saturday 21 November 2026's world news as a front page.

Pure Pillow, no network, no randomness, no clock: rendering twice
produces byte-identical output. Run: python3 render.py  (writes
entry.png next to this file).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (179, 38, 30)
NAVY = (22, 38, 77)
NAVY_DARK = (12, 23, 48)
GOLD = (201, 162, 39)
CHARCOAL = (35, 35, 35)
GREY = (90, 86, 76)
TINT_RED = (243, 217, 212)
TINT_BLUE = (216, 226, 242)
TINT_GOLD = (242, 227, 184)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; never overflows."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def dotted_arc(draw, cx, cy, rx, ry, a0, a1, fill):
    steps = 26
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        x = cx + rx * math.cos(a)
        y = cy - ry * math.sin(a)
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=fill)


def draw_night_scene(draw):
    """Left half of the hero: night sky, missile arcs, blasts, skyline."""
    # stars
    for sx, sy in [(70, 200), (140, 185), (210, 210), (300, 190),
                   (95, 260), (260, 250), (330, 280), (180, 300)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 220, 220))
    # missile trails arcing down to the blasts
    dotted_arc(draw, 130, 420, 150, 190, 15, 95, (255, 200, 90))
    dotted_arc(draw, 260, 430, 130, 170, 20, 100, (255, 200, 90))
    # explosion bursts
    starburst(draw, 120, 330, 46, 20, 10, (255, 176, 32))
    starburst(draw, 120, 330, 28, 12, 10, (255, 226, 120))
    starburst(draw, 285, 360, 38, 17, 10, (255, 140, 40))
    starburst(draw, 285, 360, 22, 10, 10, (255, 210, 110))
    starburst(draw, 205, 285, 24, 11, 8, (255, 176, 32))
    # city skyline silhouette along the bottom of the hero
    for bx, bw, bh in [(28, 52, 46), (88, 34, 70), (130, 60, 38),
                       (198, 30, 58), (236, 66, 44), (310, 40, 62)]:
        draw.rectangle([bx, 500 - bh, bx + bw, 500], fill=NAVY_DARK)
    for wx in (48, 70, 100, 146, 170, 216, 258, 286, 322):
        draw.rectangle([wx, 462, wx + 5, 468], fill=GOLD)


def draw_chart_icon(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=TINT_RED)
    ox, oy = x + 14, y + s - 14
    draw.line([ox, y + 14, ox, oy, x + s - 12, oy], fill=INK, width=3)
    pts = [(ox + 2, y + 26), (ox + 18, y + 34), (ox + 32, y + 30),
           (ox + 46, y + 46), (ox + 60, y + 58)]
    draw.line(pts, fill=RED, width=4)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey - 9), (ex + 10, ey + 2), (ex - 4, ey + 6)],
                 fill=RED)


def draw_flags_icon(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=TINT_BLUE)
    fw, fh = 24, 18
    # United States: stripes + blue canton
    fx, fy = x + 6, y + 34
    for i in range(6):
        draw.rectangle([fx, fy + i * 3, fx + fw, fy + i * 3 + 3],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, fy, fx + 10, fy + 9], fill=(30, 60, 140))
    # China: red field, yellow stars
    fx = x + 32
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    draw.ellipse([fx + 3, fy + 3, fx + 8, fy + 8], fill=GOLD)
    draw.ellipse([fx + 14, fy + 4, fx + 17, fy + 7], fill=GOLD)
    draw.ellipse([fx + 16, fy + 11, fx + 19, fy + 14], fill=GOLD)
    # Russia: white / blue / red horizontal tricolour
    fx = x + 58
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([fx, fy + i * 6, fx + fw, fy + i * 6 + 6], fill=c)


def draw_pad_icon(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=TINT_GOLD)
    draw.rounded_rectangle([x + 12, y + 30, x + s - 12, y + 62],
                           radius=12, fill=INK)
    draw.rectangle([x + 22, y + 40, x + 30, y + 52], fill=PAPER)
    draw.rectangle([x + 18, y + 44, x + 34, y + 48], fill=PAPER)
    draw.ellipse([x + 56, y + 38, x + 64, y + 46], fill=RED)
    draw.ellipse([x + 66, y + 46, x + 74, y + 54], fill=GOLD)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin; content spans mx .. W-mx

    # --- masthead ------------------------------------------------------
    mast = font(SERIF_B, 62)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 16), title, font=mast, fill=INK)
    d.rectangle([mx, 96, W - mx, 100], fill=RED)
    d.rectangle([mx, 104, W - mx, 106], fill=INK)

    # --- date bar ------------------------------------------------------
    d.rectangle([mx, 114, W - mx, 160], fill=INK)
    date_f = font(SANS_B, 28)
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 122), date, font=date_f, fill=(255, 255, 255))

    # --- hero panel ----------------------------------------------------
    d.rectangle([mx, 176, W - mx, 500], fill=NAVY)
    draw_night_scene(d)
    tx = 404
    tw_hero = W - mx - tx  # 592
    kick = font(SANS_B, 20)
    d.text((tx, 196), "RUSSIA STRIKES — MISSILES LAND IN POLAND",
           font=kick, fill=GOLD)
    head = font(SERIF_B, 44)
    y = text_block(d, ["RUSSIA'S BIGGEST", "AIR ASSAULT", "OF THE WAR"],
                   tx, 226, head, (255, 255, 255), 52)
    sub = font(SANS, 21)
    sub_lines = wrap(
        d,
        "More than 400 drones and 110 missiles hit Ukraine overnight; "
        "eight were killed in Kyiv.",
        sub, tw_hero)
    y = text_block(d, sub_lines, tx, 394, sub, (225, 230, 240), 28)
    fact = font(SANS_B, 19)
    d.text((tx, 458), "400+ DRONES  •  110 MISSILES  •  8 KILLED IN KYIV",
           font=fact, fill=GOLD)

    # --- three story columns ------------------------------------------
    d.line([mx, 516, W - mx, 516], fill=INK, width=2)
    cols = [
        ("MARKETS", "AI SELL-OFF DRAGS WALL ST INTO CORRECTION",
         "The S&P 500 and Dow fall into correction; the Nasdaq wipes "
         "out all its 2026 gains.",
         draw_chart_icon),
        ("DIPLOMACY", "TRUMP DEFENDS HIS PUTIN AND XI TIES",
         "Trump calls the first US–China–Russia summit “momentous” — "
         "nuclear war “must never happen”.",
         draw_flags_icon),
        ("CULTURE", "GTA VI: $3.79 BILLION IN ONE DAY",
         "Rockstar’s game is the biggest entertainment launch in "
         "history — 32.5 million copies pre-sold.",
         draw_pad_icon),
    ]
    col_w = 304
    gap = 16
    kicker_f = font(SANS_B, 19)
    title_f = font(SERIF_B, 26)
    body_f = font(SANS, 19)
    for i, (kicker, headline, body, icon_fn) in enumerate(cols):
        cx = mx + i * (col_w + gap)
        if i:
            d.line([cx - gap // 2, 532, cx - gap // 2, 856],
                   fill=(200, 192, 172), width=1)
        icon_fn(d, cx, 532, 88)
        d.text((cx, 636), kicker, font=kicker_f, fill=RED)
        title_lines = wrap(d, headline, title_f, col_w)
        y = text_block(d, title_lines, cx, 664, title_f, INK, 32)
        body_lines = wrap(d, body, body_f, col_w)
        text_block(d, body_lines, cx, y + 10, body_f, (60, 58, 50), 25)

    # --- ALSO strip ----------------------------------------------------
    d.rectangle([mx, 884, W - mx, 950], fill=CHARCOAL)
    also_f = font(SANS, 20)
    also = ("ALSO — Houthi missiles aimed at Riyadh intercepted for a "
            "third night  •  UK seals EU trade and youth-mobility deals")
    also_lines = wrap(d, also, also_f, W - 2 * mx - 32)
    text_block(d, also_lines, mx + 16, 892, also_f, (240, 240, 240), 27)

    # --- footer --------------------------------------------------------
    foot = font(SANS, 16)
    src = ("Sources: BBC · Reuters · Financial Times · The Guardian · "
           "Al Jazeera · CNN · USA Today · Xinhua")
    sw = d.textlength(src, font=foot)
    d.text(((W - sw) / 2, 968), src, font=foot, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
