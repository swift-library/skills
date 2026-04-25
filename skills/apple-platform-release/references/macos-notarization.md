# macOS Notarization

Use this file for macOS Developer ID distribution outside the Mac App Store:
Developer ID signing, notarization, stapling, Gatekeeper verification, and
notary troubleshooting.

## Preconditions

- Xcode and command line tools are installed.
- The macOS app builds from an Xcode project or workspace.
- A Developer ID Application certificate is available in the local keychain.
- Notarization credentials exist through App Store Connect API keys,
  `notarytool` keychain profile, or another approved local tool setup.

## Verify Signing Identity

Before archiving or exporting, confirm the Developer ID identity:

```bash
security find-identity -v -p codesigning | grep "Developer ID Application"
```

If no identity exists, create a Developer ID Application certificate in the
Apple Developer portal. Do not assume API tooling can create every Developer ID
certificate type.

## Fix Broken Trust Settings

`codesign` or `xcodebuild` errors such as "Invalid trust settings" or
`errSecInternalComponent` can come from custom trust overrides.

Check for overrides:

```bash
security dump-trust-settings 2>&1 | grep -A1 "Developer ID"
```

If overrides exist, export and remove the custom trusted cert entry:

```bash
security find-certificate \
  -c "Developer ID Application" \
  -p ~/Library/Keychains/login.keychain-db > /tmp/devid-cert.pem
security remove-trusted-cert /tmp/devid-cert.pem
```

Verify the signing chain:

```bash
codesign --deep --force --options runtime \
  --sign "Developer ID Application: YOUR NAME (TEAM_ID)" \
  /path/to/any.app 2>&1
```

The chain should resolve through Developer ID Application, Developer ID
Certification Authority, and Apple Root CA.

## Archive And Export With Developer ID

Archive:

```bash
xcodebuild archive \
  -scheme "YourMacScheme" \
  -configuration Release \
  -archivePath /tmp/YourApp.xcarchive \
  -destination "generic/platform=macOS"
```

Export:

```bash
xcodebuild -exportArchive \
  -archivePath /tmp/YourApp.xcarchive \
  -exportPath /tmp/YourAppExport \
  -exportOptionsPlist ExportOptions.developer-id.plist
```

The export should produce a Developer ID signed `.app` with a secure timestamp.

Verify:

```bash
codesign -dvvv "/tmp/YourAppExport/YourApp.app" 2>&1 | grep -E "Authority|Timestamp"
```

Confirm the authority starts with Developer ID Application and a timestamp is
present.

## Create A ZIP For Notarization

```bash
ditto -c -k --keepParent \
  "/tmp/YourAppExport/YourApp.app" \
  "/tmp/YourAppExport/YourApp.zip"
```

Use `ditto` rather than zipping `Contents/` directly.

## Submit For Notarization

With `notarytool` profile:

```bash
xcrun notarytool submit "/tmp/YourAppExport/YourApp.zip" \
  --keychain-profile "$NOTARY_PROFILE" \
  --wait
```

With `asc`, when available:

```bash
asc notarization submit --file "/tmp/YourAppExport/YourApp.zip" --wait
asc notarization submit \
  --file "/tmp/YourAppExport/YourApp.zip" \
  --wait \
  --poll-interval 30s \
  --timeout 1h
```

Fire-and-forget is acceptable only when another process records the submission
ID and checks the result:

```bash
asc notarization submit --file "/tmp/YourAppExport/YourApp.zip"
```

`asc notarization` uses Apple's Notary API v2 rather than `xcrun notarytool`.
It authenticates through the same API key setup as other `asc` commands,
streams files directly to Apple's upload storage, and may use multipart upload
for files larger than 5 GB. Check `asc notarization submit --help` for exact
flags supported by the installed CLI version.

## Check Results And Logs

With `asc`:

```bash
asc notarization status --id "SUBMISSION_ID" --output table
asc notarization log --id "SUBMISSION_ID"
asc notarization list --output table
asc notarization list --limit 5 --output table
```

If a log URL is returned:

```bash
curl -sL "LOG_URL" | python3 -m json.tool
```

With `notarytool`, use the submission output or history/log commands available
in the installed Xcode version.

## Staple And Gatekeeper

Staple an accepted `.app`:

```bash
xcrun stapler staple "/tmp/YourAppExport/YourApp.app"
xcrun stapler validate "/tmp/YourAppExport/YourApp.app"
spctl --assess --type execute --verbose "/tmp/YourAppExport/YourApp.app"
```

For DMG distribution, staple the DMG after creating it:

```bash
hdiutil create \
  -volname "YourApp" \
  -srcfolder "/tmp/YourAppExport/YourApp.app" \
  -ov \
  -format UDZO \
  "/tmp/YourApp.dmg"
xcrun stapler staple "/tmp/YourApp.dmg"
```

## Supported File Formats

| Format | Use Case |
|---|---|
| `.zip` | Simplest notarization container for a signed `.app` bundle |
| `.dmg` | Drag-and-drop install distribution |
| `.pkg` | Installer package; requires Developer ID Installer certificate |

## PKG Notarization

PKG notarization requires a Developer ID Installer certificate, separate from
Developer ID Application.

Sign:

```bash
productsign \
  --sign "Developer ID Installer: YOUR NAME (TEAM_ID)" \
  unsigned.pkg \
  signed.pkg
```

Submit:

```bash
xcrun notarytool submit signed.pkg --keychain-profile "$NOTARY_PROFILE" --wait
```

or, if using `asc`:

```bash
asc notarization submit --file signed.pkg --wait
```

## Troubleshooting

### Invalid Trust Settings During Export

The Developer ID certificate has custom trust overrides. Remove the custom
trust entry and verify the chain.

### Binary Is Not Signed With Developer ID

The app was signed with development or App Store signing. Re-export using
Developer ID export options.

### Signature Does Not Include Secure Timestamp

Add `--timestamp` to manual `codesign` calls, or use
`xcodebuild -exportArchive`, which normally adds timestamps for Developer ID
exports.

### Upload Timeout

Use a longer upload timeout in tools that support it, for example:

```bash
ASC_UPLOAD_TIMEOUT=5m asc notarization submit --file ./LargeApp.zip --wait
```

### Notarization Invalid But Signing Looks Correct

Fetch the developer log. Common causes include unsigned nested binaries,
missing hardened runtime, embedded libraries without timestamps, or entitlement
mismatches.
