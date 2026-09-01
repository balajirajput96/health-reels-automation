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
    card(d,(120,800,630,1320),TEAL); card(d,(810,800,1320,1320),AMBER)
    # astrocyte-like star and microglia-like ramified cell
    cx,cy=370,1050
    for a in range(0,360,30):
        x2=cx+230*math.cos(math.radians(a)); y2=cy+230*math.sin(math.radians(a))
        d.line((cx,cy,x2,y2),fill=(*TEAL,220),width=14)
        d.ellipse((x2-16,y2-16,x2+16,y2+16),fill=(*WHITE,190))
    d.ellipse((cx-45,cy-45,cx+45,cy+45),fill=(*CYAN,220),outline=(*WHITE,180),width=6)
    cx,cy=1065,1050
    for a in range(0,360,45):
        x2=cx+200*math.cos(math.radians(a)); y2=cy+150*math.sin(math.radians(a))
        d.line((cx,cy,x2,y2),fill=(*AMBER,220),width=13)
        d.ellipse((x2-15,y2-15,x2+15,y2+15),fill=(*WHITE,180))
    d.ellipse((cx-40,cy-40,cx+40,cy+40),fill=(*VIOLET,220),outline=(*WHITE,180),width=6)
    d.line((720,1370,720,1530),fill=(*WHITE,210),width=12)
    card(d,(260,1570,1180,1770),RED)
    for i in range(4): d.line((420,1630+i*28,1030,1630+i*28),fill=(*WHITE,160),width=8)
    lower(d); return im


def scene2():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,CYAN,42)
    card(d,(100,790,430,1260),CYAN); card(d,(555,790,885,1260),TEAL); card(d,(1010,790,1340,1260),AMBER)
    # model systems
    d.ellipse((145,930,385,1090),outline=(*CYAN,230),width=12)
    d.line((190,1020,340,1020),fill=(*WHITE,160),width=7)
    wave(d,600,1040,220,3,45,TEAL)
    for x in (1070,1140,1210): d.ellipse((x-30,1000,x+30,1060),fill=(*AMBER,210),outline=(*WHITE,160),width=5)
    d.line((720,1320,720,1480),fill=(*WHITE,210),width=12)
    card(d,(180,1520,1260,1770),VIOLET)
    pts=[(390,1650),(580,1580),(770,1690),(960,1580),(1120,1660)]
    network(d,pts,[(0,1),(1,2),(2,3),(3,4),(0,2),(2,4)],[VIOLET,TEAL,CYAN])
    lower(d); return im


def scene3():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),480,AMBER,42)
    card(d,(90,800,410,1260),AMBER); card(d,(515,800,845,1260),TEAL); card(d,(950,800,1350,1260),VIOLET)
    # omics symbols
    for i in range(5):
        d.line((150,920+i*52,350,920+i*52),fill=(*AMBER,190),width=10)
        d.ellipse((220+i*24,900+i*52,250+i*24,930+i*52),fill=(*WHITE,180))
    # tissue and PET tracer dots
    d.rounded_rectangle((590,950,770,1100),radius=20,outline=(*TEAL,220),width=10)
    for x,y in [(620,985),(690,1015),(735,1060),(650,1080)]: d.ellipse((x-16,y-16,x+16,y+16),fill=(*TEAL,220))
    for x,y in [(1020,940),(1110,1020),(1200,930),(1260,1090),(1080,1140)]: d.ellipse((x-20,y-20,x+20,y+20),fill=(*VIOLET,220),outline=(*WHITE,150),width=4)
    d.line((720,1320,720,1460),fill=(*WHITE,210),width=12)
    card(d,(160,1500,1280,1770),CYAN)
    for i,h in enumerate([90,150,120,190,135]):
        x=360+i*110; d.rounded_rectangle((x,1690-h,x+52,1690),radius=10,fill=(*CYAN,210))
    lower(d); return im


def scene4():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),470,VIOLET,42)
    card(d,(180,800,1260,1150),TEAL)
    d.line((350,1020,1090,1020),fill=(*WHITE,200),width=12)
    for x,c in [(400,TEAL),(600,CYAN),(800,AMBER),(1000,VIOLET)]: d.ellipse((x-28,992,x+28,1048),fill=(*c,220),outline=(*WHITE,170),width=5)
    card(d,(120,1270,610,1600),AMBER); card(d,(830,1270,1320,1600),RED)
    for i in range(4): d.line((210,1360+i*48,510,1360+i*48),fill=(*WHITE,160),width=9)
    d.line((930,1350,1230,1520),fill=(*RED,220),width=18); d.line((1230,1350,930,1520),fill=(*RED,220),width=18)
    card(d,(280,1670,1160,1770),CYAN)
    d.line((480,1720,960,1720),fill=(*WHITE,210),width=12)
    lower(d); return im


for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
    path=OUT/f'reel_0019_scene_{i:02d}.png'; fn().save(path,optimize=True); print(path)
