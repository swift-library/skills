# SwiftUI App Wiring And Routing Patterns

Use this file for pattern-level SwiftUI app shell, TabView, NavigationStack,
and deep-link wiring when the project's architecture is already established.
Choosing, migrating, or validating an app-wide architecture is out of scope.

## App Shell

- Keep the app entry point small: construct long-lived dependencies, inject
  environment values, and hand off screen composition to root views.
- Avoid doing network fetches, persistence migrations, or navigation decisions
  directly inside the `App` body.
- Prefer explicit dependency containers or environment keys over global
  singletons when a dependency is shared across multiple screens.
- Keep preview and test dependency graphs easy to replace.

## TabView

- Treat each tab as a stable feature surface with its own root view.
- Give tabs independent navigation state when each tab needs its own back
  stack.
- Keep tab selection side effects explicit; do not hide major behavior inside a
  binding setter.
- Avoid recreating tab roots just to reset navigation unless the reset is a
  deliberate user action.

## NavigationStack

- Prefer typed routes or values over stringly typed route identifiers.
- Centralize destination mapping at the feature boundary that owns the route.
- Keep child views focused on emitting navigation intent, not constructing
  unrelated destination graphs.
- Use stable route values so restoration, deep links, and repeated pushes do
  not depend on transient view state.

## Deep Links

- Parse external URLs into domain-level route intents before touching SwiftUI
  navigation state.
- Validate required IDs, permissions, and feature availability before pushing a
  destination.
- Route through the same destination mapping used by in-app navigation.
- If a deep link crosses tabs, select the tab first, then update that tab's
  navigation path.

## Sheet And Modal Wiring

- Prefer item-driven or enum-driven sheet destinations over many boolean flags.
- Let sheets own their save/cancel actions when the action belongs to the modal
  task.
- Use sheet-local navigation when the modal flow has multiple steps.
- Keep global sheet routers narrow; if every feature writes to the same router,
  the router has become architecture, not a local pattern.

## Boundary Checks

- If the work changes feature ownership, dependency lifetime, state model, or
  navigation architecture, treat it as architecture work, which is out of
  scope.
- If the work is only wiring a known TabView, NavigationStack, deep link, or
  sheet pattern into existing architecture, keep it here.
- If source-level performance symptoms appear during routing changes, treat
  dedicated performance diagnosis and remediation as out of scope.
