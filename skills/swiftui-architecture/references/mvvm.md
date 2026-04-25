# SwiftUI MVVM

Use MVVM for ordinary SwiftUI features that need explicit state, dependency,
and effect boundaries without a reducer framework.

## Boundaries

- View: renders state and forwards user intents.
- ViewModel: owns presentation state, maps domain data, coordinates async work,
  validates input, and exposes intent methods.
- Model/domain: no dependency on View or ViewModel.
- Services/repositories: injected through protocols or local dependency
  containers.

## State Ownership

- Prefer `@Observable` ViewModels with `@State` ownership when the deployment
  target supports Observation.
- Use `ObservableObject`/`@Published` only for legacy targets or Combine/UIKit
  interop.
- Keep canonical state in the ViewModel. Do not mirror the same mutable state
  in both View and ViewModel.
- Derived display values should be computed from canonical state or mapped in a
  focused helper.

## Dependencies And Effects

- Inject repositories/services through the ViewModel initializer.
- Build live dependencies in feature assembly or an app-level composition root.
- Mark UI-facing ViewModels `@MainActor` unless the project uses Main Actor
  default isolation.
- Store and cancel in-flight tasks when a new request supersedes the old one.
- Handle `CancellationError` separately from user-visible failures.

## Navigation

- For pure SwiftUI, model destinations as `Hashable` route values bound to
  `NavigationStack`.
- Keep simple route state in the ViewModel only when it remains feature-local.
- For multi-step or shared flows, move routing to a coordinator/router object
  and inject navigation closures or a small router protocol.
- Do not import UIKit or call `UINavigationController` from a ViewModel.

## Anti-Patterns

- God ViewModel: split domain work into use cases, repositories, or helpers.
- ViewModel creates live network or persistence dependencies directly: inject
  them.
- View performs loading, validation, mapping, or retry policy: move that to the
  ViewModel.
- Duplicate state in View and ViewModel: choose one owner.
- Sleep-based async tests: use controllable stubs or clocks.

## Testing

- Test initial state, success, failure, cancellation, and repeated-intent
  behavior.
- Use stub repositories and explicit clocks where timing matters.
- If the ViewModel is `@MainActor`, run setup and assertions on MainActor.
- Assert state transitions and emitted routes, not SwiftUI rendering details.

## PR Checklist

- [ ] View renders state and sends intents only.
- [ ] ViewModel exposes explicit state and intent methods.
- [ ] Dependencies are injected, not read from app-wide singletons.
- [ ] Async tasks cancel stale requests and handle errors.
- [ ] Navigation is modeled as route state or router closures.
- [ ] Tests cover success, failure, cancellation, and important routes.
