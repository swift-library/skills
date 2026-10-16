# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Profile exports respect the repository's community-file inheritance decision."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/swiftpm-docs"
spec = importlib.util.spec_from_file_location(
    "template_exports", SKILL / "scripts/validate_template_exports.py"
)
exports = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exports)

COMMUNITY_FILES = {
    Path(name) for name in (
        "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
        ".github/ISSUE_TEMPLATE/bug.md", ".github/ISSUE_TEMPLATE/feature.md",
        ".github/ISSUE_TEMPLATE/config.yml", ".github/pull_request_template.md",
    )
}


class TemplateExportTests(unittest.TestCase):
    def exported_files(self, profile, inherited_paths):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            exports.export_profile(
                SKILL / "profiles" / f"{profile}.md", root,
                inherited_paths=inherited_paths,
            )
            return {
                path.relative_to(root): path.read_text()
                for path in root.rglob("*") if path.is_file()
            }

    def test_absent_inheritance_decision_emits_no_community_files(self):
        for profile in ("minimal", "standard"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with self.assertRaisesRegex(TypeError, "required.*inherited_paths"):
                    exports.export_profile(SKILL / "profiles" / f"{profile}.md", root)
                self.assertFalse(any((root / path).exists() for path in COMMUNITY_FILES))

    def test_local_community_files_and_issue_chooser_are_exported(self):
        minimal = self.exported_files("minimal", set())
        self.assertEqual(set(minimal) & COMMUNITY_FILES, {Path("CONTRIBUTING.md")})
        standard = self.exported_files("standard", set())
        self.assertTrue(COMMUNITY_FILES <= set(standard))
        self.assertEqual(
            {path.name for path in standard if path.parent == Path(".github/ISSUE_TEMPLATE")},
            {"bug.md", "feature.md", "config.yml"},
        )
        self.assertEqual(
            standard[Path(".github/ISSUE_TEMPLATE/config.yml")].strip(),
            "blank_issues_enabled: true",
        )

    def test_inherited_community_files_are_omitted(self):
        for profile in ("minimal", "standard"):
            with self.subTest(profile=profile):
                files = self.exported_files(profile, COMMUNITY_FILES)
                self.assertFalse(set(files) & COMMUNITY_FILES)
                self.assertIn(Path("AGENTS.md"), files)
                self.assertIn(Path("README.md"), files)
                self.assertIn(Path("Documentation/Architecture/VersioningAndRelease.md"), files)
                if profile == "standard":
                    for name in ("LICENSE", "GOVERNANCE.md", ".github/CODEOWNERS"):
                        self.assertIn(Path(name), files)

    def test_mixed_inheritance_preserves_local_community_files(self):
        inherited = {Path("CONTRIBUTING.md"), Path("SECURITY.md")}
        files = self.exported_files("standard", inherited)
        self.assertEqual(set(files) & COMMUNITY_FILES, COMMUNITY_FILES - inherited)


if __name__ == "__main__":
    unittest.main()
