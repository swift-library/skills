# Templates

This directory holds skill-local template source material for
`swiftpm-docs`.

Use it for:

- minimal reusable file skeletons
- scaffold fragments used to build downstream exports

Current template sources:

- `AGENTS.md.tpl`: route-oriented repository entry
- `README.md.tpl`: root GitHub-facing landing manual and entry index
- `LICENSE.tpl`: root OSS license
- `CODE_OF_CONDUCT.md.tpl`: root participation standards
- `SECURITY.md.tpl`: root security reporting guidance
- `SUPPORT.md.tpl`: root support and triage guidance
- `GOVERNANCE.md.tpl`: root maintainer and decision model
- `CODEOWNERS.tpl`: `.github/CODEOWNERS` ownership defaults
- `Documentation.README.md.tpl`: `Documentation/` tree index
- `Documentation.Architecture.README.md.tpl`: current-truth architecture index
- `Documentation.Architecture.Doc.md.tpl`: single current-truth architecture document
- `Documentation.Proposals.README.md.tpl`: proposal-space index
- `Documentation.Proposals.Doc.md.tpl`: single proposal document
- `Documentation.Decisions.README.md.tpl`: decision-record index
- `Documentation.Decisions.Record.md.tpl`: single decision record
- `Documentation.Migrations.README.md.tpl`: migration-record index
- `Documentation.Archive.README.md.tpl`: archive index
- `Documentation.Reference.README.md.tpl`: reference-material index
- `CONTRIBUTING.md.tpl`: contributor guidance for repository documentation work
- `.agent.PLANS.md.tpl`: `.agent/PLANS.md` temporary execution-state scaffold
  for larger normalize, migration, or export work
- `.github.ISSUE_TEMPLATE.bug.md.tpl`: bug-report issue template
- `.github.ISSUE_TEMPLATE.feature.md.tpl`: feature-request issue template
- `.github.ISSUE_TEMPLATE._config.yml.tpl`: issue-template config
- `.github.pull_request_template.md.tpl`: pull-request template

Special-case template sources:

- `.github.README.md.tpl`: `.github/` placement index for GitHub profile or
  default community-health repositories. Do not include this in ordinary Swift
  package repository default exports because GitHub can surface it ahead of the
  root `README.md`.

Do not use it for:

- architecture authority
- checked-in generated output
- speculative future template inventories
- workflow systems outside this skill's scope

These templates are the sources for scaffold and export work.

Profile composition guidance lives in `../profiles/`.
