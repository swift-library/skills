# TCA View Binding Patterns

Use this for SwiftUI view code that renders a `Store` and sends actions.
Ordinary layout and visual polish are out of scope.

## Store-Driven Views

- Inject `StoreOf<Feature>` or the local equivalent into the view.
- Views read store state and send actions; reducers own mutation sequencing.
- Keep expensive formatting or domain rules out of `body`. Move them to state
  helpers, reducers, dependencies, or small view-local helpers when purely
  presentational.
- Scope child stores before passing them to child views.
- Direct state reads such as `store.isLoading`, `store.error`, and
  `store.rows` are fine for rendering. They should not become a place to derive
  business behavior that the reducer cannot test.

```swift
struct SearchView: View {
  @Bindable var store: StoreOf<SearchFeature>

  var body: some View {
    List {
      ForEach(store.scope(state: \.results, action: \.results)) { rowStore in
        ResultRowView(store: rowStore)
      }
    }
    .searchable(text: $store.query.sending(\.queryChanged))
  }
}
```

If the local TCA version uses a different binding helper, follow the nearby
project pattern instead of forcing this syntax.

## Bindings

- Use `BindingReducer` when user-editable state is bound through actions.
- Route mutations through action cases, not through ad hoc view state that
  duplicates feature state.
- Prefer semantic binding actions such as `queryChanged` when the field has
  domain meaning; use a generic `BindingAction<State>` style only when that is
  the local convention.
- Do not bind to derived state unless a setter is well-defined and testable.

## Observation And Local State

- `@Bindable var store` is appropriate when the store participates in SwiftUI
  bindings.
- Local `@State` is acceptable for transient view-only details such as focus,
  scroll position, local animations, or a temporary drag gesture. It should not
  mirror canonical feature state.
- If local state affects reducer behavior, promote it into feature state.
- State-driven animations should key off store state in the view. If the
  animation changes domain state over time, model the timed updates through
  reducer actions and clock dependencies.

## View Actions

- If a view uses `@ViewAction`, send actions through the macro-provided `send`
  route and keep direct `store.send` out of that view style.
- Keep view-action cases focused on user and lifecycle events. The reducer can
  translate them into effect responses or delegate actions.
- Use `.task`, `.onAppear`, and `.onDisappear` to send lifecycle actions when
  the reducer owns the side effect or cancellation.
- For long-lived `.task` work, send an action and let the reducer return the
  effect; do not run the business effect directly in the view.
- Await `store.send(...).finish()` from `.task` when the effect should remain
  alive for the view lifetime and automatically cancel when the task is
  cancelled. The action name is local convention, not a framework requirement.

## Review Checks

- View starts network, persistence, analytics, timer, or domain validation work.
- View owns state that the reducer also owns.
- Binding writes bypass actions.
- `@ViewAction` and direct `store.send` are mixed in the same view without a
  local convention.
- Child views receive broad parent stores instead of scoped stores.
- One-time loading is placed in `.task` but should be idempotent across view
  re-creation, or should instead be triggered by explicit state.
