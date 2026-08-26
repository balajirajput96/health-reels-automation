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
 # two assortments: small and large, visually countable without numeric claims
 for x,n,c in ((250,5,TEAL),(820,12,AMBER)):
  for j in range(n):
   xx=x+(j%4)*95; yy=880+(j//4)*135
   d.rounded_rectangle((xx,yy,xx+66,yy+66),radius=15,fill=(*c,190),outline=(*WHITE,160),width=4)
 footer(d); return im

def s2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,VIOLET); card(d,(100,720,1340,1490),VIOLET)
 centers=[(300,930,CYAN),(720,930,TEAL),(1140,930,AMBER),(510,1240,ROSE),(930,1240,VIOLET)]
 for x,y,c in centers: dot(d,x,y,c,55)
 for a,b in zip(centers,centers[1:]): d.line((a[0],a[1],b[0],b[1]),fill=(*WHITE,150),width=8)
 footer(d); return im

def s3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,AMBER); card(d,(100,720,1340,1490),AMBER)
 # outcome meter: deferral, switching, regret, satisfaction/confidence
 for i,(x,c) in enumerate(((220,CYAN),(500,ROSE),(780,AMBER),(1060,TEAL))):
  d.rounded_rectangle((x,1040,x+160,1250),radius=28,fill=(*c,175),outline=(*WHITE,170),width=5)
  d.line((x+80,900,x+80,1040),fill=(*WHITE,150),width=7)
 d.line((180,900,1240,900),fill=(*WHITE,150),width=10)
 footer(d); return im

def s4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,430,560,TEAL); card(d,(100,720,1340,1490),TEAL)
 for y,c in ((1900,CYAN),(2070,AMBER),(2240,ROSE)):
  check(d,230,y,c); d.line((340,y,1170,y),fill=(*WHITE,150),width=8)
 return im

for i,fn in enumerate((s1,s2,s3,s4),1):
 p=OUT/f'reel_0052_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
