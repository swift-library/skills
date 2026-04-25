#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import build_swift_package_bundle as builder


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render(repo: Path, max_files: int = 8) -> str:
    package_text = builder.read_package_text(repo)
    targets = builder.parse_targets(package_text)
    records = builder.make_records(repo, builder.walk_repo(repo), targets)
    selected = builder.select_files(records, max_files=max_files, include_tests=False)
    return builder.render_bundle(repo, package_text, targets, records, selected)


def render_with_budget(
    repo: Path,
    max_files: int = 8,
    max_bytes: int = 80_000,
    max_file_lines: int = 900,
) -> str:
    package_text = builder.read_package_text(repo)
    targets = builder.parse_targets(package_text)
    records = builder.make_records(repo, builder.walk_repo(repo), targets)
    selected = builder.select_files(
        records,
        max_files=max_files,
        include_tests=False,
        max_file_lines=max_file_lines,
    )
    _, _, bundle = builder.enforce_bundle_budget(
        repo,
        package_text,
        targets,
        records,
        selected,
        max_bytes=max_bytes,
        max_file_lines=max_file_lines,
        manifest_source="test manifest",
    )
    return bundle


class BuildSwiftPackageBundleTests(unittest.TestCase):
    def test_dump_package_payload_normalizes_target_metadata(self) -> None:
        payload = {
            "targets": [
                {
                    "name": "App",
                    "type": "executable",
                    "path": "Tools/App",
                    "dependencies": [
                        {"byName": ["Core", None]},
                        {"product": ["ArgumentParser", "swift-argument-parser", None]},
                    ],
                },
                {
                    "name": "CoreTests",
                    "type": "test",
                    "dependencies": [{"target": ["Core", None]}],
                },
            ],
        }

        targets = builder.targets_from_dump_payload(payload)

        self.assertEqual(targets[0]["kind"], "executableTarget")
        self.assertEqual(targets[0]["path"], "Tools/App")
        self.assertEqual(targets[0]["dependencies"], ["Core", "ArgumentParser"])
        self.assertEqual(targets[1]["kind"], "testTarget")
        self.assertEqual(targets[1]["dependencies"], ["Core"])

    def test_docs_heavy_repo_still_selects_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write(
                repo / "Package.swift",
                """
import PackageDescription

let package = Package(
  name: "DocsHeavy",
  targets: [
    .target(name: "Core"),
  ]
)
""",
            )
            write(repo / "README.md", "# DocsHeavy\n")
            write(repo / "Docs/Architecture/README.md", "# Architecture\nBoundary notes.\n")
            for idx in range(8):
                write(repo / f"Docs/Usage/Feature{idx}/README.md", "# Usage\nExamples only.\n")
            write(
                repo / "Sources/Core/CoreService.swift",
                """
public protocol CoreService {
  func run()
}
""",
            )

            bundle = render(repo)

            self.assertIn("## `Sources/Core/CoreService.swift`", bundle)
            self.assertIn("## `Docs/Architecture/README.md`", bundle)
            self.assertNotIn("Docs/Usage/Feature7/README.md", bundle)

    def test_non_package_swift_does_not_pollute_arch_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write(
                repo / "Package.swift",
                """
import PackageDescription

let package = Package(
  name: "Scoped",
  targets: [
    .target(name: "Scoped"),
  ]
)
""",
            )
            write(repo / "Sources/Scoped/StoreType.swift", "public protocol StoreType {}\n")
            write(repo / "stash/OldReducer.swift", "public protocol OldReducerType {}\n")
            write(
                repo / "Sources/Scoped/Upstreams/VendorClient.swift",
                "public protocol VendorClient {}\n",
            )
            write(
                repo / "Sources/Scoped/Embedded/Sources/Embedded/EmbeddedClient.swift",
                "public protocol EmbeddedClient {}\n",
            )

            bundle = render(repo)

            self.assertIn("`StoreType` (Sources/Scoped/StoreType.swift)", bundle)
            self.assertNotIn("OldReducerType", bundle)
            self.assertNotIn("stash/OldReducer.swift", bundle)
            self.assertNotIn("VendorClient", bundle)
            self.assertNotIn("EmbeddedClient", bundle)

    def test_missing_package_swift_falls_back_to_layout_inference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write(repo / "Sources/Inferred/InferredClient.swift", "public struct InferredClient {}\n")

            bundle = render(repo)

            self.assertIn("does not contain `Package.swift`", bundle)
            self.assertIn("- Main modules/targets: (inferred from Sources/)", bundle)
            self.assertIn("## `Sources/Inferred/InferredClient.swift`", bundle)
            self.assertNotIn("## `Package.swift`", bundle)

    def test_large_important_file_is_listed_not_embedded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write(
                repo / "Package.swift",
                """
import PackageDescription

let package = Package(
  name: "Budgeted",
  targets: [
    .target(name: "Budgeted"),
  ]
)
""",
            )
            write(repo / "Sources/Budgeted/SmallModel.swift", "public struct SmallModel {}\n")
            huge_lines = "\n".join(["public protocol HugeClient {"] + ["  func call()"] * 40 + ["}"])
            write(repo / "Sources/Budgeted/HugeClient.swift", huge_lines)

            bundle = render_with_budget(repo, max_file_lines=20)

            self.assertIn("Omitted but important:", bundle)
            self.assertIn("`Sources/Budgeted/HugeClient.swift` - exceeds per-file embed budget", bundle)
            self.assertNotIn("## `Sources/Budgeted/HugeClient.swift`", bundle)
            self.assertIn("## `Sources/Budgeted/SmallModel.swift`", bundle)


if __name__ == "__main__":
    unittest.main()
