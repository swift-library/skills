# Standard Export Preview

## Profile

This preview shows the expected target-repository outcome for the `standard`
profile when the GitHub settings owner has selected local community files.
Inherited community-health files are omitted from the export.

## Module Selection

This preview uses the default agent guide, which omits the Canonical Artifacts
section. For a target adopting that contract, add `--module canonical-artifacts`
to `scripts/export_profile.py`; the target tree stays the same.

## Source Templates Used

- `templates/Documentation.Reference.Release.md.tpl` ->
  `Documentation/Reference/Release.md`
- `templates/AGENTS.md.tpl` -> `AGENTS.md`
- `templates/README.md.tpl` -> `README.md`
- `templates/CONTRIBUTING.md.tpl` -> `CONTRIBUTING.md`
- `templates/LICENSE.tpl` -> `LICENSE`
- `templates/CODE_OF_CONDUCT.md.tpl` -> `CODE_OF_CONDUCT.md`
- `templates/SECURITY.md.tpl` -> `SECURITY.md`
- `templates/SUPPORT.md.tpl` -> `SUPPORT.md`
- `templates/GOVERNANCE.md.tpl` -> `GOVERNANCE.md`
- `templates/CODEOWNERS.tpl` -> `.github/CODEOWNERS`
- `templates/Documentation.README.md.tpl` -> `Documentation/README.md`
- `templates/Documentation.Architecture.README.md.tpl` ->
  `Documentation/Architecture/README.md`
- `templates/Documentation.Proposals.README.md.tpl` ->
  `Documentation/Proposals/README.md`
- `templates/Documentation.Decisions.README.md.tpl` ->
  `Documentation/Decisions/README.md`
- `templates/Documentation.Migrations.README.md.tpl` ->
  `Documentation/Migrations/README.md`
- `templates/Documentation.Archive.README.md.tpl` ->
  `Documentation/Archive/README.md`
- `templates/Documentation.Reference.README.md.tpl` ->
  `Documentation/Reference/README.md`
- `templates/.github.ISSUE_TEMPLATE.bug.md.tpl` ->
  `.github/ISSUE_TEMPLATE/bug.md`
- `templates/.github.ISSUE_TEMPLATE.feature.md.tpl` ->
  `.github/ISSUE_TEMPLATE/feature.md`
- `templates/.github.ISSUE_TEMPLATE.config.yml.tpl` ->
  `.github/ISSUE_TEMPLATE/config.yml`
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
  Documentation/
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
      Release.md
  .github/
    CODEOWNERS
    ISSUE_TEMPLATE/
      bug.md
      feature.md
      config.yml
    pull_request_template.md
```

## Extension Over Minimal

This profile includes all `minimal` files and adds subtree indexes plus a
larger GitHub/community-health surface.

It does not emit `.github/README.md` by default; root `README.md` remains the
GitHub-facing landing page for ordinary repositories.
