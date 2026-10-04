#!/usr/bin/env python3
"""Validate a normalized target's canonical documentation contract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

AGENT_MARKERS = {
    "editing input": "editing input",
    "path independence": "not on the editing path",
    "A+B normalization": "`A + B`",
    "residual-name example": "AWithoutB",
    "semantic-role normalization": "semantic identity and artifact role",
    "history creation boundary": "Do not create a history artifact merely",
    "role-owned fact preservation": "Preserve role-owned facts unless separate evidence changes them",
    "unchanged role-owned artifacts": "Leave an already-correct history",
    "disabled-state boundary": "disabled state alone is not an invariant",
    "cold-start acceptance": "mentally subtracting",
}

CORRECTION_PATTERNS = (
    re.compile(r"\bjson[- ]only\b", re.IGNORECASE),
    re.compile(r"\bwithout\s+yaml\b", re.IGNORECASE),
    re.compile(
        r"yaml.{0,48}\b(?:removed|rejected|deprecated|no longer supported|"
        r"never accepted|explored|draft)\b",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\b(?:removed|rejected|deprecated|no longer supported|never accepted|"
        r"explored|draft)\b.{0,48}yaml",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(r"yaml\s*=\s*false", re.IGNORECASE),
    re.compile(r"\bdo not\s+(?:add|enable|document|support).{0,48}yaml", re.IGNORECASE),
    re.compile(r"yaml.{0,48}\b(?:disabled|prohibited)\b", re.IGNORECASE),
    re.compile(r"\b(?:disabled|prohibited)\b.{0,48}yaml", re.IGNORECASE),
)

HISTORY_PARTS = {"decisions", "migrations", "archive", ".agent", ".git"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    parser.add_argument(
        "--allow-path",
        action="append",
        default=[],
        help="Reviewed repository-relative active document with an independent current exception.",
    )
    return parser.parse_args()


def active_markdown(repository: Path) -> list[Path]:
    candidates = [repository / "README.md"]
    for role in ("Architecture", "Reference"):
        root = repository / "Documentation" / role
        if root.is_dir():
            candidates.extend(root.rglob("*.md"))
    sources = repository / "Sources"
    if sources.is_dir():
        candidates.extend(sources.rglob("*.docc/*.md"))
    return sorted({path for path in candidates if path.is_file()})


def main() -> int:
    args = parse_args()
    repository = args.repository.resolve()
    allowed = {Path(item) for item in args.allow_path}
    failures: list[str] = []

    agent_guide = repository / "AGENTS.md"
    if not agent_guide.is_file():
        failures.append("AGENTS.md is missing")
    else:
        normalized = " ".join(agent_guide.read_text(encoding="utf-8").split())
        for name, marker in AGENT_MARKERS.items():
            if marker not in normalized:
                failures.append(f"AGENTS.md misses {name}: {marker}")
        agent_text = agent_guide.read_text(encoding="utf-8")
        for pattern in CORRECTION_PATTERNS:
            match = pattern.search(agent_text)
            if match is not None:
                excerpt = " ".join(match.group(0).split())
                failures.append(
                    f"AGENTS.md: correction-shaped repository policy: {excerpt!r}"
                )
                break

    for path in active_markdown(repository):
        relative = path.relative_to(repository)
        if relative in allowed or HISTORY_PARTS.intersection(relative.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in CORRECTION_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                excerpt = " ".join(match.group(0).split())
                failures.append(f"{relative}: correction-shaped active prose: {excerpt!r}")
                break

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("canonical target validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
