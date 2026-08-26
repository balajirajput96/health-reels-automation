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
  t=y/(H-1)
  for x in range(W):
   g=max(0,1-math.hypot(x-W*.5,y-H*.2)/(W*1.05))
   px[x,y]=(int(8+12*t+8*g),int(13+17*t+15*g),int(34+30*t+26*g))
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
 d.line((200,1030,1240,1030),fill=(*WHITE,160),width=10)
 for x,c in ((340,TEAL),(1100,ROSE)): dot(d,x,1030,c,44)
 d.line((340,1230,1100,1230),fill=(*AMBER,210),width=12)
 footer(d); return im

def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,VIOLET); card(d,(100,720,1340,1490),VIOLET)
 centers=[(300,950,CYAN),(720,950,TEAL),(1140,950,AMBER)]
 for x,y,c in centers: dot(d,x,y,c,70)
 for a,b in zip(centers,centers[1:]): d.line((a[0],a[1],b[0],b[1]),fill=(*WHITE,160),width=9)
 d.line((300,1240,1140,1240),fill=(*ROSE,200),width=12)
 footer(d); return im

def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,AMBER); card(d,(100,720,1340,1490),AMBER)
 for x,c in ((220,CYAN),(520,TEAL),(820,VIOLET),(1120,ROSE)):
  d.rounded_rectangle((x,960,x+150,1220),radius=25,fill=(*c,160),outline=(*WHITE,150),width=5)
  d.line((x+75,850,x+75,960),fill=(*WHITE,150),width=8)
 d.line((180,850,1240,850),fill=(*WHITE,150),width=9)
 footer(d); return im

def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,TEAL); card(d,(100,720,1340,1490),TEAL)
 for y,c in ((1900,CYAN),(2070,AMBER),(2240,ROSE)):
  check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
 return im

for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0053_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
