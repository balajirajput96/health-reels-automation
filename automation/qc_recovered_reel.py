import hashlib
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

root = Path('/home/ubuntu/repos/health-reels-automation/work/reel_0002_drive_recovery')
out = root / 'deterministic_qc_local.json'
problems = []

def sha256(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def read_json(name):
    return json.loads((root / name).read_text(encoding='utf-8'))

def require_file(name):
    p = root / name
    if not p.exists() or p.stat().st_size == 0:
        problems.append(f'missing_or_empty:{name}')
    return p

video = require_file('final.mp4')
audio = require_file('narration.wav')
captions = require_file('captions.srt')
visual = require_file('visual_reference.png')
script = require_file('script.md')
sources = require_file('sources.md')
metadata = read_json('metadata.json')
remote_qc = read_json('qc_report.json')

probe = {}
if video.exists():
    cp = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)], capture_output=True, text=True, check=False)
    if cp.returncode != 0:
        problems.append('ffprobe_failed')
        probe = {'stderr': cp.stderr.strip()}
    else:
        probe = json.loads(cp.stdout)
streams = probe.get('streams', [])
vs = next((s for s in streams if s.get('codec_type') == 'video'), {})
as_ = next((s for s in streams if s.get('codec_type') == 'audio'), {})
fmt = probe.get('format', {})
duration = float(fmt.get('duration', 0) or 0)
width, height = vs.get('width'), vs.get('height')
video_codec = vs.get('codec_name')
audio_codec = as_.get('codec_name')
ratio_ok = width == 1080 and height == 1920
codec_ok = video_codec == 'h264' and audio_codec == 'aac'
duration_ok = 45 <= duration <= 75
if not ratio_ok: problems.append(f'geometry_not_9_16:{width}x{height}')
if not codec_ok: problems.append(f'codec_mismatch:{video_codec}/{audio_codec}')
if not duration_ok: problems.append(f'duration_out_of_bounds:{duration}')

srt = captions.read_text(encoding='utf-8') if captions.exists() else ''
blocks = [b for b in re.split(r'\n\s*\n', srt.strip()) if b.strip()]
cue_count = sum(1 for b in blocks if re.search(r'\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}', b))
starts, ends = [], []
for b in blocks:
    m = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})', b)
    if m:
        def sec(x):
            h, mi, rest = x.split(':'); s, ms = rest.split(',')
            return int(h)*3600 + int(mi)*60 + int(s) + int(ms)/1000
        starts.append(sec(m.group(1))); ends.append(sec(m.group(2)))
caption_order_ok = all(a <= b for a, b in zip(starts, starts[1:])) and all(e >= s for s, e in zip(starts, ends))
hindi_present = bool(re.search(r'[\u0900-\u097F]', srt))
disclosure_present = bool(re.search(r'AI\s+(visuals|content|narration)|AI-generated|AI visuals/narration', srt, re.I)) or bool(re.search(r'AI-generated|AI visuals|AI-content', metadata.get('ai_content_disclosure',''), re.I))
script_text = script.read_text(encoding='utf-8') if script.exists() else ''
safety_terms = ['No diagnosis', 'No diagnosis', 'No treatment', 'guaranteed', 'universal', 'universal rule', 'fact नहीं', 'सभी']
safety_present = ('No diagnosis' in script_text or 'No treatment' in script_text or 'universal' in script_text.lower()) and bool(re.search(r'universal rule|universal claim|diagnosis|treatment|guaranteed', metadata.get('claims_boundary',''), re.I))
source_text = sources.read_text(encoding='utf-8') if sources.exists() else ''
source_ids_ok = (('PMID:9781405' in source_text and '10.1037//0022-3514.75.3.617' in source_text and 'https://' in source_text) or (('PMID:9781405' in metadata.get('source_ids', [])) and ('DOI:10.1037//0022-3514.75.3.617' in metadata.get('source_ids', [])) and len(metadata.get('sources', [])) >= 2))
if cue_count < 2: problems.append(f'caption_cues_too_few:{cue_count}')
if not caption_order_ok: problems.append('caption_timing_invalid')
if not hindi_present: problems.append('no_devanagari_captions')
if not disclosure_present: problems.append('ai_disclosure_missing')
if not safety_present: problems.append('safety_boundary_missing')
if not source_ids_ok: problems.append('source_identifiers_missing')

wav = {}
if audio.exists():
    with wave.open(str(audio), 'rb') as w:
        wav = {'channels': w.getnchannels(), 'sample_rate': w.getframerate(), 'frames': w.getnframes(), 'duration_seconds': w.getnframes()/w.getframerate()}

result = {
    'reel_id': 'reel_0002_emotion_prediction_what_studies_measure',
    'valid': not problems,
    'problems': problems,
    'local_media_probe': {
        'duration_seconds': round(duration, 3),
        'width': width,
        'height': height,
        'aspect_ratio_9_16': ratio_ok,
        'video_codec': video_codec,
        'audio_codec': audio_codec,
        'codec_ok': codec_ok,
        'duration_45_to_75': duration_ok,
    },
    'captions': {'cue_count': cue_count, 'timing_order_ok': caption_order_ok, 'devanagari_present': hindi_present},
    'audio_file': wav,
    'editorial': {'ai_disclosure_present': disclosure_present, 'safety_boundary_present': safety_present, 'source_identifiers_present': source_ids_ok},
    'sha256': {name: sha256(root / name) for name in ['final.mp4','narration.wav','captions.srt','visual_reference.png','script.md','sources.md','metadata.json','qc_report.json']},
    'remote_qc_claim': remote_qc,
}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
if problems:
    sys.exit(1)
