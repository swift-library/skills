# Proposal vs Truth vs History

Use this rule when classifying documentation under `Docs/`.

## Decision Test

- If the content is still being argued, shaped, or compared, it is Proposal.
- If the content states the current canonical model, it is Truth.
- If the content explains what was decided, what changed, or what is retired,
  it is History.

## Proposal

Purpose:

- hold design-in-progress
- capture options, tradeoffs, and open questions

Belongs:

- proposed structures
- candidate naming and placement options
- unresolved design comparisons

Does not belong:

- current canonical repository structure
- completed decisions
- retired material kept only for record

Example:

- "Option A keeps module ownership in `Docs/Architecture/Modules.md`; Option B
  splits ownership by package target."

## Truth

Purpose:

- state the current canonical repository model
- tell readers what is true now

Belongs:

- current architecture descriptions
- current document-role boundaries
- current package documentation layout

Does not belong:

- unresolved alternatives
- decision logs and migration diaries
- archived or superseded guidance

Example:

- "Module ownership is indexed from `Docs/Architecture/Modules.md`."

## History

Purpose:

- preserve the why, how, and retired state of changes over time

Belongs:

- `Docs/Decisions/*`: decision records and rationale
- `Docs/Migrations/*`: transition plans, cutovers, and migration notes
- `Docs/Archive/*`: retired or superseded material kept for record and no
  longer authoritative

Does not belong:

- the current canonical architecture description
- active design exploration
- active guidance that should still be treated as current truth

Examples:

- "ADR-004 adopted Architecture and Proposal separation."
- "Migration 2026-04 moves package docs out of the root."

## Common Failure Modes

- Proposal text left inside `Docs/Architecture/*` after a decision is made.
- Current truth written into a decision record and never restated in
  `Docs/Architecture/*`.
- Migration checklists left as the only source of current structure.
- Archived documents linked as if they were current guidance.

## Normalization Guidance

- If the document contains unresolved options, move or split that material into
  `Docs/Proposals/*`.
- If the document states what is true now, move or rewrite it into
  `Docs/Architecture/*`.
- If the document mainly explains why a change happened or how a change was
  rolled out, move it into `Docs/Decisions/*` or `Docs/Migrations/*`.
- If the document is retained only for record, move it into `Docs/Archive/*`
  and mark it as retired and non-current.
- When one file mixes roles, split by section rather than forcing one file to
  carry Proposal, Truth, and History together.
