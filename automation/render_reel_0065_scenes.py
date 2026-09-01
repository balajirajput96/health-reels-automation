from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(8,17,41); WHITE=(244,247,252); CYAN=(72,210,255); TEAL=(64,222,177); AMBER=(249,185,68); VIOLET=(171,139,244); ROSE=(237,103,145)

def base():
    im=Image.new('RGB',(W,H),BG); p=im.load()
    for y in range(H):
        t=y/(H-1); c=(int(8+13*t),int(17+17*t),int(41+23*t))
        for x in range(W): p[x,y]=c
    return im

def glow(im,x,y,r,c):
    q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,62)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)

def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(16,38,74,235),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def pill(d,b,text,c): d.rounded_rectangle(b,radius=28,fill=(*c,150),outline=(*WHITE,150),width=4)
def node(d,x,y,c,r=30): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,155),width=4)

def scene1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,CYAN); card(d,(80,700,1360,1515),CYAN)
    # alternating trial cards
    for i,(y,label,c) in enumerate([(855,'REPEAT',TEAL),(1095,'SWITCH',AMBER)]):
        d.rounded_rectangle((170,y,1270,y+150),radius=28,fill=(6,22,50,220),outline=(*c,210),width=6)
        d.line((250,y+75,520,y+75),fill=(*c,220),width=12); d.line((760,y+75,1190,y+75),fill=(*c,220),width=12)
        d.ellipse((565,y+37,635,y+107),fill=(*c,220)); d.ellipse((665,y+37,735,y+107),fill=(*WHITE,210))
    footer(d); return im

def scene2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,AMBER); card(d,(80,700,1360,1515),AMBER)
    d.line((190,1100,1250,1100),fill=(*WHITE,190),width=9)
    for x,c,label in [(300,CYAN,'cue'),(610,TEAL,'prepare'),(880,AMBER,'switch'),(1150,ROSE,'residual')]:
        node(d,x,1100,c,34); d.rounded_rectangle((x-85,1210,x+85,1295),radius=20,fill=(*c,130),outline=(*WHITE,130),width=3)
    d.line((300,1010,610,1010),fill=(*CYAN,180),width=8); d.line((610,1010,880,1010),fill=(*TEAL,180),width=8)
    footer(d); return im

def scene3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(85,700,1355,1530),ROSE)
    center=(720,1100); node(d,*center,VIOLET,44)
    pts=[(300,900,CYAN),(300,1300,AMBER),(1140,900,TEAL),(1140,1300,ROSE)]
    for x,y,c in pts:
        node(d,x,y,c,34); d.line((x,y,center[0],center[1]),fill=(*c,180),width=9)
    footer(d); return im

def scene4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(90,700,1350,1530),VIOLET)
    for i,(x,h,c) in enumerate([(250,250,CYAN),(500,370,AMBER),(750,300,TEAL),(1000,430,ROSE)]):
        d.rounded_rectangle((x,1310-h,x+170,1310),radius=22,fill=(*c,200),outline=(*WHITE,145),width=5)
    d.line((180,1310,1240,1310),fill=(*WHITE,190),width=8)
    footer(d); return im

for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
    p=OUT/f'reel_0065_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
