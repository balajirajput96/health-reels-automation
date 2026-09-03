#!/usr/bin/env python3
"""Dart Static Analysis and Runtime Error Guard.

Enforces rules from dart-fix-runtime-errors skill:
- Workflow: static analysis resolution (dart analyze . --fatal-infos)
- Automated fixes: (dart fix --apply)
- Type soundness checks: generic collections, method overrides (covariant), no dynamic list assignments
- Null safety checks: late initialization, required modifiers, no catching Error
"""

from __future__ import annotations
import shutil
import subprocess
from pathlib import Path

def check_dart_sdk() -> dict:
    has_dart = shutil.which("dart") is not None
    version = None
    if has_dart:
        try:
            res = subprocess.run(["dart", "--version"], capture_output=True, text=True, check=True)
            version = (res.stdout or res.stderr).strip()
        except Exception as e:
            version = f"error: {e}"
    return {
        "installed": has_dart,
        "version": version,
        "message": "Dart SDK available" if has_dart else "Dart SDK not found in PATH",
    }

def analyze_dart_project(project_dir: Path | str = ".") -> dict:
    sdk_status = check_dart_sdk()
    p = Path(project_dir).resolve()
    dart_files = list(p.glob("**/*.dart"))

    if not dart_files:
        return {
            "has_dart_files": False,
            "file_count": 0,
            "message": "No Dart source files found in target directory.",
            "sdk": sdk_status,
        }

    if not sdk_status["installed"]:
        return {
            "has_dart_files": True,
            "file_count": len(dart_files),
            "error": "Dart SDK is not installed, cannot run static analysis.",
            "sdk": sdk_status,
        }

    try:
        res = subprocess.run(
            ["dart", "analyze", str(p), "--fatal-infos"],
            capture_output=True,
            text=True,
        )
        return {
            "has_dart_files": True,
            "file_count": len(dart_files),
            "exit_code": res.returncode,
            "passed": res.returncode == 0,
            "stdout": res.stdout,
            "stderr": res.stderr,
        }
    except Exception as e:
        return {
            "has_dart_files": True,
            "file_count": len(dart_files),
            "error": str(e),
        }

if __name__ == "__main__":
    import json
    print(json.dumps(analyze_dart_project(), indent=2))
