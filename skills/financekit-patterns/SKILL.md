---
name: financekit-patterns
description: Use this skill for FinanceKit implementation and review across FinanceStore availability, managed entitlement gating, NSFinancialDataUsageDescription, authorization, account queries, account balances, transaction queries, HistoryToken persistence, transaction history streams, Wallet orders, background delivery extensions, App Group handoff, FinanceKitUI, high-sensitivity financial-data display, and graceful unavailable states. Do not use for StoreKit purchases, PassKit checkout, market finance copy, generic budgeting models, or payment processing.
---

# FinanceKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for FinanceKit features that
access Wallet financial data, accounts, balances, transactions, orders, history,
and background delivery.

## When To Use

- Checking FinanceKit availability, managed entitlement setup, and financial
  data usage descriptions.
- Requesting FinanceKit authorization and handling restricted, denied, or
  unavailable states.
- Querying accounts, balances, transactions, transaction history, or history
  tokens through `FinanceStore`.
- Saving or checking Wallet orders.
- Implementing background delivery extensions, App Group handoff, or
  FinanceKitUI flows.
- Reviewing high-sensitivity financial-data display, storage, and logging.

## When Not To Use

- Do not use for StoreKit purchases or digital goods.
- Do not use for PassKit checkout or Apple Pay token handling.
- Do not use for market finance copy, pricing, or commerce strategy.
- Do not use for generic budgeting models unless FinanceKit data access is in
  scope.
- Do not invent managed-entitlement eligibility, region/device availability, or
  background delivery behavior. Verify current Apple documentation and portal
  state.

## Inputs To Inspect

- FinanceKit managed entitlement state, organization/account-holder
  assumptions, `NSFinancialDataUsageDescription`, and target capabilities.
- `FinanceStore.isDataAvailable`, authorization status, request authorization,
  and unavailable-state UI.
- Account, balance, transaction, order, query predicate, sort, limit/offset, and
  history-token code.
- Background delivery extension, App Group storage, history token persistence,
  and extension-to-app handoff.
- Financial data display, redaction, logging, analytics, and tests with sample
  data.

## Workflow

1. Confirm FinanceKit data availability and entitlement readiness before
   designing feature behavior.
2. Request authorization only after explaining the user-visible financial data
   task.
3. Scope queries by account, date range, status, type, category, sort, and limit
   rather than fetching broad transaction sets.
4. Persist `HistoryToken` values safely and handle invalidation or restricted
   data by resetting only the affected stream.
5. Keep account balances and credit/debit indicators clear in UI and business
   logic.
6. For background delivery, isolate extension work, share only necessary data
   through App Groups, and handle launch/update frequency constraints.
7. Redact financial data in logs, previews, analytics, and final reports.

## Review Rules

- Do not present FinanceKit as available without entitlement and data
  availability checks.
- Do not store or log raw financial data beyond the feature's explicit need.
- Do not assume authorization remains stable across app launches.
- Do not discard history tokens without a sync-rebuild plan.
- Do not mix StoreKit, PassKit, and FinanceKit responsibilities.
- Treat every entitlement, region, and background delivery claim as
  current-source gated.

## Validation

- Build the affected app and extension targets.
- Test unavailable, restricted, denied, authorized, and revoked authorization
  states when feasible.
- Test account, balance, transaction, order, and history queries with bounded
  predicates.
- Test history-token persistence/invalidation and background delivery handoff
  when in scope.
- Inspect logs/previews/screenshots for accidental financial-data leakage.

## Output

For implementation or review work, return:

1. FinanceKit availability and entitlement status
2. Authorization, query, history, and background-delivery findings
3. Financial-data privacy and display boundaries
4. Validation run or still needed
5. Current-source assumptions for entitlement or regional behavior
