---
name: accessibility-patterns
description: Use this skill for Apple-platform accessibility implementation, review, auditing, or modernization in SwiftUI, UIKit, AppKit, RealityKit, media, or Apple UI flows when work mentions accessibility, a11y, Assistive Access, VoiceOver, Voice Control, Switch Control, Full Keyboard Access, Dynamic Type, Larger Text, Reduce Motion, Increase Contrast, Differentiate Without Color, accessibility labels, values, hints, traits, actions, UIAccessibility, NSAccessibility, AccessibilityComponent, Accessibility Inspector, performAccessibilityAudit(), WCAG, or App Store Accessibility Nutrition Labels. Do not use for general Focus Engine behavior, tvOS remote focus, UIKit/AppKit focus systems, SwiftUI @FocusState without an accessibility goal, general SwiftUI layout, state, navigation, animation, performance, Swift Charts, visual design, persistence, networking, package architecture, or repository documentation unless accessibility is the concrete goal.
---

# Accessibility Patterns

## Purpose

Guide Apple-platform accessibility implementation, review, and auditing for
SwiftUI, UIKit, and AppKit. Focus on semantic accessibility, assistive
technology support, Dynamic Type, display settings, input alternatives,
manual verification, automated checks, and App Store Accessibility Nutrition
Label recommendations.

Do not assume every API comes from `import Accessibility`; many app UI APIs
live in SwiftUI, UIKit, or AppKit.

## When To Use

- Reviewing SwiftUI, UIKit, or AppKit code for accessibility defects.
- Fixing VoiceOver labels, values, hints, traits, grouping, focus, actions,
  rotors, announcements, or reading order.
- Checking Dynamic Type, Larger Text, custom fonts, text clipping, touch
  targets, Voice Control, Switch Control, or Full Keyboard Access support.
- Checking Reduce Motion, Reduce Transparency, Increase Contrast,
  Differentiate Without Color, Dark Interface, captions, or audio descriptions.
- Using Accessibility Inspector, Xcode accessibility audits, manual device
  testing, or accessibility QA checklists.
- Preparing an App Store Accessibility Nutrition Label recommendation or WCAG
  mapping for reviewed app flows.

## When Not To Use

- Do not use for general SwiftUI state, layout, navigation, animation, source
  performance, macOS windows, or Liquid Glass unless the issue is explicitly
  accessibility-related.
- Do not use for Swift Charts implementation or chart-specific accessibility
  descriptors.
- Do not use for visual design polish without an accessibility goal.
- Do not use for general Focus Engine behavior, tvOS remote focus, UIKit/AppKit
  focus systems, SwiftUI `@FocusState`, focus restoration, or focus debugging
  unless accessibility is the concrete goal.
- Do not use for SwiftData, Core Data, networking, package architecture,
  dependency replacement, or repository documentation.
- Do not present Nutrition Label or WCAG output as legal certification.

## Inputs To Inspect

- User request, code, screenshots, Accessibility Inspector output, audit
  results, crash/build logs, or QA notes.
- UI framework and platform: SwiftUI, UIKit, AppKit, mixed stack, Catalyst,
  iOS, iPadOS, macOS, tvOS, watchOS, or visionOS.
- Deployment target and API availability.
- Existing localization, design system, semantic colors, typography,
  component, test, and accessibility conventions.
- The specific user flow or common tasks being evaluated.

## Workflow

1. Read local project truth first: explicit user instructions, `AGENTS.md`,
   `README.md`, project settings, deployment target, and nearby UI patterns.
2. Identify the framework, platform, assistive technology or accessibility
   feature, and user impact before proposing a fix.
3. Classify the task: new implementation, existing-code fix, accessibility
   audit, Nutrition Label recommendation, or testing workflow.
4. Load one primary reference file that matches the task. Open
   `references/_index.md` only when routing is unclear.
5. Apply only project-compatible APIs. Gate availability-sensitive APIs with
   `#available` or preserve the existing lower-target pattern.
6. Prefer native controls, semantic text and color roles, system media
   controls, and platform accessibility APIs before custom alternatives.
7. Keep changes minimal and localized. Do not change product copy, layout, or
   architecture unless accessibility requires it.
8. Include manual verification steps for any accessibility-sensitive change.

## Reference Files To Consult

- `references/_index.md`: routing table for deeper references.
- `references/voiceover-semantics.md`: labels, values, hints, traits, actions,
  grouping, focus, announcements, and reading order.
- `references/swiftui.md`: SwiftUI accessibility modifiers and patterns.
- `references/uikit.md`: `UIAccessibility` patterns for UIKit.
- `references/appkit.md`: `NSAccessibility` patterns for AppKit.
- `references/display-text-input.md`: display settings, touch, keyboard,
  Voice Control, Switch Control, and Full Keyboard Access.
- `references/dynamic-type.md`: Dynamic Type, custom fonts, scaling, layout
  adaptation, and Large Content Viewer.
- `references/testing-and-auditing.md`: Accessibility Inspector, manual
  testing, XCUITest accessibility audits, and severity triage.
- `references/manual-testing.md`: device and simulator manual test steps by
  assistive technology.
- `references/nutrition-labels.md`: App Store Accessibility Nutrition Label
  recommendation workflow and WCAG mapping boundaries.
- `references/wcag-mapping.md`: WCAG 2.2 A/AA mapping for Apple-platform
  findings.
- `references/media.md`: captions, audio descriptions, speech, media, and the
  chart-accessibility boundary.
- `references/assistive-access.md`: Assistive Access app declarations, scenes,
  design rules, and testing.
- `references/platform-specifics.md`: macOS, Catalyst, watchOS, tvOS,
  visionOS, and cross-platform differences.
- `references/review-red-flags.md`: PR review red flags and severity triage.
- `references/principles-sources-glossary.md`: principles, glossary, and
  source policy.
## Examples And Templates

- `examples/before-after-swiftui.md`: SwiftUI patch examples. Read only when a
  SwiftUI before/after output shape is useful.
- `examples/before-after-uikit.md`: UIKit patch examples. Read only when a
  UIKit before/after output shape is useful.
- `examples/before-after-appkit.md`: AppKit patch examples. Read only when an
  AppKit before/after output shape is useful.
- `templates/audit-template.swift`: XCUITest accessibility audit starter. Use
  only when the user asks for a reusable test file.
- `templates/qa-checklist.md`: manual QA handoff checklist. Use only when the
  user asks for a checklist, QA handoff, or repeatable manual verification
  artifact.

## Decision Rules

- Repository-local truth wins over this skill.
- Accessibility is user-experience work, not only static linting. Explain
  assumptions and tradeoffs when multiple fixes are reasonable.
- Do not add redundant labels to native controls that already expose correct
  visible text.
- Do not put role words such as "button" in labels when the trait already
  supplies the role.
- Do not hide interactive elements from accessibility.
- Localize accessibility labels, values, hints, action names, announcements,
  and custom content according to the project's localization strategy.
- Treat `accessibilityIdentifier` as a UI-test hook, not a VoiceOver label.
- Prefer manual testing with assistive technologies alongside automated checks.
- For App Store Nutrition Labels, evaluate complete common tasks per device
  and report recommendations, not guarantees.

## Output Format

For reviews or audits, return:

1. Phase / stage judgment
2. Accessibility surface inspected
3. Findings grouped by P0 / P1 / P2
4. Patch-ready recommended changes
5. Compatibility / availability impact
6. Validation performed or required
7. Risks
8. Next steps

For code changes, summarize:

1. Accessibility surface changed
2. Patterns applied
3. Compatibility / availability impact
4. Verification performed
5. Remaining manual checks

For Nutrition Label work, return:

1. Scope and common tasks reviewed
2. Labels that can be recommended
3. Labels that should not be recommended
4. Evidence and blockers
5. Required device / flow verification

## Failure / Uncertainty Handling

- If framework, platform, deployment target, or user flow is unknown, state the
  assumption and avoid availability-sensitive claims.
- If a fix needs product copy or design-system changes, identify the dependency
  instead of silently rewriting the UI.
- If a task requires chart-specific descriptors, source-level SwiftUI
  architecture, or visual redesign, state that part is out of scope.
