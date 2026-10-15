---
name: swiftpm-github-release
description: Audit and dry-run GitHub release readiness for SwiftPM packages and Swift command-line tools. Use for pre-tag gates, version/tag consistency, dependency requirement review, interface evidence comparison, CLI smoke planning, publish-boundary checks, and local checkout closure after explicitly authorized publication. Produce readiness findings and exact next commands. Do not use for live tag pushes, GitHub release creation, external package-manager publishing, notarization/signing, App Store releases, or broad code fixes unless the user explicitly asks for those separate actions.
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
- The canonical local checkout, which may differ from the audit or release
  worktree, and the remote's actual default branch.

For swift-library repositories, use the organization's
[VERSIONING](https://github.com/swift-library/.github/blob/master/VERSIONING.md),
[MAINTENANCE](https://github.com/swift-library/.github/blob/master/MAINTENANCE.md),
and [Workflow Integration](https://github.com/swift-library/.github/blob/master/Documentation/Reference/WorkflowIntegration.md)
as the shared authorities. Repository-local declarations supply package facts;
do not copy shared policy or a workflow run's collector/configuration values
into a package checklist.

## Workflow

1. Classify the release as library package, executable tool, mixed package, or
   dry-run command plan.
2. Identify the release identity:
   - SwiftPM package name from `Package.swift`.
   - Product names and executable names.
   - GitHub owner/repository, if configured.
   - Intended version tag.
   - Fetch the selected remote and tags before drawing conclusions about
     published state. Record local and remote commit IDs; a stale checkout
     cannot establish what was released.
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
   - prefer widening a dependency requirement to cover the previous and new
     supported versions over a disjoint jump. Verify resolution, builds and
     relevant tests at both ends; the lockfile alone tests only one resolution.
     If both ends cannot be supported, classify the requirement change under
     the applicable versioning policy before accepting the bump.
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

For a tagged mistake in swift-library, follow
[Immutable tags](https://github.com/swift-library/.github/blob/master/VERSIONING.md#immutable-tags):
prepare a new patch release and record the superseded version and correction
in `CHANGELOG.md`. A failure before tagging and an interrupted publication have
different recovery rules there; inspect tag and publication state first.

Compare interface evidence only when both snapshots use the same collector
version and compatible configuration and scope. Follow the shared
[API evidence and comparison workflow](https://github.com/swift-library/.github/blob/master/Documentation/Reference/WorkflowIntegration.md#api-evidence-and-comparison)
for baseline selection and recollection with the current pin. Never compare
an old asset directly with a new collector's output. Failed recollection,
missing evidence or incomplete collection leaves the comparison unavailable;
it does not prove compatibility. Report collector identities and whether the
baseline was reused or recollected, separately from the candidate result.

Separate artifact identity from checker identity. A check-only correction does
not itself require rebuilding, re-signing or a new product version; validate
the correction and rerun affected checks against the same identified artifact.
Source, dependency, build, packaging or signing changes may affect that artifact.
Follow project policy and investigate uncertain inputs; do not exempt files
merely because they are scripts.

## Local Release Closure

After explicitly authorized publication, close the release in the canonical
local checkout as well as on the remote. A release worktree alone does not
update the checkout used by subsequent audits.

1. Verify the published release and its immutable tag's resolved commit. Record
   the canonical checkout path, remote, default branch and starting local HEAD.
2. In that checkout, fetch the selected remote and tags without forcing tag
   updates. Inspect status and compare the local default branch with the fetched
   default branch. Preserve unrelated edits, local commits and tag identities.
3. When the checkout can be updated safely, switch to the default branch and
   use `git merge --ff-only <remote>/<default-branch>`. Confirm its final HEAD
   matches the fetched branch and contains the released tag commit. Verify the
   local tag resolves to the same commit as the remote tag.
4. If dirty state, a conflicting tag, divergence or another active worktree
   prevents closure, report it with status, local/remote/tag commit IDs and
   ahead/behind or ancestry evidence. Do not reset, force, discard work or
   claim that the canonical checkout is current.

For a readiness-only audit, report the closure commands as a plan. Keep
publication status and local closure status separate in the handoff.

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
Local release closure: current / planned / blocked, with commit evidence
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
from an executed check. See the [reference index](references/_index.md) for
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
