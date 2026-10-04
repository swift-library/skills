---
name: focus-engine-patterns
description: Use this skill for Apple platform focus management and focus movement patterns across SwiftUI, UIKit, AppKit, RealityKit, tvOS, iOS/iPadOS, watchOS, visionOS, and macOS, including Focus Engine APIs, @FocusState, focusable views, focus sections, focus guides, key view loops, Digital Crown focus, hover/focus coordination, focus restoration, styling, async focus updates, focus accessibility integration, and focus debugging. Do not use for visual design polish, general SwiftUI state/layout work, dedicated accessibility audits unrelated to UI focus, persistence, networking, package architecture, or repository documentation.
---

# Focus Engine Patterns

## Purpose

Guide Apple platform focus management, focus movement, and indirect-input
navigation across SwiftUI, UIKit, AppKit, RealityKit, and Apple platforms.
Use official Focus Engine terminology while covering related platform focus
systems such as SwiftUI `@FocusState`, AppKit key view loops, watchOS Digital
Crown focus, and visionOS hover/focus coordination.

## When To Use

- Reviewing or fixing focus movement, focus restoration, focus styling, or
  focus debugging.
- Implementing tvOS remote navigation, focus sections, focus guides, focusable
  custom views, or focus-aware layouts.
- Handling iPad keyboard/game-controller focus, focus groups, and hardware
  keyboard navigation.
- Handling watchOS Digital Crown focus and sequential focus behavior.
- Handling visionOS gaze, hover effects, RealityKit entity interaction, and
  keyboard/assistive focus.
- Handling macOS key view loops, first responder focus, focus rings, menu
  command focus values, Catalyst focus, panels, sheets, or multi-window focus.
- Coordinating focus with async data loads, navigation transitions, data
  reloads, animation, VoiceOver, Switch Control, or Full Keyboard Access.

## When Not To Use

- Do not use for visual polish, spacing, typography, color, or native UI
  design; visual design is out of scope.
- Do not use for general SwiftUI state, layout, navigation, performance, or
  source-level refactoring when focus is not the concrete issue; leave that to
  general SwiftUI implementation guidance.
- Do not use for dedicated accessibility audits where focus is only one part
  of VoiceOver, Voice Control, Switch Control, WCAG, or Nutrition Label work;
  full accessibility audits are out of scope.
- Do not use for SwiftData, Core Data, networking, package architecture,
  dependency replacement, or repository documentation.

## Inputs To Inspect

- Target platform, UI framework, deployment target, and input method:
  Siri Remote, keyboard, game controller, Digital Crown, gaze, pointer,
  VoiceOver, Switch Control, or Full Keyboard Access.
- SwiftUI focus state, `focusable`, focus sections/scopes, focused values, and
  search focus.
- UIKit focus environments, focus guides, collection/table focus delegates,
  focus update callbacks, and reload behavior.
- AppKit first responder, key view loop, focus rings, panels, sheets, menus,
  and focused values.
- RealityKit input target, collision, hover effect, gestures, and mixed
  SwiftUI/RealityKit surfaces.
- Async data loading, navigation transitions, layout geometry, scroll behavior,
  and focus restoration points.

## Workflow

1. Identify platform, framework, input method, and the broken focus behavior.
2. Check `references/anti-patterns.md` for high-risk focus breakage.
3. Load only the platform/framework references needed for the task. Open
   `references/_index.md` if routing is unclear.
4. Verify whether the issue is focusability, movement geometry/order, default
   focus, restoration, styling, async timing, accessibility integration, or
   debugging/testing.
5. Prefer platform-native focus APIs before custom state machines or manual
   scrolling.
6. Keep SwiftUI focus, UIKit focus, AppKit responder, and accessibility focus
   concepts distinct unless coordinating them deliberately.
7. Validate on the relevant device class where simulator behavior is known to
   differ, especially tvOS and visionOS focus/hover behavior.

## Reference Files To Consult

- `references/_index.md`: routing table and symptom mapping.
- `references/anti-patterns.md`: focus-breaking patterns across platforms.
- `references/swiftui-focus.md`: SwiftUI focus APIs, focused values, search
  focus, focus sections, default focus, and common pitfalls.
- `references/uikit-focus.md`: UIKit focus APIs and focus guides.
- `references/ios-focus.md`: iOS/iPadOS keyboard, focus groups, halo, game
  controller, pointer, and multi-window focus.
- `references/watchos-focus.md`: Digital Crown and sequential focus.
- `references/visionos-focus.md`: gaze, hover, keyboard focus, and spatial
  input.
- `references/realitykit-focus.md`: RealityKit entity hover and input target
  setup.
- `references/macos-focus.md`: key view loops, first responder, focus rings,
  focused values, Catalyst, panels, sheets, and multi-window focus.
- `references/layout-patterns.md`: tvOS/macOS layout patterns and focus
  section isolation.
- `references/focus-styling.md`: focus visual feedback and custom focus rings.
- `references/focus-restoration.md`: restoring focus after reloads,
  navigation, sheets, and async transitions.
- `references/async-focus.md`: main actor, deferred focus, cancellation,
  debouncing, and scroll feedback loops.
- `references/accessibility-focus.md`: coordination with
  `@AccessibilityFocusState`, VoiceOver, Switch Control, Full Keyboard Access,
  labels, order, and Reduce Motion.
- `references/debugging.md`: focus debugging, launch arguments, LLDB commands,
  focus tests, and first responder inspection.
## Decision Rules

- Repository-local truth wins over this skill.
- Focus is input navigation state, not visual design state.
- Do not add `.focusable()` to controls that are already focusable.
- Do not mix SwiftUI and UIKit focus APIs on the same hierarchy branch unless
  the bridge is explicit and tested.
- Treat VoiceOver focus and UI focus as separate systems; coordinate only when
  user context requires it.
- On tvOS, consider focus movement geometric and verify unreachable gaps,
  scroll feedback loops, disabled controls, lazy deallocation, and simulator
  differences.
- On macOS, reason through first responder, key view loop, focus ring, menu
  command state, and Full Keyboard Access.
- On visionOS, distinguish gaze targeting, hover effects, keyboard focus, and
  assistive focus.
- On watchOS, preserve Digital Crown routing and modifier order.
- Avoid broad focus rewrites when a focus guide, section, restoration point, or
  timing fix solves the concrete failure.

## Review Checklist

- Every intended interactive element can become focused by the target input
  method.
- Focus movement is predictable for the platform's navigation model.
- Default focus and restoration survive navigation, data reloads, and sheets.
- Focus styling is visible, consistent, and not confused with hover or
  accessibility focus.
- Async focus updates happen on the main actor after the target exists.
- Accessibility focus, UI focus, and keyboard focus are coordinated only where
  needed.
- Debugging or device validation is specified for platform-sensitive behavior.

## Output Format

For reviews, report findings first by severity with file and line references
when available. Include the violated focus rule, user-visible effect, and a
patch-ready before/after or concrete change.

For implementation work, summarize:

1. Focus surface changed
2. Platform/framework focus APIs affected
3. Accessibility or input-method impact
4. Validation performed
5. Remaining device checks or risks
