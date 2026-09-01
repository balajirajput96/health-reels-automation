from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(8,13,34); WHITE=(241,247,252); CYAN=(75,187,245); TEAL=(57,221,183); AMBER=(247,187,74); VIOLET=(166,127,244); ROSE=(240,106,132)

def base():
    im=Image.new('RGB',(W,H),BG); px=im.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.2)/(W*1.05))
            px[x,y]=(int(8+12*t+8*g),int(13+17*t+15*g),int(34+30*t+26*g))
    return im

def glow(im,x,y,r,c,a=64):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); lay=lay.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(lay,(0,0),lay)

def card(d,box,c): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))
def check(d,x,y,c):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
    d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)

def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,CYAN); card(d,(100,720,1340,1490),CYAN)
    d.rounded_rectangle((170,850,620,1320),radius=38,fill=(*ROSE,90),outline=(*WHITE,140),width=6)
    d.rounded_rectangle((820,850,1270,1320),radius=38,fill=(*TEAL,90),outline=(*WHITE,140),width=6)
    for x in (270,390,510):
        for y in (980,1100,1220): dot(d,x,y,AMBER,22)
    for x,y,c in ((900,930,CYAN),(1080,1110,VIOLET),(900,1290,TEAL),(1160,950,AMBER),(1060,1270,ROSE)): dot(d,x,y,c,22)
    d.line((680,850,680,1320),fill=(*WHITE,150),width=9); footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,TEAL); card(d,(100,720,1340,1490),TEAL)
    d.line((220,1130,1220,1130),fill=(*WHITE,150),width=10)
    for x,c in ((280,AMBER),(500,CYAN),(720,TEAL),(940,VIOLET),(1160,ROSE)): dot(d,x,1130,c,28)
    d.line((280,920,280,1130),fill=(*AMBER,180),width=10); d.line((1160,870,1160,1130),fill=(*ROSE,180),width=10)
    d.rounded_rectangle((175,810,445,925),radius=20,fill=(*AMBER,110),outline=(*WHITE,140),width=5)
    d.rounded_rectangle((985,760,1270,875),radius=20,fill=(*ROSE,110),outline=(*WHITE,140),width=5)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,AMBER); card(d,(100,720,1340,1490),AMBER)
    d.line((230,1280,1210,1280),fill=(*WHITE,150),width=9); d.line((260,1260,470,1090,700,1160,920,890,1160,980),fill=(*CYAN,210),width=14)
    for x,y,c in ((470,1090,CYAN),(700,1160,TEAL),(920,890,VIOLET),(1160,980,ROSE)): dot(d,x,y,c,28)
    d.line((330,900,330,1370),fill=(*WHITE,110),width=6); d.line((330,1370,1180,1370),fill=(*WHITE,110),width=6)
    footer(d); return im

def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    d.line((720,840,720,980),fill=(*WHITE,170),width=9)
    for x,c in ((300,CYAN),(570,TEAL),(840,AMBER),(1110,ROSE)):
        d.line((720,980,x,1160),fill=(*WHITE,150),width=8); dot(d,x,1160,c,27)
    for y,c in ((1900,TEAL),(2070,AMBER),(2240,ROSE)):
        check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
    return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0049_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
