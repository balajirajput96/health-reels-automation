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
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,TEAL,42); card(d,(590,820,850,1110),TEAL)
 for x,y,c in [(240,820,CYAN),(220,1110,AMBER),(1190,820,VIOLET),(1210,1110,RED),(390,1390,CYAN),(1050,1390,AMBER)]:
  d.ellipse((x-80,y-80,x+80,y+80),fill=(*c,215),outline=(*WHITE,150),width=6); d.line((x+80 if x<720 else x-80,y,640 if x<720 else 800,965),fill=(*c,180),width=10)
 d.ellipse((650,895,790,1035),outline=(*WHITE,190),width=8); lower(d); return im
def scene2():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,AMBER,42); card(d,(110,790,620,1180),CYAN); card(d,(820,790,1330,1180),TEAL)
 for y in [880,960,1040,1120]: d.line((190,y,520,y),fill=(*WHITE,180),width=9)
 d.ellipse((980,850,1170,1040),outline=(*WHITE,190),width=8); d.line((1075,1040,1075,1120),fill=(*WHITE,180),width=10); d.line((1000,1120,1150,1120),fill=(*WHITE,180),width=10)
 card(d,(110,1320,620,1680),AMBER); card(d,(820,1320,1330,1680),VIOLET); d.line((220,1500,510,1500),fill=(*WHITE,190),width=10); d.line((900,1430,1220,1570),fill=(*WHITE,190),width=12); d.line((1220,1430,900,1570),fill=(*WHITE,190),width=12); lower(d); return im
def scene3():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,VIOLET,42); card(d,(130,780,1310,1160),TEAL); d.ellipse((620,820,820,1100),outline=(*WHITE,190),width=9); d.arc((490,850,950,1170),180,360,fill=(*CYAN,190),width=10); d.arc((500,860,940,1180),0,180,fill=(*AMBER,190),width=10)
 card(d,(110,1300,610,1680),CYAN); card(d,(830,1300,1330,1680),RED); pts=[(190,1550),(270,1450),(350,1580),(430,1430),(520,1540)]; d.line(pts,fill=(*WHITE,200),width=9); d.line((930,1510,1240,1510),fill=(*RED,220),width=16); d.line((930,1430,1240,1580),fill=(*RED,150),width=9); lower(d); return im
def scene4():
 im=gradient(); d=ImageDraw.Draw(im,'RGBA'); glow(im,(720,420),500,RED,42); card(d,(160,800,1280,1120),TEAL); d.line((300,960,1140,960),fill=(*WHITE,200),width=12)
 for x,c in [(360,TEAL),(560,CYAN),(760,AMBER),(960,VIOLET),(1120,RED)]: d.ellipse((x-28,932,x+28,988),fill=(*c,230))
 card(d,(100,1260,600,1630),AMBER); card(d,(840,1260,1340,1630),RED); d.line((200,1370,500,1520),fill=(*WHITE,160),width=10); d.line((500,1370,200,1520),fill=(*WHITE,160),width=10); d.line((930,1370,1230,1520),fill=(*RED,220),width=18); d.line((1230,1370,930,1520),fill=(*RED,220),width=18); card(d,(290,1710,1150,1790),CYAN); d.line((500,1750,940,1750),fill=(*WHITE,220),width=12); lower(d); return im
for i,fn in enumerate([scene1,scene2,scene3,scene4],1):
 p=OUT/f'reel_0025_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
