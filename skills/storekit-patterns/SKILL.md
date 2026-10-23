---
name: storekit-patterns
description: StoreKit implementation and review for in-app purchases, subscriptions, Product loading, verified transactions, current entitlements, Transaction.updates, restore/sync, and StoreKitTest. Not for pricing strategy, release operations, or PassKit checkout.
---

# StoreKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for StoreKit code that loads
products, sells in-app purchases or subscriptions, verifies transactions, grants
entitlements, and tests purchase flows.

## When To Use

- Implementing or reviewing in-app purchase, subscription, paywall, restore, or
  entitlement code.
- Loading `Product` values, displaying localized product information, or using
  `StoreView`, `ProductView`, or `SubscriptionStoreView`.
- Handling purchase results, verified transactions, current entitlements,
  unfinished transactions, and `Transaction.updates`.
- Testing StoreKit with StoreKit configuration files, sandbox, `SKTestSession`,
  Ask to Buy, billing retry, refunds, or subscription renewal states.
- Reviewing App Transaction use or server-side transaction/JWS validation.
- Reviewing `AppTransaction` and subscription offer flows.

## When Not To Use

- Do not use for pricing strategy, monetization positioning, App Store metadata,
  market commerce review, or promotional copy.
- Do not use for App Store Connect operations unless they directly block local
  StoreKit code validation.
- Do not use for release signing, provisioning, archive/export, or upload
  readiness.
- Do not use for non-StoreKit payment integrations.
- Do not invent App Review policy, external purchase rules, offer availability,
  or StoreKit regional behavior. Verify current Apple policy, App Store
  Connect, and StoreKit documentation before relying on them.

## Inputs To Inspect

- Product identifiers, StoreKit configuration files, App Store Connect product
  setup records, and subscription group shape.
- Product loading, paywall, purchase, restore/sync, entitlement, transaction
  listener, and server-validation code.
- StoreKit SwiftUI view usage and custom merchandising UI.
- Tests using StoreKitTest, sandbox notes, receipt or JWS handling, and server
  notification handling if present.
- Business-rule boundaries where market or commerce decisions should stay
  outside code implementation.

## Workflow

1. Identify product types: consumable, non-consumable, non-renewing
   subscription, auto-renewable subscription, or app transaction.
2. Confirm product identifiers and test configuration before changing purchase
   code.
3. Load products with `Product.products(for:)`, display localized names,
   descriptions, and prices from StoreKit, and handle missing products.
4. Handle purchase results explicitly: success with verification, pending,
   user-cancelled, and unknown or thrown errors.
5. Grant access from verified transactions and current entitlements, then call
   `finish()` only after delivering the purchased content or service.
6. Maintain a transaction listener for updates that arrive outside the active
   purchase flow.
7. Review subscription status, renewal info, revocation, refunds, family
   sharing, billing retry, grace period, and offer logic where applicable.
8. Validate using StoreKit configuration, StoreKitTest, sandbox, and server
   verification results according to the app's risk.
- `Product.purchase(options:)` is `@MainActor async throws` and unavailable on
  visionOS; there, use an available `purchase(confirmIn:options:)` overload.
- `PurchaseResult.success` contains `VerificationResult<Transaction>`; handle
  `.verified`/`.unverified` separately from `.pending` and `.userCancelled`.
- Iterate `Transaction.currentEntitlements`, `.unfinished`, and `.updates` as
  async sequences of verification results; `Transaction.finish()` is async.

## Review Rules

- Never unlock paid content from unverified transactions.
- Do not hard-code display prices, product names, or localized subscription
  terms.
- Do not ignore pending, Ask to Buy, refund, revocation, billing retry, or grace
  period states.
- Do not finish a transaction before the app has delivered access.
- Keep paywall UI decisions separate from entitlement truth.
- Avoid original StoreKit APIs unless the task is migration or legacy support.
- Treat external purchase, subscription offer, and regional policy claims as
  current-policy gated.
- Gate `Transaction.currentEntitlements(for:)` and `Product.currentEntitlements`
  to iOS 18.4/macOS 15.4/tvOS 18.4/watchOS 11.4/visionOS 2.4 or newer.
- Migrate the singular `currentEntitlement(for:)`/`currentEntitlement` APIs,
  deprecated at those versions, to the corresponding plural sequences.
- Legacy `SKPaymentQueue.restoreCompletedTransactions()` is deprecated from
  iOS 18/macOS 15/tvOS 18/watchOS 11/visionOS 2; use `AppStore.sync()` (async throws).

## Validation

- Build the affected app target.
- Run StoreKit configuration or StoreKitTest coverage for product load,
  purchase, cancellation, pending, restore/sync, and entitlement refresh.
- Test subscription renewal, billing retry, grace period, refund, revocation,
  and Ask to Buy when those states affect behavior.
- Check server-side JWS validation or App Store Server Notifications when the
  app relies on a server entitlement source.

## Output

For implementation or review work, return:

1. Product and entitlement model
2. Purchase and transaction handling findings
3. StoreKit UI and test configuration status
4. Server validation or notification assumptions
5. Validation run or still needed
