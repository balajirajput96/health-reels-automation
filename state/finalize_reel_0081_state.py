from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
queue_path = ROOT / 'state/reels_3000_queue.jsonl'
checkpoint_path = ROOT / 'state/reels_3000_checkpoint.json'
ledger_path = ROOT / 'state/reels_ledger.json'
meta_path = ROOT / 'assets/reel_0081_metadata.json'
qc_path = ROOT / 'assets/reel_0081_qc_report.json'
drive_path = ROOT / 'state/reel_0081_drive_final_verification.json'
sha_path = ROOT / 'state/reel_0081_mp4_sha256.txt'
reel_id = 'reel_0081_stress_and_attention_what_studies_measure'

rows = [json.loads(line) for line in queue_path.read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows) == 3000
row = next(item for item in rows if item['sequence'] == 81)
assert row['reel_id'] == reel_id and row['production_stage'] == 'uploaded'
meta = json.loads(meta_path.read_text(encoding='utf-8'))
qc = json.loads(qc_path.read_text(encoding='utf-8'))
drive = json.loads(drive_path.read_text(encoding='utf-8'))
assert qc['valid'] is True and drive['valid'] is True
assert drive['expected_count'] == 11 and drive['found_expected_count'] == 11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent'] and not drive['duplicate_expected_names']
assert drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero'] and drive['unrelated_remote_object_count'] == 0
sha = sha_path.read_text(encoding='utf-8').split()[0]
assert meta['measured_mp4_sha256'] == sha
ledger = json.loads(ledger_path.read_text(encoding='utf-8'))['items']
records = [item for item in ledger if item.get('source_id') == reel_id and item.get('stage') == 'final']
assert len(records) == 1 and records[0]['sha256'] == sha
row['production_stage'] = 'final'
row['research_stage'] = 'verified'
row['safety_status'] = meta['safety_status']
row['source_ids'] = [item['source_id'] for item in meta['source_ids']]
row['qc'] = {
    'ai_disclosure': True,
    'aspect_ratio_9_16': True,
    'captions': True,
    'decode_ok': True,
    'drive_verified': True,
    'duration_seconds': qc['checks']['duration_seconds'],
    'hindi_audio': True,
}
row.setdefault('asset_checksums', {})['reel_0081_stress_and_attention_what_studies_measure_hi.mp4'] = sha
row['notes'] = 'Final R0081 closure: fresh four-source evidence, accepted Hindi narration/captions, deterministic visuals, local QC pass, canonical Drive exact package verification, not published.'
row['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
queue_path.write_text('\n'.join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in rows) + '\n', encoding='utf-8')
checkpoint = json.loads(checkpoint_path.read_text(encoding='utf-8'))
final_count = sum(1 for item in rows if item.get('production_stage') == 'final')
planned_count = sum(1 for item in rows if item.get('production_stage') == 'planned')
assert final_count == 81 and planned_count == 2919
next_row = next(item for item in rows if item['sequence'] == 82)
checkpoint['production_counts'] = {'final': final_count, 'planned': planned_count}
checkpoint['completed_drive_verified'] = final_count
checkpoint['next_sequence'] = 82
checkpoint['next_reel'] = next_row['reel_id']
checkpoint['last_completed'] = reel_id
checkpoint['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
checkpoint_path.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'queue_sequence': 81, 'production_stage': row['production_stage'], 'final': final_count, 'planned': planned_count, 'next_sequence': 82, 'next_reel': next_row['reel_id'], 'sha256': sha}, ensure_ascii=False, indent=2))
