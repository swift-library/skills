# Scripts

Read-only checks for the publish boundary. Both print one finding per line as
`category<TAB>detail` and exit 1 when findings exist. `check_repo_facts.py`
also prints non-failing `note:<category><TAB>detail` lines.

- `scan_publish_surface.py`: scans commit history (`--history REPO_OR_BUNDLE
  -- REV...`), tracked files (`--tree DIR`) or release attachments
  (`--asset FILE...`, including nested tar, zip and gzip) for workstation home
  paths, the local account name, agent execution-state files, credentials, and
  maintainer-supplied patterns (`--deny-file`). CI runner home paths pass.
- `check_repo_facts.py`: compares README install lines with the origin owner
  and existing tags, flags a `.github/README.md` that hides the root README,
  checks push workflow branch filters against the default branch, checks that
  `.spi.yml` documentation targets exist in `Package.swift`, flags a raised
  deployment target or `swift-tools-version` as a non-failing `floor-raise`
  note for the adopted VERSIONING policy, checks commit identities in `--range`,
  and with
  `--live` asks GitHub which README it renders and whether the About
  description is set.

Pass `--forbid-ai-trailers` to enforce a repository or adopted organization
policy forbidding AI attribution trailers in `--range`. Pass
`--breaking-floor-raise` only when that policy requires a MINOR bump during 0.x
or MAJOR bump from 1.0 for deployment-target or tools-version raises; a smaller
bump produces a failing `version-bump` finding. Other checks remain active.
The pending version comes from `--next-version`, `.github/release.json` when
present, or `VERSION` when present; otherwise the two latest version tags are
compared. These local checks do not prove publication; verify README install
facts against origin with the README checker and inspect live release state.
