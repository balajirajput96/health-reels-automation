from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'state'
QUEUE = STATE / 'reels_3000_queue.jsonl'
CHECKPOINT = STATE / 'reels_3000_checkpoint.json'
RECORD = ROOT / 'records' / 'reels' / 'batch01' / 'reel0004'
QC = ROOT / 'work' / 'reel_0004' / 'qc.json'
TARGET = 'reel_0004_cognitive_biases_what_studies_measure'


def now() -> str:
    return datetime.now(UTC).isoformat().replace('+00:00', 'Z')


def atomic_write(path: Path, text: str) -> None:
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(text, encoding='utf-8')
    temp.replace(path)


def main() -> None:
    RECORD.mkdir(parents=True, exist_ok=True)
    stamp = now().replace(':', '').replace('-', '')
    shutil.copy2(QUEUE, RECORD / f'pre_state_queue_{stamp}.jsonl')
    shutil.copy2(CHECKPOINT, RECORD / f'pre_state_checkpoint_{stamp}.json')
    queue_lines = [line for line in QUEUE.read_text(encoding='utf-8').splitlines() if line.strip()]
    entries = [json.loads(line) for line in queue_lines]
    matches = [entry for entry in entries if entry.get('reel_id') == TARGET]
    if len(matches) != 1:
        raise RuntimeError(f'Expected exactly one queue entry for {TARGET}, found {len(matches)}')
    checkpoint = json.loads(CHECKPOINT.read_text(encoding='utf-8'))
    if checkpoint.get('next_reel') != TARGET or checkpoint.get('next_sequence') != 4:
        raise RuntimeError('Checkpoint no longer points to reel 0004; refusing to mutate state')
    qc = json.loads(QC.read_text(encoding='utf-8'))
    if not qc.get('valid'):
        raise RuntimeError('Local QC is not valid; refusing to record this state')
    target = matches[0]
    target['asset_checksums'] = qc['sha256']
    target['research_stage'] = 'verified'
    target['source_ids'] = ['DOI:10.3389/fpsyg.2021.630177', 'DOI:10.3389/fpsyg.2015.01770', 'DOI:10.3758/s13428-022-01804-9']
    target['safety_status'] = 'SAFE_WITH_CAVEATS'
    target['failure_count'] = int(target.get('failure_count', 0)) + 1
    target['retries'] = int(target.get('retries', 0)) + 1
    target['notes'] = ('Local evidence, Hindi script, narration, procedural 9:16 visuals, assembly, and deterministic QC passed. '
                       'Authenticated Drive inspection found the canonical Reel_0004 folder occupied by a verified but different topic '
                       '(MND-L01-Q04, Default Mode Network). No upload, overwrite, duplicate folder, or public posting performed. '
                       'Retryable blocker recorded in checkpoint failure_log; re-check canonical identity before any upload.')
    target['qc'] = {
        'ai_disclosure': True,
        'aspect_ratio_9_16': True,
        'captions': True,
        'decode_ok': True,
        'drive_verified': False,
        'duration_seconds': qc['local_media_probe']['duration_seconds'],
        'hindi_audio': True,
    }
    atomic_write(QUEUE, ''.join(json.dumps(entry, ensure_ascii=False, separators=(',', ':')) + '\n' for entry in entries))
    failure = {
        'reel_id': TARGET,
        'stage': 'canonical_path_topic_conflict',
        'status': 'blocked_retryable',
        'exact_error': ('Canonical Drive path 3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0004 already contains folder ID '
                        '1dL1yz1Lx3tnT9ali6nujGLHvmAbJLwIa with a verified package titled '
                        '"मन भटकते क्यों है? Default Mode Network की कहानी" (tuple MND-L01-Q04), '
                        'which conflicts with queued topic "संज्ञानात्मक पूर्वाग्रह: अध्ययन वास्तव में क्या मापते हैं". '
                        'Upload and overwrite were refused to prevent duplicate or ambiguous canonical records.'),
        'retry_state': 'keep next_reel at reel_0004; re-check authoritative remote identity before upload',
        'local_qc': 'passed',
        'recorded_at': now(),
    }
    failure_log = checkpoint.setdefault('failure_log', [])
    failure_log.append(failure)
    checkpoint['next_reel'] = TARGET
    checkpoint['next_sequence'] = 4
    checkpoint['last_completed'] = 'reel_0003_self_concept_what_studies_measure'
    checkpoint['completed_drive_verified'] = 3
    checkpoint['production_counts'] = {'final': 3, 'planned': 2997}
    checkpoint['updated_at'] = now()
    atomic_write(CHECKPOINT, json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'queue_updated': TARGET, 'checkpoint_next_reel': checkpoint['next_reel'], 'failure': failure}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
