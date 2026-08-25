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
    card(d, (110, 760, 1330, 1370), VIOLET)
    # Mood is a state and memory has stages; the visual keeps them distinct.
    centers = [(300, 1020, CYAN), (720, 1020, TEAL), (1140, 1020, AMBER)]
    for i, (x, y, c) in enumerate(centers):
        d.ellipse((x-92, y-92, x+92, y+92), outline=(*c, 230), width=15)
        d.ellipse((x-28, y-28, x+28, y+28), fill=(*c, 220))
        for r in [125, 170]: d.arc((x-r, y-r, x+r, y+r), 205, 335, fill=(*c, 150), width=8)
        if i < 2: d.line((x+100, y, centers[i+1][0]-100, y), fill=(*WHITE, 180), width=12)
    d.line((300, 1250, 300, 1320), fill=(*WHITE, 170), width=9)
    d.line((720, 1250, 720, 1320), fill=(*WHITE, 170), width=9)
    d.line((1140, 1250, 1140, 1320), fill=(*WHITE, 170), width=9)
    footer(d); return im


def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, CYAN)
    # Emotional items enter a memory task, then split into recognition and recall.
    card(d, (95, 720, 515, 1450), CYAN); card(d, (600, 720, 1345, 1450), TEAL)
    for i, c in enumerate([RED, AMBER, VIOLET, TEAL]):
        x = 190 + (i % 2) * 185; y = 900 + (i // 2) * 220
        d.rounded_rectangle((x-62, y-62, x+62, y+62), radius=22, fill=(*c, 210), outline=(*WHITE, 170), width=6)
        dot(d, x, y, WHITE, 16)
    d.line((515, 1080, 600, 1080), fill=(*WHITE, 190), width=12)
    d.line((720, 890, 720, 1010), fill=(*WHITE, 190), width=12)
    d.line((720, 1150, 720, 1270), fill=(*WHITE, 190), width=12)
    d.rounded_rectangle((655, 805, 785, 900), radius=18, fill=(*VIOLET, 210))
    # Recognition panel: seen/not seen choice.
    d.rounded_rectangle((675, 1010, 875, 1150), radius=24, fill=(*CYAN, 210))
    for x in [710, 790, 870]: dot(d, x, 1090, WHITE, 14)
    # Free recall panel: open retrieval lines.
    d.rounded_rectangle((675, 1270, 875, 1400), radius=24, fill=(*AMBER, 210))
    for y in [1305, 1340, 1375]: d.line((710, y, 840, y), fill=(*WHITE, 190), width=9)
    footer(d); return im


def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER)
    card(d, (105, 720, 1335, 1490), AMBER)
    # Four outcomes: accuracy, autobiographical retrieval, false lure, and delayed memory.
    boxes = [(180, 835, 430, 1110, CYAN), (500, 835, 750, 1110, TEAL), (820, 835, 1070, 1110, RED), (1140, 835, 1290, 1110, VIOLET)]
    for x1, y1, x2, y2, c in boxes: card(d, (x1, y1, x2, y2), c)
    d.line((225, 1040, 385, 900), fill=(*WHITE, 190), width=10); d.line((385, 900, 385, 1030), fill=(*WHITE, 190), width=10)
    d.ellipse((570, 900, 680, 1010), outline=(*WHITE, 200), width=9); d.line((625, 1010, 625, 1060), fill=(*WHITE, 190), width=9)
    d.rounded_rectangle((875, 900, 1015, 1030), radius=24, fill=(*RED, 160), outline=(*WHITE, 200), width=8)
    d.line((900, 925, 990, 1005), fill=(*WHITE, 210), width=10); d.line((990, 925, 900, 1005), fill=(*WHITE, 210), width=10)
    for r in [38, 75, 112]: d.arc((1215-r, 965-r, 1215+r, 965+r), 195, 345, fill=(*WHITE, 180), width=8)
    # Different colored bars underneath emphasize that outcomes need not agree.
    for i, (c, h) in enumerate([(CYAN, 180), (TEAL, 125), (RED, 85), (VIOLET, 155)]):
        x = 240 + i * 250
        d.rounded_rectangle((x, 1220, x+125, 1220+h), radius=18, fill=(*c, 205))
    footer(d); return im


def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, RED)
    card(d, (100, 720, 1340, 1430), RED)
    # Guardrails: mood timing, task, delay, outcome, and sample.
    checkpoints = [(230, 930, CYAN), (475, 930, VIOLET), (720, 930, AMBER), (965, 930, TEAL), (1210, 930, WHITE)]
    for x, y, c in checkpoints: check(d, x, y, c)
    for a, b in zip(checkpoints, checkpoints[1:]):
        d.line((a[0]+64, a[1], b[0]-64, b[1]), fill=(*WHITE, 165), width=9)
    card(d, (220, 1160, 1220, 1360), TEAL)
    d.line((350, 1260, 1090, 1260), fill=(*WHITE, 175), width=11)
    for x in [430, 620, 810, 1000]: dot(d, x, 1260, TEAL, 22)
    footer(d); return im


for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0035_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
