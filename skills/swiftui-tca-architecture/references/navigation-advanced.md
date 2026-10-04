# TCA Navigation Advanced Patterns

Use this for mixed navigation, deep links, external events, route inspection,
and recursive flows.

## Mixed Stack And Presentation

A feature can own both a stack path and a presentation destination when the UI
really has both concepts. Keep them separate in state and actions:

- `path` for pushed screens.
- `destination` or named optional state for modal/alert/popover presentation.
- parent reducer logic decides which route opens for a user intent.
- tests assert both path and presentation transitions.

Avoid one generic route enum that mixes stack elements and modal state unless
nearby code already proves that shape works.

## Deep Links

- Parse external URLs or notifications outside the reducer when parsing needs
  host services, then send a domain action with route intent.
- Reducers translate deep-link intent into state: selected tab, path elements,
  presented destination, loaded IDs, or pending route state.
- If a deep link requires data loading, model the loading and response actions
  explicitly before completing the route.
- Reject impossible or unauthorized routes by state, not by silently doing
  nothing in the view.

## External Events

External events such as push notifications, handoff, widgets, or app delegate
callbacks should enter through app-level actions and flow down to the owning
feature. Avoid letting a view singleton mutate a child stack directly.

## Path Inspection

Path inspection is acceptable when parent behavior depends on the current top
screen or an existing route. Keep it narrow:

- prefer high-level route predicates over switching on deep child internals,
- avoid mutating a child state only because it is reachable in the path,
- test the route condition that drives the parent behavior.

## Recursive Navigation

Recursive flows need strict identity and cancellation discipline. Each pushed
feature should own its own state and effects; parent-level shared dependencies
or shared state should carry only the cross-cutting domain data.

## Review Checks

- Deep links push views instead of constructing feature state.
- A modal and a stack screen fight over the same state slot.
- External events mutate navigation from outside the store.
- Path inspection reaches too deeply into child implementation state.
- Recursive route effects survive after the route is popped.
