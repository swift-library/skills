#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Export a Swift package documentation profile, or check a repository against it."""

from __future__ import annotations

import argparse
import difflib
import os
from pathlib import Path
import re
import sys

from profile_export import (
    MODULE_NAMES, PLACEHOLDER, PROFILE_NAMES, SKILL_ROOT, drifted_files, export_files,
    output_map, package_facts, render_template,
)


def assignment(argument: str) -> tuple[str, str]:
    name, separator, value = argument.partition("=")
    if not separator or re.fullmatch(r"[a-z0-9-]+", name) is None:
        raise argparse.ArgumentTypeError(f"--set {argument}: expected NAME=VALUE with a lowercase name")
    return name, value


def report_drift(drifted: list[tuple[Path, bytes | None, bytes]], profile: str) -> None:
    for destination, actual, expected in drifted:
        if actual is None:
            print(f"{destination}: missing file", file=sys.stderr)
        sys.stdout.flush()
        sys.stdout.buffer.writelines(difflib.diff_bytes(
            difflib.unified_diff, (actual or b"").splitlines(keepends=True),
            expected.splitlines(keepends=True), fromfile=os.fsencode(destination),
            tofile=os.fsencode(f"{destination} ({profile} export)"),
        ))
    sys.stdout.flush()
    print(
        f"{len(drifted)} file(s) differ from the {profile} export; "
        "run the same command with --force instead of --check to write it",
        file=sys.stderr,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=PROFILE_NAMES)
    parser.add_argument(
        "--module", action="append", choices=MODULE_NAMES, default=[],
        help="include an optional contract (default: none)",
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--package-root", type=Path,
        help="repository root; reads package_directory from .github/swift-package.json when present",
    )
    parser.add_argument("--set", action="append", type=assignment, default=[], dest="values")
    parser.add_argument("--inherited", action="append", type=Path, default=[])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--force", action="store_true", help="overwrite existing files")
    mode.add_argument(
        "--check", action="store_true",
        help="compare the output directory with the export and write nothing; exit 1 on differences",
    )
    args = parser.parse_args()

    try:
        profile = SKILL_ROOT / "profiles" / f"{args.profile}.md"
        all_outputs = output_map(profile, inherited_paths=set())
        targets = {target for target, _ in all_outputs}
        for inherited in args.inherited:
            if inherited not in targets:
                parser.error(f"--inherited {inherited}: path is not in the {args.profile} profile")
        outputs = output_map(profile, inherited_paths=set(args.inherited))
        modules = frozenset(args.module)
        names = {
            name for _, source in outputs
            for name in PLACEHOLDER.findall(render_template(source, modules=modules))
        }
        values = dict(args.values)
        for name in values:
            if name not in names:
                parser.error(f"--set {name}: no exported template uses this name")
        replacements = package_facts(args.package_root) if args.package_root else {}
        replacements.update(values)
        if args.check:
            drifted = drifted_files(outputs, args.output, replacements=replacements, modules=modules)
            if drifted:
                report_drift(drifted, args.profile)
                return 1
            print(f"{len(outputs)} files match the {args.profile} export")
            return 0
        for path in export_files(
            outputs, args.output, replacements=replacements, force=args.force, modules=modules,
        ):
            print(path)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
