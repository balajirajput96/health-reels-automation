import unittest

from automation import drive_checkpoint_guard as guard


class DriveCheckpointGuardTests(unittest.TestCase):
    def make_pointer(self, completed, next_reel_id="0004"):
        return {
            "project": "3000_HINDI_RESEARCH_REELS",
            "provider": "Google Drive",
            "root": {"name": "3000_HINDI_RESEARCH_REELS", "id": "root"},
            "active_batch": {"name": "Batch_001", "id": "batch"},
            "completed": completed,
            "next_reel_id": next_reel_id,
            "target_total_reels": 3000,
            "reels_per_batch": 30,
            "format": {
                "language": "hi-IN",
                "aspect_ratio": "9:16",
                "target_duration_seconds": 60,
                "voice_required": True,
                "captions_required": True,
            },
        }

    def verified_record(self, sequence):
        return {
            "sequence": sequence,
            "reel_id": f"reel_{sequence:04d}_test",
            "production_stage": "final",
            "qc": {"drive_verified": True},
            "asset_checksums": {"mp4": f"sha-{sequence}"},
        }

    def pending_record(self, sequence):
        return {
            "sequence": sequence,
            "reel_id": f"reel_{sequence:04d}_test",
            "production_stage": "planned",
            "qc": {"drive_verified": False},
        }

    def checkpoint(self, completed=3, next_reel="reel_0004_cognitive_biases"):
        return {"completed_drive_verified": completed, "next_reel": next_reel}

    def pointer_entry(self, sequence):
        return {"status": "qc_passed_drive_verified", "video_file_id": f"video-{sequence}", "video_sha256": f"sha-{sequence}"}

    def test_recovered_three_reel_state_passes(self):
        queue = [self.verified_record(item) for item in (1, 2, 3)] + [self.pending_record(4)]
        pointer = self.make_pointer({f"reel_{item:04d}": self.pointer_entry(item) for item in (1, 2, 3)})
        self.assertEqual([], guard.validate(pointer, queue, self.checkpoint()))

    def test_stale_pointer_completion_is_rejected(self):
        queue = [self.verified_record(item) for item in (1, 2, 3)] + [self.pending_record(4)]
        completed = {f"reel_{item:04d}": self.pointer_entry(item) for item in (1, 2, 3, 4)}
        errors = guard.validate(self.make_pointer(completed, next_reel_id="0005"), queue, self.checkpoint())
        self.assertTrue(any("claims completions not verified" in error for error in errors))
        self.assertTrue(any("next_reel_id" in error for error in errors))

    def test_checkpoint_count_mismatch_is_rejected(self):
        queue = [self.verified_record(item) for item in (1, 2, 3)] + [self.pending_record(4)]
        pointer = self.make_pointer({f"reel_{item:04d}": self.pointer_entry(item) for item in (1, 2, 3)})
        errors = guard.validate(pointer, queue, self.checkpoint(completed=10))
        self.assertTrue(any("completed_drive_verified" in error for error in errors))

    def test_duplicate_queue_sequence_is_rejected(self):
        queue = [self.verified_record(1), self.verified_record(1), self.verified_record(2), self.verified_record(3)]
        pointer = self.make_pointer({f"reel_{item:04d}": self.pointer_entry(item) for item in (1, 2, 3)})
        errors = guard.validate(pointer, queue, self.checkpoint())
        self.assertTrue(any("duplicate sequence" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
