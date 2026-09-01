import json
from pathlib import Path
obj=json.loads(Path('/tmp/reel0029_folder.json').read_text())
assert obj.get('id') and obj.get('name')=='Reel_0029'
Path('state/reel_0029_drive_folder_id.txt').write_text(obj['id']+'\n')
Path('state/reel_0029_folder_creation.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('CREATED',obj['name'],obj['id'])
