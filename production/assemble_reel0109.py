from __future__ import annotations
import hashlib, json, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work' / 'reel_0109'
ASSETS = WORK / 'assets'
AUDIO = WORK / 'narration.wav'
MP3_RAW = WORK / 'narration_raw.mp3'
FINAL = WORK / 'final.mp4'
CAPTIONS = WORK / 'captions.srt'
ASS = WORK / 'captions.ass'
METADATA = WORK / 'metadata.json'
VISUAL_REFERENCE = WORK / 'visual_reference.png'
WIDTH, HEIGHT, FPS = 720, 1280, 30
SPANS = [
    ("Span 01 — Hook", "क्या आपने ध्यान दिया है कि एक शानदार छुट्टी का आखिरी दिन अगर खराब हो जाए, तो पूरी ट्रिप बुरी लगने लगती है? ऐसा क्यों होता है?"),
    ("Span 02 — Kahneman Memory Rule", "Nobel Prize विजेता Daniel Kahneman ने खोजा कि हमारा दिमाग पूरी घटना का औसत याद नहीं रखता, बल्कि इसे Peak-End Rule कहते हैं।"),
    ("Span 03 — Two Critical Points", "दिमाग किसी भी अनुभव को सिर्फ दो बिंदुओं से मापता है: पहला, सबसे तीव्र भावनात्मक पल यानी Peak और दूसरा, उसका अंत यानी End।"),
    ("Span 04 — Duration Neglect", "वैज्ञानिकों ने पाया कि घटना कितनी देर चली यानी Duration, दिमाग उसे लगभग नजरअंदाज कर देता है—सिर्फ अंत कैसा था, यही याद रहता है।"),
    ("Span 05 — Remembering Self", "हमारा Remembering Self भविष्य के फैसले इस आधार पर लेता है कि पिछली बार अंत में कैसा अहसास हुआ था।"),
    ("Span 06 — Practical Life Hack", "अपनी मीटिंग्स को तारीफ के साथ खत्म करें, वर्कआउट के अंत में कोई मजेदार एक्सरसाइज करें और सोने से पहले सिर्फ अच्छी बातें सोचें।"),
    ("Span 07 — Safety Boundary", "यह वीडियो केवल cognitive psychology awareness के लिए है और clinical memory evaluation का विकल्प नहीं है।"),
]
CAPTION_TEXT = [s[1] for s in SPANS]
WEIGHTS = [0.15, 0.16, 0.15, 0.16, 0.14, 0.12, 0.12]
ACCENT = (245, 158, 11)  # Amber for peak-end / memory evaluation

def run(cmd): print('+', ' '.join(cmd)); subprocess.run(cmd, check=True)
def duration(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],text=True).strip())
def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def ts(s):
    ms=int(round(s*1000)); hh,ms=divmod(ms,3_600_000); mm,ms=divmod(ms,60_000); ss,ms=divmod(ms,1000)
    return f'{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}'
def ass_ts(s): return f'{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}'
def generate_audio():
    gTTS(text=" ".join(CAPTION_TEXT),lang='hi',slow=False).save(str(MP3_RAW))
    run(['ffmpeg','-y','-i',str(MP3_RAW),'-filter:a','atempo=1.15','-ac','1','-ar','24000','-c:a','pcm_s16le',str(AUDIO)])
def generate_scene_graphic(index, title, subtitle, out_path):
    img=Image.new('RGB',(WIDTH,HEIGHT),color=(15,23,42)); draw=ImageDraw.Draw(img)
    draw.rectangle([(0,0),(WIDTH,140)],fill=(30,41,59))
    draw.rectangle([(0,140),(WIDTH,146)],fill=ACCENT)
    try:
        fh=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",28)
        ft=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",36)
        fb=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",24)
    except: fh=ft=fb=ImageFont.load_default()
    draw.text((40,50),"HEALTH REELS AUTOMATION",fill=ACCENT,font=fh)
    draw.text((40,90),f"REEL-0109 • SCENE {index:02d}",fill=(148,163,184),font=fb)
    draw.rounded_rectangle([(40,240),(WIDTH-40,HEIGHT-240)],radius=20,fill=(30,41,59),outline=(51,65,85),width=2)
    draw.text((70,280),title.upper(),fill=(248,250,252),font=ft)
    words=subtitle.split(); lines=[]; curr=[]
    for w in words:
        curr.append(w)
        if len(" ".join(curr))>30: lines.append(" ".join(curr[:-1])); curr=[w]
    if curr: lines.append(" ".join(curr))
    y=380
    for line in lines[:8]: draw.text((70,y),line,fill=(203,213,225),font=fb); y+=45
    draw.text((40,HEIGHT-180),"Peak End Rule Kahneman Duration Neglect Evidence",fill=(148,163,184),font=fb)
    draw.text((40,HEIGHT-130),"General Education Only • Not Medical Advice",fill=(100,116,139),font=fb)
    out_path.parent.mkdir(parents=True,exist_ok=True); img.save(out_path)
def make_captions(durations):
    start=0.0; srt=[]; ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 720','PlayResY: 1280','WrapStyle: 2','ScaledBorderAndShadow: yes','','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Reel,DejaVu Sans,26,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99060E1A,0,0,3,2,0,2,36,36,126,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    for i,(d,text) in enumerate(zip(durations,CAPTION_TEXT),1):
        end=start+d; srt.extend([str(i),f'{ts(start)} --> {ts(end)}',text,'']); ass.append(f'Dialogue: 0,{ass_ts(start)},{ass_ts(end)},Reel,,0,0,0,,{text}'); start=end
    CAPTIONS.write_text('\n'.join(srt),encoding='utf-8'); ASS.write_text('\n'.join(ass)+'\n',encoding='utf-8')
def main():
    WORK.mkdir(parents=True,exist_ok=True); ASSETS.mkdir(parents=True,exist_ok=True)
    clips_dir=WORK/'clips'; clips_dir.mkdir(parents=True,exist_ok=True)
    print("=== Generating Hindi Audio (gTTS) ==="); generate_audio()
    print("=== Generating Scene Graphics ===")
    images=[]
    for i,(title,subtitle) in enumerate(SPANS,1):
        p=ASSETS/f'frame_{i:02d}.png'; generate_scene_graphic(i,title,subtitle,p); images.append(p)
    total=duration(AUDIO); durations=[total*w for w in WEIGHTS]; durations[-1]+=total-sum(durations)
    clip_paths=[]
    for i,(image,seg_dur) in enumerate(zip(images,durations),1):
        out=clips_dir/f'clip_{i:02d}.mp4'
        vf=f'scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},zoompan=z=\'min(zoom+0.00028,1.04)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=1:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p'
        run(['ffmpeg','-y','-loop','1','-framerate',str(FPS),'-i',str(image),'-t',f'{seg_dur:.3f}','-vf',vf,'-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',str(out)]); clip_paths.append(out)
    listing=WORK/'concat.txt'; listing.write_text(''.join(f"file '{p.as_posix()}'\n" for p in clip_paths),encoding='utf-8')
    silent=WORK/'silent.mp4'; run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)])
    make_captions(durations)
    run(['ffmpeg','-y','-i',str(silent),'-i',str(AUDIO),'-vf',f'subtitles={ASS.as_posix()}','-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',str(FINAL)])
    shutil.copy2(images[0],VISUAL_REFERENCE)
    meta={'reel_id':'reel_0109_peak_end_rule_kahneman','display_id':'REEL-0109','topic_hi':'Peak-End Rule: दिमाग पुरानी यादों का मूल्यांकन कैसे करता है?','target_account':'@balajirajput96','publication_allowed':True,'claims_boundary':'No medical diagnosis. General education only.','format':{'width':WIDTH,'height':HEIGHT,'aspect_ratio':'9:16','fps':FPS,'duration_seconds':round(duration(FINAL),3)},'sha256':{}}
    for name in ['final.mp4','narration.wav','captions.srt','visual_reference.png']: meta['sha256'][name]=sha256(WORK/name)
    METADATA.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'final':str(FINAL),'duration_seconds':duration(FINAL),'package':str(WORK),'caption_file':str(CAPTIONS)},ensure_ascii=False))
if __name__=='__main__': main()
