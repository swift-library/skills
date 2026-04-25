# UIKit MVVM

Use MVVM when UIKit modules benefit from an explicit view state object, async
loading boundary, and testable mapping logic.

## Boundaries

- ViewController: binds controls, renders state, forwards user events.
- ViewModel: owns presentation state, view data mapping, validation, async
  loading, and intent methods.
- Domain/services/repositories: injected through protocols or a dependency
  container.
- Coordinator/Router: owns navigation for nontrivial flows.

## Binding Options

- Use simple callbacks/closures for small UIKit modules.
- Use Combine when the project already uses it or state changes are stream-like.
- Avoid adding RxSwift or Combine just to bind one simple request/response
  screen.
- Keep UIKit rendering on MainActor/main thread.

## State

- Expose one view state model when it simplifies rendering.
- Avoid duplicating the same mutable state in both ViewController and ViewModel.
- Keep UIKit types out of reusable ViewModel state when possible.
- Map domain models to display values before rendering.

## Navigation

- ViewModel can expose route intents or navigation closures.
- Do not pass `UINavigationController` into ViewModels.
- For reusable flows, route through a Coordinator.

## Anti-Patterns

- ViewModel imports UIKit to push or present controllers.
- ViewController still owns loading, mapping, and retry logic.
- ViewModel creates concrete live dependencies.
- Bindings are not cancelled and retain the ViewController.
- ViewModel becomes a domain service or cache.

## Testing

- Test ViewModel state transitions with stub repositories.
- Verify initial, loading, success, failure, cancellation, and repeated action
  paths.
- Test route output as values or spy closures.
- Avoid sleeps; use controllable stubs/schedulers.

## PR Checklist

- [ ] ViewController renders state and forwards events.
- [ ] ViewModel owns presentation state and async orchestration.
- [ ] Dependencies are injected.
- [ ] Bindings/subscriptions are cancelled with lifecycle.
- [ ] Navigation leaves ViewModel through values, closures, or protocols.
- [ ] Tests cover state and route outputs.
