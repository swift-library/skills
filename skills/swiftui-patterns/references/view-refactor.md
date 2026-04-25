# SwiftUI View Refactor

Use this reference for focused cleanup passes after `swiftui-patterns` has been
selected and the target view file is known. It preserves the same SwiftUI
knowledge system as ordinary view implementation; explicit invocation only
changes the mode to review or refactor.

## File Ordering

Prefer this order unless the local file has a stronger convention:

1. Environment and dependency properties.
2. Stored inputs.
3. `@State`, `@Binding`, and other mutable view state.
4. Non-view computed values.
5. `init`.
6. `body`.
7. Small computed view helpers.
8. Action, async, and helper methods.

## Dedicated Subviews

- Extract meaningful sections into dedicated `View` types.
- Prefer dedicated subviews when a section has state, branching, async work,
  repeated layout, or deserves a preview.
- Keep computed `some View` helpers small, static, and local.
- Pass explicit values, bindings, and callbacks into extracted subviews.
- Move independently meaningful or reused subviews into their own files.

## Actions And Side Effects

- Keep `body` declarative.
- Move non-trivial `Button` actions into named methods.
- Keep `.task`, `.onAppear`, `.onChange`, and `.refreshable` bodies thin.
- Move business logic into existing services/models instead of hiding it in
  closures.

## Stable View Trees

- Prefer one stable root view with conditional sections or modifier values.
- Avoid swapping entire root branches just to represent state.
- Use conditional branches when the UI is genuinely different, not when only a
  modifier value changes.

## ViewModel Boundary

- Do not introduce a ViewModel by default.
- A ViewModel may be justified when the project already uses one, the user asks
  for one, async/effect ownership needs a test boundary, or local architecture
  requires it.
- For iOS 17+ Observation, own root `@Observable` models with `@State`.
- For iOS 16 or earlier, use `@StateObject` for ownership and `@ObservedObject`
  for injection.

## Checklist

- [ ] `body` reads as UI structure.
- [ ] Long sections are dedicated subviews, not hidden computed properties.
- [ ] Actions and async work are named and testable.
- [ ] View identity remains stable where state should be preserved.
- [ ] No new architecture was introduced just to clean up a file.
