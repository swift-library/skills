# SwiftUI MVI

Use MVI when a SwiftUI feature needs deterministic state transitions and
strict unidirectional data flow without adopting TCA.

## Mental Model

```text
Intent -> Reducer -> State
                 -> Effect -> Action -> Reducer -> State
```

## Core Types

- State: value type holding canonical screen or feature state.
- Intent: user or lifecycle input from the View.
- Action: result from async work, child feature output, or system event.
- Reducer: pure transition logic. It may request an effect but must not perform
  side effects directly.
- Store: owns state, runs reducer/effects, publishes state to SwiftUI.

## SwiftUI Integration

- View reads state from the Store and sends intents.
- Use `@Observable` stores with `@State` on modern targets; keep
  `ObservableObject` when Combine/UIKit interop is required.
- Keep derived view data out of the View when it is part of the state machine.
- Compose child reducers for child feature state and route actions back to the
  parent.

## Effects

- Effects should be explicit and cancellable.
- Inject services, clocks, clients, and repositories into the Store or reducer
  environment.
- Never perform network, database, or timing work inside the reducer branch.
- Include cancellation IDs or request tokens for long-running work.

## When To Prefer

- The feature has many states, events, and edge cases.
- Transitions need deterministic tests.
- The team wants unidirectional flow but does not want a TCA dependency.
- Replay/debug of intents and actions is useful.

## Anti-Patterns

- Reducer performs side effects directly.
- State stores redundant derived values that drift out of sync.
- View mutates state directly instead of sending intents.
- Store becomes a generic app-wide singleton.
- Effects cannot be cancelled or tested deterministically.

## Testing

- Test reducers as pure functions for immediate state changes.
- Test effect output separately with stub services and clocks.
- Cover success, failure, cancellation, repeated intents, and child reducer
  routing.
- Assert the action sequence when async loops matter.

## PR Checklist

- [ ] State, Intent, Action, Reducer, and Store responsibilities are separate.
- [ ] Reducers are deterministic and side-effect free.
- [ ] Effects are injected, cancellable, and testable.
- [ ] Views send intents instead of mutating state directly.
- [ ] Tests cover state transitions and effect result actions.
