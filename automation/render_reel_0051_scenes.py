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

def glow(im,x,y,r,c,a=62):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); lay=lay.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(lay,(0,0),lay)

def card(d,box,c): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))
def check(d,x,y,c):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
    d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)

def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,CYAN); card(d,(100,720,1340,1490),CYAN)
    d.line((210,1040,1190,1040),fill=(*WHITE,140),width=10)
    d.line((310,900,310,1190),fill=(*AMBER,220),width=18); d.line((870,900,870,1190),fill=(*TEAL,220),width=18)
    for x,c in ((310,AMBER),(870,TEAL)): dot(d,x,1040,c,30)
    d.line((310,1240,870,1240),fill=(*VIOLET,200),width=12)
    footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,TEAL); card(d,(100,720,1340,1490),TEAL)
    boxes=[(180,880,520,1080,CYAN),(550,880,900,1080,AMBER),(930,880,1260,1080,VIOLET),(365,1160,715,1360,TEAL),(745,1160,1095,1360,ROSE)]
    for x1,y1,x2,y2,c in boxes: d.rounded_rectangle((x1,y1,x2,y2),radius=28,fill=(*c,125),outline=(*WHITE,160),width=5)
    for x,y in ((520,980),(930,980),(715,1260)): d.line((x,y,x+30,y+25),fill=(*WHITE,170),width=8)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,AMBER)
    card(d,(110,720,650,1490),AMBER); card(d,(790,720,1330,1490),CYAN)
    d.line((220,950,540,950),fill=(*WHITE,150),width=9); d.line((260,1070,500,860),fill=(*TEAL,220),width=14)
    d.line((900,950,1220,950),fill=(*WHITE,150),width=9); d.line((940,1070,1180,820),fill=(*ROSE,220),width=14)
    footer(d); return im

def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    d.line((720,850,720,1030),fill=(*WHITE,170),width=9)
    for x,c in ((275,CYAN),(560,TEAL),(845,AMBER),(1130,ROSE)):
        d.line((720,1030,x,1190),fill=(*WHITE,150),width=8); dot(d,x,1190,c,27)
    for y,c in ((1900,TEAL),(2070,AMBER),(2240,ROSE)):
        check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
    return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0051_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
