#!/usr/bin/env python3
"""Build a README Quick start the way a new user would.

Usage:
  quickstart_check.py REPO [--product NAME ...] [--section TITLE] [--local]
                      [--run] [--destination DEST] [--work DIR] [--keep]

Reads the README's .package(url:) line for this repository and the first
```swift block under the Quick start section, writes a scratch consumer
package that depends on the published URL with the same requirement, and
builds it. --local depends on the working tree instead, for checks before
publishing. --destination builds with xcodebuild for that destination, for
snippets that need a platform other than the host.

Exit codes: 0 build passed, 1 build failed, 2 README or repository input missing.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from readme_facts import collect  # noqa: E402

URL_ARGUMENT = re.compile(r"\s*url:\s*\"(https?://github\.com/([^/\"]+)/([^\"]+?)(?:\.git)?)\"\s*,\s*(.+?)\s*$",
                          re.S)
PRODUCT = re.compile(r"\.product\(\s*name:\s*\"([^\"]+)\"\s*,\s*package:\s*\"([^\"]+)\"\s*\)")


def fail(message, code=2):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(code)


def package_calls(text):
    for match in re.finditer(r"\.package\(", text):
        depth, index = 1, match.end()
        while index < len(text) and depth:
            depth += {"(": 1, ")": -1}.get(text[index], 0)
            index += 1
        yield text[match.end():index - 1]


def package_line(readme, name):
    for arguments in package_calls(readme):
        found = URL_ARGUMENT.match(arguments)
        if found and found.group(3).lower() == name.lower():
            return found.group(1), re.sub(r"\s+", " ", found.group(4))
    return None, None


def section_code(readme, title):
    lines = readme.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.match(rf"^##\s+{re.escape(title)}\s*$", line, re.I)), None)
    if start is None:
        return None
    block, inside = [], False
    for line in lines[start + 1:]:
        if not inside and re.match(r"^##\s", line):
            break
        if not inside and re.match(r"^\s*```swift\s*$", line):
            inside = True
            continue
        if inside and re.match(r"^\s*```\s*$", line):
            return "\n".join(block) + "\n"
        if inside:
            block.append(line)
    return None


def platforms_block(root):
    text = (root / "Package.swift").read_text()
    match = re.search(r"platforms:\s*\[(.*?)\]", text, re.S)
    return f"platforms: [{match.group(1).strip()}]," if match else ""


def write_consumer(work, tools, platforms, dependency, identity, products, code):
    deps = ", ".join(f'.product(name: "{p}", package: "{identity}")' for p in products)
    (work / "Sources" / "QuickStart").mkdir(parents=True)
    (work / "Package.swift").write_text(
        f"// swift-tools-version:{tools}\n"
        "import PackageDescription\n\n"
        "let package = Package(\n"
        '  name: "QuickStartConsumer",\n'
        f"  {platforms}\n"
        f"  dependencies: [{dependency}],\n"
        f'  targets: [.executableTarget(name: "QuickStart", dependencies: [{deps}])]\n'
        ")\n")
    filename = "QuickStart.swift" if "@main" in code else "main.swift"
    (work / "Sources" / "QuickStart" / filename).write_text(code)


def run(command, cwd):
    print("$ " + " ".join(command), file=sys.stderr)
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def main(argv):
    parser = argparse.ArgumentParser(description="Build a README Quick start in a scratch consumer.")
    parser.add_argument("repo", type=pathlib.Path)
    parser.add_argument("--product", action="append", default=[], help="product to depend on (repeatable)")
    parser.add_argument("--section", default="Quick start", help="README section holding the snippet")
    parser.add_argument("--local", action="store_true", help="depend on the working tree, not the URL")
    parser.add_argument("--run", action="store_true", help="run the built executable and print its output")
    parser.add_argument("--destination", help="build with xcodebuild for this destination")
    parser.add_argument("--work", type=pathlib.Path, help="consumer directory (default: a temp dir)")
    parser.add_argument("--keep", action="store_true", help="keep the consumer directory")
    args = parser.parse_args(argv)

    root = args.repo.resolve()
    readme_path = root / "README.md"
    if not readme_path.exists() or not (root / "Package.swift").exists():
        fail("REPO needs README.md and Package.swift")
    readme = readme_path.read_text()
    facts = collect(root)
    if not facts["name"]:
        fail("origin is not a GitHub remote")

    url, requirement = package_line(readme, facts["name"])
    if not url and not args.local:
        fail(f"README has no .package(url:) line for {facts['name']}")
    code = section_code(readme, args.section)
    if code is None:
        fail(f'no ```swift block under "## {args.section}"')
    if re.search(r"\bPackage\(|\.package\(", code):
        fail("the Quick start block is a manifest snippet, not code to build")
    products = args.product or sorted({p for p, pkg in PRODUCT.findall(readme)
                                       if pkg.lower() == facts["name"].lower()})
    if not products:
        fail("no .product(name:package:) for this repository in the README; pass --product")

    if args.local:
        identity = root.name.lower()
        dependency = f'.package(path: "{root}")'
    else:
        identity = facts["name"].lower()
        dependency = f'.package(url: "{url}", {requirement})'

    work = args.work.resolve() if args.work else pathlib.Path(tempfile.mkdtemp(prefix="quickstart-"))
    if work.exists() and any(work.iterdir()):
        fail(f"{work} is not empty")
    work.mkdir(parents=True, exist_ok=True)
    tools = facts["swift_tools"] or "5.9"
    write_consumer(work, tools, platforms_block(root), dependency, identity, products, code)
    print(f"consumer: {work}", file=sys.stderr)
    print(f"dependency: {dependency}", file=sys.stderr)
    print(f"products: {', '.join(products)}", file=sys.stderr)

    if args.destination:
        result = run(["xcodebuild", "-scheme", "QuickStart", "-destination", args.destination,
                      "-derivedDataPath", ".build/xcode", "-skipPackagePluginValidation", "build"], work)
    else:
        result = run(["swift", "build"], work)
    output = result.stdout + result.stderr
    ok = result.returncode == 0
    if ok and args.run and not args.destination:
        executed = run(["swift", "run", "-q", "QuickStart"], work)
        print(executed.stdout, end="")
        ok = executed.returncode == 0
        output += executed.stderr
    if not ok:
        errors = [line for line in output.splitlines() if "error:" in line][:10]
        print("\n".join(errors or output.splitlines()[-20:]), file=sys.stderr)
    print("PASS" if ok else "FAIL")
    if not args.keep and not args.work:
        shutil.rmtree(work, ignore_errors=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
