# Architecture Doc Format

Use this rule when writing or normalizing documents under
`Docs/Architecture/*`.

## Purpose

- Keep current architecture descriptions explicit, structured, and easy to
  maintain.
- Cover the main current-state concerns without importing the full arc42
  system.

## Recommended Sections

- `# <title>`
- `Scope / Purpose`
- `Context / Boundaries`
- `Constraints`
- `Current Structure`
- `Key Principles`
- `Cross-cutting Concerns`
- `Risks / Known Gaps`
- `Related Decisions`

## Format Expectations

- Treat this as a recommended coverage shape, not a rigid full-framework
  import.
- State what is true now.
- Keep one document focused on one architecture topic or boundary area.
- Link to supporting proposals, decisions, migrations, archives, and reference
  material instead of absorbing those roles here.

## Does Not Absorb Other Roles

- Do not turn architecture docs into proposal comparison logs.
- Do not turn architecture docs into migration diaries or archive dumps.
- Do not use reference notes as a substitute for current structure.

## Basis

This rule is aligned with
[arc42 Documentation](https://arc42.org/documentation/), using a lighter
coverage shape for current architecture documents.
