#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINTER = ROOT / "state" / "drive_active_state_pointer.json"


def main() -> None:
    pointer = json.loads(POINTER.read_text(encoding="utf-8"))
    assert pointer["project"] == "3000_HINDI_RESEARCH_REELS"
    assert pointer["provider"] == "Google Drive"
    assert pointer["root"]["name"] == "3000_HINDI_RESEARCH_REELS"
    assert pointer["active_batch"]["name"] == "Batch_001"
    assert pointer["next_reel_id"] == "0003"
    assert pointer["target_total_reels"] == 3000
    assert pointer["reels_per_batch"] == 30
    fmt = pointer["format"]
    assert fmt["language"] == "hi-IN"
    assert fmt["aspect_ratio"] == "9:16"
    assert fmt["target_duration_seconds"] == 60
    assert fmt["voice_required"] is True
    assert fmt["captions_required"] is True
    completed = pointer["completed"]
    for reel_id in ("reel_0001", "reel_0002"):
        assert completed[reel_id]["status"] == "qc_passed_drive_verified"
    assert completed["reel_0002"]["folder_id"]
    assert completed["reel_0002"]["video_file_id"]
    print(json.dumps({"status": "PASS", "project": pointer["project"], "completed": ["0001", "0002"], "next_reel_id": pointer["next_reel_id"], "target_total_reels": pointer["target_total_reels"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
