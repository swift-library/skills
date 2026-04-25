# VoiceOver And Semantic Accessibility

Use this file for spoken feedback, semantic roles, reading order, grouping,
focus, announcements, and custom control behavior across SwiftUI, UIKit, and
AppKit.

## Baseline Rules

- Prefer native controls. A native button, toggle, text field, picker, slider,
  table, or sheet usually supplies role, focus, and interaction behavior.
- Add accessibility metadata only when the default semantics are missing,
  ambiguous, duplicated, or misleading.
- Use concise, context-independent labels. Do not include role words such as
  "button" or "image" when traits already provide the role.
- Use values for changing state, progress, selection, counts, dates, and
  quantities.
- Use hints sparingly. A hint should explain consequence or interaction only
  when label, value, and trait are insufficient.
- State belongs in traits or values, not labels. Prefer selected/disabled
  traits or values over labels such as "Selected photo".
- Decorative imagery should be hidden from assistive technologies. Meaningful
  imagery needs an equivalent label.
- Never hide an interactive element from accessibility.
- Localize labels, values, hints, action names, custom content, and
  announcements.

## Labels

Visible text controls generally do not need an explicit label. Examples:

- `Button("Save")` should keep its automatic label.
- `Toggle("Dark Mode", isOn: $enabled)` should keep its automatic label.
- `UIButton` with a clear localized title should keep its title-derived label.

Icon-only, image-only, or custom controls need labels:

```swift
Button {
    close()
} label: {
    Image(systemName: "xmark")
}
.accessibilityLabel("Close")
```

When generating a label from an icon name or inferred intent, mark it for human
verification if the project accepts code comments:

```swift
.accessibilityLabel("Share") // [VERIFY] Confirm the action label.
```

## Values And Traits

Use values for current state or data:

```swift
Text(progressTitle)
    .accessibilityValue("\(completed) of \(total) complete")
```

Use traits for role or state:

```swift
.accessibilityAddTraits(item.isSelected ? [.isSelected, .isButton] : .isButton)
```

Avoid overriding native semantics unless the default behavior is wrong. If a
custom view behaves like a button, expose button semantics and activation.

## Grouping

Group content when individual child stops are noisy or incomplete. Do not group
when users need to interact with children separately.

- Combine related static text that forms one idea.
- Contain groups when users need to navigate into the group.
- Ignore children only when the parent supplies complete label, value, traits,
  and actions.

Common cell pattern:

- A dense list row with title, subtitle, status, and one row action can often
  be one accessible element.
- A row with multiple independent controls should preserve separate controls.

## Actions

Expose non-obvious or hidden operations as accessibility actions. Swipe-only,
hover-only, drag-only, or gesture-only actions need accessible alternatives.

- SwiftUI: `.accessibilityAction`, `.accessibilityActions`, or
  `.accessibilityAdjustableAction`.
- UIKit: `UIAccessibilityCustomAction`.
- AppKit: `NSAccessibilityCustomAction` or action methods on the accessibility
  element.

Adjustable controls should support increment and decrement rather than forcing
users through precise drag gestures.

## Focus And Announcements

Move focus when the user's context changes substantially, such as navigation,
modal presentation, validation errors, or content replacing a loading state.

Use announcements for status changes that should not move focus. Avoid frequent
or repeated announcements during progress updates; they interrupt assistive
technology users.

Prefer focus movement over an announcement for form errors when the user needs
to act on a specific field.

## Reading Order

Reading order should match the user's mental model, not merely the source
order. Check visual order, grouping, navigation hierarchy, and focus loops.

Use ordering APIs sparingly:

- SwiftUI: `accessibilitySortPriority(_:)` or grouping.
- UIKit: `accessibilityElements`.
- AppKit: accessibility children and key view loop.

Prefer structural fixes over numeric priority when the hierarchy itself is
wrong.

## Anti-Patterns

- Adding `accessibilityLabel` to every native control.
- Labeling a button "Close button".
- Hiding interactive elements with `.accessibilityHidden(true)` or
  `isAccessibilityElement = false` without exposing an accessible alternative.
- Using a hint to compensate for an unclear label.
- Making a custom tappable view with only a tap gesture and no control
  semantics.
- Using `accessibilityIdentifier` as if it were a user-facing label.
