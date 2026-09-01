from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
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
 im=bg((9,25,54),(26,14,55)); d=ImageDraw.Draw(im); head(d,'01 / BASIC NEEDS','तीन अनुभव','Autonomy • Competence • Relatedness')
 cards=[('AUTONOMY','choice / volition',(130,211,255)),('COMPETENCE','mastery / efficacy',(76,210,190)),('RELATEDNESS','connection / belonging',(255,184,105))]
 for i,(lab,sub,col) in enumerate(cards):
  y=650+i*390; P(d,(150,y,1290,y+270),fill=(25,43,72),outline=col); T(d,(310,y+112),lab,42,col,True,anchor='mm'); T(d,(820,y+112),sub,38,(239,244,255),True,anchor='mm')
 P(d,(190,1980,1250,2330),fill=(40,28,66),outline=(166,139,255)); T(d,(720,2155),'अनुभव report ≠ पूरा inner state',42,(240,218,255),True,anchor='mm'); return im
def scene2():
 im=bg((8,41,57),(13,61,58)); d=ImageDraw.Draw(im); head(d,'02 / REGULATION','काम क्यों?','Reasons and regulatory style')
 P(d,(180,690,1260,1780),fill=(25,52,67),outline=(76,210,190)); T(d,(720,830),'MOTIVATION',58,(184,235,220),True,anchor='mm')
 steps=[('interest / enjoyment',(76,210,190)),('self-endorsed',(130,211,255)),('reward / pressure',(255,184,105))]
 for i,(lab,col) in enumerate(steps):
  x=260+i*300; d.ellipse((x-65,1110,x+65,1240),fill=col); T(d,(x,1175),str(i+1),44,(10,25,45),True,anchor='mm'); T(d,(x,1400),lab,32,col,True,anchor='mm')
  if i<2: d.line((x+70,1175,x+225,1175),fill=(210,220,240),width=8)
 P(d,(190,1980,1250,2330),fill=(37,27,63),outline=(166,139,255)); T(d,(720,2155),'कारणों को एक ही label मत बनाइए',42,(240,218,255),True,anchor='mm'); return im
def scene3():
 im=bg((34,18,58),(9,28,53)); d=ImageDraw.Draw(im); head(d,'03 / SCALES','किस domain में?','General-life और domain-specific measures')
 cards=[('GENERAL LIFE','21 items',(130,211,255)),('WORK','domain scale',(76,210,190)),('RELATIONSHIP','9 items',(255,184,105))]
 for i,(lab,sub,col) in enumerate(cards):
  x=120+i*430; P(d,(x,720,x+360,1710),fill=(25,39,71),outline=col); T(d,(x+180,900),lab,38,col,True,anchor='mm'); T(d,(x+180,1190),sub,40,(239,244,255),True,anchor='mm'); T(d,(x+180,1480),'AUTONOMY\nCOMPETENCE\nRELATEDNESS',28,(184,201,226),anchor='mm')
 P(d,(190,1980,1250,2330),fill=(37,27,63),outline=(166,139,255)); T(d,(720,2155),'scores interchangeable नहीं',42,(240,218,255),True,anchor='mm'); return im
def scene4():
 im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); head(d,'04 / OUTCOMES','Need score ≠ outcome','Relationship, diagnosis नहीं')
 P(d,(150,680,590,1790),fill=(33,31,58),outline=(130,211,255)); T(d,(370,820),'NEED\nREPORT',46,(130,211,255),True,anchor='mm'); T(d,(370,1260),'autonomy\ncompetence\nrelatedness',34,(239,244,255),anchor='mm')
 P(d,(850,680,1290,1790),fill=(25,52,67),outline=(76,210,190)); T(d,(1070,820),'OBSERVED\nOUTCOME',46,(184,235,220),True,anchor='mm'); T(d,(1070,1260),'engagement\npersistence\nperformance\nwell-being',34,(239,244,255),anchor='mm')
 d.line((590,1230,850,1230),fill=(255,184,105),width=10); d.polygon([(850,1230),(775,1180),(775,1280)],fill=(255,184,105)); T(d,(720,1970),'context-bound relationship • no guarantee',40,(255,218,225),True,anchor='mm')
 P(d,(170,2090,1270,2390),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2240),'educational content • personal assessment नहीं',38,(240,218,255),True,anchor='mm'); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 path=OUT/f'reel_0075_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
