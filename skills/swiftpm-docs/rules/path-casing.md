# Path Casing

Use this rule when scaffolding, normalizing, auditing, or exporting the
repository documentation tree.

## Principle

The canonical `swiftpm-docs` repository tree uses stable, case-sensitive path
segments for documentation roles.

Use the PascalCase-style role directory segments shown by the profiles and
templates:

- `Documentation/Architecture/`
- `Documentation/Proposals/`
- `Documentation/Decisions/`
- `Documentation/Migrations/`
- `Documentation/Archive/`
- `Documentation/Reference/`

Use PascalCase file stems for non-index Markdown documents under those role
directories:

- `Documentation/Architecture/Package.md`
- `Documentation/Architecture/Modules.md`
- `Documentation/Proposals/PackageDocsLayout.md`
- `Documentation/Decisions/SaveSemantics.md`
- `Documentation/Migrations/SwiftSixMigration.md`
- `Documentation/Reference/MigrationNotes.md`

Keep root and conventional special files in their established forms:

- `AGENTS.md`
- `README.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`
- `GOVERNANCE.md`
- `.github/CODEOWNERS`
- `.github/`

## Normalization Guidance

- Do not rename canonical documentation role paths to lowercase variants such as
  `documentation/architecture/`.
- Do not mix variants such as `Documentation/architecture/` or
  `documentation/Architecture/`.
- Do not create lowercase or kebab-case Markdown document names under canonical
  `Documentation/` role directories when a new file is being scaffolded or normalized.
- When importing an existing repository that already uses lowercase
  documentation paths, treat casing as normalization scope and call out the
  migration risk on
  case-insensitive filesystems.
- Do not apply PascalCase broadly to every file. Preserve conventional names
  such as `README.md`, `.github/ISSUE_TEMPLATE/bug.md`,
  `.github/pull_request_template.md`, and target-level DocC pages that mirror
  Swift module or symbol names.
