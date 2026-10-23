# Testing CryptoKit and Secure Enclave Code

> Scope: Unit, integration, and CI patterns for validating CryptoKit operations and Secure Enclave keys across Simulator, CI runners, and physical devices.

Run software encryption, signing, key agreement, and failure-path tests on Simulator and CI. Inject signing providers into consumers so unit tests can use software keys or mocks. Reserve hardware-key and access-control integration tests for supported physical devices.

Persisted keys also need storage integration tests: save and reload the key representation through an injected key store, then verify that the restored key decrypts or signs as expected. Store private key material in the Keychain; Secure Enclave `dataRepresentation` is an opaque, device-bound representation, not exportable private key bytes.

## Simulator vs. Device Testing Matrix

| Feature | Simulator | Physical device |
| --- | --- | --- |
| CryptoKit software crypto (AES-GCM, ChaChaPoly, P256, SHA256) | Supported | Supported |
| `SecureEnclave.isAvailable` | Do not rely on a fixed value or use it alone to enable key operations | Check at runtime before key operations |
| Secure Enclave key generation | Exclude with `#if targetEnvironment(simulator)` or inject a software/mock provider | Check availability and handle creation errors |
| Software ML-KEM / ML-DSA | Requires an OS runtime supporting the API (iOS 26+) | Requires a supported OS version |

Use compile-time Simulator exclusion plus the runtime `SecureEnclave.isAvailable` check for hardware tests. A true availability result does not guarantee successful key creation; propagate operation errors.

## Essential Testing Patterns

### CryptoKit Round-Trip Tests (Simulator-Safe)

All CryptoKit software operations work on simulator. These tests run everywhere:

```swift
import XCTest
import CryptoKit

final class CryptoKitTests: XCTestCase {

    func testAESGCMRoundTrip() throws {
        let key = SymmetricKey(size: .bits256)
        let plaintext = "Sensitive credentials".data(using: .utf8)!
        let sealedBox = try AES.GCM.seal(plaintext, using: key)
        let ciphertext = sealedBox.combined!
        XCTAssertNotEqual(ciphertext, plaintext)

        let reopened = try AES.GCM.SealedBox(combined: ciphertext)
        let decrypted = try AES.GCM.open(reopened, using: key)
        XCTAssertEqual(decrypted, plaintext)
    }

    func testAESGCMWrongKeyFails() throws {
        let correctKey = SymmetricKey(size: .bits256)
        let wrongKey = SymmetricKey(size: .bits256)
        let sealed = try AES.GCM.seal("secret".data(using: .utf8)!, using: correctKey)
        XCTAssertThrowsError(try AES.GCM.open(sealed, using: wrongKey))
    }

    func testP256SignVerify() throws {
        let privateKey = P256.Signing.PrivateKey()
        let data = "Message to authenticate".data(using: .utf8)!
        let signature = try privateKey.signature(for: data)
        XCTAssertTrue(privateKey.publicKey.isValidSignature(signature, for: data))

        let tampered = "Tampered message".data(using: .utf8)!
        XCTAssertFalse(privateKey.publicKey.isValidSignature(signature, for: tampered))
    }

    func testCurve25519KeyAgreement() throws {
        let alice = Curve25519.KeyAgreement.PrivateKey()
        let bob = Curve25519.KeyAgreement.PrivateKey()
        let aliceShared = try alice.sharedSecretFromKeyAgreement(with: bob.publicKey)
        let bobShared = try bob.sharedSecretFromKeyAgreement(with: alice.publicKey)

        let aliceKey = aliceShared.hkdfDerivedSymmetricKey(
            using: SHA256.self, salt: Data(), sharedInfo: Data(), outputByteCount: 32)
        let bobKey = bobShared.hkdfDerivedSymmetricKey(
            using: SHA256.self, salt: Data(), sharedInfo: Data(), outputByteCount: 32)

        // Both parties can decrypt each other's messages
        let sealed = try AES.GCM.seal("test".data(using: .utf8)!, using: aliceKey)
        XCTAssertEqual(try AES.GCM.open(sealed, using: bobKey), "test".data(using: .utf8)!)
    }
}
```

**iOS 26 note:** Post-quantum cryptography (ML-KEM, ML-DSA) is available via CryptoKit starting iOS 26. Gate these tests with `@available(iOS 26, *)` and use the same round-trip pattern. Software-based PQC works on simulator (see `cryptokit-public-key.md`).

---

## Secure Enclave Test Strategy — Protocol Fallback

A single function returning `P256.Signing.PrivateKey` for both SE and software paths is a type error — `SecureEnclave.P256.Signing.PrivateKey` and `P256.Signing.PrivateKey` are distinct types. Use a protocol-based abstraction:

### SigningKeyProvider Protocol with SE/Software Implementations

```swift
import CryptoKit
import Foundation

enum SigningKeyError: Error {
    case secureEnclaveUnavailable
}

protocol SigningKeyProvider {
    func sign(_ data: Data) throws -> Data
    func publicKeyData() -> Data
}

final class SecureEnclaveSigningKey: SigningKeyProvider {
    private let key: SecureEnclave.P256.Signing.PrivateKey

    init() throws {
        #if targetEnvironment(simulator)
        throw SigningKeyError.secureEnclaveUnavailable
        #else
        guard SecureEnclave.isAvailable else {
            throw SigningKeyError.secureEnclaveUnavailable
        }
        self.key = try SecureEnclave.P256.Signing.PrivateKey()
        #endif
    }

    func sign(_ data: Data) throws -> Data {
        try key.signature(for: data).derRepresentation
    }

    func publicKeyData() -> Data { key.publicKey.derRepresentation }
}

final class SoftwareSigningKey: SigningKeyProvider {
    private let key = P256.Signing.PrivateKey()

    func sign(_ data: Data) throws -> Data {
        try key.signature(for: data).derRepresentation
    }

    func publicKeyData() -> Data { key.publicKey.derRepresentation }
}

struct SigningKeyFactory {
    static func make() throws -> any SigningKeyProvider {
        #if targetEnvironment(simulator)
        return SoftwareSigningKey()
        #else
        if SecureEnclave.isAvailable {
            return try SecureEnclaveSigningKey()
        }
        return SoftwareSigningKey()
        #endif
    }
}
```

Use this factory only when software fallback is permitted by the application’s security requirements. Inject `SoftwareSigningKey` or a mock for deterministic unit tests. If hardware backing is required, propagate unavailability and key-creation errors.

### Testing Secure Enclave Code

```swift
// ❌ INCORRECT: Attempts hardware key creation on Simulator and CI
func testSecureEnclaveSigning_BROKEN() throws {
    let key = try SecureEnclave.P256.Signing.PrivateKey() // throws on simulator
    let sig = try key.signature(for: "data".data(using: .utf8)!)
    XCTAssertTrue(key.publicKey.isValidSignature(sig, for: "data".data(using: .utf8)!))
}

// ✅ CORRECT: Exclude Simulator and check hardware availability
func testSecureEnclaveSigning_withGuard() throws {
    #if targetEnvironment(simulator)
    throw XCTSkip("Requires a physical device with Secure Enclave support")
    #else
    try XCTSkipUnless(SecureEnclave.isAvailable,
                      "Secure Enclave unavailable on this device")
    let key = try SecureEnclave.P256.Signing.PrivateKey()
    let data = "authenticated payload".data(using: .utf8)!
    let sig = try key.signature(for: data)
    XCTAssertTrue(key.publicKey.isValidSignature(sig, for: data))
    #endif
}

// ✅ CORRECT: Protocol-based test runs everywhere
func testSigningWithFallback() throws {
    let signer = try SigningKeyFactory.make()
    let data = "payload".data(using: .utf8)!
    let sigBytes = try signer.sign(data)
    XCTAssertFalse(sigBytes.isEmpty)

    let publicKey = try P256.Signing.PublicKey(derRepresentation: signer.publicKeyData())
    let signature = try P256.Signing.ECDSASignature(derRepresentation: sigBytes)
    XCTAssertTrue(publicKey.isValidSignature(signature, for: data))
}
```

---

## Xcode Test Plans — Separating Simulator from Device

Create two test plans for CI/device split:

- **CITests.xctestplan**: Software CryptoKit round trips, wrong-key and tampering failures, and injected signing providers. Excludes Secure Enclave integration tests.
- **DeviceTests.xctestplan**: Secure Enclave key generation, signing, key agreement, and access-control integration. Requires supported physical hardware.

```bash
# CI: simulator-safe tests on every push
xcodebuild test -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -testPlan CITests

# Nightly: device farm runs everything
xcodebuild test -scheme MyApp \
  -destination 'platform=iOS,id=DEVICE_UDID' \
  -testPlan DeviceTests
```

---

## Advanced Patterns

### Mutation Testing

Mutation testing introduces deliberate bugs (flipping `==` to `!=`, removing signature-verification calls, swapping `&&` to `||`) and checks whether your tests catch them. A project can have high line coverage and a low mutation score — tests execute security code without validating it does the right thing.

**Muter** (`brew install muter-mutation-testing/muter/muter`) is a mutation testing tool for Swift. Its `RelationalOperatorReplacement` operator catches authentication bypasses; `RemoveSideEffects` catches removed cryptographic verification side effects. For security code, set an explicit mutation-score threshold and raise it as surviving mutants are fixed.

---

## Summary Checklist

1. **Software round trips** — Encrypt/decrypt and sign/verify tests cover AES-GCM, ChaChaPoly, P256, and Curve25519 as used by the app; include wrong-key and tampering failures.
2. **Secure Enclave guards** — Hardware tests use `#if targetEnvironment(simulator)` to skip Simulator and `XCTSkipUnless(SecureEnclave.isAvailable, ...)` on device; unit tests inject software or mock providers.
3. **Provider boundary** — Secure Enclave and software private keys have distinct types; expose the required signing or key-agreement operation through a protocol.
4. **Simulator/device split** — Keep software and injected-provider tests in `CITests`, and hardware-key integration tests in `DeviceTests`.
5. **Key persistence** — Test restoration through an injected key store and validate the restored key with a cryptographic operation.
6. **Mutation testing** — Track Muter’s mutation score against an agreed threshold; exercise `RelationalOperatorReplacement` and `RemoveSideEffects` on security-critical paths.
7. **Availability** — Gate post-quantum tests on the API’s OS availability.
