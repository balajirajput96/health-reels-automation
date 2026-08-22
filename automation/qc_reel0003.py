from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/repos/health-reels-automation')
PACKAGE = ROOT / 'work' / 'reel_0003'
OUT = PACKAGE / 'qc.json'
REQUIRED = ['final.mp4', 'narration.wav', 'captions.srt', 'visual_reference.png', 'script.md', 'sources.md', 'production_brief.md', 'metadata.json']


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
    metadata = {}
    if (PACKAGE / 'metadata.json').is_file():
        try:
            metadata = json.loads((PACKAGE / 'metadata.json').read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            problems.append('metadata_invalid_json')
    probe = {}
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
    timing_ok = all(start < end for start, end, _ in cues) and all(cues[i][1] <= cues[i + 1][0] + 0.001 for i in range(len(cues) - 1))
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
    if not re.search(r'medical advice|medical advice नहीं|diagnosis|treatment', ai_text, re.I):
        problems.append('safety_boundary_missing')
    required_sources = ['10.3390/children10020399', '10.1007/BF01322177', '10.3389/fpsyg.2026.1822881']
    for source in required_sources:
        if source not in sources_text:
            problems.append(f'source_missing:{source}')
    if metadata.get('canonical_drive_path') != '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0003':
        problems.append('canonical_path_mismatch')
    if metadata.get('publication_allowed') is not False:
        problems.append('publication_boundary_not_false')
    result = {
        'reel_id': metadata.get('reel_id', 'reel_0003_self_concept_what_studies_measure'),
        'valid': not problems,
        'problems': problems,
        'local_media_probe': {
            'duration_seconds': round(duration, 3),
            'width': video_stream.get('width'),
            'height': video_stream.get('height'),
            'aspect_ratio_9_16': geometry_ok,
            'video_codec': video_stream.get('codec_name'),
            'audio_codec': audio_stream.get('codec_name'),
            'codec_ok': codec_ok,
            'duration_45_to_75': duration_ok,
        },
        'captions': {'cue_count': len(cues), 'timing_order_ok': timing_ok, 'devanagari_present': bool(re.search(r'[\u0900-\u097F]', captions_text))},
        'editorial': {
            'ai_disclosure_present': not any(problem == 'ai_disclosure_missing' for problem in problems),
            'safety_boundary_present': not any(problem == 'safety_boundary_missing' for problem in problems),
            'source_identifiers_present': not any(problem.startswith('source_missing:') for problem in problems),
            'publication_allowed': metadata.get('publication_allowed'),
        },
        'sha256': {name: sha256(PACKAGE / name) for name in REQUIRED if (PACKAGE / name).is_file()},
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
