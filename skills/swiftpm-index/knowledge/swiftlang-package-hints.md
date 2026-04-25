# swiftlang Package Hints

Read this file after the target package capability inventory suggests a Swift
project official or toolchain-adjacent candidate.

This is a curated hint list, not a complete swiftlang repository catalog. Use it
to recognize common target-code patterns and likely official candidates. Use the
CLI index or P1 official sources for current package facts such as repository,
manifest status, products/modules, platform support, and package status.

## Known High-Value Hints

| Trigger pattern | Candidate | Default review stance | Caution |
|---|---|---|---|
| custom Swift parser, rewriter, formatter input model, or source generator | `swift-syntax` | Adopt / Wrap | Keep syntax APIs behind a facade if public API stability matters. |
| custom Markdown parser, renderer, or document editor | `swift-markdown` | Adopt / Wrap | Simple pass-through Markdown rendering may not justify a dependency. |
| custom test DSL or migration from ad hoc test helpers | `swift-testing` | Adopt / Reference | Test-only dependencies should not leak to library consumers. |
| custom documentation compiler integration | `swift-docc` | Reference / Wrap | Often a tooling dependency rather than runtime dependency. |
| custom SwiftPM DocC scripts | `swift-docc-plugin` | Adopt / Wrap | Prefer plugin use when the package owns DocC generation. |
| custom Swift formatter or linter scripts | `swift-format` | Adopt / Wrap | Formatting may be repo workflow, not package architecture. |
| custom subprocess runner | `swift-subprocess` | Adopt / Wrap | Foundation `Process` may be sufficient for simple cases. |
| custom package graph, manifest, or SwiftPM integration | `swift-package-manager` | Reference | Most SwiftPM internals are not normal library dependencies. |
| custom build-system integration | `swift-build` | Reference | Treat as toolchain-adjacent unless public package role is verified. |
| custom SDK bundle generation | `swift-sdk-generator` | Reference / Wrap | Usually relevant only for SDK-generation tooling. |
| custom SourceKit or LSP integration | `sourcekit-lsp` | Reference | Runtime libraries should normally not depend on language-server tooling. |
| custom indexstore readers | `indexstore-db` | Adopt / Wrap | Only relevant for compiler index data processing. |
| custom Foundation-adjacent implementation | `swift-foundation` | Reference | Standard Foundation APIs are usually the dependency boundary. |
