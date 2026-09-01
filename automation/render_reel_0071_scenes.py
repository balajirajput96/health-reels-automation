from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets'; W,H=1440,2560
FONT='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'; BOLD='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf'
def F(n,b=False): return ImageFont.truetype(BOLD if b and Path(BOLD).exists() else FONT,n)
def T(d,xy,s,n,fill=(239,244,255),b=False,anchor=None): d.text(xy,s,font=F(n,b),fill=fill,anchor=anchor,spacing=12)
def P(d,box,fill=(24,38,70),outline=(75,111,158),r=36,w=4): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def bg(a,b):
 im=Image.new('RGB',(W,H)); px=im.load()
 for y in range(H):
  q=y/(H-1); c=tuple(int(a[i]*(1-q)+b[i]*q) for i in range(3))
  for x in range(W): px[x,y]=c
 return im
def head(d,k,title,sub): T(d,(90,110),k,44,(130,211,255),True); T(d,(90,205),title,76,(239,244,255),True); T(d,(90,360),sub,38,(184,201,226))
def person(d,cx,cy,col): d.ellipse((cx-92,cy-92,cx+92,cy+92),fill=(247,207,171),outline='white',width=5); d.rounded_rectangle((cx-145,cy+92,cx+145,cy+430),radius=65,fill=col)
def scene1():
 im=bg((9,25,54),(26,14,55)); d=ImageDraw.Draw(im); head(d,'01 / PERCEIVED EXPERIENCE','Belonging: एक feeling','Group, जगह या अनुभव का हिस्सा महसूस करना')
 person(d,720,930,(81,174,205));
 for ang in range(0,360,60):
  r=480; cx=720+int(r*math.cos(math.radians(ang))); cy=1120+int(r*math.sin(math.radians(ang)))
  d.line((720,1120,cx,cy),fill=(76,210,190),width=8); d.ellipse((cx-50,cy-50,cx+50,cy+50),fill=(166,139,255),outline=(239,244,255),width=4)
 T(d,(720,1710),'perceived fit / connection',48,(184,235,220),True,anchor='mm'); P(d,(140,1980,1300,2280),fill=(40,28,66),outline=(166,139,255)); T(d,(720,2130),'यह रिश्तों की गिनती नहीं',52,(240,218,255),True,anchor='mm'); return im
def scene2():
 im=bg((8,41,57),(13,61,58)); d=ImageDraw.Draw(im); head(d,'02 / STRUCTURAL CONNECTION','Contacts ≠ belonging','Network और अनुभव अलग चीजें पूछते हैं')
 P(d,(120,600,650,2040),fill=(16,61,69),outline=(76,210,190)); T(d,(385,760),'network',52,(184,235,220),True,anchor='mm')
 for i in range(8):
  ang=2*math.pi*i/8; x=385+int(290*math.cos(ang)); y=1300+int(490*math.sin(ang)); d.line((385,1300,x,y),fill=(76,210,190),width=7); d.ellipse((x-38,y-38,x+38,y+38),fill=(255,184,105))
 d.ellipse((345,1260,425,1340),fill=(166,139,255))
 P(d,(790,600,1320,2040),fill=(35,43,73),outline=(255,184,105)); T(d,(1055,760),'felt support',52,(255,206,123),True,anchor='mm'); T(d,(1055,1120),'acceptance\nfit\nconnection',52,(239,244,255),True,anchor='mm'); T(d,(1055,1730),'quantity alone\nnot enough',44,(255,218,225),True,anchor='mm'); return im
def scene3():
 im=bg((34,18,58),(9,28,53)); d=ImageDraw.Draw(im); head(d,'03 / RELATED, NOT IDENTICAL','अलग measures','Support, loneliness और belonging एक जैसे नहीं')
 cards=[('Belonging','fit / connection',(166,139,255)),('Support','पर्याप्त मदद',(76,210,190)),('Loneliness','desired vs actual',(255,184,105))]
 for i,(a,b,col) in enumerate(cards):
  y=680+i*380; P(d,(140,y,1300,y+270),fill=(27,36,67),outline=col); T(d,(245,y+80),a,48,col,True); T(d,(245,y+170),b,38,(210,221,241)); d.ellipse((1120,y+75,1210,y+165),fill=col)
 P(d,(190,1940,1250,2280),fill=(45,27,68),outline=(166,139,255)); T(d,(720,2110),'जुड़े हो सकते हैं • identical नहीं',47,(240,218,255),True,anchor='mm'); return im
def scene4():
 im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); head(d,'04 / SPECIFIED OUTCOMES','Intervention study','Process और outcome को अलग पढ़िए')
 P(d,(120,620,1320,1120),fill=(33,31,58),outline=(130,211,255)); T(d,(720,780),'belonging uncertainty',48,(130,211,255),True,anchor='mm'); T(d,(720,930),'specified process / population',36,(184,201,226),anchor='mm')
 d.line((720,1130,720,1420),fill=(76,210,190),width=10); d.polygon([(720,1420),(680,1360),(760,1360)],fill=(76,210,190))
 P(d,(120,1500,1320,2120),fill=(24,64,62),outline=(76,210,190)); T(d,(720,1650),'grades • well-being\nmentorship • persistence',48,(184,235,220),True,anchor='mm'); T(d,(720,1990),'outcomes, not a direct meter',40,(255,206,123),True,anchor='mm')
 P(d,(160,2220,1280,2410),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2315),'AI-generated visuals • personal assessment नहीं',35,(240,218,255),anchor='mm'); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 path=OUT/f'reel_0071_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
