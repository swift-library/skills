---
name: devicecheck-patterns
description: Use this skill for DeviceCheck and App Attest implementation and review across DCDevice support checks, device token generation, two server-side bits, DCAppAttestService, App Attest key generation, attestation, assertions, nonce/challenge handling, server verification, environment entitlement, DCError handling, rollout strategy, invalidated keys, retry policy, fraud-risk signals, and graceful unsupported states. Do not use for Keychain storage, CryptoKit primitive selection, certificate trust, authentication UI, or generic security review without DeviceCheck/App Attest.
---

# DeviceCheck Patterns

## Purpose

Guide implementation, review, and troubleshooting for DeviceCheck and App
Attest flows that protect server APIs and maintain limited per-device state.

## When To Use

- Generating `DCDevice` tokens and coordinating server-side two-bit state.
- Implementing App Attest key generation, attestation, assertion, challenge,
  nonce, and server verification flows.
- Reviewing App Attest environment setup, rollout strategy, invalidated keys,
  retry policy, and fraud-risk signals.
- Debugging `DCError`, unsupported devices, development versus production
  behavior, and graceful fallback.

## When Not To Use

- Do not use for Keychain storage or biometric-protected credentials.
- Do not use for cryptographic primitive design.
- Do not use for certificate trust or TLS pinning.
- Do not use for Sign in with Apple, OAuth, or authentication UI.
- Do not invent App Attest server behavior, environment behavior, or fraud
  guarantees. Verify current Apple documentation and server implementation.

## Inputs To Inspect

- DeviceCheck/App Attest entitlement and environment configuration.
- `DCDevice.isSupported`, token generation, App Attest key generation,
  attestation, assertion, nonce/challenge, and key persistence code.
- Server verification code, endpoint contracts, replay protection, risk
  scoring, retry policy, and gradual rollout gates.
- Error handling, unsupported states, telemetry, logs, and tests.

## Workflow

1. Identify whether the feature uses DeviceCheck two-bit state, App Attest, or
   both.
2. Confirm support checks and environment configuration before app code assumes
   integrity protection.
3. Keep server-generated challenges fresh, single-use, and bound to the
   protected request.
4. Treat attestation as key enrollment and assertions as request protection.
   Do not repeat attestation on every request without a reason.
5. Persist key identifiers carefully and handle invalidation with controlled
   re-enrollment.
6. Keep fraud decisions server-side and combine DeviceCheck/App Attest signals
   with broader risk assessment.
7. Provide graceful unsupported, temporarily failed, and rollout-disabled
   states.

## Review Rules

- Do not ship App Attest as client-only validation.
- Do not treat DeviceCheck's two bits as user identity.
- Do not log raw tokens, attestations, assertions, or server secrets.
- Do not block all users on transient App Attest errors during rollout.
- Treat environment, server validation, and failure behavior as
  current-source and implementation gated.

## Validation

- Build the affected app target.
- Test unsupported, development, production, token failure, attestation failure,
  assertion failure, replay, invalidated key, and server-rejected states.
- Verify server challenge freshness and one-time use.
- Verify rollout flags and fallback behavior.
- Inspect logs for accidental token, key, or challenge leakage.

## Output

For implementation or review work, return:

1. DeviceCheck/App Attest surface and environment status
2. Token, attestation, assertion, and server verification findings
3. Rollout, retry, fallback, and fraud-risk boundaries
4. Validation run or still needed
5. Current-source assumptions for App Attest behavior
