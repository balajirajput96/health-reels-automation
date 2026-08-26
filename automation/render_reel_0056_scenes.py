from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560
OUT=Path('/home/ubuntu/repos/health-reels-automation/assets')
BG=(8,13,34); WHITE=(241,247,252); CYAN=(75,187,245); TEAL=(57,221,183); AMBER=(247,187,74); VIOLET=(166,127,244); ROSE=(240,106,132)
def base():
 im=Image.new('RGB',(W,H),BG); px=im.load()
 for y in range(H):
  t=y/(H-1); g=max(0,1-math.hypot(W*.5,y-H*.2)/(W*1.05)); col=(int(8+12*t+8*g),int(13+17*t+15*g),int(34+30*t+26*g))
  for x in range(W): px[x,y]=col
 return im
def glow(im,x,y,r,c,a=62):
 lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); lay=lay.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(lay,(0,0),lay)
def card(d,box,c): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,140),width=4)
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8); d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)
def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,CYAN); card(d,(100,720,1340,1490),CYAN)
 d.arc((250,850,1190,1430),180,350,fill=(*AMBER,230),width=22); d.line((720,1140,970,900),fill=(*ROSE,230),width=18); dot(d,720,1140,WHITE,48); dot(d,970,900,AMBER,42)
 for x,y,c in ((300,1250,TEAL),(1140,1250,VIOLET),(350,900,ROSE),(1090,900,CYAN)): dot(d,x,y,c,34)
 footer(d); return im
def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,TEAL); card(d,(100,720,1340,1490),TEAL)
 dot(d,720,1090,WHITE,62)
 for x,y,c in ((300,880,CYAN),(1140,880,AMBER),(300,1300,VIOLET),(1140,1300,ROSE)):
  d.line((720,1090,x,y),fill=(*WHITE,170),width=10); dot(d,x,y,c,55)
 for x,y in ((300,880),(1140,880),(300,1300),(1140,1300)):
  d.line((x,y+85,x,y+180),fill=(*WHITE,130),width=8); dot(d,x,y+205,WHITE,16)
 footer(d); return im
def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,AMBER); card(d,(100,720,1340,1490),AMBER)
 boxes=[(180,CYAN),(500,TEAL),(820,VIOLET),(1140,ROSE)]
 for x,c in boxes:
  d.rounded_rectangle((x,930,x+180,1250),radius=28,fill=(*c,145),outline=(*WHITE,170),width=6)
  d.line((x+90,850,x+90,930),fill=(*WHITE,150),width=8)
  for j in range(3): dot(d,x+90,820-j*70,WHITE,13)
 d.line((180,1320,1260,1320),fill=(*WHITE,120),width=8)
 for x in (360,680,1000): d.ellipse((x-40,1280,x+40,1360),outline=(*WHITE,150),width=5)
 footer(d); return im
def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,ROSE); card(d,(100,720,1340,1490),ROSE)
 d.rounded_rectangle((180,860,760,1370),radius=30,fill=(*CYAN,100),outline=(*WHITE,160),width=6)
 pts=[]
 for i in range(10): pts.append((235+i*52,1210-int(260*math.sin(i/9*math.pi))))
 d.line(pts,fill=(*TEAL,235),width=12)
 d.rounded_rectangle((880,860,1250,1370),radius=30,fill=(*VIOLET,110),outline=(*WHITE,160),width=6)
 for y,c in ((970,TEAL),(1115,AMBER),(1260,ROSE)): check(d,980,y,c); d.line((1070,y,1190,y),fill=(*WHITE,155),width=8)
 return im
for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0056_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
