# Minimal Export Preview

## Profile

This preview shows the expected target-repository outcome for the `minimal`
profile.

## Source Templates Used

- `templates/AGENTS.md.tpl` -> `AGENTS.md`
- `templates/README.md.tpl` -> `README.md`
- `templates/CONTRIBUTING.md.tpl` -> `CONTRIBUTING.md`
- `templates/Docs.README.md.tpl` -> `Docs/README.md`
- `templates/Docs.Architecture.README.md.tpl` ->
  `Docs/Architecture/README.md`
- `templates/.github.README.md.tpl` -> `.github/README.md`

## Expected Target Tree

```text
<swift-package-repo>/
  AGENTS.md
  README.md
  CONTRIBUTING.md
  Docs/
    README.md
    Architecture/
      README.md
  .github/
    README.md
```

## Intentional Omissions

This profile does not require `Docs/Proposals/`, `Docs/Decisions/`,
`Docs/Migrations/`, `Docs/Archive/`, or `Docs/Reference/`.
