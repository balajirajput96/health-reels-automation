from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    'reel_0080_social_buffering_what_studies_measure_hi.mp4',
    'reel_0080_social_buffering_what_studies_measure_narration_hi.wav',
    'reel_0080_social_buffering_what_studies_measure_captions_hi.srt',
    'reel_0080_metadata.json',
    'reel_0080_qc_report.json',
    'reel_0080_social_buffering_what_studies_measure_sources.md',
    'reel_0080_social_buffering_what_studies_measure_script.md',
    'reel_0080_scene_01.png',
    'reel_0080_scene_02.png',
    'reel_0080_scene_03.png',
    'reel_0080_scene_04.png',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--listing', type=Path, required=True)
    parser.add_argument('--folder-id', required=True)
    parser.add_argument('--manifest-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    files = json.loads(args.listing.read_text(encoding='utf-8')).get('files', [])
    current = [f for f in files if f.get('name') in EXPECTED]
    by = {f.get('name'): f for f in current}
    manifests = [f for f in files if f.get('id') == args.manifest_id]
    missing = sorted(EXPECTED - set(by))
    zero = sorted(name for name, item in by.items() if int(item.get('size', 0) or 0) <= 0)
    wrong = sorted(name for name, item in by.items() if args.folder_id not in (item.get('parents') or []))
    dups = sorted(name for name in EXPECTED if sum(1 for f in files if f.get('name') == name) > 1)
    unrelated = [f for f in files if f.get('name') not in EXPECTED and f.get('id') != args.manifest_id]
    report = {
        'folder_id': args.folder_id,
        'manifest_id': args.manifest_id,
        'expected_count': 11,
        'found_expected_count': len(by),
        'missing': missing,
        'zero_size': zero,
        'wrong_parent': wrong,
        'duplicate_expected_names': dups,
        'manifest_found_once': len(manifests) == 1,
        'manifest_parent_ok': len(manifests) == 1 and args.folder_id in (manifests[0].get('parents') or []),
        'manifest_nonzero': len(manifests) == 1 and int(manifests[0].get('size', 0) or 0) > 0,
        'unrelated_remote_object_count': len(unrelated),
        'unrelated_remote_objects': sorted(f.get('name') for f in unrelated),
        'expected_objects': [
            {'name': name, 'id': by[name].get('id'), 'size': int(by[name].get('size', 0) or 0),
             'mimeType': by[name].get('mimeType'), 'parents': by[name].get('parents')}
            for name in sorted(by)
        ],
    }
    report['valid'] = not (
        missing or zero or wrong or dups or len(manifests) != 1
        or not report['manifest_parent_ok'] or not report['manifest_nonzero'] or unrelated
    )
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
