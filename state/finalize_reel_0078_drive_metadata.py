from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
meta_path = ROOT / 'assets/reel_0078_metadata.json'
verify = json.loads((ROOT / 'state/reel_0078_drive_final_verification.json').read_text(encoding='utf-8'))
folder_id = (ROOT / 'state/reel_0078_drive_folder_id.txt').read_text(encoding='utf-8').strip()
manifest_id = (ROOT / 'state/reel_0078_manifest_file_id.txt').read_text(encoding='utf-8').strip()
if not verify.get('valid') or verify.get('expected_count') != 11 or verify.get('found_expected_count') != 11:
    raise SystemExit('Drive exact-package verification must pass before metadata finalization')
meta = json.loads(meta_path.read_text(encoding='utf-8'))
meta['qc']['local_media_qc'] = 'passed'
meta['qc']['drive_verified'] = True
meta['qc']['drive_manifest_uploaded'] = True
meta['qc']['drive_manifest_file_id'] = manifest_id
meta['qc']['drive_folder_id'] = folder_id
meta['qc']['drive_verification_note'] = 'Final exact-package verification passed: 11 expected objects, one nonzero correctly parented manifest, zero missing/zero-size/wrong-parent/duplicate/unrelated objects; metadata and manifest updated in place.'
meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'drive_folder_id': folder_id, 'drive_manifest_file_id': manifest_id, 'drive_verified': True}, ensure_ascii=False, indent=2))
