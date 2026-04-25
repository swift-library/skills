# Focus Engine Reference Index

## Core

- `anti-patterns.md`: focus-breaking patterns across platforms.
- `debugging.md`: focus debugging, LLDB commands, launch arguments, focus tests,
  and first responder inspection.
- `focus-restoration.md`: preserving and restoring focus after reloads,
  navigation, sheets, and async transitions.
- `async-focus.md`: main actor focus updates, deferred focus, cancellation,
  debouncing, and scroll feedback loops.
- `focus-styling.md`: focus visual feedback, focus rings, custom styling, and
  cleanup.

## Platform And Framework

- `swiftui-focus.md`: SwiftUI focus APIs, `@FocusState`, focused values,
  search focus, focus sections, default focus, move/exit commands, focusable
  views, hover effects, and common pitfalls.
- `uikit-focus.md`: UIKit focus environment, focus guides, focus update
  callbacks, and table/collection focus delegates.
- `ios-focus.md`: iOS/iPadOS keyboard focus, focus groups, halo effects,
  game controllers, pointer hover, and multi-window focus.
- `watchos-focus.md`: Digital Crown focus and sequential focus behavior.
- `visionos-focus.md`: gaze, hover, keyboard focus, and spatial input.
- `realitykit-focus.md`: RealityKit entity hover, input targets, collision,
  gestures, and mixed SwiftUI/RealityKit surfaces.
- `macos-focus.md`: key view loop, first responder, focus rings, focused
  values, Catalyst, panels, sheets, and multi-window focus.
- `layout-patterns.md`: tvOS/macOS layout patterns, focus section isolation,
  shelves, sidebars, split detail, and scroll edge handling.
- `accessibility-focus.md`: coordination with accessibility focus, VoiceOver,
  Switch Control, Full Keyboard Access, labels, order, and Reduce Motion.
- `licenses.md`: license file locations.

## Symptom Routing

- tvOS focus skips or cannot move across rows: `anti-patterns.md`,
  `layout-patterns.md`, `swiftui-focus.md`, or `uikit-focus.md`.
- Focus disappears after data reload or navigation: `focus-restoration.md` and
  `async-focus.md`.
- Custom view does not receive keyboard/delete/move commands:
  `swiftui-focus.md`, `ios-focus.md`, or `macos-focus.md`.
- iPad keyboard focus or controller behavior is wrong: `ios-focus.md`.
- Digital Crown input goes to the wrong control: `watchos-focus.md`.
- visionOS gaze/hover/focus behavior is confused: `visionos-focus.md` and
  `realitykit-focus.md`.
- macOS tab order, first responder, menu command, or focus ring issue:
  `macos-focus.md`.
- VoiceOver or Switch Control must coordinate with UI focus:
  `accessibility-focus.md`, then route full accessibility audits to
  `accessibility-patterns`.
