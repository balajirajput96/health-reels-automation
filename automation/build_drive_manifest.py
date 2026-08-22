#!/usr/bin/env python3
"""Build a local-to-Drive manifest from a saved gws Drive files-list response."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
listing_path = Path('/tmp/reel_0003_drive_listing.json')
out_path = ROOT / 'state' / 'reel_0003_drive_upload_manifest.json'
folder_id = '151fUghK2X7wURMqBZtPxTzD7AtlOZWtn'

mapping = {
    'reel_0003_self_concept_what_studies_measure_hi.mp4': ROOT / 'assets/reel_0003_self_concept_what_studies_measure_hi.mp4',
    'reel_0003_self_concept_what_studies_measure_narration_hi.wav': ROOT / 'assets/reel_0003_self_concept_what_studies_measure_narration_hi.wav',
    'reel_0003_self_concept_what_studies_measure_captions_hi.srt': ROOT / 'assets/reel_0003_self_concept_what_studies_measure_captions_hi.srt',
    'reel_0003_metadata.json': ROOT / 'assets/reel_0003_metadata.json',
    'reel_0003_qc_report.json': ROOT / 'state/reel_0003_qc_report.json',
    'reel_0003_self_concept_sources.md': ROOT / 'research/reel_0003_self_concept_sources.md',
    'reel_0003_self_concept_script.md': ROOT / 'research/reel_0003_self_concept_script.md',
    'reel_0003_self_concept_source_notes.md': ROOT / 'research/reel_0003_self_concept_source_notes.md',
    'reel_0003_self_concept_what_studies_measure_visual_reference.png': ROOT / 'assets/reel_0003_self_concept_what_studies_measure_visual_reference.png',
    'reel_0003_scene_01_questionnaire.png': ROOT / 'assets/reel_0003_scene_01_questionnaire.png',
    'reel_0003_scene_02_clarity_scale.png': ROOT / 'assets/reel_0003_scene_02_clarity_scale.png',
    'reel_0003_scene_03_multiple_instruments.png': ROOT / 'assets/reel_0003_scene_03_multiple_instruments.png',
    'reel_0003_scene_04_research_window.png': ROOT / 'assets/reel_0003_scene_04_research_window.png',
}

listing = json.loads(listing_path.read_text())
remote = {item['name']: item for item in listing.get('files', [])}
missing = sorted(set(mapping) - set(remote))
if missing:
    raise SystemExit(f'Missing remote objects: {missing}')

files = []
for name, local in mapping.items():
    data = local.read_bytes()
    item = remote[name]
    files.append({
        'name': name,
        'local_path': str(local.relative_to(ROOT)),
        'local_bytes': len(data),
        'local_sha256': hashlib.sha256(data).hexdigest(),
        'drive_file_id': item['id'],
        'drive_bytes': int(item.get('size', 0)),
        'drive_md5': item.get('md5Checksum'),
        'drive_mime_type': item['mimeType'],
        'drive_parent_id': item['parents'][0],
        'drive_modified_time': item.get('modifiedTime'),
        'drive_web_view_link': item.get('webViewLink'),
    })

bad_sizes = [f['name'] for f in files if f['local_bytes'] != f['drive_bytes']]
if bad_sizes:
    raise SystemExit(f'Byte-size mismatch: {bad_sizes}')

manifest = {
    'schema_version': 1,
    'reel_id': 'reel_0003_self_concept_what_studies_measure',
    'sequence': 3,
    'batch': 'Batch_001',
    'drive_folder_id': folder_id,
    'drive_path': '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0003',
    'drive_verification': 'verified_by_gws_files_list',
    'object_count': len(files),
    'total_bytes': sum(f['drive_bytes'] for f in files),
    'files': files,
}
out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'output': str(out_path), 'object_count': len(files), 'total_bytes': manifest['total_bytes']}, ensure_ascii=False))
