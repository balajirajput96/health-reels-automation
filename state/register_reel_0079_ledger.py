from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ledger_path = ROOT / 'state/reels_ledger.json'
video = ROOT / 'assets/reel_0079_recovery_what_studies_measure_hi.mp4'
source_id = 'reel_0079_recovery_what_studies_measure'
sha = hashlib.sha256(video.read_bytes()).hexdigest()
data = json.loads(ledger_path.read_text(encoding='utf-8'))
items = data.setdefault('items', [])
matching = [item for item in items if item.get('source_id') == source_id]
if matching:
    if len(matching) == 1 and matching[0].get('stage') == 'final' and matching[0].get('sha256') == sha:
        print('R0079_LEDGER_ALREADY_REGISTERED')
        print(json.dumps(matching[0], ensure_ascii=False, indent=2))
        raise SystemExit(0)
    raise SystemExit(f'conflicting R0079 ledger records: {matching!r}')
record = {
    'source_id': source_id,
    'sha256': sha,
    'filename': 'reel_0079_recovery_what_studies_measure_hi.mp4',
    'stage': 'final',
    'target_account': '@balajirajput96',
    'recorded_at': datetime.now(UTC).isoformat(timespec='microseconds').replace('+00:00', 'Z'),
    'notes': 'R0079 final: 4 fresh verified sources; local QC passed; 68.167s encoded 1080x1920 H.264/AAC reel; canonical Drive exact package independently verified; not published.',
}
items.append(record)
ledger_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(record, ensure_ascii=False, indent=2))
