#!/usr/bin/env python3
"""Non-destructive repository health checks for the health-Reels automation.

This script reads only repository files and writes requested report artifacts. It
never calls external services, handles credentials, changes publishing state, or
modifies the idempotency ledger.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "automation" / "maintenance_manifest.json"


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_manifest(manifest: Any, errors: list[str]) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        add_error(errors, "Maintenance manifest must be a JSON object.")
        return {}

    required_keys = {
        "version",
        "target_account",
        "excluded_publish_account",
        "ledger_path",
        "required_files",
        "allowed_ledger_stages",
        "published_stage",
        "workflow_schedules",
    }
    missing = sorted(required_keys - set(manifest))
    if missing:
        add_error(errors, f"Maintenance manifest is missing keys: {', '.join(missing)}.")

    if not isinstance(manifest.get("required_files"), list):
        add_error(errors, "Maintenance manifest required_files must be a list.")
    if not isinstance(manifest.get("allowed_ledger_stages"), list):
        add_error(errors, "Maintenance manifest allowed_ledger_stages must be a list.")
    if not isinstance(manifest.get("workflow_schedules"), dict):
        add_error(errors, "Maintenance manifest workflow_schedules must be an object.")
    return manifest


def validate_required_files(manifest: dict[str, Any], errors: list[str]) -> list[str]:
    missing: list[str] = []
    for relative in manifest.get("required_files", []):
        if not isinstance(relative, str) or not relative:
            add_error(errors, "Maintenance manifest contains an invalid required_files entry.")
            continue
        if not (ROOT / relative).is_file():
            missing.append(relative)
            add_error(errors, f"Required file is missing: {relative}.")
    return missing


def validate_ledger(manifest: dict[str, Any], errors: list[str]) -> dict[str, int]:
    summary: dict[str, int] = {}
    ledger_relative = manifest.get("ledger_path")
    if not isinstance(ledger_relative, str) or not ledger_relative:
        add_error(errors, "Maintenance manifest ledger_path is invalid.")
        return summary

    ledger_path = ROOT / ledger_relative
    if not ledger_path.is_file():
        add_error(errors, f"Ledger file is missing: {ledger_relative}.")
        return summary

    try:
        ledger = load_json(ledger_path)
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"Ledger JSON could not be read: {exc}.")
        return summary

    if not isinstance(ledger, dict) or not isinstance(ledger.get("items"), list):
        add_error(errors, "Ledger must be a JSON object containing an items list.")
        return summary

    allowed_stages = set(manifest.get("allowed_ledger_stages", []))
    target_account = manifest.get("target_account")
    published_stage = manifest.get("published_stage")

    for index, item in enumerate(ledger["items"]):
        if not isinstance(item, dict):
            add_error(errors, f"Ledger item {index} is not an object.")
            continue
        stage = item.get("stage")
        if stage not in allowed_stages:
            add_error(errors, f"Ledger item {index} has unsupported stage: {stage!r}.")
        else:
            summary[stage] = summary.get(stage, 0) + 1
        if item.get("target_account") != target_account:
            add_error(
                errors,
                f"Ledger item {index} targets {item.get('target_account')!r}, expected {target_account!r}.",
            )
        if stage == published_stage and not item.get("post_id"):
            add_error(errors, f"Published ledger item {index} has no post_id.")
    return summary


def validate_workflow_schedules(manifest: dict[str, Any], errors: list[str]) -> None:
    schedules = manifest.get("workflow_schedules", {})
    if not isinstance(schedules, dict):
        return
    for relative, expected_cron in schedules.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if expected_cron not in content:
            add_error(errors, f"Workflow schedule drift in {relative}; expected cron {expected_cron!r}.")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Repository Health Check",
        "",
        f"**Timestamp:** {report['timestamp_utc']}",
        f"**Status:** {report['status'].upper()}",
        "",
        "## Ledger Summary",
        "",
    ]
    ledger_summary = report["ledger_by_stage"]
    if ledger_summary:
        for stage, count in sorted(ledger_summary.items()):
            lines.append(f"- `{stage}`: {count}")
    else:
        lines.append("- No valid ledger stages were counted.")

    lines.extend(["", "## Findings", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Required files, ledger structure, target-account boundary, and workflow cadence checks passed.")

    lines.extend(
        [
            "",
            "## Safety Boundary",
            "",
            "This check read repository files and wrote only its requested report artifacts. It did not access credentials, external APIs, browser sessions, Drive, media files, publishing controls, or schedules.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run non-destructive health-Reels repository checks.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path, required=True)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        manifest = load_json(args.manifest)
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "timestamp_utc": utc_now(),
            "status": "fail",
            "errors": [f"Maintenance manifest could not be read: {exc}."],
            "ledger_by_stage": {},
        }
    else:
        manifest = validate_manifest(manifest, errors)
        missing_files = validate_required_files(manifest, errors)
        ledger_summary = validate_ledger(manifest, errors)
        validate_workflow_schedules(manifest, errors)
        report = {
            "timestamp_utc": utc_now(),
            "status": "pass" if not errors else "fail",
            "manifest_version": manifest.get("version"),
            "target_account": manifest.get("target_account"),
            "missing_required_files": missing_files,
            "ledger_by_stage": ledger_summary,
            "errors": errors,
        }

    write_text(args.report_json, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_text(args.summary_md, render_markdown(report))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
