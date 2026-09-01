from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
W,H=1440,2560; OUT=Path('/home/ubuntu/repos/health-reels-automation/assets'); BG=(8,16,38); WHITE=(242,247,252); CYAN=(74,204,245); TEAL=(54,221,178); AMBER=(248,188,72); VIOLET=(169,133,246); ROSE=(239,106,143)
def base():
 im=Image.new('RGB',(W,H),BG); p=im.load()
 for y in range(H):
  t=y/(H-1); c=(int(8+14*t),int(16+18*t),int(38+24*t))
  for x in range(W): p[x,y]=c
 return im
def glow(im,x,y,r,c):
 q=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(q).ellipse((x-r,y-r,x+r,y+r),fill=(*c,62)); q=q.filter(ImageFilter.GaussianBlur(r*.55)); im.paste(q,(0,0),q)
def card(d,b,c): d.rounded_rectangle(b,radius=44,fill=(15,39,72,235),outline=(*c,225),width=7)
def dot(d,x,y,c,r=28): d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,230),outline=(*WHITE,150),width=4)
def footer(d): d.rounded_rectangle((82,1840,1358,2460),radius=60,fill=(3,8,25,150))
def trace(d,x,y,c,scale=1.0):
 pts=[(x-190*scale,y+40*scale),(x-135*scale,y-90*scale),(x-65*scale,y+80*scale),(x+10*scale,y-115*scale),(x+95*scale,y+75*scale),(x+170*scale,y-35*scale)]
 d.line(pts,fill=(*c,205),width=max(5,int(16*scale)),joint='curve')
 for px,py in pts: dot(d,px,py,c,max(12,int(26*scale)))
def scene1():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,580,ROSE); card(d,(90,700,1350,1515),ROSE)
 trace(d,720,1080,CYAN,1.25); d.arc((430,830,1010,1390),200,520,fill=(*WHITE,160),width=9); dot(d,720,760,AMBER,42); d.line((720,760,720,880),fill=(*AMBER,190),width=10); footer(d); return im
def scene2():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,CYAN); card(d,(70,700,1370,1515),CYAN)
 xs=[120,550,980]; cs=[CYAN,AMBER,VIOLET]
 for i,(x,c) in enumerate(zip(xs,cs)):
  d.rounded_rectangle((x,900,x+330,1320),radius=36,fill=(*c,120),outline=(*WHITE,180),width=7)
  if i==0: trace(d,x+165,1110,c,.58)
  elif i==1:
   d.polygon([(x+165,930),(x+265,1110),(x+165,1290),(x+65,1110)],fill=(*c,130),outline=(*WHITE,180)); dot(d,x+165,1110,WHITE,22)
  else:
   for j in range(4): dot(d,x+85+j*72,1030+(j%2)*150,WHITE,20)
  if i<2: d.line((x+330,1110,x+425,1110),fill=(*WHITE,200),width=12)
 footer(d); return im
def scene3():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,TEAL); card(d,(85,700,1355,1530),TEAL)
 xs=[170,560,950]; cs=[CYAN,AMBER,VIOLET]
 for i,(x,c) in enumerate(zip(xs,cs)):
  d.ellipse((x,900,x+250,1150),fill=(*c,145),outline=(*WHITE,180),width=7)
  if i==0: trace(d,x+125,1025,c,.48)
  elif i==1: d.arc((x+38,938,x+212,1112),30,300,fill=(*WHITE,220),width=12); dot(d,x+125,1025,WHITE,18)
  else:
   for j in range(5): d.line((x+45+j*40,1080-j*22,x+185-j*20,965+j*22),fill=(*WHITE,190),width=8)
  if i<2: d.line((x+250,1025,x+355,1025),fill=(*WHITE,190),width=10)
 for y,c in ((1240,CYAN),(1370,AMBER)): d.rounded_rectangle((230,y,1210,y+54),radius=27,fill=(*c,170),outline=(*WHITE,140),width=4)
 footer(d); return im
def scene4():
 im=base(); d=ImageDraw.Draw(im,'RGBA'); glow(im,720,420,560,VIOLET); card(d,(90,700,1350,1530),VIOLET)
 centers=[(320,980,CYAN),(720,870,TEAL),(1120,980,AMBER),(720,1240,ROSE)]
 for a,b in zip(centers,centers[1:]): d.line((a[0],a[1],b[0],b[1]),fill=(*WHITE,170),width=10)
 d.line((320,980,720,1240),fill=(*WHITE,145),width=8); d.line((1120,980,720,1240),fill=(*WHITE,145),width=8)
 for x,y,c in centers: dot(d,x,y,c,78)
 for y,c in ((1380,CYAN),(1460,AMBER)): d.rounded_rectangle((300,y,1140,y+46),radius=23,fill=(*c,170),outline=(*WHITE,140),width=4)
 footer(d); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 p=OUT/f'reel_0061_scene_{i:02d}.png'; fn().save(p,optimize=True); print(p)
