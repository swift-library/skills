# Clean Architecture For SwiftUI

Use this when a SwiftUI feature needs domain/data isolation, replaceable
infrastructure, or a shared domain model across multiple UIs.

## Dependency Rule

Dependencies point inward:

```text
SwiftUI View -> ViewModel/Presenter Adapter -> Use Case -> Repository Protocol
Data Adapter -> Repository Protocol
```

Domain entities and use cases must not import SwiftUI, UIKit, persistence, or
networking frameworks unless the repository already has a different local rule.

## Layers

- Domain entities: business data and invariants.
- Use cases: application actions that coordinate domain operations.
- Repository protocols: boundaries owned by the domain/application layer.
- Data adapters: API, persistence, cache, or platform implementations.
- Presentation adapter: SwiftUI ViewModel, Store, or Presenter that maps use
  case results into view state.

## SwiftUI Adapter

- Keep Views declarative and free of repository/use-case calls.
- Put loading, retry, validation, mapping, and cancellation in the adapter.
- Inject use cases or a dependency container into the adapter.
- Expose view-ready state, not transport DTOs.

## DTO Mapping

- Convert network/persistence DTOs at the boundary.
- Keep transport errors and persistence details out of SwiftUI state unless
  they are intentionally user-visible.
- Prefer domain errors or presentation errors for UI messaging.

## Async And Cancellation

- Use cases should be async and cancellation-friendly.
- Presentation adapters cancel stale tasks and handle `CancellationError`
  separately.
- Repositories should not assume MainActor unless their implementation is
  UI-bound.

## When To Prefer

- Domain rules are important and reused.
- Multiple UI surfaces share the same use cases.
- Infrastructure may be swapped or tested independently.
- Live API/persistence should not leak into presentation code.

## Anti-Patterns

- ViewModel calls a concrete `LiveRepository` or API client directly.
- Domain entities import SwiftUI/UIKit.
- DTOs are shown directly in SwiftUI views.
- Use cases return view-specific strings or colors.
- Tests hit real infrastructure for domain behavior.

## PR Checklist

- [ ] Dependency direction points inward.
- [ ] Domain entities and use cases are UI-framework independent.
- [ ] Repository protocols sit at the domain/application boundary.
- [ ] Data adapters map DTOs to domain types.
- [ ] SwiftUI adapter owns presentation state and cancellation.
- [ ] Tests can cover use cases with stub repositories.
