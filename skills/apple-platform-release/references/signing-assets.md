# Signing Assets

Use this file for Apple signing setup: bundle IDs, capabilities, certificates,
provisioning profiles, rotation, and shared signing storage.

## Preconditions

- Apple Developer team access is available.
- Authentication for the chosen tool is configured when using automation, such
  as `asc auth login` or `ASC_*` environment variables.
- Bundle identifier and platform are known.
- A CSR file exists when creating certificates through API-backed tooling.

## Bundle IDs

Find or create the bundle ID before creating profiles:

```bash
asc bundle-ids list --paginate
asc bundle-ids create \
  --identifier "com.example.app" \
  --name "Example" \
  --platform IOS
```

Use the platform matching the target: iOS-family apps, macOS apps, or other
Apple-platform targets. Do not reuse a bundle ID across unrelated products.

## Capabilities

List current capabilities before adding new ones:

```bash
asc bundle-ids capabilities list --bundle "BUNDLE_ID"
asc bundle-ids capabilities add --bundle "BUNDLE_ID" --capability ICLOUD
```

Some capabilities require structured settings:

```bash
asc bundle-ids capabilities add \
  --bundle "BUNDLE_ID" \
  --capability ICLOUD \
  --settings '[{"key":"ICLOUD_VERSION","options":[{"key":"XCODE_13","enabled":true}]}]'
```

Keep capabilities aligned with entitlements in the Xcode target. Capability
drift is a common cause of archive/export and runtime entitlement failures.

## Certificates

List certificate inventory before creating or revoking anything:

```bash
asc certificates list --certificate-type IOS_DISTRIBUTION
```

Create a certificate from a CSR when needed:

```bash
asc certificates create \
  --certificate-type IOS_DISTRIBUTION \
  --csr "./cert.csr"
```

Certificate type must match release path: iOS distribution, Apple
distribution, Developer ID Application, or Developer ID Installer as
appropriate. Developer ID certificates may require manual creation in the
Apple Developer portal depending on available API support.

## Provisioning Profiles

Create App Store profiles for upload builds:

```bash
asc profiles create \
  --name "AppStore Profile" \
  --profile-type IOS_APP_STORE \
  --bundle "BUNDLE_ID" \
  --certificate "CERT_ID"
```

Create development or ad-hoc profiles with devices when needed:

```bash
asc profiles create \
  --name "Dev Profile" \
  --profile-type IOS_APP_DEVELOPMENT \
  --bundle "BUNDLE_ID" \
  --certificate "CERT_ID" \
  --device "DEVICE_ID"
```

Download profiles to a local path:

```bash
asc profiles download \
  --id "PROFILE_ID" \
  --output "./profiles/AppStore.mobileprovision"
```

For multiple certificates, use the chosen tool's multi-certificate support,
such as comma-separated certificate IDs where supported.

Device management is separate from profile creation. When development or
ad-hoc profiles require devices, use the chosen tool's device commands first;
with `asc`, device management uses `asc devices` and requires UDIDs.

## Rotation And Cleanup

Rotation should be explicit:

```bash
asc certificates revoke --id "CERT_ID" --confirm
asc profiles delete --id "PROFILE_ID" --confirm
```

Before revoking, identify every app, CI system, and local developer workflow
that depends on the old certificate or profile.

## Shared Team Storage

Use encrypted team storage when signing assets must be shared across CI or a
small team. This is a release engineering concern, not App Store operations.

Example with `asc signing sync`:

```bash
asc signing sync push \
  --bundle-id "com.example.app" \
  --profile-type IOS_APP_STORE \
  --repo "git@github.com:team/certs.git" \
  --password "$MATCH_PASSWORD"

asc signing sync pull \
  --repo "git@github.com:team/certs.git" \
  --password "$MATCH_PASSWORD" \
  --output-dir "./signing"
```

Notes:

- `--password` may fall back to `ASC_MATCH_PASSWORD`.
- Pulling writes files to disk; keychain import and profile installation are
  separate steps.
- Do not commit unencrypted certificates, private keys, provisioning profiles,
  or API keys.

## Validation

- `security find-identity -v -p codesigning`
- Check bundle ID capabilities against target entitlements.
- Confirm profile type matches export method.
- Confirm team ID and bundle ID match the Xcode target.
- Use `--paginate` for large accounts.
- Check `--help` for exact enum values such as certificate types, profile
  types, platforms, and capability names.
