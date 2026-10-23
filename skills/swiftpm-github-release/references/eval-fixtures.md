# Eval Fixtures

Exercise the applicable cases when changing release behavior.

These cases check readiness audits and dry-run command plans against the
repository's adopted policy and CI design. Apply [Shared CI](shared-ci.md) only
to callers implementing that specification. Supply repository declarations,
candidate commit, required-check configuration and available results as inputs.

## Minimal Library Validation

Input: A library adopting Shared CI declares one compiler and has no optional
validation jobs. Audit its readiness for a GitHub release.

Expected behavior:

- Requires exactly `policy / policy` and `validate / result`.
- Checks formatting, tests and a release build for the candidate commit.
- Checks version/tag consistency, the changelog and shared release caller.
- Enables shared jobs through member configuration instead of generating
  duplicate member check scripts.

## Declared Jobs and Repository Commands

Input: A command-line package adopting Shared CI declares an Apple platform,
DocC targets, a terminal demo and a repository-specific specification check.

Expected behavior:

- Includes the declared platform and docs jobs in validation.
- Uses the demo switch to re-record and compare `recording.json`; rendering
  belongs to the local presentation toolchain.
- Runs the specification check through `commands`, using lowercase `scripts/`
  only when the repository needs a script.
- Derives local commands from the configured package directory and toolchains.

## Local Checks Without GitHub Results

Input: Local validation passes, but GitHub check results for the candidate
commit are unavailable. The user asks for a readiness verdict and command plan.

Expected behavior: reports the local result and unknown required-check status
separately. Lists the remaining checks and exact next commands, distinguishing
executed validation from planned operations. Does not publish or change Git
state while preparing the plan.

## Shared Release Dry Run

Input: A member adopting Shared CI has a release declaration and asks for the
steps to publish its next version.

Expected behavior: checks the shared release caller runs after successful
validation of the tagged commit, verifies a signed annotated tag, version and
changelog, and publishes release notes according to the contract. Reports this
as a plan and leaves live operations to the release owner.

## Correction After Tagging

Input: A published tag contains a mistake. The owner asks how to correct it;
the project follows the VERSIONING policy it adopts from its organization.

Expected behavior: references the immutable-tag policy, prepares a new patch
version and a changelog entry identifying the superseded version and fix.
Separately identifies a pre-tag failure or interrupted publication when that
is the supplied state.

Forbidden behavior: moves/deletes the published tag, overwrites release
attachments, or consumes a new patch solely to retry an interrupted upload.

## Standalone Repository

Input: A standalone SwiftPM repository uses its own GitHub Actions workflows,
with `build-and-test` required by branch protection and no shared workflow.

Expected behavior:

- Checks version/tag consistency, release-facing files, README facts and the
  publish boundary, and runs or plans the repository's declared commands.
- Reports `build-and-test` and its candidate-commit status.
- Produces no Shared CI configuration, caller or fixed-check-name findings.

Acceptance checks: passing declared validation and required checks can yield
Ready. Missing `policy / policy`, `validate / result` or
`.github/swift-package.json` does not change that verdict.

## Organization Adopting the Shared Specification

Input: An organization's member calls
`<org>/github-workflows/.github/workflows/swift-package.yml@<sha>` with
`.github/swift-package.json`; the referenced workflow implements Shared CI.

Expected behavior:

- Checks the caller, pin, configuration and declared jobs against Shared CI.
- Requires `policy / policy` and `validate / result` as specified, and checks
  their statuses for the candidate commit.
- Applies the repository's adopted VERSIONING and enables policy flags only
  when that policy requires them.

Acceptance checks: an invalid configuration or required-check mismatch is a
finding; a conforming caller with passing checks satisfies the CI gate.
Changing the organization name does not change the applicable specification.

## Organization With a Different CI Design

Input: An organization member uses another reusable workflow with its own
configuration and requires `verify / tests`; it does not adopt Shared CI.

Expected behavior:

- Follows that organization's adopted declarations and configured checks.
- Reports `verify / tests` and its candidate-commit status.
- Does not apply Shared CI based on organization membership or file names.

Acceptance checks: absence of Shared CI job names or configuration is not a
finding. A failing declared required check blocks readiness. Verified absence
of required checks is reported as `none configured`; inaccessible branch
protection or rulesets are reported as `unknown`.
