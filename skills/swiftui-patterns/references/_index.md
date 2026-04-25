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
- `focus-patterns.md`: route stub for SwiftUI focus knowledge owned by
  `focus-engine-patterns`.

## UI Quality

- `accessibility-patterns.md`: route stub for SwiftUI accessibility knowledge
  owned by `accessibility-patterns`.
- `text-patterns.md`: localized vs verbatim `Text`.
- `image-optimization.md`: `AsyncImage`, image decoding, downsampling, caching.
- `performance-patterns.md`: route stub for SwiftUI source-level performance
  knowledge owned by `swiftui-performance`.

## Motion

- `animation-basics.md`: implicit/explicit animations and animation placement.
- `animation-transitions.md`: transitions and `matchedGeometryEffect`.
- `animation-advanced.md`: transactions, phase/keyframe animations, newer APIs.

## Platform And Tools

- `liquid-glass.md`: iOS 26+ Liquid Glass and fallback patterns.
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
- App shell, TabView, NavigationStack, deep-link, or local sheet routing within
  established architecture: `app-wiring-and-routing.md`.
- Navigation path, sheet, or inspector issue: `sheet-navigation-patterns.md`.
- Dedicated SwiftUI view cleanup pass: `view-refactor.md`.
- Dedicated SwiftUI performance work: use `swiftui-performance`.
- Basic SwiftUI `@FocusState` issue: `focus-patterns.md`.
- tvOS remote focus, UIKit/AppKit focus, RealityKit hover/focus, Digital Crown
  focus, focus restoration, or focus debugging: use `focus-engine-patterns`.
- VoiceOver, Voice Control, Switch Control, Full Keyboard Access, Dynamic Type
  accessibility review, Accessibility Inspector, WCAG, or Nutrition Label
  issue: use `accessibility-patterns`.
- Small SwiftUI modifier cleanup for labels, grouping, traits, or image-only
  buttons while already doing SwiftUI source work: `accessibility-patterns.md`.
- Tap target, fixed frame, system control, or HIG-aligned layout issue:
  `layout-best-practices.md`.
- Animation runs unexpectedly or not at all: `animation-basics.md` or
  `animation-transitions.md`.
- Swift Charts API or accessibility issue: use `swift-charts-patterns`.
- Source-level high body updates, jank, memory growth, or performance work:
  use `swiftui-performance`. Use `performance-patterns.md` only for
  incidental notes during ordinary SwiftUI implementation.
- Instruments `.trace`, `xctrace`, hang, hitch, jank, or trace recording issue:
  use `xcode-instruments`.
- New API, deprecation, macOS scene, menu bar extra, or Liquid Glass
  API/fallback question:
  `latest-apis.md`, `macos-*.md`, or `liquid-glass.md`.
