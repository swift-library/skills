---
name: swiftpm-index
description: Check Swift package code for custom reusable infrastructure that may duplicate official Apple/swiftlang libraries, including CLI parsing, collections, sequence or async-sequence algorithms, process execution, Markdown or Swift source tooling, DocC/testing/system wrappers, logging, metrics, tracing, HTTP types, OpenAPI, protobuf, crypto, certificates, or ASN.1. Use automatically during implementation or review for lightweight official-library checks, and use manually for full SwiftPM Index audits, SPI discovery, local candidates, source refresh, and Adopt / Wrap / Reference / Keep custom decisions. Do not use for GitHub popularity ranking, Apple SDK framework catalogs, automatic migrations, code rewrites, or non-Swift package discovery.
---

# SwiftPM Index

## Purpose

Find Swift libraries that may replace, wrap, or inform custom implementation in
a target Swift package. The skill has two entry modes:

- **Automatic lightweight check**: coding-time and review-time checks for
  custom reusable Swift infrastructure that may duplicate official
  Apple/swiftlang libraries.
- **Manual full index / discovery**: user-requested full audits, source refresh,
  SPI discovery, local workspace candidate checks, and review bundle exports.

## Entry Modes

### Automatic Lightweight Check

Use this entry when implementation or review is about to introduce, rewrite, or
accept custom reusable Swift infrastructure within the official Apple/swiftlang
capability scope.

Default behavior:

- Use only curated official hints and replacement patterns.
- Do not run CLI refresh/update/search commands as a precondition.
- Do not use SPI/community candidates by default.
- Keep the result short enough to guide implementation without blocking it.

Read in this order:

1. `knowledge/replacement-patterns.md`
2. `knowledge/apple-package-hints.md` or `knowledge/swiftlang-package-hints.md`
3. `rules/recommendation-taxonomy.md` only when the Adopt / Wrap / Reference /
   Keep custom distinction is needed

### Manual Full Index / Discovery

Use this entry when the user explicitly asks for a full audit, dependency
discovery, SPI search, local workspace candidate review, index refresh, drift
check, source acquisition, or export bundle.

Manual mode may use the broader source model:

- **Official profile**: Apple Swift Package Collection, `github.com/apple/*`,
  and `github.com/swiftlang/*`.
- **SPI profile**: community packages discoverable through Swift Package Index
  and its public PackageList repository.
- **Local profile**: repo-local or workspace-local Swift packages.

Read task-specific rules and CLI docs only as needed.

## When To Use

- During Swift implementation or review, when code shape suggests custom
  reusable infrastructure in the official hint scope.
- Audit `Package.swift` and source code for custom wheels that may overlap with
  existing Swift libraries.
- Map target capabilities to official, SPI community, or local workspace
  library candidates.
- Compare dependency cost, API fit, module boundaries, platform/toolchain fit,
  public API leakage, compliance notes when requested, and maintenance signals.
- Produce Adopt / Wrap / Reference / Keep custom recommendations.
- Review or document the source-acquisition CLI contract for official and SPI
  package indexes.

## When Not To Use

- Do not rank packages by GitHub stars or popularity.
- Do not catalog Apple SDK frameworks.
- Do not automatically rewrite source code or migrate dependencies.
- Do not recommend a third-party package from discovery metadata alone.
- Do not treat generated source lists as curated skill truth.

## Inputs To Inspect

- Target package: `Package.swift`, `Sources/`, `Tests/`, `Docs/`, `README.md`,
  `AGENTS.md`, `Examples/`, `Plugins/`, and existing dependencies.
- Official source lists and SPI PackageList output from the CLI when available.
- Curated knowledge files under `knowledge/`.
- Source and workflow rules under `rules/`.
- Report templates under `templates/`.

## Workflow

1. Select the entry mode: automatic lightweight check or manual full index /
   discovery.
2. Inventory the target package capabilities and existing dependencies.
3. Identify custom wheels and classify the audit profile:
   - `official`: only Apple/swiftlang candidates.
   - `spi`: community Swift Package Index candidates.
   - `mixed`: official first, SPI only when official candidates do not fit.
   - `local`: local workspace packages only.
4. Consult source authority in order for the selected profile.
5. Load only the relevant reference files from `rules/` or `knowledge/`.
6. Classify candidates using Adopt / Wrap / Reference / Keep custom.
7. Check dependency cost before recommending adoption.
8. Report migration seams, risks, and recommended next steps.

## Source Categories

- `target_package_source`: local package files being audited.
- `local_workspace_package`: repo-local or workspace-local Swift package.
- `apple_package_collection`: Apple Swift Package Collection seed.
- `swiftlang_repository`: repositories under `github.com/swiftlang`.
- `apple_authored_repository`: repositories under `github.com/apple`.
- `official_documentation`: swift.org, docs.swift.org, developer.apple.com,
  official package docs, and official Swift Forums announcements/proposals.
- `spi_package_list`: Swift Package Index PackageList repository; community
  discovery only until package source and metadata are checked.
- `spi_package_page`: Swift Package Index package page; community discovery and
  health metadata, not final adoption authority by itself.

## Reference Files To Consult

Read only files relevant to the selected operation:

- `rules/source-policy.md`: source authority order and exclusions.
- `rules/source-acquisition.md`: CLI responsibility and storage boundaries.
- `rules/catalog-normalization.md`: normalized catalog shape.
- `rules/candidate-matching.md`: match fetched descriptions and target code
  patterns.
- `rules/audit-workflow.md`: audit sequence and report expectations.
- `rules/recommendation-taxonomy.md`: Adopt / Wrap / Reference / Keep custom.
- `knowledge/official-source-index.md`: official source category index.
- `knowledge/apple-package-hints.md`: curated Apple-authored package hints.
- `knowledge/swiftlang-package-hints.md`: curated swiftlang package hints.
- `knowledge/replacement-patterns.md`: common wheel-to-library mappings.
- `knowledge/non-adoption-patterns.md`: reasons to avoid adoption.
- `cli/README.md`: source-acquisition CLI command contract.
- `templates/`: report and candidate-card formats.

## Decision Rules

- Treat local target source as P0 authority for what the package actually does.
- In automatic lightweight mode, stay official-first and use curated
  Apple/swiftlang hints only.
- Prefer official Apple/swiftlang candidates over community candidates when API
  fit and dependency cost are comparable.
- Treat SPI as discovery and health metadata. Before adopting a community
  package, verify repository source, `Package.swift`, releases, maintenance
  activity, supported platforms, Swift tools version, dependency tree, and
  public-boundary impact.
- Do not use GitHub stars alone as adoption evidence.
- Do not recommend adoption unless platform support, Swift tools version, API
  stability, dependency weight, maintenance, and module-boundary fit are
  acceptable.
- Prefer Adopt when a library can directly replace a matching custom
  implementation without public API leakage.
- Prefer Wrap when the library is useful but public API or module boundaries
  must remain stable.
- Prefer Reference when the candidate is useful mainly as design guidance,
  toolchain-adjacent, unstable, or too heavy to adopt.
- Prefer Keep custom when the candidate is mismatched, heavier than the local
  need, stale, unstable, or boundary-breaking.

## CLI Contract

The source-acquisition CLI name is `swiftpm-index`.

Expected commands:

- `swiftpm-index update`
- `swiftpm-index fetch`
- `swiftpm-index fetch-spi`
- `swiftpm-index search-spi --query <term> [--limit <n>]`
- `swiftpm-index enrich`
- `swiftpm-index diff`
- `swiftpm-index render`
- `swiftpm-index export --output <path>`
- `swiftpm-index show-paths`

The executable lives at `cli/swiftpm-index`.

## Validation Rules

- No fetched runtime artifacts are stored inside the skill directory.
- Generated source lists do not mutate curated `knowledge/` files.
- Automatic lightweight checks do not require CLI refresh, SPI search, or
  runtime indexes.
- CLI enrichment records candidate-quality facts; it does not make
  recommendations.
- Every recommendation cites source category and authority level.
- Each candidate includes dependency-cost checks.
- Community recommendations must include maintenance checks or be marked
  `TODO(source-needed)`.
- Adoption recommendations distinguish normal dependency, wrapped dependency,
  reference-only package, and keep-custom outcome.
- Automatic lightweight checks should default to `Evaluate` unless verified P1
  source evidence is already available in the current context.

## Output Format

For automatic lightweight checks, return a short provisional library check
note:

```markdown
Library check:
- Trigger:
- Candidate:
- Source layer:
- Evidence:
- Provisional decision: Evaluate / Likely Adopt / Likely Wrap / Reference / Keep custom
- Reason:
- Implementation impact:
```

For package audits, return:

1. Phase / stage judgment
2. Target package summary
3. Current capability inventory
4. Existing dependencies
5. Candidate libraries by profile
6. Replacement opportunities
7. Non-replacement decisions
8. Migration seams
9. Risks / compatibility notes
10. Recommended next steps
11. Code diff (key hunks), if files changed

## Failure / Uncertainty Handling

- Stop before code changes unless the user explicitly requests migration.
- If official ownership or package status is unclear, mark it
  `TODO(source-needed)`.
- If SPI data and repository source disagree, prefer repository source and
  report the SPI mismatch.
- If dependency cost is disproportionate, recommend Reference or Keep custom.
