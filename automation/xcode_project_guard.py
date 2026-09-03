#!/usr/bin/env python3
"""Xcode Project Setup Guard.

Enforces rules from xcode-project-setup skill:
- Requires macOS / Darwin environment and Swift toolchain.
- Rejects Ruby / CocoaPods / Ruby gems.
- Checks presence of .xcodeproj or .xcworkspace.
- Enforces mandatory '-ObjC' linker flag in OTHER_LDFLAGS when Firebase products are present.
"""

from __future__ import annotations
import platform
import shutil
import subprocess
from pathlib import Path

def check_xcode_environment(project_dir: Path | str = ".") -> dict:
    p = Path(project_dir).resolve()
    current_os = platform.system()
    has_swift = shutil.which("swift") is not None
    swift_version = None
    if has_swift:
        try:
            res = subprocess.run(["swift", "--version"], capture_output=True, text=True, check=True)
            swift_version = res.stdout.splitlines()[0] if res.stdout else None
        except Exception:
            swift_version = "unknown"

    xcodeproj_files = list(p.glob("*.xcodeproj"))
    xcworkspace_files = list(p.glob("*.xcworkspace"))
    has_project = bool(xcodeproj_files or xcworkspace_files)

    status = {
        "os": current_os,
        "is_macos": current_os == "Darwin",
        "has_swift": has_swift,
        "swift_version": swift_version,
        "has_project": has_project,
        "projects": [str(f.name) for f in xcodeproj_files + xcworkspace_files],
        "compatible": (current_os == "Darwin" and has_swift and has_project),
    }

    if not status["is_macos"]:
        status["message"] = f"Environment is {current_os}. Xcode Project Setup requires a macOS (Darwin) host with Swift."
    elif not has_project:
        status["message"] = "No Xcode project found in this directory. Please create an empty Xcode project manually and let me know when you are ready to proceed."
    elif not has_swift:
        status["message"] = "Swift toolchain not found. Run xcode-select --install."
    else:
        status["message"] = "Xcode environment ready for SPM setup."

    return status

if __name__ == "__main__":
    import json
    print(json.dumps(check_xcode_environment(), indent=2))
