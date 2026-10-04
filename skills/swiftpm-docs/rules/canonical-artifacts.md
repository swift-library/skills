# Canonical Artifacts

Use this rule when review feedback or iterative implementation has left active
documentation describing how the package changed instead of what the package
is now.

## Principle

Treat the editing conversation as input. Normative documentation, DocC source,
examples, and target-facing agent guidance must express the complete currently
accepted package directly and remain understandable without that conversation.
Different editing paths that reach the same accepted package and artifact roles
must produce semantically equivalent active documentation.

If an intermediate design contains `A + B` and the accepted design is `A`,
rewrite current documentation to describe `A`. Do not describe it as `A
without B`, add a permanent prohibition against `B`, or retain removal
commentary unless excluding `B` is itself a current compatibility, safety, or
ownership invariant.

Normalize by semantic identity and artifact role, not by token. Rejecting a
current capability named `B` does not invalidate a distinct historical fact,
migration, ownership record, or safety boundary that happens to mention `B`.
Preserve those role-owned facts unless separate evidence or an explicit request
changes them. The correction to current behavior alone is not such evidence.

## Normalization

- Remove stale names, configuration, examples, DocC descriptions, diagrams,
  fixtures, and template content for rejected concepts.
- Keep current architecture and reference docs affirmative and direct.
- Avoid correction-shaped qualifiers such as `only`, `without`, `removed`,
  `rejected`, `formerly`, `legacy`, `deprecated`, or `no longer supported`
  when their sole purpose is to contrast the accepted result with the editing
  path.
- Keep unresolved alternatives in `Documentation/Proposals/*` only while they
  remain genuinely unresolved.
- Keep change history in commits, changelogs, release records,
  `Documentation/Decisions/*`, `Documentation/Migrations/*`, or
  `Documentation/Archive/*` according to the artifact's role.
- Do not create a history artifact merely to preserve every correction. Retain
  history only when its rationale, migration, or audit value remains useful.
- Do not edit or delete a history, ownership, migration, or safety artifact
  merely to make a repository-wide search for a rejected term come back empty.
- When such an artifact is already correct and the task does not change its
  facts, leave its contents unchanged. Do not polish, clarify, or restate it
  merely because it is relevant to the current edit.
- Treat `b = false`, a skipped B test, a dead B branch, a retained B fixture,
  or a new "do not add B" instruction as residue when it exists only because B
  was attempted. Disabled state alone is not a compatibility, safety, or
  ownership invariant.
- Do not hand-edit generated schemas, help, DocC output, or generated metadata.
  Report the source-of-truth drift and regeneration owner instead.

## Validation

Read the normalized documentation without the editing conversation. It passes
only when the current package behavior, boundaries, and operating guidance are
complete and no rejected intermediate concept must be mentally subtracted.
Compare the result with the direct-design counterfactual: if the accepted
package had always been `A`, active documentation should have the same meaning.
