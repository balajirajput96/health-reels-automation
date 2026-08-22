from __future__ import annotations

import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path('/home/ubuntu/repos/health-reels-automation')
QUEUE = ROOT / 'state' / 'reels_3000_queue.jsonl'
CHECKPOINT = ROOT / 'state' / 'reels_3000_checkpoint.json'
LEDGER = ROOT / 'state' / 'reels_ledger.json'
MANIFEST = ROOT / 'remote_reel003_drive_upload_manifest.json'
METADATA = ROOT / 'remote_reel003_metadata.json'
REMOTE_QC = ROOT / 'remote_reel003_qc_report.json'
RECON = ROOT / 'records' / 'reels' / 'batch01' / 'reel0003' / 'remote_reconciliation_qc.json'
TARGET = 'reel_0003_self_concept_what_studies_measure'


def atomic_write(path: Path, text: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def now() -> str:
    return datetime.now(UTC).isoformat().replace('+00:00', 'Z')


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    metadata = json.loads(METADATA.read_text(encoding='utf-8'))
    remote_qc = json.loads(REMOTE_QC.read_text(encoding='utf-8'))
    recon = json.loads(RECON.read_text(encoding='utf-8'))
    if recon.get('valid') is not True:
        raise RuntimeError('Refusing state update: independent Drive reconciliation is not valid.')
    if manifest.get('drive_path') != '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0003':
        raise RuntimeError('Refusing state update: canonical Drive path mismatch.')
    if metadata.get('reel_id') != TARGET:
        raise RuntimeError('Refusing state update: remote metadata reel ID mismatch.')
    if remote_qc.get('valid') is not True:
        raise RuntimeError('Refusing state update: remote QC record is not valid.')
    lines = QUEUE.read_text(encoding='utf-8').splitlines(keepends=True)
    matches = []
    parsed = []
    for index, raw in enumerate(lines):
        if not raw.strip():
            parsed.append(None)
            continue
        item = json.loads(raw)
        parsed.append(item)
        if item.get('reel_id') == TARGET:
            matches.append((index, item))
    if len(matches) != 1:
        raise RuntimeError(f'Refusing state update: expected exactly one queue record for {TARGET}, found {len(matches)}.')
    target_index, target = matches[0]
    existing_ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    ledger_items = existing_ledger.setdefault('items', [])
    if any(item.get('source_id') == TARGET or item.get('sha256') == recon.get('downloaded_video_sha256') for item in ledger_items):
        if target.get('production_stage') == 'final' and target.get('qc', {}).get('drive_verified') is True:
            print(json.dumps({'status': 'already_complete', 'reel_id': TARGET}, ensure_ascii=False))
            return 0
        raise RuntimeError('Refusing state update: matching ledger identity exists but queue state is not already complete.')
    if target.get('sequence') != 3 or target.get('production_stage') not in {'planned', 'research', 'assembled'}:
        raise RuntimeError(f'Refusing state update: unexpected target queue state {target.get("production_stage")} / sequence {target.get("sequence")}.')
    manifest_by_name = {entry['name']: entry for entry in manifest.get('files', [])}
    def h(name: str) -> str:
        if name not in manifest_by_name:
            raise RuntimeError(f'Manifest missing expected asset {name}.')
        return manifest_by_name[name]['local_sha256']
    target.update({
        'asset_checksums': {
            'mp4': h('reel_0003_self_concept_what_studies_measure_hi.mp4'),
            'wav': h('reel_0003_self_concept_what_studies_measure_narration_hi.wav'),
            'srt': h('reel_0003_self_concept_what_studies_measure_captions_hi.srt'),
            'metadata.json': h('reel_0003_metadata.json'),
            'sources.md': h('reel_0003_self_concept_sources.md'),
            'script.md': h('reel_0003_self_concept_script.md'),
            'visual_reference.png': h('reel_0003_self_concept_what_studies_measure_visual_reference.png'),
        },
        'evidence_class': metadata.get('evidence_class'),
        'failure_count': 0,
        'notes': 'Pre-existing canonical Drive package reconciled in this run; authenticated listing and independent local media QC verified; no duplicate folder/file created; not published.',
        'production_stage': 'final',
        'qc': {
            'ai_disclosure': True,
            'aspect_ratio_9_16': True,
            'captions': True,
            'decode_ok': True,
            'drive_verified': True,
            'duration_seconds': remote_qc.get('checks', {}).get('duration_seconds'),
            'hindi_audio': True,
        },
        'research_stage': 'verified',
        'retries': 0,
        'safety_status': metadata.get('safety_status', 'SAFE_WITH_CAVEATS'),
        'source_ids': metadata.get('source_ids', []),
    })
    parsed[target_index] = target
    new_queue = ''.join(('' if item is None else json.dumps(item, ensure_ascii=False) + '\n') for item in parsed)
    checkpoint = json.loads(CHECKPOINT.read_text(encoding='utf-8'))
    next_item = next((item for item in parsed if item and item.get('sequence') == 4), None)
    checkpoint.update({
        'completed_drive_verified': 3,
        'failure_log': checkpoint.get('failure_log', []) + [
            {'reel_id': TARGET, 'stage': 'drive_reconciliation_helper', 'status': 'recovered', 'exact_error': 'gws drive files download returned 500 backendError; alternate authenticated file-content get succeeded.', 'recorded_at': now()},
            {'reel_id': TARGET, 'stage': 'connector_config_inspection', 'status': 'non_blocking', 'exact_error': 'manus-config config load --search drive returned permission_denied: 403 Forbidden; authenticated Google Workspace Drive CLI remained available.', 'recorded_at': now()},
        ],
        'last_completed': TARGET,
        'next_reel': next_item.get('reel_id') if next_item else None,
        'next_sequence': next_item.get('sequence') if next_item else None,
        'production_counts': {'final': 3, 'planned': 2997},
        'updated_at': now(),
    })
    ledger_items.append({
        'source_id': TARGET,
        'sha256': recon.get('downloaded_video_sha256'),
        'filename': 'reel_0003_self_concept_what_studies_measure_hi.mp4',
        'stage': 'drive_verified',
        'target_account': '@balajirajput96',
        'drive_folder_id': manifest.get('drive_folder_id'),
        'drive_file_id': manifest_by_name['reel_0003_self_concept_what_studies_measure_hi.mp4']['drive_file_id'],
        'recorded_at': now(),
        'notes': 'Existing authenticated Drive package reconciled at canonical nested path 3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0003; independent local QC passed; no social publication or post ID created.',
    })
    atomic_write(QUEUE, new_queue)
    atomic_write(CHECKPOINT, json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n')
    atomic_write(LEDGER, json.dumps(existing_ledger, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'completed', 'reel_id': TARGET, 'next_reel': checkpoint.get('next_reel'), 'ledger_stage': 'drive_verified', 'drive_path': manifest.get('drive_path')}, ensure_ascii=False))


if __name__ == '__main__':
    raise SystemExit(main())
