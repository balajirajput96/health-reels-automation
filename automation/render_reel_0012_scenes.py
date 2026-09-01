from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 15, 36)
TEAL = (57, 220, 194)
CYAN = (93, 177, 244)
AMBER = (249, 184, 77)
VIOLET = (163, 124, 239)
WHITE = (229, 241, 252)
RED = (241, 105, 119)


def gradient() -> Image.Image:
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * 0.52, y - H * 0.28) / (W * 0.95))
            px[x, y] = (min(255, int(7 + 10 * t + 8 * glow)), min(255, int(15 + 18 * t + 19 * glow)), min(255, int(36 + 37 * t + 28 * glow)))
    return im


def glow_circle(base: Image.Image, center, radius, color, alpha=70):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    base.paste(layer, (0, 0), layer)


def card(d, box, fill, outline, width=7, radius=42):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, x1, y1, x2, y2, color=WHITE, width=11):
    d.line((x1, y1, x2, y2), fill=(*color, 220), width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 34
    left = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    right = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), left, right], fill=(*color, 220))


def lower_panel(d):
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 135))


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 500, TEAL, 42)
    card(d, (110, 850, 620, 1360), (17, 38, 69, 242), (*TEAL, 220))
    card(d, (820, 850, 1330, 1360), (17, 38, 69, 242), (*AMBER, 220))
    for i in range(3):
        y = 1010 + i * 100
        d.rounded_rectangle((190, y, 540, y + 52), radius=18, fill=(*TEAL, 180 - i * 15))
        d.rounded_rectangle((900, y, 1250, y + 52), radius=18, fill=(*AMBER, 180 - i * 15))
    arrow(d, 620, 1110, 820, 1110, WHITE, 12)
    card(d, (430, 1450, 1010, 1740), (17, 38, 69, 242), (*CYAN, 220), 7, 34)
    d.ellipse((570, 1515, 650, 1595), outline=(*TEAL, 230), width=10)
    d.ellipse((790, 1515, 870, 1595), outline=(*RED, 230), width=10)
    arrow(d, 650, 1555, 790, 1555, WHITE, 9)
    lower_panel(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, CYAN, 42)
    card(d, (110, 840, 1330, 1240), (17, 38, 69, 242), (*CYAN, 220))
    for i in range(2):
        y = 960 + i * 110
        d.rounded_rectangle((190, y, 1240, y + 58), radius=18, fill=(*TEAL, 170))
        for j in range(5 + i * 2):
            x = 220 + j * 120
            d.ellipse((x, y + 15, x + 26, y + 41), fill=(*WHITE, 220))
    card(d, (110, 1370, 610, 1790), (17, 38, 69, 242), (*VIOLET, 220))
    card(d, (830, 1370, 1330, 1790), (17, 38, 69, 242), (*AMBER, 220))
    for i in range(5):
        h = 80 + i * 55
        d.rounded_rectangle((180 + i * 75, 1700 - h, 220 + i * 75, 1700), radius=12, fill=(*VIOLET, 205))
    for i in range(5):
        h = 100 + ((4 - i) % 3) * 70
        d.rounded_rectangle((900 + i * 75, 1700 - h, 940 + i * 75, 1700), radius=12, fill=(*AMBER, 205))
    arrow(d, 610, 1580, 830, 1580, WHITE, 11)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 480, VIOLET, 42)
    cards = [(100, 850, 620, 1250), (820, 850, 1340, 1250), (100, 1380, 620, 1780), (820, 1380, 1340, 1780)]
    colors = [TEAL, AMBER, CYAN, VIOLET]
    for box, color in zip(cards, colors):
        card(d, box, (17, 38, 69, 242), (*color, 220), 7, 36)
    d.line((220, 1060, 500, 1060), fill=(*WHITE, 180), width=10)
    for i in range(5):
        d.ellipse((250 + i * 46, 1015 - (i % 2) * 40, 282 + i * 46, 1047 - (i % 2) * 40), fill=(*TEAL, 220))
    d.ellipse((960, 980, 1180, 1200), outline=(*AMBER, 220), width=12)
    d.arc((1010, 1030, 1130, 1150), 20, 300, fill=(*WHITE, 220), width=8)
    for i in range(3):
        y = 1480 + i * 82
        d.rounded_rectangle((180, y, 540, y + 44), radius=14, fill=(*CYAN, 170))
    nodes = [(900, 1510), (1050, 1450), (1200, 1530), (1030, 1660)]
    for a, b in [(0, 1), (1, 2), (0, 3), (2, 3)]:
        d.line((*nodes[a], *nodes[b]), fill=(*WHITE, 150), width=7)
    for i, (x, y) in enumerate(nodes):
        d.ellipse((x - 28, y - 28, x + 28, y + 28), fill=(*(VIOLET if i % 2 else TEAL), 220))
    lower_panel(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, AMBER, 42)
    card(d, (120, 850, 1320, 1770), (17, 38, 69, 242), (*CYAN, 220))
    inputs = [(350, 1030, TEAL), (720, 930, VIOLET), (1090, 1030, AMBER)]
    for x, y, color in inputs:
        d.ellipse((x - 62, y - 62, x + 62, y + 62), fill=(*color, 220), outline=(*WHITE, 190), width=5)
        d.line((x, y + 62, 720, 1510), fill=(*color, 150), width=8)
    d.ellipse((650, 1440, 790, 1580), fill=(*WHITE, 220))
    d.line((720, 1580, 720, 1750), fill=(*WHITE, 150), width=8)
    card(d, (390, 1870, 1050, 2130), (17, 38, 69, 242), (*TEAL, 220), 7, 34)
    d.rounded_rectangle((500, 1950, 940, 2010), radius=20, outline=(*TEAL, 220), width=8)
    d.ellipse((530, 1968, 574, 2012), fill=(*TEAL, 220))
    d.line((720, 2130, 720, 2290), fill=(*WHITE, 120), width=8)
    for i, color in enumerate([TEAL, AMBER, RED]):
        x = 390 + i * 230
        d.rounded_rectangle((x, 2180, x + 170, 2250), radius=20, outline=(*color, 220), width=8)
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0012_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
