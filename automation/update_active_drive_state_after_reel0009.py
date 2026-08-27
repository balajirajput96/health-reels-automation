#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "production" / "active_drive_batch001" / "REEL-0009_context_cues"
BASE = REPO / "production" / "active_drive_batch001" / "REEL-0008_fresh_start" / "drive_upload_results"
CHECKPOINT = BASE / "remote_checkpoint_verified.json"
REGISTRY = BASE / "remote_registry_verified.json"
CANONICAL = BASE / "remote_canonical_verified.json"
INVENTORY = PACKAGE / "drive_upload_results" / "remote_inventory.json"
MANIFEST = PACKAGE / "rendered" / "REEL-0009_local_manifest.json"
CHECKPOINT_UPDATE = PACKAGE / "drive_upload_results" / "remote_checkpoint_after_reel0009.json"
REGISTRY_UPDATE = PACKAGE / "drive_upload_results" / "remote_registry_after_reel0009.json"
CANONICAL_UPDATE = PACKAGE / "drive_upload_results" / "remote_canonical_production_state_after_reel0009.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    checkpoint = read(CHECKPOINT)
    registry = read(REGISTRY)
    canonical = read(CANONICAL)
    inventory = read(INVENTORY)
    manifest = read(MANIFEST)
    files = {item["name"]: item for item in inventory.get("files", [])}
    expected = [
        "REEL-0009_context_cues_QC_pending.mp4", "REEL-0009_narration_hi-IN.wav",
        "REEL-0009_captions_hi-IN.srt", "REEL-0009_captions_hi-IN.ass",
        "REEL-0009_local_manifest.json", "REEL-0009_qc_report.json",
        "REEL-0009_qc_ffprobe.json", "REEL-0009_qc_sha256.txt",
        "REEL-0009_script_hi-IN.md", "REEL-0009_production_brief.md",
        "REEL-0009_source_validation.md", "REEL-0009_scene_01_everyday_signal.png",
        "REEL-0009_scene_02_cue_action_context.png", "REEL-0009_scene_03_stable_repetition.png",
        "REEL-0009_scene_04_context_change.png", "REEL-0009_scene_05_small_action_plan.png",
        "REEL-0009_scene_06_cue_not_command.png", "REEL-0009_style_reference.png",
        "REEL-0009_qc_frame_02s.jpg", "REEL-0009_qc_frame_38s.jpg", "REEL-0009_qc_frame_70s.jpg",
    ]
    missing = [name for name in expected if name not in files]
    if missing:
        raise SystemExit("Remote inventory is missing: " + ", ".join(missing))
    reel = next(item for item in registry if item.get("reel_id") == "0009")
    reel = {
        **reel,
        "status": "qc_passed_drive_verified",
        "evidence_status": "verified_with_limits",
        "working_title_hi": manifest["working_title_hi"],
        "drive_folder_id": files["REEL-0009_local_manifest.json"]["parents"][0],
        "video_file_id": files["REEL-0009_context_cues_QC_pending.mp4"]["id"],
        "manifest_file_id": files["REEL-0009_local_manifest.json"]["id"],
        "source_metadata_file_id": files["REEL-0009_source_validation.md"]["id"],
        "qc_report_file_id": files["REEL-0009_qc_report.json"]["id"],
        "artifact_count": len(expected),
        "duration_seconds": manifest["format"]["duration_seconds"],
        "format": manifest["format"],
        "language": manifest["language"],
        "completed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    checkpoint.setdefault("progress", {})
    checkpoint["progress"].update({
        "completed_in_current_batch": 9,
        "completed_reels": ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008", "0009"],
        "current_batch": 1,
        "failed_reels": [],
        "next_reel_id": "0010",
        "target_reels_per_batch": 30,
        "target_total_reels": 3000,
    })
    checkpoint["storage"] = {
        **checkpoint.get("storage", {}),
        "root_folder_id": "1vYLRarvedtfaYzNcINGKpKAeeFaz0OnD",
        "active_batch_folder_id": "1EUgS6DJLcu6n1UQJqtXPmphWjZail8oi",
        "active_batch_id": "Batch_001",
    }
    checkpoint["reel_0009"] = reel
    checkpoint["production_rules"] = {**checkpoint.get("production_rules", {}), "target_duration_seconds": 60}
    for index, item in enumerate(registry):
        if item.get("reel_id") == "0009":
            registry[index] = reel
            break
    else:
        raise SystemExit("Registry does not contain reel_id 0009")
    canonical_reels = canonical.get("reels", [])
    for index, item in enumerate(canonical_reels):
        if item.get("reel_id") == "0009":
            canonical_reels[index] = {**item, **reel}
            break
    else:
        raise SystemExit("Canonical production state does not contain reel_id 0009")
    canonical["reels"] = canonical_reels
    canonical["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    write(CHECKPOINT_UPDATE, checkpoint)
    write(REGISTRY_UPDATE, registry)
    write(CANONICAL_UPDATE, canonical)
    print(json.dumps({"status":"ready_for_remote_update","reel_id":"0009","artifact_count":len(expected),"registry_entries":len(registry),"canonical_reels":len(canonical_reels),"checkpoint_next_reel_id":checkpoint["progress"]["next_reel_id"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
