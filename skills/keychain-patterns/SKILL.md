---
name: keychain-patterns
description: >-
  Use for Apple Keychain Services in Swift or Apple-platform code: SecItem
  CRUD, OSStatus, kSecClass, kSecAttrAccessible, SecAccessControl, access
  groups/sharing, credential storage, migration from
  UserDefaults/@AppStorage/plists/NSCoding, keychain-bound biometrics, macOS
  data protection keychain, and keychain tests. Do not use for CryptoKit
  algorithms, certificate trust/pinning, App Transport Security, or server auth
  architecture.
---

# Keychain Patterns

Use this skill for Keychain Services implementation, review, debugging, and
modernization on Apple platforms. Keep the workflow centered on Keychain
storage and access control; route cryptography and certificate trust work to
the more specific sibling skills.

## Workflow

1. Identify the operation: review existing code, implement new storage, migrate
   legacy storage, debug a failure, or add tests.
2. Check local constraints before applying a pattern: deployment targets,
   platforms, entitlements, app extensions, background access, biometrics, and
   whether macOS native targets are present.
3. Load only the reference files needed for the operation.
4. For reviews, start with `common-anti-patterns.md`, then load the
   domain-specific file for each finding.
5. For implementations, include explicit `OSStatus` handling, explicit
   accessibility policy, and a test strategy before considering the change
   complete.

## Reference Routing

| Task | Read |
| --- | --- |
| Keychain CRUD, query dictionaries, `OSStatus`, add-or-update | `references/keychain-fundamentals.md` |
| Choosing `kSecClass` or primary-key attributes | `references/keychain-item-classes.md` |
| `kSecAttrAccessible`, `SecAccessControl`, lock-state behavior | `references/keychain-access-control.md` |
| Face ID, Touch ID, `LAContext`, biometric-protected secrets | `references/biometric-authentication.md` |
| OAuth tokens, API keys, password lifecycle, logout cleanup | `references/credential-storage-patterns.md` |
| App extensions, access groups, iCloud Keychain sync | `references/keychain-sharing.md` |
| UserDefaults, `@AppStorage`, plists, NSCoding, first-launch cleanup | `references/migration-legacy-stores.md` |
| Review or audit of generated/security-sensitive code | `references/common-anti-patterns.md` |
| Unit, integration, CI, simulator/device test strategy | `references/testing-security-code.md` |
| OWASP Mobile Top 10, MASVS, or MASTG mapping | `references/compliance-owasp-mapping.md` |

## Core Checks

- Never store passwords, tokens, API keys, or cryptographic key material in
  `UserDefaults`, `@AppStorage`, plist files, source code, or logs.
- Every `SecItem*` call must check `OSStatus` and handle expected cases such as
  `errSecSuccess`, `errSecDuplicateItem`, `errSecItemNotFound`, and
  `errSecInteractionNotAllowed`.
- Every item added to the keychain must set an explicit accessibility policy.
- Use add-or-update for writes; do not delete-then-add as the normal save path.
- Do not run blocking keychain work on `@MainActor` or the UI thread.
- Biometric protection for secrets must be keychain-bound with
  `SecAccessControl`; do not treat `LAContext.evaluatePolicy()` alone as a
  security boundary.
- Native macOS targets that need iOS-style behavior must use
  `kSecUseDataProtectionKeychain: true` unless local constraints rule that out.

## Coordination

- Use `cryptokit-patterns` for AES-GCM, ChaChaPoly, HMAC, hashing, ECDH, ECDSA,
  HPKE, post-quantum CryptoKit APIs, or Secure Enclave key operations.
- Use `certificate-trust-patterns` for `SecTrust`, certificate pinning, SPKI
  hashes, client certificates, mTLS, and URLSession trust challenges.
- Use `swift-programming-language` only for broad baseline checks such as
  spotting secrets in obvious places; move deep Keychain work here.

## Output

For reviews, report findings with severity, affected code, the specific
reference file, and the safer pattern. For implementation or migration, state
deployment-target assumptions, include compatibility notes, and list the
reference files used.
