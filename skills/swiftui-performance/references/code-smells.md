# SwiftUI Performance Code Smells

Use this file after `swiftui-performance` is selected and SwiftUI source
is available.

## Triage Order

1. Broad invalidation from state, environment, or observation.
2. Unstable identity in `ForEach`, `List`, `Table`, or navigation data.
3. Heavy work inside `body`, view builders, or view initializers.
4. Layout thrash from deep stacks, GeometryReader chains, preferences, or
   frequent geometry updates.
5. Image decoding, resizing, or caching costs.
6. Animation or transition work applied too broadly.

## High-Signal Smells

- Sorting, filtering, mapping, formatting, or decoding inside `body`.
- Creating formatters, clients, tasks, models, or caches inside `body`.
- Passing a whole model/config object when a row only needs one or two values.
- Reading frequently changing environment values across many descendants.
- Using indices as identity for mutable collections.
- Rebuilding root branches for modifier-only state changes.
- Updating `@State` repeatedly with the same value.
- Launching unstructured tasks without cancellation.
- Using `.equatable()` without a cheap and complete equality definition.

## Remediation

- Narrow inputs passed to child views.
- Move derived work into models, services, cached dependencies, or explicit
  state updated when inputs change.
- Use stable semantic IDs.
- Preserve structural identity with modifier values where possible.
- Downsample images before rendering large collections.
- Use `_logChanges()` or `_printChanges()` to confirm update sources.
- Ask for Instruments evidence when source review cannot rank likely causes.

## Remediation Patterns

### Redundant State Updates

Redundant assignments can add work in hot update paths; observation and
invalidation behavior depends on the value, storage, and framework version.
Measure update causes and guard repeated assignments when equality is cheap:

```swift
.onReceive(publisher) { value in
    if currentValue != value {
        currentValue = value
    }
}
```

Prefer `.task` over `onAppear { Task { ... } }` for view-bound async work so
SwiftUI owns cancellation when the view disappears.

### Hot Paths

Scroll handlers, geometry preferences, animations, and gestures can update
very frequently. Only write state when a threshold or semantic value changes:

```swift
.onPreferenceChange(ScrollOffsetKey.self) { offset in
    let shouldShow = offset.y <= -32
    if shouldShow != shouldShowTitle {
        shouldShowTitle = shouldShow
    }
}
```

### Dependency Granularity

Avoid passing a whole config, model, or environment object when a child only
needs one or two values. With `ObservableObject`, any `@Published` change can
wake all observers. With Observation, accessed properties are tracked more
precisely, but passing broad objects still makes dependencies harder to reason
about.

For large lists, consider per-row or per-item observable state only when it
measurably narrows updates. Do not introduce per-item models just as style.

### Equatable And Structural Identity

Use `.equatable()` only when equality is complete and cheaper than recomputing
the subtree. Remember to update equality when inputs change.

Prefer changing modifier values over swapping branches when the UI is the same
view in a different state:

```swift
Text(title)
    .foregroundStyle(isError ? .red : .primary)
    .opacity(isHidden ? 0 : 1)
```

Use `if` when the branches are genuinely different UI.

### Lazy Loading And Images

Use lazy containers for large collections, and downsample or cache images
before rendering them repeatedly. Prefer reusing image work rather than
decoding, resizing, or formatting inside `body`.

Choose lazy containers for the actual data volume and measurements; small
collections can use ordinary stacks. In lazy containers, check stable item IDs
and a stable number of leaf views per item. Filter at the data level when rows
would otherwise emit a variable number of leaves.

Offscreen row state may be released; put state that must survive scrolling in
the item model or another longer-lived owner. Content size and absolute offsets
can be estimates, so use visible-item semantics for visibility tasks. Avoid
layout changes triggered only after appearance. Do not defeat prefetching by
recreating loading work in every `onAppear`; keep cache, cancellation, and reuse
with the model or loader owner.

With Xcode 27, lazy Observable `@State` initialization can reduce initialization
work even on supported older deployment targets. OS 27 AsyncImage HTTP caching
is a separate runtime change and does not remove image decoding cost.
ContentBuilder's type-checking changes do not establish faster runtime frames.
Use `official-sources.md` for the version-specific evidence.

### Debugging Updates

Use `Self._printChanges()` or `Self._logChanges()` in debug builds to identify
which properties drive unexpected body updates. `@self` means the view value
changed; `@identity` means persistent view data was recycled.

### Off-Main-Thread SwiftUI Closures

SwiftUI may call some closures off the main thread for performance. Treat these
closures as `Sendable` and avoid reading `@MainActor` state directly:

- `Shape.path(in:)`
- `visualEffect` closure
- `Layout` protocol methods
- `onGeometryChange` transform closure

Capture needed values instead:

```swift
.visualEffect { [pulse] content, geometry in
    content.blur(radius: pulse ? 5 : 0)
}
```

### Cheap Initializers

View initializers should be small and side-effect free. Move loading, decoding,
sorting, network calls, and other non-trivial work into `.task`, a model, or a
cached dependency.

## Checklist

- [ ] State writes avoid assigning the same value repeatedly.
- [ ] Hot paths minimize update frequency.
- [ ] Child views receive narrow inputs.
- [ ] Lists use stable identity and lazy containers where appropriate.
- [ ] View-bound async work has a clear cancellation owner.
- [ ] Modifier values preserve structural identity where possible.
- [ ] View initializers avoid expensive work and side effects.
- [ ] `body` avoids sorting, filtering, formatting, decoding, object creation,
      and side effects.
- [ ] Derived values are computed or cached intentionally, not mirrored into
      arbitrary state.
- [ ] `_logChanges()` or `_printChanges()` is used when update sources are
      unclear.
- [ ] Equatable views have cheap and complete equality.
- [ ] Frequently changing values are not stored in broad environment
      dependencies.
