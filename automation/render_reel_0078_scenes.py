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
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, 100))
    blurred = layer.filter(ImageFilter.GaussianBlur(radius // 2))
    im.paste(blurred, (0, 0), blurred)


def label(d, text, y, color=CYAN):
    d.text((100, y), text, font=font(44, True), fill=color)


def title(d, text, y=180):
    d.text((100, y), text, font=font(78, True), fill=INK)


def card(d, box, fill=(19, 31, 59), outline=(71, 98, 141), width=5, radius=34):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(d, xy, text, size, fill=INK, bold=False):
    box = d.textbbox((0, 0), text, font=font(size, bold))
    d.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=font(size, bold), fill=fill)


def note(d, text, xy, fill=MUTED, size=34):
    d.text(xy, text, font=font(size), fill=fill)


def scene1():
    im = gradient(); glow(im, (730, 600), 510, VIOLET); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'ACUTE STRESS MAP', 90, CYAN); title(d, '“STRESS” किस layer का?', 180)
    card(d, (100, 530, 1340, 900), fill=(28, 42, 77), outline=VIOLET)
    centered(d, (720, 715), 'ACUTE STRESS', 76, fill=INK, bold=True)
    centered(d, (720, 825), 'एक शब्द, कई measurements', 40, fill=MUTED)
    d.line((720, 900, 720, 1100), fill=(*INK, 170), width=8)
    nodes = [
        (300, 1370, CYAN, 'EXPOSURE', 'क्या हुआ?'),
        (720, 1370, VIOLET, 'APPRAISAL', 'कैसा लगा?'),
        (1140, 1370, AMBER, 'PHYSIOLOGY', 'body signal'),
        (430, 2050, TEAL, 'BEHAVIOR', 'क्या किया?'),
        (1010, 2050, RED, 'OUTCOME', 'क्या बदला?'),
    ]
    for x, y, c, en, hi in nodes:
        d.line((720, 1100, x, y - 145), fill=(*c, 170), width=7)
        d.ellipse((x - 145, y - 145, x + 145, y + 145), fill=(*c, 220), outline=(*INK, 220), width=7)
        centered(d, (x, y - 28), en, 34, fill=BG, bold=True)
        centered(d, (x, y + 52), hi, 30, fill=BG)
    note(d, 'एक score = पूरी कहानी नहीं', (100, 2380), fill=AMBER, size=40)
    return im


def scene2():
    im = gradient(); glow(im, (350, 760), 420, CYAN); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'EXPOSURE vs APPRAISAL', 90, CYAN); title(d, 'Event ≠ अनुभव', 180)
    card(d, (100, 540, 650, 1560), fill=(18, 42, 69), outline=CYAN)
    centered(d, (375, 700), 'STRESSOR', 76, fill=CYAN, bold=True)
    centered(d, (375, 850), 'short-term task', 44, fill=INK, bold=True)
    events = ['social evaluation', 'novelty', 'कम control']
    for i, text in enumerate(events):
        y = 1060 + i * 155
        d.rounded_rectangle((160, y, 590, y + 98), radius=24, fill=(25, 66, 96), outline=(*CYAN, 150), width=4)
        centered(d, (375, y + 49), text, 32, fill=INK)
    card(d, (790, 540, 1340, 1560), fill=(46, 35, 55), outline=VIOLET)
    centered(d, (1065, 700), 'APPRAISAL', 62, fill=VIOLET, bold=True)
    centered(d, (1065, 850), 'perception scale', 42, fill=INK)
    for i, text in enumerate(['stressful?', 'threatening?', 'challenging?']):
        y = 1060 + i * 155
        d.rounded_rectangle((850, y, 1280, y + 98), radius=24, fill=(70, 43, 78), outline=(*VIOLET, 150), width=4)
        centered(d, (1065, y + 49), text, 34, fill=INK)
    d.line((650, 1060, 790, 1060), fill=(*TEAL, 230), width=8)
    centered(d, (720, 990), 'related', 32, fill=TEAL, bold=True)
    note(d, 'Questionnaire perception पूछता है; event अलग measure है।', (100, 1800), fill=INK, size=32)
    card(d, (100, 2040, 1340, 2280), fill=(22, 55, 61), outline=TEAL)
    centered(d, (720, 2160), 'instrument + time window matter', 44, fill=TEAL, bold=True)
    return im


def scene3():
    im = gradient(); glow(im, (1040, 770), 470, AMBER); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'SELECTED BODY SIGNALS', 90, AMBER); title(d, 'अलग signals, अलग clocks', 180)
    cards = [
        ((100, 560, 650, 1070), CYAN, 'BLOOD PRESSURE', 'SBP / DBP'),
        ((790, 560, 1340, 1070), AMBER, 'CORTISOL', 'endocrine'),
        ((100, 1220, 650, 1730), TEAL, 'PULSE', 'autonomic'),
        ((790, 1220, 1340, 1730), VIOLET, 'ANXIETY', 'state rating'),
    ]
    for box, c, head, sub in cards:
        card(d, box, fill=(25, 39, 69), outline=c)
        centered(d, ((box[0] + box[2]) // 2, box[1] + 110), head, 42, fill=c, bold=True)
        centered(d, ((box[0] + box[2]) // 2, box[1] + 190), sub, 35, fill=INK)
        x0, y0, x1 = box[0] + 70, box[1] + 390, box[2] - 70
        d.line((x0, y0, x1, y0), fill=(*c, 150), width=5)
        pts = [(x0, y0 + 30), (x0 + 70, y0 - 10), (x0 + 140, y0 + 20), (x0 + 220, y0 - 85), (x0 + 300, y0 - 25), (x1, y0 - 60)]
        d.line(pts, fill=c, width=10, joint='curve')
    card(d, (180, 1940, 1260, 2270), fill=(42, 37, 66), outline=RED)
    centered(d, (720, 2070), 'एक biomarker ≠ universal proxy', 46, fill=RED, bold=True)
    centered(d, (720, 2180), 'timing और context लिखिए', 38, fill=INK)
    return im


def scene4():
    im = gradient(); glow(im, (720, 780), 430, TEAL); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'READ THE PAPER CAREFULLY', 90, TEAL); title(d, 'Association ≠ diagnosis', 180)
    card(d, (120, 540, 1320, 1150), fill=(19, 31, 59), outline=VIOLET)
    centered(d, (720, 690), 'CHECKLIST', 64, fill=VIOLET, bold=True)
    qs = ['task / exposure', 'instrument', 'time window', 'endpoint + design']
    for i, q in enumerate(qs):
        y = 835 + i * 75
        d.ellipse((240, y - 19, 278, y + 19), fill=TEAL)
        d.line((250, y, 265, y + 14), fill=BG, width=6)
        d.line((265, y + 14, 294, y - 20), fill=BG, width=6)
        d.text((330, y - 32), q, font=font(39), fill=INK)
    card(d, (120, 1310, 650, 2040), fill=(24, 63, 62), outline=TEAL)
    centered(d, (385, 1450), 'MEASURED', 50, fill=TEAL, bold=True)
    centered(d, (385, 1600), 'one layer', 44, fill=INK)
    centered(d, (385, 1780), 'not the whole person', 38, fill=MUTED)
    card(d, (790, 1310, 1320, 2040), fill=(63, 36, 61), outline=RED)
    centered(d, (1055, 1450), 'NOT ESTABLISHED', 39, fill=RED, bold=True)
    centered(d, (1055, 1600), 'causal proof', 44, fill=INK)
    centered(d, (1055, 1780), 'diagnosis', 44, fill=INK)
    card(d, (120, 2180, 1320, 2350), fill=(28, 42, 77), outline=CYAN)
    centered(d, (720, 2265), 'AI visuals • public education • no personal advice', 34, fill=CYAN, bold=True)
    return im


def main():
    scenes = [scene1(), scene2(), scene3(), scene4()]
    for i, im in enumerate(scenes, 1):
        out = OUT / f'reel_0078_scene_{i:02d}.png'
        im.convert('RGB').save(out, format='PNG', optimize=False, compress_level=6)
        print(out)


if __name__ == '__main__':
    main()
