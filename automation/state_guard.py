#!/usr/bin/env python3
"""Local, idempotent state guard for the health-Reels workflow.

The guard holds no credentials and does not call social platforms. It records
source and publishing identifiers so orchestration layers can refuse duplicate
processing or accidental re-publication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "state" / "reels_ledger.json"


def load() -> dict[str, Any]:
    if not LEDGER.exists():
        return {"version": 1, "items": []}
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(data: dict[str, Any]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


IDENTITY_KEYS = ("source_id", "sha256", "draft_id", "post_id")


def matches(item: dict[str, Any], keys: dict[str, str]) -> bool:
    strong_keys = [key for key in IDENTITY_KEYS if keys.get(key)]
    if strong_keys:
        return any(item.get(key) == keys[key] for key in strong_keys)

    filename = keys.get("filename", "")
    return bool(filename) and item.get("filename") == filename


def duplicate(data: dict[str, Any], keys: dict[str, str]) -> dict[str, Any] | None:
    return next((item for item in data["items"] if matches(item, keys)), None)


def register(args: argparse.Namespace) -> int:
    data = load()
    source_hash = args.sha256 or (sha256(Path(args.file)) if args.file else "")
    keys = {
        "source_id": args.source_id or "",
        "sha256": source_hash,
        "filename": Path(args.file).name if args.file else (args.filename or ""),
        "draft_id": args.draft_id or "",
        "post_id": args.post_id or "",
    }
    if not any(keys[key] for key in IDENTITY_KEYS) and not keys["filename"]:
        raise ValueError("At least one identity is required: source_id, sha256, filename, draft_id, or post_id")

    prior = duplicate(data, keys)
    if prior:
        print(json.dumps({"decision": "duplicate", "existing": prior}, ensure_ascii=False, indent=2))
        return 2

    record = {
        **{key: value for key, value in keys.items() if value},
        "stage": args.stage,
        "target_account": args.target_account,
        "recorded_at": utc_now(),
        "notes": args.notes or "",
    }
    data["items"].append(record)
    save(data)
    print(json.dumps({"decision": "registered", "record": record}, ensure_ascii=False, indent=2))
    return 0


def status(_: argparse.Namespace) -> int:
    data = load()
    summary: dict[str, int] = {}
    for item in data["items"]:
        stage = item.get("stage", "unknown")
        summary[stage] = summary.get(stage, 0) + 1
    print(json.dumps({"items": len(data["items"]), "by_stage": summary}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Health-Reels idempotency guard")
    subparsers = parser.add_subparsers(required=True, dest="command")

    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--stage", required=True, choices=["original", "edited", "final", "drive_verified", "scheduled", "published", "failed", "rejected"])
    register_parser.add_argument("--target-account", default="@balajirajput96")
    register_parser.add_argument("--source-id")
    register_parser.add_argument("--file")
    register_parser.add_argument("--filename")
    register_parser.add_argument("--sha256")
    register_parser.add_argument("--draft-id")
    register_parser.add_argument("--post-id")
    register_parser.add_argument("--notes")
    register_parser.set_defaults(handler=register)

    status_parser = subparsers.add_parser("status")
    status_parser.set_defaults(handler=status)
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
