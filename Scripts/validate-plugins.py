#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Validate whole-collection plugin distribution for Claude Code and Codex."""

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
NAME = "swift-skills"
LICENSE = "Apache-2.0 WITH Swift-exception"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root):
    def read(path):
        return json.loads((root / path).read_text())

    claude = read(".claude-plugin/plugin.json")
    marketplace = read(".claude-plugin/marketplace.json")
    codex = read(".codex-plugin/plugin.json")
    agents = read(".agents/plugins/marketplace.json")
    version = (root / "VERSION").read_text().strip()
    require(re.fullmatch(r"\d+\.\d+\.\d+", version), "Invalid plugin version")
    description = claude["description"]
    require(bool(description), "Missing plugin description")
    for manifest in (claude, codex):
        require(manifest["name"] == NAME, "Unexpected plugin identity")
        require(manifest["version"] == version, "Plugin versions differ")
        require(manifest["description"] == description, "Plugin descriptions differ")
    require(claude["license"] == LICENSE, "Claude plugin license differs from LICENSE.txt")
    # Claude always discovers skills/ relative to the plugin root.
    require("skills" not in claude, "Claude must use default skills/ discovery")
    require(codex["skills"] == "./skills/", "Codex must expose the whole skills/ directory")
    require(marketplace["name"] == NAME, "Unexpected Claude marketplace identity")
    require(marketplace["metadata"]["version"] == version, "Marketplace version differs")
    require(marketplace["plugins"] == [{
        "name": NAME, "description": description, "source": "./",
    }], "Claude marketplace must publish one repository-root plugin")
    require(agents["name"] == NAME, "Unexpected Codex marketplace identity")
    require(agents["plugins"] == [{
        "name": NAME,
        "source": {
            "source": "url",
            "url": "https://github.com/swift-library/skills.git",
            "ref": "master",
        },
        "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
        "category": "Developer Tools",
    }], "Codex marketplace must publish one repository-root Git plugin")
    directories = sorted(path for path in (root / "skills").iterdir() if path.is_dir())
    require(bool(directories), "The collection has no skills")
    for path in directories:
        require((path / "SKILL.md").is_file(), f"Missing SKILL.md: {path.name}")
    return [path.name for path in directories]


if __name__ == "__main__":
    try:
        skills = validate(ROOT)
    except (KeyError, OSError, ValueError) as error:
        raise SystemExit(f"Plugin validation failed: {error}")
    print(f"Whole-collection plugins validated: {len(skills)} skill directories")
