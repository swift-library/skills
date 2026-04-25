# SwiftUI Accessibility Route

SwiftUI accessibility knowledge belongs to `accessibility-patterns`.

Use this route only when ordinary SwiftUI implementation touches a small
accessibility-sensitive detail and the task has not become a dedicated
accessibility review.

## Route

- SwiftUI accessibility modifiers, native controls, grouping, custom actions,
  focus, rotors, or custom control representation:
  `../accessibility-patterns/references/swiftui.md`
- Dynamic Type, custom fonts, `@ScaledMetric`, text clipping, reflow, or Larger
  Text behavior:
  `../accessibility-patterns/references/dynamic-type.md`
- VoiceOver semantics, labels, values, hints, traits, and actions:
  `../accessibility-patterns/references/voiceover-semantics.md`
- Display settings, Reduce Motion, Differentiate Without Color, Voice Control,
  Switch Control, Full Keyboard Access, or touch targets:
  `../accessibility-patterns/references/display-text-input.md`
- Accessibility Inspector, manual verification, audit output, WCAG, or App
  Store Accessibility Nutrition Labels:
  use the `accessibility-patterns` skill.

## Local Reminder

For an incidental SwiftUI source edit, at least preserve these basics:

- prefer native controls such as `Button`, `Toggle`, `Picker`, and `Slider`
- hide decorative images and label meaningful images
- give icon-only controls useful labels
- keep text Dynamic Type-friendly
- avoid color-only or motion-only meaning
