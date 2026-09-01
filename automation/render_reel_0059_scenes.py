from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
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
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,220),outline=(*WHITE,210),width=7); d.line((x-29,y+2,x-7,y+24),fill=(*BG,240),width=13); d.line((x-7,y+24,x+38,y-32),fill=(*BG,240),width=13)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def scene1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,VIOLET); card(d,(110,710,1330,1500),VIOLET)
 d.ellipse((245,860,650,1265),fill=(*VIOLET,120),outline=(*WHITE,180),width=7); d.ellipse((790,860,1195,1265),fill=(*AMBER,105),outline=(*WHITE,180),width=7)
 d.line((650,1062,790,1062),fill=(*WHITE,220),width=10); dot(d,720,1062,ROSE,32)
 for x,y,c in ((360,1010,WHITE),(505,1145,TEAL),(900,1010,WHITE),(1045,1145,CYAN)): dot(d,x,y,c,30)
 footer(d); return im
def scene2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,CYAN); card(d,(70,700,1370,1510),CYAN)
 for x,c in ((140,CYAN),(570,TEAL),(1000,AMBER)):
  d.rounded_rectangle((x,850,x+300,1350),radius=32,fill=(*c,110),outline=(*WHITE,175),width=7)
  for j in range(4): dot(d,x+76+j*55,1010+(j%2)*115,WHITE,18)
  d.line((x+65,1260,x+235,1260),fill=(*WHITE,170),width=9)
 footer(d); return im
def scene3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,TEAL); card(d,(100,710,1340,1500),TEAL)
 for y,c in ((900,CYAN),(1050,AMBER),(1200,VIOLET),(1350,ROSE)): check(d,270,y,c); d.line((390,y,1150,y),fill=(*WHITE,135),width=8)
 footer(d); return im
def scene4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(95,700,1345,1510),ROSE)
 centers=[(335,1080,CYAN),(720,900,TEAL),(1105,1080,AMBER)]
 for x,y,c in centers: dot(d,x,y,c,72)
 for a,b in zip(centers,centers[1:]): d.line((a[0],a[1],b[0],b[1]),fill=(*WHITE,190),width=12)
 d.line((335,1080,1105,1080),fill=(*WHITE,130),width=8)
 d.rounded_rectangle((390,1260,1050,1360),radius=25,fill=(*VIOLET,150),outline=(*WHITE,150),width=5)
 return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 p=OUT/f'reel_0059_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
