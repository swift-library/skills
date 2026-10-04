# SwiftUI Focus Basics

Use this file only when ordinary SwiftUI implementation touches a small
`@FocusState` or focused-value detail and the task has not become a dedicated
focus review.

## Out Of Scope

Dedicated focus work stays outside this skill:

- focusable views, focused values, search focus, focus sections, default focus,
  move/exit commands, hover effects, or focus pitfalls beyond a local edit
- focus restoration after navigation, data reloads, sheets, or async updates
- async focus timing, main-actor focus updates, cancellation, or scroll
  feedback loops
- focus styling, custom rings, or hover/focus visual feedback
- focus debugging or platform focus behavior

## Local Reminder

For an incidental SwiftUI source edit, at least preserve these basics:

- keep `@FocusState` private to the owning view
- use distinct enum cases for distinct focusable targets
- do not write redundant tap gestures that fight `.focused()`
- add `.focusable()` before expecting custom views to receive focus
