#!/usr/bin/env python3
"""Dart Coverage Guard and LCOV Auditor.

Enforces rules and workflows from the dart-collect-coverage skill:
- Ensures 'coverage' is strictly under 'dev_dependencies' in pubspec.yaml.
- Audits Dart source code for coverage directives (ignore-line, ignore-start/end, ignore-file).
- Validates existence and integrity of coverage/coverage.json and coverage/lcov.info.
- Parses LCOV files to calculate coverage metrics (lines found, lines hit, percentage).
- Provides recommended automated and manual coverage collection commands.
"""

from __future__ import annotations
import os
import re
import shutil
import subprocess
from pathlib import Path

IGNORE_LINE_RE = re.compile(r"//\s*coverage:ignore-line")
IGNORE_START_RE = re.compile(r"//\s*coverage:ignore-start")
IGNORE_END_RE = re.compile(r"//\s*coverage:ignore-end")
IGNORE_FILE_RE = re.compile(r"//\s*coverage:ignore-file")


def audit_pubspec_coverage(pubspec_path: Path | str = "pubspec.yaml") -> dict:
    """Verifies that the 'coverage' package is placed under dev_dependencies."""
    p = Path(pubspec_path).resolve()
    if not p.exists():
        return {
            "has_pubspec": False,
            "has_coverage_dev_dependency": False,
            "message": f"pubspec file not found at {p}",
        }

    content = p.read_text(encoding="utf-8")
    lines = content.splitlines()

    in_dev_dependencies = False
    in_dependencies = False
    dev_dep_has_coverage = False
    regular_dep_has_coverage = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("dependencies:") and not stripped.startswith("dev_dependencies:"):
            in_dependencies = True
            in_dev_dependencies = False
            continue
        elif stripped.startswith("dev_dependencies:"):
            in_dev_dependencies = True
            in_dependencies = False
            continue
        elif line and not line[0].isspace() and ":" in line:
            in_dependencies = False
            in_dev_dependencies = False

        if in_dev_dependencies and stripped.startswith("coverage:"):
            dev_dep_has_coverage = True
        elif in_dependencies and stripped.startswith("coverage:"):
            regular_dep_has_coverage = True

    valid = dev_dep_has_coverage and not regular_dep_has_coverage
    msg = "coverage package correctly configured in dev_dependencies" if valid else ""
    if regular_dep_has_coverage:
        msg = "VIOLATION: coverage package must strictly be in dev_dependencies, not dependencies"
    elif not dev_dep_has_coverage:
        msg = "Missing 'coverage' package in dev_dependencies. Add using: dart pub add dev:coverage"

    return {
        "has_pubspec": True,
        "has_coverage_dev_dependency": dev_dep_has_coverage,
        "has_coverage_regular_dependency": regular_dep_has_coverage,
        "valid": valid,
        "message": msg,
    }


def audit_coverage_directives(dart_source_or_dir: Path | str) -> dict:
    """Scans Dart file(s) for coverage ignore directives."""
    p = Path(dart_source_or_dir).resolve()
    files_to_scan = [p] if p.is_file() else list(p.glob("**/*.dart"))

    results = {
        "files_scanned": len(files_to_scan),
        "ignored_files": [],
        "ignored_lines_count": 0,
        "ignored_blocks_count": 0,
        "details": {},
    }

    for f in files_to_scan:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        file_has_ignore_file = bool(IGNORE_FILE_RE.search(text))
        line_ignores = len(IGNORE_LINE_RE.findall(text))
        block_starts = len(IGNORE_START_RE.findall(text))
        block_ends = len(IGNORE_END_RE.findall(text))

        if file_has_ignore_file:
            results["ignored_files"].append(str(f))

        results["ignored_lines_count"] += line_ignores
        results["ignored_blocks_count"] += min(block_starts, block_ends)

        if file_has_ignore_file or line_ignores > 0 or block_starts > 0:
            results["details"][str(f)] = {
                "ignore_file": file_has_ignore_file,
                "ignore_lines": line_ignores,
                "ignore_block_starts": block_starts,
                "ignore_block_ends": block_ends,
                "balanced_blocks": block_starts == block_ends,
            }

    return results


def parse_lcov_report(lcov_path: Path | str) -> dict:
    """Parses an lcov.info file to calculate coverage statistics."""
    p = Path(lcov_path).resolve()
    if not p.exists():
        return {
            "found": False,
            "message": f"LCOV report not found at {p}",
        }

    total_lf = 0
    total_lh = 0
    total_fnf = 0
    total_fnh = 0
    file_records = {}

    current_file = None
    curr_lf = 0
    curr_lh = 0

    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.startswith("SF:"):
                current_file = line[3:]
                curr_lf = 0
                curr_lh = 0
            elif line.startswith("LF:"):
                try:
                    curr_lf = int(line[3:])
                except ValueError:
                    curr_lf = 0
                total_lf += curr_lf
            elif line.startswith("LH:"):
                try:
                    curr_lh = int(line[3:])
                except ValueError:
                    curr_lh = 0
                total_lh += curr_lh
            elif line.startswith("FNF:"):
                try:
                    total_fnf += int(line[4:])
                except ValueError:
                    pass
            elif line.startswith("FNH:"):
                try:
                    total_fnh += int(line[4:])
                except ValueError:
                    pass
            elif line == "end_of_record":
                if current_file:
                    coverage_pct = (curr_lh / curr_lf * 100.0) if curr_lf > 0 else 100.0
                    file_records[current_file] = {
                        "lines_found": curr_lf,
                        "lines_hit": curr_lh,
                        "coverage_pct": round(coverage_pct, 2),
                    }
                current_file = None

    overall_pct = (total_lh / total_lf * 100.0) if total_lf > 0 else 0.0

    return {
        "found": True,
        "path": str(p),
        "lines_found": total_lf,
        "lines_hit": total_lh,
        "coverage_pct": round(overall_pct, 2),
        "functions_found": total_fnf,
        "functions_hit": total_fnh,
        "file_count": len(file_records),
        "files": file_records,
    }


def validate_coverage_output(project_dir: Path | str = ".") -> dict:
    """Validates the coverage/ directory, coverage.json, and lcov.info."""
    p = Path(project_dir).resolve()
    cov_dir = p / "coverage"
    lcov_file = cov_dir / "lcov.info"
    json_file = cov_dir / "coverage.json"

    has_dir = cov_dir.is_dir()
    has_lcov = lcov_file.is_file()
    has_json = json_file.is_file()

    status = {
        "coverage_dir_exists": has_dir,
        "lcov_exists": has_lcov,
        "coverage_json_exists": has_json,
        "valid": has_dir and has_lcov,
    }

    if has_lcov:
        status["metrics"] = parse_lcov_report(lcov_file)
    else:
        status["message"] = "Coverage report missing. Run: dart run coverage:test_with_coverage"

    return status


def get_coverage_commands(is_flutter: bool = False, test_dirs: list[str] | None = None) -> dict:
    """Returns recommended CLI commands according to dart-collect-coverage skill."""
    add_dep = "flutter pub add dev:coverage" if is_flutter else "dart pub add dev:coverage"
    dirs_arg = (" -- " + " ".join(test_dirs)) if test_dirs else ""
    automated = f"dart run coverage:test_with_coverage{dirs_arg}"

    manual = {
        "step_1_run_test_with_vm": "dart run --pause-isolates-on-exit --disable-service-auth-codes --enable-vm-service=8181 test &",
        "step_2_collect_json": "dart run coverage:collect_coverage --wait-paused --uri=http://127.0.0.1:8181/ -o coverage/coverage.json --resume-isolates",
        "step_3_format_lcov": "dart run coverage:format_coverage --packages=.dart_tool/package_config.json --lcov -i coverage/coverage.json -o coverage/lcov.info --check-ignore",
    }

    return {
        "dependency_command": add_dep,
        "automated_command": automated,
        "manual_workflow": manual,
    }


if __name__ == "__main__":
    import json
    print(json.dumps({
        "commands": get_coverage_commands(),
        "status": validate_coverage_output(),
    }, indent=2))
