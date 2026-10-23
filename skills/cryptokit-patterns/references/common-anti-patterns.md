# Common Anti-Patterns

> **Scope:** Cryptographic anti-patterns in algorithm selection, nonce handling, random generation, and key lifecycle. Each entry includes insecure code, a replacement, a detection heuristic, and an OWASP mapping.
>
> **Cross-references:** `cryptokit-symmetric.md` (symmetric crypto, hashing, and RNG), `cryptokit-public-key.md` (signing, key agreement, and post-quantum APIs), `compliance-owasp-mapping.md` (OWASP/MASVS mapping).

Review generated cryptographic code even when it compiles and passes a round-trip test. Correct encryption does not establish safe nonce reuse, key provenance, or storage policy.

**OWASP standard:** Mobile Top 10 (2024) with MASTG test IDs. Legacy MSTG identifiers are included for audit cross-referencing.

---

## Anti-Pattern #1 — Nonce Reuse in AES-GCM

**Severity:** CRITICAL | **OWASP:** M10 (Insufficient Cryptography) | **Fix effort:** Medium

Reusing a nonce with the same key in AES-GCM is a complete cryptographic break. Identical nonces produce identical keystreams, enabling plaintext recovery via `C1 ⊕ C2 = P1 ⊕ P2` and authentication key recovery via polynomial factorization ("forbidden attack," Joux 2006). CryptoKit's `AES.GCM.seal` has a safe default: omitting the `nonce` parameter auto-generates a random 12-byte nonce. Danger occurs when AI explicitly constructs nonces. Full patterns: see `cryptokit-symmetric.md`.

**❌ Insecure — AI-generated patterns:**

```swift
import CryptoKit

// Hardcoded nonce — identical keystream every encryption
let fixedNonce = try! AES.GCM.Nonce(data: Data(repeating: 0x00, count: 12))

func encrypt(_ plaintext: Data, using key: SymmetricKey) throws -> Data {
    let sealedBox = try AES.GCM.seal(
        plaintext, using: key, nonce: fixedNonce)  // CATASTROPHIC
    return sealedBox.combined!
}
// Also dangerous: counter-based nonce that resets on app restart → collision
```

**✅ Secure — let CryptoKit handle nonces:**

```swift
import CryptoKit

func encrypt(_ plaintext: Data, using key: SymmetricKey) throws -> Data {
    // Nonce omitted → CryptoKit generates random 12-byte nonce
    let sealedBox = try AES.GCM.seal(plaintext, using: key)
    return sealedBox.combined!  // Contains: nonce ‖ ciphertext ‖ tag
}

func decrypt(_ combined: Data, using key: SymmetricKey) throws -> Data {
    let sealedBox = try AES.GCM.SealedBox(combined: combined)
    return try AES.GCM.open(sealedBox, using: key)
}

let key = SymmetricKey(size: .bits256)  // AES-256 per WWDC 2025 guidance
```

WWDC 2019-709 introduced CryptoKit with the design philosophy: "easy to use, hard to misuse."

**MASTG test:** MASTG-TEST-0317. **MASWE:** MASWE-0022. **Legacy:** MASTG-CRYPTO-4.

**Detection heuristic:**

```bash
grep -rn "AES\.GCM\.Nonce(data:" --include="*.swift"
grep -rn "let.*nonce.*=.*AES\.GCM\.Nonce" --include="*.swift"
grep -rn "Data(repeating:.*count:\s*12)" --include="*.swift"
grep -rn "\.seal(.*nonce:" --include="*.swift"
```

---

## Anti-Pattern #2 — MD5/SHA-1 for Security Purposes

**Severity:** HIGH | **OWASP:** M10 (Insufficient Cryptography) | **Fix effort:** Low

MD5 broken since Wang & Yu (2005); SHA-1 broken by SHAttered (2017). CISA January 2025 lists both as insecure. Apple signals this via CryptoKit's `Insecure.MD5` and `Insecure.SHA1` namespacing.

**❌ Insecure — AI-generated pattern:**

```swift
import CryptoKit
func hashPassword(_ password: String) -> String {
    let hash = Insecure.MD5.hash(data: password.data(using: .utf8)!)
    return hash.map { String(format: "%02x", $0) }.joined()
}
// Also: CC_MD5, CC_SHA1 from CommonCrypto
```

**✅ Secure — SHA-256 minimum, KDF for passwords:**

```swift
import CryptoKit

// Integrity verification
func hashData(_ data: Data) -> String {
    let hash = SHA256.hash(data: data)
    return hash.map { String(format: "%02x", $0) }.joined()
}

// HMAC for message authentication
func authenticate(_ data: Data, key: SymmetricKey) -> Data {
    Data(HMAC<SHA256>.authenticationCode(for: data, using: key))
}

// Password storage — NEVER raw hashes. Use a KDF:
// Server-side: Argon2id, bcrypt, or scrypt
// On-device: PBKDF2 with ≥600,000 iterations (OWASP 2023 minimum for HMAC-SHA256)
// See cryptokit-symmetric.md for full PBKDF2 implementation
```

iOS 26 adds SHA-3 family (`SHA3_256`, `SHA3_384`, `SHA3_512`) in CryptoKit. WWDC 2025-314 covers post-quantum additions (ML-KEM, ML-DSA), not SHA-3.

**MASTG test:** MASTG-TEST-0211. **MASTG demos:** MASTG-DEMO-0015, MASTG-DEMO-0016. **Legacy:** MSTG-CRYPTO-1.

**Detection heuristic:**

```bash
grep -rn "Insecure\.\(MD5\|SHA1\)" --include="*.swift"
grep -rn "CC_MD5\|CC_SHA1\|CC_MD5_DIGEST_LENGTH\|CC_SHA1_DIGEST_LENGTH" \
  --include="*.swift" --include="*.m"
```

---

## Anti-Pattern #3 — Non-Cryptographic RNG for Security Operations

**Severity:** HIGH | **OWASP:** M10 (Insufficient Cryptography) | **Fix effort:** Low

`arc4random()` returns only 32-bit `UInt32` — insufficient for cryptographic purposes requiring 128–256 bits. Character-by-character token construction introduces bias. Truly non-cryptographic alternatives (`rand()`, `drand48()`, GameplayKit RNG) must never be used for security operations.

**❌ Insecure — AI-generated patterns:**

```swift
func generateToken() -> String {
    return String(arc4random_uniform(999_999))  // ~20 bits of entropy
}

func generateSessionId(length: Int = 16) -> String {
    let chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return String((0..<length).map { _ in chars.randomElement()! })  // Bias
}
// Also dangerous: srand48/drand48, rand(), GameplayKit RNG
```

**✅ Secure — SecRandomCopyBytes / CryptoKit:**

```swift
import Security
import CryptoKit

// SecRandomCopyBytes — canonical iOS crypto RNG
func generateSecureToken(byteCount: Int = 32) throws -> String {
    var bytes = [UInt8](repeating: 0, count: byteCount)
    let status = SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes)
    guard status == errSecSuccess else {
        throw CryptoError.randomGenerationFailed(status)
    }
    return bytes.map { String(format: "%02x", $0) }.joined()
}

// CryptoKit key generation (secure RNG internally)
let encryptionKey = SymmetricKey(size: .bits256)
```

`SecRandomCopyBytes` sources entropy from the Secure Enclave's hardware TRNG via corecrypto's `ccrng_generate`. It reports errors via return status — unlike `arc4random`, which silently cannot fail.

**MASTG test:** MASTG-TEST-0311. **MASTG demos:** MASTG-DEMO-0073, MASTG-DEMO-0074. **Legacy:** MSTG-CRYPTO-6.

**Detection heuristic:**

```bash
grep -rn "arc4random\|arc4random_uniform\|arc4random_buf" --include="*.swift" | \
  grep -iE "token|nonce|salt|key|secret|session|iv"
grep -rn "\bsrand\b\|\brand()\|\brandom()\|\bdrand48\b" --include="*.swift"
grep -rn "GKARC4RandomSource\|GKMersenneTwisterRandomSource" --include="*.swift"
```

---

## Key Material Handling

Generate cryptographic keys with CryptoKit or provision them through an authenticated protocol. Do not initialize private or symmetric keys from hardcoded source strings, bundled configuration, or `Info.plist`. Scan source and compiled binaries for embedded key bytes. Persist private key material in the Keychain, and keep keys and plaintext out of logs; log operation outcomes instead. These checks complement the algorithm tests.

---

## Quick Reference Matrix

| #   | Anti-Pattern             | OWASP 2024 | MASTG Test      | Dangerous API              | Secure API                          | Fix Effort |
| --- | ------------------------ | ---------- | --------------- | -------------------------- | ----------------------------------- | ---------- |
| 1   | Nonce reuse AES-GCM      | M10        | MASTG-TEST-0317 | `AES.GCM.Nonce(data:)`     | Omit nonce (auto-random)            | Medium     |
| 2   | MD5/SHA-1 for security   | M10        | MASTG-TEST-0211 | `Insecure.MD5/.SHA1`       | `SHA256`+ / KDF for passwords       | Low        |
| 3   | Non-crypto RNG           | M10        | MASTG-TEST-0311 | `arc4random()`             | `SecRandomCopyBytes`                | Low        |

---

## CI/CD Detection Strategy

**Semgrep** (pre-commit/PR gate): Fast structural pattern matching for hardcoded keys, explicit AES-GCM nonces, and broken hash calls. Limited data-flow analysis.

**CodeQL** (nightly/PR gate): Deep semantic taint tracking — catches key material or plaintext assigned to variables then logged. Slower execution.

**Binary scanning** (post-build): `strings`/`class-dump` on compiled binary catches hardcoded keys surviving source-level obfuscation.

Recommended: Semgrep on every PR + post-build binary scanning. CodeQL nightly for deep analysis.

---

## iOS 26 / WWDC 2025 Implications

WWDC 2025-314 introduced the most significant CryptoKit expansion since 2019:

- **Symmetric keys:** `.bits256` recommended over `.bits128` for quantum resistance (anti-patterns #1, #3)
- **Hashing:** SHA-3 family (`SHA3_256/384/512`) in CryptoKit on iOS 26+ (anti-pattern #2)
- **Post-quantum:** ML-KEM 768/1024 and ML-DSA 65/87 with Secure Enclave support, plus the X-Wing hybrid KEM in software
- **TLS:** `X25519MLKEM768` enabled by default for `URLSession` in iOS 26
- **Secure Enclave:** Protect hardware-backed keys with access control when user authentication is required

---

## Summary Checklist

When reviewing iOS code for security anti-patterns, verify each item:

1. **No nonce reuse** — `AES.GCM.seal` called without explicit `nonce:` parameter (auto-random); no stored/global/counter-based nonce variables
1. **No broken hashes** — no `Insecure.MD5`, `Insecure.SHA1`, `CC_MD5`, `CC_SHA1` for security purposes; passwords use KDF (Argon2id, bcrypt, PBKDF2-HMAC-SHA256 with ≥600,000 iterations)
1. **Cryptographic RNG only** — `SecRandomCopyBytes` or CryptoKit APIs for tokens, nonces, salts, keys; no `arc4random` / `rand()` / `drand48()` / GameplayKit RNG in security contexts
1. **iOS 26 readiness** — symmetric keys use `.bits256`; no deprecated algorithms; aware of post-quantum CryptoKit APIs for forward-looking implementations
