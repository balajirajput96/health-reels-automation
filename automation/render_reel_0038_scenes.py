from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H = 1440, 2560
OUT = Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(6,13,34); WHITE=(235,244,252); TEAL=(61,220,194); CYAN=(93,177,244); AMBER=(249,184,77); VIOLET=(163,124,239); RED=(241,105,119)

def base():
    im=Image.new('RGB',(W,H),BG); px=im.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.24)/(W*.97))
            px[x,y]=(int(6+10*t+8*g),int(13+18*t+18*g),int(34+38*t+28*g))
    return im

def glow(im,x,y,r,c,a=62):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); layer=layer.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(layer,(0,0),layer)

def card(d,box,color): d.rounded_rectangle(box,radius=42,fill=(15,37,68,242),outline=(*color,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,9,25,145))
def dot(d,x,y,c,r=20): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))
def check(d,x,y,c):
    d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
    d.line((x-27,y+2,x-4,y+25),fill=(*BG,230),width=13); d.line((x-4,y+25,x+34,y-30),fill=(*BG,230),width=13)

def s1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,CYAN); card(d,(100,720,1340,1490),CYAN)
    # several cues approach an attention gate
    gate=(670,850,760,1370); d.rounded_rectangle(gate,radius=30,fill=(*TEAL,155),outline=(*WHITE,190),width=8)
    for i,(x,y,c) in enumerate([(250,870,AMBER),(250,1050,VIOLET),(250,1230,RED)]):
        d.ellipse((x-55,y-55,x+55,y+55),fill=(*c,220)); d.line((x+70,y,640,y),fill=(*WHITE,180),width=9); d.polygon((640,y,600,y-24,600,y+24),fill=(*WHITE,220))
    d.line((810,1110,1120,1110),fill=(*WHITE,180),width=10); d.polygon((1120,1110,1075,1084,1075,1136),fill=(*WHITE,220)); d.ellipse((1140,1050,1245,1170),fill=(*AMBER,210),outline=(*WHITE,180),width=7)
    footer(d); return im

def s2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,VIOLET); card(d,(100,720,1340,1490),VIOLET)
    # prospective vs retrospective split
    d.rounded_rectangle((190,850,620,1320),radius=32,fill=(8,20,46,230),outline=(*CYAN,220),width=7)
    d.rounded_rectangle((820,850,1250,1320),radius=32,fill=(8,20,46,230),outline=(*AMBER,220),width=7)
    for y in [950,1040,1130]: d.line((280,y,530,y),fill=(*CYAN,180),width=9)
    for y in [950,1040,1130]: d.line((910,y,1160,y),fill=(*AMBER,180),width=9)
    d.line((650,1085,790,1085),fill=(*WHITE,190),width=10); d.polygon((790,1085,750,1060,750,1110),fill=(*WHITE,220))
    for x,c in [(280,CYAN),(420,TEAL),(910,AMBER),(1050,RED)]: dot(d,x,1240,c,18)
    footer(d); return im

def s3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,AMBER); card(d,(100,720,1340,1490),AMBER)
    # two separate performance traces
    d.rounded_rectangle((190,850,1250,1320),radius=30,fill=(8,20,46,230),outline=(*WHITE,160),width=5)
    d.line((280,1200,450,1150,600,1170,760,1000,900,940,1080,890,1190,850),fill=(*TEAL,230),width=14)
    d.line((280,1000,450,1030,600,1070,760,1120,900,1180,1080,1160,1190,1210),fill=(*RED,220),width=12)
    for x,y,c in [(450,1150,TEAL),(760,1000,TEAL),(1080,890,TEAL),(600,1070,RED),(900,1180,RED),(1190,1210,RED)]: dot(d,x,y,c,17)
    footer(d); return im

def s4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,520,RED); card(d,(100,720,1340,1490),RED)
    # lab to ecology chain with blocked transfer edge
    xs=[250,520,790,1060]
    for x,c in zip(xs,[CYAN,TEAL,AMBER,VIOLET]):
        d.rounded_rectangle((x-105,900,x+105,1110),radius=28,fill=(*c,185),outline=(*WHITE,190),width=6)
        d.line((x-55,1010,x+55,1010),fill=(*WHITE,200),width=9)
    for x in [355,625,895]:
        d.line((x,1005,x+60,1005),fill=(*WHITE,180),width=9); d.polygon((x+60,1005,x+25,980,x+25,1030),fill=(*WHITE,220))
    d.line((895,1190,1060,1190),fill=(*RED,220),width=12); d.line((895,1190,1060,1260),fill=(*RED,120),width=7)
    for y in [1200,1280,1360]: d.line((260,y,1180,y),fill=(*WHITE,150),width=8)
    footer(d); return im

for i,fn in enumerate((s1,s2,s3,s4),1):
    p=OUT/f'reel_0038_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
