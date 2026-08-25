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
 for b,c in [((90,800,410,1260),CYAN),((560,800,880,1260),TEAL),((1030,800,1350,1260),AMBER)]: card(d,b,c)
 for x in [170,640,1110]:
  d.ellipse((x,900,x+100,1000),fill=(*WHITE,220)); d.line((x+50,1000,x+50,1150),fill=(*WHITE,210),width=18)
  d.line((x+50,1040,x+150,1090),fill=(*WHITE,210),width=15)
 footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,CYAN); card(d,(100,790,610,1320),VIOLET); card(d,(830,790,1340,1320),TEAL)
 lines(d,190,940,520,[940,1050,1160]); d.ellipse((270,1110,330,1170),fill=(*AMBER,230))
 d.ellipse((1020,930,1120,1030),fill=(*WHITE,220)); d.line((1070,1030,1070,1190),fill=(*WHITE,210),width=18); d.line((1070,1080,1165,1135),fill=(*WHITE,210),width=15)
 d.line((610,1060,830,1060),fill=(*WHITE,180),width=12); d.polygon([(830,1060),(780,1028),(780,1092)],fill=(*WHITE,210)); footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER)
 for b,c in [((100,800,430,1280),CYAN),((555,800,885,1280),TEAL),((1010,800,1340,1280),VIOLET)]: card(d,b,c)
 for x in [175,630,1085]:
  lines(d,x,940,x+210,[940,1050,1160]); d.ellipse((x+70,1010,x+130,1070),fill=(*AMBER,230))
 d.line((430,1040,555,1040),fill=(*WHITE,175),width=10); d.line((885,1040,1010,1040),fill=(*WHITE,175),width=10)
 card(d,(160,1430,1280,1720),RED); d.line((300,1580,1140,1580),fill=(*WHITE,190),width=12)
 for x,c in [(470,CYAN),(720,AMBER),(970,VIOLET)]: d.ellipse((x-25,1555,x+25,1605),fill=(*c,230))
 footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED); card(d,(100,790,1340,1180),CYAN); lines(d,210,920,1230,[920,1030,1135])
 card(d,(100,1320,610,1690),TEAL); card(d,(830,1320,1340,1690),AMBER)
 for y in [1435,1545,1655]:
  d.rounded_rectangle((190,y,250,y+60),radius=12,fill=(*WHITE,220)); d.line((290,y+30,510,y+30),fill=(*WHITE,180),width=11)
  d.rounded_rectangle((920,y,980,y+60),radius=12,fill=(*WHITE,220)); d.line((1020,y+30,1240,y+30),fill=(*WHITE,180),width=11)
 footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0030_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
