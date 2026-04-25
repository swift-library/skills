#!/usr/bin/env python3
"""Optional IDB semantic UI helpers for iOS Simulator."""

from __future__ import annotations

import argparse
import json
import shutil
import time
from typing import Any

from tool_common import fail, print_result, run_command


INTERACTIVE_TYPES = {
    "Button",
    "Cell",
    "Link",
    "MenuItem",
    "SearchField",
    "SegmentedControl",
    "Slider",
    "Switch",
    "TabBarItem",
    "TextField",
}

SPECIAL_KEYS = {
    "return": 40,
    "enter": 40,
    "delete": 42,
    "backspace": 42,
    "tab": 43,
    "space": 44,
    "escape": 41,
    "up": 82,
    "down": 81,
    "left": 80,
    "right": 79,
}

HARDWARE_BUTTONS = {
    "home": "HOME",
    "lock": "LOCK",
    "power": "LOCK",
    "volume-up": "VOLUME_UP",
    "volume-down": "VOLUME_DOWN",
    "ringer": "RINGER",
    "screenshot": "SCREENSHOT",
}


def require_idb(*, json_output: bool = False) -> None:
    if not shutil.which("idb"):
        fail("IDB is not installed. Install idb-companion for semantic UI actions.", json_output=json_output)


def idb_args(args: argparse.Namespace, *parts: str) -> list[str]:
    cmd = ["idb", *parts]
    device = getattr(args, "udid", None) or getattr(args, "device", None)
    if device and device != "booted":
        cmd.extend(["--udid", device])
    return cmd


def get_tree(args: argparse.Namespace, *, nested: bool = True) -> Any:
    require_idb(json_output=args.json)
    cmd = idb_args(args, "ui", "describe-all", "--json")
    if nested:
        cmd.append("--nested")
    result = run_command(cmd, json_output=args.json)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON from IDB: {exc}", json_output=args.json)
    if isinstance(payload, list) and len(payload) == 1:
        return payload[0]
    return payload


def flatten(node: Any, depth: int = 0) -> list[dict[str, Any]]:
    if isinstance(node, list):
        out: list[dict[str, Any]] = []
        for item in node:
            out.extend(flatten(item, depth))
        return out
    if not isinstance(node, dict):
        return []
    current = dict(node)
    current["depth"] = depth
    children = current.pop("children", []) or []
    out = [current]
    for child in children:
        out.extend(flatten(child, depth + 1))
    return out


def label_for(element: dict[str, Any]) -> str:
    for key in ("AXLabel", "label", "name", "title", "text", "value", "AXValue", "identifier", "AXIdentifier"):
        value = element.get(key)
        if value:
            return str(value)
    return ""


def identifier_for(element: dict[str, Any]) -> str:
    for key in ("AXIdentifier", "identifier", "AXUniqueId", "id"):
        value = element.get(key)
        if value:
            return str(value)
    return ""


def frame_for(element: dict[str, Any]) -> dict[str, float] | None:
    frame = element.get("frame") or element.get("rect")
    if not isinstance(frame, dict):
        return None
    try:
        return {
            "x": float(frame.get("x", 0)),
            "y": float(frame.get("y", 0)),
            "width": float(frame.get("width", frame.get("w", 0))),
            "height": float(frame.get("height", frame.get("h", 0))),
        }
    except (TypeError, ValueError):
        return None


def center_of(element: dict[str, Any]) -> tuple[int, int] | None:
    frame = frame_for(element)
    if not frame:
        return None
    return (round(frame["x"] + frame["width"] / 2), round(frame["y"] + frame["height"] / 2))


def screen_size(elements: list[dict[str, Any]]) -> tuple[int, int]:
    for element in elements:
        frame = frame_for(element)
        if frame and frame["width"] >= 100 and frame["height"] >= 100:
            return (round(frame["width"]), round(frame["height"]))
    return (390, 844)


def interactive(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for element in elements:
        kind = str(element.get("type") or element.get("role") or "")
        label = label_for(element)
        center = center_of(element)
        if kind in INTERACTIVE_TYPES or element.get("enabled") is True or element.get("AXEnabled") is True:
            rows.append(
                {
                    "type": kind,
                    "label": label,
                    "identifier": identifier_for(element),
                    "center": center,
                    "depth": element.get("depth", 0),
                    "frame": frame_for(element),
                }
            )
    return rows


def match_elements(
    elements: list[dict[str, Any]],
    *,
    text: str | None = None,
    exact: str | None = None,
    element_type: str | None = None,
    identifier: str | None = None,
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for element in elements:
        label = label_for(element)
        kind = str(element.get("type") or element.get("role") or "")
        ident = identifier_for(element)
        if exact is not None and label == exact:
            matches.append(element)
        elif text is not None and text.lower() in label.lower():
            matches.append(element)
        elif element_type is not None and element_type.lower() == kind.lower():
            matches.append(element)
        elif identifier is not None and identifier.lower() in ident.lower():
            matches.append(element)
    return matches


def parse_point(value: str) -> tuple[int, int]:
    if "," not in value:
        fail(f"Point must be x,y: {value}")
    x, y = value.split(",", 1)
    return (int(float(x.strip())), int(float(y.strip())))


def tap_xy(args: argparse.Namespace, x: int, y: int) -> None:
    run_command(idb_args(args, "ui", "tap", str(x), str(y)), json_output=args.json)


def cmd_check(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    result = run_command(["idb", "list-targets"], check=False, json_output=args.json)
    ok = result.returncode == 0
    print_result(
        {
            "ok": ok,
            "message": "IDB is available" if ok else "IDB is installed but list-targets failed",
            "targets": result.stdout.splitlines(),
            "stderr": result.stderr.strip(),
        },
        json_output=args.json,
    )
    raise SystemExit(result.returncode)


def cmd_tree(args: argparse.Namespace) -> None:
    tree = get_tree(args, nested=not args.flat)
    print_result({"ok": True, "tree": tree}, json_output=True)


def cmd_map(args: argparse.Namespace) -> None:
    tree = get_tree(args, nested=True)
    elements = flatten(tree)
    rows = interactive(elements)
    summary = {
        "ok": True,
        "count": len(rows),
        "elements": rows if args.verbose or args.json else rows[: args.limit],
        "type_counts": {},
    }
    for element in elements:
        kind = str(element.get("type") or element.get("role") or "Unknown")
        summary["type_counts"][kind] = summary["type_counts"].get(kind, 0) + 1
    if args.hints:
        summary["hints"] = [
            f"tap-text --text {json.dumps(row['label'])}" for row in rows[:10] if row.get("label")
        ]
    if args.json:
        print_result(summary, json_output=True)
        return
    print(f"Screen: {len(elements)} elements, {len(rows)} interactive")
    for index, row in enumerate(rows[: args.limit], start=1):
        center = row["center"] or ("?", "?")
        print(f"{index}. {row['type']} | {row['label']} | id={row['identifier']} | center={center}")
    if args.hints and summary.get("hints"):
        print("Hints:")
        for hint in summary["hints"]:
            print(f"- {hint}")


def cmd_find(args: argparse.Namespace) -> None:
    tree = get_tree(args, nested=True)
    elements = flatten(tree)
    if args.list:
        matches = interactive(elements)
    else:
        matches = match_elements(
            elements,
            text=args.find_text,
            exact=args.find_exact,
            element_type=args.find_type,
            identifier=args.find_id,
        )
    if not matches:
        fail("No matching elements", json_output=args.json)
    index = min(args.index, len(matches) - 1)
    element = matches[index]
    center = center_of(element)
    action = None
    if args.tap:
        if not center:
            fail("Matched element has no tappable frame", json_output=args.json)
        tap_xy(args, center[0], center[1])
        action = "tap"
    if args.enter_text is not None:
        if center:
            tap_xy(args, center[0], center[1])
        run_command(idb_args(args, "ui", "text", args.enter_text), json_output=args.json)
        action = "enter-text"
    payload = {
        "ok": True,
        "matches": len(matches),
        "selected": {
            "type": element.get("type"),
            "label": label_for(element),
            "identifier": identifier_for(element),
            "center": center,
            "frame": frame_for(element),
        },
        "action": action,
        "message": f"Matched {label_for(element) or element.get('type')} ({len(matches)} match(es))",
    }
    print_result(payload, json_output=args.json)


def cmd_tap(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    tap_xy(args, int(args.x), int(args.y))
    print_result({"ok": True, "x": args.x, "y": args.y, "message": f"Tapped {args.x},{args.y}"}, json_output=args.json)


def cmd_tap_text(args: argparse.Namespace) -> None:
    args.find_text = args.text
    args.find_exact = None
    args.find_type = None
    args.find_id = None
    args.index = args.index
    args.tap = True
    args.enter_text = None
    args.list = False
    cmd_find(args)


def cmd_type(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    if args.slow:
        for char in args.text:
            run_command(idb_args(args, "ui", "text", char), json_output=args.json)
            time.sleep(args.delay)
    else:
        run_command(idb_args(args, "ui", "text", args.text), json_output=args.json)
    print_result({"ok": True, "message": "Typed text through IDB"}, json_output=args.json)


def key_code(key: str) -> str:
    mapped = SPECIAL_KEYS.get(key.lower())
    if mapped is not None:
        return str(mapped)
    int(key)
    return key


def cmd_key(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    code = key_code(args.key)
    for _ in range(args.count):
        run_command(idb_args(args, "ui", "key", code), json_output=args.json)
        if args.count > 1:
            time.sleep(0.1)
    print_result({"ok": True, "key": args.key, "count": args.count, "message": f"Pressed {args.key} x{args.count}"}, json_output=args.json)


def cmd_key_sequence(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    codes = [key_code(key.strip()) for key in args.keys.split(",") if key.strip()]
    run_command(idb_args(args, "ui", "key-sequence", *codes), json_output=args.json)
    print_result({"ok": True, "keys": codes, "message": "Pressed key sequence"}, json_output=args.json)


def cmd_button(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    button = HARDWARE_BUTTONS.get(args.button.lower(), args.button)
    run_command(idb_args(args, "ui", "button", button), json_output=args.json)
    print_result({"ok": True, "button": button, "message": f"Pressed {button}"}, json_output=args.json)


def cmd_clear(args: argparse.Namespace) -> None:
    for _ in range(args.count):
        run_command(idb_args(args, "ui", "key", str(SPECIAL_KEYS["delete"])), json_output=args.json)
    print_result({"ok": True, "message": f"Sent delete x{args.count}"}, json_output=args.json)


def cmd_swipe(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    tree = get_tree(args, nested=False)
    width, height = screen_size(flatten(tree))
    if args.start and args.end:
        x1, y1 = parse_point(args.start)
        x2, y2 = parse_point(args.end)
    elif args.direction:
        cx, cy = width // 2, height // 2
        if args.direction == "up":
            x1, y1, x2, y2 = cx, int(height * 0.75), cx, int(height * 0.25)
        elif args.direction == "down":
            x1, y1, x2, y2 = cx, int(height * 0.25), cx, int(height * 0.75)
        elif args.direction == "left":
            x1, y1, x2, y2 = int(width * 0.8), cy, int(width * 0.2), cy
        else:
            x1, y1, x2, y2 = int(width * 0.2), cy, int(width * 0.8), cy
    else:
        fail("swipe requires --direction or --from/--to", json_output=args.json)
    for _ in range(args.count):
        run_command(idb_args(args, "ui", "swipe", str(x1), str(y1), str(x2), str(y2)), json_output=args.json)
        if args.count > 1:
            time.sleep(0.2)
    print_result({"ok": True, "message": f"Swiped {x1},{y1} -> {x2},{y2} x{args.count}"}, json_output=args.json)


def cmd_refresh(args: argparse.Namespace) -> None:
    args.direction = "down"
    args.count = 1
    args.start = None
    args.end = None
    cmd_swipe(args)


def cmd_scroll(args: argparse.Namespace) -> None:
    args.direction = args.direction
    args.count = args.amount
    args.start = None
    args.end = None
    cmd_swipe(args)


def cmd_long_press(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    x, y = parse_point(args.point)
    cmd = idb_args(args, "ui", "tap", str(x), str(y))
    cmd.extend(["--duration", str(int(args.duration * 1000))])
    run_command(cmd, json_output=args.json)
    print_result({"ok": True, "message": f"Long-pressed {x},{y} for {args.duration}s"}, json_output=args.json)


def cmd_pinch(args: argparse.Namespace) -> None:
    require_idb(json_output=args.json)
    tree = get_tree(args, nested=False)
    width, height = screen_size(flatten(tree))
    cx, cy = parse_point(args.center) if args.center else (width // 2, height // 2)
    offset = 100 if args.direction == "out" else 50
    if args.direction == "out":
        swipes = [((cx - 20, cy - 20), (cx - offset, cy - offset)), ((cx + 20, cy + 20), (cx + offset, cy + offset))]
    else:
        swipes = [((cx - offset, cy - offset), (cx - 20, cy - 20)), ((cx + offset, cy + offset), (cx + 20, cy + 20))]
    for start, end in swipes:
        run_command(idb_args(args, "ui", "swipe", str(start[0]), str(start[1]), str(end[0]), str(end[1])), json_output=args.json)
    print_result({"ok": True, "message": f"Pinch {args.direction} at {cx},{cy}"}, json_output=args.json)


def audit_elements(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for element in elements:
        kind = str(element.get("type") or "")
        label = label_for(element)
        frame = frame_for(element)
        if kind in {"Button", "Link"} and not label:
            issues.append({"severity": "critical", "rule": "missing_label", "type": kind, "fix": "Add accessibility label"})
        if kind == "Button" and not label:
            issues.append({"severity": "critical", "rule": "empty_button", "type": kind, "fix": "Set button title or accessibility label"})
        if kind == "Image" and not label:
            issues.append({"severity": "critical", "rule": "image_no_alt", "type": kind, "fix": "Add alternative text"})
        if kind in {"Slider", "TextField"} and not (element.get("help") or element.get("AXHelp")):
            issues.append({"severity": "warning", "rule": "missing_hint", "type": kind, "label": label, "fix": "Add hint for complex controls"})
        if kind in INTERACTIVE_TYPES and frame and (frame["width"] < 44 or frame["height"] < 44):
            issues.append({"severity": "warning", "rule": "small_touch_target", "type": kind, "label": label, "fix": "Increase target to at least 44x44 pt"})
        if element.get("depth", 0) > 5:
            issues.append({"severity": "info", "rule": "deep_nesting", "type": kind, "label": label, "fix": "Review hierarchy depth"})
    return issues


def cmd_audit(args: argparse.Namespace) -> None:
    tree = get_tree(args, nested=True)
    elements = flatten(tree)
    issues = audit_elements(elements)
    if not args.verbose:
        issues = [issue for issue in issues if issue["severity"] != "info"]
    counts = {level: len([i for i in issues if i["severity"] == level]) for level in ("critical", "warning", "info")}
    payload = {"ok": counts["critical"] == 0, "counts": counts, "issues": issues, "elements": len(elements)}
    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
    if args.json:
        print_result(payload, json_output=True)
        return
    print(f"Accessibility audit: {counts['critical']} critical, {counts['warning']} warnings, {counts['info']} info")
    for issue in issues[:20]:
        print(f"- {issue['severity']}: {issue['rule']} {issue.get('type', '')} {issue.get('label', '')}")
    if args.output:
        print(f"Saved report: {args.output}")


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--device", default="booted", help="Simulator UDID or booted")
    parser.add_argument("--udid", help="Simulator UDID alias")
    parser.add_argument("--json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Optional IDB semantic UI helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="Check IDB availability")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("tree", help="Print accessibility tree as JSON")
    add_common(p)
    p.add_argument("--flat", action="store_true")
    p.set_defaults(func=cmd_tree)

    p = sub.add_parser("map", help="Print concise interactive element map")
    add_common(p)
    p.add_argument("--limit", type=int, default=60)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--hints", action="store_true")
    p.set_defaults(func=cmd_map)

    p = sub.add_parser("find", help="Find and optionally interact with an element")
    add_common(p)
    p.add_argument("--find-text")
    p.add_argument("--find-exact")
    p.add_argument("--find-type")
    p.add_argument("--find-id")
    p.add_argument("--index", type=int, default=0)
    p.add_argument("--tap", action="store_true")
    p.add_argument("--enter-text")
    p.add_argument("--list", action="store_true")
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("tap", help="Tap coordinates")
    add_common(p)
    p.add_argument("--x", required=True)
    p.add_argument("--y", required=True)
    p.set_defaults(func=cmd_tap)

    p = sub.add_parser("tap-text", help="Find element by text/label and tap it")
    add_common(p)
    p.add_argument("--text", required=True)
    p.add_argument("--index", type=int, default=0)
    p.set_defaults(func=cmd_tap_text)

    p = sub.add_parser("type", help="Type text")
    add_common(p)
    p.add_argument("--text", required=True)
    p.add_argument("--slow", action="store_true")
    p.add_argument("--delay", type=float, default=0.1)
    p.set_defaults(func=cmd_type)

    p = sub.add_parser("key", help="Press a special key")
    add_common(p)
    p.add_argument("--key", required=True)
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_key)

    p = sub.add_parser("key-sequence", help="Press a comma-separated key sequence")
    add_common(p)
    p.add_argument("--keys", required=True)
    p.set_defaults(func=cmd_key_sequence)

    p = sub.add_parser("button", help="Press a hardware button")
    add_common(p)
    p.add_argument("--button", required=True)
    p.set_defaults(func=cmd_button)

    p = sub.add_parser("clear", help="Send repeated delete keys")
    add_common(p)
    p.add_argument("--count", type=int, default=50)
    p.set_defaults(func=cmd_clear)

    p = sub.add_parser("dismiss", help="Dismiss keyboard with return")
    add_common(p)
    p.set_defaults(func=lambda args: (setattr(args, "key", "return"), setattr(args, "count", 1), cmd_key(args)))

    p = sub.add_parser("swipe", help="Swipe by direction or coordinates")
    add_common(p)
    p.add_argument("--direction", choices=["up", "down", "left", "right"])
    p.add_argument("--from", dest="start")
    p.add_argument("--to", dest="end")
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_swipe)

    p = sub.add_parser("refresh", help="Pull to refresh")
    add_common(p)
    p.set_defaults(func=cmd_refresh)

    p = sub.add_parser("scroll", help="Scroll with repeated directional swipes")
    add_common(p)
    p.add_argument("--direction", choices=["up", "down"], required=True)
    p.add_argument("--amount", type=int, default=3)
    p.set_defaults(func=cmd_scroll)

    p = sub.add_parser("long-press", help="Long press at x,y")
    add_common(p)
    p.add_argument("--point", required=True)
    p.add_argument("--duration", type=float, default=2.0)
    p.set_defaults(func=cmd_long_press)

    p = sub.add_parser("pinch", help="Pinch in or out")
    add_common(p)
    p.add_argument("--direction", choices=["in", "out"], default="out")
    p.add_argument("--center")
    p.set_defaults(func=cmd_pinch)

    p = sub.add_parser("audit", help="Run a lightweight accessibility-tree audit")
    add_common(p)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--output")
    p.set_defaults(func=cmd_audit)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
