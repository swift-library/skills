# Governance vs Documentation Placement

Use this rule when deciding between `.github/`, root governance files, and
`Documentation/`.

## Decision Test

- If the file configures or directly supports GitHub collaboration behavior, it
  belongs in `.github/`.
- If the file gives repo-wide contributor policy or participation guidance, it
  belongs in a root governance file.
- If the file explains repository-native documentation architecture, it belongs
  in `Documentation/`.

## `.github/`

Belongs:

- pull request templates
- issue templates
- GitHub Actions workflows
- `CODEOWNERS`
- other GitHub-facing collaboration configuration

Does not belong:

- default repository landing README for ordinary source repositories
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
- documentation architecture truth or history

## `Documentation/`

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

- PR templates describe the full documentation architecture instead of linking
  to `Documentation/`.
- `CONTRIBUTING.md` becomes the only place that explains the repository model.
- `Documentation/` stores GitHub template content that should live in `.github/`.
- `.github/` stores internal architecture notes because they affect review.

## Normalization Guidance

- Move GitHub-facing files into `.github/`.
- Keep ordinary repository landing pages at root `README.md`; use
  `.github/README.md` only for special GitHub profile or default
  community-health repositories.
- Move repo-wide contribution and conduct guidance into root governance files.
- Move internal architecture, proposal, truth, history, and reference content
  into `Documentation/`.
- If a governance file must mention documentation structure, keep the guidance
  short and link to the authoritative `Documentation/` location.
- If a documentation file needs to mention PR or issue flow, link to `.github/`
  or root governance files instead of embedding the full policy there.
