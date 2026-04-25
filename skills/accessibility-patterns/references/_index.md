# Accessibility Reference Index

Use this index only when `SKILL.md` routing is not enough.

## Ownership

This skill owns dedicated Apple-platform accessibility implementation, review,
auditing, testing, and Nutrition Label work across SwiftUI, UIKit, and AppKit.
Pick framework files after identifying the UI stack, and pick topic files for
cross-framework concerns such as VoiceOver semantics, Dynamic Type, testing, or
media.

Keep chart-specific accessibility in `swift-charts-patterns` because chart
descriptors and Audio Graph are Swift Charts domain APIs. SwiftUI
accessibility knowledge lives here; `swiftui-patterns` may keep only a route
stub for incidental reminders during ordinary SwiftUI implementation.

## Core Topics

- `voiceover-semantics.md`: semantic labels, values, hints, traits, actions,
  grouping, focus, announcements, reading order, and custom controls.
- `display-text-input.md`: Dynamic Type, display settings, touch targets,
  Voice Control, Switch Control, Full Keyboard Access, and keyboard input.
- `dynamic-type.md`: Dynamic Type, custom fonts, scaled metrics, layout
  adaptation, and Large Content Viewer.
- `testing-and-auditing.md`: manual testing, Accessibility Inspector,
  automated audits, severity triage, and QA handoff.
- `manual-testing.md`: concrete device and simulator test steps.
- `nutrition-labels.md`: App Store Accessibility Nutrition Label
  recommendations and WCAG mapping boundaries.
- `wcag-mapping.md`: WCAG 2.2 A/AA mapping for Apple-platform findings.
- `media.md`: captions, audio descriptions, speech, media playback, Smart
  Invert, and chart-accessibility routing.
- `assistive-access.md`: Assistive Access support, scene setup, design rules,
  and testing.
- `platform-specifics.md`: macOS, Catalyst, watchOS, tvOS, visionOS, and
  cross-platform differences.
- `review-red-flags.md`: PR review red flags and P0/P1/P2 triage.
- `principles-sources-glossary.md`: principles, glossary, and source policy.

## Framework Files

- `swiftui.md`: SwiftUI accessibility modifiers, native controls, grouping,
  custom actions, focus, rotors, and custom control representation.
- `uikit.md`: UIKit `UIAccessibility` properties, containers, notifications,
  Dynamic Type, cells, custom controls, and hit testing.
- `appkit.md`: AppKit `NSAccessibility`, keyboard navigation, focus order,
  tables, outline views, custom controls, and announcements.

## Symptom Routing

- Icon-only button, unlabeled image, duplicated announcements, wrong trait, or
  custom control semantics: `voiceover-semantics.md`, then framework file.
- SwiftUI modifier, `Button`, `Image`, `accessibilityElement(children:)`,
  `accessibilityRepresentation`, `AccessibilityFocusState`, or rotor issue:
  `swiftui.md`.
- UIKit view controller, cell, custom `UIView`, `UIAccessibilityCustomAction`,
  notification, or `UIFontMetrics` issue: `uikit.md`.
- AppKit `NSView`, `NSButton`, `NSTableView`, `NSOutlineView`, focus ring, or
  `NSAccessibility` issue: `appkit.md`.
- Fixed font, clipped text, large content viewer, touch target, color-only
  state, Reduce Motion, Voice Control, Switch Control, or keyboard-only issue:
  `display-text-input.md`.
- Custom fonts, `@ScaledMetric`, `UIFontMetrics`, large text clipping, reflow,
  or Larger Text Nutrition Label issue: `dynamic-type.md`.
- Accessibility Inspector, XCUITest, `performAccessibilityAudit()`, manual
  device verification, or P0/P1/P2 audit output: `testing-and-auditing.md`.
- Concrete VoiceOver, Voice Control, Switch Control, keyboard, Dynamic Type, or
  display setting test steps: `manual-testing.md`.
- App Store Accessibility Nutrition Labels, common-task matrix, WCAG mapping,
  or accessibility metadata recommendation: `nutrition-labels.md`.
- WCAG 2.2 A/AA mapping, compliance language, or success-criterion-style
  explanation: `wcag-mapping.md`.
- Caption, subtitle, audio description, video, audio, speech, or image/video
  invert issue: `media.md`.
- Assistive Access, `AssistiveAccess` scene, `UISupportsAssistiveAccess`, or
  cognitive simplification issue: `assistive-access.md`.
- macOS/AppKit divergence, Mac Catalyst, watchOS, tvOS, visionOS, RealityKit,
  or cross-platform accessibility code: `platform-specifics.md`.
- PR review triage, noisy findings, speculative fixes, or severity calibration:
  `review-red-flags.md`.
- Need definitions, source policy, or high-level accessibility principles:
  `principles-sources-glossary.md`.
- Chart accessibility, `AXChartDescriptorRepresentable`, or Audio Graph issue:
  use `swift-charts-patterns`.
- General SwiftUI state, layout, navigation, or performance without a concrete
  accessibility issue: use `swiftui-patterns`.

## Optional Artifacts

- Need a reusable XCUITest audit starter: `templates/audit-template.swift`.
- Need a QA handoff checklist: `templates/qa-checklist.md`.
- Need before/after patch style examples: load the single matching file under
  `examples/`.
