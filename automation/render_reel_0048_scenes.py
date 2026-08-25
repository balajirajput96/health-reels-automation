from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(7,14,35); WHITE=(240,247,252); CYAN=(78,185,247); TEAL=(58,219,181); AMBER=(249,188,77); VIOLET=(164,127,244); ROSE=(241,108,132)

def base():
    im=Image.new('RGB',(W,H),BG); px=im.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.2)/(W*1.05))
            px[x,y]=(int(7+12*t+8*g),int(14+17*t+16*g),int(35+30*t+28*g))
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
    d.rounded_rectangle((180,850,620,1320),radius=38,fill=(*ROSE,90),outline=(*WHITE,140),width=6)
    d.rounded_rectangle((820,850,1260,1320),radius=38,fill=(*TEAL,90),outline=(*WHITE,140),width=6)
    for x in (270,370,470):
        for y in (980,1100,1220): dot(d,x,y,AMBER,22)
    for x,y in ((900,930),(1080,1110),(900,1290),(1160,950),(1060,1270)): dot(d,x,y,AMBER,22)
    d.line((680,850,680,1320),fill=(*WHITE,150),width=9)
    footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,TEAL); card(d,(100,720,1340,1490),TEAL)
    d.line((250,1130,1190,1130),fill=(*WHITE,150),width=10)
    for x,c in ((300,AMBER),(520,CYAN),(740,TEAL),(960,VIOLET),(1180,ROSE)): dot(d,x,1130,c,28)
    d.line((300,930,300,1130),fill=(*AMBER,180),width=10); d.line((1180,900,1180,1130),fill=(*ROSE,180),width=10)
    d.rounded_rectangle((220,820,420,930),radius=20,fill=(*AMBER,110),outline=(*WHITE,140),width=5)
    d.rounded_rectangle((1030,790,1260,900),radius=20,fill=(*ROSE,110),outline=(*WHITE,140),width=5)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,AMBER); card(d,(100,720,1340,1490),AMBER)
    d.line((230,1280,1210,1280),fill=(*WHITE,150),width=9); d.line((260,1280,480,1040,730,890,930,980,1160,1160),fill=(*CYAN,210),width=14)
    for x,y,c in ((480,1040,CYAN),(730,890,TEAL),(930,980,VIOLET),(1160,1160,ROSE)): dot(d,x,y,c,28)
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
    p=OUT/f'reel_0048_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
