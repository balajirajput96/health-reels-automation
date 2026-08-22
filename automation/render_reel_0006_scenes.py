from PIL import Image, ImageDraw, ImageFilter
import math
import random
from pathlib import Path

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 15, 36)
TEAL = (57, 220, 194)
CYAN = (93, 177, 244)
AMBER = (249, 184, 77)
VIOLET = (163, 124, 239)
WHITE = (229, 241, 252)
MUTED = (135, 164, 198)


def gradient():
    im = Image.new('RGB', (W, H), BG)
    p = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * 0.52, y - H * 0.28) / (W * 0.95))
            p[x, y] = (
                min(255, int(7 + 10 * t + 8 * glow)),
                min(255, int(15 + 18 * t + 19 * glow)),
                min(255, int(36 + 37 * t + 28 * glow)),
            )
    return im


def glow_circle(base, center, radius, color, alpha=70):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    base.paste(layer, (0, 0), layer)


def network(im, cx, cy, scale=1.0, seed=0):
    rng = random.Random(seed)
    pts = []
    for i in range(22):
        a = i / 22 * math.tau + rng.uniform(-0.13, 0.13)
        r = rng.uniform(130, 370) * scale
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.64))
    d = ImageDraw.Draw(im, 'RGBA')
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i + 1:]:
            if math.hypot(x2 - x1, y2 - y1) < 320 * scale:
                d.line((x1, y1, x2, y2), fill=(*TEAL, 62), width=max(2, int(4 * scale)))
    for i, (x, y) in enumerate(pts):
        c = AMBER if i % 6 == 0 else CYAN
        r = max(8, int(15 * scale))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*c, 215))


def card(d, box, fill, outline, width=6, radius=42):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def safe_lower_third(d):
    d.rounded_rectangle((86, 1835, 1354, 2450), radius=60, fill=(4, 10, 27, 112))


def frame_card(d, box, color, accent=True):
    card(d, box, (18, 43, 74, 235), (*color, 225), 7)
    x1, y1, x2, y2 = box
    d.rounded_rectangle((x1 + 45, y1 + 55, x2 - 45, y1 + 135), radius=16, fill=(*color, 62))
    for i in range(4):
        yy = y1 + 230 + i * 68
        d.line((x1 + 58, yy, x2 - 58, yy), fill=(*WHITE, 135 if i == 0 else 74), width=8)
    if accent:
        d.ellipse((x1 + 65, y2 - 170, x1 + 145, y2 - 90), fill=(*color, 210))


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 575), 470, TEAL, 48)
    network(im, 720, 560, 0.9, 19)
    # One neutral decision at the centre and two surrounding frames.
    frame_card(d, (125, 1040, 595, 1560), TEAL)
    frame_card(d, (845, 1040, 1315, 1560), AMBER)
    d.ellipse((625, 1125, 815, 1315), fill=(*WHITE, 218), outline=(*CYAN, 245), width=10)
    d.line((595, 1300, 625, 1235), fill=(*TEAL, 220), width=12)
    d.line((845, 1235, 815, 1235), fill=(*AMBER, 220), width=12)
    d.arc((530, 960, 910, 1420), 205, 335, fill=(*CYAN, 170), width=10)
    safe_lower_third(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 630), 430, CYAN, 48)
    # Two equivalent outcomes represented as alternate framing windows.
    for box, color in [((170, 890, 625, 1480), TEAL), ((815, 890, 1270, 1480), AMBER)]:
        frame_card(d, box, color)
        x1, y1, x2, y2 = box
        for j in range(5):
            yy = y1 + 245 + j * 48
            d.ellipse((x1 + 85 + j * 38, yy, x1 + 121 + j * 38, yy + 36), fill=(*color, 190))
        d.line((x1 + 75, y1 + 500, x2 - 75, y1 + 500), fill=(*WHITE, 90), width=6)
    d.line((690, 1170, 750, 1170), fill=(*WHITE, 215), width=11)
    d.polygon([(752, 1170), (715, 1143), (715, 1197)], fill=(*WHITE, 215))
    network(im, 720, 570, .72, 21)
    safe_lower_third(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 590), 440, VIOLET, 48)
    # A third option enters and changes the measured choice pattern.
    frame_card(d, (155, 930, 555, 1510), TEAL)
    frame_card(d, (885, 930, 1285, 1510), AMBER)
    card(d, (495, 1120, 945, 1655), (33, 41, 81, 242), (*VIOLET, 230), 9, 48)
    d.ellipse((655, 1195, 785, 1325), fill=(*WHITE, 210), outline=(*VIOLET, 245), width=8)
    for i, r in enumerate([80, 132, 184]):
        d.arc((720 - r, 1380 - r, 720 + r, 1380 + r), 205, 335, fill=(*VIOLET, 220 - i * 35), width=9)
    d.line((555, 1210, 640, 1260), fill=(*TEAL, 200), width=10)
    d.line((885, 1260, 800, 1260), fill=(*AMBER, 200), width=10)
    d.line((720, 900, 720, 1110), fill=(*VIOLET, 180), width=10)
    network(im, 720, 570, .62, 23)
    safe_lower_third(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 560), 450, AMBER, 40)
    # A measurement gauge with a visible context boundary, not a personality label.
    card(d, (180, 820, 1260, 1540), (17, 38, 69, 240), (*CYAN, 210), 7)
    d.ellipse((445, 975, 995, 1525), outline=(*TEAL, 210), width=17)
    d.arc((445, 975, 995, 1525), 205, 330, fill=(*AMBER, 245), width=18)
    d.line((720, 1250, 900, 1135), fill=(*WHITE, 220), width=14)
    d.ellipse((690, 1220, 750, 1280), fill=(*WHITE, 235))
    d.line((260, 1700, 1180, 1700), fill=(*MUTED, 135), width=6)
    d.line((720, 1620, 720, 1790), fill=(*AMBER, 225), width=12)
    d.line((440, 1620, 440, 1790), fill=(*TEAL, 200), width=9)
    d.line((1000, 1620, 1000, 1790), fill=(*VIOLET, 200), width=9)
    d.line((350, 1870, 1090, 1870), fill=(*WHITE, 125), width=8)
    d.line((720, 1830, 720, 1910), fill=(*AMBER, 235), width=12)
    network(im, 720, 490, .58, 29)
    safe_lower_third(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0006_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
