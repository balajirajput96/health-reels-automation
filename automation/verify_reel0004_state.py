from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
queue = [json.loads(line) for line in (ROOT / 'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
entry = next(item for item in queue if item['reel_id'] == 'reel_0004_cognitive_biases_what_studies_measure')
checkpoint = json.loads((ROOT / 'state/reels_3000_checkpoint.json').read_text(encoding='utf-8'))
ledger = json.loads((ROOT / 'state/reels_ledger.json').read_text(encoding='utf-8'))
assert checkpoint['next_reel'] == entry['reel_id']
assert checkpoint['next_sequence'] == 4
assert entry['production_stage'] == 'planned'
assert entry['research_stage'] == 'verified'
assert entry['qc']['drive_verified'] is False
assert entry['failure_count'] == 1
assert entry['retries'] == 1
assert any(item.get('stage') == 'failed' and item.get('sha256') == entry['asset_checksums']['final.mp4'] for item in ledger['items'])
assert any(item.get('stage') == 'canonical_path_topic_conflict' for item in checkpoint['failure_log'])
print(json.dumps({'target': entry['reel_id'], 'next_reel': checkpoint['next_reel'], 'failure_count': entry['failure_count'], 'drive_verified': entry['qc']['drive_verified'], 'ledger_failed_match': True}, ensure_ascii=False, indent=2))
