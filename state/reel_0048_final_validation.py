from __future__ import annotations
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))

qc = load('assets/reel_0048_qc_report.json')
assert qc['valid'] is True
assert qc['checks']['width'] == 1080 and qc['checks']['height'] == 1920
assert 45 <= qc['checks']['duration_seconds'] <= 75
assert qc['checks']['audio_stream'] == {'codec':'aac','sample_rate':'48000','channels':1}
assert qc['checks']['caption_timing_ok'] is True and qc['checks']['source_records'] == 3

drive = load('state/reel_0048_drive_final_verification.json')
assert drive['valid'] is True
assert drive['expected_count'] == 11 and drive['found_expected_count'] == 11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero']
assert drive['unrelated_remote_object_count'] == 0

queue = [json.loads(x) for x in (ROOT/'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(queue) == 3000
r48 = next(x for x in queue if x['sequence'] == 48)
assert r48['production_stage'] == 'final' and r48['research_stage'] == 'verified'
assert r48['safety_status'] == 'SAFE_WITH_EDITS' and r48['qc']['drive_verified'] is True
sha = (ROOT/'state/reel_0048_mp4_sha256.txt').read_text().split()[0]
assert r48['asset_checksums']['reel_0048_spacing_effect_what_studies_measure_hi.mp4'] == sha
assert set(r48['source_ids']) == {'doi:10.3389/fpsyg.2017.00962','doi:10.1111/j.1467-9280.2008.02209.x','doi:10.1007/s10648-020-09572-8'}

ledger = load('state/reels_ledger.json')['items']
records = [x for x in ledger if x.get('source_id') == 'reel_0048_spacing_effect_what_studies_measure' and x.get('stage') == 'final']
assert len(records) == 1 and records[0]['sha256'] == sha
checkpoint = load('state/reels_3000_checkpoint.json')
assert checkpoint['production_counts'] == {'final':48,'planned':2952}
assert checkpoint['completed_drive_verified'] == 48 and checkpoint['next_sequence'] == 49
assert checkpoint['next_reel'] == 'reel_0049_interleaving_what_studies_measure'
manifest = load('state/reel_0048_drive_upload_manifest.json')
assert len(manifest['files']) == 11
assert any(f['name']=='reel_0048_spacing_effect_what_studies_measure_hi.mp4' and f['local_sha256']==sha for f in manifest['files'])
print('R0048_FINAL_VALIDATION_OK')
print('queue_rows',len(queue),'ledger_final_records',len(records),'drive_expected',drive['found_expected_count'],'mp4_sha256',sha)
