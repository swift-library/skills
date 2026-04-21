# Minimal Profile

Use the minimal profile for the smallest stable docs-first repository baseline
that still makes Route, Index, Truth, and Governance explicit.

This profile is intentionally small. It is not the default home for the full
public-repo GitHub/community-health surface.

## Output Map

| Target path | Source template | Required |
| --- | --- | --- |
| `AGENTS.md` | `../templates/AGENTS.md.tpl` | yes |
| `README.md` | `../templates/README.md.tpl` | yes |
| `CONTRIBUTING.md` | `../templates/CONTRIBUTING.md.tpl` | yes |
| `Docs/README.md` | `../templates/Docs.README.md.tpl` | yes |
| `Docs/Architecture/README.md` | `../templates/Docs.Architecture.README.md.tpl` | yes |
| `.github/README.md` | `../templates/.github.README.md.tpl` | yes |

## Not Forced In This Profile

- `Docs/Proposals/README.md`
- `Docs/Decisions/README.md`
- `Docs/Migrations/README.md`
- `Docs/Archive/README.md`
- `Docs/Reference/README.md`
- `LICENSE`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`
- `GOVERNANCE.md`
- `CODEOWNERS`
- `.github/ISSUE_TEMPLATE/bug.md`
- `.github/ISSUE_TEMPLATE/feature.md`
- `.github/ISSUE_TEMPLATE/_config.yml`
- `.github/pull_request_template.md`
