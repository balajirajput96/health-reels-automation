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


def gradient():
    im = Image.new('RGB', (W, H), BG); px = im.load()
    for y in range(H):
        t = y/(H-1)
        for x in range(W):
            glow=max(0.0,1-math.hypot(x-W*.5,y-H*.28)/(W*.95))
            px[x,y]=(min(255,int(7+10*t+8*glow)),min(255,int(15+18*t+19*glow)),min(255,int(36+37*t+28*glow)))
    return im


def glow(im, center, radius, color, alpha=70):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer); x,y=center
    d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(*color,alpha))
    layer=layer.filter(ImageFilter.GaussianBlur(radius*.55)); im.paste(layer,(0,0),layer)


def card(d, box, outline, fill=(17,38,69,242), width=7, radius=40):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=(*outline,220),width=width)


def wave(d,x0,y0,width,cycles,amp,color):
    pts=[]
    for i in range(180):
        t=i/179; pts.append((x0+width*t,y0+amp*math.sin(t*math.tau*cycles)+20*math.sin(t*math.tau*cycles*3.1)))
    d.line(pts,fill=(*color,225),width=10)


def network(d, pts, edges, cols):
    for a,b in edges: d.line((*pts[a],*pts[b]),fill=(*WHITE,130),width=7)
    for i,(x,y) in enumerate(pts):
        r=28; c=cols[i%len(cols)]
        d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,170),width=5)


def lower(d): d.rounded_rectangle((82,1830,1358,2460),radius=60,fill=(4,10,27,140))


def scene1():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,TEAL,42)
    card(d,(100,790,410,1320),TEAL); card(d,(565,790,875,1320),CYAN); card(d,(1030,790,1340,1320),AMBER)
    # eye, ear, touch cues
    d.ellipse((155,940,350,1080),outline=(*TEAL,230),width=14); d.ellipse((225,975,280,1030),fill=(*TEAL,220))
    wave(d,610,1020,205,4,38,CYAN)
    for i in range(4): d.ellipse((1100+i*50,965,1140+i*50,1005),fill=(*AMBER,220),outline=(*WHITE,140),width=3)
    d.line((720,1370,720,1510),fill=(*WHITE,210),width=12)
    card(d,(220,1560,1220,1770),VIOLET)
    d.line((360,1665,1080,1665),fill=(*WHITE,180),width=12)
    for x,c in [(420,TEAL),(600,CYAN),(800,AMBER),(1010,VIOLET)]: d.ellipse((x-23,1642,x+23,1688),fill=(*c,220))
    lower(d); return im


def scene2():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,CYAN,42)
    card(d,(130,800,620,1170),CYAN); card(d,(820,800,1310,1170),AMBER)
    # noisy versus clear cue
    wave(d,200,960,340,10,100,CYAN); wave(d,880,960,340,3,32,AMBER)
    d.line((720,1175,720,1390),fill=(*WHITE,210),width=12)
    card(d,(260,1420,1180,1740),TEAL)
    d.line((420,1580,1020,1580),fill=(*WHITE,190),width=12)
    for x,c,r in [(520,CYAN,26),(780,AMBER,45),(970,VIOLET,28)]: d.ellipse((x-r,1580-r,x+r,1580+r),fill=(*c,220),outline=(*WHITE,160),width=4)
    lower(d); return im


def scene3():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),480,AMBER,42)
    card(d,(110,800,1320,1170),AMBER)
    # flash, beep, touch markers with offset clock
    d.ellipse((245,930,350,1035),fill=(*WHITE,230),outline=(*AMBER,220),width=8)
    wave(d,525,985,260,4,35,CYAN)
    for i,x in enumerate([930,1000,1070]): d.ellipse((x,955,x+45,1000),fill=(*TEAL,220))
    d.line((220,1350,1220,1350),fill=(*WHITE,170),width=8)
    for x,c in [(420,AMBER),(760,CYAN),(1040,VIOLET)]: d.ellipse((x-26,1324,x+26,1376),fill=(*c,220))
    card(d,(250,1480,1190,1760),VIOLET)
    d.arc((460,1510,980,1730),0,180,fill=(*WHITE,190),width=10)
    d.line((720,1620,720,1515),fill=(*RED,220),width=10)
    lower(d); return im


def scene4():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),470,RED,42)
    card(d,(160,800,1280,1140),TEAL)
    d.line((320,1010,1120,1010),fill=(*WHITE,200),width=12)
    for x,c in [(370,TEAL),(560,CYAN),(760,AMBER),(960,VIOLET),(1120,RED)]: d.ellipse((x-28,982,x+28,1038),fill=(*c,220),outline=(*WHITE,170),width=5)
    card(d,(110,1270,620,1600),AMBER); card(d,(820,1270,1330,1600),RED)
    d.line((205,1350,510,1510),fill=(*WHITE,155),width=9); d.line((510,1350,205,1510),fill=(*WHITE,155),width=9)
    d.line((920,1340,1230,1530),fill=(*RED,220),width=18); d.line((1230,1340,920,1530),fill=(*RED,220),width=18)
    card(d,(260,1670,1180,1770),CYAN)
    d.line((480,1720,960,1720),fill=(*WHITE,210),width=12)
    lower(d); return im


for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
    path=OUT/f'reel_0021_scene_{i:02d}.png'; fn().save(path,optimize=True); print(path)
