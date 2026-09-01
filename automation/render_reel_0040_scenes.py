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
    # A path with adjustable effort: distance, steps, time and access are separate levers.
    d.rounded_rectangle((190, 900, 520, 1260), radius=34, fill=(*TEAL, 150), outline=(*WHITE, 180), width=6)
    d.ellipse((300, 1000, 410, 1110), outline=(*WHITE, 220), width=13)
    d.line((355, 1110, 355, 1170), fill=(*WHITE, 220), width=12)
    d.line((330, 1145, 380, 1145), fill=(*WHITE, 220), width=10)
    d.line((570, 1080, 850, 1080), fill=(*AMBER, 230), width=16)
    for x in (600, 700, 800):
        dot(d, x, 1080, AMBER, 20)
    d.polygon((850, 1080, 800, 1048, 800, 1112), fill=(*AMBER, 230))
    d.rounded_rectangle((930, 870, 1230, 1290), radius=34, fill=(*VIOLET, 140), outline=(*WHITE, 180), width=6)
    for y, color in ((950, CYAN), (1060, TEAL), (1170, RED)):
        d.line((990, y, 1170, y), fill=(*WHITE, 180), width=9)
        dot(d, 1040 if color != RED else 1120, y, color, 24)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, TEAL); card(d, (100, 720, 1340, 1490), TEAL)
    # Same behavior, stable place/time versus variable place/time.
    d.rounded_rectangle((170, 850, 610, 1340), radius=32, fill=(8, 20, 46, 230), outline=(*TEAL, 220), width=7)
    d.rounded_rectangle((830, 850, 1270, 1340), radius=32, fill=(8, 20, 46, 230), outline=(*AMBER, 220), width=7)
    for y in (940, 1060, 1180):
        d.rounded_rectangle((250, y-32, 530, y+32), radius=16, fill=(*TEAL, 210), outline=(*WHITE, 160), width=4)
        d.line((900, y, 1160, y + (55 if y == 1060 else -42)), fill=(*AMBER, 200), width=12)
        dot(d, 900, y, AMBER, 18); dot(d, 1160, y + (55 if y == 1060 else -42), AMBER, 18)
    d.line((610, 1090, 830, 1090), fill=(*WHITE, 150), width=8)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER); card(d, (100, 720, 1340, 1490), AMBER)
    # Four separate outcome instruments: choice, completion, response time, self-report.
    boxes = [(170, 850, 610, 1080), (830, 850, 1270, 1080), (170, 1160, 610, 1390), (830, 1160, 1270, 1390)]
    colors = [CYAN, VIOLET, TEAL, RED]
    for box, color in zip(boxes, colors):
        d.rounded_rectangle(box, radius=30, fill=(*color, 160), outline=(*WHITE, 190), width=6)
    d.ellipse((270, 920, 350, 1000), outline=(*WHITE, 210), width=9); d.ellipse((430, 920, 510, 1000), outline=(*WHITE, 210), width=9); d.line((350, 960, 430, 960), fill=(*WHITE, 210), width=8)
    d.line((920, 965, 1050, 965), fill=(*WHITE, 210), width=10); d.line((1050, 965, 1120, 900), fill=(*WHITE, 210), width=10); dot(d, 920, 965, WHITE, 16); dot(d, 1120, 900, WHITE, 16)
    d.line((260, 1275, 520, 1275), fill=(*WHITE, 210), width=10); d.line((300, 1275, 300, 1205), fill=(*WHITE, 210), width=8); d.line((390, 1275, 390, 1230), fill=(*WHITE, 210), width=8); d.line((480, 1275, 480, 1185), fill=(*WHITE, 210), width=8)
    for x in (930, 1010, 1090, 1170):
        d.line((x, 1210, x, 1330), fill=(*WHITE, 180), width=8)
    d.line((930, 1270, 1170, 1270), fill=(*WHITE, 210), width=8); dot(d, 1050, 1270, RED, 22)
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, VIOLET); card(d, (100, 720, 1340, 1490), VIOLET)
    # A spread of study estimates, including near-zero and negative values: average is not a guarantee.
    d.line((220, 1110, 1220, 1110), fill=(*WHITE, 190), width=12)
    for x, color, y in ((300, CYAN, 930), (520, TEAL, 1010), (740, AMBER, 1095), (950, RED, 1200), (1160, VIOLET, 990)):
        d.line((x, y-65, x, y+65), fill=(*color, 220), width=10)
        d.ellipse((x-30, y-30, x+30, y+30), fill=(*color, 220), outline=(*WHITE, 160), width=4)
        d.line((x, 1110, x, y), fill=(*color, 150), width=6)
    d.line((300, 1400, 1140, 1400), fill=(*WHITE, 130), width=8)
    d.line((300, 1400, 760, 1290), fill=(*TEAL, 190), width=12)
    d.line((760, 1290, 1140, 1400), fill=(*RED, 190), width=12)
    for y, color in ((1910, TEAL), (2070, AMBER), (2230, RED)):
        check(d, 230, y, color); d.line((340, y, 1170, y), fill=(*WHITE, 155), width=8)
    return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0040_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
