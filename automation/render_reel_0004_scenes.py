from PIL import Image, ImageDraw, ImageFilter
import math
from pathlib import Path

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (9, 18, 38)
TEAL = (47, 205, 190)
CYAN = (88, 170, 235)
AMBER = (246, 179, 76)
PURPLE = (145, 112, 226)
WHITE = (226, 238, 250)
MUTED = (132, 160, 190)


def gradient():
    im = Image.new('RGB', (W, H), BG)
    p = im.load()
    for y in range(H):
        t = y / (H - 1)
        r = int(9 + 8 * t)
        g = int(18 + 14 * t)
        b = int(38 + 35 * t)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * .55, y - H * .28) / (W * .9))
            p[x, y] = (min(255, int(r + 8 * glow)), min(255, int(g + 18 * glow)), min(255, int(b + 22 * glow)))
    return im


def glow_circle(base, center, radius, color, alpha=90):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * .55))
    base.paste(layer, (0, 0), layer)


def node_network(im, cx, cy, scale=1.0, seed=0):
    import random
    rng = random.Random(seed)
    pts = []
    for i in range(18):
        a = (i / 18) * math.tau + rng.uniform(-.12, .12)
        r = rng.uniform(120, 350) * scale
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * .66))
    d = ImageDraw.Draw(im, 'RGBA')
    for i, (x1, y1) in enumerate(pts):
        for j in range(i + 1, len(pts)):
            x2, y2 = pts[j]
            if math.hypot(x2-x1, y2-y1) < 300 * scale:
                d.line((x1, y1, x2, y2), fill=(*TEAL, 75), width=max(2, int(4*scale)))
    for i, (x, y) in enumerate(pts):
        c = AMBER if i % 5 == 0 else CYAN
        r = max(8, int(16*scale))
        d.ellipse((x-r, y-r, x+r, y+r), fill=(*c, 210))


def rounded_card(d, box, fill, outline, width=5, radius=38):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 730), 420, TEAL, 52)
    node_network(im, 720, 640, 1.0, 4)
    # neutral decision cards
    rounded_card(d, (150, 1030, 610, 1580), (20, 48, 79, 230), (75, 183, 220, 220), 6)
    rounded_card(d, (830, 1030, 1290, 1580), (54, 43, 86, 230), (177, 129, 234, 220), 6)
    d.line((610, 1305, 830, 1305), fill=(*AMBER, 220), width=10)
    d.polygon([(830,1305),(790,1275),(790,1335)], fill=(*AMBER,220))
    d.ellipse((660, 1160, 780, 1280), fill=(*WHITE, 180), outline=(*TEAL, 255), width=7)
    d.arc((570, 1040, 870, 1350), 210, 330, fill=(*TEAL, 180), width=12)
    # caption-safe lower third vignette only
    d.rounded_rectangle((90, 1840, 1350, 2450), radius=55, fill=(6, 14, 31, 85))
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 750), 390, CYAN, 48)
    # reaction-time rings
    for r, a in [(320, 110), (250, 150), (180, 210)]:
        d.ellipse((720-r, 700-r, 720+r, 700+r), outline=(*CYAN, a), width=8)
    d.ellipse((650, 630, 790, 770), fill=(*AMBER, 230))
    d.ellipse((685, 665, 755, 735), fill=(*BG, 230))
    d.line((720, 700, 720, 560), fill=(*WHITE, 230), width=9)
    d.line((720, 700, 820, 760), fill=(*WHITE, 230), width=9)
    # waveform panel
    rounded_card(d, (150, 1120, 1290, 1600), (14, 38, 65, 215), (47, 205, 190, 180), 5)
    pts=[]
    for i in range(0, 1000, 10):
        x=220+i
        y=1360 + 80*math.sin(i/56) + 35*math.sin(i/11) * (0.4 + i/1200)
        pts.append((x,y))
    d.line(pts, fill=(*TEAL, 235), width=8, joint='curve')
    d.line((220,1360,1220,1360), fill=(*MUTED,90), width=3)
    d.line((720,1180,720,1540), fill=(*AMBER,120), width=4)
    node_network(im, 720, 850, .75, 7)
    d.rounded_rectangle((90, 1840, 1350, 2450), radius=55, fill=(6, 14, 31, 85))
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (710, 630), 470, PURPLE, 46)
    # three non-text instrument panels
    boxes=[(120, 1020, 420, 1530), (570, 1020, 870, 1530), (1020, 1020, 1320, 1530)]
    colors=[TEAL, CYAN, AMBER]
    for idx, (box,c) in enumerate(zip(boxes,colors)):
        rounded_card(d, box, (20, 37, 69, 225), (*c, 215), 6)
        x1,y1,x2,y2=box
        if idx==0:
            for k in range(4):
                d.rounded_rectangle((x1+55, y1+85+k*85, x2-55, y1+140+k*85), radius=18, fill=(*c, 80), outline=(*c, 180), width=3)
            d.ellipse((x1+105,y1+345,x1+195,y1+435), outline=(*WHITE,170), width=6)
        elif idx==1:
            for r in [70,115,160]:
                d.arc((x1+150-r,y1+260-r,x1+150+r,y1+260+r), 200, 340, fill=(*c, 210), width=8)
            d.line((x1+150,y1+260,x1+225,y1+190), fill=(*WHITE, 210), width=8)
        else:
            d.line((x1+55,y1+390,x2-55,y1+390), fill=(*MUTED,120), width=3)
            pts=[]
            for i in range(0,210,8):
                pts.append((x1+55+i, y1+390 + 50*math.sin(i/18) + 20*math.sin(i/4)))
            d.line(pts, fill=(*c, 235), width=7)
    # connecting context arc
    d.arc((260, 410, 1180, 1160), 195, 345, fill=(*WHITE, 110), width=8)
    node_network(im, 720, 610, .75, 10)
    d.rounded_rectangle((90, 1840, 1350, 2450), radius=55, fill=(6, 14, 31, 85))
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 700), 440, AMBER, 42)
    # layered research notebook / separation of questions
    rounded_card(d, (220, 720, 1220, 1660), (18, 38, 67, 235), (88, 170, 235, 210), 7)
    for i, c in enumerate([TEAL, AMBER, PURPLE]):
        y=880+i*220
        rounded_card(d, (330, y, 1110, y+130), (27, 51, 80, 230), (*c, 210), 5)
        d.ellipse((390, y+35, 470, y+115), fill=(*c, 190))
        for j in range(4):
            d.line((540, y+42+j*22, 1010, y+42+j*22), fill=(*WHITE, 95 if j else 180), width=8)
    # magnifying glass and network
    d.ellipse((510, 300, 930, 720), outline=(*TEAL, 210), width=18)
    d.line((855, 645, 1110, 900), fill=(*TEAL, 210), width=22)
    node_network(im, 720, 500, .65, 13)
    d.rounded_rectangle((90, 1840, 1350, 2450), radius=55, fill=(6, 14, 31, 85))
    return im

for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0004_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
