#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "production" / "active_drive_batch001" / "REEL-0002_habit_21_days"
REMOTE_CHECKPOINT = REPO / "research" / "drive_checkpoint_2026-08-23.json"
REMOTE_REGISTRY = REPO / "research" / "drive_reel_registry_3000_slots_2026-08-23.json"
REMOTE_CANONICAL = REPO / "research" / "drive_canonical_production_state_2026-08-23.json"
CHECKPOINT_UPDATE = PACKAGE / "remote_checkpoint_after_reel0002.json"
REGISTRY_UPDATE = PACKAGE / "remote_registry_after_reel0002.json"
CANONICAL_UPDATE = PACKAGE / "remote_canonical_production_state_after_reel0002.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    checkpoint = read(CHECKPOINT_UPDATE)
    registry = read(REGISTRY_UPDATE)
    canonical = read(REMOTE_CANONICAL)
    reel2 = next(item for item in registry if item.get("reel_id") == "0002")
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
    checkpoint["reel_0002"] = reel2
    checkpoint["production_rules"] = {**checkpoint.get("production_rules", {}), "target_duration_seconds": 60}
    canonical_reels = canonical.get("reels", [])
    found = False
    for index, item in enumerate(canonical_reels):
        if item.get("reel_id") == "0002":
            canonical_reels[index] = {**item, **reel2}
            found = True
            break
    if not found:
        raise SystemExit("Canonical production state does not contain reel_id 0002")
    canonical["reels"] = canonical_reels
    canonical["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    write(CHECKPOINT_UPDATE, checkpoint)
    write(REGISTRY_UPDATE, registry)
    write(CANONICAL_UPDATE, canonical)
    print(json.dumps({"status": "ready_for_remote_update", "reel_id": "0002", "canonical_reels": len(canonical_reels), "registry_entries": len(registry), "checkpoint_next_reel_id": checkpoint["progress"]["next_reel_id"], "canonical_updated_at": canonical["updated_at"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
