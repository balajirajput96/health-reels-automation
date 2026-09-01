import json
from pathlib import Path
obj=json.loads(Path('/tmp/reel0028_manifest.json').read_text())
assert obj.get('id') and obj.get('name')=='reel_0028_drive_upload_manifest.json'
Path('state/reel_0028_manifest_file_id.txt').write_text(obj['id']+'\n')
Path('state/reel_0028_manifest_upload.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('MANIFEST_UPLOADED',obj['id'])
