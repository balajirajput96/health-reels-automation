from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
qc=load('assets/reel_0050_qc_report.json'); assert qc['valid'] is True
assert qc['checks']['width']==1080 and qc['checks']['height']==1920 and 45<=qc['checks']['duration_seconds']<=75
assert qc['checks']['audio_stream']=={'codec':'aac','sample_rate':'48000','channels':1}
assert qc['checks']['caption_timing_ok'] is True and qc['checks']['source_records']==3

drive=load('state/reel_0050_drive_final_verification.json'); assert drive['valid'] is True
assert drive['expected_count']==11 and drive['found_expected_count']==11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero'] and drive['unrelated_remote_object_count']==0

queue=[json.loads(x) for x in (ROOT/'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(queue)==3000
r50=next(x for x in queue if x['sequence']==50)
assert r50['production_stage']=='final' and r50['research_stage']=='verified' and r50['safety_status']=='SAFE_WITH_EDITS'
assert r50['qc']['drive_verified'] is True
sha=(ROOT/'state/reel_0050_mp4_sha256.txt').read_text().split()[0]
assert r50['asset_checksums']['reel_0050_desirable_difficulty_what_studies_measure_hi.mp4']==sha
assert set(r50['source_ids'])=={'doi:10.1007/s10648-023-09766-w','doi:10.3758/s13421-018-0843-3','doi:10.1038/s41539-019-0053-1'}
ledger=load('state/reels_ledger.json')['items']
records=[x for x in ledger if x.get('source_id')=='reel_0050_desirable_difficulty_what_studies_measure' and x.get('stage')=='final']
assert len(records)==1 and records[0]['sha256']==sha
checkpoint=load('state/reels_3000_checkpoint.json')
assert checkpoint['production_counts']=={'final':50,'planned':2950} and checkpoint['completed_drive_verified']==50
assert checkpoint['next_sequence']==51 and checkpoint['next_reel']=='reel_0051_feedback_learning_what_studies_measure'
manifest=load('state/reel_0050_drive_upload_manifest.json'); assert len(manifest['files'])==11
assert any(f['name']=='reel_0050_desirable_difficulty_what_studies_measure_hi.mp4' and f['local_sha256']==sha for f in manifest['files'])
print('R0050_FINAL_VALIDATION_OK')
print('queue_rows',len(queue),'ledger_final_records',len(records),'drive_expected',drive['found_expected_count'],'mp4_sha256',sha)
