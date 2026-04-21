# Governance vs Docs Placement

Use this rule when deciding between `.github/`, root governance files, and
`Docs/`.

## Decision Test

- If the file configures or directly supports GitHub collaboration behavior, it
  belongs in `.github/`.
- If the file gives repo-wide contributor policy or participation guidance, it
  belongs in a root governance file.
- If the file explains repository-native documentation architecture, it belongs
  in `Docs/`.

## `.github/`

Belongs:

- pull request templates
- issue templates
- GitHub Actions workflows
- `CODEOWNERS`
- other GitHub-facing collaboration configuration

Does not belong:

- architecture truth
- proposal drafts
- decision records
- long-form contributor guidance better suited to root governance files

## Root Governance Files

Belongs:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- other repo-wide human policy and participation guidance

Does not belong:

- GitHub UI/configuration files
- docs architecture truth or history

## `Docs/`

Belongs:

- architecture truth
- proposals
- decisions
- migrations
- archives
- reference material

Does not belong:

- GitHub templates and workflow configuration
- generic contributor policy

## Common Failure Modes

- PR templates describe the full docs architecture instead of linking to `Docs/`.
- `CONTRIBUTING.md` becomes the only place that explains the repository model.
- `Docs/` stores GitHub template content that should live in `.github/`.
- `.github/` stores internal architecture notes because they affect review.

## Normalization Guidance

- Move GitHub-facing files into `.github/`.
- Move repo-wide contribution and conduct guidance into root governance files.
- Move internal architecture, proposal, truth, history, and reference content
  into `Docs/`.
- If a governance file must mention docs structure, keep the guidance short and
  link to the authoritative `Docs/` location.
- If a docs file needs to mention PR or issue flow, link to `.github/` or root
  governance files instead of embedding the full policy there.
