# Xcode Archive And Export

Use this file for Xcode release builds: version/build numbers, archive, export,
IPA/PKG preparation, and upload-ready checks.

## Preconditions

- Xcode and command line tools are installed.
- A valid signing identity and provisioning profiles exist, or automatic
  signing is enabled and allowed.
- Scheme, workspace/project path, target platform, and export method are known.

## Version And Build Numbers

Before archiving, inspect the current version and build number. Projects may
use legacy `agvtool` settings or modern `MARKETING_VERSION` /
`CURRENT_PROJECT_VERSION`.

Optional `asc` examples:

```bash
asc xcode version view
asc xcode version edit --version "1.3.0" --build-number "42"
asc xcode version bump --type build
asc xcode version bump --type patch
```

Use project and target flags for deterministic reads in multi-target projects:

```bash
asc xcode version view --project-dir "./MyApp" --target "App"
```

Each uploaded build needs a unique build number higher than previously
uploaded builds for the same app, platform, and version.

Optional remote-safe build number lookup:

```bash
asc builds next-build-number \
  --app "APP_ID" \
  --version "2.2.0" \
  --platform IOS
```

## iOS / iPadOS / watchOS / tvOS / visionOS Build Flow

Clean and archive:

```bash
xcodebuild clean archive \
  -scheme "YourScheme" \
  -configuration Release \
  -archivePath /tmp/YourApp.xcarchive \
  -destination "generic/platform=iOS"
```

Export an IPA:

```bash
xcodebuild -exportArchive \
  -archivePath /tmp/YourApp.xcarchive \
  -exportPath /tmp/YourAppExport \
  -exportOptionsPlist ExportOptions.plist \
  -allowProvisioningUpdates
```

Use `templates/ExportOptions.app-store.plist` for App Store Connect exports.

Optional upload with `asc`:

```bash
asc builds upload --app "APP_ID" --ipa "/tmp/YourAppExport/YourApp.ipa"
```

## macOS App Store Build Flow

Archive:

```bash
xcodebuild archive \
  -scheme "YourMacScheme" \
  -configuration Release \
  -archivePath /tmp/YourMacApp.xcarchive \
  -destination "generic/platform=macOS"
```

Export a PKG:

```bash
xcodebuild -exportArchive \
  -archivePath /tmp/YourMacApp.xcarchive \
  -exportPath /tmp/YourMacAppExport \
  -exportOptionsPlist ExportOptions.plist \
  -allowProvisioningUpdates
```

macOS App Store exports often produce `.pkg` files.

Optional upload with `asc`:

```bash
asc builds upload \
  --app "APP_ID" \
  --pkg "/tmp/YourMacAppExport/YourApp.pkg" \
  --version "1.0.0" \
  --build-number "123"
```

For `.pkg` uploads, version and build number may need to be passed explicitly
when they are not auto-extracted.

When using `asc`, `--pkg` selects macOS upload handling. Add `--wait` when the
task requires waiting for build processing to complete before handoff.

## Developer ID Export

For macOS distribution outside the Mac App Store, export with Developer ID:

```bash
xcodebuild -exportArchive \
  -archivePath /tmp/YourApp.xcarchive \
  -exportPath /tmp/YourAppExport \
  -exportOptionsPlist ExportOptions.developer-id.plist
```

Use `templates/ExportOptions.developer-id.plist`.

## Troubleshooting

### No Profiles For Bundle ID

- Add `-allowProvisioningUpdates` when automatic signing is acceptable.
- Verify the Apple ID or API context has access to the team.
- Verify bundle ID, profile type, certificate, platform, and target
  entitlements match.

### Build Rejected For Missing Icon

macOS requires ICNS icons with the required 1x and 2x sizes, including 16x16,
32x32, 128x128, 256x256, and 512x512.

### CFBundleVersion Too Low

Increment the build number or resolve a remote-safe number before rebuilding.

### Export Method Mismatch

Profile type must match export method: App Store profiles for App Store
exports, Developer ID signing for Developer ID exports, and ad-hoc/development
profiles only for their matching distribution paths.

### Submission Metadata Issues

Encryption declarations, content rights, review answers, and other App Store
submission-health issues are App Store operations. Do not solve them in this
release engineering skill; hand off once the build artifact is valid.

## Validation

- Run clean archive for release builds.
- Use `xcodebuild -showBuildSettings` to verify target settings.
- Confirm archive exists at the requested path.
- Confirm export produced an `.ipa`, `.pkg`, or signed `.app` as expected.
- Confirm exported artifact path before upload or notarization.
