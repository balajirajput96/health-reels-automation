from __future__ import annotations
import argparse
import json
from pathlib import Path

EXPECTED = {
    'reel_0041_identity_and_habits_what_studies_measure_hi.mp4',
    'reel_0041_identity_and_habits_what_studies_measure_narration_hi.wav',
    'reel_0041_identity_and_habits_what_studies_measure_captions_hi.srt',
    'reel_0041_metadata.json',
    'reel_0041_qc_report.json',
    'reel_0041_identity_and_habits_what_studies_measure_sources.md',
    'reel_0041_identity_and_habits_what_studies_measure_script.md',
    'reel_0041_scene_01.png',
    'reel_0041_scene_02.png',
    'reel_0041_scene_03.png',
    'reel_0041_scene_04.png',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--listing', type=Path, required=True)
    parser.add_argument('--folder-id', required=True)
    parser.add_argument('--manifest-id', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()

    files = json.loads(args.listing.read_text(encoding='utf-8')).get('files', [])
    current = {item.get('name'): item for item in files if item.get('name') in EXPECTED}
    manifests = [item for item in files if item.get('id') == args.manifest_id]
    missing = sorted(EXPECTED - set(current))
    zero = sorted(name for name, item in current.items() if int(item.get('size', 0) or 0) <= 0)
    wrong_parent = sorted(name for name, item in current.items() if args.folder_id not in (item.get('parents') or []))
    result = {
        'folder_id': args.folder_id,
        'manifest_id': args.manifest_id,
        'expected_count': len(EXPECTED),
        'found_expected_count': len(current),
        'missing': missing,
        'zero_size': zero,
        'wrong_parent': wrong_parent,
        'manifest_found_once': len(manifests) == 1,
        'manifest_parent_ok': len(manifests) == 1 and args.folder_id in (manifests[0].get('parents') or []),
        'manifest_nonzero': len(manifests) == 1 and int(manifests[0].get('size', 0) or 0) > 0,
        'unrelated_remote_object_count': max(0, len(files) - len(current) - len(manifests)),
        'unrelated_remote_objects': sorted(item.get('name') for item in files if item.get('name') not in EXPECTED and item.get('id') != args.manifest_id),
        'expected_objects': [
            {
                'name': name,
                'id': current[name].get('id'),
                'size': int(current[name].get('size', 0) or 0),
                'mimeType': current[name].get('mimeType'),
            }
            for name in sorted(current)
        ],
    }
    result['valid'] = not (
        missing or zero or wrong_parent or len(manifests) != 1
        or not result['manifest_parent_ok'] or not result['manifest_nonzero']
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text, end='')
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
