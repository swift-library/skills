# TCA Testing Patterns

Use this for concrete test scripts: actions, state, dependencies, errors,
async effects, presentation, navigation, and shared state.

## Action Testing

- Send a user or lifecycle action.
- Assert the state mutation caused by that action.
- Receive effect actions in the order the feature promises.
- Avoid asserting internal helper actions unless they are public behavior.
- When an action intentionally returns an effect but does not immediately
  mutate state, send it without a state assertion and then receive the effect
  output.

## Success Flow

Test success flows by asserting loading state, dependency input, response
action, and final state. If the feature can receive stale responses, include
the request identity in the response action and test the stale case.

## Delegate Actions

For child features, send child actions through the child store or scoped parent
action, then receive/assert the delegate output that the parent observes.
Parent tests should not assert child internals beyond the parent contract.

## State Verification

- Assert direct state changes in `send`/`receive` closures.
- Test computed properties separately only when they contain domain logic.
- Keep snapshots out of reducer tests unless local convention requires them.

## Dependency Testing

- Capture dependency inputs with isolated test storage when needed.
- Assert call counts only when repeated calls are user-visible or expensive.
- Test multiple dependencies together when their ordering matters; otherwise
  keep them separate.
- If an action calls several dependencies, override all of them in the test and
  assert the important inputs for each. Missing overrides should fail loudly.

## Error Testing

- Throw or return domain failures from dependency overrides.
- Assert loading cleanup, alert state, retry affordances, and retained input.
- Test recovery by sending the retry or dismiss action.

## Presentation Testing

- Assert destination state when presentation opens.
- Send presentation child actions through `PresentationAction`.
- Assert dismissal clears state and handles delegate output.
- Test alert/dialog button actions when they mutate state or start effects.

## Navigation Testing

- Assert `StackState` after pushes, pops, and deep links.
- Drive child path actions through `StackAction`.
- Test child delegate outputs that pop, replace, or append routes.

## Async Testing

- Use deterministic dependency responses.
- Use `TestClock` for timers, debounce, throttle, delay, and polling.
- Finish or cancel long-running effects.
- Do not use wall-clock sleeps in tests.

## Shared State Testing

- Seed shared state explicitly.
- Assert mutations after sends or receives.
- Isolate persistence between tests.
- Test both features when shared state is the integration contract.
- If the repository uses dependency/test traits for shared-state isolation,
  use them consistently. Otherwise create isolated keys, temporary files, or
  in-memory storage per test.
- For effect-driven shared mutations, assert the ordinary reducer state first,
  then finish/receive the effect and assert the shared value after the effect
  has had a chance to run.
