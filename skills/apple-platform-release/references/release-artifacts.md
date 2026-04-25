# Release Artifacts

Use this file for cross-cutting release artifact readiness and handoff checks.

## Artifact Types

- App Store / App Store Connect upload: `.ipa` for iOS-family platforms, `.pkg`
  for macOS App Store when exported that way.
- Developer ID distribution: signed `.app`, notarization `.zip`, `.dmg`, or
  signed `.pkg`.
- Supporting evidence: archive path, export log, ExportOptions plist, signing
  identity, team ID, bundle ID, profile, notarization submission ID, notary log,
  staple validation, and Gatekeeper assessment.

## Release Engineering Checklist

1. Confirm scheme, platform, bundle ID, team ID, and export method.
2. Confirm version and build number are upload-safe.
3. Confirm signing identity and provisioning profile match the target.
4. Confirm capabilities and entitlements match the bundle ID.
5. Run a clean archive.
6. Export with the intended ExportOptions plist.
7. Verify exported artifact exists and has the expected type.
8. For macOS Developer ID, verify signature, timestamp, notarization, staple,
   and Gatekeeper.
9. Record remaining blockers without printing secrets.

## Common Failure Boundaries

- Signing asset problem: missing certificate, wrong profile type, wrong team,
  wrong bundle ID, capability/entitlement mismatch.
- Xcode export problem: wrong ExportOptions method, missing provisioning
  profile, automatic signing not allowed, stale build settings.
- Upload-readiness problem: duplicate or too-low build number, missing icon,
  unsupported artifact type, wrong platform.
- Notarization problem: unsigned nested binaries, missing hardened runtime,
  invalid entitlements, missing timestamp, broken trust chain, upload timeout.

## Handoff Notes

Keep the handoff concrete:

- Artifact path:
- Scheme / archive path:
- Export method:
- Bundle ID:
- Team ID:
- Version / build:
- Signing identity:
- Profile:
- Notarization submission ID:
- Validation commands run:
- Blocking errors:
