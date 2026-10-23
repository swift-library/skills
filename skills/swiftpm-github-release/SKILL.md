---
name: swiftpm-github-release
description: SwiftPM package and CLI GitHub release readiness audits and dry runs. Check pre-tag gates, version consistency, adopted CI and repository validation; report blockers and exact next commands. Not for live publishing, signing or App Store release operations.
---

# SwiftPM GitHub Release

## Purpose

Dry-run a SwiftPM package or Swift command-line tool release before GitHub
publication. Decide whether the repository is ready to tag, push, and publish,
and list the smallest set of blockers or follow-up checks.

This skill owns release readiness reporting and command planning. It does not
create tags, push commits, publish GitHub releases, or perform live
distribution operations.

## When To Use

- The user asks whether a SwiftPM package is ready for GitHub release.
- The task mentions release gate, preflight, pre-tag audit, GitHub release,
  SwiftPM publication, release checklist, or package release readiness.
- The repository has `Package.swift` and needs format/test/release-build
  checks before publication.
- The user wants a dry-run command plan for tagging or GitHub release creation
  without performing the live operation.
- A repository is about to become public or push to a public remote for the
  first time, or release attachments are about to be uploaded.
- Checking version/tag consistency, adopted CI readiness, package-declared validation commands, and publish boundaries before release.

## When Not To Use

- App Store, TestFlight, notarization, codesigning, or Xcode archive release
  flows.
- Live `git push`, tag creation, GitHub release creation, or external
  publishing without explicit user confirmation.
- External package-manager packaging, publishing, repository layout, install
  command, audit, or test behavior.
- General implementation, bug fixing, refactoring, or release-note copywriting
  unless the release audit specifically asks for those artifacts.
- Hosted package registry administration beyond noting SwiftPM package identity
  and repository URL implications.

## Inputs To Inspect

- `Package.swift`, `Package.resolved`, and package products/targets.
- README, license, security/contact files, contribution/governance files, and
  GitHub workflow files.
- `.github/swift-package.json` and `.github/release.json` when present.
- VERSIONING, the repository's or the organization's it adopts, for version
  rules, and the release reference `Documentation/Reference/Release.md` for
  each component's version source, compatibility surface, checks and entry
  points. Distinguish generated runtime constants and CLI output from the
  declaration or tag that owns their value.
- Git status, branch, remotes, tags, and the intended release version.
- CI output or local validation command output, if the user provides it.
- Release attachments planned for upload.

Derive CI expectations from the repository's workflows and configured branch
protection or rulesets. Apply [Shared CI](references/shared-ci.md) only when a
caller uses a reusable workflow implementing that specification, for example
`<org>/github-workflows/.github/workflows/swift-package.yml@<sha>` with
`.github/swift-package.json`. Inspect the referenced workflow or its declared
contract to establish adoption; organization membership or a configuration
filename alone does not establish it. Other CI designs follow their own
workflow declarations and configured required checks.

Use the repository's VERSIONING, or the organization VERSIONING adopted through
its own documentation and links. The package's release reference and
declarations supply package facts; link adopted policy instead of copying it
into a package checklist.

## Workflow

1. Classify the release as library package, executable tool, mixed package, or
   dry-run command plan.
2. Identify the release identity:
   - SwiftPM package name from `Package.swift`.
   - Product names and executable names.
   - GitHub owner/repository, if configured.
   - Intended version tag.
   - Candidate commit and the existing tag set; distinguish local observations
     from live GitHub results.
3. Check repository hygiene:
   - no accidental machine-local paths, credentials, generated user state, or
     ignored build output in release-facing files;
   - working tree state is understood;
   - README, license, security, and CI files match the public scope;
   - README install requirements match origin's published tags and branches;
     local refs alone do not establish publication.
4. Check SwiftPM readiness:
   - `Package.swift` parses;
   - package identity and product names are intentional;
   - version/tag owner is clear for executable tools;
   - version owner, CLI `--version` output when available, intended SemVer tag,
     and existing tag set are consistent or the mismatch is reported as a
     blocker/warning.
   - identify the component, change type and accepted bump rationale; compatible
     fixes, features and breaking changes follow its documented policy,
     including explicit 0.x semantics. Number comparison alone does not prove
     compatibility;
5. Run or plan validation commands:
   - derive build, test and other checks from the repository's workflows,
     configuration and existing entry points, including its package directory
     and toolchains;
   - inspect branch protection or rulesets for required checks as configured.
     Report unavailable configuration as unknown, not as none configured;
   - for a caller implementing [Shared CI](references/shared-ci.md), check its
     caller, configuration, jobs and required checks against that
     specification;
   - for other repositories, validate their declared commands and required
     checks without imposing shared job names, configuration or script layout.
6. Check GitHub release readiness:
   - required checks pass for the candidate commit, or their status is unknown;
   - release declarations and callers follow the repository's adopted contract;
   - tag naming is documented or obvious;
   - release notes/changelog source is identified;
   - security reporting path is present.
7. Return a verdict with blockers, warnings, and exact next safe commands.

## Version and Validation Checks

Use the repository's existing read-only version and release checks before
adding generic commands. Updates belong to an explicit generation/update
operation; readiness checks must fail on drift rather than silently repair it.
Whether a change needs a release follows VERSIONING's release timing. A changed
upstream only requires downstream changes or revalidation where it has impact.

Bind check results to the candidate commit and the repository's declared
validation. Report failed or unavailable checks explicitly; a local pass does
not establish the required GitHub check status.

For a tagged mistake or interrupted publication, inspect tag and publication
state first. Follow the adopted release policy and the Safety Rules: preserve
published tags and correct released source through a new version. Distinguish
a source correction from retrying an interrupted publication.

## Publish Boundary Gate

Run this gate when a repository first becomes public, changes from private to
public, pushes to a public remote for the first time, or uploads release
attachments. The scripts live in this skill's `scripts/` directory:

- `scan_publish_surface.py --history <repo>` audits the full history before
  first publication; afterwards `-- <published>..HEAD` covers new commits.
- `scan_publish_surface.py --tree <repo>` and `--asset <file>...` cover the
  tree and any separately planned attachments before upload, including nested
  archives.
- `check_repo_facts.py <repo> --range <published>..HEAD --allow-identity
  <maintainer email> --live` checks commit identities, install URLs and versions,
  workflow branches, `.spi.yml` documentation targets, and the README that
  GitHub renders. It reports deployment-target or tools-version raises as
  non-failing notes for applying the adopted VERSIONING. Pass `--next-version`
  when the pending version is not in `.github/release.json` or `VERSION`.
  Add `--forbid-ai-trailers` only when the repository's or adopted organization's
  policy forbids AI attribution trailers. Add `--breaking-floor-raise` only
  when that policy requires a MINOR bump during 0.x or MAJOR bump from 1.0 for
  deployment-target or tools-version raises.

Pass `--local-name` for other machine or account names and `--deny-file` for
internal names the maintainer lists. Then read shipped docs against the
project's rule for public content: current product facts, without run notes or
comparisons against other projects. Findings are blockers; non-failing notes
require interpretation under the adopted version policy. For content that is
already public, use `references/cleanup-decisions.md`: rotate any exposed
credential and prepare a forward fix. Published history and version tags remain
immutable; removing visible content does not revoke a leaked credential.

## Safety Rules

- Do not run `git tag`, `git push`, `gh release create`, or any command that
  publishes or mutates external state without explicit confirmation.
- Never rewrite published history or move or delete published version tags.
  Correct released source through a new version and rotate exposed credentials.
- Repository deletion, visibility changes and attachment replacement require
  explicit maintainer instructions; none revokes previously downloaded copies.
- Do not infer legal, license, security-contact, or distribution ownership
  decisions. Report missing or inconsistent state.
- If the configured package directory has no `Package.swift`, stop and say
  this skill does not apply.
- If validation commands fail, report the failing command and first actionable
  failure; do not bury the result in a long log.
- If network access is required for GitHub checks, distinguish live
  verification from local-only inference.

## Output Format

Use this shape for most release audits:

```text
SwiftPM GitHub Release Gate

Verdict: Ready / Not ready / Ready with warnings / Unknown
Package: <Package.swift name>
Products: <products>
Version/tag: <version or unknown>
Evidence level: local validation / CI output / dry-run only
Required checks: <repository-configured checks and statuses / none configured / unknown>
Publish surface: clean / <n> findings in history, tree, assets or facts

Blocking issues:
- <surface>: <issue>, <evidence>, <next action>

Warnings:
- ...

Passed checks:
- ...

Next safe commands:
- ...
```

For a repository adopting the shared specification, list the required checks it
names with their statuses and report any configuration mismatch. Otherwise list
the repository's own required checks, or `none configured` when verified; use
`unknown` when unavailable.

For command-plan-only requests, separate local validation commands from live
commands and label live commands as requiring confirmation.

## Validation Rules

Exercise the applicable cases in
[eval fixtures](references/eval-fixtures.md) when changing release behavior.
Use actual Git state and check output as evidence; distinguish a command plan
from an executed check. Apply [Shared CI](references/shared-ci.md) validation
and release requirements only to repositories adopting an implementation of
that specification. Use the [reference index](references/_index.md) for
publish-cleanup guidance.

## Decision Rules

- A passing local release gate is not the same as a published release. It only
  means known local and repository-facing checks are ready.
- For CLI tools, product/executable names matter more to users than
  `Package.swift` display name.
- For CLI tools with an in-source version constant, the intended release tag,
  source version, and `--version` output must agree unless the release owner has
  explicitly chosen a different convention.
- For SwiftPM library consumers, source-control package identity usually follows
  the dependency URL basename; call out mismatches between repository basename
  and intended package identity.
- For GitHub organization/repository naming, prefer the product/repository
  identity the user has chosen unless it breaks SwiftPM consumer ergonomics.
- Keep release automation reusable. Project-specific release checklists should
  become repo-local plans or CI jobs, not permanent general skill text.
