---
name: uikit-architecture
description: Use this skill for UIKit app, feature, or module architecture selection, review, refactoring, or scaffolding involving MVC-to-MVP/MVVM/VIPER migration, Presenter/ViewModel/Interactor boundaries, Coordinator or Router navigation, Clean Architecture adapters, Combine/RxSwift presentation pipelines, UIViewController responsibility cleanup, dependency injection, async cancellation, testability, or UIKit and SwiftUI interop ownership. Do not use for SwiftUI-only architecture, SwiftUI view implementation, visual design, accessibility audits, local Swift Package architecture review, persistence schema work, or deep Swift Concurrency diagnostics.
---

# UIKit Architecture

## Purpose

Guide UIKit app and feature architecture choices for UIViewController-heavy,
mixed UIKit/SwiftUI, and legacy codebases. This skill is for selecting,
reviewing, or applying patterns such as MVP, MVVM, VIPER, Coordinator, Clean
Architecture adapters, and reactive presentation pipelines.

## When To Use

- Refactoring large UIViewControllers or MVC-style modules into testable
  boundaries.
- Choosing between MVP, MVVM, VIPER, Clean Architecture, Coordinator, or a
  reactive presentation layer for UIKit.
- Reviewing Presenter, ViewModel, Interactor, Router, or Coordinator
  responsibilities.
- Designing module assembly, dependency injection, async cancellation, and test
  strategy.
- Deciding ownership in UIKit apps that host SwiftUI screens or migrate feature
  by feature.

## When Not To Use

- Do not use for SwiftUI-only app or feature architecture.
- Do not use for SwiftUI view layout, state wrapper usage, animation, or
  navigation modifier behavior.
- Do not use for visual polish or native UI feel.
- Do not use for dedicated accessibility audits.
- Do not use for local Swift Package target/module architecture.
- Do not use for deep Swift Concurrency diagnostics, actor isolation, or
  `Sendable` migration.

## Workflow

1. Read local truth first: user request, current module code, `AGENTS.md`,
   `README.md`, project/package files, and architecture docs.
2. Capture constraints:
   - UI stack: UIKit, mixed UIKit/SwiftUI, or SwiftUI hosted from UIKit.
   - Scope: one view controller, feature module, flow, tab, or app shell.
   - Current pattern: MVC, MVP, MVVM, VIPER, Coordinator, Clean Architecture,
     reactive, or local conventions.
   - Navigation complexity, state complexity, async/effect complexity, testing
     needs, and framework dependency tolerance.
3. If the user names a pattern, do a fit check. If it mismatches the codebase,
   state the mismatch and recommend the closest lower-risk alternative.
4. If no pattern is named, read `references/selection.md` and choose the
   smallest pattern that addresses the actual risk.
5. Load only the relevant pattern reference:
   - `references/mvc-migration.md` for fat controller cleanup.
   - `references/mvp.md` for passive View plus Presenter.
   - `references/mvvm.md` for observable or callback-driven view state.
   - `references/viper.md` for strict feature-module separation.
   - `references/coordinator.md` for navigation and flow ownership.
   - `references/clean-architecture.md` for domain/data isolation.
   - `references/reactive.md` for Combine/Rx pipelines in presentation logic.
   - `references/swiftui-interop.md` for UIHostingController and migration
     ownership.
   - `references/implementation-playbooks.md` when the user asks for concrete
     scaffolding, migration steps, or a fuller implementation playbook after
     the pattern has been selected.
6. Produce scoped guidance: module structure, boundaries, dependency wiring,
   async/cancellation handling, navigation ownership, tests, migration steps, or
   review findings.

## Decision Rules

- Preserve nearby architecture unless it is the source of the issue.
- Do not rewrite UIKit code into SwiftUI architecture unless the user asks for
  migration.
- Coordinator owns navigation and assembly, not business logic.
- Presenters/ViewModels own presentation logic; ViewControllers render and
  forward user events.
- Interactors/use cases own business actions; they do not navigate or update
  views directly.
- Prefer protocol boundaries where they improve testing or module isolation.
- Do not introduce RxSwift, TCA, or other third-party frameworks unless the
  project already uses them or the user approves.

## Output Format

For recommendations, include:

1. Fit judgment
2. Recommended pattern and why
3. View, presentation, domain/data, and navigation boundaries
4. File/module structure and assembly
5. Testing strategy
6. Migration or review risks

For review tasks, lead with findings and line/file evidence.
