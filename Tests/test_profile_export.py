# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Profile exports fill package facts and preserve author content."""

import json
import os
from pathlib import Path
import shlex
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
        self.config = self.package / ".github/swift-package.json"
        self.config.parent.mkdir()
        self.config.write_text("{}\n")
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
        self.assertIn("swift build\nswift test\n", readme)
        self.assertIn(
            "Swift 6.2 or later; visionOS 26.1, iOS 15, macOS 12, tvOS 16, watchOS 9",
            readme,
        )

    def test_commented_out_platforms_are_ignored(self):
        (self.package / "Package.swift").write_text(
            '// swift-tools-version: 6.2\nimport PackageDescription\n'
            'let package = Package(\n'
            '    name: "https://example.test/*Example*/",\n'
            '    // platforms: [.macOS(.v99)],\n'
            '    /* platforms: [.tvOS(.v99)], /* nested comment */ */\n'
            '    platforms: [\n'
            '        // .watchOS(.v99),\n'
            '        /* .visionOS(.v99), */\n'
            '        .iOS /* deployment floor */ (.v15),\n'
            '        .macOS(.v12),\n'
            '    ],\n'
            '    products: []\n)\n'
        )
        self.export("--package-root", self.package)
        self.assertIn("- Swift 6.2 or later; iOS 15, macOS 12\n", self.readme())
        self.assertNotIn("99", self.readme())

    def test_only_commented_platforms_have_no_platform_requirement(self):
        for comment in ("// platforms: [.iOS(.v99)],", "/* platforms: [.iOS(.v99)], */"):
            with self.subTest(comment=comment):
                (self.package / "Package.swift").write_text(
                    '// swift-tools-version: 6.2\nimport PackageDescription\n'
                    f'{comment}\nlet package = Package(name: "Example")\n'
                )
                self.export("--package-root", self.package, "--force")
                self.assertIn("- Swift 6.2 or later\n", self.readme())

    def test_string_platform_version_preserves_its_text(self):
        (self.package / "Package.swift").write_text(
            '// swift-tools-version: 6.2\nimport PackageDescription\n'
            'let package = Package(name: "Example", '
            'platforms: [.iOS("17.0"), .macOS(.v12)])\n'
        )
        self.export("--package-root", self.package)
        self.assertIn("- Swift 6.2 or later; iOS 17.0, macOS 12\n", self.readme())

    def test_unsupported_platform_expression_fails_without_writing(self):
        manifest = self.package / "Package.swift"
        for expression in (
            ".iOS(minimumVersion)", "minimumPlatform",
            '.custom("Other", versionString: "1.0")',
            ".iOS(.v15) + extraPlatforms[0]",
        ):
            with self.subTest(expression=expression):
                manifest.write_text(
                    '// swift-tools-version: 6.2\nimport PackageDescription\n'
                    'let package = Package(name: "Example", '
                    f'platforms: [.macOS(.v12), {expression}])\n'
                )
                result = self.export("--package-root", self.package, expected=1)
                self.assertIn(str(manifest), result.stderr)
                self.assertIn(expression, result.stderr)
                self.assertFalse(self.output.exists())

    def test_set_values_win_over_package_facts(self):
        self.export(
            "--package-root", self.package, "--set", "build-command=scripts/build",
            "--set", "test-command=scripts/test", "--set", "requirement=Custom requirement",
        )
        readme = self.readme()
        self.assertIn("scripts/build\nscripts/test\n", readme)
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

    def test_symlinked_file_fails_before_any_writes(self):
        for location in ("outside", "inside", "missing"):
            with self.subTest(location=location):
                output = self.root / location
                destination = output / "Documentation/Reference/Release.md"
                destination.parent.mkdir(parents=True)
                existing = output / "AGENTS.md"
                existing.write_bytes(b"existing guide\n")
                referent = output / "Local.md" if location == "inside" else self.root / f"{location}.md"
                if location != "missing":
                    referent.write_bytes(b"existing release\n")
                destination.symlink_to(referent)
                before = {path.relative_to(output) for path in output.rglob("*")}

                result = self.export("--force", output=output, expected=1)

                self.assertIn(str(destination), result.stderr)
                self.assertEqual(existing.read_bytes(), b"existing guide\n")
                self.assertTrue(destination.is_symlink())
                self.assertEqual({path.relative_to(output) for path in output.rglob("*")}, before)
                if location == "missing":
                    self.assertFalse(referent.exists())
                else:
                    self.assertEqual(referent.read_bytes(), b"existing release\n")

    def test_symlinked_parent_directory_fails_before_any_writes(self):
        for exists in (True, False):
            with self.subTest(parent_exists=exists):
                output = self.root / f"export-{exists}"
                output.mkdir()
                existing = output / "AGENTS.md"
                existing.write_bytes(b"existing guide\n")
                outside = self.root / f"outside-{exists}"
                if exists:
                    outside.mkdir()
                    (outside / "README.md").write_bytes(b"existing index\n")
                parent = output / "Documentation"
                parent.symlink_to(outside, target_is_directory=True)

                result = self.export("--force", output=output, expected=1)

                self.assertIn(str(parent), result.stderr)
                self.assertEqual(existing.read_bytes(), b"existing guide\n")
                self.assertTrue(parent.is_symlink())
                self.assertEqual(set(output.iterdir()), {existing, parent})
                if exists:
                    self.assertEqual(set(outside.iterdir()), {outside / "README.md"})
                    self.assertEqual((outside / "README.md").read_bytes(), b"existing index\n")
                else:
                    self.assertFalse(outside.exists())

    def test_directory_destination_fails_before_any_writes(self):
        destination = self.output / "Documentation/Reference/Release.md"
        destination.mkdir(parents=True)
        result = self.export("--force", expected=1)
        self.assertIn(str(destination), result.stderr)
        self.assertTrue(destination.is_dir())
        self.assertFalse((self.output / "AGENTS.md").exists())
        self.assertFalse((self.output / "README.md").exists())

    def test_file_parent_fails_before_any_writes(self):
        parent = self.output / "Documentation"
        self.output.mkdir()
        parent.write_bytes(b"existing file\n")
        result = self.export("--force", expected=1)
        self.assertIn(str(parent), result.stderr)
        self.assertEqual(parent.read_bytes(), b"existing file\n")
        self.assertEqual(set(self.output.iterdir()), {parent})

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

    def test_missing_configuration_uses_root_package(self):
        self.config.unlink()
        self.export("--package-root", self.package)
        self.assertIn("swift build\nswift test\n", self.readme())

    def test_root_package_directory_preserves_commands(self):
        self.config.write_text(json.dumps({"package_directory": "."}))
        self.export("--package-root", self.package)
        self.assertIn("swift build\nswift test\n", self.readme())

    def test_nested_package_selects_manifest_and_quotes_commands(self):
        for directory in ("Packages/Core", "Packages/Client's Core"):
            with self.subTest(directory=directory):
                nested = self.package / directory
                nested.mkdir(parents=True)
                (nested / "Package.swift").write_text(MANIFEST.replace("6.2", "6.1"))
                self.config.write_text(json.dumps({"package_directory": directory}))
                self.export("--package-root", self.package, "--force")
                self.assertIn("- Swift 6.1 or later;", self.readme())
                for line in self.readme().splitlines():
                    if line.startswith(("swift build", "swift test")):
                        self.assertEqual(shlex.split(line)[2:], ["--package-path", directory])
                self.assertIn(f"swift build --package-path {shlex.quote(directory)}\n", self.readme())
                self.assertIn(f"swift test --package-path {shlex.quote(directory)}\n", self.readme())

    def test_nested_package_does_not_require_root_manifest(self):
        nested = self.package / "Package"
        nested.mkdir()
        (self.package / "Package.swift").rename(nested / "Package.swift")
        self.config.write_text(json.dumps({"package_directory": "Package"}))
        self.export("--package-root", self.package)
        self.assertIn("swift test --package-path Package\n", self.readme())

    def test_missing_selected_manifest_fails_before_writing(self):
        self.config.write_text(json.dumps({"package_directory": "Missing"}))
        result = self.export("--package-root", self.package, expected=1)
        self.assertIn(str(self.package / "Missing/Package.swift"), result.stderr)
        self.assertFalse(self.output.exists())

    def test_invalid_configuration_fails_before_writing(self):
        for config in ([], None, {"package_directory": []}, {"package_directory": ""},
                       {"package_directory": "../outside"}, {"package_directory": str(self.root)}):
            with self.subTest(config=config):
                self.config.write_text(json.dumps(config))
                result = self.export("--package-root", self.package, expected=1)
                self.assertIn(str(self.config), result.stderr)
                self.assertFalse(self.output.exists())

    def test_package_directory_cannot_resolve_outside_repository(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "Package.swift").write_text(MANIFEST)
        (self.package / "Linked").symlink_to(outside, target_is_directory=True)
        self.config.write_text(json.dumps({"package_directory": "Linked"}))
        result = self.export("--package-root", self.package, expected=1)
        self.assertIn(str(self.config), result.stderr)
        self.assertFalse(self.output.exists())

    def test_package_exports_only_replace_fact_placeholders(self):
        replacements = {
            "<build-command>": "swift build",
            "<test-command>": "swift test",
            "<requirement>": "Swift 6.2 or later; visionOS 26.1, iOS 15, macOS 12, tvOS 16, watchOS 9",
        }
        for profile in ("minimal", "standard"):
            with self.subTest(profile=profile):
                output = self.root / profile
                self.export("--package-root", self.package, profile=profile, output=output)
                for line in (SKILL / "profiles" / f"{profile}.md").read_text().splitlines():
                    if not line.startswith("| `"):
                        continue
                    target, source = line.split("`")[1:4:2]
                    expected = (SKILL / "profiles" / source).read_bytes()
                    for placeholder, value in replacements.items():
                        expected = expected.replace(placeholder.encode(), value.encode())
                    self.assertEqual((output / target).read_bytes(), expected, target)

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

    def test_invalid_configuration_json_names_file(self):
        self.config.write_text("{\n")
        result = self.export("--package-root", self.package, expected=1)
        self.assertIn(str(self.config), result.stderr)
        self.assertFalse(self.output.exists())

    def template_check(self, expected):
        result = subprocess.run(
            [str(ROOT / "scripts/check-package-template"), str(self.package)],
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
