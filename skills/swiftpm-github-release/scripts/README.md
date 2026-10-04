# Scripts

Read-only checks for the publish boundary. Both print one finding per line as
`category<TAB>detail` and exit 1 when anything is found.

- `scan_publish_surface.py`: scans commit history (`--history REPO_OR_BUNDLE
  -- REV...`), tracked files (`--tree DIR`) or release attachments
  (`--asset FILE...`, including nested tar, zip and gzip) for workstation home
  paths, the local account name, agent execution-state files, credentials, and
  maintainer-supplied patterns (`--deny-file`). CI runner home paths pass.
- `check_repo_facts.py`: compares README install lines with the origin owner
  and existing tags, flags a `.github/README.md` that hides the root README,
  checks push workflow branch filters against the default branch, checks commit
  identities and AI attribution trailers in `--range`, and with `--live` asks
  GitHub which README it renders and whether the About description is set.
