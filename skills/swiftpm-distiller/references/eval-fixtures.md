# Eval Fixtures

When changing the workflow or its examples, exercise the handoff fixture with
the matching CLI. Verify command spelling, output paths and the distinction
between collected declarations and package tool/plugin behavior.

## Compiler API Snapshots In A Skill Handoff

Input: A package has a supporting public library plus executable/plugin
products. Prepare a skill-creation handoff using compiler API snapshots and usage
docs, with a supplied tool version and ignored output directory.

Expected behavior:

- Uses the installed `interface-distiller` command contract for configuration,
  package collection, rendering and symbol queries.
- Routes collection options and snapshot interpretation to the interface
  usage skill; keeps this handoff focused on package-specific operating value.
- Records canonical snapshot and emitted view paths separately, along with
  actual commands, exit codes, configuration, scope and gaps.
- Supports plugin/tool behavior claims with manifest, docs and tests rather
  than assuming library collection describes executable behavior.
- Reports unavailable or stale snapshots without inventing successful commands
  or complete module coverage.

Acceptance checks: execute the example command sequence with the matching
released CLI; its snapshot is valid, its rendered part exists, and its query
finds the library declaration. Review the handoff for provenance and ownership.
