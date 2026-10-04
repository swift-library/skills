# Reference Index

Use this index only when `SKILL.md` routing is not enough.

## Core SwiftUI

- `latest-apis.md`: deprecated API replacements and OS availability.
- `state-management.md`: `@State`, `@Binding`, Observation, environment, data
  flow.
- `view-structure.md`: subview extraction, `@ViewBuilder`, view identity,
  `AnyView`, representables.
- `view-refactor.md`: focused cleanup passes for long view bodies, subview
  extraction, action extraction, and stable view trees.
- `layout-best-practices.md`: adaptive layout, tap targets, system controls,
  GeometryReader alternatives, layout performance.

## Lists, Navigation, And Input

- `list-patterns.md`: `ForEach` identity, `List`, `Table`, inline filtering.
- `component-patterns.md`: controls, forms, searchable views, previews,
  grids, haptics, theming, loading placeholders, overlays, title/top bars,
  input toolbars, scroll-reveal affordances, media.
- `app-wiring-and-routing.md`: app shell, dependency injection boundaries,
  TabView, NavigationStack, deep links, and sheet routing when architecture is
  already established.
- `sheet-navigation-patterns.md`: sheets, navigation, split views, inspectors.
- `scroll-patterns.md`: `ScrollViewReader`, scroll position, scroll effects.
- `focus-patterns.md`: basic SwiftUI `@FocusState` reminders and the
  dedicated-focus boundary.

## UI Quality

- `accessibility-basics.md`: basic SwiftUI accessibility reminders and the
  dedicated-audit boundary.
- `text-patterns.md`: localized vs verbatim `Text`.
- `image-optimization.md`: `AsyncImage`, image decoding, downsampling, caching.
- `performance-patterns.md`: incidental SwiftUI performance reminders and the
  dedicated-performance boundary.

## Motion

- `animation-basics.md`: implicit/explicit animations and animation placement.
- `animation-transitions.md`: transitions and `matchedGeometryEffect`.
- `animation-advanced.md`: transactions, phase/keyframe animations, newer APIs.

## Platform And Tools

- `liquid-glass.md`: platform SDK 26+ Liquid Glass and fallback patterns.
- `macos-scenes.md`: macOS scenes, windows, settings, menu bar extras, and
  menu-bar-only utility rules.
- `macos-window-styling.md`: macOS window and toolbar styling.
- `macos-views.md`: macOS SwiftUI views, file APIs, AppKit interop.

## Symptom Routing

- `@State` not updating from parent: `state-management.md`.
- Large body or confusing view composition: `view-structure.md`.
- Layout instability or GeometryReader overuse: `layout-best-practices.md`.
- Rows jump, duplicate, or animate incorrectly: `list-patterns.md`.
- Toggle, slider, picker, form, searchable, grid, haptic, theming, preview,
  placeholder, toast, overlay, input toolbar, top bar, scroll-reveal, or media
  viewer basics:
  `component-patterns.md`.
- `Form`, `Section`, `LabeledContent`, `Label`, title-value rows, settings
  rows, inspector rows, or manual row replacement with native SwiftUI
  primitives:
  `component-patterns.md`, then `layout-best-practices.md`.
- Custom tactile patterns, AHAP files, synchronized audio-haptic feedback,
  advanced haptic players, or `CHHapticEngine` lifecycle: out of scope.
- App shell, TabView, NavigationStack, deep-link, or local sheet routing within
  established architecture: `app-wiring-and-routing.md`.
- Navigation path, sheet, or inspector issue: `sheet-navigation-patterns.md`.
- Dedicated SwiftUI view cleanup pass: `view-refactor.md`.
- Dedicated SwiftUI performance work: out of scope.
- Basic SwiftUI `@FocusState` issue: `focus-patterns.md`.
- tvOS remote focus, UIKit/AppKit focus, RealityKit hover/focus, Digital Crown
  focus, focus restoration, or focus debugging: out of scope.
- VoiceOver, Voice Control, Switch Control, Full Keyboard Access, Dynamic Type
  accessibility review, Accessibility Inspector, WCAG, or Nutrition Label
  issue: out of scope.
- Small SwiftUI modifier cleanup for labels, grouping, traits, or image-only
  buttons while already doing SwiftUI source work: `accessibility-basics.md`.
- Tap target, fixed frame, system control, or HIG-aligned layout issue:
  `layout-best-practices.md`.
- Animation runs unexpectedly or not at all: `animation-basics.md` or
  `animation-transitions.md`.
- Swift Charts API or accessibility issue: out of scope.
- Source-level high body updates, jank, memory growth, or performance work:
  out of scope. Use `performance-patterns.md` only for incidental notes during
  ordinary SwiftUI implementation.
- Instruments `.trace`, `xctrace`, hang, hitch, jank, or trace recording issue:
  out of scope.
- New API, deprecation, macOS scene, menu bar extra, or Liquid Glass
  API/fallback question:
  `latest-apis.md`, `macos-*.md`, or `liquid-glass.md`.
