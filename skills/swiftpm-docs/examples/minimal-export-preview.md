# Minimal Export Preview

## Profile

This preview shows the expected target-repository outcome for the `minimal`
profile.

## Source Templates Used

- `templates/Documentation.Architecture.VersioningAndRelease.md.tpl` ->
  `Documentation/Architecture/VersioningAndRelease.md`
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
      VersioningAndRelease.md
```

## Intentional Omissions

This profile does not require `Documentation/Proposals/`,
`Documentation/Decisions/`, `Documentation/Migrations/`,
`Documentation/Archive/`, or `Documentation/Reference/`.

It also does not emit `.github/README.md`; normal repositories default to the
root `README.md` for GitHub's surfaced repository landing page.
