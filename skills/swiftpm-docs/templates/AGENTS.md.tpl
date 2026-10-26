# <repo-name> Agent Guide

Read `README.md` first for repository purpose and entry points.

<!-- module:canonical-artifacts -->
## Canonical Artifacts

- Treat conversation, review feedback, plans, and intermediate attempts as
  editing input. Recompute the complete accepted result before finalizing.
- Active artifacts depend only on that result and their repository role, not
  on the editing path. Apply this to code, symbols, files, wrappers, branches,
  configuration, schemas, defaults, generated sources, scripts, templates,
  automation, comments, DocC, diagrams, tests, fixtures, snapshots, examples,
  and normative docs.
- If an intermediate result is `A + B` and the accepted result is `A`, express
  `A` directly. Remove `B` and its residual surface rather than retaining names
  such as `AOnly` or `AWithoutB`, or prose such as "B was removed."
- Normalize by semantic identity and artifact role, not by token. A rejected
  current capability does not invalidate a distinct historical fact,
  migration, ownership record, or safety boundary that uses the same term.
- Keep a negative constraint only when excluding `B` is independently required
  by a current compatibility, safety, or ownership invariant.
- A disabled B flag, skipped B test, dead B branch, retained B fixture, or
  "do not add B" rule is residue when it exists only because B was attempted;
  disabled state alone is not an invariant.
- Keep change history only in commits, pull requests, changelogs, release
  records, migrations, archives, or accepted decision records with durable
  value. Do not create a history artifact merely to preserve a correction.
- Preserve role-owned facts unless separate evidence changes them; do not
  rewrite history or ownership merely to make a rejected term disappear.
- Leave an already-correct history, migration, provenance, ownership, or safety
  artifact unchanged when the task does not change its facts. Do not polish or
  restate it merely because it is relevant to the current edit.
- Comments explain non-obvious current semantics and invariants, not the
  sequence of edits.
- Before handoff, verify that a new agent with no editing conversation can
  derive the complete current behavior, boundaries, and operating guidance
  without mentally subtracting a rejected concept.

<!-- /module:canonical-artifacts -->
## Task Route

- Before changing versions, dependencies, packaging or release workflows, read
  `VERSIONING.md`, or the organization VERSIONING the project adopts, and
  `Documentation/Reference/Release.md`.
- Read `Documentation/README.md` before placing documentation and
  `Documentation/Architecture/README.md` before changing package structure.

## Code Review Rules

### Public claims

- Flag README, DocC or release-note statements that the code, tests and CI do
  not support: missing capabilities, existing behavior described as new, or
  platforms CI does not build. Flag public prose that compares the package
  with other projects or describes internal process. Safe path: state only
  this package's verified behavior.

### Public documentation

- Flag a new public symbol without a documentation comment. Safe path:
  document what the symbol does and how it fails.

### Behavior and compatibility

- Flag a change to public API or observable behavior, including serialized
  output, products, traits and raised minimum platform, Swift tools or
  toolchain versions, that lacks a test failing before the change or a
  `CHANGELOG.md` entry under `## Unreleased` as VERSIONING requires. Safe
  path: add the test, record the change, mark breaking changes **Breaking**
  with the new minimums or upgrade path, and leave the version bump to release
  preparation.
