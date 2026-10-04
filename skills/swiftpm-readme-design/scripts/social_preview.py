#!/usr/bin/env python3
"""Compose a 1280x640 social preview card from an existing logo.

Usage:
  social_preview.py --logo Logo.svg --owner OWNER --name REPO --summary "About sentence"
                    --font-bold Bold.ttf --font-regular Regular.ttf [--font-medium Medium.ttf]
                    [--glow "#e8f0ff"] --out card.svg [--png card.png]

Text is converted to outlines with fontTools, so the card does not depend on
installed fonts. Use fonts whose license allows this, such as SIL OFL fonts.
--png renders with rsvg-convert when it is installed.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_embed import embed  # noqa: E402

try:
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
except ImportError:
    TTFont = None

W, H = 1280, 640
LOGO_CENTER, LOGO_SIZE = 300, 420
TEXT_X, TEXT_RIGHT = 560, 1200


class Face:
    def __init__(self, path):
        self.font = TTFont(path)
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm
        self.hmtx = self.font["hmtx"]

    def _name(self, char):
        return self.cmap.get(ord(char), ".notdef")

    def width(self, text, size):
        return sum(self.hmtx[self._name(c)][0] for c in text) * size / self.upm

    def path(self, text, size, x, y):
        pen = SVGPathPen(self.glyphs)
        scale = size / self.upm
        for char in text:
            name = self._name(char)
            self.glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
            x += self.hmtx[name][0] * scale
        return pen.getCommands()


def wrap(face, text, size, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if face.width(trial, size) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def compose(args):
    bold = Face(args.font_bold)
    regular = Face(args.font_regular)
    medium = Face(args.font_medium) if args.font_medium else regular
    room = TEXT_RIGHT - TEXT_X

    name_size = 76
    while bold.width(args.name, name_size) > room and name_size > 44:
        name_size -= 2
    body_size = 32
    lines = wrap(regular, args.summary, body_size, room)
    while len(lines) > 3 and body_size > 22:
        body_size -= 2
        lines = wrap(regular, args.summary, body_size, room)

    owner_size = 30
    block = owner_size + 22 + name_size + 30 + len(lines) * body_size * 1.35
    top = (H - block) / 2
    y_owner = top + owner_size
    y_name = y_owner + 22 + name_size * 0.95
    y_body = y_name + 30 + body_size

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        "<defs>",
        '<linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#fbfbfd"/><stop offset="1" stop-color="#f0f0f3"/></linearGradient>',
    ]
    if args.glow:
        parts.append(f'<radialGradient id="card-glow" cx="{LOGO_CENTER}" cy="{H / 2}" r="360" '
                     f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{args.glow}" stop-opacity="0.9"/>'
                     f'<stop offset="1" stop-color="{args.glow}" stop-opacity="0"/></radialGradient>')
    parts += ["</defs>", f'<rect width="{W}" height="{H}" fill="url(#card-bg)"/>']
    if args.glow:
        parts.append(f'<rect width="{W}" height="{H}" fill="url(#card-glow)"/>')
    parts.append(embed(args.logo, LOGO_CENTER - LOGO_SIZE / 2, (H - LOGO_SIZE) / 2, LOGO_SIZE, "logo-"))
    parts.append(f'<path d="{medium.path(args.owner, owner_size, TEXT_X, y_owner)}" fill="#6e6e73"/>')
    parts.append(f'<path d="{bold.path(args.name, name_size, TEXT_X - name_size * 0.04, y_name)}" fill="#1d1d1f"/>')
    for index, line in enumerate(lines):
        y = y_body + index * body_size * 1.35
        parts.append(f'<path d="{regular.path(line, body_size, TEXT_X, y)}" fill="#424245"/>')
    parts.append("</svg>")
    return "".join(parts), name_size, body_size, len(lines)


def main(argv):
    parser = argparse.ArgumentParser(description="Compose a social preview card from an existing logo.")
    parser.add_argument("--logo", type=pathlib.Path, required=True, help="existing logo (.svg or .png)")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--summary", required=True, help="the repository's About sentence")
    parser.add_argument("--font-bold", required=True, help="font file for the repository name")
    parser.add_argument("--font-regular", required=True, help="font file for the summary")
    parser.add_argument("--font-medium", help="font file for the owner label (default: regular)")
    parser.add_argument("--glow", help="light accent color behind the logo, such as #e8f0ff")
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--png", type=pathlib.Path, help="also render a 1280x640 PNG with rsvg-convert")
    args = parser.parse_args(argv)
    if TTFont is None:
        sys.exit("error: fontTools is required (python3 -m pip install fonttools)")

    svg, name_size, body_size, line_count = compose(args)
    args.out.write_text(svg)
    print(f"{args.out} name={name_size}px summary={body_size}px lines={line_count}")
    if args.png:
        if not shutil.which("rsvg-convert"):
            sys.exit("error: rsvg-convert not found; convert the SVG to a 1280x640 PNG with another renderer")
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), str(args.out), "-o", str(args.png)], check=True)
        size = args.png.stat().st_size
        print(f"{args.png} {size} bytes" + ("" if size < 1_000_000 else " (over GitHub's 1 MB limit)"))


if __name__ == "__main__":
    main(sys.argv[1:])
