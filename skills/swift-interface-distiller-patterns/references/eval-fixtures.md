# Eval Fixtures

Use the matching released executable and real output for command checks. These
cases define behavior expectations, not recorded performance or trigger scores.
Fixture modules, symbols, paths, configurations and budgets are supplied inputs.

## Understand An Unfamiliar Dependency

Input prompt: "Show me this dependency's construction API and protocol
requirements without reading its implementation. I have its resolved checkout."

Expected behavior: records the package and resolved module identities, selects
configuration and scope explicitly, collects the selected dependency module,
reads the interface, and queries initializers/members or observed conformers.
Keeps gaps and unreported fields visible.

Forbidden behavior: guesses modules from repository names, reads implementation
as the default discovery path, or invents runtime semantics from signatures.

Acceptance checks: commands succeed with the real CLI; selected modules and
configuration match the request; declarations are traceable to the snapshot.

## Compact Context With A Hard Delivery Limit

Input prompt: "Give another agent the interface around this type within the
supplied total byte limit. Include the declarations it references."

Expected behavior: chooses a format and documentation depth, slices the roots,
checks `symbolBytes`, omissions and state, then measures the whole artifact.
Accounts for headers/diagnostics outside the query budget. Reduces the payload
or explains an infeasible minimum instead of claiming the flag caps stdout.

Forbidden behavior: cuts raw bytes from JSON or declarations, treats a truncated
slice as complete, or hides omission diagnostics to fit the limit.

Acceptance checks: actual UTF-8 delivery size fits the requested limit, or an
explicit size blocker is returned; selection and collection states remain visible.

## External References And Unknown Fields

Input prompt: "The slice is complete but lists external references. Can we say
this type has no concurrency constraints and nothing else is needed?"

Expected behavior: distinguishes out-of-scope compiler IDs from budget-omitted
in-snapshot symbols and checks collection gaps separately. Missing reported
concurrency fields remain unknown; no negative isolation/conformance claim.

Forbidden behavior: marks external references as truncation, calls every
complete slice a complete collection, or converts unknown into "no".

Acceptance checks: JSON and explanation preserve each completeness category.

## Producer Inputs And Language Views

Input prompt: "We have graphs and an importable binary from CI, plus these
C and Objective-C headers. Collect their public API."

Expected behavior: requires the graphs/binary producer configuration, matching
compiler and binary content/search roots. Normalizes graphs and collects
modules/headers through their respective adapters, with explicit target/SDK
configuration and language-labelled results.

Forbidden behavior: assigns the current machine's detected configuration to
unknown producer inputs, or presents the C/Objective-C result as Swift imports.

Acceptance checks: all selected adapter commands run successfully with known
producer inputs; absent configuration or a failed import is reported explicitly.

## Review Two Releases

Input prompt: "Review public API changes between these releases. The attached
evidence was made by different collector versions."

Expected behavior: verifies release/snapshot identities, recollects both
revisions with one collector and compatible configuration/scope before
running the requested comparison explicitly with swift-interface-distiller,
or reports why comparison is unavailable. Separates interface,
documentation, availability and provenance changes.

Forbidden behavior: compares mixed collectors or chooses a SemVer bump from
the diff. Never treats missing baseline evidence as an empty API.

Acceptance checks: the comparison uses matching identities; nonzero difference
status preserves the report; unavailable evidence remains an explicit result.

## Baseline Protection

Input prompt: "Update this baseline from the candidate snapshot, then check it.
One expected module failed collection."

Expected behavior: validates the candidate, rejects an incomplete replacement
and preserves the existing baseline bytes. Explains the incomplete-baseline
exit code. A check operation never writes the baseline.

Forbidden behavior: overwrites the baseline, filters away a gap to pass, or
confuses external references alone with incomplete collection.

Acceptance checks: baseline digest is unchanged after rejected write and check;
stderr/exit evidence identifies the failure.

## Large Interface View

Input prompt: "The interface is larger than tracked source and one declaration
does not fit a rendered part. Make a readable context bundle."

Expected behavior: checks generated public API and counting definitions, uses
module navigation or focused queries, and handles render `minimumBytes`
without splitting a type's members. Explains index/context overhead and uses
`--docs`/`--show-implied` according to the question.

Forbidden behavior: promises a fixed compression ratio, drops generated API
or silently omits members to satisfy a render budget.

Acceptance checks: successful parts fit their render budgets; an oversized
indivisible block produces an explicit actionable size error.

## Adjacent Tasks

Input prompts: "Which source files call this method?" / "Why does this function
deadlock at runtime?" / "Should this API change be a major release?"

Expected behavior: identifies the question as outside public-interface evidence
ownership. May retain relevant declarations as supporting context, but does
not claim to answer source indexing, runtime semantics or version policy.

Acceptance checks: no implementation-index or runtime claims are invented and
no release-policy decision is attributed to the collector.
