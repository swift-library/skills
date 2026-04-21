# Standard Target Tree

This example shows a more standard normalized end-state for a Swift package
repository.

## Role Map

- Route: `AGENTS.md`
- Index: root and directory `README` files
- Proposal: `Docs/Proposals/*`
- Truth: `Docs/Architecture/*`
- History: `Docs/Decisions/*`, `Docs/Migrations/*`, `Docs/Archive/*`
- Governance: `.github/*`
- Reference: `Docs/Reference/*`

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
  Package.swift
  Sources/
  Tests/
  Docs/
    README.md
    Architecture/
      README.md
      Package.md
      Modules.md
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
    workflows/
      ci.yml
```

This is a profile example, not a mandatory file-for-file export. The authority
is the role boundary, not the exact filename list.
