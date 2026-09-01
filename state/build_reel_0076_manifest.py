import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = (ROOT / 'state/reel_0076_drive_folder_id.txt').read_text().strip()
listing = json.loads((ROOT / 'state/reel_0076_drive_listing_post_final_metadata.json').read_text())
remote = {item['name']: item for item in listing.get('files', [])}
files = [
    ('reel_0076_procrastination_what_studies_measure_hi.mp4', 'assets/reel_0076_procrastination_what_studies_measure_hi.mp4'),
    ('reel_0076_procrastination_what_studies_measure_narration_hi.wav', 'assets/reel_0076_procrastination_what_studies_measure_narration_hi.wav'),
    ('reel_0076_procrastination_what_studies_measure_captions_hi.srt', 'assets/reel_0076_procrastination_what_studies_measure_captions_hi.srt'),
    ('reel_0076_metadata.json', 'assets/reel_0076_metadata.json'),
    ('reel_0076_qc_report.json', 'assets/reel_0076_qc_report.json'),
    ('reel_0076_procrastination_what_studies_measure_sources.md', 'research/reel_0076_procrastination_what_studies_measure_sources.md'),
    ('reel_0076_procrastination_what_studies_measure_script.md', 'research/reel_0076_procrastination_what_studies_measure_script.md'),
    ('reel_0076_scene_01.png', 'assets/reel_0076_scene_01.png'),
    ('reel_0076_scene_02.png', 'assets/reel_0076_scene_02.png'),
    ('reel_0076_scene_03.png', 'assets/reel_0076_scene_03.png'),
    ('reel_0076_scene_04.png', 'assets/reel_0076_scene_04.png'),
]
entries = []
total = 0
for name, rel in files:
    path = ROOT / rel
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    item = remote.get(name)
    if item is None:
        raise SystemExit(f'missing remote object: {name}')
    local_bytes = len(data)
    drive_bytes = int(item.get('size', 0) or 0)
    total += local_bytes
    entries.append({
        'name': name,
        'local_path': rel,
        'local_bytes': local_bytes,
        'local_sha256': sha,
        'drive_file_id': item.get('id'),
        'drive_bytes': drive_bytes,
        'drive_md5': item.get('md5Checksum'),
        'drive_mime_type': item.get('mimeType'),
        'drive_parent_id': (item.get('parents') or [None])[0],
        'drive_modified_time': item.get('modifiedTime'),
        'drive_web_view_link': item.get('webViewLink'),
    })
manifest = {
    'schema_version': 1,
    'reel_id': 'reel_0076_procrastination_what_studies_measure',
    'sequence': 76,
    'batch': 'Batch_003',
    'drive_folder_id': FOLDER,
    'drive_path': '3000_HINDI_RESEARCH_REELS/Batch_003/Reel_0076',
    'drive_verification': 'verified_by_gws_files_list',
    'object_count': len(entries),
    'total_bytes': total,
    'files': entries,
}
out = ROOT / 'state/reel_0076_drive_upload_manifest_v1.json'
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(out)
print(json.dumps({'object_count': len(entries), 'total_bytes': total, 'all_drive_parents_match': all(e['drive_parent_id'] == FOLDER for e in entries)}, ensure_ascii=False))
