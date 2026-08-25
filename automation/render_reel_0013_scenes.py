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


def wave(d, x0, y0, width, cycles, amp, color):
    pts = []
    for i in range(180):
        t = i / 179
        pts.append((x0 + width * t, y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)))
    d.line(pts, fill=(*color, 225), width=10)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 500, TEAL, 42)
    card(d, (110, 850, 1330, 1280), (17, 38, 69, 242), (*TEAL, 220))
    for i, color in enumerate([TEAL, VIOLET, AMBER]):
        x = 210 + i * 380
        d.ellipse((x, 950, x + 150, 1100), outline=(*color, 230), width=12)
        d.arc((x + 28, 978, x + 122, 1072), 25, 320, fill=(*WHITE, 220), width=8)
    arrow(d, 720, 1280, 720, 1420, WHITE, 12)
    card(d, (250, 1450, 1190, 1760), (17, 38, 69, 242), (*CYAN, 220), 7, 36)
    for i in range(5):
        d.rounded_rectangle((360 + i * 130, 1550, 450 + i * 130, 1610), radius=18, fill=(*CYAN, 170 - i * 18))
    d.line((350, 1660, 1090, 1660), fill=(*WHITE, 150), width=7)
    lower_panel(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, CYAN, 42)
    card(d, (130, 840, 1310, 1190), (17, 38, 69, 242), (*CYAN, 220))
    d.rounded_rectangle((280, 930, 1160, 1050), radius=28, outline=(*WHITE, 190), width=8)
    for x in [350, 610, 860, 1080]:
        d.ellipse((x, 970, x + 32, 1002), fill=(*TEAL, 220))
    d.ellipse((590, 955, 650, 1015), fill=(*AMBER, 230))
    arrow(d, 720, 1190, 720, 1370, WHITE, 12)
    card(d, (170, 1410, 600, 1770), (17, 38, 69, 242), (*TEAL, 220))
    card(d, (840, 1410, 1270, 1770), (17, 38, 69, 242), (*AMBER, 220))
    for i in range(4):
        d.line((240, 1530 + i * 48, 510, 1530 + i * 48), fill=(*TEAL, 170), width=14)
    for i in range(4):
        d.ellipse((920 + i * 75, 1540, 965 + i * 75, 1585), outline=(*AMBER, 210), width=8)
    d.line((960, 1600, 1120, 1690), fill=(*WHITE, 170), width=8)
    d.line((1120, 1600, 960, 1690), fill=(*WHITE, 170), width=8)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 480, AMBER, 42)
    card(d, (120, 850, 1320, 1260), (17, 38, 69, 242), (*AMBER, 220))
    for i in range(5):
        d.rounded_rectangle((220 + i * 185, 970, 340 + i * 185, 1050), radius=20, fill=(*AMBER, 190 - i * 18))
    d.line((250, 1140, 1180, 1140), fill=(*WHITE, 150), width=8)
    for i in range(4):
        x = 330 + i * 250
        d.ellipse((x - 36, 1110, x + 36, 1182), outline=(*VIOLET, 210), width=9)
    arrow(d, 720, 1260, 720, 1390, WHITE, 12)
    card(d, (280, 1420, 1160, 1770), (17, 38, 69, 242), (*VIOLET, 220), 7, 38)
    wave(d, 380, 1580, 680, 3, 75, VIOLET)
    d.line((520, 1500, 520, 1690), fill=(*RED, 220), width=10)
    d.line((920, 1500, 920, 1690), fill=(*RED, 220), width=10)
    lower_panel(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, VIOLET, 42)
    cards = [(110, 860, 570, 1260), (870, 860, 1330, 1260), (110, 1400, 570, 1770), (870, 1400, 1330, 1770)]
    colors = [TEAL, CYAN, AMBER, VIOLET]
    for box, color in zip(cards, colors):
        card(d, box, (17, 38, 69, 242), (*color, 220), 7, 36)
    wave(d, 190, 1060, 300, 4, 70, TEAL)
    wave(d, 950, 1060, 280, 6, 58, CYAN)
    for i in range(4):
        y = 1510 + i * 58
        d.line((190, y, 490, y + 12 * math.sin(i)), fill=(*AMBER, 200), width=9)
    nodes = [(980, 1530), (1130, 1480), (1230, 1600), (1080, 1690)]
    for a, b in [(0, 1), (1, 2), (0, 3), (2, 3)]:
        d.line((*nodes[a], *nodes[b]), fill=(*WHITE, 150), width=8)
    for i, (x, y) in enumerate(nodes):
        d.ellipse((x - 35, y - 35, x + 35, y + 35), fill=(*(VIOLET if i % 2 else CYAN), 220), outline=(*WHITE, 180), width=5)
    arrow(d, 720, 1820, 720, 1970, WHITE, 10)
    d.line((530, 2050, 910, 2050), fill=(*RED, 220), width=16)
    d.line((530, 2010, 530, 2090), fill=(*RED, 220), width=12)
    d.line((910, 2010, 910, 2090), fill=(*RED, 220), width=12)
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0013_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
