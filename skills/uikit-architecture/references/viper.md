# UIKit VIPER

Use VIPER when a large or legacy UIKit feature needs strict per-feature
separation and the team accepts the boilerplate.

## Components

- View: renders data and forwards user events.
- Presenter: transforms entities into display output and coordinates View,
  Interactor, and Router.
- Interactor: executes business actions and calls repositories/services.
- Entity: domain feature data, independent of UIKit.
- Router: navigation and module assembly.

Dependency flow:

```text
View -> Presenter -> Interactor -> Repository/Service
Presenter -> Router
Interactor -> Presenter
Presenter -> View
```

## Responsibilities

- View does not call repositories or perform business rules.
- Presenter does not implement business logic directly.
- Interactor does not navigate or update UIKit views.
- Router does not fetch data or make business decisions.
- Entity does not contain display formatting.

## Assembly

- Build View, Presenter, Interactor, Router, and dependencies from an assembly
  function or module builder.
- Keep boundary protocols near the feature module unless local style centralizes
  them.
- Router may be backed by a Coordinator in larger flows.

## SwiftUI Interop

- For UIKit-first modules, wrap SwiftUI screens with `UIHostingController` and
  keep Router/Presenter ownership unchanged.
- For pure SwiftUI migration, reconsider whether VIPER still fits; often
  MVVM, MVI, or TCA is a better target.

## When To Prefer

- UIKit-heavy app has large feature modules.
- Strict role separation is an established team convention.
- Navigation, business actions, and presentation mapping are all complex.
- Test coverage needs separate Presenter and Interactor tests.

## Anti-Patterns

- VIPER for a small one-screen feature.
- Presenter becomes massive because Interactor is underused.
- Interactor performs navigation.
- Router owns business logic.
- Retain cycles between View, Presenter, and Router.

## Testing

- Presenter tests with mocked View, Interactor, and Router.
- Interactor tests with stub repositories/services.
- Router tests with spy navigation wrappers when routing is nontrivial.
- Cover async cancellation and stale-response behavior in Presenter.

## PR Checklist

- [ ] Component responsibilities are respected.
- [ ] Presenter does not own business implementation details.
- [ ] Interactor does not navigate.
- [ ] Router assembles and routes only.
- [ ] Boundary protocols avoid concrete coupling.
- [ ] Tests cover Presenter and Interactor contracts.
