# TCA Navigation Basics

Use this for stack navigation, push/pop, dismiss, and child route actions.

## Stack Navigation

- Model stack navigation with `StackState<Path.State>` when the flow is a
  push-style stack.
- Route stack actions through `StackActionOf<Path>` or the local equivalent.
- Compose the path reducer with `.forEach` over the path state and action.
- In SwiftUI, derive the path binding from the store using the modern
  `$store.scope(state:action:)` integration when supported.

```swift
@Reducer
struct Feature {
  @ObservableState
  struct State: Equatable {
    var path = StackState<Path.State>()
  }

  enum Action: Equatable {
    case path(StackActionOf<Path>)
    case itemTapped(Item.ID)
  }

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case let .itemTapped(id):
        state.path.append(.detail(DetailFeature.State(id: id)))
        return .none
      case .path:
        return .none
      }
    }
    .forEach(\.path, action: \.path) {
      Path()
    }
  }

  @Reducer
  enum Path {
    case detail(DetailFeature)
  }
}
```

Use slash-case-path syntax if the local project has not migrated to macro
case-key paths.

## Push And Pop

- Push by appending path state in the reducer.
- Pop by mutating path state or by allowing the SwiftUI binding to send path
  actions.
- Programmatic dismiss inside a child can use the local TCA dismiss dependency
  pattern when that is already used.
- Avoid direct imperative navigation in views when the route is feature
  behavior.

## Handling Child Actions

- Parent reducers can inspect path actions to handle child delegate outputs.
- Keep delegate outputs narrow. The parent should not switch over every child
  implementation action.
- When a child requests dismissal, let the parent mutate path/presentation
  state or use the local dismiss dependency pattern.

## Enum Reducer Conformance

Path reducers are often reducer enums where each case wraps a child feature.
This keeps the stack closed and testable. If the set of destinations is open or
plugin-driven, do a local architecture check before forcing an enum.

## Review Checks

- Navigation state lives only in the view.
- Stack path contains view models or views instead of feature state.
- Child routes are pushed without stable identity.
- Parent handles child implementation actions instead of delegate actions.
