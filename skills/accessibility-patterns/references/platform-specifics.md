# Platform-Specific Accessibility

Use this file when accessibility behavior diverges from ordinary iOS SwiftUI or
UIKit patterns: macOS/AppKit, Mac Catalyst, watchOS, tvOS, visionOS, RealityKit,
or cross-platform conditional code.

## macOS And AppKit

macOS uses `NSAccessibility` for AppKit. Do not apply `UIAccessibility` APIs to
AppKit-only views.

SwiftUI on macOS handles many standard controls automatically, but AppKit
custom views need explicit roles, labels, values, and keyboard behavior.

Common macOS checks:

- every interactive element is reachable by keyboard
- focus rings remain visible
- custom controls expose `NSAccessibility.Role`
- tables and outline views expose row meaning and selection state
- popovers, panels, and custom modals have an escape path
- dynamic content changes use `NSAccessibility.post` only when meaningful

Common AppKit roles:

| Role | Use |
|---|---|
| `.button` | Clickable custom controls |
| `.checkBox` | Two-state toggles |
| `.radioButton` | Mutually exclusive options |
| `.textField` | Editable text |
| `.staticText` | Non-interactive text |
| `.slider` | Adjustable ranges |
| `.progressIndicator` | Progress or loading |
| `.table` / `.list` | Structured collections |
| `.group` | Semantic containers |
| `.toolbar` | Toolbar controls |
| `.window` | Window-level container |

Custom macOS actions should use the platform's accessibility custom action
surface or the action method expected by the role.

## Mac Catalyst

Mac Catalyst uses UIKit APIs while running on macOS. Most `UIAccessibility`
properties still apply, but test pointer, keyboard, hover, focus, and modal
behavior on Mac hardware or an appropriate simulator.

Watch for:

- pointer-only affordances
- modals that do not trap focus
- keyboard shortcuts conflicting with AppKit conventions
- custom hover state with no accessible equivalent

## watchOS

watchOS has a smaller screen and a different interaction model.

- VoiceOver navigation is based on watch gestures and the Digital Crown.
- Test larger text at watch-supported sizes, not only iOS assumptions.
- Adjustable controls should support `accessibilityAdjustableAction` and, when
  appropriate, Digital Crown interaction.
- Use WatchKit accessibility APIs for settings such as Reduce Motion when
  working in WatchKit.

For watch complications and widgets, make the visible content meaningful
without surrounding visual context.

## tvOS

tvOS is focus-driven. Every interactive element must be focusable and have a
clear focused state.

UIKit custom views need:

- `canBecomeFocused == true` where appropriate
- `didUpdateFocus(in:with:)` visual feedback
- `preferredFocusEnvironments` for default focus
- `UIFocusGuide` when directional navigation has gaps
- Menu button / Escape behavior for back or dismissal

SwiftUI buttons are focusable by default on tvOS. Use `.focusable()` for custom
interactive views and `.onMoveCommand` only when you need custom directional
navigation.

## visionOS

visionOS uses eye tracking, hand gestures, voice input, and VoiceOver. Standard
SwiftUI accessibility modifiers still apply.

For RealityKit content, provide accessibility metadata on entities when the 3D
content is meaningful or interactive:

```swift
var component = AccessibilityComponent()
component.label = "Spinning Globe"
component.value = "Currently rotating"
component.isAccessibilityElement = true
component.traits = [.button]
entity.components.set(component)
```

Interactive visionOS elements should have a hover effect and an accessible
alternative for look/pinch interactions.

## Cross-Platform Code

Use platform conditional code when the same view needs platform-specific hints,
input behavior, or accessibility APIs.

```swift
MyView()
    .accessibilityLabel("Chart")
#if os(macOS)
    .accessibilityHint("Press Space to toggle data view")
#elseif os(tvOS)
    .accessibilityHint("Press Select to expand")
#else
    .accessibilityHint("Double-tap to expand")
#endif
```

Do not hide platform differences behind a helper that makes the wrong API look
portable. Shared abstractions should expose semantic intent, then apply the
correct framework implementation at the edge.

## Common Mistakes

| Mistake | Platform | Fix |
|---|---|---|
| Using `UIAccessibility` in AppKit | macOS | Use `NSAccessibility` |
| Mouse-only custom control | macOS | Add keyboard and `NSAccessibility` action |
| No custom focus state | tvOS | Implement focusability and focus feedback |
| Assuming iOS gestures | watchOS | Test watch gestures and Digital Crown |
| Missing 3D metadata | visionOS | Add `AccessibilityComponent` |
| Hover-only affordance | macOS/visionOS | Add label, role, and activation path |
| Generic iOS hint text | tvOS/macOS | Use platform-appropriate input language |
