from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'state/reels_3000_queue.jsonl'
REEL_ID = 'reel_0081_stress_and_attention_what_studies_measure'
VIDEO = ROOT / 'assets/reel_0081_stress_and_attention_what_studies_measure_hi.mp4'
QC = ROOT / 'assets/reel_0081_qc_report.json'
SHA_FILE = ROOT / 'state/reel_0081_mp4_sha256.txt'

parser = argparse.ArgumentParser()
parser.add_argument('stage', choices=['assembled', 'qc_passed'])
stage = parser.parse_args().stage
rows = [json.loads(line) for line in QUEUE.read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows) == 3000
row = next(item for item in rows if item['sequence'] == 81)
assert row['reel_id'] == REEL_ID
if stage == 'assembled':
    assert row['production_stage'] == 'visuals_ready'
    assert VIDEO.exists() and VIDEO.stat().st_size > 0
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,codec_name,width,height,pix_fmt,sample_rate,channels,channel_layout,duration', '-of', 'json', str(VIDEO)], text=True))
    streams = probe['streams']
    video = next(item for item in streams if item.get('codec_type') == 'video')
    audio = next(item for item in streams if item.get('codec_type') == 'audio')
    duration = float(video.get('duration') or probe['format']['duration'])
    assert (video['width'], video['height'], video['pix_fmt']) == (1080, 1920, 'yuv420p')
    assert video['codec_name'] == 'h264' and 45.0 <= duration <= 75.0
    assert audio['codec_name'] == 'aac' and audio['sample_rate'] == '48000' and int(audio['channels']) == 1 and audio['channel_layout'] == 'mono'
    row['qc']['aspect_ratio_9_16'] = True
    row['qc']['decode_ok'] = True
    row['qc']['duration_seconds'] = round(duration, 3)
else:
    assert row['production_stage'] == 'assembled'
    report = json.loads(QC.read_text(encoding='utf-8'))
    assert report.get('valid') is True
    assert report['checks']['caption_cues'] == 15
    assert report['checks']['source_records'] == 4
    assert report['checks']['ai_disclosure_present'] is True
    assert report['checks']['safety_wording_ok'] is True
    assert SHA_FILE.exists() and SHA_FILE.read_text().split()[0]
    sha = SHA_FILE.read_text().split()[0]
    assert hashlib.sha256(VIDEO.read_bytes()).hexdigest() == sha
    row['qc'].update({'ai_disclosure': True, 'captions': True, 'aspect_ratio_9_16': True, 'decode_ok': True, 'duration_seconds': report['checks']['duration_seconds'], 'hindi_audio': True})
    row['asset_checksums'][VIDEO.name] = sha
row['production_stage'] = stage
row['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
QUEUE.write_text('\n'.join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in rows) + '\n', encoding='utf-8')
print(json.dumps({'sequence': 81, 'reel_id': REEL_ID, 'production_stage': stage, 'qc': row['qc'], 'asset_checksums': row['asset_checksums']}, ensure_ascii=False, indent=2))
