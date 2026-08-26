from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
meta=load('assets/reel_0069_metadata.json'); qc=load('assets/reel_0069_qc_report.json'); assert qc['valid'] is True
checks=qc['checks']; assert checks['width']==1080 and checks['height']==1920 and checks['aspect_ratio_9_16'] is True and checks['duration_seconds']==62.0 and checks['duration_45_to_75'] is True
assert checks['audio_stream']=={'codec':'aac','sample_rate':'48000','channels':1} and checks['caption_cues']==15 and checks['caption_timing_ok'] is True
assert checks['source_records']==3 and checks['source_identifier_present'] is True and checks['ai_disclosure_present'] is True and checks['safety_wording_ok'] is True
assert meta['measured_narration_duration_seconds']==62.0 and meta['qc']['local_media_qc']=='passed' and meta['qc']['drive_verified'] is True and meta['qc']['drive_manifest_uploaded'] is True
assert meta['qc']['drive_manifest_file_id']=='1LAmXvrscUZz9eFFXariJPNC-975ooc7m' and meta['qc']['drive_verification_note']
assert meta['publication']['status']=='not_published' and len(meta['source_ids'])==3
for rel in [meta['assets']['video'],meta['assets']['narration'],meta['assets']['captions'],meta['assets']['script'],meta['assets']['sources'],meta['assets']['browser_findings'],meta['assets']['qc_report']]: assert (ROOT/rel).exists(), rel
assert (ROOT/'state/reel_0069_audio_probe_final.txt').read_text().strip()=='62.000000'
attempts=(ROOT/'state/reel_0069_audio_attempts.txt').read_text(); assert 'attempt1\t86.16\tfailed_duration' in attempts and 'attempt2\t62.00\taccepted_canonical' in attempts
assert 'reel_0068_social_learning' not in attempts
drive=load('state/reel_0069_drive_final_verification.json'); assert drive['valid'] is True and drive['expected_count']==11 and drive['found_expected_count']==11
assert not drive['missing'] and not drive['zero_size'] and not drive['wrong_parent'] and not drive['duplicate_expected_names'] and drive['manifest_found_once'] and drive['manifest_parent_ok'] and drive['manifest_nonzero'] and drive['unrelated_remote_object_count']==0
queue=[json.loads(x) for x in (ROOT/'state/reels_3000_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]; assert len(queue)==3000
row=next(x for x in queue if x['sequence']==69); assert row['production_stage']=='final' and row['research_stage']=='verified' and row['safety_status']=='SAFE_WITH_EDITS' and row['qc']['drive_verified'] is True and row['qc']['duration_seconds']==62.0
sha=(ROOT/'state/reel_0069_mp4_sha256.txt').read_text().split()[0]; assert row['asset_checksums']['reel_0069_empathy_what_studies_measure_hi.mp4']==sha
assert set(row['source_ids'])=={x['source_id'] for x in meta['source_ids']}
ledger=load('state/reels_ledger.json')['items']; records=[x for x in ledger if x.get('source_id')=='reel_0069_empathy_what_studies_measure' and x.get('stage')=='final']; assert len(records)==1 and records[0]['sha256']==sha and records[0]['target_account']=='@balajirajput96'
checkpoint=load('state/reels_3000_checkpoint.json'); assert checkpoint['production_counts']=={'final':69,'planned':2931} and checkpoint['completed_drive_verified']==69 and checkpoint['next_sequence']==70 and checkpoint['next_reel']=='reel_0070_dehumanization_what_studies_measure'
manifest=load('state/reel_0069_drive_upload_manifest.json'); assert len(manifest['files'])==11 and any(f['name']=='reel_0069_empathy_what_studies_measure_hi.mp4' and f['local_sha256']==sha for f in manifest['files'])
assert hashlib.sha256((ROOT/'assets/reel_0069_empathy_what_studies_measure_hi.mp4').read_bytes()).hexdigest()==sha
print('R0069_FINAL_VALIDATION_OK'); print('queue_rows',len(queue),'ledger_final_records',len(records),'drive_expected',drive['found_expected_count'],'mp4_sha256',sha)
