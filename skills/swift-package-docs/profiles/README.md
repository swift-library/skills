# Profiles

Profiles define target-repository output composition from existing template
sources.

Use profiles as composition guidance for scaffold and export work. They are not
automation.

Profiles currently defined:

- `minimal.md`: smallest stable docs-first baseline
- `standard.md`: first public-repo-complete baseline

The distinction is intentional:

- `minimal` keeps the baseline small and docs-first.
- `standard` extends beyond `minimal` into a fuller public repository surface.
- Future profile changes should preserve that boundary unless the product
  strategy changes deliberately.

Manual preview examples live in `../examples/minimal-export-preview.md` and
`../examples/standard-export-preview.md`.
