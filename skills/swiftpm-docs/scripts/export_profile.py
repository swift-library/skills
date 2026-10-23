#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Export a Swift package documentation profile."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from profile_export import (
    PLACEHOLDER, PROFILE_NAMES, SKILL_ROOT, export_files, output_map,
    package_facts, read_utf8,
)


def assignment(argument: str) -> tuple[str, str]:
    name, separator, value = argument.partition("=")
    if not separator or re.fullmatch(r"[a-z0-9-]+", name) is None:
        raise argparse.ArgumentTypeError(f"--set {argument}: expected NAME=VALUE with a lowercase name")
    return name, value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=PROFILE_NAMES)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--package-root", type=Path,
        help="repository root; reads package_directory from .github/swift-package.json when present",
    )
    parser.add_argument("--set", action="append", type=assignment, default=[], dest="values")
    parser.add_argument("--inherited", action="append", type=Path, default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        profile = SKILL_ROOT / "profiles" / f"{args.profile}.md"
        all_outputs = output_map(profile, inherited_paths=set())
        targets = {target for target, _ in all_outputs}
        for inherited in args.inherited:
            if inherited not in targets:
                parser.error(f"--inherited {inherited}: path is not in the {args.profile} profile")
        outputs = output_map(profile, inherited_paths=set(args.inherited))
        names = {
            name for _, source in outputs for name in PLACEHOLDER.findall(read_utf8(source))
        }
        values = dict(args.values)
        for name in values:
            if name not in names:
                parser.error(f"--set {name}: no exported template uses this name")
        replacements = package_facts(args.package_root) if args.package_root else {}
        replacements.update(values)
        for path in export_files(outputs, args.output, replacements=replacements, force=args.force):
            print(path)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
