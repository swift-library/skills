# SwiftUI Navigation And Coordinator

Use this when the primary architectural problem is flow ownership, deep links,
or navigation reuse across screens.

## Core Rule

Coordinator is a navigation layer, not a complete architecture. Pair it with
MVVM, MVI, TCA, Clean Architecture, or the project's existing presentation
pattern.

## Pure SwiftUI

- Model destinations as `Hashable` route values.
- Bind route state to `NavigationStack(path:)`.
- Use optional enum state for sheets and full-screen covers.
- Keep route construction close to the composition root when dependencies are
  needed to build child screens.
- Expose intent methods or closures from feature state objects instead of
  letting Views mutate shared routers directly.

## Mixed UIKit/SwiftUI

- If UIKit owns the root navigation controller, let a UIKit coordinator own the
  flow and host SwiftUI screens with `UIHostingController`.
- Inject navigation closures or small router protocols into SwiftUI ViewModels.
- Do not pass `UINavigationController` into SwiftUI ViewModels.
- Keep SwiftUI route values and UIKit route APIs mapped at the boundary.

## Deep Links

- Parse URLs or activity inputs into app route values.
- Let the app coordinator or root router decide whether prerequisites such as
  auth or tab selection are needed.
- Keep deep-link parsing out of individual Views.
- Test unknown or partial links as no-op/error paths.

## Anti-Patterns

- Navigation logic is scattered across View bodies.
- ViewModels import UIKit to push or present controllers.
- Global router singleton is mutated from unrelated features.
- Coordinator fetches data or applies business rules before routing.
- Destination state duplicates the same selection in multiple owners.

## Testing

- Assert route state changes for user intents.
- Test deep-link mapping separately from rendering.
- For UIKit-hosted flows, use a spy router/navigation wrapper rather than
  waiting for UIKit presentation timing.

## PR Checklist

- [ ] Navigation ownership is explicit.
- [ ] Routes are value types for pure SwiftUI navigation.
- [ ] SwiftUI ViewModels depend on closures/protocols, not UIKit types.
- [ ] Deep links route through an app/root coordinator.
- [ ] Coordinators do not own business logic.
