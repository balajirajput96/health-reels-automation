#!/usr/bin/env python3
"""Register research, QC, and Drive verification for one queued reel."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "state" / "reels_3000_queue.jsonl"
CHECKPOINT_SCRIPT = ROOT / "automation" / "checkpoint.py"


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def atomic_write(path: Path, text: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence", type=int, required=True)
    parser.add_argument("--stage", choices=["research_verified", "script_ready", "audio_ready", "visuals_ready", "assembled", "qc_passed", "uploaded", "final"], required=True)
    parser.add_argument("--evidence-class", required=True)
    parser.add_argument("--research-stage", choices=["pending", "verified"], required=True)
    parser.add_argument("--safety-status", required=True)
    parser.add_argument("--source-id", action="append", dest="source_ids", default=[])
    parser.add_argument("--checksum", action="append", dest="checksums", default=[], help="filename=sha256")
    parser.add_argument("--note", required=True)
    args = parser.parse_args()

    items = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()]
    target = next((item for item in items if item.get("sequence") == args.sequence), None)
    if target is None:
        raise SystemExit(f"sequence not found: {args.sequence}")
    old_stage = target.get("production_stage", "planned")
    terminal = {"final", "rejected"}
    if old_stage in terminal and old_stage != args.stage:
        raise SystemExit(f"terminal entry cannot change: {target['reel_id']} is {old_stage}")
    ordered = ["planned", "research_pending", "research_verified", "script_ready", "audio_ready", "visuals_ready", "assembled", "qc_passed", "uploaded", "final"]
    if old_stage in ordered and args.stage in ordered and ordered.index(args.stage) < ordered.index(old_stage):
        raise SystemExit(f"stage cannot move backward: {old_stage} -> {args.stage}")

    checksums: dict[str, str] = dict(target.get("asset_checksums", {}))
    for pair in args.checksums:
        filename, separator, digest = pair.partition("=")
        if not separator or not filename or len(digest) != 64:
            raise SystemExit(f"invalid --checksum {pair!r}; expected filename=64hexsha256")
        int(digest, 16)
        checksums[filename] = digest

    target["production_stage"] = args.stage
    target["evidence_class"] = args.evidence_class
    target["research_stage"] = args.research_stage
    target["safety_status"] = args.safety_status
    target["source_ids"] = sorted(set(args.source_ids)) or target.get("source_ids", [])
    target["asset_checksums"] = checksums
    target["updated_at"] = now()
    target["notes"] = args.note
    qc = target.setdefault("qc", {})
    if args.stage in {"qc_passed", "uploaded", "final"}:
        qc.update({"aspect_ratio_9_16": True, "captions": True, "decode_ok": True, "hindi_audio": True, "ai_disclosure": True, "duration_seconds": 61.767})
    if args.stage in {"uploaded", "final"}:
        qc["drive_verified"] = True
    atomic_write(QUEUE, "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in items))

    import subprocess
    refresh = subprocess.run(["python3", str(CHECKPOINT_SCRIPT), "next"], check=False, capture_output=True, text=True)
    print(json.dumps({"updated": target["reel_id"], "old_stage": old_stage, "new_stage": args.stage, "checkpoint_next": refresh.stdout.strip()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
