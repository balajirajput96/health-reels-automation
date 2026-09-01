import json
from pathlib import Path
rows=[json.loads(x) for x in Path('state/reels_3000_queue.jsonl').read_text().splitlines() if x.strip()]
assert len(rows)==3000
r=next(x for x in rows if int(x.get('sequence',-1))==29)
assert r['production_stage']=='final' and r['research_stage']=='verified' and r['qc']['drive_verified'] is True
cp=json.loads(Path('state/reels_3000_checkpoint.json').read_text())
assert cp['production_counts']=={'final':29,'planned':2971} and cp['completed_drive_verified']==29 and cp['next_sequence']==30
assert json.loads(Path('assets/reel_0029_qc_report.json').read_text())['valid'] is True
v=json.loads(Path('state/reel_0029_drive_verification.json').read_text())
assert v['valid'] is True and v['expected_count']==11 and v['found_expected_count']==11 and v['unrelated_remote_object_count']==0
m=json.loads(Path('assets/reel_0029_metadata.json').read_text())
assert m['qc']['local_media_qc']=='passed' and m['qc']['drive_verified'] is True and m['publication']['status']=='not_published'
items=json.loads(Path('state/reels_ledger.json').read_text())['items']
assert sum(1 for x in items if x.get('source_id')=='reel_0029_choice_architecture_what_studies_measure' and x.get('stage')=='final')==1
print('REEL29_CLOSURE_OK queue=3000 final=29 planned=2971 next=30 qc=true drive=true ledger=true')
