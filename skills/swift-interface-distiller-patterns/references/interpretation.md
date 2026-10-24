# Interpreting API Snapshots

## Completeness Has Two Layers

First inspect expected/collected modules, conflicts and collection gaps. Then
inspect the query or slice's selected-symbol state. A selection can be complete
while the underlying collection is incomplete.

| Observation | Meaning | Safe conclusion |
| --- | --- | --- |
| `present` / observed declaration | Producer supplied the field or declaration | Report it with its provenance and configuration. |
| `absent` | An observation establishes absence | Use only the stated observation's scope. |
| `notCollected`, `unsupported`, `failed`, `filtered`, `unresolved` | Different reasons observations are unavailable or excluded | Preserve the reason; none is a negative fact. |
| `externalReferences` | Compiler IDs outside the collected scope | External observation, not a budget omission or collection gap. |
| `omittedReferences` with `truncated` | Budget omitted in-snapshot symbols | Narrow roots, change format or raise the budget. |
| `complete` slice | All in-snapshot references in the closure were selected | Check collection gaps independently. |

Missing attributes do not prove nonisolation, non-Sendable behavior or absence
of a conformance. Observed conformers are not an exhaustive runtime population.
Returns-a-type and initializer queries yield compiler-reported candidates,
without type inference or witness selection.

An empty default library scope can be successful for a package with no library
products. It says nothing about the package's executable behavior. An import
failure is an error, never a successful empty interface.

## Views And Provenance

The interface view nests reported members and preserves signatures, generic
constraints, availability and reported isolation. It omits bodies and cannot
recover unreported default arguments or attributes. Summary docs stop at a
blank line or structural content; list-only comments have no prose summary.

Readable views collapse standard requirements implied by observed conformances.
`--show-implied` reveals those collected declarations. Canonical JSON and
`--view symbols` retain them regardless. Default synthesized-member exclusion
is a recorded scope policy; it is not missing collection. Protocol extension
declarations and conformances remain in scope.

Interface anchors identify top-level blocks, including standalone external
extensions; members link to their containing block. Views rendered with
`--view symbols` use per-symbol anchors. Use canonical IDs when a stable symbol
identity is needed.

Distinguish compiler-reported, parsed, derived and policy fields. Snapshot
normalization determinism applies to identical observations, not arbitrary
compiler builds or undeclared external inputs. Run reports hold timing, cache
state and execution paths separately from portable canonical snapshots.

## Budgets And Measurements

- Query/slice `--max-bytes` counts the selected payload in the chosen format.
  Snapshot headers and omission diagnostics are outside that limit. JSON
  counts independently encoded symbol records; text counts its rendered
  UTF-8 declarations and context. Inspect `symbolBytes` and actual total
  output when handing the result to a bounded context window.
- `--max-symbols` and `--max-bytes` can produce a truncated selection. External
  references remain separate from omitted in-snapshot symbols.
- Render `--byte-budget` counts an entire Markdown part, including context.
  A top-level declaration stays together with its members and constrained
  extensions. An indivisible block that cannot fit fails with `minimumBytes`;
  do not silently discard its members.
- `--by-module` adds an index and repeated context. Summed file sizes can
  exceed the unsplit interface measured by `render --report`.
- Upstream interface-size measurements compare tracked implementation bytes,
  the whole unsplit interface and the whole canonical JSON. Generated public
  declarations can make an interface larger than tracked source. Preserve
  counting definitions and configuration when comparing new measurements.

Coverage counts collected non-extension symbols once under the recorded
synthesized-member policy. A nonblank raw comment line counts as documented;
excluded symbols and conflicted variants are outside the denominator. A zero
denominator yields null, not full documentation coverage.

## Comparison And Failure Handling

Compare one collector version with compatible configuration identities. A
configuration includes the extractor version; changing it can make snapshots
incomparable. Different scopes record provenance changes without manufacturing
interface additions or removals. Collection gaps, unknown schemas and failures
cannot establish compatibility.

| Exit | Meaning |
| --- | --- |
| `0` | Success or equal observations; inspect result status too. |
| `1` | Observed difference; preserve the structured comparison. |
| `2` | Usage, input, schema or I/O failure. |
| `3` | Process failure or timeout. |
| `4` | Incomplete baseline. |
| `130` | Cancellation. |

Command data goes to stdout or `--output`; JSON errors go to stderr. Child
compiler streams are captured. Keep diagnostics rather than converting errors
into empty snapshots. A valid baseline cannot be replaced by missing expected
modules, failed/unsupported collection or conflicts. External references alone
do not invalidate a scoped baseline.

When the user asks for an interface comparison, run swift-interface-distiller
explicitly with the revisions or snapshots selected for that task. `equal`
describes these observations; it is not a compatibility or runtime-behavior
guarantee and does not choose a SemVer bump.
