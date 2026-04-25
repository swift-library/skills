# SwiftUI TCA

Use TCA when the project already uses The Composable Architecture, explicitly
accepts the dependency, or needs strong feature composition and deterministic
effect testing.

## Feature Shape

- Prefer modern TCA with `@Reducer` and `@ObservableState` when available.
- State owns canonical feature state and navigation state.
- Action enumerates user events, lifecycle events, child actions, and effect
  responses.
- Reducer mutates state and returns effects.
- Dependencies are accessed through TCA dependency values, not singletons.

## SwiftUI Views

- In modern TCA, use `@Bindable var store: StoreOf<Feature>` when bindings are
  needed.
- Views should send actions and render store state.
- Avoid putting business logic, request orchestration, or mutation sequencing in
  the View.
- Use scoped stores for child features.

## Effects And Cancellation

- Effects should be explicit and cancellable.
- Use dependency clients for network, persistence, clocks, UUIDs, dates, and
  environment values.
- Model loading, success, failure, and cancellation paths in Actions.
- Avoid fire-and-forget effects unless the result truly does not matter.

## Navigation

- Model navigation in state.
- Prefer modern TCA navigation tools already used by the project.
- Scope child state/actions for child screens.
- Do not push/present imperatively from reducers.

## When To Prefer

- The codebase is already TCA-based.
- Child feature composition is important.
- Tests need deterministic action/effect assertions with `TestStore`.
- The team accepts the learning curve and dependency.

## Anti-Patterns

- Adding TCA to a small feature only to replace simple MVVM.
- Reducer performs direct side effects.
- Dependencies bypass TCA dependency injection.
- View owns local mutable state that duplicates feature state.
- Navigation happens outside state and is hard to test.

## Testing

- Use `TestStore` for action/state/effect assertions.
- Override dependencies for success, failure, cancellation, dates, UUIDs, and
  clocks.
- Assert child feature actions and navigation state when they are part of the
  feature contract.

## PR Checklist

- [ ] State and Action model the feature explicitly.
- [ ] Reducer avoids direct side effects.
- [ ] Dependencies are injected through TCA dependency values.
- [ ] Effects cover success, failure, and cancellation.
- [ ] Navigation is modeled in state.
- [ ] Tests use `TestStore` for core behavior.
