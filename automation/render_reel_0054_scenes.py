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
  for x in range(W): px[x,y]=(int(8+12*t+8*g),int(13+17*t+15*g),int(34+30*t+26*g))
 return im

def glow(im,x,y,r,c,a=62):
 lay=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(lay).ellipse((x-r,y-r,x+r,y+r),fill=(*c,a)); lay=lay.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(lay,(0,0),lay)

def card(d,box,c): d.rounded_rectangle(box,radius=44,fill=(14,37,69,242),outline=(*c,225),width=7)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def dot(d,x,y,c,r=22): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230))
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,210),outline=(*WHITE,220),width=8)
 d.line((x-28,y+2,x-5,y+25),fill=(*BG,230),width=13); d.line((x-5,y+25,x+35,y-32),fill=(*BG,230),width=13)

def s1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,CYAN); card(d,(100,720,1340,1490),CYAN)
 d.line((190,1110,1250,1110),fill=(*WHITE,150),width=10)
 for x,c in ((300,TEAL),(1120,AMBER)): dot(d,x,1110,c,55)
 for y in (850,980,1240,1370):
  d.ellipse((570,y,650,y+80),fill=(*VIOLET,180),outline=(*WHITE,140),width=5)
  d.ellipse((790,y,870,y+80),fill=(*ROSE,180),outline=(*WHITE,140),width=5)
 d.line((650,890,790,890),fill=(*WHITE,130),width=8); d.line((650,1020,790,1020),fill=(*WHITE,130),width=8)
 footer(d); return im

def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,TEAL); card(d,(100,720,1340,1490),TEAL)
 d.rounded_rectangle((180,850,600,1370),radius=30,fill=(*VIOLET,150),outline=(*WHITE,160),width=6)
 d.rounded_rectangle((840,850,1260,1370),radius=30,fill=(*AMBER,150),outline=(*WHITE,160),width=6)
 for x,y,c in ((300,970,CYAN),(420,1140,ROSE),(960,970,TEAL),(1080,1140,CYAN)): dot(d,x,y,c,45)
 d.line((600,1110,840,1110),fill=(*WHITE,170),width=12)
 footer(d); return im

def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,AMBER); card(d,(100,720,1340,1490),AMBER)
 cols=[(200,CYAN),(500,TEAL),(800,VIOLET),(1100,ROSE)]
 for x,c in cols:
  d.rounded_rectangle((x,960,x+160,1220),radius=25,fill=(*c,160),outline=(*WHITE,150),width=5)
  for j in range(3): dot(d,x+80,850-j*70,WHITE,14)
 d.line((180,850,1260,850),fill=(*WHITE,150),width=9)
 footer(d); return im

def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,ROSE); card(d,(100,720,1340,1490),ROSE)
 for y,c in ((1900,CYAN),(2070,AMBER),(2240,TEAL)):
  check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
 return im

for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0054_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
