import json
import tempfile
import unittest
from pathlib import Path

from automation.select_next_reel import choose


class SelectNextReelTests(unittest.TestCase):
    def test_skips_topic_recorded_in_notes_and_selects_next_unique_row(self):
        backlog = [
            {
                "Canonical Title": "Optimizing Your Bedroom Environment For Better Sleep Quality",
                "Subject": "Sleep environment: bedroom darkness, noise, and comfort as contextual sleep supports",
            },
            {
                "Canonical Title": "Regular Meal Timing And Everyday Energy Rhythms Explained",
                "Subject": "Regular meal timing and everyday energy rhythms",
                "Primary Source": "https://example.test/primary",
            },
        ]
        ledger = {
            "items": [
                {
                    "filename": "REEL-0002.mp4",
                    "stage": "drive_verified_fallback",
                    "notes": "Sleep environment: darkness, noise, temperature, and comfort.",
                }
            ]
        }
        selection, audit = choose(backlog, ledger)
        self.assertEqual(selection["title"], "Regular Meal Timing And Everyday Energy Rhythms Explained")
        self.assertEqual(audit["skipped"][0]["reason"], "ledger_identity_match")

    def test_external_drive_claims_skip_existing_canonical_topic(self):
        backlog = [
            {
                "Canonical Title": "Predictive Processing And Perceptual Inference Explained",
                "Subject": "Predictive processing and how the brain uses expectations",
            },
            {
                "Canonical Title": "Regular Meal Timing And Everyday Energy Rhythms Explained",
                "Subject": "Regular meal timing and everyday energy rhythms",
            },
        ]
        selection, audit = choose(
            backlog,
            {"items": []},
            [{
                "reel_id": "REEL-0003",
                "title": "Predictive processing: क्या predictive brain reality को ignore करता है?",
                "topic": "Predictive processing and perceptual inference",
                "status": "complete_drive_verified",
            }],
        )
        self.assertEqual(selection["title"], "Regular Meal Timing And Everyday Energy Rhythms Explained")
        self.assertEqual(audit["external_claim_items"], 1)
        self.assertEqual(audit["skipped"][0]["reason"], "ledger_or_drive_identity_match")

    def test_selection_is_json_serializable_and_does_not_require_mutation(self):
        selection, audit = choose(
            [{"Canonical Title": "Fresh Topic", "Subject": "A new validated subject"}],
            {"items": []},
        )
        payload = {"selection": selection, "audit": audit}
        self.assertEqual(json.loads(json.dumps(payload, ensure_ascii=False)), payload)

    def test_no_unused_concept_returns_none(self):
        selection, audit = choose(
            [{"Canonical Title": "Known Topic", "Subject": "Known subject"}],
            {"items": [{"notes": "Known Topic and Known subject already recorded"}]},
        )
        self.assertIsNone(selection)
        self.assertEqual(audit["skipped"][0]["reason"], "ledger_identity_match")


if __name__ == "__main__":
    unittest.main()
