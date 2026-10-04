# Official Source Index

Read this file after selecting the `official` profile in `swiftpm-index`
when source category or authority needs to be classified.

## Source Categories

- `apple_package_collection`: Apple Swift Package Collection. Primary source
  seed for Apple official package candidates.
- `swiftlang_repository`: repositories under `github.com/swiftlang`. Primary
  source for Swift project official packages and toolchain-adjacent packages.
- `apple_authored_repository`: repositories under `github.com/apple`.
  Official Apple-authored packages, but not automatically adoptable.
- `official_documentation`: swift.org, docs.swift.org, developer.apple.com,
  official package README/docs/Package.swift, and official Swift Forums
  announcements or proposals when relevant.
- `spi_crosscheck`: Swift Package Index Apple and swiftlang owner pages.
  Discovery and cross-check only.
- `spi_package_list`: community package inventory. Not official source; use the
  SPI profile and verify repository source before adoption.
- `target_package_source`: the local package being audited.

## Tool References

- `swift_package_collection_generator`:
  `swiftlang/swift-package-collection-generator` fixed runtime tool backend for
  package collection JSON generation, validation, diffing, and signing. It is
  not a source category, authority tier, or package adoption candidate.

## Authority Summary

- P0: local package source
- P1: official package source
- P2: official documentation
- P3: SPI discovery/cross-check only

Do not use P3 as final authority for adoption.
