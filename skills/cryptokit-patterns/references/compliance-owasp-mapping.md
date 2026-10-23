# Compliance & OWASP Mapping Reference

> Scope: Maps CryptoKit algorithms, key generation, key lifecycle, and Secure Enclave operations to OWASP Mobile Top 10 (2024), MASVS, and MASTG controls for audit and remediation.

Use OWASP Mobile Top 10 (2024) numbering: M10 covers insufficient cryptography; the 2016 edition called this M5. Record the MASVS control and MASTG test version used by an audit. Cryptographic key management also contributes to M1 (credential usage) and M9 (data storage).

## Master Traceability Matrix

| OWASP 2024 | MASVS controls | MASTG tests | CryptoKit/API concern | Required evidence |
| --- | --- | --- | --- | --- |
| M10 — Insufficient Cryptography | MASVS-CRYPTO-1, MASVS-CRYPTO-2 | 0209, 0210, 0211, 0213, 0214, 0311, 0317 | AES-GCM, ChaChaPoly, secure randomness, key sizes, Secure Enclave keys | Crypto inventory, algorithm audit, unit tests |
| M1 — Improper Credential Usage | MASVS-CRYPTO-2 | 0213, 0214 | Hardcoded cryptographic keys in source or bundled files | Static source and binary scans |
| M9 — Insecure Data Storage | MASVS-STORAGE-1, MASVS-CRYPTO-2 | 0302 | Authenticated encryption and separate protection of its key | Encryption round trips and key-persistence evidence |

Persist private and symmetric key material in the Keychain with an explicit access policy. Secure Enclave keys remain device-bound; protect their opaque persisted representations. Key storage and access-control integration need separate evidence from cryptographic correctness tests.

---

## M10 — Insufficient Cryptography

**Scope:** Weak algorithms, insufficient key lengths, poor key management, insecure RNG, deprecated hashes. Attack vectors: AVERAGE. Impact: SEVERE. Was M5 in 2016.

### Deprecated vs. Approved Algorithms

| Category       | ❌ Deprecated/Broken              | ✅ Approved (CryptoKit, iOS 13+)                               |
| -------------- | --------------------------------- | -------------------------------------------------------------- |
| Hashing        | MD5, SHA-1 (for security)         | SHA256, SHA384, SHA512; SHA3 (iOS 26+)                         |
| Symmetric      | DES, 3DES, RC4, Blowfish, AES-ECB | AES.GCM (AES-256-GCM), ChaChaPoly                              |
| Asymmetric     | RSA < 2048 bits                   | P256, P384, P521, Curve25519, Ed25519                          |
| Key derivation | Simple SHA hash of password       | HKDF; Argon2/bcrypt/scrypt server-side                         |
| RNG            | `rand()`, `random()`, `srand()`   | `SecRandomCopyBytes` (iOS 2+), CryptoKit auto-nonces (iOS 13+) |
| Post-quantum   | All classical PKC (by 2030)       | ML-KEM, ML-DSA, X-Wing (iOS 26+)                               |

**`arc4random()` nuance:** On modern Apple platforms, `arc4random()` uses a CSPRNG internally (not broken RC4). It is technically secure on iOS. However, `SecRandomCopyBytes` remains recommended for explicit cryptographic use — its security guarantees are documented and cross-platform portable. See `cryptokit-symmetric.md` for detailed algorithm guidance.

**AES-GCM nonce reuse is catastrophic:** A single reuse with the same key destroys both confidentiality (XOR of ciphertexts reveals XOR of plaintexts) and authentication (leaks GHASH key `H`, enabling arbitrary forgery). CryptoKit mitigates this by auto-generating random nonces when `AES.GCM.seal()` is called without an explicit nonce.

### MASTG Test Cases

| Test ID         | Legacy ID     | Verifies                                        | Profile |
| --------------- | ------------- | ----------------------------------------------- | ------- |
| MASTG-TEST-0209 | MSTG-CRYPTO-2 | Key size meets minimum requirements             | L1, L2  |
| MASTG-TEST-0210 | MSTG-CRYPTO-2 | No broken symmetric algorithms (DES, 3DES, RC4) | L1, L2  |
| MASTG-TEST-0211 | MSTG-CRYPTO-3 | No broken hashes (MD5, SHA-1 for security)      | L1, L2  |
| MASTG-TEST-0317 | MSTG-CRYPTO-3 | No broken encryption modes (ECB)                | L1, L2  |
| MASTG-TEST-0311 | MSTG-CRYPTO-6 | CSPRNG used (not `rand`/`random`)               | L1, L2  |
| MASTG-TEST-0213 | MSTG-CRYPTO-1 | No hardcoded cryptographic keys in code         | L1, L2  |
| MASTG-TEST-0214 | MSTG-CRYPTO-5 | No hardcoded cryptographic keys in files        | L1, L2  |

**iOS-specific testing:** Use radare2 to find references to `kCCAlgorithmDES`, `kCCAlgorithm3DES`, `kCCAlgorithmRC4`, `kCCOptionECBMode` in CommonCrypto calls. Search for `CC_MD5`, `CC_SHA1` or CryptoKit `Insecure.MD5`/`Insecure.SHA1`. MASTG demos: MASTG-DEMO-0015 (CommonCrypto broken hash), MASTG-DEMO-0016 (CryptoKit broken hash), MASTG-DEMO-0018 (broken encryption).

### Compliant: CryptoKit encryption

Canonical full round-trip patterns are in `cryptokit-symmetric.md` and anti-pattern #1 in `common-anti-patterns.md`. This compliance snippet stays minimal to avoid duplicating canonical crypto guidance.

```swift
import CryptoKit

enum CryptoError: Error { case invalidCiphertext }

/// Compliance: OWASP M10 (Insufficient Cryptography), MASVS-CRYPTO-1.
/// Test cases: MASTG-TEST-0210, MASTG-TEST-0317. iOS 13.0+.
func sealForStorage(_ plaintext: Data, using key: SymmetricKey) throws -> Data {
    let sealedBox = try AES.GCM.seal(plaintext, using: key)
    guard let combined = sealedBox.combined else { throw CryptoError.invalidCiphertext }
    return combined
}

// Compliance: MASVS-CRYPTO-2, MASTG-TEST-0213
let encryptionKey = SymmetricKey(size: .bits256) // 256-bit from CSPRNG
```

### Anti-pattern: insecure cryptography

```swift
// ❌ WRONG — MD5 (collisions trivially constructable) — fails MASTG-TEST-0211
var digest = [UInt8](repeating: 0, count: Int(CC_MD5_DIGEST_LENGTH))
CC_MD5(data.bytes, CC_LONG(data.count), &digest)

// ❌ WRONG — ECB mode — fails MASTG-TEST-0317
CCCrypt(CCOperation(kCCEncrypt), CCAlgorithm(kCCAlgorithmAES),
        CCOptions(kCCOptionECBMode), key, keyLength, nil, plaintext, ...)

// ❌ WRONG — Insecure RNG — fails MASTG-TEST-0311
let seed = srand(UInt32(time(nil)))  // Predictable seed

// ❌ WRONG — Hardcoded key — fails MASTG-TEST-0213
let key = SymmetricKey(data: "my-secret-key-1234567890123456".data(using: .utf8)!)

// ❌ WRONG — Static nonce (catastrophic if reused)
let nonce = try AES.GCM.Nonce(data: Data(repeating: 0, count: 12))
let sealed = try AES.GCM.seal(data, using: key, nonce: nonce)
```

---

## Enterprise Audit Workflow

Use MobSF for static scanning and radare2 for targeted API analysis. Inspect `SecKeyCreateWithData` and CryptoKit initializers for inline key bytes; inspect `.xcconfig`, `Info.plist`, and embedded resources. Use `strings`, class-dump, or dsdump on the binary to identify embedded keys and reachable crypto code.

| Finding | OWASP | MASVS | MASTG tests | Severity |
| --- | --- | --- | --- | --- |
| Hardcoded cryptographic keys | M1, M10 | CRYPTO-2 | 0213, 0214 | Critical |
| Deprecated crypto (MD5, DES) | M10 | CRYPTO-1 | 0210, 0211 | High |

Collect a static analysis report, a cryptographic inventory with algorithms and key sizes, relevant code snippets, and positive and negative operation tests. Record the key-persistence and hardware-test evidence separately. Use the supported assessment environment; static and binary analysis remain available when a jailbroken device is unavailable.

---

## Post-Quantum Cryptography Roadmap

Apple announced PQC support at WWDC 2025 (Session 314: "Get ahead with quantum-secure cryptography"). The threat model: "harvest now, decrypt later" — adversaries collecting encrypted traffic today for future quantum decryption.

| Date                     | Milestone                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------- |
| February 2024 (iOS 17.4) | iMessage PQ3 — first quantum-secure messaging at scale                                |
| August 2024              | NIST finalizes FIPS 203/204/205                                                       |
| January 2025             | CISA adds insecure crypto algorithms to bad practices list                            |
| June 2025 (WWDC)         | CryptoKit PQC APIs announced for iOS 26                                               |
| September 2025 (iOS 26)  | ML-KEM-768/1024, ML-DSA-65/87, X-Wing KEM in CryptoKit; quantum-secure TLS by default |
| 2030 (NIST target)       | Classical public-key crypto deprecated                                                |
| 2035 (CNSA 2.0)          | Classical algorithms disallowed for National Security Systems                         |

Apple uses hybrid cryptography — combining post-quantum and classical algorithms so updates never reduce security below the classical baseline. Build crypto agility now: abstract cryptographic interfaces behind protocols to allow configuration-level switches when PQC adoption becomes mandatory. See `cryptokit-public-key.md` for ML-KEM/ML-DSA implementation details.

---

## Cross-Reference Index

| iOS Practice                                              | M1  | M3  | M9  | M10              | Primary Reference                |
| --------------------------------------------------------- | --- | --- | --- | ---------------- | -------------------------------- |
| CryptoKit AES.GCM with auto-nonce                         | —   | —   | ✅  | ✅               | `cryptokit-symmetric.md`         |
| `SecRandomCopyBytes` for key/token generation             | ✅  | ✅  | —   | ✅               | `cryptokit-symmetric.md`         |
| ML-KEM/ML-DSA (iOS 26+)                                   | —   | —   | —   | ✅               | `cryptokit-public-key.md`        |

---

## Summary Checklist

1. **Audit identifiers** — Use OWASP 2024 numbering and record MASVS controls and MASTG test IDs with their source versions.
2. **Algorithms** — Use appropriate CryptoKit or SecKey primitives; reject MD5, DES, 3DES, RC4, and ECB for security work.
3. **Nonces** — Prefer AES-GCM automatic nonces; require a documented uniqueness strategy when a protocol supplies them.
4. **Key lifecycle** — Generate keys securely, reject embedded private or symmetric keys, and protect persisted key material separately from ciphertext.
5. **Evidence** — Include algorithm inventory, source/binary findings, correct API usage, and positive and negative crypto tests.
6. **Post-quantum readiness** — Evaluate hybrid cryptographic strategies and keep interfaces adaptable to ML-KEM/ML-DSA adoption.
