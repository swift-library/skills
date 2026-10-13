# Cleanup Decisions

Use this table after the publish gate finds content that is already public.
Recommend one approach with its residue; the maintainer decides and executes.

Published history and version tags remain immutable. Rotate or revoke exposed
credentials immediately, then prepare a forward fix. Removing a credential from
visible content does not make the old credential safe. Corrections to released
source use a new version; signed annotated tags retain their original identity.

| Approach | Use when | Residue that remains | Effect |
| --- | --- | --- | --- |
| Forward fix | Current source or documentation needs correction | Old content stays in history, forks and clones | Preserves published identities; release a new version when shipped behavior changes |
| Remove or replace a release attachment | Only an uploaded asset leaked and the maintainer explicitly requests the asset operation | Copies already downloaded | Changes the asset identity; record its digest and verify the corrected upload |
| GitHub Support request | Sensitive content needs removal from hosted cached views or pull request refs | Forks owned by others and external clones | Completion and available remedies are Support's decision; do not assume a history rewrite is required |
| Restrict repository visibility | The maintainer explicitly requests restricting future access | Existing public forks, clones and downloaded assets | Public links and access change; published tag identities remain unchanged |
| Delete a repository | The maintainer explicitly requests deletion after reviewing its consequences | Forks, external clones and mirrors | Removes hosted issues, pull requests, releases, discussions and configuration; do not recreate published versions with different identities |

## Response Procedure

1. Identify the exposed surface and rotate or revoke every affected credential.
   Treat copies outside the repository as still exposed.
2. Preserve the release identities and evidence needed to establish scope.
   Record sensitive findings without copying secret values into reports.
3. Prepare a forward fix through the repository's normal review and validation.
   Correct shipped source in a new release instead of changing a published tag.
4. If an attachment or hosted view needs removal, describe the exact operation,
   remaining copies and affected links for the maintainer's decision.
5. Verify the corrected tree and approved attachment changes. Check that existing
   published tags still resolve to their original commits.

## Facts That Decide Between Rows

- Pull request refs, SHA-addressable views, forks, clones and caches can retain
  old content. Changing visible branches cannot establish that every copy is gone.
- Forks keep their own copies. Deleting the repository or making it private
  does not remove content from public forks.
- Commit IDs and tag targets are inputs to release records and provenance.
  Replacing them invalidates references and previously accepted evidence.
- SwiftPM records a fingerprint per package version on first resolution. Moving
  a published tag can fail resolution for consumers who resolved it before.
  Keep that version stable and publish a corrected version.

## Reporting

For each finding, state the chosen row, credential rotation status without
secret values, residue that remains, affected release or asset identities, and
the verification that proves the correction. Distinguish a prepared change from
an approved or completed external operation.
