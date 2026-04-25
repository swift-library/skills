# UIKit Architecture Selection

Use this file when no architecture has been chosen or when a requested
architecture needs a fit check.

## Fit Matrix

| Pattern | Best fit | Avoid when |
|---|---|---|
| MVC cleanup | Small refactor of a large UIViewController | The module needs durable test boundaries |
| MVP | Passive ViewController, direct Presenter testability, low ceremony | Observable state binding is already the local standard |
| MVVM | UIKit feature state, async loading, cell/view data mapping | ViewModel starts owning UIKit navigation directly |
| VIPER | Large UIKit modules with strict role separation | Small feature where boilerplate will dominate |
| Coordinator | Navigation flow ownership, deep links, reusable flows | Used as a replacement for presentation/domain boundaries |
| Clean Architecture | Domain/data isolation and replaceable infrastructure | Presentation-only refactor |
| Reactive | Search, live feeds, realtime updates, event pipelines | Simple request/response async work is enough |

## Decision Flow

1. If local modules already use a clear pattern, prefer it.
2. If the controller is simply too large, start with MVC cleanup and extract
   collaborators before introducing a named architecture.
3. If UIKit ViewControllers should be fully passive and Presenter tests are the
   priority, choose MVP.
4. If state and rendering are easier as a view state object, choose MVVM.
5. If the module needs strict per-feature role separation, choose VIPER.
6. If navigation is scattered across view controllers, add Coordinator.
7. If domain/data isolation is the core issue, add Clean Architecture layers.
8. If behavior is stream-heavy, add Reactive pipelines inside Presenter or
   ViewModel.

## Fit Check

For an explicit user-requested architecture, check:

- Existing architecture nearby.
- UIKit vs mixed SwiftUI ownership.
- Size and lifetime of the feature.
- Navigation and deep-link complexity.
- Async/effect and cancellation requirements.
- Testing goals and team familiarity.
- Framework dependency tolerance.

Return `fit` when the pattern solves the current risk with reasonable ceremony.
Return `mismatch` when a smaller extraction, MVP/MVVM, or Coordinator layer
would solve the problem with less churn.

## Common Combinations

- MVP + Coordinator: passive ViewControllers plus centralized navigation.
- MVVM + Coordinator: ViewModels own state, coordinators own flow.
- VIPER + Coordinator: Router may be backed by a coordinator hierarchy.
- Clean Architecture + MVP/MVVM/VIPER: domain/data layers plus a presentation
  adapter.
- MVVM/MVP + Reactive: presentation object owns Combine/Rx pipelines.
