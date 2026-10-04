"""Place an existing SVG or PNG logo inside another SVG.

SVG logos are inlined as a nested <svg> with every id prefixed, so several
logos with the same gradient or filter ids can share one document. PNG logos
are embedded as base64 data. Used by social_preview.py and logo_row.py.
"""

from __future__ import annotations

import base64
import pathlib
import re

ROOT = re.compile(r"<svg\b([^>]*)>(.*)</svg>\s*$", re.S)
DROP = {"xmlns", "xmlns:xlink", "width", "height", "x", "y", "viewBox", "version", "id", "style"}


def _attrs(text):
    return dict(re.findall(r"([\w:-]+)\s*=\s*\"([^\"]*)\"", text))


def _length(value):
    match = re.match(r"\s*([\d.]+)", value or "")
    return float(match.group(1)) if match else None


def embed(path: pathlib.Path, x: float, y: float, size: float, prefix: str) -> str:
    """Markup that draws the logo inside the square (x, y, size)."""
    path = pathlib.Path(path)
    if path.suffix.lower() == ".png":
        data = base64.b64encode(path.read_bytes()).decode()
        return (f'<image x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" '
                f'href="data:image/png;base64,{data}"/>')
    text = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->", "", path.read_text(), flags=re.S).strip()
    match = ROOT.search(text)
    if not match:
        raise ValueError(f"{path}: no <svg> root")
    attrs = _attrs(match.group(1))
    inner = match.group(2)
    view_box = attrs.get("viewBox")
    if not view_box:
        width, height = _length(attrs.get("width")), _length(attrs.get("height"))
        if not (width and height):
            raise ValueError(f"{path}: needs viewBox or width and height")
        view_box = f"0 0 {width:g} {height:g}"
    for name in sorted(set(re.findall(r"\bid=\"([^\"]+)\"", inner)), key=len, reverse=True):
        escaped = re.escape(name)
        inner = re.sub(rf"\bid=\"{escaped}\"", f'id="{prefix}{name}"', inner)
        inner = re.sub(rf"url\(\s*#{escaped}\s*\)", f"url(#{prefix}{name})", inner)
        inner = re.sub(rf"(href=\")#{escaped}\"", rf'\g<1>#{prefix}{name}"', inner)
    kept = " ".join(f'{k}="{v}"' for k, v in attrs.items() if k not in DROP and not k.startswith("xmlns"))
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" viewBox="{view_box}" '
            f'preserveAspectRatio="xMidYMid meet" {kept}>{inner}</svg>')
