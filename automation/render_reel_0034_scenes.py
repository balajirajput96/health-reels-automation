from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 14, 35); WHITE = (235, 244, 252); TEAL = (61, 220, 194)
CYAN = (93, 177, 244); AMBER = (249, 184, 77); VIOLET = (163, 124, 239); RED = (241, 105, 119)


def base():
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            g = max(0, 1 - math.hypot(x - W * .50, y - H * .26) / (W * .96))
            px[x, y] = (min(255, int(7 + 10*t + 8*g)), min(255, int(14 + 18*t + 18*g)), min(255, int(35 + 38*t + 28*g)))
    return im


def glow(im, x, y, r, c, a=64):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*c, a))
    layer = layer.filter(ImageFilter.GaussianBlur(r * .55))
    im.paste(layer, (0, 0), layer)


def card(d, box, color):
    d.rounded_rectangle(box, radius=42, fill=(16, 38, 69, 242), outline=(*color, 225), width=7)


def footer(d):
    d.rounded_rectangle((82, 1840, 1358, 2460), radius=60, fill=(3, 9, 25, 145))


def dot(d, x, y, color, r=20):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, 230))


def check(d, x, y, color):
    d.ellipse((x-58, y-58, x+58, y+58), fill=(*color, 210), outline=(*WHITE, 220), width=8)
    d.line((x-27, y+2, x-4, y+25), fill=(*BG, 230), width=13)
    d.line((x-4, y+25, x+34, y-30), fill=(*BG, 230), width=13)


def s1():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, VIOLET)
    card(d, (90, 720, 655, 1450), CYAN); card(d, (785, 720, 1350, 1450), TEAL)
    # Habitual questionnaire card.
    d.rounded_rectangle((170, 830, 575, 1025), radius=26, fill=(*WHITE, 220))
    for y, c in [(880, CYAN), (940, VIOLET), (1000, CYAN)]:
        d.rounded_rectangle((215, y, 535, y+24), radius=12, fill=(*c, 210))
    for x in [220, 310, 400, 490]:
        d.ellipse((x-16, 1100, x+16, 1132), outline=(*WHITE, 210), width=7)
    d.ellipse((396, 1096, 432, 1136), fill=(*CYAN, 230))
    d.line((235, 1230, 515, 1230), fill=(*WHITE, 180), width=12)
    d.line((235, 1300, 450, 1300), fill=(*WHITE, 130), width=12)
    # In-task instruction card.
    d.rounded_rectangle((865, 830, 1270, 1025), radius=26, fill=(*WHITE, 220))
    d.ellipse((945, 875, 1015, 945), outline=(*TEAL, 230), width=10)
    d.line((1035, 910, 1215, 910), fill=(*TEAL, 220), width=12)
    d.rounded_rectangle((885, 1080, 1250, 1165), radius=20, fill=(*TEAL, 190))
    d.line((930, 1260, 1210, 1260), fill=(*WHITE, 180), width=12)
    d.line((930, 1330, 1130, 1330), fill=(*WHITE, 130), width=12)
    d.line((655, 1080, 785, 1080), fill=(*AMBER, 210), width=12)
    dot(d, 720, 1080, AMBER, 26)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, CYAN)
    card(d, (105, 720, 1335, 1500), TEAL)
    # One instruction branches into four distinct outcome channels.
    d.rounded_rectangle((555, 820, 885, 1030), radius=30, fill=(*VIOLET, 205), outline=(*WHITE, 190), width=7)
    dot(d, 720, 895, WHITE, 34)
    d.line((720, 929, 720, 1030), fill=(*WHITE, 200), width=12)
    branches = [(300, 1190, CYAN), (590, 1190, AMBER), (880, 1190, VIOLET), (1170, 1190, RED)]
    for x, y, c in branches:
        d.line((720, 1030, x, y-100), fill=(*c, 205), width=11)
        card(d, (x-135, y-90, x+135, y+180), c)
        if c is CYAN:
            for yy in [y-15, y+45, y+105]: d.line((x-75, yy, x+75, yy), fill=(*WHITE, 190), width=10)
        elif c is AMBER:
            d.line((x-85, y+110, x-25, y+40), fill=(*WHITE, 190), width=9)
            d.line((x-25, y+40, x+20, y+75), fill=(*WHITE, 190), width=9)
            d.line((x+20, y+75, x+85, y-5), fill=(*WHITE, 190), width=9)
        elif c is VIOLET:
            d.arc((x-75, y-15, x+75, y+135), 200, 340, fill=(*WHITE, 190), width=10)
            d.arc((x-52, y+15, x+52, y+120), 20, 160, fill=(*WHITE, 130), width=8)
        else:
            for i in range(5): dot(d, x-80+i*40, y+65+int(35*math.sin(i)), WHITE, 10)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER)
    card(d, (105, 730, 1335, 1490), VIOLET)
    # Different trajectories intentionally show that channels need not agree.
    axes = (215, 1370, 1225, 850)
    d.line((axes[0], axes[1], axes[2], axes[1]), fill=(*WHITE, 180), width=10)
    d.line((axes[0], axes[1], axes[0], axes[3]), fill=(*WHITE, 180), width=10)
    series = [(CYAN, [1280, 1180, 1080, 990, 900]), (AMBER, [1230, 1250, 1210, 1190, 1170]), (TEAL, [1300, 1260, 1190, 1120, 1050])]
    for color, ys in series:
        pts = [(300 + i*190, y) for i, y in enumerate(ys)]
        d.line(pts, fill=(*color, 225), width=18, joint='curve')
        for x, y in pts: dot(d, x, y, color, 20)
    d.rounded_rectangle((250, 1560, 1190, 1700), radius=28, fill=(3, 9, 25, 180), outline=(*WHITE, 120), width=5)
    for i, c in enumerate([CYAN, AMBER, TEAL]):
        d.line((330+i*270, 1630, 430+i*270, 1630), fill=(*c, 220), width=14)
        dot(d, 455+i*270, 1630, c, 13)
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, RED)
    card(d, (100, 720, 1340, 1430), RED)
    # Interpretation guardrails: outcome, timing, task, sample, purpose.
    checkpoints = [(250, 930, CYAN), (490, 930, VIOLET), (730, 930, AMBER), (970, 930, TEAL), (1210, 930, WHITE)]
    for x, y, c in checkpoints: check(d, x, y, c)
    for a, b in zip(checkpoints, checkpoints[1:]):
        d.line((a[0]+64, a[1], b[0]-64, b[1]), fill=(*WHITE, 165), width=9)
    card(d, (220, 1160, 1220, 1360), TEAL)
    d.line((350, 1260, 1090, 1260), fill=(*WHITE, 175), width=11)
    for x in [430, 620, 810, 1000]: dot(d, x, 1260, TEAL, 22)
    footer(d); return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0034_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
