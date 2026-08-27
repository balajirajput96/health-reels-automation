#!/usr/bin/env python3
"""Deterministic repository-maintenance checks for the reels project.

The maintenance job is intentionally read-only with respect to safety language.
It audits active/promoted production content, reports findings, and may correct
only an explicitly stale target-account reference. Research archives, legacy
production files, generated media, and historical diagnostics are not scanned
for safety-language occurrences because those documents commonly describe
prohibitions and limitations rather than making claims.
"""

import datetime
import hashlib
import os
import re
from pathlib import Path

TARGET_ACCOUNT = "@balajirajput96"
SCHEDULE = "30 0 * * *"
UNSAFE_PATTERNS = (
    re.compile(r"\bcure\b", re.IGNORECASE),
    re.compile(r"\bguarantee\b", re.IGNORECASE),
    re.compile(r"\bdiagnosis\b", re.IGNORECASE),
    re.compile(r"\btreat\b", re.IGNORECASE),
    re.compile(r"\bmedical advice\b", re.IGNORECASE),
)
NEGATIVE_CONTEXT_PATTERNS = (
    re.compile(r"\bnot\s+(?:a\s+)?(?:cure|guarantee|diagnosis|treat|medical advice)\b", re.IGNORECASE),
    re.compile(r"\bno\s+(?:cure|guarantee|diagnosis)\b", re.IGNORECASE),
    re.compile(r"\b(?:never|cannot|can't|does not|doesn't|do not|don't|avoid|without)\s+(?:guarantee|diagnosis|treat)\b", re.IGNORECASE),
    re.compile(r"\bnot\s+(?:provide|offer|give)\s+(?:a\s+)?diagnosis\b", re.IGNORECASE),
    re.compile(r"\b(?:cure|guarantee|diagnosis|treat|medical advice)\b\s*(?:नहीं|नही|नहीं है|नहीं देता|नहीं देती|नहीं देना)", re.IGNORECASE),
)
ROOT_DIR = Path(__file__).resolve().parents[1]
ACTIVE_SCAN_ROOTS = (
    ROOT_DIR / "production" / "active_drive_batch001",
    ROOT_DIR / "production" / "active",
    ROOT_DIR / "production" / "promoted",
)
SAFETY_DOCUMENT_NAME_MARKERS = (
    "source-validation",
    "source_validation",
    "source-retry",
    "source_retry",
    "diagnostic",
    "standard",
)


def read_files():
    """Return markdown/YAML files in active or explicitly promoted content only."""
    files = []
    for scan_root in ACTIVE_SCAN_ROOTS:
        if not scan_root.exists():
            continue
        for root, _, filenames in os.walk(scan_root):
            if ".git" in root or "__pycache__" in root:
                continue
            for filename in filenames:
                if filename.endswith((".md", ".yml", ".yaml")):
                    files.append(Path(root) / filename)
    return sorted(files)


def hash_file(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def check_stale_references(files):
    """Find affirmative occurrences of the historical mistyped account name."""
    stale_pattern = re.compile(r"@bala\.jirajput966", re.IGNORECASE)
    affected = []
    for f in files:
        if f.suffix.lower() != ".md" or f.name.lower() in {"maintenance_report.md"}:
            continue
        content = f.read_text(encoding="utf-8")
        for line in content.splitlines():
            if stale_pattern.search(line):
                line_lower = line.lower()
                if not any(exclusion in line_lower for exclusion in ("not", "never", "excluded", "must not")):
                    affected.append(f)
                    break
    return affected


def check_duplicated_state(files):
    hashes = {}
    duplicates = []
    for f in files:
        if f.suffix.lower() != ".md" or f.name.lower() in {"maintenance_report.md"}:
            continue
        digest = hash_file(f)
        if digest in hashes:
            duplicates.append((hashes[digest], f))
        else:
            hashes[digest] = f
    return duplicates


def check_schedule_drift():
    workflow_file = ROOT_DIR / ".github/workflows/repository-maintenance.yml"
    if not workflow_file.exists():
        return True, "Workflow file not found"
    content = workflow_file.read_text(encoding="utf-8")
    if SCHEDULE not in content:
        return True, f"Schedule drifted. Expected {SCHEDULE}"
    return False, None


def _is_allowlisted_safety_document(path):
    lowered = path.name.lower()
    return any(marker in lowered for marker in SAFETY_DOCUMENT_NAME_MARKERS)


def _sentence_window(content, start, end):
    """Return the sentence/line containing a match and its local offset."""
    boundaries = ".!?\n;"
    left = max(content.rfind(char, 0, start) for char in boundaries)
    right_candidates = [content.find(char, end) for char in boundaries]
    right_candidates = [candidate for candidate in right_candidates if candidate != -1]
    right = min(right_candidates) if right_candidates else len(content)
    sentence_start = left + 1
    return content[sentence_start:right], start - sentence_start


def _is_negative_context(sentence, local_start, local_end):
    observed = sentence[:local_end]
    # English negation normally precedes the term; Hindi negation commonly
    # follows it. Limit postposed inspection to the immediate local phrase so
    # a later unrelated disclaimer cannot protect an earlier claim.
    suffix = sentence[local_start:min(len(sentence), local_end + 48)]
    return any(pattern.search(observed) or pattern.search(suffix) for pattern in NEGATIVE_CONTEXT_PATTERNS)


def check_unsafe_patterns(files):
    """Return affirmative unsupported health-language matches in active files.

    Prohibitions and disclaimers such as ``not a diagnosis`` are not findings.
    Word boundaries ensure ``treats`` is not mistaken for the verb ``treat``.
    """
    unsafe_found = []
    for f in files:
        if f.suffix.lower() != ".md" or _is_allowlisted_safety_document(f):
            continue
        content = f.read_text(encoding="utf-8")
        for pattern in UNSAFE_PATTERNS:
            for match in pattern.finditer(content):
                sentence, local_start = _sentence_window(content, match.start(), match.end())
                if not _is_negative_context(sentence, local_start, local_start + len(match.group(0))):
                    unsafe_found.append((f, pattern.pattern))
                    break
    return unsafe_found


def generate_report(stale, duplicates, drift, drift_msg, unsafe):
    report_path = ROOT_DIR / "MAINTENANCE_REPORT.md"
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    report = (
        f"# Daily Repository Maintenance Report\n\n**Date:** {today}\n\n"
        "This report audits active/promoted production content, workflow schedule drift, "
        "stale account references, and duplicated state. Safety-language findings are "
        "context-aware; archives and source-validation diagnostics are excluded.\n\n"
        "## Findings\n\n"
    )
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
        report += f"{findings_count}. **Duplicated Active Content:**\n"
        report += "   - Identical markdown content was found in active/promoted files.\n"
        for first, duplicate in duplicates:
            report += f"     - `{first.relative_to(ROOT_DIR)}` and `{duplicate.relative_to(ROOT_DIR)}`\n"
        report += "\n"
        findings_count += 1

    if drift:
        report += f"{findings_count}. **Schedule Configuration Drift:**\n"
        report += f"   - {drift_msg}\n\n"
        findings_count += 1

    if unsafe:
        report += f"{findings_count}. **Affirmative Unsupported Health-Language Patterns:**\n"
        for f, pattern in unsafe:
            report += f"   - `{f.relative_to(ROOT_DIR)}` contains `{pattern}` outside a negative context.\n"
        report += "\n"
        findings_count += 1

    if findings_count == 1:
        report += "No issues found in the active/promoted scan scope.\n\n## Proposed Patch\n\nNo patch required.\n"
    else:
        report += "## Proposed Patch\n\n"
        if stale:
            report += "Only stale affirmative account references may be corrected automatically. Safety wording is never rewritten by this job.\n"
        else:
            report += "Review the findings manually; this job does not rewrite health-language content.\n"

    report_path.write_text(report, encoding="utf-8")


def create_patch(stale):
    """Correct only affirmative stale account references; never rewrite safety terms."""
    stale_pattern = re.compile(r"@bala\.jirajput966", re.IGNORECASE)
    for f in stale:
        content = f.read_text(encoding="utf-8")
        new_lines = []
        for line in content.splitlines():
            line_lower = line.lower()
            if stale_pattern.search(line) and not any(
                exclusion in line_lower for exclusion in ("not", "never", "excluded", "must not")
            ):
                line = stale_pattern.sub(TARGET_ACCOUNT, line)
            new_lines.append(line)
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
