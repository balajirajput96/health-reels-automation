from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (6, 13, 34)
WHITE = (235, 244, 252)
TEAL = (61, 220, 194)
CYAN = (93, 177, 244)
AMBER = (249, 184, 77)
VIOLET = (163, 124, 239)
RED = (241, 105, 119)


def base():
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            g = max(0, 1 - math.hypot(x - W * 0.5, y - H * 0.24) / (W * 0.97))
            px[x, y] = (int(6 + 10 * t + 8 * g), int(13 + 18 * t + 18 * g), int(34 + 38 * t + 28 * g))
    return im


def glow(im, x, y, r, color, alpha=62):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    im.paste(layer, (0, 0), layer)


def card(d, box, color):
    d.rounded_rectangle(box, radius=42, fill=(15, 37, 68, 242), outline=(*color, 225), width=7)


def footer(d):
    d.rounded_rectangle((82, 1840, 1358, 2460), radius=60, fill=(3, 9, 25, 145))


def dot(d, x, y, color, r=20):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, 230))


def check(d, x, y, color):
    d.ellipse((x-58, y-58, x+58, y+58), fill=(*color, 210), outline=(*WHITE, 220), width=8)
    d.line((x-27, y+2, x-4, y+25), fill=(*BG, 230), width=13)
    d.line((x-4, y+25, x+34, y-30), fill=(*BG, 230), width=13)


def s1():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, CYAN); card(d, (100, 720, 1340, 1490), CYAN)
    # Self-description card separated from a crossed-out hidden-personality scanner.
    d.rounded_rectangle((180, 870, 760, 1320), radius=36, fill=(*TEAL, 155), outline=(*WHITE, 190), width=7)
    d.rounded_rectangle((270, 960, 670, 1080), radius=24, fill=(8, 20, 46, 220), outline=(*WHITE, 180), width=5)
    d.ellipse((320, 1000, 390, 1070), outline=(*WHITE, 220), width=9)
    d.line((410, 1035, 600, 1035), fill=(*WHITE, 220), width=10)
    d.line((260, 1160, 680, 1160), fill=(*WHITE, 175), width=9)
    d.line((260, 1220, 560, 1220), fill=(*WHITE, 145), width=9)
    d.rounded_rectangle((900, 880, 1230, 1300), radius=34, fill=(*VIOLET, 140), outline=(*WHITE, 180), width=7)
    d.ellipse((970, 960, 1160, 1150), outline=(*WHITE, 210), width=12)
    d.line((940, 920, 1190, 1190), fill=(*RED, 230), width=18)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, TEAL); card(d, (100, 720, 1340, 1490), TEAL)
    # Frequency, context, automaticity and longitudinal score are distinct channels.
    boxes = [(170, 850, 610, 1080), (830, 850, 1270, 1080), (170, 1160, 610, 1390), (830, 1160, 1270, 1390)]
    colors = [CYAN, AMBER, VIOLET, RED]
    for box, color in zip(boxes, colors):
        d.rounded_rectangle(box, radius=30, fill=(*color, 160), outline=(*WHITE, 190), width=6)
    for x in (270, 360, 450, 540):
        d.rounded_rectangle((x, 940, x+48, 1000), radius=12, fill=(*WHITE, 210))
    for y in (930, 1030):
        d.line((930, y, 1170, y + 40), fill=(*WHITE, 205), width=11)
        dot(d, 930, y, WHITE, 15); dot(d, 1170, y + 40, WHITE, 15)
    d.ellipse((280, 1210, 400, 1330), outline=(*WHITE, 210), width=12); d.line((340, 1270, 450, 1205), fill=(*WHITE, 210), width=12); dot(d, 340, 1270, VIOLET, 22)
    d.line((930, 1290, 1170, 1290), fill=(*WHITE, 190), width=10); dot(d, 1040, 1290, RED, 24)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER); card(d, (100, 720, 1340, 1490), AMBER)
    # A 90-day timeline with repeated behavior, self-control and habit-strength observations.
    d.line((210, 1110, 1230, 1110), fill=(*WHITE, 190), width=12)
    for i, x in enumerate((260, 430, 600, 770, 940, 1110)):
        c = (CYAN, TEAL, AMBER, VIOLET, RED, CYAN)[i]
        dot(d, x, 1110, c, 30)
        d.line((x, 1110, x, 960 if i % 2 == 0 else 1260), fill=(*c, 200), width=9)
    for j, y in enumerate((880, 1320, 1480)):
        c = (TEAL, CYAN, VIOLET)[j]
        d.line((260, y, 1160, y), fill=(*c, 125), width=8)
        for x in (360, 560, 760, 960):
            dot(d, x, y - (j * 25) + ((x // 200) % 2) * 34, c, 16)
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, VIOLET); card(d, (100, 720, 1340, 1490), VIOLET)
    # Overlapping identity and behavior circles with a dashed, non-causal bridge.
    d.ellipse((240, 850, 760, 1370), fill=(*CYAN, 85), outline=(*CYAN, 220), width=8)
    d.ellipse((680, 850, 1200, 1370), fill=(*TEAL, 85), outline=(*TEAL, 220), width=8)
    d.line((600, 1110, 840, 1110), fill=(*AMBER, 220), width=10)
    for x in (620, 690, 760, 830):
        d.ellipse((x-8, 1102, x+8, 1118), fill=(*AMBER, 230))
    for y, color in ((1900, TEAL), (2070, AMBER), (2230, RED)):
        check(d, 230, y, color); d.line((340, y, 1170, y), fill=(*WHITE, 155), width=8)
    return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0041_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
