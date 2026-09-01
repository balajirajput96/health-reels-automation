from __future__ import annotations
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(6,14,34); WHITE=(231,243,252); TEAL=(57,220,194); CYAN=(93,177,244); AMBER=(249,184,77); VIOLET=(163,124,239); RED=(241,105,119)
def base():
 im=Image.new('RGB',(W,H),BG); px=im.load()
 for y in range(H):
  t=y/(H-1)
  for x in range(W):
   g=max(0,1-math.hypot(x-W*.52,y-H*.27)/(W*.95)); px[x,y]=(min(255,int(6+11*t+8*g)),min(255,int(14+18*t+19*g)),min(255,int(34+38*t+28*g)))
 return im
def glow(im,x,y,r,c,a=64):
 l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); l=l.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(l,(0,0),l)
def card(d,b,c): d.rounded_rectangle(b,radius=42,fill=(16,38,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,9,25,145))
def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,TEAL); d.ellipse((600,780,840,1160),outline=(*WHITE,210),width=10)
 for x,y,c in [(260,820,CYAN),(210,1120,AMBER),(1180,820,VIOLET),(1230,1120,RED),(410,1430,CYAN),(1030,1430,AMBER)]:
  d.ellipse((x-80,y-80,x+80,y+80),fill=(*c,215),outline=(*WHITE,145),width=6); d.line((x+80 if x<720 else x-80,y,650 if x<720 else 790,970),fill=(*c,180),width=10)
 footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER); card(d,(100,790,630,1180),CYAN); card(d,(810,790,1340,1180),TEAL)
 for y in [870,960,1050,1140]: d.line((190,y,540,y),fill=(*WHITE,180),width=9)
 for x in [270,380,485]: d.ellipse((x-18,950,x+18,986),fill=(*CYAN,230))
 d.ellipse((980,850,1170,1040),outline=(*WHITE,195),width=8); d.line((1075,1040,1075,1120),fill=(*WHITE,180),width=10); d.line((990,1120,1160,1120),fill=(*WHITE,180),width=10)
 card(d,(100,1330,630,1690),AMBER); card(d,(810,1330,1340,1690),VIOLET); d.line((190,1510,530,1510),fill=(*WHITE,190),width=10); d.line((900,1460,1230,1590),fill=(*WHITE,180),width=10); d.line((1230,1460,900,1590),fill=(*WHITE,180),width=10); footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,VIOLET); card(d,(110,780,1330,1130),TEAL)
 pts=[(180,980),(270,880),(360,1010),(450,860),(540,970),(630,830),(720,960),(810,850),(900,1010),(990,890),(1080,1000),(1180,860)]; d.line(pts,fill=(*WHITE,195),width=10)
 for x,y in pts: d.ellipse((x-20,y-20,x+20,y+20),fill=(*TEAL,230))
 card(d,(100,1300,600,1690),CYAN); card(d,(840,1300,1340,1690),RED); d.arc((210,1390,490,1650),180,360,fill=(*WHITE,210),width=10); d.line((930,1490,1230,1490),fill=(*RED,220),width=15); d.line((930,1410,1230,1570),fill=(*RED,150),width=9); footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED); card(d,(150,800,1290,1130),TEAL); d.line((280,965,1160,965),fill=(*WHITE,190),width=12)
 for x,c in [(360,TEAL),(560,CYAN),(760,AMBER),(960,VIOLET),(1120,RED)]: d.ellipse((x-28,937,x+28,993),fill=(*c,230))
 card(d,(100,1320,600,1640),AMBER); card(d,(840,1320,1340,1640),RED); d.line((200,1430,500,1530),fill=(*WHITE,160),width=10); d.line((500,1430,200,1530),fill=(*WHITE,160),width=10); d.line((930,1430,1230,1530),fill=(*RED,220),width=16); d.line((1230,1430,930,1530),fill=(*RED,220),width=16); card(d,(290,1730,1150,1810),CYAN); d.line((500,1770,940,1770),fill=(*WHITE,220),width=12); footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0026_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
