from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 14, 34)
WHITE = (239, 247, 252)
TEAL = (61, 222, 185)
CYAN = (88, 181, 247)
AMBER = (249, 187, 76)
VIOLET = (168, 130, 244)
ROSE = (244, 111, 134)


def base():
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            g = max(0, 1 - math.hypot(x - W * .5, y - H * .22) / (W * 1.02))
            px[x, y] = (int(7 + 11*t + 8*g), int(14 + 18*t + 17*g), int(34 + 34*t + 30*g))
    return im


def glow(im, x, y, r, color, alpha=58):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((x-r, y-r, x+r, y+r), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(r * .55))
    im.paste(layer, (0, 0), layer)


def card(d, box, color):
    d.rounded_rectangle(box, radius=44, fill=(14, 37, 69, 242), outline=(*color, 225), width=7)


def footer(d):
    d.rounded_rectangle((82, 1840, 1358, 2460), radius=60, fill=(3, 8, 25, 150))


def dot(d, x, y, color, r=22):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, 232))


def check(d, x, y, color):
    d.ellipse((x-58, y-58, x+58, y+58), fill=(*color, 210), outline=(*WHITE, 220), width=8)
    d.line((x-28, y+2, x-5, y+25), fill=(*BG, 230), width=13)
    d.line((x-5, y+25, x+35, y-32), fill=(*BG, 230), width=13)


def s1():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 530, CYAN); card(d, (100, 720, 1340, 1490), CYAN)
    d.rounded_rectangle((220, 840, 1215, 1110), radius=34, fill=(*VIOLET, 110), outline=(*WHITE, 180), width=7)
    for x, y, c in ((310, 950, TEAL), (510, 950, AMBER), (710, 950, TEAL), (910, 950, CYAN), (1110, 950, TEAL)):
        dot(d, x, y, c, 26)
    d.line((250, 1250, 1190, 1250), fill=(*WHITE, 180), width=10)
    for x, y, c in ((360, 1250, TEAL), (600, 1250, TEAL), (840, 1250, ROSE), (1080, 1250, TEAL)):
        dot(d, x, y, c, 26)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 530, AMBER); card(d, (100, 720, 1340, 1490), AMBER)
    d.rounded_rectangle((180, 850, 1260, 1220), radius=34, fill=(*CYAN, 100), outline=(*WHITE, 170), width=7)
    for x, c in ((300, TEAL), (570, AMBER), (840, VIOLET), (1110, ROSE)):
        d.rounded_rectangle((x, 940, x+120, 1120), radius=24, fill=(*c, 190), outline=(*WHITE, 140), width=5)
        dot(d, x+60, 1030, WHITE, 18)
    d.line((300, 1310, 1140, 1310), fill=(*WHITE, 170), width=10)
    for x, c in ((360, TEAL), (640, TEAL), (920, ROSE), (1120, TEAL)):
        dot(d, x, 1310, c, 25)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 530, VIOLET); card(d, (100, 720, 1340, 1490), VIOLET)
    d.rounded_rectangle((180, 860, 670, 1280), radius=30, fill=(*ROSE, 100), outline=(*WHITE, 160), width=7)
    d.rounded_rectangle((770, 860, 1260, 1280), radius=30, fill=(*CYAN, 100), outline=(*WHITE, 160), width=7)
    d.arc((240, 930, 570, 1220), 210, 510, fill=(*AMBER, 230), width=17)
    d.arc((830, 930, 1170, 1220), 210, 510, fill=(*TEAL, 230), width=17)
    d.line((250, 1370, 1190, 1370), fill=(*WHITE, 175), width=10)
    points = [(300,1370),(390,1370),(450,1280),(520,1460),(600,1370),(680,1370),(760,1300),(840,1445),(930,1370),(1030,1370),(1110,1320),(1190,1370)]
    d.line(points, fill=(*AMBER, 225), width=10, joint='curve')
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 530, TEAL); card(d, (100, 720, 1340, 1490), TEAL)
    d.line((720, 850, 720, 1000), fill=(*WHITE, 180), width=10)
    for x, c in ((320, CYAN), (720, AMBER), (1120, VIOLET)):
        d.line((720, 1000, x, 1140), fill=(*WHITE, 155), width=8); dot(d, x, 1140, c, 28)
    for y, c in ((1900, TEAL), (2070, AMBER), (2230, ROSE)):
        check(d, 230, y, c); d.line((340, y, 1170, y), fill=(*WHITE, 155), width=8)
    return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0045_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
