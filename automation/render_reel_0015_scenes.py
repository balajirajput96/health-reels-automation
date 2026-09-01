from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (8, 14, 34)
TEAL = (63, 220, 190)
CYAN = (82, 178, 244)
AMBER = (248, 182, 73)
VIOLET = (165, 126, 238)
WHITE = (232, 243, 252)
RED = (242, 106, 120)


def gradient() -> Image.Image:
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * 0.50, y - H * 0.28) / (W * 0.96))
            px[x, y] = (min(255, int(8 + 10 * t + 8 * glow)), min(255, int(14 + 19 * t + 18 * glow)), min(255, int(34 + 39 * t + 27 * glow)))
    return im


def glow_circle(base: Image.Image, center, radius, color, alpha=68):
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
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(3, 9, 26, 145))


def wave(d, x0, y0, width, cycles, amp, color):
    pts = []
    for i in range(180):
        t = i / 179
        pts.append((x0 + width * t, y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)))
    d.line(pts, fill=(*color, 225), width=10)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 520, TEAL, 42)
    card(d, (110, 820, 1330, 1260), (17, 38, 69, 242), (*TEAL, 220))
    d.ellipse((260, 900, 460, 1100), outline=(*CYAN, 230), width=13)
    d.arc((315, 950, 405, 1040), 25, 320, fill=(*WHITE, 210), width=8)
    card(d, (560, 900, 1180, 1150), (10, 24, 50, 235), (*WHITE, 170), 5, 28)
    for i, color in enumerate([TEAL, CYAN, VIOLET]):
        y = 950 + i * 60
        d.line((630, y, 840, y), fill=(*WHITE, 150), width=11)
        d.rounded_rectangle((900, y - 18, 1040, y + 18), radius=16, fill=(*color, 195))
    arrow(d, 720, 1260, 720, 1410, WHITE, 12)
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
    card(d, (180, 790, 1260, 1370), (17, 38, 69, 242), (*CYAN, 220))
    d.rounded_rectangle((520, 900, 920, 1220), radius=42, fill=(10, 24, 50, 245), outline=(*WHITE, 180), width=8)
    d.rectangle((640, 850, 800, 900), fill=(*WHITE, 190))
    for i in range(3):
        d.line((590, 980 + i * 68, 850, 980 + i * 68), fill=(*WHITE, 145), width=10)
    d.line((260, 1530, 1180, 1530), fill=(*WHITE, 150), width=8)
    for i, x in enumerate([320, 500, 680, 860, 1040, 1160]):
        d.ellipse((x - 23, 1507, x + 23, 1553), fill=(*(TEAL if i % 2 == 0 else AMBER), 220))
        d.line((x, 1410, x, 1465 + (i % 3) * 18), fill=(*WHITE, 170), width=8)
    for i in range(4):
        y = 1660 + i * 48
        d.ellipse((330 + i * 170, y, 365 + i * 170, y + 35), outline=(*VIOLET, 200), width=7)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 430), 500, AMBER, 42)
    card(d, (110, 820, 630, 1280), (17, 38, 69, 242), (*AMBER, 220), 7, 36)
    card(d, (810, 820, 1330, 1280), (17, 38, 69, 242), (*VIOLET, 220), 7, 36)
    # Content side: feeling/problem/memory symbols.
    d.ellipse((230, 940, 360, 1070), outline=(*AMBER, 220), width=10)
    d.line((270, 1100, 470, 1100), fill=(*WHITE, 155), width=12)
    d.rectangle((250, 1150, 390, 1220), outline=(*AMBER, 210), width=9)
    d.arc((430, 930, 540, 1040), 210, 510, fill=(*WHITE, 200), width=10)
    # Process side: repetition, intrusion, stuck.
    for i in range(3):
        x = 930 + i * 105
        d.arc((x, 950, x + 90, 1040), 20, 310, fill=(*VIOLET, 210), width=9)
    d.line((930, 1130, 1210, 1130), fill=(*RED, 210), width=14)
    d.line((930, 1090, 930, 1170), fill=(*RED, 210), width=10)
    d.line((1210, 1090, 1210, 1170), fill=(*RED, 210), width=10)
    arrow(d, 720, 1320, 720, 1480, WHITE, 12)
    card(d, (250, 1530, 1190, 1770), (17, 38, 69, 242), (*CYAN, 220), 7, 36)
    wave(d, 370, 1650, 700, 4, 65, CYAN)
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
    path = OUT / f'reel_0015_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
