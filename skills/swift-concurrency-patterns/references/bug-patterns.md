# Bug Patterns

Use this when:

- Reviewing code for likely Swift Concurrency correctness bugs.
- A build is clean but behavior is flaky, duplicated, leaked, or silently
  failing.
- You need concrete failure modes before proposing changes.

Skip this file if:

- The task is a broad migration plan. Use `migration.md`.
- The task is only a term definition. Use `glossary.md`.

## Actor Reentrancy: Check Then Act Across `await`

Failure shape:

```swift
actor Cache {
    private var values: [String: Data] = [:]

    func value(for key: String) async throws -> Data {
        if values[key] == nil {
            values[key] = try await load(key)
        }
        return values[key]!
    }
}
```

The actor may run another call while suspended at `await`. Re-check assumptions
after the suspension, store async results in locals, and avoid force unwraps
that depend on pre-`await` state.

For duplicate work, store in-flight tasks behind the actor and remove them on
success and failure.

## Continuation Never Resumed

Failure shape:

- early return before registering a callback,
- object deallocation drops the callback,
- underlying API times out without calling back,
- cancellation path forgets to resume.

Use checked continuations and audit every path. If the legacy API can silently
drop completion, add a timeout or redesign the wrapper so callers are not left
waiting forever.

## Continuation Resumed Twice

Failure shape:

- success and cancellation both resume,
- delegate emits terminal events more than once,
- both timeout and callback race to resume.

Serialize terminal state with an actor, lock, or carefully scoped flag. Keep
`withCheckedContinuation` / `withCheckedThrowingContinuation` during
development so double resumes fail loudly.

## Unstructured Tasks In Loops

Failure shape:

```swift
for item in items {
    Task { try await process(item) }
}
```

This loses cancellation propagation, error collection, and completion waiting.
Use `withTaskGroup` or `withThrowingTaskGroup`; use discarding groups for
side-effect-only work.

## Swallowed Task Errors

Failure shape:

```swift
Task {
    try await save()
}
```

If nobody awaits the task value, thrown errors are easy to lose. Handle errors
inside the task, expose the task to callers, or make the surrounding API async
so the error can propagate normally.

## Main Actor Blocking

Failure shape:

- CPU-heavy parsing, image processing, compression, or search runs in
  `@MainActor` code.
- A plain async helper is assumed to leave the main actor, but the project uses
  Swift 6.2 caller-actor execution behavior.

Keep UI mutations on the main actor, but move heavy work into a deliberately
offloaded async function such as `@concurrent` when compatible. Use
`Task.detached` only with a concrete reason.

## Unbounded AsyncStream

Failure shape:

- high-frequency producer,
- slow consumer,
- default unbounded buffering,
- missing termination cleanup.

Set an explicit buffering policy and define what happens when the consumer is
cancelled. Always finish streams and clean up underlying observers, delegates,
timers, or tasks.

## Cancellation Treated As Failure

Failure shape:

```swift
do {
    try await load()
} catch {
    errorMessage = error.localizedDescription
}
```

Filter `CancellationError` before user-visible error handling. Cancellation is
often normal lifecycle behavior, especially for SwiftUI `.task` work.

## Unsafe Sendability Silences Real Races

Failure shape:

- `@unchecked Sendable` added to a mutable class with no synchronization,
- `nonisolated(unsafe)` used to quiet a global/static warning,
- `@preconcurrency` added without tracking removal.

Prefer value types, actors, global actors, or a verified lock invariant. If an
escape hatch remains, document why it is safe and how to remove it later.
