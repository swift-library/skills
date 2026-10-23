# Release

Release status: partly manual. `scripts/check` validates the collection and
`.github/workflows/ci.yml` runs it for pull requests and pushes to `master`.
Release publication automation is not established in this repository.

Version rules for `swift-skills`, covering tags, release timing, choosing the
next version and the changelog, are in the organization's
[VERSIONING](https://github.com/swift-library/.github/blob/master/VERSIONING.md).
This document records the repository's release facts and mechanics and does not
restate those rules.

## Components and Version Sources

The shipped component is the `swift-skills` plugin. Claude Code and Codex load
the same collection under `skills/`.

| Shipped component | Version meaning | Version source | Mirrors and derived fields | Update and read-only check |
| --- | --- | --- | --- | --- |
| `swift-skills` plugin | Release version in `X.Y.Z` form | Root [`VERSION`](../../VERSION) | `version` in [Claude plugin](../../.claude-plugin/plugin.json) and [root plugin](../../plugin.json); `metadata.version` in [Claude marketplace](../../.claude-plugin/marketplace.json) | Update the source and three mirrors manually; run `python3 -B scripts/validate-plugins.py` or `scripts/check` |

## Compatibility Surface

Consumers depend on the `swift-skills` plugin name, skill names under `skills/`,
and the installation routes in [Installation](../installation.md). VERSIONING
decides how a change to this surface affects the next version. Compatibility
is established by review and tests, not inferred from comparing version
numbers.

## Dependencies and Verified Combinations

Collection checks use Python 3 and Git. Each skill's `SKILL.md` or
`scripts/README.md` identifies the tools its workflow needs. The collection has
no Swift package dependency declarations or lockfile.

[Plugin distribution](../architecture/skill-authoring.md#plugin-distribution)
documents isolated Claude Code and Codex installation checks. Verified host,
operating-system and tool-version combinations for this release are not
established.

## Derived Metadata and Drift Checks

[`scripts/validate-plugins.py`](../../scripts/validate-plugins.py) reads
`VERSION`, checks its `X.Y.Z` format and requires all three mirrors to match.
It also checks plugin identity, marketplace sources and whole-collection skill
discovery. Checks are read-only. Version updates are manual; a version metadata
generator is not established.

[`scripts/check`](../../scripts/check) runs plugin and skill validation,
regression tests, both documentation profile exports and a whitespace check.
Skill validation checks frontmatter, host metadata, links, reference cycles and
organization-neutral content, and reports host listing sizes.
The CI validation job uses read-only repository permissions.

## Candidate, Acceptance and Publication

The candidate is the committed source tree for the whole plugin. Run
`scripts/check` against that candidate and review the version source, mirrors
and changelog. Use the isolated host checks in
[Plugin distribution](../architecture/skill-authoring.md#plugin-distribution)
for installation evidence.

Publication follows the organization's
[release procedure](https://github.com/swift-library/.github/blob/master/VERSIONING.md#release-procedure)
with tag `vX.Y.Z` and message `skills X.Y.Z`. Publication requires an authorized
maintainer with tag and release write access. The repository has collection CI;
a release workflow, automated acceptance receipts and release attachments are
not established. The maintainer must resolve those manual steps before
publication and publish the exact accepted source commit.

## Evidence Reuse and Invalidation

Review local check output and CI results against the candidate commit, check
definitions and actual tool environment. Automated evidence receipts and a
release evidence retention mechanism are not established. Keep required check
logs and host installation results with the candidate's review record.

Changed source, manifests, dependencies or installation routes require fresh
affected checks. Check-only changes require fresh affected validation against
the same identified source artifact. Host installation evidence must identify
the installed plugin version and skill inventory; source checks alone do not
establish host loading. Record failures and retry decisions in the review
record.

## Entry Points and Artifact Retention

| Operation | Existing command or explicit manual procedure | Required access |
| --- | --- | --- |
| Version update and check | Manually update `VERSION` and the three mirrors; run `python3 -B scripts/validate-plugins.py` and `scripts/check` | Repository write access for updates; local read and execution access for checks |
| Candidate validation and build | `scripts/check`; isolated host checks in [Plugin distribution](../architecture/skill-authoring.md#plugin-distribution); a collection release build is not established | Local execution access and the selected hosts |
| Status and interrupted-run recovery | Inspect `git status`, the candidate commit and CI results; publication recovery follows VERSIONING | Repository read access; publication access for recovery |
| Acceptance and publication | Manually review candidate evidence and follow VERSIONING's release procedure with tag `vX.Y.Z` and message `skills X.Y.Z`; release automation is not established | Authorized maintainer with tag and release write access |
| Cleanup | Manually inventory and remove the task's reproducible `.build/` outputs and isolated host homes after verification | Local filesystem access |

The task owns its `.build/` check outputs, isolated host homes and exports.
Preserve unique source changes, required evidence and active processes when
cleaning up. Keep private paths and individual run status in local records,
outside this reference. Automated artifact retention is not established.
