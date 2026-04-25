# Clean Architecture For UIKit

Use this when UIKit presentation should be separated from domain rules and
replaceable infrastructure.

## Dependency Rule

Dependencies point inward:

```text
UIViewController -> Presenter/ViewModel -> Use Case -> Repository Protocol
Data Adapter -> Repository Protocol
```

Domain entities and use cases must not import UIKit, persistence frameworks, or
networking clients unless the repository has a local exception.

## Layers

- Domain entities: business data and invariants.
- Use cases: application actions.
- Repository protocols: domain/application boundaries.
- Data adapters: API, persistence, cache, or platform implementations.
- UIKit presentation adapter: Presenter, ViewModel, or VIPER Presenter.

## UIKit Adapter

- ViewController renders view data and forwards events.
- Presenter/ViewModel calls use cases and maps results to view state/commands.
- Router/Coordinator handles navigation.
- Concrete repositories are assembled outside the presentation object.

## DTO Mapping

- Convert API/persistence DTOs at repository boundaries.
- Keep transport and persistence details out of presentation state.
- Map domain errors to presentation/user-visible errors at the adapter layer.

## Async And Cancellation

- Use cases should be async and cancellation-friendly.
- Presenter/ViewModel cancels stale requests and guards UI updates.
- Data adapters should not assume main thread unless UI-bound.

## When To Prefer

- Domain logic must be tested without UIKit.
- Multiple presentation surfaces share the same use cases.
- Live infrastructure should be swappable.
- Existing controllers mix business rules with data access.

## Anti-Patterns

- ViewController calls concrete API or database clients.
- Use case returns UIKit-specific strings, colors, or images.
- Domain entity imports UIKit.
- Repository leaks DTOs to presentation.
- Tests require real infrastructure for domain behavior.

## PR Checklist

- [ ] Dependency direction points inward.
- [ ] Domain/use case layer is UIKit-independent.
- [ ] Repository protocols define the boundary.
- [ ] Data adapters map DTOs to domain types.
- [ ] Presenter/ViewModel owns presentation mapping and cancellation.
- [ ] Tests cover use cases with stub repositories.
