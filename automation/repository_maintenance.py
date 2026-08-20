#!/usr/bin/env python3
"""Daily repository-maintenance workflow for health-reels automation.

Reads policy, editorial-standard, and integration-audit documents.
Checks that documented schedules, target account @balajirajput96, and
safety constraints remain internally consistent. Flags stale references,
duplicated state, unsafe health-language patterns, and untracked config drift.
Produces a concise markdown maintenance report and a proposed patch if
changes are documentation-only, testable, and non-breaking.
"""

import datetime
import hashlib
import os
import re
from pathlib import Path

TARGET_ACCOUNT = "@balajirajput96"
SCHEDULE = "30 0 * * *"
UNSAFE_PATTERNS = ["cure", "guarantee", "diagnosis", "medical advice"]
ROOT_DIR = Path(__file__).resolve().parents[1]

def read_files():
    files = []
    for root, _, filenames in os.walk(ROOT_DIR):
        if '.git' in root or '__pycache__' in root:
            continue
        for filename in filenames:
            if filename.endswith(".md") or filename.endswith(".yml"):
                files.append(Path(root) / filename)
    return files

def hash_file(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def check_stale_references(files):
    # Match the stale account name only when it is mistakenly listed as the target
    stale_pattern = r"@bala\.jirajput966"
    affected = []
    for f in files:
        if f.suffix == ".md" and f.name not in ["MAINTENANCE_REPORT.md", "maintenance_report.md"]:
            content = f.read_text(encoding="utf-8")
            if re.search(stale_pattern, content):
                # Ensure it's not a context-appropriate warning
                is_stale = False
                for line in content.splitlines():
                    if re.search(stale_pattern, line):
                        line_lower = line.lower()
                        if not any(exclusion in line_lower for exclusion in ["not", "never", "excluded", "must not"]):
                            is_stale = True
                            break
                if is_stale:
                    affected.append(f)
    return affected

def check_duplicated_state(files):
    hashes = {}
    duplicates = []
    for f in files:
        if f.suffix == ".md" and f.name not in ["MAINTENANCE_REPORT.md", "maintenance_report.md"]:
            h = hash_file(f)
            if h in hashes:
                duplicates.append((hashes[h], f))
            else:
                hashes[h] = f
    return duplicates

def check_schedule_drift():
    workflow_file = ROOT_DIR / ".github/workflows/repository-maintenance.yml"
    if not workflow_file.exists():
        return True, "Workflow file not found"
    content = workflow_file.read_text(encoding="utf-8")
    if SCHEDULE not in content:
        return True, f"Schedule drifted. Expected {SCHEDULE}"
    return False, None

def check_unsafe_patterns(files):
    unsafe_found = []
    for f in files:
        if f.suffix == ".md" and f.name not in ["MAINTENANCE_REPORT.md", "maintenance_report.md"]:
            content = f.read_text(encoding="utf-8").lower()
            for pattern in UNSAFE_PATTERNS:
                # Disallow raw occurrences unless it's the standard itself
                if pattern in content and "HEALTH_CONTENT_EDITORIAL_STANDARD.md" not in f.name:
                    unsafe_found.append((f, pattern))
    return unsafe_found

def generate_report(stale, duplicates, drift, drift_msg, unsafe):
    report_path = ROOT_DIR / "MAINTENANCE_REPORT.md"
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    report = f"# Daily Repository Maintenance Report\n\n**Date:** {today}\n\n"
    report += "This report identifies configuration drift, stale references, and safety constraints checked across the private health-reels automation repository.\n\n## Findings\n\n"

    findings_count = 1

    if stale:
        report += f"{findings_count}. **Incorrect Target Account References:**\n"
        report += "   - Stale references to `@bala.jirajput966` were found.\n"
        report += "   - **Affected files:**\n"
        for f in stale:
            report += f"     - `{f.relative_to(ROOT_DIR)}`\n"
        report += "\n"
        findings_count += 1

    if duplicates:
        report += f"{findings_count}. **Duplicated State:**\n"
        report += "   - Duplicated content found.\n"
        report += "   - **Affected files:**\n"
        for d1, d2 in duplicates:
            report += f"     - `{d1.relative_to(ROOT_DIR)}` and `{d2.relative_to(ROOT_DIR)}`\n"
        report += "\n"
        findings_count += 1

    if drift:
        report += f"{findings_count}. **Schedule Configuration Drift:**\n"
        report += f"   - {drift_msg}\n\n"
        findings_count += 1

    if unsafe:
        report += f"{findings_count}. **Unsafe Health-Language Patterns:**\n"
        report += "   - Unsafe patterns detected.\n"
        for f, p in unsafe:
            report += f"     - `{f.relative_to(ROOT_DIR)}` contains '{p}'\n"
        report += "\n"
        findings_count += 1

    if findings_count == 1:
        report += "No issues found. All configurations, state, and safety constraints are consistent.\n"
        report += "\n## Proposed Patch\n\nNo patch required.\n"
    else:
        report += "## Proposed Patch\n\n"
        if stale:
            report += "A documentation-only patch has been prepared to correct the stale target account references. "
        report += "Please review the proposed patch to ensure constraints and standards are maintained.\n"

    report_path.write_text(report, encoding="utf-8")

def create_patch(stale):
    for f in stale:
        content = f.read_text(encoding="utf-8")
        stale_pattern = r"@bala\.jirajput966"

        new_lines = []
        for line in content.splitlines():
            if re.search(stale_pattern, line):
                line_lower = line.lower()
                if not any(exclusion in line_lower for exclusion in ["not", "never", "excluded", "must not"]):
                    line = re.sub(stale_pattern, TARGET_ACCOUNT, line)
            new_lines.append(line)

        # Determine whether it's safe to replace the account
        # Since 'not @bala.jirajput966' exists, it means replacing it would make it 'not @balajirajput96',
        # which defeats the purpose. So we replace only affirmative occurrences.

        f.write_text("\n".join(new_lines) + ("\n" if content.endswith("\n") else ""), encoding="utf-8")

def main():
    files = read_files()
    stale = check_stale_references(files)
    duplicates = check_duplicated_state(files)
    drift, drift_msg = check_schedule_drift()
    unsafe = check_unsafe_patterns(files)

    generate_report(stale, duplicates, drift, drift_msg, unsafe)

    if stale:
        create_patch(stale)

if __name__ == "__main__":
    main()
