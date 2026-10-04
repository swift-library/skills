# Reference Index

Use this index only when `SKILL.md` routing is not enough.

## Feature Shape

- `reducer-structure.md`: feature shape, state/action organization, result
  actions, reducer enums, and macro/version choices.
- `views-binding.md`: store-driven views, `@Bindable`, binding actions,
  observation, lifecycle actions, and `@ViewAction`.
- `views-composition.md`: `IdentifiedArrayOf`, `ForEach`, child scopes,
  optional children, and delegate actions.

## Effects And Dependencies

- `effects.md`: `.run`, `.send`, error handling, composition, cancellation,
  timers, lifecycle effects, and state capture.
- `dependencies.md`: dependency clients, `@Dependency`, `@DependencyClient`,
  test/preview values, streams, errors, and concurrency.

## Navigation, Presentation, And Shared State

- `navigation-basics.md`: `StackState`, `StackActionOf`, path reducers,
  push/pop, dismiss, and child route actions.
- `navigation-advanced.md`: mixed stack/sheet flows, deep links, path
  inspection, external events, and recursive routes.
- `presentation.md`: `@Presents`, destination enums, alerts, sheets, popovers,
  confirmation dialogs, and multiple presentation states.
- `shared-state.md`: `@Shared`, `@SharedReader`, app storage, file storage,
  in-memory storage, effects, and shared-state tests.

## Testing

- `testing-fundamentals.md`: `TestStore` setup, Equatable state, naming, and
  dependency overrides.
- `testing-patterns.md`: action, state, dependency, error, async,
  presentation, navigation, and shared-state test scripts.
- `testing-advanced.md`: given/when/then, state machines, edge cases, time
  control, key-path receive helpers, and exhaustivity choices.
- `testing-utilities.md`: test data, organization, confirmation dialogs,
  dependency completeness, `LockIsolated`, and post-effect shared-state
  assertions.

## Performance, Examples, And Review

- `performance.md`: reducer logic sharing, computed state, high-frequency
  actions, store scoping, memory, and async performance.
- `closed-loop-examples.md`: compact complete examples when isolated rules are
  not enough.
- `review-rules.md`: common TCA review findings, scope limits, and review
  output shape.
