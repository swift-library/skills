# SwiftUI Accessibility Basics

Use this file only when ordinary SwiftUI implementation touches a small
accessibility-sensitive detail and the task has not become a dedicated
accessibility review.

## Out Of Scope

Dedicated accessibility work stays outside this skill:

- accessibility modifier design, grouping, custom actions, rotors, or custom
  control representation beyond a local edit
- Dynamic Type, custom fonts, `@ScaledMetric`, text clipping, reflow, or Larger
  Text reviews
- VoiceOver semantics, labels, values, hints, traits, and actions reviews
- display settings, Reduce Motion, Differentiate Without Color, Voice Control,
  Switch Control, Full Keyboard Access, or touch-target audits
- Accessibility Inspector, manual verification, audit output, WCAG, or App
  Store Accessibility Nutrition Labels

## Local Reminder

For an incidental SwiftUI source edit, at least preserve these basics:

- prefer native controls such as `Button`, `Toggle`, `Picker`, and `Slider`
- hide decorative images and label meaningful images
- give icon-only controls useful labels
- keep text Dynamic Type-friendly
- avoid color-only or motion-only meaning
