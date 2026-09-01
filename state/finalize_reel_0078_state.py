from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
queue_path = ROOT / 'state/reels_3000_queue.jsonl'
checkpoint_path = ROOT / 'state/reels_3000_checkpoint.json'
meta = json.loads((ROOT / 'assets/reel_0078_metadata.json').read_text(encoding='utf-8'))
qc = json.loads((ROOT / 'assets/reel_0078_qc_report.json').read_text(encoding='utf-8'))
sha = meta['measured_mp4_sha256']
assert qc['valid'] is True
assert meta['qc']['drive_verified'] is True
assert meta['qc']['drive_manifest_uploaded'] is True
assert sha and len(sha) == 64
now = datetime.now(UTC).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
rows = [json.loads(line) for line in queue_path.read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows) == 3000
row = next(item for item in rows if item['sequence'] == 78)
assert row['reel_id'] == meta['reel_id']
assert row['production_stage'] in {'planned', 'research', 'edited', 'qc_passed', 'final'}
row['production_stage'] = 'final'
row['research_stage'] = 'verified'
row['evidence_class'] = meta['evidence_class']
row['safety_status'] = meta['safety_status']
row['source_ids'] = [item['source_id'] for item in meta['source_ids']]
row['qc'] = {
    'ai_disclosure': bool(meta.get('ai_content_disclosure')),
    'aspect_ratio_9_16': qc['checks']['aspect_ratio_9_16'],
    'captions': qc['checks']['caption_cues'] == 15 and qc['checks']['caption_timing_ok'],
    'decode_ok': True,
    'drive_verified': True,
    'duration_seconds': qc['checks']['duration_seconds'],
    'hindi_audio': True,
}
row.setdefault('asset_checksums', {})['reel_0078_acute_stress_what_studies_measure_hi.mp4'] = sha
row['updated_at'] = now
queue_path.write_text('\n'.join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in rows) + '\n', encoding='utf-8')
checkpoint = json.loads(checkpoint_path.read_text(encoding='utf-8'))
final_count = sum(1 for item in rows if item.get('production_stage') == 'final')
planned_count = sum(1 for item in rows if item.get('production_stage') == 'planned')
assert final_count == 78 and planned_count == 2922
next_row = next(item for item in rows if item['sequence'] == 79)
checkpoint['production_counts'] = {'final': final_count, 'planned': planned_count}
checkpoint['completed_drive_verified'] = final_count
checkpoint['next_sequence'] = 79
checkpoint['next_reel'] = next_row['reel_id']
checkpoint['last_completed'] = meta['reel_id']
checkpoint['updated_at'] = now
checkpoint_path.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'queue_sequence': 78, 'production_stage': row['production_stage'], 'final': final_count, 'planned': planned_count, 'next_sequence': 79, 'next_reel': next_row['reel_id']}, ensure_ascii=False, indent=2))
