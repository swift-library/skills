# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Profile exports fill package facts and preserve author content."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/swiftpm-docs"
COMMAND = SKILL / "scripts/export_profile.py"
MANIFEST = """// swift-tools-version: 6.2
import PackageDescription
let package = Package(
    name: "Example",
    platforms: [.visionOS(.v26_1), .iOS(.v15), .macOS(.v12), .tvOS(.v16), .watchOS(.v9)],
    products: []
)
"""


class ProfileExportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.package = self.root / "package"
        self.package.mkdir()
        (self.package / "Package.swift").write_text(MANIFEST)
        self.release = self.package / ".github/release.json"
        self.release.parent.mkdir()
        self.release.write_text(json.dumps({"check_command": "Scripts/check --strict"}))
        self.output = self.root / "export"

    def tearDown(self):
        self.temporary.cleanup()

    def export(self, *args, profile="minimal", output=None, expected=0):
        result = subprocess.run(
            [sys.executable, "-B", str(COMMAND), "--profile", profile,
             "--output", str(output if output is not None else self.output), *map(str, args)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def readme(self):
        return (self.output / "README.md").read_text()

    def test_package_facts_are_filled_in_declaration_order(self):
        self.export("--package-root", self.package)
        readme = self.readme()
        self.assertIn("swift build\nScripts/check --strict\n", readme)
        self.assertIn(
            "Swift 6.2 or later; visionOS 26.1, iOS 15, macOS 12, tvOS 16, watchOS 9",
            readme,
        )

    def test_set_values_win_over_package_facts(self):
        self.export(
            "--package-root", self.package, "--set", "build-command=Scripts/build",
            "--set", "test-command=Scripts/test", "--set", "requirement=Custom requirement",
        )
        readme = self.readme()
        self.assertIn("Scripts/build\nScripts/test\n", readme)
        self.assertIn("- Custom requirement\n", readme)
        self.assertNotIn("Swift 6.2 or later", readme)

    def test_identity_values_are_filled(self):
        self.export("--set", "repo-name=swift-example", "--set", "package-name=Example")
        self.assertIn("# swift-example\n", self.readme())
        self.assertIn("`swift-example` is the home of `Example`.", self.readme())
        self.assertIn(
            "# swift-example Agent Guide",
            (self.output / "AGENTS.md").read_text(),
        )

    def test_unknown_set_name_is_a_usage_error(self):
        result = self.export("--set", "unknown-value=Example", expected=2)
        self.assertIn("unknown-value", result.stderr)
        self.assertFalse(self.output.exists())

    def test_malformed_set_is_a_usage_error(self):
        for argument in ("repo-name", "Repo-name=Example"):
            with self.subTest(argument=argument):
                result = self.export("--set", argument, expected=2)
                self.assertIn(argument, result.stderr)

    def test_inherited_contributing_is_omitted(self):
        self.export("--inherited", "CONTRIBUTING.md")
        self.assertFalse((self.output / "CONTRIBUTING.md").exists())
        self.assertTrue((self.output / "README.md").is_file())

    def test_unknown_inherited_path_is_a_usage_error(self):
        result = self.export("--inherited", "SECURITY.md", expected=2)
        self.assertIn("SECURITY.md", result.stderr)
        self.assertFalse(self.output.exists())

    def test_inheritance_does_not_omit_required_rows(self):
        self.export("--inherited", "README.md")
        self.assertTrue((self.output / "README.md").is_file())

    def test_existing_file_fails_without_force(self):
        self.output.mkdir()
        existing = self.output / "README.md"
        existing.write_bytes(b"existing documentation\n")
        result = self.export(expected=1)
        self.assertIn(str(existing), result.stderr)
        self.assertEqual(existing.read_bytes(), b"existing documentation\n")
        self.assertFalse((self.output / "AGENTS.md").exists())

    def test_force_overwrites_exports_and_preserves_other_files(self):
        self.export()
        unrelated = self.output / "Documentation/Local.md"
        unrelated.write_bytes(b"local documentation\r\n")
        (self.output / "README.md").write_text("old documentation\n")
        self.export("--force", "--set", "repo-name=swift-example")
        self.assertIn("# swift-example\n", self.readme())
        self.assertEqual(unrelated.read_bytes(), b"local documentation\r\n")

    def test_author_placeholders_and_guidance_remain(self):
        self.export("--package-root", self.package, "--set", "repo-name=swift-example")
        self.assertIn("<one-line-purpose>", self.readme())
        source = (SKILL / "templates/Documentation.Reference.Release.md.tpl").read_text()
        release = (self.output / "Documentation/Reference/Release.md").read_text()
        self.assertEqual(release, source.replace("<repo-name>", "swift-example"))

    def test_exports_match_each_profile_map_and_report_each_file(self):
        for profile in ("minimal", "standard"):
            with self.subTest(profile=profile):
                output = self.root / profile
                result = self.export(profile=profile, output=output)
                expected = {
                    Path(line.split("`")[1])
                    for line in (SKILL / "profiles" / f"{profile}.md").read_text().splitlines()
                    if line.startswith("| `")
                }
                actual = {path.relative_to(output) for path in output.rglob("*") if path.is_file()}
                self.assertEqual(actual, expected)
                self.assertEqual(set(result.stdout.splitlines()), {str(output / path) for path in expected})
                self.assertEqual(len(result.stdout.splitlines()), len(expected))

    def test_export_without_values_preserves_template_bytes(self):
        self.export()
        self.assertEqual(
            (self.output / "README.md").read_bytes(),
            (SKILL / "templates/README.md.tpl").read_bytes(),
        )

    def test_missing_release_file_defaults_to_swift_test(self):
        self.release.unlink()
        self.export("--package-root", self.package)
        self.assertIn("swift build\nswift test\n", self.readme())

    def test_missing_check_command_defaults_to_swift_test(self):
        self.release.write_text("{}\n")
        self.export("--package-root", self.package)
        self.assertIn("swift build\nswift test\n", self.readme())

    def test_manifest_without_platforms_has_only_swift_requirement(self):
        (self.package / "Package.swift").write_text(
            '// swift-tools-version: 6.0\nimport PackageDescription\n'
            'let package = Package(name: "Example")\n'
        )
        self.export("--package-root", self.package)
        self.assertIn("- Swift 6.0 or later\n", self.readme())

    def test_unreadable_tools_version_names_manifest(self):
        manifest = self.package / "Package.swift"
        manifest.write_text('import PackageDescription\nlet package = Package(name: "Example")\n')
        result = self.export("--package-root", self.package, expected=1)
        self.assertIn(str(manifest), result.stderr)
        self.assertIn("swift-tools-version", result.stderr)

    def test_invalid_release_json_names_file(self):
        self.release.write_text("{\n")
        result = self.export("--package-root", self.package, expected=1)
        self.assertIn(str(self.release), result.stderr)

    def template_check(self, expected):
        result = subprocess.run(
            [str(ROOT / "Scripts/check-package-template"), str(self.package)],
            env={**os.environ, "RUNNER_TEMP": str(self.root / "runner")},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertFalse((self.root / "runner/export").exists())
        return result

    def export_template(self):
        self.export(
            "--package-root", self.package, "--set", "repo-name=swift-package-template",
            "--set", "package-name=swift-package-template", output=self.package,
        )

    def test_template_check_accepts_matching_export_and_extra_files(self):
        self.export_template()
        self.template_check(0)
        self.template_check(0)
        self.assertTrue((self.package / "Package.swift").is_file())

    def test_template_check_prints_unified_diff_for_changed_file(self):
        self.export_template()
        (self.package / "README.md").write_text("changed documentation\n")
        result = self.template_check(1)
        self.assertIn(f"--- {self.package / 'README.md'}", result.stdout)
        self.assertIn("+++ ", result.stdout)
        self.assertIn("-changed documentation", result.stdout)
        self.assertIn("+# swift-package-template", result.stdout)

    def test_template_check_reports_missing_file(self):
        self.export_template()
        missing = self.package / "CONTRIBUTING.md"
        missing.unlink()
        result = self.template_check(1)
        self.assertIn(str(missing), result.stderr)
        self.assertIn("+++ ", result.stdout)


if __name__ == "__main__":
    unittest.main()
