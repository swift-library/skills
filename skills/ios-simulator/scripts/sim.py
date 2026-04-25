#!/usr/bin/env python3
"""iOS Simulator helper backed by xcrun simctl."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from tool_common import (
    bool_text,
    devices_matching,
    ensure_parent,
    fail,
    list_device_types,
    list_runtimes,
    list_simulators,
    parse_duration,
    print_result,
    resolve_device,
    run_command,
)


STATUS_PRESETS = {
    "clean": {"time": "9:41", "battery_level": 100, "battery_state": "charged", "wifi_bars": 3, "cellular_bars": 4},
    "testing": {"time": "11:11", "battery_level": 50, "battery_state": "discharging", "wifi_bars": 3, "cellular_bars": 4},
    "low-battery": {"time": "9:41", "battery_level": 20, "battery_state": "discharging", "wifi_bars": 2, "cellular_bars": 3},
    "airplane": {"time": "9:41", "battery_level": 100, "battery_state": "charged", "wifi_bars": 0, "cellular_bars": 0},
}


def cmd_list(args: argparse.Namespace) -> None:
    devices = list_simulators(json_output=args.json, platform=None if args.all_platforms else "iOS")
    if args.device_type:
        devices = [d for d in devices if args.device_type.lower() in str(d["name"]).lower()]
    if args.runtime:
        devices = [d for d in devices if args.runtime.lower() in str(d["runtime"]).lower()]
    if not args.all:
        devices = [d for d in devices if d["isAvailable"]]
    if args.json:
        print_result({"ok": True, "devices": devices}, json_output=True)
        return
    for d in devices:
        print(f"{d['name']} | {d['state']} | {d['udid']} | {d['runtime']} | available={bool_text(d['isAvailable'])}")


def cmd_suggest(args: argparse.Namespace) -> None:
    devices = list_simulators(json_output=args.json)
    booted = [d for d in devices if d["state"] == "Booted" and d["isAvailable"]]
    iphones = [d for d in devices if d["isAvailable"] and "iPhone" in str(d["name"])]
    ipads = [d for d in devices if d["isAvailable"] and "iPad" in str(d["name"])]
    suggestions = (booted + iphones + ipads)[: args.count]
    if args.json:
        print_result({"ok": True, "suggestions": suggestions}, json_output=True)
        return
    for d in suggestions:
        marker = "booted" if d["state"] == "Booted" else "available"
        print(f"{d['name']} | {marker} | {d['udid']}")


def resolve_device_type(value: str, *, json_output: bool) -> str:
    if value.startswith("com.apple.CoreSimulator.SimDeviceType."):
        return value
    matches = [t for t in list_device_types(json_output=json_output) if value.lower() in str(t.get("name", "")).lower()]
    if not matches:
        fail(f"No device type matches '{value}'. Use create --list-devices.", json_output=json_output)
    exact = [t for t in matches if str(t.get("name", "")).lower() == value.lower()]
    match = exact[0] if len(exact) == 1 else matches[0]
    if len(matches) > 1 and not exact:
        summary = "\n".join(f"- {m.get('name')} | {m.get('identifier')}" for m in matches[:10])
        fail(f"Multiple device types match '{value}':\n{summary}", json_output=json_output)
    return str(match["identifier"])


def resolve_runtime(value: str, *, json_output: bool) -> str:
    if value.startswith("com.apple.CoreSimulator.SimRuntime."):
        return value
    normalized = value.lower().replace(" ", "-")
    matches = [
        r
        for r in list_runtimes(json_output=json_output)
        if value.lower() in str(r.get("name", "")).lower()
        or normalized in str(r.get("identifier", "")).lower()
        or value.lower() in str(r.get("version", "")).lower()
    ]
    matches = [r for r in matches if r.get("isAvailable", True)]
    if not matches:
        fail(f"No iOS runtime matches '{value}'. Use create --list-runtimes.", json_output=json_output)
    exact = [r for r in matches if str(r.get("name", "")).lower() == value.lower()]
    match = exact[0] if len(exact) == 1 else matches[0]
    if len(matches) > 1 and not exact:
        summary = "\n".join(f"- {m.get('name')} | {m.get('identifier')}" for m in matches[:10])
        fail(f"Multiple runtimes match '{value}':\n{summary}", json_output=json_output)
    return str(match["identifier"])


def cmd_create(args: argparse.Namespace) -> None:
    if args.list_devices:
        types = list_device_types(json_output=args.json)
        if args.json:
            print_result({"ok": True, "device_types": types}, json_output=True)
        else:
            for item in types:
                print(f"{item.get('name')} | {item.get('identifier')}")
        return
    if args.list_runtimes:
        runtimes = list_runtimes(json_output=args.json)
        if args.json:
            print_result({"ok": True, "runtimes": runtimes}, json_output=True)
        else:
            for item in runtimes:
                print(f"{item.get('name')} | {item.get('identifier')} | available={bool_text(bool(item.get('isAvailable', True)))}")
        return
    if not args.device_type or not args.runtime:
        fail("create requires --device-type and --runtime, or --list-devices/--list-runtimes", json_output=args.json)
    device_type = resolve_device_type(args.device_type, json_output=args.json)
    runtime = resolve_runtime(args.runtime, json_output=args.json)
    name = args.name or f"{args.device_type} Test"
    result = run_command(["xcrun", "simctl", "create", name, device_type, runtime], timeout=args.timeout, json_output=args.json)
    udid = result.stdout.strip()
    print_result({"ok": True, "name": name, "udid": udid, "message": f"Created simulator {name}: {udid}"}, json_output=args.json)


def device_targets(args: argparse.Namespace) -> list[str]:
    if getattr(args, "all", False):
        matches = devices_matching(all_devices=False, json_output=args.json)
    elif getattr(args, "type", None):
        matches = devices_matching(device_type=args.type, json_output=args.json)
    elif getattr(args, "booted", False):
        matches = devices_matching(booted_only=True, json_output=args.json)
    else:
        identifier = getattr(args, "udid", None) or getattr(args, "name", None) or getattr(args, "device", None)
        if not identifier:
            fail("Specify --device, --udid, --name, --all, --type, or --booted", json_output=args.json)
        return [resolve_device(identifier, json_output=args.json)]
    if not matches:
        fail("No matching simulators", json_output=args.json)
    return [str(d["udid"]) for d in matches]


def device_arg(args: argparse.Namespace) -> str | None:
    return getattr(args, "udid", None) or getattr(args, "device", None)


def cmd_boot(args: argparse.Namespace) -> None:
    targets = device_targets(args)
    statuses = []
    for device in targets:
        result = run_command(["xcrun", "simctl", "boot", device], check=False, timeout=args.timeout, json_output=args.json)
        already_booted = "Unable to boot device in current state: Booted" in result.stderr
        if result.returncode != 0 and not already_booted:
            detail = result.stderr.strip() or result.stdout.strip()
            fail(f"Failed to boot {device}: {detail}", json_output=args.json)
        if args.wait or args.verify:
            run_command(["xcrun", "simctl", "bootstatus", device, "-b"], timeout=args.timeout, json_output=args.json)
        statuses.append({"device": device, "already_booted": already_booted})
    print_result({"ok": True, "devices": statuses, "message": f"Booted {len(statuses)} simulator(s)"}, json_output=args.json)


def cmd_shutdown(args: argparse.Namespace) -> None:
    targets = device_targets(args)
    for device in targets:
        run_command(["xcrun", "simctl", "shutdown", device], check=False, timeout=args.timeout, json_output=args.json)
    if args.verify:
        deadline = time.time() + args.timeout
        remaining = set(targets)
        while remaining and time.time() < deadline:
            states = {d["udid"]: d["state"] for d in list_simulators(json_output=args.json)}
            remaining = {udid for udid in remaining if states.get(udid) != "Shutdown"}
            if remaining:
                time.sleep(1)
    print_result({"ok": True, "devices": targets, "message": f"Shutdown requested for {len(targets)} simulator(s)"}, json_output=args.json)


def cmd_erase(args: argparse.Namespace) -> None:
    if not args.yes:
        fail("erase requires --yes", json_output=args.json)
    targets = device_targets(args)
    for device in targets:
        run_command(["xcrun", "simctl", "erase", device], timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "devices": targets, "message": f"Erased {len(targets)} simulator(s)"}, json_output=args.json)


def cmd_delete(args: argparse.Namespace) -> None:
    if not args.yes:
        fail("delete requires --yes", json_output=args.json)
    if args.old is not None:
        devices = [d for d in list_simulators(json_output=args.json) if d["isAvailable"]]
        grouped: dict[str, list[dict[str, Any]]] = {}
        for device in devices:
            grouped.setdefault(str(device["name"]), []).append(device)
        targets = []
        for group in grouped.values():
            ordered = sorted(group, key=lambda d: str(d.get("runtime", "")), reverse=True)
            targets.extend(str(d["udid"]) for d in ordered[args.old :])
    else:
        targets = device_targets(args)
    for device in targets:
        run_command(["xcrun", "simctl", "delete", device], timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "devices": targets, "message": f"Deleted {len(targets)} simulator(s)"}, json_output=args.json)


def cmd_install(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    app = Path(args.app).expanduser()
    if not app.exists():
        fail(f"App bundle not found: {app}", json_output=args.json)
    run_command(["xcrun", "simctl", "install", device, str(app)], timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "app": str(app), "message": f"Installed {app.name} on {device}"}, json_output=args.json)


def cmd_app_list(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    result = run_command(["xcrun", "simctl", "listapps", device], json_output=args.json)
    apps: object = result.stdout
    convert = run_command(["plutil", "-convert", "json", "-o", "-", "-"], input_text=result.stdout, check=False, json_output=args.json)
    if convert.returncode == 0:
        try:
            apps = json.loads(convert.stdout)
        except json.JSONDecodeError:
            apps = result.stdout
    if args.json:
        print_result({"ok": True, "device": device, "apps": apps}, json_output=True)
        return
    if isinstance(apps, dict):
        for bundle_id in sorted(apps):
            print(bundle_id)
    else:
        print(apps)


def cmd_launch(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    cmd = ["xcrun", "simctl", "launch"]
    if args.wait_for_debugger:
        cmd.append("--wait-for-debugger")
    cmd.extend([device, args.bundle_id])
    result = run_command(cmd, timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "bundle_id": args.bundle_id, "stdout": result.stdout.strip(), "message": f"Launched {args.bundle_id} on {device}"}, json_output=args.json)


def cmd_restart(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    run_command(["xcrun", "simctl", "terminate", device, args.bundle_id], check=False, timeout=args.timeout, json_output=args.json)
    result = run_command(["xcrun", "simctl", "launch", device, args.bundle_id], timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "bundle_id": args.bundle_id, "stdout": result.stdout.strip(), "message": f"Restarted {args.bundle_id} on {device}"}, json_output=args.json)


def bundle_command(args: argparse.Namespace, operation: str, label: str) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    run_command(["xcrun", "simctl", operation, device, args.bundle_id], timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "bundle_id": args.bundle_id, "message": f"{label} {args.bundle_id} on {device}"}, json_output=args.json)


def cmd_terminate(args: argparse.Namespace) -> None:
    bundle_command(args, "terminate", "Terminated")


def cmd_uninstall(args: argparse.Namespace) -> None:
    bundle_command(args, "uninstall", "Uninstalled")


def cmd_app_state(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    result = run_command(["xcrun", "simctl", "spawn", device, "launchctl", "list"], json_output=args.json)
    running = args.bundle_id in result.stdout
    print_result({"ok": True, "device": device, "bundle_id": args.bundle_id, "running": running, "message": f"{args.bundle_id} running={bool_text(running)}"}, json_output=args.json)


def cmd_open_url(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    run_command(["xcrun", "simctl", "openurl", device, args.url], timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "url": args.url, "message": f"Opened URL on {device}: {args.url}"}, json_output=args.json)


def cmd_screenshot(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    output = ensure_parent(args.output)
    cmd = ["xcrun", "simctl", "io", device, "screenshot"]
    if args.image_type:
        cmd.append(f"--type={args.image_type}")
    cmd.append(str(output))
    run_command(cmd, timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "output": str(output), "message": f"Screenshot saved: {output}"}, json_output=args.json)


def run_stream(cmd: list[str], seconds: int, *, json_output: bool) -> tuple[str, str, int]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        stdout, stderr = proc.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode or 0


def cmd_logs(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    mode = "stream" if args.follow or args.duration else "show"
    cmd = ["xcrun", "simctl", "spawn", device, "log", mode, "--style", "compact"]
    if mode == "show":
        cmd.extend(["--last", args.last])
    if args.process:
        cmd.extend(["--predicate", f'processImagePath CONTAINS "{args.process}"'])
    elif args.predicate:
        cmd.extend(["--predicate", args.predicate])
    if args.severity and not args.process and not args.predicate:
        predicates = [f'eventMessage CONTAINS[c] "{level.strip()}"' for level in args.severity.split(",") if level.strip()]
        if predicates:
            cmd.extend(["--predicate", " OR ".join(predicates)])

    if mode == "stream":
        stdout, stderr, code = run_stream(cmd, parse_duration(args.duration, default_seconds=args.timeout), json_output=args.json)
        result_stdout = stdout
    else:
        result = run_command(cmd, timeout=args.timeout, json_output=args.json)
        result_stdout = result.stdout
        code = result.returncode
    lines = result_stdout.splitlines()
    if args.tail and len(lines) > args.tail:
        lines = lines[-args.tail :]
    output = None
    if args.output:
        output = ensure_parent(Path(args.output) / f"simulator-log-{int(time.time())}.log")
        output.write_text("\n".join(lines), encoding="utf-8")
    if args.json:
        print_result({"ok": code == 0, "device": device, "lines": lines, "count": len(lines), "output": str(output) if output else None}, json_output=True)
        return
    print("\n".join(lines))
    if output:
        print(f"\nSaved log: {output}")


def cmd_privacy(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    if args.list:
        services = ["all", "calendar", "camera", "contacts", "faceid", "health", "homekit", "location", "media-library", "microphone", "motion", "photos", "reminders", "siri"]
        print_result({"ok": True, "services": services}, json_output=args.json)
        return
    if args.grant:
        action = "grant"
        service = args.grant
    elif args.revoke:
        action = "revoke"
        service = args.revoke
    elif args.reset:
        action = "reset"
        service = args.reset
    else:
        fail("privacy requires --grant, --revoke, --reset, or --list", json_output=args.json)
    services = [item.strip() for item in service.split(",") if item.strip()]
    for item in services:
        cmd = ["xcrun", "simctl", "privacy", device, action, item]
        if args.bundle_id:
            cmd.append(args.bundle_id)
        run_command(cmd, timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "action": action, "services": services, "bundle_id": args.bundle_id, "message": f"Privacy {action} {','.join(services)} on {device}"}, json_output=args.json)


def cmd_clipboard(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    run_command(["xcrun", "simctl", "pbcopy", device], input_text=args.copy, timeout=args.timeout, json_output=args.json)
    data = {"ok": True, "device": device, "message": "Copied text to simulator clipboard"}
    if args.test_name:
        data["test_name"] = args.test_name
    if args.expected:
        data["expected"] = args.expected
    print_result(data, json_output=args.json)


def cmd_push(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    payload_path: Path | None = Path(args.payload).expanduser() if args.payload else None
    temp_name: str | None = None
    if payload_path is None:
        payload = {
            "Simulator Target Bundle": args.bundle_id,
            "aps": {"alert": {"title": args.title or "", "body": args.body or ""}},
        }
        if args.badge is not None:
            payload["aps"]["badge"] = args.badge
        if not args.no_sound:
            payload["aps"]["sound"] = args.sound or "default"
        tmp = tempfile.NamedTemporaryFile("w", suffix=".apns", delete=False)
        json.dump(payload, tmp)
        tmp.close()
        temp_name = tmp.name
        payload_path = Path(temp_name)
    if not payload_path.exists():
        fail(f"Payload not found: {payload_path}", json_output=args.json)
    run_command(["xcrun", "simctl", "push", device, args.bundle_id, str(payload_path)], timeout=args.timeout, json_output=args.json)
    if temp_name:
        Path(temp_name).unlink(missing_ok=True)
    print_result({"ok": True, "device": device, "bundle_id": args.bundle_id, "message": f"Sent push to {args.bundle_id} on {device}"}, json_output=args.json)


def cmd_status_bar(args: argparse.Namespace) -> None:
    device = resolve_device(device_arg(args), json_output=args.json)
    if args.clear:
        run_command(["xcrun", "simctl", "status_bar", device, "clear"], timeout=args.timeout, json_output=args.json)
        print_result({"ok": True, "device": device, "message": f"Cleared status bar on {device}"}, json_output=args.json)
        return
    preset = STATUS_PRESETS.get(args.preset or "", {})
    for attr, value in preset.items():
        if getattr(args, attr) is None:
            setattr(args, attr, value)
    cmd = ["xcrun", "simctl", "status_bar", device, "override"]
    for flag, value in (
        ("--time", args.time),
        ("--dataNetwork", args.data_network),
        ("--wifiMode", args.wifi_mode),
        ("--batteryLevel", args.battery_level),
        ("--batteryState", args.battery_state),
        ("--wifiBars", args.wifi_bars),
        ("--cellularBars", args.cellular_bars),
        ("--operatorName", args.operator_name),
    ):
        if value is not None:
            cmd.extend([flag, str(value)])
    run_command(cmd, timeout=args.timeout, json_output=args.json)
    print_result({"ok": True, "device": device, "message": f"Overrode status bar on {device}"}, json_output=args.json)


def cmd_health(args: argparse.Namespace) -> None:
    checks = []
    for tool in ("xcrun", "xcodebuild", "python3"):
        result = subprocess.run(["/usr/bin/which", tool], capture_output=True, text=True, check=False)
        checks.append({"tool": tool, "ok": result.returncode == 0, "path": result.stdout.strip()})
    idb = subprocess.run(["/usr/bin/which", "idb"], capture_output=True, text=True, check=False)
    checks.append({"tool": "idb", "ok": idb.returncode == 0, "path": idb.stdout.strip(), "optional": True})
    try:
        import PIL  # type: ignore

        pillow = True
    except Exception:
        pillow = False
    booted = [d for d in list_simulators(json_output=args.json) if d["state"] == "Booted"]
    data = {
        "ok": all(c["ok"] for c in checks if not c.get("optional")),
        "checks": checks,
        "pillow": pillow,
        "booted": booted,
        "message": f"health: {len(booted)} booted iOS simulator(s), idb={bool_text(idb.returncode == 0)}, pillow={bool_text(pillow)}",
    }
    print_result(data, json_output=args.json)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--device", default="booted", help="Simulator UDID, name, or booted")
    parser.add_argument("--udid", help="Simulator UDID alias")
    parser.add_argument("--timeout", type=int, default=60, help="Command timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Emit JSON")


def add_target_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--name")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--type")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="iOS Simulator helper backed by xcrun simctl")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="List simulator devices")
    p.add_argument("--all", action="store_true", help="Include unavailable devices")
    p.add_argument("--all-platforms", action="store_true", help="Include non-iOS simulator runtimes")
    p.add_argument("--device-type")
    p.add_argument("--runtime")
    p.add_argument("--json", action="store_true", help="Emit JSON")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("suggest", help="Suggest useful simulator targets")
    p.add_argument("--count", type=int, default=3)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_suggest)

    p = sub.add_parser("create", help="Create a simulator or list create inputs")
    p.add_argument("--device-type", "--device", dest="device_type")
    p.add_argument("--runtime")
    p.add_argument("--name")
    p.add_argument("--list-devices", action="store_true")
    p.add_argument("--list-runtimes", action="store_true")
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("boot", help="Boot simulator(s)")
    add_common(p)
    add_target_args(p)
    p.add_argument("--wait", "--wait-ready", action="store_true", dest="wait")
    p.add_argument("--verify", action="store_true")
    p.set_defaults(func=cmd_boot)

    p = sub.add_parser("shutdown", help="Shutdown simulator(s)")
    add_common(p)
    add_target_args(p)
    p.add_argument("--verify", action="store_true")
    p.set_defaults(func=cmd_shutdown)

    p = sub.add_parser("erase", help="Erase simulator(s)")
    add_common(p)
    add_target_args(p)
    p.add_argument("--booted", action="store_true")
    p.add_argument("--verify", action="store_true")
    p.add_argument("--yes", action="store_true", help="Confirm erase")
    p.set_defaults(func=cmd_erase)

    p = sub.add_parser("delete", help="Delete simulator(s)")
    add_common(p)
    add_target_args(p)
    p.add_argument("--old", type=int, help="Delete older simulators, keeping N per name")
    p.add_argument("--yes", action="store_true", help="Confirm delete")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("install", help="Install an .app bundle")
    add_common(p)
    p.add_argument("--app", required=True, help="Path to .app bundle")
    p.set_defaults(func=cmd_install)

    p = sub.add_parser("app-list", help="List installed apps")
    add_common(p)
    p.set_defaults(func=cmd_app_list)

    for name, func, help_text in (
        ("launch", cmd_launch, "Launch an installed app"),
        ("restart", cmd_restart, "Restart an app"),
        ("terminate", cmd_terminate, "Terminate an app"),
        ("uninstall", cmd_uninstall, "Uninstall an app"),
    ):
        p = sub.add_parser(name, help=help_text)
        add_common(p)
        p.add_argument("--bundle-id", required=True)
        if name == "launch":
            p.add_argument("--wait-for-debugger", action="store_true")
        p.set_defaults(func=func)

    p = sub.add_parser("app-state", help="Check whether an app appears running")
    add_common(p)
    p.add_argument("--bundle-id", required=True)
    p.set_defaults(func=cmd_app_state)

    p = sub.add_parser("open-url", help="Open a URL in the simulator")
    add_common(p)
    p.add_argument("--url", required=True)
    p.set_defaults(func=cmd_open_url)

    p = sub.add_parser("screenshot", help="Capture a screenshot")
    add_common(p)
    p.add_argument("--output", required=True)
    p.add_argument("--image-type", choices=["png", "jpeg"])
    p.set_defaults(func=cmd_screenshot)

    p = sub.add_parser("logs", help="Show or stream simulator logs")
    add_common(p)
    p.add_argument("--last", default="5m")
    p.add_argument("--process")
    p.add_argument("--predicate")
    p.add_argument("--severity", help="Comma-separated severity hints")
    p.add_argument("--follow", action="store_true")
    p.add_argument("--duration", help="Capture duration like 30s, 5m, 1h")
    p.add_argument("--output", help="Output directory")
    p.add_argument("--tail", type=int, default=120)
    p.set_defaults(func=cmd_logs)

    p = sub.add_parser("privacy", help="Grant, revoke, reset, or list permissions")
    add_common(p)
    p.add_argument("--bundle-id")
    p.add_argument("--scenario")
    p.add_argument("--step", type=int)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--grant")
    group.add_argument("--revoke")
    group.add_argument("--reset")
    group.add_argument("--list", action="store_true")
    p.set_defaults(func=cmd_privacy)

    p = sub.add_parser("clipboard", help="Copy text to simulator clipboard")
    add_common(p)
    p.add_argument("--copy", required=True)
    p.add_argument("--test-name")
    p.add_argument("--expected")
    p.set_defaults(func=cmd_clipboard)

    p = sub.add_parser("push", help="Send a simulated push notification")
    add_common(p)
    p.add_argument("--bundle-id", required=True)
    p.add_argument("--payload", help="Path to .apns payload")
    p.add_argument("--title")
    p.add_argument("--body")
    p.add_argument("--badge", type=int)
    p.add_argument("--sound")
    p.add_argument("--no-sound", action="store_true")
    p.add_argument("--test-name")
    p.add_argument("--expected")
    p.set_defaults(func=cmd_push)

    p = sub.add_parser("status-bar", help="Override or clear the status bar")
    add_common(p)
    p.add_argument("--preset", choices=sorted(STATUS_PRESETS))
    p.add_argument("--clear", action="store_true")
    p.add_argument("--time")
    p.add_argument("--data-network")
    p.add_argument("--wifi-mode")
    p.add_argument("--battery-level", type=int)
    p.add_argument("--battery-state", choices=["charging", "charged", "discharging"])
    p.add_argument("--wifi-bars", type=int)
    p.add_argument("--cellular-bars", type=int)
    p.add_argument("--operator-name")
    p.set_defaults(func=cmd_status_bar)

    p = sub.add_parser("health", help="Check simulator tool environment")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_health)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
