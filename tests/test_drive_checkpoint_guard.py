import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import drive_checkpoint_guard


class DriveCheckpointGuardTests(unittest.TestCase):
    def valid_pointer_data(self):
        return {
            "project": "3000_HINDI_RESEARCH_REELS",
            "provider": "Google Drive",
            "root": {"name": "3000_HINDI_RESEARCH_REELS"},
            "active_batch": {"name": "Batch_001"},
            "next_reel_id": "0011",
            "target_total_reels": 3000,
            "reels_per_batch": 30,
            "format": {
                "language": "hi-IN",
                "aspect_ratio": "9:16",
                "target_duration_seconds": 60,
                "voice_required": True,
                "captions_required": True,
            },
            "completed": {
                f"reel_{i:04d}": {
                    "status": "qc_passed_drive_verified",
                    "folder_id": f"folder_{i}",
                    "video_file_id": f"video_{i}",
                }
                for i in range(1, 11)
            },
        }

    def test_valid_drive_checkpoint_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            pointer_path = Path(directory) / "drive_active_state_pointer.json"
            pointer_path.write_text(json.dumps(self.valid_pointer_data()), encoding="utf-8")
            with patch.object(drive_checkpoint_guard, "POINTER", pointer_path):
                drive_checkpoint_guard.main()

    def test_invalid_project_fails_assertion(self):
        with tempfile.TemporaryDirectory() as directory:
            pointer_path = Path(directory) / "drive_active_state_pointer.json"
            data = self.valid_pointer_data()
            data["project"] = "INVALID_PROJECT"
            pointer_path.write_text(json.dumps(data), encoding="utf-8")
            with patch.object(drive_checkpoint_guard, "POINTER", pointer_path):
                with self.assertRaises(AssertionError):
                    drive_checkpoint_guard.main()


if __name__ == "__main__":
    unittest.main()
