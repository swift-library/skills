# Minimal Profile

Use the minimal profile for the smallest stable documentation-first repository
baseline that still makes Route, Index, Truth, and Governance explicit.

This profile is intentionally small. It is not the default home for the full
public-repo GitHub/community-health surface.

## Output Map

| Target path | Source template | Required |
| --- | --- | --- |
| `AGENTS.md` | `../templates/AGENTS.md.tpl` | yes |
| `README.md` | `../templates/README.md.tpl` | yes |
| `CONTRIBUTING.md` | `../templates/CONTRIBUTING.md.tpl` | yes |
| `Documentation/README.md` | `../templates/Documentation.README.md.tpl` | yes |
| `Documentation/Architecture/README.md` | `../templates/Documentation.Architecture.README.md.tpl` | yes |
| `Documentation/Architecture/VersioningAndRelease.md` | `../templates/Documentation.Architecture.VersioningAndRelease.md.tpl` | yes |

## Not Forced In This Profile

- `Documentation/Proposals/README.md`
- `Documentation/Decisions/README.md`
- `Documentation/Migrations/README.md`
- `Documentation/Archive/README.md`
- `Documentation/Reference/README.md`
- `LICENSE`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`
- `GOVERNANCE.md`
- `.github/CODEOWNERS`
- `.github/ISSUE_TEMPLATE/bug.md`
- `.github/ISSUE_TEMPLATE/feature.md`
- `.github/ISSUE_TEMPLATE/_config.yml`
- `.github/pull_request_template.md`

## README Placement

GitHub recognizes README files in the hidden `.github`, root, and `docs`
directories. For ordinary Swift package repositories, this profile defaults to
the root `README.md` as the surfaced repository landing page. Do not emit
`.github/README.md` unless the target is a special GitHub profile or default
community-health repository.
