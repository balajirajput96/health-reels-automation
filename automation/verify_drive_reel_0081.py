from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    'reel_0081_stress_and_attention_what_studies_measure_hi.mp4',
    'reel_0081_stress_and_attention_what_studies_measure_narration_hi.wav',
    'reel_0081_stress_and_attention_what_studies_measure_captions_hi.srt',
    'reel_0081_metadata.json',
    'reel_0081_qc_report.json',
    'reel_0081_stress_and_attention_what_studies_measure_sources.md',
    'reel_0081_stress_and_attention_what_studies_measure_script.md',
    'reel_0081_scene_01.png',
    'reel_0081_scene_02.png',
    'reel_0081_scene_03.png',
    'reel_0081_scene_04.png',
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--listing', type=Path, required=True)
    parser.add_argument('--folder-id', required=True)
    parser.add_argument('--manifest-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    files = json.loads(args.listing.read_text(encoding='utf-8')).get('files', [])
    current = [item for item in files if item.get('name') in EXPECTED]
    by_name = {item.get('name'): item for item in current}
    manifests = [item for item in files if item.get('id') == args.manifest_id]
    missing = sorted(EXPECTED - set(by_name))
    zero = sorted(name for name, item in by_name.items() if int(item.get('size', 0) or 0) <= 0)
    wrong = sorted(name for name, item in by_name.items() if args.folder_id not in (item.get('parents') or []))
    duplicates = sorted(name for name in EXPECTED if sum(1 for item in files if item.get('name') == name) > 1)
    unrelated = [item for item in files if item.get('name') not in EXPECTED and item.get('id') != args.manifest_id]
    report = {
        'folder_id': args.folder_id,
        'manifest_id': args.manifest_id,
        'expected_count': 11,
        'found_expected_count': len(by_name),
        'missing': missing,
        'zero_size': zero,
        'wrong_parent': wrong,
        'duplicate_expected_names': duplicates,
        'manifest_found_once': len(manifests) == 1,
        'manifest_parent_ok': len(manifests) == 1 and args.folder_id in (manifests[0].get('parents') or []),
        'manifest_nonzero': len(manifests) == 1 and int(manifests[0].get('size', 0) or 0) > 0,
        'unrelated_remote_object_count': len(unrelated),
        'unrelated_remote_objects': sorted(item.get('name') for item in unrelated),
        'expected_objects': [
            {
                'name': name,
                'id': by_name[name].get('id'),
                'size': int(by_name[name].get('size', 0) or 0),
                'mimeType': by_name[name].get('mimeType'),
                'parents': by_name[name].get('parents'),
            }
            for name in sorted(by_name)
        ],
    }
    report['valid'] = not (
        missing or zero or wrong or duplicates or len(manifests) != 1
        or not report['manifest_parent_ok'] or not report['manifest_nonzero'] or unrelated
    )
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
