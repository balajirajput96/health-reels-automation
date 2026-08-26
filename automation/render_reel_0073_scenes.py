from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets'; W,H=1440,2560
FONT='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'; BOLD='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf'
def F(n,b=False): return ImageFont.truetype(BOLD if b and Path(BOLD).exists() else FONT,n)
def T(d,xy,s,n,fill=(239,244,255),b=False,anchor=None): d.multiline_text(xy,s,font=F(n,b),fill=fill,anchor=anchor,spacing=16,align='center')
def P(d,box,fill=(24,38,70),outline=(75,111,158),r=36,w=4): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def bg(a,b):
 im=Image.new('RGB',(W,H)); px=im.load()
 for y in range(H):
  q=y/(H-1); c=tuple(int(a[i]*(1-q)+b[i]*q) for i in range(3))
  for x in range(W): px[x,y]=c
 return im
def head(d,k,title,sub): T(d,(90,110),k,44,(130,211,255),True); T(d,(90,205),title,76,(239,244,255),True); T(d,(90,360),sub,38,(184,201,226))
def scene1():
 im=bg((9,25,54),(26,14,55)); d=ImageDraw.Draw(im); head(d,'01 / OBSERVED BEHAVIOR','Goal gradient?','Study में behavior का कौन-सा signal?')
 P(d,(120,650,1320,1780),fill=(23,42,70),outline=(76,210,190)); T(d,(720,790),'reward path',54,(184,235,220),True,anchor='mm')
 for i,(lab,col,val) in enumerate((('purchases',(255,184,105),0.78),('visits',(130,211,255),0.66),('persistence',(166,139,255),0.54))):
  y=1050+i*210; T(d,(240,y),lab,40,col,True,anchor='lm'); d.rounded_rectangle((540,y-30,1170,y+30),radius=30,fill=(43,58,91),outline=col,width=4); d.rounded_rectangle((540,y-30,540+int(630*val),y+30),radius=30,fill=col)
 d.line((250,1710,1190,1710),fill=(76,210,190),width=8); d.polygon([(1190,1710),(1120,1670),(1120,1750)],fill=(76,210,190)); T(d,(720,1970),'observable outcome',50,(184,235,220),True,anchor='mm'); P(d,(190,2140,1250,2350),fill=(40,28,66),outline=(166,139,255)); T(d,(720,2245),'behavior ≠ private motive',45,(240,218,255),True,anchor='mm'); return im
def scene2():
 im=bg((8,41,57),(13,61,58)); d=ImageDraw.Draw(im); head(d,'02 / PERCEIVED DISTANCE','Perceived distance','Bonus stamps और completion speed')
 P(d,(140,650,670,1920),fill=(16,61,69),outline=(76,210,190)); T(d,(405,800),'regular card',46,(184,235,220),True,anchor='mm');
 for i in range(10):
  x=240+(i%5)*80; y=1040+(i//5)*190; d.rounded_rectangle((x,y,x+58,y+58),radius=12,fill=(49,83,94),outline=(184,235,220),width=3)
 T(d,(405,1600),'10 required',40,(184,235,220),True,anchor='mm')
 P(d,(770,650,1300,1920),fill=(35,43,73),outline=(255,184,105)); T(d,(1035,800),'bonus-progress',46,(255,206,123),True,anchor='mm')
 for i in range(12):
  x=870+(i%6)*65; y=1040+(i//6)*190; d.rounded_rectangle((x,y,x+48,y+48),radius=10,fill=(255,184,105) if i<2 else (59,70,96),outline=(255,206,123),width=3)
 T(d,(1035,1600),'10 required\n2 appear complete',38,(255,218,225),True,anchor='mm')
 d.line((720,1980,720,2220),fill=(76,210,190),width=10); d.polygon([(720,2220),(680,2150),(760,2150)],fill=(76,210,190)); T(d,(720,2320),'perceived distance → completion behavior',39,(184,235,220),True,anchor='mm'); return im
def scene3():
 im=bg((34,18,58),(9,28,53)); d=ImageDraw.Draw(im); head(d,'03 / CONTEXTUAL MARKERS','Markers + context','Number, relevance और salience matter')
 for j,(title,n,col,walk) in enumerate((('few markers',3,(76,210,190),'faster'),('many markers',8,(130,211,255),'slower?'),('unrelated / salient',5,(255,184,105),'can reverse'))):
  y=650+j*430; P(d,(130,y,1310,y+310),fill=(27,36,67),outline=col); T(d,(270,y+85),title,42,col,True,anchor='lm');
  d.line((650,y+220,1190,y+220),fill=(184,201,226),width=8)
  for i in range(n):
   x=690+i*int(480/max(n-1,1)); d.ellipse((x-16,y+204,x+16,y+236),fill=col)
  T(d,(1160,y+95),walk,39,(239,244,255),True,anchor='rm')
 P(d,(180,2020,1260,2310),fill=(45,27,68),outline=(166,139,255)); T(d,(720,2165),'effect fixed नहीं • protocol-specific',43,(240,218,255),True,anchor='mm'); return im
def scene4():
 im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); head(d,'04 / MODERATOR','Context matters','Goal proximity का असर किस पर निर्भर?')
 for x,label,col in ((150,'low power',(255,184,105)),(790,'high power',(76,210,190))):
  P(d,(x,690,x+500,1820),fill=(33,31,58),outline=col); T(d,(x+250,820),label,46,col,True,anchor='mm');
  d.line((x+130,1350,x+370,1350),fill=(130,211,255),width=8); d.ellipse((x+130,1310,x+210,1390),fill=(166,139,255)); d.ellipse((x+290,1310,x+370,1390),fill=col)
  T(d,(x+250,1540),'far goal → near goal',32,(184,201,226),anchor='mm')
 T(d,(400,1700),'proximity effect\nstronger in one condition',33,(255,218,225),anchor='mm'); T(d,(1040,1700),'proximity effect\nless affected',33,(184,235,220),anchor='mm')
 P(d,(160,2040,1280,2340),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2185),'behavior, reward, context, moderator पूछिए',40,(240,218,255),True,anchor='mm'); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 path=OUT/f'reel_0073_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
