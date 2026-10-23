---
name: swiftui-architecture
description: SwiftUI app and feature architecture selection, review, and scaffolding with MVVM, MVI, TCA fit checks, Clean Architecture, Coordinators, and testable effect boundaries. Not for detailed TCA implementation or ordinary view layout.
---

# SwiftUI Architecture

## Purpose

Guide SwiftUI app and feature architecture choices without turning ordinary
view implementation work into an architecture migration. This skill is for
selecting, reviewing, or applying feature-level patterns such as MVVM, MVI,
TCA fit checks, Clean Architecture adapters, and Coordinator-style navigation
state. Detailed TCA feature work after TCA is selected or already present is
out of scope.

## When To Use

- Choosing between MVVM, MVI, TCA, Clean Architecture, or Coordinator-style
  navigation for a SwiftUI feature.
- Reviewing whether a SwiftUI feature has clear state, dependency, effect,
  navigation, and test boundaries.
- Refactoring ad hoc `@State`, singleton, or view-owned async work into a
  testable feature boundary.
- Designing feature file/module structure, dependency injection, async
  cancellation, and testing strategy.
- Migrating a SwiftUI feature incrementally toward an existing local
  architecture.
- Designing `NavigationStack` flow state and Coordinator ownership.

## When Not To Use

- Do not use for ordinary SwiftUI state wrapper, layout, list, sheet,
  animation, or API-usage work.
- Do not use for source-level SwiftUI performance review, diagnosis, or
  optimization.
- Do not use for detailed Point-Free ComposableArchitecture reducer, store,
  effect, dependency, navigation, shared-state, or `TestStore` work after TCA
  is accepted or already present.
- Do not use for visual polish, native Apple UI feel, spacing, typography, or
  screenshots.
- Do not use for dedicated accessibility audits.
- Do not use for local Swift Package target/module architecture.
- Do not use for UIKit-only module architecture.
- Do not use for deep Swift Concurrency diagnostics, actor isolation, or
  `Sendable` migration.

## Workflow

1. Read local truth first: user request, existing feature code, `AGENTS.md`,
   `README.md`, package/project files, and architecture docs.
2. Capture constraints:
   - UI stack and app root: SwiftUI, mixed, or UIKit-hosted SwiftUI.
   - Scope: one screen, feature flow, tab, app shell, or shared module.
   - Current pattern: MVVM, reducer/store, TCA, coordinator, clean layers, or
     informal local conventions.
   - State complexity, async/effect complexity, navigation complexity, testing
     needs, and dependency tolerance.
3. If the user names a pattern, do a fit check before applying it. If it
   mismatches local constraints, state the mismatch and recommend the closest
   lower-risk alternative.
4. If no pattern is named, read `references/selection.md` and choose the
   smallest pattern that fits the feature.
5. Load only the relevant pattern reference:
   - `references/mvvm.md` for screen-level state and explicit ViewModel
     boundaries.
   - `references/mvi.md` for strict state machines without a TCA dependency.
   - `references/tca.md` for deciding whether TCA fits and when to hand off to
     `swiftui-tca-architecture`.
   - `references/clean-architecture.md` for domain/data isolation.
   - `references/navigation-coordinator.md` for flow ownership, deep links, or
     centralized SwiftUI navigation state.
   - `references/reactive.md` for stream-heavy Combine/Rx pipelines inside the
     selected architecture.
   - `references/implementation-playbooks.md` when the user asks for concrete
     scaffolding, migration steps, or a fuller implementation playbook after
     the pattern has been selected.
6. Produce scoped guidance: file structure, state model, dependency boundary,
   async/effect handling, navigation ownership, test plan, migration steps, or
   review findings.

## Decision Rules

- Preserve the architecture already used nearby unless it is causing the
  reported problem.
- Do not introduce TCA, RxSwift, or any third-party framework unless the user
  asks or the project already uses it.
- Prefer the smallest architecture that makes state, dependencies, effects, and
  navigation testable.
- Coordinator is a navigation layer, not a full feature architecture. Pair it
  with MVVM, MVI, TCA, or a local presentation pattern.
- Keep SwiftUI views declarative. Views render state and send intents; feature
  objects own loading, mapping, validation, cancellation, and dependencies.
- Model navigation as value state for pure SwiftUI when practical. Use
  coordinator or router protocols for mixed UIKit/SwiftUI flows.
- Do not rewrite a feature into a named architecture when a local extraction or
  dependency boundary fixes the issue.

## Output Format

For recommendations, include:

1. Fit judgment
2. Recommended pattern and why
3. State, dependency, effect, and navigation boundaries
4. File/module structure
5. Testing strategy
6. Migration or review risks

For review tasks, lead with findings and line/file evidence.
