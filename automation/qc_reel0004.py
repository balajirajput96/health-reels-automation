from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'work' / 'reel_0004'
OUT = PACKAGE / 'qc.json'
REQUIRED = ['final.mp4', 'narration.wav', 'captions.srt', 'visual_reference.png', 'script.md', 'sources.md', 'production_brief.md', 'metadata.json']
EXPECTED_SOURCES = ['10.3389/fpsyg.2021.630177', '10.3389/fpsyg.2015.01770', '10.3758/s13428-022-01804-9']
EXPECTED_PATH = '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004'
EXPECTED_ID = 'reel_0004_cognitive_biases_what_studies_measure'


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def sec(value: str) -> float:
    hours, minutes, rest = value.split(':')
    seconds, millis = rest.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000


def main() -> int:
    problems: list[str] = []
    missing = [name for name in REQUIRED if not (PACKAGE / name).is_file() or (PACKAGE / name).stat().st_size == 0]
    problems.extend(f'missing_or_empty:{name}' for name in missing)
    metadata: dict = {}
    meta_path = PACKAGE / 'metadata.json'
    if meta_path.is_file():
        try:
            metadata = json.loads(meta_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            problems.append('metadata_invalid_json')
    if metadata.get('reel_id') != EXPECTED_ID:
        problems.append('reel_id_mismatch')
    if metadata.get('canonical_drive_path') != EXPECTED_PATH:
        problems.append('canonical_path_mismatch')
    if metadata.get('publication_allowed') is not False:
        problems.append('publication_boundary_not_false')
    probe: dict = {}
    video = PACKAGE / 'final.mp4'
    if video.is_file():
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)], capture_output=True, text=True, check=False)
        if result.returncode:
            problems.append('ffprobe_failed')
        else:
            probe = json.loads(result.stdout)
    streams = probe.get('streams', [])
    video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
    audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})
    duration = float(probe.get('format', {}).get('duration', 0) or 0)
    geometry_ok = video_stream.get('width') == 720 and video_stream.get('height') == 1280
    codec_ok = video_stream.get('codec_name') == 'h264' and audio_stream.get('codec_name') == 'aac'
    duration_ok = 45 <= duration <= 75
    if not geometry_ok:
        problems.append(f'geometry_not_9_16:{video_stream.get("width")}x{video_stream.get("height")}')
    if not codec_ok:
        problems.append(f'codec_mismatch:{video_stream.get("codec_name")}/{audio_stream.get("codec_name")}')
    if not duration_ok:
        problems.append(f'duration_out_of_bounds:{duration}')
    captions_text = (PACKAGE / 'captions.srt').read_text(encoding='utf-8') if (PACKAGE / 'captions.srt').is_file() else ''
    blocks = [block for block in re.split(r'\n\s*\n', captions_text.strip()) if block.strip()]
    cues = []
    for block in blocks:
        match = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\n(.+)', block, re.S)
        if match:
            cues.append((sec(match.group(1)), sec(match.group(2)), match.group(3).strip()))
    if len(cues) != 6:
        problems.append(f'caption_cue_count:{len(cues)}')
    timing_ok = bool(cues) and all(start < end for start, end, _ in cues) and all(cues[i][1] <= cues[i + 1][0] + 0.001 for i in range(len(cues) - 1))
    if not timing_ok:
        problems.append('caption_timing_invalid_or_overlapping')
    if cues and cues[-1][1] > duration + 0.25:
        problems.append('captions_extend_beyond_video')
    if not re.search(r'[\u0900-\u097F]', captions_text):
        problems.append('no_devanagari_captions')
    script_text = (PACKAGE / 'script.md').read_text(encoding='utf-8') if (PACKAGE / 'script.md').is_file() else ''
    sources_text = (PACKAGE / 'sources.md').read_text(encoding='utf-8') if (PACKAGE / 'sources.md').is_file() else ''
    ai_text = ' '.join([captions_text, script_text, json.dumps(metadata, ensure_ascii=False)])
    if not re.search(r'AI[- ]generated narration|AI का उपयोग|AI-generated', ai_text, re.I):
        problems.append('ai_disclosure_missing')
    if not re.search(r'medical advice|medical advice नहीं|diagnosis|treatment|निदान|इलाज', ai_text, re.I):
        problems.append('safety_boundary_missing')
    for source in EXPECTED_SOURCES:
        if source not in sources_text:
            problems.append(f'source_missing:{source}')
    narration = PACKAGE / 'narration.wav'
    narration_probe = {}
    if narration.is_file():
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(narration)], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            narration_probe = json.loads(result.stdout)
        else:
            problems.append('narration_ffprobe_failed')
    nstream = next((s for s in narration_probe.get('streams', []) if s.get('codec_type') == 'audio'), {})
    if nstream.get('sample_rate') != '24000' or nstream.get('channels') != 1:
        problems.append(f'narration_format_mismatch:{nstream.get("sample_rate")}/{nstream.get("channels")}')
    result = {
        'reel_id': metadata.get('reel_id', EXPECTED_ID),
        'valid': not problems,
        'problems': problems,
        'local_media_probe': {
            'duration_seconds': round(duration, 3),
            'width': video_stream.get('width'), 'height': video_stream.get('height'),
            'aspect_ratio_9_16': geometry_ok,
            'video_codec': video_stream.get('codec_name'), 'audio_codec': audio_stream.get('codec_name'),
            'codec_ok': codec_ok, 'duration_45_to_75': duration_ok,
        },
        'narration_probe': {'sample_rate': nstream.get('sample_rate'), 'channels': nstream.get('channels'), 'codec_name': nstream.get('codec_name')},
        'captions': {'cue_count': len(cues), 'timing_order_ok': timing_ok, 'devanagari_present': bool(re.search(r'[\u0900-\u097F]', captions_text))},
        'editorial': {
            'ai_disclosure_present': 'ai_disclosure_missing' not in problems,
            'safety_boundary_present': 'safety_boundary_missing' not in problems,
            'source_identifiers_present': not any(p.startswith('source_missing:') for p in problems),
            'publication_allowed': metadata.get('publication_allowed'),
        },
        'sha256': {name: sha256(PACKAGE / name) for name in REQUIRED if (PACKAGE / name).is_file()},
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
