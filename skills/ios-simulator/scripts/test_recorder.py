#!/usr/bin/env python3
"""Create a compact test evidence bundle from the current simulator screen."""

from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path

from tool_common import print_result, resolve_device, run_command


def main() -> None:
    parser = argparse.ArgumentParser(description="Record current simulator state as test evidence")
    parser.add_argument("--test-name", required=True)
    parser.add_argument("--output", default="test-artifacts")
    parser.add_argument("--device", default="booted")
    parser.add_argument("--udid", help="Simulator UDID alias")
    parser.add_argument("--inline", action="store_true")
    parser.add_argument("--size", choices=["quarter", "half", "full"], default="half")
    parser.add_argument("--app-name")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    device = resolve_device(args.udid or args.device, json_output=args.json)
    out_dir = Path(args.output).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in args.test_name).strip("-")
    screenshot = out_dir / f"{safe_name}-{stamp}.png"
    hierarchy = out_dir / f"{safe_name}-{stamp}.json"
    report = out_dir / f"{safe_name}-{stamp}.md"

    run_command(["xcrun", "simctl", "io", device, "screenshot", str(screenshot)], json_output=args.json)
    hierarchy_ok = False
    if shutil.which("idb"):
        cmd = ["idb", "ui", "describe-all", "--json", "--nested"]
        if device != "booted":
            cmd.extend(["--udid", device])
        result = run_command(cmd, check=False, json_output=args.json)
        if result.returncode == 0:
            hierarchy.write_text(result.stdout, encoding="utf-8")
            hierarchy_ok = True

    report.write_text(
        "\n".join(
            [
                f"# {args.test_name}",
                "",
                f"- Captured: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- Device: {device}",
                f"- Screenshot: {screenshot}",
                f"- Accessibility tree: {hierarchy if hierarchy_ok else 'not captured'}",
            ]
        ),
        encoding="utf-8",
    )
    print_result(
        {
            "ok": True,
            "device": device,
            "screenshot": str(screenshot),
            "hierarchy": str(hierarchy) if hierarchy_ok else None,
            "report": str(report),
            "message": f"Recorded test evidence: {report}",
        },
        json_output=args.json,
    )


if __name__ == "__main__":
    main()
