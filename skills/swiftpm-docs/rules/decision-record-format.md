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

## Basis

This rule is aligned with
[MADR](https://adr.github.io/madr/), using a lighter ADR/MADR-style structure
for adopted decisions in repository-native documentation.
