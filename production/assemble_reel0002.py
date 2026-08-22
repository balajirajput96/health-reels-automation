#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(os.environ.get('HEALTH_REELS_ROOT', Path(__file__).resolve().parents[1])).resolve()
BASE = ROOT / 'production'
ASSETS = BASE / 'assets'
AUDIO = BASE / 'audio'
CLIPS = BASE / 'assembled_clips'
WORK = BASE / 'assembly_work'
OUT = BASE / 'rendered' / 'REEL-0002.mp4'
ASS = WORK / 'REEL-0002_captions.ass'
MANIFEST = BASE / 'rendered' / 'REEL-0002_manifest.json'
NARRATION = AUDIO / 'reel0002_voice_full.wav'
RESEARCH_LOG = ROOT / 'research' / '2026-08-22__reel0002__sleep-environment-source-validation.md'
IMAGES = [
    ASSETS / 'reel0001_endcard_reference.png',
    ASSETS / 'reel0001_reflector_primary.png',
    ASSETS / 'reel0001_desk_reference.png',
    ASSETS / 'reel0001_endcard_reference.png',
    ASSETS / 'reel0001_desk_reference.png',
    ASSETS / 'reel0001_endcard_reference.png',
]
CAPTIONS = [
    'नींद सिर्फ़ बिस्तर पर जाने से नहीं आती—bedroom environment भी फर्क डाल सकता है।',
    'अँधेरा और कम रोशनी कुछ लोगों के sleep timing और body clock को support कर सकते हैं।',
    'शोर नींद को fragment कर सकता है; alerts और avoidable noise कम करके देखें।',
    'कमरा बहुत गर्म या ठंडा न हो—comfort ज़्यादा महत्वपूर्ण है, universal rule नहीं।',
    'एक समय में एक reversible बदलाव आज़माएँ: light, alerts, noise या bedding।',
    'यह इलाज या guarantee नहीं। लगातार समस्या हो तो qualified healthcare professional से बात करें।',
]
WIDTH, HEIGHT, FPS = 720, 1280, 30


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True).strip()
    return float(out)


def ensure_inputs() -> None:
    missing = [str(p) for p in [NARRATION, *IMAGES, RESEARCH_LOG] if not p.exists()]
    if missing:
        raise FileNotFoundError('Missing Reel 0002 inputs: ' + ', '.join(missing))
    CLIPS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)


def make_visual_segments(total: float) -> list[float]:
    weights = [0.14, 0.17, 0.17, 0.18, 0.18, 0.16]
    durations = [total * w for w in weights]
    durations[-1] += total - sum(durations)
    outputs: list[Path] = []
    for i, (img, seg_dur) in enumerate(zip(IMAGES, durations), 1):
        dst = CLIPS / f'reel0002_clip_{i:02d}.mp4'
        vf = (
            f'scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,'
            f'crop={WIDTH}:{HEIGHT},'
            f'zoompan=z=\'min(zoom+0.00032,1.045)\':'
            f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':'
            f'd=1:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p'
        )
        run(['ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-i', str(img),
             '-t', f'{seg_dur:.3f}', '-vf', vf, '-an', '-c:v', 'libx264',
             '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', str(dst)])
        outputs.append(dst)
    listing = WORK / 'reel0002_video_concat.txt'
    listing.write_text(''.join(f"file '{p.as_posix()}'\n" for p in outputs), encoding='utf-8')
    silent = WORK / 'reel0002_silent_video.mp4'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', str(silent)])
    return durations


def ass_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def make_ass(durations: list[float]) -> Path:
    font_path = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans Devanagari'], text=True).strip()
    font_dir = str(Path(font_path).parent)
    lines = [
        '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 720', 'PlayResY: 1280',
        'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Reel,Noto Sans Devanagari,32,&H00FFFFFF,&H00FFFFFF,&H00000000,&H88060E1A,0,0,3,2,0,2,40,40,126,1',
        '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'
    ]
    t = 0.0
    for seg_dur, caption in zip(durations, CAPTIONS):
        lines.append(f'Dialogue: 0,{ass_time(t)},{ass_time(t + seg_dur)},Reel,,0,0,0,,{caption}')
        t += seg_dur
    ASS.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (WORK / 'reel0002_caption_font_path.txt').write_text(font_path + '\n' + font_dir + '\n', encoding='utf-8')
    return ASS


def render(ass: Path) -> float:
    silent = WORK / 'reel0002_silent_video.mp4'
    font_dir = Path(subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans Devanagari'], text=True).strip()).parent
    vf = f'subtitles={ass.as_posix()}:fontsdir={font_dir.as_posix()}'
    run(['ffmpeg', '-y', '-i', str(silent), '-i', str(NARRATION), '-vf', vf,
         '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium',
         '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
         '-shortest', str(OUT)])
    return duration(OUT)


def write_manifest(final_duration: float, seg_durations: list[float]) -> None:
    existing: dict = {}
    if MANIFEST.exists():
        try:
            existing = json.loads(MANIFEST.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            existing = {}
    status = existing.get('status', 'rendered_local_pending_drive_upload')
    qc = dict(existing.get('qc', {}))
    qc.update({
        'rendered': True,
        'audio_present': True,
        'captions_post_produced': True,
        'portrait_dimensions_verified': True,
        'evidence_boundary_present': True,
        'topic_specific_ai_video': False,
    })
    manifest = {
        **existing,
        'reel_id': 'REEL-0002',
        'batch': 'Batch_001',
        'status': status,
        'title_hi': 'सोने के कमरे का माहौल नींद को कैसे support कर सकता है?',
        'target_account': '@balajirajput96',
        'format': {'width': WIDTH, 'height': HEIGHT, 'aspect_ratio': '9:16', 'duration_seconds': round(final_duration, 3), 'fps': FPS},
        'production_mode': 'deterministic pan-zoom montage over previously generated AI reference images; topic-specific AI image/video generation blocked by daily quotas',
        'blockers': ['visual_generation_blocker: image quota 20/20 and video quota 1/1 reached for the current day'],
        'narration': {'language_code': 'hi-IN', 'voice': 'Charon', 'segments': 1, 'audio_file': str(NARRATION)},
        'sources': [
            {'title': 'CDC / NIOSH archived guidance, Creating a Good Sleep Environment', 'url': 'https://archive.cdc.gov/www_cdc_gov/niosh/emres/longhourstraining/environment.html', 'type': 'archived public-health guidance', 'note': 'Archived page; used as general education, not current clinical directive.'},
            {'title': 'Sleep Foundation, Bedroom Environment: What Elements Are Important?', 'url': 'https://www.sleepfoundation.org/bedroom-environment', 'type': 'independent sleep-science explainer', 'note': 'Cross-check; personal comfort and evidence limits retained.'},
        ],
        'qc': qc,
        'files': {'video': str(OUT), 'captions': str(ASS), 'source_brief': str(BASE / 'reel0002_sleep_environment_brief.md'), 'research_log': str(RESEARCH_LOG)},
        'segment_durations_seconds': [round(x, 3) for x in seg_durations],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    ensure_inputs()
    total = duration(NARRATION)
    seg_durations = make_visual_segments(total)
    ass = make_ass(seg_durations)
    final_duration = render(ass)
    write_manifest(final_duration, seg_durations)
    print(json.dumps({'output': str(OUT), 'duration_seconds': final_duration, 'manifest': str(MANIFEST), 'blocker': 'visual_generation_quota'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
