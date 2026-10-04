---
name: cryptotokenkit-patterns
description: Use this skill for CryptoTokenKit implementation and review across TKToken, TKTokenDriver, TKTokenSession, TKTokenWatcher, TKSmartCard, TKSmartCardToken, TKSmartCardTokenDriver, smart card app extensions, token keychain contents, certificate/key exposure, PIN/authentication state, APDU exchange, TLV records, managed smart card authentication, and token errors. Do not use for Keychain storage without hardware tokens, CryptoKit algorithms, certificate trust policy, Passkeys, or generic authentication UI.
---

# CryptoTokenKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for CryptoTokenKit tokens,
smart cards, token drivers, sessions, keychain exposure, and smart card
authentication.

## When To Use

- Implementing or reviewing `TKToken`, `TKTokenDriver`, `TKTokenSession`,
  `TKTokenWatcher`, or token keychain item behavior.
- Building smart card app extensions with `TKSmartCardToken`,
  `TKSmartCardTokenDriver`, `TKSmartCard`, APDUs, and TLV records.
- Debugging token insertion/removal, PIN/authentication state, session
  creation, certificate/key exposure, and managed smart card preferences.
- Reviewing hardware-token integration boundaries with Keychain and
  certificate trust.

## When Not To Use

- Do not use for normal Keychain storage without hardware token semantics.
- Do not use for CryptoKit primitive choice or data encryption.
- Do not use for TLS trust or certificate pinning policy.
- Do not use for passkeys, Sign in with Apple, OAuth, or generic login UI.
- Do not invent platform support, extension behavior, smart card management, or
  token-session semantics. Verify current Apple documentation and deployment
  environment.

## Inputs To Inspect

- Token driver, smart card extension, entitlements, app group, bundle, and
  managed configuration.
- `TKToken`, `TKTokenSession`, keychain contents, certificate/key item mapping,
  object identifiers, and access control.
- `TKSmartCard`, APDU exchange, TLV parsing, PIN flows, error handling, and
  card insertion/removal handling.
- Keychain consumers, certificate trust consumers, logs, device tests, and
  managed-device assumptions.

## Workflow

1. Classify the token: generic CryptoTokenKit token, smart card token, watcher,
   or consumer of token-backed keychain items.
2. Confirm platform, extension, entitlement, and managed-device constraints
   before code changes.
3. Keep token identity, object IDs, keychain item exposure, and certificate/key
   mapping stable.
4. Keep session authentication state explicit and avoid leaking PINs or token
   secrets into logs.
5. Treat smart card communication as a state machine: connect, select, APDU,
   parse, error, disconnect, and card removal.
6. Leave certificate trust policy to trust-evaluation code once token-backed
   identity exposure is correct.

## Review Rules

- Do not treat token-backed keychain items like normal app-created secrets.
- Do not store PINs or APDU secrets in app logs or analytics.
- Do not assume every smart card supports the same AID, APDU, or certificate
  layout.
- Do not hide token removal, locked token, and authentication-needed states.
- Treat smart card extension and managed authentication behavior as
  current-source gated.

## Validation

- Build the app and extension targets.
- Test token unavailable, inserted, removed, locked, unlocked, PIN failure,
  session failure, and certificate/key lookup states.
- Test APDU/TLV parsing with known card fixtures when feasible.
- Test managed-device configuration when deployment depends on it.
- Inspect logs for accidental PIN, APDU, private key, or certificate material
  leakage.

## Output

For implementation or review work, return:

1. CryptoTokenKit token/smart card surface and deployment assumptions
2. Driver, session, keychain, APDU, and authentication findings
3. Keychain, certificate trust, management, and privacy boundaries
4. Validation run or still needed
5. Current-source assumptions for platform or extension behavior
