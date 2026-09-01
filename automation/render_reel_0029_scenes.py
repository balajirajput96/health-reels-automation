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
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,TEAL); card(d,(95,800,655,1280),CYAN); card(d,(785,800,1345,1280),AMBER)
 lines(d,175,940,575,[940,1060,1180]); lines(d,865,940,1265,[940,1060,1180])
 for x,y,c in [(275,940,TEAL),(425,1060,TEAL),(975,940,RED),(1125,1180,RED)]: d.ellipse((x-28,y-28,x+28,y+28),fill=(*c,230))
 d.line((655,1040,785,1040),fill=(*WHITE,180),width=12); d.polygon([(785,1040),(735,1008),(735,1072)],fill=(*WHITE,210)); footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,AMBER); card(d,(100,790,1340,1120),TEAL); lines(d,210,905,1230,[905,1010],WHITE)
 for x,c in [(360,CYAN),(650,AMBER),(940,VIOLET)]: d.ellipse((x-32,950,x+32,1014),fill=(*c,230))
 card(d,(100,1250,620,1680),CYAN); card(d,(820,1250,1340,1680),VIOLET)
 lines(d,190,1370,530,[1370,1490,1610]); lines(d,910,1370,1250,[1370,1490,1610])
 d.line((620,1460,820,1460),fill=(*AMBER,220),width=12); d.polygon([(820,1460),(770,1428),(770,1492)],fill=(*AMBER,220)); footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,VIOLET)
 for b,c in [((100,800,430,1260),CYAN),((555,800,885,1260),TEAL),((1010,800,1340,1260),AMBER)]: card(d,b,c)
 for x in [180,635,1090]: lines(d,x,935,x+210,[935,1050,1165])
 d.line((430,1030,555,1030),fill=(*WHITE,180),width=10); d.line((885,1030,1010,1030),fill=(*WHITE,180),width=10)
 card(d,(170,1380,1270,1720),RED); d.line((290,1550,1150,1550),fill=(*WHITE,190),width=12)
 for x,c in [(470,CYAN),(720,AMBER),(970,VIOLET)]: d.ellipse((x-25,1525,x+25,1575),fill=(*c,230))
 footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,500,RED); card(d,(110,800,1330,1180),CYAN); lines(d,220,930,1220,[930,1050,1140])
 card(d,(110,1320,610,1690),TEAL); card(d,(830,1320,1330,1690),AMBER)
 d.line((210,1450,510,1450),fill=(*WHITE,190),width=12); d.line((930,1450,1230,1450),fill=(*WHITE,190),width=12)
 d.ellipse((330,1410,390,1470),fill=(*CYAN,230)); d.ellipse((1050,1410,1110,1470),fill=(*RED,230)); footer(d); return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0029_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
