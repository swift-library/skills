# Eval Fixtures

These fixtures protect `swiftpm-docs` role boundaries and current-artifact
normalization. They are durable behavior inputs, not execution logs.

## canonical-artifact-path-independence

Target behavior: normalize the documentation-owned surface to the accepted
package contract while detecting, but not silently taking ownership of,
cross-surface implementation drift.

Input prompt: "A draft Swift package gained JSON and YAML export while we were
exploring the feature. The YAML export branch was never accepted; the package
contract is JSON export. The released 0.9 storage migration and the external
reader ownership record remain valid. Make the repository documentation and
agent guide current."

Context and files:

- `README.md`, DocC, examples, architecture and reference docs mention JSON and
  YAML, `JSON-only`, or `YAML was removed after review`.
- `AGENTS.md` has an `AWithoutB`-shaped route and no self-contained canonical
  artifact contract.
- Implementation residue includes `YAMLExporter`, a `.yaml` branch,
  `yaml.enabled = false`, generated CLI/schema inputs, a skipped YAML test, and
  YAML fixtures or snapshots.
- A historical ADR records why an earlier released schema required YAML
  migration, and a current security boundary independently rejects a YAML
  deserializer owned by another subsystem.

Expected output:

- Re-derives the accepted current contract as JSON export and expresses it
  directly in documentation and the generated target `AGENTS.md`.
- Removes correction-shaped YAML wording, names, examples, diagrams, DocC/API
  prose, and other documentation-owned residue with no current contract value.
- Reports implementation, test, configuration, schema, and generated-source
  residue as a blocking handoff to the implementation owner; it does not claim
  that the repository is fully current while that drift remains.
- Preserves the historical ADR and the independently current security or
  ownership boundary in their explicit roles.
- Produces the same active documentation meaning that a direct JSON design path
  would have produced, without inventing a history artifact for the correction.

Forbidden behavior:

- Mutates Swift implementation, tests, configuration, schemas, or generated
  sources under `swiftpm-docs` ownership alone.
- Renames the capability to `JSONOnlyExporter`, `ExporterWithoutYAML`, or adds a
  permanent "YAML is unsupported" section solely because the draft changed.
- Leaves current YAML residue and compensates with `removed`, `deprecated`,
  `legacy`, or `no longer supported` narration.
- Deletes a durable ADR, migration record, or still-current security/ownership
  constraint.
- Creates a new ADR, migration note, archive, or provenance record merely to
  preserve the correction sequence.

Acceptance checks:

- A reader with no conversation can understand the complete current package
  contract without mentally subtracting YAML.
- Active documentation contains no rejected YAML surface unless an independent
  current compatibility, safety, or ownership invariant requires it.
- Cross-surface residue outside documentation ownership is enumerated and
  routed to its owner rather than silently edited or ignored.
- The handoff includes every discovered implementation, configuration, test,
  fixture, schema, and generated-source blocker, not only representative
  examples.
- Historical artifact content remains unchanged and role-labelled.
- The unchanged decision and ownership records have no content diff; an agent
  may cite them in the handoff but may not restate them in place.
- `python3 scripts/validate_template_exports.py` passes for both `minimal` and
  `standard` profile exports.

Baseline expectation:

- The old skill may patch prose incrementally, retain `JSON-only` or removal
  narration, miss generated target-guide semantics, or overreach into Swift
  implementation and tests.

Evidence sources:

- Final documentation and generated target `AGENTS.md` diff.
- Cross-surface drift or handoff report.
- Historical artifact hashes before and after the run.
- Template export smoke-test output.

Owner notes:

- `swiftpm-docs` owns documentation structure, content, and its target-guide
  template. Swift implementation, tests, configuration, schemas, and generated
  source require their applicable implementation owner.

## package-review-rules

Target behavior: give a Swift package's agent guide review rules a reviewer
can apply, written against the package's own documentation paths.

Input prompt: "Our pull requests are reviewed automatically. Normalize the
agent guide for this package."

Context and files:

- `AGENTS.md` has the canonical contract but no `## Code Review Rules`.
- `Documentation/Architecture/VersioningAndRelease.md` defines the version
  bump and the change record; DocC catalogs live under
  `Sources/<Target>/<Target>.docc/`.
- `Scripts/check` already runs formatting and a forbidden-path scan.

Expected output:

- `AGENTS.md` gains `## Code Review Rules` with `###` groups for compatibility
  and versioning, claims, public documentation, and tests, each naming the
  behavior, the reason, and the safe path.
- The versioning rule routes to `VersioningAndRelease.md` instead of copying
  its bump rules.
- Formatting and forbidden paths are left to `Scripts/check`.
- No `CLAUDE.md` or `REVIEW.md` is created.

Forbidden behavior:

- Review rules that restate `Scripts/check`, copy the versioning policy, or
  name functions likely to move.

Acceptance checks:

- `scripts/validate_canonical_target.py` passes, including the review-rule
  section and size budget.

Evidence sources:

- Target `AGENTS.md` diff and validator output.

Owner notes:

- The review-rule shape comes from the bundled `rules/code-review-rules.md`.

## Version and Release Scaffold Cases

Run both minimal and standard profile export checks. Review filled output against
these facts; a template containing placeholders is not evidence of implemented
release automation.

| Input | Expected output |
| --- | --- |
| SwiftPM library released only by tags | Preserve the actual single version authority; do not add an App build number or another declaration. |
| CLI with a plugin manifest and derived runtime constant | Identify CLI and plugin authorities separately; route generation and checks to existing tools. |
| Existing release policy at another repository path | Complete it, adjust the profile target and all routes, and retain one normative entry. |
| New project with no release scripts | Explicitly state that automation is not established; no invented commands or claims of candidate validation. |
| New toolchain or changed check definitions | Previous evidence is invalid for the affected stage and its dependents; retain failure records. |
| Unchanged source and exact accepted package | Reuse only trusted matching evidence; preserve the accepted bytes during publication. |
