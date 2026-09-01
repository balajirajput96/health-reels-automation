from __future__ import annotations

import math
import random
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
MUTED = (135, 164, 198)


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


def lower_panel(d: ImageDraw.ImageDraw) -> None:
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 130))


def arrow(d: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, color=WHITE, width: int = 10) -> None:
    d.line((x1, y1, x2, y2), fill=(*color, 215), width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 34
    left = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    right = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), left, right], fill=(*color, 215))


def ecg_points(x0: float, y0: float, width: float, cycles: int, amp: float) -> list[tuple[float, float]]:
    pts = []
    for i in range(180):
        t = i / 179
        x = x0 + width * t
        phase = (t * cycles) % 1.0
        if phase < 0.72:
            y = y0 + 12 * math.sin(phase * math.tau)
        elif phase < 0.78:
            y = y0 - amp * (phase - 0.72) / 0.06
        elif phase < 0.83:
            y = y0 + amp * (phase - 0.78) / 0.05
        else:
            y = y0 + 10 * math.sin((phase - 0.83) * math.tau * 2)
        pts.append((x, y))
    return pts


def signal_dots(d: ImageDraw.ImageDraw, x0: int, y: int, count: int, color=TEAL) -> None:
    for i in range(count):
        x = x0 + i * 130
        r = 15 if i % 3 else 22
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*color, 220))
        if i:
            d.line((x - 130 + 20, y, x - 20, y), fill=(*color, 110), width=6)


def scene_01() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 520, TEAL, 42)
    d.line(ecg_points(150, 650, 1140, 4, 210), fill=(*TEAL, 230), width=12)
    for x in (310, 590, 870, 1150):
        d.ellipse((x - 24, 626, x + 24, 674), outline=(*WHITE, 215), width=7)
        d.line((x, 700, x, 880), fill=(*WHITE, 90), width=5)
    card(d, (130, 980, 1310, 1500), (17, 38, 69, 240), (*CYAN, 215), 7, 38)
    signal_dots(d, 250, 1190, 7, TEAL)
    arrow(d, 720, 840, 720, 970, WHITE, 11)
    d.ellipse((610, 1550, 830, 1770), outline=(*AMBER, 220), width=12)
    d.line((720, 1500, 720, 1560), fill=(*AMBER, 200), width=9)
    lower_panel(d)
    return im


def scene_02() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 460), 480, AMBER, 40)
    card(d, (125, 900, 1315, 1290), (17, 38, 69, 242), (*AMBER, 215), 7, 38)
    d.ellipse((275, 1000, 420, 1145), outline=(*AMBER, 220), width=10)
    signal_dots(d, 540, 1070, 5, AMBER)
    card(d, (170, 1390, 630, 1780), (17, 38, 69, 242), (*VIOLET, 215), 7, 34)
    card(d, (810, 1390, 1270, 1780), (17, 38, 69, 242), (*CYAN, 215), 7, 34)
    for i in range(5):
        x = 230 + i * 76
        d.ellipse((x, 1540 - (i % 2) * 70, x + 30, 1570 - (i % 2) * 70), fill=(*VIOLET, 220))
    for i in range(5):
        x = 870 + i * 76
        d.ellipse((x, 1540 - (i % 3) * 45, x + 30, 1570 - (i % 3) * 45), fill=(*CYAN, 220))
    arrow(d, 630, 1585, 810, 1585, WHITE, 11)
    d.arc((330, 1760, 1110, 2210), 190, 350, fill=(*WHITE, 125), width=10)
    lower_panel(d)
    return im


def scene_03() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 450), 500, VIOLET, 40)
    boxes = [(90, 900, 430, 1710), (550, 900, 890, 1710), (1010, 900, 1350, 1710)]
    colors = [TEAL, VIOLET, AMBER]
    for box, color in zip(boxes, colors):
        card(d, box, (17, 38, 69, 240), (*color, 215), 7, 35)
    d.line(ecg_points(145, 1300, 230, 3, 120), fill=(*TEAL, 220), width=8)
    for i in range(5):
        d.rounded_rectangle((620, 1110 + i * 92, 820, 1150 + i * 92), radius=18, fill=(*VIOLET, 180 - i * 12))
    d.arc((1060, 1110, 1300, 1500), 200, 340, fill=(*AMBER, 220), width=10)
    d.line((1180, 1305, 1180, 1510), fill=(*AMBER, 190), width=8)
    d.ellipse((1148, 1468, 1212, 1532), fill=(*WHITE, 210))
    arrow(d, 430, 1300, 550, 1300, WHITE, 9)
    arrow(d, 890, 1300, 1010, 1300, WHITE, 9)
    lower_panel(d)
    return im


def scene_04() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 470, CYAN, 42)
    card(d, (140, 880, 1300, 1790), (17, 38, 69, 242), (*CYAN, 215), 7, 42)
    rows = [(1030, TEAL, 820), (1260, VIOLET, 650), (1490, AMBER, 480)]
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
    path = OUT / f'reel_0009_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
