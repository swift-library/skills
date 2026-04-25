# SwiftUI Architecture Selection

Use this file when no architecture has been chosen or when a requested
architecture needs a fit check.

## Fit Matrix

| Pattern | Best fit | Avoid when |
|---|---|---|
| MVVM | Simple to medium SwiftUI screens, local async work, explicit ViewModel boundary | Complex state machine or cross-feature composition dominates |
| MVI | Deterministic state transitions, replayable intents, no third-party dependency | Team wants low ceremony for a small screen |
| TCA | Existing TCA codebase, strong composition, deterministic effects/tests | Adding `swift-composable-architecture` is not acceptable |
| Clean Architecture | Domain/data isolation, replaceable infrastructure, shared domain across UIs | Feature is presentation-only or too small |
| Coordinator | Flow ownership, deep links, reusable navigation, mixed UIKit/SwiftUI | Used as the only architecture without a presentation pattern |
| Reactive | Search, live feeds, realtime updates, multi-event streams | A simple async button/load flow is enough |

## Decision Flow

1. If the project already uses a clear pattern nearby, prefer that pattern.
2. If strict reducer/state-machine flow is required:
   - Use TCA when the project already has TCA or can accept the dependency.
   - Use MVI when a lightweight in-house reducer/store is better.
3. If the main problem is domain/data isolation, use Clean Architecture with a
   SwiftUI presentation adapter.
4. If the main problem is navigation, deep links, or reusable flows, add a
   Coordinator layer and pair it with the local presentation pattern.
5. If the feature is stream-heavy, add a Reactive overlay inside MVVM, MVI, or
   TCA rather than making streams leak into views.
6. Default to MVVM for ordinary SwiftUI feature work.

## Fit Check

For an explicit user-requested architecture, check:

- Current local pattern and team conventions.
- SwiftUI root vs UIKit-hosted SwiftUI.
- State and navigation complexity.
- Async effects and cancellation requirements.
- Need for deterministic reducer/effect tests.
- Third-party dependency tolerance.

Return `fit` when the requested pattern solves the stated problem with
reasonable ceremony. Return `mismatch` when it adds dependency, boilerplate, or
state indirection that does not address the actual risk.

## Common Combinations

- MVVM + Coordinator: screen ViewModels plus centralized flow routing.
- MVVM + Reactive: ViewModels own Combine/Rx pipelines for streams.
- Clean Architecture + MVVM: domain/data layers plus ViewModels.
- Clean Architecture + TCA: domain/data layers plus TCA features.
- MVI + Coordinator: reducer-backed screens plus separate flow ownership.
