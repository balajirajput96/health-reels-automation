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
    # Subjective attention-awareness questionnaire as one measurement layer.
    d.rounded_rectangle((190, 860, 1250, 1320), radius=36, fill=(*TEAL, 145), outline=(*WHITE, 190), width=7)
    d.rounded_rectangle((300, 940, 1140, 1035), radius=24, fill=(8, 20, 46, 220), outline=(*WHITE, 180), width=5)
    d.line((390, 987, 1030, 987), fill=(*WHITE, 205), width=10)
    for x, c in ((430, CYAN), (610, TEAL), (790, AMBER), (970, VIOLET)):
        dot(d, x, 987, c, 23)
    d.rounded_rectangle((360, 1140, 1080, 1210), radius=20, fill=(*VIOLET, 135), outline=(*WHITE, 160), width=5)
    d.line((440, 1175, 1010, 1175), fill=(*WHITE, 180), width=8)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER); card(d, (100, 720, 1340, 1490), AMBER)
    # Task-specific response-time and error outcomes.
    d.rounded_rectangle((180, 850, 770, 1330), radius=34, fill=(*CYAN, 135), outline=(*WHITE, 190), width=7)
    for i, x in enumerate((280, 410, 540, 670)):
        c = (RED, TEAL, RED, AMBER)[i]
        d.rounded_rectangle((x, 950, x+72, 1050), radius=14, fill=(*c, 210), outline=(*WHITE, 170), width=4)
    d.line((280, 1190, 670, 1190), fill=(*WHITE, 200), width=12)
    for x, h, c in ((300, 110, TEAL), (430, 190, CYAN), (560, 145, AMBER), (650, 220, VIOLET)):
        d.rounded_rectangle((x, 1190-h, x+45, 1190), radius=12, fill=(*c, 210))
    d.rounded_rectangle((900, 870, 1220, 1290), radius=34, fill=(*RED, 125), outline=(*WHITE, 180), width=7)
    d.line((970, 990, 1145, 990), fill=(*WHITE, 210), width=10)
    d.line((970, 1080, 1110, 1080), fill=(*WHITE, 210), width=10)
    d.line((970, 1170, 1060, 1170), fill=(*WHITE, 210), width=10)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, VIOLET); card(d, (100, 720, 1340, 1490), VIOLET)
    # Generic EEG/ERP electrodes and time-locked waveform; not a mind-reading device.
    d.ellipse((250, 850, 720, 1320), fill=(*CYAN, 95), outline=(*WHITE, 190), width=7)
    for x, y in ((360, 960), (530, 930), (430, 1120), (590, 1160)):
        dot(d, x, y, TEAL, 22); d.line((x, y, 860, 1110), fill=(*TEAL, 100), width=5)
    d.line((800, 1110, 1240, 1110), fill=(*WHITE, 180), width=10)
    points = [(820,1110),(870,1110),(900,980),(930,1190),(970,1080),(1010,1110),(1060,1010),(1100,1140),(1150,1090),(1210,1110)]
    d.line(points, fill=(*AMBER, 230), width=10, joint='curve')
    d.line((900, 900, 900, 1280), fill=(*RED, 150), width=6)
    d.line((1060, 900, 1060, 1280), fill=(*RED, 150), width=6)
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, TEAL); card(d, (100, 720, 1340, 1490), TEAL)
    # Randomized timeline, comparison group, small final sample and method checklist.
    d.line((220, 980, 1220, 980), fill=(*WHITE, 185), width=10)
    for x, c in ((300, CYAN), (520, TEAL), (740, AMBER), (960, VIOLET), (1160, RED)):
        dot(d, x, 980, c, 25)
    d.rounded_rectangle((180, 1110, 580, 1330), radius=28, fill=(*CYAN, 145), outline=(*WHITE, 170), width=6)
    d.rounded_rectangle((860, 1110, 1260, 1330), radius=28, fill=(*AMBER, 145), outline=(*WHITE, 170), width=6)
    d.line((580, 1220, 860, 1220), fill=(*WHITE, 150), width=8)
    for y, color in ((1900, TEAL), (2070, AMBER), (2230, RED)):
        check(d, 230, y, color); d.line((340, y, 1170, y), fill=(*WHITE, 155), width=8)
    return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0042_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
