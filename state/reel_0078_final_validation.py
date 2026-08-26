from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


meta = load('assets/reel_0078_metadata.json')
qc = load('assets/reel_0078_qc_report.json')
assert qc['valid'] is True
checks = qc['checks']
assert checks['width'] == 1080 and checks['height'] == 1920
assert checks['aspect_ratio_9_16'] is True and 45 <= checks['duration_seconds'] <= 75
assert abs(checks['duration_seconds'] - 73.600) < 0.01
assert checks['audio_stream'] == {'codec': 'aac', 'sample_rate': '48000', 'channels': 1}
assert checks['caption_cues'] == 15 and checks['caption_timing_ok'] is True
assert checks['source_records'] == 4 and checks['source_identifier_present'] is True
assert checks['ai_disclosure_present'] is True and checks['safety_wording_ok'] is True
assert abs(meta['measured_narration_duration_seconds'] - 73.60) < 0.01
assert meta['qc']['local_media_qc'] == 'passed'
assert meta['qc']['drive_verified'] is True and meta['qc']['drive_manifest_uploaded'] is True
assert meta['qc']['drive_manifest_file_id'] == (ROOT / 'state/reel_0078_manifest_file_id.txt').read_text().strip()
assert meta['qc']['drive_folder_id'] == (ROOT / 'state/reel_0078_drive_folder_id.txt').read_text().strip()
assert 'Final exact-package verification passed' in meta['qc']['drive_verification_note']
assert meta['publication']['status'] == 'not_published'
assert len(meta['source_ids']) == 4
for rel in [
    meta['assets']['video'], meta['assets']['narration'], meta['assets']['captions'],
    meta['assets']['script'], meta['assets']['sources'], meta['assets']['browser_findings'],
    meta['assets']['qc_report'],
]:
    assert (ROOT / rel).exists(), rel
attempts = (ROOT / 'state/reel_0078_audio_attempts.txt').read_text(encoding='utf-8')
assert attempts.count('attempt1\t124.68\tfailed_duration') == 1
assert attempts.count('attempt2\t91.12\tfailed_duration') == 1
assert attempts.count('attempt3\t73.60\taccepted_canonical') == 1
assert 'DURATION 124.68' in (ROOT / 'state/reel_0078_audio_probe_attempt1.txt').read_text(encoding='utf-8')
assert 'DURATION 91.12' in (ROOT / 'state/reel_0078_audio_probe_attempt2.txt').read_text(encoding='utf-8')
assert 'DURATION 73.60' in (ROOT / 'state/reel_0078_audio_probe_attempt3.txt').read_text(encoding='utf-8')
video = ROOT / 'assets/reel_0078_acute_stress_what_studies_measure_hi.mp4'
mp4_sha = hashlib.sha256(video.read_bytes()).hexdigest()
assert mp4_sha == meta['measured_mp4_sha256']
drive = load('state/reel_0078_drive_final_verification.json')
assert drive['valid'] is True and drive['expected_count'] == 11 and drive['found_expected_count'] == 11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert not drive['duplicate_expected_names'] and drive['manifest_found_once']
assert drive['manifest_parent_ok'] and drive['manifest_nonzero']
assert drive['unrelated_remote_object_count'] == 0
queue = [json.loads(line) for line in (ROOT / 'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(queue) == 3000
row = next(item for item in queue if item['sequence'] == 78)
assert row['production_stage'] == 'final' and row['research_stage'] == 'verified'
assert row['safety_status'] == 'SAFE_WITH_EDITS' and row['qc']['drive_verified'] is True
assert abs(row['qc']['duration_seconds'] - 73.6) < 0.01
assert row['asset_checksums']['reel_0078_acute_stress_what_studies_measure_hi.mp4'] == mp4_sha
ledger = load('state/reels_ledger.json')['items']
records = [item for item in ledger if item.get('source_id') == 'reel_0078_acute_stress_what_studies_measure' and item.get('stage') == 'final']
assert len(records) == 1 and records[0]['sha256'] == mp4_sha
checkpoint = load('state/reels_3000_checkpoint.json')
assert checkpoint['production_counts'] == {'final': 78, 'planned': 2922}
assert checkpoint['completed_drive_verified'] == 78
assert checkpoint['next_sequence'] == 79
assert checkpoint['next_reel'] == 'reel_0079_recovery_what_studies_measure'
manifest = load('state/reel_0078_drive_upload_manifest.json')
assert len(manifest['files']) == 11 and manifest['object_count'] == 11
assert manifest['drive_folder_id'] == (ROOT / 'state/reel_0078_drive_folder_id.txt').read_text().strip()
remote = {item['name']: item for item in load('state/reel_0078_drive_listing_final.json')['files']}
for item in manifest['files']:
    local = (ROOT / item['local_path']).read_bytes()
    assert len(local) == item['local_bytes'] == int(remote[item['name']]['size'])
    assert hashlib.sha256(local).hexdigest() == item['local_sha256']
    assert item['drive_file_id'] == remote[item['name']]['id']
print('R0078_FINAL_VALIDATION_OK')
print('queue_rows', len(queue), 'ledger_final_records', len(records), 'drive_expected', drive['found_expected_count'], 'mp4_sha256', mp4_sha)
