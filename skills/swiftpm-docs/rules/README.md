# Rules

This directory holds the stable invariants enforced by `swiftpm-docs`.

Core role boundaries:

- `AGENTS.md` is the high-signal agent guide: first-principles edit
  guardrails, task route, authority boundaries, and concrete boundary checks.
- `README`-class files are indexes/manuals, not agent route contracts.
- root `README.md` is the GitHub-facing landing manual and entry index.
- `Documentation/README.md` is the documentation reading index.
- `Documentation/Architecture/README.md` is the architecture reading index.
- `Documentation/Proposals/*` is Proposal space only.
- `Documentation/Architecture/*` is current Truth.
- `Documentation/Decisions/*`, `Documentation/Migrations/*`, and
  `Documentation/Archive/*` are History.
- `.github/*` is Governance.
- `Documentation/Reference/*` is Reference.
- `Sources/<Target>/<Target>.docc/*` is target-level DocC API documentation
  source.
- `.doccarchive` directories are generated DocC output unless a repository
  explicitly governs them as published artifacts.
- `templates/` in this skill holds the template sources.
- exported outputs are generated artifacts, not authority.
- canonical documentation role directory casing is
  `Documentation/Architecture`, `Documentation/Proposals`,
  `Documentation/Decisions`, `Documentation/Migrations`,
  `Documentation/Archive`, and `Documentation/Reference`.
- non-index Markdown documents under canonical `Documentation/` role directories
  use PascalCase file stems, such as `Package.md`, `Modules.md`,
  `PackageDocsLayout.md`, or `MigrationNotes.md`.

Operational rules:

- `architecture-description-primacy.md`: keep `Documentation/Architecture/*` as the
  primary current architecture description.
- `canonical-artifacts.md`: collapse iterative feedback into standalone current
  documentation without correction narratives or rejected-concept residue.
- `architecture-doc-format.md`: use a lightweight arc42-style structure for
  current architecture documents.
- `decision-record-format.md`: use a lightweight ADR/MADR-style structure for
  adopted decision records.
- `proposal-doc-format.md`: use a lightweight Swift Evolution-inspired
  structure for design-in-progress proposals.
- `proposal-vs-truth-vs-history.md`: classify design-in-progress, current
  canonical state, and historical record.
- `docc-placement.md`: distinguish target-level DocC source catalogs from
  repository-level documentation and generated `.doccarchive` output.
- `docc-landing-identity.md`: give each public module's DocC landing page the
  package icon and page color.
- `path-casing.md`: preserve canonical documentation path casing during
  scaffold, normalize, audit, and export work.
- `readme-layering.md`: distinguish root README, documentation README, architecture
  README, and architecture-rule ownership.
- `route-vs-index.md`: classify agent guide content versus index and
  placement guidance.
- `governance-vs-documentation-placement.md`: classify GitHub-facing governance
  files, root governance documentation, and internal documentation architecture.

Keep rules short, operational, and boundary-first.
