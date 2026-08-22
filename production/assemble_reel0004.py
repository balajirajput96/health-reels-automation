from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work' / 'reel_0004'
ASSETS = ROOT / 'production' / 'assets' / 'reel0004'
AUDIO = ROOT / 'production' / 'audio' / 'reel0004_voice_full.wav'
SCRIPT = ROOT / 'production' / 'rendered' / 'REEL-0004_script_hi-IN.md'
SOURCES = ROOT / 'research' / '2026-08-22__reel0004__cognitive-biases-source-validation.md'
BRIEF = ROOT / 'production' / 'reel0004_cognitive_biases_brief.md'
FINAL = WORK / 'final.mp4'
CAPTIONS = WORK / 'captions.srt'
ASS = WORK / 'captions.ass'
METADATA = WORK / 'metadata.json'
VISUAL_REFERENCE = WORK / 'visual_reference.png'
WIDTH, HEIGHT, FPS = 720, 1280, 30
CAPTION_TEXT = [
    'क्या cognitive bias का मतलब है कि किसी व्यक्ति का दिमाग हमेशा गलत सोचता है? नहीं—study आम तौर पर एक खास task में response pattern मापती है।',
    'Cognitive bias यानी judgment में ऐसा systematic pattern जो किसी norm या accuracy benchmark से अलग दिख सकता है। Researchers इसे label से नहीं, operational definition से पकड़ते हैं।',
    'कुछ tasks में answer को base rate या सही calculation से compare करते हैं। कुछ में एक ही सवाल के दो versions देते हैं—जैसे framing बदलकर—और responses का फर्क देखते हैं।',
    'लेकिन एक task = पूरी personality नहीं। Reviews बताते हैं कि अलग tasks को जोड़कर बना score कभी कम reliable हो सकता है; wording, response mode और context भी परिणाम बदल सकते हैं।',
    'एक study में dot-probe, AAT और IAT की reliability task और समय के साथ अलग रही। इसलिए सही सवाल है: इस sample में, इस design ने क्या मापा?',
    'यह general education है, medical advice नहीं। किसी personal concern के लिए qualified professional से बात करें। Narration में AI का उपयोग हुआ है; visuals procedural graphics हैं.',
]
WEIGHTS = [0.12, 0.17, 0.20, 0.20, 0.17, 0.14]


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


def make_captions(durations: list[float]) -> None:
    start = 0.0
    srt: list[str] = []
    ass = [
        '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 720', 'PlayResY: 1280',
        'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Reel,Noto Sans Devanagari,31,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99060E1A,0,0,3,2,0,2,36,36,126,1',
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
    images = [ASSETS / f'frame_{i:02d}.png' for i in range(1, 7)]
    missing = [str(p) for p in [AUDIO, SCRIPT, SOURCES, BRIEF, *images] if not p.exists()]
    if missing:
        raise FileNotFoundError('Missing reel-0004 inputs: ' + ', '.join(missing))
    WORK.mkdir(parents=True, exist_ok=True)
    clips = WORK / 'clips'
    clips.mkdir(parents=True, exist_ok=True)
    total = duration(AUDIO)
    durations = [total * w for w in WEIGHTS]
    durations[-1] += total - sum(durations)
    clip_paths: list[Path] = []
    for i, (image, seg_dur) in enumerate(zip(images, durations), 1):
        out = clips / f'clip_{i:02d}.mp4'
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
    font_path = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans Devanagari'], text=True).strip()
    font_dir = str(Path(font_path).parent)
    run(['ffmpeg', '-y', '-i', str(silent), '-i', str(AUDIO), '-vf', f'subtitles={ASS.as_posix()}:fontsdir={font_dir}', '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', str(FINAL)])
    shutil.copy2(AUDIO, WORK / 'narration.wav')
    shutil.copy2(images[0], VISUAL_REFERENCE)
    shutil.copy2(SCRIPT, WORK / 'script.md')
    shutil.copy2(SOURCES, WORK / 'sources.md')
    shutil.copy2(BRIEF, WORK / 'production_brief.md')
    metadata = {
        'reel_id': 'reel_0004_cognitive_biases_what_studies_measure',
        'display_id': 'REEL-0004',
        'batch': 'Batch_001',
        'canonical_drive_path': '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004',
        'status': 'rendered_local_pending_qc_and_drive_upload',
        'topic_hi': 'संज्ञानात्मक पूर्वाग्रह: अध्ययन वास्तव में क्या मापते हैं',
        'topic_key': 'cognitive_biases',
        'pillar': 'psychology',
        'evidence_class': 'peer_reviewed_measurement_review_plus_methodological_and_psychometric_studies',
        'research_stage': 'verified',
        'safety_status': 'SAFE_WITH_CAVEATS',
        'target_account': '@balajirajput96',
        'publication_allowed': False,
        'ai_content_disclosure': 'AI-generated Hindi narration was used. Visuals are procedurally generated graphics; no external copyrighted media was used.',
        'claims_boundary': 'No diagnosis, no treatment recommendation, no personality verdict, no intelligence inference, no outcome guarantee, and no universal claim. General education only; not medical advice.',
        'format': {'width': WIDTH, 'height': HEIGHT, 'aspect_ratio': '9:16', 'fps': FPS, 'duration_seconds': round(duration(FINAL), 3)},
        'narration': {'language_code': 'hi-IN', 'engine': 'gTTS Hindi with deterministic 1.20x tempo conversion', 'audio_file': 'narration.wav'},
        'source_ids': ['DOI:10.3389/fpsyg.2021.630177', 'DOI:10.3389/fpsyg.2015.01770', 'DOI:10.3758/s13428-022-01804-9'],
        'files': ['final.mp4', 'narration.wav', 'captions.srt', 'visual_reference.png', 'script.md', 'sources.md', 'production_brief.md', 'metadata.json'],
        'segment_durations_seconds': [round(x, 3) for x in durations],
        'sha256': {},
    }
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name in metadata['files']:
        metadata['sha256'][name] = sha256(WORK / name)
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'final': str(FINAL), 'duration_seconds': duration(FINAL), 'package': str(WORK), 'caption_file': str(CAPTIONS)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
