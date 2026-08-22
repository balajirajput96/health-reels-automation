import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from automation import state_guard


class StateGuardTests(unittest.TestCase):
    def test_same_source_hash_is_duplicate(self):
        item = {"sha256": "abc123", "filename": "reel.mp4"}
        keys = {"source_id": "", "sha256": "abc123", "filename": "other.mp4", "draft_id": "", "post_id": ""}
        self.assertTrue(state_guard.matches(item, keys))

    def test_same_filename_with_different_hash_is_not_duplicate(self):
        item = {"sha256": "old-hash", "filename": "reel.mp4"}
        keys = {"source_id": "", "sha256": "new-hash", "filename": "reel.mp4", "draft_id": "", "post_id": ""}
        self.assertFalse(state_guard.matches(item, keys))

    def test_filename_is_fallback_identity_when_no_stronger_key_exists(self):
        item = {"filename": "reel.mp4"}
        keys = {"source_id": "", "sha256": "", "filename": "reel.mp4", "draft_id": "", "post_id": ""}
        self.assertTrue(state_guard.matches(item, keys))

    def test_register_requires_an_identity(self):
        args = Namespace(
            sha256="",
            file=None,
            source_id=None,
            filename=None,
            draft_id=None,
            post_id=None,
            stage="failed",
            target_account="@balajirajput96",
            notes=None,
        )
        with self.assertRaises(ValueError):
            state_guard.register(args)

    def test_register_accepts_drive_verified_fallback_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            args = Namespace(
                sha256="fallback-hash",
                file=None,
                source_id=None,
                filename="REEL-0002.mp4",
                draft_id=None,
                post_id=None,
                stage="drive_verified_fallback",
                target_account="@balajirajput96",
                notes="quota-limited fallback",
            )
            with patch.object(state_guard, "LEDGER", ledger):
                self.assertEqual(state_guard.register(args), 0)
                record = json.loads(ledger.read_text(encoding="utf-8"))["items"][0]
                self.assertEqual(record["stage"], "drive_verified_fallback")
                self.assertNotIn("post_id", record)

    def test_register_is_idempotent_for_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reel.mp4"
            path.write_bytes(b"stable source")
            ledger = Path(directory) / "ledger.json"
            args = Namespace(
                sha256="",
                file=str(path),
                source_id=None,
                filename=None,
                draft_id=None,
                post_id=None,
                stage="final",
                target_account="@balajirajput96",
                notes="test",
            )
            with patch.object(state_guard, "LEDGER", ledger):
                self.assertEqual(state_guard.register(args), 0)
                self.assertEqual(state_guard.register(args), 2)
                records = json.loads(ledger.read_text(encoding="utf-8"))
                self.assertEqual(len(records["items"]), 1)


if __name__ == "__main__":
    unittest.main()
