# Route vs Index

Use this rule when classifying `AGENTS.md` and `README`-class files.
`AGENTS.md` is a high-signal agent guide: first-principles edit
guardrails, task route, authority boundaries, and concrete boundary checks.
README-class files are indexes and manuals.

## Decision Test

- If a sentence tells an agent what to read, when to act, or how to handle a
  task type, it is Route.
- If a sentence states a high-signal working rule that prevents unsafe or
  mis-scoped agent edits, it may be an Operational Guardrail in `AGENTS.md`.
- If a sentence explains what exists, where it lives, or who owns it, it is
  Index.

Subject heuristic:

- task, intent, or change-type subject => Route
- directory, file, doc type, or placement subject => Index

## Route And Operational Guardrails

Belongs in:

- `AGENTS.md`

Sentence cues:

- starts with "when", "if", "before", "for this task", or "stop and clarify"
- tells the reader to enter, read, check, avoid, or escalate
- depends on request type or change intent
- states a concise cross-cutting working rule for agent edits

Examples:

- "When normalizing documentation placement, read `rules/` before editing
  templates."
- "If the request becomes release automation, stop and clarify."
- "Before exporting a template, audit the repo structure."
- "Before editing reusable artifacts, name the invariant and owning layer."
- "Before editing reusable artifacts, classify concrete values by ownership
  and variability."

## Index

Belongs in:

- root `README.md`
- directory `README.md`

Sentence cues:

- names a directory or file role
- describes scope, placement, ownership, or contents
- answers "what is here?" or "where should this live?"

Examples:

- "`skills/` holds authoritative skill source material."
- "`examples/` holds small target-tree and normalization examples."
- "`Documentation/Architecture/*` is current truth."

## Does Not Belong

Route and operational guardrails do not belong in:

- `README` files that explain tree layout or file ownership

Index does not belong in:

- `AGENTS.md` files that should stay task-driven and operational

Long explanations, many examples, and repo-specific current architecture truth
do not belong in `AGENTS.md`; place them under `Documentation/Architecture/*`
or `Documentation/Reference/*` as appropriate and keep `AGENTS.md` as the
agent guide.

## Common Failure Modes

- `AGENTS.md` becomes a directory catalog.
- `AGENTS.md` becomes a long architecture or reference manual.
- `README.md` starts telling agents which task flow to run.
- One file mixes placement explanations with escalation instructions.
- Task-driven warnings are buried inside a directory index.
- README or reference text explains why an agent changed wording, avoided a
  past mistake, or removed old guidance instead of stating current product
  behavior.
- Defensive migration notes are placed in user-facing documentation instead of
  agent guidance or history.

## Normalization Guidance

- Move task-driven sentences into `AGENTS.md`.
- Keep high-signal operational guardrails in `AGENTS.md` when they directly affect
  agent edit behavior.
- Move agent editing guardrails and process explanations out of README-class
  files; keep them in `AGENTS.md`, history records, temporary execution state,
  or omit them when they do not help future work.
- Move tree, placement, and ownership sentences into the nearest `README`.
- Move detailed rationale, long examples, and current repo-specific structure
  truth into `Documentation/Architecture/*` or `Documentation/Reference/*`.
- If a mixed file is mostly route, keep the route file and extract the index
  sections into a `README`.
- If a mixed file is mostly index, keep the index file and move task-handling
  instructions into `AGENTS.md`.
- Prefer cross-links over duplication when both route and index need to point
  to the same area.
