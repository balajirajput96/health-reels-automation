from __future__ import annotations
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(7,14,34); WHITE=(242,247,252); CYAN=(66,190,245); TEAL=(48,219,174); AMBER=(247,188,72); VIOLET=(165,125,244); ROSE=(239,104,135)
def base():
 im=Image.new('RGB',(W,H),BG); px=im.load()
 for y in range(H):
  t=y/(H-1)
  col=(int(7+14*t),int(14+18*t),int(34+28*t))
  for x in range(W): px[x,y]=col
 return im
def glow(im,x,y,r,c,a=65):
 q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)
def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(14,38,70,240),outline=(*c,225),width=7)
def dot(d,x,y,c,r=28): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,220),outline=(*WHITE,210),width=7); d.line((x-28,y+2,x-6,y+25),fill=(*BG,240),width=13); d.line((x-6,y+25,x+38,y-32),fill=(*BG,240),width=13)
def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,CYAN); card(d,(110,720,1330,1500),CYAN)
 d.rounded_rectangle((220,900,690,1290),radius=32,fill=(*CYAN,115),outline=(*WHITE,170),width=6)
 d.rounded_rectangle((780,900,1220,1290),radius=32,fill=(*ROSE,95),outline=(*WHITE,170),width=6)
 d.line((690,1095,780,1095),fill=(*WHITE,210),width=10); dot(d,720,1095,AMBER,30)
 for x,y,c in ((330,1030,WHITE),(470,1165,TEAL),(895,1030,WHITE),(1050,1170,VIOLET)): dot(d,x,y,c,32)
 footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,TEAL); card(d,(90,700,1350,1510),TEAL)
 for x,c in ((190,CYAN),(570,AMBER),(950,VIOLET)):
  d.rounded_rectangle((x,850,x+300,1350),radius=35,fill=(*c,105),outline=(*WHITE,175),width=7)
  for j in range(4): dot(d,x+75+j*55,1010+j%2*115,WHITE,18)
  d.line((x+70,1260,x+230,1260),fill=(*WHITE,165),width=9)
 footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,AMBER); card(d,(100,720,1340,1500),AMBER)
 bars=[(190,620,CYAN),(420,460,TEAL),(650,730,VIOLET),(880,540,ROSE),(1110,380,AMBER)]
 for x,h,c in bars:
  d.rounded_rectangle((x,1340-h,x+130,1340),radius=18,fill=(*c,200),outline=(*WHITE,140),width=5)
 d.line((150,1340,1280,1340),fill=(*WHITE,180),width=9); d.line((150,830,150,1340),fill=(*WHITE,180),width=9)
 footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,ROSE); card(d,(100,700,1340,1510),ROSE)
 d.rounded_rectangle((180,850,700,1360),radius=30,fill=(*VIOLET,105),outline=(*WHITE,165),width=6)
 for y,c in ((970,CYAN),(1110,TEAL),(1250,AMBER)): check(d,290,y,c); d.line((390,y,620,y),fill=(*WHITE,145),width=8)
 d.rounded_rectangle((820,850,1250,1360),radius=30,fill=(*CYAN,95),outline=(*WHITE,165),width=6)
 for i in range(5): d.line((900+i*70,1260,900+i*70,1000-(i%2)*90),fill=(*TEAL,210),width=16)
 return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0057_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
