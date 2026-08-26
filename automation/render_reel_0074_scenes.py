from PIL import Image, ImageDraw, ImageFont
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
 im=bg((9,25,54),(26,14,55)); d=ImageDraw.Draw(im); head(d,'01 / EXPECTANCY','क्या मैं कर पाऊँगा?','Task-specific success belief')
 P(d,(160,650,1280,1840),fill=(23,42,70),outline=(76,210,190)); T(d,(720,820),'EXPECTANCY',62,(184,235,220),True,anchor='mm')
 T(d,(720,1080),'किसी खास task में\nसफल होने का belief',54,(239,244,255),True,anchor='mm')
 for i,(lab,val,col) in enumerate((('perceived ability',0.78,(130,211,255)),('task difficulty',0.58,(255,184,105)),('success expectation',0.68,(166,139,255)))):
  y=1390+i*120; T(d,(280,y),lab,34,col,True,anchor='lm'); d.rounded_rectangle((650,y-24,1180,y+24),radius=24,fill=(43,58,91),outline=col,width=4); d.rounded_rectangle((650,y-24,650+int(530*val),y+24),radius=24,fill=col)
 P(d,(190,2070,1250,2350),fill=(40,28,66),outline=(166,139,255)); T(d,(720,2210),'belief report ≠ guaranteed ability',43,(240,218,255),True,anchor='mm'); return im
def scene2():
 im=bg((8,41,57),(13,61,58)); d=ImageDraw.Draw(im); head(d,'02 / TASK VALUE','यह task क्यों?','Value और cost अलग dimensions हैं')
 cards=[('interest / enjoyment',(76,210,190)),('personal importance',(130,211,255)),('future usefulness',(255,184,105)),('effort / time / emotion',(166,139,255))]
 for i,(lab,col) in enumerate(cards):
  x=130+(i%2)*620; y=650+(i//2)*520; P(d,(x,y,x+500,y+360),fill=(25,52,67),outline=col); T(d,(x+250,y+115),lab,38,col,True,anchor='mm'); d.ellipse((x+215,y+235,x+285,y+305),fill=col); T(d,(x+250,y+270),'?',48,(12,25,45),True,anchor='mm')
 P(d,(190,1980,1250,2330),fill=(37,27,63),outline=(166,139,255)); T(d,(720,2155),'subjective • task-specific • context-bound',42,(240,218,255),True,anchor='mm'); return im
def scene3():
 im=bg((34,18,58),(9,28,53)); d=ImageDraw.Draw(im); head(d,'03 / MEASUREMENT','Belief ≠ outcome','Questionnaire और behavior को अलग रखें')
 P(d,(150,700,620,1870),fill=(25,39,71),outline=(130,211,255)); T(d,(385,830),'SELF-REPORT',44,(130,211,255),True,anchor='mm'); T(d,(385,1080),'“यह subject\nuseful लगता है”',44,(239,244,255),True,anchor='mm'); T(d,(385,1570),'rating / belief',40,(184,201,226),anchor='mm')
 P(d,(820,700,1290,1870),fill=(38,30,63),outline=(76,210,190)); T(d,(1055,830),'OBSERVED',44,(76,210,190),True,anchor='mm'); T(d,(1055,1080),'class में रहना\nया score',44,(239,244,255),True,anchor='mm'); T(d,(1055,1570),'choice / outcome',40,(184,235,220),anchor='mm')
 d.line((620,1280,820,1280),fill=(255,184,105),width=10); d.polygon([(820,1280),(750,1235),(750,1325)],fill=(255,184,105)); T(d,(720,2020),'एक ही चीज़ मानना → measurement error',42,(255,218,225),True,anchor='mm'); return im
def scene4():
 im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); head(d,'04 / INTERPRETATION','Relationship, guarantee नहीं','Context, task और outcome पूछिए')
 P(d,(150,680,1290,1780),fill=(33,31,58),outline=(76,210,190)); T(d,(720,810),'RESEARCH FRAME',52,(184,235,220),True,anchor='mm')
 labels=[('कौन-सा task?',(130,211,255)),('कौन-सी value?',(255,184,105)),('कितना cost?',(166,139,255)),('कौन-सा outcome?',(76,210,190))]
 for i,(lab,col) in enumerate(labels):
  y=1020+i*150; d.ellipse((300,y-24,348,y+24),fill=col); T(d,(390,y),lab,39,col,True,anchor='lm'); d.line((850,y,1120,y),fill=col,width=7); d.ellipse((1100,y-20,1140,y+20),fill=col)
 P(d,(170,2020,1270,2350),fill=(41,25,63),outline=(166,139,255)); T(d,(720,2185),'पूरी motivation का diagnosis नहीं',41,(240,218,255),True,anchor='mm'); return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
 path=OUT/f'reel_0074_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
