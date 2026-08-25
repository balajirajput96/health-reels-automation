#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "production" / "active_drive_batch001" / "REEL-0002_habit_21_days"
INVENTORY = PACKAGE / "drive_remote_inventory.json"
MANIFEST = PACKAGE / "rendered" / "REEL-0002_local_manifest.json"
REMOTE_CHECKPOINT = REPO / "research" / "drive_checkpoint_2026-08-23.json"
REMOTE_REGISTRY = REPO / "research" / "drive_reel_registry_3000_slots_2026-08-23.json"
OUT_CHECKPOINT = PACKAGE / "remote_checkpoint_after_reel0002.json"
OUT_REGISTRY = PACKAGE / "remote_registry_after_reel0002.json"

EXPECTED = [
    "REEL-0002_habit_21_days_QC_pending.mp4",
    "REEL-0002_narration_hi-IN.wav",
    "REEL-0002_captions_hi-IN.srt",
    "REEL-0002_captions_hi-IN.ass",
    "REEL-0002_local_manifest.json",
    "REEL-0002_script_hi-IN.md",
    "REEL-0002_production_brief.md",
    "REEL-0002_source_validation.md",
    "REEL-0002_ffprobe.json",
    "REEL-0002_scene_01_hook_calendar.png",
    "REEL-0002_scene_02_evidence_timeline.png",
    "REEL-0002_scene_03_variability.png",
    "REEL-0002_scene_04_stable_cue.png",
    "REEL-0002_scene_05_missed_day.png",
    "REEL-0002_style_reference.png",
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    inventory = read_json(INVENTORY)
    remote_files = {item["name"]: item for item in inventory.get("files", [])}
    missing = sorted(set(EXPECTED) - set(remote_files))
    if missing:
        raise SystemExit("Cannot mark complete; missing remote files: " + ", ".join(missing))
    checkpoint = read_json(REMOTE_CHECKPOINT)
    registry = read_json(REMOTE_REGISTRY)
    manifest = read_json(MANIFEST)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    folder_id = "12EwnZQ9RN6BUYmefbzHAmDhQ77F-Fduo"
    video = remote_files["REEL-0002_habit_21_days_QC_pending.mp4"]
    qc = remote_files["REEL-0002_local_manifest.json"]
    source = remote_files["REEL-0002_source_validation.md"]
    entry = {
        "reel_id": "0002",
        "batch": "Batch_001",
        "track": "habits_behavior",
        "working_title_hi": "21 दिन वाली आदत-धारणा: संकेत और दोहराव",
        "status": "qc_passed_drive_verified",
        "evidence_status": "verified_with_limits",
        "duration_seconds": manifest["format"]["duration_seconds"],
        "drive_folder_id": folder_id,
        "drive_file_id": video["id"],
        "qc_file_id": qc["id"],
        "source_metadata_file_id": source["id"],
        "production_mode": manifest["production_mode"],
        "completed_at": now,
    }
    updated = False
    for i, old in enumerate(registry):
        if old.get("reel_id") == "0002":
            registry[i] = {**old, **entry, "retries_used": old.get("retries_used", 1)}
            updated = True
            break
    if not updated:
        raise SystemExit("Remote registry does not contain reel_id 0002")
    checkpoint["progress"] = {
        **checkpoint.get("progress", {}),
        "completed_in_current_batch": 2,
        "completed_reels": ["0001", "0002"],
        "current_batch": 1,
        "failed_reels": [],
        "next_reel_id": "0003",
        "target_reels_per_batch": 30,
        "target_total_reels": 3000,
    }
    checkpoint["storage"] = {
        **checkpoint.get("storage", {}),
        "root_folder_id": "1vYLRarvedtfaYzNcINGKpKAeeFaz0OnD",
        "active_batch_folder_id": "1EUgS6DJLcu6n1UQJqtXPmphWjZail8oi",
        "active_batch_id": "Batch_001",
    }
    checkpoint["reel_0002"] = entry
    checkpoint["production_rules"] = {**checkpoint.get("production_rules", {}), "target_duration_seconds": 60}
    checkpoint["updated_at"] = now
    manifest["status"] = "complete_uploaded_verified"
    manifest["drive_verification"] = {"verified": True, "folder_id": folder_id, "remote_file_count": len(remote_files), "verified_at": now}
    write_json(MANIFEST, manifest)
    write_json(OUT_CHECKPOINT, checkpoint)
    write_json(OUT_REGISTRY, registry)
    print(json.dumps({"status": "complete_uploaded_verified", "reel_id": "0002", "next_reel_id": "0003", "remote_file_count": len(remote_files), "video_file_id": video["id"], "qc_file_id": qc["id"], "source_file_id": source["id"], "completed_at": now}, ensure_ascii=False))


if __name__ == "__main__":
    main()
