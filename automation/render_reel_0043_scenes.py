from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 12, 35)
WHITE = (239, 247, 252)
TEAL = (54, 218, 184)
CYAN = (83, 180, 246)
AMBER = (248, 180, 72)
VIOLET = (165, 124, 242)
RED = (239, 103, 119)


def base():
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            g = max(0, 1 - math.hypot(x - W * 0.5, y - H * 0.23) / (W * 0.98))
            px[x, y] = (int(7 + 11 * t + 8 * g), int(12 + 17 * t + 18 * g), int(35 + 32 * t + 30 * g))
    return im


def glow(im, x, y, r, color, alpha=60):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((x-r, y-r, x+r, y+r), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    im.paste(layer, (0, 0), layer)


def card(d, box, color):
    d.rounded_rectangle(box, radius=42, fill=(14, 35, 68, 242), outline=(*color, 225), width=7)


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
    # Assigned training dose: calendar plus separate duration bars.
    d.rounded_rectangle((190, 850, 650, 1340), radius=34, fill=(*CYAN, 120), outline=(*WHITE, 180), width=7)
    d.line((235, 965, 605, 965), fill=(*WHITE, 190), width=9)
    for i in range(4):
        for j in range(3):
            dot(d, 280 + j * 105, 1060 + i * 72, (TEAL if (i+j) % 2 else AMBER), 17)
    d.rounded_rectangle((820, 880, 1220, 1060), radius=28, fill=(*TEAL, 135), outline=(*WHITE, 180), width=6)
    d.rounded_rectangle((820, 1140, 1220, 1320), radius=28, fill=(*AMBER, 135), outline=(*WHITE, 180), width=6)
    d.line((880, 970, 1140, 970), fill=(*WHITE, 205), width=13)
    d.line((880, 1230, 1170, 1230), fill=(*WHITE, 205), width=13)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER); card(d, (100, 720, 1340, 1490), AMBER)
    # Adherence self-report, questionnaire outcome, and dropout are separate instruments.
    d.rounded_rectangle((180, 850, 600, 1320), radius=32, fill=(*TEAL, 125), outline=(*WHITE, 180), width=7)
    for y in (950, 1050, 1150):
        d.rounded_rectangle((250, y, 315, y+65), radius=12, fill=(*WHITE, 180))
        d.line((350, y+32, 520, y+32), fill=(*WHITE, 195), width=9)
        check(d, 282, y+32, TEAL)
    d.rounded_rectangle((760, 850, 1240, 1080), radius=32, fill=(*VIOLET, 125), outline=(*WHITE, 180), width=7)
    d.line((830, 950, 1160, 950), fill=(*WHITE, 190), width=10)
    for x, h, c in ((850, 80, CYAN), (945, 140, TEAL), (1040, 115, AMBER), (1135, 175, VIOLET)):
        d.rounded_rectangle((x, 1010-h, x+48, 1010), radius=10, fill=(*c, 220))
    d.rounded_rectangle((760, 1160, 1240, 1320), radius=32, fill=(*RED, 125), outline=(*WHITE, 180), width=7)
    d.line((840, 1240, 1060, 1240), fill=(*WHITE, 190), width=10)
    d.line((1120, 1190, 1190, 1290), fill=(*WHITE, 190), width=11)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, VIOLET); card(d, (100, 720, 1340, 1490), VIOLET)
    # EEG signal entering a transparent model and output labels, not a thought-reader.
    d.ellipse((190, 850, 610, 1270), fill=(*CYAN, 92), outline=(*WHITE, 180), width=7)
    for x, y in ((300, 960), (470, 930), (360, 1120), (510, 1160)):
        dot(d, x, y, TEAL, 22); d.line((x, y, 720, 1080), fill=(*TEAL, 105), width=5)
    d.rounded_rectangle((700, 880, 1110, 1260), radius=30, fill=(19, 50, 85, 230), outline=(*AMBER, 220), width=7)
    for y in (980, 1070, 1160):
        d.line((780, y, 1030, y), fill=(*WHITE, 180), width=9)
    d.line((1160, 1080, 1280, 1080), fill=(*WHITE, 190), width=9)
    d.polygon([(1280,1080),(1225,1045),(1225,1115)], fill=(*AMBER, 220))
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, TEAL); card(d, (100, 720, 1340, 1490), TEAL)
    # Protocol timeline and interpretation questions.
    d.line((230, 980, 1210, 980), fill=(*WHITE, 185), width=10)
    for x, c in ((300, CYAN), (520, TEAL), (740, AMBER), (960, VIOLET), (1160, RED)):
        dot(d, x, 980, c, 25)
    d.rounded_rectangle((180, 1120, 1260, 1330), radius=30, fill=(9, 23, 50, 210), outline=(*WHITE, 170), width=6)
    d.line((270, 1225, 1170, 1225), fill=(*WHITE, 160), width=8)
    for x, c in ((320, TEAL), (540, CYAN), (760, AMBER), (980, VIOLET)):
        check(d, x, 1225, c)
    for y, c in ((1900, TEAL), (2070, AMBER), (2230, RED)):
        check(d, 230, y, c); d.line((340, y, 1170, y), fill=(*WHITE, 155), width=8)
    return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0043_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
