---
name: swift-testings-patterns
description: 'Use for Swift Testing test writing, review, XCTest migration, #expect/#require diagnostics, parameterized tests, traits/tags, async tests, fixtures, test doubles, integration tests, snapshot tests, dump snapshots, and flaky or parallel test reliability. Do not use for production concurrency design, UI automation, XCTest metrics, or non-test architecture work.'
---

# Swift Testing Patterns

## Purpose

Use this skill to write, review, migrate, and debug Swift tests with modern
Swift Testing APIs. Prioritize readable tests, robust parallel execution, clear
diagnostics, and incremental migration from XCTest where needed.

## When To Use

Use this skill for Swift test code and test-target design:

- new Swift Testing suites and test functions,
- XCTest-to-Swift-Testing migration,
- `#expect`, `#require`, thrown-error checks, and diagnostics,
- parameterized tests,
- traits, tags, conditions, bug links, and test-plan filtering,
- flaky tests, parallel execution, isolation, and `.serialized`,
- async test waiting, callbacks, confirmations, and event streams,
- fixtures, factories, test doubles, mocks, stubs, fakes, and spies,
- integration-test boundaries, controlled I/O, and dependency injection for
  testability,
- snapshot tests and dump snapshots for UI or data-structure regressions,
- modern Swift Testing API updates such as raw identifiers, test scopes, exit
  tests, attachments, and range-based confirmations.

## When Not To Use

- Do not use for UI automation using `XCUIApplication`; keep that on XCTest.
- Do not use for performance metrics using `XCTMetric`; keep that on XCTest.
- Do not use for Objective-C-only tests.
- Do not use for legacy XCTest suites that are intentionally out of migration
  scope.
- Do not use for production-code concurrency design, actor isolation,
  `Sendable`, or Swift 6 strict-concurrency migration unless the concrete
  issue is test structure.
- Do not use for deep SwiftUI implementation, SwiftData/Core Data persistence,
  package architecture, dependency replacement, or repository documentation.

## Inputs To Inspect

- Swift/Xcode version, platform targets, and whether Swift Testing APIs are
  available for the requested pattern.
- Test target manifest/settings, imports, and coexistence with XCTest.
- Test files, helper fixtures, mocks/fakes, snapshot artifacts, and failure
  output if present.
- Shared resources used by tests: databases, files, networking, clocks,
  randomness, global state, and process environment.
- CI filters, tags, disabled tests, known issues, and flaky-failure history when
  reliability is in scope.

## Workflow

1. Identify whether the task is new test writing, test review, migration,
   flakiness, async waiting, fixtures/test doubles, snapshots, integration
   testing, CI filtering, or diagnostics quality.
2. Inspect the smallest useful surface first: test target manifest/settings,
   test files, helper fixtures, and failure output if present.
3. Prefer Swift Testing for Swift unit and integration tests.
4. Use `#expect` as the default assertion.
5. Use `try #require(...)` when later assertions depend on a prerequisite value.
6. Prefer fixing shared-state isolation before applying `.serialized`.
7. Prefer traits and tags over naming conventions or comments for behavior and
   metadata.
8. Recommend parameterized tests when tests share logic and differ only by input
   or expected value.
9. Use `@available` on test functions for OS-gated behavior instead of runtime
   `#available` checks inside test bodies; never annotate suite types with
   `@available`.
10. Keep migration incremental: assertions first, then test declarations, then
   suites, parameterization, traits, and tags.
11. Import `Testing` only in test targets.
12. For test quality review, check Arrange-Act-Assert and F.I.R.S.T. before
    recommending broader test architecture changes.
13. Keep test doubles explicit: use stub, fake, mock, spy, or dummy terminology
    according to the behavior under test.
14. Prefer state verification over behavior verification unless interaction is
    itself the contract.

## Reference Files To Consult

- Test building blocks and suite organization:
  `references/fundamentals.md`
- `#expect`, `#require`, thrown-error expectations, and known issues:
  `references/expectations.md`
- Traits, tags, bug links, conditions, and Xcode test-plan filtering:
  `references/traits-and-tags.md`
- Parameterized test design and scaling:
  `references/parameterized-testing.md`
- Parallel execution, randomized order, `.serialized`, and isolation:
  `references/parallelization-and-isolation.md`
- Test speed, determinism, flakiness prevention, and CI reliability:
  `references/performance-and-best-practices.md`
- Async tests, callback bridging, confirmations, and event-stream checks:
  `references/async-testing-and-waiting.md`
- XCTest coexistence and migration workflow:
  `references/migration-from-xctest.md`
- Xcode test navigator, reports, and diagnostics workflows:
  `references/xcode-workflows.md`
- High-signal review rules for idiomatic Swift Testing:
  `references/review-rules.md`
- Test quality, Arrange-Act-Assert, F.I.R.S.T., hidden dependencies, and
  diagnostic readability:
  `references/test-quality-rules.md`
- Async review rules, `.serialized` caveats, confirmations, and actor-bound
  tests:
  `references/async-review-rules.md`
- Newer Swift Testing APIs and availability-sensitive recommendations:
  `references/modern-api-updates.md`
- XCTest migration rule set:
  `references/xctest-migration-rules.md`
- Test suite organization, tags, traits, setup, teardown, and discovery:
  `references/organization-patterns.md`
- Test-double vocabulary and patterns:
  `references/test-doubles.md`
- Fixtures, factories, builders, and sample data:
  `references/fixtures.md`
- Integration test boundaries and controlled external dependencies:
  `references/integration-testing.md`
- UI snapshot testing patterns:
  `references/snapshot-testing.md`
- Dump snapshot testing for structured values:
  `references/dump-snapshot-testing.md`
- Async test examples and waiting strategies:
  `references/async-patterns.md`
- Additional parameterized-test design examples:
  `references/parameterized-design.md`
- Additional XCTest migration playbook:
  `references/xctest-migration-playbook.md`
- Reference index:
  `references/_index.md`

## Decision Rules

- Repository-local truth wins over this skill.
- Keep tests small, deterministic, readable, and parallel-safe by default.
- Use Arrange-Act-Assert as the default structure when writing examples or
  refactoring unclear tests.
- Apply F.I.R.S.T. as a review lens for unit tests: fast, isolated,
  repeatable, self-verifying, and timely.
- Put fixtures and test doubles near the model or interface they support when
  that improves discoverability; use `#if DEBUG` only when helpers must live
  outside test targets.
- Prefer injected clocks, randomness, file systems, sessions, stores, and
  services over hidden global dependencies.
- Use snapshot tests for stable UI regression checks and dump snapshots for
  structured data where explicit assertions would be less readable.
- Keep UI automation and XCTest metrics on XCTest.
- Gate modern Swift Testing APIs by Swift/Xcode availability and do not apply
  surprising style changes such as raw identifier test names unless already
  project-compatible.

## Review Checklist

- Tests have a single clear behavior and useful display names when helpful.
- Tests follow Arrange-Act-Assert or another locally consistent structure.
- Preconditions use `#require` when failure should stop later checks.
- Repeated logic is parameterized rather than copied or hidden in loops.
- Expected values are concrete enough to catch regressions.
- Tests are parallel-safe or intentionally serialized with rationale.
- Async code is awaited deterministically; callback APIs are bridged safely.
- Test doubles use the right abstraction and do not over-specify interactions.
- Fixtures are deterministic, local to the behavior under test, and cheap to
  construct.
- Integration and snapshot tests isolate external state and produce actionable
  failure output.
- Swift Testing and XCTest are not mixed accidentally in the same test function.
- Unsupported XCTest-only scenarios remain on XCTest.

## Output Format

For reviews, report findings first by severity with exact files and lines when
available. Include the violated testing rule, likely impact, and a concrete
change.

For implementation work, summarize:

1. Test surface changed
2. Swift Testing APIs or XCTest boundaries affected
3. Fixtures, doubles, snapshots, async behavior, or CI filters affected
4. Validation performed
5. Remaining risks or follow-up checks

## Do Not

- Do not import `Testing` into app, library, or binary targets.
- Do not replace UI automation or performance tests with Swift Testing.
- Do not use `.serialized` as a blanket fix for hidden shared state.
- Do not move test code to `@MainActor` just to quiet flaky behavior.
- Do not propose broad production architecture changes unless the user asks for
  a separate implementation or architecture task.
