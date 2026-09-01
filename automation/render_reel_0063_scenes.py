from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(10,18,40); WHITE=(244,247,252); CYAN=(79,208,255); TEAL=(57,220,176); AMBER=(248,191,76); VIOLET=(173,139,246); ROSE=(239,111,149)

def base():
    im=Image.new('RGB',(W,H),BG)
    p=im.load()
    for y in range(H):
        t=y/(H-1)
        c=(int(10+12*t), int(18+17*t), int(40+22*t))
        for x in range(W):
            p[x,y]=c
    return im

def glow(im,x,y,r,c):
    q=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,64))
    q=q.filter(ImageFilter.GaussianBlur(r*0.55))
    im.paste(q,(0,0),q)

def card(d,b,c):
    d.rounded_rectangle(b,radius=44,fill=(16,38,72,235),outline=(*c,225),width=7)

def footer(d):
    d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))

def dot(d,x,y,c,r=24):
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)

def scene1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,CYAN); card(d,(80,700,1360,1515),CYAN)
    xs=[210,350,490,630,770,910,1050,1190]
    cols=[WHITE,WHITE,AMBER,WHITE,TEAL,WHITE,WHITE,WHITE]
    for x,c in zip(xs,cols):
        d.rounded_rectangle((x,965,x+95,1215),radius=20,fill=(*c,180),outline=(*WHITE,120),width=4)
    d.line((260,1090,1115,1090),fill=(*WHITE,110),width=6)
    footer(d)
    return im

def scene2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,AMBER); card(d,(80,700,1360,1515),AMBER)
    d.line((220,1110,1220,1110),fill=(*WHITE,190),width=10)
    for x,c,r in ((320,CYAN,38),(620,ROSE,30),(930,TEAL,38),(1140,VIOLET,28)):
        dot(d,x,1110,c,r)
    d.line((320,980,320,1240),fill=(*CYAN,170),width=8)
    d.line((930,980,930,1240),fill=(*TEAL,170),width=8)
    footer(d)
    return im

def scene3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(85,700,1355,1530),VIOLET)
    boxes=[(170,900,450,1230,CYAN),(500,900,780,1230,AMBER),(830,900,1110,1230,TEAL),(1160,900,1340,1230,ROSE)]
    for x1,y1,x2,y2,c in boxes:
        d.rounded_rectangle((x1,y1,x2,y2),radius=30,fill=(*c,125),outline=(*WHITE,170),width=6)
        d.line(((x1+x2)//2,1240,(x1+x2)//2,1400),fill=(*WHITE,170),width=8)
        d.rounded_rectangle((x1+20,1400,x2-20,1448),radius=18,fill=(*c,155),outline=(*WHITE,130),width=4)
    footer(d)
    return im

def scene4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(90,700,1350,1530),ROSE)
    for x,c in ((280,AMBER),(520,WHITE),(760,ROSE),(1000,WHITE),(1240,TEAL)):
        d.rounded_rectangle((x-55,930,x+55,1190),radius=22,fill=(*c,175),outline=(*WHITE,120),width=4)
    for x1,y1,x2,y2,c in ((210,1340,540,1490,CYAN),(555,1340,885,1490,VIOLET),(900,1340,1230,1490,TEAL)):
        d.rounded_rectangle((x1,y1,x2,y2),radius=26,fill=(*c,130),outline=(*WHITE,150),width=5)
    footer(d)
    return im

for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
    p=OUT/f'reel_0063_scene_{i:02d}.png'
    fn().save(p,optimize=True)
    print(p)
