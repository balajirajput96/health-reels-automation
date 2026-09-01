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
  t=y/(H-1); g=max(0,1-math.hypot(W*.5,y-H*.2)/(W*1.05))
  col=(int(8+12*t+8*g),int(13+17*t+15*g),int(34+30*t+26*g))
  for x in range(W): px[x,y]=col
 return im

def glow(im,x,y,r,c,a=62):
 lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); lay=lay.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(lay,(0,0),lay)

def card(d,box,c): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,140),width=4)
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
 d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)

def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,CYAN); card(d,(100,720,1340,1490),CYAN)
 # central construct node splitting into distinct operational meanings
 dot(d,720,1030,WHITE,72)
 for x,y,c in ((300,850,TEAL),(1140,850,AMBER),(300,1270,VIOLET),(1140,1270,ROSE)):
  d.line((720,1030,x,y),fill=(*WHITE,170),width=10); dot(d,x,y,c,55)
 for x,y in ((300,850),(1140,850),(300,1270),(1140,1270)):
  for k in range(3): dot(d,x+(k-1)*55,y+115,WHITE,12)
 footer(d); return im

def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,TEAL); card(d,(100,720,1340,1490),TEAL)
 # self-report card and response distribution
 d.rounded_rectangle((185,835,1255,1375),radius=34,fill=(*VIOLET,120),outline=(*WHITE,165),width=6)
 d.line((300,1110,1140,1110),fill=(*WHITE,190),width=12)
 for i,c in enumerate((TEAL,CYAN,AMBER,ROSE)):
  x=390+i*220; dot(d,x,1110,c,32)
 d.ellipse((840,1030,980,1170),fill=(*AMBER,220),outline=(*WHITE,210),width=7)
 d.line((910,900,910,1025),fill=(*WHITE,170),width=8)
 d.rounded_rectangle((360,1240,1080,1300),radius=20,fill=(*WHITE,150))
 footer(d); return im

def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,AMBER); card(d,(100,720,1340,1490),AMBER)
 # four distinct task outputs: accuracy, time, confidence, physiology
 xs=[220,500,780,1060]; cs=[CYAN,TEAL,VIOLET,ROSE]
 for x,c in zip(xs,cs):
  d.rounded_rectangle((x,940,x+160,1250),radius=25,fill=(*c,155),outline=(*WHITE,170),width=6)
  d.line((x+80,880,x+80,940),fill=(*WHITE,140),width=7)
  for j in range(4): dot(d,x+80,870-j*70,WHITE,13)
 d.line((180,840,1260,840),fill=(*WHITE,140),width=9)
 for x in (360,640,920): d.line((x,860,x,1320),fill=(*WHITE,90),width=5)
 footer(d); return im

def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,ROSE); card(d,(100,720,1340,1490),ROSE)
 # model estimate beside a boundary frame
 d.rounded_rectangle((190,870,760,1370),radius=30,fill=(*CYAN,100),outline=(*WHITE,160),width=6)
 pts=[]
 for i in range(9):
  x=250+i*58; y=1210-int(250*math.sin(i/8*math.pi))
  pts.append((x,y))
 d.line(pts,fill=(*TEAL,230),width=12)
 d.rounded_rectangle((860,870,1250,1370),radius=30,fill=(*VIOLET,110),outline=(*WHITE,160),width=6)
 for y,c in ((960,TEAL),(1100,AMBER),(1240,ROSE)): check(d,980,y,c)
 d.line((1070,960,1190,960),fill=(*WHITE,160),width=8); d.line((1070,1100,1190,1100),fill=(*WHITE,160),width=8); d.line((1070,1240,1190,1240),fill=(*WHITE,160),width=8)
 footer(d); return im

for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0055_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
