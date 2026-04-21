# Standard Export Preview

## Profile

This preview shows the expected target-repository outcome for the `standard`
profile.

## Source Templates Used

- `templates/AGENTS.md.tpl` -> `AGENTS.md`
- `templates/README.md.tpl` -> `README.md`
- `templates/CONTRIBUTING.md.tpl` -> `CONTRIBUTING.md`
- `templates/LICENSE.tpl` -> `LICENSE`
- `templates/CODE_OF_CONDUCT.md.tpl` -> `CODE_OF_CONDUCT.md`
- `templates/SECURITY.md.tpl` -> `SECURITY.md`
- `templates/SUPPORT.md.tpl` -> `SUPPORT.md`
- `templates/GOVERNANCE.md.tpl` -> `GOVERNANCE.md`
- `templates/CODEOWNERS.tpl` -> `CODEOWNERS`
- `templates/Docs.README.md.tpl` -> `Docs/README.md`
- `templates/Docs.Architecture.README.md.tpl` ->
  `Docs/Architecture/README.md`
- `templates/Docs.Proposals.README.md.tpl` -> `Docs/Proposals/README.md`
- `templates/Docs.Decisions.README.md.tpl` -> `Docs/Decisions/README.md`
- `templates/Docs.Migrations.README.md.tpl` -> `Docs/Migrations/README.md`
- `templates/Docs.Archive.README.md.tpl` -> `Docs/Archive/README.md`
- `templates/Docs.Reference.README.md.tpl` -> `Docs/Reference/README.md`
- `templates/.github.README.md.tpl` -> `.github/README.md`
- `templates/.github.ISSUE_TEMPLATE.bug.md.tpl` ->
  `.github/ISSUE_TEMPLATE/bug.md`
- `templates/.github.ISSUE_TEMPLATE.feature.md.tpl` ->
  `.github/ISSUE_TEMPLATE/feature.md`
- `templates/.github.ISSUE_TEMPLATE._config.yml.tpl` ->
  `.github/ISSUE_TEMPLATE/_config.yml`
- `templates/.github.pull_request_template.md.tpl` ->
  `.github/pull_request_template.md`

## Expected Target Tree

```text
<swift-package-repo>/
  AGENTS.md
  README.md
  CONTRIBUTING.md
  LICENSE
  CODE_OF_CONDUCT.md
  SECURITY.md
  SUPPORT.md
  GOVERNANCE.md
  CODEOWNERS
  Docs/
    README.md
    Architecture/
      README.md
    Proposals/
      README.md
    Decisions/
      README.md
    Migrations/
      README.md
    Archive/
      README.md
    Reference/
      README.md
  .github/
    README.md
    ISSUE_TEMPLATE/
      bug.md
      feature.md
      _config.yml
    pull_request_template.md
```

## Extension Over Minimal

This profile includes all `minimal` files and adds subtree indexes plus a
larger GitHub/community-health surface.
