#!/usr/bin/env python3
"""Check a repository README against facts the repository can prove.

Usage: check_readme.py REPO [--readme PATH] [--workflow FILE] [--linux auto|yes|no]

Categories:
  shadowed   .github/README.md hides the root README on the home page
  link       a relative link or image target does not exist
  anchor     an in-page #anchor matches no heading
  alt        an image has no alt attribute, or a Markdown image has empty alt
  emoji      emoji outside code blocks
  install    a .package(url:) for this repository names another owner, a
             version with no matching tag, or a branch that does not exist
  badge      a Swift, platforms, or license badge differs from repository facts,
             or the CI workflow exists without a CI badge (or the reverse)
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
from readme_facts import badges, collect, git  # noqa: E402

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
SHIELD = re.compile(r"https://img\.shields\.io/badge/([^\"\s)]+)")
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
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


def check(root, readme, workflow, linux):
    findings = []
    if (root / ".github" / "README.md").exists() and (root / "README.md").exists() and root.name != ".github":
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
        for match in EMOJI.finditer(line):
            findings.append(("emoji", number, f"U+{ord(match.group()):04X}"))

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

        expected_shields = set(SHIELD.findall(badges(facts)))
        for match in SHIELD.finditer(text):
            label = urllib.parse.unquote(match.group(1).split("-")[0]).lower()
            if label in {"swift", "platforms", "license"} and match.group(1) not in expected_shields:
                findings.append(("badge", line_of(text, match.start()), f"{label} badge differs from facts"))
        if facts["ci_workflow"]:
            if f"actions/workflows/{facts['ci_workflow']}/badge.svg" not in text:
                findings.append(("badge", 0, f"missing CI badge for {facts['ci_workflow']}"))
        for match in re.finditer(r"actions/workflows/([^/\"]+)/badge\.svg", text):
            if not (root / ".github" / "workflows" / match.group(1)).exists():
                findings.append(("badge", line_of(text, match.start()), f"workflow {match.group(1)} not found"))
    return findings


def main(argv):
    parser = argparse.ArgumentParser(description="Check a README against repository facts.")
    parser.add_argument("repo", type=pathlib.Path)
    parser.add_argument("--readme", type=pathlib.Path, help="README to check (default REPO/README.md)")
    parser.add_argument("--workflow", help="CI workflow file name under .github/workflows")
    parser.add_argument("--linux", choices=("auto", "yes", "no"), default="auto",
                        help="Linux detection passed to readme_facts.py")
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    readme = (args.readme or root / "README.md").resolve()
    if not readme.exists():
        sys.exit(f"error: {readme} not found")
    findings = check(root, readme, args.workflow, args.linux)
    for category, number, detail in findings:
        print(f"{category}\t{number}\t{detail}")
    print(f"{len(findings)} findings", file=sys.stderr)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
