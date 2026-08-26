from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(9,18,42); WHITE=(244,247,252); CYAN=(74,211,255); TEAL=(69,224,180); AMBER=(250,190,74); VIOLET=(173,142,246); ROSE=(239,111,149)

def base():
    im=Image.new('RGB',(W,H),BG); p=im.load()
    for y in range(H):
        t=y/(H-1); c=(int(9+12*t),int(18+17*t),int(42+24*t))
        for x in range(W): p[x,y]=c
    return im

def glow(im,x,y,r,c):
    q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,64)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)

def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(16,38,74,235),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=24): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)

def scene1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,CYAN); card(d,(80,700,1360,1515),CYAN)
    d.rounded_rectangle((170,875,1270,1315),radius=34,fill=(6,22,50,220),outline=(*WHITE,150),width=5)
    for x,c in [(250,WHITE),(410,WHITE),(570,AMBER),(730,WHITE),(890,TEAL),(1050,WHITE),(1210,WHITE)]:
        d.rounded_rectangle((x-45,990,x+45,1190),radius=18,fill=(*c,190),outline=(*WHITE,130),width=4)
    d.ellipse((625,790,815,980),fill=(*ROSE,215),outline=(*WHITE,180),width=6); d.line((720,980,720,1190),fill=(*ROSE,220),width=9)
    footer(d); return im

def scene2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,AMBER); card(d,(80,700,1360,1515),AMBER)
    d.line((200,1060,1240,1060),fill=(*WHITE,190),width=9)
    for x,c in [(290,CYAN),(500,VIOLET),(720,TEAL),(940,AMBER),(1150,ROSE)]: dot(d,x,1060,c,32)
    for y,c in [(880,CYAN),(1170,TEAL)]: d.rounded_rectangle((330,y,1110,y+90),radius=26,fill=(*c,105),outline=(*WHITE,140),width=5)
    footer(d); return im

def scene3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(85,700,1355,1530),VIOLET)
    bars=[(180,1180,390,CYAN),(480,1050,690,AMBER),(780,1280,990,TEAL),(1080,940,1290,ROSE)]
    for x1,y2,x2,c in bars:
        d.rounded_rectangle((x1,900,x2,1330),radius=28,fill=(7,22,52,220),outline=(*WHITE,120),width=5)
        d.rounded_rectangle((x1+30,y2,x2-30,1300),radius=18,fill=(*c,190))
    footer(d); return im

def scene4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(90,700,1350,1530),ROSE)
    centers=[(290,1030,CYAN),(530,1030,AMBER),(770,1030,VIOLET),(1010,1030,TEAL),(1210,1030,WHITE)]
    for x,y,c in centers: dot(d,x,y,c,48)
    for x1,x2,c in [(338,482,CYAN),(578,722,AMBER),(818,962,VIOLET),(1058,1162,TEAL)]: d.line((x1,1030,x2,1030),fill=(*c,190),width=8)
    d.rounded_rectangle((260,1280,1180,1410),radius=30,fill=(*TEAL,130),outline=(*WHITE,160),width=6)
    footer(d); return im

for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
    p=OUT/f'reel_0064_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
