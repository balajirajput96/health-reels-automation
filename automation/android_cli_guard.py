#!/usr/bin/env python3
"""Android CLI Guard and Wrapper.

Enforces rules and workflows from the android-cli skill:
- Verifies installation of 'android' CLI.
- Checks SDK presence and environment info.
- Provides helper commands for project creation, layout inspection, and doc search.
"""

from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path

DEFAULT_ANDROID_BIN = Path("/home/ubuntu/.local/bin/android")

def get_android_bin() -> str | None:
    if shutil.which("android"):
        return shutil.which("android")
    try:
        if DEFAULT_ANDROID_BIN.exists() and os.access(DEFAULT_ANDROID_BIN, os.X_OK):
            return str(DEFAULT_ANDROID_BIN)
    except PermissionError:
        pass
    return None

def check_android_cli() -> dict:
    bin_path = get_android_bin()
    if not bin_path:
        return {
            "installed": False,
            "version": None,
            "path": None,
            "message": "android CLI not found in PATH or ~/.local/bin/android. Run install script: curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install.sh | bash",
        }

    try:
        res = subprocess.run([bin_path, "--version"], capture_output=True, text=True, check=True)
        # Parse version line (ignoring license headers)
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip() and not line.startswith("http") and "License" not in line and "Google" not in line and "Disable" not in line]
        version = lines[0] if lines else "installed"
        return {
            "installed": True,
            "version": version,
            "path": bin_path,
            "message": f"Android CLI is operational (version: {version})",
        }
    except Exception as e:
        return {
            "installed": True,
            "version": "unknown",
            "path": bin_path,
            "error": str(e),
            "message": "Failed to execute android --version",
        }

def list_templates() -> list[str]:
    bin_path = get_android_bin()
    if not bin_path:
        return []
    try:
        res = subprocess.run([bin_path, "create", "--list"], capture_output=True, text=True, check=True)
        return [l.strip() for l in res.stdout.splitlines() if l.strip()]
    except Exception:
        return []

if __name__ == "__main__":
    import json
    print(json.dumps(check_android_cli(), indent=2))
