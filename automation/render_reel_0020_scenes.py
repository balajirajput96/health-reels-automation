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
    card(d,(110,800,650,1320),TEAL); card(d,(790,800,1330,1320),AMBER)
    # brain and glucose tracer
    d.ellipse((205,930,555,1170),outline=(*TEAL,220),width=14)
    d.line((290,980,470,1110),fill=(*TEAL,180),width=10); d.line((470,980,290,1110),fill=(*TEAL,180),width=10)
    for x,y in [(270,1010),(350,950),(450,1040),(360,1130)]: d.ellipse((x-22,y-22,x+22,y+22),fill=(*CYAN,220),outline=(*WHITE,160),width=4)
    for x,y in [(930,940),(1030,1020),(1130,930),(1210,1080),(1010,1160)]:
        d.ellipse((x-23,y-23,x+23,y+23),fill=(*AMBER,220),outline=(*WHITE,160),width=4)
        d.line((x+20,y+20,x+70,y+70),fill=(*WHITE,140),width=6)
    d.line((720,1370,720,1530),fill=(*WHITE,210),width=12)
    card(d,(250,1580,1190,1770),VIOLET)
    d.line((390,1690,1050,1690),fill=(*WHITE,180),width=12)
    for x,c in [(430,TEAL),(620,CYAN),(820,AMBER),(1020,VIOLET)]: d.ellipse((x-23,1667,x+23,1713),fill=(*c,220))
    lower(d); return im


def scene2():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,CYAN,42)
    card(d,(120,800,1320,1170),CYAN)
    # vessel and hemoglobin
    d.rounded_rectangle((250,925,1190,1045),radius=60,fill=(100,35,60,210),outline=(*RED,180),width=8)
    for x,c in [(410,RED),(570,AMBER),(730,RED),(890,AMBER),(1050,RED)]: d.ellipse((x-34,945,x+34,1015),fill=(*c,220),outline=(*WHITE,120),width=4)
    wave(d,220,1320,400,3,50,RED); wave(d,820,1320,400,3,50,CYAN)
    card(d,(130,1240,620,1590),RED); card(d,(820,1240,1310,1590),CYAN)
    d.line((720,1175,720,1210),fill=(*WHITE,210),width=10)
    card(d,(280,1660,1160,1770),AMBER)
    d.line((480,1715,960,1715),fill=(*WHITE,205),width=12)
    lower(d); return im


def scene3():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),480,AMBER,42)
    card(d,(100,800,410,1260),AMBER); card(d,(515,800,845,1260),TEAL); card(d,(950,800,1350,1260),VIOLET)
    # MRS peaks, isotope tags, microdialysis
    for i,h in enumerate([110,210,145,250]):
        x=155+i*54; d.rounded_rectangle((x,1160-h,x+32,1160),radius=8,fill=(*AMBER,210))
    wave(d,570,1010,220,3,45,TEAL)
    d.line((1040,930,1220,1120),fill=(*VIOLET,210),width=10)
    d.ellipse((1008,900,1072,964),fill=(*WHITE,210)); d.ellipse((1185,1085,1249,1149),fill=(*VIOLET,220))
    d.line((720,1320,720,1460),fill=(*WHITE,210),width=12)
    card(d,(160,1500,1280,1770),CYAN)
    pts=[(360,1640),(560,1550),(760,1680),(960,1560),(1130,1650)]
    network(d,pts,[(0,1),(1,2),(2,3),(3,4),(0,2),(2,4)],[CYAN,TEAL,VIOLET])
    lower(d); return im


def scene4():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),470,VIOLET,42)
    card(d,(160,800,1280,1150),TEAL)
    d.line((310,1020,1130,1020),fill=(*WHITE,200),width=12)
    for x,c in [(360,TEAL),(560,CYAN),(760,AMBER),(960,VIOLET),(1120,RED)]: d.ellipse((x-28,992,x+28,1048),fill=(*c,220),outline=(*WHITE,170),width=5)
    card(d,(110,1270,620,1600),AMBER); card(d,(820,1270,1330,1600),RED)
    d.line((210,1360,510,1360),fill=(*WHITE,160),width=9); d.line((210,1410,510,1410),fill=(*WHITE,160),width=9); d.line((210,1460,510,1460),fill=(*WHITE,160),width=9)
    d.line((920,1340,1230,1530),fill=(*RED,220),width=18); d.line((1230,1340,920,1530),fill=(*RED,220),width=18)
    card(d,(260,1670,1180,1770),CYAN)
    d.line((480,1720,960,1720),fill=(*WHITE,210),width=12)
    lower(d); return im


for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
    path=OUT/f'reel_0020_scene_{i:02d}.png'; fn().save(path,optimize=True); print(path)
