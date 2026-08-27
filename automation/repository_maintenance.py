"""Non-destructive daily repository-maintenance audit for health-reels automation.

Scheduled runs only report documentation and policy inconsistencies. They never rewrite
repository files, create commits, or open pull requests. A human or separately
confirmed repair job may opt into a narrow documentation-only account-reference patch.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
from pathlib import Path

TARGET_ACCOUNT = "@balajirajput96"
SCHEDULE = "30 0 * * *"
UNSAFE_PATTERNS = [r"\bcure\b", r"\bguarantee\b", r"\bdiagnosis\b", r"\btreat\b", r"\bmedical advice\b"]
ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_NAME = "MAINTENANCE_REPORT.md"


def read_files(root: Path = ROOT_DIR) -> list[Path]:
    files: list[Path] = []
    for current_root, directories, filenames in os.walk(root):
        directories[:] = [directory for directory in directories if directory not in {".git", "__pycache__"}]
        for filename in filenames:
            if filename.endswith((".md", ".yml")):
                files.append(Path(current_root) / filename)
    return sorted(files)


def hash_file(filepath: Path) -> str:
    return hashlib.md5(filepath.read_bytes()).hexdigest()


def is_report_file(path: Path) -> bool:
    return path.name.lower() == REPORT_NAME.lower()


def is_negative_account_warning(line: str) -> bool:
    text = line.lower()
    return any(token in text for token in ("not", "never", "excluded", "must not", "do not", "avoid"))


def check_stale_references(files: list[Path]) -> list[Path]:
    stale_pattern = r"@bala\.jirajput966"
    affected: list[Path] = []
    for file_path in files:
        if file_path.suffix != ".md" or is_report_file(file_path):
            continue
        lines = file_path.read_text(encoding="utf-8").splitlines()
        if any(re.search(stale_pattern, line) and not is_negative_account_warning(line) for line in lines):
            affected.append(file_path)
    return affected


def check_duplicated_state(files: list[Path]) -> list[tuple[Path, Path]]:
    hashes: dict[str, Path] = {}
    duplicates: list[tuple[Path, Path]] = []
    for file_path in files:
        if file_path.suffix != ".md" or is_report_file(file_path):
            continue
        digest = hash_file(file_path)
        if digest in hashes:
            duplicates.append((hashes[digest], file_path))
        else:
            hashes[digest] = file_path
    return duplicates


def check_schedule_drift(root: Path = ROOT_DIR) -> tuple[bool, str | None]:
    workflow_file = root / ".github/workflows/repository-maintenance.yml"
    if not workflow_file.exists():
        return True, "Workflow file not found"
    if SCHEDULE not in workflow_file.read_text(encoding="utf-8"):
        return True, f"Schedule drifted. Expected {SCHEDULE}"
    return False, None


def has_safe_negative_context(content: str, match_start: int) -> bool:
    window = content[max(0, match_start - 48):match_start]
    return bool(re.search(r"\b(not|no|avoid|without|instead of|never|do not|must not)\b", window))


def check_unsafe_patterns(files: list[Path]) -> list[tuple[Path, str]]:
    unsafe_found: list[tuple[Path, str]] = []
    for file_path in files:
        if file_path.suffix != ".md" or is_report_file(file_path) or file_path.name == "HEALTH_CONTENT_EDITORIAL_STANDARD.md":
            continue
        content = file_path.read_text(encoding="utf-8").lower()
        for pattern in UNSAFE_PATTERNS:
            if any(not has_safe_negative_context(content, match.start()) for match in re.finditer(pattern, content)):
                unsafe_found.append((file_path, pattern))
    return unsafe_found


def generate_report(
    stale: list[Path],
    duplicates: list[tuple[Path, Path]],
    drift: bool,
    drift_message: str | None,
    unsafe: list[tuple[Path, str]],
    applied_patch: bool,
    root: Path = ROOT_DIR,
) -> Path:
    report_path = root / REPORT_NAME
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    findings: list[str] = []
    if stale:
        affected = "\n".join(f"  - `{file_path.relative_to(root)}`" for file_path in stale)
        findings.append("**Incorrect target-account references**\n\n" + affected)
    if duplicates:
        affected = "\n".join(f"  - `{first.relative_to(root)}` and `{second.relative_to(root)}`" for first, second in duplicates)
        findings.append("**Duplicated Markdown content**\n\n" + affected)
    if drift:
        findings.append(f"**Schedule configuration drift**\n\n  - {drift_message}")
    if unsafe:
        affected = "\n".join(f"  - `{file_path.relative_to(root)}` contains `{pattern}`" for file_path, pattern in unsafe)
        findings.append("**Potentially unsafe health-language patterns**\n\n" + affected)

    report = [f"# Daily Repository Maintenance Report\n\n**Date:** {today}\n"]
    report.append(
        "This is a non-destructive audit. It does not access accounts, credentials, Drive, or social platforms, "
        "and it does not modify production state.\n"
    )
    report.append("## Findings\n")
    if findings:
        report.extend(f"{index}. {finding}\n" for index, finding in enumerate(findings, start=1))
    else:
        report.append("No repository-policy or documentation inconsistencies were found.\n")
    report.append("## Patch policy\n")
    if stale and not applied_patch:
        report.append("No files were changed. An explicit `--apply-documentation-account-fix` run is required before the narrow documentation-only account-reference patch may be applied.\n")
    elif applied_patch:
        report.append("An explicit documentation-only account-reference patch was applied. Review the working tree before committing.\n")
    else:
        report.append("No patch was required or applied.\n")
    report_path.write_text("\n".join(report), encoding="utf-8")
    return report_path


def create_documentation_account_patch(stale: list[Path]) -> list[Path]:
    changed: list[Path] = []
    stale_pattern = r"@bala\.jirajput966"
    for file_path in stale:
        content = file_path.read_text(encoding="utf-8")
        rendered_lines: list[str] = []
        file_changed = False
        for line in content.splitlines(keepends=True):
            if re.search(stale_pattern, line) and not is_negative_account_warning(line):
                replacement = re.sub(stale_pattern, TARGET_ACCOUNT, line)
                file_changed = file_changed or replacement != line
                rendered_lines.append(replacement)
            else:
                rendered_lines.append(line)
        if file_changed:
            file_path.write_text("".join(rendered_lines), encoding="utf-8")
            changed.append(file_path)
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a non-destructive repository maintenance audit.")
    parser.add_argument(
        "--apply-documentation-account-fix",
        action="store_true",
        help="Explicitly apply only affirmative stale-account replacements in Markdown documentation.",
    )
    args = parser.parse_args(argv)
    files = read_files()
    stale = check_stale_references(files)
    duplicates = check_duplicated_state(files)
    drift, drift_message = check_schedule_drift()
    unsafe = check_unsafe_patterns(files)
    if args.apply_documentation_account_fix:
        create_documentation_account_patch(stale)
    generate_report(stale, duplicates, drift, drift_message, unsafe, args.apply_documentation_account_fix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
