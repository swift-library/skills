# Eval Fixtures

These cases check readiness audits and dry-run command plans against
[Shared CI](shared-ci.md). Supply the repository declarations, candidate commit
and available check results as inputs.

## Minimal Library Validation

Input: A library declares one compiler and has no optional validation jobs.
Audit its readiness for a GitHub release.

Expected behavior:

- Requires exactly `policy / policy` and `validate / result`.
- Checks formatting, tests and a release build for the candidate commit.
- Checks version/tag consistency, the changelog and shared release caller.
- Enables shared jobs through member configuration instead of generating
  duplicate member check scripts.

## Declared Jobs and Repository Commands

Input: A command-line package declares an Apple platform, DocC targets, a
terminal demo and a repository-specific specification check.

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

Input: A member has a release declaration and asks for the steps to publish
its next version.

Expected behavior: checks the shared release caller runs after successful
validation of the tagged commit, verifies a signed annotated tag, version and
changelog, and publishes release notes according to the contract. Reports this
as a plan and leaves live operations to the release owner.

## Correction After Tagging

Input: A published tag contains a mistake. The owner asks how to correct it;
the project follows swift-library VERSIONING.

Expected behavior: references the immutable-tag policy, prepares a new patch
version and a changelog entry identifying the superseded version and fix.
Separately identifies a pre-tag failure or interrupted publication when that
is the supplied state.

Forbidden behavior: moves/deletes the published tag, overwrites release
attachments, or consumes a new patch solely to retry an interrupted upload.
