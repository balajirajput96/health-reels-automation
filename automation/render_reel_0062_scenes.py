from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(8,16,38); WHITE=(242,247,252); CYAN=(74,204,245); TEAL=(54,221,178); AMBER=(248,188,72); VIOLET=(169,133,246); ROSE=(239,106,143)
def base():
 im=Image.new('RGB',(W,H),BG); p=im.load()
 for y in range(H):
  t=y/(H-1); c=(int(8+14*t),int(16+18*t),int(38+24*t))
  for x in range(W): p[x,y]=c
 return im
def glow(im,x,y,r,c):
 q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,62)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)
def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(15,39,72,235),outline=(*c,225),width=7)
def dot(d,x,y,c,r=28): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def scene1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,580,ROSE); card(d,(90,700,1350,1515),ROSE)
 d.rounded_rectangle((170,900,570,1280),radius=35,fill=(*CYAN,125),outline=(*WHITE,180),width=7)
 d.rounded_rectangle((870,900,1270,1280),radius=35,fill=(*AMBER,125),outline=(*WHITE,180),width=7)
 for x,y,c in ((260,1000,CYAN),(480,1170,WHITE),(960,1000,AMBER),(1180,1170,WHITE)): dot(d,x,y,c,28)
 d.line((570,1090,870,1090),fill=(*WHITE,200),width=12); dot(d,720,1090,TEAL,40); footer(d); return im
def scene2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,CYAN); card(d,(70,700,1370,1515),CYAN)
 target=(720,1090)
 for y in (870,1030,1210,1320):
  for x in (220,420,1020,1220): dot(d,x,y,WHITE,18)
 for x,y in ((330,910),(500,1250),(920,930),(1110,1240)): dot(d,x,y,AMBER,24)
 dot(d,*target,TEAL,46); d.line((180,1090,660,1090),fill=(*TEAL,190),width=12); d.line((780,1090,1260,1090),fill=(*TEAL,190),width=12); footer(d); return im
def scene3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,TEAL); card(d,(85,700,1355,1530),TEAL)
 xs=[150,480,810,1140]; cs=[CYAN,AMBER,VIOLET,ROSE]
 for x,c in zip(xs,cs):
  d.rounded_rectangle((x,900,x+180,1220),radius=32,fill=(*c,125),outline=(*WHITE,170),width=6)
  for j in range(3): dot(d,x+55+j*38,1010+(j%2)*105,WHITE,15)
  d.line((x+90,1260,x+90,1390),fill=(*WHITE,170),width=8)
  d.rounded_rectangle((x-15,1390,x+195,1438),radius=20,fill=(*c,160),outline=(*WHITE,130),width=4)
 footer(d); return im
def scene4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(90,700,1350,1530),VIOLET)
 for row,(y,c) in enumerate(((900,CYAN),(1080,AMBER),(1260,TEAL))):
  for x in (240,430,620,810,1000,1190): dot(d,x,y,c,25)
  d.line((210,y,1230,y),fill=(*WHITE,120),width=5)
 for x,y,c in ((240,1440,CYAN),(720,1440,AMBER),(1200,1440,ROSE)): dot(d,x,y,c,52)
 d.line((292,1440,668,1440),fill=(*WHITE,170),width=9); d.line((772,1440,1148,1440),fill=(*WHITE,170),width=9); footer(d); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 p=OUT/f'reel_0062_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
