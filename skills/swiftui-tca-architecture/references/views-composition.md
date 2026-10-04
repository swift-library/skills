# TCA View Composition Patterns

Use this when a SwiftUI TCA feature owns child features, collections,
optional children, or delegate outputs.

## Collections

- Use `IdentifiedArrayOf<Child.State>` for stable, identifiable child state
  when child reducers need actions.
- Route child actions with `IdentifiedActionOf<Child>` or the local version's
  equivalent.
- Compose child reducers with `.forEach` over the child state and action.
- In views, scope the store collection before `ForEach` rather than manually
  indexing into parent state.

Review for:

- unstable array indices as child identities,
- child state recreated from computed filters,
- broad parent store passed to every row,
- row actions handled by the view instead of the child reducer.

## Filtered Collections

Filtering is a view concern only when it does not affect child identity or
action routing. If filtering changes which child reducer receives actions,
keep the canonical collection in state and derive filtered IDs or filtered
views without losing stable IDs.

## Single Child Features

- Store child state under a named property.
- Route actions through a child action case.
- Compose with `Scope` or the local equivalent.
- Let the child reducer own child internals; the parent observes delegate
  actions or state transitions that form the parent contract.

## Optional Children

- Use optional state for optional child features.
- Compose with `ifLet` or presentation-aware reducers according to whether the
  child is plain optional state or presented UI.
- Clear optional child state through reducer actions, not by view-only flags.
- Cancel child effects when the child disappears if the reducer composition
  does not handle it automatically.

## Delegate Actions

Delegate actions are child outputs meant for a parent. Keep them explicit:

```swift
enum Action {
  case saveButtonTapped
  case delegate(Delegate)

  enum Delegate: Equatable {
    case didSave(Item.ID)
    case didRequestDismissal
  }
}
```

Parent reducers can react to `.child(.delegate(...))` without knowing child
implementation details.

## Review Checks

- Parent handles every child action in a giant switch instead of scoping the
  child reducer.
- Child sends generic `.done` or `.callback` actions that hide the domain
  output.
- Optional child state can survive dismissal.
- Collection child state is derived from a filtered array and loses identity.
