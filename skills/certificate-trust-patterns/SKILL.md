---
name: certificate-trust-patterns
description: >-
  Use for Apple certificate trust and TLS trust in Swift: SecTrust,
  SecCertificate, SecIdentity, URLSession authentication challenges,
  certificate/SPKI/CA/leaf pinning, NSPinnedDomains, client certificates,
  PKCS#12, mTLS, trust debugging, SecTrustEvaluate migration, and rotation. Do
  not use for Keychain storage, CryptoKit algorithms, App Transport Security, or
  server TLS deployment.
---

# Certificate Trust Patterns

Use this skill for certificate trust evaluation, pinning, client certificates,
and URLSession trust handling on Apple platforms. Keep Keychain storage and
general cryptography routed to the sibling skills.

## Workflow

1. Identify the trust concern: system trust evaluation, pinning strategy,
   URLSession challenge handling, client certificate import, mTLS, rotation, or
   deprecated API migration.
2. Check local platform targets, networking stack, server ownership, and
   whether declarative pinning can replace custom trust code.
3. Read `references/certificate-trust.md` before implementing or reviewing
   trust logic.
4. For reviews, look for deprecated trust APIs, bypassed trust evaluation,
   fragile leaf pins, missing backup pins, and main-thread trust work.

## Core Checks

- Do not bypass system trust evaluation to make a connection succeed.
- Prefer declarative `NSPinnedDomains`, SPKI pins, or CA/intermediate pins over
  leaf certificate pins unless the rotation cost is understood.
- Use current trust APIs and migrate away from deprecated synchronous
  `SecTrustEvaluate` patterns.
- Run trust evaluation away from the main thread when the code path can block.
- Plan pin rotation and backup pins before shipping a pinning strategy.
- Treat client certificate private keys as sensitive credentials; use
  `keychain-patterns` for persistent storage details.

## Coordination

- Use `keychain-patterns` for storing client certificate identities, private
  keys, credentials, access groups, and Keychain troubleshooting.
- Use `cryptokit-patterns` for hashing, key agreement, signatures, or custom
  cryptographic protocols.
- Use Apple networking or platform documentation directly for App Transport
  Security and server-side TLS deployment; those are outside this skill.

## Output

For reviews, report severity, the trust or rotation risk, the safer pattern,
and the reference section used. For implementations, include platform
availability, rotation assumptions, fallback behavior, and tests or manual
verification steps.
