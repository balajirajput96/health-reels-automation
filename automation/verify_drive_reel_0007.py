from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    "reel_0007_neural_plasticity_what_studies_measure_hi.mp4",
    "reel_0007_neural_plasticity_what_studies_measure_narration_hi.wav",
    "reel_0007_neural_plasticity_what_studies_measure_captions_hi.srt",
    "reel_0007_metadata.json",
    "reel_0007_qc_report.json",
    "reel_0007_neural_plasticity_what_studies_measure_sources.md",
    "reel_0007_neural_plasticity_what_studies_measure_script.md",
    "reel_0007_scene_01.png",
    "reel_0007_scene_02.png",
    "reel_0007_scene_03.png",
    "reel_0007_scene_04.png",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--listing", type=Path, required=True)
    parser.add_argument("--folder-id", required=True)
    args = parser.parse_args()
    payload = json.loads(args.listing.read_text(encoding="utf-8"))
    files = payload.get("files", [])
    by_name = {item.get("name"): item for item in files if item.get("name") in EXPECTED}
    missing = sorted(EXPECTED - set(by_name))
    zero = sorted(name for name, item in by_name.items() if int(item.get("size", 0) or 0) <= 0)
    wrong_parent = sorted(name for name, item in by_name.items() if args.folder_id not in (item.get("parents") or []))
    result = {
        "folder_id": args.folder_id,
        "expected_count": len(EXPECTED),
        "found_expected_count": len(by_name),
        "missing": missing,
        "zero_size": zero,
        "wrong_parent": wrong_parent,
        "unrelated_remote_object_count": max(0, len(files) - len(by_name)),
        "expected_objects": [
            {"name": name, "id": by_name[name].get("id"), "size": int(by_name[name].get("size", 0) or 0), "mimeType": by_name[name].get("mimeType")}
            for name in sorted(by_name)
        ],
    }
    result["valid"] = not (missing or zero or wrong_parent)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
