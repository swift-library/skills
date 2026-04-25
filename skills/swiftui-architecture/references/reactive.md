# Reactive Overlay For SwiftUI

Use this when a SwiftUI feature is stream-heavy: search, live feeds, realtime
updates, debounce/throttle behavior, or multi-source event pipelines.

Reactive is usually an overlay inside MVVM, MVI, or TCA, not a replacement for
feature boundaries.

## Placement

- Keep Combine/Rx pipelines in ViewModels, Stores, Presenters, or dependency
  clients.
- Views bind to state and send intents; they do not assemble pipelines.
- Inject schedulers/clocks for deterministic tests.
- Convert stream output into explicit state transitions.

## Combine Guidance

- Debounce search and validation streams at the feature boundary.
- Use `removeDuplicates()` when repeated input should not trigger work.
- Switch to latest request behavior for typeahead or superseded loads.
- Treat errors as state transitions; do not terminate a long-lived UI pipeline
  unless that is the desired UX.
- Cancel subscriptions with the feature lifecycle.

## RxSwift Notes

- Follow the project's existing Rx conventions if already present.
- Keep dispose bags owned by the feature object or view controller boundary.
- Do not add RxSwift to a Combine/async-await codebase without explicit
  approval.

## Async/Await Interop

- Prefer async/await for simple request/response work.
- Use streams when repeated values, cancellation, or backpressure matter.
- Bridge to `AsyncSequence` when it reduces framework coupling and local
  deployment targets support it.

## Anti-Patterns

- View body creates subscriptions.
- Pipeline captures `self` strongly and outlives the feature.
- Network errors terminate the only stream and leave UI stuck.
- Tests rely on wall-clock sleeps.
- Reactive layer bypasses the architecture state model.

## Testing

- Inject test schedulers or clocks.
- Assert debounced output, cancellation, failure state, and repeated input
  behavior.
- Keep stream tests focused on observable state, not implementation operators.

## PR Checklist

- [ ] Pipelines live outside Views.
- [ ] Scheduling is injectable or deterministic.
- [ ] Errors map to recoverable state.
- [ ] Subscriptions/tasks are cancelled with feature lifetime.
- [ ] Stream output enters the same state model as other feature events.
