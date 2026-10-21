# Minimal Export Preview

## Profile

This preview shows the expected target-repository outcome for the `minimal`
profile when the GitHub settings owner has selected local community files.
Inherited community-health files are omitted from the export.

## Source Templates Used

- `templates/Documentation.Reference.Release.md.tpl` ->
  `Documentation/Reference/Release.md`
- `templates/AGENTS.md.tpl` -> `AGENTS.md`
- `templates/README.md.tpl` -> `README.md`
- `templates/CONTRIBUTING.md.tpl` -> `CONTRIBUTING.md`
- `templates/Documentation.README.md.tpl` -> `Documentation/README.md`
- `templates/Documentation.Architecture.README.md.tpl` ->
  `Documentation/Architecture/README.md`

## Expected Target Tree

```text
<swift-package-repo>/
  AGENTS.md
  README.md
  CONTRIBUTING.md
  Documentation/
    README.md
    Architecture/
      README.md
    Reference/
      Release.md
```

## Intentional Omissions

This profile does not require `Documentation/Proposals/`,
`Documentation/Decisions/`, `Documentation/Migrations/` or
`Documentation/Archive/`. From `Documentation/Reference/` it requires only
`Release.md`.

It also does not emit `.github/README.md`; normal repositories default to the
root `README.md` for GitHub's surfaced repository landing page.
