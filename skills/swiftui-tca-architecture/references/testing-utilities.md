# TCA Testing Utilities

Use this for test data, organization, dialog tests, dependency completeness,
isolated capture, and post-effect shared-state assertions.

## Test Data

- Prefer named fixtures for domain models.
- Keep fixtures close to tests unless they are shared across many feature
  tests.
- Use deterministic IDs, dates, and UUIDs.
- Avoid fixture builders that hide the exact state important to the test.
- Prefer constants for IDs used across assertions. A new random UUID per test
  run makes failures harder to read and can hide identity mistakes.
- Use factory helpers for wide models, but override important fields explicitly
  at the call site.

## Test Organization

- Group tests by feature behavior: loading, editing, navigation, presentation,
  sharing, errors, permissions.
- Keep reducer tests near the feature when the repository does that; otherwise
  follow package test target conventions.
- Use short comments only to mark scenario phases in complex tests.
- A `makeStore` helper is useful when it keeps dependency defaults strict and
  visible. It is harmful when it silently installs live-like test behavior.
- Document complex tests by stating the behavior contract, not by narrating
  each assertion.

## Confirmation Dialogs

- Assert dialog state when it appears.
- Send the button action that represents the user choice.
- Assert the destructive or cancel path separately.
- Keep button action naming domain-specific.
- When a dialog action carries a pending ID or item, assert both the dialog
  state and the pending-tracking state clear or persist according to the
  feature contract.
- If the dialog action starts an effect, call `finish` or receive the effect
  output before asserting captured dependency calls.

## Dependency Mocking Completeness

- A dependency touched by the reducer should either be explicitly overridden or
  intentionally fail when called.
- When several dependencies are expected, capture and assert the important
  inputs.
- Do not leave a live preview value active in tests.

## Isolated Capture

Use thread-safe isolated storage for captured dependency input or callback
state when the effect crosses concurrency boundaries. Keep it test-only and do
not use it as a production state transport.

- Use a direct setter when replacing one captured value.
- Use a locked mutation when appending to call history or updating compound
  captured state.
- Prefer asserting captured values after the store has received/finished the
  effect that performs the dependency call.

## Shared State After Effects

When an effect mutates `@Shared`, assert the final shared value after the
effect response or after the store has finished relevant work. Isolate backing
storage and avoid order-dependent tests.

## Summary Checklist

- deterministic initial state,
- explicit dependency overrides,
- no real time sleeps,
- no live services,
- action script matches user behavior,
- state and route assertions cover the feature contract,
- long-running effects finish or cancel.
