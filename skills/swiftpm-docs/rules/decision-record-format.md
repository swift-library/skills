# Decision Record Format

Use this rule when writing or normalizing documents under `Documentation/Decisions/*`.

## Purpose

- Keep adopted decisions concise, structured, and easy to review.
- Preserve rationale without turning decision records into the primary current
  architecture description.

## Required Sections

- `# <title>`
- `Status`
- `Context`
- `Decision`
- `Consequences`
- `Alternatives Considered`
- `Related Documentation`

## Format Expectations

- Record adopted decisions and their rationale.
- Keep the document focused on one decision.
- Use short sections and direct statements.
- Keep current architecture truth in `Documentation/Architecture/*`, even when a
  decision record explains why that truth changed.

## Does Not Replace Architecture Truth

- Do not treat a decision record as the only place that states the current
  structure.
- After a decision changes the repository model, update
  `Documentation/Architecture/*` explicitly.

## Status and Supersession

- `Proposed` belongs only in `Documentation/Proposals/*`. A record enters
  `Documentation/Decisions/*` as `Accepted` when the repository's designated
  authority accepts it; record that authority and date in Related Documentation.
- `Accepted` records the design decision, not implementation completion. Link
  pending implementation work and the current Architecture/Reference documents.
  Update current-model documents with the implementation merge as described in
  `proposal-vs-truth-vs-history.md`.
- Use `Superseded` when a replacement decision is accepted. In the old record's
  Status section add `Superseded by: [title](replacement.md)`; link back from the
  replacement with `Supersedes: [title](original.md)`. Preserve the old rationale.
- Keep each successor link pointing to its immediate replacement so chains
  remain traversable, acyclic, and end at an `Accepted` decision. Update the
  Decisions index with statuses and links in the acceptance change. Supersession
  alone does not change the implemented model; current docs remain accurate
  until the replacement implementation merges.

## Basis

This rule is aligned with
[MADR](https://adr.github.io/madr/), using a lighter ADR/MADR-style structure
for adopted decisions in repository-native documentation.
