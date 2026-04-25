# Source Acquisition

Use this rule when working with the `swiftpm-index` CLI or reviewing
source list updates.

## CLI Responsibility

The CLI belongs to the manual source-acquisition and maintenance layer. It is
not a prerequisite for ordinary coding-time progressive disclosure.

It may:

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
swiftpm-index enrich
swiftpm-index diff
swiftpm-index render
swiftpm-index export --output <path>
swiftpm-index show-paths
```

## Runtime Storage

Do not store fetched runtime artifacts inside the skill directory by default.

State, snapshots, normalized indexes, and diffs:

```text
~/Library/Application Support/swiftpm-index/
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
