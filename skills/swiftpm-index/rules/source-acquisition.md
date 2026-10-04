# Source Acquisition

Use this rule when working with the `swiftpm-index` CLI or reviewing
source list updates.

## CLI Responsibility

The CLI belongs to the manual source-acquisition and maintenance layer. It is
not a prerequisite for ordinary coding-time progressive disclosure.

It may:

- fetch official source lists
- fetch Swift Package Index PackageList community repository inventory
- run SwiftPM package collection tooling as a fixed backend for collection
  generation, validation, diffing, and signing
- enrich official repository candidates with mechanical quality signals
- normalize fetched metadata
- produce latest indexes
- produce diff reports between fetches
- render reviewable markdown output
- export portable review bundles when explicitly requested

The CLI must not:

- make Adopt / Wrap / Reference / Keep custom recommendations by itself
- rewrite package source code
- automatically mutate curated `knowledge/` files
- treat generated or fetched source lists as curated skill truth
- treat primary language, root `Package.swift` presence, SPI presence, or stars
  as recommendations by themselves

## Coding-Time Relationship

Automatic lightweight checks should start from curated `knowledge/` hints and
target code evidence. Use the CLI when the task is full index maintenance,
freshness/drift review, SPI discovery, local candidate discovery, source
refresh, or explicit review-bundle export.

## Commands

```bash
swiftpm-index update
swiftpm-index fetch
swiftpm-index fetch-spi
swiftpm-index search-spi --query <term> [--limit <n>]
swiftpm-index ensure-package-collection-tool [--build]
swiftpm-index package-collection-tool [--build] <product> [-- <arguments>...]
swiftpm-index enrich
swiftpm-index diff
swiftpm-index render
swiftpm-index export --output <path>
swiftpm-index show-paths
```

## Swift Package Collection Tooling

`swift-package-collection-generator` is the current fixed tool backend for
SwiftPM native package collection generation, validation, diffing, and signing.

Pinned tool snapshot:

```text
repository: swiftlang/swift-package-collection-generator
branch: main
commit: 7bc2514946443f31242f17c25365c97491674d27
commit date: 2025-10-17
versioned branches observed: 5.5, 5.6, 5.7, 5.8, 5.9, 5.10
```

The `main` branch follows SwiftPM `main` and may be unstable. Prefer a
matching versioned branch for build-backed use.

Use this tooling as a skill-local execution backend, not as a source category or
adoption authority. Its useful boundary for `swiftpm-index` is:

- generate SwiftPM-native package collection JSON from a curated package list
- validate a generated package collection
- diff two package collection JSON files
- sign package collection JSON when publishing requires signatures

The current `swiftpm-index` CLI parses Apple Package Collection directly. It
does not require this Swift tool for ordinary source acquisition.

SwiftPM does not provide a `swift run <git-url> <product>` one-shot remote
execution command. When this tool is needed, acquire it into runtime storage
with the fixed CLI command instead of vendoring the source into the skill:

```bash
swiftpm-index ensure-package-collection-tool --build
swiftpm-index package-collection-tool package-collection-validate -- <collection.json>
swiftpm-index package-collection-tool package-collection-diff -- <old.json> <new.json>
```

Use a fresh or pinned cache clone when reproducibility matters. Do not store the
tool checkout, build products, or fetched package repositories inside the skill
directory.

Use `package-collection-tool` as the fixed execution wrapper for supported
products:

- `package-collection-generate`
- `package-collection-validate`
- `package-collection-diff`
- `package-collection-sign`

The first execution can be slow because SwiftPM resolves and builds the
tooling package and its SwiftPM dependencies. Prefer the pinned runtime cache
over fresh ad-hoc clones.

## Runtime Storage

Do not store fetched runtime artifacts inside the skill directory by default.

State, snapshots, normalized indexes, and diffs:

```text
~/Library/Application Support/swiftpm-index/
```

Tool checkouts used by optional package collection backends:

```text
~/Library/Application Support/swiftpm-index/tools/
```

Cache, HTTP cache, ETags, and rate-limit metadata:

```text
~/Library/Caches/swiftpm-index/
```

Logs:

```text
~/Library/Logs/swiftpm-index/
```

Write export/review bundles only when the user provides `--output <path>`.
