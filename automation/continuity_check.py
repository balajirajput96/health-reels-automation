#!/usr/bin/env python3
"""Validate non-secret CLI continuity metadata for the health-Reels workflow.

The checker reads repository metadata and may optionally check whether declared
local commands are present on PATH. It never invokes authentication flows,
reads credentials, exports sessions, or calls external service APIs.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "automation" / "cli_continuity_manifest.json"


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# CLI Continuity Check",
        "",
        f"**Timestamp:** {report['timestamp_utc']}",
        f"**Status:** {report['status'].upper()}",
        "",
        "## Declared Services",
        "",
    ]
    for service in report.get("services", []):
        command = service.get("command") or "browser/service session"
        local = service.get("local_command_available")
        local_text = "not checked" if local is None else ("available" if local else "missing")
        lines.append(f"- `{service['id']}` — command: `{command}`; local availability: {local_text}.")

    lines.extend(["", "## Findings", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Manifest schema and required repository files are present.")

    lines.extend(
        [
            "",
            "## Credential Boundary",
            "",
            "This check did not invoke login, access credential stores, inspect API keys, export tokens, read browser sessions, or call external APIs.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate_manifest(manifest: Any, check_local_commands: bool) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    services: list[dict[str, Any]] = []
    if not isinstance(manifest, dict):
        return ["CLI continuity manifest must be a JSON object."], services

    if not isinstance(manifest.get("services"), list):
        errors.append("CLI continuity manifest services must be a list.")
    if not isinstance(manifest.get("required_repository_files"), list):
        errors.append("CLI continuity manifest required_repository_files must be a list.")

    seen_ids: set[str] = set()
    for raw in manifest.get("services", []):
        if not isinstance(raw, dict):
            errors.append("A CLI continuity service entry is not an object.")
            continue
        identifier = raw.get("id")
        if not isinstance(identifier, str) or not identifier:
            errors.append("A CLI continuity service is missing a non-empty id.")
            continue
        if identifier in seen_ids:
            errors.append(f"Duplicate CLI continuity service id: {identifier}.")
        seen_ids.add(identifier)
        command = raw.get("command")
        if command is not None and not isinstance(command, str):
            errors.append(f"Service {identifier} command must be a string or null.")
        services.append(
            {
                "id": identifier,
                "command": command,
                "local_command_available": shutil.which(command) is not None if check_local_commands and command else None,
            }
        )

    for relative in manifest.get("required_repository_files", []):
        if not isinstance(relative, str) or not relative:
            errors.append("A required_repository_files entry is invalid.")
            continue
        if not (ROOT / relative).is_file():
            errors.append(f"Required repository file is missing: {relative}.")
    return errors, services


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate non-secret CLI continuity metadata.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path, required=True)
    parser.add_argument("--check-local-commands", action="store_true")
    args = parser.parse_args()

    try:
        manifest = load_json(args.manifest)
    except (OSError, json.JSONDecodeError) as exc:
        report = {
            "timestamp_utc": utc_now(),
            "status": "fail",
            "errors": [f"CLI continuity manifest could not be read: {exc}."],
            "services": [],
        }
    else:
        errors, services = validate_manifest(manifest, args.check_local_commands)
        report = {
            "timestamp_utc": utc_now(),
            "status": "pass" if not errors else "fail",
            "manifest_version": manifest.get("version"),
            "check_local_commands": args.check_local_commands,
            "services": services,
            "errors": errors,
        }

    write_text(args.report_json, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_text(args.summary_md, render_markdown(report))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
