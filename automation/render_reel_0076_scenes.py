from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
W, H = 1440, 2560
FONT = '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
BOLD = '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf'

def F(n, bold=False):
    return ImageFont.truetype(BOLD if bold and Path(BOLD).exists() else FONT, n)

def T(draw, xy, text, size, fill=(239, 244, 255), bold=False, anchor=None):
    draw.multiline_text(xy, text, font=F(size, bold), fill=fill, anchor=anchor,
                        spacing=16, align='center')

def P(draw, box, fill=(24, 38, 70), outline=(75, 111, 158), radius=36, width=4):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def bg(a, b):
    im = Image.new('RGB', (W, H))
    px = im.load()
    for y in range(H):
        q = y / (H - 1)
        c = tuple(int(a[i] * (1 - q) + b[i] * q) for i in range(3))
        for x in range(W):
            px[x, y] = c
    return im

def head(draw, kicker, title, sub):
    T(draw, (90, 110), kicker, 44, (130, 211, 255), True)
    T(draw, (90, 205), title, 76, (239, 244, 255), True)
    T(draw, (90, 360), sub, 38, (184, 201, 226))

def scene1():
    im = bg((9, 25, 54), (26, 14, 55)); d = ImageDraw.Draw(im)
    head(d, '01 / OPERATIONALIZE', 'मापा कैसे?', 'One label • several instruments')
    P(d, (140, 650, 1300, 940), fill=(28, 43, 75), outline=(166, 139, 255))
    T(d, (720, 795), 'PROCRASTINATION', 54, (240, 218, 255), True, 'mm')
    cards = [('SELF-REPORT', 'delay / discomfort', (130, 211, 255)),
             ('BEHAVIOR', 'timing / completion', (76, 210, 190)),
             ('OUTCOME', 'mood / performance', (255, 184, 105))]
    for i, (lab, sub, col) in enumerate(cards):
        y = 1100 + i * 350
        P(d, (170, y, 1270, y + 230), fill=(25, 43, 72), outline=col)
        T(d, (720, y + 78), lab, 42, col, True, 'mm')
        T(d, (720, y + 160), sub, 34, (239, 244, 255), False, 'mm')
    P(d, (180, 2200, 1260, 2390), fill=(40, 28, 66), outline=(166, 139, 255))
    T(d, (720, 2295), 'एक label ≠ एक ही measure', 42, (240, 218, 255), True, 'mm')
    return im

def scene2():
    im = bg((8, 41, 57), (13, 61, 58)); d = ImageDraw.Draw(im)
    head(d, '02 / BEHAVIOR', 'समय का रिकॉर्ड', 'Planned • actual • deadline pacing')
    P(d, (120, 690, 1320, 1800), fill=(25, 52, 67), outline=(76, 210, 190))
    T(d, (720, 825), 'STUDY TASK', 52, (184, 235, 220), True, 'mm')
    y = 1120
    d.line((230, y, 1210, y), fill=(210, 220, 240), width=8)
    marks = [(300, 'PLAN', (130, 211, 255)), (700, 'ACTUAL', (76, 210, 190)), (1110, 'DEADLINE', (255, 184, 105))]
    for x, lab, col in marks:
        d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=col)
        T(d, (x, y + 120), lab, 34, col, True, 'mm')
    T(d, (720, 1500), 'planned − actual\ncompletion days\ndeadline pacing', 40, (239, 244, 255), True, 'mm')
    P(d, (170, 2040, 1270, 2370), fill=(37, 27, 63), outline=(166, 139, 255))
    T(d, (720, 2205), 'observed delay भी एक definition है', 40, (240, 218, 255), True, 'mm')
    return im

def scene3():
    im = bg((34, 18, 58), (9, 28, 53)); d = ImageDraw.Draw(im)
    head(d, '03 / COMPARISON', 'Measure ≠ outcome', 'Different instruments, different links')
    P(d, (120, 700, 600, 1810), fill=(25, 39, 71), outline=(130, 211, 255))
    T(d, (360, 870), 'SELF-REPORT', 43, (130, 211, 255), True, 'mm')
    T(d, (360, 1210), 'delay\ndiscomfort\nstate', 40, (239, 244, 255), True, 'mm')
    P(d, (840, 700, 1320, 1810), fill=(25, 52, 67), outline=(76, 210, 190))
    T(d, (1080, 870), 'BEHAVIOR', 43, (184, 235, 220), True, 'mm')
    T(d, (1080, 1210), 'study time\ncompletion days\npacing', 40, (239, 244, 255), True, 'mm')
    d.line((600, 1250, 840, 1250), fill=(255, 184, 105), width=10)
    d.polygon([(840, 1250), (765, 1200), (765, 1300)], fill=(255, 184, 105))
    T(d, (720, 1930), 'संबंध केवल moderate हो सकता है', 39, (255, 218, 225), True, 'mm')
    P(d, (160, 2110, 1280, 2380), fill=(41, 25, 63), outline=(166, 139, 255))
    T(d, (720, 2245), 'mood और completion अलग outcomes', 38, (240, 218, 255), True, 'mm')
    return im

def scene4():
    im = bg((19, 31, 49), (49, 15, 38)); d = ImageDraw.Draw(im)
    head(d, '04 / INTERPRET', 'Association ≠ cause', 'Ask four questions before a conclusion')
    P(d, (150, 650, 1290, 1550), fill=(33, 31, 58), outline=(130, 211, 255))
    T(d, (720, 820), 'CORRELATES / THEORY', 48, (130, 211, 255), True, 'mm')
    T(d, (720, 1110), 'task aversiveness\nself-efficacy\nimpulsiveness\nconscientiousness', 36, (239, 244, 255), True, 'mm')
    P(d, (150, 1710, 1290, 2240), fill=(25, 52, 67), outline=(76, 210, 190))
    T(d, (720, 1840), 'CHECK THE STUDY', 44, (184, 235, 220), True, 'mm')
    T(d, (720, 2070), 'कौन-सा scale?  कौन-सा task?\nकौन-सा domain?  कौन-सा outcome?', 35, (239, 244, 255), True, 'mm')
    P(d, (190, 2320, 1250, 2460), fill=(41, 25, 63), outline=(166, 139, 255))
    T(d, (720, 2390), 'diagnosis नहीं • measurement literacy', 34, (240, 218, 255), True, 'mm')
    return im

for i, fn in enumerate((scene1, scene2, scene3, scene4), 1):
    path = OUT / f'reel_0076_scene_0{i}.png'
    fn().save(path, format='PNG')
    print(path)
