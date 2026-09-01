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
            p[x, y] = (
                min(255, int(7 + 10 * t + 8 * glow)),
                min(255, int(15 + 18 * t + 19 * glow)),
                min(255, int(36 + 37 * t + 28 * glow)),
            )
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


def node_network(d: ImageDraw.ImageDraw, cx: int, cy: int, scale: float, seed: int) -> None:
    rng = random.Random(seed)
    pts = []
    for i in range(24):
        a = i / 24 * math.tau + rng.uniform(-0.14, 0.14)
        r = rng.uniform(110, 360) * scale
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.66))
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i + 1:]:
            if math.hypot(x2 - x1, y2 - y1) < 300 * scale:
                d.line((x1, y1, x2, y2), fill=(*TEAL, 62), width=max(2, int(4 * scale)))
    for i, (x, y) in enumerate(pts):
        c = AMBER if i % 6 == 0 else CYAN
        r = max(9, int(15 * scale))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*c, 220))


def lower_panel(d: ImageDraw.ImageDraw) -> None:
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 120))


def arrow(d: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, color=WHITE, width: int = 10) -> None:
    d.line((x1, y1, x2, y2), fill=(*color, 215), width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 34
    left = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    right = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), left, right], fill=(*color, 215))


def scene_01() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 500), 500, TEAL, 42)
    node_network(d, 720, 500, 0.78, 801)
    # Repeated choice-feedback loop: abstract cards, tokens, and arrows.
    card(d, (130, 900, 610, 1430), (17, 38, 69, 240), (*TEAL, 215), 7, 38)
    card(d, (830, 900, 1310, 1430), (17, 38, 69, 240), (*AMBER, 215), 7, 38)
    d.ellipse((300, 1040, 440, 1180), outline=(*TEAL, 220), width=12)
    d.ellipse((1000, 1040, 1140, 1180), outline=(*AMBER, 220), width=12)
    arrow(d, 610, 1165, 830, 1165, WHITE, 12)
    arrow(d, 1060, 1430, 1060, 1640, AMBER, 11)
    arrow(d, 380, 1640, 380, 1430, TEAL, 11)
    d.arc((260, 1400, 1170, 1850), 8, 172, fill=(*VIOLET, 190), width=12)
    lower_panel(d)
    return im


def scene_02() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 470), 470, CYAN, 44)
    node_network(d, 720, 475, 0.65, 802)
    # A model pipeline with expectation, outcome, and error.
    boxes = [(120, 920, 1320, 1190), (120, 1280, 1320, 1550), (120, 1640, 1320, 1910)]
    colors = [VIOLET, AMBER, TEAL]
    for i, (box, c) in enumerate(zip(boxes, colors)):
        card(d, box, (17, 38, 69, 242), (*c, 215), 7, 38)
        x0, y0, x1, y1 = box
        for j in range(8):
            xx = x0 + 130 + j * 135
            h = 30 + ((j * 29 + i * 41) % 110)
            d.rounded_rectangle((xx, y1 - 78 - h, xx + 58, y1 - 78), radius=12, fill=(*c, 205))
        d.line((x0 + 80, y1 - 78, x1 - 80, y1 - 78), fill=(*WHITE, 82), width=5)
    arrow(d, 720, 1195, 720, 1260, WHITE, 10)
    arrow(d, 720, 1555, 720, 1620, WHITE, 10)
    d.line((310, 1050, 1130, 1050), fill=(*WHITE, 95), width=5)
    d.line((310, 1410, 1130, 1410), fill=(*WHITE, 95), width=5)
    d.line((310, 1770, 1130, 1770), fill=(*WHITE, 95), width=5)
    lower_panel(d)
    return im


def scene_03() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 480), 480, VIOLET, 42)
    node_network(d, 720, 480, 0.58, 803)
    # Model estimate on the left and indirect BOLD waveform on the right.
    card(d, (110, 900, 650, 1720), (17, 38, 69, 240), (*TEAL, 215), 7, 38)
    card(d, (790, 900, 1330, 1720), (17, 38, 69, 240), (*AMBER, 215), 7, 38)
    for j in range(7):
        x = 190 + j * 57
        y = 1450 - (j * 73 % 290)
        d.ellipse((x, y, x + 30, y + 30), fill=(*TEAL, 220))
        if j:
            d.line((x - 27, y + 15, x, y + 15), fill=(*TEAL, 175), width=7)
    base_y = 1430
    pts = []
    for i in range(80):
        x = 850 + i * 5.3
        y = base_y - 95 * math.sin(i / 7.4) - 38 * math.sin(i / 2.9)
        pts.append((x, y))
    d.line(pts, fill=(*AMBER, 220), width=10)
    arrow(d, 650, 1310, 790, 1310, WHITE, 12)
    d.ellipse((676, 1235, 764, 1323), outline=(*WHITE, 180), width=6)
    d.line((720, 900, 720, 1810), fill=(*WHITE, 48), width=5)
    lower_panel(d)
    return im


def scene_04() -> Image.Image:
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 490), 470, AMBER, 40)
    node_network(d, 720, 490, 0.50, 804)
    # Context guardrail: observed, inferred, and limits remain separate.
    card(d, (150, 900, 1290, 1740), (17, 38, 69, 242), (*CYAN, 215), 7, 42)
    rows = [(1010, TEAL, 770), (1230, VIOLET, 620), (1450, AMBER, 470)]
    for y, c, width in rows:
        d.rounded_rectangle((720 - width // 2, y, 720 + width // 2, y + 92), radius=24, fill=(*c, 190))
        d.ellipse((720 - 16, y + 30, 720 + 16, y + 62), fill=(*WHITE, 220))
    d.line((720, 1740, 720, 1940), fill=(*WHITE, 90), width=7)
    d.arc((360, 1700, 1080, 2230), 192, 348, fill=(*VIOLET, 215), width=14)
    d.line((720, 1990, 910, 1875), fill=(*WHITE, 220), width=12)
    d.ellipse((690, 1960, 750, 2020), fill=(*WHITE, 230))
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0008_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
