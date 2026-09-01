#!/usr/bin/env python3
"""Build a local-to-Drive manifest from a saved gws Drive files-list response."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--listing', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--folder-id', required=True)
    parser.add_argument('--reel-id', required=True)
    parser.add_argument('--sequence', required=True, type=int)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--drive-path', required=True)
    parser.add_argument('--mapping', required=True, help='JSON object mapping remote names to local paths')
    args = parser.parse_args()

    listing_path = args.listing if args.listing.is_absolute() else ROOT / args.listing
    out_path = args.output if args.output.is_absolute() else ROOT / args.output
    mapping = json.loads(args.mapping)
    listing = json.loads(listing_path.read_text())
    remote = {item['name']: item for item in listing.get('files', [])}
    missing = sorted(set(mapping) - set(remote))
    if missing:
        raise SystemExit(f'Missing remote objects: {missing}')

    files = []
    for name, local_name in mapping.items():
        local = Path(local_name)
        if not local.is_absolute():
            local = ROOT / local
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
        'reel_id': args.reel_id,
        'sequence': args.sequence,
        'batch': args.batch,
        'drive_folder_id': args.folder_id,
        'drive_path': args.drive_path,
        'drive_verification': 'verified_by_gws_files_list',
        'object_count': len(files),
        'total_bytes': sum(f['drive_bytes'] for f in files),
        'files': files,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(out_path), 'object_count': len(files), 'total_bytes': manifest['total_bytes']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
