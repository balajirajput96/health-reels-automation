from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(7,15,36); TEAL=(57,220,194); CYAN=(93,177,244); AMBER=(249,184,77); VIOLET=(163,124,239); WHITE=(229,241,252); RED=(241,105,119)
def gradient():
    im=Image.new('RGB',(W,H),BG); px=im.load()
    for y in range(H):
        t=y/(H-1)
        for x in range(W):
            g=max(0,1-math.hypot(x-W*.5,y-H*.28)/(W*.95))
            px[x,y]=(min(255,int(7+10*t+8*g)),min(255,int(15+18*t+19*g)),min(255,int(36+37*t+28*g)))
    return im
def glow(im,center,radius,color,alpha=70):
    l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); x,y=center; d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(*color,alpha)); l=l.filter(ImageFilter.GaussianBlur(radius*.55)); im.paste(l,(0,0),l)
def card(d,b,o,fill=(17,38,69,242),width=7): d.rounded_rectangle(b,radius=40,fill=fill,outline=(*o,220),width=width)
def wave(d,x0,y0,width,cycles,amp,color):
    pts=[]
    for i in range(180):
        t=i/179; pts.append((x0+width*t,y0+amp*math.sin(t*math.tau*cycles)+20*math.sin(t*math.tau*cycles*3.1)))
    d.line(pts,fill=(*color,225),width=10)
def lower(d): d.rounded_rectangle((82,1830,1358,2460),radius=60,fill=(4,10,27,140))
def scene1():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,TEAL,42)
    card(d,(120,800,650,1320),TEAL); card(d,(790,800,1330,1320),CYAN)
    d.ellipse((220,930,550,1170),outline=(*TEAL,220),width=14); d.ellipse((348,1020,422,1094),fill=(*TEAL,220))
    for x,y in [(270,980),(450,980),(300,1120),(480,1110)]: d.ellipse((x-20,y-20,x+20,y+20),fill=(*CYAN,220))
    wave(d,860,1030,320,4,45,CYAN); d.line((720,1370,720,1510),fill=(*WHITE,210),width=12)
    card(d,(260,1570,1180,1770),AMBER); d.line((410,1670,1030,1670),fill=(*WHITE,180),width=12)
    for x,c in [(470,TEAL),(650,CYAN),(830,AMBER),(1010,VIOLET)]: d.ellipse((x-24,1646,x+24,1694),fill=(*c,220))
    lower(d); return im
def scene2():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,AMBER,42)
    card(d,(110,800,1330,1140),CYAN); d.rounded_rectangle((250,920,1190,1040),radius=40,fill=(11,25,50,210),outline=(*CYAN,180),width=7)
    for x in [330,470,610,750,890,1030]: d.rectangle((x,955,x+45,1005),fill=(*VIOLET,200))
    d.line((720,1170,720,1300),fill=(*WHITE,210),width=12)
    card(d,(120,1360,620,1710),TEAL); card(d,(820,1360,1320,1710),RED)
    d.line((205,1460,510,1460),fill=(*WHITE,170),width=9); d.line((205,1510,510,1510),fill=(*WHITE,170),width=9); d.line((920,1430,1230,1620),fill=(*RED,220),width=18); d.line((1230,1430,920,1620),fill=(*RED,220),width=18)
    lower(d); return im
def scene3():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),470,VIOLET,42)
    card(d,(110,800,1330,1160),VIOLET); d.ellipse((270,910,420,1060),outline=(*TEAL,220),width=10); d.ellipse((315,955,375,1015),fill=(*TEAL,220))
    wave(d,570,1000,260,4,35,CYAN); d.line((1000,900,1160,1100),fill=(*AMBER,210),width=10); d.ellipse((980,880,1040,940),fill=(*AMBER,220))
    d.line((720,1190,720,1360),fill=(*WHITE,210),width=12); card(d,(220,1410,1220,1760),CYAN)
    for i,(x,y,c) in enumerate([(400,1590,TEAL),(600,1500,VIOLET),(800,1640,AMBER),(1030,1530,CYAN)]): d.ellipse((x-28,y-28,x+28,y+28),fill=(*c,220),outline=(*WHITE,160),width=5)
    d.line((428,1578,572,1512),fill=(*WHITE,140),width=7); d.line((628,1516,772,1625),fill=(*WHITE,140),width=7); d.line((828,1620,1002,1545),fill=(*WHITE,140),width=7)
    lower(d); return im
def scene4():
    im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),470,RED,42)
    card(d,(160,800,1280,1140),TEAL); d.line((320,1010,1120,1010),fill=(*WHITE,200),width=12)
    for x,c in [(370,TEAL),(560,CYAN),(760,AMBER),(960,VIOLET),(1120,RED)]: d.ellipse((x-28,982,x+28,1038),fill=(*c,220),outline=(*WHITE,170),width=5)
    card(d,(110,1270,620,1600),AMBER); card(d,(820,1270,1330,1600),RED)
    d.line((205,1350,510,1510),fill=(*WHITE,155),width=9); d.line((510,1350,205,1510),fill=(*WHITE,155),width=9); d.line((920,1340,1230,1530),fill=(*RED,220),width=18); d.line((1230,1340,920,1530),fill=(*RED,220),width=18)
    card(d,(260,1670,1180,1770),CYAN); d.line((480,1720,960,1720),fill=(*WHITE,210),width=12); lower(d); return im
for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
    p=OUT/f'reel_0022_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
