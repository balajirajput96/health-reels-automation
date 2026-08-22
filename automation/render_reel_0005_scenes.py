from PIL import Image, ImageDraw, ImageFilter
import math
import random
from pathlib import Path

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (8, 17, 39)
TEAL = (52, 214, 192)
CYAN = (98, 178, 242)
AMBER = (247, 183, 79)
VIOLET = (157, 123, 234)
WHITE = (226, 240, 252)
MUTED = (137, 166, 198)


def gradient():
    im = Image.new('RGB', (W, H), BG)
    p = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * .52, y - H * .28) / (W * .95))
            p[x, y] = (min(255, int(8 + 9*t + 7*glow)), min(255, int(17 + 16*t + 18*glow)), min(255, int(39 + 35*t + 25*glow)))
    return im


def glow_circle(base, center, radius, color, alpha=80):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * .55))
    base.paste(layer, (0, 0), layer)


def network(im, cx, cy, scale=1.0, seed=0):
    rng = random.Random(seed)
    pts = []
    for i in range(20):
        a = i / 20 * math.tau + rng.uniform(-.13, .13)
        r = rng.uniform(130, 370) * scale
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * .64))
    d = ImageDraw.Draw(im, 'RGBA')
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i+1:]:
            if math.hypot(x2-x1, y2-y1) < 320 * scale:
                d.line((x1, y1, x2, y2), fill=(*TEAL, 68), width=max(2, int(4*scale)))
    for i, (x, y) in enumerate(pts):
        c = AMBER if i % 6 == 0 else CYAN
        r = max(8, int(15*scale))
        d.ellipse((x-r, y-r, x+r, y+r), fill=(*c, 215))


def card(d, box, fill, outline, width=6, radius=42):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def safe_lower_third(d):
    d.rounded_rectangle((86, 1835, 1354, 2450), radius=60, fill=(4, 11, 28, 105))


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 650), 450, TEAL, 45)
    network(im, 720, 600, 1.0, 5)
    # Three contextual windows around one neutral center
    for box, col in [((150, 1020, 540, 1540), TEAL), ((525, 960, 915, 1480), CYAN), ((900, 1020, 1290, 1540), AMBER)]:
        card(d, box, (18, 44, 74, 225), (*col, 220), 6)
    d.ellipse((650, 1130, 790, 1270), fill=(*WHITE, 205), outline=(*TEAL, 255), width=8)
    for x1, y1, x2, y2, col in [(540,1280,650,1200,TEAL),(915,1200,790,1200,CYAN),(540,1280,650,1360,AMBER),(915,1280,790,1270,TEAL)]:
        d.line((x1,y1,x2,y2), fill=(*col, 210), width=10)
    safe_lower_third(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 700), 400, CYAN, 47)
    # abstract openness / awareness / engagement rings
    for r, col, a in [(330, TEAL, 100), (250, CYAN, 150), (170, AMBER, 205)]:
        d.ellipse((720-r, 700-r, 720+r, 700+r), outline=(*col, a), width=10)
    d.ellipse((655, 635, 785, 765), fill=(*WHITE, 210), outline=(*TEAL, 255), width=7)
    d.arc((575, 1040, 865, 1330), 200, 340, fill=(*TEAL, 220), width=14)
    d.arc((530, 1090, 910, 1470), 205, 335, fill=(*CYAN, 185), width=10)
    d.arc((480, 1140, 960, 1620), 210, 330, fill=(*AMBER, 155), width=8)
    for x, col in [(380, TEAL), (720, CYAN), (1060, AMBER)]:
        d.ellipse((x-45, 1510, x+45, 1600), fill=(*col, 225))
    safe_lower_third(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 600), 460, VIOLET, 44)
    # instrument cards: different windows, no readable text
    boxes = [(120, 1040, 420, 1570), (570, 1040, 870, 1570), (1020, 1040, 1320, 1570)]
    cols = [TEAL, CYAN, AMBER]
    for idx, (box, col) in enumerate(zip(boxes, cols)):
        card(d, box, (20, 39, 70, 230), (*col, 220), 6)
        x1, y1, x2, y2 = box
        if idx == 0:
            for k in range(5):
                d.rounded_rectangle((x1+50, y1+75+k*82, x2-50, y1+130+k*82), radius=17, fill=(*col, 75), outline=(*col, 170), width=3)
            d.ellipse((x1+100, y1+400, x1+200, y1+500), outline=(*WHITE, 180), width=7)
        elif idx == 1:
            for r in [68, 115, 162]:
                d.arc((x1+150-r, y1+270-r, x1+150+r, y1+270+r), 200, 340, fill=(*col, 210), width=9)
            d.line((x1+150, y1+270, x1+222, y1+205), fill=(*WHITE, 215), width=8)
        else:
            base = y1 + 410
            d.line((x1+50, base, x2-50, base), fill=(*MUTED, 120), width=3)
            pts = [(x1+50+i, base + 48*math.sin(i/18) + 20*math.sin(i/5)) for i in range(0, 210, 7)]
            d.line(pts, fill=(*col, 235), width=8)
    d.arc((250, 370, 1190, 1120), 195, 345, fill=(*WHITE, 115), width=8)
    network(im, 720, 600, .72, 11)
    safe_lower_third(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 650), 450, AMBER, 42)
    # correlation-like association paired with an explicit separation marker
    card(d, (190, 700, 1250, 1510), (18, 39, 68, 238), (88, 170, 235, 215), 7)
    for i, col in enumerate([TEAL, CYAN, AMBER]):
        y = 870 + i*190
        card(d, (300, y, 1140, y+110), (26, 52, 82, 230), (*col, 215), 5)
        d.ellipse((360, y+24, 438, y+102), fill=(*col, 190))
        for j in range(5):
            d.line((520, y+28+j*17, 1050, y+28+j*17), fill=(*WHITE, 155 if j == 0 else 85), width=7)
    # magnifier over a line, plus non-causal divider symbol
    d.ellipse((505, 300, 900, 695), outline=(*TEAL, 215), width=17)
    d.line((830, 625, 1085, 885), fill=(*TEAL, 215), width=21)
    d.line((545, 1710, 895, 1710), fill=(*AMBER, 225), width=12)
    d.line((720, 1540, 720, 1875), fill=(*AMBER, 225), width=12)
    d.line((580, 1570, 860, 1850), fill=(*WHITE, 170), width=9)
    d.line((860, 1570, 580, 1850), fill=(*WHITE, 170), width=9)
    network(im, 720, 510, .62, 17)
    safe_lower_third(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0005_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
