#!/usr/bin/env python3
"""Read-only environment check for Swift SDKs for WebAssembly."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    required: bool = True


def run(args: list[str]) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            args,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as error:
        return 127, "", str(error)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def command_check(binary: str, label: str, required: bool = True) -> Check:
    path = shutil.which(binary)
    if path:
        return Check(label, True, path, required)
    return Check(label, False, f"{binary} not found", required)


def swift_version() -> Check:
    code, stdout, stderr = run(["swift", "--version"])
    if code == 0 and stdout:
        return Check("swift --version", True, stdout.splitlines()[0])
    return Check("swift --version", False, stderr or "swift --version failed")


def swift_target_info() -> Check:
    code, stdout, stderr = run(["swiftc", "-print-target-info"])
    if code != 0 or not stdout:
        return Check("swiftc -print-target-info", False, stderr or "target info failed")
    try:
        info = json.loads(stdout)
    except json.JSONDecodeError as error:
        return Check("swiftc -print-target-info", False, f"invalid JSON: {error}")

    compiler_tag = info.get("swiftCompilerTag") or "unknown compiler tag"
    target = info.get("target", {}).get("triple") or "unknown target"
    if str(compiler_tag).startswith("swiftlang-"):
        detail = (
            f"{compiler_tag}; target {target}. Xcode toolchain detected; "
            "verify against Swift.org Wasm SDK instructions."
        )
        return Check("Swift toolchain", False, detail)
    return Check("Swift toolchain", True, f"{compiler_tag}; target {target}")


def swift_sdk_list() -> Check:
    code, stdout, stderr = run(["swift", "sdk", "list"])
    if code != 0:
        return Check("swift sdk list", False, stderr or "swift sdk list failed")
    wasm_lines = [line.strip() for line in stdout.splitlines() if "wasm" in line.lower()]
    if wasm_lines:
        detail = "; ".join(wasm_lines[:4])
        if len(wasm_lines) > 4:
            detail += f"; ... {len(wasm_lines) - 4} more"
        return Check("Swift SDKs for WebAssembly", True, detail)
    return Check("Swift SDKs for WebAssembly", False, "no wasm SDK found in swift sdk list")


def print_check(check: Check) -> None:
    status = "ok" if check.ok else ("missing" if check.required else "optional")
    print(f"[{status}] {check.name}: {check.detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero when required checks fail",
    )
    args = parser.parse_args()

    checks = [
        command_check("swift", "swift command"),
        command_check("swiftc", "swiftc command"),
        swift_version(),
        swift_target_info(),
        swift_sdk_list(),
        command_check("node", "Node.js", required=False),
        command_check("npm", "npm", required=False),
    ]

    for check in checks:
        print_check(check)

    failures = [check for check in checks if check.required and not check.ok]
    if failures:
        print("")
        print("Swift Wasm environment is incomplete. Refresh facts from Swift.org and local tool output before editing build rules.")
        return 1 if args.strict else 0

    print("")
    print("Swift Wasm environment looks ready for local build validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
