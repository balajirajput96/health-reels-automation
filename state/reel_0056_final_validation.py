from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
qc=load('assets/reel_0056_qc_report.json'); assert qc['valid'] is True
assert qc['checks']['width']==1080 and qc['checks']['height']==1920 and 45<=qc['checks']['duration_seconds']<=75
assert qc['checks']['audio_stream']=={'codec':'aac','sample_rate':'48000','channels':1}
assert qc['checks']['caption_timing_ok'] is True and qc['checks']['source_records']==4
metadata=load('assets/reel_0056_metadata.json')
assert metadata['measured_narration_duration_seconds']==60.04
assert metadata['qc']['local_media_qc']=='passed' and metadata['qc']['drive_verified'] is True
assert metadata['qc']['drive_manifest_uploaded'] is True and metadata['qc']['drive_manifest_file_id']=='1pcDv_CcCIn9y_BhCUwr8GU0m3ftfS8YB'
assert metadata['publication']['status']=='not_published'
drive=load('state/reel_0056_drive_final_verification.json'); assert drive['valid'] is True
assert drive['expected_count']==11 and drive['found_expected_count']==11 and not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero'] and drive['unrelated_remote_object_count']==0
queue=[json.loads(x) for x in (ROOT/'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]; assert len(queue)==3000
r56=next(x for x in queue if x['sequence']==56)
assert r56['production_stage']=='final' and r56['research_stage']=='verified' and r56['safety_status']=='SAFE_WITH_EDITS'
assert r56['qc']['drive_verified'] is True and r56['qc']['duration_seconds']==60.067
sha=(ROOT/'state/reel_0056_mp4_sha256.txt').read_text().split()[0]
assert r56['asset_checksums']['reel_0056_deliberation_what_studies_measure_hi.mp4']==sha
assert set(r56['source_ids'])=={'doi:10.1038/s44159-025-00466-6','doi:10.1098/rstb.2011.0416','doi:10.1371/journal.pone.0186404','doi:10.1016/j.cogpsych.2015.05.001'}
ledger=load('state/reels_ledger.json')['items']; records=[x for x in ledger if x.get('source_id')=='reel_0056_deliberation_what_studies_measure' and x.get('stage')=='final']
assert len(records)==1 and records[0]['sha256']==sha and records[0]['target_account']=='@balajirajput96'
checkpoint=load('state/reels_3000_checkpoint.json'); assert checkpoint['production_counts']=={'final':56,'planned':2944} and checkpoint['completed_drive_verified']==56
assert checkpoint['next_sequence']==57 and checkpoint['next_reel']=='reel_0057_working_memory_what_studies_measure'
manifest=load('state/reel_0056_drive_upload_manifest.json'); assert len(manifest['files'])==11 and any(f['name']=='reel_0056_deliberation_what_studies_measure_hi.mp4' and f['local_sha256']==sha for f in manifest['files'])
assert hashlib.sha256((ROOT/'assets/reel_0056_deliberation_what_studies_measure_hi.mp4').read_bytes()).hexdigest()==sha
print('R0056_FINAL_VALIDATION_OK'); print('queue_rows',len(queue),'ledger_final_records',len(records),'drive_expected',drive['found_expected_count'],'mp4_sha256',sha)
