# SwiftUI Focus Route

SwiftUI focus knowledge belongs to `focus-engine-patterns`.

Use this route only when ordinary SwiftUI implementation touches a small
`@FocusState` or focused-value detail and the task has not become a dedicated
focus review.

## Route

- SwiftUI `@FocusState`, focusable views, focused values, search focus, focus
  sections, default focus, move/exit commands, hover effects, or common
  pitfalls:
  `../focus-engine-patterns/references/swiftui-focus.md`
- Focus restoration after navigation, data reloads, sheets, or async updates:
  `../focus-engine-patterns/references/focus-restoration.md`
- Async focus timing, main-actor focus updates, cancellation, or scroll
  feedback loops:
  `../focus-engine-patterns/references/async-focus.md`
- Focus styling, custom rings, hover/focus visual feedback:
  `../focus-engine-patterns/references/focus-styling.md`
- Dedicated focus debugging or platform focus behavior:
  use the `focus-engine-patterns` skill.

## Local Reminder

For an incidental SwiftUI source edit, at least preserve these basics:

- keep `@FocusState` private to the owning view
- use distinct enum cases for distinct focusable targets
- do not write redundant tap gestures that fight `.focused()`
- add `.focusable()` before expecting custom views to receive focus
