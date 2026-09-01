from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
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
def face(d,cx,cy,accent): d.ellipse((cx-105,cy-105,cx+105,cy+105),fill=(247,207,171),outline='white',width=5); d.rounded_rectangle((cx-165,cy+105,cx+165,cy+500),radius=70,fill=accent)
def scene1():
 im=bg((9,21,49),(28,13,54)); d=ImageDraw.Draw(im); head(d,'01 / EXPLICIT RATING','पहला सवाल: target को कितना human माना?','यह rating target, wording और context से बंधी है')
 P(d,(100,560,1340,1880),fill=(18,31,62),outline=(80,132,184)); face(d,350,950,(81,174,205)); T(d,(350,1500),'तय target',44,anchor='mm',b=True)
 T(d,(785,680),'Humanity rating',50,(255,206,123),True); T(d,(785,820),'कम  ←────────→  ज्यादा',36,(210,221,241))
 d.rounded_rectangle((780,980,1230,1045),radius=30,fill=(55,71,105)); d.rounded_rectangle((780,980,1080,1045),radius=30,fill=(255,184,105)); d.ellipse((1050,950,1110,1075),fill=(255,232,175))
 for i,s in enumerate(['human','complex','mind-bearing']): T(d,(785,1210+i*155),s,40,(184,235,220)); d.line((785,1280+i*155,1200,1280+i*155),fill=(76,210,190),width=8)
 P(d,(145,2020,1295,2260),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2140),'Score context से बाहर नहीं पढ़ा जाता',44,(240,218,255),True,anchor='mm'); return im
def scene2():
 im=bg((10,34,56),(10,59,62)); d=ImageDraw.Draw(im); head(d,'02 / CONTEXT + IMPLICIT TASK','दूसरा: questionnaire और categorization','कभी relationship report, कभी speed और errors')
 P(d,(100,560,1340,2100),fill=(14,49,63),outline=(72,190,190)); T(d,(250,720),'Relationship scale',46,(255,206,123),True); P(d,(180,850,640,1550),fill=(26,70,76),outline=(76,210,190)); T(d,(410,950),'Reported\ntreatment /\nexperience',43,(184,235,220),True,anchor='mm')
 d.line((720,1030,1060,1030),fill=(255,184,105),width=9); d.polygon([(1060,1030),(1005,995),(1005,1065)],fill=(255,184,105)); T(d,(885,900),'implicit task',38,(255,206,123),True,anchor='mm'); P(d,(800,1150,1240,1630),fill=(35,52,78),outline=(166,139,255)); T(d,(1020,1260),'speed +\nerrors',48,(240,218,255),True,anchor='mm'); T(d,(720,1810),'association-strength index',42,(239,244,255),True,anchor='mm'); return im
def scene3():
 im=bg((35,18,58),(9,26,53)); d=ImageDraw.Draw(im); head(d,'03 / DEFINED OUTCOMES','तीसरा: interaction में क्या हुआ?','Behavior record हो सकता है, पर design की सीमा रहती है')
 for i,(a,b,col) in enumerate([('Cooperation','एक task में साथ काम करना',(81,210,190)),('Empathic accuracy','एक partner की emotion पर match',(255,184,105)),('Self-report','व्यक्ति का अपना वर्णन',(166,139,255))]):
  y=670+i*390; P(d,(130,y,1310,y+290),fill=(25,35,68),outline=col); d.ellipse((195,y+80,305,y+190),fill=col); T(d,(375,y+75),a,46,col,True); T(d,(375,y+165),b,35,(210,221,241))
 P(d,(180,1970,1260,2270),fill=(44,28,68),outline=(166,139,255)); T(d,(720,2090),'एक interaction ≠ हर situation',49,(240,218,255),True,anchor='mm'); return im
def scene4():
 im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); head(d,'04 / NEURAL CORRELATE','EEG signal क्या बताता है?','Protocol में मिला correlate, direct mind-reading नहीं')
 P(d,(120,620,1320,1620),fill=(33,31,58),outline=(242,131,134)); T(d,(720,780),'EEG',74,(130,211,255),True,anchor='mm'); pts=[]
 for x in range(250,1190,12):
  import math
  y=1100+int(65*math.sin(x/31)+25*math.sin(x/9)); pts.append((x,y))
 d.line(pts,fill=(76,210,190),width=7); T(d,(720,1335),'correlate under a protocol',38,(184,235,220),anchor='mm')
 T(d,(720,1770),'≠',95,(242,131,134),True,anchor='mm'); T(d,(720,1940),'private belief का transcript',50,(255,218,225),True,anchor='mm'); P(d,(170,2150,1270,2370),fill=(22,64,62),outline=(76,210,190)); T(d,(720,2260),'AI-generated educational visuals • personal assessment नहीं',34,(184,235,220),anchor='mm'); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 path=OUT/f'reel_0070_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
