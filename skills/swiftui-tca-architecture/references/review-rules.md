# TCA Review Rules

## Common Findings

- Direct side effects in reducers: networking, persistence, analytics, timers,
  dates, UUIDs, or global state.
- Internal action ping-pong used only to share synchronous reducer logic.
- View-owned business logic: the view sequences requests, validates domain
  rules, or mutates feature state outside actions.
- Duplicated local SwiftUI state: `@State` mirrors store state that should be
  canonical in the feature.
- Missing cancellation: long-running, debounced, polling, or restartable work
  cannot be cancelled or replaced.
- Weak action modeling: success/failure/cancel/stale-response paths are hidden
  in closures or booleans.
- Unscoped child features: parent directly edits child internals instead of
  routing child actions through TCA composition.
- Presentation outside state: sheets, alerts, dialogs, or stacks are driven by
  view-only flags when they affect behavior.
- Shared state overuse: `@Shared` hides ownership or persistence instead of
  solving a real shared-value problem.
- Thin tests: no `TestStore` coverage for effect responses, dependency
  overrides, navigation, or presentation.
- Performance traps: full parent stores passed into rows, unstable row
  identity, unbounded streams, or high-frequency actions doing expensive work.

## Scope Limits

Keep these out of TCA review findings and call them out as separate work:

- "Should we adopt TCA?" decisions.
- Ordinary SwiftUI view/layout implementation.
- Visual polish.
- Source-level SwiftUI rendering performance outside reducer/store behavior.
- General Swift Testing mechanics.
- Package target/module structure.

## Review Output

Lead with concrete findings. Each finding should name the broken TCA boundary,
the user-visible or testing risk, and the smallest fix that preserves local
style.

When a finding is easier to explain structurally, use
`closed-loop-examples.md` as the source of example shapes rather than
inventing a long one-off snippet in the response.
