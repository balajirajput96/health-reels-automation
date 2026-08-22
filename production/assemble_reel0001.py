#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
from pathlib import Path

BASE = Path('/home/ubuntu/github-workspace/repos/health-reels-automation/production')
ASSETS = BASE / 'assets'
AUDIO = BASE / 'audio'
CLIPS = BASE / 'assembled_clips'
WORK = BASE / 'assembly_work'
OUT = BASE / 'rendered' / 'REEL-0001.mp4'
ASS = WORK / 'REEL-0001_captions.ass'
MANIFEST = BASE / 'rendered' / 'REEL-0001_manifest.json'

VOICE_FILES = [AUDIO / f'reel0001_voice_{i:02d}.wav' for i in range(1, 8)]
IMAGE_FILES = [
    ASSETS / 'reel0001_reflector_primary.png',
    ASSETS / 'reel0001_brain_reference.png',
    ASSETS / 'reel0001_brain_reference.png',
    ASSETS / 'reel0001_reflector_primary.png',
    ASSETS / 'reel0001_desk_reference.png',
    ASSETS / 'reel0001_reflector_primary.png',
    ASSETS / 'reel0001_endcard_reference.png',
]
CAPTIONS = [
    'जब मन भारी हो, भावना को नाम देकर देखिए',
    'Feeling को नाम देना = Affect labeling',
    'कुछ fMRI studies में amygdala response कम दिखा',
    'यह इलाज या guarantee नहीं है',
    'मुझे अभी ___ महसूस हो रहा है, क्योंकि ___',
    'लगातार या intense distress में professional support लें',
    'Sources: Lieberman et al. 2007, PMID 17576282\\N\u2022 Burklund et al. 2014, Frontiers in Psychology',
]
ATEMPO = 1.15
FPS = 30
WIDTH = 720
HEIGHT = 1280


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True).strip()
    return float(out)


def ensure_inputs() -> None:
    missing = [str(p) for p in [*VOICE_FILES, *IMAGE_FILES] if not p.exists()]
    if missing:
        raise FileNotFoundError('Missing production inputs: ' + ', '.join(missing))
    CLIPS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)


def make_audio_segments() -> tuple[list[Path], list[float]]:
    adjusted = []
    durations = []
    for i, src in enumerate(VOICE_FILES, 1):
        dst = WORK / f'voice_{i:02d}_adjusted.wav'
        run(['ffmpeg', '-y', '-i', str(src), '-filter:a', f'atempo={ATEMPO}', '-ar', '48000', '-ac', '2', str(dst)])
        adjusted.append(dst)
        durations.append(probe_duration(dst))
    audio_list = WORK / 'audio_concat.txt'
    audio_list.write_text(''.join(f"file '{p.as_posix()}'\n" for p in adjusted), encoding='utf-8')
    concat_audio = WORK / 'narration_concat.wav'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(audio_list), '-c:a', 'pcm_s16le', str(concat_audio)])
    return adjusted, durations


def make_visual_segments(durations: list[float]) -> list[Path]:
    outputs = []
    for i, (img, dur) in enumerate(zip(IMAGE_FILES, durations), 1):
        dst = CLIPS / f'clip_{i:02d}.mp4'
        # The motion is deliberately deterministic: a slow, bounded push-in on AI-generated stills.
        vf = (
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='min(zoom+0.00045,1.06)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={WIDTH}x{HEIGHT}:fps={FPS},"
            "format=yuv420p"
        )
        run(['ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-i', str(img), '-t', f'{dur:.3f}', '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', str(dst)])
        outputs.append(dst)
    video_list = WORK / 'video_concat.txt'
    video_list.write_text(''.join(f"file '{p.as_posix()}'\n" for p in outputs), encoding='utf-8')
    silent_video = WORK / 'silent_video.mp4'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(video_list), '-c', 'copy', str(silent_video)])
    return outputs


def make_ass(durations: list[float]) -> None:
    font_path = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans Devanagari'], text=True).strip()
    font_dir = str(Path(font_path).parent)
    # The ASS renderer uses the installed font family; the directory is recorded for reproducibility.
    lines = [
        '[Script Info]',
        'ScriptType: v4.00+',
        'PlayResX: 720',
        'PlayResY: 1280',
        'WrapStyle: 2',
        'ScaledBorderAndShadow: yes',
        '',
        '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        'Style: Reel,Noto Sans Devanagari,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H880B1324,0,0,3,2,0,2,40,40,120,1',
        '',
        '[Events]',
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]
    t = 0.0
    for dur, caption in zip(durations, CAPTIONS):
        start = t
        end = t + dur
        def ass_time(sec: float) -> str:
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = sec % 60
            return f'{h}:{m:02d}:{s:05.2f}'
        lines.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Reel,,0,0,0,,{caption}')
        t = end
    ASS.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (WORK / 'caption_font_path.txt').write_text(font_path + '\n' + font_dir + '\n', encoding='utf-8')


def render_final(durations: list[float]) -> None:
    silent_video = WORK / 'silent_video.mp4'
    narration = WORK / 'narration_concat.wav'
    # The subtitles filter keeps Devanagari captions inside the portrait safe area.
    vf = f"subtitles={ASS.as_posix()}:fontsdir={Path(subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans Devanagari'], text=True).strip()).parent.as_posix()}"
    run(['ffmpeg', '-y', '-i', str(silent_video), '-i', str(narration), '-vf', vf, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', str(OUT)])


def write_manifest(durations: list[float]) -> None:
    duration = probe_duration(OUT)
    manifest = {
        'reel_id': 'REEL-0001',
        'batch': 'Batch_001',
        'status': 'rendered_local_pending_drive_upload',
        'title_hi': 'भावना को नाम देने से दिमाग को क्या मदद मिल सकती है?',
        'format': {'width': WIDTH, 'height': HEIGHT, 'aspect_ratio': '9:16', 'duration_seconds': round(duration, 3), 'fps': FPS},
        'production_mode': 'AI-generated portrait reference images with deterministic pan-zoom animation fallback; native AI video clip 1 retained separately because daily quota was reached.',
        'narration': {'language_code': 'hi-IN', 'voice': 'Erinome', 'segments': 7, 'tempo_filter': ATEMPO},
        'sources': [
            {'title': 'Lieberman et al. 2007, Putting Feelings Into Words', 'url': 'https://pubmed.ncbi.nlm.nih.gov/17576282/', 'type': 'peer-reviewed PubMed record'},
            {'title': 'Burklund et al. 2014, The Common and Distinct Neural Bases of Affect Labeling and Reappraisal', 'url': 'https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00221/full', 'type': 'peer-reviewed review/cross-check'},
            {'title': 'UCLA Health summary of affect labeling neuroimaging study', 'url': 'https://www.uclahealth.org/news/release/putting-feelings-into-words-produces-therapeutic-effects-in-the-brain-ucla-neuroimaging-study-supports-ancient-buddhist-teachings', 'type': 'university expert summary'},
        ],
        'qc': {'rendered': True, 'audio_present': True, 'captions_post_produced': True, 'no_generated_text_in_images': True, 'source_card_included': True, 'technical_checks_pending': True},
        'files': {'video': str(OUT), 'captions': str(ASS), 'source_brief': str(BASE / 'reel0001_affect_labeling_brief.md')},
        'segment_durations_seconds': [round(x, 3) for x in durations],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    ensure_inputs()
    _, durations = make_audio_segments()
    make_visual_segments(durations)
    make_ass(durations)
    render_final(durations)
    write_manifest(durations)
    print(json.dumps({'output': str(OUT), 'duration_seconds': probe_duration(OUT), 'manifest': str(MANIFEST)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
