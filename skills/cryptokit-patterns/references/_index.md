# CryptoKit Patterns References

Use these files selectively. Prefer the primitive-specific file first and add
review, testing, or compliance references only when the task calls for them.

| File | Use for |
| --- | --- |
| `cryptokit-symmetric.md` | Hashing, HMAC, AES-GCM, ChaChaPoly, SymmetricKey, nonce handling, HKDF/PBKDF2 |
| `cryptokit-public-key.md` | P256/P384/P521, Curve25519, ECDSA, ECDH, HPKE, ML-KEM, ML-DSA, PEM/DER |
| `secure-enclave.md` | Secure Enclave capabilities, constraints, persistence, availability, simulator behavior |
| `common-anti-patterns.md` | Review backbone for weak crypto, hardcoded keys, nonce reuse, and related generated-code mistakes |
| `testing-security-code.md` | CryptoKit round-trip tests, Secure Enclave test strategy, CI/device split |
| `compliance-owasp-mapping.md` | OWASP Mobile Top 10, MASVS, and MASTG cryptography mapping |

Some copied references mention Keychain storage because persistent keys need a
secure store. Use `keychain-patterns` for the storage implementation.
