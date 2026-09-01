from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(7,16,39); WHITE=(244,247,252); CYAN=(77,211,255); TEAL=(61,224,176); AMBER=(249,185,68); VIOLET=(172,139,244); ROSE=(238,103,145)
def base():
    im=Image.new('RGB',(W,H),BG); p=im.load()
    for y in range(H):
        t=y/(H-1); c=(int(7+14*t),int(16+18*t),int(39+25*t))
        for x in range(W): p[x,y]=c
    return im
def glow(im,x,y,r,c):
    q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,62)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)
def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(15,37,73,235),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,155))
def node(d,x,y,c,r=30): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,235),outline=(*WHITE,160),width=4)
def arrow(d,a,b,c):
    d.line((a[0],a[1],b[0],b[1]),fill=(*c,210),width=11); ang=math.atan2(b[1]-a[1],b[0]-a[0]); size=30
    pts=[b,(b[0]-size*math.cos(ang-.5),b[1]-size*math.sin(ang-.5)),(b[0]-size*math.cos(ang+.5),b[1]-size*math.sin(ang+.5))]; d.polygon(pts,fill=(*c,220))
def scene1():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,400,590,CYAN); card(d,(85,690,1355,1515),CYAN)
    node(d,370,1050,CYAN,65); node(d,1070,1050,TEAL,65); arrow(d,(455,1050),(985,1050),CYAN)
    for x in (570,720,870): node(d,x,1050,AMBER,24)
    d.line((280,1260,1160,1260),fill=(*WHITE,150),width=8); footer(d); return im
def scene2():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,390,560,AMBER); card(d,(80,670,1360,1570),AMBER)
    d.rounded_rectangle((130,790,650,1430),radius=36,fill=(9,26,54,225),outline=(*TEAL,210),width=6); d.rounded_rectangle((790,790,1310,1430),radius=36,fill=(9,26,54,225),outline=(*ROSE,210),width=6)
    for x,y,c in [(280,980,TEAL),(500,1250,TEAL),(950,980,ROSE),(1130,1250,ROSE)]: node(d,x,y,c,36)
    arrow(d,(315,980),(465,1250),TEAL); arrow(d,(985,980),(1095,1250),ROSE); d.line((650,1110,790,1110),fill=(*WHITE,180),width=7); node(d,720,1110,WHITE,30); footer(d); return im
def scene3():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,410,570,VIOLET); card(d,(75,650,1365,1600),VIOLET)
    boxes=[(150,820,610,1080,CYAN),(830,820,1290,1080,TEAL),(150,1180,610,1440,AMBER),(830,1180,1290,1440,ROSE)]
    for x1,y1,x2,y2,c in boxes:
        d.rounded_rectangle((x1,y1,x2,y2),radius=34,fill=(8,23,50,240),outline=(*c,220),width=6); d.line((x1+65,y2-65,x2-65,y2-65),fill=(*WHITE,130),width=7)
    for x,y,c in [(240,980,CYAN),(920,980,TEAL),(240,1340,AMBER),(920,1340,ROSE)]:
        for i in range(4): node(d,x+70+i*70,y-50*(i%2),c,18)
    footer(d); return im
def scene4():
    im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,390,560,ROSE); card(d,(80,680,1360,1580),ROSE)
    centers=[(250,990,CYAN),(570,990,TEAL),(890,990,AMBER),(1190,990,VIOLET)]
    for x,y,c in centers: d.ellipse((x-105,y-105,x+105,y+105),fill=(9,24,52,235),outline=(*c,220),width=7); node(d,x,y,c,32)
    for a,b in zip(centers,centers[1:]): arrow(d,(a[0]+110,a[1]),(b[0]-110,b[1]),WHITE)
    d.line((230,1300,1210,1300),fill=(*WHITE,175),width=8)
    for x,h,c in [(270,160,CYAN),(500,260,TEAL),(730,210,AMBER),(960,320,VIOLET),(1190,180,ROSE)]: d.rounded_rectangle((x,1300-h,x+90,1300),radius=18,fill=(*c,210),outline=(*WHITE,120),width=4)
    footer(d); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
    path=OUT/f'reel_0068_scene_{i:02d}.png'; fn().save(path,optimize=True); print(path)
