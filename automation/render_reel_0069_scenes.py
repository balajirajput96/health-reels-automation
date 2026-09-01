from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets'
W,H=1440,2560
FONT='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf'
def f(size,bold=False):
    path=BOLD if bold and Path(BOLD).exists() else FONT
    return ImageFont.truetype(path,size)
def text(draw,xy,s,size,fill=(239,244,255),bold=False,anchor=None):
    draw.text(xy,s,font=f(size,bold),fill=fill,anchor=anchor,spacing=12)
def panel(draw,box,fill=(24,37,67),outline=(71,101,148),radius=36,width=4):
    draw.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)
def bg(top,bottom):
    im=Image.new('RGB',(W,H)); px=im.load()
    for y in range(H):
        t=y/(H-1); c=tuple(int(top[i]*(1-t)+bottom[i]*t) for i in range(3))
        for x in range(W): px[x,y]=c
    return im
def header(d,kicker,title,sub):
    text(d,(90,110),kicker,44,fill=(130,211,255),bold=True)
    text(d,(90,205),title,76,bold=True)
    text(d,(90,360),sub,38,fill=(184,201,226))
def person(d,cx,cy,scale=1.0,accent=(255,184,105)):
    r=int(105*scale); d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(247,207,171),outline=(255,255,255),width=5)
    d.arc((cx-r//2,cy-r//4,cx+r//2,cy+r//2),0,180,fill=(45,55,80),width=max(3,int(8*scale)))
    d.rounded_rectangle((cx-int(170*scale),cy+r,cx+int(170*scale),cy+int(470*scale)),radius=int(70*scale),fill=accent)
def scene1():
    im=bg((9,20,46),(25,13,55)); d=ImageDraw.Draw(im); header(d,'01 / SELF-REPORT','पहला meter: अपनी report','Questionnaire व्यक्ति की धारणा और tendency पूछता है')
    panel(d,(100,560,1340,1840),fill=(18,31,62),outline=(80,132,184))
    person(d,360,910,0.9,(81,174,205)); text(d,(360,1390),'मैं perspective\nलेता/लेती हूँ',42,anchor='mm',bold=True)
    d.line((650,900,650,1600),fill=(80,132,184),width=5)
    text(d,(780,680),'Questionnaire',52,fill=(255,206,123),bold=True)
    for i,(label,val,col) in enumerate([('Perspective taking',0.76,(76,210,190)),('Empathic concern',0.61,(255,184,105)),('Self-report',0.48,(166,139,255))]):
        y=900+i*210; text(d,(780,y),label,37); d.rounded_rectangle((780,y+75,1230,y+125),radius=25,fill=(49,65,97)); d.rounded_rectangle((780,y+75,780+450*val,y+125),radius=25,fill=col)
    panel(d,(145,1990,1295,2250),fill=(36,24,60),outline=(166,139,255)); text(d,(720,2115),'Self-report ≠ observed behavior',48,anchor='mm',bold=True,fill=(240,218,255))
    return im

def scene2():
    im=bg((10,32,55),(12,56,61)); d=ImageDraw.Draw(im); header(d,'02 / EMPATHIC ACCURACY','दूसरा meter: target से match','एक video, एक emotion, और एक defined comparison')
    panel(d,(100,560,1340,2050),fill=(14,49,63),outline=(72,190,190))
    person(d,355,940,0.78,(242,131,134)); text(d,(355,1420),'Target\nअपनी feeling rate करता है',38,anchor='mm',bold=True)
    person(d,1080,940,0.78,(81,174,205)); text(d,(1080,1420),'Participant\nदूसरे की emotion rate करता है',38,anchor='mm',bold=True)
    d.line((535,1010,900,1010),fill=(255,206,123),width=9); d.polygon([(900,1010),(850,980),(850,1040)],fill=(255,206,123)); text(d,(720,900),'video',40,anchor='mm',fill=(255,206,123),bold=True)
    panel(d,(270,1660,1170,1930),fill=(25,75,77),outline=(76,210,190)); text(d,(720,1730),'Rating A  ↔  Rating B',48,anchor='mm',bold=True); text(d,(720,1825),'agreement / error',40,anchor='mm',fill=(184,235,220))
    return im

def scene3():
    im=bg((35,18,58),(9,26,53)); d=ImageDraw.Draw(im); header(d,'03 / DIFFERENT OUTCOMES','अलग methods, अलग सवाल','Empathy कोई single meter नहीं है')
    items=[('Self-report','व्यक्ति क्या report करता है',(166,139,255)),('Target agreement','दूसरे की emotion से कितना match',(255,184,105)),('Own affect','देखते समय अपनी feeling',(81,210,190)),('Context & reliability','task और instrument की सीमा',(242,131,134))]
    for i,(a,b,col) in enumerate(items):
        y=620+i*355; panel(d,(130,y,1310,y+265),fill=(25,35,68),outline=col); d.ellipse((190,y+62,300,y+172),fill=col); text(d,(370,y+62),a,46,bold=True,fill=col); text(d,(370,y+145),b,34,fill=(210,221,241))
    panel(d,(170,2110,1270,2315),fill=(44,28,68),outline=(166,139,255)); text(d,(720,2210),'Score का मतलब context से आता है',42,anchor='mm',bold=True)
    return im

def scene4():
    im=bg((19,31,49),(49,15,38)); d=ImageDraw.Draw(im); header(d,'04 / INTERPRETATION LIMITS','एक score से बड़ा दावा नहीं','Correlate दिखना direct mind-reading नहीं है')
    panel(d,(130,630,1310,1710),fill=(34,31,58),outline=(242,131,134))
    text(d,(720,820),'एक score',62,anchor='mm',bold=True,fill=(255,206,123)); text(d,(720,970),'≠',95,anchor='mm',fill=(242,131,134),bold=True)
    claims=['पूरी empathy','हर situation की kindness','किसी व्यक्ति का diagnosis','private feeling का transcript']
    for i,s in enumerate(claims):
        y=1110+i*125; d.line((300,y,370,y),fill=(242,131,134),width=7); text(d,(410,y),s,40,fill=(255,218,225))
    panel(d,(170,1870,1270,2250),fill=(22,64,62),outline=(76,210,190)); text(d,(720,1970),'Study का outcome बताइए, उससे ज्यादा दावा नहीं।',43,anchor='mm',bold=True); text(d,(720,2090),'AI-generated educational visuals • diagnosis या personal assessment नहीं',30,anchor='mm',fill=(184,235,220))
    return im
for i,fn in enumerate((scene1,scene2,scene3,scene4),1):
    path=OUT/f'reel_0069_scene_0{i}.png'; fn().save(path,format='PNG'); print(path)
