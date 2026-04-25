# Candidate Matching

Use this rule when mapping target package code patterns to library candidates.

## Entry Mode

- Automatic lightweight checks use curated official Apple/swiftlang hints only.
  Do not add SPI/community candidates to the default coding-time check.
- Manual full index / discovery may use generated indexes, SPI PackageList
  data, local workspace candidates, and exported review bundles when the user
  explicitly asks for that broader scope.

## Inputs

- Target evidence from P0 source: imports, files, symbols, tests, docs,
  scripts, plugins, and dependency usage.
- Candidate discovery fields from the generated index: fetched `summary`,
  `description`, `source_categories`, `entry_kind`, `package_manifest_status`,
  `primary_language`, `language_filter_status`, `swift_package_candidate`,
  `candidate_confidence`, `adoptability_basis`, and `status_notes`.
- Candidate evidence from P1/P2 sources: README/docs/Package.swift, products,
  modules, supported platforms, release state, license, maintenance, and status
  notes.
- Curated hints from `knowledge/replacement-patterns.md`,
  `knowledge/apple-package-hints.md`, and `knowledge/swiftlang-package-hints.md`.

## Matching Rule

- For automatic coding-time checks, start from `knowledge/replacement-patterns.md`
  and the official hint files. Emit a short library check note, then continue
  implementation or review.
- Default automatic checks to Evaluate unless verified P1 source evidence is
  already available in the current context.
- Use fetched `summary` and `description` fields to infer candidate capability
  for manual discovery only.
- Treat generated GitHub repository entries as official candidates, not as
  verified adoptable packages, until package manifest and product/module facts
  are checked.
- Treat SPI PackageList entries as community discovery candidates, not as
  verified adoptable packages, until repository source, license, maintenance,
  releases, products/modules, platforms, and dependency tree are checked.
- Use primary language filtering to reduce noise, but do not reject an official
  candidate solely because GitHub language metadata is missing or imperfect.
- Treat root `Package.swift` presence as stronger candidate evidence than
  primary language alone.
- Match candidates against concrete target package patterns, not package names
  alone.
- Verify any plausible match against candidate package source or documentation
  before recommending Adopt or Wrap.
- Final recommendations require target code evidence, candidate source
  evidence, API fit, platform/toolchain fit, dependency cost, license,
  maintenance, and public-boundary impact.
- Treat weak or unverified matches as Reference or Keep custom until source
  evidence improves.

## Fit Levels

- Strong fit: target code duplicates the candidate's documented purpose and
  dependency cost is acceptable.
- Partial fit: candidate covers part of the target behavior or requires a
  local adapter.
- Weak fit: candidate is adjacent, toolchain-facing, or useful mostly as
  design reference.
- No fit: candidate purpose does not match the target package pattern.

## Required Evidence

Every candidate should include:

- target evidence: where the current wheel appears in the target package
- source evidence: which candidate source describes the candidate capability
- matching reason: why the candidate does or does not fit
