# Eval Fixtures

## Complete Checking Before And After Swift 6 Migration

Input: A package has a target in Swift 5 language mode and another in Swift 6
mode. Assess shared mutable state before migrating the older target. The
manifest tools version and compiler are supplied independently.

Expected behavior:

- Reads both manifest tools version and effective target language mode.
- For a pre-Swift 6 mode, enables complete checking using the manifest's
  supported feature setting or the complete-checking compiler flag.
- Uses the experimental StrictConcurrency setting with Swift 5.9/5.10 tools
  and the upcoming-feature setting with Swift 6.0+ tools.
- Keeps complete checking unconditional for the Swift 6 target and does not
  add a redundant feature setting there.
- Treats warnings from the earlier mode as migration diagnostics, without
  claiming that a newer compiler tests an older compiler's runtime support.

Acceptance checks: compile a nonisolated shared-mutable-state probe under the
selected modes; verify warnings with complete checking in Swift 5 and errors
in Swift 6 without an opt-in. Build representative manifests and inspect their
emitted flags. Preserve the package's supported compiler/OS requirements.
