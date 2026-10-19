#!/usr/bin/env python3
"""Check a repository README against facts the repository can prove.

Usage: check_readme.py REPO [--readme PATH] [--workflow FILE] [--linux auto|yes|no]

PATH is relative to REPO (default README.md).

Categories:
  shadowed   .github/README.md hides the checked root README on the home page
  link       a relative link or image target does not exist
  anchor     an in-page #anchor matches no heading
  alt        an image has no alt attribute, or a Markdown image has empty alt
  install    a .package(url:) for this repository names another owner, a
             version with no matching tag, or a branch that does not exist
  badge      a Swift, platforms, or license badge value differs from repository
             facts or has no backing fact, or a CI badge names a missing workflow
  local-path an absolute home-directory path

Prints "category<TAB>line<TAB>detail" per finding and exits 1 when any exist.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from readme_facts import collect, git  # noqa: E402

FENCE = re.compile(r"^\s*(```|~~~)")
MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_REF = re.compile(r"<(img|a|source)\b[^>]*?\b(src|href|srcset)=\"([^\"]+)\"", re.I)
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
HEADING_MD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HEADING_HTML = re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>", re.I)
PACKAGE = re.compile(
    r"\.package\(\s*url:\s*\"https?://github\.com/([^/\"]+)/([^\"]+?)(?:\.git)?\"\s*,\s*"
    r"(?:(?:from|exact):\s*\"([^\"]+)\"|\.upTo\w+\(\s*from:\s*\"([^\"]+)\"\s*\)"
    r"|\"([^\"]+)\"\s*\.\.[.<]|branch:\s*\"([^\"]+)\"|revision:\s*\"[^\"]+\")",
    re.S,
)
SHIELD = re.compile(r"https://img\.shields\.io/badge/([^\"\s)?]+)")
SHIELD_SEPARATOR = re.compile(r"(?<!-)-(?!-)")
LIST_SEPARATOR = re.compile(r"\s*[|,\u00b7]\s*")
HOME_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)([A-Za-z0-9._-]+)")
PLACEHOLDER_USERS = {"you", "your-name", "username", "user", "me", "name", "runner", "shared"}


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", text)
    return re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")


def prose_lines(lines):
    inside = False
    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            yield number, line


def anchors(lines):
    seen, result = {}, set()
    for _, line in prose_lines(lines):
        texts = []
        match = HEADING_MD.match(line)
        if match:
            texts.append(match.group(2))
        texts += HEADING_HTML.findall(line)
        for text in texts:
            base = slug(text)
            count = seen.get(base, 0)
            result.add(base if count == 0 else f"{base}-{count}")
            seen[base] = count + 1
        result.update(re.findall(r"<a\s+(?:name|id)=\"([^\"]+)\"", line))
    return result


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def shield_fields(path):
    """Label and message of a shields.io static badge path, or None without a label."""
    parts = SHIELD_SEPARATOR.split(path)
    if len(parts) != 3:
        return None

    def decode(part):
        part = part.replace("--", "-").replace("__", "\0").replace("_", " ").replace("\0", "_")
        return urllib.parse.unquote(part).strip()

    return decode(parts[0]), decode(parts[1])


def badge_mismatch(kind, message, values):
    """Why a badge message disagrees with the repository's badge values, or None."""
    if kind not in values:
        return f"{kind} badge has no backing fact"
    expected = values[kind]
    if kind == "swift":
        if message != expected:
            return f"swift badge says {message}, facts say {expected}"
    elif kind == "platforms":
        if set(LIST_SEPARATOR.split(message)) != set(expected):
            return f"platforms badge says {message}, facts say {' | '.join(expected)}"
    elif kind == "license":
        if message not in {expected, expected.split(" WITH ")[0]}:
            return f"license badge says {message}, facts say {expected}"
    return None


def check(root, readme, workflow, linux):
    findings = []
    if readme == root / "README.md" and (root / ".github" / "README.md").exists() and root.name != ".github":
        findings.append(("shadowed", 0, ".github/README.md is shown instead of README.md"))

    text = readme.read_text()
    lines = text.splitlines()
    known = anchors(lines)

    for number, line in prose_lines(lines):
        refs = [(m.group(1), m.group(2), m.group(3)) for m in MD_LINK.finditer(line)]
        refs += [("html", "", m.group(3)) for m in HTML_REF.finditer(line)]
        for bang, alt, target in refs:
            if bang == "!" and not alt.strip():
                findings.append(("alt", number, f"empty alt for {target}"))
            for item in target.split(","):
                item = item.strip().split(" ")[0]
                if not item or re.match(r"^[a-z][a-z0-9+.-]*:", item, re.I):
                    continue
                if item.startswith("#"):
                    if urllib.parse.unquote(item[1:]).lower() not in known:
                        findings.append(("anchor", number, item))
                    continue
                path = urllib.parse.unquote(item.split("#")[0].split("?")[0])
                resolved = (root / path.lstrip("/")) if path.startswith("/") else (readme.parent / path)
                if path and not resolved.exists():
                    findings.append(("link", number, item))
        for tag in IMG_TAG.findall(line):
            if not re.search(r"\balt=", tag, re.I):
                findings.append(("alt", number, "img without alt attribute"))

    for match in HOME_PATH.finditer(text):
        if match.group(1).lower() not in PLACEHOLDER_USERS:
            findings.append(("local-path", line_of(text, match.start()), match.group(0)))

    facts = collect(root, workflow, linux)
    if facts["owner"] and facts["name"]:
        tags = {t.lstrip("v") for t in git(root, "tag", "--list").splitlines()}
        for match in PACKAGE.finditer(text):
            owner, name = match.group(1), match.group(2)
            if name.lower() != facts["name"].lower():
                continue
            number = line_of(text, match.start())
            if owner.lower() != facts["owner"].lower():
                findings.append(("install", number, f"owner {owner}, origin is {facts['owner']}"))
            version = match.group(3) or match.group(4) or match.group(5)
            branch = match.group(6)
            if version and version.lstrip("v") not in tags:
                findings.append(("install", number, f"version {version} has no tag"))
            if branch and not (git(root, "rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{branch}")
                               or git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}")):
                findings.append(("install", number, f"branch {branch} does not exist"))

    for match in SHIELD.finditer(text):
        fields = shield_fields(match.group(1))
        kind = fields[0].lower() if fields else None
        if kind in {"swift", "platforms", "license"}:
            problem = badge_mismatch(kind, fields[1], facts["badges"])
            if problem:
                findings.append(("badge", line_of(text, match.start()), problem))
    for match in re.finditer(r"actions/workflows/([^/\"]+)/badge\.svg", text):
        if not (root / ".github" / "workflows" / match.group(1)).exists():
            findings.append(("badge", line_of(text, match.start()), f"workflow {match.group(1)} not found"))
    return findings


def main(argv):
    parser = argparse.ArgumentParser(description="Check a README against repository facts.")
    parser.add_argument("repo", type=pathlib.Path)
    parser.add_argument("--readme", type=pathlib.Path, default=pathlib.Path("README.md"),
                        help="README to check, relative to REPO (default README.md)")
    parser.add_argument("--workflow", help="CI workflow file name under .github/workflows")
    parser.add_argument("--linux", choices=("auto", "yes", "no"), default="auto",
                        help="Linux detection passed to readme_facts.py")
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    readme = (root / args.readme).resolve()
    if not readme.exists():
        sys.exit(f"error: {readme} not found")
    findings = check(root, readme, args.workflow, args.linux)
    for category, number, detail in findings:
        print(f"{category}\t{number}\t{detail}")
    print(f"{len(findings)} findings", file=sys.stderr)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
