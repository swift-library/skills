# Cleanup Decisions

Use this table after the publish gate finds content that is already public.
Recommend one approach with its residue; the maintainer decides and executes.

The default for content that has to leave the visible history is to rewrite the
existing repository and force-push it. Recommend deleting and recreating a
repository only when the maintainer explicitly asks for deletion.

| Approach | Use when | Residue that remains | What it breaks |
| --- | --- | --- | --- |
| Forward fix | The content is not sensitive, or it is already forked, mirrored or cached elsewhere | Old content stays in history, forks and clones | Nothing |
| Replace a release attachment | Only an uploaded asset leaked; the tag and notes are correct | Copies already downloaded | Asset digests recorded elsewhere |
| Rewrite history and force-push (default) | Content must leave the visible history of branches and tags | Pull request refs, SHA-addressable views until GitHub collects garbage, forks, existing clones | Tags and releases on rewritten commits, commit links, SwiftPM fingerprints for moved tags |
| GitHub Support request | Sensitive content must also disappear from cached views and pull request refs after a rewrite | Forks owned by others, external clones | Nothing locally; completion is Support's decision |
| Make private, publish a new repository | A fresh public history is needed while keeping the old issues and pull requests | The private original; public forks split into their own network | Stars and watchers stay with the original; links point to a private repository |
| Delete and recreate under the same name (explicit request only) | The maintainer explicitly asks to delete the repository | Forks (one becomes the new network root), external clones and mirrors | Stars, watchers, issues, pull requests, releases, discussions, wiki, webhooks, secrets, rulesets; consumers' SwiftPM fingerprints for re-created tags |

## Rewrite Procedure

1. Back up a mirror bundle of all refs, release assets, labels, rulesets,
   secret names and repository settings.
2. Merge or close open pull requests, and rotate any exposed credential before
   rewriting. A rewrite never makes a leaked credential safe again.
3. Rewrite in a scratch clone, scan the full new history of every ref, then
   force-push the branches and tags.
4. If published tags moved, publish a new patch release right away so consumers
   have a version that never moved.
5. Remove release attachments that name commits which no longer exist.

## Facts That Decide Between Rows

- Every pull request keeps a `refs/pull/<n>/head` ref on GitHub. That ref keeps
  the pull request's commits and all their ancestors reachable by SHA, so a
  rewrite hides content from branches, tags and search but does not delete it.
  Accept that residue, or ask GitHub Support to purge sensitive data.
- Forks keep their own copies. Deleting the repository or making it private
  does not remove content from public forks.
- A rewrite changes commit identity. Published tags, release records and
  provenance that name the old commits become dangling unless they are
  re-created, which consumers observe as a moved tag.
- SwiftPM records a fingerprint per package version on first resolution. A tag
  that now points at a different commit fails resolution on machines that
  resolved it before. Recovery on each affected machine: delete the package's
  entry under `~/Library/org.swift.swiftpm/security/fingerprints/` (macOS) or
  `~/.swiftpm/security/fingerprints/`, then resolve again. The new patch
  release from the procedure above avoids the problem for new consumers.

## Reporting

For each finding, state the chosen row, the residue that will remain, what the
maintainer must back up, and the verification that proves the result (scan of
the new history, release assets and rendered README).
