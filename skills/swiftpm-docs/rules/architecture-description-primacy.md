# Architecture Description Primacy

Use this rule when current structure is being implied through supporting
documents instead of stated directly.

## Principle

- `Docs/Architecture/*` is the primary home of the current architecture
  description.
- `Docs/Proposals/*`, `Docs/Decisions/*`, `Docs/Migrations/*`,
  `Docs/Archive/*`, and `Docs/Reference/*` are supporting artifacts.
- Supporting artifacts may prepare, justify, record, retire, or reference
  change. They do not redefine current architectural truth on their own.

## Basis

This rule is aligned with
[ISO/IEC/IEEE 42010: Architecture Descriptions](https://www.iso-architecture.org/ieee-1471/ads/),
which treats an architecture description as a distinct artifact used to
express architecture. Keep current truth explicit in `Docs/Architecture/*`,
not only implied through supporting materials.

## Required Outcome

- When repository structure or document-role boundaries change,
  `Docs/Architecture/*` must be updated explicitly.
- Do not leave current architecture true only by inference from proposal,
  decision, migration, archive, or reference material.

## Failure Modes

- A decision record becomes the only place that states the current structure.
- A migration note becomes the effective source of truth after rollout.
- A proposal is treated as current because architecture files were never
  updated.
- Reference material is read as current guidance even though architecture files
  say less.

## Normalization Guidance

- If a supporting document states what is true now and architecture files do
  not, move or restate that current description in `Docs/Architecture/*`.
- Keep supporting documents as context, rationale, rollout record, retired
  record, or reference after truth has been restated in architecture files.
