#!/usr/bin/env python3
"""Compare a repository's public claims with the facts they must match.

Usage: check_repo_facts.py REPO [--range REV_RANGE] [--allow-identity EMAIL ...]
                           [--next-version X.Y.Z] [--live]

Checks:
  install-owner     README GitHub URLs for this repository use the origin owner
  install-version   README dependency versions exist as tags
  surfaced-readme   no .github/README.md hides the root README (except a .github repository)
  workflow-branch   push-triggered workflows that filter branches include the default branch
  spi-targets       .spi.yml documentation targets exist in Package.swift
  version-bump      raising a deployment target or swift-tools-version is a breaking bump:
                    MINOR during 0.x, MAJOR from 1.0. Checks the pending version (from
                    --next-version, .github/release.json or VERSION) against the latest
                    tag, or the latest tag against the one before it
  identity          commit authors and committers in --range are allowed identities
  ai-trailer        commit messages in --range carry no AI attribution trailers
  rendered-readme   (--live) GitHub renders the root README.md
  about             (--live) the repository has an About description

Prints one finding per line and exits 1 when anything is found.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

AI_TOOLS = r"cursor|claude|anthropic|openai|codex|copilot|chatgpt|gemini|devin|aider|windsurf"
TRAILER = re.compile(rf"^(?:co-authored-by|generated-by|made-with|assisted-by)\s*:.*\b(?:{AI_TOOLS})\b", re.I | re.M)
GENERATED = re.compile(rf"generated (?:with|by) \[?(?:{AI_TOOLS})", re.I)
SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
TARGET = re.compile(r"\.(?:target|executableTarget|testTarget|macro|plugin|systemLibrary|binaryTarget)\(\s*name:\s*\"([^\"]+)\"")
PLATFORM = re.compile(r"\.(\w+)\(\s*(?:\.v(\d+(?:_\d+)*)|\"([\d.]+)\")")
PLATFORM_IDENTITIES = {
    "noreply@github.com",
    "41898282+github-actions[bot]@users.noreply.github.com",
    "49699333+dependabot[bot]@users.noreply.github.com",
}


def git(repo, *args, check=True):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and result.returncode:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def origin_slug(repo):
    url = git(repo, "remote", "get-url", "origin", check=False)
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def default_branch(repo):
    ref = git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD", check=False)
    return ref.rsplit("/", 1)[-1] if ref else git(repo, "branch", "--show-current", check=False)


def version_tuple(text):
    return tuple(int(part) for part in re.split(r"[._]", text) if part)


def manifest_floor(text):
    tools = re.search(r"^//\s*swift-tools-version\s*:\s*([\d.]+)", text, re.M)
    block = re.search(r"platforms:\s*\[(.*?)\]", text, re.S)
    platforms = {}
    for m in PLATFORM.finditer(block.group(1) if block else ""):
        platforms[m.group(1)] = version_tuple(m.group(2) or m.group(3))
    return (version_tuple(tools.group(1)) if tools else None), platforms


def raised_floor(old, new):
    raised = []
    if old[0] and new[0] and new[0] > old[0]:
        raised.append("swift-tools-version " + ".".join(map(str, old[0])) + " -> " + ".".join(map(str, new[0])))
    for platform, version in sorted(new[1].items()):
        before = old[1].get(platform)
        if before is None or version > before:
            shown = ".".join(map(str, before)) if before else "unset"
            raised.append(f"{platform} {shown} -> " + ".".join(map(str, version)))
    return raised


def pending_version(repo, explicit):
    if explicit:
        return explicit.lstrip("v")
    config = repo / ".github" / "release.json"
    if config.exists():
        data = json.loads(config.read_text())
        source, pattern = data.get("version_file"), data.get("version_pattern")
        if source and pattern and (repo / source).exists():
            m = re.search(pattern, (repo / source).read_text())
            if m:
                return m.group(1)
    version = repo / "VERSION"
    return version.read_text().strip().lstrip("v") if version.exists() else None


def spi_targets(text):
    names = []
    for m in re.finditer(r"documentation_targets:\s*\[([^\]]*)\]", text):
        names += [n.strip().strip("'\"") for n in m.group(1).split(",") if n.strip()]
    for m in re.finditer(r"documentation_targets:\s*\n((?:[ \t]+-[^\n]*\n?)+)", text):
        names += [l.split("-", 1)[1].strip().strip("'\"") for l in m.group(1).splitlines() if l.strip().startswith("-")]
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo")
    parser.add_argument("--range", help="commits to check for identity and trailers, e.g. origin/main..HEAD")
    parser.add_argument("--allow-identity", action="append", default=[], help="allowed author/committer email")
    parser.add_argument("--next-version", help="version about to be released, when not readable from the repository")
    parser.add_argument("--live", action="store_true", help="also query GitHub with gh")
    args = parser.parse_args()
    repo = pathlib.Path(args.repo)
    findings = []
    owner, name = origin_slug(repo)
    tags = set(git(repo, "tag", "--list", check=False).split())
    versions = {SEMVER.match(t).group(0).lstrip("v") for t in tags if SEMVER.match(t)}

    readme = repo / "README.md"
    text = readme.read_text() if readme.exists() else ""
    code = "\n".join(re.findall(r"^```[^\n]*\n(.*?)^```", text, re.M | re.S))
    if name:
        for m in re.finditer(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?=[\s\"'`)/#]|$)", code):
            if m.group(2).lower() == name.lower() and m.group(1).lower() != owner.lower():
                findings.append(("install-owner", f"README.md code block: {m.group(0)} (origin is {owner}/{name})"))
    for m in re.finditer(r"\.package\(\s*url:\s*\"([^\"]+)\"[^)]*?(?:from|exact):\s*\"([^\"]+)\"", text, re.S):
        url, version = m.groups()
        if name and name.lower() in url.lower() and versions and version not in versions:
            latest = max(versions, key=lambda v: tuple(map(int, v.split("."))))
            findings.append(("install-version", f"README.md pins {version}; tags have no such version (latest {latest})"))

    if (repo / ".github" / "README.md").exists() and readme.exists() and name != ".github":
        findings.append(("surfaced-readme", ".github/README.md is rendered instead of the root README.md"))

    manifest = repo / "Package.swift"
    manifest_text = manifest.read_text() if manifest.exists() else ""
    spi = repo / ".spi.yml"
    if spi.exists() and manifest_text:
        declared = set(TARGET.findall(manifest_text))
        for target in spi_targets(spi.read_text()):
            if target not in declared:
                findings.append(("spi-targets", f".spi.yml documents {target}, which Package.swift does not declare"))

    tag_for = {t.lstrip("v"): t for t in tags if SEMVER.match(t)}
    ordered = sorted(versions, key=version_tuple)
    pending = pending_version(repo, args.next_version)
    base = head = None
    if ordered and pending and SEMVER.match(pending) and version_tuple(pending) > version_tuple(ordered[-1]):
        base, new = ordered[-1], pending
    elif len(ordered) > 1:
        base, head, new = ordered[-2], ordered[-1], ordered[-1]
    if base and manifest_text:
        old_v, new_v = version_tuple(base), version_tuple(new)
        breaking = new_v[0] > old_v[0] or (new_v[0] == 0 and new_v[1] > old_v[1])
        old_text = git(repo, "show", f"{tag_for[base]}:Package.swift", check=False)
        new_text = git(repo, "show", f"{tag_for[head]}:Package.swift", check=False) if head else manifest_text
        raised = raised_floor(manifest_floor(old_text), manifest_floor(new_text)) if old_text and new_text else []
        if raised and not breaking:
            level = "MINOR" if old_v[0] == 0 else "MAJOR"
            findings.append(("version-bump", f"{base} -> {new} raises {', '.join(raised)}; that needs a {level} bump"))

    branch = default_branch(repo)
    for workflow in sorted((repo / ".github" / "workflows").glob("*.y*ml")):
        body = workflow.read_text()
        push = re.search(r"^\s*push:\s*\n((?:\s{4,}.*\n?)*)", body, re.M)
        if not push:
            continue
        block = push.group(1)
        inline = re.search(r"branches:\s*\[([^\]]*)\]", block)
        dashed = re.search(r"branches:\s*\n((?:[ \t]+-[^\n]*\n?)+)", block)
        if inline:
            listed = [b.strip().strip("'\"") for b in inline.group(1).split(",") if b.strip()]
        elif dashed:
            listed = [l.split("-", 1)[1].strip().strip("'\"") for l in dashed.group(1).splitlines() if l.strip().startswith("-")]
        else:
            continue
        if branch and branch not in listed and not any("*" in b for b in listed):
            findings.append(("workflow-branch", f"{workflow.relative_to(repo)} pushes on {listed}; default branch is {branch}"))

    if args.range:
        log = git(repo, "log", "--format=%H%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B%x1e", args.range)
        allowed = {e.lower() for e in args.allow_identity} | PLATFORM_IDENTITIES if args.allow_identity else set()
        for record in filter(None, (r.strip() for r in log.split("\x1e"))):
            sha, an, ae, cn, ce, body = (record.split("\x1f") + [""] * 6)[:6]
            short = sha[:12]
            for role, person, email in (("author", an, ae), ("committer", cn, ce)):
                if allowed and email.lower() not in allowed:
                    findings.append(("identity", f"{short} {role} {person} <{email}>"))
                elif re.search(AI_TOOLS, f"{person} {email}", re.I):
                    findings.append(("identity", f"{short} {role} {person} <{email}>"))
            for m in TRAILER.finditer(body):
                findings.append(("ai-trailer", f"{short} {m.group(0).strip()}"))
            if GENERATED.search(body):
                findings.append(("ai-trailer", f"{short} {GENERATED.search(body).group(0)}"))

    if args.live and owner:
        def gh(path, jq):
            result = subprocess.run(["gh", "api", path, "--jq", jq], capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else None

        rendered = gh(f"repos/{owner}/{name}/readme", ".path")
        if rendered != "README.md":
            findings.append(("rendered-readme", f"GitHub renders {rendered or 'no README'}"))
        if not gh(f"repos/{owner}/{name}", ".description // empty"):
            findings.append(("about", "repository has no About description"))

    for category, detail in findings:
        print(f"{category}\t{detail}")
    print(f"summary: {len(findings)} finding(s) for {owner}/{name}", file=sys.stderr)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
