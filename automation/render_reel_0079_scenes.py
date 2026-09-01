from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 1440, 2560
BG = (7, 14, 31)
INK = (234, 242, 255)
MUTED = (160, 178, 205)
CYAN = (67, 224, 255)
VIOLET = (157, 116, 255)
AMBER = (255, 190, 91)
TEAL = (60, 220, 183)
RED = (255, 105, 125)
FONT_REG = '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf'


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def gradient():
    im = Image.new('RGB', (W, H), BG)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = int(9 * max(0.0, 1 - (((x - 720) / 800) ** 2 + ((y - 760) / 1250) ** 2)))
            px[x, y] = (int(7 + 9 * t), int(14 + 10 * t + glow // 3), int(31 + 25 * t + glow))
    return im


def glow(im, xy, radius, color):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, 100))
    blurred = layer.filter(ImageFilter.GaussianBlur(radius // 2))
    im.paste(blurred, (0, 0), blurred)


def label(d, text, y, color=CYAN):
    d.text((100, y), text, font=font(42, True), fill=color)


def title(d, text, y=180):
    d.text((100, y), text, font=font(74, True), fill=INK)


def card(d, box, fill=(19, 31, 59), outline=(71, 98, 141), width=5, radius=34):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(d, xy, text, size, fill=INK, bold=False):
    box = d.textbbox((0, 0), text, font=font(size, bold))
    d.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=font(size, bold), fill=fill)


def note(d, text, xy, fill=MUTED, size=34):
    d.text(xy, text, font=font(size), fill=fill)


def scene1():
    im = gradient(); glow(im, (720, 650), 520, VIOLET); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'RECOVERY MAP', 90, CYAN); title(d, 'रिकवरी = एक स्कोर नहीं', 180)
    card(d, (120, 520, 1320, 950), fill=(27, 39, 75), outline=VIOLET)
    centered(d, (720, 665), 'RECOVERY?', 78, fill=INK, bold=True)
    centered(d, (720, 810), 'किस measure की बात है?', 44, fill=MUTED)
    d.line((720, 950, 720, 1110), fill=(*INK, 170), width=8)
    nodes = [(300, 1430, CYAN, 'AFFECT', 'reported feeling'), (720, 1430, VIOLET, 'PHYSIOLOGY', 'body signal'), (1140, 1430, AMBER, 'FUNCTION', 'task / outcome')]
    for x, y, c, en, sub in nodes:
        d.line((720, 1110, x, y - 140), fill=(*c, 170), width=7)
        d.ellipse((x - 145, y - 145, x + 145, y + 145), fill=(*c, 225), outline=(*INK, 220), width=7)
        centered(d, (x, y - 28), en, 34, fill=BG, bold=True)
        centered(d, (x, y + 52), sub, 28, fill=BG)
    card(d, (120, 1990, 1320, 2300), fill=(22, 55, 61), outline=TEAL)
    centered(d, (720, 2145), 'पहले पूछिए: क्या मापा गया?', 46, fill=TEAL, bold=True)
    note(d, 'measure बदलते ही conclusion भी बदल सकता है', (140, 2390), fill=AMBER, size=34)
    return im


def scene2():
    im = gradient(); glow(im, (350, 760), 430, CYAN); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'TIME WINDOW', 90, CYAN); title(d, 'समय के बिना recovery?', 180)
    card(d, (100, 570, 1340, 1210), fill=(18, 42, 69), outline=CYAN)
    centered(d, (720, 700), 'TIMELINE', 58, fill=CYAN, bold=True)
    d.line((220, 940, 1220, 940), fill=(*INK, 210), width=10)
    points = [(260, 'BASELINE', CYAN), (600, 'STRESS', RED), (940, 'POST-STRESS', AMBER), (1190, 'LATER', TEAL)]
    for x, txt, c in points:
        d.ellipse((x - 25, 915, x + 25, 965), fill=c)
        centered(d, (x, 1040), txt, 30, fill=c, bold=True)
    note(d, 'कौन-सा अंतर निकाला गया?', (190, 1140), fill=INK, size=38)
    cards = [(100, 1410, 650, 1930, VIOLET, 'AFFECT', 'समय के साथ बदलाव'), (790, 1410, 1340, 1930, AMBER, 'HR / HRV', 'शारीरिक signal')]
    for x0, y0, x1, y1, c, head, sub in cards:
        card(d, (x0, y0, x1, y1), fill=(29, 38, 69), outline=c)
        centered(d, ((x0 + x1) // 2, y0 + 115), head, 46, fill=c, bold=True)
        centered(d, ((x0 + x1) // 2, y0 + 255), sub, 36, fill=INK)
        d.line((x0 + 70, y0 + 390, x1 - 70, y0 + 390), fill=(*c, 150), width=5)
        pts = [(x0 + 75, y0 + 425), (x0 + 180, y0 + 390), (x0 + 280, y0 + 450), (x0 + 390, y0 + 345), (x1 - 75, y0 + 405)]
        d.line(pts, fill=c, width=10, joint='curve')
    card(d, (120, 2130, 1320, 2350), fill=(42, 37, 66), outline=RED)
    centered(d, (720, 2240), 'एक time-point ≠ पूरी trajectory', 42, fill=RED, bold=True)
    return im


def scene3():
    im = gradient(); glow(im, (1070, 720), 460, AMBER); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'SELF-REPORT + SIGNAL', 90, AMBER); title(d, 'अनुभव और body signal', 180)
    card(d, (100, 560, 650, 1710), fill=(22, 51, 75), outline=CYAN)
    centered(d, (375, 720), 'SELF-REPORT', 48, fill=CYAN, bold=True)
    centered(d, (375, 865), '“अभी कैसा लगा?”', 42, fill=INK)
    for i, txt in enumerate(['affect', 'stress', 'perceived effort']):
        y = 1100 + i * 160
        d.rounded_rectangle((170, y, 580, y + 100), radius=22, fill=(31, 74, 100), outline=(*CYAN, 160), width=4)
        centered(d, (375, y + 50), txt, 34, fill=INK)
    card(d, (790, 560, 1340, 1710), fill=(53, 42, 60), outline=AMBER)
    centered(d, (1065, 720), 'BODY SIGNAL', 48, fill=AMBER, bold=True)
    centered(d, (1065, 865), 'recorded under conditions', 34, fill=INK)
    for i, txt in enumerate(['heart rate', 'HRV', 'skin conductance']):
        y = 1100 + i * 160
        d.rounded_rectangle((855, y, 1275, y + 100), radius=22, fill=(88, 60, 58), outline=(*AMBER, 160), width=4)
        centered(d, (1065, y + 50), txt, 31, fill=INK)
    d.line((650, 1200, 790, 1200), fill=(*TEAL, 230), width=8)
    centered(d, (720, 1130), 'different layers', 30, fill=TEAL, bold=True)
    card(d, (130, 1920, 1310, 2310), fill=(63, 36, 61), outline=RED)
    centered(d, (720, 2045), 'biomarker ≠ mind-reading', 48, fill=RED, bold=True)
    centered(d, (720, 2170), 'self-report भी पूरा विकल्प नहीं', 38, fill=INK)
    return im


def scene4():
    im = gradient(); glow(im, (720, 820), 470, TEAL); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'DAILY LIFE SAMPLING', 90, TEAL); title(d, 'context लिखना ज़रूरी है', 180)
    card(d, (120, 550, 1320, 1180), fill=(19, 31, 59), outline=VIOLET)
    centered(d, (720, 700), 'PHONE PROMPTS', 54, fill=VIOLET, bold=True)
    hours = ['09:00', '12:30', '16:00', '20:30']
    for i, h in enumerate(hours):
        x = 245 + i * 305
        d.line((x, 890, x, 1010), fill=(*TEAL, 220), width=8)
        d.ellipse((x - 25, 855, x + 25, 905), fill=TEAL)
        centered(d, (x, 1080), h, 30, fill=INK, bold=True)
    card(d, (120, 1330, 650, 2050), fill=(24, 63, 62), outline=TEAL)
    centered(d, (385, 1470), 'CAPTURE', 46, fill=TEAL, bold=True)
    centered(d, (385, 1620), 'mood', 42, fill=INK)
    centered(d, (385, 1740), 'behavior', 42, fill=INK)
    centered(d, (385, 1860), 'context', 42, fill=INK)
    card(d, (790, 1330, 1320, 2050), fill=(63, 36, 61), outline=RED)
    centered(d, (1055, 1470), 'DO NOT JUMP', 42, fill=RED, bold=True)
    centered(d, (1055, 1620), 'one reading', 40, fill=INK)
    centered(d, (1055, 1740), '→ diagnosis', 40, fill=INK)
    centered(d, (1055, 1860), '→ guarantee', 40, fill=INK)
    card(d, (120, 2180, 1320, 2370), fill=(28, 42, 77), outline=CYAN)
    centered(d, (720, 2275), 'माप + समय + संदर्भ = सावधान निष्कर्ष', 38, fill=CYAN, bold=True)
    return im


def main():
    scenes = [scene1(), scene2(), scene3(), scene4()]
    for i, im in enumerate(scenes, 1):
        out = OUT / f'reel_0079_scene_{i:02d}.png'
        im.convert('RGB').save(out, format='PNG', optimize=False, compress_level=6)
        print(out)


if __name__ == '__main__':
    main()
