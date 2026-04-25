---
name: apple-platform-release
description: 'Use this skill for Apple-platform release engineering before App Store Connect or Developer ID distribution: signing assets, bundle IDs, capabilities, certificates, provisioning profiles, Xcode version/build numbers, xcodebuild archive/export, IPA or PKG preparation, macOS Developer ID notarization, stapling, Gatekeeper verification, release artifact checks, and upload-ready build troubleshooting. Do not use for App Store metadata operations, TestFlight management, screenshots, pricing, review submission copy, SwiftPM-only no-Xcode app packaging, simulator work, Instruments traces, or app source architecture.'
---

# Apple Platform Release

## Purpose

Prepare Apple-platform apps for release from the engineering side: signing
assets, Xcode archive/export, IPA/PKG or Developer ID artifacts, notarization,
stapling, Gatekeeper checks, and release build troubleshooting.

This is a release engineering skill. It does not own App Store operations,
marketing metadata, screenshots, pricing, TestFlight setup, review submission
copy, or product release planning.

## When To Use

- Setting up or rotating bundle IDs, capabilities, certificates, or
  provisioning profiles.
- Preparing an iOS, iPadOS, watchOS, tvOS, visionOS, or macOS Xcode app for
  release with `xcodebuild archive` and `xcodebuild -exportArchive`.
- Managing `MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`, or upload-safe build
  numbers before release.
- Exporting App Store / App Store Connect IPAs or macOS PKGs.
- Preparing a macOS Developer ID `.app`, `.zip`, `.dmg`, or `.pkg` for
  notarization outside the Mac App Store.
- Debugging signing, provisioning, archive/export, notarization, staple,
  Gatekeeper, or release artifact failures.

## When Not To Use

- Do not use for App Store Connect metadata, pricing, screenshot, TestFlight,
  review submission, encryption questionnaire, or content rights operations.
- Do not use for SwiftPM-only macOS `.app` packaging without an Xcode app
  project; use `swiftpm-macos-app-packaging`.
- Do not use for simulator lifecycle or UI driving; use `ios-simulator`.
- Do not use for Instruments traces; use `xcode-instruments`.
- Do not use for app source architecture, SwiftUI/UI design, or code
  implementation.
- Do not turn this into release automation or roadmap workflow machinery.

## Inputs To Inspect

- Project type: Xcode project/workspace, scheme, target, platform, bundle ID,
  team ID, signing style, entitlements, capabilities, export method, and
  current version/build settings.
- Release goal: App Store IPA/PKG, Developer ID `.app`, `.zip`, `.dmg`, `.pkg`,
  upload-ready artifact, notarized artifact, or troubleshooting report.
- Local tool state: Xcode command line tools, `xcodebuild`, `security`,
  `codesign`, `notarytool`, `stapler`, `spctl`, `ditto`, and optional `asc`.
- Credentials and secrets only by reference: API key profiles, keychain
  profiles, signing identities, CSR paths, profile paths, and environment
  variable names. Do not print or commit secret values.

## Workflow

1. Identify the release path: signing setup, Xcode archive/export, macOS
   notarization, or artifact troubleshooting.
2. Read only the matching reference file from `references/`.
3. Use templates from `templates/` when an ExportOptions plist or release
   checklist is needed.
4. Prefer local project conventions over generic command examples.
5. Keep secrets out of repository files and final output.
6. Validate each handoff point before claiming the artifact is release-ready.

## Reference Files To Consult

- `references/signing-assets.md`: bundle IDs, capabilities, certificates,
  provisioning profiles, rotation, and shared signing storage.
- `references/xcode-archive-export.md`: version/build numbers, Xcode
  archive/export, IPA/PKG preparation, and upload-ready checks.
- `references/macos-notarization.md`: Developer ID signing, notarization,
  staple, Gatekeeper, DMG/PKG notes, and notary troubleshooting.
- `references/release-artifacts.md`: artifact checklist and common handoff
  failures across signing, export, upload, and notarization.

## Templates To Reuse

- `templates/ExportOptions.app-store.plist`: App Store Connect export method.
- `templates/ExportOptions.developer-id.plist`: Developer ID export method.
- `templates/release-checklist.md`: compact release engineering checklist.

## Decision Rules

- App Store metadata and build upload operations are not the same as release
  engineering. This skill stops at upload-ready or notarized artifacts unless
  the user explicitly asks for upload commands as part of artifact preparation.
- Signing asset changes should be explicit and reversible. Do not revoke or
  rotate certificates/profiles without user confirmation.
- Developer ID notarization requires a valid Developer ID Application
  certificate; Developer ID Installer is separate and required for signed PKGs.
- Xcode archive/export should be validated before notarization or upload.
- Build numbers must be upload-safe: higher than previous uploaded builds for
  the same app, platform, and version.
- Use `asc` examples only when the user has or wants that CLI. Otherwise use
  Apple-native tools such as `xcodebuild`, `security`, `codesign`,
  `notarytool`, `stapler`, and `spctl`.

## Validation Rules

- Verify signing identity: `security find-identity -v -p codesigning`.
- Verify project settings with `xcodebuild -showBuildSettings` when the
  project is available.
- Verify archive/export logs before diagnosing App Store Connect or notary
  errors.
- Verify signatures with `codesign -dvvv` and `codesign --verify --deep
  --strict --verbose=2`.
- Verify macOS notarized artifacts with `stapler validate` and `spctl`.
- For IPA/PKG upload readiness, verify version/build number, export method,
  team ID, bundle ID, signing identity/profile, icon presence, and artifact
  path.

## Output Format

For release engineering work, return:

1. Phase / stage judgment
2. Release path
3. Inputs inspected
4. Actions performed or recommended
5. Signing / provisioning status
6. Archive / export status
7. Notarization / Gatekeeper status, if applicable
8. Risks / blockers
9. Next steps
10. Code diff or template diff, if files changed

## Failure / Uncertainty Handling

- If credentials, team IDs, certificate identities, or profiles are unknown,
  state the missing local value and do not invent it.
- If a signing or notarization failure occurs, fetch or request the concrete
  log before proposing broad changes.
- If the task is really App Store operations or TestFlight management, route
  away from this skill.
- If the target is a SwiftPM-only no-Xcode macOS app, route to
  `swiftpm-macos-app-packaging`.
