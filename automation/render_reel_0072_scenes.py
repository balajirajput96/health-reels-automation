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
def person(d,cx,cy,col): d.ellipse((cx-92,cy-92,cx+92,cy+92),fill=(247,207,171),outline='white',width=5); d.rounded_rectangle((cx-145,cy+92,cx+145,cy+430),radius=65,fill=col)
def scene1():
 im=bg((9,25,54),(26,14,55)); d=ImageDraw.Draw(im); head(d,'01 / ACTIVITY-SPECIFIC SELF-REPORT','Interest / enjoyment','किस activity में कैसा अनुभव हुआ?')
 P(d,(140,650,1300,1770),fill=(23,42,70),outline=(76,210,190)); T(d,(720,790),'activity',54,(184,235,220),True,anchor='mm')
 for i,(lab,col) in enumerate((('interesting',(130,211,255)),('enjoyable',(166,139,255)),('engaging',(255,184,105)))):
  y=1040+i*200; d.ellipse((280,y-38,356,y+38),fill=col); d.rounded_rectangle((410,y-40,1120,y+40),radius=35,fill=(43,58,91),outline=col,width=4); d.rounded_rectangle((410,y-40,410+int((i+1)*210),y+40),radius=35,fill=col); T(d,(1170,y),lab,42,col,True,anchor='lm')
 P(d,(170,1930,1270,2260),fill=(40,28,66),outline=(166,139,255)); T(d,(720,2095),'self-report • इस context का',50,(240,218,255),True,anchor='mm'); return im
def scene2():
 im=bg((8,41,57),(13,61,58)); d=ImageDraw.Draw(im); head(d,'02 / BEHAVIOR UNDER A PROTOCOL','Free-choice behavior','Reward हटने के बाद return-to-task')
 P(d,(170,620,1270,1960),fill=(16,61,69),outline=(76,210,190)); T(d,(720,760),'protocol',50,(184,235,220),True,anchor='mm')
 d.line((330,1220,1110,1220),fill=(130,211,255),width=12)
 for x in range(360,1110,150): d.line((x,1175,x,1265),fill=(130,211,255),width=7)
 d.ellipse((430,1135,570,1275),fill=(255,184,105),outline='white',width=4); d.ellipse((850,1135,990,1275),fill=(166,139,255),outline='white',width=4)
 d.line((920,1135,920,900),fill=(166,139,255),width=10); d.polygon([(920,900),(880,970),(960,970)],fill=(166,139,255)); T(d,(500,1480),'task',46,(255,206,123),True,anchor='mm'); T(d,(920,1480),'return',46,(240,218,255),True,anchor='mm')
 T(d,(720,1780),'behavioral indicator',42,(184,235,220),True,anchor='mm'); P(d,(200,2070,1240,2320),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2195),'opportunity + instructions + task design',37,(240,218,255),anchor='mm'); return im
def scene3():
 im=bg((34,18,58),(9,28,53)); d=ImageDraw.Draw(im); head(d,'03 / RELATED DIMENSIONS','Related ≠ identical','Choice, competence, effort, value, pressure')
 cards=[('choice','क्या विकल्प महसूस हुआ?',(166,139,255)),('competence','क्या सक्षम महसूस हुआ?',(76,210,190)),('effort / value','कितना प्रयास या मूल्य?',(255,184,105)),('pressure','कितना दबाव?',(130,211,255))]
 for i,(a,b,col) in enumerate(cards):
  y=650+i*300; P(d,(140,y,1300,y+220),fill=(27,36,67),outline=col); T(d,(245,y+60),a,43,col,True); T(d,(245,y+145),b,32,(210,221,241)); d.ellipse((1120,y+60,1210,y+150),fill=col)
 P(d,(190,1980,1250,2300),fill=(45,27,68),outline=(166,139,255)); T(d,(720,2140),'related dimensions • exact synonym नहीं',43,(240,218,255),True,anchor='mm'); return im
def scene4():
 im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); head(d,'04 / CORRELATE BOUNDARY','Correlate ≠ private motive','Outcome और neural signal को अलग पढ़िए')
 P(d,(110,650,670,1260),fill=(33,31,58),outline=(255,184,105)); T(d,(390,820),'reward /\nfeedback',45,(255,206,123),True,anchor='mm'); d.line((670,950,770,950),fill=(76,210,190),width=10); d.polygon([(770,950),(710,910),(710,990)],fill=(76,210,190))
 P(d,(770,650,1330,1260),fill=(24,64,62),outline=(76,210,190)); T(d,(1050,820),'interest /\npersistence /\nperformance',43,(184,235,220),True,anchor='mm')
 P(d,(180,1450,1260,2040),fill=(26,31,63),outline=(130,211,255)); T(d,(720,1590),'neural signal',48,(130,211,255),True,anchor='mm');
 for i in range(7):
  x=330+i*130; y=1780+int(75*math.sin(i)); d.ellipse((x-18,y-18,x+18,y+18),fill=(166,139,255));
  if i: d.line((x-130,1780+int(75*math.sin(i-1)),x, y),fill=(166,139,255),width=6)
 T(d,(720,1950),'conceptual correlate, direct mind-reading नहीं',37,(255,218,225),anchor='mm')
 P(d,(160,2220,1280,2410),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2315),'AI-generated educational visuals • personal assessment नहीं',33,(240,218,255),anchor='mm'); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 path=OUT/f'reel_0072_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
