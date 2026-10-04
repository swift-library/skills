# TCA Presentation State

Use this for sheets, popovers, alerts, confirmation dialogs, optional child
features, and destination reducers.

## Destination Management

- Prefer one destination enum when a feature has multiple mutually exclusive
  presentations.
- Use `@Presents var destination: Destination.State?` when the resolved TCA
  version supports it.
- Route actions through `PresentationAction<Destination.Action>` or
  `PresentationActionOf<Destination>` if the local version provides that
  helper.
- Compose with presentation-aware `ifLet` on the destination state.
- Treat a unified destination as the default for a feature that can show a
  sheet, popover, alert, confirmation dialog, or drill-down route one at a
  time. It gives one source of truth, one composition point, and easier tests.
- Multiple presentation properties are a deliberate exception, not the default.
  Use them only when the surfaces are genuinely independent and can be active
  without conflicting.

```swift
@Reducer
struct Parent {
  @ObservableState
  struct State: Equatable {
    @Presents var destination: Destination.State?
  }

  enum Action: Equatable {
    case addButtonTapped
    case destination(PresentationAction<Destination.Action>)
  }

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case .addButtonTapped:
        state.destination = .editor(EditorFeature.State())
        return .none
      case .destination:
        return .none
      }
    }
    .ifLet(\.$destination, action: \.destination)
  }

  @Reducer
  enum Destination {
    case editor(EditorFeature)
  }
}
```

Adjust for local syntax if the project uses older presentation APIs.

## Multiple Presentation Slots

Multiple `@Presents` properties can be valid, but they make it easier to
present conflicting UI. Prefer a unified destination when the presentations are
mutually exclusive or when tests need one route contract.

Separate presentation slots can still make sense for truly independent
surfaces, such as an alert independent of a long-lived child editor. Document
the independence in state shape or tests.

If multiple properties can be non-nil for UI that cannot be displayed together,
that is a state-modeling bug. Convert to a destination enum before adding more
view conditionals.

## Alerts And Confirmation Dialogs

- Model alert/dialog state when button choices feed reducer actions.
- Keep destructive actions explicit in alert actions.
- Clear alert state through presentation actions or the local TCA presentation
  mechanism.
- Do not show reducer-owned alerts from a view-only boolean.

## Sheets, Popovers, And Drill-Down

- Parent owns whether a child is presented.
- Child owns its internal form/loading state.
- Parent handles child delegate output such as save, cancel, or delete.
- Dismissal should cancel or finish child effects when appropriate.
- SwiftUI presentation modifiers should use scoped stores derived from the
  destination case when the local TCA version supports case-scoped bindings.
- Keep the view modifier for each case next to the view that owns the store,
  but keep the decision to present in the reducer.

## Combining Alerts With Destinations

When a child flow can also show alerts, decide the owner:

- child-owned alert for child-local decisions,
- parent-owned alert for decisions that mutate parent domain state,
- app-owned alert for global errors or account/session state.

## Review Checks

- Several optional presentation states can be non-nil for mutually exclusive
  UI.
- View controls presentation state that affects reducer behavior.
- Alert buttons perform work directly in the view.
- Dismissal does not clear child state or cancel child work.
