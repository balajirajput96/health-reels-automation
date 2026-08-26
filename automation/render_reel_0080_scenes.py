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
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    return ImageFont.truetype(FONT_LATIN_BOLD if bold else FONT_LATIN_REG, size)


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
    for run, devanagari in _runs(text):
        box = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), run, font=font(size, bold, devanagari))
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


def font_height(size: int, bold: bool = False):
    return font(size, bold, True)


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
    draw_smart(d, (100, y), text, 42, fill=color, bold=True)


def title(d, text, y=180):
    draw_smart(d, (100, y), text, 74, fill=INK, bold=True)


def card(d, box, fill=(19, 31, 59), outline=(71, 98, 141), width=5, radius=34):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(d, xy, text, size, fill=INK, bold=False):
    draw_smart(d, xy, text, size, fill=fill, bold=bold, centered_text=True)


def note(d, text, xy, fill=MUTED, size=34):
    draw_smart(d, xy, text, size, fill=fill, bold=False)


def scene1():
    im = gradient(); glow(im, (720, 650), 520, VIOLET); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'SOCIAL BUFFERING', 90, CYAN); title(d, 'साथ होना = क्या मापा?', 180)
    card(d, (120, 520, 1320, 960), fill=(27, 39, 75), outline=VIOLET)
    centered(d, (720, 665), 'SOCIAL CONDITION', 54, fill=CYAN, bold=True)
    centered(d, (720, 810), 'presence / assistance / support', 36, fill=INK)
    d.line((720, 960, 720, 1110), fill=(*INK, 170), width=8)
    nodes = [(300, 1430, CYAN, 'STRESSOR', 'defined task'), (720, 1430, VIOLET, 'MEASURE', 'signal / report'), (1140, 1430, AMBER, 'TIME', 'when observed')]
    for x, y, c, en, sub in nodes:
        d.line((720, 1110, x, y - 140), fill=(*c, 170), width=7)
        d.ellipse((x - 145, y - 145, x + 145, y + 145), fill=(*c, 225), outline=(*INK, 220), width=7)
        centered(d, (x, y - 28), en, 34, fill=BG, bold=True)
        centered(d, (x, y + 52), sub, 28, fill=BG)
    card(d, (120, 1990, 1320, 2300), fill=(22, 55, 61), outline=TEAL)
    centered(d, (720, 2145), 'defined comparison, not a guarantee', 40, fill=TEAL, bold=True)
    note(d, 'support का अर्थ context के साथ पढ़िए', (170, 2390), fill=AMBER, size=34)
    return im


def scene2():
    im = gradient(); glow(im, (350, 760), 430, CYAN); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'LAB TASK', 90, CYAN); title(d, 'एक stress test की timeline', 180)
    card(d, (100, 560, 1340, 1260), fill=(18, 42, 69), outline=CYAN)
    centered(d, (720, 700), 'LABORATORY COMPARISON', 48, fill=CYAN, bold=True)
    d.line((190, 970, 1250, 970), fill=(*INK, 210), width=10)
    points = [(230, 'BASELINE', CYAN), (520, 'FRIEND SUPPORT', TEAL), (840, 'SOCIAL TASK', RED), (1160, 'READOUT', AMBER)]
    for x, txt, c in points:
        d.ellipse((x - 25, 945, x + 25, 995), fill=c)
        centered(d, (x, 1080), txt, 27, fill=c, bold=True)
    note(d, 'किस window में support मिला?', (200, 1175), fill=INK, size=36)
    cards = [(100, 1420, 650, 1970, VIOLET, 'SUBJECTIVE', 'stress / calmness / anxiety'), (790, 1420, 1340, 1970, AMBER, 'PHYSIOLOGY', 'cortisol / cardiovascular')]
    for x0, y0, x1, y1, c, head, sub in cards:
        card(d, (x0, y0, x1, y1), fill=(29, 38, 69), outline=c)
        centered(d, ((x0 + x1) // 2, y0 + 120), head, 42, fill=c, bold=True)
        centered(d, ((x0 + x1) // 2, y0 + 275), sub, 31, fill=INK)
        d.line((x0 + 70, y0 + 410, x1 - 70, y0 + 410), fill=(*c, 150), width=5)
        if head == 'SUBJECTIVE':
            centered(d, ((x0 + x1) // 2, y0 + 470), 'reported experience', 33, fill=MUTED)
        else:
            pts = [(x0 + 75, y0 + 470), (x0 + 180, y0 + 430), (x0 + 280, y0 + 510), (x0 + 390, y0 + 390), (x1 - 75, y0 + 465)]
            d.line(pts, fill=c, width=10, joint='curve')
    card(d, (120, 2160, 1320, 2370), fill=(42, 37, 66), outline=RED)
    centered(d, (720, 2265), 'task + timing बदलें तो निष्कर्ष बदल सकता है', 36, fill=RED, bold=True)
    return im


def scene3():
    im = gradient(); glow(im, (1080, 720), 460, AMBER); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'SUPPORT TYPES', 90, AMBER); title(d, 'support एक ही चीज़ नहीं', 180)
    card(d, (100, 560, 650, 1710), fill=(22, 51, 75), outline=CYAN)
    centered(d, (375, 710), 'PERCEIVED', 46, fill=CYAN, bold=True)
    centered(d, (375, 850), 'संभावित access', 38, fill=INK)
    centered(d, (375, 1020), '“ज़रूरत पर कौन साथ होगा?”', 32, fill=MUTED)
    card(d, (790, 560, 1340, 1710), fill=(53, 42, 60), outline=AMBER)
    centered(d, (1065, 710), 'RECEIVED', 46, fill=AMBER, bold=True)
    centered(d, (1065, 850), 'मिला हुआ support', 38, fill=INK)
    centered(d, (1065, 1020), '“इस समय क्या मिला?”', 32, fill=MUTED)
    for x, c, txt in [(375, CYAN, 'construct A'), (1065, AMBER, 'construct B')]:
        for i in range(3):
            y = 1220 + i * 145
            d.rounded_rectangle((x - 170, y, x + 170, y + 82), radius=18, fill=(*c, 45), outline=(*c, 150), width=4)
            centered(d, (x, y + 41), txt, 29, fill=INK)
    d.line((650, 1120, 790, 1120), fill=(*TEAL, 230), width=8)
    centered(d, (720, 1050), 'अलग variables', 30, fill=TEAL, bold=True)
    card(d, (130, 1920, 1310, 2310), fill=(63, 36, 61), outline=RED)
    centered(d, (720, 2045), 'context भी measure का हिस्सा है', 42, fill=RED, bold=True)
    centered(d, (720, 2170), 'हर relationship पर एक जैसा निष्कर्ष नहीं', 32, fill=INK)
    return im


def scene4():
    im = gradient(); glow(im, (720, 820), 470, TEAL); d = ImageDraw.Draw(im, 'RGBA')
    label(d, 'DAILY-LIFE SAMPLING', 90, TEAL); title(d, 'हर prompt एक छोटा snapshot', 180)
    card(d, (120, 550, 1320, 1180), fill=(19, 31, 59), outline=VIOLET)
    centered(d, (720, 700), 'SMARTPHONE PROMPTS', 48, fill=VIOLET, bold=True)
    hours = ['09:00', '12:30', '16:00', '20:30']
    for i, h in enumerate(hours):
        x = 245 + i * 305
        d.line((x, 890, x, 1010), fill=(*TEAL, 220), width=8)
        d.ellipse((x - 25, 855, x + 25, 905), fill=TEAL)
        centered(d, (x, 1080), h, 30, fill=INK, bold=True)
    card(d, (120, 1330, 650, 2050), fill=(24, 63, 62), outline=TEAL)
    centered(d, (385, 1470), 'ASK NOW', 42, fill=TEAL, bold=True)
    centered(d, (385, 1615), 'context', 40, fill=INK)
    centered(d, (385, 1735), 'mood', 40, fill=INK)
    centered(d, (385, 1855), 'stress', 40, fill=INK)
    card(d, (790, 1330, 1320, 2050), fill=(63, 36, 61), outline=RED)
    centered(d, (1055, 1470), 'DO NOT JUMP', 38, fill=RED, bold=True)
    centered(d, (1055, 1615), 'one reading', 38, fill=INK)
    centered(d, (1055, 1735), '=> diagnosis', 38, fill=INK)
    centered(d, (1055, 1855), '=> guarantee', 38, fill=INK)
    card(d, (120, 2180, 1320, 2370), fill=(28, 42, 77), outline=CYAN)
    centered(d, (720, 2275), 'measure + time + context = सावधान निष्कर्ष', 35, fill=CYAN, bold=True)
    return im


def main():
    scenes = [scene1(), scene2(), scene3(), scene4()]
    for i, im in enumerate(scenes, 1):
        out = OUT / f'reel_0080_scene_{i:02d}.png'
        im.convert('RGB').save(out, format='PNG', optimize=False, compress_level=6)
        print(out)


if __name__ == '__main__':
    main()
