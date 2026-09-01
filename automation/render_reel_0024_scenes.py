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
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,TEAL,42); card(d,(560,850,880,1180),TEAL)
 for x,y,c in [(260,880,CYAN),(250,1150,AMBER),(1180,880,VIOLET),(1190,1150,RED)]:
  d.ellipse((x-90,y-90,x+90,y+90),fill=(*c,210),outline=(*WHITE,150),width=6); d.line((x+90 if x<720 else x-90,y,640 if x<720 else 800,1015),fill=(*c,180),width=11)
 d.arc((500,720,940,1310),0,360,fill=(*WHITE,160),width=8); lower(d); return im
def scene2():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,AMBER,42); card(d,(130,790,1310,1140),CYAN); d.line((250,965,1190,965),fill=(*WHITE,180),width=12)
 for x,c in [(320,TEAL),(520,CYAN),(720,AMBER),(920,VIOLET),(1120,RED)]: d.ellipse((x-28,937,x+28,993),fill=(*c,230))
 card(d,(130,1280,610,1680),TEAL); card(d,(830,1280,1310,1680),AMBER)
 for y in [1390,1470,1550]: d.line((220,y,520,y),fill=(*WHITE,170),width=9)
 d.line((920,1390,1220,1540),fill=(*WHITE,180),width=12); d.line((1220,1390,920,1540),fill=(*WHITE,180),width=12); lower(d); return im
def scene3():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,VIOLET,42); card(d,(100,790,1340,1150),VIOLET); d.line((210,980,1230,980),fill=(*WHITE,180),width=10)
 for x,c in [(280,TEAL),(500,CYAN),(720,AMBER),(940,VIOLET),(1160,RED)]: d.ellipse((x-28,952,x+28,1008),fill=(*c,230))
 card(d,(110,1300,610,1680),CYAN); card(d,(830,1300,1330,1680),RED); pts=[(200,1550),(280,1460),(360,1570),(440,1430),(520,1540)]; d.line(pts,fill=(*WHITE,200),width=9); d.line((920,1510,1240,1510),fill=(*RED,220),width=16); d.line((920,1430,1240,1580),fill=(*RED,150),width=9); lower(d); return im
def scene4():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,RED,42); card(d,(150,800,1290,1130),TEAL); d.line((280,965,1160,965),fill=(*WHITE,200),width=12)
 for x,c in [(350,TEAL),(550,CYAN),(750,AMBER),(950,VIOLET),(1130,RED)]: d.ellipse((x-28,937,x+28,993),fill=(*c,230))
 card(d,(110,1260,600,1630),AMBER); card(d,(840,1260,1330,1630),RED); d.line((210,1370,500,1520),fill=(*WHITE,160),width=10); d.line((500,1370,210,1520),fill=(*WHITE,160),width=10); d.line((930,1360,1230,1530),fill=(*RED,220),width=18); d.line((1230,1360,930,1530),fill=(*RED,220),width=18); card(d,(290,1710,1150,1790),CYAN); d.line((500,1750,940,1750),fill=(*WHITE,220),width=12); lower(d); return im
for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
 p=OUT/f'reel_0024_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
