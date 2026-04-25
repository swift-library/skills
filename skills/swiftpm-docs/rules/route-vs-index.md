# Route vs Index

Use this rule when classifying `AGENTS.md` and `README`-class files.

## Decision Test

- If a sentence tells an agent what to read, when to act, or how to handle a
  task type, it is Route.
- If a sentence explains what exists, where it lives, or who owns it, it is
  Index.

Subject heuristic:

- task, intent, or change-type subject => Route
- directory, file, doc type, or placement subject => Index

## Route

Belongs in:

- `AGENTS.md`

Sentence cues:

- starts with "when", "if", "before", "for this task", or "stop and clarify"
- tells the reader to enter, read, check, avoid, or escalate
- depends on request type or change intent

Examples:

- "When normalizing docs placement, read `rules/` before editing templates."
- "If the request becomes release automation, stop and clarify."
- "Before exporting a template, audit the repo structure."

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
- "`Docs/Architecture/*` is current truth."

## Does Not Belong

Route does not belong in:

- `README` files that explain tree layout or file ownership

Index does not belong in:

- `AGENTS.md` files that should stay task-driven and operational

## Common Failure Modes

- `AGENTS.md` becomes a directory catalog.
- `README.md` starts telling agents which task flow to run.
- One file mixes placement explanations with escalation instructions.
- Task-driven warnings are buried inside a directory index.

## Normalization Guidance

- Move task-driven sentences into `AGENTS.md`.
- Move tree, placement, and ownership sentences into the nearest `README`.
- If a mixed file is mostly route, keep the route file and extract the index
  sections into a `README`.
- If a mixed file is mostly index, keep the index file and move task-handling
  instructions into `AGENTS.md`.
- Prefer cross-links over duplication when both route and index need to point
  to the same area.
