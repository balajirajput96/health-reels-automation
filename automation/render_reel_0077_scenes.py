from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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
        r = int(7 + 9 * t)
        g = int(14 + 10 * t)
        b = int(31 + 25 * t)
        for x in range(W):
            glow = int(8 * max(0.0, 1 - (((x - 720) / 800) ** 2 + ((y - 760) / 1250) ** 2)))
            px[x, y] = (r, g + glow // 3, b + glow)
    return im


def glow(im, xy, radius, color):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*color, 100))
    im.paste(layer.filter(ImageFilter.GaussianBlur(radius // 2)), (0, 0), layer.filter(ImageFilter.GaussianBlur(radius // 2)))


def label(d, text, y, color=CYAN):
    d.text((100, y), text, font=font(44, True), fill=color)


def title(d, text, y=180):
    d.text((100, y), text, font=font(78, True), fill=INK)


def card(d, box, fill=(19, 31, 59), outline=(71, 98, 141), width=5, radius=34):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(d, xy, text, size, fill=INK, bold=False):
    box = d.textbbox((0, 0), text, font=font(size, bold))
    d.text((xy[0] - (box[2]-box[0])/2, xy[1] - (box[3]-box[1])/2), text, font=font(size, bold), fill=fill)


def small_note(d, text, xy, fill=MUTED):
    d.text(xy, text, font=font(34), fill=fill)


def scene1():
    im = gradient(); glow(im, (730, 520), 500, VIOLET); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'MEASUREMENT MAP', 90, CYAN); title(d, '“STRESS” किस layer का?', 180)
    card(d, (100, 570, 1340, 950), fill=(28, 42, 77), outline=VIOLET)
    centered(d, (720, 760), 'STRESS', 92, fill=INK, bold=True)
    d.line((720, 950, 720, 1130), fill=(*INK, 170), width=8)
    nodes = [(300, 1400, CYAN, 'EXPOSURE', 'क्या हुआ?'), (720, 1400, VIOLET, 'APPRAISAL', 'कैसा लगा?'), (1140, 1400, AMBER, 'PHYSIOLOGY', 'शरीर का signal'), (720, 2050, TEAL, 'OUTCOME', 'क्या बदला?')]
    for x, y, c, en, hi in nodes:
        d.line((720, 1130, x, y-140), fill=(*c, 170), width=7)
        d.ellipse((x-145, y-145, x+145, y+145), fill=(*c, 220), outline=(*INK, 220), width=7)
        centered(d, (x, y-25), en, 37, fill=BG, bold=True)
        centered(d, (x, y+58), hi, 31, fill=BG)
    small_note(d, 'एक score = पूरी कहानी नहीं', (100, 2370), fill=AMBER)
    return im


def scene2():
    im = gradient(); glow(im, (390, 760), 430, CYAN); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'PERCEIVED STRESS', 90, CYAN); title(d, 'Perception ≠ event count', 180)
    card(d, (100, 540, 650, 1560), fill=(18, 42, 69), outline=CYAN)
    centered(d, (375, 690), 'PSS', 100, fill=CYAN, bold=True)
    centered(d, (375, 850), 'हाल की ज़िंदगी', 48, fill=INK, bold=True)
    prompts = ['अनिश्चित?', 'कंट्रोल से बाहर?', 'कितनी stressful?']
    for i, text in enumerate(prompts):
        y = 1060 + i*155
        d.rounded_rectangle((180, y, 570, y+96), radius=24, fill=(25, 66, 96), outline=(*CYAN, 150), width=4)
        centered(d, (375, y+48), text, 35, fill=INK)
    card(d, (790, 540, 1340, 1560), fill=(46, 35, 55), outline=AMBER)
    centered(d, (1065, 690), 'EVENTS', 74, fill=AMBER, bold=True)
    centered(d, (1065, 850), 'timeline', 46, fill=INK)
    x0, y0, x1 = 910, 1160, 1220
    d.line((x0, y0, x1, y0), fill=(*AMBER, 230), width=12)
    for i, x in enumerate([930, 1015, 1100, 1185]):
        d.ellipse((x-22, y0-22, x+22, y0+22), fill=AMBER)
        d.line((x, y0+30, x, y0+140), fill=(*AMBER, 190), width=5)
        centered(d, (x, y0+190), str(i+1), 35, fill=INK, bold=True)
    small_note(d, 'Questionnaire perception पूछता है; घटना अलग measure है।', (100, 1790), fill=INK)
    card(d, (100, 2010, 1340, 2260), fill=(22, 55, 61), outline=TEAL)
    centered(d, (720, 2135), 'SAMPLE + TIME WINDOW matter', 47, fill=TEAL, bold=True)
    return im


def scene3():
    im = gradient(); glow(im, (1040, 800), 470, AMBER); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'COGNITIVE APPRAISAL', 90, AMBER); title(d, 'Anticipated situation', 180)
    card(d, (240, 570, 1200, 1020), fill=(42, 37, 66), outline=AMBER)
    centered(d, (720, 760), 'UPCOMING SITUATION', 55, fill=INK, bold=True)
    centered(d, (720, 900), 'अभी होने वाली घटना', 48, fill=MUTED)
    d.line((720, 1020, 720, 1220), fill=(*INK, 190), width=8)
    d.line((720, 1220, 430, 1450), fill=(*RED, 210), width=8)
    d.line((720, 1220, 1010, 1450), fill=(*TEAL, 210), width=8)
    card(d, (150, 1470, 710, 1860), fill=(63, 36, 61), outline=RED)
    centered(d, (430, 1600), 'THREAT', 62, fill=RED, bold=True)
    centered(d, (430, 1740), 'खतरे जैसा appraisal', 39, fill=INK)
    card(d, (730, 1470, 1290, 1860), fill=(24, 63, 62), outline=TEAL)
    centered(d, (1010, 1600), 'CHALLENGE', 55, fill=TEAL, bold=True)
    centered(d, (1010, 1740), 'challenge जैसा appraisal', 35, fill=INK)
    card(d, (150, 2030, 1290, 2290), fill=(28, 42, 77), outline=VIOLET)
    centered(d, (720, 2160), 'Instrument • language • sample', 50, fill=VIOLET, bold=True)
    return im


def scene4():
    im = gradient(); glow(im, (700, 770), 430, TEAL); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'INTERPRETATION GUARDRAIL', 90, TEAL); title(d, 'Association ≠ diagnosis', 180)
    card(d, (120, 560, 640, 1330), fill=(25, 54, 71), outline=CYAN)
    centered(d, (380, 700), 'SELF-REPORT', 52, fill=CYAN, bold=True)
    d.line((180, 1030, 580, 1030), fill=(*CYAN, 170), width=5)
    pts = [(190,1000),(250,930),(310,970),(370,850),(430,900),(490,780),(550,820)]
    d.line(pts, fill=CYAN, width=10, joint='curve')
    card(d, (800, 560, 1320, 1330), fill=(47, 42, 57), outline=AMBER)
    centered(d, (1060, 700), 'HRV / BODY', 52, fill=AMBER, bold=True)
    d.line((860, 1030, 1260, 1030), fill=(*AMBER, 170), width=5)
    pts = [(870,970),(930,1010),(990,900),(1050,950),(1110,820),(1170,930),(1230,860)]
    d.line(pts, fill=AMBER, width=10, joint='curve')
    d.line((640, 940, 800, 940), fill=(*TEAL, 220), width=8)
    centered(d, (720, 870), 'association', 38, fill=TEAL, bold=True)
    card(d, (120, 1540, 1320, 2240), fill=(19, 31, 59), outline=VIOLET)
    centered(d, (720, 1690), 'पूछिए:', 58, fill=INK, bold=True)
    qs = ['कौन-सा instrument?', 'कौन-सा time window?', 'कौन-सा sample?', 'कौन-सा outcome?']
    for i, q in enumerate(qs):
        y = 1810 + i*100
        d.ellipse((230, y-22, 274, y+22), fill=VIOLET)
        d.line((250, y, 272, y+20), fill=BG, width=7)
        d.line((272, y+20, 310, y-28), fill=BG, width=7)
        d.text((350, y-35), q, font=font(39), fill=INK)
    return im


def main():
    scenes = [scene1(), scene2(), scene3(), scene4()]
    for i, im in enumerate(scenes, 1):
        out = OUT / f'reel_0077_scene_{i:02d}.png'
        im.convert('RGB').save(out, format='PNG', optimize=False, compress_level=6)
        print(out)


if __name__ == '__main__':
    main()
