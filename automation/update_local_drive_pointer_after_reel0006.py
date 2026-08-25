#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POINTER_PATH = REPO / "state" / "drive_active_state_pointer.json"
PACKAGE = REPO / "production" / "active_drive_batch001" / "REEL-0006_ordinary_forgetting"
INVENTORY = PACKAGE / "drive_upload_results" / "remote_inventory.json"
VERIFY = PACKAGE / "drive_upload_results" / "remote_state_verification.json"


def main() -> None:
    pointer = json.loads(POINTER_PATH.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    verify = json.loads(VERIFY.read_text(encoding="utf-8"))
    if verify.get("status") != "PASS" or verify.get("remote_state_verified") is not True:
        raise SystemExit("Remote verification is not PASS")
    files = {item["name"]: item for item in inventory["files"]}
    pointer["verified_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    pointer["completed"]["reel_0006"] = {
        "status": "qc_passed_drive_verified",
        "folder_id": files["REEL-0006_local_manifest.json"]["parents"][0],
        "video_file_id": files["REEL-0006_ordinary_forgetting_QC_pending.mp4"]["id"],
        "manifest_file_id": files["REEL-0006_local_manifest.json"]["id"],
        "source_metadata_file_id": files["REEL-0006_source_validation.md"]["id"],
        "qc_report_file_id": files["REEL-0006_qc_report.json"]["id"],
        "artifact_count": verify["artifact_count"],
        "duration_seconds": 72.7,
        "evidence_status": "verified_with_limits",
        "production_mode": "original AI-generated still scenes with deterministic pan-zoom motion, Hindi narration, and burned-in captions",
    }
    pointer["next_reel_id"] = "0007"
    POINTER_PATH.write_text(json.dumps(pointer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":"PASS","completed_reel":"0006","next_reel_id":pointer["next_reel_id"],"artifact_count":pointer["completed"]["reel_0006"]["artifact_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
