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


def network(d, pts, edges, cols):
    for a,b in edges: d.line((*pts[a],*pts[b]),fill=(*WHITE,130),width=7)
    for i,(x,y) in enumerate(pts):
        r=28; c=cols[i%len(cols)]
        d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,170),width=5)


def wave(d,x0,y0,width,cycles,amp,color):
    pts=[]
    for i in range(180):
        t=i/179; pts.append((x0+width*t,y0+amp*math.sin(t*math.tau*cycles)+20*math.sin(t*math.tau*cycles*3.1)))
    d.line(pts,fill=(*color,225),width=10)


def lower(d): d.rounded_rectangle((82,1830,1358,2460),radius=60,fill=(4,10,27,140))


def scene1():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),510,TEAL,42)
    card(d,(90,790,650,1370),AMBER); card(d,(790,790,1350,1370),CYAN)
    # language side
    for i in range(4): d.rounded_rectangle((190,930+i*72,520,970+i*72),radius=18,fill=(*AMBER,190))
    # spatial side
    d.line((900,1080,1240,1080),fill=(*CYAN,210),width=14)
    for x in (1010,1130): d.line((x,1010,x,1150),fill=(*VIOLET,210),width=12)
    d.ellipse((1060,1050,1100,1090),fill=(*WHITE,230))
    d.line((720,1420,720,1570),fill=(*WHITE,210),width=12)
    card(d,(240,1610,1200,1770),TEAL)
    for i in range(6): d.line((360+i*120,1690,430+i*120,1690),fill=(*WHITE,170),width=9)
    lower(d); return im


def scene2():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,CYAN,42)
    card(d,(150,780,1290,1160),CYAN)
    pts=[(360,920),(560,850),(760,980),(950,840),(1130,950)]
    network(d,pts,[(0,1),(1,2),(2,3),(3,4),(0,2),(2,4)],[CYAN,TEAL,VIOLET])
    card(d,(180,1240,620,1580),AMBER); card(d,(820,1240,1260,1580),VIOLET)
    wave(d,240,1400,300,3,46,AMBER); wave(d,880,1400,300,3,46,VIOLET)
    d.line((720,1170,720,1210),fill=(*WHITE,210),width=10)
    lower(d); return im


def scene3():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),480,AMBER,42)
    card(d,(100,800,430,1250),AMBER); card(d,(555,800,885,1250),TEAL); card(d,(1010,800,1340,1250),VIOLET)
    # activation, fMRI and graph cards
    for i,h in enumerate([100,180,140,220]):
        x=160+i*62; d.rounded_rectangle((x,1160-h,x+36,1160),radius=10,fill=(*AMBER,210))
    wave(d,620,1010,200,3,48,TEAL)
    pts=[(1050,980),(1160,900),(1260,1020),(1150,1130)]
    network(d,pts,[(0,1),(1,2),(2,3),(3,0),(0,2)],[VIOLET,CYAN])
    d.line((720,1280,720,1450),fill=(*WHITE,210),width=12)
    card(d,(200,1490,1240,1770),CYAN)
    for i in range(5): d.line((390,1570+i*35,1050-i*40,1570+i*35),fill=(*WHITE,155),width=8)
    lower(d); return im


def scene4():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),470,VIOLET,42)
    card(d,(140,820,1300,1150),TEAL)
    d.line((300,1030,1140,1030),fill=(*WHITE,200),width=12)
    for x in (360,610,860,1110): d.ellipse((x-28,1002,x+28,1058),fill=(*TEAL,220),outline=(*WHITE,170),width=5)
    card(d,(140,1240,600,1590),AMBER); card(d,(840,1240,1300,1590),RED)
    for i in range(4): d.line((220,1330+i*50,510,1330+i*50),fill=(*WHITE,160),width=9)
    d.line((930,1320,1210,1510),fill=(*RED,220),width=18); d.line((1210,1320,930,1510),fill=(*RED,220),width=18)
    card(d,(260,1660,1180,1770),CYAN)
    d.line((480,1715,960,1715),fill=(*WHITE,210),width=12)
    lower(d); return im


for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
    path=OUT/f'reel_0018_scene_{i:02d}.png'; fn().save(path,optimize=True); print(path)
