from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path('/home/ubuntu/repos/health-reels-automation')
OUT = ROOT / 'production' / 'assets' / 'reel0003'
W, H = 720, 1280

BG_TOP = (10, 20, 42)
BG_BOTTOM = (37, 25, 66)
ACCENT = (91, 215, 196)
WARM = (245, 186, 103)
LILAC = (172, 143, 245)
PALE = (229, 241, 247)
MUTED = (128, 159, 185)
DARK = (8, 15, 31)


def gradient() -> Image.Image:
    im = Image.new('RGB', (W, H))
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(BG_TOP[i] * (1 - t) + BG_BOTTOM[i] * t) for i in range(3))
        for x in range(W):
            px[x, y] = c
    return im


def glow(base: Image.Image, center: tuple[int, int], radius: int, color: tuple[int, int, int], alpha: int = 85) -> None:
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius // 2))
    base.paste(layer, (0, 0), layer)


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=2, radius=22):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def silhouette(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0, color=PALE, outline=ACCENT):
    r = int(52 * scale)
    draw.ellipse((cx - r, cy - r - int(155 * scale), cx + r, cy + r - int(155 * scale)), fill=color)
    body = (cx - int(92 * scale), cy - int(90 * scale), cx + int(92 * scale), cy + int(195 * scale))
    rounded(draw, body, fill=color, outline=outline, width=max(2, int(5 * scale)), radius=int(55 * scale))
    draw.line((cx - int(42 * scale), cy + int(10 * scale), cx - int(132 * scale), cy + int(115 * scale)), fill=outline, width=max(3, int(8 * scale)))
    draw.line((cx + int(42 * scale), cy + int(10 * scale), cx + int(132 * scale), cy + int(115 * scale)), fill=outline, width=max(3, int(8 * scale)))


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / name, format='PNG', optimize=True)


def frame_01():
    im = gradient(); glow(im, (150, 260), 190, WARM, 75); glow(im, (560, 1000), 260, LILAC, 45)
    d = ImageDraw.Draw(im)
    d.ellipse((180, 190, 540, 550), outline=(125, 175, 205), width=6)
    silhouette(d, 360, 720, 1.1)
    for i, (x, y, c) in enumerate([(105, 915, ACCENT), (235, 1015, WARM), (430, 1000, LILAC), (550, 885, MUTED)]):
        rounded(d, (x, y, x + 92, y + 92), fill=(*c, 70), outline=c, width=3, radius=18)
        d.line((x + 24, y + 48, x + 68, y + 48), fill=c, width=5)
        d.line((x + 46, y + 26, x + 46, y + 70), fill=c, width=5)
    d.arc((78, 625, 642, 1190), 205, 335, fill=(205, 225, 240), width=3)
    save(im, 'frame_01_hook.png')


def frame_02():
    im = gradient(); glow(im, (350, 710), 240, ACCENT, 40)
    d = ImageDraw.Draw(im); silhouette(d, 360, 740, 0.9)
    cards = [(95, 300, ACCENT), (405, 250, WARM), (220, 975, LILAC)]
    for x, y, c in cards:
        rounded(d, (x, y, x + 220, y + 150), fill=(19, 37, 65), outline=c, width=4, radius=24)
        d.ellipse((x + 36, y + 38, x + 84, y + 86), outline=c, width=4)
        d.line((x + 110, y + 45, x + 185, y + 45), fill=PALE, width=5)
        d.line((x + 110, y + 78, x + 170, y + 78), fill=MUTED, width=4)
        d.line((x + 110, y + 107, x + 192, y + 107), fill=MUTED, width=4)
    d.line((315, 450, 290, 650), fill=ACCENT, width=3)
    d.line((455, 400, 420, 650), fill=WARM, width=3)
    d.line((340, 975, 350, 930), fill=LILAC, width=3)
    save(im, 'frame_02_concepts.png')


def frame_03():
    im = gradient(); glow(im, (360, 650), 270, ACCENT, 45)
    d = ImageDraw.Draw(im)
    positions = [(80, 250), (390, 250), (80, 570), (390, 570), (80, 890), (390, 890)]
    colors = [ACCENT, WARM, LILAC, (112, 200, 235), (242, 139, 155), (192, 215, 155)]
    for (x, y), c in zip(positions, colors):
        rounded(d, (x, y, x + 250, y + 210), fill=(16, 31, 57), outline=c, width=4, radius=28)
        d.ellipse((x + 85, y + 38, x + 165, y + 118), outline=c, width=5)
        d.line((x + 65, y + 157, x + 185, y + 157), fill=PALE, width=5)
        d.line((x + 95, y + 180, x + 155, y + 180), fill=MUTED, width=4)
    d.arc((245, 160, 475, 1110), 90, 270, fill=(205, 225, 240), width=3)
    save(im, 'frame_03_domains.png')


def frame_04():
    im = gradient(); glow(im, (160, 780), 200, WARM, 55); glow(im, (550, 410), 220, ACCENT, 45)
    d = ImageDraw.Draw(im)
    rounded(d, (78, 180, 642, 1010), fill=(16, 31, 57), outline=PALE, width=4, radius=30)
    for i, y in enumerate([300, 420, 540, 660, 780]):
        d.ellipse((125, y - 18, 161, y + 18), outline=ACCENT if i % 2 == 0 else WARM, width=4)
        d.line((205, y, 575, y), fill=(80, 116, 146), width=7)
        d.line((205, y, 330 + i * 38, y), fill=ACCENT if i % 2 == 0 else WARM, width=7)
        d.ellipse((315 + i * 38, y - 18, 351 + i * 38, y + 18), fill=PALE)
    d.line((110, 900, 610, 900), fill=LILAC, width=5)
    d.line((150, 945, 570, 945), fill=MUTED, width=5)
    d.line((205, 1020, 205, 1120), fill=ACCENT, width=4)
    d.line((360, 1020, 360, 1120), fill=WARM, width=4)
    d.line((515, 1020, 515, 1120), fill=LILAC, width=4)
    save(im, 'frame_04_questionnaire.png')


def frame_05():
    im = gradient(); glow(im, (360, 780), 280, LILAC, 42)
    d = ImageDraw.Draw(im)
    silhouette(d, 160, 710, 0.72)
    rounded(d, (330, 295, 625, 760), fill=(16, 31, 57), outline=ACCENT, width=5, radius=28)
    for y, c, length in [(390, ACCENT, 205), (485, WARM, 160), (580, LILAC, 220), (675, MUTED, 135)]:
        d.line((370, y, 570, y), fill=(76, 114, 143), width=8)
        d.line((370, y, 370 + length, y), fill=c, width=8)
    d.rectangle((74, 990, 646, 1070), outline=(216, 225, 239), width=4)
    d.line((360, 1080, 360, 1160), fill=PALE, width=4)
    d.line((330, 1160, 390, 1160), fill=PALE, width=4)
    save(im, 'frame_05_limits.png')


def frame_06():
    im = gradient(); glow(im, (360, 520), 280, ACCENT, 42); glow(im, (360, 1050), 220, WARM, 32)
    d = ImageDraw.Draw(im)
    d.ellipse((130, 260, 590, 720), outline=(129, 180, 205), width=5)
    silhouette(d, 360, 760, 0.82, color=(218, 231, 239), outline=ACCENT)
    d.arc((160, 805, 560, 1190), 190, 350, fill=WARM, width=4)
    for x in [220, 315, 410, 505]:
        d.ellipse((x, 1040, x + 18, 1058), fill=ACCENT)
    save(im, 'frame_06_endcard.png')


if __name__ == '__main__':
    frame_01(); frame_02(); frame_03(); frame_04(); frame_05(); frame_06()
    print(f'generated 6 frames in {OUT}')
