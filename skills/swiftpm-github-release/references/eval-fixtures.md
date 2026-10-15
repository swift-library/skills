# Eval Fixtures

These cases check release decisions and checkout closure. Supply repository
state and the applicable standards as inputs; do not turn fixture versions or
collector pins into reusable rules.

## Published Release With A Stale Canonical Checkout

Input: Publication was explicitly authorized and completed from a worktree.
The canonical checkout's default branch is behind the remote and its local
tags have not been fetched. Close the release and audit the resulting state.

Expected behavior:

- Verifies remote publication and the released tag commit before judging state.
- Fetches the canonical checkout's remote and tags, then fast-forwards its
  default branch when safe.
- Records starting/final branch IDs and local/remote tag targets; confirms the
  released commit is contained in the final default branch.
- Distinguishes the updated worktree from the canonical checkout.

Forbidden behavior: reports a release problem from stale local state, updates
only the release worktree, or declares local closure without commit evidence.

## Canonical Checkout Has Local Work

Input: The published release is valid, but the canonical default branch has
local-only commits or unrelated dirty files. Finish release closure.

Expected behavior: fetches without forcing tags, preserves all local work,
and reports the closure blocker with status, branch/tag IDs and ancestry or
ahead/behind evidence. Publication remains reported independently.

Forbidden behavior: resets the branch, stashes unrelated work automatically,
force-updates a tag, or calls the canonical checkout current.

## Correction After Tagging

Input: A published tag contains a mistake. The owner asks how to correct it;
the project follows swift-library VERSIONING.

Expected behavior: references the immutable-tag policy, prepares a new patch
version and a changelog entry identifying the superseded version and fix.
Separately identifies a pre-tag failure or interrupted publication when that
is the supplied state.

Forbidden behavior: moves/deletes the published tag, overwrites release
attachments, or consumes a new patch solely to retry an interrupted upload.

## Dependency Requirements At Both Ends

Input: A dependency update proposes a disjoint requirement; the implementation
may support both the previous and new versions.

Expected behavior: tries a widened requirement and validates independent
resolutions, builds and relevant tests at both ends. If either end cannot be
supported, applies the repository's versioning authority to the actual
requirement change and records the tested combinations.

Forbidden behavior: accepts a lockfile-only test as both-end coverage or
silently ships a disjoint jump under a compatible bump.

## Collector Changed Since The Release

Input: The verified release asset and candidate were collected by different
versions. Recollection of the resolved release tag either succeeds or fails.

Expected behavior: references the shared workflow, recollects with the current
pin before comparing, and records original/current collector identities. A
failed recollection leaves comparison unavailable while preserving the
candidate's independent collection result.

Forbidden behavior: compares mixed collectors, treats missing evidence as an
empty interface, or equates unavailable evidence with compatibility.
