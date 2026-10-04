# CLI Contract

This directory contains the source-acquisition CLI named `swiftpm-index`.

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

## Responsibilities

The CLI is for manual source acquisition, freshness review, drift checking,
discovery, and export. Ordinary coding-time lightweight checks should start
from curated `knowledge/` hints and should not require running the CLI.

The CLI may:

- fetch official source lists
- fetch Swift Package Index PackageList community repository inventory
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

## macOS Runtime Paths

State, snapshots, normalized index, and diffs:

```text
~/Library/Application Support/swiftpm-index/
├── config.json
├── state.json
├── snapshots/
│   ├── apple-package-collection/
│   ├── apple-repositories/
│   ├── swiftlang-repositories/
│   ├── spi-crosscheck/
│   ├── spi-package-list/
│   └── package-manifest-enrichment/
├── latest/
│   ├── apple-package-collection.json
│   ├── apple-repositories.json
│   ├── swiftlang-repositories.json
│   ├── spi-crosscheck.json
│   ├── spi-package-list.json
│   ├── package-manifest-enrichment.json
│   ├── official-package-index.json
│   └── official-package-index.md
├── normalized/
├── diffs/
└── tools/
    └── swift-package-collection-generator/
```

Cache, HTTP cache, ETag, and rate-limit metadata:

```text
~/Library/Caches/swiftpm-index/
├── http/
├── etags.json
└── rate-limit.json
```

Logs:

```text
~/Library/Logs/swiftpm-index/
```

## Explicit Export Bundle

Only write export/review bundles when the user provides `--output <path>`.

Example:

```bash
swiftpm-index export --output ./artifacts/swiftpm-index
```

The exported bundle may contain:

- `official-package-index.json`
- `official-package-index.md`
- `spi-package-list.json`, when `fetch-spi` has been run
- `source-summary.md`
- `diff.md`
- `manifest.json`

## Output Semantics

Generated official indexes contain official candidates and normalized index
entries. Apple Swift Package Collection entries are high-signal package seeds.
Apple and swiftlang GitHub org entries are official repository candidates until
package manifest and product/module facts are verified.

`fetch-spi` fetches the Swift Package Index PackageList repository inventory.
`search-spi` filters that inventory locally and returns discovery candidates
only. Community candidates require repository source, license, releases,
maintenance activity, supported platforms, Swift tools version, dependency tree,
and public API impact checks before any adoption recommendation.

`enrich` checks root `Package.swift` presence and records GitHub primary
language as candidate-quality metadata for official candidates. It uses those
facts for filtering and grouping only; final Adopt / Wrap / Reference / Keep
custom recommendations still require target code evidence and candidate source
evidence.

## Package Collection Tool Backend

SwiftPM native package collection generation, validation, diffing, and signing
run through `swiftlang/swift-package-collection-generator` as a fixed tool
backend.

Pinned tool snapshot:

```text
branch: main
commit: 7bc2514946443f31242f17c25365c97491674d27
commit date: 2025-10-17
versioned branches observed: 5.5, 5.6, 5.7, 5.8, 5.9, 5.10
```

The CLI currently parses Apple Package Collection directly and does not shell
out to this tool. Treat the tool as the execution backend for package collection
export, validate, diff, or sign behavior, not as package adoption authority.

SwiftPM does not currently have a `swift run <git-url> <product>` one-shot
remote execution command. If this backend is needed, use the fixed CLI command
to clone the pinned tool snapshot into runtime storage and run products
from that package path:

```bash
swiftpm-index ensure-package-collection-tool --build
swiftpm-index package-collection-tool package-collection-validate -- <collection.json>
swiftpm-index package-collection-tool package-collection-diff -- <old.json> <new.json>
```

Do not vendor the tool checkout or its build products into this skill.

Supported package collection tool products:

- `package-collection-generate`
- `package-collection-validate`
- `package-collection-diff`
- `package-collection-sign`

The first execution can be slow because SwiftPM resolves and builds the tooling
package and its SwiftPM dependencies. Keep the pinned runtime cache between
runs.
