from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(9,14,34); WHITE=(242,247,252); CYAN=(65,190,245); TEAL=(48,220,173); AMBER=(248,189,72); VIOLET=(166,126,245); ROSE=(239,104,138)
def base():
 im=Image.new('RGB',(W,H),BG); p=im.load()
 for y in range(H):
  t=y/(H-1); c=(int(9+13*t),int(14+18*t),int(34+28*t))
  for x in range(W): p[x,y]=c
 return im
def glow(im,x,y,r,c):
 q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,65)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)
def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(15,39,71,240),outline=(*c,225),width=7)
def dot(d,x,y,c,r=28): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)
def check(d,x,y,c):
 d.ellipse((x-58,y-58,x+58,y+58),fill=(*c,220),outline=(*WHITE,210),width=7); d.line((x-29,y+2,x-7,y+24),fill=(*BG,240),width=13); d.line((x-7,y+24,x+38,y-32),fill=(*BG,240),width=13)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def scene1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,570,ROSE); card(d,(100,710,1340,1500),ROSE)
 d.rounded_rectangle((220,900,580,1260),radius=32,fill=(*CYAN,130),outline=(*WHITE,180),width=7)
 d.rounded_rectangle((860,900,1220,1260),radius=32,fill=(*AMBER,120),outline=(*WHITE,180),width=7)
 for x in (300,430,940,1070): dot(d,x,1080,WHITE,25)
 d.line((580,1080,860,1080),fill=(*WHITE,220),width=12); dot(d,720,1080,TEAL,34); footer(d); return im
def scene2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,CYAN); card(d,(70,700,1370,1510),CYAN)
 xs=[130,560,990]; cs=[CYAN,AMBER,VIOLET]
 for i,(x,c) in enumerate(zip(xs,cs)):
  d.rounded_rectangle((x,860,x+320,1340),radius=32,fill=(*c,120),outline=(*WHITE,180),width=7)
  for j in range(3): dot(d,x+80+j*80,1010+(j%2)*120,WHITE,18)
  if i<2: d.line((x+320,1100,x+430,1100),fill=(*WHITE,190),width=10)
 footer(d); return im
def scene3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,TEAL); card(d,(100,710,1340,1500),TEAL)
 for y,c in ((900,CYAN),(1060,AMBER),(1220,VIOLET)): check(d,270,y,c); d.line((390,y,1150,y),fill=(*WHITE,135),width=8)
 d.rounded_rectangle((390,1320,1050,1400),radius=24,fill=(*ROSE,150),outline=(*WHITE,150),width=5); footer(d); return im
def scene4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(95,700,1345,1510),VIOLET)
 centers=[(330,1100,CYAN),(720,900,TEAL),(1110,1100,AMBER)]
 for x,y,c in centers: dot(d,x,y,c,72)
 for a,b in zip(centers,centers[1:]): d.line((a[0],a[1],b[0],b[1]),fill=(*WHITE,190),width=12)
 d.line((330,1100,1110,1100),fill=(*WHITE,130),width=8)
 d.rounded_rectangle((390,1260,1050,1360),radius=25,fill=(*ROSE,150),outline=(*WHITE,150),width=5); footer(d); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 p=OUT/f'reel_0060_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
