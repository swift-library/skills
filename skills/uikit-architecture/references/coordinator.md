# UIKit Coordinator

Use Coordinator when navigation flow ownership, deep links, child flows, or
reusable modules are the main architectural issue.

## Core Responsibilities

- Own one navigation flow.
- Create and connect screens.
- Pass dependencies into feature builders.
- Retain child coordinators until their flow completes.
- Convert route/deep-link inputs into navigation actions.

Coordinators should not own business rules, data fetching, formatting, or view
state.

## Router Wrapper

- Wrap `UINavigationController` or presentation APIs behind a small router when
  it improves testability.
- ViewControllers and ViewModels should receive closures or router protocols,
  not concrete navigation controllers.
- Keep modal, push, pop, and dismissal behavior centralized when it spans more
  than one screen.

## Child Coordinators

- Add child coordinator before `start()`.
- Remove child coordinator on completion or cancellation.
- Pass only the dependencies the child flow needs.
- Avoid parent coordinators reaching into child screen internals.

## Deep Links

- Parse external inputs into app route values.
- Route through the app coordinator so auth, tab selection, and prerequisite
  flows are handled consistently.
- Keep URL parsing and route decisions out of ViewControllers.

## UIKit And SwiftUI

- UIKit coordinator can host SwiftUI screens with `UIHostingController`.
- Inject navigation closures into SwiftUI ViewModels or adapters.
- Keep SwiftUI route state at the SwiftUI boundary when a SwiftUI subtree owns
  its internal flow.

## Anti-Patterns

- Push/present calls scattered across many ViewControllers.
- Coordinator retained only by a local variable.
- ViewModel holds a concrete coordinator and calls arbitrary methods.
- Coordinator fetches data or decides business rules.
- Deep links bypass root flow ownership.

## Testing

- Test navigation by asserting router calls or route state.
- Use spy routers instead of waiting for UIKit presentation timing.
- Test unknown deep links and cancelled child flows.

## PR Checklist

- [ ] Coordinator owns flow and assembly.
- [ ] Child coordinators are retained and released deliberately.
- [ ] ViewControllers/ViewModels receive closures or protocols.
- [ ] Deep links enter through root flow ownership.
- [ ] Coordinator does not own business logic.
