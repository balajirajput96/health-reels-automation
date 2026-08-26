from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / 'state/reels_3000_queue.jsonl'
DRIVE = ROOT / 'state/reel_0081_drive_final_verification.json'
REEL_ID = 'reel_0081_stress_and_attention_what_studies_measure'
rows = [json.loads(line) for line in QUEUE.read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows) == 3000
row = next(item for item in rows if item['sequence'] == 81)
assert row['reel_id'] == REEL_ID and row['production_stage'] == 'qc_passed'
drive = json.loads(DRIVE.read_text(encoding='utf-8'))
assert drive.get('valid') is True
assert drive['expected_count'] == 11 and drive['found_expected_count'] == 11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert not drive['duplicate_expected_names'] and drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero']
assert drive['unrelated_remote_object_count'] == 0
row['production_stage'] = 'uploaded'
row['qc']['drive_verified'] = True
row['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
QUEUE.write_text('\n'.join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in rows) + '\n', encoding='utf-8')
print(json.dumps({'sequence': 81, 'reel_id': REEL_ID, 'production_stage': row['production_stage'], 'qc': row['qc']}, ensure_ascii=False, indent=2))
