# TCA Shared State

Use this for `@Shared`, `@SharedReader`, app storage, file storage, in-memory
storage, and shared-state test isolation.

## When To Use

Use shared state when multiple features truly share ownership of one value, or
when a value is backed by a supported persistence strategy. Do not use shared
state to avoid parent-child composition, dependency injection, or explicit
delegate outputs.

## App Storage

- Use app storage for small user preferences or settings.
- Keep keys stable and namespaced.
- Avoid storing sensitive data in app storage.
- Tests should isolate or seed the value explicitly.
- For raw-value backed settings, expose type-safe computed properties and keep
  the raw shared value private to the feature state when possible.

## File Storage

- Use file storage for codable domain data that should persist outside the
  feature lifetime.
- Keep file locations and keys centralized.
- Consider migration and failure behavior for existing files.
- Never let tests read or write real user files. Use temporary or in-memory
  storage when available.
- File-backed shared values should have a single named key definition near the
  domain model or persistence boundary. Repeating path construction in many
  features makes migrations and tests fragile.
- File storage requires codable state and should have an explicit default.

## In-Memory Storage

- Use in-memory shared storage for cross-feature state that should not persist
  across app launches.
- Keep lifetime expectations explicit. In-memory sharing can hide ownership if
  used as a global state bag.

## Shared State Between Features

- Parent and child can share a value when both have legitimate ownership.
- If only the parent owns the value, pass child state or delegate actions
  instead.
- If many distant features share the value, verify whether the value is really
  app/session state and whether a dependency client is a better owner.

## Mutations

- Mutate shared values through the wrapper's lock/update API used by the local
  TCA version.
- For collection updates, do the full append/remove/update inside one locked
  mutation.
- If the UI should animate the shared-state change, wrap the mutation in the
  same animation boundary the project uses for ordinary state changes.
- Avoid read-modify-write sequences split across async suspension points.

## Effects And Static Helpers

- Effects can read shared values when the effect's behavior depends on the
  shared value.
- Avoid passing `@Shared` wrappers around as arbitrary parameters. Prefer
  accessing shared state at the feature or helper boundary used by the local
  project.
- Be explicit about whether an effect captures the old value or observes later
  changes.
- A helper can declare the same shared key directly when that makes the helper
  self-contained and avoids capturing `state.$property` only to pass it along.
  Do this only for stable, named shared keys, not anonymous local state.

## Testing

- Seed shared state at the same boundary the feature reads it.
- Assert shared-value mutations when they are the feature output.
- Isolate storage between tests.
- After effect-driven shared mutations, use the local assertion pattern to
  verify the final shared value.

## Review Checks

- Shared state hides ownership that should remain in a parent feature.
- File or app storage keys are duplicated or unstable.
- Tests depend on real persisted data.
- A child feature mutates shared state without the parent feature expecting the
  observable behavior.
- Shared state is used where a dependency client would give clearer behavior.
- Shared mutation is split across multiple actions or tasks and can interleave
  with another mutation.
