from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
qc=load('assets/reel_0053_qc_report.json'); assert qc['valid'] is True
assert qc['checks']['width']==1080 and qc['checks']['height']==1920 and 45<=qc['checks']['duration_seconds']<=75
assert qc['checks']['audio_stream']=={'codec':'aac','sample_rate':'48000','channels':1}
assert qc['checks']['caption_timing_ok'] is True and qc['checks']['source_records']==4

drive=load('state/reel_0053_drive_final_verification.json'); assert drive['valid'] is True
assert drive['expected_count']==11 and drive['found_expected_count']==11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent']
assert drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero'] and drive['unrelated_remote_object_count']==0

queue=[json.loads(x) for x in (ROOT/'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(queue)==3000
r53=next(x for x in queue if x['sequence']==53)
assert r53['production_stage']=='final' and r53['research_stage']=='verified' and r53['safety_status']=='SAFE_WITH_EDITS'
assert r53['qc']['drive_verified'] is True
sha=(ROOT/'state/reel_0053_mp4_sha256.txt').read_text().split()[0]
assert r53['asset_checksums']['reel_0053_framing_effect_what_studies_measure_hi.mp4']==sha
assert set(r53['source_ids'])=={'doi:10.1006/obhd.1998.2781','article:psicothema-3107','doi:10.1177/17456916221079611','doi:10.17179/excli2023-6169'}
ledger=load('state/reels_ledger.json')['items']
records=[x for x in ledger if x.get('source_id')=='reel_0053_framing_effect_what_studies_measure' and x.get('stage')=='final']
assert len(records)==1 and records[0]['sha256']==sha
checkpoint=load('state/reels_3000_checkpoint.json')
assert checkpoint['production_counts']=={'final':53,'planned':2947} and checkpoint['completed_drive_verified']==53
assert checkpoint['next_sequence']==54 and checkpoint['next_reel']=='reel_0054_base_rate_reasoning_what_studies_measure'
manifest=load('state/reel_0053_drive_upload_manifest.json'); assert len(manifest['files'])==11
assert any(f['name']=='reel_0053_framing_effect_what_studies_measure_hi.mp4' and f['local_sha256']==sha for f in manifest['files'])
print('R0053_FINAL_VALIDATION_OK')
print('queue_rows',len(queue),'ledger_final_records',len(records),'drive_expected',drive['found_expected_count'],'mp4_sha256',sha)
