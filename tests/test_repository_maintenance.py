import tempfile
import unittest
from pathlib import Path

from automation import repository_maintenance


class RepositoryMaintenanceSafetyTests(unittest.TestCase):
    def _findings_for(self, filename, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / filename
            path.write_text(content, encoding="utf-8")
            return repository_maintenance.check_unsafe_patterns([path])

    def test_negative_diagnosis_disclaimer_is_not_flagged(self):
        findings = self._findings_for("script.md", "यह वीडियो diagnosis नहीं है और medical advice नहीं देता।")
        self.assertEqual(findings, [])

    def test_negative_english_disclaimer_is_not_flagged(self):
        findings = self._findings_for("script.md", "This is not a diagnosis and does not guarantee a cure.")
        self.assertEqual(findings, [])

    def test_affirmative_claim_is_flagged(self):
        findings = self._findings_for("script.md", "This breathing exercise will cure anxiety.")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0][1], r"\bcure\b")

    def test_treats_does_not_match_treat(self):
        findings = self._findings_for("script.md", "The experiment treats participants respectfully.")
        self.assertEqual(findings, [])

    def test_allowlisted_source_validation_file_is_skipped(self):
        findings = self._findings_for(
            "2026-08-27__source-validation.md",
            "The evidence does not guarantee an outcome and is not medical advice.",
        )
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
