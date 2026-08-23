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


def wave(d, x0, y0, width, cycles, amp, color):
    pts = []
    for i in range(180):
        t = i / 179
        pts.append((x0 + width * t, y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)))
    d.line(pts, fill=(*color, 225), width=10)


def lower_panel(d):
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 135))


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 500, TEAL, 42)
    boxes = [(100, 850, 630, 1530), (810, 850, 1340, 1530)]
    colors = [TEAL, AMBER]
    for box, color in zip(boxes, colors):
        card(d, box, (17, 38, 69, 242), (*color, 220))
        for i in range(4):
            y = 990 + i * 110
            d.rounded_rectangle((box[0] + 90, y, box[2] - 90, y + 52), radius=18, fill=(*color, 180 - i * 15))
    d.ellipse((610, 520, 830, 740), outline=(*CYAN, 230), width=13)
    d.line((720, 740, 720, 850), fill=(*CYAN, 200), width=8)
    arrow(d, 630, 1190, 810, 1190, WHITE, 12)
    lower_panel(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, CYAN, 42)
    card(d, (110, 850, 1330, 1220), (17, 38, 69, 242), (*CYAN, 220))
    wave(d, 180, 1040, 1080, 5, 85, CYAN)
    card(d, (110, 1320, 610, 1770), (17, 38, 69, 242), (*TEAL, 220))
    card(d, (830, 1320, 1330, 1770), (17, 38, 69, 242), (*AMBER, 220))
    for i in range(6):
        x = 190 + i * 62
        h = 110 + (i % 3) * 55
        d.rounded_rectangle((x, 1640 - h, x + 34, 1640), radius=14, fill=(*TEAL, 200))
    for i in range(6):
        x = 900 + i * 62
        h = 90 + ((i + 1) % 3) * 70
        d.rounded_rectangle((x, 1640 - h, x + 34, 1640), radius=14, fill=(*AMBER, 200))
    arrow(d, 610, 1545, 830, 1545, WHITE, 11)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 480, VIOLET, 42)
    card(d, (100, 820, 620, 1760), (17, 38, 69, 242), (*VIOLET, 220))
    card(d, (820, 820, 1340, 1760), (17, 38, 69, 242), (*AMBER, 220))
    d.ellipse((270, 960, 450, 1510), outline=(*CYAN, 210), width=12)
    d.arc((260, 900, 460, 1580), 90, 270, fill=(*CYAN, 220), width=10)
    wave(d, 900, 1080, 360, 4, 75, AMBER)
    for row in range(4):
        for col in range(5):
            x = 930 + col * 68
            y = 1320 + row * 68
            fill = VIOLET if (row + col) % 2 else TEAL
            d.rounded_rectangle((x, y, x + 34, y + 34), radius=8, fill=(*fill, 205))
    arrow(d, 620, 1290, 820, 1290, WHITE, 11)
    for i in range(6):
        x = 650 + i * 40
        d.ellipse((x, 600 - i * 12, x + 28, 628 - i * 12), fill=(*WHITE, 210))
    lower_panel(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, AMBER, 42)
    card(d, (120, 850, 1320, 1790), (17, 38, 69, 242), (*CYAN, 220))
    nodes = [(360, 1060), (720, 980), (1080, 1060), (470, 1420), (970, 1420), (720, 1600)]
    for a, b in [(0, 1), (1, 2), (0, 3), (2, 4), (3, 5), (4, 5)]:
        d.line((*nodes[a], *nodes[b]), fill=(*WHITE, 135), width=8)
    for i, (x, y) in enumerate(nodes):
        color = [TEAL, VIOLET, AMBER, CYAN, RED, WHITE][i]
        d.ellipse((x - 55, y - 55, x + 55, y + 55), fill=(*color, 220), outline=(*WHITE, 180), width=5)
    d.line((720, 1790, 720, 1940), fill=(*WHITE, 100), width=7)
    for i, color in enumerate([TEAL, AMBER, RED]):
        y = 2020 + i * 105
        d.rounded_rectangle((310, y, 1130, y + 58), radius=18, outline=(*color, 210), width=7)
        d.ellipse((350, y + 17, 390, y + 57), fill=(*color, 220))
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0011_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
