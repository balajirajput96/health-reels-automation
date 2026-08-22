from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'production' / 'assets' / 'reel0004'
W, H = 720, 1280
BG = (8, 18, 32)
INK = (234, 241, 247)
MUTED = (159, 181, 198)
CYAN = (64, 211, 192)
GOLD = (247, 190, 74)
CORAL = (242, 116, 104)
VIOLET = (151, 126, 255)
FONT = '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
BOLD = '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf'


def font(size: int, bold: bool = False):
    path = BOLD if bold and Path(BOLD).exists() else FONT
    return ImageFont.truetype(path, size=size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base(title: str, kicker: str, accent: tuple[int, int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line((0, y, W, y), fill=(int(8 + 7*t), int(18 + 12*t), int(32 + 20*t)))
    d.ellipse((500, -120, 900, 280), fill=tuple(min(255, int(v * 0.28)) for v in accent))
    d.ellipse((-180, 970, 240, 1390), fill=(int(accent[0]*0.13), int(accent[1]*0.13), int(accent[2]*0.13)))
    d.text((48, 54), kicker, font=font(24, True), fill=accent)
    d.text((48, 100), title, font=font(46, True), fill=INK)
    d.line((48, 194, 672, 194), fill=(52, 78, 98), width=2)
    d.text((48, 1195), 'रील ०००४ - रिसर्च विजुअल', font=font(20, True), fill=MUTED)
    return im, d


def save(im: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / name, format='PNG', optimize=True)


def frame_01():
    im, d = base('पूर्वाग्रह बराबर नहीं पूरी पहचान', 'कॉग्निटिव बायस', CORAL)
    rounded(d, (70, 330, 650, 820), 36, (22, 40, 58), outline=(68, 93, 113), width=3)
    d.ellipse((205, 420, 515, 730), outline=CORAL, width=10)
    d.arc((260, 475, 460, 675), 205, 335, fill=GOLD, width=10)
    d.line((360, 520, 360, 630), fill=CYAN, width=10)
    d.ellipse((330, 505, 390, 565), fill=CYAN)
    d.text((115, 875), 'एक खास कार्य में', font=font(38, True), fill=INK)
    d.text((115, 935), 'रिस्पॉन्स पैटर्न', font=font(38, True), fill=GOLD)
    d.text((115, 995), 'मापा जाता है', font=font(38, True), fill=INK)
    return im


def frame_02():
    im, d = base('अध्ययन कैसे मापता है?', 'परिचालन परिभाषा', CYAN)
    for i, (label, color, x) in enumerate([('कार्य', CYAN, 66), ('रिस्पॉन्स', GOLD, 258), ('स्कोर', VIOLET, 476)]):
        rounded(d, (x, 360, x+170, 520), 24, (20, 38, 56), outline=color, width=4)
        d.text((x+26, 415), label, font=font(25, True), fill=color)
        d.ellipse((x+68, 570, x+102, 604), fill=color)
        if i < 2:
            d.line((x+175, 440, x+205, 440), fill=MUTED, width=4)
            d.polygon([(x+205, 440), (x+193, 430), (x+193, 450)], fill=MUTED)
    d.text((72, 730), 'लेबल नहीं,', font=font(44, True), fill=INK)
    d.text((72, 800), 'परिचालन परिभाषा', font=font(35, True), fill=CYAN)
    d.text((72, 860), 'महत्वपूर्ण है', font=font(44, True), fill=INK)
    return im


def frame_03():
    im, d = base('मानक या तुलना', 'मापन डिज़ाइन', GOLD)
    rounded(d, (62, 320, 658, 700), 32, (19, 36, 53), outline=(60, 85, 104), width=3)
    d.line((110, 570, 610, 570), fill=GOLD, width=8)
    d.text((110, 470), 'मानक / सटीकता', font=font(28, True), fill=GOLD)
    d.ellipse((260, 520, 318, 578), fill=CYAN)
    d.ellipse((430, 520, 488, 578), fill=CORAL)
    d.text((102, 800), 'या दो स्थितियाँ', font=font(40, True), fill=INK)
    rounded(d, (102, 890, 330, 1010), 22, (33, 69, 75), outline=CYAN, width=3)
    rounded(d, (390, 890, 618, 1010), 22, (70, 48, 54), outline=CORAL, width=3)
    d.text((165, 930), 'फ्रेम एक', font=font(24, True), fill=CYAN)
    d.text((455, 930), 'फ्रेम दो', font=font(24, True), fill=CORAL)
    d.line((330, 950, 390, 950), fill=MUTED, width=4)
    return im


def frame_04():
    im, d = base('एक स्कोर सब कुछ नहीं', 'संदर्भ महत्वपूर्ण', VIOLET)
    rounded(d, (70, 330, 650, 630), 30, (24, 40, 62), outline=VIOLET, width=3)
    d.text((112, 400), 'स्कोर', font=font(48, True), fill=VIOLET)
    d.text((112, 510), 'बराबर नहीं व्यक्तित्व', font=font(35, True), fill=INK)
    tags = [('शब्द-चयन', CYAN), ('उत्तर का तरीका', GOLD), ('संदर्भ', CORAL), ('नमूना', VIOLET)]
    for i, (label, col) in enumerate(tags):
        x = 74 + (i % 2) * 315
        y = 760 + (i // 2) * 130
        rounded(d, (x, y, x+270, y+76), 18, (20, 34, 51), outline=col, width=3)
        d.text((x+24, y+22), label, font=font(27, True), fill=col)
    return im


def frame_05():
    im, d = base('विश्वसनीयता कार्य से बदल सकती है', 'मनोमिति', CYAN)
    chart = (90, 360, 630, 870)
    rounded(d, chart, 30, (18, 34, 51), outline=(63, 88, 108), width=3)
    d.line((145, 770, 570, 770), fill=MUTED, width=3)
    d.line((145, 450, 145, 770), fill=MUTED, width=3)
    bars = [('डॉट-प्रोब', 140, CORAL), ('एएटी', 230, GOLD), ('आईएटी', 285, CYAN)]
    for i, (label, height, col) in enumerate(bars):
        x = 190 + i*125
        d.rounded_rectangle((x, 770-height, x+72, 770), radius=12, fill=col)
        d.text((x-15, 810), label, font=font(21, True), fill=INK)
    d.text((175, 400), 'कार्य - उपकरण - समय', font=font(30, True), fill=CYAN)
    d.text((98, 980), 'इसलिए डिज़ाइन की सीमा', font=font(36, True), fill=INK)
    d.text((98, 1040), 'बतानी ज़रूरी है', font=font(36, True), fill=GOLD)
    return im


def frame_06():
    im, d = base('सही सवाल पूछिए', 'आर्काइव टेकअवे', CORAL)
    rounded(d, (70, 340, 650, 720), 34, (24, 40, 57), outline=CORAL, width=3)
    d.text((112, 420), 'इस नमूने में', font=font(42, True), fill=INK)
    d.text((112, 500), 'इस डिज़ाइन ने', font=font(42, True), fill=GOLD)
    d.text((112, 580), 'क्या मापा?', font=font(52, True), fill=CYAN)
    d.line((112, 660, 608, 660), fill=(82, 107, 125), width=3)
    d.text((86, 835), 'निदान नहीं', font=font(34, True), fill=CORAL)
    d.text((86, 900), 'सामान्य शिक्षा', font=font(30, True), fill=INK)
    d.text((86, 958), 'चिकित्सकीय सलाह नहीं', font=font(30, True), fill=INK)
    d.text((86, 1030), 'एआई आवाज़ - प्रक्रियात्मक दृश्य', font=font(24, True), fill=MUTED)
    return im


if __name__ == '__main__':
    for index, image in enumerate([frame_01(), frame_02(), frame_03(), frame_04(), frame_05(), frame_06()], 1):
        save(image, f'frame_{index:02d}.png')
    print(OUT)
