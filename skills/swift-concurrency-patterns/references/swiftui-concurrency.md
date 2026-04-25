# SwiftUI Concurrency

Use this when:

- A SwiftUI view, modifier, model, or closure triggers a concurrency diagnostic.
- `@MainActor` state is captured from a `Sendable` SwiftUI closure.
- UI work mixes immediate state updates with async background work.

Skip this file if:

- The problem is general actor isolation. Use `actors.md`.
- The problem is a broad SwiftUI architecture review.

## Main Actor Defaults

- SwiftUI `View` work is commonly main-actor isolated, and `body` should be
  treated as UI-owned.
- Swift 6.2 default actor isolation can make most app-target declarations
  main-actor-isolated by default. Confirm the target setting before adding
  redundant annotations.
- SDK UI types from SwiftUI, UIKit, and AppKit are generally main-actor-bound.

Do not blanket-annotate everything with `@MainActor` without checking whether
the work is UI-owned or CPU-heavy.

## Sendable SwiftUI Closures

Some SwiftUI closures may execute outside the main actor or require `Sendable`
captures, including layout, drawing, geometry, and visual-effect style APIs.
Common examples include custom `Shape` path generation, `Layout` methods,
`visualEffect`, and `onGeometryChange`.

If a closure only needs one value from `self`, capture that value explicitly:

```swift
let isEnabled = model.isEnabled

content.visualEffect { content, proxy in
    content.opacity(isEnabled ? 1 : 0.5)
}
```

Avoid sending `self` into a `Sendable` closure just to read one main-actor
property.

## UI Actions And Async Work

SwiftUI action callbacks are synchronous so state can update immediately:

```swift
@MainActor
func refreshTapped() {
    isLoading = true
    refreshTask = Task {
        defer { isLoading = false }
        await model.refresh()
    }
}

Button("Refresh", action: refreshTapped)
```

Prefer making the model API async and main-actor-aware rather than scattering
manual actor hops through views. For view lifecycle work, prefer `.task` over
`onAppear { Task { ... } }` because `.task` participates in cancellation when
the view disappears.

## Performance Boundary

- Keep animations, gestures, focus changes, and immediate UI state synchronous
  and main-actor-bound.
- Move parsing, image processing, compression, large filtering, and expensive
  transforms out of the main actor when measurement or UI hitches justify it.
- Use `@concurrent` for compatible Swift 6.2 offloading. Use `Task.detached`
  only when deliberately shedding caller isolation and task-local context.

## Review Checks

- Is the diagnostic caused by implicit default main-actor isolation?
- Is a SwiftUI closure `Sendable`, and can it capture values instead of `self`?
- Is `.task` available instead of `onAppear` plus unstructured `Task`?
- Does async work expose cancellation and errors to the model or view state?
- Is CPU-heavy work accidentally running on the main actor?
