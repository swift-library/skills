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
SWIFT_STRING = re.compile(r'"(?:\\.|[^"\\])*"', re.DOTALL)
PLATFORM_VERSION = re.compile(
    r"\.(?P<platform>iOS|macOS|tvOS|watchOS|visionOS)\s*\(\s*"
    r'(?:\.v(?P<version>\d+(?:_\d+)*)|"(?P<string>[^"\\\r\n]*)")\s*\)'
)


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


def strip_swift_comments(manifest: str) -> str:
    parts: list[str] = []
    index = 0
    while index < len(manifest):
        if manifest.startswith("//", index):
            end = manifest.find("\n", index)
            if end == -1:
                break
            parts.append("\n")
            index = end + 1
        elif manifest.startswith("/*", index):
            depth = 1
            index += 2
            while depth and index < len(manifest):
                if manifest.startswith("/*", index):
                    depth += 1
                    index += 2
                elif manifest.startswith("*/", index):
                    depth -= 1
                    index += 2
                else:
                    index += 1
            parts.append(" ")
        elif match := SWIFT_STRING.match(manifest, index):
            parts.append(match.group())
            index = match.end()
        else:
            parts.append(manifest[index])
            index += 1
    return "".join(parts)


def platform_expressions(manifest: str, manifest_path: Path) -> list[str]:
    platforms = re.search(r"\bplatforms\s*:\s*\[", manifest)
    if platforms is None:
        return []
    expressions: list[str] = []
    start = platforms.end()
    depth = 0
    tokens = re.compile(SWIFT_STRING.pattern + r"|[\[\](){},]", re.DOTALL)
    for token in tokens.finditer(manifest, start):
        value = token.group()
        if value == "]" and depth == 0:
            expression = manifest[start:token.start()].strip()
            if expression:
                expressions.append(expression)
            return expressions
        if value == "," and depth == 0:
            expressions.append(manifest[start:token.start()].strip())
            start = token.end()
        elif value in ("[", "(", "{"):
            depth += 1
        elif value in ("]", ")", "}"):
            depth -= 1
    raise ValueError(f"{manifest_path}: unterminated platforms array: {manifest[start:].strip()}")


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
    versions: list[str] = []
    for expression in platform_expressions(strip_swift_comments(manifest), manifest_path):
        match = PLATFORM_VERSION.fullmatch(expression)
        if match is None:
            raise ValueError(f"{manifest_path}: unsupported platform expression: {expression}")
        version = match.group("string")
        if version is None:
            version = match.group("version").replace("_", ".")
        versions.append(f"{match.group('platform')} {version}")
    if versions:
        requirement += "; " + ", ".join(versions)

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
    try:
        resolved_root = output_root.resolve()
    except (OSError, RuntimeError) as error:
        raise ValueError(f"{output_root}: cannot resolve output directory") from error
    for target, _ in outputs:
        destination = output_root / target
        for relative in (target, *target.parents):
            path = output_root / relative
            try:
                path.resolve().relative_to(resolved_root)
            except (OSError, RuntimeError, ValueError) as error:
                raise ValueError(f"{path}: must resolve inside output directory {output_root}") from error
            if relative != target and path.exists() and not path.is_dir():
                raise ValueError(f"{path}: destination parent must be a directory")
        if destination.is_symlink() or (destination.exists() and not destination.is_file()):
            raise ValueError(f"{destination}: destination must be a regular file, not a symlink")
        if not force and destination.exists():
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
