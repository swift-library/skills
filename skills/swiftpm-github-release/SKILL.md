---
name: swiftpm-github-release
description: Audit and dry-run GitHub release readiness for SwiftPM packages and Swift command-line tools. Use for pre-tag release gates, SwiftPM package publication checks, GitHub release readiness, CI/repository hygiene review, version/tag consistency, CLI smoke planning, and publish-boundary checks before a repository goes public or release attachments are uploaded (history and asset leak scans, commit identity, install URLs, rendered README), with cleanup recommendations for content already public. Do not use for live tag pushes, GitHub release creation, external package-manager publishing, notarization/signing, App Store release work, or broad code fixes unless the user explicitly asks for those separate actions.
---

# SwiftPM GitHub Release

## Purpose

Dry-run a SwiftPM package or Swift command-line tool release before GitHub
publication. Decide whether the repository is ready to tag, push, and publish,
and list the smallest set of blockers or follow-up checks.

This skill owns release readiness reporting and command planning. It does not
create tags, push commits, publish GitHub releases, or perform live
distribution operations by default.

## When To Use

- The user asks whether a SwiftPM package is ready for GitHub release.
- The task mentions release gate, preflight, pre-tag audit, GitHub release,
  SwiftPM publication, release checklist, or package release readiness.
- The repository has `Package.swift` and needs build/test/format/release smoke
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
- Project version/release policy and each component's authoritative version
  source. Distinguish generated runtime constants and CLI output from the
  declaration or tag that owns their value.
- Git status, branch, remotes, tags, and the intended release version.
- CI output or local validation command output, if the user provides it.
- Release attachments planned for upload.

## Workflow

1. Classify the release as library package, executable tool, mixed package, or
   dry-run command plan.
2. Identify the release identity:
   - SwiftPM package name from `Package.swift`.
   - Product names and executable names.
   - GitHub owner/repository, if configured.
   - Intended version tag.
3. Check repository hygiene:
   - no accidental machine-local paths, credentials, generated user state, or
     ignored build output in release-facing files;
   - working tree state is understood;
   - README, license, security, and CI files match the public scope.
4. Check SwiftPM readiness:
   - `Package.swift` parses;
   - dependencies are resolved consistently;
   - package identity and product names are intentional;
   - version/tag owner is clear for executable tools;
   - version owner, CLI `--version` output when available, intended SemVer tag,
     and existing tag set are consistent or the mismatch is reported as a
     blocker/warning.
   - identify the component, change type and accepted bump rationale; compatible
     fixes, features and breaking changes follow its documented policy,
     including explicit 0.x semantics. Number comparison alone does not prove
     compatibility;
   - check declared dependency ranges, locked revisions and public tag
     identities. Keep upstream protocol baselines separate from actual runtime
     versions, and record the combinations that were tested.
5. Run or plan validation commands:
   - read repo-local CI workflows, release docs, scripts, or Makefile tasks and
     prefer their release-facing build/test/format/smoke commands when safe;
   - `swift-format lint --configuration .swift-format --recursive Package.swift Sources Tests`
     when `.swift-format` exists and no repo-local command supersedes it;
   - `swift test`;
   - `swift build -c release`;
   - `swift build -c release --product <product>` for executable products;
   - executable smoke checks such as `--version`, `--help`, and one unknown
     route when the CLI has a route boundary.
6. Check GitHub release readiness:
   - CI workflow covers build/test/format where appropriate;
   - tag naming is documented or obvious;
   - release notes/changelog source is identified;
   - security reporting path is present.
7. Return a verdict with blockers, warnings, and exact next safe commands.

## Version and Evidence Checks

Use the repository's existing read-only version and release checks before
adding generic commands. Updates belong to an explicit generation/update
operation; readiness checks must fail on drift rather than silently repair it.
Documentation, CI and cleanup alone do not force a product release. A changed
upstream only requires downstream changes or revalidation where it has impact.

Identify the candidate commit and the exact artifacts covered by acceptance.
Reuse a successful result only when its provenance is trusted and its source,
dependencies, check definitions, toolchain, environment, target configuration
and relevant artifact digests still match. Missing or modified receipts are
not evidence. Changed inputs invalidate affected checks and their dependents;
preserve the original failure and use bounded retries.

For repositories that distribute built artifacts, check that the candidate is
accepted before formal publication and that publication promotes those same
bytes. A rebuild or re-sign changes artifact identity and requires affected
acceptance again. A failed candidate revises candidate/build identity under
the project policy; it does not by itself consume a formal patch version.
Published tags and artifacts remain immutable. Report absent automation
accurately; this readiness skill does not implement a release scheduler.

Separate artifact identity from checker identity. A check-only correction does
not itself require rebuilding, re-signing or a new product version; validate
the correction and rerun affected checks against the same identified artifact.
Source, dependency, build, packaging or signing changes may affect that artifact.
Follow project policy and investigate uncertain inputs; do not exempt files
merely because they are scripts.

## Publish Boundary Gate

Run this gate when a repository first becomes public, changes from private to
public, pushes to a public remote for the first time, or uploads release
attachments. The scripts live in this skill's `scripts/` directory:

- `scan_publish_surface.py --history <repo>` audits the full history before
  first publication; afterwards `-- <published>..HEAD` covers new commits.
- `scan_publish_surface.py --tree <repo>` and `--asset <file>...` cover the
  tree and every attachment before upload, including nested archives. Attach
  CI-built evidence or files that pass the scan.
- `check_repo_facts.py <repo> --range <published>..HEAD --allow-identity
  <maintainer email> --live` checks commit identities, AI attribution
  trailers, install URLs and versions, workflow branches, and the README that
  GitHub renders.

Pass `--local-name` for other machine or account names and `--deny-file` for
internal names the maintainer lists. Then read shipped docs against the
project's rule for public content: current product facts, without run notes or
comparisons against other projects. Findings are blockers. For content that is
already public, recommend a row from `references/cleanup-decisions.md`.

## Safety Rules

- Do not run `git tag`, `git push`, `gh release create`, or any command that
  publishes or mutates external state without explicit confirmation.
- History rewrites, force pushes, repository deletion, visibility changes and
  attachment replacement are recommendations until the maintainer explicitly
  instructs them.
- Do not infer legal, license, security-contact, or distribution ownership
  decisions. Report missing or inconsistent state.
- If the current repository has no `Package.swift`, stop and say this skill
  does not apply.
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
