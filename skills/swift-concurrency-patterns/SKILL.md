---
name: swift-concurrency-patterns
description: Diagnose and review Swift Concurrency problems with project-compatible patterns. Use when work involves Swift Concurrency, async/await, actors, tasks, task groups, AsyncSequence, AsyncStream, AsyncAlgorithms, @MainActor, Sendable, actor isolation, data races, strict concurrency, Swift 6 migration, SwiftUI concurrency diagnostics, Core Data concurrency, async testing, concurrency performance, concurrency bug hunts, or concurrency-related SwiftLint diagnostics such as async_without_await. Do not use for broad SwiftUI, SwiftData schema, Core Data schema, package architecture, dependency replacement, or repository documentation work unless the concrete issue is concurrency-specific.
---

# Swift Concurrency Patterns

## Progressive Disclosure

Use this file as the entry router. Do not read every reference file.

1. Read project-local truth first: user request, `AGENTS.md`, `README.md`,
   `Package.swift`, `.pbxproj`, and relevant architecture docs.
2. Capture the exact compiler, test, runtime, or lint diagnostic before
   proposing a fix.
3. Determine the isolation boundary: `@MainActor`, custom global actor, actor
   instance isolation, `nonisolated`, task boundary, or Sendable transfer.
4. Open only the smallest matching reference below. Open `references/_index.md`
   only if routing is unclear.
5. Prefer the smallest behavior-preserving change, then build and test before
   broadening the migration.

For review or bug-hunt requests, open `references/hotspots.md` first, then
`references/bug-patterns.md` only for confirmed suspicious code.

## Build Settings First

For migration-sensitive guidance, inspect settings before diagnosing:

| Setting | SwiftPM | Xcode |
|---|---|---|
| Language mode | `swiftLanguageVersions` or `-swift-version` | Swift Language Version |
| Strict concurrency | `.enableExperimentalFeature("StrictConcurrency=targeted")` | `SWIFT_STRICT_CONCURRENCY` |
| Default isolation | `.defaultIsolation(MainActor.self)` | `SWIFT_DEFAULT_ACTOR_ISOLATION` |
| Upcoming features | `.enableUpcomingFeature(...)` | `SWIFT_UPCOMING_FEATURE_*` |

`// swift-tools-version:` is not enough to infer Swift language mode. If these
settings cannot be discovered locally, ask before giving migration-sensitive
advice.

## Guardrails

- Do not recommend `@MainActor` as a blanket fix. Justify why the code is
  genuinely UI-owned or main-actor-owned.
- Prefer structured concurrency over unstructured tasks.
- Use `Task.detached` only with a concrete reason.
- Flag mutable shared state that is not protected by an actor, global actor,
  project-approved lock, or value ownership boundary.
- Before recommending `MainActor.run`, check whether the surrounding API should
  be actor-isolated or whether the project already uses Main Actor default
  isolation.
- Do not introduce third-party packages unless the user explicitly approves
  them or the project already depends on them.
- Treat `@preconcurrency`, `@unchecked Sendable`, and `nonisolated(unsafe)` as
  temporary escape hatches requiring a documented safety invariant and removal
  plan.
- Keep migration commits small. Fix one diagnostic category or ownership
  boundary at a time.

## Quick Fix Mode

Use this file alone, plus at most one focused reference, when:

- the issue is localized to one file or one type,
- the project settings are known,
- the isolation boundary is clear,
- and the fix can be explained in one or two behavior-preserving steps.

Skip quick fix mode and route deeper when the issue crosses modules, changes
public API behavior, involves unsafe escape hatches, or depends on unknown build
settings.

## Diagnostic Router

| Symptom | Open |
|---|---|
| Callback or delegate API should become async/await | `references/async-await-basics.md` |
| Review, bug hunt, or suspicious generated concurrency code | `references/hotspots.md`, then `references/bug-patterns.md` |
| Need to start async work, cancel work, run parallel work, or choose task groups | `references/tasks.md` |
| Main actor, actor isolation, actor reentrancy, protocol conformance, custom actors | `references/actors.md` |
| Non-Sendable value crossing boundaries, `@Sendable`, `sending`, global mutable state | `references/sendable.md` |
| Confusion about threads, suspension points, `nonisolated(nonsending)`, `@concurrent` | `references/threading.md` |
| SwiftUI `Sendable` closure, `View` isolation, `.task`, `visualEffect`, `Layout`, `Shape`, or geometry closure issues | `references/swiftui-concurrency.md` |
| AsyncSequence, AsyncStream, callback streams, delegate streams | `references/async-sequences.md` |
| Debounce, throttle, merge, combineLatest, timers, channels | `references/async-algorithms.md` |
| Async tests, flaky scheduling, XCTest `wait(...)` in async contexts | `references/testing.md` |
| Retain cycles, task lifetime, async stream cleanup, deallocation checks | `references/memory-management.md` |
| Core Data objects crossing contexts or actors | `references/core-data.md` |
| Slow async code, actor hops, suspension overhead, parallelism tradeoffs | `references/performance.md` |
| Swift 6 or strict concurrency migration plan | `references/migration.md` |
| SwiftLint `async_without_await` or concurrency lint decisions | `references/linting.md` |
| Term definition only | `references/glossary.md` |

## Common First Checks

- UI-bound state usually belongs on `@MainActor`; waiting, retrying, parsing,
  networking, and CPU work usually do not.
- Shared mutable state should have one owner: an actor, a global actor, a
  project-approved lock, or a value passed immutably across boundaries.
- Sendability fixes should prefer immutable values and explicit ownership over
  `@unchecked Sendable`.
- Intermediate-state async tests need deterministic scheduling or a tested
  public effect. Do not add a test helper package without approval.
- Performance claims require measurement with Instruments or a project-local
  benchmark.

## Verification

When changing concurrency code:

1. Re-check build settings before interpreting diagnostics.
2. Build after each category of fix.
3. Run tests that cover actor isolation, cancellation, lifetime, and async
   scheduling.
4. Verify deallocation for long-lived tasks or streams.
5. Check cancellation in long-running operations.
6. Document any temporary unsafe escape hatch and its removal trigger.
