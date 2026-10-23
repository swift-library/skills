# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Skill validation against isolated collection fixtures."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parent.parent / "scripts/validate-skills.py"
spec = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class SkillValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill("alpha")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def skill(self, name, description="A focused task.", body=""):
        return self.write(f"skills/{name}/SKILL.md",
                          f"---\nname: {name}\ndescription: {description}\n---\n{body}")

    def findings(self):
        return [item.format(self.root) for item in validator.validate(self.root)[0]]

    def test_valid_plain_and_quoted_scalars_and_known_keys(self):
        self.skill("bravo", "'Swift''s tests.'")
        self.skill("charlie", json.dumps('Swift "quoted" text.'))
        extra = "".join(f"{key}: 'value'\n" for key in sorted(
            validator.FRONTMATTER_KEYS - {"name", "description"}))
        self.write("skills/alpha/SKILL.md", f"---\nname: alpha\ndescription: Text.\n{extra}---\n")
        self.assertEqual(self.findings(), [])

    def test_frontmatter_diagnostics_locate_invalid_contracts(self):
        cases = [
            ("# Alpha\n", 1, "must start"),
            ("---\nname: alpha\n", 1, "closing"),
            ("---\ndescription: Text.\n---\n", 1, "requires name"),
            ("---\nname: alpha\n---\n", 1, "requires description"),
            ("---\nname: beta\ndescription: Text.\n---\n", 2, "must equal"),
            ("---\nname: Alpha_bad\ndescription: Text.\n---\n", 2, "must match"),
            ("---\nname: alpha\ndescription: ''\n---\n", 3, "1–1,024"),
            ("---\nname: alpha\ndescription: Text.\nunknown: yes\n---\n", 4, "unknown"),
            ("---\nname: alpha\nname: alpha\ndescription: Text.\n---\n", 3, "duplicate"),
            ("---\nname: alpha\ndescription: |\n  Text.\n---\n", 3, "unsupported YAML"),
            ("---\nname: alpha\ndescription: Text.\nmetadata:\n  nested: value\n---\n", 5, "unsupported frontmatter"),
        ]
        for content, line, message in cases:
            with self.subTest(content=content):
                self.write("skills/alpha/SKILL.md", content)
                self.assertTrue(any(f"SKILL.md:{line}:" in f and message in f for f in self.findings()))

    def test_unsupported_scalars_fail_without_guessing(self):
        for value in ('[one, two]', '{a: b}', '> folded', '*alias', '&anchor text',
                      '!tag text', 'text # comment', '"unterminated', "'bad'quote'", '"line\\nline"'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validator.scalar(value)

    def test_character_limits_count_decoded_characters(self):
        self.skill("a" * 64, json.dumps("界" * 1024))
        self.assertEqual(self.findings(), [])
        self.skill("a" * 65, "x" * 1025)
        messages = self.findings()
        self.assertTrue(any("64 characters" in f for f in messages))
        self.assertTrue(any("found 1025" in f for f in messages))

    def test_missing_skill_file(self):
        (self.root / "skills/alpha/SKILL.md").unlink()
        self.assertIn("skills/alpha/SKILL.md:1: missing SKILL.md", self.findings())

    def test_metadata_prompt_and_icons(self):
        self.write("skills/alpha/assets/icon.svg", "<svg/>")
        self.write("skills/alpha/agents/openai.yaml", "interface:\n  default_prompt: 'Use $alpha.'\n  icon_small: './assets/icon.svg'\n")
        self.assertEqual(self.findings(), [])
        self.write("skills/alpha/agents/openai.yaml", "interface:\n  default_prompt: 'Use $alpha-extra.'\n  icon_large: './missing.png'\n")
        messages = self.findings()
        self.assertTrue(any("openai.yaml:2:" in f and "$alpha" in f for f in messages))
        self.assertTrue(any("openai.yaml:3:" in f and "missing.png" in f for f in messages))

    def test_metadata_missing_prompt_and_unsupported_scalar(self):
        self.write("skills/alpha/agents/openai.yaml", "interface:\n  icon_small: |\n    icon.svg\n")
        messages = self.findings()
        self.assertTrue(any("openai.yaml:1:" in f and "default_prompt" in f for f in messages))
        self.assertTrue(any("openai.yaml:2:" in f and "unsupported" in f for f in messages))

    def test_relative_links_in_every_document_scope(self):
        self.write("docs/reference/a (b).md", "# Reference\n")
        self.write("README.md", '[A](docs/reference/a%20(b).md#part "title")\n[A][ref]\n[ref]: <docs/reference/a (b).md>\n')
        self.write("AGENTS.md", "[A](docs/reference/a%20\\(b\\).md)\n")
        self.write("docs/README.md", "[Home](../README.md)\n")
        self.write("skills/alpha/references/notes.md", "[Manual](../../../README.md)\n")
        self.assertEqual(self.findings(), [])
        for file in ("README.md", "AGENTS.md", "docs/README.md", "skills/alpha/references/notes.md"):
            with self.subTest(file=file):
                path = self.root / file
                path.write_text(path.read_text() + "![missing](absent.png)\n")
                self.assertTrue(any(f.startswith(file + ":") and "absent.png" in f for f in self.findings()))

    def test_reference_definitions_are_checked_and_code_and_urls_ignored(self):
        self.write("README.md", """[web](https://example.com/missing)
[mail](mailto:a@example.com)
[local](#anchor)
[remote](//example.com/file)
`[sample](missing.md)`
```md
[sample](missing.md)
```
~~~md
[sample](missing.md)
~~~
""")
        self.assertEqual(self.findings(), [])
        with (self.root / "README.md").open("a") as output:
            output.write("[broken]: missing.md\n")
        self.assertTrue(any("README.md:12:" in f and "missing.md" in f for f in self.findings()))

    def test_multiline_labels_and_nested_image_links(self):
        self.write("image.svg", "<svg/>")
        self.write("README.md", "[a multiline\nlabel](missing.md)\n[![image](image.svg)](another.md)\n")
        messages = self.findings()
        self.assertEqual(len(messages), 2)
        self.assertTrue(any("README.md:2:" in f and "missing.md" in f for f in messages))
        self.assertTrue(any("README.md:3:" in f and "another.md" in f for f in messages))

    def test_dependency_cycles_include_resource_edges(self):
        self.skill("alpha", body="`bravo` and `alpha` and `external`.\n")
        self.skill("bravo", body="`charlie`.\n")
        self.skill("charlie")
        self.assertEqual(self.findings(), [])
        self.write("skills/charlie/references/notes.md", "# Notes\n`alpha`\n")
        cycle = next(f for f in self.findings() if "reference cycle" in f)
        self.assertIn("notes.md:2:", cycle)
        self.assertIn("alpha -> bravo -> charlie -> alpha", cycle)
        self.write("skills/charlie/references/notes.md", "Boundary by responsibility.\n")
        self.write("skills/charlie/scripts/check.py", "# `alpha`\n")
        self.assertTrue(any("check.py:1:" in f and "reference cycle" in f for f in self.findings()))

    def test_organization_names_and_product_exceptions(self):
        for organization in ("swift-library", "agents-tools", "skill-cli", "showxu"):
            with self.subTest(organization=organization):
                self.write("skills/alpha/references/source.md", f"# Source\n{organization}\n")
                self.assertTrue(any("source.md:2:" in f and organization in f for f in self.findings()))
        (self.root / "skills/alpha/references/source.md").unlink()
        for name in ("swift-interface-distiller-patterns", "swift-sh-patterns", "swift-data-writable-patterns"):
            self.skill(name, body="https://github.com/swift-library/product\n")
            self.assertTrue(validator.ORGANIZATION_ALLOWLIST[name][2])
        self.assertEqual(self.findings(), [])

    def test_cli_identity_exception_is_limited_to_user_agent(self):
        self.skill("swiftpm-index")
        path = "skills/swiftpm-index/cli/swiftpm-index"
        header = 'USER_AGENT = f"{NAME}/0.1 (+https://github.com/swift-library/skills)"\n'
        self.write(path, header)
        self.assertEqual(self.findings(), [])
        self.write(path, header + '# swift-library policy\n')
        self.assertTrue(any("swiftpm-index:2:" in f and "organization name" in f for f in self.findings()))
        self.write(path, header)
        self.write("skills/swiftpm-index/references/source.md", header)
        self.assertTrue(any("source.md:1:" in f and "organization name" in f for f in self.findings()))

    def test_listing_totals_floors_order_and_greedy_fit(self):
        rows = validator.listing_report([("bravo", "BB"), ("alpha", "A")], {"fixture": (10, "")})
        # '- alpha: A' is 10 chars; '- bravo: BB' is 11; one newline joins them.
        self.assertEqual(rows, [("fixture", 22, 15, 1, 10)])
        rows = validator.listing_report([("alpha", "x" * 20), ("bravo", "B")], {"fixture": (10, "")})
        self.assertEqual(rows[0][3], 1)
        rows = validator.listing_report([("alpha", "A")], {"claude": (40, "swift-skills:")})
        self.assertEqual(rows[0][1:4], (23, 20, 1))

    def test_listing_budgets_report_only_or_enforced(self):
        with patch.object(validator, "SCENARIOS", {"fixture": (1, "")}):
            self.assertEqual(self.findings(), [])
            with patch.object(validator, "ENFORCED_SCENARIOS", {"fixture"}):
                self.assertTrue(any("validate-skills.py:" in f and "exceeds budget" in f for f in self.findings()))
        with patch.object(validator, "SCENARIOS", {"fixture": (1000, "")}), patch.object(validator, "ENFORCED_SCENARIOS", {"fixture"}):
            self.assertEqual(self.findings(), [])

    def test_cli_status_and_listing_assumptions(self):
        command = [sys.executable, "-B", str(SCRIPT), "--root", str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("4 characters/token", result.stdout)
        self.assertIn("report only", result.stdout)
        self.assertIn("Claude 200k context", result.stdout)
        self.skill("alpha", "''")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("skills/alpha/SKILL.md:3:", result.stdout)


if __name__ == "__main__":
    unittest.main()
