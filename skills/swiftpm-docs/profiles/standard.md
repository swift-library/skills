# Standard Profile

Use the standard profile for the first public-repo-complete repository
baseline.

This profile extends beyond `minimal` with proposal, history, reference, and a
fuller GitHub/community-health surface. That distinction is intentional.

## Output Map

`when not inherited` rows are emitted only when the repository's GitHub
settings owner has selected local files instead of shared defaults. That owner
verifies their effect on GitHub; this profile owns the template composition.
See `../rules/governance-vs-documentation-placement.md` for inheritance rules.

| Target path | Source template | Required |
| --- | --- | --- |
| `AGENTS.md` | `../templates/AGENTS.md.tpl` | yes |
| `README.md` | `../templates/README.md.tpl` | yes |
| `CONTRIBUTING.md` | `../templates/CONTRIBUTING.md.tpl` | when not inherited |
| `LICENSE` | `../templates/LICENSE.tpl` | yes |
| `CODE_OF_CONDUCT.md` | `../templates/CODE_OF_CONDUCT.md.tpl` | when not inherited |
| `SECURITY.md` | `../templates/SECURITY.md.tpl` | when not inherited |
| `SUPPORT.md` | `../templates/SUPPORT.md.tpl` | when not inherited |
| `GOVERNANCE.md` | `../templates/GOVERNANCE.md.tpl` | yes |
| `.github/CODEOWNERS` | `../templates/CODEOWNERS.tpl` | yes |
| `Documentation/README.md` | `../templates/Documentation.README.md.tpl` | yes |
| `Documentation/Architecture/README.md` | `../templates/Documentation.Architecture.README.md.tpl` | yes |
| `Documentation/Architecture/VersioningAndRelease.md` | `../templates/Documentation.Architecture.VersioningAndRelease.md.tpl` | yes |
| `Documentation/Proposals/README.md` | `../templates/Documentation.Proposals.README.md.tpl` | yes |
| `Documentation/Decisions/README.md` | `../templates/Documentation.Decisions.README.md.tpl` | yes |
| `Documentation/Migrations/README.md` | `../templates/Documentation.Migrations.README.md.tpl` | yes |
| `Documentation/Archive/README.md` | `../templates/Documentation.Archive.README.md.tpl` | yes |
| `Documentation/Reference/README.md` | `../templates/Documentation.Reference.README.md.tpl` | yes |
| `.github/ISSUE_TEMPLATE/bug.md` | `../templates/.github.ISSUE_TEMPLATE.bug.md.tpl` | when not inherited |
| `.github/ISSUE_TEMPLATE/feature.md` | `../templates/.github.ISSUE_TEMPLATE.feature.md.tpl` | when not inherited |
| `.github/ISSUE_TEMPLATE/config.yml` | `../templates/.github.ISSUE_TEMPLATE.config.yml.tpl` | when not inherited |
| `.github/pull_request_template.md` | `../templates/.github.pull_request_template.md.tpl` | when not inherited |

## README Placement

GitHub recognizes README files in the hidden `.github`, root, and `docs`
directories. For ordinary Swift package repositories, this profile defaults to
the root `README.md` as the surfaced repository landing page. Keep
`.github/README.md` out of default exports unless the target is a special GitHub
profile or default community-health repository.
