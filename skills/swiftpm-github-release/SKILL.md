---
name: swiftpm-github-release
description: Audit and dry-run GitHub release readiness for SwiftPM packages and Swift command-line tools. Use for pre-tag gates, version/tag consistency, shared CI readiness, repository validation commands, and publish-boundary checks. Produce readiness findings and exact next commands from the package declarations and shared CI contract. Do not use for live tag pushes, GitHub release creation, external package-manager publishing, notarization/signing, App Store releases, or broad code fixes.
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

Read [Shared CI](references/shared-ci.md) for the validation and release
contract. Members enable its shared jobs through their declarations. For
swift-library repositories, also use the organization's
[VERSIONING](https://github.com/swift-library/.github/blob/master/VERSIONING.md),
and [MAINTENANCE](https://github.com/swift-library/.github/blob/master/MAINTENANCE.md).
The package's release reference and declarations supply package facts; link
shared policy instead of copying it into a package checklist.

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
   - README, license, security, and CI files match the public scope.
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
   - check the member's caller and configuration against
     [Shared CI](references/shared-ci.md); the required checks are exactly
     `policy / policy` and `validate / result`;
   - formatting, tests and a release build always run; platforms, docs and
     the terminal demo run only when declared;
   - derive local commands from the repository's configuration and existing
     entry points, including its package directory and toolchains;
   - enable shared jobs instead of writing member check scripts. Additional
     repository-specific checks use `commands`; create lowercase `scripts/`
     only when such automation is needed.
6. Check GitHub release readiness:
   - required checks pass for the candidate commit, or their status is unknown;
   - release declarations and the shared release caller follow the contract;
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

For a tagged mistake or an interrupted publication in swift-library, inspect tag
and publication state first, then follow
[Immutable tags](https://github.com/swift-library/.github/blob/master/VERSIONING.md#immutable-tags).

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
  <maintainer email> --live` checks commit identities, AI attribution
  trailers, install URLs and versions, workflow branches, `.spi.yml`
  documentation targets, deployment-target or tools-version raises hidden in a
  non-breaking bump, and the README that GitHub renders. Pass `--next-version`
  when the pending version is not in `.github/release.json` or `VERSION`.

Pass `--local-name` for other machine or account names and `--deny-file` for
internal names the maintainer lists. Then read shipped docs against the
project's rule for public content: current product facts, without run notes or
comparisons against other projects. Findings are blockers. For content that is
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
Required checks: policy / policy <status>; validate / result <status>
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

For command-plan-only requests, separate local validation commands from live
commands and label live commands as requiring confirmation.

## Validation Rules

Exercise the applicable cases in
[eval fixtures](references/eval-fixtures.md) when changing release behavior.
Use actual Git state and check output as evidence; distinguish a command plan
from an executed check. Read [Shared CI](references/shared-ci.md) for validation
and release requirements and the [reference index](references/_index.md) for
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
