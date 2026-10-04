#!/usr/bin/env python3
"""Derive README facts from a Swift package repository.

Usage:
  readme_facts.py REPO                 print facts as JSON
  readme_facts.py REPO --badges        print the centered badge block
  readme_facts.py REPO --install       print the SwiftPM dependency line
  readme_facts.py REPO --workflow FILE use FILE as the CI workflow
  readme_facts.py REPO --linux yes|no  override Linux detection

Facts come from the origin remote, git tags, Package.swift, LICENSE, and
.github/workflows; nothing is typed by hand.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse

PLATFORM_NAMES = {
    "iOS": "iOS", "macOS": "macOS", "tvOS": "tvOS", "watchOS": "watchOS",
    "visionOS": "visionOS", "macCatalyst": "Mac Catalyst", "driverKit": "DriverKit",
}
LINUX_MARKERS = re.compile(r"ubuntu-|runs-on:\s*\[?\s*linux|image:\s*swift:|container:\s*swift:|\"ubuntu", re.I)


def git(root: pathlib.Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def remote_slug(root):
    url = git(root, "remote", "get-url", "origin")
    match = re.search(r"github\.com[:/]+([^/]+)/(.+?)(?:\.git)?/?$", url)
    return (match.group(1), match.group(2)) if match else (None, None)


def default_branch(root):
    ref = git(root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    return ref.split("/", 1)[1] if ref else git(root, "branch", "--show-current") or None


def latest_tag(root):
    tags = git(root, "tag", "--list", "--sort=-v:refname").splitlines()
    tags = [t for t in tags if re.fullmatch(r"v?\d+\.\d+\.\d+", t)]
    return tags[0] if tags else None


def manifest(root):
    path = root / "Package.swift"
    if not path.exists():
        return None, None, []
    text = path.read_text()
    tools = re.search(r"swift-tools-version:\s*([\d.]+)", text)
    name = re.search(r"Package\(\s*name:\s*\"([^\"]+)\"", text)
    platforms = []
    block = re.search(r"platforms:\s*\[(.*?)\]", text, re.S)
    if block:
        for key, enum_version, string_version in re.findall(
                r"\.(\w+)\(\s*(?:\.v([\d_]+)|\"([\d.]+)\")", block.group(1)):
            if key in PLATFORM_NAMES:
                version = (enum_version or string_version).replace("_", ".")
                platforms.append(f"{PLATFORM_NAMES[key]} {version}+")
    return (tools.group(1) if tools else None), (name.group(1) if name else None), platforms


def workflows(root):
    folder = root / ".github" / "workflows"
    return sorted(p for p in folder.glob("*.y*ml")) if folder.exists() else []


def ci_workflow(root, override):
    names = [p.name for p in workflows(root)]
    if override:
        return override if override in names else None
    return next((n for n in ("ci.yml", "ci.yaml") if n in names), None)


def builds_on_linux(root, workflow):
    sources = sorted((root / ".github").glob("*.json"))
    if workflow:
        sources.append(root / ".github" / "workflows" / workflow)
    return any(LINUX_MARKERS.search(p.read_text(errors="ignore")) for p in sources if p.is_file())


def license_file(root):
    return next((p for p in (root / n for n in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"))
                 if p.exists()), None)


def license_id(root):
    path = license_file(root)
    if not path:
        return None
    text = path.read_text(errors="ignore")
    head = text[:4000]
    if "Apache License" in head:
        return "Apache-2.0 WITH Swift-exception" if "Runtime Library Exception" in text else "Apache-2.0"
    if "Mozilla Public License" in head and "2.0" in head:
        return "MPL-2.0"
    if "Permission is hereby granted, free of charge" in head:
        return "MIT"
    if "Redistribution and use in source and binary forms" in head:
        return "BSD-3-Clause" if "Neither the name" in head else "BSD-2-Clause"
    if "Permission to use, copy, modify, and/or distribute" in head:
        return "ISC"
    if "unlicense" in head.lower():
        return "Unlicense"
    return None


def requirement(tag):
    if not tag:
        return None
    version = tag.lstrip("v")
    if version.split(".")[0] == "0":
        return f'.upToNextMinor(from: "{version}")'
    return f'from: "{version}"'


def shield(label, message, color):
    def quote(s):
        return urllib.parse.quote(s.replace("-", "--").replace("_", "__"), safe="")
    return f"https://img.shields.io/badge/{quote(label)}-{quote(message)}-{color}"


def collect(root, override=None, linux="auto"):
    owner, name = remote_slug(root)
    tools, package_name, platforms = manifest(root)
    workflow = ci_workflow(root, override)
    linux = builds_on_linux(root, workflow) if linux == "auto" else linux == "yes"
    tag = latest_tag(root)
    return {
        "owner": owner,
        "name": name,
        "package_name": package_name,
        "default_branch": default_branch(root),
        "latest_tag": tag,
        "requirement": requirement(tag),
        "swift_tools": tools,
        "platforms": platforms + (["Linux"] if linux else []),
        "license": license_id(root),
        "license_file": license_file(root).name if license_file(root) else None,
        "ci_workflow": workflow,
    }


def badges(facts):
    base = f"https://github.com/{facts['owner']}/{facts['name']}"
    lines = []
    workflow = facts["ci_workflow"]
    if workflow:
        lines.append(f'  <a href="{base}/actions/workflows/{workflow}"><img src="{base}/actions/workflows/'
                     f'{workflow}/badge.svg?branch={facts["default_branch"]}" alt="CI"></a>')
    if facts["swift_tools"]:
        version = facts["swift_tools"]
        lines.append(f'  <img src="{shield("Swift", version + "+", "F05138")}" alt="Swift {version}+">')
    if facts["platforms"]:
        text = " | ".join(facts["platforms"])
        lines.append(f'  <img src="{shield("platforms", text, "lightgrey")}" alt="Platforms: {text}">')
    if facts["license"]:
        short = facts["license"].split(" WITH ")[0]
        lines.append(f'  <a href="{facts["license_file"]}"><img src="{shield("license", short, "blue")}" '
                     f'alt="License: {facts["license"]}"></a>')
    return '<p align="center">\n' + "\n".join(lines) + "\n</p>"


def install(facts):
    url = f"https://github.com/{facts['owner']}/{facts['name']}.git"
    if facts["requirement"]:
        return f'.package(url: "{url}", {facts["requirement"]}),'
    return f'.package(url: "{url}", branch: "{facts["default_branch"]}"),'


def main(argv):
    parser = argparse.ArgumentParser(description="Derive README facts from a Swift package repository.")
    parser.add_argument("repo", type=pathlib.Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--badges", action="store_true", help="print the badge block")
    mode.add_argument("--install", action="store_true", help="print the SwiftPM dependency line")
    parser.add_argument("--workflow", help="CI workflow file name under .github/workflows")
    parser.add_argument("--linux", choices=("auto", "yes", "no"), default="auto",
                        help="list Linux among platforms (auto: the CI workflow or .github/*.json names a Linux runner)")
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    facts = collect(root, args.workflow, args.linux)
    if (args.badges or args.install) and not (facts["owner"] and facts["name"]):
        sys.exit("error: origin is not a GitHub remote; cannot build URLs")
    if args.badges:
        print(badges(facts))
    elif args.install:
        print(install(facts))
    else:
        print(json.dumps(facts, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
