#!/usr/bin/env python3
"""Shared helpers for iOS Simulator scripts."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


UDID_RE = re.compile(r"^[0-9A-Fa-f-]{36}$")


@dataclass
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


def fail(message: str, code: int = 1, *, json_output: bool = False) -> None:
    if json_output:
        print(json.dumps({"ok": False, "error": message}, indent=2))
    else:
        print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def require_tool(name: str, *, json_output: bool = False) -> str:
    path = shutil.which(name)
    if not path:
        fail(f"Required tool not found: {name}", json_output=json_output)
    return path


def run_command(
    args: list[str],
    *,
    check: bool = True,
    timeout: int | None = None,
    input_text: str | None = None,
    json_output: bool = False,
) -> CommandResult:
    try:
        proc = subprocess.run(
            args,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        fail(f"Command timed out: {' '.join(args)}", code=124, json_output=json_output)
    result = CommandResult(args, proc.returncode, proc.stdout, proc.stderr)
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        fail(
            f"Command failed ({result.returncode}): {' '.join(args)}\n{detail}",
            code=result.returncode,
            json_output=json_output,
        )
    return result


def print_result(data: dict[str, Any], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    message = data.get("message")
    if message:
        print(message)
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


def simctl_json(*args: str, json_output: bool = False) -> dict[str, Any]:
    require_tool("xcrun", json_output=json_output)
    result = run_command(["xcrun", "simctl", *args], json_output=json_output)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON from simctl: {exc}", json_output=json_output)


def parse_duration(value: str | None, *, default_seconds: int = 0) -> int:
    if not value:
        return default_seconds
    match = re.fullmatch(r"(\d+)([smh]?)", value.strip())
    if not match:
        raise ValueError(f"Invalid duration: {value}")
    amount = int(match.group(1))
    unit = match.group(2) or "s"
    if unit == "h":
        return amount * 3600
    if unit == "m":
        return amount * 60
    return amount


def list_simulators(
    *,
    json_output: bool = False,
    platform: str | None = "iOS",
) -> list[dict[str, Any]]:
    payload = simctl_json("list", "devices", "--json", json_output=json_output)
    devices: list[dict[str, Any]] = []
    for runtime, entries in payload.get("devices", {}).items():
        if platform and f"SimRuntime.{platform}-" not in runtime:
            continue
        for entry in entries:
            devices.append(
                {
                    "name": entry.get("name"),
                    "udid": entry.get("udid"),
                    "state": entry.get("state"),
                    "isAvailable": bool(entry.get("isAvailable", True)),
                    "runtime": runtime,
                }
            )
    return devices


def list_device_types(*, json_output: bool = False, platform: str | None = "iOS") -> list[dict[str, Any]]:
    payload = simctl_json("list", "devicetypes", "--json", json_output=json_output)
    types = payload.get("devicetypes", [])
    if platform:
        types = [t for t in types if platform.lower() in str(t.get("productFamily", "")).lower()]
    return list(types)


def list_runtimes(*, json_output: bool = False, platform: str | None = "iOS") -> list[dict[str, Any]]:
    payload = simctl_json("list", "runtimes", "--json", json_output=json_output)
    runtimes = payload.get("runtimes", [])
    if platform:
        runtimes = [
            r
            for r in runtimes
            if platform.lower() in str(r.get("platform", "")).lower()
            or f"SimRuntime.{platform}-" in str(r.get("identifier", ""))
        ]
    return list(runtimes)


def first_booted_device(*, json_output: bool = False) -> dict[str, Any] | None:
    for device in list_simulators(json_output=json_output):
        if device.get("state") == "Booted":
            return device
    return None


def devices_matching(
    *,
    identifier: str | None = None,
    device_type: str | None = None,
    all_devices: bool = False,
    booted_only: bool = False,
    json_output: bool = False,
) -> list[dict[str, Any]]:
    devices = list_simulators(json_output=json_output)
    if not all_devices:
        devices = [d for d in devices if d.get("isAvailable")]
    if booted_only:
        devices = [d for d in devices if d.get("state") == "Booted"]
    if identifier:
        if UDID_RE.match(identifier):
            devices = [d for d in devices if str(d.get("udid", "")).upper() == identifier.upper()]
        else:
            lowered = identifier.lower()
            devices = [d for d in devices if lowered in str(d.get("name", "")).lower()]
    if device_type:
        lowered = device_type.lower()
        devices = [d for d in devices if lowered in str(d.get("name", "")).lower()]
    return devices


def resolve_device(identifier: str | None, *, json_output: bool = False) -> str:
    if not identifier or identifier == "booted":
        return "booted"
    if UDID_RE.match(identifier):
        return identifier.upper()

    devices = list_simulators(json_output=json_output)
    matches = [
        d
        for d in devices
        if d.get("name") and identifier.lower() in str(d["name"]).lower()
    ]
    available = [d for d in matches if d.get("isAvailable")]
    matches = available or matches
    if not matches:
        fail(f"No simulator matches '{identifier}'", json_output=json_output)
    if len(matches) > 1:
        exact = [d for d in matches if str(d.get("name", "")).lower() == identifier.lower()]
        if len(exact) == 1:
            return str(exact[0]["udid"])
        summary = "\n".join(
            f"- {d['name']} {d['state']} {d['udid']} ({d['runtime']})" for d in matches[:10]
        )
        fail(f"Multiple simulators match '{identifier}':\n{summary}", json_output=json_output)
    return str(matches[0]["udid"])


def ensure_parent(path: str | Path) -> Path:
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def bool_text(value: bool) -> str:
    return "yes" if value else "no"
