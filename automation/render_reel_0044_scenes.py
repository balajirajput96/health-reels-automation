from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (6, 13, 34)
WHITE = (238, 246, 252)
TEAL = (56, 220, 186)
CYAN = (87, 178, 244)
AMBER = (249, 184, 75)
VIOLET = (163, 125, 241)
RED = (241, 105, 120)


def base():
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            g = max(0, 1 - math.hypot(x - W * 0.5, y - H * 0.23) / (W * 0.98))
            px[x, y] = (int(6 + 11 * t + 8 * g), int(13 + 17 * t + 17 * g), int(34 + 35 * t + 30 * g))
    return im


def glow(im, x, y, r, color, alpha=60):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((x-r, y-r, x+r, y+r), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    im.paste(layer, (0, 0), layer)


def card(d, box, color):
    d.rounded_rectangle(box, radius=42, fill=(14, 36, 68, 242), outline=(*color, 225), width=7)


def footer(d):
    d.rounded_rectangle((82, 1840, 1358, 2460), radius=60, fill=(3, 8, 25, 145))


def dot(d, x, y, color, r=20):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, 230))


def check(d, x, y, color):
    d.ellipse((x-58, y-58, x+58, y+58), fill=(*color, 210), outline=(*WHITE, 220), width=8)
    d.line((x-27, y+2, x-4, y+25), fill=(*BG, 230), width=13)
    d.line((x-4, y+25, x+34, y-30), fill=(*BG, 230), width=13)


def s1():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, CYAN); card(d, (100, 720, 1340, 1490), CYAN)
    # Breath-counting cycles, counter, and probe markers.
    d.ellipse((250, 850, 640, 1240), fill=(*CYAN, 105), outline=(*WHITE, 185), width=7)
    d.arc((330, 930, 560, 1160), 205, 520, fill=(*TEAL, 225), width=18)
    d.ellipse((430, 1045, 460, 1075), fill=(*AMBER, 230))
    d.rounded_rectangle((780, 850, 1210, 1080), radius=32, fill=(*TEAL, 125), outline=(*WHITE, 180), width=7)
    for i, x in enumerate((850, 950, 1050, 1150), 1):
        dot(d, x, 965, (AMBER if i % 2 == 0 else WHITE), 22)
        d.line((x, 1015, x, 1060), fill=(*WHITE, 160), width=8)
    d.line((280, 1320, 1160, 1320), fill=(*WHITE, 185), width=10)
    for x, c in ((340, TEAL), (560, TEAL), (780, RED), (1000, TEAL)):
        dot(d, x, 1320, c, 25)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER); card(d, (100, 720, 1340, 1490), AMBER)
    # Behavioral accuracy versus subjective self-report.
    d.rounded_rectangle((170, 850, 660, 1320), radius=32, fill=(*CYAN, 120), outline=(*WHITE, 180), width=7)
    for y, c in ((960, TEAL), (1080, RED), (1200, TEAL)):
        check(d, 270, y, c); d.line((370, y, 570, y), fill=(*WHITE, 190), width=9)
    d.rounded_rectangle((820, 850, 1250, 1320), radius=32, fill=(*VIOLET, 120), outline=(*WHITE, 180), width=7)
    d.line((900, 980, 1170, 980), fill=(*WHITE, 185), width=10)
    d.line((900, 1090, 1100, 1090), fill=(*WHITE, 185), width=10)
    d.line((900, 1200, 1140, 1200), fill=(*WHITE, 185), width=10)
    dot(d, 930, 980, AMBER, 22); dot(d, 1130, 1090, TEAL, 22); dot(d, 1050, 1200, CYAN, 22)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, VIOLET); card(d, (100, 720, 1340, 1490), VIOLET)
    # Generic chest-belt respiratory waveform and controlled-resistance blocks.
    d.rounded_rectangle((190, 880, 600, 1260), radius=100, fill=(*CYAN, 88), outline=(*WHITE, 175), width=7)
    d.arc((260, 900, 530, 1240), 195, 520, fill=(*TEAL, 230), width=18)
    d.line((700, 1090, 1240, 1090), fill=(*WHITE, 180), width=10)
    points = [(720,1090),(780,1090),(830,980),(880,1180),(930,1080),(990,1090),(1040,1000),(1090,1150),(1150,1060),(1220,1090)]
    d.line(points, fill=(*AMBER, 230), width=10, joint='curve')
    for x, y, c in ((760, 1350, CYAN), (900, 1350, AMBER), (1040, 1350, RED)):
        d.rounded_rectangle((x, 1300, x+95, 1400), radius=20, fill=(*c, 190), outline=(*WHITE, 150), width=5)
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, TEAL); card(d, (100, 720, 1340, 1490), TEAL)
    # Interpretation branches: task, channel, and design.
    d.line((720, 850, 720, 1010), fill=(*WHITE, 180), width=10)
    for x, c in ((360, CYAN), (720, AMBER), (1080, VIOLET)):
        d.line((720, 1010, x, 1160), fill=(*WHITE, 160), width=8); dot(d, x, 1160, c, 28)
        d.line((x, 1210, x, 1370), fill=(*WHITE, 150), width=8)
    for y, c in ((1900, TEAL), (2070, AMBER), (2230, RED)):
        check(d, 230, y, c); d.line((340, y, 1170, y), fill=(*WHITE, 155), width=8)
    return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0044_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
