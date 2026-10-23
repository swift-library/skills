# Proposal vs Truth vs History

Use this rule when classifying documentation under `Documentation/`.

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

- "Option A keeps module ownership in `Documentation/Architecture/Modules.md`; Option B
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

- "Module ownership is indexed from `Documentation/Architecture/Modules.md`."

## History

Purpose:

- preserve the why, how, and retired state of changes over time

Belongs:

- `Documentation/Decisions/*`: decision records and rationale
- `Documentation/Migrations/*`: transition plans, cutovers, and migration notes
- `Documentation/Archive/*`: retired or superseded material kept for record and no
  longer authoritative

Does not belong:

- the current canonical architecture description
- active design exploration
- active guidance that should still be treated as current truth

Examples:

- "ADR-004 adopted Architecture and Proposal separation."
- "Migration 2026-04 moves package documentation out of the root."

## Common Failure Modes

- Proposal text left inside `Documentation/Architecture/*` after a decision is made.
- Current truth written into a decision record and never restated in
  `Documentation/Architecture/*`.
- Migration checklists left as the only source of current structure.
- Archived documents linked as if they were current guidance.
- Historical behavior, transition rationale, or temporary comparison notes are
  written as current product truth.

## Lifecycle

1. Start a design in `Documentation/Proposals/*` when it needs agreement on
   alternatives, boundaries, or compatibility before implementation. Name its
   author, affected owners, and the maintainer or decision authority designated
   by the repository's governance; that authority accepts the design.
2. At acceptance, record the accepted choice, rationale, tradeoffs, accepting
   authority, and date in `Documentation/Decisions/*`. Acceptance settles the
   design; it does not establish that the behavior is implemented.
3. Until implementation merges, Architecture and Reference describe the
   implemented model and interfaces. If readers need the pending direction,
   add a clearly labelled accepted-but-unimplemented note linking the Decision
   and implementation issue; do not advertise the planned behavior as available.
4. With the implementation merge, update Architecture's current model and
   Reference's current interfaces and operating guidance, link the Decision for
   rationale, and resolve the pending note. For staged implementation, describe
   each implemented portion accurately and keep the remainder explicitly pending.
5. Once a proposal's disposition is settled and its accepted content has owning
   documents, delete it if it has no durable value beyond those documents.
   Archive it only for distinct rationale, migration, or audit value, marked
   non-current with links to its replacements. A rejected or withdrawn proposal
   follows the same value test and does not require a Decision. Update inbound
   links and remove the proposal from the active Proposals index in the same
   change; durable links belong in the Decisions or Archive index.

Use `proposal-doc-format.md` for proposal metadata and index upkeep,
`decision-record-format.md` for decision statuses and supersession, and
`architecture-description-primacy.md` for current-model ownership.

## Normalization Guidance

- If the document contains unresolved options, move or split that material into
  `Documentation/Proposals/*`.
- If the document states what is true now, move or rewrite it into
  `Documentation/Architecture/*`.
- If the document mainly explains why an accepted change happened, move it into
  `Documentation/Decisions/*`.
- If the document mainly explains a durable transition, rollout, or cutover,
  move it into `Documentation/Migrations/*`.
- Keep temporary notes, local logs and outputs, local paths, run-specific artifacts, and
  current-session explanations in `.agent/*` or omit them.
- If the document is retained only for record, move it into `Documentation/Archive/*`
  and mark it as retired and non-current.
- When one file mixes roles, split by section rather than forcing one file to
  carry Proposal, Truth, and History together.
