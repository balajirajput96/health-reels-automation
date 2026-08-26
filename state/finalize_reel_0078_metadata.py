from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
meta_path = ROOT / 'assets/reel_0078_metadata.json'
qc_path = ROOT / 'assets/reel_0078_qc_report.json'
video = ROOT / 'assets/reel_0078_acute_stress_what_studies_measure_hi.mp4'
meta = json.loads(meta_path.read_text(encoding='utf-8'))
qc = json.loads(qc_path.read_text(encoding='utf-8'))
if not qc.get('valid'):
    raise SystemExit('local QC must pass before metadata finalization')
meta['measured_narration_duration_seconds'] = 73.60
meta['measured_mp4_sha256'] = hashlib.sha256(video.read_bytes()).hexdigest()
meta['qc']['local_media_qc'] = 'passed'
meta['qc']['drive_verified'] = False
meta['qc']['drive_manifest_uploaded'] = False
meta['qc']['drive_manifest_file_id'] = None
meta['qc']['drive_folder_id'] = None
meta['qc']['drive_verification_note'] = 'Pending canonical Drive upload and independent exact-package verification.'
meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'measured_narration_duration_seconds': meta['measured_narration_duration_seconds'], 'measured_mp4_sha256': meta['measured_mp4_sha256'], 'local_media_qc': meta['qc']['local_media_qc']}, ensure_ascii=False, indent=2))
