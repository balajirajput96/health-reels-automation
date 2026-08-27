import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import repository_maintenance as maintenance


class RepositoryMaintenanceTests(unittest.TestCase):
    def test_negative_wrong_account_warning_is_not_marked_stale(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            warning = root / "warning.md"
            warning.write_text("Do not publish to @bala.jirajput966.\n", encoding="utf-8")
            self.assertEqual([], maintenance.check_stale_references([warning]))

    def test_affirmative_wrong_account_reference_is_reported_and_not_patched_without_opt_in(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            document = root / "target.md"
            document.write_text("Target account: @bala.jirajput966\n", encoding="utf-8")
            stale = maintenance.check_stale_references([document])
            self.assertEqual([document], stale)
            maintenance.generate_report(stale, [], False, None, [], False, root=root)
            self.assertIn("No files were changed", (root / maintenance.REPORT_NAME).read_text(encoding="utf-8"))
            self.assertIn("@bala.jirajput966", document.read_text(encoding="utf-8"))

    def test_explicit_account_patch_changes_only_affirmative_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            document = root / "target.md"
            document.write_text(
                "Target account: @bala.jirajput966\nDo not publish to @bala.jirajput966.\n",
                encoding="utf-8",
            )
            changed = maintenance.create_documentation_account_patch([document])
            self.assertEqual([document], changed)
            text = document.read_text(encoding="utf-8")
            self.assertIn("Target account: @balajirajput96", text)
            self.assertIn("Do not publish to @bala.jirajput966", text)

    def test_main_does_not_patch_without_explicit_flag(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            document = root / "target.md"
            document.write_text("Target account: @bala.jirajput966\n", encoding="utf-8")
            with patch.object(maintenance, "ROOT_DIR", root):
                self.assertEqual(0, maintenance.main([]))
            self.assertIn("@bala.jirajput966", document.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
