# .github

This directory indexes GitHub-facing collaboration and governance files for
`<repo-name>`.

Use this template only for special GitHub profile or default community-health
repositories. Ordinary Swift package repositories should not export
`.github/README.md`; keep the root `README.md` as the GitHub-facing landing
page.

## Belongs Here

- pull request templates
- issue templates
- issue-template configuration
- GitHub Actions workflows
- other GitHub-specific collaboration configuration

## Does Not Belong Here

- current docs architecture truth
- design proposals
- decision records and migrations
- long-form contributor guidance better kept in root governance files

## Related Files

- `CODEOWNERS`: ownership defaults when that file is present
- `../CONTRIBUTING.md`: repo-wide contributor guidance
- `../SECURITY.md` and `../SUPPORT.md`: repo-wide reporting guidance when
  those files are present
- `../Documentation/README.md`: internal docs index
