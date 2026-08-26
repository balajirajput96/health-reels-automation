import json
import tempfile
import unittest
from pathlib import Path

from automation import reel_3000_guard as guard


class Reel3000GuardTests(unittest.TestCase):
    def make_project(self, directory: Path) -> Path:
        root = directory / guard.PROJECT_NAME
        (root / "PROGRESS").mkdir(parents=True)
        master = {
            "project": {"id": guard.PROJECT_NAME},
            "counts": {
                "target": 3000,
                "completed_verified": 0,
                "in_production": 0,
                "pending": 3000,
                "retry_queue": 0,
                "failed_terminal": 0,
            },
        }
        (root / "MASTER_PROGRESS.json").write_text(json.dumps(master), encoding="utf-8")
        (root / "PROGRESS" / "events.jsonl").write_text("", encoding="utf-8")
        (root / "PROGRESS" / "RETRY_QUEUE.jsonl").write_text("", encoding="utf-8")
        record = {
            "reel_id": "Reel_0001",
            "status": "PENDING_EVIDENCE_RESEARCH",
            "completion_claimed": False,
            "topic_key": "test-topic",
        }
        (root / "PROGRESS" / "reel_registry.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
        return root

    def test_transition_cannot_skip_directly_to_completed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_project(Path(temporary))
            with self.assertRaisesRegex(ValueError, "Unsupported transition"):
                guard.transition(
                    root,
                    "Reel_0001",
                    "PENDING_EVIDENCE_RESEARCH",
                    "COMPLETED_VERIFIED",
                    {},
                    dry_run=True,
                )

    def test_completion_claim_outside_final_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_project(Path(temporary))
            registry = root / "PROGRESS" / "reel_registry.jsonl"
            registry.write_text(
                json.dumps(
                    {
                        "reel_id": "Reel_0001",
                        "status": "QC_PASSED",
                        "completion_claimed": True,
                        "topic_key": "test-topic",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            problems = guard.validate_project(root)
            self.assertTrue(any("completion_claimed" in problem for problem in problems))

    def test_retry_is_allowed_from_pending_and_is_counted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_project(Path(temporary))
            result = guard.transition(
                root,
                "Reel_0001",
                "PENDING_EVIDENCE_RESEARCH",
                "RETRY_QUEUED",
                {"retry_reason": "test"},
                dry_run=False,
            )
            self.assertEqual(result["decision"], "transition_recorded")
            master = json.loads((root / "MASTER_PROGRESS.json").read_text(encoding="utf-8"))
            self.assertEqual(master["counts"]["retry_queue"], 1)
            self.assertEqual(master["counts"]["pending"], 2999)


if __name__ == "__main__":
    unittest.main()
