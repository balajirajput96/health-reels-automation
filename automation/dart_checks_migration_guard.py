#!/usr/bin/env python3
"""Dart Checks Migration Guard and Assertion Auditor.

Enforces rules and workflows from the dart-migrate-to-checks-package skill:
- Ensures 'package:checks' is listed under dev_dependencies in pubspec.yaml.
- Flags legacy 'package:matcher' explicit dev_dependencies.
- Detects legacy assertions: expect(), expectLater(), having(), matches().
- Audits against critical pitfalls:
  * Collection equality pitfall: .equals([..]) vs .deepEquals([..])
  * Map containment: .contains(key) vs .containsKey(key)
  * Reason parameter: reason: '...' vs check(because: '...', ...)
  * RegExp matching: matches(str) vs matchesPattern(RegExp(...))
  * Property extraction: TypeMatcher.having() vs .has()
  * Synchronous vs Asynchronous throws handling
  * Nullable bool checks on bool?
- Audits test file imports (package:test/test.dart -> package:test/scaffolding.dart + package:checks/checks.dart).
- Provides assertion translation suggestions.
"""

from __future__ import annotations
import re
from pathlib import Path

# Legacy and anti-pattern regexes
EXPECT_RE = re.compile(r"\bexpect\s*\(")
EXPECT_LATER_RE = re.compile(r"\bexpectLater\s*\(")
HAVING_RE = re.compile(r"\.having\s*\(")
MATCHES_RE = re.compile(r"\bmatches\s*\(")
COLLECTION_EQUALS_RE = re.compile(r"(\bexpect\s*\([^,]+,\s*[\[{]|\.equals\s*\(\s*[\[{])")
MAP_CONTAINS_RE = re.compile(r"\bcheck\s*\([^)]*map[^)]*\)\s*\.contains\s*\(")
REASON_ARG_RE = re.compile(r"\bexpect\s*\([^)]*,\s*reason\s*:\s*['\"][^'\"]*['\"]\s*\)")
LEGACY_TEST_IMPORT_RE = re.compile(r"import\s+['\"]package:test/test\.dart['\"]")
CHECKS_IMPORT_RE = re.compile(r"import\s+['\"]package:checks/checks\.dart['\"]")
SCAFFOLDING_IMPORT_RE = re.compile(r"import\s+['\"]package:test/scaffolding\.dart['\"]")


def audit_pubspec_checks(pubspec_path: Path | str = "pubspec.yaml") -> dict:
    """Verifies that 'checks' is in dev_dependencies and flags redundant 'matcher'."""
    p = Path(pubspec_path).resolve()
    if not p.exists():
        return {
            "has_pubspec": False,
            "has_checks": False,
            "has_explicit_matcher": False,
            "message": f"pubspec file not found at {p}",
        }

    content = p.read_text(encoding="utf-8")
    lines = content.splitlines()

    in_dev_dependencies = False
    has_checks = False
    has_explicit_matcher = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("dev_dependencies:"):
            in_dev_dependencies = True
            continue
        elif line and not line[0].isspace() and ":" in line:
            in_dev_dependencies = False

        if in_dev_dependencies:
            if stripped.startswith("checks:"):
                has_checks = True
            elif stripped.startswith("matcher:"):
                has_explicit_matcher = True

    valid = has_checks and not has_explicit_matcher
    messages = []
    if not has_checks:
        messages.append("Missing 'checks' in dev_dependencies. Run: dart pub add dev:checks")
    if has_explicit_matcher:
        messages.append("Remove explicit 'matcher' from dev_dependencies; checks replaces it.")
    if valid:
        messages.append("pubspec is correctly configured for package:checks migration.")

    return {
        "has_pubspec": True,
        "has_checks": has_checks,
        "has_explicit_matcher": has_explicit_matcher,
        "valid": valid,
        "message": " | ".join(messages),
    }


def audit_dart_test_file(file_path: Path | str) -> dict:
    """Audits a single Dart test file for legacy matcher patterns and pitfalls."""
    p = Path(file_path).resolve()
    if not p.is_file():
        return {"file": str(p), "exists": False}

    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()

    has_legacy_import = bool(LEGACY_TEST_IMPORT_RE.search(text))
    has_checks_import = bool(CHECKS_IMPORT_RE.search(text))
    has_scaffolding_import = bool(SCAFFOLDING_IMPORT_RE.search(text))

    expect_count = len(EXPECT_RE.findall(text))
    expect_later_count = len(EXPECT_LATER_RE.findall(text))
    having_count = len(HAVING_RE.findall(text))
    matches_count = len(MATCHES_RE.findall(text))
    collection_equals_pitfalls = []
    map_contains_pitfalls = []
    reason_arg_count = len(REASON_ARG_RE.findall(text))

    for idx, line in enumerate(lines, 1):
        if COLLECTION_EQUALS_RE.search(line):
            collection_equals_pitfalls.append({
                "line": idx,
                "content": line.strip(),
                "issue": "Collection equality pitfall: .equals on collections checks identity. Use .deepEquals instead.",
            })
        if MAP_CONTAINS_RE.search(line):
            map_contains_pitfalls.append({
                "line": idx,
                "content": line.strip(),
                "issue": "Map containment pitfall: use .containsKey(...) instead of .contains(...).",
            })

    is_fully_migrated = (
        expect_count == 0
        and expect_later_count == 0
        and having_count == 0
        and len(collection_equals_pitfalls) == 0
        and not has_legacy_import
        and has_checks_import
    )

    issues = []
    if has_legacy_import:
        issues.append("Replace 'package:test/test.dart' with 'package:test/scaffolding.dart' and 'package:checks/checks.dart'.")
    if expect_count > 0 or expect_later_count > 0:
        issues.append(f"Found {expect_count} expect() and {expect_later_count} expectLater() calls requiring migration.")
    if having_count > 0:
        issues.append(f"Found {having_count} legacy .having() calls; convert to .has().")
    if matches_count > 0:
        issues.append(f"Found {matches_count} matches() calls; convert string patterns to matchesPattern(RegExp(...)).")
    if collection_equals_pitfalls:
        issues.append(f"Found {len(collection_equals_pitfalls)} potential collection equality pitfalls (use .deepEquals).")
    if map_contains_pitfalls:
        issues.append(f"Found {len(map_contains_pitfalls)} map containment pitfalls (use .containsKey).")

    return {
        "file": str(p),
        "exists": True,
        "is_fully_migrated": is_fully_migrated,
        "imports": {
            "has_legacy_test_import": has_legacy_import,
            "has_checks_import": has_checks_import,
            "has_scaffolding_import": has_scaffolding_import,
        },
        "counts": {
            "expect": expect_count,
            "expectLater": expect_later_count,
            "having": having_count,
            "matches": matches_count,
            "reason_arg": reason_arg_count,
            "collection_equals_pitfalls": len(collection_equals_pitfalls),
        },
        "pitfalls": collection_equals_pitfalls + map_contains_pitfalls,
        "issues": issues,
    }


def audit_test_directory(test_dir: Path | str = "test") -> dict:
    """Scans all Dart test files in a directory."""
    p = Path(test_dir).resolve()
    if not p.is_dir():
        return {
            "test_dir_exists": False,
            "message": f"Test directory not found at {p}",
            "total_files": 0,
            "migrated_files": 0,
            "pending_files": 0,
            "files": [],
        }

    test_files = list(p.glob("**/*_test.dart"))
    reports = [audit_dart_test_file(f) for f in test_files]

    migrated_count = sum(1 for r in reports if r["is_fully_migrated"])
    pending_count = len(reports) - migrated_count

    return {
        "test_dir_exists": True,
        "test_dir": str(p),
        "total_files": len(reports),
        "migrated_files": migrated_count,
        "pending_files": pending_count,
        "all_migrated": (len(reports) > 0 and pending_count == 0),
        "files": reports,
    }


def suggest_assertion_replacement(legacy_code: str) -> str:
    """Translates common matcher assertions to checks equivalents."""
    s = legacy_code.strip()

    # expect(actual, [1, 2, 3]) -> check(actual).deepEquals([1, 2, 3])
    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*(\[[^\]]*\]|\{[^\}]*\})\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).deepEquals({m.group(2).strip()});"

    # expect(actual, equals(expected)) or expect(actual, expected)
    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*equals\s*\((.*)\)\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).equals({m.group(2).strip()});"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isNotNull\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isNotNull();"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isNull\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isNull();"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isTrue\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isTrue();"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isFalse\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isFalse();"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isEmpty\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isEmpty();"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isNotEmpty\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isNotEmpty();"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*startsWith\s*\((.*)\)\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).startsWith({m.group(2).strip()});"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*endsWith\s*\((.*)\)\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).endsWith({m.group(2).strip()});"

    m = re.match(r"^expect\s*\(\s*([^,]+)\s*,\s*isA<([^>]+)>\s*\(\s*\)\s*\);?$", s)
    if m:
        return f"check({m.group(1).strip()}).isA<{m.group(2).strip()}>();"

    return f"// Manual review needed for: {s}"


if __name__ == "__main__":
    import json
    print(json.dumps({
        "audit": audit_test_directory(),
        "sample_suggestion": suggest_assertion_replacement("expect(myList, [1, 2, 3]);"),
    }, indent=2))
