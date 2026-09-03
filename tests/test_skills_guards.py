from __future__ import annotations
import unittest
from automation.xcode_project_guard import check_xcode_environment
from automation.android_cli_guard import check_android_cli, get_android_bin
from automation.resource_attribution import format_bq_command, format_gcloud_env, wrap_gcloud_command_string
from automation.dart_analysis_guard import check_dart_sdk, analyze_dart_project

class TestSkillsGuards(unittest.TestCase):
    def test_xcode_guard_environment(self):
        status = check_xcode_environment()
        self.assertIn("os", status)
        self.assertIn("has_project", status)
        self.assertIn("message", status)
        # On Linux, is_macos should be False
        self.assertFalse(status["is_macos"])
        self.assertIn("requires a macOS", status["message"])

    def test_android_cli_guard(self):
        status = check_android_cli()
        self.assertIn("installed", status)
        # We installed the Android CLI, so it should be installed
        self.assertTrue(status["installed"])
        self.assertIsNotNone(status["path"])

    def test_resource_attribution_bq(self):
        # Unlabelled command
        raw_cmd = ["bq", "query", "--use_legacy_sql=false", "SELECT 1"]
        attributed = format_bq_command(raw_cmd, ide="antigravity")
        self.assertIn("--label=datacloud=antigravity", attributed)

        # Already labelled command
        labelled = ["bq", "query", "--label", "datacloud=antigravity", "SELECT 1"]
        attributed_again = format_bq_command(labelled, ide="antigravity")
        self.assertEqual(attributed_again, labelled)

    def test_resource_attribution_gcloud(self):
        cmd = "gcloud compute instances list"
        wrapped = wrap_gcloud_command_string(cmd, ide="antigravity")
        self.assertTrue(wrapped.startswith("CLOUDSDK_METRICS_ENVIRONMENT=datacloud.antigravity"))

        env = format_gcloud_env({}, ide="antigravity")
        self.assertEqual(env["CLOUDSDK_METRICS_ENVIRONMENT"], "datacloud.antigravity")

    def test_dart_analysis_guard(self):
        status = analyze_dart_project()
        self.assertIn("has_dart_files", status)
        self.assertFalse(status["has_dart_files"])
        self.assertEqual(status["file_count"], 0)

if __name__ == "__main__":
    unittest.main()
