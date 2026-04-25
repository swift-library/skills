# Rules

This directory holds the stable invariants enforced by `swiftpm-docs`.

Core role boundaries:

- `AGENTS.md` is Route only.
- `README`-class files are Index only.
- root `README.md` is the public landing page and concise entry index.
- `Docs/README.md` is the documentation reading index.
- `Docs/Architecture/README.md` is the architecture reading index.
- `Docs/Proposals/*` is Proposal space only.
- `Docs/Architecture/*` is current Truth.
- `Docs/Decisions/*`, `Docs/Migrations/*`, and `Docs/Archive/*` are History.
- `.github/*` is Governance.
- `Docs/Reference/*` is Reference.
- `templates/` in this skill holds upstream template source material.
- exported outputs are downstream artifacts, not authority.

Operational rules:

- `architecture-description-primacy.md`: keep `Docs/Architecture/*` as the
  primary current architecture description.
- `architecture-doc-format.md`: use a lightweight arc42-style structure for
  current architecture documents.
- `decision-record-format.md`: use a lightweight ADR/MADR-style structure for
  adopted decision records.
- `proposal-doc-format.md`: use a lightweight Swift Evolution-inspired
  structure for design-in-progress proposals.
- `proposal-vs-truth-vs-history.md`: classify design-in-progress, current
  canonical state, and historical record.
- `readme-layering.md`: distinguish root README, docs README, architecture
  README, and architecture-rule ownership.
- `route-vs-index.md`: classify route instructions versus index and placement
  guidance.
- `governance-vs-docs-placement.md`: classify GitHub-facing governance files,
  root governance docs, and internal docs architecture.

Keep rules short, operational, and boundary-first.
