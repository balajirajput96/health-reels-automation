from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 14, 35); WHITE = (235, 244, 252); TEAL = (61, 220, 194)
CYAN = (93, 177, 244); AMBER = (249, 184, 77); VIOLET = (163, 124, 239); RED = (241, 105, 119)

def base():
    im = Image.new('RGB', (W, H), BG); px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            g = max(0, 1 - math.hypot(x - W*.50, y - H*.26) / (W*.96))
            px[x, y] = (min(255, int(7 + 10*t + 8*g)), min(255, int(14 + 18*t + 18*g)), min(255, int(35 + 38*t + 28*g)))
    return im

def glow(im, x, y, r, c, a=64):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*c, a))
    layer = layer.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(layer, (0, 0), layer)

def card(d, box, color):
    d.rounded_rectangle(box, radius=42, fill=(16, 38, 69, 242), outline=(*color, 225), width=7)

def footer(d):
    d.rounded_rectangle((82, 1840, 1358, 2460), radius=60, fill=(3, 9, 25, 145))

def spark(d, x, y, color, r=24):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, 230))
    d.line((x-r*2.5, y, x+r*2.5, y), fill=(*color, 150), width=7)
    d.line((x, y-r*2.5, x, y+r*2.5), fill=(*color, 150), width=7)

def s1():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, TEAL)
    card(d, (100, 760, 1340, 1320), VIOLET)
    # Three repeated daily contexts around a central sampling prompt.
    for x, y, c in [(270, 920, CYAN), (720, 870, TEAL), (1170, 920, AMBER)]:
        d.ellipse((x-78, y-78, x+78, y+78), outline=(*WHITE, 210), width=13)
        d.line((x, y+78, x, y+230), fill=(*WHITE, 200), width=18)
        d.line((x-78, y+230, x+78, y+230), fill=(*WHITE, 180), width=12)
        d.rounded_rectangle((x-95, y+310, x+95, y+425), radius=22, fill=(*c, 210))
        for i in range(3): spark(d, x-50+i*50, y+500, c, 14)
    d.line((350, 1040, 610, 1040), fill=(*TEAL, 190), width=11)
    d.line((830, 1040, 1090, 1040), fill=(*TEAL, 190), width=11)
    footer(d); return im

def s2():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, CYAN)
    card(d, (105, 760, 1335, 1325), TEAL)
    # Emotion rating trajectories are deliberately distinct rather than a personal score.
    axes = (240, 1180, 1200, 840)
    d.line((axes[0], axes[1], axes[2], axes[1]), fill=(*WHITE, 180), width=10)
    d.line((axes[0], axes[1], axes[0], axes[3]), fill=(*WHITE, 180), width=10)
    series = [(CYAN, [1120, 1030, 1090, 930, 970, 850]), (AMBER, [1080, 1110, 980, 1010, 880, 920]), (VIOLET, [1140, 990, 920, 950, 860, 870])]
    for color, ys in series:
        pts = [(300 + i*160, y) for i, y in enumerate(ys)]
        d.line(pts, fill=(*color, 220), width=18, joint='curve')
        for x, y in pts: d.ellipse((x-20, y-20, x+20, y+20), fill=(*color, 235))
    d.ellipse((615, 340, 825, 550), fill=(*TEAL, 180), outline=(*WHITE, 200), width=10)
    for r in [130, 190, 250]: d.arc((720-r, 445-r, 720+r, 445+r), 200, 340, fill=(*TEAL, 150), width=8)
    footer(d); return im

def s3():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, AMBER)
    # Four separate channels: vignette, rating card, body signal, and context notes.
    boxes = [((95, 760, 405, 1200), CYAN), ((520, 760, 830, 1200), VIOLET), ((945, 760, 1345, 1200), AMBER), ((270, 1350, 1170, 1730), TEAL)]
    for box, c in boxes: card(d, box, c)
    d.rounded_rectangle((165, 900, 335, 1010), radius=20, fill=(*CYAN, 210))
    for y in [920, 1000, 1080]: d.line((585, y, 765, y), fill=(*WHITE, 190), width=12)
    d.line((1030, 1030, 1260, 1030), fill=(*AMBER, 220), width=10)
    for x, y in [(1040, 1000), (1090, 1060), (1150, 990), (1210, 1080), (1270, 1020)]: d.ellipse((x-15, y-15, x+15, y+15), fill=(*AMBER, 220))
    d.ellipse((520, 1460, 620, 1560), fill=(*WHITE, 210)); d.line((570, 1560, 570, 1660), fill=(*WHITE, 190), width=14)
    for i in range(6):
        x = 700 + i*65; y = 1560 + int(70*math.sin(i*1.4))
        if i: d.line((x-65, prev_y, x, y), fill=(*TEAL, 220), width=12)
        d.ellipse((x-12, y-12, x+12, y+12), fill=(*TEAL, 230)); prev_y = y
    for x in [820, 940, 1060]: d.rounded_rectangle((x, 1450, x+80, 1570), radius=15, fill=(*WHITE, 190))
    footer(d); return im

def s4():
    im = base(); d = ImageDraw.Draw(im, 'RGBA'); glow(im, 720, 430, 520, RED)
    card(d, (100, 760, 1340, 1330), RED)
    # Guardrails represented as separate checkpoints, not a prescriptive checklist.
    checkpoints = [(260, 930, CYAN), (540, 930, VIOLET), (820, 930, AMBER), (1100, 930, TEAL)]
    for x, y, c in checkpoints:
        d.ellipse((x-62, y-62, x+62, y+62), fill=(*c, 210), outline=(*WHITE, 220), width=8)
        d.line((x-30, y, x-5, y+27), fill=(*BG, 230), width=13)
        d.line((x-5, y+27, x+38, y-32), fill=(*BG, 230), width=13)
    d.line((320, 930, 480, 930), fill=(*WHITE, 170), width=9); d.line((600, 930, 760, 930), fill=(*WHITE, 170), width=9); d.line((880, 930, 1040, 930), fill=(*WHITE, 170), width=9)
    card(d, (235, 1430, 1205, 1710), TEAL)
    for i in range(4):
        x = 420 + i*190
        d.rounded_rectangle((x, 1500, x+115, 1600), radius=18, fill=(*WHITE, 190))
        d.line((x+22, 1640, x+95, 1640), fill=(*WHITE, 170), width=10)
    footer(d); return im

for i, fn in enumerate((s1, s2, s3, s4), 1):
    path = OUT / f'reel_0033_scene_{i:02d}.png'
    fn().save(path, optimize=True)
    print(path)
