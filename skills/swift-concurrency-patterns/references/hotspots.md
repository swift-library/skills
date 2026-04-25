# Review Hotspots

Use this when:

- The user asks for a Swift Concurrency review or bug hunt.
- You need a fast scan before choosing a deeper reference file.
- The code was AI-generated and may contain common concurrency mistakes.

Skip this file if:

- You already have a specific compiler diagnostic. Start from `../SKILL.md`
  or `diagnostics.md` if present.

## Search First

Use targeted search before reading the whole project:

| Search pattern | What to inspect |
|---|---|
| `DispatchQueue` | Can ownership be expressed with actor isolation, `@MainActor`, or structured async code? Keep GCD only for justified low-level interop. |
| `Task.detached` | Does the work truly need to shed caller isolation, priority, and task-local values? |
| mutable `static var` / shared singleton state | Is it protected by an actor, global actor, lock, or immutable value boundary? |
| `Task {` | Is this a necessary sync-to-async bridge, or should the caller become `async` / use SwiftUI `.task` / use structured concurrency? |
| `for .* Task` / `Task {` in loops | Fire-and-forget child work usually loses cancellation, errors, and completion. Prefer task groups. |
| `withCheckedContinuation` / `withCheckedThrowingContinuation` | Verify every path resumes exactly once. Prefer checked continuations over unsafe variants. |
| `AsyncStream` / `AsyncThrowingStream` | Check finish, termination cleanup, buffering policy, and single vs multiple consumer assumptions. |
| `@unchecked Sendable` | Require a concrete synchronization invariant. It must not be a diagnostic silencer. |
| `nonisolated(unsafe)` | Treat as a temporary escape hatch with a clear invariant and removal trigger. |
| `MainActor.run` | Check default actor isolation and whether the surrounding API should be actor-isolated instead of manually hopping. |
| `await` inside `actor` methods | Re-check state assumptions after each suspension point. |
| `!` after `await` in actor methods | Force unwraps after suspension often hide reentrancy bugs. |
| `Thread.sleep`, `Task.sleep` in tests | Timing-based async tests are usually flaky unless testing time itself. |
| `wait(for:` / `wait(` in async tests | Use async XCTest fulfillment or Swift Testing patterns instead. |

## Review Order

1. Build settings: language mode, strict concurrency, default actor isolation,
   upcoming features.
2. Diagnostics: exact error text and offending symbol.
3. Ownership: which actor, global actor, task, or value owns the mutable state.
4. Lifecycle: cancellation, task references, stream termination, deallocation.
5. Review the matching topic file only after the hotspot is confirmed.

## Escalate To

- Actor reentrancy, `@MainActor`, isolated conformances: `actors.md`.
- Non-Sendable values and unsafe escape hatches: `sendable.md`.
- Task groups, cancellation, unstructured tasks: `tasks.md`.
- Streams and continuations: `async-sequences.md` or `async-await-basics.md`.
- Flaky tests: `testing.md`.
- Performance and main-actor stalls: `performance.md`.
- SwiftUI-specific Sendable closure issues: `swiftui-concurrency.md`.
