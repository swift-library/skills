# Rules

This directory holds the stable invariants enforced by `swiftpm-docs`. Roles
map to repository paths in the `SKILL.md` Role Model.

Role rules, bundled from the `repository-docs` skill (edit them there and
re-derive):

- `route-vs-index.md`: document roles and authority, including agent route,
  edit guardrails, review rules, and tool entry files.
- `readme-layering.md`: root README, directory and documentation indexes, and
  where detailed content belongs.
- `code-review-rules.md`: the `## Code Review Rules` section and the files
  that carry it to a specific reviewer.

Swift package rules:

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
- `path-casing.md`: canonical `Documentation/` role directory casing and
  PascalCase document names.
- `governance-vs-documentation-placement.md`: classify GitHub-facing governance
  files, root governance documentation, and internal documentation architecture.

Keep rules short, operational, and boundary-first.
