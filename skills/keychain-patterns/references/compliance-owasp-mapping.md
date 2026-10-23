# Compliance & OWASP Mapping Reference

> Scope: Maps Keychain storage and access-control patterns to OWASP Mobile Top 10 (2024), MASVS, and MASTG controls for audit and remediation workflows.

**Older guidance still uses the 2016 OWASP Mobile Top 10 numbering — "M2: Insecure Data Storage," "M5: Insufficient Cryptography" — which the 2024 list replaced.** This reference maps current iOS security practices to the OWASP Mobile Top 10 (2024), MASVS v2.1.0, and MASTG test cases for the 2024–2026 compliance window. It covers M1 (Improper Credential Usage), M3 (Insecure Authentication/Authorization), and M9 (Insecure Data Storage), plus key-storage obligations under MASVS-CRYPTO-2. Hardcoded credentials (CWE-798) are listed as a dangerous practice in CISA and FBI's Product Security Bad Practices guidance.

---

## What Changed: 2016 → 2024 OWASP Mobile Top 10

The 2024 edition is a complete overhaul. Four categories are entirely new, two pairs were merged, and everything was renumbered. Any code comment or documentation citing the 2016 numbering is outdated.

| 2024 Category                                 | Status     | 2016 Predecessor   |
| --------------------------------------------- | ---------- | ------------------ |
| **M1: Improper Credential Usage**             | New        | None               |
| **M2: Inadequate Supply Chain Security**      | New        | None               |
| **M3: Insecure Authentication/Authorization** | Merged     | 2016 M4 + M6       |
| **M4: Insufficient Input/Output Validation**  | New        | None               |
| **M5: Insecure Communication**                | Renumbered | 2016 M3            |
| **M6: Inadequate Privacy Controls**           | New        | None               |
| **M7: Insufficient Binary Protections**       | Merged     | 2016 M8 + M9       |
| **M8: Security Misconfiguration**             | Expanded   | 2016 M10 (partial) |
| **M9: Insecure Data Storage**                 | Renumbered | 2016 M2            |
| **M10: Insufficient Cryptography**            | Renumbered | 2016 M5            |

**MASVS v2.1.0** (January 18, 2024) reorganized into 8 control groups with concise, testable controls. The old L1/L2/R verification levels became **MAS Testing Profiles** within the MASTG, aligned with NIST OSCAL. Legacy MSTG-\* test IDs (e.g., MSTG-STORAGE-1) were deprecated in favor of new MASTG-TEST-02xx/03xx identifiers with granular, tool-specific test procedures.

---

## Master Traceability Matrix

This matrix links each OWASP 2024 category to its MASVS controls, MASTG test cases, iOS APIs, and required audit evidence.

| OWASP 2024                        | MASVS v2 Controls                             | Key MASTG Tests (New IDs)                                        | iOS APIs / Flags                                                                        | Required Evidence                                                   |
| --------------------------------- | --------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **M1** Improper Credential Usage  | MASVS-STORAGE-1, MASVS-AUTH-1, MASVS-CRYPTO-2 | 0213, 0214, 0299, 0300, 0302                                     | Keychain + `SecAccessControl`; App Attest                                               | Static scan (no literals); keychain dump with ACL; attestation logs |
| **M3** Insecure Auth/AuthZ        | MASVS-AUTH-1, MASVS-AUTH-2, MASVS-AUTH-3      | 0266, 0267, 0268, 0269, 0270, 0271                               | `SecAccessControlCreateWithFlags` + `.biometryCurrentSet`; `ASWebAuthenticationSession` | Auth flow diagrams; biometric bypass test results; token TTL policy |
| **M9** Insecure Data Storage      | MASVS-STORAGE-1, MASVS-STORAGE-2              | 0296, 0297, 0299, 0300, 0301, 0302, 0303, 0215, 0298, 0313, 0314 | Keychain accessibility flags; `NSFileProtectionComplete`; `isExcludedFromBackup`        | `xattr` listings; backup extraction; keychain dump                  |

> **Cross-reference note:** MASVS-STORAGE-1 and MASTG-TEST-0299/0302 appear under both M1 and M9. This is intentional — keychain configuration simultaneously addresses credential storage and data-at-rest protection. See `keychain-access-control.md` for detailed accessibility flag guidance.

---

## M1 — Improper Credential Usage

**Scope:** Hardcoded credentials in source/config, insecure credential transmission, insecure on-device storage, weak auth protocols. Attack vectors: EASY. Impact: SEVERE. Entirely new in 2024 — no 2016 predecessor.

**Cybernews 2025 data:** 815,000+ hardcoded secrets across 156,080 iOS apps (average 5.2 per app), including 19 Stripe secret keys, 836 unprotected cloud endpoints exposing 406TB, and 2,218 misconfigured Firebase endpoints leaking 19.8M records. Secrets found in plaintext IPA files without decompilation.

### MASTG Test Cases

| Test ID         | Legacy ID      | Verifies                                              | Profile |
| --------------- | -------------- | ----------------------------------------------------- | ------- |
| MASTG-TEST-0213 | MSTG-CRYPTO-1  | No hardcoded cryptographic keys in source/binary      | L1, L2  |
| MASTG-TEST-0214 | MSTG-CRYPTO-5  | No cryptographic keys in bundle files (plist, config) | L1, L2  |
| MASTG-TEST-0299 | MSTG-STORAGE-1 | Files use appropriate Data Protection classes         | L1      |
| MASTG-TEST-0300 | MSTG-STORAGE-1 | Static: references to APIs storing unencrypted data   | L2      |
| MASTG-TEST-0302 | MSTG-STORAGE-2 | Sensitive data unencrypted in private storage         | L2      |

**Testing procedure:** Use radare2 for static analysis — search for `SecKeyCreateWithData` with hardcoded key data or CryptoKit key initialization with inline bytes. Use objection (`ios keychain dump`, `ios nsuserdefaults get`) and filesystem grep at runtime. Check `.xcconfig`, `Info.plist`, and embedded resources for API keys.

**App Attest (iOS 14+):** Closes the secret provisioning gap by verifying device integrity before the server issues credentials. This avoids hardcoded secrets entirely — the server provisions secrets only to attested, genuine app instances. See `credential-storage-patterns.md` for implementation details.

### Compliant: Keychain credential storage

```swift
import Security

/// Stores a credential securely in the iOS Keychain.
/// Compliance: OWASP M1 (Improper Credential Usage), MASVS-STORAGE-1
/// Test cases: MASTG-TEST-0213, MASTG-TEST-0299
/// iOS 8.0+ (SecAccessControlCreateWithFlags), iOS 11.3+ (.biometryCurrentSet)
func storeCredential(account: String, secret: Data, service: String) throws {
    // ✅ CORRECT — secrets are persisted in Keychain with explicit access control
    // Delete existing item first to avoid errSecDuplicateItem
    let deleteQuery: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service
    ]
    SecItemDelete(deleteQuery as CFDictionary)

    var error: Unmanaged<CFError>?
    guard let accessControl = SecAccessControlCreateWithFlags(
        kCFAllocatorDefault,
        kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
        .biometryCurrentSet,
        &error
    ) else {
        throw error!.takeRetainedValue() as Error
    }

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service,
        kSecAttrAccessControl as String: accessControl,
        kSecValueData as String: secret
    ]

    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else {
        throw NSError(domain: NSOSStatusErrorDomain, code: Int(status))
    }
}
```

### Anti-pattern: common AI-generated credential storage

```swift
// ❌ WRONG — UserDefaults writes to UNENCRYPTED plist at:
//   <AppSandbox>/Library/Preferences/<BundleID>.plist
// Extractable via iTunes backup, iMazing, or objection
UserDefaults.standard.set(apiToken, forKey: "auth_token")

// ❌ WRONG — Hardcoded API key in source
let stripeKey = "sk_live_<redacted>"

// ❌ WRONG — Secret in Info.plist (plaintext in IPA archive)
// <key>API_SECRET</key><string>my-secret-key-12345</string>

// ❌ WRONG — NSKeyedArchiver to Documents directory (no encryption)
let data = try NSKeyedArchiver.archivedData(
    withRootObject: credentials, requiringSecureCoding: true)
try data.write(to: documentsURL.appendingPathComponent("creds.dat"))
```

**Why these fail audits:** objection `ios nsuserdefaults get` reveals UserDefaults instantly. MobSF flags hardcoded key patterns. Backup extraction exposes Documents directory. All fail MASTG-TEST-0213 and MASTG-TEST-0302.

---

## M3 — Insecure Authentication/Authorization

**Scope:** Merges 2016 M4 + M6. Covers remote server-side auth, local biometric auth, and client-only authorization. Attack vectors: EASY. Impact: SEVERE. Critical iOS risk: LAContext-only biometric auth is bypassable via Frida in under 10 seconds.

### MASTG Test Cases

| Test ID         | Legacy ID   | Verifies                                                      | Profile |
| --------------- | ----------- | ------------------------------------------------------------- | ------- |
| MASTG-TEST-0266 | MSTG-AUTH-8 | Static: references to `LAContext.evaluatePolicy`              | L2      |
| MASTG-TEST-0267 | MSTG-AUTH-8 | Dynamic: runtime event-based biometric auth (bypassable)      | L2      |
| MASTG-TEST-0268 | MSTG-AUTH-8 | Static: APIs allowing fallback to non-biometric auth          | L2      |
| MASTG-TEST-0269 | MSTG-AUTH-8 | Dynamic: runtime fallback to non-biometric auth               | L2      |
| MASTG-TEST-0270 | MSTG-AUTH-8 | Static: `.biometryCurrentSet` for enrollment change detection | L2      |
| MASTG-TEST-0271 | MSTG-AUTH-8 | Dynamic: enrollment change detection enforced at runtime      | L2      |

### The LAContext Vulnerability

`LAContext.evaluatePolicy` performs a software-only biometric check returning a Boolean in the completion handler. This Boolean executes in user space and is hookable by Frida to always return `true`. The Secure Enclave performs the biometric match, but the result is a plain callback with no cryptographic proof of authentication.

**Frida bypass (< 10 lines):**

```javascript
// Forces LAContext.evaluatePolicy to always succeed
if (ObjC.available) {
  var hook = ObjC.classes.LAContext["- evaluatePolicy:localizedReason:reply:"];
  Interceptor.attach(hook.implementation, {
    onEnter: function (args) {
      var block = new ObjC.Block(args[4]);
      const appCallback = block.implementation;
      block.implementation = function (error, value) {
        return appCallback(1, null); // Force success=true
      };
    },
  });
}
```

**objection one-liner:** `ios ui biometrics_bypass` — hooks `evaluatePolicy` to return `true`.

The correct pattern ties secrets to Keychain items protected by `SecAccessControlCreateWithFlags`. The Secure Enclave holds the decryption key and will not release it without valid biometric authentication. There is no Boolean to hook — failed biometrics means the data is cryptographically inaccessible.

### `.biometryCurrentSet` vs `.biometryAny`

| Flag                  | Behavior                                              | Security                                             | iOS   |
| --------------------- | ----------------------------------------------------- | ---------------------------------------------------- | ----- |
| `.biometryCurrentSet` | Item invalidated if new biometric enrolled            | **Recommended** — prevents enrollment-change attacks | 11.3+ |
| `.biometryAny`        | Accessible with any enrolled biometric, even new ones | Lower — attacker can add their own fingerprint       | 11.3+ |
| `.userPresence`       | Biometry OR passcode (system chooses)                 | Allows passcode fallback                             | 8.0+  |
| `.devicePasscode`     | Passcode only                                         | No biometric option                                  | 9.0+  |

For high-security items, always use `.biometryCurrentSet`. If an attacker adds their fingerprint to a stolen device, `.biometryAny` items become accessible; `.biometryCurrentSet` items are permanently invalidated. See `biometric-authentication.md` for full implementation patterns.

### Compliant: hardware-bound biometric authentication

```swift
import LocalAuthentication
import Security

/// Hardware-bound biometric auth using Keychain + Secure Enclave.
/// Compliance: OWASP M3 (Insecure Auth), MASVS-AUTH-2
/// Test cases: MASTG-TEST-0266, MASTG-TEST-0270
/// iOS 11.3+ (.biometryCurrentSet)
/// Canonical pattern with full error handling: biometric-authentication.md § The Secure Pattern — Hardware-Bound Secrets

// STEP 1: Store secret with biometric protection
func storeBiometricProtectedSecret(account: String, secret: Data) throws {
    // ✅ CORRECT — Secure Enclave gates secret release through keychain ACLs
    var error: Unmanaged<CFError>?
    guard let accessControl = SecAccessControlCreateWithFlags(
        kCFAllocatorDefault,
        kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
        .biometryCurrentSet,
        &error
    ) else {
        throw error!.takeRetainedValue() as Error
    }

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: "com.app.biometric-auth",
        kSecAttrAccessControl as String: accessControl,
        kSecValueData as String: secret
    ]

    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else {
        throw NSError(domain: NSOSStatusErrorDomain, code: Int(status))
    }
}

// STEP 2: Retrieve — Secure Enclave enforces biometric check
func retrieveBiometricProtectedSecret(account: String) throws -> Data? {
    let context = LAContext()
    context.localizedReason = "Authenticate to access your account"

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: "com.app.biometric-auth",
        kSecUseAuthenticationContext as String: context,
        kSecReturnData as String: true
    ]

    var result: AnyObject?
    let status = SecItemCopyMatching(query as CFDictionary, &result)
    guard status == errSecSuccess else { return nil }
    return result as? Data
}
```

### Anti-pattern: LAContext-only authentication

```swift
// ❌ WRONG — #2 most common iOS audit finding
// Bypassable: objection -g com.app explore -> ios ui biometrics_bypass
let context = LAContext()
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics,
                       localizedReason: "Log in") { success, error in
    if success {
        // ❌ This Boolean is hookable — no cryptographic proof
        self.showMainScreen()  // Attacker gains full access
    }
}
```

---

## M9 — Insecure Data Storage

**Scope:** All vulnerabilities in how apps store sensitive data: weak/no encryption, accessible locations, insufficient access controls, unintentional leakage (logs, caches, backups). Was M2 in 2016 — renumbered to M9 (priority shift, not diminished importance).

### iOS Storage Security Properties

| Storage Location                           | Encrypted          | In Backups     | Accessible w/o Jailbreak | Verdict                         |
| ------------------------------------------ | ------------------ | -------------- | ------------------------ | ------------------------------- |
| Keychain (`WhenPasscodeSetThisDeviceOnly`) | ✅ AES-256-GCM     | ❌             | ❌                       | ✅ Use for secrets              |
| Keychain (`AfterFirstUnlock`)              | ✅                 | ✅ (encrypted) | ❌                       | ⚠️ Acceptable for L1            |
| `NSFileProtectionComplete` files           | ✅ (when locked)   | ✅             | ❌                       | ✅ Use for sensitive files      |
| UserDefaults                               | ❌ Plaintext plist | ✅             | ✅ (via backup)          | ❌ Never for secrets            |
| Documents/ (default protection)            | ✅ (Class C)       | ✅             | ✅ (via backup)          | ❌ Not without extra encryption |
| SQLite/CoreData (no SQLCipher)             | ❌                 | ✅             | ✅ (via backup)          | ❌ Not for secrets              |
| NSLog output                               | ❌                 | N/A            | ✅ (Console.app)         | ❌ Never log secrets            |

**Keychain persistence note:** Keychain items survive app uninstall and persist across install/uninstall cycles (confirmed since iOS 10.3). Only factory reset clears them. Exception: `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` items are deleted when the passcode is removed.

### MASTG Test Cases

| Test ID         | Legacy ID      | Verifies                                          | Profile |
| --------------- | -------------- | ------------------------------------------------- | ------- |
| MASTG-TEST-0299 | MSTG-STORAGE-1 | Data Protection classes for private storage files | L1      |
| MASTG-TEST-0300 | MSTG-STORAGE-1 | Static: references to unencrypted storage APIs    | L2      |
| MASTG-TEST-0301 | MSTG-STORAGE-1 | Dynamic: runtime use of unencrypted storage       | L2      |
| MASTG-TEST-0302 | MSTG-STORAGE-2 | Sensitive data unencrypted in private storage     | L2      |
| MASTG-TEST-0296 | MSTG-STORAGE-3 | Sensitive data in logs                            | L1, L2  |
| MASTG-TEST-0297 | MSTG-STORAGE-3 | Insertion of sensitive data into log statements   | L1, L2  |
| MASTG-TEST-0215 | MSTG-STORAGE-8 | Sensitive data not excluded from backup           | L1, L2  |
| MASTG-TEST-0313 | MSTG-STORAGE-5 | APIs preventing keyboard caching                  | L1, L2  |

### NSFileProtection Classes

| Class               | Constant                                               | Accessible When                                   | Default? |
| ------------------- | ------------------------------------------------------ | ------------------------------------------------- | -------- |
| A: Complete         | `NSFileProtectionComplete`                             | Only when unlocked; key discarded ~10s after lock | No       |
| B: Unless Open      | `NSFileProtectionCompleteUnlessOpen`                   | Already-open files remain accessible when locked  | No       |
| C: Until First Auth | `NSFileProtectionCompleteUntilFirstUserAuthentication` | After first unlock, even when locked              | **Yes**  |
| D: None             | `NSFileProtectionNone`                                 | Always; protected only by device UID              | No       |

### Compliant: file storage with Data Protection

```swift
import Foundation

/// Writes sensitive data with Complete file protection.
/// Compliance: OWASP M9 (Insecure Data Storage), MASVS-STORAGE-1
/// Test cases: MASTG-TEST-0299
/// iOS 9.0+ (.completeFileProtection option)
func writeProtectedFile(data: Data, to url: URL) throws {
    try data.write(to: url, options: [.atomic, .completeFileProtection])
}

/// Excludes a file from device backups.
/// Compliance: MASVS-STORAGE-2, MASTG-TEST-0215
/// iOS 5.1+
func excludeFromBackup(url: URL) throws {
    var resourceURL = url
    var resourceValues = URLResourceValues()
    resourceValues.isExcludedFromBackup = true
    try resourceURL.setResourceValues(resourceValues)
}
```

### Anti-pattern: insecure data storage

```swift
// ❌ WRONG — Unencrypted plist
UserDefaults.standard.set("Bearer eyJhbGciOiJSUzI1NiIs...", forKey: "authToken")

// ❌ WRONG — Default file protection (Class C) for sensitive file
try sensitiveData.write(to: documentsURL.appendingPathComponent("profile.dat"))

// ❌ WRONG — Logging sensitive data (Console.app / idevicesyslog)
NSLog("User token: %@", authToken)
print("Password entered: \(password)")

// ❌ WRONG — Not excluding sensitive files from backup
// Files in Documents/ are in iTunes/Finder backups by default
// Extractable with iMazing on non-jailbroken devices
```

---

## kSecAttrAccessible Selection Guide

> Complete selection criteria and data protection tier mapping: `keychain-access-control.md` § The "When" Layer: Seven Accessibility Constants. The guidance below is a compliance-focused quick-reference for audit contexts.

Keychain accessibility is the single most important iOS security decision — it simultaneously addresses M1, M3, M9, and M10 requirements.

| Constant                                           | Backup | iCloud | Passcode Required       | Use For                                               |
| -------------------------------------------------- | ------ | ------ | ----------------------- | ----------------------------------------------------- |
| `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`  | ❌     | ❌     | ✅ (deleted if removed) | **Highest-sensitivity: auth tokens, encryption keys** |
| `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`     | ❌     | ❌     | ❌                      | Sensitive data, device-specific                       |
| `kSecAttrAccessibleWhenUnlocked` (default)         | ✅     | ✅     | ❌                      | General credentials needing sync                      |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | ❌     | ❌     | ❌                      | Background-accessible, device-specific                |
| `kSecAttrAccessibleAfterFirstUnlock`               | ✅     | ✅     | ❌                      | Background tasks (e.g., push notification keys)       |
| `kSecAttrAccessibleAlways`                         | ✅     | ✅     | ❌                      | **❌ DEPRECATED (iOS 12) — never use**                |

**Critical:** `kSecAttrAccessible` and `kSecAttrAccessControl` are mutually exclusive. When using `SecAccessControlCreateWithFlags`, pass the accessibility level as its `protection` argument — do not also set `kSecAttrAccessible` in the query dictionary, or you get `errSecParam (-50)`. See `keychain-access-control.md`.

> **Choosing a device-only default:** `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` and `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` are both valid. The `WhenPasscodeSet` variant is strictly more secure (items are deleted if passcode is removed) but may surprise users. Choose based on threat model: `WhenPasscodeSet` for high-security credentials, `WhenUnlocked` for general sensitive data.

---

## Enterprise Audit Workflow

### How Security Teams Evaluate iOS Apps

Auditors evaluate against MAS Testing Profiles: **L1 (standard)** for low-risk apps, **L2 (defense-in-depth)** for apps handling financial, health, or highly sensitive data — requiring Keychain-managed encryption, hardware-bound biometrics, and certificate pinning.

**Audit tool workflow:** (1) Static analysis — MobSF for automated scanning; radare2 for targeted API analysis. (2) Dynamic analysis — objection for keychain dumping (`ios keychain dump`), file protection verification, UserDefaults inspection (`ios nsuserdefaults get`), biometric bypass (`ios ui biometrics_bypass`). (3) Network — Burp Suite with objection SSL pinning bypass. (4) Binary — class-dump/dsdump for method enumeration.

**Key filesystem paths auditors target:** `<Sandbox>/Library/Preferences/<BundleID>.plist` (UserDefaults), `<Sandbox>/Documents/` (databases), `<Sandbox>/Library/Caches/` (web cache), `<Sandbox>/Library/SplashBoard/Snapshots/` (screenshot cache), `<Sandbox>/tmp/` (temporary files with uncleared data).

### Audit Findings

| Finding                         | OWASP  | MASVS        | MASTG Tests | Severity |
| ------------------------------- | ------ | ------------ | ----------- | -------- |
| Secrets in UserDefaults/plists  | M1, M9 | STORAGE-1    | 0299, 0302  | Critical |
| LAContext-only biometric auth   | M3     | AUTH-2       | 0266, 0267  | High     |
| Missing certificate pinning     | M5     | NETWORK-2    | 0244        | High     |
| Hardcoded API keys in binary    | M1     | CRYPTO-2     | 0213, 0214  | Critical |
| Insecure keychain accessibility | M9     | STORAGE-1    | 0299        | Medium   |
| Sensitive data in logs          | M9     | STORAGE-2    | 0296, 0297  | Medium   |
| Missing jailbreak detection     | M7     | RESILIENCE-1 | —           | Low      |
| Unencrypted SQLite/Realm        | M9     | STORAGE-1    | 0302        | High     |
| ATS exceptions allowing HTTP    | M5     | NETWORK-1    | —           | Medium   |


### Evidence Kit (5 Artifacts)

| Artifact               | Proves                                        | OWASP/MASVS |
| ---------------------- | --------------------------------------------- | ----------- |
| Static analysis report | No hardcoded secrets                          | M1          |
| Filesystem/xattr log   | `NSFileProtectionComplete` applied            | M9          |
| Keychain dump          | `ThisDeviceOnly` + `SecAccessControl` present | M1, M9      |
| Backup extraction      | No sensitive data migrated                    | M9          |
| Code snippets          | Correct APIs and flags used                   | All         |

### Jailbreak-Era Testing (2025–2026)

Public jailbreaks usually lag the current iOS release, so a jailbroken test device is often unavailable. Auditors use non-jailbreak techniques: objection with Frida Gadget injection into repackaged IPAs, Corellium virtual devices, or iMazing for backup extraction. This makes automated static analysis (MobSF, semgrep) and Frida Gadget–based dynamic testing the primary assessment paths.

---

## Cross-Reference Index

| iOS Practice                                              | M1  | M3  | M9  | M10              | Primary Reference                |
| --------------------------------------------------------- | --- | --- | --- | ---------------- | -------------------------------- |
| Keychain + `WhenPasscodeSetThisDeviceOnly`                | ✅  | —   | ✅  | ✅ (key storage) | `keychain-access-control.md`     |
| `SecAccessControlCreateWithFlags` + `.biometryCurrentSet` | ✅  | ✅  | ✅  | —                | `biometric-authentication.md`    |
| `NSFileProtectionComplete`                                | —   | —   | ✅  | —                | `keychain-access-control.md`     |
| App Attest for credential provisioning                    | ✅  | ✅  | —   | —                | `credential-storage-patterns.md` |

---

## Conclusion

Three patterns emerge from this mapping. First, the Keychain is the universal compliance mechanism on iOS — a single correctly configured `SecItemAdd` with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` and `.biometryCurrentSet` simultaneously satisfies M1, M3, and M9. Second, any reference to "M2: Insecure Data Storage" or "M5: Insufficient Cryptography" flags outdated 2016 guidance. Third, the MASTG transition to new test IDs (MASTG-TEST-02xx/03xx) means legacy MSTG-\* references in code comments should be updated.

---

## Summary Checklist

1. **OWASP 2024 numbering** — All references use 2024 numbering (M1/M3/M9/M10), not 2016 (M2/M5/M4+M6)
1. **MASTG test IDs** — References use new MASTG-TEST-02xx/03xx IDs (not legacy MSTG-\* only)
1. **Keychain-only credential storage** — Credentials stored in Keychain with `ThisDeviceOnly` accessibility, never in UserDefaults/plists/files
1. **Keychain-bound biometrics** — Authentication uses `SecAccessControlCreateWithFlags` + `.biometryCurrentSet`, not LAContext-only
1. **No dual access control** — `kSecAttrAccessible` and `kSecAttrAccessControl` are never set simultaneously in the same query
1. **File protection** — Sensitive files use `NSFileProtectionComplete` and are excluded from backup via `isExcludedFromBackup`
1. **No sensitive logging** — No sensitive data appears in `NSLog`/`print` statements or keyboard caches (`.autocorrectionType = .no`, `.isSecureTextEntry = true`)
1. **Compliance annotations** — Code comments include OWASP category, MASVS control, and MASTG test case IDs
