# Eval Fixtures

These fixtures protect `swiftpm-docs` role boundaries and current-artifact
normalization. They are durable behavior inputs, not execution logs.

## Open Work and Community Templates

| Input | Expected output |
| --- | --- |
| An architecture document lists defects, requested changes, and pending decisions | Open work moves out of the document: into the owner's task plan when that owner does it, or into the owning repository's GitHub issues when it is handed off; documents link to issues while retaining current architecture facts. |
| The GitHub settings owner confirms shared community defaults apply | Omit inherited community-health files from both profiles. Retain repository-specific documentation, license, governance, and ownership files. That owner verifies the defaults take effect. |
| The settings owner selects local community files | Emit the selected profile's community files, including `.github/ISSUE_TEMPLATE/config.yml` for the standard profile. Both bug and feature templates ask for current behavior or state, expected outcome, evidence with commands, versions and links, the decision needed, and completion checks. |
| Contributor and security guidance are inherited; issue and pull request templates are local | Omit the inherited files and emit the selected local templates. Inheritance is an input from the settings owner, not a decision inferred from missing local files. |

Acceptance checks: run `scripts/check` from the collection root for local,
inherited, and mixed profile exports; inspect the issue prompts and documentation
diff against these cases. This skill owns community-file text and templates;
the GitHub settings owner owns selection and effective-behavior verification.

## canonical-artifact-path-independence

Target behavior: normalize the documentation-owned surface to the accepted
package contract while detecting, but not silently taking ownership of,
cross-surface implementation drift.

Input prompt: "A draft Swift package gained JSON and YAML export while we were
exploring the feature. The YAML export branch was never accepted; the package
contract is JSON export. Adopt the canonical-artifacts contract in our agent
guide. The released 0.9 storage migration and the external
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
  `standard` profile exports, with and without the canonical-artifacts module.

Failure signatures:

- Incremental prose patches retain `JSON-only` or removal
  narration, miss generated target-guide semantics, or overreach into Swift
  implementation and tests.

Review inputs:

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
- `VERSIONING.md` defines the version bump and the change record;
  `Documentation/Reference/Release.md` records the compatibility surface;
  DocC catalogs live under `Sources/<Target>/<Target>.docc/`.
- The repository's validation CI already runs formatting and a forbidden-path scan.

Expected output:

- `AGENTS.md` gains `## Code Review Rules` with `###` groups for compatibility
  and versioning, claims, public documentation, and tests, each naming the
  behavior, the reason, and the safe path.
- The versioning rule routes to VERSIONING and the release reference instead of copying its bump rules.
- Formatting and forbidden paths are left to the repository's validation CI.
- No `CLAUDE.md` or `REVIEW.md` is created.

Forbidden behavior:

- Review rules that restate validation CI, copy the versioning policy, or
  name functions likely to move.

Acceptance checks:

- `scripts/validate_canonical_target.py` passes, including the review-rule
  section and size budget.

Review inputs:

- Target `AGENTS.md` diff and validator output.

Owner notes:

- The review-rule shape comes from the bundled `rules/code-review-rules.md`.

## Optional Canonical Artifacts

| Input | Expected output |
| --- | --- |
| Minimal or standard export without a module request | AGENTS.md includes ordinary routes and Code Review Rules; it has no Canonical Artifacts contract or module delimiters. |
| Target adopts the contract or the user requests it | `--module canonical-artifacts` emits the complete contract; both validators check it. |
| Normalize documentation after feedback without target adoption | Normalize current documentation; preserve the target's module selection rather than adding a repository-wide contract. |
| Guide has no module | Target validator reports not applicable; an explicit module requirement fails. |
| Guide carries an incomplete Canonical Artifacts section | Target validator reports the missing contract clauses. |

Acceptance checks: run `Tests/test_profile_export.py` and
`Tests/test_template_exports.py` for both export modes and target validation.

## Document Lifecycle

| Input | Expected output |
| --- | --- |
| Design alternatives need agreement | Proposed document names the author, affected owners, and governance-designated acceptance authority; Proposals index links it with owner and review status. |
| Authority accepts a design before implementation | Accepted Decision records choice, rationale, authority, and date. Architecture and Reference keep the implemented model, optionally linking a clearly labelled accepted-but-unimplemented direction and implementation issue. |
| Implementation merges in stages | Current Architecture/Reference describe each implemented portion; pending notes track the unimplemented remainder and disappear when resolved. |
| Settled proposal duplicates its Decision and current-model docs | Delete the proposal, remove its active index entry, and repair inbound links. Archive only distinct durable rationale, migration, or audit material as non-current. |
| Rejected or withdrawn proposal has no durable record value | Delete it and its active index entry; do not create a Decision to preserve the rejection. |
| Accepted decision replaces another accepted decision | Mark the earlier record Superseded with a Superseded by link, link back from its successor, preserve rationale and intermediate chain links, and update the Decisions index. Keep implemented-model docs accurate until the replacement merges. |

Acceptance checks: review the resulting document roles, status values, links,
and index entries against `rules/proposal-vs-truth-vs-history.md`,
`rules/proposal-doc-format.md`, `rules/decision-record-format.md`, and
`rules/architecture-description-primacy.md`.

## Package Command Exports

| Input | Expected output |
| --- | --- |
| Package at the repository root | Local commands are `swift build` and `swift test`; requirements come from its manifest. |
| `.github/swift-package.json` declares a nested `package_directory` | Read that directory's manifest and add a shell-quoted `--package-path` argument to both local commands. |
| Explicit command or requirement overrides | `--set` values take precedence over package facts. |
| Invalid configuration or missing selected manifest | Report the input path and fail before writing any export. |

Acceptance checks: run `Tests/test_profile_export.py` and verify both profiles
retain their template bytes apart from the selected placeholder values.

## Version and Release Scaffold Cases

Run both minimal and standard profile export checks. Review filled output against
these facts; a template containing placeholders is not evidence of implemented
release automation.

| Input | Expected output |
| --- | --- |
| SwiftPM library released only by tags | Preserve the actual single version authority; do not add an App build number or another declaration. |
| CLI with a plugin manifest and derived runtime constant | Identify CLI and plugin authorities separately; route generation and checks to existing tools. |
| Existing release facts and mechanics reference at another repository path | Complete it, adjust the profile target and all routes, keep one release reference and leave VERSIONING separate. |
| New project with no release scripts | Explicitly state that automation is not established; no invented commands or claims of candidate validation. |
| New toolchain or changed check definitions | Check results are invalid for the affected stage and its dependents; retain failure records. |
| Unchanged source and exact accepted package | Reuse only trusted matching check results; preserve the accepted bytes during publication. |
