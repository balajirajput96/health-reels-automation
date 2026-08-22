#!/usr/bin/env python3
"""Resumable queue/checkpoint operations for the 3,000-reel mission."""
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
CHECKPOINT = ROOT / "state" / "reels_3000_checkpoint.json"
STAGES = ["planned", "research_pending", "research_verified", "script_ready", "audio_ready", "visuals_ready", "assembled", "qc_passed", "uploaded", "final", "failed", "rejected"]
TERMINAL = {"final", "rejected"}


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def read_items() -> list[dict[str, Any]]:
    return [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()]


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


def write_items(items: list[dict[str, Any]]) -> None:
    atomic_write(QUEUE, "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in items))


def refresh(items: list[dict[str, Any]], failure_log: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for item in items:
        stage = item.get("production_stage", "unknown")
        counts[stage] = counts.get(stage, 0) + 1
    completed = [i for i in items if i.get("production_stage") == "final" and i.get("qc", {}).get("drive_verified")]
    next_item = next((i for i in items if i.get("production_stage") not in TERMINAL), None)
    current = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
    data = {
        **current,
        "schema_version": 1,
        "mission": "3000 unique Hindi research reels",
        "total_reels": len(items),
        "total_batches": 100,
        "reels_per_batch": 30,
        "updated_at": now(),
        "production_counts": counts,
        "completed_drive_verified": len(completed),
        "next_reel": next_item.get("reel_id") if next_item else None,
        "next_sequence": next_item.get("sequence") if next_item else None,
        "last_completed": completed[-1].get("reel_id") if completed else None,
    }
    if failure_log is not None:
        data["failure_log"] = failure_log
    atomic_write(CHECKPOINT, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return data


def select_next() -> int:
    items = read_items()
    item = next((i for i in items if i.get("production_stage") not in TERMINAL), None)
    if not item:
        print(json.dumps({"next": None, "message": "all queue entries are terminal"}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps({"next": item}, ensure_ascii=False, indent=2))
    return 0


def mark(args: argparse.Namespace) -> int:
    items = read_items()
    target = next((i for i in items if i.get("sequence") == args.sequence), None)
    if not target:
        raise SystemExit(f"sequence not found: {args.sequence}")
    old = target.get("production_stage", "planned")
    if old in TERMINAL and old != args.stage:
        raise SystemExit(f"terminal entry cannot change: {target['reel_id']} is {old}")
    if old in STAGES and args.stage in STAGES and old not in {"failed", "rejected"} and args.stage not in {"failed", "rejected"} and STAGES.index(args.stage) < STAGES.index(old):
        raise SystemExit(f"stage cannot move backward: {old} -> {args.stage}")
    if args.stage == "final":
        qc = target.get("qc", {})
        if not qc.get("drive_verified") or not qc.get("decode_ok") or not qc.get("captions") or not qc.get("hindi_audio") or not qc.get("ai_disclosure"):
            raise SystemExit("final requires drive_verified, decode_ok, captions, hindi_audio, and ai_disclosure QC flags")
        if not target.get("source_ids"):
            raise SystemExit("final requires non-empty source_ids")
    target["production_stage"] = args.stage
    target["updated_at"] = now()
    if args.note:
        target["notes"] = args.note
    write_items(items)
    data = refresh(items)
    print(json.dumps({"updated": target["reel_id"], "old_stage": old, "new_stage": args.stage, "next_sequence": data["next_sequence"]}, ensure_ascii=False, indent=2))
    return 0


def failure(args: argparse.Namespace) -> int:
    items = read_items()
    target = next((i for i in items if i.get("sequence") == args.sequence), None)
    if not target:
        raise SystemExit(f"sequence not found: {args.sequence}")
    target["production_stage"] = "failed"
    target["failure_count"] = int(target.get("failure_count", 0)) + 1
    target["retries"] = int(target.get("retries", 0)) + 1
    target["updated_at"] = now()
    write_items(items)
    cp = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
    failures = cp.get("failure_log", [])
    failures.append({"sequence": args.sequence, "reel_id": target["reel_id"], "at": now(), "reason": args.reason})
    data = refresh(items, failures)
    print(json.dumps({"failed": target["reel_id"], "failure_count": target["failure_count"], "next_sequence": data["next_sequence"]}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("next").set_defaults(handler=lambda _: select_next())
    mark_parser = sub.add_parser("mark")
    mark_parser.add_argument("--sequence", type=int, required=True)
    mark_parser.add_argument("--stage", choices=STAGES, required=True)
    mark_parser.add_argument("--note")
    mark_parser.set_defaults(handler=mark)
    failure_parser = sub.add_parser("failure")
    failure_parser.add_argument("--sequence", type=int, required=True)
    failure_parser.add_argument("--reason", required=True)
    failure_parser.set_defaults(handler=failure)
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
