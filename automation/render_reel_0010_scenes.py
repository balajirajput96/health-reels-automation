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


def gradient() -> Image.Image:
    im = Image.new('RGB', (W, H), BG)
    p = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * 0.52, y - H * 0.28) / (W * 0.95))
            p[x, y] = (min(255, int(7 + 10 * t + 8 * glow)), min(255, int(15 + 18 * t + 19 * glow)), min(255, int(36 + 37 * t + 28 * glow)))
    return im


def glow_circle(base: Image.Image, center: tuple[int, int], radius: int, color: tuple[int, int, int], alpha: int = 70) -> None:
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    base.paste(layer, (0, 0), layer)


def card(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, outline, width: int = 6, radius: int = 42) -> None:
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, color=WHITE, width: int = 10) -> None:
    d.line((x1, y1, x2, y2), fill=(*color, 215), width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 34
    left = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    right = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), left, right], fill=(*color, 215))


def wave(d: ImageDraw.ImageDraw, x0: float, y0: float, width: float, cycles: int, amp: float, color) -> None:
    pts = []
    for i in range(180):
        t = i / 179
        x = x0 + width * t
        y = y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)
        pts.append((x, y))
    d.line(pts, fill=(*color, 220), width=10)


def lower_panel(d: ImageDraw.ImageDraw) -> None:
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 130))


def scene_01() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 500, TEAL, 42)
    card(d, (110, 920, 650, 1580), (17, 38, 69, 242), (*TEAL, 215), 7, 40)
    card(d, (790, 920, 1330, 1580), (17, 38, 69, 242), (*AMBER, 215), 7, 40)
    for i in range(4):
        d.rounded_rectangle((190, 1060 + i * 105, 570, 1110 + i * 105), radius=18, fill=(*TEAL, 170 - i * 12))
        d.rounded_rectangle((870, 1060 + i * 105, 1250, 1110 + i * 105), radius=18, fill=(*AMBER, 170 - i * 12))
    arrow(d, 650, 1250, 790, 1250, WHITE, 12)
    d.ellipse((615, 690, 825, 900), outline=(*CYAN, 220), width=12)
    d.line((720, 900, 720, 920), fill=(*CYAN, 190), width=8)
    lower_panel(d)
    return im


def scene_02() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 470, CYAN, 42)
    card(d, (110, 900, 1330, 1220), (17, 38, 69, 242), (*TEAL, 215), 7, 38)
    wave(d, 180, 1060, 1080, 5, 85, TEAL)
    card(d, (110, 1320, 610, 1770), (17, 38, 69, 242), (*VIOLET, 215), 7, 38)
    card(d, (830, 1320, 1330, 1770), (17, 38, 69, 242), (*AMBER, 215), 7, 38)
    d.line((190, 1550, 530, 1550), fill=(*VIOLET, 180), width=8)
    for i in range(5):
        x = 210 + i * 62
        d.ellipse((x, 1500 - (i % 2) * 70, x + 28, 1528 - (i % 2) * 70), fill=(*VIOLET, 220))
    for i in range(5):
        x = 900 + i * 62
        d.ellipse((x, 1500 - (i % 3) * 45, x + 28, 1528 - (i % 3) * 45), fill=(*AMBER, 220))
    arrow(d, 610, 1545, 830, 1545, WHITE, 11)
    lower_panel(d)
    return im


def scene_03() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 480, VIOLET, 42)
    card(d, (100, 910, 620, 1730), (17, 38, 69, 242), (*CYAN, 215), 7, 38)
    card(d, (820, 910, 1340, 1730), (17, 38, 69, 242), (*AMBER, 215), 7, 38)
    wave(d, 160, 1320, 400, 4, 95, CYAN)
    d.ellipse((990, 1170, 1170, 1350), outline=(*AMBER, 210), width=12)
    d.arc((1020, 1140, 1290, 1510), 200, 340, fill=(*AMBER, 220), width=10)
    for i in range(6):
        x = 930 + i * 58
        y = 1540 - int(75 * math.sin(i / 1.7))
        d.ellipse((x, y, x + 26, y + 26), fill=(*AMBER, 210))
        if i:
            d.line((x - 44, y + 13, x, y + 13), fill=(*AMBER, 150), width=6)
    arrow(d, 620, 1320, 820, 1320, WHITE, 11)
    d.ellipse((670, 1235, 770, 1335), outline=(*WHITE, 180), width=7)
    lower_panel(d)
    return im


def scene_04() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 470, AMBER, 42)
    card(d, (130, 900, 1310, 1790), (17, 38, 69, 242), (*CYAN, 215), 7, 42)
    rows = [(1040, TEAL, 820), (1280, VIOLET, 650), (1520, AMBER, 480)]
    for y, color, width in rows:
        d.rounded_rectangle((720 - width // 2, y, 720 + width // 2, y + 92), radius=24, fill=(*color, 190))
        d.ellipse((704, y + 30, 736, y + 62), fill=(*WHITE, 225))
    d.line((720, 1790, 720, 1980), fill=(*WHITE, 90), width=7)
    d.arc((360, 1730, 1080, 2240), 192, 348, fill=(*VIOLET, 215), width=14)
    d.line((720, 2020, 930, 1880), fill=(*WHITE, 220), width=12)
    d.ellipse((690, 1990, 750, 2050), fill=(*WHITE, 230))
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0010_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
