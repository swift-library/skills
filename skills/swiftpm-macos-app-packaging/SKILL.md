---
name: swiftpm-macos-app-packaging
description: 'Use this skill for SwiftPM-only macOS app packaging without an Xcode app project: scaffold a minimal app layout, package SwiftPM targets and resources into a custom .app bundle, build universal binaries, copy resource bundles and frameworks, build icons, run or verify a local app, configure menu bar LSUIElement behavior, code sign with explicit entitlements, notarize, staple, zip, or prepare a Sparkle appcast. Do not use for Xcode project packaging, iOS Simulator work, Instruments traces, SwiftUI source design, package architecture review, or repository documentation.'
---

# macOS SwiftPM App Packaging

## Purpose

Package SwiftPM-based macOS apps that do not use an Xcode app target. This
skill covers the mechanical app-bundle, signing, notarization, launch, and
optional appcast surface needed to turn a SwiftPM executable into a distributable
macOS `.app`.

This is a packaging skill, not a SwiftUI architecture or source-code design
skill. When packaging evidence identifies a code problem, report it as a
source-level follow-up outside packaging scope.

## When To Use

- Creating or reviewing a `.app` wrapper for a SwiftPM executable.
- Building a macOS app bundle from `.build/release/<executable>`.
- Creating or checking `Contents/Info.plist`, `Contents/MacOS`, resources, or
  bundle identifiers.
- Building host-arch or universal `arm64 x86_64` app binaries with SwiftPM.
- Copying SwiftPM resource bundles or embedded frameworks into an app bundle.
- Setting `MENU_BAR_APP=1` to emit `LSUIElement` for menu bar style apps.
- Running, zipping, signing, notarizing, stapling, or Gatekeeper-verifying a
  SwiftPM-built macOS app.
- Creating a stable local development signing identity for repeatable
  packaging checks.
- Preparing optional Sparkle appcast metadata from an already packaged app.

## When Not To Use

- Do not use for Xcode app target packaging or project signing setup.
- Do not use for iOS Simulator operations.
- Do not use for Instruments `.trace` recording or analysis.
- Do not use for SwiftUI source architecture, visual design, or view
  refactoring.
- Do not use for Swift Package architecture.

## Inputs To Inspect

- `Package.swift`, executable product name, bundle identifier, app name,
  deployment target, resources, frameworks, entitlements, icon source, menu bar
  mode, target architectures, and version values.
- Local signing expectations: ad-hoc, development identity, Developer ID
  Application identity, team ID, App Store Connect API credentials,
  notarization profile, and hardened runtime.
- Existing release scripts, Sparkle configuration, appcast location, and
  project-local packaging docs.

## Workflow

1. Read local project truth first.
2. Decide whether the task is scaffold, package, launch, sign, notarize,
   Gatekeeper verification, or appcast preparation.
3. Open only the matching reference file. Use `references/_index.md` only when
   routing is unclear.
4. Prefer adapting files from `assets/templates/` instead of inventing new
   shell scripts from scratch.
5. Keep local signing and notarization secrets out of repository files. Use
   environment variables or local notarytool keychain profiles.
6. Validate the bundle mechanically before claiming success.

## Version and Artifact Identity

Read the project's version/release policy and existing declaration before
packaging. Record the source of product version and build number, the candidate
commit, dependency lock and target configuration. Derive Info.plist and runtime
display from that authority; prefer existing generation and read-only checks.
An installed app, stale build directory or template default is not the version
source for a distribution build. Missing or conflicting values must fail.

The bootstrap template supplies an explicit `version.env` for a new project.
When adapting the packaging script to a project with another authority, replace
that input with the real source rather than adding a second declaration. The
packaging template requires its source file and does not guess version values.

After signing and notarization, verify the actual bundle's product/build
metadata, executable identity, signature and distribution archive digest.
Bind installation and runtime acceptance to those exact bytes, including a run
without the source/build directories available. Promote the accepted artifact
without rebuilding it. Rebuilds, re-signing, entitlements or packaging changes
invalidate affected evidence; changed toolchain/configuration also invalidates
the stages that used it. Retain original failure logs and resume only with
trusted matching evidence.

Separate artifact identity from checker identity. A check-only correction does
not itself require rebuilding, re-signing or a new product version; validate
the correction and rerun affected checks against the same identified artifact.
Source, dependency, build, packaging or signing changes may affect that artifact.
Follow project policy and investigate uncertain inputs; do not exempt files
merely because they are scripts.

## Reference Files To Consult

- `references/scaffold.md`: minimal SwiftPM app shape and bootstrap template.
- `references/packaging.md`: `.app` bundle construction, Info.plist, resources,
  launch checks, and local validation.
- `references/release.md`: signing, notarization, stapling, Gatekeeper, zip,
  and optional Sparkle appcast handling.

## Assets To Reuse

- `assets/templates/bootstrap/`: minimal SwiftPM macOS app skeleton.
- `assets/templates/package_app.sh`: package a release executable into `.app`.
- `assets/templates/launch.sh`: launch the packaged app.
- `assets/templates/compile_and_run.sh`: package, relaunch, and verify.
- `assets/templates/sign-and-notarize.sh`: Developer ID signing and
  notarization template.
- `assets/templates/setup_dev_signing.sh`: optional self-signed development
  code-signing identity helper.
- `assets/templates/App.entitlements`: optional minimal entitlements plist.
- `assets/templates/build_icon.sh`: `.icon` / image to `.icns` helper.
- `assets/templates/make_appcast.sh`: optional Sparkle appcast template.

## Decision Rules

- Repository-local packaging conventions win over this skill.
- A valid `.app` needs a correct bundle layout, executable binary, Info.plist,
  resources, SwiftPM resource bundles, embedded frameworks, and executable
  permissions before signing or notarization matters.
- Use `SIGNING_MODE=adhoc` for local packaging checks. Use `APP_IDENTITY` with
  a Developer ID Application identity for distribution outside the Mac App
  Store.
- Use `APP_ENTITLEMENTS` for explicit entitlements. Scripts default to
  `.build/entitlements/<AppName>.entitlements`.
- Use `ARCHES="arm64 x86_64"` for universal release builds.
- Use `MENU_BAR_APP=1` only when the app should run as a menu bar / agent-style
  app with `LSUIElement`.
- Notarization must not depend on hard-coded Apple ID credentials in scripts.
- Sparkle appcast generation is optional and only applies when the target
  project already uses Sparkle or explicitly requests appcast output.
- Do not claim Gatekeeper readiness until `spctl` verification passes on the
  packaged or stapled app.

## Validation Rules

- Run `swift build -c release` before packaging.
- For universal builds, verify the final executable contains each requested
  architecture.
- Verify `<App>.app/Contents/MacOS/<Executable>` exists and is executable.
- Verify `plutil -lint <App>.app/Contents/Info.plist`.
- Verify app resources, SwiftPM resource bundles, and embedded frameworks are
  copied when the target project uses them.
- Verify `codesign --verify --deep --strict --verbose=2 <App>.app` after
  signing.
- Verify `spctl --assess --type execute --verbose <App>.app` for Gatekeeper.
- Verify `xcrun stapler validate <App>.app` after notarization and stapling.

## Minimum End-To-End Example

```bash
# 1. Copy and rename the skeleton.
cp -R assets/templates/bootstrap/ ~/Projects/MyApp
cd ~/Projects/MyApp
sed -i '' 's/MyApp/HelloApp/g' Package.swift version.env
mv Sources/MyApp Sources/HelloApp

# 2. Copy scripts.
mkdir -p Scripts
cp assets/templates/package_app.sh Scripts/
cp assets/templates/compile_and_run.sh Scripts/
chmod +x Scripts/*.sh

# 3. Build and launch.
swift build
Scripts/compile_and_run.sh
```

## Common Notarization Failures

| Symptom | Likely Cause | Recovery |
|---|---|---|
| `The software asset has already been uploaded` | Existing submission for the same artifact | Inspect the submission ID, status and log; resume or reuse acceptance only for identical bytes. Rebuild and advance candidate/build identity only when the artifact must change. |
| `Package Invalid: Invalid Code Signing Entitlements` | Entitlements in `.entitlements` do not match provisioning or allowed capabilities | Audit entitlements and remove unsupported keys. |
| `The executable does not have the hardened runtime enabled` | Missing `--options runtime` in distribution signing | Use the release signing path with Developer ID identity. |
| Notarization hangs or no status email arrives | `xcrun notarytool` network or credential issue | Run `xcrun notarytool history` and refresh App Store Connect credentials. |
| `stapler validate` fails after successful notarization | Ticket not propagated yet | Wait briefly, then rerun `xcrun stapler staple`. |

## Output Format

For packaging work, return:

1. Phase / stage judgment
2. Packaging surface inspected
3. Files or templates used
4. Actions performed
5. Validation performed
6. Signing / notarization status
7. Risks
8. Next steps

## Failure / Uncertainty Handling

- If the executable product name is unknown, inspect `Package.swift` before
  guessing.
- If signing identity or notary profile is unknown, keep the script placeholder
  and state the required local value.
- If App Store Connect API credentials are unknown, keep them outside the
  repository and request the local environment values.
- If notarization fails, report the notary log summary and do not mark the app
  as distributable.
- If the target should become an Xcode app project, stop and state that this
  skill is scoped to SwiftPM-only packaging.
