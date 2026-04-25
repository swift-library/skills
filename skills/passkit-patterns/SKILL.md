---
name: passkit-patterns
description: Use this skill for PassKit, Apple Pay, and Wallet implementation and review across PKPaymentRequest, PKPaymentAuthorizationController, Apple Pay buttons, merchant IDs, payment capabilities, shipping/contact updates, payment token handoff, recurring/deferred/multimerchant payments, Wallet pass access, PKAddPassesViewController, PKPassLibrary, pass entitlements, pass update services, and simulator/device payment constraints. Do not use for StoreKit digital goods, pricing strategy, market commerce planning, or generic payment-provider SDK work with no PassKit behavior.
---

# PassKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for Apple Pay and Wallet
features that use PassKit payment sheets, merchant configuration, payment token
handoff, Wallet passes, and pass-library access.

## When To Use

- Building or reviewing Apple Pay checkout with `PKPaymentRequest`,
  `PKPaymentAuthorizationController`, or Apple Pay buttons.
- Configuring merchant IDs, supported networks, merchant capabilities, summary
  items, shipping/contact fields, coupons, recurring/deferred payments, or
  multimerchant payments.
- Handing payment tokens to a payment processor and reporting authorization
  results.
- Adding, checking, replacing, or reading Wallet passes with `PKPassLibrary` and
  `PKAddPassesViewController`.
- Debugging Wallet entitlements, pass type IDs, payment-sheet updates, device
  constraints, or simulator limitations.

## When Not To Use

- Do not use for StoreKit digital goods or subscriptions.
- Do not use for pricing strategy, market commerce planning, or payment copy.
- Do not use for generic payment-provider SDK behavior unless Apple Pay or
  Wallet PassKit code is in scope.
- Do not use for release signing/provisioning alone; use
  `apple-platform-release`.
- Do not invent regional payment rules, merchant configuration requirements, or
  payment-network availability. Verify current Apple documentation, portal
  setup, and processor requirements.

## Inputs To Inspect

- Merchant IDs, entitlements, Wallet capability, pass type identifiers, and
  provisioning state.
- `PKPaymentRequest`, summary items, networks, merchant capabilities, shipping,
  contact fields, coupon, recurring, deferred, and multimerchant configuration.
- Apple Pay button/UI wiring, sheet presentation, delegate callbacks, payment
  result handling, and token handoff.
- Wallet pass loading, pass-library access, add-pass UI, pass update web
  service, and push update model.
- Device/simulator constraints, test cards, payment processor docs, and failure
  logs.

## Workflow

1. Identify whether the task is Apple Pay checkout, Wallet pass management, pass
   updates, identity/pass access, or entitlement troubleshooting.
2. Verify capabilities, merchant ID, pass type IDs, and provisioning before
   diagnosing code.
3. Build `PKPaymentRequest` from product totals, country/currency, supported
   networks, capabilities, shipping/contact requirements, and summary item
   totals.
4. Present the payment sheet from an appropriate controller/context and handle
   shipping/contact updates, authorization, cancellation, and errors.
5. Hand payment tokens to the processor without logging sensitive payment data.
6. For Wallet passes, verify signing, identifiers, add-pass UI, library access,
   contains/replace flows, and update service behavior.
7. Validate on a supported device whenever Apple Pay or Wallet hardware/account
   behavior matters.

## Review Rules

- Do not use PassKit for digital goods that belong in StoreKit.
- Do not assume simulator behavior proves Apple Pay or Wallet readiness.
- Do not log payment tokens, pass identifiers, or sensitive Wallet data.
- Do not let payment summary totals drift from the actual order total.
- Do not present Apple Pay as available without device, card, merchant, and
  network checks.
- Treat regional rules, recurring/deferred APIs, and pass entitlements as
  current-source gated.

## Validation

- Build the affected app target.
- Verify merchant ID, entitlements, capabilities, and pass type IDs.
- Test unavailable Apple Pay, missing card, cancelled payment, shipping/contact
  update, failed authorization, and successful token handoff.
- Test Wallet pass add/check/replace flows where applicable.
- Use supported device testing for payment-sheet and Wallet behavior.

## Output

For implementation or review work, return:

1. PassKit feature type and entitlement status
2. Payment request or pass-library findings
3. Token, processor, and Wallet data boundaries
4. Device/simulator validation status
5. Current-source assumptions for regional or entitlement behavior
