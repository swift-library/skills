# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Profile exports respect the repository's community-file inheritance decision."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/swiftpm-docs"
sys.path.insert(0, str(SKILL / "scripts"))
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
    def exported_files(self, profile, inherited_paths, modules=frozenset()):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            exports.export_profile(
                SKILL / "profiles" / f"{profile}.md", root,
                inherited_paths=inherited_paths, modules=modules,
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
                self.assertIn(Path("Documentation/Reference/Release.md"), files)
                self.assertNotIn(Path("Documentation/Architecture/VersioningAndRelease.md"), files)
                if profile == "standard":
                    for name in ("LICENSE", "GOVERNANCE.md", ".github/CODEOWNERS"):
                        self.assertIn(Path(name), files)

    def test_mixed_inheritance_preserves_local_community_files(self):
        inherited = {Path("CONTRIBUTING.md"), Path("SECURITY.md")}
        files = self.exported_files("standard", inherited)
        self.assertEqual(set(files) & COMMUNITY_FILES, COMMUNITY_FILES - inherited)

    def test_module_selection_preserves_inheritance_in_both_profiles(self):
        for profile in ("minimal", "standard"):
            for modules in (frozenset(), frozenset({"canonical-artifacts"})):
                with self.subTest(profile=profile, modules=modules):
                    files = self.exported_files(profile, COMMUNITY_FILES, modules)
                    self.assertFalse(set(files) & COMMUNITY_FILES)
                    self.assertEqual(
                        "## Canonical Artifacts" in files[Path("AGENTS.md")], bool(modules),
                    )

    def test_validator_rejects_missing_or_unrequested_contract(self):
        selected = frozenset({"canonical-artifacts"})
        guide = self.exported_files("minimal", set(), selected)[Path("AGENTS.md")]
        with self.assertRaisesRegex(ValueError, "unrequested"):
            exports.validate_agent_guide(guide, "minimal")
        for incomplete in ("## Canonical Artifacts\n", guide.replace("editing input", "input")):
            with self.subTest(guide=incomplete[:40]), self.assertRaises(ValueError):
                exports.validate_agent_guide(incomplete, "minimal", modules=selected)
        exports.validate_agent_guide(guide, "minimal", modules=selected)

    def target_validation(self, root, *args, expected=0):
        result = subprocess.run(
            [sys.executable, "-B", str(SKILL / "scripts/validate_canonical_target.py"),
             str(root), *args], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_target_validator_applies_only_to_adopted_or_required_module(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            exports.export_profile(SKILL / "profiles/minimal.md", root, inherited_paths=set())
            (root / "README.md").write_text("JSON-only export\n")
            self.assertIn("not applicable", self.target_validation(root))
            self.assertIn(
                "requested Canonical Artifacts section",
                self.target_validation(root, "--module", "canonical-artifacts", expected=1),
            )
            exports.export_profile(
                SKILL / "profiles/minimal.md", root, inherited_paths=set(),
                modules=frozenset({"canonical-artifacts"}),
            )
            self.assertIn("validation passed", self.target_validation(root))
            self.assertIn(
                "validation passed", self.target_validation(root, "--module", "canonical-artifacts"),
            )
            (root / "README.md").write_text("JSON-only export\n")
            self.assertIn("correction-shaped active prose", self.target_validation(root, expected=1))

    def test_target_validator_rejects_incomplete_module_and_review_rules(self):
        selected = frozenset({"canonical-artifacts"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = self.exported_files("minimal", set(), selected)
            guide = files[Path("AGENTS.md")]
            for text, message in (
                (guide.replace("editing input", "input"), "misses editing input"),
                (guide.replace("## Code Review Rules", "## Reviews"), "Code Review Rules section"),
                (guide + "x" * (32 * 1024), "agents read at most"),
            ):
                with self.subTest(message=message):
                    (root / "AGENTS.md").write_text(text)
                    self.assertIn(message, self.target_validation(root, expected=1))


if __name__ == "__main__":
    unittest.main()
