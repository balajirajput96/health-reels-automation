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
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,AMBER); card(d,(100,720,1340,1490),AMBER)
    d.line((220,1260,1180,900),fill=(*CYAN,220),width=16)
    for x,y,c in ((250,1245,ROSE),(480,1155,AMBER),(720,1065,VIOLET),(960,975,TEAL),(1180,890,CYAN)): dot(d,x,y,c,28)
    for x in range(250,1200,180): d.line((x,1330,x+90,1150),fill=(*WHITE,120),width=7)
    footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,CYAN); card(d,(100,720,1340,1490),CYAN)
    labels=[(210,880,490,1050,CYAN),(560,880,840,1050,AMBER),(910,880,1230,1050,TEAL),(210,1130,490,1300,VIOLET),(560,1130,840,1300,ROSE),(910,1130,1230,1300,CYAN)]
    for x1,y1,x2,y2,c in labels: d.rounded_rectangle((x1,y1,x2,y2),radius=24,fill=(*c,115),outline=(*WHITE,155),width=5)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,TEAL); card(d,(100,720,1340,1490),TEAL)
    d.line((220,1280,1220,1280),fill=(*WHITE,150),width=9); d.line((260,1210,520,1090,780,1140,1030,900,1190,980),fill=(*AMBER,215),width=14)
    for x,y,c in ((520,1090,CYAN),(780,1140,TEAL),(1030,900,VIOLET),(1190,980,ROSE)): dot(d,x,y,c,28)
    d.line((330,900,330,1370),fill=(*WHITE,110),width=6); d.line((330,1370,1180,1370),fill=(*WHITE,110),width=6)
    footer(d); return im

def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,540,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    d.line((720,850,720,1030),fill=(*WHITE,170),width=9)
    for x,c in ((300,CYAN),(570,TEAL),(840,AMBER),(1110,ROSE)):
        d.line((720,1030,x,1190),fill=(*WHITE,150),width=8); dot(d,x,1190,c,27)
    for y,c in ((1900,TEAL),(2070,AMBER),(2240,ROSE)):
        check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
    return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0050_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
