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
   g=max(0,1-math.hypot(x-W*.52,y-H*.27)/(W*.95)); px[x,y]=(min(255,int(7+10*t+8*g)),min(255,int(14+18*t+18*g)),min(255,int(35+38*t+28*g)))
 return im
def glow(im,x,y,r,c,a=64):
 l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); l=l.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(l,(0,0),l)
def card(d,b,c): d.rounded_rectangle(b,radius=42,fill=(16,38,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,9,25,145))
def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,TEAL); card(d,(100,800,650,1250),CYAN); card(d,(790,800,1340,1250),AMBER)
 for y,c in [(925,CYAN),(1070,CYAN)]: d.line((190,y,560,y),fill=(*WHITE,190),width=12)
 for y,c in [(925,AMBER),(1070,AMBER)]: d.line((880,y,1250,y),fill=(*WHITE,190),width=12)
 for x,y,c in [(270,925,TEAL),(430,1070,TEAL),(990,925,RED),(1160,1070,RED)]: d.ellipse((x-28,y-28,x+28,y+28),fill=(*c,230))
 d.line((650,1025,790,1025),fill=(*WHITE,180),width=12); d.polygon([(790,1025),(740,995),(740,1055)],fill=(*WHITE,210)); footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER); card(d,(100,800,600,1180),TEAL); card(d,(840,800,1340,1180),VIOLET)
 for y in [930,1040,1150]: d.line((190,y,510,y),fill=(*WHITE,180),width=10)
 for y in [930,1040,1150]: d.line((930,y,1250,y),fill=(*WHITE,180),width=10)
 d.line((600,990,840,990),fill=(*AMBER,220),width=13); d.polygon([(840,990),(790,960),(790,1020)],fill=(*AMBER,220))
 card(d,(180,1350,1260,1700),CYAN); d.line((300,1530,1140,1530),fill=(*WHITE,200),width=12)
 for x,c in [(420,TEAL),(680,AMBER),(940,RED)]: d.ellipse((x-25,1505,x+25,1555),fill=(*c,230))
 footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,VIOLET); card(d,(110,800,1330,1200),CYAN)
 for x in [280,520,760,1000,1200]: d.ellipse((x-42,940,x+42,1024),outline=(*WHITE,190),width=8)
 d.line((360,982,440,982),fill=(*TEAL,220),width=10); d.line((600,982,680,982),fill=(*TEAL,220),width=10); d.line((840,982,920,982),fill=(*TEAL,220),width=10); d.line((1080,982,1120,982),fill=(*TEAL,220),width=10)
 card(d,(120,1340,630,1690),AMBER); card(d,(810,1340,1320,1690),RED)
 d.line((230,1510,520,1510),fill=(*WHITE,190),width=12); d.line((920,1510,1210,1510),fill=(*WHITE,190),width=12)
 for x,y in [(280,1510),(430,1510),(1000,1510),(1150,1510)]: d.ellipse((x-20,y-20,x+20,y+20),fill=(*TEAL,220))
 footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED); card(d,(120,800,1320,1170),TEAL)
 d.line((220,990,1220,990),fill=(*WHITE,190),width=12)
 for x,c in [(350,CYAN),(560,AMBER),(770,VIOLET),(980,RED),(1160,TEAL)]: d.ellipse((x-25,965,x+25,1015),fill=(*c,230))
 card(d,(120,1330,620,1680),CYAN); card(d,(820,1330,1320,1680),AMBER)
 d.line((220,1490,520,1490),fill=(*WHITE,190),width=11); d.line((920,1490,1220,1490),fill=(*WHITE,190),width=11)
 d.ellipse((350,1450,390,1490),fill=(*TEAL,230)); d.ellipse((1050,1450,1090,1490),fill=(*RED,230)); footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0028_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
