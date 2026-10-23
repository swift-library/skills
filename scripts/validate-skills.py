#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Validate skill contracts, resources, references and host discovery budgets."""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_KEYS = {
    "name", "description", "license", "allowed-tools", "metadata",
    "disable-model-invocation", "user-invocable", "argument-hint", "model",
}
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ORGANIZATIONS = re.compile(r"swift-library|agents-tools|skill-cli|showxu", re.I)
# Each exception names its product owner and rationale. Optional path/pattern
# constraints keep the collection identity exception local to the HTTP header.
ORGANIZATION_ALLOWLIST = {
    "swift-interface-distiller-patterns": (
        None, None, "Documents the organization's swift-interface-distiller product."),
    "swift-sh-patterns": (
        None, None, "Documents the organization's swift-sh runner."),
    "swift-data-writable-patterns": (
        None, None, "Documents the organization's SwiftDataWritable product."),
    "swiftpm-index": (
        "cli/swiftpm-index", re.compile(r'^USER_AGENT = f"\{NAME\}/[^"\n]+ \(\+https://github\.com/swift-library/skills\)"$'),
        "The CLI HTTP user agent identifies this collection to source servers."),
}
SCENARIOS = {
    "Claude 1M context": (40_000, "swift-skills:"),
    "Claude 200k context": (8_000, "swift-skills:"),
    "Codex max_context_tokens=10000": (40_000, ""),
}
ENFORCED_SCENARIOS = frozenset({"Claude 1M context", "Codex max_context_tokens=10000"})


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    message: str

    def format(self, root):
        try:
            path = self.path.relative_to(root)
        except ValueError:
            path = self.path
        return f"{path}:{self.line}: {self.message}"


def scalar(value):
    """Read the collection's single-line scalar subset; reject other YAML forms."""
    value = value.strip()
    if not value:
        raise ValueError("expected a single-line scalar")
    if value.startswith('"'):
        try:
            result = json.loads(value)
        except (ValueError, TypeError) as error:
            raise ValueError("unsupported double-quoted scalar") from error
        if not isinstance(result, str) or any(c in result for c in "\r\n"):
            raise ValueError("expected a single-line string")
        return result
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise ValueError("unsupported single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value[0] in "|>[]{},&*!%@`\"'" or re.match(r"[-?:](?:\s|$)", value):
        raise ValueError("unsupported YAML form; use a single-line scalar")
    if re.search(r"(?:^|\s)#", value) or "\t" in value:
        raise ValueError("quote scalars containing YAML comments or tabs")
    return value


def frontmatter(path, content, findings):
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        findings.append(Finding(path, 1, "SKILL.md must start with YAML frontmatter (---)"))
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        findings.append(Finding(path, 1, "frontmatter is missing its closing ---"))
        return {}
    values = {}
    for number, line in enumerate(lines[1:end], 2):
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z][a-z-]*):[ \t]*(.*)", line)
        if not match:
            findings.append(Finding(path, number, "unsupported frontmatter; expected key: single-line scalar"))
            continue
        key, raw = match.groups()
        if key not in FRONTMATTER_KEYS:
            findings.append(Finding(path, number, f"unknown frontmatter key: {key}"))
        if key in values:
            findings.append(Finding(path, number, f"duplicate frontmatter key: {key}"))
        try:
            values[key] = (scalar(raw), number)
        except ValueError as error:
            findings.append(Finding(path, number, f"{key}: {error}"))
    for key in ("name", "description"):
        if key not in values:
            findings.append(Finding(path, 1, f"frontmatter requires {key}"))
    if "name" in values:
        name, line = values["name"]
        if name != path.parent.name:
            findings.append(Finding(path, line, f"name {name!r} must equal directory {path.parent.name!r}"))
        if not NAME.fullmatch(name) or len(name) > 64:
            findings.append(Finding(path, line, "name must match ^[a-z0-9]+(-[a-z0-9]+)*$ and be at most 64 characters"))
    if "description" in values:
        description, line = values["description"]
        if not description.strip() or len(description) > 1024:
            findings.append(Finding(path, line, f"description must contain 1–1,024 characters (found {len(description)})"))
    return values


def agent_metadata(skill, findings):
    path = skill / "agents/openai.yaml"
    if not path.is_file():
        return
    fields = {}
    in_interface = False
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if line and not line[0].isspace() and not line.startswith("#"):
            in_interface = line == "interface:"
        if not in_interface:
            continue
        match = re.fullmatch(r"  (default_prompt|icon_small|icon_large):[ \t]*(.*)", line)
        if not match:
            continue
        key, raw = match.groups()
        if key in fields:
            findings.append(Finding(path, number, f"duplicate interface field: {key}"))
        try:
            fields[key] = (scalar(raw), number)
        except ValueError as error:
            findings.append(Finding(path, number, f"{key}: {error}"))
    prompt, line = fields.get("default_prompt", ("", 1))
    if not re.search(r"\$" + re.escape(skill.name) + r"(?![a-zA-Z0-9_-])", prompt):
        findings.append(Finding(path, line, f"default_prompt must contain ${skill.name}"))
    for key in ("icon_small", "icon_large"):
        if key in fields:
            target, line = fields[key]
            if not target or not (skill / target).is_file():
                findings.append(Finding(path, line, f"{key} path does not exist: {target!r}"))


def mask_code(content):
    """Preserve offsets and line numbers while hiding fenced and inline code."""
    lines = content.splitlines(keepends=True)
    fence = None
    for index, line in enumerate(lines):
        match = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if fence:
            lines[index] = re.sub(r"[^\n]", " ", line)
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = None
        elif match:
            fence = match[1]
            lines[index] = re.sub(r"[^\n]", " ", line)
    return re.sub(r"(?<!`)(`+)(?!`)(.*?)\1(?!`)",
                  lambda m: re.sub(r"[^\n]", " ", m[0]), "".join(lines), flags=re.S)


def destination(text, start):
    """Read Markdown destinations, including escaped and balanced parentheses."""
    index = start
    while index < len(text) and text[index].isspace():
        index += 1
    if index < len(text) and text[index] == "<":
        end = text.find(">", index + 1)
        return text[index + 1:end] if end >= 0 else ""
    chars = []
    depth = 0
    while index < len(text):
        char = text[index]
        if char == "\\" and index + 1 < len(text):
            chars.append(text[index + 1])
            index += 2
            continue
        if char.isspace() or (char == ")" and not depth):
            break
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        chars.append(char)
        index += 1
    return "".join(chars)


def markdown_links(root, path, content, findings):
    text = mask_code(content)
    # Closing markers also cover nested image labels and multiline link labels.
    patterns = (r"(?<!\\)\]\(", r"(?m)^ {0,3}\[[^\]\n]+\]:[ \t]*")
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            target = destination(text, match.end())
            if not target or target.startswith(("#", "//")) or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            relative = unquote(urlsplit(target).path)
            resolved = (root / relative.lstrip("/")) if relative.startswith("/") else path.parent / relative
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                findings.append(Finding(path, line, f"relative Markdown target does not exist: {target}"))


def reference_cycles(graph, edges, findings):
    visited, active, stack = set(), set(), []

    def visit(skill):
        visited.add(skill)
        active.add(skill)
        stack.append(skill)
        for target in sorted(graph[skill]):
            if target in active:
                cycle = stack[stack.index(target):] + [target]
                path, line = edges[skill, target]
                locations = "; ".join(f"{edges[a, b][0]}:{edges[a, b][1]}" for a, b in zip(cycle, cycle[1:]))
                findings.append(Finding(path, line, f"skill reference cycle: {' -> '.join(cycle)} ({locations})"))
            elif target not in visited:
                visit(target)
        stack.pop()
        active.remove(skill)

    for skill in sorted(graph):
        if skill not in visited:
            visit(skill)


def listing_report(skills, scenarios=None):
    reports = []
    for scenario, (budget, namespace) in (SCENARIOS if scenarios is None else scenarios).items():
        entries = [f"- {namespace}{name}: {description}" for name, description in sorted(skills)]
        names = [f"- {namespace}{name}" for name, _ in sorted(skills)]
        used = count = 0
        for entry in entries:
            cost = len(entry) + bool(count)
            if used + cost <= budget:
                used += cost
                count += 1
        reports.append((scenario, len("\n".join(entries)), len("\n".join(names)), count, budget))
    return reports


def validate(root):
    root = root.resolve()
    findings, listings = [], []
    skill_root = root / "skills"
    directories = sorted(p for p in skill_root.iterdir() if p.is_dir()) if skill_root.is_dir() else []
    graph = {p.name: set() for p in directories}
    edges = {}
    if not directories:
        findings.append(Finding(skill_root / "SKILL.md", 1, "collection contains no skill directories"))
    for skill in directories:
        path = skill / "SKILL.md"
        if not path.is_file():
            findings.append(Finding(path, 1, "missing SKILL.md"))
        else:
            metadata = frontmatter(path, path.read_text(), findings)
            if "name" in metadata and "description" in metadata:
                listings.append((metadata["name"][0], metadata["description"][0]))
        agent_metadata(skill, findings)
        for path in sorted(skill.rglob("*")):
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for number, line in enumerate(content.splitlines(), 1):
                for target in re.findall(r"(?<!`)`([^`\n]+)`(?!`)", line):
                    if target in graph and target != skill.name:
                        graph[skill.name].add(target)
                        edges.setdefault((skill.name, target), (path, number))
                match = ORGANIZATIONS.search(line)
                if match:
                    rule = ORGANIZATION_ALLOWLIST.get(skill.name)
                    allowed = rule and (rule[0] is None or (
                        path.relative_to(skill).as_posix() == rule[0] and rule[1].fullmatch(line)))
                    if not allowed:
                        findings.append(Finding(path, number, f"organization name {match[0]!r} requires an organization-neutral input or a product exception"))
    reference_cycles(graph, edges, findings)
    markdown = set(skill_root.rglob("*.md")) | set((root / "docs").rglob("*.md"))
    markdown.update(root / name for name in ("README.md", "AGENTS.md") if (root / name).is_file())
    for path in sorted(markdown):
        markdown_links(root, path, path.read_text(), findings)
    reports = listing_report(listings)
    for scenario, total, _, _, budget in reports:
        if scenario in ENFORCED_SCENARIOS and total > budget:
            script = Path(__file__).resolve()
            line = next(i for i, text in enumerate(script.read_text().splitlines(), 1) if text.startswith("ENFORCED_SCENARIOS ="))
            findings.append(Finding(script, line, f"{scenario} listing exceeds budget: {total} > {budget} characters"))
    return findings, reports, len(directories)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="collection root (default: this repository)")
    args = parser.parse_args()
    findings, reports, count = validate(args.root)
    print(f"Skill listing: {count} skills; newline separators count toward each budget.")
    print("Claude entries: - swift-skills:<name>: <description>; Codex entries: - <name>: <description>.")
    print("Codex estimate assumes 4 characters/token; max_context_tokens=10000 gives 40,000 characters.")
    for scenario, total, floor, fit, budget in reports:
        mode = "enforced" if scenario in ENFORCED_SCENARIOS else "report only"
        print(f"{scenario}: {total:,} chars; names-only floor {floor:,}; full descriptions fit {fit}/{count} in {budget:,} chars (greedy name order; {mode}).")
    for finding in findings:
        print(finding.format(args.root.resolve()))
    print(f"Skill validation {'failed' if findings else 'passed'}: {len(findings)} finding(s).")
    return bool(findings)


if __name__ == "__main__":
    raise SystemExit(main())
