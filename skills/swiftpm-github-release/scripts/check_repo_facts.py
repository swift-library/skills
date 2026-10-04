#!/usr/bin/env python3
"""Compare a repository's public claims with the facts they must match.

Usage: check_repo_facts.py REPO [--range REV_RANGE] [--allow-identity EMAIL ...] [--live]

Checks:
  install-owner     README GitHub URLs for this repository use the origin owner
  install-version   README dependency versions exist as tags
  surfaced-readme   no .github/README.md hides the root README (except a .github repository)
  workflow-branch   push-triggered workflows that filter branches include the default branch
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


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo")
    parser.add_argument("--range", help="commits to check for identity and trailers, e.g. origin/main..HEAD")
    parser.add_argument("--allow-identity", action="append", default=[], help="allowed author/committer email")
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
