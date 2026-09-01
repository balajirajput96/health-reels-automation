from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 15, 36)
TEAL = (57, 220, 194)
CYAN = (93, 177, 244)
AMBER = (249, 184, 77)
VIOLET = (163, 124, 239)
WHITE = (229, 241, 252)
RED = (241, 105, 119)


def gradient() -> Image.Image:
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - W * 0.52, y - H * 0.28) / (W * 0.95))
            px[x, y] = (min(255, int(7 + 10 * t + 8 * glow)), min(255, int(15 + 18 * t + 19 * glow)), min(255, int(36 + 37 * t + 28 * glow)))
    return im


def glow_circle(base: Image.Image, center, radius, color, alpha=70):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    base.paste(layer, (0, 0), layer)


def card(d, box, fill, outline, width=7, radius=42):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, x1, y1, x2, y2, color=WHITE, width=11):
    d.line((x1, y1, x2, y2), fill=(*color, 220), width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 34
    left = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    right = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    d.polygon([(x2, y2), left, right], fill=(*color, 220))


def lower_panel(d):
    d.rounded_rectangle((82, 1830, 1358, 2460), radius=60, fill=(4, 10, 27, 140))


def wave(d, x0, y0, width, cycles, amp, color):
    pts = []
    for i in range(180):
        t = i / 179
        pts.append((x0 + width * t, y0 + amp * math.sin(t * math.tau * cycles) + 22 * math.sin(t * math.tau * cycles * 3.1)))
    d.line(pts, fill=(*color, 225), width=10)


def network_nodes(d, centers, links, colors):
    for a, b in links:
        d.line((*centers[a], *centers[b]), fill=(*WHITE, 120), width=7)
    for i, (x, y) in enumerate(centers):
        d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=(*colors[i % len(colors)], 230), outline=(*WHITE, 170), width=5)


def scene_01():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 420), 520, TEAL, 42)
    card(d, (130, 780, 1310, 1390), (17, 38, 69, 242), (*TEAL, 220), 7, 42)
    centers = [(300, 960), (530, 880), (790, 970), (1080, 850), (430, 1190), (720, 1190), (1010, 1160)]
    links = [(0,1),(1,2),(2,3),(0,4),(1,5),(2,5),(2,6),(3,6),(4,5),(5,6)]
    network_nodes(d, centers, links, [TEAL, CYAN, AMBER, VIOLET])
    arrow(d, 720, 1400, 720, 1530, WHITE, 12)
    card(d, (260, 1570, 1180, 1770), (17, 38, 69, 242), (*CYAN, 220), 7, 36)
    for i in range(5):
        d.line((380, 1630 + i * 25, 1060 - i * 55, 1630 + i * 25), fill=(*WHITE, 150), width=8)
    lower_panel(d)
    return im


def scene_02():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 420), 480, CYAN, 42)
    card(d, (100, 800, 650, 1330), (17, 38, 69, 242), (*AMBER, 220), 7, 40)
    card(d, (790, 800, 1340, 1330), (17, 38, 69, 242), (*CYAN, 220), 7, 40)
    # Structural tract panel.
    for i in range(5):
        pts = []
        for j in range(40):
            t = j / 39
            x = 190 + t * 380
            y = 930 + i * 62 + 42 * math.sin(t * math.tau * 1.3 + i)
            pts.append((x, y))
        d.line(pts, fill=(*AMBER, 210), width=12)
    # Functional time-series panel.
    wave(d, 850, 980, 390, 3, 55, CYAN)
    wave(d, 850, 1110, 390, 3, 55, VIOLET)
    d.line((850, 1240, 1240, 1240), fill=(*WHITE, 130), width=7)
    arrow(d, 720, 1370, 720, 1510, WHITE, 12)
    card(d, (230, 1550, 1210, 1770), (17, 38, 69, 242), (*RED, 220), 7, 36)
    d.line((430, 1660, 1010, 1660), fill=(*RED, 220), width=14)
    d.line((720, 1600, 720, 1720), fill=(*RED, 220), width=10)
    lower_panel(d)
    return im


def scene_03():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 420), 500, AMBER, 42)
    card(d, (120, 800, 540, 1240), (17, 38, 69, 242), (*AMBER, 220), 7, 36)
    card(d, (570, 800, 970, 1240), (17, 38, 69, 242), (*TEAL, 220), 7, 36)
    card(d, (1000, 800, 1320, 1240), (17, 38, 69, 242), (*VIOLET, 220), 7, 36)
    # BOLD, EEG and graph/matrix symbols.
    wave(d, 180, 1010, 300, 2, 58, AMBER)
    for i in range(4):
        d.line((660, 930 + i * 70, 880, 930 + i * 70), fill=(*TEAL, 175), width=8)
    d.ellipse((690, 960, 735, 1005), fill=(*WHITE, 210))
    for i in range(4):
        d.line((1060, 930 + i * 70, 1270, 930 + i * 70), fill=(*VIOLET, 180), width=8)
        d.line((1060 + i * 50, 930, 1060 + i * 50, 1140), fill=(*VIOLET, 140), width=7)
    arrow(d, 720, 1260, 720, 1420, WHITE, 12)
    card(d, (190, 1460, 1250, 1770), (17, 38, 69, 242), (*CYAN, 220), 7, 36)
    centers = [(360, 1610), (540, 1540), (720, 1660), (900, 1540), (1080, 1610)]
    links = [(0,1),(1,2),(2,3),(3,4),(0,2),(2,4)]
    network_nodes(d, centers, links, [CYAN, TEAL, AMBER])
    lower_panel(d)
    return im


def scene_04():
    im = gradient(); d = ImageDraw.Draw(im, 'RGBA')
    glow_circle(im, (720, 420), 470, VIOLET, 42)
    cards = [(110, 820, 580, 1190), (860, 820, 1330, 1190), (110, 1320, 580, 1690), (860, 1320, 1330, 1690)]
    colors = [TEAL, CYAN, AMBER, VIOLET]
    for box, color in zip(cards, colors):
        card(d, box, (17, 38, 69, 242), (*color, 220), 7, 36)
    # Four analysis-choice cards.
    for i in range(4):
        d.line((180, 930 + i * 52, 500, 930 + i * 52), fill=(*WHITE, 160), width=10)
    for i in range(4):
        d.ellipse((930 + i * 72, 955, 970 + i * 72, 995), fill=(*CYAN, 200))
    d.line((910, 1090, 1260, 1090), fill=(*WHITE, 150), width=9)
    for i, h in enumerate([95, 150, 120, 190]):
        x = 190 + i * 80
        d.rounded_rectangle((x, 1610 - h, x + 45, 1610), radius=10, fill=(*AMBER, 200))
    wave(d, 930, 1510, 280, 4, 60, VIOLET)
    arrow(d, 720, 1740, 720, 1890, WHITE, 10)
    d.line((440, 2040, 1000, 2040), fill=(*RED, 220), width=18)
    d.line((440, 1990, 440, 2090), fill=(*RED, 220), width=12)
    d.line((1000, 1990, 1000, 2090), fill=(*RED, 220), width=12)
    lower_panel(d)
    return im


for idx, maker in enumerate([scene_01, scene_02, scene_03, scene_04], 1):
    path = OUT / f'reel_0017_scene_{idx:02d}.png'
    maker().save(path, optimize=True)
    print(path)
