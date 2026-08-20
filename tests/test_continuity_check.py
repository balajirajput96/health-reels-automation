import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import continuity_check


class ContinuityCheckTests(unittest.TestCase):
    def manifest(self):
        return {
            "version": 1,
            "services": [
                {"id": "github_cli", "command": "gh"},
                {"id": "google_jules", "command": None},
            ],
            "required_repository_files": ["automation/required.py"],
        }

    def test_valid_manifest_passes_with_required_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            required = root / "automation" / "required.py"
            required.parent.mkdir(parents=True)
            required.write_text("# required\n", encoding="utf-8")
            with patch.object(continuity_check, "ROOT", root):
                errors, services = continuity_check.validate_manifest(self.manifest(), False)
            self.assertEqual(errors, [])
            self.assertEqual(services[0]["local_command_available"], None)

    def test_missing_required_file_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(continuity_check, "ROOT", Path(directory)):
                errors, _ = continuity_check.validate_manifest(self.manifest(), False)
            self.assertTrue(any("Required repository file is missing" in error for error in errors))

    def test_duplicate_service_identifier_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            required = root / "automation" / "required.py"
            required.parent.mkdir(parents=True)
            required.write_text("# required\n", encoding="utf-8")
            manifest = self.manifest()
            manifest["services"].append({"id": "github_cli", "command": "git"})
            with patch.object(continuity_check, "ROOT", root):
                errors, _ = continuity_check.validate_manifest(manifest, False)
            self.assertTrue(any("Duplicate CLI continuity service id" in error for error in errors))

    def test_local_command_check_does_not_invoke_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            required = root / "automation" / "required.py"
            required.parent.mkdir(parents=True)
            required.write_text("# required\n", encoding="utf-8")
            with patch.object(continuity_check, "ROOT", root):
                with patch.object(continuity_check.shutil, "which", return_value="/usr/bin/gh") as which:
                    errors, services = continuity_check.validate_manifest(self.manifest(), True)
            self.assertEqual(errors, [])
            which.assert_called_once_with("gh")
            self.assertTrue(services[0]["local_command_available"])
            self.assertIsNone(services[1]["local_command_available"])


if __name__ == "__main__":
    unittest.main()
