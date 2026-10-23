# Common Anti-Patterns

> **Scope:** Keychain storage, access-control, credential, and logging anti-patterns in iOS apps. Each entry includes the vulnerability explanation, realistic ❌ insecure code, ✅ correct replacement, detection heuristic, and OWASP risk mapping. This is the skill's backbone — the single most important file for correcting AI-generated security code.
>
> **Cross-references:** `biometric-authentication.md` (anti-pattern #3 deep dive), `keychain-fundamentals.md` (anti-pattern #4 CRUD patterns), `keychain-access-control.md` (anti-pattern #5 protection classes), `credential-storage-patterns.md` (anti-patterns #1–2 token lifecycle), `migration-legacy-stores.md` (anti-pattern #7 first-launch cleanup), `compliance-owasp-mapping.md` (full OWASP/MASVS mapping).

---

## Why AI Generates Insecure iOS Code

AI assistants optimize for functional correctness, not security, and tend to reproduce the most common patterns in their training data, many of which are insecure by default. Hardcoded secrets and plaintext credential storage remain recurring findings in scans of shipped iOS apps, so review generated security code line by line instead of trusting that it compiles and runs.

Apple's security primitives (Keychain, CryptoKit, Secure Enclave) are excellent but AI consistently bypasses them. CISA/FBI classified hardcoded credentials as elevating "risk to national security" in their January 2025 Bad Practices v2.0 (CWE-798).

**OWASP standard:** Mobile Top 10 (2024) with MASTG v2 test IDs. Legacy MSTG-\* identifiers noted where commonly referenced.

---

## Anti-Pattern #1 — Storing Secrets in UserDefaults

**Severity:** CRITICAL | **OWASP:** M9 (Insecure Data Storage) | **Fix effort:** Medium

UserDefaults writes to an unencrypted XML plist at `~/Library/Preferences/{BUNDLE_ID}.plist`. Apple's documentation: "Don't store personal or sensitive information as settings." Readable from unencrypted backups, jailbroken devices (Objection `ios nsuserdefaults get`), and third-party SDKs. **SwiftUI's `@AppStorage` is a wrapper over `UserDefaults`** — it has identical security properties and must never be used for tokens, keys, or credentials.

**❌ Insecure — AI-generated pattern:**

```swift
// Plaintext on disk, readable from backups
func saveAuthToken(_ token: String) {
    UserDefaults.standard.set(token, forKey: "userAuthToken")
    UserDefaults.standard.set(refreshToken, forKey: "refreshToken")
    UserDefaults.standard.synchronize()
}

let token = UserDefaults.standard.string(forKey: "userAuthToken")
```

**✅ Secure — Keychain with add-or-update:**

```swift
func saveTokenToKeychain(_ token: Data, account: String) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.myapp.auth",
        kSecAttrAccount as String: account,
        kSecValueData as String: token,
        kSecAttrAccessible as String:
            kSecAttrAccessibleWhenUnlockedThisDeviceOnly
    ]
    let status = SecItemAdd(query as CFDictionary, nil)
    if status == errSecDuplicateItem {
        // Full add-or-update pattern → see anti-pattern #4
        let search: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: "com.myapp.auth",
            kSecAttrAccount as String: account
        ]
        let updateStatus = SecItemUpdate(
            search as CFDictionary,
            [kSecValueData as String: token] as CFDictionary)
        guard updateStatus == errSecSuccess else {
            throw KeychainError.unexpectedStatus(updateStatus)
        }
    } else if status != errSecSuccess {
        throw KeychainError.unexpectedStatus(status)
    }
}
```

**MASTG tests:** MASTG-TEST-0300, MASTG-TEST-0302. **MASWE:** MASWE-0006. **Legacy:** MSTG-STORAGE-1.

**Detection heuristic:**

```bash
grep -rn "UserDefaults" --include="*.swift" | \
  grep -iE "token|password|secret|credential|auth|session|api.?key|jwt|bearer"
```

---

## Anti-Pattern #2 — Hardcoded API Keys

**Severity:** CRITICAL | **OWASP:** M1 (Improper Credential Usage) | **Fix effort:** High

API keys compiled into Swift appear in the binary's `__TEXT.__cstring` segment — `strings MyApp.app/MyApp` extracts them instantly. Even `.xcconfig` or `Info.plist` values ship inside the IPA. Cybernews found 78,800 Google API keys across 156,000 iOS apps.

**❌ Insecure — AI-generated pattern:**

```swift
class PaymentService {
    private let stripeKey = "sk_live_51H7bK2E..."   // In binary
    private let firebaseKey = "AIzaSyB..."            // In binary

    func charge(amount: Int) async throws {
        var request = URLRequest(
            url: URL(string: "https://api.stripe.com/v1/charges")!)
        request.setValue("Bearer \(stripeKey)",
                        forHTTPHeaderField: "Authorization")
        let (data, _) = try await URLSession.shared.data(for: request)
    }
}

// Also dangerous: key in Info.plist or .xcconfig bundled in app
let key = Bundle.main.infoDictionary?["API_KEY"] as? String
```

**✅ Secure — server proxy + Keychain cache:**

```swift
class SecureAPIKeyManager {
    static let shared = SecureAPIKeyManager()

    /// Best: proxy through your server (key never on device)
    func secureRequest(endpoint: String, params: [String: Any]) async throws -> Data {
        var request = URLRequest(
            url: URL(string: "https://api.myserver.com/proxy/\(endpoint)")!)
        request.httpMethod = "POST"
        request.httpBody = try JSONSerialization.data(withJSONObject: params)
        let (data, _) = try await URLSession.shared.data(for: request)
        return data
    }

    /// If client must hold key: fetch at runtime, cache in Keychain
    func getAPIKey() async throws -> String {
        if let cached = try? readFromKeychain(service: "api-keys", account: "primary") {
            return String(data: cached, encoding: .utf8)!
        }
        let (data, _) = try await URLSession.shared.data(
            from: URL(string: "https://api.myserver.com/config/key")!)
        try saveToKeychain(data, service: "api-keys", account: "primary")
        return String(data: data, encoding: .utf8)!
    }
}
```

Apple's DeviceCheck and App Attest frameworks provide server-side device verification without embedding secrets. WWDC 2019-709 advises storing credentials in Keychain, not in code.

**MASTG tests:** MASTG-TEST-0213, MASTG-TEST-0214. **MASWE:** MASWE-0005. **Legacy:** MSTG-STORAGE-12. **CISA/FBI:** CWE-798 — Product Security Bad Practices v2.0 (January 2025).

**Detection heuristic:**

```bash
grep -rn 'let.*[Kk]ey.*=.*"[A-Za-z0-9_\-]\{20,\}"' --include="*.swift"
grep -rn '"sk_live_\|"pk_live_\|"AIza[A-Za-z0-9]\|"AKIA[A-Z0-9]' \
  --include="*.swift" --include="*.plist" --include="*.xcconfig"
```

---

## Anti-Pattern #3 — LAContext-Only Biometric Authentication

**Severity:** CRITICAL | **OWASP:** M3 (Insecure Authentication) | **Fix effort:** Medium

Using `LAContext.evaluatePolicy()` alone is the single most reproduced insecure pattern across iOS tutorials. The method returns a simple boolean callback in user-space — no cryptographic binding. Frida forces `success = true` in one command; Objection packages this as `ios ui biometrics_bypass`. OWASP MASTG: "Biometric authentication must be based on unlocking the keychain." Full deep dive: see `biometric-authentication.md`.

**❌ Insecure — AI-generated pattern:**

```swift
func authenticateUser(completion: @escaping (Bool) -> Void) {
    let context = LAContext()
    context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: "Authenticate to access your account"
    ) { success, authError in
        DispatchQueue.main.async {
            if success {
                self.showSensitiveData()  // Gated on a hookable boolean
            }
            completion(success)
        }
    }
}
```

**✅ Secure — Keychain + SecAccessControl hardware binding:**

```swift
// STORE: biometric-protected via Secure Enclave
func storeWithBiometric(secret: Data, account: String) throws {
    let access = SecAccessControlCreateWithFlags(
        nil,
        kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
        .biometryCurrentSet, nil)!

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.myapp.biometric",
        kSecAttrAccount as String: account,
        kSecAttrAccessControl as String: access,
        kSecValueData as String: secret
    ]
    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess || status == errSecDuplicateItem else {
        throw KeychainError.unexpectedStatus(status)
    }
}

// READ: Secure Enclave enforces biometric before releasing data
func readWithBiometric(account: String) throws -> Data {
    let context = LAContext()
    context.localizedReason = "Access your secure data"
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.myapp.biometric",
        kSecAttrAccount as String: account,
        kSecReturnData as String: true,
        kSecMatchLimit as String: kSecMatchLimitOne,
        kSecUseAuthenticationContext as String: context
    ]
    var result: AnyObject?
    let status = SecItemCopyMatching(query as CFDictionary, &result)
    guard status == errSecSuccess, let data = result as? Data else {
        throw KeychainError.unexpectedStatus(status)
    }
    return data  // Only returned after hardware biometric validation
}
```

The `.biometryCurrentSet` flag invalidates the item if biometrics change, preventing an attacker with physical access from enrolling their own biometric. Objection's documentation confirms this bypass "will NOT work" with keychain-bound biometric items.

**MASTG tests:** MASTG-TEST-0266, MASTG-TEST-0267. **MASWE:** MASWE-0044. **Legacy:** MSTG-AUTH-8. **WWDC:** 2014-711 introduced `SecAccessControlCreateWithFlags`.

**Detection heuristic:**

```bash
# evaluatePolicy without SecAccessControl → insecure
grep -rn "evaluatePolicy" --include="*.swift" -l | \
  xargs grep -L "SecAccessControlCreateWithFlags"
# Verify secure pattern exists
grep -rn "\.biometryCurrentSet\|\.biometryAny" --include="*.swift"
```

---

## Anti-Pattern #4 — Ignoring SecItem Error Codes

**Severity:** HIGH | **OWASP:** M8 (Security Misconfiguration) | **Fix effort:** Low

`errSecDuplicateItem` (OSStatus -25299) is the most common Keychain failure. When `SecItemAdd` hits a duplicate, it silently discards the new value. Password updates never persist, refreshed tokens are lost, and auth breaks in hard-to-debug ways. Other critical codes: `errSecItemNotFound` (-25300), `errSecAuthFailed` (-25293), `errSecInteractionNotAllowed` (-25308).

Full CRUD patterns: see `keychain-fundamentals.md`.

**❌ Insecure — AI-generated pattern:**

```swift
func saveToken(_ token: Data) {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.app.auth",
        kSecAttrAccount as String: "accessToken",
        kSecValueData as String: token
    ]
    SecItemAdd(query as CFDictionary, nil)  // Return value ignored!
}
```

**✅ Secure — OSStatus switch with add-or-update:**

```swift
func saveToKeychain(value: Data, service: String, account: String) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: service,
        kSecAttrAccount as String: account,
        kSecValueData as String: value,
        kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
    ]
    let status = SecItemAdd(query as CFDictionary, nil)
    switch status {
    case errSecSuccess: return
    case errSecDuplicateItem:
        let search: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]
        let updateStatus = SecItemUpdate(
            search as CFDictionary, [kSecValueData as String: value] as CFDictionary)
        guard updateStatus == errSecSuccess else { throw KeychainError.updateFailed(updateStatus) }
    case errSecInteractionNotAllowed: throw KeychainError.deviceLocked
    case errSecAuthFailed: throw KeychainError.authenticationFailed
    default: throw KeychainError.unexpectedStatus(status)
    }
}
```

Critical detail: `SecItemUpdate` takes two dictionaries — search query (without `kSecValueData`) and attributes to update. Passing the full query as the search parameter is a common mistake.

**MASTG tests:** MASTG-TEST-0300, MASTG-TEST-0301. **Legacy:** MASVS-STORAGE-2.

**Detection heuristic:**

```bash
grep -rn "SecItemAdd" --include="*.swift" -l | \
  xargs grep -L "errSecDuplicateItem\|DuplicateItem\|-25299"
grep -rn "SecItemAdd(" --include="*.swift" | \
  grep -v "let\|var\|status\|=\|switch\|if\|guard"
```

---

## Anti-Pattern #5 — Wrong or Missing Data Protection Class

**Severity:** HIGH | **OWASP:** M9 (Insecure Data Storage) | **Fix effort:** Low

Omitting `kSecAttrAccessible` inherits a default that may be insufficient. Using deprecated `kSecAttrAccessibleAlways` (deprecated iOS 12) leaves data decryptable on a locked device. Missing `ThisDeviceOnly` suffix means items are included in backups. Full protection class guide: see `keychain-access-control.md`.

**❌ Insecure — AI-generated patterns:**

```swift
// Missing kSecAttrAccessible entirely
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "user_password",
    kSecValueData as String: passwordData
]
SecItemAdd(query as CFDictionary, nil)

// Deprecated — accessible when device is locked
kSecAttrAccessible as String: kSecAttrAccessibleAlways
```

**✅ Secure — selection by use case:**

```swift
// Passwords, auth tokens (foreground-only)
kSecAttrAccessible as String:
    kSecAttrAccessibleWhenUnlockedThisDeviceOnly

// Highest sensitivity — requires passcode to exist
kSecAttrAccessible as String:
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly

// Background-access items (push tokens, refresh tokens)
kSecAttrAccessible as String:
    kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
```

WWDC 2014-711: "Always use the most restrictive option that makes sense for your app."

**MASTG test:** MASTG-TEST-0299. **Legacy:** MASTG-STORAGE-3.

**Detection heuristic:**

```bash
grep -rn "kSecAttrAccessibleAlways\b" --include="*.swift"
grep -rn "SecItemAdd" --include="*.swift" -l | \
  xargs grep -L "kSecAttrAccessible\|kSecAttrAccessControl"
grep -rn "kSecAttrAccessibleWhenUnlocked\b" --include="*.swift" | \
  grep -v "ThisDeviceOnly"
```

---

## Anti-Pattern #6 — Logging Sensitive Data

**Severity:** HIGH | **OWASP:** M9 (Insecure Data Storage) | **Fix effort:** Low

`print()`, `NSLog()`, and `os_log()` with sensitive values persist in device logs — accessible via Xcode Console, `idevicesyslog`, and `log collect --device`. On jailbroken devices, any process reads log storage. Apple's `OSLogPrivacy` (iOS 14+): `.private` redacts in production; `.sensitive` (iOS 15+) always redacted.

**❌ Insecure — AI-generated pattern:**

```swift
func login(username: String, password: String) async throws {
    print("Logging in with password: \(password)")       // In device logs!
    let token = try await authService.authenticate(username, password)
    print("Got auth token: \(token)")                     // In device logs!
    os_log("API key loaded: %{public}@", apiKey)          // Explicitly public!
}
```

**✅ Secure — OSLogPrivacy with redaction:**

```swift
import os

let logger = Logger(subsystem: Bundle.main.bundleIdentifier!, category: "auth")

func login(username: String, password: String) async throws {
    // Log events, not values — .private(mask: .hash) enables correlation
    logger.info("Login attempt: \(username, privacy: .private(mask: .hash))")
    let token = try await authService.authenticate(username, password)
    logger.info("Authentication succeeded")  // No token value
}

// Legacy os_log
os_log("Account: %{private}@", log: .default, type: .info, accountNumber)

// Strip debug logging in release builds
#if DEBUG
print("Debug: \(sensitiveValue)")
#endif
```

**MASTG tests:** MASTG-TEST-0296, MASTG-TEST-0297. **MASWE:** MASWE-0001. **Legacy:** MSTG-STORAGE-3.

**Detection heuristic:**

```bash
grep -rn "print(.*\\\(" --include="*.swift" | \
  grep -iE "password|token|secret|key|credential|ssn|credit"
grep -rn "NSLog(.*%@" --include="*.swift" --include="*.m" | \
  grep -iE "password|token|secret|key"
grep -rn 'os_log.*%{public}' --include="*.swift" | \
  grep -iE "password|token|secret|key"
```

---

## Anti-Pattern #7 — Not Clearing Keychain on First Launch

**Severity:** MEDIUM | **OWASP:** M9 (Insecure Data Storage) | **Fix effort:** Low

Keychain items persist in a system-wide encrypted database managed by `securityd`, outside the app sandbox. App deletion removes the sandbox but keychain items survive. Apple DTS engineer Quinn "The Eskimo!" confirmed this as "currently expected behaviour despite being an obvious privacy concern." Consequences: stale credentials on reinstall, cross-user data leakage on device resale, and Firebase SDK authentication errors on reinstall. Full migration patterns: see `migration-legacy-stores.md`.

**❌ The missing pattern — AI never generates this:**

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
    }
    // Stale keychain items from previous install persist silently
}
```

**✅ Secure — first-launch keychain cleanup:**

```swift
@main
struct MyApp: App {
    init() { clearKeychainIfFirstLaunch() }

    var body: some Scene {
        WindowGroup { ContentView() }
    }

    private func clearKeychainIfFirstLaunch() {
        let defaults = UserDefaults.standard
        guard !defaults.bool(forKey: "hasLaunchedBefore") else { return }

        // UserDefaults was cleared on uninstall → this is first launch
        for secClass in [kSecClassGenericPassword, kSecClassInternetPassword,
                         kSecClassCertificate, kSecClassKey, kSecClassIdentity] {
            SecItemDelete([
                kSecClass: secClass,
                kSecAttrSynchronizable: kSecAttrSynchronizableAny
            ] as NSDictionary)
        }
        defaults.set(true, forKey: "hasLaunchedBefore")
    }
}
```

Place this before initializing any SDKs (Firebase, analytics) that read from Keychain. Including `kSecAttrSynchronizableAny` ensures iCloud Keychain items are also cleared.

**MASTG tests:** MASTG-TEST-0300, MASTG-TEST-0301. **Legacy:** MSTG-STORAGE-11.

**Detection heuristic:**

```bash
grep -rn "SecItemAdd\|SecItemCopyMatching" --include="*.swift" -l | \
  xargs grep -L "hasLaunchedBefore\|isFirstLaunch\|firstRun"
grep -rn "SecItemDelete" --include="*.swift" -l | \
  xargs grep "hasLaunchedBefore\|isFirstLaunch"
```

---

## Quick Reference Matrix

| #   | Anti-Pattern             | OWASP 2024 | MASTG Test      | Dangerous API              | Secure API                          | Fix Effort |
| --- | ------------------------ | ---------- | --------------- | -------------------------- | ----------------------------------- | ---------- |
| 1   | UserDefaults secrets     | M9         | MASTG-TEST-0302 | `UserDefaults.set`         | `SecItemAdd` + Keychain             | Medium     |
| 2   | Hardcoded API keys       | M1         | MASTG-TEST-0213 | String literals            | Server proxy + Keychain cache       | High       |
| 3   | LAContext-only biometric | M3         | MASTG-TEST-0266 | `evaluatePolicy`           | `SecAccessControlCreateWithFlags`   | Medium     |
| 4   | Ignored SecItem errors   | M8         | MASTG-TEST-0300 | Unchecked `SecItemAdd`     | OSStatus switch + `SecItemUpdate`   | Low        |
| 5   | Wrong data protection    | M9         | MASTG-TEST-0299 | `kSecAttrAccessibleAlways` | `WhenUnlockedThisDeviceOnly`        | Low        |
| 6   | Logging sensitive data   | M9         | MASTG-TEST-0297 | `print(token)`             | `Logger` + `.private`               | Low        |
| 7   | No keychain cleanup      | M9         | MASTG-TEST-0300 | Missing cleanup            | UserDefaults flag + `SecItemDelete` | Low        |

---

## CI/CD Detection Strategy

**Semgrep** (pre-commit/PR gate): Fast structural pattern matching for `UserDefaults` misuse, missing `errSecDuplicateItem`, `LAContext` booleans. Limited data-flow analysis.

**CodeQL** (nightly/PR gate): Deep semantic taint tracking — catches tokens assigned to variables then logged. Slower execution.

**Binary scanning** (post-build): `strings`/`class-dump` on compiled binary catches hardcoded keys surviving source-level obfuscation.

Recommended: Semgrep on every PR + post-build binary scanning. CodeQL nightly for deep analysis.

---

## Summary Checklist

When reviewing iOS code for security anti-patterns, verify each item:

1. **No secrets in UserDefaults** — tokens, passwords, API keys, JWTs use Keychain with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` or stricter
1. **No hardcoded keys in source** — API keys fetched at runtime via server proxy or authenticated endpoint; no high-entropy string literals, no secrets in `.xcconfig` or `Info.plist`
1. **Biometrics bound to Keychain** — `evaluatePolicy` is never used alone to gate sensitive actions; `SecAccessControlCreateWithFlags` with `.biometryCurrentSet` protects keychain items
1. **All SecItem calls checked** — `SecItemAdd` handles `errSecDuplicateItem` with `SecItemUpdate` fallback; `SecItemCopyMatching` handles `errSecItemNotFound`; no discarded `OSStatus` return values
1. **Explicit data protection class** — every `SecItemAdd` includes `kSecAttrAccessible` or `kSecAttrAccessControl`; no `kSecAttrAccessibleAlways`; `ThisDeviceOnly` variants used for non-syncing items
1. **No sensitive data in logs** — `print()` and `NSLog()` never contain tokens, keys, or credentials; `os_log` uses `%{private}@`; `Logger` uses `.private` or `.private(mask: .hash)`
1. **First-launch keychain cleanup** — `UserDefaults` flag + `SecItemDelete` for all classes runs before SDK initialization at app startup
