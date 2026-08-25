from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(7,14,35); WHITE=(240,247,252); TEAL=(66,222,184); CYAN=(86,181,246); AMBER=(249,187,76); VIOLET=(168,130,244); ROSE=(241,108,132)

def base():
    im=Image.new('RGB',(W,H),BG); px=im.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.2)/(W*1.05))
            px[x,y]=(int(7+12*t+8*g),int(14+17*t+16*g),int(35+30*t+28*g))
    return im

def glow(im,x,y,r,color,a=60):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).ellipse((x-r,y-r,x+r,y+r),fill=(*color,a)); lay=lay.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(lay,(0,0),lay)

def card(d,box,color): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*color,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))
def check(d,x,y,c):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
    d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)

def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,CYAN); card(d,(100,720,1340,1490),CYAN)
    d.rounded_rectangle((240,880,1200,1130),radius=38,fill=(*CYAN,92),outline=(*WHITE,170),width=7)
    d.ellipse((330,945,430,1045),fill=(*AMBER,220)); d.line((480,995,1000,995),fill=(*WHITE,190),width=12)
    for x,y,c in ((340,1260,TEAL),(720,1260,AMBER),(1100,1260,VIOLET)): dot(d,x,y,c,30)
    d.line((340,1260,720,1260),fill=(*WHITE,150),width=8); d.line((720,1260,1100,1260),fill=(*WHITE,150),width=8)
    footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,TEAL); card(d,(100,720,1340,1490),TEAL)
    for i,x in enumerate((220,500,780,1060)):
        d.rounded_rectangle((x,870,x+180,1190),radius=28,fill=(*(TEAL if i%2==0 else VIOLET),110),outline=(*WHITE,150),width=6)
        d.ellipse((x+62,930,x+118,986),fill=(*AMBER,220)); d.line((x+48,1040,x+132,1040),fill=(*WHITE,160),width=9); d.line((x+48,1090,x+132,1090),fill=(*WHITE,160),width=9)
    d.line((210,1300,1230,1300),fill=(*WHITE,160),width=10)
    for x in range(270,1160,125): dot(d,x,1300,AMBER if x%250 else ROSE,18)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,AMBER); card(d,(100,720,1340,1490),AMBER)
    d.line((260,1030,1180,1030),fill=(*WHITE,150),width=9)
    for x,c in ((300,CYAN),(570,TEAL),(840,VIOLET),(1110,ROSE)): dot(d,x,1030,c,31)
    for x,label in ((300,0),(570,1),(840,2),(1110,3)):
        d.line((x,1030,x,900),fill=(*WHITE,140),width=7); d.rounded_rectangle((x-80,820,x+80,900),radius=20,fill=(*CYAN,100),outline=(*WHITE,130),width=5)
    d.line((260,1250,1180,1250),fill=(*WHITE,130),width=8); dot(d,360,1250,TEAL,25); dot(d,1080,1250,AMBER,25)
    footer(d); return im

def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    d.line((720,840,720,980),fill=(*WHITE,170),width=9)
    for x,c in ((330,CYAN),(720,TEAL),(1110,AMBER)):
        d.line((720,980,x,1160),fill=(*WHITE,150),width=8); dot(d,x,1160,c,28)
    for y,c in ((1900,TEAL),(2070,AMBER),(2240,ROSE)):
        check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
    return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0047_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
