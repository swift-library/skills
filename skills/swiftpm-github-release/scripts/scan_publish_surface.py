#!/usr/bin/env python3
"""Scan content that is about to become public for workstation leaks.

Targets:
  --history REPO_OR_BUNDLE [-- REV ...]  added lines and paths in commits (default: --all)
  --tree DIR                          tracked files (all files when DIR is not a Git checkout)
  --asset FILE ...                    release attachments, opening nested tar, zip and gzip

Categories:
  workstation-path  home-directory paths of a real user (CI runner homes pass)
  local-name        the local account name (from $HOME and $USER, plus --local-name)
  agent-state       files under agent execution-state directories (.agent/ by default)
  credential        high-confidence token and private-key formats
  denied            patterns from --deny-file (maintainer-supplied internal names)

Prints one finding per line and exits 1 when anything is found.
"""
import argparse
import gzip
import io
import os
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile
import zipfile

CI_HOMES = {"runner", "admin", "shared", "builder", "travis", "circleci", "vsts", "distiller", "root"}
PLACEHOLDERS = {"user", "username", "you", "me", "name", "example", "jappleseed", "johnappleseed", "your-name", "yourname", "foo", "bar"}
HOME_PATH = re.compile(rb"(?:/Users/|/home/|[A-Za-z]:\\\\?Users\\\\?)([A-Za-z0-9._-]+)")
CREDENTIALS = [
    ("github-token", re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("github-pat", re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("aws-access-key", re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("slack-token", re.compile(rb"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("openai-key", re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b")),
    ("anthropic-key", re.compile(rb"\bsk-ant-[A-Za-z0-9_-]{32,}\b")),
    ("private-key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY")),
]
MAX_DEPTH = 6


class Scanner:
    def __init__(self, local_names, deny, state_dirs):
        self.local = [n for n in local_names if n and n.lower() not in CI_HOMES | PLACEHOLDERS]
        self.local_re = (
            re.compile(rb"(?<![A-Za-z0-9])(?:" + b"|".join(re.escape(n.encode()) for n in self.local) + rb")(?![A-Za-z0-9])", re.I)
            if self.local
            else None
        )
        self.deny = deny
        self.state_dirs = [d.strip("/") + "/" for d in state_dirs]
        self.findings = []

    def add(self, category, where, match):
        text = match.decode("utf-8", "replace") if isinstance(match, bytes) else match
        self.findings.append((category, where, text.strip()[:160]))

    def path(self, where, rel):
        for d in self.state_dirs:
            if rel.startswith(d) or f"/{d}" in rel:
                self.add("agent-state", where, rel)
                return

    def content(self, where, data):
        for m in HOME_PATH.finditer(data):
            user = m.group(1).decode("utf-8", "replace")
            if user.lower() in CI_HOMES | PLACEHOLDERS or user.startswith(("<", "$", "{")):
                continue
            self.add("workstation-path", where, m.group(0))
        if self.local_re:
            for m in self.local_re.finditer(data):
                self.add("local-name", where, m.group(0))
        for name, pattern in CREDENTIALS:
            for m in pattern.finditer(data):
                self.add("credential", where, name)
        for pattern in self.deny:
            for m in pattern.finditer(data):
                self.add("denied", where, m.group(0))

    def blob(self, where, data, depth=0):
        if depth < MAX_DEPTH:
            buffer = io.BytesIO(data)
            if data[:2] == b"\x1f\x8b":
                try:
                    inner = gzip.decompress(data)
                except OSError:
                    inner = None
                if inner is not None:
                    if tarfile.is_tarfile(io.BytesIO(inner)):
                        return self.tar(where, inner, depth)
                    return self.blob(where + "!gunzip", inner, depth + 1)
            if tarfile.is_tarfile(buffer):
                return self.tar(where, data, depth)
            if zipfile.is_zipfile(io.BytesIO(data)):
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    for name in archive.namelist():
                        self.path(f"{where}!{name}", name)
                        self.content(f"{where}!{name} (name)", name.encode())
                        if not name.endswith("/"):
                            self.blob(f"{where}!{name}", archive.read(name), depth + 1)
                return
        self.content(where, data)

    def tar(self, where, data, depth):
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            for member in archive.getmembers():
                self.path(f"{where}!{member.name}", member.name)
                self.content(f"{where}!{member.name} (name)", member.name.encode())
                if member.isfile():
                    self.blob(f"{where}!{member.name}", archive.extractfile(member).read(), depth + 1)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def scan_history(scanner, target, revs):
    target = pathlib.Path(target)
    with tempfile.TemporaryDirectory() as tmp:
        repo = target
        if target.is_file():
            subprocess.run(["git", "clone", "-q", "--mirror", str(target), tmp], check=True)
            repo = pathlib.Path(tmp)
        revs = revs or ["--all"]
        log = git(repo, "log", "-p", "--no-color", "--no-ext-diff", "--format=%x00commit %H%n%B", *revs)
        commit, path = "?", "?"
        for line in log.split(b"\n"):
            if line.startswith(b"\x00commit "):
                commit, path = line[8:20].decode(), "(message)"
                continue
            if line.startswith(b"diff --git "):
                path = line.rsplit(b" b/", 1)[-1].decode("utf-8", "replace")
                scanner.path(f"{commit}:{path}", path)
                continue
            if line.startswith((b"+++", b"---", b"index ", b"@@")):
                continue
            if path == "(message)" or line.startswith(b"+"):
                scanner.content(f"{commit}:{path}", line)


def scan_tree(scanner, root):
    root = pathlib.Path(root)
    try:
        files = git(root, "ls-files", "-z").decode().split("\0")
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    for rel in filter(None, files):
        scanner.path(rel, rel)
        full = root / rel
        if full.is_file() and not full.is_symlink():
            scanner.blob(rel, full.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--history", metavar="REPO_OR_BUNDLE")
    target.add_argument("--tree", metavar="DIR")
    target.add_argument("--asset", nargs="+", metavar="FILE")
    parser.add_argument("--local-name", action="append", default=[], help="extra local account or machine name")
    parser.add_argument("--allow-name", action="append", default=[], help="name that is public on purpose")
    parser.add_argument("--deny-file", help="file with one regular expression per line")
    parser.add_argument("--state-dir", action="append", default=[".agent"], help="agent execution-state directory")
    parser.add_argument("revs", nargs="*", help="revisions for --history, after --")
    args = parser.parse_args()
    if args.revs and not args.history:
        parser.error("revisions apply only to --history")

    names = {pathlib.Path.home().name, os.environ.get("USER", ""), *args.local_name}
    names -= set(args.allow_name)
    deny = []
    if args.deny_file:
        for line in pathlib.Path(args.deny_file).read_text().splitlines():
            if line.strip() and not line.startswith("#"):
                deny.append(re.compile(line.strip().encode(), re.I))
    scanner = Scanner(sorted(names), deny, args.state_dir)

    if args.history:
        scan_history(scanner, args.history, args.revs)
    elif args.tree:
        scan_tree(scanner, args.tree)
    else:
        for asset in args.asset:
            scanner.blob(pathlib.Path(asset).name, pathlib.Path(asset).read_bytes())

    seen = set()
    for category, where, match in scanner.findings:
        key = (category, where, match)
        if key not in seen:
            seen.add(key)
            print(f"{category}\t{where}\t{match}")
    counts = {}
    for category, _, _ in seen:
        counts[category] = counts.get(category, 0) + 1
    summary = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "clean"
    print(f"summary: {summary}", file=sys.stderr)
    sys.exit(1 if seen else 0)


if __name__ == "__main__":
    main()
