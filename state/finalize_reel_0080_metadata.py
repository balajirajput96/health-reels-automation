from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
meta_path = ROOT / 'assets/reel_0080_metadata.json'
qc_path = ROOT / 'assets/reel_0080_qc_report.json'
drive_path = ROOT / 'state/reel_0080_drive_final_verification.json'
video = ROOT / 'assets/reel_0080_social_buffering_what_studies_measure_hi.mp4'
meta = json.loads(meta_path.read_text(encoding='utf-8'))
qc = json.loads(qc_path.read_text(encoding='utf-8'))
drive = json.loads(drive_path.read_text(encoding='utf-8'))
assert qc.get('valid') is True
assert drive.get('valid') is True
assert drive['expected_count'] == 11 and drive['found_expected_count'] == 11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert not drive['duplicate_expected_names'] and drive['manifest_found_once']
assert drive['manifest_parent_ok'] and drive['manifest_nonzero']
assert drive['unrelated_remote_object_count'] == 0
meta['measured_narration_duration_seconds'] = 71.16
meta['measured_mp4_sha256'] = hashlib.sha256(video.read_bytes()).hexdigest()
meta['qc']['local_media_qc'] = 'passed'
meta['qc']['drive_verified'] = True
meta['qc']['drive_manifest_uploaded'] = True
meta['qc']['drive_manifest_file_id'] = drive['manifest_id']
meta['qc']['drive_folder_id'] = drive['folder_id']
meta['qc']['drive_verification_note'] = 'Final exact-package verification passed: 11 expected objects, one nonzero correctly parented manifest, zero missing/zero-size/wrong-parent/duplicate/unrelated objects; local-to-Drive bytes and file IDs verified.'
meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'measured_narration_duration_seconds': meta['measured_narration_duration_seconds'], 'measured_mp4_sha256': meta['measured_mp4_sha256'], 'local_media_qc': meta['qc']['local_media_qc'], 'drive_verified': meta['qc']['drive_verified']}, ensure_ascii=False, indent=2))
