# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""README facts report badge values, and README checks compare values, not styling."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills/swiftpm-readme/scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("check_readme", SCRIPTS / "check_readme.py")
check_readme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_readme)

MANIFEST = """// swift-tools-version: 6.0
import PackageDescription
let package = Package(name: "swift-example", platforms: [.iOS(.v15), .macOS(.v12)], products: [])
"""
SHIELDS = "https://img.shields.io/badge/"


class ReadmeCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "remote", "add", "origin",
                        "https://github.com/example-owner/swift-example.git"], check=True)
        (self.root / "Package.swift").write_text(MANIFEST)

    def tearDown(self):
        self.temporary.cleanup()

    def add_ci(self):
        workflows = self.root / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "ci.yml").write_text("jobs:\n  test:\n    runs-on: ubuntu-24.04\n")

    def add_license(self):
        (self.root / "LICENSE").write_text("Apache License\nVersion 2.0, January 2004\n")

    def badge_findings(self, *badges):
        readme = self.root / "README.md"
        readme.write_text("\n".join(f'<img src="{badge}" alt="badge">' for badge in badges) + "\n")
        findings = check_readme.check(self.root, readme, None, "auto")
        return [detail for category, _, detail in findings if category == "badge"]

    def test_badge_values_include_only_backed_kinds(self):
        values = check_readme.collect(self.root)["badges"]
        self.assertEqual(values, {"swift": "6.0+", "platforms": ["iOS 15+", "macOS 12+"]})
        self.add_ci()
        self.add_license()
        values = check_readme.collect(self.root)["badges"]
        self.assertEqual(values, {
            "ci": "ci.yml", "swift": "6.0+",
            "platforms": ["iOS 15+", "macOS 12+", "Linux"], "license": "Apache-2.0",
        })

    def test_styling_does_not_affect_values(self):
        self.add_ci()
        self.add_license()
        self.assertEqual(self.badge_findings(
            SHIELDS + "Swift-6.0%2B-F05138?style=flat",
            SHIELDS + "platforms-iOS%2015%2B%20%7C%20macOS%2012%2B%20%7C%20Linux-lightgrey?style=flat",
            SHIELDS + "license-Apache--2.0-0A84FF",
        ), [])

    def test_contradictory_values_are_reported(self):
        self.add_ci()
        self.add_license()
        findings = self.badge_findings(
            SHIELDS + "Swift-6.0--6.1-blue",
            SHIELDS + "Swift-6.0_or_earlier-blue",
            SHIELDS + "platforms-iOS%2015%2B%20%7C%20macOS%2012%2B-lightgrey",
            SHIELDS + "license-MIT-blue",
        )
        self.assertEqual(len(findings), 4, findings)

    def test_badge_without_backing_fact_is_reported(self):
        self.assertEqual(self.badge_findings(SHIELDS + "license-MIT-blue"),
                         ["license badge has no backing fact"])

    def test_shadowing_applies_to_the_checked_root_readme(self):
        (self.root / "README.md").write_text("# swift-example\n")
        surfaced = self.root / ".github" / "README.md"
        surfaced.parent.mkdir()
        surfaced.write_text("# swift-example\n")
        root_findings = check_readme.check(self.root, self.root / "README.md", None, "auto")
        self.assertIn("shadowed", [category for category, _, _ in root_findings])
        surfaced_findings = check_readme.check(self.root, surfaced, None, "auto")
        self.assertNotIn("shadowed", [category for category, _, _ in surfaced_findings])

    def test_readme_paths_resolve_against_the_repository(self):
        surfaced = self.root / ".github" / "README.md"
        surfaced.parent.mkdir()
        surfaced.write_text(
            "## Quick look\n\nRun the tool.\n\n## Install\n\n```swift\n"
            '.product(name: "Example", package: "swift-example"),\n```\n'
        )
        with tempfile.TemporaryDirectory() as elsewhere:
            checked = subprocess.run(
                [sys.executable, "-B", str(SCRIPTS / "check_readme.py"), str(self.root),
                 "--readme", ".github/README.md"],
                cwd=elsewhere, capture_output=True, text=True,
            )
            built = subprocess.run(
                [sys.executable, "-B", str(SCRIPTS / "quickstart_check.py"), str(self.root),
                 "--readme", ".github/README.md", "--section", "Quick look", "--local"],
                cwd=elsewhere, capture_output=True, text=True,
            )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertEqual(built.returncode, 2)
        self.assertIn('no ```swift block under "## Quick look"', built.stderr)

    def test_ci_badge_needs_its_workflow_but_is_not_required(self):
        self.add_ci()
        self.assertEqual(self.badge_findings(), [])
        missing = "https://github.com/example-owner/swift-example/actions/workflows/build.yml/badge.svg"
        self.assertEqual(self.badge_findings(missing), ["workflow build.yml not found"])


if __name__ == "__main__":
    unittest.main()
