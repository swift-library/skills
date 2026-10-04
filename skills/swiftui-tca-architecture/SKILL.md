---
name: swiftui-tca-architecture
description: Use this skill for detailed SwiftUI feature design, implementation, review, refactoring, or testing when Point-Free's The Composable Architecture (TCA) is already used or explicitly accepted. Covers ComposableArchitecture @Reducer, @ObservableState, Store/StoreOf, ViewAction, BindingReducer, Effect, @Dependency, @DependencyClient, dependency clients, @Shared, @SharedReader, @Presents, PresentationAction, StackState, StackAction, IdentifiedActionOf, reducer composition, child features, scoped stores, delegate actions, TCA navigation and presentation, TestStore, TestClock, performance pitfalls, and migration of existing TCA code. Do not use to decide whether a project should adopt TCA instead of MVVM, MVI, Clean Architecture, or a coordinator. Do not use for ordinary SwiftUI layout, visual design, generic Swift Testing syntax, SwiftData/Core Data persistence, Swift package architecture, or broad Swift Concurrency diagnostics.
---

# SwiftUI TCA Architecture

## Purpose

Work inside SwiftUI codebases that already use, or have explicitly accepted,
Point-Free's The Composable Architecture. This skill owns TCA feature shape,
reducers, stores, dependencies, effects, navigation, shared state, tests, and
review rules. It does not sell TCA into a project; the adoption decision is out
of scope.

## Authority

- Prefer the local project's resolved `ComposableArchitecture` version,
  nearby feature conventions, and migration state.
- For mutable API details, verify against the official
  `pointfreeco/swift-composable-architecture` package source or DocC before
  promoting a rule.
- Treat third-party TCA guides, checklists, and examples as coverage signals,
  not authority.
- `ComposableArchitecture` re-exports several supporting packages. Attribute
  APIs correctly when it matters: dependencies, sharing, case paths, clocks,
  navigation, identified collections, and observation may come from re-exported
  Point-Free or Swift packages.

## When To Use

- The project already imports `ComposableArchitecture`.
- The user explicitly asks for TCA, `@Reducer`, `StoreOf`, `Effect`,
  `TestStore`, `@Dependency`, `@Shared`, TCA navigation, or TCA presentation.
- A review or refactor is scoped to existing TCA code.
- An architecture decision has already selected TCA and handed off detailed
  work.

## When Not To Use

- Do not decide whether TCA should be introduced.
- Do not use for ordinary SwiftUI view layout or controls.
- Do not use for visual polish or native UI feel.
- Do not use for SwiftUI performance outside TCA reducer/store behavior.
- Do not use for generic Swift Testing syntax.
- Do not use for broad actor isolation, `Sendable`, or task cancellation
  diagnostics outside TCA effects.

## Workflow

1. Read local truth: feature code, tests, `Package.resolved` or manifest,
   app/module route docs, nearby TCA features, and local naming conventions.
2. Confirm TCA is already accepted. If the task is still an adoption decision,
   state that it is outside this skill's scope.
3. Classify the work and load only the matching reference:
   - `references/reducer-structure.md` for feature shape, state/action
     organization, result actions, reducer enums, and macro/version choices.
   - `references/views-binding.md` for store-driven views, `@Bindable`,
     binding actions, observation, lifecycle actions, and `@ViewAction`.
   - `references/views-composition.md` for `IdentifiedArrayOf`, `ForEach`,
     child scopes, optional children, and delegate actions.
   - `references/effects.md` for `.run`, `.send`, error handling, composition,
     cancellation, timers, lifecycle effects, and state capture.
   - `references/dependencies.md` for dependency clients, `@Dependency`,
     `@DependencyClient`, test/preview values, streams, errors, and concurrency.
   - `references/navigation-basics.md` for `StackState`, `StackActionOf`, path
     reducers, push/pop, dismiss, and child route actions.
   - `references/navigation-advanced.md` for mixed stack/sheet flows, deep
     links, path inspection, external events, and recursive routes.
   - `references/presentation.md` for `@Presents`, destination enums, alerts,
     sheets, popovers, confirmation dialogs, and multiple presentation states.
   - `references/shared-state.md` for `@Shared`, `@SharedReader`, app storage,
     file storage, in-memory storage, effects, and shared-state tests.
   - `references/testing-fundamentals.md` for `TestStore` setup, Equatable
     state, naming, and dependency overrides.
   - `references/testing-patterns.md` for action, state, dependency, error,
     async, presentation, navigation, and shared-state test scripts.
   - `references/testing-advanced.md` for given/when/then, state machines, edge
     cases, time control, key-path receive helpers, and exhaustivity choices.
   - `references/testing-utilities.md` for test data, organization,
     confirmation dialogs, dependency completeness, `LockIsolated`, and
     post-effect shared-state assertions.
   - `references/performance.md` for reducer logic sharing, computed state,
     high-frequency actions, store scoping, memory, and async performance.
   - `references/closed-loop-examples.md` when a compact complete example is
     more useful than isolated rules.
   - `references/review-rules.md` for TCA review findings and scope limits.
4. Preserve local TCA style. Do not mechanically rewrite older but working TCA
   syntax unless the task is a migration.
5. Keep views render/send focused, reducers state/effect focused, and external
   work behind dependencies.
6. Validate with the narrowest meaningful build and focused TCA tests. If API
   availability is uncertain, verify against the resolved package before
   editing.

## Decision Rules

- Use TCA for its local value: deterministic reducers, explicit effects,
  composable feature boundaries, dependency injection, navigation state, and
  `TestStore` coverage.
- Do not add direct side effects, singleton access, URL loading, persistence,
  analytics, or clock/date/UUID calls in reducers; put them behind
  dependencies.
- Do not duplicate feature state in SwiftUI local state unless it is strictly
  transient view-only state.
- Model navigation and presentation in feature state when they are part of the
  feature contract.
- Prefer official modern TCA APIs when the resolved version supports them, but
  keep version-compatible syntax in existing code.
- A TCA review finding should identify the broken boundary: state, action,
  reducer, effect, dependency, presentation, navigation, shared state, or test.

## Output

For implementation, produce the concrete file/code change and focused
validation. For architecture guidance, include state/action shape,
dependency/effect boundary, navigation/presentation model, and test plan. For
review, lead with findings and file/line evidence.
