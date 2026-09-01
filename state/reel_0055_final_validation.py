from __future__ import annotations
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
qc=load('assets/reel_0055_qc_report.json'); assert qc['valid'] is True
assert qc['checks']['width']==1080 and qc['checks']['height']==1920 and 45<=qc['checks']['duration_seconds']<=75
assert qc['checks']['audio_stream']=={'codec':'aac','sample_rate':'48000','channels':1}
assert qc['checks']['caption_timing_ok'] is True and qc['checks']['source_records']==4
metadata=load('assets/reel_0055_metadata.json')
assert metadata['measured_narration_duration_seconds']==72.88
assert metadata['qc']['local_media_qc']=='passed' and metadata['qc']['drive_verified'] is True
assert metadata['qc']['drive_manifest_uploaded'] is True and metadata['qc']['drive_manifest_file_id']=='1tU7LSNsp5pPM2Pd9STnDKW7cmC1Dz-6E'
assert metadata['publication']['status']=='not_published'
drive=load('state/reel_0055_drive_final_verification.json'); assert drive['valid'] is True
assert drive['expected_count']==11 and drive['found_expected_count']==11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero'] and drive['unrelated_remote_object_count']==0
queue=[json.loads(x) for x in (ROOT/'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(queue)==3000
r55=next(x for x in queue if x['sequence']==55)
assert r55['production_stage']=='final' and r55['research_stage']=='verified' and r55['safety_status']=='SAFE_WITH_EDITS'
assert r55['qc']['drive_verified'] is True and r55['qc']['duration_seconds']==72.9
sha=(ROOT/'state/reel_0055_mp4_sha256.txt').read_text().split()[0]
assert r55['asset_checksums']['reel_0055_uncertainty_what_studies_measure_hi.mp4']==sha
assert set(r55['source_ids'])=={'doi:10.3389/fpsyg.2026.1844980','doi:10.3389/frvir.2023.951435','doi:10.3389/fpsyg.2019.02504','doi:10.1037/1076-898X.2.4.343'}
ledger=load('state/reels_ledger.json')['items']
records=[x for x in ledger if x.get('source_id')=='reel_0055_uncertainty_what_studies_measure' and x.get('stage')=='final']
assert len(records)==1 and records[0]['sha256']==sha and records[0]['target_account']=='@balajirajput96'
checkpoint=load('state/reels_3000_checkpoint.json')
assert checkpoint['production_counts']=={'final':55,'planned':2945} and checkpoint['completed_drive_verified']==55
assert checkpoint['next_sequence']==56 and checkpoint['next_reel']=='reel_0056_deliberation_what_studies_measure'
manifest=load('state/reel_0055_drive_upload_manifest.json'); assert len(manifest['files'])==11
assert any(f['name']=='reel_0055_uncertainty_what_studies_measure_hi.mp4' and f['local_sha256']==sha for f in manifest['files'])
assert hashlib.sha256((ROOT/'assets/reel_0055_uncertainty_what_studies_measure_hi.mp4').read_bytes()).hexdigest()==sha
print('R0055_FINAL_VALIDATION_OK')
print('queue_rows',len(queue),'ledger_final_records',len(records),'drive_expected',drive['found_expected_count'],'mp4_sha256',sha)
