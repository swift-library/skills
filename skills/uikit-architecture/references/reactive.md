# Reactive UIKit Architecture

Use this when UIKit behavior is stream-heavy: search, validation, live feeds,
realtime updates, or multi-source event pipelines.

Reactive is usually an overlay inside MVP, MVVM, VIPER, or Clean Architecture.

## Placement

- Keep Combine/Rx pipelines in Presenters, ViewModels, Interactors, or
  dependency clients.
- ViewControllers bind controls and render outputs; they do not own business
  pipelines.
- Inject schedulers/clocks where possible.
- Convert stream output into explicit view state or Presenter commands.

## Combine

- Store cancellables at the feature object or ViewController boundary.
- Use debounce/throttle for search and validation.
- Use switch-to-latest behavior for superseded requests.
- Map errors to recoverable UI state.
- Avoid terminating long-lived UI pipelines unless the screen should stop
  receiving values.

## RxSwift

- Follow local Rx conventions when present.
- Dispose subscriptions with the correct lifecycle owner.
- Do not add RxSwift to a Combine/async-await codebase without explicit
  approval.

## Anti-Patterns

- ViewController assembles complex pipelines inline.
- Subscriptions retain ViewController after dismissal.
- Errors terminate the only pipeline and leave UI stale.
- Tests rely on wall-clock sleeps.
- Reactive output bypasses Presenter/ViewModel state.

## Testing

- Use test schedulers or deterministic stubs.
- Assert debounced output, cancellation, failure state, and repeated input
  behavior.
- Test Presenter/ViewModel output, not private operator chains.

## PR Checklist

- [ ] Pipelines live in presentation/domain boundary objects, not View code.
- [ ] Scheduling is deterministic in tests.
- [ ] Errors map to recoverable view state or commands.
- [ ] Subscriptions are cancelled/disposed with lifecycle.
- [ ] Stream output flows through the module architecture.
