import hashlib
import json
from pathlib import Path

video = Path('rendered/REEL-0010_study_reading_QC_pending.mp4')
probe = json.loads(Path('rendered/qc_ffprobe.json').read_text())
manifest = json.loads(Path('rendered/REEL-0010_local_manifest.json').read_text())
duration = float(probe['format']['duration'])
video_stream = next(s for s in probe['streams'] if s.get('codec_type') == 'video')
audio_stream = next(s for s in probe['streams'] if s.get('codec_type') == 'audio')
assert sum(1 for s in probe['streams'] if s.get('codec_type') == 'video') == 1
assert sum(1 for s in probe['streams'] if s.get('codec_type') == 'audio') == 1
ass = Path('work/captions_hi-IN.ass').read_text(encoding='utf-8')
caption_entries = []
for line in ass.splitlines():
    if line.startswith('Dialogue:'):
        text = line.rsplit(',,', 1)[-1]
        caption_entries.append(text)
caption_lines = [part for entry in caption_entries for part in entry.split(r'\N')]
caption_line_lengths = [len(part) for part in caption_lines]
assert video_stream['width'] == 720 and video_stream['height'] == 1280
assert 60 <= duration <= 85
assert audio_stream['codec_type'] == 'audio'
assert video_stream['codec_name'] == 'h264'
assert audio_stream['codec_name'] == 'aac'
assert len(caption_entries) == 6
assert max(caption_line_lengths) <= 30
assert abs(duration - float(manifest['format']['duration_seconds'])) < 0.01
sha = hashlib.sha256(video.read_bytes()).hexdigest()
report = {
    'status': 'PASS',
    'reel_id': '0010',
    'width': video_stream['width'],
    'height': video_stream['height'],
    'aspect_ratio': '9:16',
    'duration_seconds': round(duration, 3),
    'audio_codec': audio_stream['codec_name'],
    'caption_entries': len(caption_entries),
    'wrapped_captions': True,
    'max_caption_line_length': max(caption_line_lengths),
    'sha256': sha,
    'frames': ['qc_frame_02s.jpg', 'qc_frame_37s.jpg', 'qc_frame_68s.jpg'],
}
Path('rendered/qc_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
Path('rendered/qc_sha256.txt').write_text(f'{sha}  {video.name}\n')
print(json.dumps(report, ensure_ascii=False))
