#!/usr/bin/env python3
"""Inspect Core Data .xcdatamodeld packages and SwiftData @Model declarations."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from tool_common import fail, print_result


SKIP_DIRS = {".build", ".git", "DerivedData", "Pods", "Carthage", ".swiftpm"}


def inspect_core_data(root: Path, *, show_versions: bool = False) -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = []
    for package in root.rglob("*.xcdatamodeld"):
        versions = sorted(package.glob("*.xcdatamodel"))
        current = None
        version_info = package / ".xccurrentversion"
        if version_info.exists():
            text = version_info.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"_XCCurrentVersionName\s*</key>\s*<string>([^<]+)</string>", text)
            if match:
                current = match.group(1)
        for version in versions:
            contents = version / "contents"
            if not contents.exists():
                continue
            try:
                tree = ET.parse(contents)
            except ET.ParseError:
                continue
            entities = []
            for entity in tree.findall(".//entity"):
                attrs = [
                    {"name": a.get("name"), "type": a.get("attributeType"), "optional": a.get("optional") == "YES"}
                    for a in entity.findall("attribute")
                ]
                rels = [
                    {"name": r.get("name"), "destination": r.get("destinationEntity"), "to_many": r.get("toMany") == "YES", "optional": r.get("optional") == "YES"}
                    for r in entity.findall("relationship")
                ]
                entities.append({"name": entity.get("name"), "class": entity.get("representedClassName"), "attributes": attrs, "relationships": rels})
            models.append(
                {
                    "package": str(package),
                    "version": version.name,
                    "is_current": current == version.name if current else None,
                    "entities": entities,
                }
            )
    if not show_versions:
        compact: list[dict[str, Any]] = []
        by_package: dict[str, list[dict[str, Any]]] = {}
        for model in models:
            by_package.setdefault(model["package"], []).append(model)
        for entries in by_package.values():
            current = [entry for entry in entries if entry.get("is_current")]
            compact.append(current[0] if current else entries[-1])
        return compact
    return models


def swift_files(root: Path):
    for path in root.rglob("*.swift"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def extract_block(text: str, start: int) -> str:
    brace = text.find("{", start)
    if brace == -1:
        return ""
    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return text[start:]


def inspect_swiftdata(root: Path) -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = []
    pattern = re.compile(r"@Model(?:\s+[^\n]+)?\s*(?:final\s+)?class\s+(\w+)")
    prop_pattern = re.compile(r"(?:@Attribute\([^)]+\)\s*)?(?:@Relationship\([^)]+\)\s*)?var\s+(\w+)\s*:\s*([^\n=]+)")
    for path in swift_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            name = match.group(1)
            block = extract_block(text, match.start())
            props = [{"name": m.group(1), "type": m.group(2).strip()} for m in prop_pattern.finditer(block)]
            models.append({"name": name, "file": str(path), "properties": props, "raw": block})
    return models


def raw_model(root: Path, name: str) -> tuple[bool, str]:
    for model in inspect_swiftdata(root):
        if model["name"] == name:
            return True, str(model["raw"])
    for model in inspect_core_data(root, show_versions=True):
        for entity in model["entities"]:
            if entity.get("name") == name:
                return True, json.dumps(entity, indent=2)
    return False, ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect Core Data and SwiftData models")
    parser.add_argument("--project-path", default=".")
    parser.add_argument("--core-data-only", action="store_true")
    parser.add_argument("--swiftdata-only", action="store_true")
    parser.add_argument("--show-versions", action="store_true")
    parser.add_argument("--raw")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_path).expanduser()
    if not root.exists():
        fail(f"Project path not found: {root}", json_output=args.json)
    if args.raw:
        found, raw = raw_model(root, args.raw)
        if not found:
            fail(f"Model not found: {args.raw}", json_output=args.json)
        print(raw)
        return

    payload: dict[str, Any] = {"ok": True}
    if not args.swiftdata_only:
        payload["core_data"] = inspect_core_data(root, show_versions=args.show_versions)
    if not args.core_data_only:
        swiftdata = inspect_swiftdata(root)
        if not args.verbose:
            swiftdata = [{k: v for k, v in item.items() if k != "raw"} for item in swiftdata]
        payload["swiftdata"] = swiftdata
    payload["message"] = (
        f"Models: Core Data={len(payload.get('core_data', []))}, "
        f"SwiftData={len(payload.get('swiftdata', []))}"
    )
    if args.json:
        print_result(payload, json_output=True)
        return
    print(payload["message"])
    for model in payload.get("core_data", []):
        print(f"- Core Data {Path(model['package']).name}/{model['version']}: {len(model['entities'])} entities")
    for model in payload.get("swiftdata", []):
        print(f"- SwiftData {model['name']} ({model['file']}): {len(model['properties'])} properties")


if __name__ == "__main__":
    main()
