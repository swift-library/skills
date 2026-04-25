# Catalog Normalization

Use this rule when shaping fetched official, SPI, local, or curated hint data.

## Normalized Index Entry Fields

- entry name
- repository URL
- source categories
- primary source category
- authority level
- entry kind
- adoptability basis
- package manifest status
- primary language
- language filter status
- Swift package candidate flag
- candidate confidence
- dependency role hint
- fetched summary or description
- repository metadata when available: archived, fork, language, default branch,
  pushed date, and updated date
- license and maintenance metadata when available
- package products/modules
- purpose
- maturity/status notes
- supported platforms
- Swift tools version
- dependency role: normal dependency, tool, plugin, toolchain/internal, or
  reference-only
- source-needed notes

## Review Rules

- Preserve source category and authority level on every entry.
- Preserve Apple Swift Package Collection as the primary source category when a
  matching GitHub repository also appears, but enrich missing fields from
  GitHub metadata.
- Treat GitHub org repository entries as official candidates until
  `Package.swift`, products, modules, and package role are verified.
- Treat SPI PackageList entries as community discovery candidates until
  repository source, license, releases, maintenance, products/modules,
  platforms, and dependency tree are verified.
- Use primary language as a filtering signal only. `language == "Swift"`
  raises review priority but does not prove adoptability.
- Use root `Package.swift` presence as a stronger package-candidate signal, but
  do not infer products/modules until manifest parsing exists.
- Mark uncertain facts with `TODO(source-needed)`.
- Keep fetched output separate from curated `knowledge/` files.
- Do not promote a package to adoptable only because it exists in an official
  namespace.
- Keep SPI data as discovery/cross-check metadata only until verified against
  candidate repository source.
