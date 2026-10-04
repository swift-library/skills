# Reference Index

Use this index only when `SKILL.md` routing is not enough.

## References

- `scaffold.md`: minimal SwiftPM macOS app skeleton and bootstrap decisions.
- `packaging.md`: `.app` bundle construction, Info.plist, resources, launch,
  and local validation.
- `release.md`: signing, development signing identity, notarization, stapling,
  Gatekeeper, zip, GitHub release, and optional Sparkle appcast.

## Routing

- New SwiftPM-only app skeleton: `scaffold.md`.
- Existing executable needs a `.app`: `packaging.md`.
- Bundle fails to launch or validate: `packaging.md`.
- Development signing setup, Developer ID signing, notarization, stapling, zip,
  GitHub release, or appcast:
  `release.md`.
- If the work becomes source architecture or UI design, it is outside packaging
  scope.
