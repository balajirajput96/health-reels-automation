from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (7, 14, 35); WHITE = (235, 244, 252); TEAL = (61, 220, 194)
CYAN = (93, 177, 244); AMBER = (249, 184, 77); VIOLET = (163, 124, 239); RED = (241, 105, 119)


def base():
    im = Image.new('RGB', (W, H), BG); px = im.load()
    for y in range(H):
        t = y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.24)/(W*.97))
            px[x,y]=(int(7+10*t+8*g),int(14+18*t+18*g),int(35+38*t+28*g))
    return im


def glow(im,x,y,r,c,a=64):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); layer=layer.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(layer,(0,0),layer)


def card(d,box,color):
    d.rounded_rectangle(box,radius=42,fill=(16,38,69,242),outline=(*color,225),width=7)


def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,9,25,145))

def dot(d,x,y,c,r=20): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))

def person(d,x,y,c,scale=1.0):
    d.ellipse((x-62*scale,y-190*scale,x+62*scale,y-66*scale),fill=(*c,215),outline=(*WHITE,150),width=7)
    d.rounded_rectangle((x-100*scale,y-40*scale,x+100*scale,y+185*scale),radius=55,fill=(*c,175),outline=(*WHITE,140),width=7)
    d.line((x-82*scale,y+55*scale,x-170*scale,y+135*scale),fill=(*c,220),width=max(6,int(18*scale)))
    d.line((x+82*scale,y+55*scale,x+170*scale,y+135*scale),fill=(*c,220),width=max(6,int(18*scale)))


def check(d,x,y,c):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
    d.line((x-27,y+2,x-4,y+25),fill=(*BG,230),width=13); d.line((x-4,y+25,x+34,y-30),fill=(*BG,230),width=13)


def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,VIOLET)
    card(d,(100,720,1340,1450),VIOLET)
    person(d,430,1000,CYAN,1.0); person(d,1010,1000,TEAL,1.0)
    # timed sender-to-observer signal with separate channels
    d.line((610,980,830,980),fill=(*WHITE,190),width=11); d.polygon((830,980,790,955,790,1005),fill=(*WHITE,210))
    for yy,c in [(820,CYAN),(900,AMBER),(1060,TEAL),(1140,VIOLET)]:
        d.line((585,yy,855,yy),fill=(*c,170),width=8)
        for x in range(610,850,55): dot(d,x,yy,c,10)
    d.ellipse((270,1280,590,1380),outline=(*CYAN,190),width=10)
    d.ellipse((850,1280,1170,1380),outline=(*TEAL,190),width=10)
    footer(d); return im


def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,CYAN)
    card(d,(100,720,1340,1490),CYAN)
    # four distinct instruments: questionnaire, face/EMG, heart, report
    xs=[250,560,870,1180]; cs=[VIOLET,AMBER,RED,TEAL]
    for x,c in zip(xs,cs): card(d,(x-120,860,x+120,1240),c)
    # questionnaire lines
    for y in [930,1000,1070,1140]:
        d.line((175,y,320,y),fill=(*WHITE,190),width=9); dot(d,350,y,c=VIOLET,r=13)
    # facial waveform
    pts=[]
    for i in range(180):
        xx=470+i*1.0; yy=1050+70*math.sin(i*.11)+25*math.sin(i*.31); pts.append((xx,yy))
    d.line(pts,fill=(*WHITE,220),width=8)
    # ECG-like trace
    pts=[]
    for i in range(190):
        xx=780+i*1.0; basey=1050; phase=i%48
        yy=basey-(115 if phase==15 else 45 if phase in (14,16) else 0)
        pts.append((xx,yy))
    d.line(pts,fill=(*WHITE,220),width=8)
    # reported affect dots and scale
    for x in [1080,1125,1170,1215]: dot(d,x,1050,TEAL,18)
    d.line((1060,1150,1280,1150),fill=(*WHITE,180),width=8)
    footer(d); return im


def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,AMBER)
    card(d,(100,720,1340,1490),AMBER)
    # social context: friend and stranger dyads, with positive/neutral/negative conditions
    for x,c in [(310,TEAL),(690,CYAN),(1070,VIOLET)]:
        person(d,x-105,1020,c,.55); person(d,x+105,1020,c,.55)
        d.line((x-45,1000,x+45,1000),fill=(*WHITE,180),width=7)
        for k in range(3): dot(d,x-32+k*32,1140,c,10)
    # context strips: close vs distant and emotion conditions as separate axes
    d.rounded_rectangle((180,1260,1260,1380),radius=28,fill=(8,20,46,220),outline=(*WHITE,150),width=5)
    for x,c in [(270,TEAL),(550,AMBER),(830,RED),(1110,VIOLET)]:
        d.ellipse((x-28,1304-28,x+28,1304+28),fill=(*c,220))
        d.line((x,1335,x,1370),fill=(*WHITE,170),width=6)
    footer(d); return im


def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,RED)
    card(d,(100,720,1340,1490),RED)
    # interpretation checklist: report, behavior, arousal, timing, context, sample
    xs=[210,410,610,810,1010,1210]
    for x,c in zip(xs,[CYAN,TEAL,AMBER,VIOLET,RED,WHITE]): check(d,x,980,c)
    d.line((270,980,1150,980),fill=(*WHITE,165),width=9)
    d.rounded_rectangle((220,1190,1220,1360),radius=30,fill=(8,20,46,220),outline=(*TEAL,190),width=6)
    for y in [1240,1290,1340]:
        d.line((330,y,1110,y),fill=(*WHITE,150),width=8)
    footer(d); return im


for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0036_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
