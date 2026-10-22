#!/usr/bin/env python3
"""Smoke-test profile exports and the generated Agent Guide contract."""

from __future__ import annotations

import tempfile
from pathlib import Path

from profile_export import PROFILE_NAMES, SKILL_ROOT, export_files, output_map


def review_rule_groups(text: str) -> int | None:
    """Count `###` groups in the Code Review Rules section, or None when absent."""
    lines = text.splitlines()
    if "## Code Review Rules" not in lines:
        return None
    groups = 0
    for line in lines[lines.index("## Code Review Rules") + 1 :]:
        if line.startswith("## "):
            break
        groups += line.startswith("### ")
    return groups


def validate_review_rules(text: str, profile_name: str) -> None:
    groups = review_rule_groups(text)
    if groups is None:
        raise ValueError(f"{profile_name} exported AGENTS.md has no Code Review Rules section")
    if groups == 0:
        raise ValueError(f"{profile_name} exported AGENTS.md Code Review Rules has no ### group")


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


def validate_release_reference(root: Path, profile_name: str) -> None:
    reference = root / "Documentation/Reference/Release.md"
    if not reference.is_file():
        raise FileNotFoundError(f"{profile_name}: release reference was not exported")
    text = reference.read_text(encoding="utf-8")
    for heading in (
        "Components and Version Sources", "Compatibility Surface",
        "Dependencies and Verified Combinations", "Derived Metadata and Drift Checks",
        "Candidate, Acceptance and Publication", "Evidence Reuse and Invalidation",
        "Entry Points and Artifact Retention",
    ):
        if f"## {heading}" not in text:
            raise ValueError(f"{profile_name}: missing release section {heading}")
    routes = {
        root / "AGENTS.md": ("Documentation/Reference/Release.md", "VERSIONING"),
        root / "Documentation/README.md": ("Reference/Release.md",),
    }
    reference_index = root / "Documentation/Reference/README.md"
    if reference_index.is_file():
        routes[reference_index] = ("Release.md",)
    for path, required_routes in routes.items():
        for route in required_routes:
            if route not in path.read_text(encoding="utf-8"):
                raise ValueError(f"{profile_name}: {path.name} does not route to {route}")
    if (root / "Documentation/Architecture/VersioningAndRelease.md").exists():
        raise ValueError(f"{profile_name}: architecture versioning document was exported")


def export_profile(
    profile_path: Path, profile_root: Path, *, inherited_paths: set[Path]
) -> None:
    export_files(output_map(profile_path, inherited_paths=inherited_paths), profile_root)
    profile_name = profile_path.stem
    agent_guide = profile_root / "AGENTS.md"
    if not agent_guide.is_file():
        raise FileNotFoundError(f"{profile_name}: AGENTS.md was not exported")
    validate_agent_guide(agent_guide.read_text(encoding="utf-8"), profile_name)
    validate_review_rules(agent_guide.read_text(encoding="utf-8"), profile_name)
    validate_release_reference(profile_root, profile_name)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="docs-template-export-") as temporary:
        export_root = Path(temporary)
        for profile_name in PROFILE_NAMES:
            profile_path = SKILL_ROOT / "profiles" / f"{profile_name}.md"
            export_profile(profile_path, export_root / profile_name, inherited_paths=set())
            print(f"{profile_name}: template export passed")


if __name__ == "__main__":
    main()
