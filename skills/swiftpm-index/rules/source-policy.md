# Source Policy

Use this rule when deciding what evidence can support a Swift library
recommendation.

## Authority Order

P0. Local target source:

- `Package.swift`
- `Sources/`
- `Tests/`
- `Docs/`
- `README.md`
- `AGENTS.md`
- `Examples/`
- `Plugins/`
- existing dependencies

P1. Candidate source:

- official Apple/swiftlang package source
- community package repository source
- candidate `README`, docs, `Package.swift`, releases, license, and dependency
  manifest
- local workspace package source

P2. Official context:

- `swift.org`
- `docs.swift.org`
- `developer.apple.com`
- official Swift Forums announcements and proposals when relevant

P3. Discovery / cross-check:

- Apple Swift Package Collection
- GitHub org inventory for `apple` and `swiftlang`
- Swift Package Index package pages and PackageList repository
- package collection metadata

## Excluded Evidence

- GitHub star ranking as adoption evidence by itself
- blog posts as source truth
- AI-generated package lists as source truth
- package search results without source verification
- non-Swift package registries unless the target explicitly depends on them

## Rule

Use P0 to understand the target package. Use P1 to understand candidate
capabilities and adoption risk. Use P2 for official context. Use P3 to discover
or cross-check candidates, never as final authority for adoption.

## SPI Guardrails

- Do not use SPI during automatic lightweight coding-time checks.
- Use SPI only when the user explicitly asks for ecosystem discovery, when a
  manual full-index audit selects the SPI or mixed profile, or when maintaining
  SPI discovery metadata.
- Label SPI candidates clearly as official Apple-authored, official swiftlang,
  community, or unknown before using them in a recommendation.
- Do not silently promote SPI community packages into curated official
  knowledge.
- Do not recommend SPI community packages from discovery metadata alone.
