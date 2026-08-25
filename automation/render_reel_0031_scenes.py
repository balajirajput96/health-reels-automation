from __future__ import annotations
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(7,14,35); WHITE=(235,244,252); TEAL=(61,220,194); CYAN=(93,177,244); AMBER=(249,184,77); VIOLET=(163,124,239); RED=(241,105,119)
def base():
 im=Image.new('RGB',(W,H),BG); px=im.load()
 for y in range(H):
  t=y/(H-1)
  for x in range(W):
   g=max(0,1-math.hypot(x-W*.50,y-H*.26)/(W*.96)); px[x,y]=(min(255,int(7+10*t+8*g)),min(255,int(14+18*t+18*g)),min(255,int(35+38*t+28*g)))
 return im
def glow(im,x,y,r,c,a=64):
 l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); l=l.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(l,(0,0),l)
def card(d,b,c): d.rounded_rectangle(b,radius=42,fill=(16,38,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,9,25,145))
def lines(d,x0,y0,x1,ys,c=WHITE):
 for y in ys: d.line((x0,y,x1,y),fill=(*c,185),width=11)
def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,TEAL)
 card(d,(120,800,610,1280),VIOLET); card(d,(830,800,1320,1280),TEAL)
 d.ellipse((310,920,410,1020),fill=(*WHITE,220)); d.line((360,1020,360,1160),fill=(*WHITE,210),width=18); d.line((360,1060,470,1110),fill=(*WHITE,210),width=15)
 for y in [920,1030,1140]: d.line((940,y,1220,y),fill=(*WHITE,180),width=11)
 d.line((610,1040,830,1040),fill=(*AMBER,220),width=12); d.polygon([(830,1040),(780,1008),(780,1072)],fill=(*AMBER,220)); footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,CYAN)
 for b,c in [((90,790,410,1280),CYAN),((560,790,880,1280),TEAL),((1030,790,1350,1280),AMBER)]: card(d,b,c)
 for x in [170,640,1110]:
  d.rounded_rectangle((x+55,920,x+185,1060),radius=20,fill=(*WHITE,205)); d.line((x+80,1120,x+240,1120),fill=(*WHITE,180),width=12); d.line((x+80,1180,x+210,1180),fill=(*WHITE,180),width=12)
 footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER)
 for b,c in [((90,790,410,1190),VIOLET),((510,790,930,1190),TEAL),((1030,790,1350,1190),CYAN),((300,1320,1140,1700),AMBER)]: card(d,b,c)
 for x in [170,590,1110]: lines(d,x,900,min(x+230,1260),[900,1010,1120])
 d.line((720,1190,720,1320),fill=(*WHITE,180),width=12); d.polygon([(720,1320),(688,1270),(752,1270)],fill=(*WHITE,210)); lines(d,430,1450,1010,[1450,1560,1670],WHITE); footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED); card(d,(100,800,1340,1120),CYAN)
 d.line((210,980,1230,980),fill=(*WHITE,180),width=12); d.ellipse((390,940,450,1000),fill=(*TEAL,220)); d.ellipse((930,940,990,1000),fill=(*AMBER,220)); d.line((450,980,930,980),fill=(*WHITE,150),width=8)
 card(d,(130,1280,610,1690),TEAL); card(d,(830,1280,1310,1690),VIOLET)
 for y in [1400,1510,1620]: d.line((210,y,510,y),fill=(*WHITE,185),width=12); d.line((910,y,1210,y),fill=(*WHITE,185),width=12)
 footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0031_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
