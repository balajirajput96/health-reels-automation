import json
from pathlib import Path
rows=[json.loads(x) for x in Path('state/reels_3000_queue.jsonl').read_text().splitlines() if x.strip()]
assert len(rows)==3000
r=next(x for x in rows if int(x.get('sequence',-1))==27)
assert r['production_stage']=='final' and r['research_stage']=='verified' and r['qc']['drive_verified'] is True
cp=json.loads(Path('state/reels_3000_checkpoint.json').read_text())
assert cp['production_counts']=={'final':27,'planned':2973} and cp['completed_drive_verified']==27 and cp['next_sequence']==28
assert json.loads(Path('assets/reel_0027_qc_report.json').read_text())['valid'] is True
v=json.loads(Path('state/reel_0027_drive_verification.json').read_text())
assert v['valid'] is True and v['expected_count']==11 and v['found_expected_count']==11 and v['unrelated_remote_object_count']==0
m=json.loads(Path('assets/reel_0027_metadata.json').read_text())
assert m['qc']['local_media_qc']=='passed' and m['qc']['drive_verified'] is True and m['publication']['status']=='not_published'
items=json.loads(Path('state/reels_ledger.json').read_text())['items']
assert sum(1 for x in items if x.get('source_id')=='reel_0027_observational_learning_what_studies_measure' and x.get('stage')=='final')==1
print('REEL27_POST_PUSH_OK queue=3000 final=27 planned=2973 next=28 qc=true drive=true ledger=true')
