from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/repos/health-reels-automation')
WORK = ROOT / 'work' / 'reel_0003'
ASSETS = ROOT / 'production' / 'assets' / 'reel0003'
AUDIO = ROOT / 'production' / 'audio' / 'reel0003_voice_full.wav'
SCRIPT = ROOT / 'production' / 'rendered' / 'REEL-0003_script_hi-IN.md'
SOURCES = ROOT / 'research' / '2026-08-22__reel0003__self-concept-source-validation.md'
BRIEF = ROOT / 'production' / 'reel0003_self_concept_brief.md'
FINAL = WORK / 'final.mp4'
CAPTIONS = WORK / 'captions.srt'
ASS = WORK / 'captions.ass'
METADATA = WORK / 'metadata.json'
VISUAL_REFERENCE = WORK / 'visual_reference.png'
WIDTH, HEIGHT, FPS = 720, 1280, 30

CAPTION_TEXT = [
    'जब कोई psychology study कहती है कि उसने self-concept मापा, तो इसका मतलब यह नहीं कि उसने किसी व्यक्ति को पूरी तरह पढ़ लिया।',
    'Self-concept का अर्थ है—अपने बारे में हमारी धारणाएँ: जैसे traits, roles और values। यह अनुभव और सामाजिक संदर्भ से बनती हैं, और समय के साथ बदल भी सकती हैं।',
    'अच्छे measures इसे अलग-अलग हिस्सों में देखते हैं: academic, social, physical, emotional, behavioral, या general self-worth। इसलिए दो studies के scores सीधे एक जैसे नहीं माने जा सकते।',
    'अक्सर participants questionnaire में statements को rate करते हैं। कुछ studies specific domains पूछती हैं, कुछ self-concept clarity—यानी beliefs कितने clear, consistent और stable लगते हैं।',
    'लेकिन score केवल चुने हुए items और उस sample की context बताता है। यह आपकी पूरी personality, objective ability, या mental-health diagnosis का प्रमाण नहीं है।',
    'यह general education है, medical advice नहीं। व्यक्तिगत चिंता हो तो qualified professional से बात करें। Narration में AI का उपयोग हुआ है और visuals procedurally generated graphics हैं।',
]
IMAGES = [ASSETS / f'frame_{i:02d}_{name}.png' for i, name in enumerate(['hook', 'concepts', 'domains', 'questionnaire', 'limits', 'endcard'], 1)]
WEIGHTS = [0.14, 0.17, 0.20, 0.18, 0.16, 0.15]


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True).strip()
    return float(out)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, millis = divmod(ms, 1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}'


def ass_time(seconds: float) -> str:
    return f'0:{int(seconds // 60):02d}:{seconds % 60:05.2f}'


def make_captions(durations: list[float]) -> None:
    start = 0.0
    srt = []
    ass = [
        '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 720', 'PlayResY: 1280',
        'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Reel,Noto Sans Devanagari,31,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99060E1A,0,0,3,2,0,2,36,36,126,1',
        '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]
    for index, (duration, text) in enumerate(zip(durations, CAPTION_TEXT), 1):
        end = start + duration
        srt.extend([str(index), f'{timestamp(start)} --> {timestamp(end)}', text, ''])
        ass.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Reel,,0,0,0,,{text}')
        start = end
    CAPTIONS.write_text('\n'.join(srt), encoding='utf-8')
    ASS.write_text('\n'.join(ass) + '\n', encoding='utf-8')


def main() -> None:
    required = [AUDIO, SCRIPT, SOURCES, BRIEF, *IMAGES]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError('Missing reel-0003 inputs: ' + ', '.join(missing))
    WORK.mkdir(parents=True, exist_ok=True)
    clips = WORK / 'clips'
    clips.mkdir(parents=True, exist_ok=True)
    total = probe_duration(AUDIO)
    durations = [total * weight for weight in WEIGHTS]
    durations[-1] += total - sum(durations)
    clip_paths = []
    for index, (image, duration) in enumerate(zip(IMAGES, durations), 1):
        output = clips / f'clip_{index:02d}.mp4'
        vf = (
            f'scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,'
            f'crop={WIDTH}:{HEIGHT},'
            "zoompan=z='min(zoom+0.00028,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p"
        )
        run(['ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-i', str(image), '-t', f'{duration:.3f}', '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', str(output)])
        clip_paths.append(output)
    listing = WORK / 'concat.txt'
    listing.write_text(''.join(f"file '{path.as_posix()}'\n" for path in clip_paths), encoding='utf-8')
    silent = WORK / 'silent.mp4'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', str(silent)])
    make_captions(durations)
    font_path = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans Devanagari'], text=True).strip()
    font_dir = str(Path(font_path).parent)
    vf = f'subtitles={ASS.as_posix()}:fontsdir={font_dir}'
    run(['ffmpeg', '-y', '-i', str(silent), '-i', str(AUDIO), '-vf', vf, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', str(FINAL)])
    shutil.copy2(AUDIO, WORK / 'narration.wav')
    shutil.copy2(IMAGES[0], VISUAL_REFERENCE)
    shutil.copy2(SCRIPT, WORK / 'script.md')
    shutil.copy2(SOURCES, WORK / 'sources.md')
    shutil.copy2(BRIEF, WORK / 'production_brief.md')
    metadata = {
        'reel_id': 'reel_0003_self_concept_what_studies_measure',
        'display_id': 'REEL-0003',
        'batch': 'Batch_001',
        'canonical_drive_path': '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0003',
        'status': 'rendered_local_pending_qc_and_drive_upload',
        'topic_hi': 'स्व-अवधारणा: अध्ययन वास्तव में क्या मापते हैं',
        'topic_key': 'self_concept',
        'pillar': 'psychology',
        'evidence_class': 'systematic_review_plus_foundational_review_plus_integrative_review',
        'research_stage': 'verified',
        'safety_status': 'SAFE_WITH_EDITS',
        'target_account': '@balajirajput96',
        'publication_allowed': False,
        'ai_content_disclosure': 'AI-generated Hindi narration was used. Visuals are procedurally generated graphics; no external copyrighted media was used.',
        'claims_boundary': 'No diagnosis, no treatment recommendation, no objective ability inference, no personality verdict, no outcome guarantee, and no universal claim. General education only; not medical advice.',
        'format': {'width': WIDTH, 'height': HEIGHT, 'aspect_ratio': '9:16', 'fps': FPS, 'duration_seconds': round(probe_duration(FINAL), 3)},
        'narration': {'language_code': 'hi-IN', 'voice': 'Charon', 'audio_file': 'narration.wav'},
        'source_ids': ['DOI:10.3390/children10020399', 'DOI:10.1007/BF01322177', 'DOI:10.3389/fpsyg.2026.1822881'],
        'files': ['final.mp4', 'narration.wav', 'captions.srt', 'visual_reference.png', 'script.md', 'sources.md', 'production_brief.md', 'metadata.json'],
        'segment_durations_seconds': [round(value, 3) for value in durations],
        'sha256': {},
    }
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name in metadata['files']:
        metadata['sha256'][name] = sha256(WORK / name)
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'final': str(FINAL), 'duration_seconds': probe_duration(FINAL), 'package': str(WORK), 'caption_file': str(CAPTIONS)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
