from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/repos/health-reels-automation')
REMOTE = ROOT / 'work' / 'reel_0003_remote'
MANIFEST = ROOT / 'remote_reel003_drive_upload_manifest.json'
METADATA = ROOT / 'remote_reel003_metadata.json'
REMOTE_QC = ROOT / 'remote_reel003_qc_report.json'
SOURCES = REMOTE / 'sources.md'
OUT = ROOT / 'records' / 'reels' / 'batch01' / 'reel0003' / 'remote_reconciliation_qc.json'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def seconds(value: str) -> float:
    h, m, rest = value.split(':')
    s, ms = rest.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    metadata = json.loads(METADATA.read_text(encoding='utf-8'))
    recorded_qc = json.loads(REMOTE_QC.read_text(encoding='utf-8'))
    inventory = json.loads((ROOT / 'work_drive_reel003_inventory.json').read_text(encoding='utf-8'))
    problems: list[str] = []
    if manifest.get('drive_path') != '3000_HINDI_RESEARCH_REELS/Batch_001/Reel_0003':
        problems.append('canonical_path_mismatch')
    if manifest.get('drive_folder_id') != '151fUghK2X7wURMqBZtPxTzD7AtlOZWtn':
        problems.append('canonical_folder_id_mismatch')
    if manifest.get('object_count') != len(manifest.get('files', [])):
        problems.append('manifest_object_count_mismatch')
    inv_names = {item.get('name') for item in inventory.get('files', [])}
    manifest_names = {item.get('name') for item in manifest.get('files', [])}
    manifest_record_name = 'reel_0003_drive_upload_manifest.json'
    if inv_names != manifest_names | {manifest_record_name}:
        problems.append('inventory_manifest_name_mismatch')
    if metadata.get('reel_id') != 'reel_0003_self_concept_what_studies_measure':
        problems.append('metadata_reel_id_mismatch')
    if metadata.get('qc_gates', {}).get('drive_verified') is not True:
        problems.append('metadata_drive_verified_false')
    if not metadata.get('source_ids') or len(metadata.get('source_urls', [])) < 2:
        problems.append('remote_source_records_insufficient')
    video = REMOTE / 'final.mp4'
    probe = {}
    if not video.is_file():
        problems.append('remote_video_not_downloaded')
    else:
        cp = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)], capture_output=True, text=True, check=False)
        if cp.returncode:
            problems.append('remote_ffprobe_failed')
        else:
            probe = json.loads(cp.stdout)
    streams = probe.get('streams', [])
    vs = next((s for s in streams if s.get('codec_type') == 'video'), {})
    aus = next((s for s in streams if s.get('codec_type') == 'audio'), {})
    duration = float(probe.get('format', {}).get('duration', 0) or 0)
    media_ok = vs.get('width') == 1080 and vs.get('height') == 1920 and vs.get('codec_name') == 'h264' and aus.get('codec_name') == 'aac' and 45 <= duration <= 75
    if not media_ok:
        problems.append('remote_media_qc_failed')
    captions = REMOTE / 'captions.srt'
    caption_text = captions.read_text(encoding='utf-8') if captions.is_file() else ''
    cues = []
    for block in re.split(r'\n\s*\n', caption_text.strip()):
        m = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\n(.+)', block, re.S)
        if m:
            cues.append((seconds(m.group(1)), seconds(m.group(2)), m.group(3).strip()))
    caption_ok = len(cues) == 11 and all(start < end for start, end, _ in cues) and all(cues[i][1] <= cues[i + 1][0] + 0.001 for i in range(len(cues) - 1)) and bool(re.search(r'[\u0900-\u097F]', caption_text))
    if not caption_ok:
        problems.append('remote_caption_qc_failed')
    if not re.search(r'AI|AI-generated|AI-assisted', ' '.join([caption_text, json.dumps(metadata, ensure_ascii=False)]), re.I):
        problems.append('remote_ai_disclosure_missing')
    if not re.search(r'diagnosis|treatment advice|treatment|medical advice', caption_text, re.I):
        problems.append('remote_safety_wording_missing')
    manifest_hashes = {item.get('name'): item.get('local_sha256') for item in manifest.get('files', [])}
    downloaded_hash = sha256(video) if video.is_file() else None
    expected_video_hash = manifest_hashes.get('reel_0003_self_concept_what_studies_measure_hi.mp4')
    if downloaded_hash != expected_video_hash:
        problems.append('downloaded_video_sha256_mismatch')
    source_text = SOURCES.read_text(encoding='utf-8') if SOURCES.is_file() else ''
    source_ok = len(re.findall(r'https?://', source_text)) >= 2 and 'Evidence taxonomy' in source_text
    if not source_ok:
        problems.append('remote_source_file_qc_failed')
    result = {
        'valid': not problems,
        'problems': problems,
        'canonical_path': manifest.get('drive_path'),
        'drive_folder_id': manifest.get('drive_folder_id'),
        'object_count': manifest.get('object_count'),
        'remote_media': {
            'duration_seconds': round(duration, 3),
            'width': vs.get('width'),
            'height': vs.get('height'),
            'video_codec': vs.get('codec_name'),
            'audio_codec': aus.get('codec_name'),
            'geometry_and_codec_ok': media_ok,
        },
        'captions': {'cue_count': len(cues), 'timing_ok': caption_ok, 'devanagari_present': bool(re.search(r'[\u0900-\u097F]', caption_text))},
        'source_records': {'source_ids': metadata.get('source_ids', []), 'source_urls': metadata.get('source_urls', []), 'source_file_ok': source_ok},
        'disclosure_and_safety': {'ai_disclosure': bool(re.search(r'AI|AI-generated|AI-assisted', ' '.join([caption_text, json.dumps(metadata, ensure_ascii=False)]), re.I)), 'safety_wording': bool(re.search(r'diagnosis|treatment advice|treatment|medical advice', caption_text, re.I)), 'publication_allowed': False},
        'remote_recorded_qc': recorded_qc,
        'downloaded_video_sha256': downloaded_hash,
        'manifest_expected_video_sha256': expected_video_hash,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
