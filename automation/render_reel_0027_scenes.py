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
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,TEAL)
 d.ellipse((970,740,1120,990),outline=(*WHITE,220),width=10); d.line((1045,990,1045,1200),fill=(*WHITE,200),width=10); d.line((950,1200,1140,1200),fill=(*WHITE,200),width=10)
 d.ellipse((320,740,470,990),outline=(*CYAN,220),width=10); d.line((395,990,395,1200),fill=(*CYAN,200),width=10); d.line((300,1200,490,1200),fill=(*CYAN,200),width=10)
 d.line((470,865,970,865),fill=(*TEAL,200),width=10); d.polygon([(970,865),(920,835),(920,895)],fill=(*TEAL,220))
 d.line((470,1060,970,1120),fill=(*AMBER,180),width=10); d.polygon([(970,1120),(918,1085),(912,1145)],fill=(*AMBER,220))
 footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER); card(d,(110,800,1330,1130),CYAN)
 pts=[(200,960),(350,900),(500,990),(650,860),(800,980),(950,890),(1100,960),(1240,870)]; d.line(pts,fill=(*WHITE,190),width=12)
 for x,y in pts: d.ellipse((x-24,y-24,x+24,y+24),fill=(*CYAN,230))
 card(d,(110,1310,610,1680),TEAL); card(d,(830,1310,1330,1680),VIOLET)
 for y in [1410,1510,1610]: d.line((190,y,530,y),fill=(*WHITE,170),width=10)
 d.ellipse((1000,1390,1160,1550),outline=(*WHITE,200),width=9); d.line((1080,1550,1080,1620),fill=(*WHITE,180),width=10); footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,VIOLET); card(d,(100,780,650,1160),AMBER); card(d,(790,780,1340,1160),TEAL)
 d.line((190,980,550,980),fill=(*WHITE,180),width=12); d.line((890,980,1250,980),fill=(*WHITE,180),width=12)
 for x in [260,390,520]: d.ellipse((x-18,962,x+18,998),fill=(*AMBER,230))
 for x in [950,1080,1210]: d.ellipse((x-18,962,x+18,998),fill=(*TEAL,230))
 card(d,(120,1330,1320,1700),CYAN); pts=[(180,1570),(280,1500),(380,1610),(480,1450),(580,1550),(680,1410),(780,1530),(880,1480),(980,1600),(1080,1430),(1180,1530),(1260,1470)]; d.line(pts,fill=(*WHITE,200),width=10)
 for x,y in pts: d.ellipse((x-15,y-15,x+15,y+15),fill=(*CYAN,230))
 footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED); card(d,(150,800,1290,1120),TEAL)
 d.line((300,960,1140,960),fill=(*WHITE,190),width=12);
 for x,c in [(400,TEAL),(610,CYAN),(820,AMBER),(1030,VIOLET)]: d.ellipse((x-28,932,x+28,988),fill=(*c,230))
 card(d,(100,1310,600,1660),AMBER); card(d,(840,1310,1340,1660),RED)
 d.line((200,1430,500,1540),fill=(*WHITE,180),width=10); d.line((500,1430,200,1540),fill=(*WHITE,180),width=10)
 d.line((940,1430,1240,1540),fill=(*RED,220),width=15); d.line((1240,1430,940,1540),fill=(*RED,220),width=15); card(d,(300,1740,1140,1810),CYAN); d.line((520,1775,920,1775),fill=(*WHITE,220),width=12); footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0027_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
