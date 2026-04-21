# Templates

This directory holds skill-local template source material for
`swift-package-docs`.

Use it for:

- minimal reusable file skeletons
- scaffold fragments used to build downstream exports

Current template sources:

- `AGENTS.md.tpl`: route-oriented repository entry
- `README.md.tpl`: root repository index
- `LICENSE.tpl`: root OSS license
- `CODE_OF_CONDUCT.md.tpl`: root participation standards
- `SECURITY.md.tpl`: root security reporting guidance
- `SUPPORT.md.tpl`: root support and triage guidance
- `GOVERNANCE.md.tpl`: root maintainer and decision model
- `CODEOWNERS.tpl`: root ownership defaults
- `Docs.README.md.tpl`: `Docs/` tree index
- `Docs.Architecture.README.md.tpl`: current-truth architecture index
- `Docs.Architecture.Doc.md.tpl`: single current-truth architecture document
- `Docs.Proposals.README.md.tpl`: proposal-space index
- `Docs.Proposals.Doc.md.tpl`: single proposal document
- `Docs.Decisions.README.md.tpl`: decision-record index
- `Docs.Decisions.Record.md.tpl`: single decision record
- `Docs.Migrations.README.md.tpl`: migration-record index
- `Docs.Archive.README.md.tpl`: archive index
- `Docs.Reference.README.md.tpl`: reference-material index
- `CONTRIBUTING.md.tpl`: contributor guidance for repo-docs work
- `.github.README.md.tpl`: `.github/` placement index
- `.github.ISSUE_TEMPLATE.bug.md.tpl`: bug-report issue template
- `.github.ISSUE_TEMPLATE.feature.md.tpl`: feature-request issue template
- `.github.ISSUE_TEMPLATE._config.yml.tpl`: issue-template config
- `.github.pull_request_template.md.tpl`: pull-request template

Do not use it for:

- architecture authority
- checked-in generated output
- speculative future template inventories
- workflow systems outside this skill's scope

These templates are upstream inputs for scaffold and export work.

Profile composition guidance lives in `../profiles/`.
