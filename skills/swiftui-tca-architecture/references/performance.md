# TCA Performance

Use this for source-level TCA performance review before escalating to
Instruments. General SwiftUI rendering outside TCA state/store behavior is out
of scope.

## State Updates

- Keep state mutations minimal and localized.
- Avoid recomputing expensive derived values on every action.
- Store expensive derived results only when they represent real cached state;
  otherwise make cheap computed properties.
- Avoid replacing large state subtrees when a small mutation is enough.
- Use computed properties for cheap formatting/filtering. Store the result only
  when the computation is expensive, externally meaningful, or needed to avoid
  repeated work across many views/actions.
- For large collections, update by stable ID instead of rebuilding the entire
  array when possible.

## Sharing Reducer Logic

- Do not send internal actions only to share synchronous logic.
- Prefer reducer helper methods that take `inout State` and return an effect
  when needed.
- Keep helper methods deterministic and dependency-aware.
- Tests should read as user actions and effect responses, not as internal
  helper-action choreography.

## Effects

- Debounce, throttle, or cancel user-driven repeated effects such as search.
- Avoid starting duplicate long-running effects for repeated lifecycle actions.
- Use streams carefully; ensure they cancel when the feature disappears.
- Move CPU-heavy work behind a dependency or off the main actor when
  appropriate, then return a typed action.
- For CPU-heavy transformations, capture input, run work off the reducer path,
  and send a result action. Reducers should not block the main actor with
  parsing, scoring, image work, or large diff computation.

## Reducer Composition

- Scope child reducers so parent reducers do not switch over every child
  implementation action.
- Avoid broad parent state observation when only child state is needed.
- Keep reducer bodies readable; split features when one reducer owns unrelated
  workflows.

## High-Frequency Actions

- High-frequency UI input should not trigger expensive reducer work on every
  event unless that is the product behavior.
- Coalesce or debounce where user-visible behavior allows it.
- Avoid analytics or persistence writes on every keystroke unless deliberately
  required.
- For sliders, text fields, drag gestures, and sensors, separate fast local UI
  responsiveness from slower effects. Persist or sync at commit/debounce
  boundaries when possible.

## Store Scoping

- Pass scoped stores to child views.
- Avoid giving a row view access to the full parent store.
- Keep row identity stable.
- Watch for computed child state that changes identity and causes unnecessary
  view invalidation.
- If a child view only needs row state/actions, scope to the row. Broad stores
  make unrelated parent state changes invalidate many children.

## Memory

- Effects should not strongly retain long-lived objects unnecessarily.
- Long-running streams and tasks need cancellation paths.
- Large cached data should live behind dependencies or shared storage when the
  feature does not own it.

## Async/Await

- Avoid blocking the main actor in effects.
- Keep UI state mutations in reducer actions.
- Use dependencies to isolate actor-bound services.
- If an async dependency is slow and repeatable, model loading and cancellation
  explicitly.

## Review Checks

- Internal action ping-pong for shared logic.
- Full parent store passed to many child views.
- Large arrays replaced for tiny row changes.
- Debounced work lacks cancellation.
- Real-time streams continue after dismissal or pop.
