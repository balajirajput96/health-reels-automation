from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG = (8, 14, 35)
WHITE = (240, 247, 252)
TEAL = (65, 220, 183)
CYAN = (88, 181, 247)
AMBER = (249, 186, 75)
VIOLET = (168, 130, 244)
ROSE = (241, 109, 133)


def base():
    im = Image.new('RGB', (W, H), BG); px = im.load()
    for y in range(H):
        t = y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.22)/(W*1.02))
            px[x,y]=(int(8+11*t+8*g),int(14+18*t+17*g),int(35+34*t+30*g))
    return im


def glow(im,x,y,r,color,alpha=58):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(layer).ellipse((x-r,y-r,x+r,y+r),fill=(*color,alpha)); layer=layer.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(layer,(0,0),layer)


def card(d,box,color): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*color,225),width=7)

def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))

def dot(d,x,y,color,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,232))

def check(d,x,y,color):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*color,210),outline=(*WHITE,220),width=8)
    d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)


def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,530,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    d.ellipse((350,840,790,1280),fill=(*VIOLET,90),outline=(*WHITE,170),width=7)
    d.arc((420,930,720,1190),205,515,fill=(*TEAL,230),width=18)
    for x,y,c in ((250,920,CYAN),(1050,900,AMBER),(1010,1230,TEAL),(280,1260,ROSE)):
        dot(d,x,y,c,30); d.line((x,y,x+(720-x)*.55,y+(1040-y)*.55),fill=(*WHITE,130),width=7)
    d.line((200,1360,1240,1360),fill=(*WHITE,165),width=10)
    for x,c in ((320,CYAN),(590,AMBER),(860,TEAL),(1130,VIOLET)): dot(d,x,1360,c,25)
    footer(d); return im


def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,530,CYAN); card(d,(100,720,1340,1490),CYAN)
    for x,c in ((200,TEAL),(590,AMBER),(980,VIOLET)):
        d.rounded_rectangle((x,850,x+300,1220),radius=30,fill=(*c,100),outline=(*WHITE,165),width=7)
        for k in range(4):
            d.line((x+55,940+k*62,x+245-(k%2)*50,940+k*62),fill=(*WHITE,145),width=9)
    d.line((210,1300,1230,1300),fill=(*WHITE,170),width=10)
    for x in (260,380,500,620,740,860,980,1100): dot(d,x,1300,TEAL if x%240 else AMBER,18)
    footer(d); return im


def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,530,AMBER); card(d,(100,720,1340,1490),AMBER)
    for x,y,c in ((220,900,CYAN),(220,1120,TEAL),(220,1340,VIOLET)):
        dot(d,x,y,c,32); d.line((310,y,1190,y),fill=(*WHITE,160),width=9); d.rounded_rectangle((520,y-48,900,y+48),radius=25,fill=(*c,150),outline=(*WHITE,150),width=5)
    d.line((1010,830,1010,1410),fill=(*WHITE,150),width=8)
    for y,c in ((920,TEAL),(1120,AMBER),(1320,ROSE)): dot(d,1010,y,c,25)
    footer(d); return im


def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,530,TEAL); card(d,(100,720,1340,1490),TEAL)
    d.line((720,850,720,1010),fill=(*WHITE,180),width=10)
    for x,c in ((290,CYAN),(720,AMBER),(1150,VIOLET)):
        d.line((720,1010,x,1160),fill=(*WHITE,155),width=8); dot(d,x,1160,c,28)
    for y,c in ((1900,TEAL),(2070,AMBER),(2230,ROSE)):
        check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,155),width=8)
    return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    path=OUT/f'reel_0046_scene_{i:02d}.png'; fn().save(path,optimize=True); print(path)
