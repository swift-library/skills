#!/usr/bin/env python3
"""Lay existing logos out in one row as a text-free banner.

Usage: logo_row.py LOGO [LOGO ...] --out banner.svg [--cell 160] [--fill 0.96]

Logos are drawn in the order given; sort them before calling (for example by
group or by hue). Each logo fills --fill of a --cell square, with a quarter
cell of padding at the ends.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_embed import embed  # noqa: E402


def main(argv):
    parser = argparse.ArgumentParser(description="Lay existing logos out in one row.")
    parser.add_argument("logos", nargs="+", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--cell", type=float, default=160)
    parser.add_argument("--fill", type=float, default=0.96, help="logo size as a fraction of the cell")
    args = parser.parse_args(argv)

    pad = args.cell * 0.25
    width = len(args.logos) * args.cell + 2 * pad
    height = args.cell + 2 * pad * 0.6
    size = args.cell * args.fill
    body = []
    for index, logo in enumerate(args.logos):
        cx = pad + index * args.cell + args.cell / 2
        body.append(embed(logo, cx - size / 2, (height - size) / 2, size, f"l{index}-"))
    args.out.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" height="{height:.0f}">'
        + "".join(body) + "</svg>")
    print(f"{args.out} {width:.0f}x{height:.0f} logos={len(args.logos)}")


if __name__ == "__main__":
    main(sys.argv[1:])
