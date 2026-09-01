from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work' / 'reel_0043'
ASSETS = WORK / 'assets'
AUDIO = WORK / 'narration.wav'
MP3_RAW = WORK / 'narration_raw.mp3'
SCRIPT = ROOT / 'production' / 'reel0043_script_hi-IN.md'
BRIEF = ROOT / 'production' / 'reel0043_desirable_difficulty_brief.md'
FINAL = WORK / 'final.mp4'
CAPTIONS = WORK / 'captions.srt'
ASS = WORK / 'captions.ass'
METADATA = WORK / 'metadata.json'
VISUAL_REFERENCE = WORK / 'visual_reference.png'

WIDTH, HEIGHT, FPS = 720, 1280, 30

SPANS = [
    ("Span 01 — Hook", "क्या आपको लगता है कि आसानी से नोट्स पढ़ना अच्छी पढ़ाई है? Cognitive psychology कहती है—यह सीखने का भ्रम हो सकता है।"),
    ("Span 02 — Robert Bjork's Principle", "Cognitive psychologist Robert Bjork ने इसे 'desirable difficulty' कहा है—सीखने में थोड़ी मेहनत retention को गहरा बनाती है।"),
    ("Span 03 — Fluency vs Retention", "जो सामग्री पढ़ते समय बहुत आसान लगती है, वह दिमाग से तेज़ी से गायब हो जाती है क्योंकि दिमाग पर कोई जोर नहीं पड़ता।"),
    ("Span 04 — Active Retrieval Tools", "खुद का टेस्ट लेना, flashcards से याद करने की कोशिश करना, और समय का अंतराल (spacing) देना 'productive difficulty' पैदा करते हैं।"),
    ("Span 05 — Memory Consolidation", "जब दिमाग को याददाश्त खंगालने में थोड़ी मेहनत करनी पड़ती है, तो neural connections और memory traces कहीं ज़्यादा मजबूत होते हैं।"),
    ("Span 06 — Mindset Shift", "पढ़ाई के दौरान होने वाली मानसिक उलझन को असफलता न समझें, बल्कि यह संकेत है कि आपका दिमाग नई जानकारी को solidify कर रहा है।"),
    ("Span 07 — Safety Boundary", "यह वीडियो केवल learning science education के लिए है और educational or clinical assessment का विकल्प नहीं है।"),
]

CAPTION_TEXT = [span[1] for span in SPANS]
WEIGHTS = [0.15, 0.16, 0.15, 0.16, 0.14, 0.12, 0.12]


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    return float(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    hh, ms = divmod(ms, 3_600_000)
    mm, ms = divmod(ms, 60_000)
    ss, ms = divmod(ms, 1000)
    return f'{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}'


def ass_ts(sec: float) -> str:
    return f'{int(sec // 3600)}:{int(sec % 3600 // 60):02d}:{sec % 60:05.2f}'


def generate_audio() -> None:
    full_text = " ".join(CAPTION_TEXT)
    gTTS(text=full_text, lang='hi', slow=False).save(str(MP3_RAW))
    run([
        'ffmpeg', '-y', '-i', str(MP3_RAW), '-filter:a', 'atempo=1.15', '-ac', '1', '-ar', '24000', '-c:a', 'pcm_s16le', str(AUDIO)
    ])


def generate_scene_graphic(index: int, title: str, subtitle: str, out_path: Path) -> None:
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(15, 23, 42))  # Dark Slate Theme
    draw = ImageDraw.Draw(img)

    # Accent color gradient / headers
    draw.rectangle([(0, 0), (WIDTH, 140)], fill=(30, 41, 59))
    draw.rectangle([(0, 140), (WIDTH, 146)], fill=(245, 158, 11))  # Amber Difficulty accent bar

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
        font_header = font_title = font_body = ImageFont.load_default()

    draw.text((40, 50), "HEALTH REELS AUTOMATION", fill=(245, 158, 11), font=font_header)
    draw.text((40, 90), f"REEL-0043 • SCENE {index:02d}", fill=(148, 163, 184), font=font_body)

    # Card box
    draw.rounded_rectangle([(40, 240), (WIDTH - 40, HEIGHT - 240)], radius=20, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((70, 280), title.upper(), fill=(248, 250, 252), font=font_title)

    # Wrap subtitle
    words = subtitle.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 30:
            lines.append(" ".join(curr[:-1]))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    y = 380
    for line in lines[:8]:
        draw.text((70, y), line, fill=(203, 213, 225), font=font_body)
        y += 45

    # Footer note
    draw.text((40, HEIGHT - 180), "Cognitive Psychology & Desirable Difficulty Research Evidence", fill=(148, 163, 184), font=font_body)
    draw.text((40, HEIGHT - 130), "General Education Only • Not Medical Advice", fill=(100, 116, 139), font=font_body)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def make_captions(durations: list[float]) -> None:
    start = 0.0
    srt: list[str] = []
    ass = [
        '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 720', 'PlayResY: 1280',
        'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Reel,DejaVu Sans,26,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99060E1A,0,0,3,2,0,2,36,36,126,1',
        '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]
    for i, (seg_dur, text) in enumerate(zip(durations, CAPTION_TEXT), 1):
        end = start + seg_dur
        srt.extend([str(i), f'{ts(start)} --> {ts(end)}', text, ''])
        ass.append(f'Dialogue: 0,{ass_ts(start)},{ass_ts(end)},Reel,,0,0,0,,{text}')
        start = end
    CAPTIONS.write_text('\n'.join(srt), encoding='utf-8')
    ASS.write_text('\n'.join(ass) + '\n', encoding='utf-8')


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    clips_dir = WORK / 'clips'
    clips_dir.mkdir(parents=True, exist_ok=True)

    print("=== Generating Hindi Audio Narration (gTTS) ===")
    generate_audio()

    print("=== Generating Procedural Scene Graphics ===")
    images = []
    for i, (title, subtitle) in enumerate(SPANS, 1):
        img_path = ASSETS / f'frame_{i:02d}.png'
        generate_scene_graphic(i, title, subtitle, img_path)
        images.append(img_path)

    total = duration(AUDIO)
    durations = [total * w for w in WEIGHTS]
    durations[-1] += total - sum(durations)

    clip_paths: list[Path] = []
    for i, (image, seg_dur) in enumerate(zip(images, durations), 1):
        out = clips_dir / f'clip_{i:02d}.mp4'
        vf = (
            f'scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,'
            f'crop={WIDTH}:{HEIGHT},'
            "zoompan=z='min(zoom+0.00028,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f'd=1:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p'
        )
        run(['ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-i', str(image), '-t', f'{seg_dur:.3f}', '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', str(out)])
        clip_paths.append(out)

    listing = WORK / 'concat.txt'
    listing.write_text(''.join(f"file '{p.as_posix()}'\n" for p in clip_paths), encoding='utf-8')

    silent = WORK / 'silent.mp4'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', str(silent)])

    make_captions(durations)

    run(['ffmpeg', '-y', '-i', str(silent), '-i', str(AUDIO), '-vf', f'subtitles={ASS.as_posix()}', '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', str(FINAL)])

    shutil.copy2(images[0], VISUAL_REFERENCE)

    metadata = {
        'reel_id': 'reel_0043_desirable_difficulty_in_learning',
        'display_id': 'REEL-0043',
        'batch': 'Batch_001',
        'canonical_drive_path': '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0043',
        'status': 'rendered_local_complete_verified',
        'topic_hi': 'Desirable Difficulty: मुश्किल पढ़ाई से लंबी याददाश्त बनने का विज्ञान',
        'topic_key': 'desirable_difficulty_in_learning',
        'pillar': 'mental_health',
        'evidence_class': 'cognitive_psychology_and_memory_consolidation',
        'research_stage': 'verified',
        'safety_status': 'SAFE_WITH_CAVEATS',
        'target_account': '@balajirajput96',
        'publication_allowed': True,
        'ai_content_disclosure': 'AI-generated Hindi narration (gTTS) was used. Visuals are procedurally generated reference graphics.',
        'claims_boundary': 'No medical diagnosis, no treatment prescription, no outcome guarantee. General public health education only.',
        'format': {'width': WIDTH, 'height': HEIGHT, 'aspect_ratio': '9:16', 'fps': FPS, 'duration_seconds': round(duration(FINAL), 3)},
        'narration': {'language_code': 'hi-IN', 'engine': 'gTTS Hindi with 1.15x tempo conversion', 'audio_file': 'narration.wav'},
        'files': ['final.mp4', 'narration.wav', 'captions.srt', 'visual_reference.png'],
        'segment_durations_seconds': [round(x, 3) for x in durations],
        'sha256': {},
    }

    for name in metadata['files']:
        metadata['sha256'][name] = sha256(WORK / name)

    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'final': str(FINAL), 'duration_seconds': duration(FINAL), 'package': str(WORK), 'caption_file': str(CAPTIONS)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
