#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Validate whole-collection plugin distribution for Claude Code and Codex."""

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
NAME = "swift-skills"
LICENSE = "Apache-2.0 WITH Swift-exception"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
IDENTITY = ("name", "version", "description", "author", "homepage", "repository",
            "license", "keywords")
PLUGIN_NAME = re.compile(r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?")
PLUGIN_STRINGS = ("version", "description", "homepage", "repository", "license")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_root_manifest(plugin):
    """Check a root plugin.json against the Agent Plugins 1.0.0 manifest schema."""
    require(isinstance(plugin, dict), "Root plugin must be a JSON object")
    name = plugin.get("name")
    author = plugin.get("author", {})
    keywords = plugin.get("keywords", [])
    extensions = plugin.get("extensions", {})
    require(plugin.get("$schema") == SCHEMA, "Root plugin must use the Agent Plugins 1.0.0 schema")
    require(isinstance(name, str) and len(name) <= 64 and PLUGIN_NAME.fullmatch(name),
            "Root plugin name is not a valid Agent Plugins name")
    require(set(plugin) <= {"$schema", "name", "author", "keywords", "extensions", *PLUGIN_STRINGS},
            "Root plugin has fields outside the Agent Plugins schema")
    require(all(isinstance(plugin[key], str) for key in PLUGIN_STRINGS if key in plugin),
            "Root plugin version, description, homepage, repository and license must be strings")
    require(isinstance(author, dict) and set(author) <= {"name", "email", "url"}
            and all(isinstance(value, str) for value in author.values()),
            "Root plugin author must hold only name, email and url strings")
    require(isinstance(keywords, list) and all(isinstance(value, str) for value in keywords),
            "Root plugin keywords must be a list of strings")
    require(isinstance(extensions, dict)
            and all(isinstance(value, dict) for value in extensions.values()),
            "Root plugin extensions must map each namespace to an object")
    require(isinstance(extensions.get("com.openai", {}).get("interface"), dict),
            "Root plugin must carry the Codex interface in extensions.com.openai")


def validate(root):
    def read(path):
        return json.loads((root / path).read_text())

    claude = read(".claude-plugin/plugin.json")
    marketplace = read(".claude-plugin/marketplace.json")
    plugin = read("plugin.json")
    validate_root_manifest(plugin)
    agents = read(".agents/plugins/marketplace.json")
    version = (root / "VERSION").read_text().strip()
    require(re.fullmatch(r"\d+\.\d+\.\d+", version), "Invalid plugin version")
    description = claude["description"]
    require(bool(description), "Missing plugin description")
    for manifest in (claude, plugin):
        require(manifest["name"] == NAME, "Unexpected plugin identity")
        require(manifest["version"] == version, "Plugin versions differ")
        require(manifest["description"] == description, "Plugin descriptions differ")
    require(claude["license"] == LICENSE, "Claude plugin license differs from LICENSE.txt")
    # Claude always discovers skills/ relative to the plugin root.
    require("skills" not in claude, "Claude must use default skills/ discovery")
    require({key: plugin[key] for key in IDENTITY if key in plugin} == claude,
            "Claude plugin must mirror the root plugin identity")
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
