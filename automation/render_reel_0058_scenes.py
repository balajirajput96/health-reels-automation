from __future__ import annotations
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(8,14,34); WHITE=(242,247,252); CYAN=(65,190,245); TEAL=(48,220,173); AMBER=(248,189,72); VIOLET=(166,126,245); ROSE=(239,104,138)
def base():
 im=Image.new('RGB',(W,H),BG); p=im.load()
 for y in range(H):
  t=y/(H-1); c=(int(8+15*t),int(14+18*t),int(34+27*t))
  for x in range(W): p[x,y]=c
 return im
def glow(im,x,y,r,c):
 q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,70)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)
def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(15,39,71,240),outline=(*c,225),width=7)
def dot(d,x,y,c,r=28): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,220),outline=(*WHITE,210),width=7); d.line((x-29,y+2,x-7,y+24),fill=(*BG,240),width=13); d.line((x-7,y+24,x+38,y-32),fill=(*BG,240),width=13)
def scene1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,VIOLET); card(d,(110,710,1330,1500),VIOLET)
 d.ellipse((260,850,690,1280),fill=(*VIOLET,125),outline=(*WHITE,180),width=7)
 d.ellipse((750,850,1180,1280),fill=(*AMBER,105),outline=(*WHITE,180),width=7)
 d.line((690,1065,750,1065),fill=(*WHITE,220),width=10); dot(d,720,1065,ROSE,32)
 for x,y,c in ((375,1020,WHITE),(520,1140,TEAL),(865,1020,WHITE),(1015,1140,CYAN)): dot(d,x,y,c,31)
 footer(d); return im
def scene2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,CYAN); card(d,(80,700,1360,1510),CYAN)
 for x,c in ((150,CYAN),(570,TEAL),(990,AMBER)):
  d.rounded_rectangle((x,850,x+300,1350),radius=32,fill=(*c,110),outline=(*WHITE,175),width=7)
  for j in range(4): dot(d,x+78+j*52,1015+(j%2)*110,WHITE,18)
  d.line((x+70,1260,x+230,1260),fill=(*WHITE,170),width=9)
 footer(d); return im
def scene3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,TEAL); card(d,(100,710,1340,1500),TEAL)
 pts=[(230,1130),(520,920),(820,1190),(1120,900)]
 for a,b in zip(pts,pts[1:]): d.line((*a,*b),fill=(*WHITE,180),width=10)
 for i,(x,y) in enumerate(pts): dot(d,x,y,(CYAN,AMBER,VIOLET,ROSE)[i],48)
 d.line((230,1300,1120,1300),fill=(*WHITE,160),width=8)
 footer(d); return im
def scene4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(100,700,1340,1510),ROSE)
 d.rounded_rectangle((170,850,670,1370),radius=32,fill=(*CYAN,100),outline=(*WHITE,170),width=6)
 d.rounded_rectangle((770,850,1270,1370),radius=32,fill=(*AMBER,90),outline=(*WHITE,170),width=6)
 for y,c in ((980,TEAL),(1130,VIOLET),(1280,CYAN)): check(d,290,y,c); d.line((390,y,590,y),fill=(*WHITE,145),width=8)
 d.line((860,1260,1190,960),fill=(*WHITE,190),width=12); d.line((860,960,1190,1260),fill=(*WHITE,190),width=12)
 return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 p=OUT/f'reel_0058_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
