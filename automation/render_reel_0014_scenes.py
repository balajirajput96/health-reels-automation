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
            glow = max(0.0, 1 - math.hypot(x - W * 0.50, y - H * 0.28) / (W * 0.95))
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
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 145))


def wave(d, x0, y0, width, cycles, amp, color):
    pts = []
    for i in range(180):
        t = i / 179
        pts.append((x0 + width * t, y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)))
    d.line(pts, fill=(*color, 225), width=10)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 520, TEAL, 42)
    card(d, (110, 820, 1330, 1280), (17, 38, 69, 242), (*TEAL, 220))
    # Abstract person and questionnaire cards: no readable private content.
    d.ellipse((270, 900, 470, 1100), outline=(*CYAN, 230), width=13)
    d.arc((325, 955, 415, 1045), 25, 320, fill=(*WHITE, 210), width=8)
    card(d, (570, 900, 1180, 1160), (10, 24, 50, 235), (*WHITE, 170), 5, 28)
    for i, color in enumerate([TEAL, CYAN, VIOLET]):
        y = 950 + i * 62
        d.line((640, y, 850, y), fill=(*WHITE, 150), width=11)
        d.rounded_rectangle((910, y - 18, 1040, y + 18), radius=16, fill=(*color, 195))
    arrow(d, 720, 1280, 720, 1410, WHITE, 12)
    card(d, (270, 1440, 1170, 1760), (17, 38, 69, 242), (*AMBER, 220), 7, 36)
    d.line((390, 1610, 1050, 1610), fill=(*WHITE, 150), width=8)
    for i, color in enumerate([TEAL, CYAN, AMBER, VIOLET, RED]):
        x = 420 + i * 145
        d.ellipse((x - 25, 1585, x + 25, 1635), fill=(*color, 220))
    lower_panel(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 480, CYAN, 42)
    card(d, (120, 820, 1320, 1160), (17, 38, 69, 242), (*CYAN, 220))
    # Repeated trials with answer and confidence markers.
    d.line((250, 1010, 1190, 1010), fill=(*WHITE, 160), width=8)
    for i, x in enumerate([300, 485, 670, 855, 1040, 1170]):
        d.ellipse((x - 22, 988, x + 22, 1032), fill=(*(TEAL if i % 2 == 0 else AMBER), 220))
        d.line((x, 920, x, 955 + (i % 3) * 22), fill=(*WHITE, 180), width=8)
    arrow(d, 720, 1160, 720, 1320, WHITE, 12)
    card(d, (130, 1370, 620, 1770), (17, 38, 69, 242), (*TEAL, 220), 7, 36)
    card(d, (820, 1370, 1310, 1770), (17, 38, 69, 242), (*AMBER, 220), 7, 36)
    for i in range(5):
        d.ellipse((230 + i * 68, 1510 - i * 24, 270 + i * 68, 1550 - i * 24), fill=(*TEAL, 190))
        d.ellipse((920 + i * 68, 1540 + i * 20, 960 + i * 68, 1580 + i * 20), fill=(*AMBER, 190))
    d.line((190, 1660, 530, 1480), fill=(*WHITE, 150), width=7)
    d.line((880, 1480, 1240, 1660), fill=(*WHITE, 150), width=7)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 500, AMBER, 42)
    card(d, (120, 820, 1320, 1130), (17, 38, 69, 242), (*AMBER, 220))
    # Prospective prediction before outcome.
    card(d, (220, 900, 580, 1060), (10, 24, 50, 235), (*CYAN, 200), 5, 28)
    card(d, (860, 900, 1220, 1060), (10, 24, 50, 235), (*TEAL, 200), 5, 28)
    arrow(d, 580, 980, 860, 980, WHITE, 10)
    d.ellipse((350, 945, 430, 1025), outline=(*CYAN, 220), width=10)
    d.ellipse((990, 945, 1070, 1025), fill=(*TEAL, 200))
    arrow(d, 720, 1130, 720, 1280, WHITE, 12)
    card(d, (245, 1330, 1195, 1760), (17, 38, 69, 242), (*VIOLET, 220), 7, 38)
    for i, h in enumerate([100, 165, 120, 210, 145]):
        x = 390 + i * 145
        d.rounded_rectangle((x, 1610 - h, x + 76, 1610), radius=14, fill=(*VIOLET, 190 - i * 12))
    d.line((350, 1610, 1080, 1610), fill=(*WHITE, 150), width=8)
    d.ellipse((1000, 1460, 1080, 1540), outline=(*AMBER, 220), width=10)
    arrow(d, 720, 1760, 720, 1850, WHITE, 10)
    card(d, (390, 1880, 1050, 2180), (10, 24, 50, 235), (*CYAN, 200), 5, 30)
    for i in range(4):
        d.line((500, 1980 + i * 42, 940 - i * 70, 1980 + i * 42), fill=(*WHITE, 155), width=10)
    lower_panel(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 470, VIOLET, 42)
    cards = [(110, 850, 570, 1240), (870, 850, 1330, 1240), (110, 1380, 570, 1740), (870, 1380, 1330, 1740)]
    colors = [TEAL, CYAN, AMBER, VIOLET]
    for box, color in zip(cards, colors):
        card(d, box, (17, 38, 69, 242), (*color, 220), 7, 36)
    # Questionnaire, confidence gauge, performance bars, and neural correlate.
    for i in range(4):
        d.line((190, 960 + i * 50, 480, 960 + i * 50), fill=(*WHITE, 160), width=10)
    d.arc((940, 930, 1250, 1235), 205, 335, fill=(*CYAN, 220), width=18)
    d.line((1095, 1085, 1190, 1015), fill=(*WHITE, 220), width=12)
    for i, h in enumerate([90, 150, 115, 190]):
        x = 180 + i * 80
        d.rounded_rectangle((x, 1660 - h, x + 45, 1660), radius=10, fill=(*AMBER, 200))
    wave(d, 940, 1550, 300, 4, 65, VIOLET)
    arrow(d, 720, 1785, 720, 1920, WHITE, 10)
    d.line((490, 2040, 950, 2040), fill=(*RED, 220), width=18)
    d.line((490, 1990, 490, 2090), fill=(*RED, 220), width=12)
    d.line((950, 1990, 950, 2090), fill=(*RED, 220), width=12)
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0014_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
