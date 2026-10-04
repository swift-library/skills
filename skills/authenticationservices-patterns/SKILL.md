---
name: authenticationservices-patterns
description: Use this skill for AuthenticationServices implementation and review across Sign in with Apple, ASAuthorizationAppleIDProvider, ASAuthorizationController, ASAuthorizationAppleIDCredential, credential state checks, identity-token validation handoff, ASWebAuthenticationSession, WebAuthenticationSession, OAuth callback handling, password AutoFill, passkeys, security-key authentication, associated domains, SignInWithAppleButton, presentation contexts, existing-account setup, and account-security upgrades. Do not use for generic Keychain storage, generic OAuth server design, or biometric-protected local secrets unless AuthenticationServices is in scope.
---

# AuthenticationServices Patterns

## Purpose

Guide implementation, review, and troubleshooting for AuthenticationServices
flows in Swift and Apple-platform apps. This skill owns app-side system
authentication surfaces such as Sign in with Apple, passkeys, password AutoFill,
and web authentication sessions; credential storage and local secret
protection are out of scope.

## When To Use

- Implementing or reviewing Sign in with Apple requests, buttons, credential
  handling, credential-state checks, revocation handling, and server validation
  handoff.
- Building OAuth or web login through `ASWebAuthenticationSession` or SwiftUI
  `WebAuthenticationSession`.
- Implementing passkeys, platform public-key credentials, physical security-key
  authentication, associated domains, or passwordless registration/login.
- Integrating password AutoFill, password credential requests, existing-account
  setup, or account-security upgrade flows.
- Reviewing presentation context providers, callback URLs, cancellation,
  ephemeral sessions, or user-visible authentication errors.

## When Not To Use

- Do not use for plain Keychain CRUD or credential migration unless the
  AuthenticationServices flow is part of the work.
- Do not use for generic OAuth server design beyond app callback and token
  validation handoff.
- Do not use for embedded `WKWebView` login surfaces; prefer system web
  authentication unless the task explicitly requires embedded web content.
- Do not use for broad account UX copy or wording.

## Inputs To Inspect

- Entitlements, associated domains, services identifiers, callback schemes,
  presentation anchors, app groups, and target capabilities.
- `ASAuthorizationController`, Apple ID provider requests, scopes, nonce/state
  handling, delegate/coordinator code, and SwiftUI buttons.
- `ASWebAuthenticationSession` or `WebAuthenticationSession` setup, callback
  URL parsing, ephemeral preferences, cancellation handling, and browser-session
  assumptions.
- Passkey, public-key credential, password AutoFill, credential provider, and
  account-modification code.
- Server token-validation handoff, secure storage boundary, logs, tests, and
  revoked/denied/cancelled states.

## Workflow

1. Identify the authentication surface: Sign in with Apple, passkey, password
   credential, web authentication session, account upgrade, or SSO extension.
2. Verify entitlements, associated domains, callback identifiers, and current
   Apple documentation before treating behavior as fixed.
3. Review request construction, scopes, nonce/state handling, delegate or SwiftUI
   ownership, and presentation context.
4. For Sign in with Apple, separate app-side credential receipt from server-side
   identity-token validation and account linking.
5. For web authentication, verify callback URL handling, cancellation, session
   lifetime, cookie/ephemeral expectations, and external browser boundaries.
6. For passkeys and password AutoFill, verify domain association, credential
   creation/retrieval, user verification expectations, and fallback behavior.
7. Treat storage of refresh tokens, local secrets, or biometric-protected access
   as Keychain work outside this skill when implementation goes beyond the auth
   flow.
8. Test denied, cancelled, revoked, expired, existing-account, and first-run
   states where feasible.

## Review Rules

- Do not validate Apple identity tokens only on the client when a server account
  is involved.
- Do not log identity tokens, authorization codes, credential identifiers, or
  callback URLs containing secrets.
- Do not implement OAuth through embedded web views when a system session is
  suitable.
- Do not assume credential state, associated domains, callback delivery, or
  passkey behavior without current documentation or local device testing.
- Keep Keychain storage and AuthenticationServices flow ownership separate.

## Validation

- Build the affected app, extension, and associated-domain configuration.
- Test first sign-in, returning sign-in, cancellation, denied authorization,
  revoked credential, and account-linking paths.
- Test callback URL handling for success, error, state mismatch, and malformed
  callback cases.
- Test passkey or password AutoFill flows on supported devices and browsers
  when in scope.
- Confirm logs and analytics redact credentials and tokens.

## Output

Return:

1. AuthenticationServices surface and boundary decision
2. Entitlement, associated-domain, and callback readiness
3. Flow, token handoff, credential-state, and fallback findings
4. Security/logging concerns
5. Validation run or still needed
