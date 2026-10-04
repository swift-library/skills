# Profiles

Profiles define target-repository output composition from existing template
sources.

Use profiles as composition guidance for scaffold and export work. They are not
automation.

Profiles describe durable repository documentation output only. They do not
force `.agent/PLANS.md`; create that temporary execution-state artifact only
when a normalize, migration, or export task needs a session-spanning plan.

Profiles currently defined:

- `minimal.md`: smallest stable documentation-first baseline
- `standard.md`: first public-repo-complete baseline

The distinction is intentional:

- `minimal` keeps the baseline small and documentation-first.
- `standard` extends beyond `minimal` into a fuller public repository surface.
- Future profile changes should preserve that boundary unless the product
  strategy changes deliberately.

Manual preview examples live in `../examples/minimal-export-preview.md` and
`../examples/standard-export-preview.md`.
