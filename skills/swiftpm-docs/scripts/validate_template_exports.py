#!/usr/bin/env python3
"""Smoke-test profile exports and the generated Agent Guide contract."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = SKILL_ROOT / "templates"
PROFILE_NAMES = ("minimal", "standard")
OUTPUT_ROW = re.compile(
    r"^\|\s*`(?P<target>[^`]+)`\s*\|\s*`(?P<source>[^`]+)`\s*\|\s*yes\s*\|$"
)


def output_map(profile_path: Path) -> list[tuple[Path, Path]]:
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
        rows.append((target, source))
    if not rows:
        raise ValueError(f"{profile_path}: no required output map rows")
    if len({target for target, _ in rows}) != len(rows):
        raise ValueError(f"{profile_path}: duplicate target path")
    return rows


def validate_agent_guide(text: str, profile_name: str) -> None:
    normalized = " ".join(text.split())
    checks = {
        "editing input": "editing input" in normalized,
        "path independence": "not on the editing path" in normalized,
        "A+B normalization": "`A + B`" in normalized and "AWithoutB" in normalized,
        "current-invariant exceptions": all(
            term in normalized for term in ("compatibility", "safety", "ownership")
        ),
        "durable history boundary": (
            "Do not create a history artifact merely" in normalized
        ),
        "semantic-role normalization": (
            "semantic identity and artifact role" in normalized
            and "does not invalidate a distinct historical fact" in normalized
        ),
        "role-owned fact preservation": (
            "Preserve role-owned facts unless separate evidence changes them"
            in normalized
        ),
        "unchanged role-owned artifacts": (
            "Leave an already-correct history" in normalized
            and "Do not polish or restate it" in normalized
        ),
        "disabled-state boundary": (
            "disabled state alone is not an invariant" in normalized
        ),
        "cold-start acceptance": (
            "no editing conversation" in normalized
            and "mentally subtracting" in normalized
        ),
        "active-surface coverage": all(
            term in normalized
            for term in (
                "configuration",
                "schemas",
                "generated sources",
                "scripts",
                "templates",
                "tests",
                "fixtures",
                "normative docs",
            )
        ),
    }
    missing = [name for name, passed in checks.items() if not passed]
    if missing:
        raise ValueError(
            f"{profile_name} exported AGENTS.md misses: {', '.join(missing)}"
        )


def validate_release_policy(root: Path, profile_name: str) -> None:
    policy = root / "Documentation/Architecture/VersioningAndRelease.md"
    if not policy.is_file():
        raise FileNotFoundError(f"{profile_name}: version/release policy was not exported")
    text = policy.read_text(encoding="utf-8")
    for heading in (
        "Components and Version Authority", "Dependencies and Verified Combinations",
        "Derived Metadata and Drift Checks", "Candidate, Acceptance and Publication",
        "Evidence Reuse and Invalidation", "Entry Points and Artifact Retention",
    ):
        if f"## {heading}" not in text:
            raise ValueError(f"{profile_name}: missing policy section {heading}")
    routes = {
        root / "AGENTS.md": "Documentation/Architecture/VersioningAndRelease.md",
        root / "Documentation/README.md": "Architecture/VersioningAndRelease.md",
        root / "Documentation/Architecture/README.md": "VersioningAndRelease.md",
    }
    for path, route in routes.items():
        if route not in path.read_text(encoding="utf-8"):
            raise ValueError(f"{profile_name}: {path.name} does not route to {route}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="docs-template-export-") as temporary:
        export_root = Path(temporary)
        for profile_name in PROFILE_NAMES:
            profile_path = SKILL_ROOT / "profiles" / f"{profile_name}.md"
            profile_root = export_root / profile_name
            for target, source in output_map(profile_path):
                destination = profile_root / target
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())
            agent_guide = profile_root / "AGENTS.md"
            if not agent_guide.is_file():
                raise FileNotFoundError(f"{profile_name}: AGENTS.md was not exported")
            validate_agent_guide(agent_guide.read_text(encoding="utf-8"), profile_name)
            validate_release_policy(profile_root, profile_name)
            print(f"{profile_name}: template export passed")


if __name__ == "__main__":
    main()
