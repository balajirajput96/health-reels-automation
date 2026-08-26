from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'state/reels_3000_queue.jsonl'
REEL_ID = 'reel_0081_stress_and_attention_what_studies_measure'
AUDIO = ROOT / 'assets/reel_0081_stress_and_attention_what_studies_measure_narration_hi.wav'
SRT = ROOT / 'assets/reel_0081_stress_and_attention_what_studies_measure_captions_hi.srt'
SCENES = [ROOT / f'assets/reel_0081_scene_{i:02d}.png' for i in range(1, 5)]

parser = argparse.ArgumentParser()
parser.add_argument('stage', choices=['audio_ready', 'visuals_ready'])
stage = parser.parse_args().stage
rows = [json.loads(line) for line in QUEUE.read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows) == 3000
row = next(item for item in rows if item['sequence'] == 81)
assert row['reel_id'] == REEL_ID
if stage == 'audio_ready':
    assert row['production_stage'] == 'script_ready'
    assert AUDIO.exists() and AUDIO.stat().st_size > 0
    assert abs(float(__import__('subprocess').check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(AUDIO)], text=True).strip()) - 64.44) < 0.001
    row['qc']['hindi_audio'] = True
else:
    assert row['production_stage'] == 'audio_ready'
    assert SRT.exists() and SRT.stat().st_size > 0
    for scene in SCENES:
        assert scene.exists() and scene.stat().st_size > 0
        with Image.open(scene) as image:
            assert image.size == (1440, 2560) and image.mode == 'RGB'
    row['qc']['captions'] = True
    row['qc']['decode_ok'] = True
row['production_stage'] = stage
row['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
QUEUE.write_text('\n'.join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in rows) + '\n', encoding='utf-8')
print(json.dumps({'sequence': 81, 'reel_id': REEL_ID, 'production_stage': stage, 'qc': row['qc']}, ensure_ascii=False, indent=2))
