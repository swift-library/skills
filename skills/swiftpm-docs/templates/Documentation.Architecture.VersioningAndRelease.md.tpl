# Versioning and Release

Release status: <implemented, partly manual, or not established; cite evidence>.

This document owns the current version and release rules for <repo-name>.
Operational command details belong in <existing release reference, or not
established>. If an existing document already owns these rules, complete that
document and route readers to it instead of maintaining two normative copies.

## Components and Version Authority

Inspect actual SwiftPM library, CLI, App and plugin components. A library may use
its release tag as authority; an App may declare a product version and build
number; a plugin may own its version in a manifest. Record only the components
this project ships, and preserve each existing source of truth.

| Shipped component | Version meaning | Authoritative source | Derived fields | Update and read-only check |
| --- | --- | --- | --- | --- |
| <actual component> | <accepted scheme; build/candidate meaning if used> | <existing file, backend or tag> | <actual metadata/runtime fields> | <existing entry points, manual step, or not established> |

<Specify accepted compatible-fix, compatible-feature and incompatible-change
rules, including 0.x behavior when applicable. Compatibility is established by
review and tests, not inferred from comparing version numbers. Record the
component, change type and rationale when advancing its version. Documentation,
CI or cleanup alone do not require a product release unless shipped behavior
changes.>

## Dependencies and Verified Combinations

<Identify dependency declarations, compatibility ranges, lockfiles and public
release tags. Explain how a locked revision is verified against the selected
tag, including the ecosystem's version normalization. Keep upstream protocol
baselines separate from actual runtime/tool versions; their numbers need not
match. Record which combinations were actually tested. Upstream changes require
downstream changes or revalidation only when the downstream behavior is affected.>

## Derived Metadata and Drift Checks

<Identify the authority for each field and the real generation entry point.
Separate explicit updates from read-only CI verification. Check declarations,
generated fields, runtime display, dependency locks, tags and actual package
identity where applicable. Missing or conflicting required identity must fail;
installed binaries and old work directories are not release-version sources.
If checks are manual or absent, state that accurately rather than inventing
commands or implemented automation.>

## Candidate, Acceptance and Publication

<Describe the actual candidate and release sequence, source trust boundary,
signing/publishing permissions and the exact artifact accepted. State which
rules are adopted and which automation is implemented. Where candidates exist,
failed candidates revise candidate/build identity rather than consuming a new
formal patch version. Published tags and artifact bytes remain immutable.
Promote the same accepted artifact; rebuilding changes its identity and requires
the affected acceptance again. Publish changed components in dependency order
after their candidate combination has passed.>

## Evidence Reuse and Invalidation

<Identify the trusted evidence source and its validation mechanism. Bind stage
results to source, dependencies, check definitions, toolchain, environment,
target configuration and artifact digests. Reuse only successful evidence with
matching inputs and verified provenance. Reject missing, modified or untrusted
receipts. Changed inputs invalidate affected stages and their downstream results.
Installation evidence identifies the actual package and cannot be replaced by
source tests. Preserve failed results, timings and bounded retry decisions.
Distinguish artifact inputs from checker inputs: identify when check-only changes
can reuse the same artifact with fresh affected checks. Explain which source,
dependency, build or packaging changes require a new artifact. Describe the
project's actual mechanism or manual review; do not assume scripts are exempt
or claim automation that does not exist.>

## Entry Points and Artifact Retention

| Operation | Existing command or explicit manual procedure | Required access |
| --- | --- | --- |
| Version update and check | <actual entries or not established> | <actual access> |
| Candidate validation and build | <actual entries or not established> | <actual access> |
| Status and interrupted-run recovery | <actual entries or not established> | <actual access> |
| Acceptance and publication | <actual entries or not established> | <actual access> |
| Cleanup | <actual entry or manual inventory and removal> | <actual access> |

<Define run ownership and safe cleanup of reproducible caches and temporary
outputs. Preserve unique source changes, required evidence, active processes,
production data and necessary rollback artifacts. Keep private paths and
individual run status in local records, outside this normative document.>
