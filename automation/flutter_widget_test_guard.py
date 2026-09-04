#!/usr/bin/env python3
"""Flutter Widget Test Guard and Workflow Validator.

Enforces rules and workflows from the flutter-add-widget-test skill:
- Setup & Configuration: flutter_test under dev_dependencies, files in test/ with *_test.dart suffix.
- 9-step workflow validation:
  1. Define test: testWidgets(..., (WidgetTester tester) async { ... })
  2. Build widget: await tester.pumpWidget(...)
  3. Locate elements: find.text(), find.byType(), find.byKey(), etc.
  4. Verify initial state: expect(finder, matcher)
  5. Simulate interactions: tester.tap(), tester.enterText(), tester.drag(), etc.
  6. Rebuild tree: await tester.pump() or await tester.pumpAndSettle()
  7. Verify updated state: expect()
  8. Run & validate: flutter test test/<file>_test.dart
  9. Feedback loop: review output -> fix assertions -> re-run
- Anti-pattern detection:
  * Missing await on tester asynchronous calls.
  * Triggering interaction (tap/enterText/drag) without subsequent pump()/pumpAndSettle().
  * Unwrapped widgets needing directional or theme data.
- Generates standards-compliant widget test templates.
"""

from __future__ import annotations
import re
from pathlib import Path

TEST_WIDGETS_RE = re.compile(r"testWidgets\s*\(\s*['\"][^'\"]+['\"]\s*,\s*\(\s*(?:WidgetTester\s+)?([a-zA-Z0-9_]+)\s*\)\s*async\s*\{")
PUMP_WIDGET_RE = re.compile(r"\bawait\s+([a-zA-Z0-9_]+)\.pumpWidget\s*\(")
UN_AWAITED_PUMP_WIDGET_RE = re.compile(r"(?<!await\s)\b([a-zA-Z0-9_]+)\.pumpWidget\s*\(")
FINDER_RE = re.compile(r"\bfind\.(text|byType|byKey|byIcon|bySemanticsLabel|widgetWithText)\s*\(")
EXPECT_FINDER_RE = re.compile(r"\bexpect\s*\(\s*(?:find\.[^,]+|[a-zA-Z0-9_]+Finder)\s*,\s*(findsOneWidget|findsNothing|findsNWidgets\(\d+\)|findsWidgets)\s*\)")
INTERACTION_RE = re.compile(r"\bawait\s+([a-zA-Z0-9_]+)\.(tap|enterText|drag|fling|press|scrollUntilVisible)\s*\(")
PUMP_RE = re.compile(r"\bawait\s+([a-zA-Z0-9_]+)\.(pump|pumpAndSettle)\s*\(")
UN_AWAITED_PUMP_RE = re.compile(r"(?<!await\s)\b([a-zA-Z0-9_]+)\.(pump|pumpAndSettle)\s*\(")


def audit_pubspec_flutter_test(pubspec_path: Path | str = "pubspec.yaml") -> dict:
    """Verifies that flutter_test is configured under dev_dependencies."""
    p = Path(pubspec_path).resolve()
    if not p.exists():
        return {
            "has_pubspec": False,
            "has_flutter_test": False,
            "message": f"pubspec file not found at {p}",
        }

    content = p.read_text(encoding="utf-8")
    lines = content.splitlines()

    in_dev_dependencies = False
    has_flutter_test = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("dev_dependencies:"):
            in_dev_dependencies = True
            continue
        elif line and not line[0].isspace() and ":" in line:
            in_dev_dependencies = False

        if in_dev_dependencies and (stripped.startswith("flutter_test:") or stripped == "sdk: flutter"):
            has_flutter_test = True

    return {
        "has_pubspec": True,
        "has_flutter_test": has_flutter_test,
        "valid": has_flutter_test,
        "message": "flutter_test present in dev_dependencies" if has_flutter_test else "Missing flutter_test under dev_dependencies.",
    }


def audit_widget_test_file(file_path: Path | str) -> dict:
    """Audits a Flutter widget test file against the 9-step workflow and anti-patterns."""
    p = Path(file_path).resolve()
    if not p.is_file():
        return {"file": str(p), "exists": False}

    text = p.read_text(encoding="utf-8")
    is_named_correctly = p.name.endswith("_test.dart")
    is_in_test_dir = "test" in p.parts

    test_widgets_matches = TEST_WIDGETS_RE.findall(text)
    pump_widget_count = len(PUMP_WIDGET_RE.findall(text))
    unawaited_pump_widget = len(UN_AWAITED_PUMP_WIDGET_RE.findall(text))
    finder_count = len(FINDER_RE.findall(text))
    expect_count = len(EXPECT_FINDER_RE.findall(text))
    interaction_count = len(INTERACTION_RE.findall(text))
    pump_count = len(PUMP_RE.findall(text))
    unawaited_pump = len(UN_AWAITED_PUMP_RE.findall(text))

    has_material_app_wrap = "MaterialApp" in text or "Directionality" in text

    # Anti-pattern checks:
    # If interactions exist, there should be pumps following interactions
    # (total pumps should usually be >= interaction_count + pump_widget_count)
    unpumped_interactions = max(0, interaction_count - (pump_count - pump_widget_count)) if pump_count >= pump_widget_count else interaction_count

    violations = []
    if not is_named_correctly:
        violations.append(f"File name '{p.name}' must end with '_test.dart'.")
    if not is_in_test_dir:
        violations.append("Test file must reside within the 'test/' directory tree.")
    if unawaited_pump_widget > 0:
        violations.append(f"Found {unawaited_pump_widget} unawaited tester.pumpWidget() calls.")
    if unawaited_pump > 0:
        violations.append(f"Found {unawaited_pump} unawaited tester.pump()/pumpAndSettle() calls.")
    if interaction_count > 0 and pump_count == 0:
        violations.append("Simulated interactions (tap/enterText) detected without subsequent tester.pump() or pumpAndSettle().")
    if pump_widget_count > 0 and not has_material_app_wrap:
        violations.append("Widget tested without MaterialApp or Directionality wrapper; may cause 'No Directionality widget found' error.")

    is_compliant = (
        is_named_correctly
        and is_in_test_dir
        and len(test_widgets_matches) > 0
        and pump_widget_count > 0
        and len(violations) == 0
    )

    return {
        "file": str(p),
        "exists": True,
        "is_compliant": is_compliant,
        "workflow_metrics": {
            "test_widgets_blocks": len(test_widgets_matches),
            "pump_widget_calls": pump_widget_count,
            "finders_found": finder_count,
            "widget_assertions": expect_count,
            "interactions": interaction_count,
            "tree_rebuild_pumps": pump_count,
            "has_wrapper": has_material_app_wrap,
        },
        "violations": violations,
    }


def generate_widget_test_scaffold(
    widget_name: str,
    import_path: str,
    description: str = "renders correctly and handles interactions",
    initial_text: str = "Click Me",
    updated_text: str = "Clicked!",
) -> str:
    """Generates a complete, high-fidelity Flutter widget test compliant with skill guidelines."""
    return f"""import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '{import_path}';

void main() {{
  testWidgets('{description}', (WidgetTester tester) async {{
    // 1. Build the widget with MaterialApp harness
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: {widget_name}(),
        ),
      ),
    );

    // 2. Verify initial state
    final initialFinder = find.text('{initial_text}');
    expect(initialFinder, findsOneWidget);

    // 3. Simulate interaction
    await tester.tap(initialFinder);

    // 4. Rebuild the widget tree to reflect state changes
    await tester.pumpAndSettle();

    // 5. Verify updated state
    expect(find.text('{updated_text}'), findsOneWidget);
  }});
}}
"""


if __name__ == "__main__":
    import json
    print(json.dumps({
        "sample_scaffold": generate_widget_test_scaffold("CounterButton", "package:my_app/counter.dart"),
        "audit": audit_pubspec_flutter_test(),
    }, indent=2))
