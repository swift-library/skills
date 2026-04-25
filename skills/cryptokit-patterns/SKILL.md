---
name: cryptokit-patterns
description: >-
  Use for CryptoKit cryptography in Swift or Apple-platform code: AES-GCM,
  ChaChaPoly, HMAC, SHA, SymmetricKey, HKDF/PBKDF2, P256/P384/P521,
  Curve25519, ECDSA/ECDH, HPKE, ML-KEM/ML-DSA, Secure Enclave, nonce/key
  derivation, crypto migration/review/tests. Do not use for Keychain
  CRUD/storage or certificate trust/TLS pinning.
---

# CryptoKit Patterns

Use this skill for cryptographic implementation, review, debugging, migration,
and testing with CryptoKit and Apple-platform cryptographic APIs. Keep storage
and trust-chain concerns routed to the sibling skills.

## Workflow

1. Identify the primitive or concern: hashing, MAC, authenticated encryption,
   key derivation, signing, key agreement, HPKE, post-quantum APIs, Secure
   Enclave, migration, review, or tests.
2. Check local deployment targets and platform constraints before recommending
   APIs such as SHA-3, HPKE, or post-quantum CryptoKit types.
3. Load the most specific reference file first. Add `common-anti-patterns.md`
   only for review/audit tasks.
4. For code changes, include availability gates, correct key lifecycle, and a
   focused test strategy.

## Reference Routing

| Task | Read |
| --- | --- |
| SHA, HMAC, AES-GCM, ChaChaPoly, nonce handling, symmetric keys | `references/cryptokit-symmetric.md` |
| ECDSA, ECDH, HKDF, HPKE, PEM/DER, post-quantum APIs | `references/cryptokit-public-key.md` |
| Secure Enclave keys, hardware constraints, simulator handling | `references/secure-enclave.md` |
| Review of generated or security-sensitive crypto code | `references/common-anti-patterns.md` plus the specific crypto file |
| Tests, CI, simulator/device split, mutation or round-trip tests | `references/testing-security-code.md` |
| OWASP Mobile Top 10, MASVS, or MASTG crypto mapping | `references/compliance-owasp-mapping.md` |

## Core Checks

- Do not invent or hand-roll cryptographic protocols when CryptoKit provides a
  suitable primitive.
- Do not use MD5 or SHA-1 for security purposes.
- Use authenticated encryption for new encryption work; do not emit unauthentic
  encryption examples as the safe default.
- Do not reuse an AES-GCM nonce with the same key. Prefer CryptoKit's automatic
  nonce generation unless a protocol explicitly requires nonce management.
- Derive ECDH shared secrets through HKDF before using them as symmetric keys.
- Treat Secure Enclave keys as generated-in-place, device-bound, and
  non-exportable; do not suggest importing external private keys into the
  Secure Enclave.
- Guard Secure Enclave code for simulator and hardware availability.
- Persist cryptographic keys through the Keychain when persistence is required;
  coordinate with `keychain-patterns` for storage details.

## Coordination

- Use `keychain-patterns` for Keychain CRUD, credential storage, access groups,
  data protection classes, biometric-gated secret retrieval, and migration from
  insecure stores.
- Use `certificate-trust-patterns` for `SecTrust`, SPKI pinning, client
  certificates, mTLS, and URLSession trust evaluation.
- Use `swiftpm-index` when reviewing whether custom reusable crypto,
  certificate, ASN.1, or protobuf infrastructure should be replaced by an
  official package.

## Output

For reviews, state severity, explain the cryptographic failure mode, cite the
reference file, and give the safer pattern. For implementations, include API
availability, key lifecycle, persistence assumptions, and tests. When a claim
depends on recent Apple APIs, prefer official documentation over memory.
