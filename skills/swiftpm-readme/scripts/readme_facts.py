#!/usr/bin/env python3
"""Derive README facts from a Swift package repository.

Usage:
  readme_facts.py REPO                 print facts and badge values as JSON
  readme_facts.py REPO --install       print the SwiftPM dependency line
  readme_facts.py REPO --workflow FILE use FILE as the CI workflow
  readme_facts.py REPO --linux yes|no  override Linux detection

Facts come from the origin's published refs, Package.swift, LICENSE, and
.github/workflows. Unknown remote facts are JSON null; an empty published_tags
list means the remote was read and has no tags. --install fails when publication
facts are unknown. Local branches and tags are not publication evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

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


def remote_output(root, *args):
    """Read published refs without prompting; None means the remote is unknown."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "ls-remote", *args, "origin", *(["HEAD"] if "--symref" in args else [])],
            text=True, stderr=subprocess.DEVNULL, timeout=30,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None


def default_branch(root):
    output = remote_output(root, "--symref")
    match = re.search(r"^ref: refs/heads/(.+)\tHEAD$", output or "", re.M)
    return match.group(1) if match else None


def published_refs(root, kind):
    output = remote_output(root, "--" + kind)
    if output is None:
        return None
    prefix = "refs/" + kind + "/"
    return sorted({ref[len(prefix):].removesuffix("^{}")
                   for line in output.splitlines()
                   for _, ref in [line.split("\t", 1)] if ref.startswith(prefix)})


def newest_version(tags):
    versions = [t for t in tags or [] if re.fullmatch(r"v?\d+\.\d+\.\d+", t)]
    return max(versions, key=lambda t: (tuple(map(int, t.lstrip("v").split("."))), t)) if versions else None


def latest_tag(root):
    return newest_version(published_refs(root, "tags"))


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


def collect(root, override=None, linux="auto"):
    owner, name = remote_slug(root)
    tools, package_name, platforms = manifest(root)
    workflow = ci_workflow(root, override)
    linux = builds_on_linux(root, workflow) if linux == "auto" else linux == "yes"
    tags = published_refs(root, "tags")
    tag = newest_version(tags)
    facts = {
        "owner": owner,
        "name": name,
        "package_name": package_name,
        "default_branch": default_branch(root),
        "latest_tag": tag,
        "published_tags": tags,
        "requirement": requirement(tag),
        "swift_tools": tools,
        "platforms": platforms + (["Linux"] if linux else []),
        "license": license_id(root),
        "license_file": license_file(root).name if license_file(root) else None,
        "ci_workflow": workflow,
    }
    facts["badges"] = badge_values(facts)
    return facts


def badge_values(facts):
    """Badge values keyed by kind; a kind appears only when a repository fact backs it."""
    values = {}
    if facts["ci_workflow"]:
        values["ci"] = facts["ci_workflow"]
    if facts["swift_tools"]:
        values["swift"] = facts["swift_tools"] + "+"
    if facts["platforms"]:
        values["platforms"] = facts["platforms"]
    if facts["license"]:
        values["license"] = facts["license"]
    return values


def install(facts):
    if facts["published_tags"] is None:
        raise ValueError("published tags are unknown; cannot derive an install requirement")
    if not facts["requirement"] and not facts["default_branch"]:
        raise ValueError("published default branch is unknown; cannot derive an install requirement")
    url = f"https://github.com/{facts['owner']}/{facts['name']}.git"
    if facts["requirement"]:
        return f'.package(url: "{url}", {facts["requirement"]}),'
    return f'.package(url: "{url}", branch: "{facts["default_branch"]}"),'


def main(argv):
    parser = argparse.ArgumentParser(description="Derive README facts from a Swift package repository.")
    parser.add_argument("repo", type=pathlib.Path)
    parser.add_argument("--install", action="store_true", help="print the SwiftPM dependency line")
    parser.add_argument("--workflow", help="CI workflow file name under .github/workflows")
    parser.add_argument("--linux", choices=("auto", "yes", "no"), default="auto",
                        help="list Linux among platforms (auto: the CI workflow or .github/*.json names a Linux runner)")
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    facts = collect(root, args.workflow, args.linux)
    if args.install and not (facts["owner"] and facts["name"]):
        sys.exit("error: origin is not a GitHub remote; cannot build URLs")
    if args.install:
        try:
            print(install(facts))
        except ValueError as error:
            sys.exit(f"error: {error}")
    else:
        print(json.dumps(facts, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
