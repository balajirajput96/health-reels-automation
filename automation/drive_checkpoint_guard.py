"""Validate the controlled Drive checkpoint without making external calls.

The guard deliberately verifies *local evidence alignment*, not Drive connectivity. A
production worker remains responsible for authenticated Drive verification before it
records a completed reel. This check prevents an old checked-in pointer from advancing
past newer queue/checkpoint blockers merely because the pointer has syntactically valid
file IDs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POINTER = ROOT / "state" / "drive_active_state_pointer.json"
QUEUE = ROOT / "state" / "reels_3000_queue.jsonl"
CHECKPOINT = ROOT / "state" / "reels_3000_checkpoint.json"
PROJECT = "3000_HINDI_RESEARCH_REELS"
COMPLETED_STATUS = "qc_passed_drive_verified"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_queue(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"Queue record at {path}:{line_number} is not an object")
        records.append(record)
    return records


def pointer_key(sequence: int) -> str:
    return f"reel_{sequence:04d}"


def sequence_from_key(value: str) -> int | None:
    match = re.fullmatch(r"reel_(\d{4})", value)
    return int(match.group(1)) if match else None


def queue_drive_verified(record: dict[str, Any]) -> bool:
    qc = record.get("qc")
    return (
        record.get("production_stage") == "final"
        and isinstance(qc, dict)
        and qc.get("drive_verified") is True
    )


def validate(pointer: dict[str, Any], queue: list[dict[str, Any]], checkpoint: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if pointer.get("project") != PROJECT:
        errors.append("Drive pointer project does not match the controlled project")
    if pointer.get("provider") != "Google Drive":
        errors.append("Drive pointer provider must be Google Drive")
    if pointer.get("root", {}).get("name") != PROJECT:
        errors.append("Drive pointer root name does not match the controlled project")
    if pointer.get("active_batch", {}).get("name") != "Batch_001":
        errors.append("Drive pointer active batch must be Batch_001")
    if pointer.get("target_total_reels") != 3000:
        errors.append("Drive pointer target_total_reels must remain 3000")
    if pointer.get("reels_per_batch") != 30:
        errors.append("Drive pointer reels_per_batch must remain 30")

    fmt = pointer.get("format", {})
    expected_format = {
        "language": "hi-IN",
        "aspect_ratio": "9:16",
        "target_duration_seconds": 60,
        "voice_required": True,
        "captions_required": True,
    }
    for key, expected in expected_format.items():
        if fmt.get(key) != expected:
            errors.append(f"Drive pointer format.{key} must be {expected!r}")

    sequences: set[int] = set()
    verified_records: dict[int, dict[str, Any]] = {}
    for record in queue:
        sequence = record.get("sequence")
        if not isinstance(sequence, int) or sequence < 1 or sequence > 3000:
            errors.append(f"Queue record has invalid sequence: {sequence!r}")
            continue
        if sequence in sequences:
            errors.append(f"Queue contains duplicate sequence {sequence:04d}")
            continue
        sequences.add(sequence)
        if queue_drive_verified(record):
            verified_records[sequence] = record

    completed = pointer.get("completed")
    if not isinstance(completed, dict):
        return errors + ["Drive pointer completed must be an object"]

    pointer_sequences: dict[int, dict[str, Any]] = {}
    for key, record in completed.items():
        sequence = sequence_from_key(key)
        if sequence is None:
            errors.append(f"Drive pointer has invalid completed key: {key!r}")
            continue
        if not isinstance(record, dict):
            errors.append(f"Drive pointer completed record {key} is not an object")
            continue
        pointer_sequences[sequence] = record

    expected_sequences = set(verified_records)
    actual_sequences = set(pointer_sequences)
    if actual_sequences != expected_sequences:
        missing = sorted(expected_sequences - actual_sequences)
        extra = sorted(actual_sequences - expected_sequences)
        if missing:
            errors.append("Drive pointer is missing queue-verified completions: " + ", ".join(f"{item:04d}" for item in missing))
        if extra:
            errors.append("Drive pointer claims completions not verified in the local queue: " + ", ".join(f"{item:04d}" for item in extra))

    for sequence, queue_record in verified_records.items():
        pointer_record = pointer_sequences.get(sequence)
        if not pointer_record:
            continue
        key = pointer_key(sequence)
        if pointer_record.get("status") != COMPLETED_STATUS:
            errors.append(f"Drive pointer {key} does not have {COMPLETED_STATUS} status")
        if not pointer_record.get("video_file_id"):
            errors.append(f"Drive pointer {key} has no video_file_id")
        queue_checksum = queue_record.get("asset_checksums", {}).get("mp4")
        pointer_checksum = pointer_record.get("video_sha256")
        if queue_checksum and pointer_checksum and queue_checksum != pointer_checksum:
            errors.append(f"Drive pointer {key} video SHA-256 differs from the verified queue record")

    completed_count = checkpoint.get("completed_drive_verified")
    if completed_count != len(verified_records):
        errors.append(
            "Checkpoint completed_drive_verified="
            f"{completed_count!r} does not equal queue-verified count {len(verified_records)}"
        )

    next_reel = checkpoint.get("next_reel")
    expected_next_sequence = max(verified_records, default=0) + 1
    if not isinstance(next_reel, str) or f"reel_{expected_next_sequence:04d}_" not in next_reel:
        errors.append(
            "Checkpoint next_reel must remain the first sequence after verified completion "
            f"({expected_next_sequence:04d})"
        )
    pointer_next = pointer.get("next_reel_id")
    if pointer_next != f"{expected_next_sequence:04d}":
        errors.append(
            "Drive pointer next_reel_id does not match the protected checkpoint "
            f"({pointer_next!r} != {expected_next_sequence:04d})"
        )
    return errors


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in (POINTER, QUEUE, CHECKPOINT) if not path.is_file()]
    if missing:
        print(json.dumps({"status": "FAIL", "errors": ["Missing required controlled state files: " + ", ".join(missing)]}, ensure_ascii=False))
        return 1
    try:
        pointer = load_json(POINTER)
        queue = load_queue(QUEUE)
        checkpoint = load_json(CHECKPOINT)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [f"Unable to parse controlled state: {exc}"]}, ensure_ascii=False))
        return 1
    errors = validate(pointer, queue, checkpoint)
    result = {
        "status": "PASS" if not errors else "FAIL",
        "project": pointer.get("project"),
        "queue_verified_sequences": sorted(
            record["sequence"] for record in queue if queue_drive_verified(record) and isinstance(record.get("sequence"), int)
        ),
        "next_reel_id": pointer.get("next_reel_id"),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
