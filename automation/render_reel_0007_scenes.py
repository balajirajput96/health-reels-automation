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


def gradient():
    im = Image.new('RGB', (W, H), BG)
    p = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * 0.52, y - H * 0.28) / (W * 0.95))
            p[x, y] = (min(255, int(7 + 10 * t + 8 * glow)), min(255, int(15 + 18 * t + 19 * glow)), min(255, int(36 + 37 * t + 28 * glow)))
    return im


def glow_circle(base, center, radius, color, alpha=70):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    base.paste(layer, (0, 0), layer)


def network(im, cx, cy, scale=1.0, seed=0):
    rng = random.Random(seed)
    pts = []
    for i in range(26):
        a = i / 26 * math.tau + rng.uniform(-0.12, 0.12)
        r = rng.uniform(120, 380) * scale
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.65))
    d = ImageDraw.Draw(im, 'RGBA')
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i + 1:]:
            if math.hypot(x2 - x1, y2 - y1) < 315 * scale:
                d.line((x1, y1, x2, y2), fill=(*TEAL, 62), width=max(2, int(4 * scale)))
    for i, (x, y) in enumerate(pts):
        c = AMBER if i % 7 == 0 else CYAN
        r = max(8, int(14 * scale))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*c, 215))


def card(d, box, fill, outline, width=6, radius=42):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def safe_lower_third(d):
    d.rounded_rectangle((86, 1835, 1354, 2450), radius=60, fill=(4, 10, 27, 112))


def scan_slice(d, x, y, w, h, color, offset=0):
    card(d, (x, y, x + w, y + h), (18, 43, 74, 232), (*color, 220), 7, 34)
    for i in range(7):
        yy = y + 70 + i * int((h - 120) / 7)
        d.line((x + 44, yy, x + w - 44, yy), fill=(*color, 52), width=5)
    d.ellipse((x + 80 + offset, y + 130, x + w - 80 + offset, y + h - 115), outline=(*color, 190), width=11)
    d.arc((x + 125, y + 175, x + w - 125, y + h - 165), 195, 350, fill=(*AMBER, 210), width=9)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 525), 480, TEAL, 50)
    network(im, 720, 520, 0.9, 31)
    scan_slice(d, 130, 950, 500, 590, TEAL, -12)
    scan_slice(d, 810, 950, 500, 590, AMBER, 12)
    d.line((630, 1245, 810, 1245), fill=(*WHITE, 215), width=12)
    d.polygon([(818, 1245), (775, 1218), (775, 1272)], fill=(*WHITE, 215))
    d.ellipse((635, 1160, 805, 1330), outline=(*VIOLET, 225), width=9)
    safe_lower_third(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 520), 450, CYAN, 45)
    network(im, 720, 510, 0.76, 37)
    colors = [TEAL, CYAN, VIOLET, AMBER]
    labels_y = [900, 1135, 1370, 1605]
    for i, (color, yy) in enumerate(zip(colors, labels_y)):
        card(d, (150, yy, 1290, yy + 150), (17, 38, 69, 240), (*color, 210), 7, 30)
        x0 = 255
        for j in range(7):
            h = 28 + ((j * 17 + i * 13) % 70)
            d.rounded_rectangle((x0 + j * 125, yy + 112 - h, x0 + j * 125 + 58, yy + 112), radius=12, fill=(*color, 185))
        d.line((205, yy + 112, 1240, yy + 112), fill=(*WHITE, 90), width=5)
    safe_lower_third(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 500), 460, VIOLET, 46)
    network(im, 720, 510, 0.66, 41)
    # Behavioural task beside a scan: converging evidence, not fabricated data.
    card(d, (135, 900, 650, 1585), (17, 38, 69, 238), (*TEAL, 215), 7, 36)
    card(d, (790, 900, 1305, 1585), (17, 38, 69, 238), (*AMBER, 215), 7, 36)
    for j in range(5):
        yy = 1015 + j * 100
        d.line((205, yy, 580, yy), fill=(*WHITE, 95), width=8)
        d.ellipse((235 + j * 55, yy - 23, 281 + j * 55, yy + 23), fill=(*TEAL, 210))
    for j in range(3):
        d.ellipse((930 + j * 105, 1110 + j * 50, 1015 + j * 105, 1195 + j * 50), outline=(*AMBER, 200), width=9)
    d.line((1050, 1035, 1050, 1425), fill=(*AMBER, 120), width=8)
    d.line((870, 1450, 1230, 1450), fill=(*WHITE, 100), width=8)
    d.line((870, 1450, 1180, 1275), fill=(*AMBER, 225), width=12)
    d.ellipse((1160, 1255, 1200, 1295), fill=(*AMBER, 235))
    d.line((650, 1230, 790, 1230), fill=(*WHITE, 190), width=10)
    safe_lower_third(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 510), 460, AMBER, 42)
    network(im, 720, 500, 0.55, 47)
    # Converging evidence funnel with explicit uncertainty boundary.
    card(d, (180, 890, 1260, 1530), (17, 38, 69, 240), (*CYAN, 215), 7, 42)
    for y, color, width in [(1030, TEAL, 790), (1190, VIOLET, 620), (1350, AMBER, 450)]:
        d.line((720 - width // 2, y, 720 + width // 2, y), fill=(*color, 205), width=18)
        d.ellipse((720 - 18, y - 18, 720 + 18, y + 18), fill=(*WHITE, 220))
    d.line((720, 850, 720, 1720), fill=(*WHITE, 72), width=5)
    d.arc((410, 1540, 1030, 2070), 190, 350, fill=(*VIOLET, 215), width=14)
    d.line((720, 1810, 910, 1695), fill=(*WHITE, 220), width=12)
    d.ellipse((690, 1780, 750, 1840), fill=(*WHITE, 230))
    safe_lower_third(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0007_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
