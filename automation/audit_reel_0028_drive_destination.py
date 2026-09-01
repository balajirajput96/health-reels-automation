import json
from pathlib import Path
p=Path('state/reel_0028_drive_listing_pre_creation.json')
d=json.loads(p.read_text())
files=d.get('files',[])
hits=[f for f in files if f.get('name')=='Reel_0028' or f.get('name','').startswith('Reel_0028')]
print('BATCH001_OBJECTS',len(files))
print('REEL28_MATCHES',json.dumps(hits,ensure_ascii=False))
assert not hits
