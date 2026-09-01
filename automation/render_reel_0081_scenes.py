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
FONT_LATIN_REG = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
FONT_LATIN_BOLD = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'


def font(size: int, bold: bool = False, devanagari: bool = True):
    if devanagari:
        path = FONT_BOLD if bold else FONT_REG
    else:
        path = FONT_LATIN_BOLD if bold else FONT_LATIN_REG
    return ImageFont.truetype(path, size)


def _is_devanagari(char: str) -> bool:
    return '\u0900' <= char <= '\u097f' or char in '\u200c\u200d\u25cc'


def _runs(text: str):
    if not text:
        return []
    runs = []
    current = text[0]
    current_deva = _is_devanagari(current)
    for char in text[1:]:
        char_deva = _is_devanagari(char)
        if char_deva == current_deva:
            current += char
        else:
            runs.append((current, current_deva))
            current = char
            current_deva = char_deva
    runs.append((current, current_deva))
    return runs


def _metrics(text: str, size: int, bold: bool):
    widths = 0
    tops = []
    bottoms = []
    probe = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    for run, devanagari in _runs(text):
        box = probe.textbbox((0, 0), run, font=font(size, bold, devanagari))
        widths += box[2] - box[0]
        tops.append(box[1])
        bottoms.append(box[3])
    return widths, min(tops, default=0), max(bottoms, default=0)


def draw_smart(d, xy, text, size, fill=INK, bold=False, centered_text=False):
    width, top, bottom = _metrics(text, size, bold)
    x, y = xy
    if centered_text:
        x -= width / 2
        y -= (bottom - top) / 2 + top
    else:
        y -= top
    for run, devanagari in _runs(text):
        d.text((x, y), run, font=font(size, bold, devanagari), fill=fill)
        box = d.textbbox((0, 0), run, font=font(size, bold, devanagari))
        x += box[2] - box[0]


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


def card(d, box, fill=(19, 31, 59), outline=(71, 98, 141), width=5, radius=34):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def label(d, text, y, color=CYAN):
    draw_smart(d, (100, y), text, 42, fill=color, bold=True)


def title(d, text, y=180):
    draw_smart(d, (100, y), text, 72, fill=INK, bold=True)


def centered(d, xy, text, size, fill=INK, bold=False):
    draw_smart(d, xy, text, size, fill=fill, bold=bold, centered_text=True)


def note(d, text, xy, fill=MUTED, size=34):
    draw_smart(d, xy, text, size, fill=fill, bold=False)


def scene1():
    im = gradient(); glow(im, (700, 650), 520, VIOLET); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'MEASUREMENT LAYERS', 90, CYAN); title(d, 'stress और attention अलग layers', 180)
    cards = [
        ((120, 560, 1320, 980), CYAN, 'STRESSOR', 'exam / social evaluation / task'),
        ((120, 1110, 1320, 1530), VIOLET, 'SUBJECTIVE', 'reported appraisal / feeling'),
        ((120, 1660, 1320, 2080), AMBER, 'ATTENTION TASK', 'response time / accuracy / errors'),
    ]
    for box, color, head, sub in cards:
        card(d, box, fill=(24, 38, 70), outline=color)
        x0, y0, x1, y1 = box
        centered(d, ((x0 + x1) // 2, y0 + 120), head, 48, fill=color, bold=True)
        centered(d, ((x0 + x1) // 2, y0 + 285), sub, 34, fill=INK)
    card(d, (120, 2230, 1320, 2420), fill=(42, 37, 66), outline=TEAL)
    centered(d, (720, 2325), 'एक label नहीं, कई measures', 40, fill=TEAL, bold=True)
    return im


def scene2():
    im = gradient(); glow(im, (350, 760), 430, CYAN); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'LAB TIMELINE', 90, CYAN); title(d, 'कब मापा गया?', 180)
    card(d, (100, 560, 1340, 1270), fill=(18, 42, 69), outline=CYAN)
    centered(d, (720, 700), 'BEFORE / DURING / AFTER', 48, fill=CYAN, bold=True)
    d.line((190, 970, 1250, 970), fill=(*INK, 210), width=10)
    points = [(230, 'BASELINE', CYAN), (560, 'STRESSOR', RED), (880, 'ATTENTION TASK', VIOLET), (1190, 'READOUT', AMBER)]
    for x, txt, color in points:
        d.ellipse((x - 25, 945, x + 25, 995), fill=color)
        centered(d, (x, 1080), txt, 25, fill=color, bold=True)
    note(d, 'timing बदलने पर interpretation भी बदलता है', (190, 1175), fill=INK, size=36)
    card(d, (100, 1450, 650, 2050), fill=(24, 57, 72), outline=TEAL)
    centered(d, (375, 1600), 'BEHAVIOR', 44, fill=TEAL, bold=True)
    centered(d, (375, 1760), 'accuracy', 38, fill=INK)
    centered(d, (375, 1870), 'response time', 38, fill=INK)
    card(d, (790, 1450, 1340, 2050), fill=(55, 42, 61), outline=AMBER)
    centered(d, (1065, 1600), 'PHYSIOLOGY', 42, fill=AMBER, bold=True)
    centered(d, (1065, 1760), 'cortisol', 38, fill=INK)
    centered(d, (1065, 1870), 'alpha-amylase', 34, fill=INK)
    card(d, (120, 2190, 1320, 2390), fill=(42, 37, 66), outline=RED)
    centered(d, (720, 2290), 'same stressor, अलग readout', 38, fill=RED, bold=True)
    return im


def scene3():
    im = gradient(); glow(im, (1070, 700), 460, AMBER); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'ATTENTION TASK', 90, AMBER); title(d, 'task में क्या दिखता है?', 180)
    card(d, (100, 560, 650, 1770), fill=(22, 51, 75), outline=CYAN)
    centered(d, (375, 720), 'BEHAVIOR', 46, fill=CYAN, bold=True)
    metrics = ['response time', 'accuracy', 'error rate']
    for i, txt in enumerate(metrics):
        y = 1000 + i * 190
        d.rounded_rectangle((170, y, 580, y + 110), radius=20, fill=(*CYAN, 45), outline=(*CYAN, 160), width=4)
        centered(d, (375, y + 55), txt, 32, fill=INK)
    card(d, (790, 560, 1340, 1770), fill=(53, 42, 60), outline=VIOLET)
    centered(d, (1065, 720), 'EEG', 52, fill=VIOLET, bold=True)
    centered(d, (1065, 900), 'N1 / N2 / P3', 38, fill=INK, bold=True)
    d.line((870, 1190, 1260, 1190), fill=(*VIOLET, 150), width=5)
    pts = [(870, 1330), (950, 1270), (1020, 1390), (1100, 1300), (1180, 1370), (1260, 1280)]
    d.line(pts, fill=VIOLET, width=10, joint='curve')
    centered(d, (1065, 1600), 'time-resolved correlate', 31, fill=MUTED)
    card(d, (130, 1980, 1310, 2320), fill=(63, 36, 61), outline=RED)
    centered(d, (720, 2100), 'task result = task context', 42, fill=RED, bold=True)
    centered(d, (720, 2215), 'universal attention score नहीं', 32, fill=INK)
    return im


def scene4():
    im = gradient(); glow(im, (720, 820), 470, TEAL); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'INTERPRETATION', 90, TEAL); title(d, 'निष्कर्ष को सीमित रखें', 180)
    card(d, (120, 560, 1320, 1150), fill=(19, 31, 59), outline=VIOLET)
    centered(d, (720, 720), 'ONE TASK', 50, fill=VIOLET, bold=True)
    centered(d, (720, 900), 'एक setting, एक sample, एक time window', 34, fill=INK)
    d.line((250, 1030, 1190, 1030), fill=(*VIOLET, 180), width=6)
    card(d, (120, 1320, 650, 2040), fill=(24, 63, 62), outline=TEAL)
    centered(d, (385, 1460), 'MEASURE', 44, fill=TEAL, bold=True)
    centered(d, (385, 1630), 'self-report', 36, fill=INK)
    centered(d, (385, 1745), 'behavior', 36, fill=INK)
    centered(d, (385, 1860), 'physiology', 36, fill=INK)
    card(d, (790, 1320, 1320, 2040), fill=(63, 36, 61), outline=RED)
    centered(d, (1055, 1460), 'DO NOT JUMP', 36, fill=RED, bold=True)
    centered(d, (1055, 1630), 'diagnosis', 36, fill=INK)
    centered(d, (1055, 1745), 'causation', 36, fill=INK)
    centered(d, (1055, 1860), 'individual forecast', 30, fill=INK)
    card(d, (120, 2190, 1320, 2400), fill=(28, 42, 77), outline=CYAN)
    centered(d, (720, 2295), 'stressor + task + timing + context', 34, fill=CYAN, bold=True)
    return im


def main():
    scenes = [scene1(), scene2(), scene3(), scene4()]
    for i, im in enumerate(scenes, 1):
        out = OUT / f'reel_0081_scene_{i:02d}.png'
        im.convert('RGB').save(out, format='PNG', optimize=False, compress_level=6)
        print(out)


if __name__ == '__main__':
    main()
