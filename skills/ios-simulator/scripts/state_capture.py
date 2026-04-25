#!/usr/bin/env python3
"""Capture screenshot, hierarchy, logs, and device state for bug reports."""

from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path

from tool_common import ensure_parent, list_simulators, print_result, resolve_device, run_command


def maybe_resize(path: Path, size: str) -> tuple[int | None, int | None]:
    if size == "full":
        return (None, None)
    try:
        from PIL import Image
    except Exception:
        return (None, None)
    scale = {"half": 0.5, "quarter": 0.25}.get(size, 1.0)
    image = Image.open(path)
    new_size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
    image.resize(new_size).save(path)
    return new_size


def capture(args: argparse.Namespace) -> dict:
    device = resolve_device(args.udid or args.device, json_output=args.json)
    out_dir = Path(args.output).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot = out_dir / f"{args.app_name or 'screen'}-{stamp}.png"
    logs = out_dir / f"logs-{stamp}.log"
    hierarchy = out_dir / f"hierarchy-{stamp}.json"
    summary = out_dir / f"summary-{stamp}.md"

    run_command(["xcrun", "simctl", "io", device, "screenshot", str(screenshot)], json_output=args.json)
    dimensions = maybe_resize(screenshot, args.size)

    log_cmd = ["xcrun", "simctl", "spawn", device, "log", "show", "--style", "compact", "--last", args.last]
    if args.app_bundle_id:
        log_cmd.extend(["--predicate", f'processImagePath CONTAINS "{args.app_bundle_id}"'])
    log_result = run_command(log_cmd, check=False, json_output=args.json)
    log_lines = log_result.stdout.splitlines()[-args.log_lines :]
    logs.write_text("\n".join(log_lines), encoding="utf-8")

    hierarchy_ok = False
    if shutil.which("idb"):
        cmd = ["idb", "ui", "describe-all", "--json", "--nested"]
        if device != "booted":
            cmd.extend(["--udid", device])
        tree = run_command(cmd, check=False, json_output=args.json)
        if tree.returncode == 0:
            hierarchy.write_text(tree.stdout, encoding="utf-8")
            hierarchy_ok = True

    booted = [d for d in list_simulators(json_output=args.json) if d["state"] == "Booted"]
    summary.write_text(
        "\n".join(
            [
                "# iOS Simulator State Capture",
                "",
                f"- Device: {device}",
                f"- App bundle: {args.app_bundle_id or 'not specified'}",
                f"- Screenshot: {screenshot}",
                f"- Logs: {logs}",
                f"- Hierarchy: {hierarchy if hierarchy_ok else 'not captured'}",
                f"- Booted simulators: {len(booted)}",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "ok": True,
        "device": device,
        "screenshot": str(screenshot),
        "screenshot_dimensions": dimensions,
        "logs": str(logs),
        "hierarchy": str(hierarchy) if hierarchy_ok else None,
        "summary": str(summary),
        "message": f"Captured simulator state in {out_dir}",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture complete app state for debugging")
    parser.add_argument("--app-bundle-id")
    parser.add_argument("--output", default=".")
    parser.add_argument("--log-lines", type=int, default=100)
    parser.add_argument("--last", default="5m")
    parser.add_argument("--device", default="booted")
    parser.add_argument("--udid", help="Simulator UDID alias")
    parser.add_argument("--inline", action="store_true")
    parser.add_argument("--size", choices=["quarter", "half", "full"], default="half")
    parser.add_argument("--app-name")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = capture(args)
    print_result(result, json_output=args.json)


if __name__ == "__main__":
    main()
