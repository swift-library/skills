# Rules

This directory holds stable source and audit rules for `swiftpm-index`.

Read only the rule needed for the active task:

- `source-policy.md`: source authority order and exclusions.
- `source-acquisition.md`: CLI responsibilities, enrichment, runtime paths,
  and mutation boundaries.
- `catalog-normalization.md`: normalized catalog shape and review fields.
- `candidate-matching.md`: use fetched package summaries/descriptions and
  target code patterns to discover candidate matches.
- `audit-workflow.md`: target package audit sequence.
- `recommendation-taxonomy.md`: Adopt / Wrap / Reference / Keep custom.

Keep rules concise, source-first, and reviewable.
