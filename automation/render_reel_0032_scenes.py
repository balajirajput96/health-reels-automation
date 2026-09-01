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
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,TEAL); card(d,(110,790,1330,1260),VIOLET)
 d.ellipse((260,930,360,1030),fill=(*WHITE,220)); d.line((310,1030,310,1160),fill=(*WHITE,210),width=18)
 for x,c in [(620,CYAN),(900,AMBER)]:
  d.rounded_rectangle((x,900,x+220,1040),radius=25,fill=(*c,210)); d.line((x+40,1100,x+180,1100),fill=(*WHITE,190),width=12); d.line((x+40,1160,x+150,1160),fill=(*WHITE,190),width=12)
 footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,CYAN)
 for b,c in [((90,800,410,1280),CYAN),((560,800,880,1280),TEAL),((1030,800,1350,1280),AMBER)]: card(d,b,c)
 for x in [170,640,1110]:
  d.rounded_rectangle((x+50,930,x+190,1060),radius=18,fill=(*WHITE,210)); d.line((x+60,1130,x+240,1130),fill=(*WHITE,180),width=12); d.line((x+60,1190,x+190,1190),fill=(*WHITE,180),width=12)
 footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER); card(d,(200,790,1240,1280),TEAL)
 d.ellipse((610,880,830,1100),outline=(*WHITE,200),width=16); d.ellipse((675,945,765,1035),fill=(*AMBER,210)); d.line((720,1100,720,1210),fill=(*WHITE,180),width=12)
 for x in [360,1030]:
  d.ellipse((x,930,x+95,1025),fill=(*WHITE,210)); d.line((x+48,1025,x+48,1170),fill=(*WHITE,190),width=14)
 d.line((450,980,610,980),fill=(*CYAN,210),width=11); d.line((830,980,990,980),fill=(*CYAN,210),width=11); footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED)
 for b,c in [((90,800,410,1210),CYAN),((515,800,925,1210),VIOLET),((1030,800,1350,1210),AMBER),((280,1350,1160,1700),TEAL)]: card(d,b,c)
 for x in [160,585,1100]:
  d.line((x,930,x+200,930),fill=(*WHITE,190),width=12); d.line((x,1040,x+150,1040),fill=(*WHITE,180),width=12); d.line((x,1150,x+230,1150),fill=(*WHITE,180),width=12)
 for x in [480,720,960]: d.ellipse((x-25,1510,x+25,1560),fill=(*AMBER,220))
 d.line((330,1535,1110,1535),fill=(*WHITE,180),width=10); footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0032_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
