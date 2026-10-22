# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Shared profile output maps, package facts, and file exports."""

from __future__ import annotations

import json
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = SKILL_ROOT / "templates"
PROFILE_NAMES = ("minimal", "standard")
OUTPUT_ROW = re.compile(
    r"^\|\s*`(?P<target>[^`]+)`\s*\|\s*`(?P<source>[^`]+)`\s*\|"
    r"\s*(?P<required>yes|when not inherited)\s*\|$"
)
PLACEHOLDER = re.compile(r"<([a-z0-9-]+)>")


def output_map(
    profile_path: Path, *, inherited_paths: set[Path]
) -> list[tuple[Path, Path]]:
    rows: list[tuple[Path, Path]] = []
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        match = OUTPUT_ROW.match(line)
        if match is None:
            continue
        target = Path(match.group("target"))
        source = (profile_path.parent / match.group("source")).resolve()
        if target.is_absolute() or ".." in target.parts:
            raise ValueError(f"{profile_path}: unsafe target path {target}")
        try:
            source.relative_to(TEMPLATES_ROOT)
        except ValueError as error:
            raise ValueError(f"{profile_path}: template escapes templates/: {source}") from error
        if not source.is_file():
            raise FileNotFoundError(f"{profile_path}: missing template {source}")
        if match.group("required") == "when not inherited" and target in inherited_paths:
            continue
        rows.append((target, source))
    if not rows:
        raise ValueError(f"{profile_path}: no required output map rows")
    if len({target for target, _ in rows}) != len(rows):
        raise ValueError(f"{profile_path}: duplicate target path")
    return rows


def read_utf8(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeError as error:
        raise ValueError(f"{path}: {error}") from error


def package_facts(package_root: Path) -> dict[str, str]:
    manifest_path = package_root / "Package.swift"
    manifest = read_utf8(manifest_path)
    tools_version = re.search(
        r"^\s*//\s*swift-tools-version:\s*(\d+\.\d+)(?:\.\d+)?\s*$",
        manifest, re.MULTILINE,
    )
    if tools_version is None:
        raise ValueError(f"{manifest_path}: unreadable swift-tools-version")
    requirement = f"Swift {tools_version.group(1)} or later"
    platforms = re.search(r"\bplatforms\s*:\s*\[(.*?)\]", manifest, re.DOTALL)
    if platforms is not None:
        versions = re.findall(
            r"\.(iOS|macOS|tvOS|watchOS|visionOS)\s*\(\s*\.v(\d+(?:_\d+)*)\s*\)",
            platforms.group(1),
        )
        if versions:
            requirement += "; " + ", ".join(
                f"{platform} {version.replace('_', '.')}" for platform, version in versions
            )

    test_command = "swift test"
    release_path = package_root / ".github/release.json"
    if release_path.exists():
        try:
            release = json.loads(read_utf8(release_path))
        except json.JSONDecodeError as error:
            raise ValueError(f"{release_path}: {error}") from error
        if not isinstance(release, dict):
            raise ValueError(f"{release_path}: expected an object")
        test_command = release.get("check_command", test_command)
        if not isinstance(test_command, str):
            raise ValueError(f"{release_path}: check_command must be a string")
    return {
        "build-command": "swift build",
        "test-command": test_command,
        "requirement": requirement,
    }


def export_files(
    outputs: list[tuple[Path, Path]], output_root: Path, *,
    replacements: dict[str, str] | None = None, force: bool = True,
) -> list[Path]:
    if not force:
        for target, _ in outputs:
            destination = output_root / target
            if destination.exists() or destination.is_symlink():
                raise FileExistsError(f"{destination}: already exists; use --force to overwrite")
    written: list[Path] = []
    for target, source in outputs:
        destination = output_root / target
        if replacements:
            text = PLACEHOLDER.sub(
                lambda match: replacements.get(match.group(1), match.group(0)),
                read_utf8(source),
            )
            content = text.encode("utf-8")
        else:
            content = source.read_bytes()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        written.append(destination)
    return written
