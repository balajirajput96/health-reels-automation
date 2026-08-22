from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    "reel_0010_amygdala_context_what_studies_measure_hi.mp4",
    "reel_0010_amygdala_context_what_studies_measure_narration_hi.wav",
    "reel_0010_amygdala_context_what_studies_measure_captions_hi.srt",
    "reel_0010_metadata.json",
    "reel_0010_qc_report.json",
    "reel_0010_amygdala_context_what_studies_measure_sources.md",
    "reel_0010_amygdala_context_what_studies_measure_script.md",
    "reel_0010_scene_01.png",
    "reel_0010_scene_02.png",
    "reel_0010_scene_03.png",
    "reel_0010_scene_04.png",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--listing", type=Path, required=True)
    parser.add_argument("--folder-id", required=True)
    parser.add_argument("--manifest-id", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.listing.read_text(encoding="utf-8"))
    files = payload.get("files", [])
    by_name = {item.get("name"): item for item in files if item.get("name") in EXPECTED}
    manifest_items = [item for item in files if item.get("id") == args.manifest_id]
    missing = sorted(EXPECTED - set(by_name))
    zero = sorted(name for name, item in by_name.items() if int(item.get("size", 0) or 0) <= 0)
    wrong_parent = sorted(name for name, item in by_name.items() if args.folder_id not in (item.get("parents") or []))
    manifest_found = len(manifest_items) == 1
    manifest_parent_ok = manifest_found and args.folder_id in (manifest_items[0].get("parents") or [])
    manifest_nonzero = manifest_found and int(manifest_items[0].get("size", 0) or 0) > 0
    result = {
        "folder_id": args.folder_id,
        "manifest_id": args.manifest_id,
        "expected_count": len(EXPECTED),
        "found_expected_count": len(by_name),
        "missing": missing,
        "zero_size": zero,
        "wrong_parent": wrong_parent,
        "manifest_found_once": manifest_found,
        "manifest_parent_ok": manifest_parent_ok,
        "manifest_nonzero": manifest_nonzero,
        "unrelated_remote_object_count": max(0, len(files) - len(by_name) - len(manifest_items)),
        "expected_objects": [
            {"name": name, "id": by_name[name].get("id"), "size": int(by_name[name].get("size", 0) or 0), "mimeType": by_name[name].get("mimeType")}
            for name in sorted(by_name)
        ],
    }
    result["valid"] = not (missing or zero or wrong_parent or not manifest_found or not manifest_parent_ok or not manifest_nonzero)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
