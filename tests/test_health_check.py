import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import health_check


class HealthCheckTests(unittest.TestCase):
    def manifest(self):
        return {
            "version": 1,
            "target_account": "@balajirajput96",
            "excluded_publish_account": "@bala.jirajput966",
            "ledger_path": "state/reels_ledger.json",
            "required_files": ["state/reels_ledger.json", ".github/workflows/audit.yml"],
            "allowed_ledger_stages": ["final", "drive_verified", "published"],
            "published_stage": "published",
            "workflow_schedules": {".github/workflows/audit.yml": "30 0 * * *"},
        }

    def write_fixture(self, root, items):
        ledger = root / "state" / "reels_ledger.json"
        ledger.parent.mkdir(parents=True)
        ledger.write_text(json.dumps({"version": 1, "items": items}), encoding="utf-8")
        workflow = root / ".github" / "workflows" / "audit.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text('on:\n  schedule:\n    - cron: "30 0 * * *"\n', encoding="utf-8")

    def test_valid_ledger_and_workflow_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_fixture(
                root,
                [{"stage": "published", "post_id": "abc", "target_account": "@balajirajput96"}],
            )
            errors = []
            with patch.object(health_check, "ROOT", root):
                manifest = health_check.validate_manifest(self.manifest(), errors)
                self.assertEqual(health_check.validate_required_files(manifest, errors), [])
                self.assertEqual(health_check.validate_ledger(manifest, errors), {"published": 1})
                health_check.validate_workflow_schedules(manifest, errors)
            self.assertEqual(errors, [])

    def test_drive_verified_record_is_accepted_without_post_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_fixture(
                root,
                [{"stage": "drive_verified", "target_account": "@balajirajput96"}],
            )
            errors = []
            with patch.object(health_check, "ROOT", root):
                self.assertEqual(
                    health_check.validate_ledger(self.manifest(), errors),
                    {"drive_verified": 1},
                )
            self.assertEqual(errors, [])

    def test_published_record_requires_post_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_fixture(root, [{"stage": "published", "target_account": "@balajirajput96"}])
            errors = []
            with patch.object(health_check, "ROOT", root):
                health_check.validate_ledger(self.manifest(), errors)
            self.assertTrue(any("has no post_id" in error for error in errors))

    def test_target_account_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_fixture(root, [{"stage": "final", "target_account": "@bala.jirajput966"}])
            errors = []
            with patch.object(health_check, "ROOT", root):
                health_check.validate_ledger(self.manifest(), errors)
            self.assertTrue(any("expected '@balajirajput96'" in error for error in errors))

    def test_workflow_schedule_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_fixture(root, [{"stage": "final", "target_account": "@balajirajput96"}])
            workflow = root / ".github" / "workflows" / "audit.yml"
            workflow.write_text('on:\n  schedule:\n    - cron: "0 0 * * *"\n', encoding="utf-8")
            errors = []
            with patch.object(health_check, "ROOT", root):
                health_check.validate_workflow_schedules(self.manifest(), errors)
            self.assertTrue(any("schedule drift" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
