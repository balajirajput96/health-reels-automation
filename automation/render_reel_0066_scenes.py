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
    q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,58)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)

def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(16,38,74,235),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def node(d,x,y,c,r=30): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,155),width=4)

def scene1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,CYAN); card(d,(80,700,1360,1530),CYAN)
 d.line((190,1280,1250,1280),fill=(*WHITE,185),width=8)
 pts=[(230,930),(440,970),(650,1030),(860,1130),(1070,1210),(1240,1260)]
 for a,b in zip(pts,pts[1:]): d.line((a[0],a[1],b[0],b[1]),fill=(*CYAN,225),width=12)
 for x,y in pts: node(d,x,y,CYAN,28)
 footer(d); return im

def scene2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,AMBER); card(d,(80,700,1360,1530),AMBER)
 for y,c,label in [(930,TEAL,'uninterrupted'),(1210,ROSE,'interrupted')]:
  d.line((190,y,1250,y),fill=(*WHITE,180),width=8)
  for x in (300,520,740,960,1180): node(d,x,y,c,25)
  d.rounded_rectangle((250,y-120,1190,y-70),radius=18,fill=(*c,100),outline=(*c,220),width=3)
 footer(d); return im

def scene3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(80,700,1360,1530),VIOLET)
 for x,y,c in [(330,970,CYAN),(330,1240,TEAL),(1110,970,AMBER),(1110,1240,ROSE)]:
  node(d,x,y,c,36); d.line((x+45 if x<720 else x-45,y,720,y),fill=(*c,180),width=10)
 node(d,720,1105,WHITE,46)
 footer(d); return im

def scene4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(80,700,1360,1530),ROSE)
 for i,(x,h,c) in enumerate([(230,250,CYAN),(455,390,AMBER),(680,320,TEAL),(905,450,VIOLET),(1130,280,ROSE)]):
  d.rounded_rectangle((x,1320-h,x+130,1320),radius=18,fill=(*c,200),outline=(*WHITE,145),width=4)
 d.line((180,1320,1260,1320),fill=(*WHITE,190),width=8)
 footer(d); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 p=OUT/f'reel_0066_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
