from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(7,14,35); WHITE=(235,244,252); TEAL=(61,220,194); CYAN=(93,177,244); AMBER=(249,184,77); VIOLET=(163,124,239); RED=(241,105,119)

def base():
    im=Image.new('RGB',(W,H),BG); px=im.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.24)/(W*.97))
            px[x,y]=(int(7+10*t+8*g),int(14+18*t+18*g),int(35+38*t+28*g))
    return im

def glow(im,x,y,r,c,a=64):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); layer=layer.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(layer,(0,0),layer)

def card(d,box,color): d.rounded_rectangle(box,radius=42,fill=(16,38,69,242),outline=(*color,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,9,25,145))
def dot(d,x,y,c,r=20): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))

def check(d,x,y,c):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
    d.line((x-27,y+2,x-4,y+25),fill=(*BG,230),width=13); d.line((x-4,y+25,x+34,y-30),fill=(*BG,230),width=13)

def person(d,x,y,c,scale=.8):
    d.ellipse((x-62*scale,y-190*scale,x+62*scale,y-66*scale),fill=(*c,215),outline=(*WHITE,150),width=7)
    d.rounded_rectangle((x-100*scale,y-40*scale,x+100*scale,y+185*scale),radius=55,fill=(*c,175),outline=(*WHITE,140),width=7)

def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    # broad goal arrow and specific if-then link
    d.ellipse((250,900,530,1180),outline=(*CYAN,210),width=12); d.line((330,1040,450,1040),fill=(*WHITE,220),width=10); d.polygon((450,1040,408,1015,408,1065),fill=(*WHITE,220))
    d.rounded_rectangle((650,850,1180,1150),radius=32,fill=(8,20,46,230),outline=(*TEAL,220),width=7)
    d.ellipse((730,960,810,1040),fill=(*AMBER,220)); d.line((830,1000,1010,1000),fill=(*WHITE,210),width=10); d.polygon((1010,1000,970,975,970,1025),fill=(*WHITE,220)); d.rounded_rectangle((1040,950,1120,1050),radius=18,fill=(*TEAL,220))
    for x in [250,330,410,490,650,730,810,890,970,1050,1130]: dot(d,x,1290,CYAN if x<600 else TEAL,12)
    footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,CYAN); card(d,(100,720,1340,1490),CYAN)
    # ladder of measurements
    cols=[VIOLET,AMBER,TEAL,RED,WHITE]; labels_y=[870,980,1090,1200,1310]
    for y,c in zip(labels_y,cols):
        d.rounded_rectangle((230,y,1210,y+62),radius=26,fill=(*c,180),outline=(*WHITE,160),width=4)
        d.ellipse((280,y+12,310,y+42),fill=(*WHITE,220))
        for x in range(360,1160,110): d.line((x,y+31,x+55,y+31),fill=(*WHITE,150),width=7)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,AMBER); card(d,(100,720,1340,1490),AMBER)
    # study panels converge, but moderator branches remain visible
    for i,(x,y,c) in enumerate([(220,850,CYAN),(560,850,TEAL),(900,850,VIOLET),(220,1190,RED),(560,1190,WHITE),(900,1190,AMBER)]):
        d.rounded_rectangle((x,y,x+300,y+190),radius=25,fill=(8,20,46,230),outline=(*c,200),width=6)
        for k in range(3):
            d.line((x+45,y+60+k*35,x+250,y+60+k*35),fill=(*c,180),width=6)
        d.ellipse((x+130,y+130,x+170,y+170),fill=(*c,220))
    d.line((520,1000,720,1090),fill=(*WHITE,170),width=9); d.line((900,1000,720,1090),fill=(*WHITE,170),width=9); d.line((520,1280,720,1090),fill=(*WHITE,170),width=9); d.line((900,1280,720,1090),fill=(*WHITE,170),width=9)
    d.ellipse((660,1030,780,1150),fill=(*TEAL,190),outline=(*WHITE,220),width=8)
    # moderators strip
    d.rounded_rectangle((230,1400,1210,1460),radius=22,fill=(*RED,150));
    for x,c in [(310,CYAN),(520,TEAL),(730,AMBER),(940,VIOLET),(1150,WHITE)]: dot(d,x,1430,c,13)
    footer(d); return im

def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,RED); card(d,(100,720,1340,1490),RED)
    xs=[270,470,670,870,1070,1270]
    for x,c in zip(xs,[CYAN,TEAL,AMBER,VIOLET,RED,WHITE]): check(d,x,1000,c)
    d.line((320,1000,1220,1000),fill=(*WHITE,165),width=9)
    d.rounded_rectangle((220,1200,1220,1390),radius=30,fill=(8,20,46,220),outline=(*TEAL,190),width=6)
    for y in [1250,1310,1370]: d.line((330,y,1110,y),fill=(*WHITE,150),width=8)
    footer(d); return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0037_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
