import json
from pathlib import Path

listing_path = Path('/home/ubuntu/repos/health-reels-automation/state/reel_0004_drive_listing_final.json')
data = json.loads(listing_path.read_text())
files = data.get('files', [])
expected = {
    'reel_0004_cognitive_biases_what_studies_measure_hi.mp4',
    'reel_0004_cognitive_biases_what_studies_measure_narration_hi.wav',
    'reel_0004_cognitive_biases_what_studies_measure_captions_hi.srt',
    'reel_0004_metadata.json',
    'reel_0004_qc_report.json',
    'reel_0004_drive_upload_manifest.json',
    'reel_0004_cognitive_biases_what_studies_measure_sources.md',
    'reel_0004_cognitive_biases_what_studies_measure_script.md',
    'reel_0004_scene_01.png',
    'reel_0004_scene_02.png',
    'reel_0004_scene_03.png',
    'reel_0004_scene_04.png',
}
by_name = {item.get('name'): item for item in files if item.get('name')}
missing = sorted(expected - set(by_name))
zero_size = sorted(
    name for name in expected
    if name in by_name and int(by_name[name].get('size') or 0) <= 0
)
summary = {
    'folder_objects': len(files),
    'current_expected': len(expected),
    'missing': missing,
    'zero_size': zero_size,
    'current_objects': [
        {
            key: by_name[name].get(key)
            for key in ('name', 'id', 'mimeType', 'size', 'md5Checksum')
        }
        for name in sorted(expected)
        if name in by_name
    ],
}
print(json.dumps(summary, ensure_ascii=False, indent=2))
if missing or zero_size:
    raise SystemExit(1)
