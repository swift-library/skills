# Cleanup Decisions

Use this table after the publish gate finds content that is already public.
Recommend one approach with its residue; the maintainer decides and executes.

| Approach | Use when | Residue that remains | What it breaks |
| --- | --- | --- | --- |
| Forward fix | The content is not sensitive, or it is already forked, mirrored or cached elsewhere | Old content stays in history, forks and clones | Nothing |
| Replace a release attachment | Only an uploaded asset leaked; the tag and notes are correct | Copies already downloaded | Asset digests recorded elsewhere |
| Rewrite history and force-push | Sensitive content, no pull requests or forks include it, no published tag must keep its commit | Pull request refs, SHA-addressable views until GitHub collects garbage, forks, existing clones | Tags and releases on rewritten commits, commit links, SwiftPM fingerprints |
| Delete and recreate under the same name | A rewrite is required and pull request refs and cached views must go too | Forks (one becomes the new network root), external clones and mirrors | Stars, watchers, issues, pull requests, releases, discussions, wiki, webhooks, secrets, rulesets; consumers' SwiftPM fingerprints for re-created tags |
| GitHub Support request | Rewritten content must also disappear from cached views and pull request refs on GitHub | Forks owned by others, external clones | Nothing locally; completion is Support's decision |
| Make private, publish a new repository | A fresh public history is needed while keeping the old issues and pull requests | The private original; public forks split into their own network | Stars and watchers stay with the original; links point to a private repository |

## Facts That Decide Between Rows

- Every pull request keeps a `refs/pull/<n>/head` ref on GitHub. That ref keeps
  the pull request's commits and all their ancestors reachable, so a history
  rewrite in a repository with pull requests hides content but does not delete
  it. Removal then needs a GitHub Support request or deletion of the repository.
- Forks keep their own copies. Deleting the repository or making it private
  does not remove content from public forks.
- A rewrite changes commit identity. Published tags, release records and
  provenance that name the old commits become dangling unless they are
  re-created, which consumers observe as a moved tag.
- SwiftPM records a fingerprint per package version on first resolution. A tag
  that now points at a different commit fails resolution on machines that
  resolved it before. Recovery on each affected machine: delete the package's
  entry under `~/Library/org.swift.swiftpm/security/fingerprints/` (macOS) or
  `~/.swiftpm/security/fingerprints/`, then resolve again. Prefer a new version
  over re-creating a published tag.
- Back up before any destructive step: a mirror bundle of all refs, release
  assets, labels, rulesets, secrets names and repository settings.

## Reporting

For each finding, state the chosen row, the residue that will remain, what the
maintainer must back up, and the verification that proves the result (scan of
the new history, release assets and rendered README).
