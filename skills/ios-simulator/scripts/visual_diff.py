#!/usr/bin/env python3
"""Compare two screenshots and optionally generate a diff image."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tool_common import ensure_parent, fail, print_result


def load_pillow(json_output: bool = False):
    try:
        from PIL import Image, ImageChops, ImageDraw

        return Image, ImageChops, ImageDraw
    except Exception:
        fail("visual_diff requires Pillow. Install with: pip3 install pillow", json_output=json_output)


def cmd_compare(args: argparse.Namespace) -> None:
    Image, ImageChops, ImageDraw = load_pillow(args.json)
    baseline_path = Path(args.baseline).expanduser()
    current_path = Path(args.current).expanduser()
    if not baseline_path.exists():
        fail(f"Baseline image not found: {baseline_path}", json_output=args.json)
    if not current_path.exists():
        fail(f"Current image not found: {current_path}", json_output=args.json)

    baseline = Image.open(baseline_path).convert("RGB")
    current = Image.open(current_path).convert("RGB")
    if baseline.size != current.size:
        fail(f"Image dimensions differ: {baseline.size} vs {current.size}", json_output=args.json)

    diff = ImageChops.difference(baseline, current)
    bbox = diff.getbbox()
    pixels = baseline.size[0] * baseline.size[1]
    changed = 0
    if bbox:
        for pixel in diff.getdata():
            if pixel != (0, 0, 0):
                changed += 1
    percent = (changed / pixels) * 100 if pixels else 0.0
    passed = percent <= args.threshold

    output_path = None
    if args.output:
        output_path = ensure_parent(args.output)
        enhanced = Image.new("RGB", baseline.size, "black")
        draw = ImageDraw.Draw(enhanced)
        for y in range(diff.size[1]):
            for x in range(diff.size[0]):
                if diff.getpixel((x, y)) != (0, 0, 0):
                    draw.point((x, y), fill=(255, 0, 0))
        enhanced.save(output_path)

    payload = {
        "ok": passed,
        "changed_pixels": changed,
        "total_pixels": pixels,
        "difference_percent": round(percent, 4),
        "threshold_percent": args.threshold,
        "bbox": bbox,
        "output": str(output_path) if output_path else None,
        "message": f"Visual diff: {percent:.4f}% changed (threshold {args.threshold}%)",
    }
    if args.json or args.details:
        print_result(payload, json_output=args.json)
    else:
        print(payload["message"])
        if output_path:
            print(f"Diff image: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare screenshots for visual differences")
    parser.add_argument("baseline")
    parser.add_argument("current")
    parser.add_argument("--output")
    parser.add_argument("--threshold", type=float, default=1.0, help="Allowed percent difference")
    parser.add_argument("--details", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cmd_compare(args)


if __name__ == "__main__":
    main()
