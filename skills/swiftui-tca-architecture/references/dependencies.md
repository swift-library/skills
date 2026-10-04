# TCA Dependencies

Use this for dependency clients, live/test/preview values, streams, typed
errors, and Swift concurrency boundaries.

## Dependency Access

- Reducers access external systems with `@Dependency`, not global singletons.
- Dependencies cover clients, clocks, dates, UUIDs, dismiss, persistence,
  analytics, location, notifications, and other host services.
- Keep live implementations out of reducers. Reducers should call a small
  client surface that returns domain values or async streams.
- If a project already uses `@DependencyClient`, follow that style. Otherwise
  use manual dependency keys and `DependencyValues` extensions as nearby code
  does.

## DependencyClient Macro

- Use `@DependencyClient` when the project already supports the dependencies
  macros and the client is a bag of sendable operations.
- The practical value is not just less boilerplate: generated test defaults
  catch unmocked calls and avoid older Swift 6 workarounds around manually
  shared unimplemented clients.
- Keep the client `Sendable` and make async operations `@Sendable`.
- Still define the live value and dependency values entry in the style used by
  the package.

## Client Shape

- Make operation names domain-specific.
- Prefer async functions and `AsyncSequence` streams for Swift concurrency
  code.
- Return domain models and domain errors rather than low-level SDK response
  types when the feature does not need SDK details.
- Keep cancellation behavior clear: async functions should cooperate with task
  cancellation and streams should finish when cancelled.

```swift
struct SearchClient {
  var search: @Sendable (String) async throws -> [SearchResult]
  var suggestions: @Sendable (String) -> AsyncStream<[Suggestion]>
}
```

## Typed Errors

- If feature tests need equatable errors, wrap underlying errors into a domain
  error that can be compared by stable fields such as code, category, or debug
  description.
- Avoid exposing arbitrary SDK errors in state only to make tests compile.
- If using typed throws in a dependency client, keep the reducer response
  action typed to the same domain error.
- For non-user-visible diagnostics, report/log inside the dependency or catch
  path and send only the state transition the feature owns.

## Swift 6 And Sendability

- Make dependency operations `@Sendable` when they cross effect/task
  boundaries.
- Avoid capturing non-sendable mutable references in `.run` effects.
- Use isolated containers only for tests or thread-safe state capture; do not
  smuggle app state through them.

## Test Values

- Tests should override every dependency a path can touch.
- Use failing/unimplemented defaults for dependencies that should not be
  called.
- Verify client input when it matters, not only reducer output.
- Use clocks, UUIDs, and dates from dependencies so assertions are stable.
- When adding a new dependency call to a reducer, grep existing feature tests
  and add the matching override in every path that can execute that action.

## Preview Values

- Preview values should be fast, deterministic, and local.
- Do not call production network, file, or account services from previews.
- Make preview streams finite or obviously controllable.
- Keep `testValue` strict and preview values friendly. Tests should fail on
  unexpected work; previews should render representative data without prompts.

## Streams

- Model streaming data as `AsyncSequence` or an existing local abstraction.
- Effects should loop streams and send typed actions for updates, completion,
  and failures when needed.
- Provide explicit stop/cancel actions for streams tied to screen lifetime.
- If the stream wraps a callback API, terminate by cancelling the underlying
  task/subscription in the stream termination handler.
- Decide whether completion is user-visible. If it is, send a completion
  action instead of silently ending the loop.

## Review Checks

- Reducer instantiates SDK clients or calls singletons directly.
- Dependency client exposes too much SDK detail to the feature.
- Tests hit live dependencies.
- Preview values can block, prompt, or mutate real data.
- A dependency operation can throw many errors but reducer only models a
  boolean failure.
