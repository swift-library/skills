# Release And Notarization Notes

Use this file for distribution packaging after the `.app` bundle is already
constructed and locally valid.

## Signing

- Use ad-hoc signing only for local validation.
- Use a `Developer ID Application` identity for distribution outside the Mac
  App Store.
- Keep entitlements explicit and minimal.
- Enable hardened runtime for notarized distribution.

## Entitlements

- The scripts use `APP_ENTITLEMENTS` and default to
  `.build/entitlements/<AppName>.entitlements`.
- Use `assets/templates/App.entitlements` as a starting point when the app
  needs an explicit project-local entitlements plist.
- For Developer ID distribution, do not assume App Sandbox is required. Add
  sandbox, network, user-selected file, Apple Events, or hardened-runtime
  exception entitlements only when the app behavior requires them.
- Review entitlements before signing because they become part of the shipped
  code-signing contract.

Verify after signing:

```bash
codesign --verify --deep --strict --verbose=2 MyApp.app
```

## Development Signing Helper

Use `assets/templates/setup_dev_signing.sh` only when a target project wants a
stable self-signed development code-signing identity to reduce repeated
keychain prompts. The helper creates a local certificate named
`<AppName> Development`, imports it into the login keychain, and prints the
matching `APP_IDENTITY` export.

Do not use that helper for Developer ID distribution. Distribution still needs
a real Developer ID Application identity.

## Notarization

Required tooling:

- Xcode Command Line Tools for `xcrun`, `notarytool`, `stapler`, `codesign`,
  `lipo`, `ditto`, and related packaging utilities.

Credential options:

- Provide App Store Connect API credentials through:
  - `APP_STORE_CONNECT_API_KEY_P8`
  - `APP_STORE_CONNECT_KEY_ID`
  - `APP_STORE_CONNECT_ISSUER_ID`
- Or provide a local `xcrun notarytool` keychain profile through
  `NOTARY_PROFILE`.
- Provide a Developer ID Application identity in `APP_IDENTITY`.

- Do not commit Apple ID credentials, app-specific passwords, API keys, or
  issuer IDs.

Submit and wait with an API key:

```bash
xcrun notarytool submit MyApp.zip \
  --key /tmp/app-store-connect-key.p8 \
  --key-id "$APP_STORE_CONNECT_KEY_ID" \
  --issuer "$APP_STORE_CONNECT_ISSUER_ID" \
  --wait
```

Or submit with a local keychain profile:

```bash
xcrun notarytool submit MyApp.zip \
  --keychain-profile "$NOTARY_PROFILE" \
  --wait
```

Staple and validate:

```bash
xcrun stapler staple MyApp.app
xcrun stapler validate MyApp.app
spctl --assess --type execute --verbose MyApp.app
```

## Zip

- Use `ditto --norsrc -c -k --keepParent MyApp.app MyApp.zip` so the archive
  preserves the app bundle correctly and avoids AppleDouble code sealing
  issues.
- Do not zip the `Contents/` directory by itself.

## Sparkle Appcast

Sparkle appcast output is optional. Use it only when the target project already
uses Sparkle or explicitly requests appcast support.

If Sparkle signing is needed, keep private keys outside the repository and pass
their paths through local environment variables.

- Install Sparkle tools so `generate_appcast` is on `PATH`.
- Provide `SPARKLE_PRIVATE_KEY_FILE` for the ed25519 private key.
- The appcast script uses the zip artifact to create an updated `appcast.xml`.
- Sparkle compares `sparkle:version` from `CFBundleVersion`, so bump
  `BUILD_NUMBER` for every release.

## Tag And GitHub Release

Use a versioned git tag and publish a GitHub release with the notarized zip and
appcast when hosting updates through GitHub Releases.

```bash
git tag v<version>
git push origin v<version>

gh release create v<version> MyApp-<version>.zip appcast.xml \
  --title "MyApp <version>" \
  --notes-file CHANGELOG.md
```

If an appcast or zip is served from GitHub Releases or raw URLs, ensure the
release is published and assets are publicly reachable.
