# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Distribution regressions that could hide skills or change installation identity."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("plugins", ROOT / "Scripts/validate-plugins.py")
plugins = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugins)


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for path in ("VERSION", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
                     ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json"):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / path).read_bytes())
        self.add_skill("first")

    def add_skill(self, name):
        path = self.root / "skills" / name
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Test skill.\n---\n")

    def change(self, path, update):
        target = self.root / path
        manifest = json.loads(target.read_text())
        update(manifest)
        target.write_text(json.dumps(manifest))

    def test_published_manifests(self):
        self.assertEqual(plugins.validate(ROOT), sorted(
            path.name for path in (ROOT / "skills").iterdir() if path.is_dir()))

    def test_new_skill_is_included_without_a_marketplace_entry(self):
        self.add_skill("second")
        self.assertEqual(plugins.validate(self.root), ["first", "second"])

    def test_claude_cannot_publish_skill_roots(self):
        self.change(".claude-plugin/marketplace.json",
                    lambda m: m["plugins"][0].update(source="./skills/first"))
        with self.assertRaisesRegex(ValueError, "one repository-root plugin"):
            plugins.validate(self.root)

    def test_claude_cannot_publish_multiple_plugins(self):
        self.change(".claude-plugin/marketplace.json",
                    lambda m: m["plugins"].append(dict(m["plugins"][0], name="first")))
        with self.assertRaisesRegex(ValueError, "one repository-root plugin"):
            plugins.validate(self.root)

    def test_codex_cannot_install_a_different_revision_or_subdirectory(self):
        self.change(".agents/plugins/marketplace.json",
                    lambda m: m["plugins"][0]["source"].update(ref="other", path="skills/first"))
        with self.assertRaisesRegex(ValueError, "repository-root Git plugin"):
            plugins.validate(self.root)

    def test_codex_cannot_expose_a_subset(self):
        self.change(".codex-plugin/plugin.json", lambda m: m.update(skills="./skills/first/"))
        with self.assertRaisesRegex(ValueError, "whole skills/"):
            plugins.validate(self.root)

    def test_versions_stay_in_sync(self):
        for path in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
                     ".claude-plugin/marketplace.json"):
            with self.subTest(path=path):
                target = self.root / path
                original = target.read_text()
                self.change(path, lambda m: (m["metadata"] if "metadata" in m else m).update(version="99.0.0"))
                with self.assertRaisesRegex(ValueError, "version"):
                    plugins.validate(self.root)
                target.write_text(original)

    def test_version_file_is_the_source(self):
        (self.root / "VERSION").write_text("99.0.0\n")
        with self.assertRaisesRegex(ValueError, "version"):
            plugins.validate(self.root)

    def test_version_file_must_be_valid(self):
        (self.root / "VERSION").write_text("1.0\n")
        with self.assertRaisesRegex(ValueError, "Invalid plugin version"):
            plugins.validate(self.root)

    def test_license_keeps_swift_exception(self):
        self.change(".claude-plugin/plugin.json", lambda m: m.update(license="Apache-2.0"))
        with self.assertRaisesRegex(ValueError, "license"):
            plugins.validate(self.root)

    def test_incomplete_skill_directory_is_reported(self):
        (self.root / "skills" / "unfinished").mkdir()
        with self.assertRaisesRegex(ValueError, "Missing SKILL.md: unfinished"):
            plugins.validate(self.root)


if __name__ == "__main__":
    unittest.main()
