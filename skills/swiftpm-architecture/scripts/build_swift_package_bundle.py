#!/usr/bin/env python3
"""
Build a compact architecture review-context bundle for a Swift Package repo.

The script is optimized for token efficiency:
- reads Package.swift and architecture-relevant files
- ranks source files by architectural importance
- emits one structured markdown evidence bundle for a human or LLM reviewer
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ARCH_DOC_KEYWORDS = (
    "architecture",
    "architectural",
    "convention",
    "design",
    "overview",
    "boundary",
    "boundaries",
)

NOISE_DIRS = {
    ".git",
    ".build",
    ".swiftpm",
    "DerivedData",
    "xcuserdata",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
}

NOISE_FILE_SUFFIXES = {
    ".o",
    ".a",
    ".so",
    ".dylib",
    ".dll",
    ".xcuserstate",
    ".DS_Store",
}

LIKELY_TEXT_EXTS = {
    ".swift",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".sh",
}

TYPE_RE = re.compile(
    r"^\s*(public\s+)?(?:final\s+)?(class|struct|enum|protocol|actor)\s+([A-Z][A-Za-z0-9_]*)",
    re.MULTILINE,
)


@dataclass
class FileRecord:
    path: Path
    rel: str
    text: str
    score: int
    reasons: list[str]
    bucket: int
    is_swift: bool
    is_test: bool


def is_root_readme(rel: str) -> bool:
    parts = rel.split("/")
    return len(parts) == 1 and parts[0].lower().startswith("readme")


def is_doc_rel(rel: str) -> bool:
    lower_rel = rel.lower()
    return (
        is_root_readme(rel)
        or lower_rel.startswith("docs/")
        or lower_rel.startswith("documentation/")
    )


def is_high_signal_doc(rel: str, text: str) -> bool:
    if is_root_readme(rel):
        return True
    lower_rel = rel.lower()
    if not (lower_rel.endswith(".md") or lower_rel.endswith(".txt")):
        return False
    if any(keyword in lower_rel for keyword in ARCH_DOC_KEYWORDS):
        return True
    head = text[:4000].lower()
    return any(keyword in head for keyword in ARCH_DOC_KEYWORDS)


def is_vendored_or_upstream_rel(rel: str) -> bool:
    lower_rel = rel.lower()
    if any(marker in lower_rel for marker in ("/upstreams/", "/vendor/", "/thirdparty/", "/third_party/")):
        return True
    parts = [part.lower() for part in rel.split("/")]
    return len(parts) > 4 and parts[0] == "sources" and any(part in {"source", "sources"} for part in parts[2:-1])


def line_count(text: str) -> int:
    return text.count("\n") + 1


def is_too_large_for_default_embedding(rec: FileRecord) -> bool:
    return rec.is_swift and line_count(rec.text) > 900


def is_too_large_for_embedding(rec: FileRecord, max_file_lines: int) -> bool:
    return rec.is_swift and line_count(rec.text) > max_file_lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a compact architecture review-context markdown bundle for a local Swift Package repository.",
    )
    parser.add_argument("repo_path", help="Path to local Swift Package repository")
    parser.add_argument(
        "--output",
        help="Output markdown path. Default: <repo>/architecture-review-bundle.md",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=24,
        help="Max selected source files for non-tiny repos (default: 24)",
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Allow tests to be selected when architecturally important",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=80_000,
        help="Maximum UTF-8 byte budget for the generated markdown bundle where fixed manifest context allows (default: 80000)",
    )
    parser.add_argument(
        "--max-file-lines",
        type=int,
        default=900,
        help="Max Swift source lines to embed by default before listing as omitted-important (default: 900)",
    )
    return parser.parse_args()


def is_noise_dir(name: str) -> bool:
    return name in NOISE_DIRS or name.endswith(".xcworkspace")


def is_probably_binary(path: Path) -> bool:
    if path.suffix in NOISE_FILE_SUFFIXES:
        return True
    if path.suffix and path.suffix.lower() not in LIKELY_TEXT_EXTS:
        # Small chance of text with unknown extension; still allow tiny files.
        if path.stat().st_size > 64_000:
            return True
    try:
        with path.open("rb") as handle:
            head = handle.read(4096)
        return b"\x00" in head
    except OSError:
        return True


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def walk_repo(repo: Path) -> list[Path]:
    files: list[Path] = []
    for root, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if not is_noise_dir(d)]
        root_path = Path(root)
        for name in names:
            p = root_path / name
            if is_probably_binary(p):
                continue
            files.append(p)
    return files


def normalize_path(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def read_package_text(repo: Path) -> str:
    package_file = repo / "Package.swift"
    if not package_file.exists():
        return ""
    return safe_read_text(package_file)


def extract_call_block(text: str, start_idx: int) -> tuple[str, int]:
    open_idx = text.find("(", start_idx)
    if open_idx < 0:
        return "", start_idx
    depth = 0
    idx = open_idx
    while idx < len(text):
        ch = text[idx]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start_idx : idx + 1], idx + 1
        idx += 1
    return text[start_idx:], len(text)


def parse_targets(package_text: str) -> list[dict]:
    kinds = ["target", "executableTarget", "testTarget", "macro", "plugin"]
    targets: list[dict] = []

    for kind in kinds:
        needle = f".{kind}("
        cursor = 0
        while True:
            hit = package_text.find(needle, cursor)
            if hit < 0:
                break
            block, next_cursor = extract_call_block(package_text, hit)
            cursor = next_cursor
            if not block:
                continue
            if kind == "plugin" and "capability" not in block:
                # Exclude plugin usages in target configuration:
                # plugins: [.plugin(name: "Tool", package: "tool-package")]
                continue

            name_match = re.search(r'name\s*:\s*"([^"]+)"', block)
            if not name_match:
                continue
            name = name_match.group(1)

            dep_names: list[str] = []
            dep_match = re.search(r"dependencies\s*:\s*\[(.*?)\]", block, re.DOTALL)
            if dep_match:
                quoted = re.findall(r'"([^"]+)"', dep_match.group(1))
                for dep in quoted:
                    if dep != name and dep not in dep_names:
                        dep_names.append(dep)

            path_match = re.search(r'path\s*:\s*"([^"]+)"', block)
            target_path = path_match.group(1).strip("/") if path_match else ""

            targets.append(
                {
                    "name": name,
                    "kind": kind,
                    "dependencies": dep_names,
                    "path": target_path,
                }
            )
    return targets


TARGET_KIND_MAP = {
    "regular": "target",
    "executable": "executableTarget",
    "test": "testTarget",
    "macro": "macro",
    "plugin": "plugin",
    "system": "systemLibrary",
    "binary": "binaryTarget",
}


def dependency_name_from_dump(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        for item in value:
            name = dependency_name_from_dump(item)
            if name:
                return name
        return None
    if not isinstance(value, dict):
        return None

    for key in ("byName", "target", "product"):
        if key in value:
            name = dependency_name_from_dump(value[key])
            if name:
                return name
    for key in ("name", "targetName", "productName"):
        item = value.get(key)
        if isinstance(item, str) and item:
            return item
    return None


def targets_from_dump_payload(payload: dict[str, Any]) -> list[dict]:
    targets: list[dict] = []
    for item in payload.get("targets", []):
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name:
            continue

        raw_kind = item.get("type") or item.get("kind") or "regular"
        kind = TARGET_KIND_MAP.get(str(raw_kind), str(raw_kind))

        dep_names: list[str] = []
        for dep in item.get("dependencies") or []:
            dep_name = dependency_name_from_dump(dep)
            if dep_name and dep_name != name and dep_name not in dep_names:
                dep_names.append(dep_name)

        target_path = item.get("path") or ""
        if not isinstance(target_path, str):
            target_path = ""

        targets.append(
            {
                "name": name,
                "kind": kind,
                "dependencies": dep_names,
                "path": target_path.strip("/"),
            }
        )
    return targets


def dump_package_targets(repo: Path) -> list[dict]:
    if not (repo / "Package.swift").exists():
        return []
    try:
        result = subprocess.run(
            ["swift", "package", "--package-path", str(repo), "dump-package"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []

    if result.returncode != 0:
        return []
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, dict):
        return []
    return targets_from_dump_payload(payload)


def load_targets(repo: Path, package_text: str) -> tuple[list[dict], str]:
    dumped_targets = dump_package_targets(repo)
    if dumped_targets:
        return dumped_targets, "swift package dump-package"
    return parse_targets(package_text), "Package.swift text scan"


def target_source_roots(targets: list[dict]) -> set[str]:
    roots = {"Sources", "Tests"}
    for target in targets:
        name = target["name"]
        target_path = target.get("path") or ""
        if target_path:
            roots.add(target_path.strip("/"))
        elif target["kind"] == "testTarget":
            roots.add(f"Tests/{name}")
        elif target["kind"] == "plugin":
            roots.add(f"Plugins/{name}")
        else:
            roots.add(f"Sources/{name}")
    return {root for root in roots if root}


def is_under_root(rel: str, root: str) -> bool:
    root = root.strip("/")
    return rel == root or rel.startswith(f"{root}/")


def is_package_relevant_rel(rel: str, source_roots: set[str]) -> bool:
    if rel == "Package.swift" or is_doc_rel(rel):
        return True
    return any(is_under_root(rel, root) for root in source_roots)


def infer_overview(package_text: str, targets: list[dict], repo_name: str) -> tuple[str, str]:
    if not package_text.strip():
        return (
            f"`{repo_name}` does not contain `Package.swift`; architecture summary is inferred from source layout and naming signals.",
            "Swift source layout without a package manifest",
        )

    style_parts: list[str] = []
    if "import SwiftUI" in package_text:
        style_parts.append("SwiftUI-oriented package composition")
    if any(t["kind"] == "executableTarget" for t in targets):
        style_parts.append("executable + library target split")
    if not style_parts:
        style_parts.append("module-oriented Swift Package")

    package_summary = (
        f"`{repo_name}` is a Swift Package with {len(targets) or 'inferred'} module(s)/target(s). "
        "Architecture summary is inferred from Package.swift, source layout, and naming signals."
    )
    style_summary = "; ".join(style_parts)
    return package_summary, style_summary


def score_file(rel: str, text: str) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    filename = Path(rel).name
    lower_rel = rel.lower()

    if rel == "Package.swift":
        score += 1000
        reasons.append("package manifest and module graph")
    if is_root_readme(rel):
        score += 700
        reasons.append("high-level architecture/convention documentation")
    elif is_doc_rel(rel):
        score += 160
        if is_high_signal_doc(rel, text):
            score += 360
            reasons.append("architecture-relevant documentation")
    if rel.startswith("Sources/"):
        score += 100
    elif rel.startswith("Tests/"):
        score += 25

    stem = Path(rel).stem.lower()
    entry_keywords = ("main", "bootstrap", "composition", "router", "coordinator", "scene")
    has_entry_name = (
        stem == "app"
        or stem.endswith("app")
        or filename.lower() == "main.swift"
        or any(k in stem for k in entry_keywords)
    )
    if has_entry_name:
        score += 170
        reasons.append("entrypoint or composition root")

    abstraction_keywords = ("protocol", "service", "repository", "provider", "store", "viewmodel", "state")
    if any(k in filename.lower() for k in abstraction_keywords):
        score += 90
        reasons.append("core abstraction surface")

    is_swift = rel.endswith(".swift")
    protocol_hits = 0
    if is_swift:
        protocol_hits = len(re.findall(r"^\s*(?:public\s+)?protocol\s+\w+", text, flags=re.MULTILINE))
    if protocol_hits:
        score += min(180, protocol_hits * 30)
        reasons.append(f"declares {protocol_hits} protocol(s)")

    public_type_hits = 0
    if is_swift:
        public_type_hits = len(
            re.findall(
                r"^\s*public\s+(?:final\s+)?(?:class|struct|enum|actor)\s+\w+",
                text,
                flags=re.MULTILINE,
            )
        )
    if public_type_hits:
        score += min(120, public_type_hits * 15)
        reasons.append("contains public API types")

    lines = line_count(text)
    if 80 <= lines <= 420:
        score += 35
    elif lines > 900:
        score -= 30

    if any(marker in lower_rel for marker in ("preview", "mock", "fixture", "generated", "g.swift")):
        score -= 150
        reasons.append("preview/mock/fixture or generated candidate")

    if is_vendored_or_upstream_rel(rel):
        score -= 500
        reasons.append("vendored/upstream implementation candidate")

    if rel.startswith("Tests/") and not any(k in lower_rel for k in ("contract", "integration", "architecture")):
        score -= 75

    if any(m in text[:500].lower() for m in ("generated by", "do not edit")):
        score -= 300

    if lines > 1500:
        score -= 350
        reasons.append("very large source file")
    elif lines > 900:
        score -= 180
        reasons.append("large source file")
    elif lines > 600:
        score -= 80
        reasons.append("moderately large source file")

    if not reasons:
        reasons.append("representative implementation file")

    return score, reasons


def bucket_for_file(rel: str, text: str, is_test: bool) -> int:
    filename = Path(rel).name.lower()
    stem = Path(rel).stem.lower()
    lower_rel = rel.lower()
    if rel == "Package.swift":
        return 0
    if filename.startswith("readme") or lower_rel.startswith("docs/") or lower_rel.startswith("documentation/"):
        return 1
    if (
        stem == "app"
        or stem.endswith("app")
        or filename == "main.swift"
        or any(k in stem for k in ("main", "bootstrap", "composition", "router", "coordinator"))
    ):
        return 2
    if re.search(r"^\s*(?:public\s+)?protocol\s+\w+", text, flags=re.MULTILINE):
        return 3
    if any(k in filename for k in ("store", "state", "viewmodel", "service", "repository", "provider")):
        return 4
    if is_test:
        return 6
    return 5


def make_records(repo: Path, files: list[Path], targets: list[dict]) -> list[FileRecord]:
    records: list[FileRecord] = []
    source_roots = target_source_roots(targets)
    for path in files:
        rel = normalize_path(path, repo)
        if not is_package_relevant_rel(rel, source_roots):
            continue
        text = safe_read_text(path)
        score, reasons = score_file(rel, text)
        is_swift = rel.endswith(".swift")
        is_test = rel.startswith("Tests/")
        bucket = bucket_for_file(rel, text, is_test)
        records.append(
            FileRecord(
                path=path,
                rel=rel,
                text=text,
                score=score,
                reasons=reasons,
                bucket=bucket,
                is_swift=is_swift,
                is_test=is_test,
            )
        )
    return records


def module_name_for_rel(rel: str) -> str:
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] in {"Sources", "Tests"}:
        return parts[1]
    return "root"


def ensure_module_coverage(selected: list[FileRecord], source_records: list[FileRecord], max_files: int) -> list[FileRecord]:
    seen_modules = {module_name_for_rel(r.rel) for r in selected if r.rel.startswith("Sources/")}
    by_module: dict[str, list[FileRecord]] = {}
    for rec in source_records:
        module = module_name_for_rel(rec.rel)
        by_module.setdefault(module, []).append(rec)
    for module, recs in by_module.items():
        if module in seen_modules:
            continue
        if len(selected) >= max_files:
            break
        top = sorted(recs, key=lambda r: (-r.score, r.rel))[0]
        selected.append(top)
    return selected


def select_files(
    records: list[FileRecord],
    max_files: int,
    include_tests: bool,
    max_file_lines: int = 900,
) -> list[FileRecord]:
    package_records = [rec for rec in records if rec.rel == "Package.swift"]
    root_readmes = sorted(
        [rec for rec in records if is_root_readme(rec.rel)],
        key=lambda r: (-r.score, r.rel),
    )
    supplemental_docs = sorted(
        [
            rec
            for rec in records
            if is_doc_rel(rec.rel)
            and not is_root_readme(rec.rel)
            and is_high_signal_doc(rec.rel, rec.text)
        ],
        key=lambda r: (-r.score, r.rel),
    )

    all_source_swift = [r for r in records if r.is_swift and not r.is_test]
    compact_source_swift = [
        r
        for r in all_source_swift
        if not is_vendored_or_upstream_rel(r.rel) and not is_too_large_for_embedding(r, max_file_lines)
    ]
    nonvendored_source_swift = [r for r in all_source_swift if not is_vendored_or_upstream_rel(r.rel)]
    source_swift = compact_source_swift or nonvendored_source_swift or all_source_swift
    test_swift = [r for r in records if r.rel.startswith("Tests/") and r.is_swift]
    tiny_repo = len(source_swift) <= 14

    ranked_sources = sorted(source_swift, key=lambda r: (-r.score, r.rel))
    ranked_tests = sorted(test_swift, key=lambda r: (-r.score, r.rel))

    selected: list[FileRecord] = []
    selected.extend(package_records[:1])
    selected.extend(root_readmes[:1])

    def append_unique(rec: FileRecord) -> None:
        if rec not in selected:
            selected.append(rec)

    def add_ranked_sources(limit: int) -> None:
        for rec in ranked_sources:
            if len(selected) >= limit:
                break
            append_unique(rec)

    if tiny_repo:
        for rec in ranked_sources:
            if rec.score > -180 and rec not in selected:
                selected.append(rec)
        for rec in supplemental_docs:
            if len(selected) >= max_files:
                break
            append_unique(rec)
        if include_tests:
            for rec in ranked_tests:
                if rec.score >= 80 and rec not in selected:
                    selected.append(rec)
    else:
        doc_reserve = min(2, max(0, max_files - len(selected) - 4))
        add_ranked_sources(max_files - doc_reserve)

        for rec in supplemental_docs[:doc_reserve]:
            if len(selected) >= max_files:
                break
            append_unique(rec)

        add_ranked_sources(max_files)

        if include_tests and len(selected) < max_files:
            room = max_files - len(selected)
            for rec in ranked_tests[: room // 3]:
                if rec.score >= 100 and rec not in selected:
                    selected.append(rec)

    coverage_limit = max(max_files, len(selected)) if tiny_repo else max_files
    selected = ensure_module_coverage(selected, ranked_sources, max_files=coverage_limit)
    deduped: dict[str, FileRecord] = {}
    for rec in selected:
        if rec.rel not in deduped:
            deduped[rec.rel] = rec

    selected = sorted(
        deduped.values(),
        key=lambda r: (r.bucket, -r.score, r.rel),
    )
    return selected


def omitted_file_rationale(rec: FileRecord, max_file_lines: int) -> str:
    reasons: list[str] = []
    lines = line_count(rec.text)
    if is_too_large_for_embedding(rec, max_file_lines):
        reasons.append(f"exceeds per-file embed budget ({lines} lines)")
    if is_vendored_or_upstream_rel(rec.rel):
        reasons.append("vendored/upstream implementation")
    if is_high_signal_doc(rec.rel, rec.text) and not is_root_readme(rec.rel):
        reasons.append("architecture-relevant doc not embedded")
    if not reasons:
        reasons.append("ranked below selected context budget")
    return "; ".join(reasons)


def important_omitted_files(
    records: list[FileRecord],
    selected: list[FileRecord],
    max_file_lines: int,
    max_items: int = 8,
) -> list[FileRecord]:
    selected_paths = {rec.rel for rec in selected}
    candidates: list[FileRecord] = []
    for rec in records:
        if rec.rel in selected_paths:
            continue
        is_interesting_source = rec.is_swift and not rec.is_test
        is_interesting_doc = is_doc_rel(rec.rel) and is_high_signal_doc(rec.rel, rec.text)
        if not is_interesting_source and not is_interesting_doc:
            continue
        if (
            rec.score >= 120
            or is_too_large_for_embedding(rec, max_file_lines)
            or is_vendored_or_upstream_rel(rec.rel)
            or is_interesting_doc
        ):
            candidates.append(rec)

    return sorted(
        candidates,
        key=lambda r: (
            not is_too_large_for_embedding(r, max_file_lines),
            is_vendored_or_upstream_rel(r.rel),
            -r.score,
            r.rel,
        ),
    )[:max_items]


def render_size_bytes(text: str) -> int:
    return len(text.encode("utf-8"))


def enforce_bundle_budget(
    repo: Path,
    package_text: str,
    targets: list[dict],
    records: list[FileRecord],
    selected: list[FileRecord],
    max_bytes: int,
    max_file_lines: int,
    manifest_source: str,
) -> tuple[list[FileRecord], list[FileRecord], str]:
    selected = list(selected)
    omitted = important_omitted_files(records, selected, max_file_lines)
    bundle = render_bundle(
        repo,
        package_text,
        targets,
        records,
        selected,
        omitted,
        manifest_source,
        max_file_lines,
    )
    if max_bytes <= 0:
        return selected, omitted, bundle

    while render_size_bytes(bundle) > max_bytes:
        removable = [rec for rec in selected if rec.rel != "Package.swift"]
        if not removable:
            break
        victim = sorted(
            removable,
            key=lambda r: (
                line_count(r.text),
                -r.score,
                is_doc_rel(r.rel),
                r.rel,
            ),
            reverse=True,
        )[0]
        selected.remove(victim)
        omitted = important_omitted_files(records, selected, max_file_lines)
        bundle = render_bundle(
            repo,
            package_text,
            targets,
            records,
            selected,
            omitted,
            manifest_source,
            max_file_lines,
        )

    return selected, omitted, bundle


def condensed_tree(paths: Iterable[str]) -> str:
    tree: dict = {}
    for rel in sorted(set(paths)):
        cursor = tree
        parts = rel.split("/")
        for part in parts:
            cursor = cursor.setdefault(part, {})

    lines: list[str] = []

    def walk(node: dict, prefix: str) -> None:
        keys = sorted(node.keys())
        for idx, key in enumerate(keys):
            branch = "└── " if idx == len(keys) - 1 else "├── "
            lines.append(f"{prefix}{branch}{key}")
            extension = "    " if idx == len(keys) - 1 else "│   "
            walk(node[key], prefix + extension)

    walk(tree, "")
    return "\n".join(lines) if lines else "(no paths selected)"


def collect_arch_signals(records: list[FileRecord]) -> dict[str, list[tuple[str, str]]]:
    signals = {
        "public_types": [],
        "protocols": [],
        "core_models": [],
        "state_containers": [],
        "services": [],
        "di_entrypoints": [],
        "composition_entrypoints": [],
    }

    for rec in records:
        if not rec.is_swift or rec.is_test or is_vendored_or_upstream_rel(rec.rel):
            continue
        for match in TYPE_RE.finditer(rec.text):
            is_public = bool(match.group(1))
            kind = match.group(2)
            name = match.group(3)
            if is_public:
                signals["public_types"].append((name, rec.rel))
            if kind == "protocol":
                signals["protocols"].append((name, rec.rel))
            lname = name.lower()
            if any(k in lname for k in ("model", "entity", "record", "payload")):
                signals["core_models"].append((name, rec.rel))
            if any(k in lname for k in ("store", "state", "viewmodel", "reducer", "controller")):
                signals["state_containers"].append((name, rec.rel))
            if any(k in lname for k in ("service", "repository", "provider", "client", "gateway")):
                signals["services"].append((name, rec.rel))
            if any(k in lname for k in ("container", "assembly", "inject", "dependency", "bootstrap")):
                signals["di_entrypoints"].append((name, rec.rel))
            if (
                lname == "app"
                or lname.endswith("app")
                or any(k in lname for k in ("scene", "router", "coordinator", "navigator", "composition"))
            ):
                signals["composition_entrypoints"].append((name, rec.rel))

    for key, entries in signals.items():
        deduped: list[tuple[str, str]] = []
        seen = set()
        for name, rel in entries:
            token = (name, rel)
            if token in seen:
                continue
            seen.add(token)
            deduped.append(token)
        signals[key] = deduped[:14]
    return signals


def summarize_module(target: dict, records: list[FileRecord]) -> tuple[str, str, str]:
    name = target["name"]
    deps = target.get("dependencies", [])
    target_path = target.get("path") or ""
    if target_path:
        module_files = [r for r in records if is_under_root(r.rel, target_path) and not is_vendored_or_upstream_rel(r.rel)]
    else:
        module_files = [
            r
            for r in records
            if r.rel.startswith(f"Sources/{name}/") and not is_vendored_or_upstream_rel(r.rel)
        ]
    if not module_files:
        module_files = [
            r
            for r in records
            if f"/{name}/" in r.rel and r.rel.endswith(".swift") and not is_vendored_or_upstream_rel(r.rel)
        ]

    role = "Responsibility inferred from naming and key type declarations."
    if module_files:
        top_names = [Path(r.rel).name for r in sorted(module_files, key=lambda r: (-r.score, r.rel))[:3]]
        role = f"Inferred core role from files: {', '.join(top_names)}."
    deps_text = ", ".join(deps) if deps else "(none declared)"
    return name, role, deps_text


def detect_persistence_network_patterns(records: list[FileRecord]) -> list[str]:
    joined = "\n".join(r.text for r in records if r.is_swift)
    findings: list[str] = []
    checks = [
        ("URLSession", "network boundary likely present (`URLSession`)"),
        ("FileManager", "filesystem persistence boundary likely present (`FileManager`)"),
        ("JSONDecoder", "JSON decode/parse boundary present (`JSONDecoder`)"),
        ("SQLite", "SQLite persistence usage detected"),
        ("CoreData", "CoreData persistence usage detected"),
        ("XMLParser", "document parsing boundary likely present (`XMLParser`)"),
    ]
    for token, message in checks:
        if token in joined:
            findings.append(message)
    return findings


def important_file_rationale(rec: FileRecord) -> str:
    deduped: list[str] = []
    for reason in rec.reasons:
        if reason not in deduped:
            deduped.append(reason)
    return "; ".join(deduped[:3])


def language_hint(rel: str) -> str:
    suffix = Path(rel).suffix.lower()
    return {
        ".swift": "swift",
        ".md": "markdown",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".json": "json",
        ".sh": "bash",
    }.get(suffix, "text")


def fenced_code(content: str, lang: str) -> str:
    fence = "```"
    if "```" in content:
        fence = "````"
    return f"{fence}{lang}\n{content.rstrip()}\n{fence}"


def review_notes(records: list[FileRecord], selected: list[FileRecord]) -> dict[str, list[str]]:
    strengths: list[str] = []
    risks: list[str] = []
    tradeoffs: list[str] = []
    opportunities: list[str] = []

    protocol_files = sum(
        1
        for r in records
        if r.is_swift
        and not is_vendored_or_upstream_rel(r.rel)
        and re.search(r"^\s*(?:public\s+)?protocol\s+\w+", r.text, flags=re.MULTILINE)
    )
    if protocol_files:
        strengths.append(f"Protocol-oriented abstraction appears in {protocol_files} file(s).")

    if any(r.rel.startswith("Tests/") for r in records):
        strengths.append("Repository includes test targets, which improves review-context confidence.")

    hardcoded_workspace = sum(1 for r in records if "/workspace" in r.text)
    if hardcoded_workspace:
        risks.append(
            f"Found {hardcoded_workspace} file(s) referencing hardcoded `/workspace` paths; runtime injection may be incomplete."
        )

    oversized = [r.rel for r in records if r.is_swift and line_count(r.text) > 900]
    if oversized:
        risks.append(f"Very large source files detected: {', '.join(oversized[:4])}.")

    if not any("dependency" in r.text.lower() for r in records if r.is_swift):
        tradeoffs.append("Dependency wiring intent appears mostly implicit; fast iteration but lower discoverability.")
    else:
        tradeoffs.append("Dependency-centric naming suggests clearer boundaries, with additional indirection cost.")

    opportunities.append("Promote key architecture decisions into lightweight docs when inferred intent is not explicit.")
    if hardcoded_workspace:
        opportunities.append("Replace hardcoded workspace path assumptions with injected runtime configuration.")

    if not strengths:
        strengths.append("Module boundaries are present in Swift Package target structure.")
    if not risks:
        risks.append("No major structural risks were flagged by static name/layout heuristics; verify with runtime and test evidence.")

    return {
        "strengths": strengths[:4],
        "risks": risks[:4],
        "tradeoffs": tradeoffs[:3],
        "opportunities": opportunities[:4],
    }


def render_bundle(
    repo: Path,
    package_text: str,
    targets: list[dict],
    records: list[FileRecord],
    selected: list[FileRecord],
    omitted_important: list[FileRecord] | None = None,
    manifest_source: str = "Package.swift text scan",
    max_file_lines: int = 900,
) -> str:
    repo_name = repo.name
    overview, style_summary = infer_overview(package_text, targets, repo_name)
    signals = collect_arch_signals(records)
    review = review_notes(records, selected)

    tree_paths = [r.rel for r in selected]
    tree_text = condensed_tree(tree_paths)

    module_lines: list[str] = []
    if targets:
        for target in targets:
            name, role, deps = summarize_module(target, records)
            module_lines.append(f"- `{name}` ({target['kind']}): {role} Dependencies: {deps}.")
    else:
        source_modules = sorted({module_name_for_rel(r.rel) for r in records if r.rel.startswith("Sources/")})
        for module in source_modules:
            module_lines.append(
                f"- `{module}` (inferred target/module): responsibility inferred from `Sources/{module}` file set."
            )
        if not module_lines:
            module_lines.append("- No clear module directories found under `Sources/`.")

    pattern_lines: list[str] = []
    if signals["state_containers"]:
        names = ", ".join(name for name, _ in signals["state_containers"][:6])
        pattern_lines.append(f"- State flow likely centers on: {names}.")
    else:
        pattern_lines.append("- State flow: inferred as local/ad-hoc (no explicit state container names detected).")

    if signals["services"]:
        names = ", ".join(name for name, _ in signals["services"][:6])
        pattern_lines.append(f"- Data/service flow likely crosses: {names}.")
    else:
        pattern_lines.append("- Data flow: mostly direct model/utility usage (few service/repository markers).")

    if signals["di_entrypoints"]:
        names = ", ".join(name for name, _ in signals["di_entrypoints"][:6])
        pattern_lines.append(f"- Dependency injection/composition entrypoints: {names}.")
    else:
        pattern_lines.append("- Dependency injection: no explicit container/assembly types detected (inferred).")

    if signals["composition_entrypoints"]:
        names = ", ".join(name for name, _ in signals["composition_entrypoints"][:6])
        pattern_lines.append(f"- Rendering/navigation/composition entrypoints: {names}.")

    boundaries = detect_persistence_network_patterns(records)
    if boundaries:
        pattern_lines.extend([f"- {item}." for item in boundaries])
    else:
        pattern_lines.append("- Persistence/network/document parsing boundaries not strongly signaled in static scan.")

    abstraction_lines: list[str] = []
    for label, key in [
        ("Public API types", "public_types"),
        ("Protocols", "protocols"),
        ("Core models", "core_models"),
        ("State containers", "state_containers"),
        ("Services/repositories/providers", "services"),
    ]:
        entries = signals[key]
        if entries:
            value = ", ".join(f"`{name}` ({rel})" for name, rel in entries[:8])
            abstraction_lines.append(f"- {label}: {value}.")
        else:
            abstraction_lines.append(f"- {label}: none strongly signaled.")

    important_lines: list[str] = []
    ordered_for_reading = [r for r in selected if r.rel.endswith(".swift") or r.rel == "Package.swift"]
    for idx, rec in enumerate(ordered_for_reading[:14], start=1):
        important_lines.append(f"{idx}. `{rec.rel}` - {important_file_rationale(rec)}.")

    selected_sections: list[str] = []
    for rec in selected:
        if rec.rel.startswith("Tests/") and not rec.rel.endswith(".swift"):
            continue
        selected_sections.append(f"## `{rec.rel}`")
        selected_sections.append(f"- file path: `{rec.rel}`")
        selected_sections.append(f"- why it matters: {important_file_rationale(rec)}.")
        selected_sections.append("")
        selected_sections.append(fenced_code(rec.text, language_hint(rec.rel)))
        selected_sections.append("")

    lines: list[str] = []
    lines.append("# Repository Overview")
    lines.append(f"- Repository: `{repo_name}`")
    lines.append(f"- Summary: {overview}")
    lines.append(f"- Architecture style: {style_summary}")
    lines.append(f"- Main modules/targets: {', '.join(t['name'] for t in targets) if targets else '(inferred from Sources/)'}")
    lines.append(f"- Manifest source: {manifest_source}")
    if package_text.strip():
        lines.append("- Uncertainty: architecture intent is inferred when not explicitly documented.")
    else:
        lines.append("- Uncertainty: `Package.swift` was not found; module and dependency information is layout-inferred.")
    lines.append("")

    lines.append("# Directory Tree")
    lines.append("```text")
    lines.append(tree_text)
    lines.append("```")
    lines.append("")

    lines.append("# Module Summary")
    lines.extend(module_lines)
    lines.append("")

    lines.append("# Key Architectural Patterns")
    lines.extend(pattern_lines)
    lines.append("")

    lines.append("# Key Abstractions")
    lines.extend(abstraction_lines)
    lines.append("")

    lines.append("# Important Files to Read First")
    lines.extend(important_lines if important_lines else ["1. `Sources/` - inferred source layout."])
    if omitted_important:
        lines.append("")
        lines.append("Omitted but important:")
        for rec in omitted_important:
            lines.append(f"- `{rec.rel}` - {omitted_file_rationale(rec, max_file_lines)}.")
    lines.append("")

    lines.append("# Selected Source Files")
    lines.extend(selected_sections)

    lines.append("# Review Notes")
    lines.append("- Review posture: static-scan cues for review focus, not a final architecture verdict.")
    lines.append("- Strengths:")
    lines.extend([f"  - {item}" for item in review["strengths"]])
    lines.append("- Risks:")
    lines.extend([f"  - {item}" for item in review["risks"]])
    lines.append("- Design tradeoffs:")
    lines.extend([f"  - {item}" for item in review["tradeoffs"]])
    lines.append("- Possible refactoring opportunities:")
    lines.extend([f"  - {item}" for item in review["opportunities"]])

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    repo = Path(args.repo_path).expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        raise SystemExit(f"Repository path does not exist or is not a directory: {repo}")

    package_text = read_package_text(repo)
    targets, manifest_source = load_targets(repo, package_text)

    files = walk_repo(repo)
    records = make_records(repo, files, targets)

    max_file_lines = max(1, args.max_file_lines)
    selected = select_files(
        records,
        max_files=max(8, args.max_files),
        include_tests=args.include_tests,
        max_file_lines=max_file_lines,
    )
    selected, omitted, bundle = enforce_bundle_budget(
        repo,
        package_text,
        targets,
        records,
        selected,
        max_bytes=args.max_bytes,
        max_file_lines=max_file_lines,
        manifest_source=manifest_source,
    )

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else repo / "architecture-review-bundle.md"
    )
    output_path.write_text(bundle, encoding="utf-8")
    print(f"Wrote bundle: {output_path}")
    print(f"Selected files: {len(selected)}")
    print(f"Omitted important files: {len(omitted)}")
    print(f"Bundle bytes: {render_size_bytes(bundle)}")


if __name__ == "__main__":
    main()
