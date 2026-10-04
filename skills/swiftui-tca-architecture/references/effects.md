# TCA Effects

Use this for async work, cancellation, timers, effect composition, and reducer
side-effect boundaries.

## Basic Effects

- Return `.none` when an action only mutates state.
- Use `.send` for an immediate follow-up action only when that action is part
  of the observable feature script. Do not use `.send` just to share
  synchronous reducer logic.
- Use `.run { send in ... }` for async work that can emit actions.
- Capture values from state before entering async work.

```swift
case .refreshButtonTapped:
  let query = state.query
  state.isLoading = true
  return .run { send in
    await send(.response(Result { try await client.search(query) }))
  }
```

## Error Handling

- Represent user-visible failures in actions and state.
- Prefer `Result` response actions or typed domain error wrappers when the
  feature must distinguish failure kinds.
- Do not swallow errors in effects when the UI needs to clear loading, show an
  alert, or retry.
- Keep raw transport errors behind dependency clients when the UI only needs a
  domain-level failure.
- Use the `.run` catch handler when the failure path should send a separate
  action and the operation body is clearer without wrapping every call in
  `Result`.
- It is acceptable to catch and report non-critical errors without sending an
  action only when the reducer state truly does not need to change.

## Composition

- Use `.merge` for independent concurrent effects.
- Use `.concatenate` when ordering matters and the next effect should start
  only after the previous effect completes.
- Prefer helper methods returning `Effect<Action>` when many actions share the
  same mutation/effect sequence.
- Avoid effect chains that bounce through private actions only to reuse code.

## Cancellation

- Add cancellation IDs for debounced searches, timers, streams, polling, and
  user-restartable work.
- Use `cancelInFlight` for interactions where a newer request supersedes an
  older one.
- Use `.cancel(id:)` for explicit stop actions.
- Ensure child feature effects cancel on dismissal/pop when that behavior
  matters and is not already handled by the composition operator.

## View Lifecycle Effects

- Views may send lifecycle actions from `.task`, `.onAppear`, and
  `.onDisappear`.
- Reducers should decide whether a lifecycle action starts, restarts, or
  cancels work.
- Long-running view lifetime effects should be cancellable by identity.
- For view-lifetime streams, the common shape is a view `.task` that awaits
  `store.send(...).finish()`. The action name is project-local; `runTasks` is a
  convention, not a TCA API.
- Use `.onAppear` for one-shot initial work and `.task` for work that should
  stay alive until the view disappears.

## Timers And Clocks

- Use clock dependencies so tests can advance time deterministically.
- Do not use real sleeps in tests.
- For animations, keep animation concerns at the view boundary unless reducer
  state must change over time.
- For repeating timers, capture whether the timer should start before entering
  the effect and attach a cancellation ID with `cancelInFlight` when repeated
  starts should replace the old timer.
- For countdown timers, send a completion action and cancel the timer when the
  duration reaches zero.
- If the timer emits animated state transitions, send the tick action with
  animation only when the local TCA version and UI convention support it.

## State Capture

- Capture IDs, queries, form values, and request tokens before the effect.
- Include identity in response actions when multiple requests can race.
- On response, verify the response still belongs to the current state before
  applying it.
- Capture multiple values explicitly, including filters and sort order, so the
  effect records the user intent at the time it started.
- For conditional effects, capture the condition and branch inside the effect
  only when the branch depends on the state at start time. If the branch should
  reflect later state, model that later state through another action.

## Review Checks

- Reducer performs side effects directly.
- Effect reads mutable state after suspension.
- Loading state is not cleared on failure or cancellation.
- Long-running effects have no cancellation path.
- Tests do not receive or finish effect-emitted actions.
