from __future__ import annotations
import tempfile
import unittest
from pathlib import Path

from automation.xcode_project_guard import check_xcode_environment
from automation.android_cli_guard import check_android_cli, get_android_bin
from automation.resource_attribution import format_bq_command, format_gcloud_env, wrap_gcloud_command_string
from automation.dart_analysis_guard import check_dart_sdk, analyze_dart_project
from automation.dart_coverage_guard import (
    audit_pubspec_coverage,
    audit_coverage_directives,
    parse_lcov_report,
    validate_coverage_output,
    get_coverage_commands,
)
from automation.dart_checks_migration_guard import (
    audit_pubspec_checks,
    audit_dart_test_file,
    suggest_assertion_replacement,
)
from automation.flutter_widget_test_guard import (
    audit_pubspec_flutter_test,
    audit_widget_test_file,
    generate_widget_test_scaffold,
)

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
        self.assertIn("message", status)
        if status["installed"]:
            self.assertIsNotNone(status["path"])
        else:
            self.assertIsNone(status["path"])
            self.assertIn("install", status["message"].lower())

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

    def test_dart_coverage_guard_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            pubspec = tmppath / "pubspec.yaml"
            pubspec.write_text(
                "name: sample_app\n\ndev_dependencies:\n  test: ^1.24.0\n  coverage: ^1.15.0\n",
                encoding="utf-8",
            )
            audit = audit_pubspec_coverage(pubspec)
            self.assertTrue(audit["valid"])
            self.assertTrue(audit["has_coverage_dev_dependency"])

            # Test directives scan
            src_file = tmppath / "lib" / "sample.dart"
            src_file.parent.mkdir(parents=True, exist_ok=True)
            src_file.write_text(
                "// coverage:ignore-file\nclass Sample {\n  void foo() {}\n}\n",
                encoding="utf-8",
            )
            directives = audit_coverage_directives(src_file)
            self.assertEqual(directives["files_scanned"], 1)
            self.assertIn(str(src_file), directives["ignored_files"])

            # Test LCOV parser
            cov_dir = tmppath / "coverage"
            cov_dir.mkdir(parents=True, exist_ok=True)
            lcov = cov_dir / "lcov.info"
            lcov.write_text(
                "SF:lib/sample.dart\nDA:1,1\nDA:2,1\nDA:3,0\nLF:3\nLH:2\nend_of_record\n",
                encoding="utf-8",
            )
            lcov_metrics = parse_lcov_report(lcov)
            self.assertTrue(lcov_metrics["found"])
            self.assertEqual(lcov_metrics["lines_found"], 3)
            self.assertEqual(lcov_metrics["lines_hit"], 2)
            self.assertEqual(lcov_metrics["coverage_pct"], 66.67)

            # Test commands helper
            cmds = get_coverage_commands()
            self.assertIn("coverage:test_with_coverage", cmds["automated_command"])

    def test_dart_checks_migration_guard_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            pubspec = tmppath / "pubspec.yaml"
            pubspec.write_text(
                "name: sample_app\n\ndev_dependencies:\n  test: ^1.24.0\n  checks: ^0.3.0\n",
                encoding="utf-8",
            )
            audit = audit_pubspec_checks(pubspec)
            self.assertTrue(audit["valid"])
            self.assertTrue(audit["has_checks"])

            # Test file with legacy expect and collection pitfall
            test_file = tmppath / "test" / "widget_sample_test.dart"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text(
                """import 'package:test/test.dart';
void main() {
  test('sample', () {
    expect(items, [1, 2, 3]);
  });
}
""",
                encoding="utf-8",
            )
            report = audit_dart_test_file(test_file)
            self.assertFalse(report["is_fully_migrated"])
            self.assertEqual(report["counts"]["expect"], 1)
            self.assertGreater(len(report["pitfalls"]), 0)

            # Test assertion replacement suggester
            repl = suggest_assertion_replacement("expect(items, [1, 2, 3]);")
            self.assertEqual(repl, "check(items).deepEquals([1, 2, 3]);")

    def test_flutter_widget_test_guard_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            pubspec = tmppath / "pubspec.yaml"
            pubspec.write_text(
                "name: sample_flutter_app\n\ndev_dependencies:\n  flutter_test:\n    sdk: flutter\n",
                encoding="utf-8",
            )
            audit = audit_pubspec_flutter_test(pubspec)
            self.assertTrue(audit["valid"])

            # Test scaffold generation and audit
            scaffold = generate_widget_test_scaffold(
                widget_name="TodoWidget",
                import_path="package:sample/todo.dart",
                initial_text="Add",
                updated_text="Done",
            )
            test_file = tmppath / "test" / "todo_widget_test.dart"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text(scaffold, encoding="utf-8")

            report = audit_widget_test_file(test_file)
            self.assertTrue(report["is_compliant"])
            self.assertEqual(len(report["violations"]), 0)
            self.assertGreater(report["workflow_metrics"]["interactions"], 0)
            self.assertGreater(report["workflow_metrics"]["tree_rebuild_pumps"], 0)

if __name__ == "__main__":
    unittest.main()
