#!/usr/bin/env python3
"""Concise xcodebuild wrapper for iOS Simulator builds and tests."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from tool_common import ensure_parent, fail, print_result, require_tool, run_command


STATE_DIR = Path(".codex/ios-simulator")
RESULT_DIR = STATE_DIR / "xcresults"
INDEX_PATH = STATE_DIR / "xcresults-index.json"


def find_project_root(start: Path) -> tuple[str | None, str | None]:
    workspaces = sorted(start.glob("*.xcworkspace"))
    projects = sorted(start.glob("*.xcodeproj"))
    workspace = str(workspaces[0]) if workspaces else None
    project = str(projects[0]) if projects else None
    return workspace, project


def project_args(args: argparse.Namespace) -> list[str]:
    if getattr(args, "workspace", None):
        return ["-workspace", args.workspace]
    if getattr(args, "project", None):
        return ["-project", args.project]
    workspace, project = find_project_root(Path.cwd())
    if workspace:
        args.workspace = workspace
        return ["-workspace", workspace]
    if project:
        args.project = project
        return ["-project", project]
    fail("No .xcworkspace or .xcodeproj found. Pass --workspace or --project.", json_output=args.json)


def list_schemes_for(args: argparse.Namespace) -> list[str]:
    cmd = ["xcodebuild", "-list", "-json", *project_args(args)]
    result = run_command(cmd, json_output=args.json)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        fallback = run_command(["xcodebuild", "-list", *project_args(args)], json_output=args.json)
        schemes: list[str] = []
        in_schemes = False
        for line in fallback.stdout.splitlines():
            stripped = line.strip()
            if stripped == "Schemes:":
                in_schemes = True
                continue
            if in_schemes and stripped:
                schemes.append(stripped)
        return schemes
    for key in ("workspace", "project"):
        schemes = payload.get(key, {}).get("schemes")
        if schemes:
            return list(schemes)
    return []


def resolve_scheme(args: argparse.Namespace) -> str:
    if args.scheme:
        return args.scheme
    schemes = list_schemes_for(args)
    if not schemes:
        fail("No schemes discovered. Pass --scheme.", json_output=args.json)
    return schemes[0]


def destination(args: argparse.Namespace, action: str) -> str:
    if args.destination:
        chosen = args.destination
    elif args.simulator:
        chosen = f"platform=iOS Simulator,name={args.simulator}"
    else:
        chosen = "generic/platform=iOS Simulator"
    if action == "test" and chosen.startswith("generic/"):
        fail(
            "Testing needs a concrete simulator. Pass --simulator NAME or "
            "--destination 'platform=iOS Simulator,id=UDID'.",
            json_output=args.json,
        )
    return chosen


def result_id(action: str) -> str:
    return f"xcresult-{time.strftime('%Y%m%d-%H%M%S')}-{action}"


def load_index() -> dict[str, Any]:
    if INDEX_PATH.exists():
        try:
            return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_index(index: dict[str, Any]) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")


def diagnostic_lines(text: str, kind: str, limit: int) -> list[str]:
    needle = f"{kind}:"
    lines = [line.strip() for line in text.splitlines() if needle in line.lower()]
    seen: set[str] = set()
    deduped: list[str] = []
    for line in lines:
        if line not in seen:
            deduped.append(line)
            seen.add(line)
    return deduped[:limit]


def register_result(result_id_value: str, payload: dict[str, Any]) -> None:
    index = load_index()
    index[result_id_value] = payload
    save_index(index)


def result_entry(identifier: str, *, json_output: bool = False) -> dict[str, Any]:
    index = load_index()
    entry = index.get(identifier)
    if not entry:
        fail(f"Unknown xcresult id: {identifier}. Use list-results.", json_output=json_output)
    return entry


def cmd_build_or_test(args: argparse.Namespace) -> None:
    require_tool("xcodebuild", json_output=args.json)
    action = "test" if args.command == "test" or args.test else "build"
    target = destination(args, action)
    scheme = resolve_scheme(args)
    rid = result_id(action)
    result_path = ensure_parent(args.result_bundle or RESULT_DIR / f"{rid}.xcresult")
    log_path = ensure_parent(args.log or STATE_DIR / f"{rid}.log")

    cmd = ["xcodebuild", "-quiet"]
    if args.clean:
        cmd.append("clean")
    cmd.append(action)
    cmd.extend(project_args(args))
    cmd.extend(["-scheme", scheme, "-configuration", args.configuration, "-destination", target, "-resultBundlePath", str(result_path)])
    if args.suite:
        cmd.extend(["-only-testing", args.suite])
    for only_testing in args.only_testing or []:
        cmd.extend(["-only-testing", only_testing])
    for skip_testing in args.skip_testing or []:
        cmd.extend(["-skip-testing", skip_testing])

    result = run_command(cmd, check=False, timeout=args.timeout, json_output=args.json)
    combined = "\n".join([result.stdout, result.stderr])
    log_path.write_text(combined, encoding="utf-8")
    errors = diagnostic_lines(combined, "error", args.diagnostic_limit)
    warnings = diagnostic_lines(combined, "warning", args.diagnostic_limit)
    ok = result.returncode == 0
    payload: dict[str, Any] = {
        "ok": ok,
        "id": rid,
        "action": action,
        "scheme": scheme,
        "destination": target,
        "returncode": result.returncode,
        "errors": errors,
        "warnings": warnings,
        "log": str(log_path),
        "result_bundle": str(result_path),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    register_result(rid, payload)
    status = "SUCCESS" if ok else "FAILED"
    payload["message"] = f"{action}: {status} ({len(errors)} errors, {len(warnings)} warnings) [{rid}]"
    print_result(payload if args.verbose or args.json else {**payload, "errors": errors[:3], "warnings": warnings[:3]}, json_output=args.json)
    if not ok and not args.json:
        print(f"log={log_path}")
        print(f"result={result_path}")
    raise SystemExit(result.returncode)


def cmd_list_schemes(args: argparse.Namespace) -> None:
    schemes = list_schemes_for(args)
    if args.json:
        print_result({"ok": True, "schemes": schemes}, json_output=True)
        return
    for scheme in schemes:
        print(scheme)


def cmd_list_results(args: argparse.Namespace) -> None:
    index = load_index()
    items = list(index.items())[-args.limit :]
    if args.json:
        print_result({"ok": True, "results": dict(items)}, json_output=True)
        return
    for rid, entry in items:
        print(f"{rid} | {entry.get('action')} | ok={entry.get('ok')} | {entry.get('scheme')} | {entry.get('result_bundle')}")


def xcresulttool(path: str, args: list[str], *, json_output: bool = False) -> str:
    require_tool("xcrun", json_output=json_output)
    cmd = ["xcrun", "xcresulttool", *args, "--path", path]
    result = run_command(cmd, check=False, json_output=json_output)
    return result.stdout if result.returncode == 0 else result.stderr


def cmd_show_result(args: argparse.Namespace) -> None:
    entry = result_entry(args.id, json_output=args.json)
    log_path = Path(entry["log"])
    text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    output: dict[str, Any] = {"ok": True, "id": args.id, "entry": entry}
    if args.errors:
        output["errors"] = diagnostic_lines(text, "error", args.limit)
    elif args.warnings:
        output["warnings"] = diagnostic_lines(text, "warning", args.limit)
    elif args.log:
        output["log"] = text.splitlines()[-args.tail :]
    elif args.all:
        output["errors"] = diagnostic_lines(text, "error", args.limit)
        output["warnings"] = diagnostic_lines(text, "warning", args.limit)
        output["log_tail"] = text.splitlines()[-args.tail :]
    elif args.xcresult_summary:
        output["xcresulttool"] = xcresulttool(entry["result_bundle"], ["get", "test-results", "summary"], json_output=args.json)
    else:
        output["errors"] = entry.get("errors", [])
        output["warnings"] = entry.get("warnings", [])
    if args.json:
        print_result(output, json_output=True)
        return
    if "errors" in output:
        print("\n".join(output["errors"]) or "No errors")
    if "warnings" in output:
        print("\n".join(output["warnings"]) or "No warnings")
    if "log" in output:
        print("\n".join(output["log"]))
    if "log_tail" in output:
        print("\n".join(output["log_tail"]))
    if "xcresulttool" in output:
        print(output["xcresulttool"])


def cmd_show_log(args: argparse.Namespace) -> None:
    path = Path(args.log).expanduser()
    if not path.exists():
        fail(f"Log not found: {path}", json_output=args.json)
    text = path.read_text(encoding="utf-8", errors="replace")
    if args.errors:
        lines = diagnostic_lines(text, "error", args.limit)
    elif args.warnings:
        lines = diagnostic_lines(text, "warning", args.limit)
    else:
        lines = text.splitlines()[-args.tail :]
    if args.json:
        print_result({"ok": True, "log": str(path), "lines": lines, "count": len(lines)}, json_output=True)
        return
    print("\n".join(lines))


def add_project_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace")
    parser.add_argument("--project")
    parser.add_argument("--scheme")
    parser.add_argument("--configuration", default="Debug")
    parser.add_argument("--destination")
    parser.add_argument("--simulator")
    parser.add_argument("--json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Concise xcodebuild wrapper for iOS Simulator")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("build", "test"):
        p = sub.add_parser(name, help=f"Run xcodebuild {name}")
        add_project_args(p)
        p.add_argument("--clean", action="store_true")
        p.add_argument("--test", action="store_true", help="Run tests even from build command")
        p.add_argument("--suite")
        p.add_argument("--timeout", type=int, default=1800)
        p.add_argument("--result-bundle")
        p.add_argument("--log")
        p.add_argument("--diagnostic-limit", type=int, default=12)
        p.add_argument("--only-testing", action="append")
        p.add_argument("--skip-testing", action="append")
        p.add_argument("--verbose", action="store_true")
        p.set_defaults(func=cmd_build_or_test)

    p = sub.add_parser("list-schemes", help="List schemes")
    add_project_args(p)
    p.set_defaults(func=cmd_list_schemes)

    p = sub.add_parser("list-results", help="List cached build/test result bundles")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list_results)

    p = sub.add_parser("show-result", help="Drill into a cached result by id")
    p.add_argument("--id", required=True)
    p.add_argument("--errors", action="store_true")
    p.add_argument("--warnings", action="store_true")
    p.add_argument("--log", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("--xcresult-summary", action="store_true")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--tail", type=int, default=120)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_show_result)

    p = sub.add_parser("show-log", help="Show saved log snippets")
    p.add_argument("--log", required=True)
    p.add_argument("--errors", action="store_true")
    p.add_argument("--warnings", action="store_true")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--tail", type=int, default=120)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_show_log)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
