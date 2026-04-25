# AppKit Accessibility

Use this file for macOS AppKit accessibility involving `NSAccessibility`,
keyboard navigation, focus behavior, tables, outline views, custom controls,
and announcements.

## Element Basics

Prefer native AppKit controls: `NSButton`, `NSPopUpButton`,
`NSSegmentedControl`, `NSSlider`, `NSTextField`, `NSTableView`, and
`NSOutlineView`. Native controls provide role, keyboard, and VoiceOver behavior
that custom `NSView` implementations must recreate.

For custom views, expose role, label, value, and action only when the view is
meant to be an accessible element:

```swift
override func isAccessibilityElement() -> Bool {
    true
}

override func accessibilityRole() -> NSAccessibility.Role? {
    .button
}

override func accessibilityLabel() -> String? {
    title
}
```

## Labels, Help, Values, Roles

- Label: concise name or meaning.
- Help: optional explanation when the result is not obvious.
- Value: state, selection, progress, or current data.
- Role: semantic role such as button, checkbox, slider, table, row, or group.

Use role descriptions sparingly. Prefer the standard role when it is accurate.

## Keyboard Navigation

macOS accessibility depends heavily on keyboard operation.

- Ensure controls are reachable with Tab / Shift-Tab or the expected arrow-key
  pattern.
- Keep focus rings visible for keyboard users.
- Avoid focus traps in custom modal, popup, or panel UI.
- Support Escape or a clear keyboard path to dismiss transient UI.
- Preserve existing shortcuts and key equivalents.

Use key view loop configuration only when AppKit's automatic order is wrong.

## Tables And Outline Views

For `NSTableView` and `NSOutlineView`:

- Rows should be understandable when read by VoiceOver.
- Selection state must be discoverable.
- Column headers should be accessible when visible.
- Custom cell views should expose a meaningful label and value.
- Do not flatten a row into one element when users need to interact with
  controls inside the row.

## Custom Controls

If a custom `NSView` behaves like a button, checkbox, toggle, or slider:

- expose the correct role and state
- allow keyboard operation with standard keys such as Space or Enter
- implement the appropriate accessibility action
- announce or update state after activation

For custom actions, use AppKit accessibility custom action APIs or expose the
standard action method expected by the role.

## Dynamic Text And Display

macOS does not map directly to iOS Dynamic Type, but accessibility still
requires readable text and adaptable layout:

- prefer system fonts and text styles where practical
- avoid tiny fixed text in primary UI
- support display scaling and larger text where the app offers it
- avoid clipping, truncating, or hiding essential information

## Announcements

When content updates without an obvious focus change, post an appropriate
accessibility notification:

```swift
NSAccessibility.post(element: resultsView, notification: .layoutChanged)
```

Use notifications carefully. Frequent announcements can make the app harder to
use with VoiceOver.

## Checklist

- [ ] Native AppKit controls are used where possible.
- [ ] Custom controls expose role, label, value, and action.
- [ ] Full keyboard navigation reaches every interactive element.
- [ ] Focus order is logical and has no traps.
- [ ] Tables and outline views expose row meaning and selection state.
- [ ] Dynamic content updates are communicated without announcement spam.
- [ ] States are not conveyed by color alone.
