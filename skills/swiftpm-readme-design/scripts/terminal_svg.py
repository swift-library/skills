#!/usr/bin/env python3
"""Render a recorded terminal transcript as a static terminal window SVG.

Usage: terminal_svg.py TRANSCRIPT OUT.svg [--title TEXT]

Lines starting with "$ " are commands; a command line ending in a backslash
continues on the next line. Everything else is output, rendered verbatim.
The transcript must be real output from the version being documented.
"""

from __future__ import annotations

import argparse
import html
import pathlib
import sys

FONT = "ui-monospace, Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"
SIZE, LINE, CHAR = 14, 21, 8.43
PAD_X, PAD_TOP, PAD_BOTTOM, BAR = 20, 16, 18, 34
BG, BAR_BG, BORDER = "#0d1117", "#161b22", "#30363d"
PROMPT, COMMAND, OUTPUT, DIM = "#3fb950", "#e6edf3", "#c9d1d9", "#8b949e"


def classify(lines):
    kinds, continuing = [], False
    for line in lines:
        if line.startswith("$ ") or continuing:
            kinds.append("cmd")
            continuing = line.rstrip().endswith("\\")
        else:
            kinds.append("out")
    return kinds


def render(lines, title):
    kinds = classify(lines)
    width = max(len(line) for line in lines) * CHAR + 2 * PAD_X + 8
    height = BAR + PAD_TOP + len(lines) * LINE + PAD_BOTTOM
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height}" '
        f'width="{width:.0f}" height="{height}" font-family="{FONT}" font-size="{SIZE}">',
        f'<rect x="0.5" y="0.5" width="{width - 1:.0f}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M0.5 {BAR} V10.5 a10 10 0 0 1 10 -10 H{width - 10.5:.0f} a10 10 0 0 1 10 10 V{BAR} Z" '
        f'fill="{BAR_BG}"/>',
        f'<line x1="0.5" y1="{BAR}" x2="{width - 0.5:.0f}" y2="{BAR}" stroke="{BORDER}"/>',
    ]
    for index, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        parts.append(f'<circle cx="{20 + index * 20}" cy="{BAR / 2}" r="6" fill="{color}"/>')
    if title:
        parts.append(f'<text x="{width / 2:.0f}" y="{BAR / 2 + 5}" text-anchor="middle" fill="{DIM}" '
                     f'font-size="13">{html.escape(title)}</text>')
    y = BAR + PAD_TOP + SIZE
    for line, kind in zip(lines, kinds):
        text = html.escape(line)
        if kind == "cmd" and line.startswith("$ "):
            parts.append(f'<text x="{PAD_X}" y="{y}" xml:space="preserve"><tspan fill="{PROMPT}">$</tspan>'
                         f'<tspan fill="{COMMAND}">{text[1:]}</tspan></text>')
        else:
            color = COMMAND if kind == "cmd" else OUTPUT
            parts.append(f'<text x="{PAD_X}" y="{y}" fill="{color}" xml:space="preserve">{text}</text>')
        y += LINE
    parts.append("</svg>")
    return "".join(parts), width, height


def main(argv):
    parser = argparse.ArgumentParser(description="Render a terminal transcript as an SVG window.")
    parser.add_argument("transcript", type=pathlib.Path)
    parser.add_argument("out", type=pathlib.Path)
    parser.add_argument("--title", default="")
    args = parser.parse_args(argv)
    lines = args.transcript.read_text().rstrip("\n").expandtabs(8).split("\n")
    svg, width, height = render(lines, args.title)
    args.out.write_text(svg)
    print(f"{args.out} {width:.0f}x{height}")


if __name__ == "__main__":
    main(sys.argv[1:])
