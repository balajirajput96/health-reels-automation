#!/usr/bin/env python3
"""Restart-safe state controls for the 3,000 Hindi research-reel production project.

This module deliberately has no credentials and makes no external calls. A connected
production worker must supply real evidence, QC, and Drive verification before a reel
may transition to COMPLETED_VERIFIED. The module supports dry-run validation so queued
work can be inspected without mutating the local master state.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_NAME = "3000_HINDI_RESEARCH_REELS"
EVIDENCE_LABELS = {
    "Established Evidence",
    "Strong Evidence",
    "Emerging Evidence",
    "Mixed Evidence",
    "Preliminary Finding",
    "Expert Interpretation",
    "Philosophical Concept",
    "Spiritual/Traditional Belief",
}
STATUS_ORDER = (
    "PENDING_EVIDENCE_RESEARCH",
    "EVIDENCE_VERIFIED",
    "SCRIPT_FACT_CHECKED",
    "ASSETS_READY",
    "NARRATION_READY",
    "RENDERED",
    "QC_PASSED",
    "DRIVE_UPLOADED_VERIFIED",
    "COMPLETED_VERIFIED",
)
RETRY_STATES = {"RETRY_QUEUED", "BLOCKED"}
REQUIRED_COMPLETION_FIELDS = {
    "source_record_path",
    "script_path",
    "asset_manifest_path",
    "narration_path",
    "render_path",
    "qc_path",
    "drive_file_id",
    "drive_verified_at",
    "drive_file_md5",
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(encoded)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc.msg}") from exc
    return records


def append_jsonl_atomic(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def project_paths(root: Path) -> dict[str, Path]:
    return {
        "master": root / "MASTER_PROGRESS.json",
        "registry": root / "PROGRESS" / "reel_registry.jsonl",
        "events": root / "PROGRESS" / "events.jsonl",
        "retry": root / "PROGRESS" / "RETRY_QUEUE.jsonl",
    }


def latest_registry_records(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for record in records:
        reel_id = record.get("reel_id")
        if not reel_id:
            raise ValueError("Every registry record requires reel_id")
        latest[reel_id] = record
    return latest


def is_relative_project_file(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_evidence_record(project_root: Path, reel: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    evidence_label = reel.get("evidence_label")
    if evidence_label not in EVIDENCE_LABELS:
        errors.append(f"{reel['reel_id']}: evidence_label must be one of the approved categories")
    source_path = reel.get("source_record_path")
    if not source_path or not is_relative_project_file(source_path):
        errors.append(f"{reel['reel_id']}: source_record_path must be a project-relative path")
        return errors
    absolute = project_root / source_path
    if not absolute.is_file():
        errors.append(f"{reel['reel_id']}: source record is missing: {source_path}")
        return errors
    try:
        source = load_json(absolute)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{reel['reel_id']}: source record cannot be parsed: {exc}")
        return errors
    for field in ("source_id", "title", "url_or_doi", "evidence_label", "verification_status", "claim_boundaries"):
        if not source.get(field):
            errors.append(f"{reel['reel_id']}: source record missing {field}")
    if source.get("evidence_label") != evidence_label:
        errors.append(f"{reel['reel_id']}: evidence label differs between registry and source record")
    if source.get("verification_status") != "VERIFIED":
        errors.append(f"{reel['reel_id']}: source record is not VERIFIED")
    return errors


def validate_completed_reel(project_root: Path, reel: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    reel_id = reel["reel_id"]
    if reel.get("status") != "COMPLETED_VERIFIED":
        return errors
    errors.extend(validate_evidence_record(project_root, reel))
    for field in REQUIRED_COMPLETION_FIELDS:
        if not reel.get(field):
            errors.append(f"{reel_id}: completed reel is missing {field}")
    for field in ("script_path", "asset_manifest_path", "narration_path", "render_path", "qc_path"):
        value = reel.get(field)
        if value and (not is_relative_project_file(value) or not (project_root / value).is_file()):
            errors.append(f"{reel_id}: required local artifact is unavailable: {value}")
    qc_path = reel.get("qc_path")
    if qc_path and is_relative_project_file(qc_path) and (project_root / qc_path).is_file():
        try:
            qc = load_json(project_root / qc_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{reel_id}: QC record cannot be parsed: {exc}")
        else:
            for key in ("render_decodes", "aspect_ratio_9_16", "captions_present", "audio_present", "editorial_review_passed"):
                if qc.get(key) is not True:
                    errors.append(f"{reel_id}: QC has not passed {key}")
    return errors


def validate_project(root: Path) -> list[str]:
    paths = project_paths(root)
    errors: list[str] = []
    if not paths["master"].is_file():
        return [f"Missing master state: {paths['master']}"]
    try:
        master = load_json(paths["master"])
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Master state cannot be parsed: {exc}"]
    if master.get("project", {}).get("id") != PROJECT_NAME:
        errors.append("Master state project id does not match the controlled project")
    if master.get("counts", {}).get("target") != 3000:
        errors.append("Master state target must remain 3000")
    try:
        records = latest_registry_records(read_jsonl(paths["registry"]))
    except ValueError as exc:
        return [str(exc)]
    completed = 0
    retry_count = 0
    seen_topic_keys: dict[str, str] = {}
    for reel_id, reel in records.items():
        if reel.get("completion_claimed") and reel.get("status") != "COMPLETED_VERIFIED":
            errors.append(f"{reel_id}: completion_claimed is true outside COMPLETED_VERIFIED")
        if reel.get("status") == "COMPLETED_VERIFIED":
            completed += 1
            errors.extend(validate_completed_reel(root, reel))
        elif reel.get("status") in RETRY_STATES:
            retry_count += 1
        topic_key = reel.get("topic_key")
        if topic_key:
            previous = seen_topic_keys.get(topic_key)
            if previous and previous != reel_id:
                errors.append(f"Duplicate topic_key {topic_key}: {previous} and {reel_id}")
            seen_topic_keys[topic_key] = reel_id
    counts = master.get("counts", {})
    if counts.get("completed_verified") != completed:
        errors.append(f"Master completed_verified={counts.get('completed_verified')} but registry has {completed}")
    if counts.get("retry_queue") != retry_count:
        errors.append(f"Master retry_queue={counts.get('retry_queue')} but registry has {retry_count}")
    if counts.get("pending") != 3000 - completed - retry_count - counts.get("in_production", 0) - counts.get("failed_terminal", 0):
        errors.append("Master pending count does not reconcile to the controlled total")
    return errors


def allowed_transition(previous: str, requested: str) -> bool:
    if requested in RETRY_STATES:
        return previous != "COMPLETED_VERIFIED"
    if previous in RETRY_STATES:
        return requested in STATUS_ORDER[:-1]
    try:
        return STATUS_ORDER.index(requested) == STATUS_ORDER.index(previous) + 1
    except ValueError:
        return False


def transition(root: Path, reel_id: str, expected_status: str, next_status: str, updates: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    paths = project_paths(root)
    records = latest_registry_records(read_jsonl(paths["registry"]))
    current = records.get(reel_id)
    if not current:
        raise ValueError(f"Unknown reel_id: {reel_id}")
    if current.get("status") != expected_status:
        raise ValueError(f"{reel_id} expected {expected_status}, found {current.get('status')}")
    if not allowed_transition(expected_status, next_status):
        raise ValueError(f"Unsupported transition: {expected_status} -> {next_status}")
    proposed = {**current, **updates, "status": next_status, "updated_at": utc_now()}
    proposed["completion_claimed"] = next_status == "COMPLETED_VERIFIED"
    if next_status == "COMPLETED_VERIFIED":
        problems = validate_completed_reel(root, proposed)
        if problems:
            raise ValueError("Completion blocked: " + "; ".join(problems))
    event = {
        "timestamp": utc_now(),
        "event_type": "REEL_STATE_TRANSITION",
        "entity_type": "reel",
        "entity_id": reel_id,
        "from_status": expected_status,
        "to_status": next_status,
        "dry_run": dry_run,
        "idempotency_key": f"{reel_id}:{expected_status}:{next_status}",
    }
    if dry_run:
        return {"decision": "dry_run_transition_valid", "proposed": proposed, "event": event}
    append_jsonl_atomic(paths["registry"], proposed)
    append_jsonl_atomic(paths["events"], event)
    reconcile(root, dry_run=False)
    return {"decision": "transition_recorded", "reel": proposed, "event": event}


def reconcile(root: Path, dry_run: bool) -> dict[str, Any]:
    paths = project_paths(root)
    master = load_json(paths["master"])
    records = latest_registry_records(read_jsonl(paths["registry"]))
    statuses = Counter(record.get("status") for record in records.values())
    completed = statuses["COMPLETED_VERIFIED"]
    retries = sum(statuses[state] for state in RETRY_STATES)
    active = sum(statuses[state] for state in STATUS_ORDER[1:-1])
    failed = statuses["FAILED_TERMINAL"]
    counts = {
        "target": 3000,
        "completed_verified": completed,
        "in_production": active,
        "pending": 3000 - completed - retries - active - failed,
        "retry_queue": retries,
        "failed_terminal": failed,
    }
    if counts["pending"] < 0:
        raise ValueError("Reconciliation produced a negative pending count")
    proposed = {**master, "counts": counts, "last_updated_at": utc_now()}
    if not dry_run:
        write_json_atomic(paths["master"], proposed)
    return {"decision": "dry_run_reconciled" if dry_run else "reconciled", "counts": counts}


def parse_update_pairs(values: list[str]) -> dict[str, Any]:
    updates: dict[str, Any] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("Updates must use key=value")
        key, raw = value.split("=", 1)
        updates[key] = json.loads(raw) if raw.startswith(("{", "[", '"')) or raw in {"true", "false", "null"} else raw
    return updates


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and atomically transition Hindi research-reel production records.")
    parser.add_argument("--project-root", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--strict", action="store_true")
    reconcile_parser = subparsers.add_parser("reconcile")
    reconcile_parser.add_argument("--dry-run", action="store_true")
    transition_parser = subparsers.add_parser("transition")
    transition_parser.add_argument("--reel-id", required=True)
    transition_parser.add_argument("--expected-status", required=True)
    transition_parser.add_argument("--next-status", required=True)
    transition_parser.add_argument("--set", action="append", default=[])
    transition_parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.command == "validate":
        problems = validate_project(args.project_root)
        print(json.dumps({"decision": "valid" if not problems else "invalid", "errors": problems}, ensure_ascii=False, indent=2))
        return 1 if problems and args.strict else 0
    if args.command == "reconcile":
        print(json.dumps(reconcile(args.project_root, args.dry_run), ensure_ascii=False, indent=2))
        return 0
    try:
        result = transition(args.project_root, args.reel_id, args.expected_status, args.next_status, parse_update_pairs(args.set), args.dry_run)
    except ValueError as exc:
        print(json.dumps({"decision": "rejected", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
