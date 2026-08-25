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
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 140))


def wave(d, x0, y0, width, cycles, amp, color):
    pts = []
    for i in range(180):
        t = i / 179
        pts.append((x0 + width * t, y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)))
    d.line(pts, fill=(*color, 225), width=10)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 520, TEAL, 42)
    card(d, (120, 820, 680, 1260), (17, 38, 69, 242), (*TEAL, 220), 7, 40)
    card(d, (760, 820, 1320, 1260), (17, 38, 69, 242), (*AMBER, 220), 7, 40)
    # Symbolic past memory and future imagination cards.
    d.arc((260, 930, 480, 1150), 20, 340, fill=(*CYAN, 220), width=13)
    d.ellipse((330, 995, 410, 1075), outline=(*WHITE, 210), width=9)
    d.line((210, 1180, 590, 1180), fill=(*WHITE, 150), width=10)
    for i in range(4):
        d.ellipse((855 + i * 90, 950 - i * 22, 905 + i * 90, 1000 - i * 22), fill=(*AMBER, 205))
    d.line((870, 1120, 1190, 970), fill=(*WHITE, 180), width=9)
    d.line((870, 1120, 1190, 1120), fill=(*WHITE, 150), width=8)
    arrow(d, 720, 1280, 720, 1420, WHITE, 12)
    card(d, (240, 1450, 1200, 1760), (17, 38, 69, 242), (*VIOLET, 220), 7, 36)
    d.line((360, 1610, 1080, 1610), fill=(*WHITE, 150), width=8)
    for x, color in zip([420, 600, 780, 960], [TEAL, CYAN, AMBER, VIOLET]):
        d.ellipse((x - 25, 1585, x + 25, 1635), fill=(*color, 220))
    lower_panel(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 480, CYAN, 42)
    card(d, (140, 800, 1300, 1180), (17, 38, 69, 242), (*CYAN, 220), 7, 38)
    # Narrative/detail/context extraction.
    d.rounded_rectangle((260, 900, 630, 1090), radius=28, outline=(*WHITE, 180), width=8)
    for i in range(3):
        d.line((320, 950 + i * 45, 560, 950 + i * 45), fill=(*TEAL, 180), width=10)
    d.rounded_rectangle((810, 900, 1180, 1090), radius=28, outline=(*AMBER, 190), width=8)
    for i in range(3):
        d.ellipse((890 + i * 80, 960, 930 + i * 80, 1000), fill=(*AMBER, 210))
    arrow(d, 720, 1180, 720, 1330, WHITE, 12)
    card(d, (180, 1380, 1260, 1770), (17, 38, 69, 242), (*TEAL, 220), 7, 38)
    d.line((300, 1600, 1140, 1600), fill=(*WHITE, 150), width=8)
    for i, color in enumerate([TEAL, CYAN, AMBER, VIOLET]):
        x = 420 + i * 200
        d.ellipse((x - 28, 1572, x + 28, 1628), outline=(*color, 220), width=9)
        d.line((x, 1510, x, 1550), fill=(*WHITE, 160), width=8)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 500, AMBER, 42)
    card(d, (120, 820, 1320, 1180), (17, 38, 69, 242), (*AMBER, 220), 7, 38)
    # Remember-versus-know and source-context branching.
    d.ellipse((280, 920, 430, 1070), outline=(*TEAL, 220), width=12)
    d.line((490, 995, 700, 995), fill=(*WHITE, 180), width=10)
    d.line((700, 995, 880, 900), fill=(*WHITE, 180), width=10)
    d.line((700, 995, 880, 1090), fill=(*WHITE, 180), width=10)
    card(d, (900, 840, 1230, 980), (10, 24, 50, 235), (*TEAL, 200), 5, 25)
    card(d, (900, 1020, 1230, 1160), (10, 24, 50, 235), (*VIOLET, 200), 5, 25)
    d.line((950, 905, 1170, 905), fill=(*WHITE, 170), width=11)
    d.line((950, 1085, 1170, 1085), fill=(*WHITE, 170), width=11)
    arrow(d, 720, 1180, 720, 1330, WHITE, 12)
    card(d, (260, 1380, 1180, 1770), (17, 38, 69, 242), (*CYAN, 220), 7, 38)
    for i in range(5):
        d.rounded_rectangle((390 + i * 145, 1580 - i * 38, 470 + i * 145, 1645), radius=14, fill=(*CYAN, 180 - i * 16))
    d.line((350, 1645, 1090, 1645), fill=(*WHITE, 150), width=8)
    lower_panel(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, VIOLET, 42)
    cards = [(110, 850, 570, 1240), (870, 850, 1330, 1240), (110, 1380, 570, 1740), (870, 1380, 1330, 1740)]
    colors = [TEAL, CYAN, AMBER, VIOLET]
    for box, color in zip(cards, colors):
        card(d, box, (17, 38, 69, 242), (*color, 220), 7, 36)
    for i in range(4):
        d.line((180, 960 + i * 52, 480, 960 + i * 52), fill=(*WHITE, 160), width=10)
    d.arc((940, 930, 1250, 1235), 205, 335, fill=(*CYAN, 220), width=18)
    d.line((1095, 1085, 1190, 1015), fill=(*WHITE, 220), width=12)
    for i, h in enumerate([90, 150, 115, 190]):
        x = 180 + i * 80
        d.rounded_rectangle((x, 1660 - h, x + 45, 1660), radius=10, fill=(*AMBER, 200))
    wave(d, 900, 1550, 300, 4, 65, VIOLET)
    arrow(d, 720, 1785, 720, 1920, WHITE, 10)
    d.line((490, 2040, 950, 2040), fill=(*RED, 220), width=18)
    d.line((490, 1990, 490, 2090), fill=(*RED, 220), width=12)
    d.line((950, 1990, 950, 2090), fill=(*RED, 220), width=12)
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0016_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
