# Profiles

Profiles define target-repository output composition from existing template
sources.

Use profiles as composition guidance for scaffold and export work. They are not
automation.

Profiles describe durable repository documentation output only. They do not
force `.agent/PLANS.md`; create that temporary execution-state artifact only
when a normalize, migration, or export task needs a session-spanning plan.

Profiles:

- `minimal.md`: smallest stable documentation-first baseline
- `standard.md`: first public-repo-complete baseline

The distinction is intentional:

- `minimal` keeps the baseline small and documentation-first.
- `standard` extends beyond `minimal` into a fuller public repository surface.
- Future profile changes should preserve that boundary unless the product
  strategy changes deliberately.

Manual preview examples live in `../examples/minimal-export-preview.md` and
`../examples/standard-export-preview.md`.

## Optional Modules

Both profiles default to no modules. `--module canonical-artifacts` adds the
complete Canonical Artifacts section to the exported agent guide when the target
adopts the contract or the user requests it. Preserve adopted selections during
regeneration. The module changes guide content, not the profile file map.
