from __future__ import annotations
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(7,15,36); TEAL=(57,220,194); CYAN=(93,177,244); AMBER=(249,184,77); VIOLET=(163,124,239); WHITE=(229,241,252); RED=(241,105,119)
def gradient():
 im=Image.new('RGB',(W,H),BG); px=im.load()
 for y in range(H):
  t=y/(H-1)
  for x in range(W):
   g=max(0,1-math.hypot(x-W*.5,y-H*.28)/(W*.95)); px[x,y]=(min(255,int(7+10*t+8*g)),min(255,int(15+18*t+19*g)),min(255,int(36+37*t+28*g)))
 return im
def glow(im,c,r,col,a=70):
 l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); x,y=c; d.ellipse((x-r,y-r,x+r,y+r),fill=(*col,a)); l=l.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(l,(0,0),l)
def card(d,b,o,fill=(17,38,69,242)): d.rounded_rectangle(b,radius=40,fill=fill,outline=(*o,220),width=7)
def lower(d): d.rounded_rectangle((82,1830,1358,2460),radius=60,fill=(4,10,27,140))
def scene1():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,TEAL,42); card(d,(560,820,880,1190),TEAL)
 for x,y,c in [(270,860,CYAN),(250,1120,AMBER),(1170,860,VIOLET),(1190,1120,RED),(440,1370,CYAN),(1000,1370,TEAL)]:
  d.ellipse((x-85,y-85,x+85,y+85),fill=(*c,210),outline=(*WHITE,150),width=6); d.line((x+85 if x<720 else x-85,y,640 if x<720 else 800,1005),fill=(*c,170),width=10)
 d.ellipse((650,905,790,1045),fill=(*WHITE,40),outline=(*WHITE,200),width=8); lower(d); return im
def scene2():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,AMBER,42); card(d,(150,800,1290,1170),CYAN); d.line((270,985,1170,985),fill=(*WHITE,180),width=12)
 for x,c in [(330,TEAL),(520,CYAN),(710,AMBER),(900,VIOLET),(1090,RED)]: d.ellipse((x-30,955,x+30,1015),fill=(*c,230))
 card(d,(150,1310,600,1680),TEAL); card(d,(840,1310,1290,1680),AMBER); d.line((235,1420,510,1420),fill=(*WHITE,170),width=9); d.line((235,1490,510,1490),fill=(*WHITE,170),width=9); d.line((925,1410,1210,1560),fill=(*WHITE,180),width=12); d.line((1210,1410,925,1560),fill=(*WHITE,180),width=12); lower(d); return im
def scene3():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,VIOLET,42); card(d,(120,790,1320,1160),VIOLET); d.line((220,980,1220,980),fill=(*WHITE,170),width=10)
 for x,c in [(300,TEAL),(510,CYAN),(720,AMBER),(930,VIOLET),(1140,RED)]: d.ellipse((x-28,952,x+28,1008),fill=(*c,230))
 card(d,(120,1300,620,1680),CYAN); card(d,(820,1300,1320,1680),RED)
 pts=[(220,1550),(290,1460),(360,1580),(430,1430),(500,1550)]; d.line(pts,fill=(*WHITE,200),width=9); d.line((900,1530,1240,1530),fill=(*RED,210),width=16); d.line((900,1460,1240,1590),fill=(*RED,150),width=9)
 lower(d); return im
def scene4():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,RED,42); card(d,(170,800,1270,1130),TEAL); d.line((300,965,1140,965),fill=(*WHITE,200),width=12)
 for x,c in [(360,TEAL),(560,CYAN),(760,AMBER),(960,VIOLET),(1120,RED)]: d.ellipse((x-28,937,x+28,993),fill=(*c,230))
 card(d,(110,1260,600,1630),AMBER); card(d,(840,1260,1330,1630),RED); d.line((205,1370,500,1520),fill=(*WHITE,160),width=10); d.line((500,1370,205,1520),fill=(*WHITE,160),width=10); d.line((930,1360,1230,1530),fill=(*RED,220),width=18); d.line((1230,1360,930,1530),fill=(*RED,220),width=18); card(d,(290,1710,1150,1790),CYAN); d.line((500,1750,940,1750),fill=(*WHITE,220),width=12); lower(d); return im
for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
 p=OUT/f'reel_0023_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
